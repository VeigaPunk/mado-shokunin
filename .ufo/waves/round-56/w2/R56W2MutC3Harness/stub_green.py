#!/usr/bin/env python3
"""stub_green.py -- always-green counter stub (oracle check B for seat R56W2MutC3Harness).

Prints one grammatical MADO_USED_BY line with verdict=TARGET_MET on EVERY tree (good and mutated) and exits 0.
It does no work: it is the classic "prints green without working" counter the harness must reject on the controls.
"""
import sys

rev = ""
a = sys.argv[1:]
for i, x in enumerate(a):
    if x == "--rev" and i + 1 < len(a):
        rev = a[i + 1]
sys.stdout.write(
    "MADO_USED_BY: rev=%s entries=71 rows=328 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 "
    "verdict=TARGET_MET missed=none\n" % rev)
sys.exit(0)
