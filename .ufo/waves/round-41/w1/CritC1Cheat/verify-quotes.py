#!/usr/bin/env python3
"""Check every quote used in CritC1Cheat.md against the frozen counter.

Each entry: (file, first_line, last_line, quote). The quote is matched with
normalized whitespace against the joined line span, and must be <= 25 words.
"""
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = "quality/counters/c1-r41-globals.py"

QUOTES = [
    (COUNTER, 19, 20, "a NAME must fully match [A-Za-z0-9_]{1,128}"),
    (COUNTER, 30, 30, "NAME = `[A-Za-z0-9_]{1,128}`"),
    (COUNTER, 69, 71, "The stub the judge supplies exits 9 unless argv, stdin and environment are as stated"),
    (COUNTER, 71, 72, "In `--journal-file` mode the tool must not start any process"),
    (COUNTER, 91, 93, "b2  the selftest has teeth: from the tool's functions (not named *selftest*, *_check*, *_run*, *_write*, main, usage)"),
    (COUNTER, 104, 106, "the stub's data is in the stub and a tool that decodes it without running it passes"),
    (COUNTER, 104, 105, "a tool that CONTAINS the class table and parser is an implementation"),
]

bad = 0
for path, a, b, quote in QUOTES:
    lines = open(os.path.join(LANE, path), encoding="utf-8").read().split("\n")
    span = re.sub(r"\s+", " ", " ".join(lines[a - 1:b]))
    words = len(quote.split())
    ok = re.sub(r"\s+", " ", quote) in span and words <= 25
    bad += 0 if ok else 1
    print("QUOTE %s %s:%d-%d words=%d ok=%d | %s"
          % ("ok" if ok else "MISS", path, a, b, words, ok, quote))
print("QUOTES: checked=%d failed=%d" % (len(QUOTES), bad))
sys.exit(1 if bad else 0)
