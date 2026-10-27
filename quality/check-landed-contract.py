#!/usr/bin/env python3
"""QUALITY 96 - a landed contract is not narrower than, nor silently different from, the frozen reference.

L1 revision (round 48, attempt 3) of the w1 draft `.ufo/waves/round-48/w1/ScrMistakes/check96.py`, after w2:
`w2/ScoutQualityCriteria` D1 (the draft errored rc 2 on the round's own tool: its docstring says `Out of contract:`
and ends `Where detected`, the draft read only `Also out of contract:` ... `On these the tool`) and D2/CritMistakes
(a class deleted from the list passed: the scored contract then no longer describes the artifact either).

Reads the out-of-contract list of the frozen reference (at --frozen-rev) and of the landed file: the text after
`Also out of contract:` or `Out of contract:` up to `On these the tool`, `Where detected` or the end of the docstring;
split at top-level `;` when the list uses them, else at top-level commas. Every delta item - ADDED (a new refused
class: the contract narrowed) or REMOVED (a class the list no longer names) - must be registered: --registered names
a file (an appended erratum, a re-registration) that carries the item's first three words. Prints one line per delta
and `CHECK96: frozen= landed= added= removed= unregistered= verdict=OK|NARROWED|UNDECLARED`.
Exit 0 = every delta registered, 1 = an unregistered delta, 2 = input unreadable or no list.
Usage: check-landed-contract.py --repo . --frozen-rev REV --frozen <path-in-repo> --landed <path-on-disk>
       [--registered <file>]
"""
import argparse
import re
import subprocess
import sys

HEAD_RE = re.compile(r"(?:Also out of contract|Out of contract):(.*?)(?:On these the tool|Where detected|\"\"\"|\Z)",
                     re.S)


def items(text):
    m = HEAD_RE.search(text)
    if not m:
        return None
    body = re.sub(r"\s+", " ", m.group(1)).strip().rstrip(".")
    sep = ";" if ";" in body else ","
    out, depth, cur = [], 0, ""
    for ch in body:
        depth += (ch == "(") - (ch == ")")
        if ch == sep and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [re.sub(r"^and\s+", "", re.sub(r"\s+", " ", i).strip()) for i in out if i.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--frozen-rev", required=True)
    ap.add_argument("--frozen", required=True)
    ap.add_argument("--landed", required=True)
    ap.add_argument("--registered", default=None)
    a = ap.parse_args()
    r = subprocess.run(["git", "-C", a.repo, "show", "%s:%s" % (a.frozen_rev, a.frozen)], capture_output=True,
                       text=True, errors="replace")
    if r.returncode:
        print("FROZEN-ABSENT %s at %s" % (a.frozen, a.frozen_rev))
        return 2
    frozen = items(r.stdout)
    try:
        landed = items(open(a.landed, encoding="utf-8", errors="replace").read())
    except OSError as exc:
        print("LANDED-UNREADABLE %s (%s)" % (a.landed, exc))
        return 2
    if frozen is None or landed is None:
        print("NO-LIST frozen=%s landed=%s" % (frozen is not None, landed is not None))
        return 2
    reg = ""
    if a.registered:
        try:
            reg = re.sub(r"\s+", " ", open(a.registered, encoding="utf-8", errors="replace").read()).lower()
        except OSError as exc:
            print("REGISTERED-UNREADABLE %s (%s)" % (a.registered, exc))
            return 2
    added = [i for i in landed if i not in set(frozen)]
    removed = [i for i in frozen if i not in set(landed)]
    unreg_a = unreg_r = 0
    for kind, lst in (("ADDED", added), ("REMOVED", removed)):
        for i in lst:
            ok = bool(reg) and " ".join(i.lower().split()[:3]) in reg
            print("%s-%s %s" % (kind, "REGISTERED" if ok else "UNREGISTERED", i))
            if not ok:
                unreg_a += kind == "ADDED"
                unreg_r += kind == "REMOVED"
    verdict = "NARROWED" if unreg_a else ("UNDECLARED" if unreg_r else "OK")
    print("CHECK96: frozen=%d landed=%d added=%d removed=%d unregistered=%d verdict=%s"
          % (len(frozen), len(landed), len(added), len(removed), unreg_a + unreg_r, verdict))
    return 0 if verdict == "OK" else 1


if __name__ == "__main__":
    sys.exit(main())
