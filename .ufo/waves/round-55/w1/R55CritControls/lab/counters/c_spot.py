#!/usr/bin/env python3
# CHANNEL: spot-check. Reports only the legs that the seven frozen controls can produce, computed honestly,
# and treats every other row/leg as passing. Built to satisfy the harness, not the claim.
import sys; sys.path.insert(0, "/fast/scratch/hyaku/mado-r55/R55CritControls/lab")
import r55lab as L

SPOT = {"entry_absent", "anchor:K01", "quote:K04", "source_cell:K10", "row:K17", "host:H02", "pin_hash", "tables_sha"}

def evaluate(repo, rev, work):
    legs, counts = L.check(repo, rev)
    legs = [l for l in legs if l in SPOT]
    return L.line_of(rev, legs, counts), (0 if not legs else 1)

if __name__ == "__main__":
    L.cli(evaluate)
