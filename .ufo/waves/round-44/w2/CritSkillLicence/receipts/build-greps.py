#!/usr/bin/env python3
"""Build receipts/greps.txt from quotes.tsv: one computed `grep -n -F` block per row.

  python3 -I .ufo/waves/round-44/w2/CritSkillLicence/receipts/build-greps.py
"""
import os
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-44/w2/CritSkillLicence")
TSV = os.path.join(SEAT, "receipts/quotes.tsv")
OUT = os.path.join(SEAT, "receipts/greps.txt")

rows = []
for ln in open(TSV, encoding="utf-8"):
    ln = ln.rstrip("\n")
    if not ln or ln.startswith("#"):
        continue
    path, line, needle = ln.split("\t")
    rows.append((path, int(line), needle))

buf = ["# computed locators for receipts/quotes.tsv (grep -n -F, cwd = lane root)", ""]
for path, line, needle in rows:
    p = subprocess.run(["grep", "-n", "-F", "--", needle, path], cwd=LANE,
                       capture_output=True, text=True)
    buf.append(f"## {path}:{line}  needle={needle!r}")
    buf.append(p.stdout.rstrip("\n") if p.stdout.strip() else "<NO MATCH>")
    buf.append("")
open(OUT, "w", encoding="utf-8").write("\n".join(buf))
print(f"GREPS: rows={len(rows)} out={OUT}")
