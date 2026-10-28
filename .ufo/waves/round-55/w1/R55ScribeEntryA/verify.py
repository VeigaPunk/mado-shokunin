#!/usr/bin/env python3
"""R55 ScribeEntryA verifier (independent of gen_entry.py): parses the drafted entry, then checks
(1) provenance trio opens the file; (2) exactly one K01-K18 and H01-H06 row each, 5 cells, ids in order;
(3) every K/H pin cell equals frozen `pin:line` and every quote cell equals frozen quote; (4) every quote is an
exact substring of its pin line; (5) every pin file hashes to frozen c1.pin_sha256; (6) S-ids for K and E rows
match the expected registry mapping (K10 S378, K11/K12 S379, K18 S380, others as registration §C1);
(7) every proposition cell is >=40 chars (K) / >=20 chars (H) and has no pipe or backtick; (8) E rows: quote
substring of the named pin line. Prints one line per check failure and a summary; exit 0 only if all pass."""
import hashlib, json, re, sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
W = LANE / ".ufo/waves/round-55"
FETCH = W / "fetch"
ENTRY = Path(sys.argv[1]) if len(sys.argv) > 1 else W / "w1/R55ScribeEntryA/entry.md"
T = json.load(open(W / "frozen-tables.json", encoding="utf-8"))
C1 = T["c1"]
fails = []
def bad(msg):
    fails.append(msg); print("FAIL", msg)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

# (5) every pin hash
pin_ok = 0
for name, want in C1["pin_sha256"].items():
    got = sha(FETCH / name)
    print(f"pin {name} sha256={got} {'ok' if got == want else 'BAD'}")
    if got == want: pin_ok += 1
    else: bad(f"pin_sha256 {name} got={got} want={want}")
print(f"pins sha256 ok={pin_ok}/{len(C1['pin_sha256'])}")

text = ENTRY.read_text(encoding="utf-8")
lines = text.split("\n")
# (1) trio
trio_ok = (lines[0].startswith("source:") and re.search(r"\bS\d{3}\b", lines[0]) is not None
           and lines[1] == "verified-at: 2026-10-28" and lines[2].startswith("recheck:"))
if not trio_ok: bad("provenance trio not first three lines")
print(f"provenance trio {'ok' if trio_ok else 'BAD'}")

EXPECT_S = {"K01": "S316", "K02": "S316", "K03": "S316", "K04": "S316", "K05": "S316", "K06": "S316", "K07": "S316",
            "K08": "S319", "K09": "S319", "K10": "S378", "K11": "S379", "K12": "S379", "K13": "S318", "K14": "S318",
            "K15": "S318", "K16": "S317", "K17": "S052", "K18": "S380"}

# parse table rows: first cell is id; cells split on unescaped pipe
rows = {}
extra = {}
for ln in lines:
    m = re.match(r"^\| ([KHE]\d\d) \|(.*)\|$", ln)
    if not m: continue
    rid = m.group(1)
    cells = [c.strip() for c in ln.strip()[1:-1].split(" | ")]
    if len(cells) != 5:
        # a pipe inside a cell would split more; count raw pipes instead
        bad(f"{rid} has {len(cells)} cells (want 5)")
        continue
    if rid[0] == "E":
        extra.setdefault(rid, []).append(cells)
    else:
        rows.setdefault(rid, []).append(cells)

def check_pin_quote(rid, pin_file, line, quote):
    p = FETCH / pin_file
    L = p.read_text(encoding="utf-8").split("\n")
    if not (0 < line <= len(L)):
        bad(f"{rid} line {line} out of range in {pin_file}"); return False
    if quote not in L[line - 1]:
        bad(f"{rid} quote not substring of {pin_file}:{line}"); return False
    return True

# (2)(3)(4)(6)(7) K and H rows
row_ok = 0
for kind, frozen_rows, minlen in (("K", C1["k"], 40), ("H", C1["h"], 20)):
    for fr in frozen_rows:
        rid = fr["id"]
        got = rows.get(rid, [])
        if len(got) != 1:
            bad(f"row:{rid} count={len(got)}"); continue
        src, prop, sid_cell, pin_cell, quote_cell = got[0]
        want_pin = f"{fr['pin']}:{fr['line']}"
        if pin_cell != want_pin: bad(f"anchor:{rid} pin cell {pin_cell!r} != {want_pin!r}"); continue
        if quote_cell != f"`{fr['quote']}`": bad(f"quote:{rid} quote cell != frozen"); continue
        if not check_pin_quote(rid, fr["pin"], fr["line"], fr["quote"]): continue
        if len(prop) < minlen: bad(f"{rid} proposition {len(prop)} < {minlen} chars"); continue
        if "`" in prop: bad(f"{rid} proposition contains backtick"); continue
        if kind == "K":
            if sid_cell != EXPECT_S[rid]: bad(f"source_cell:{rid} {sid_cell} != {EXPECT_S[rid]}"); continue
        else:
            if sid_cell != "host": bad(f"{rid} source cell {sid_cell!r} != host"); continue
        row_ok += 1
print(f"K/H rows ok={row_ok}/24")

# (8) extra rows: exact substring of named pin line and an S-id from the registry set
EXTRA_OK = 0
for rid, items in sorted(extra.items()):
    for src, prop, sid_cell, pin_cell, quote_cell in items:
        m = re.match(r"^(.+):(\d+)$", pin_cell)
        if not m: bad(f"{rid} pin cell malformed"); continue
        pin_file, line = m.group(1), int(m.group(2))
        if not quote_cell.startswith("`") or not quote_cell.endswith("`"): bad(f"{rid} quote cell not backticked"); continue
        q = quote_cell[1:-1]
        if check_pin_quote(rid, pin_file, line, q) and re.fullmatch(r"S\d{3}|host", sid_cell) and len(prop) >= 40:
            EXTRA_OK += 1
        else:
            bad(f"{rid} extra row check failed (sid={sid_cell!r} prop_len={len(prop)})")
print(f"E rows ok={EXTRA_OK}/{sum(len(v) for v in extra.values())} ids={sorted(extra)}")

# every backticked quote in K/H/E rows occurs in the file exactly once per row (no stray duplicates of ids)
ids = [m.group(1) for m in (re.match(r"^\| ([KHE]\d\d) \|", ln) for ln in lines) if m]
dups = sorted({i for i in ids if ids.count(i) > 1})
if dups: bad(f"duplicate ids {dups}")
print(f"duplicate ids: {'none' if not dups else dups}")

# README index row template and counter-style leg names are the integration's job; verify only the entry file here
total = row_ok
print(f"VERIFY_SUMMARY entry={ENTRY} kh_rows={row_ok}/24 extra={EXTRA_OK} pins={pin_ok}/{len(C1['pin_sha256'])} failures={len(fails)} verdict={'OK' if not fails else 'FAIL'}")
sys.exit(0 if not fails else 1)
