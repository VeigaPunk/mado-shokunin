#!/usr/bin/env python3
# always-red (shotgun) stub: names every leg kind for every row/host id on every tree, exit 1.
import sys
rev = sys.argv[sys.argv.index("--rev") + 1]
ids = ["K%02d" % i for i in range(1, 19)] + ["H%02d" % i for i in range(1, 7)]
legs = ["entry_absent", "provenance", "index", "pin_hash", "new_rows", "tables_sha"]
legs += ["%s:%s" % (kind, i) for kind in ("row", "anchor", "quote", "source_cell", "host") for i in ids]
print("MADO_KBD_ENTRY: rev=%s rows=0/18 hosts=0/6 sources=0/0 new_rows=0/3 verdict=TARGET_MISSED missed=%s" % (rev, ",".join(legs)))
sys.exit(1)
