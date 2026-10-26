#!/usr/bin/env python3
"""Verify every citation in citations.tsv: file, 1-based line, exact substring, <= 25 words.

Usage: verify_citations.py <seat-dir> <lane-root>
Paths in the TSV are relative to the lane root, except that a leading "receipts/" is
also tried relative to the seat directory (seat-owned receipts). Prints one PASS/FAIL
line per citation and exits 1 on any failure.
"""
import sys, os

seat, lane = sys.argv[1], sys.argv[2]
tsv = os.path.join(seat, "receipts", "citations.tsv")
rows = 0
bad = 0
for raw in open(tsv, encoding="utf-8"):
    raw = raw.rstrip("\n")
    if not raw or raw.startswith("#"):
        continue
    path, line, quote = raw.split("\t", 2)
    rows += 1
    r46 = os.path.join(lane, ".ufo/waves/round-46")
    cand = [os.path.join(r46, path), os.path.join(r46, "fetch", path),
            os.path.join(r46, "l1-draft", path), os.path.join(lane, path),
            os.path.join(seat, path)]
    cpath = next((c for c in cand if os.path.isfile(c)), None)
    if cpath is None:
        print("FAIL missing-file %s" % path)
        bad += 1
        continue
    lines = open(cpath, encoding="utf-8", errors="replace").read().split("\n")
    n = int(line)
    word_ok = len(quote.split()) <= 25
    if not (1 <= n <= len(lines)):
        print("FAIL out-of-range %s:%d" % (path, n))
        bad += 1
        continue
    hit = quote in lines[n - 1]
    if hit and word_ok:
        print("PASS %s:%d %r" % (path, n, quote))
    else:
        print("FAIL %s:%d %r (%s)" % (path, n, quote,
                                      "not-on-line" if not hit else "over-25-words"))
        bad += 1
print("CITATIONS: %d rows, %d pass, %d fail" % (rows, rows - bad, bad))
sys.exit(1 if bad else 0)
