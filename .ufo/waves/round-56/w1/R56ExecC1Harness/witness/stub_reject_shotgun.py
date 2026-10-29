#!/usr/bin/env python3
"""Rejects everything and names EVERY registered leg (shotgun): passes every control leg check, but good must be bad."""
import argparse, sys
ap = argparse.ArgumentParser(); ap.add_argument("--repo"); ap.add_argument("--rev"); ap.add_argument("--work")
a = ap.parse_args()
legs = ["entry_absent", "tables_sha", "prov", "index", "pin_hash", "new_rows"]
for kind in ("row", "quote", "source_cell", "scope", "tok", "num"):
    legs += ["%s:K%02d" % (kind, i) for i in range(1, 31)]
for kind in ("row", "quote", "host", "tok", "num"):
    legs += ["%s:H%02d" % (kind, i) for i in range(1, 4)]
print("MADO_AUTORELOAD_ENTRY: rev=%s rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33 new_rows=0/8 verdict=TARGET_MISSED missed=%s" % (a.rev, ",".join(legs)))
sys.exit(1)
