#!/usr/bin/env python3
"""Check 87 (proposed): a control battery's receipt is complete - every declared control scored, and a final
verdict line exists. A battery that aborts on its own precondition prints neither, so a truncated receipt is
the observable of "no control evidence".

Usage: check87.py --receipt FILE --controls N [--prefix CTL_C2]
Rules: (1) a `controls=<n>` header equals N; (2) exactly N distinct `<PREFIX> <NAME> want=` lines;
(3) a final `<PREFIX> VERDICT: PASS|FAIL` line; (4) N `ok`/`WRONG` marks.
Exit 0 iff all four hold, 1 otherwise, 2 on an unreadable receipt."""
import argparse
import re
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--controls", type=int, required=True)
    ap.add_argument("--prefix", default="CTL_C2")
    a = ap.parse_args()
    try:
        lines = open(a.receipt, encoding="utf-8").read().splitlines()
    except OSError as e:
        print("CHECK87: verdict=SETUP_ERROR %s" % e)
        return 2
    p = re.escape(a.prefix)
    hdr = [int(m.group(1)) for l in lines for m in [re.search(r"controls=(\d+)", l)] if m]
    rows = [m.group(1) for l in lines for m in [re.match(r"^%s (\S+) want=" % p, l)] if m]
    verdict = [l for l in lines if re.match(r"^%s VERDICT: (PASS|FAIL)" % p, l)]
    marks = sum(1 for l in lines if re.search(r"\b(ok|WRONG)\b", l) and re.match(r"^%s \S+ want=" % p, l))
    problems = []
    if not hdr or hdr[0] != a.controls:
        problems.append("header=%s want=%d" % (hdr[:1] or "absent", a.controls))
    if len(rows) != a.controls:
        problems.append("scored=%d want=%d" % (len(rows), a.controls))
    if len(set(rows)) != len(rows):
        problems.append("duplicate_names=%d" % (len(rows) - len(set(rows))))
    if not verdict:
        problems.append("verdict_line=absent")
    if marks != a.controls:
        problems.append("marks=%d want=%d" % (marks, a.controls))
    print("CHECK87: receipt=%s controls=%d scored=%d distinct=%d verdict=%s marks=%d" % (
        a.receipt, a.controls, len(rows), len(set(rows)), "present" if verdict else "absent", marks))
    if problems:
        print("CHECK87: verdict=FAIL " + " ".join(problems))
        return 1
    print("CHECK87: verdict=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
