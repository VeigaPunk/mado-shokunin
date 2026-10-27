#!/usr/bin/env python3
"""Aggregate one counter-run log into one matrix row: verdict, clause tallies, failing fixture ids.

Usage: agg.py LOG [LOG ...]   -> prints TSV: cell verdict cold warm explained generated selftest readonly tool
                                  then per-clause failing ids (truncated lists kept in full in the file).
Reads only the log files under the seat scratch root.
"""
import glob
import os
import re
import sys

S = "/fast/scratch/hyaku/mado-r48/MutC1Counter"
FIN = re.compile(r"PRED-C1-r48: cold=(\d+)/(\d+) warm=(\d+)/(\d+) explained=(\d+)/(\d+) "
                 r"generated=(\d+)/(\d+) selftest=(\w+) readonly=(\w+) tool=(\w+) verdict=(\w+)")
FAIL = re.compile(r"PRED-C1-r48 clause=(f|w) fixture=(\S+) (?:class=\S+ state=\S+ )?FAIL")
XFAIL = re.compile(r"PRED-C1-r48 clause=x fixture=(\S+) FAIL")
SETUP = re.compile(r"PRED-C1-r48: SETUP (.*)")


def row(path):
    cell = os.path.basename(path)[:-4]
    text = open(path, encoding="utf-8", errors="surrogateescape").read()
    m = FIN.search(text)
    fails = {"f": [], "w": [], "x": []}
    for mm in FAIL.finditer(text):
        fails[mm.group(1)].append(mm.group(2))
    for mm in XFAIL.finditer(text):
        fails["x"].append(mm.group(1))
    setup = SETUP.search(text)
    if not m:
        return "%s\tSETUP-OR-NO-VERDICT\t%s" % (cell, (setup.group(1) if setup else text.strip().splitlines()[-1:]))
    g = m.groups()
    notes = []
    if setup:
        notes.append("setup=" + setup.group(1)[:120])
    return "\t".join([cell, g[11], "%s/%s" % (g[0], g[1]), "%s/%s" % (g[2], g[3]), "%s/%s" % (g[4], g[5]),
                      "%s/%s" % (g[6], g[7]), g[8], g[9], g[10],
                      "f_fail=%d:%s" % (len(fails["f"]), ",".join(fails["f"][:8])),
                      "w_fail=%d:%s" % (len(fails["w"]), ",".join(fails["w"][:8])),
                      "x_fail=%d:%s" % (len(fails["x"]), ",".join(fails["x"][:8])),
                      " ".join(notes)])


def main():
    paths = sys.argv[1:] or sorted(glob.glob(os.path.join(S, "out", "*.log")))
    print("\t".join(["cell", "verdict", "cold", "warm", "explained", "generated", "selftest", "readonly",
                     "tool", "failing", "failing", "failing", "notes"]))
    for p in paths:
        print(row(p))


if __name__ == "__main__":
    main()
