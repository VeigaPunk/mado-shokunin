#!/usr/bin/env python3
"""Merge R1/R2/R3 from sections.md into a copy of l1-draft/entry.md (preview for the L1; scratch only).

usage: merge-preview.py <entry.md in> <entry.md out>
"""
import re
import sys


def blocks(text):
    out, cur, name = {}, [], None
    for line in text.split("\n"):
        if line.startswith("## R") and name is None:
            name, cur = line[3:].strip(), []
            continue
        if name is not None:
            if re.match(r"^\s{0,3}(```|~~~)", line):
                if cur and cur[0] == "FENCE":
                    out[name] = cur[1:]
                    name = None
                    continue
                if not cur:
                    cur = ["FENCE"]
                    continue
                # closing fence of a nested block inside the section: keep it
                cur.append(line)
                continue
            if cur and cur[0] == "FENCE":
                cur.append(line)
    return out


src = open("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/w1/ScrEntryDraft/sections.md").read()
b = blocks(src)
assert set(b) == {"R1", "R2", "R3"}, sorted(b)
r1 = [l for l in b["R1"]]
r2 = [l for l in b["R2"]]
r3 = [l for l in b["R3"]]
while r1 and not r1[-1].strip():
    r1.pop()
while r2 and not r2[-1].strip():
    r2.pop()
while r3 and not r3[-1].strip():
    r3.pop()
assert r1[0].startswith("## Reading a DIFFER"), r1[0]
assert r2[0].startswith("## Running the join"), r2[0]
assert r3[0].startswith("## Limits"), r3[0]

lines = open(sys.argv[1]).read().split("\n")
i_read = lines.index("## Reading a DIFFER or a FALLBACK")
i_lim = lines.index("## Limits")
new = lines[:i_read] + r2 + [""] + r1 + [""] + r3 + [""]
open(sys.argv[2], "w").write("\n".join(new))
print("merged: %d -> %d lines (R1 %d, R2 %d, R3 %d)" % (len(lines), len(new), len(r1), len(r2), len(r3)))
