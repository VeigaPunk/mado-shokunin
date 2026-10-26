#!/usr/bin/env python3
"""Verify every quote in quotes.txt appears verbatim on its cited line of the pinned source.

quotes.txt format (tab separated): <relative-source-path>:<line>\t<quote>
Sources are resolved against .ufo/waves/round-46/fetch/.
Exits 0 only if every quote verifies and every quote is <= 25 words.
"""
import pathlib
import sys

SEAT = pathlib.Path(__file__).resolve().parent
FETCH = SEAT.parent.parent / "fetch"

bad = 0
total = 0
for raw in (SEAT / "quotes.txt").read_text().splitlines():
    if not raw or raw.startswith("#"):
        continue
    total += 1
    loc, quote = raw.split("\t", 1)
    rel, line_s = loc.rsplit(":", 1)
    line_no = int(line_s)
    src = FETCH / rel
    if not src.is_file():
        print(f"FAIL missing source {src} for {loc}")
        bad += 1
        continue
    lines = src.read_text(errors="replace").splitlines()
    if line_no < 1 or line_no > len(lines):
        print(f"FAIL {loc}: line out of range ({len(lines)} lines)")
        bad += 1
        continue
    words = len(quote.split())
    if words > 25:
        print(f"FAIL {loc}: quote is {words} words (>25)")
        bad += 1
    if quote not in lines[line_no - 1]:
        print(f"FAIL {loc}: quote not on cited line")
        print(f"  quote: {quote!r}")
        print(f"  line : {lines[line_no - 1]!r}")
        bad += 1
        continue
    print(f"OK   {loc}  ({words} words)  {quote}")

print(f"-- {total - bad}/{total} quotes verified")
sys.exit(1 if bad else 0)
