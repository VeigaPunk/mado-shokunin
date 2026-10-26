#!/usr/bin/env python3
"""Expand every {{EVID path:line}} placeholder in ../ExecIndepA.md into a cited verbatim block."""
import os, re, sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REPORT = os.path.join(LANE, ".ufo/waves/round-46/w1/ExecIndepA.md")
PLACE = re.compile(r"^\{\{EVID (.+?):(\d+)\}\}$")

text = open(REPORT).read().split("\n")
out = []
filled = 0
for line in text:
    m = PLACE.match(line.strip())
    if not m:
        out.append(line)
        continue
    path, number = m.group(1), int(m.group(2))
    src = open(os.path.join(LANE, path), encoding="utf-8").read().split("\n")
    body = src[number - 1]
    out.append("<!-- evid %s:%d -->" % (path, number))
    out.append("```")
    out.append(body)
    out.append("```")
    filled += 1
open(REPORT, "w").write("\n".join(out))
print("filled %d evidence blocks" % filled)
