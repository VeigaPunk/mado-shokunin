#!/usr/bin/env python3
"""Comparison step for ExecHostSourceGraph.

Inputs (all read-only):
  graph.json        - output of derive.py (independent walk of the host tree)
  tool-static.txt   - `python3 -I tools/mado-options.py --home $HOME` (last declarer per key)
  live-8.txt        - own `hyprctl getoption -j` receipt for the 8 candidate keys
  <census>          - ExecLiveCensus receipt, the only place the L1's 8 agreement* keys are enumerated

Prints: the derived duplicate set, the L1 agreement* set, and the set difference in both
directions, plus per-key declarer/live rows.
"""
import json
import re
import sys

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/w1/ExecHostSourceGraph"
CENSUS = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/w1/ExecLiveCensus/census-receipt.txt"

g = json.load(open(f"{SEAT}/graph.json"))
tool = {r["key"]: r for r in json.load(open(f"{SEAT}/tool-static.txt"))}
mine = set(g["duplicates"])

# L1 enumeration: the agreement* line of the census receipt.
l1 = set()
for line in open(CENSUS, encoding="utf-8"):
    m = re.match(r"agreement\*=(\d+) keys: (.*)$", line.strip())
    if m:
        l1 = set(m.group(2).split())
        l1_count = int(m.group(1))
        break
else:
    sys.exit("census receipt carries no agreement* line")

# own live receipt
live = {}
for line in open(f"{SEAT}/live-8.txt", encoding="utf-8"):
    if line.startswith("#") or not line.strip():
        continue
    k, _, payload = line.rstrip("\n").partition("\t")
    obj = json.loads(payload)
    form = [f for f in ("int", "float", "str", "custom") if f in obj][0]
    live[k] = (form, obj[form], obj.get("set"))

print(f"derived distinct option keys      : {g['n_distinct_keys']}")
print(f"derived declarations              : {g['n_declarations']}")
print(f"derived keys with >1 declarer     : {len(mine)}")
print(f"L1 census agreement* count        : {l1_count}  (keys listed: {len(l1)})")
print(f"tool static rows                  : {len(tool)}")
print()
print(f"mine - L1   : {sorted(mine - l1) or '(empty)'}")
print(f"L1 - mine   : {sorted(l1 - mine) or '(empty)'}")
print()
for key in sorted(mine):
    decls = g["duplicates"][key]
    t = tool[key]
    form, val, is_set = live[key]
    print(f"{key}  (last declarer: {t['owner']}:{t['line']} layer={t['layer']})")
    for i, d in enumerate(decls, 1):
        print(f"   declarer {i}: {d['file'].replace('/home/vgpnk/', '')}:{d['line']} "
              f"as-written={d['raw']!r} expanded={d['expanded']!r}")
    print(f"   live: form={form} value={val!r} set={is_set}")
