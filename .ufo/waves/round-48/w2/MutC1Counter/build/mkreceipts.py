#!/usr/bin/env python3
"""Build the seat's receipt files from the run logs under the scratch root.

  matrix.tsv   one row per cell: counter, tool, verdict, the five clause tallies, selftest, readonly,
               verbatim final line
  own.tsv      per cell, failing fixture ids BEYOND the frozen `reference` control's baseline (that control
               is the frozen corpus's own "does the work" tool, and it fails 7 warm + 14 explain fixtures
               on the final set; a control's own rule shows up as the delta, not the raw count)
  finals.txt   the verbatim final line per cell, as measured
"""
import glob
import os
import re
import sys

S = "/fast/scratch/hyaku/mado-r48/MutC1Counter"
OUT = os.path.join(S, "receipts")
FIN = re.compile(r"^(PRED-C1-r48: .*)$", re.M)
FAILF = re.compile(r"clause=(f|w) fixture=(\S+) (?:class=\S+ state=\S+ )?FAIL")
FAILX = re.compile(r"clause=x fixture=(\S+) FAIL")
SETUP = re.compile(r"^PRED-C1-r48: SETUP (.*)$", re.M)


def parse(path):
    text = open(path, encoding="utf-8", errors="surrogateescape").read()
    m = FIN.search(text)
    fails = {"f": set(), "w": set(), "x": set()}
    for mm in FAILF.finditer(text):
        fails[mm.group(1)].add(mm.group(2))
    for mm in FAILX.finditer(text):
        fails["x"].add(mm.group(1))
    return text, (m.group(1) if m else ""), fails, (SETUP.search(text).group(1) if SETUP.search(text) else "")


def main():
    os.makedirs(OUT, exist_ok=True)
    cells = {}
    for p in sorted(glob.glob(os.path.join(S, "out", "*.log"))):
        cell = os.path.basename(p)[:-4]
        text, final, fails, setup = parse(p)
        cells[cell] = (final, fails, setup, os.path.basename(p))
    base = cells.get("p0-reference", ("", {"f": set(), "w": set(), "x": set()}, "", ""))[1]
    with open(os.path.join(OUT, "matrix.tsv"), "w") as mf, \
         open(os.path.join(OUT, "own.tsv"), "w") as of, \
         open(os.path.join(OUT, "finals.txt"), "w") as ff:
        of.write("cell\tf_own\tw_own\tx_own\tw_own_ids\tx_own_ids\n")
        for cell in sorted(cells):
            final, fails, setup, log = cells[cell]
            mf.write("%s\t%s\t%s\n" % (cell, log, final or ("SETUP: " + setup)))
            if not final:
                of.write("%s\t-\t-\t-\tSETUP:%s\t\n" % (cell, setup))
                continue
            own = {k: sorted(fails[k] - base[k]) for k in fails}
            of.write("%s\t%d\t%d\t%d\t%s\t%s\n" % (
                cell, len(own["f"]), len(own["w"]), len(own["x"]),
                ",".join(own["w"]), ",".join(own["x"])))
            ff.write("### %s\n%s\n" % (cell, final))
    # largest file in the seat scratch, for the write-bound record
    big = ("", 0)
    for d, _ds, fs in os.walk(S):
        for f in fs:
            p = os.path.join(d, f)
            try:
                n = os.path.getsize(p)
            except OSError:
                continue
            if n > big[1]:
                big = (p, n)
    print("largest file under scratch: %s %d bytes" % big)
    tot = sum(os.path.getsize(os.path.join(d, f)) for d, _ds, fs in os.walk(S) for f in fs
              if os.path.exists(os.path.join(d, f)))
    print("scratch total: %d bytes" % tot)


if __name__ == "__main__":
    sys.exit(main())
