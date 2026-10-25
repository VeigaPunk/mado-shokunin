#!/usr/bin/env python3
"""Check every block quote in finding.md: <= 25 words and present verbatim in its source.

Each quote block is a run of `> ` lines.  A quote is accepted when its whitespace-normalised
text occurs in the whitespace-normalised text of at least one source file given on the CLI.
Read-only; prints one line per quote and a final tally.
"""
import re
import sys

finding = sys.argv[1]
sources = sys.argv[2:]
src = " ".join(re.sub(r"\s+", " ", open(p, encoding="utf-8").read()) for p in sources)

blocks, cur = [], []
for line in open(finding, encoding="utf-8"):
    if line.startswith(">"):
        cur.append(line[1:].strip())
    elif cur:
        blocks.append(" ".join(cur))
        cur = []
if cur:
    blocks.append(" ".join(cur))

bad = 0
for i, q in enumerate(blocks, 1):
    n = len(re.sub(r"\s+", " ", q).split())
    hit = re.sub(r"\s+", " ", q) in src
    ok = n <= 25 and hit
    bad += not ok
    print("quote%d words=%d located=%s ok=%s :: %s" % (i, n, int(hit), ok, q[:90]))
print("QUOTES: n=%d all_ok=%s max_words=%d" % (len(blocks), int(bad == 0),
      max(len(re.sub(r"\s+", " ", q).split()) for q in blocks) if blocks else 0))
sys.exit(0 if bad == 0 else 1)
