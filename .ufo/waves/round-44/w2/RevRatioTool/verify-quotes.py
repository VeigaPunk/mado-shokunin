#!/usr/bin/env python3
"""Verify every QUOTE line in RevRatioTool.md against its located source line.

QUOTE src=<path>:<line> :: <quoted text>
<path> is relative to the lane root, or to this seat dir if the file exists only here.
Pass = the quoted text is a substring of that exact source line.
"""
import os
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
report = open(os.path.join(os.path.dirname(SEAT), "RevRatioTool.md"), encoding="utf-8").read().splitlines()

bad = 0
n = 0
for line in report:
    if not line.startswith("QUOTE src="):
        continue
    n += 1
    spec, _, quote = line[len("QUOTE src="):].partition(" :: ")
    path, _, num = spec.rpartition(":")
    for base in (LANE, SEAT):
        cand = os.path.join(base, path)
        if os.path.isfile(cand):
            src = open(cand, encoding="utf-8", errors="replace").read().splitlines()
            break
    else:
        print("FAIL %s:%s (file not found)" % (path, num))
        bad += 1
        continue
    text = src[int(num) - 1] if 0 < int(num) <= len(src) else None
    if text is not None and quote in text:
        print("PASS %s:%s" % (path, num))
    else:
        print("FAIL %s:%s quote not a substring of that line" % (path, num))
        bad += 1
print("QUOTES: %d checked, %d failed" % (n, bad))
sys.exit(1 if bad else 0)
