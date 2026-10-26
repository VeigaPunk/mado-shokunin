#!/usr/bin/env python3
"""Verify every quote in dead-weight.md: <=25 words, present on the cited line, locator recomputed.

A quote row has the shape:  | Qnn | <relative path> | <line> | <quote> |
`\\|` in the quote cell is the markdown escape for a literal pipe.
"""
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
DOC = os.path.join(LANE, ".ufo/waves/round-44/w1/SimpContract/dead-weight.md")
rows = re.findall(r"^\| (Q\d\d) \| (\S+) \| (\d+) \| (.*) \|$", open(DOC).read(), re.M)
if not rows:
    sys.exit("no quote rows found")
bad = 0
for qid, rel, line, raw in rows:
    quote = raw.replace("\\|", "|")
    words = len(quote.split())
    path = os.path.join(LANE, rel)
    lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    n = int(line)
    on_line = 0 < n <= len(lines) and quote in lines[n - 1]
    hits = [k + 1 for k, l in enumerate(lines) if quote in l]
    print("%s %-50s loc=%-4s hits=%-10s words=%-3d on_line=%s in_doc=%s" % (
        qid, rel.rsplit("/", 1)[-1], n, hits, words, on_line, quote in open(DOC).read() or quote.replace("|", "\\|") in open(DOC).read()))
    if words > 25:
        print("  FAIL %s over 25 words" % qid); bad += 1
    if not on_line:
        print("  FAIL %s not on the cited line" % qid); bad += 1
    if hits != [n]:
        print("  NOTE %s recomputed locator %s vs cited %s" % (qid, hits, n))
        if n not in hits:
            bad += 1
print("QUOTES total=%d failures=%d" % (len(rows), bad))
sys.exit(1 if bad else 0)
