#!/usr/bin/env python3
"""check72 - a mutant counted as a control is scored below target, or its equivalence is declared
with the site that preserves the property named (QUALITY criterion 72).

A mutation is only a control if the patched tool actually differs in behaviour. When the same
property is enforced at two sites (a bounded read *and* a post-check on the length), removing one
site leaves the other enforcing it: the mutant is equivalent and scores at target. Such a mutant is
either repaired (the patch removes every site) or declared equivalent with the surviving site, or
the measurement that proves the equivalence, named in the declaration's comment block.

Usage:
  check72.py --repo . --rev <REV> --controls <path-in-repo> --receipt <path-in-repo>
  check72.py --repo . --rev <REV> --controls <disk> --receipt <disk> --files
Exit 0 = PASS, 1 = FAIL, 2 = inputs unreadable.
"""
import argparse
import os
import re
import subprocess
import sys

MUTANT_TUPLE = re.compile(r'\(\s*"((?:M|N|X|Y)\d[0-9A-Za-z_-]*)"\s*,')
MUTANT_CALL = re.compile(r'mut\(\s*"((?:M|N|X|Y)\d[0-9A-Za-z_-]*)"')
DECLARED = re.compile(r'#\s*((?:M|N|X|Y)\d[0-9A-Za-z_-]*)\b[^\n]*\bequivalent\b[^\n]*')
TARGET = re.compile(r'fixtures=(\d+)/\1\b|admitted=1/1\b')
CONTROL = re.compile(r'^control=(\S+)')
FIELD = re.compile(r'(expected|observed|verdict)=(\S+)')
RECEIPT_REF = re.compile(r'(receipts/[A-Za-z0-9_./-]*[A-Za-z0-9])')
SITE = re.compile(r'\b[A-Za-z_][A-Za-z0-9_]*\(\)|`:[0-9]+`')


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True)


def read(repo, rev, path, files):
    if files:
        return open(path, encoding="utf-8", errors="replace").read()
    r = git(repo, "show", "%s:%s" % (rev, path))
    return r.stdout if r.returncode == 0 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--controls", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--files", action="store_true", help="read both inputs from disk")
    a = ap.parse_args()

    src = read(a.repo, a.rev, a.controls, a.files)
    rec = read(a.repo, a.rev, a.receipt, a.files)
    if src is None or rec is None:
        print("MISSING-INPUT controls=%s receipt=%s at %s" % (a.controls, a.receipt, a.rev))
        return 2

    names = sorted(set(MUTANT_TUPLE.findall(src)) | set(MUTANT_CALL.findall(src)))
    rows = {}
    for line in rec.splitlines():
        m = CONTROL.match(line)
        if not m:
            continue
        rows[m.group(1)] = dict(FIELD.findall(line[m.end():]))

    def reached_target(name, fields):
        if fields.get("verdict") == "TARGET_MET":
            return True
        if fields.get("verdict"):
            return False
        return bool(TARGET.search(fields.get("observed", ""))) and not name.startswith(
            ("REF-", "P-"))

    bad = 0
    for name in names:
        if name not in rows:
            print("UNSCORED %s: named as a control, no receipt row" % name)
            bad += 1

    for name, fields in rows.items():
        if name.startswith(("REF-", "P-")):
            continue
        if reached_target(name, fields):
            print("SURVIVOR %s: scored at target - equivalent mutant counted as a control"
                  % name)
            bad += 1

    for name, fields in rows.items():
        if name.startswith("REF-") and not reached_target(name, fields):
            print("REF-BROKEN %s: the reference must reach target, read %s"
                  % (name, fields.get("observed", "?")))
            bad += 1
        if name.startswith(("BASE-", "CHEAT-")) and reached_target(name, fields):
            print("FLOOR-BROKEN %s: a floor/cheat control reached target" % name)
            bad += 1

    round_dir = os.path.dirname(os.path.dirname(a.controls)) + "/"
    declared = []
    lines = src.splitlines()
    for i, line in enumerate(lines):
        m = DECLARED.search(line)
        if not m:
            continue
        name = m.group(1)
        declared.append(name)
        lo = hi = i
        while lo > 0 and lines[lo - 1].lstrip().startswith("#"):
            lo -= 1
        while hi + 1 < len(lines) and lines[hi + 1].lstrip().startswith("#"):
            hi += 1
        block = "\n".join(lines[lo:hi + 1])
        cites = RECEIPT_REF.findall(block)
        sites = SITE.findall(block)
        if cites:
            for c in cites:
                if a.files:
                    if not os.path.exists(os.path.join(a.repo, round_dir, c)):
                        print("EQUIV-UNCITED %s: %s absent" % (name, c))
                        bad += 1
                elif git(a.repo, "cat-file", "-e",
                        "%s:%s%s" % (a.rev, round_dir, c)).returncode:
                    print("EQUIV-UNCITED %s: %s absent at %s" % (name, c, a.rev))
                    bad += 1
        elif not sites:
            print("EQUIV-UNARGUED %s: declared equivalent with neither a receipt nor a code site"
                  % name)
            bad += 1
        else:
            print("EQUIV-DECLARED %s via site %s" % (name, ", ".join(sites)))

    print("CONTROLS %d mutants, receipt rows %d, equivalence declarations %d"
          % (len(names), len(rows), len(declared)))
    if bad:
        print("FAIL %d defect(s)" % bad)
        return 1
    print("PASS every control is scored below target or declares its equivalence")
    return 0


if __name__ == "__main__":
    sys.exit(main())
