#!/usr/bin/env python3
"""Verify every row of facts.md against the frozen fetch receipts.

Per row: the receipt's sha256 equals the row's; the quote is 3-25 words; the quote occurs in the
receipt's text normalized exactly as PRED-C2-r41-v1 clause d normalizes it, both over the whole
file and over the named line range. Read-only; prints one line per row and exits non-zero on any
failure.
"""
import hashlib
import html
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FACTS = os.path.join(LANE, ".ufo/waves/round-41/w1/ExecSrcClients/facts.md")


def norm(text):
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


rows = []
for line in open(FACTS, encoding="utf-8"):
    line = line.rstrip("\n")
    if not line.startswith("| ") or line.startswith("| fact |") or line.startswith("|---"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) != 4:
        print("MALFORMED cells=%d: %s" % (len(cells), line[:80]))
        sys.exit(2)
    fact, quote, locator, sha = cells
    q = quote.strip("`")
    m = re.match(r"^(fetch/[A-Za-z0-9._-]+):(\d+)(?:-(\d+))?$", locator)
    if not m:
        print("BAD-LOCATOR %s" % locator)
        sys.exit(2)
    rows.append((fact, q, m.group(1), int(m.group(2)),
                 int(m.group(3) or m.group(2)), sha))

bad = 0
for i, (fact, q, path, lo, hi, sha) in enumerate(rows, 1):
    full = os.path.join(LANE, ".ufo/waves/round-41", path)
    blob = open(full, "rb").read()
    digest = hashlib.sha256(blob).hexdigest()
    text = blob.decode("utf-8", "replace")
    lines = text.splitlines()
    rng = "\n".join(lines[lo - 1:hi])
    qn = re.sub(r"\s+", " ", q)
    words = len(q.split())
    ok_sha = digest == sha
    ok_words = 3 <= words <= 25
    ok_file = qn in norm(text)
    ok_range = qn in norm(rng)
    ok = ok_sha and ok_words and ok_file and ok_range
    bad += not ok
    print("%s %02d %-46s words=%2d sha=%s file=%s range=%s %s:%d-%d" % (
        "PASS" if ok else "FAIL", i, fact[:46], words,
        "ok" if ok_sha else "MISMATCH", "ok" if ok_file else "MISS",
        "ok" if ok_range else "MISS", path, lo, hi))
    if not ok:
        print("     quote=%r" % qn)

print("VERIFY rows=%d failed=%d" % (len(rows), bad))
sys.exit(1 if bad else 0)
