#!/usr/bin/env python3
"""check96 - a landed contract is not narrower than the frozen reference it was registered against.

QUALITY criterion 96 (draft, round 48). A round freezes a tool's contract (a docstring, a
registration paragraph) before wave w1 and delivers the tool after it. The delivered tool may
model more of the reference than the freeze did, but a *refused* input class that the frozen
reference does not name is a narrowed contract: the predicate the round is scored against no
longer covers what the artifact does, and a later reader cannot tell whether the refusal is a
modelled behaviour or an omission.

The check reads the out-of-contract item list of the frozen reference (`Also out of contract:`
up to `On these the tool`) and of the landed file, splits each list at top-level commas, and
prints the items the landed file adds. An added item is exempt only when `--registered` names a
file (an appended erratum or a re-freeze) that carries the item's first three words.

Usage:
  check96.py --repo . --frozen-rev REV --frozen <path-in-repo> --landed <path-on-disk>
             [--registered <file-on-disk>]
Exit 0 = no unregistered addition, 1 = NARROWED, 2 = input unreadable.
"""
import argparse
import re
import subprocess
import sys


def git_show(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                          capture_output=True, text=True, errors="replace")


def items(text):
    m = re.search(r"Also out of contract:(.*?)(?:On these the tool|\Z)", text, re.S)
    if not m:
        return None
    body = re.sub(r"\s+", " ", m.group(1)).strip().rstrip(".")
    body = re.sub(r"^and\s+", "", body)
    out, depth, cur = [], 0, ""
    for ch in body:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [re.sub(r"\s+", " ", i).strip() for i in out if i.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--frozen-rev", required=True)
    ap.add_argument("--frozen", required=True, help="path of the frozen reference inside --repo")
    ap.add_argument("--landed", required=True, help="path of the delivered file on disk")
    ap.add_argument("--registered", default=None,
                    help="file that registers the delta (erratum or re-freeze)")
    a = ap.parse_args()

    r = git_show(a.repo, a.frozen_rev, a.frozen)
    if r.returncode:
        print("FROZEN-ABSENT %s at %s" % (a.frozen, a.frozen_rev))
        return 2
    frozen = items(r.stdout)
    if frozen is None:
        print("FROZEN-NO-LIST %s carries no 'Also out of contract' list" % a.frozen)
        return 2
    try:
        landed_text = open(a.landed, encoding="utf-8", errors="replace").read()
    except OSError as exc:
        print("LANDED-UNREADABLE %s (%s)" % (a.landed, exc))
        return 2
    landed = items(landed_text)
    if landed is None:
        print("LANDED-NO-LIST %s carries no 'Also out of contract' list" % a.landed)
        return 2

    fset, lset = set(frozen), set(landed)
    added = [i for i in landed if i not in fset]
    removed = [i for i in frozen if i not in lset]
    reg = ""
    if a.registered:
        try:
            reg = re.sub(r"\s+", " ", open(a.registered, encoding="utf-8",
                                           errors="replace").read()).lower()
        except OSError as exc:
            print("REGISTERED-UNREADABLE %s (%s)" % (a.registered, exc))
            return 2

    unregistered = 0
    for i in added:
        head = " ".join(i.lower().split()[:3])
        if reg and head in reg:
            print("ADDED-REGISTERED %s" % i)
        else:
            unregistered += 1
            print("ADDED-UNREGISTERED %s" % i)
    for i in removed:
        print("REMOVED %s" % i)

    print("CHECK96: frozen=%d landed=%d added=%d unregistered=%d removed=%d verdict=%s"
          % (len(frozen), len(landed), len(added), unregistered, len(removed),
             "NARROWED" if unregistered else "OK"))
    return 1 if unregistered else 0


if __name__ == "__main__":
    sys.exit(main())
