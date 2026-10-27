#!/usr/bin/env python3
"""Structural check of the C2EntryDraft proposition map against the pin bytes.

Read-only: opens the TSV, the entry draft and the pins; writes nothing.
Exit 0 = every proposition has a row, a pin, an in-range verbatim quote of
at most 25 words and a support rationale, and the entry draft cites each row
and prop id. Exit 1 = at least one defect (each printed with its prop id).
Exit 2 = setup problem (missing file, bad argument).

This checks bindings, not entailment: a quote that sits at the anchor and
says something else still passes here and needs the independent reviewer.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WORD_MAX = 25
FIELDS = ["prop", "row", "proposition", "pin", "anchor", "quote", "support", "rationale"]


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True, type=Path)
    ap.add_argument("--entry", required=True, type=Path)
    ap.add_argument("--pins-dir", required=True, type=Path)
    a = ap.parse_args()

    for p in (a.map, a.entry, a.pins_dir):
        if not p.exists():
            print(f"SETUP: missing {p}")
            return 2

    rows = []
    header = None
    for n, line in enumerate(a.map.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        cells = line.split("\t")
        if header is None:
            header = cells
            missing = [f for f in FIELDS if f not in header]
            if missing:
                print(f"SETUP: header lacks {missing}")
                return 2
            continue
        if len(cells) != len(header):
            print(f"FAIL tsvline{n}: {len(cells)} cells, header {len(header)}")
            return 1
        rows.append(dict(zip(header, cells)))

    entry = a.entry.read_text(encoding="utf-8")
    failures = 0
    props = []

    for r in rows:
        pid = r["prop"]
        props.append(pid)
        problems = []
        if not re.fullmatch(r"S\d{3}", r["row"]):
            problems.append(f"row id {r['row']!r} is not S###")
        for f in FIELDS:
            if not r[f].strip():
                problems.append(f"empty {f}")
        m = re.fullmatch(r"(?:.*/)?([\w.\-]+\.(?:cpp|hpp)):(\d+)(?:-(\d+))?", r["anchor"])
        if not m:
            problems.append(f"anchor {r['anchor']!r} not path:start[-end]")
        quote = norm(r["quote"])
        words = len(quote.split())
        if words > WORD_MAX:
            problems.append(f"quote {words} words > {WORD_MAX}")
        if problems:
            print(f"FAIL {pid}: " + "; ".join(problems))
            failures += 1
            continue

        pin_name = m.group(1)
        start = int(m.group(2))
        end = int(m.group(3) or m.group(2))
        pin = a.pins_dir / pin_name
        if pin.name != r["pin"]:
            print(f"FAIL {pid}: anchor file {pin_name} != pin column {r['pin']}")
            failures += 1
            continue
        if not pin.exists():
            print(f"FAIL {pid}: pin missing {pin}")
            failures += 1
            continue
        lines = pin.read_text(encoding="utf-8", errors="replace").splitlines()
        if not (1 <= start <= end <= len(lines)):
            print(f"FAIL {pid}: span {start}-{end} outside 1-{len(lines)}")
            failures += 1
            continue
        window = norm("\n".join(lines[start - 1:end]))
        if quote not in window:
            print(f"FAIL {pid}: quote not in {pin.name}:{start}-{end}")
            failures += 1
            continue
        if f"| {pid} |" not in entry:
            print(f"FAIL {pid}: not present in entry draft proposition table")
            failures += 1
            continue
        if r["row"] not in entry:
            print(f"FAIL {pid}: row {r['row']} not cited in entry draft")
            failures += 1
            continue
        print(f"PASS {pid} row={r['row']} {pin.name}:{start}-{end} words={words}")

    if len(set(props)) < 4:
        print(f"FAIL count: {len(set(props))} propositions < 4")
        failures += 1
    dupes = sorted({p for p in props if props.count(p) > 1})
    if dupes:
        print(f"FAIL count: duplicate prop ids {dupes}")
        failures += 1

    print(
        f"MADO_R52_C2_ENTRY_CHECK: props={len(set(props))} rows={len({r['row'] for r in rows if r['row']})} "
        f"pins={len({r['pin'] for r in rows})} quote_max_words={WORD_MAX} failures={failures} "
        f"verdict={'OK' if failures == 0 else 'DEFECT'}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
