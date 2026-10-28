#!/usr/bin/env python3
"""Read-only receipt: each frozen C1 K/H quote is a substring of its pin line (single-line, byte test)."""
import json
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
PIN = LANE / ".ufo/waves/round-55/fetch"
T = json.loads((LANE / ".ufo/waves/round-55/frozen-tables.json").read_text(encoding="utf-8"))
bad = 0
for grp in ("k", "h"):
    for r in T["c1"][grp]:
        lines = (PIN / r["pin"]).read_bytes().decode("utf-8", "replace").split("\n")
        ok = r["quote"] in lines[r["line"] - 1]
        bad += 0 if ok else 1
        print(r["id"], r["pin"], r["line"], "substr=" + str(ok))
print("bad", bad)
