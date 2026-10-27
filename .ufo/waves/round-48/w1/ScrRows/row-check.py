#!/usr/bin/env python3
"""Structural check for rows.md / gate-lines.md (round 48 w1, seat ScrRows).

Checks, without touching the corpus:
  1. corpus/SOURCES.md still holds 276 rows and none of S340-S347 is taken (no id collision).
  2. every table row in rows.md has exactly 11 cells, no empty cell, no cell padded with
     leading/trailing spaces, and the status/opened/recheck/used-by values are the declared ones.
  3. every sha256 quoted in rows.md matches the committed receipt in fetch/ (prefix or full).
  4. every fetch/receipts path named in rows.md or gate-lines.md exists in this seat dir.
  5. gate-lines.md carries 8 GATE lines and at least 2 REJECT lines with a Flip condition.
Exit 1 on any failure; writes row-check.txt.
"""
import hashlib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[4]
out = []
fail = 0


def bad(msg):
    global fail
    fail += 1
    out.append("FAIL " + msg)


# 1. registry state
reg = (LANE / "corpus/SOURCES.md").read_text(encoding="utf-8").splitlines()
rows = [l for l in reg if l.startswith("| S") and l.count("|") >= 11]
ids = [l.split("|")[1].strip() for l in rows]
out.append(f"registry rows={len(rows)} max={max(ids)}")
if len(rows) != 276:
    bad(f"registry row count {len(rows)} != 276 at base")
for n in range(340, 348):
    if f"S{n}" in ids:
        bad(f"S{n} already in registry")

# 2. rows.md table
text = (HERE / "rows.md").read_text(encoding="utf-8")
table = [l for l in text.splitlines() if l.startswith("| S3")]
if len(table) != 8:
    bad(f"rows.md table lines {len(table)} != 8")
seen = []
for line in table:
    cells = line.strip().strip("|").split("|")
    if len(cells) != 11:
        bad(f"{line[:12]} cells={len(cells)}")
        continue
    seen.append(cells[0].strip())
    for i, c in enumerate(cells):
        if not c.strip():
            bad(f"{cells[0].strip()} cell {i} empty")
        if c != " " + c.strip() + " ":
            bad(f"{cells[0].strip()} cell {i} not single-space padded: {c!r}")
    if cells[7].strip() != "mined":
        bad(f"{cells[0].strip()} status {cells[7]!r}")
    if cells[8].strip() != "2026-10-26":
        bad(f"{cells[0].strip()} opened {cells[8]!r}")
    if cells[9].strip() != "on-release":
        bad(f"{cells[0].strip()} recheck {cells[9]!r}")
    if cells[10].strip() != "corpus/knowledge/xkb-keymap-compile-r48.md":
        bad(f"{cells[0].strip()} used-by {cells[10]!r}")
if seen != [f"S{n}" for n in range(340, 348)]:
    bad(f"ids in order? {seen}")

# 3. sha256 prefixes resolve to committed receipts
files = {p.name: p for p in (HERE / "fetch").iterdir() if p.is_file()}
hashes = {}
for name, p in files.items():
    hashes[hashlib.sha256(p.read_bytes()).hexdigest()] = name
cells_text = " ".join("|".join(l.strip().strip("|").split("|")) for l in table)
for m in re.finditer(r"sha256:([0-9a-f]{8,64})", cells_text):
    prefix = m.group(1)
    hit = [n for h, n in hashes.items() if h.startswith(prefix)]
    if not hit:
        bad(f"sha256 {prefix} has no committed receipt")
    else:
        out.append(f"sha256 {prefix[:8]} -> fetch/{hit[0]}")

# 4. named receipts exist
named = set(re.findall(r"(?<![\w./-])fetch/[A-Za-z0-9._-]+", text + (HERE / "gate-lines.md").read_text(encoding="utf-8")))
for n in sorted(named):
    p = HERE / n
    if not p.exists():
        bad(f"named receipt missing: {n}")
out.append(f"receipts named={len(named)} all_present={all((HERE / n).exists() for n in named)}")

# 5. gate lines
gates = (HERE / "gate-lines.md").read_text(encoding="utf-8").splitlines()
gate_rows = [l for l in gates if l.startswith("- GATE ")]
rejects = [l for l in gates if l.startswith("- REJECT ")]
out.append(f"gate lines={len(gate_rows)} reject lines={len(rejects)}")
if len(gate_rows) != 8:
    bad(f"gate lines {len(gate_rows)} != 8")
if len(rejects) < 2:
    bad("fewer than 2 rejected candidates")
if sum(1 for l in gates if "Flip:" in l) < 2:
    bad("fewer than 2 flip conditions")

out.append(f"ROW_CHECK: rows={len(table)} gates={len(gate_rows)} rejects={len(rejects)} failed={fail}")
report = "\n".join(out) + "\n"
(HERE / "row-check.txt").write_text(report, encoding="utf-8")
sys.stdout.write(report)
sys.exit(1 if fail else 0)
