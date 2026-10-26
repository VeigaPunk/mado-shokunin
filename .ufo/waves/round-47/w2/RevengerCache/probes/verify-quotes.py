#!/usr/bin/env python3
"""Verifies every quotation in the seat report: it re-reads the cited source line, asserts the quote is
there, caps the quote at 25 words, and asserts the report carries the computed locator.

Run: python3 -I probes/verify-quotes.py [--report PATH]
"""
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-47/w2/RevengerCache")
REPORT = os.path.join(LANE, ".ufo/waves/round-47/w2/RevengerCache.md")
if "--report" in sys.argv:
    REPORT = sys.argv[sys.argv.index("--report") + 1]

report = open(REPORT, encoding="utf-8").read()
rows = [l.rstrip("\n").split("\t", 2) for l in open(os.path.join(SEAT, "quotes.txt"), encoding="utf-8")]
ok = 0
bad = []
for rel, line_s, quote in rows:
    line = int(line_s)
    path = os.path.join(LANE, rel)
    src = open(path, encoding="utf-8", errors="replace").read().splitlines()
    if not (1 <= line <= len(src)) or quote not in src[line - 1]:
        bad.append("%s:%d quote_mismatch" % (rel, line))
        continue
    words = len(quote.split())
    if words > 25:
        bad.append("%s:%d quote_words=%d" % (rel, line, words))
        continue
    base = os.path.basename(rel)
    if "%s:%d" % (base, line) not in report:
        bad.append("%s:%d locator_not_in_report" % (base, line))
        continue
    ok += 1

print("quotes checked: %d/%d" % (ok, len(rows)))
for b in bad:
    print("FAIL", b)
print("locator check: %d/%d matched" % (ok, len(rows)))
sys.exit(0 if ok == len(rows) else 1)
