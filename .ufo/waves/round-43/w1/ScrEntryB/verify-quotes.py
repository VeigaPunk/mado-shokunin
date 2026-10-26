#!/usr/bin/env python3
"""Re-open every receipt cited by the ScrEntryB draft and check quotes.tsv against
the files, using PRED-C2-r43's own quote_at/norm helpers (imported read-only)."""
import hashlib
import importlib.util
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = LANE + "/quality/counters/c2-r43-gkeep-entry.py"
SEAT = LANE + "/.ufo/waves/round-43/w1/ScrEntryB"

spec = importlib.util.spec_from_file_location("c2", COUNTER)
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

rows = [l.rstrip("\n").split("\t") for l in open(SEAT + "/quotes.tsv", encoding="utf-8")]
head, rows = rows[0], [r for r in rows[1:] if r and r[0]]
bad = 0
for r in rows:
    rid, rel, sha, line, words, kind, q = r
    blob = open(os.path.join(LANE, rel), "rb").read()
    got_sha = hashlib.sha256(blob).hexdigest()
    at = c2.quote_at(blob, re.sub(r"\s+", " ", q))
    w = len(re.sub(r"\s+", " ", q).split())
    ok = got_sha == sha and str(at) == line and w == int(words) and 3 <= w <= 25
    bad += not ok
    print("%s %s sha=%s line=%s words=%d %s" % (
        rid, "ok" if ok else "FAIL", "match" if got_sha == sha else "MISMATCH",
        at, w, "3<=w<=25" if 3 <= w <= 25 else "WORDCOUNT-OUT-OF-RANGE"))
paths = [os.path.basename(r[1]) for r in rows]
print("distinct receipts=%d distinct quotes=%d" % (
    len(set(paths)), len(set(re.sub(r"\s+", " ", r[6]) for r in rows))))
print("VERDICT: %s" % ("PASS" if not bad else "FAIL"))
sys.exit(0 if not bad else 1)
