#!/usr/bin/env python3
"""Check every quote in quotes.txt against the cited line of the cited file.

Usage: python3 -I verify-quotes.py [lane-root]
Default lane root: the mado-shokunin checkout this seat works in.
Prints one line per quote: OK <path>:<line> | BAD ... ; exit 0 iff every quote is found on its line.
"""
import os
import sys

LANE = sys.argv[1] if len(sys.argv) > 1 else "/home/vgpnk/Projects/shokunin/mado-shokunin"
HERE = os.path.dirname(os.path.abspath(__file__))
bad = 0
total = 0
for raw in open(os.path.join(HERE, "quotes.txt"), encoding="utf-8"):
    line = raw.rstrip("\n")
    if not line.strip() or line.lstrip().startswith("#"):
        continue
    loc, quote = line.split(" :: ", 1)
    path, n = loc.rsplit(":", 1)
    total += 1
    try:
        with open(os.path.join(LANE, path), encoding="utf-8", errors="replace") as fh:
            src = fh.readlines()
        text = src[int(n) - 1]
    except (OSError, IndexError) as exc:
        print("BAD %s (%s)" % (loc, exc))
        bad += 1
        continue
    if quote in text:
        print("OK  %s" % loc)
    else:
        print("BAD %s :: %r not in %r" % (loc, quote, text.strip()[:160]))
        bad += 1
print("QUOTES: %d/%d verified" % (total - bad, total))
sys.exit(0 if bad == 0 else 1)
