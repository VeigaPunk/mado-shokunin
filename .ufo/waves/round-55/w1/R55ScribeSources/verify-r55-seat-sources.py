#!/usr/bin/env python3 -I
"""Verify seat R55ScribeSources draft rows S378-S380 and their Gate block.

Reads only: the draft rows.md and gate.md, the round-55 fetch pins, SHA256SUMS.txt
and frozen-tables.json. Writes nothing (no temporary files are created).
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--lane", required=True)
ap.add_argument("--seat-dir", required=True)
ap.add_argument("--work", required=True, help="accepted for the scratch rule; unused (no temp files)")
args = ap.parse_args()

LANE = Path(args.lane)
SEAT = Path(args.seat_dir)
FETCH = LANE / ".ufo/waves/round-55/fetch"
FROZEN = json.loads((LANE / ".ufo/waves/round-55/frozen-tables.json").read_text(encoding="utf-8"))
RAW = "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/"
DATE = "2026-10-28"

# id -> (pin file, upstream suffix, anchor line range, expected sha prefix from SHA256SUMS)
SPEC = {
    "S378": ("Hyprland-SeatManager.cpp", "src/managers/SeatManager.cpp", (175, 178)),
    "S379": ("Hyprland-protocols-core-Seat.cpp", "src/protocols/core/Seat.cpp", (441, 448)),
    "S380": ("Hyprland-IKeyboard.hpp", "src/devices/IKeyboard.hpp", (121, 123)),
}

fails = []
def bad(msg):
    fails.append(msg)
    print("FAIL", msg)

# 1. pin bytes vs SHA256SUMS.txt
sums = {}
for line in (FETCH / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
    digest, name = line.split(None, 1)
    sums[name.strip()] = digest
for id_, (pin, _suffix, _rng) in SPEC.items():
    got = hashlib.sha256((FETCH / pin).read_bytes()).hexdigest()
    if got != sums[pin]:
        bad(f"pin_sha {pin} {got} != SHA256SUMS {sums[pin]}")
    else:
        print(f"ok pin_sha {pin} {got}")

# 2. awk -F'|' NF==13 on every new row (shell awk, as SOURCES.md census does)
awk_out = subprocess.run(
    ["awk", "-F|", r"/^\| S37[0-9]|^\| S38[0-9]/ {print NR, NF}", str(SEAT / "rows.md")],
    capture_output=True, text=True, check=True).stdout.split("\n")
awk_rows = [l for l in awk_out if l.strip()]
print("awk rows (NR NF):", " ; ".join(awk_rows))
for l in awk_rows:
    nr, nf = l.split()
    if nf != "13":
        bad(f"awk NF!=13 at rows.md:{nr} NF={nf}")
if len(awk_rows) != 3:
    bad(f"expected 3 rows from awk, got {len(awk_rows)}")

# 3. row cells against the spec and frozen tables
rows = {}
for line in (SEAT / "rows.md").read_text(encoding="utf-8").splitlines():
    if not line.startswith("| S3"):
        continue
    cells = line.split("|")
    if len(cells) != 13:
        bad(f"python NF {len(cells)} on {cells[1].strip()}")
        continue
    cell = [c.strip() for c in cells[1:-1]]
    rows[cell[0]] = cell
    if cell[0] not in SPEC:
        bad(f"unexpected id {cell[0]}")
        continue
    pin, suffix, (lo, hi) = SPEC[cell[0]]
    if cell[1].split(" - ")[-1] != RAW + suffix:
        bad(f"{cell[0]} url cell mismatch")
    if cell[2:5] != ["code", "A", cell[4]] or cell[2] != "code" or cell[3] != "A":
        bad(f"{cell[0]} kind/tier mismatch")
    if cell[8:11] != [DATE, "on-release", "corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"]:
        bad(f"{cell[0]} opened/recheck/used-by mismatch: {cell[8:11]}")
    if cell[7] != "mined":
        bad(f"{cell[0]} status {cell[7]}")
    if f"sha256:{sums[pin]}" not in cell[5]:
        bad(f"{cell[0]} anchor cell lacks pin sha {sums[pin]}")
    if f"{lo}-{hi}" not in cell[5]:
        bad(f"{cell[0]} anchor cell lacks range {lo}-{hi}")
    if "|" in "".join(cell):
        bad(f"{cell[0]} pipe inside a cell")

if sorted(rows) != ["S378", "S379", "S380"]:
    bad(f"rows present: {sorted(rows)}")

# 4. Gate blocks: URL, date, located line, quote, teaches
gate_text = (SEAT / "gate.md").read_text(encoding="utf-8")
blocks = re.split(r"^### ", gate_text, flags=re.M)[1:]
gate = {}
for b in blocks:
    id_ = b.split()[0]
    fields = {}
    for m in re.finditer(r"^- (URL|Access date|Located|Quote|Teaches): (.*)$", b, flags=re.M):
        fields[m.group(1)] = m.group(2).strip()
    gate[id_] = fields

for id_, (pin, suffix, (lo, hi)) in SPEC.items():
    if id_ not in gate:
        bad(f"gate block missing {id_}")
        continue
    g = gate[id_]
    lines = (FETCH / pin).read_bytes().decode("utf-8").split("\n")
    if g.get("URL") != RAW + suffix:
        bad(f"{id_} gate URL mismatch")
    if g.get("Access date") != DATE:
        bad(f"{id_} gate access date {g.get('Access date')}")
    m = re.match(r"`([^`]+):(\d+)`", g.get("Located", ""))
    if not m or m.group(1) != pin:
        bad(f"{id_} located cell {g.get('Located')!r} names wrong pin")
        continue
    ln = int(m.group(2))
    if not (lo <= ln <= hi):
        bad(f"{id_} located line {ln} outside anchor {lo}-{hi}")
    qm = re.fullmatch(r"`(.+)`", g.get("Quote", ""))
    if not qm:
        bad(f"{id_} quote not backticked")
        continue
    quote = qm.group(1)
    words = len(quote.split())
    if words > 25:
        bad(f"{id_} quote has {words} words")
    pin_line = lines[ln - 1]
    if quote not in pin_line:
        bad(f"{id_} quote not substring of {pin}:{ln}")
    else:
        print(f"ok quote {id_} {pin}:{ln} words={words} len={len(quote)}")
    if id_ in rows and g.get("Teaches") != rows[id_][6]:
        bad(f"{id_} gate teaches != row teaches cell")

# 5. frozen K/H quotes for the rows (K10, K11, K12, K18) must be byte-identical substrings
frozen_k = {k["id"]: k for k in FROZEN["c1"]["k"]}
for kid, id_ in (("K10", "S378"), ("K11", "S379"), ("K12", "S379"), ("K18", "S380")):
    k = frozen_k[kid]
    pin = k["pin"]
    lines = (FETCH / pin).read_bytes().decode("utf-8").split("\n")
    ok = lines[k["line"] - 1].find(k["quote"]) >= 0
    print(("ok" if ok else "FAIL"), f"frozen {kid} {pin}:{k['line']} ({id_})")
    if not ok:
        bad(f"frozen {kid} not in pin line")
    lo, hi = SPEC[id_][2]
    if not (lo <= k["line"] <= hi):
        bad(f"frozen {kid} line outside {id_} anchor")

print("VERDICT", "OK" if not fails else f"FAIL({len(fails)})")
sys.exit(0 if not fails else 1)
