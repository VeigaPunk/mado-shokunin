#!/usr/bin/env python3
"""stub_legs.py -- "prints every leg missed" counter stub (oracle check C for seat R56W2MutC3Harness).

Prints one grammatical MADO_USED_BY line with verdict=TARGET_MISSED and every leg in `missed` (all six counted legs
nonzero), exit 1. It claims to have failed every leg on every tree, including the good one: the harness must score
FAIL because `good` is not ok.
"""
import sys

rev = ""
a = sys.argv[1:]
for i, x in enumerate(a):
    if x == "--rev" and i + 1 < len(a):
        rev = a[i + 1]
sys.stdout.write(
    "MADO_USED_BY: rev=%s entries=71 rows=328 missing=1 extra=1 dangling=1 conflict=1 stale=1 lost=1 exempt=24 "
    "verdict=TARGET_MISSED missed=missing,extra,dangling,conflict,stale,lost\n" % rev)
sys.exit(1)
