#!/usr/bin/env python3
"""RevIdRemap: falsify the registration's package-id list by reading the staged
entries' own `source:` lines and the package's own SOURCES.append.md. Read-only."""
import re, sys, hashlib, subprocess, os

PKG = "/home/vgpnk/Projects/shokuknow/merge/mado"
ENT = os.path.join(PKG, "knowledge/corpus/knowledge")
APP = os.path.join(PKG, "SOURCES.append.md")
DOCS = ["idle-lock-never-asked-r12.md", "idle-lock-chain-armed-r14.md",
        "idle-lock-offered-in-the-bar-r15.md"]
CLAIMED = ["S309", "S310", "S321", "S329", "S330", "S331", "S334", "S336"]
LANE = ["S203", "S204", "S205", "S206", "S207", "S208", "S209", "S210"]
# doc -> lane ids, read from the lane entries' own source: lines
LANE_DOC = {"idle-lock-never-asked-r12.md": ["S203", "S204"],
            "idle-lock-chain-armed-r14.md": ["S205"],
            "idle-lock-offered-in-the-bar-r15.md": ["S206", "S207", "S208", "S209", "S210"]}

def sha(p, b): return hashlib.sha256(b).hexdigest()

raw = open(APP, "rb").read()
print(f"append: {APP}")
print(f"  bytes={len(raw)} sha256={sha(APP,raw)}")
rows = []                      # (id, line, cells)
for line in raw.decode().split("\n"):
    m = re.match(r"^\|\s*(S\d+)\s*\|", line)
    if m:
        cells = re.split(r"(?<!\\)\|", line)
        rows.append((m.group(1), line, cells))
ids = [r[0] for r in rows]
base, tip = int(ids[0][1:]), int(ids[-1][1:])
print(f"  rows={len(rows)} base=S{base} tip=S{tip} contiguous={len(ids)==tip-base+1}")

# per-document package ids, two independent readings:
by_usedby = {d: [i for i, l, c in rows if d in c[-2]] for d in DOCS}
by_entry  = {}
print("\n-- staged entries' own source: lines --")
for d in DOCS:
    p = os.path.join(ENT, d)
    b = open(p, "rb").read()
    src = [ln for ln in b.decode().split("\n") if ln.startswith("source:")]
    by_entry[d] = [re.match(r"source:\s*(S\d+)", s).group(1) for s in src]
    print(f"{d}  sha256={sha(p,b)}")
    for s in src: print("   ", s[:150])

print("\n-- cross-check: entry source ids == rows whose used-by names the entry --")
ok_cross = True
for d in DOCS:
    same = by_entry[d] == by_usedby[d]
    ok_cross &= same
    print(f"  {d}: entry={by_entry[d]} usedby={by_usedby[d]} agree={same}")

true_ids = [i for d in DOCS for i in by_usedby[d]]
print(f"\nTRUE package id set (8): {true_ids}")
print(f"CLAIMED set            : {CLAIMED}")

# document -> package id -> lane id map
id2doc = {}
for i, l, c in rows: id2doc[i] = c[2].strip()[:70]
print("\n-- by-document map --")
lane_of = {}
for d in DOCS:
    for lid, pid in zip(LANE_DOC[d], by_usedby[d]):
        lane_of[pid] = lid
        print(f"  pkg {pid}  ->  lane {lid}  | {d}")
        print(f"      envelope: {id2doc[pid]}")
assert len(lane_of) == 8, lane_of

# positional / set comparison
set_hit = sorted(set(CLAIMED) & set(true_ids))
positional = sum(1 for c, t in zip(CLAIMED, true_ids) if c == t)
print(f"\nset intersection = {set_hit}  (|hit|={len(set_hit)}/8)")
print(f"positional matches = {positional}/8")

# implied base under the invariant id = base + row_index
idx = {i: int(i[1:]) - base for i in ids}
print("\n-- what each CLAIMED id actually names in the live file --")
for c in CLAIMED:
    print(f"  {c}: {id2doc[c]}")
    if c in lane_of: print(f"      ^ is one of the eight, but mapped to lane {lane_of[c]}")
print("\n-- implied append base for each CLAIMED id (id - row_index) --")
implied = set()
for c in CLAIMED:
    tgt = dict(zip(true_ids, true_ids))[true_ids[CLAIMED.index(c)]]
    b = int(c[1:]) - idx[tgt]
    implied.add(b)
    print(f"  {c} -> row_index {idx[tgt]} -> implied base S{b}")
print(f"  implied bases: {sorted(implied)}")

fail = []
if set_hit != sorted(true_ids): fail.append("claimed set != true set")
if positional != 8: fail.append(f"positional matches {positional}/8")
if not ok_cross: fail.append("entry source ids != used-by ids")
if implied != {base - 6}: fail.append(f"implied base {sorted(implied)} != {{S{base-6}}}")

print("\nverdict:", "ID_REMAP_WRONG" if fail else "ID_REMAP_RIGHT")
for f in fail: print("  -", f)
sys.exit(1 if fail else 0)
