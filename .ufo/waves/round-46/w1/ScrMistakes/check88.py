#!/usr/bin/env python3
"""Check 88 (proposed): every forgery a shape counter admits is either declared in the counter's docstring or
killed by a committed tightening candidate, and the positive control passes every candidate.

Inputs are the two receipts an attack seat already writes:
  --forge   lines `<LABEL>\t<digest>\t<rev>\tPRED-...: admitted=1/1|0/1 verdict=...`
  --tighten lines `<rev12> A=1 B=1 ... PASS|FAIL` (the candidate matrix)
  --declared comma-separated labels the counter's docstring already declares as residuals
Rules: (1) the positive revision's tighten line reads PASS with every check = 1; (2) every admitted, undeclared
forgery revision has a tighten line with FAIL; (3) no admitted, undeclared forgery's line reads PASS.
Exit 0 iff all hold, 1 otherwise, 2 on an unreadable input."""
import argparse
import re
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forge", required=True)
    ap.add_argument("--tighten", required=True)
    ap.add_argument("--positive-rev", required=True)
    ap.add_argument("--declared", default="")
    a = ap.parse_args()
    declared = {s.strip() for s in a.declared.split(",") if s.strip()}
    try:
        forge = open(a.forge, encoding="utf-8").read().splitlines()
        tight = open(a.tighten, encoding="utf-8").read().splitlines()
    except OSError as e:
        print("CHECK88: verdict=SETUP_ERROR %s" % e)
        return 2
    pos = a.positive_rev[:12]
    admitted = {}
    for l in forge:
        m = re.match(r"^(F\S*|\S+)\t\S+\t(\w{6,})\t.*admitted=1/1", l)
        if m and m.group(1) != "applied":
            admitted[m.group(2)[:12]] = m.group(1)
    matrix = {}
    for l in tight:
        m = re.match(r"^(\w{6,})\s+(.*?)(PASS|FAIL)\s*$", l.strip())
        if m:
            matrix[m.group(1)[:12]] = (dict(re.findall(r"([A-Z])=(\d)", m.group(2))), m.group(3))
    undeclared = {r: n for r, n in admitted.items() if r != pos and n not in declared}
    problems = []
    if pos not in matrix:
        problems.append("positive_line=absent(%s)" % pos)
    elif matrix[pos][1] != "PASS" or any(v != "1" for v in matrix[pos][0].values()):
        problems.append("positive_line=%s" % matrix[pos][1])
    uncovered = sorted(n for r, n in undeclared.items() if r not in matrix)
    passing = sorted(n for r, n in undeclared.items() if r in matrix and matrix[r][1] == "PASS")
    if uncovered:
        problems.append("admitted_uncovered=%s" % ",".join(uncovered))
    if passing:
        problems.append("admitted_passing=%s" % ",".join(passing))
    print("CHECK88: admitted=%d declared=%d undeclared=%d tightened=%d positive=%s" % (
        len(admitted), len(admitted) - len(undeclared), len(undeclared), len(matrix),
        matrix.get(pos, ("", "absent"))[1]))
    if problems:
        print("CHECK88: verdict=FAIL " + " ".join(problems))
        return 1
    print("CHECK88: verdict=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
