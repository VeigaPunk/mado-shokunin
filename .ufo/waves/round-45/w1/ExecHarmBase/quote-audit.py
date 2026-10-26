#!/usr/bin/env python3
"""ExecHarmBase quote audit: every backticked span in baseline.md, grepped verbatim in gates/*.txt.

Reads:  baseline.md, gates/*.txt (next to this script)
Writes: gates/quote-check.txt  (span -> receipt:line, or the "no receipt line" list for paths/commands)
Stdlib only; read-only; no network; no writes outside gates/quote-check.txt.
"""
import glob
import os
import re
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(SEAT, "baseline.md")
GATES = os.path.join(SEAT, "gates")
OUT = os.path.join(GATES, "quote-check.txt")

text = open(BASE, encoding="utf-8").read()
spans = []
for m in re.finditer(r"`([^`\n]+)`", text):
    s = m.group(1)
    if s not in spans:
        spans.append(s)

receipts = sorted(glob.glob(os.path.join(GATES, "*.txt")))
receipts = [p for p in receipts if os.path.basename(p) != "quote-check.txt"]
lines = {}
for p in receipts:
    try:
        lines[p] = open(p, encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        pass

found, missing = [], []
for s in spans:
    hit = None
    for p, ls in lines.items():
        for i, ln in enumerate(ls, 1):
            if s in ln:
                hit = (os.path.basename(p), i)
                break
        if hit:
            break
    (found.append((s, hit)) if hit else missing.append(s))

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("# quote audit for baseline.md — grep -F over gates/*.txt\n")
    fh.write("# spans=%d found=%d no-receipt-line=%d\n\n" % (len(spans), len(found), len(missing)))
    fh.write("## found (span | receipt:line | words)\n")
    for s, (p, i) in found:
        fh.write("%s | %s:%d | %d\n" % (s, p, i, len(s.split())))
    fh.write("\n## no receipt line contains this span (paths, commands, hashes, placeholders)\n")
    for s in missing:
        fh.write("%s\n" % s)

long = [(s, len(s.split())) for s, _ in found if len(s.split()) > 25]
print("QUOTE_AUDIT spans=%d found=%d no-receipt-line=%d over-25-words=%d" %
      (len(spans), len(found), len(missing), len(long)))
for s, w in long:
    print("OVER25 %d %r" % (w, s))
sys.exit(1 if long else 0)
