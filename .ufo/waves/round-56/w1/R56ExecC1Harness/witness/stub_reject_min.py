#!/usr/bin/env python3
"""Rejects everything with one fixed leg."""
import argparse, sys
ap = argparse.ArgumentParser(); ap.add_argument("--repo"); ap.add_argument("--rev"); ap.add_argument("--work")
a = ap.parse_args()
print("MADO_AUTORELOAD_ENTRY: rev=%s rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33 new_rows=0/8 verdict=TARGET_MISSED missed=tables_sha" % a.rev)
sys.exit(1)
