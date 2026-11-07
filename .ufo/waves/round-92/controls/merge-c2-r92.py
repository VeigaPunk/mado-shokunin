#!/usr/bin/env python3
"""Round-92 C2: merge the L1 battery/mutants with R92MMutC2's (ids already in the L1 battery keep the L1 copy)."""
import json, sys
l1b, mcb, l1m, mcm, outb, outm = sys.argv[1:7]
b = json.load(open(l1b))["fixtures"]
ids = {f["id"] for f in b}
b += [f for f in json.load(open(mcb))["fixtures"] if f["id"] not in ids]
m = json.load(open(l1m))["mutants"]
mids = {x["id"] for x in m}
extra = [x for x in json.load(open(mcm))["mutants"] if x["id"] not in mids]
json.dump({"fixtures": b}, open(outb, "w"), indent=1, ensure_ascii=True)
json.dump({"mutants": m + extra}, open(outm, "w"), indent=1, ensure_ascii=True)
print(f"battery {len(b)} mutants {len(m) + len(extra)}")
