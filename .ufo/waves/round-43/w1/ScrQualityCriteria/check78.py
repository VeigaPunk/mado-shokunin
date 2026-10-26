#!/usr/bin/env python3
"""check78.py - one control tally, stated once with its definition.

Reads a control-receipt of the CTL_C1 shape and, optionally, the prose line that
quotes it.  The receipt's own denominator is recomputed from its rows, every
number the claim repeats is compared to the row counts, and a disagreement is a
defect of the claim, not of the receipt.

Definitions used (and printed):
  rows       every line matching `^ok  <NAME>`
  anchors    NAME == REF, or NAME starting with BASE
  controls   rows - anchors           (the runner's own definition, `len(jobs) - 2`)
  M/D/K      single-defect mutants / do-nothing tools / cheats, by NAME prefix
  verdict_of the denominator of `controls scoring TARGET_MET: 0 of <n>`

Exit 0 when every number agrees, 1 on a mismatch, 2 on usage/IO errors.

Usage: python3 -I check78.py --receipt R [--claim FILE]
"""
import argparse
import re
import sys


def rows_of(path):
    out = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = re.match(r"^ok  (\S+)", line)
            if m:
                out.append(m.group(1))
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--claim")
    a = ap.parse_args(argv)

    try:
        rows = rows_of(a.receipt)
        text = open(a.receipt, encoding="utf-8", errors="replace").read()
    except OSError as e:
        print("SETUP_ERROR %s" % e)
        return 2
    if not rows:
        print("SETUP_ERROR no `ok  <NAME>` rows in %s" % a.receipt)
        return 2

    anchors = [n for n in rows if n == "REF" or n.startswith("BASE")]
    controls = len(rows) - len(anchors)
    count = lambda p: sum(1 for n in rows if n.startswith(p))
    M, D, K = count("M"), count("D"), count("K")
    other = controls - M - D - K

    m = re.search(r"controls=(\d+)", text)
    header = int(m.group(1)) if m else None
    m = re.search(r"TARGET_MET: \d+ of (\d+)", text)
    verdict_of = int(m.group(1)) if m else None

    print("TALLY receipt=%s rows=%d anchors=%d controls=%d M=%d D=%d K=%d other=%d header=%s verdict_of=%s"
          % (a.receipt, len(rows), len(anchors), controls, M, D, K, other, header, verdict_of))

    bad = 0
    if header is not None and header != controls:
        print("TALLY_MISMATCH header=%d computed=%d" % (header, controls))
        bad += 1
    if verdict_of is not None:
        want = len(rows) - (1 if "REF" in rows else 0)
        if verdict_of != want:
            print("TALLY_MISMATCH verdict_of=%d computed=%d" % (verdict_of, want))
            bad += 1
    if other:
        print("TALLY_NOTE %d control row(s) outside M/D/K prefixes" % other)

    if a.claim:
        try:
            claim = open(a.claim, encoding="utf-8", errors="replace").read()
        except OSError as e:
            print("SETUP_ERROR %s" % e)
            return 2
        got = {}
        for pat, key in ((r"(\d+) do-nothing", "D"), (r"(\d+) cheats?", "K"),
                         (r"(\d+) (?:single-defect )?mutants?", "M"),
                         (r"(\d+) `?ok`? lines", "rows"),
                         (r"controls=(\d+)", "controls")):
            m = re.search(pat, claim)
            if m:
                got[key] = int(m.group(1))
        m = re.search(r"(?<!controls=)(\d+) controls\b", claim)
        if m and "controls" not in got:
            got["controls"] = int(m.group(1))
        observed = {"D": D, "K": K, "M": M, "rows": len(rows), "controls": controls}
        print("TALLY claim=%s repeated=%s" % (a.claim, ",".join("%s:%d" % (k, got[k]) for k in sorted(got)) or "-"))
        for key in sorted(got):
            if got[key] != observed[key]:
                print("TALLY_MISMATCH claim %s=%d receipt=%d" % (key, got[key], observed[key]))
                bad += 1

    print("CHECK78: verdict=%s mismatches=%d" % ("FAIL" if bad else "OK", bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
