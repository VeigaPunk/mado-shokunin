#!/usr/bin/env python3
"""Exact gate-quote word counts and receipt byte offsets. Run with -I.

Counter convention: count.py:127-135 returns the full remainder after
"gate-quote: {sid} ", which still begins with "located: ". Numbers labelled
`ctr_*` follow that; `bare_*` strip the "located: " prefix.
"""
import json
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
spec = json.loads((LANE / ".ufo/waves/round-35/c1/frozen.json").read_text())

print("id  entry  line  full_awk  ctr_words  bare_words  ctr_bytes  bare_bytes  "
      "ctr_off  bare_off  receipt_size  tail_ok  once_entry  once_receipt  eq_located")
for rel, ids in spec["entries"].items():
    etext = (LANE / rel).read_text()
    elines = etext.splitlines()
    for sid in ids:
        needle = f"gate-quote: {sid} "
        hits = [i for i, l in enumerate(elines, 1) if l.startswith(needle)]
        line = elines[hits[0] - 1]
        quote = line[len(needle):]
        bare = quote[len("located: "):] if quote.startswith("located: ") else None
        rb = (LANE / spec["receipts"][sid]["path"]).read_bytes()
        loc = next(l for l in rb.decode().splitlines() if l.startswith("located: "))
        ctr_off = rb.find(quote.encode())
        bare_off = rb.find(bare.encode()) if bare else -1
        print(
            sid, Path(rel).name, hits[0], len(line.split()), len(quote.split()),
            (len(bare.split()) if bare else -1), len(quote.encode()),
            (len(bare.encode()) if bare else -1), ctr_off, bare_off, len(rb),
            ctr_off + len(quote.encode()) + 1 == len(rb),
            etext.count(quote), rb.count(quote.encode()),
            quote.encode() == loc.encode(), sep="  ")
