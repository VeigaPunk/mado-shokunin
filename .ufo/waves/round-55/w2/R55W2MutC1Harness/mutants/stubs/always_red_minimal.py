#!/usr/bin/env python3
# always-red (minimal) stub: prints a MISSED line naming three generic legs for every tree, exit 1.
import sys
rev = sys.argv[sys.argv.index("--rev") + 1]
print("MADO_KBD_ENTRY: rev=%s rows=0/18 hosts=0/6 sources=0/0 new_rows=0/3 verdict=TARGET_MISSED missed=entry_absent,provenance,index" % rev)
sys.exit(1)
