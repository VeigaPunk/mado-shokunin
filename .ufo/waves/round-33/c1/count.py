#!/usr/bin/env python3
"""PRED-C1-r33-v1 counter. One command over a tree. Exit 0 TARGET_MET, 1 TARGET_MISSED, 2 usage.

PRED-C1-r33-v1: TARGET_MET iff closed_entries=2 AND closed_rows=4 AND open_cites=0, where a frozen cite is closed only when the entry file contains a 1-25 word gate-quote line for that id that is a contiguous substring of the fetch blob and that blob's sha256 equals the digest frozen in c1/frozen.json, and the registry row for that id lists the entry path in used-by.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

PREDICATE = (
    "PRED-C1-r33-v1: TARGET_MET iff closed_entries=2 AND closed_rows=4 AND open_cites=0, "
    "where a frozen cite is closed only when the entry file contains a 1-25 word gate-quote "
    "line for that id that is a contiguous substring of the fetch blob and that blob's sha256 "
    "equals the digest frozen in c1/frozen.json, and the registry row for that id lists the "
    "entry path in used-by."
)


def die(msg: str) -> None:
    print(f"PRED-C1-r33-v1 error={msg}", file=sys.stderr)
    raise SystemExit(2)


def used_by(line: str) -> str:
    parts = [p.strip() for p in line.split("|")]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return parts[-1] if parts else ""


def row_for(sources: str, sid: str) -> str | None:
    prefix = f"| {sid} |"
    for line in sources.splitlines():
        if line.startswith(prefix) or line.startswith(f"|{sid}|"):
            return line
    return None


def gate_quote(entry: str, sid: str) -> str | None:
    needle = f"gate-quote: {sid} "
    for line in entry.splitlines():
        if line.startswith(needle):
            return line[len(needle):]
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--frozen", required=True)
    args = ap.parse_args()
    root = Path(args.root)
    frozen_path = Path(args.frozen)
    if not frozen_path.is_file():
        die("frozen-missing")
    spec = json.loads(frozen_path.read_text())
    if spec.get("predicate") != PREDICATE:
        die("predicate-drift")
    sources_path = root / "corpus" / "SOURCES.md"
    sources = sources_path.read_text() if sources_path.is_file() else ""
    closed_entries = 0
    closed_rows = 0
    open_cites = 0
    for entry_rel, ids in spec["entries"].items():
        entry_path = root / entry_rel
        entry = entry_path.read_text() if entry_path.is_file() else ""
        entry_closed = entry_path.is_file()
        for sid in ids:
            fetch = spec["fetches"][sid]
            quote = spec["quotes"][sid]
            blob_path = root / fetch["path"]
            blob = blob_path.read_bytes() if blob_path.is_file() else b""
            digest = hashlib.sha256(blob).hexdigest() if blob else ""
            found = gate_quote(entry, sid)
            words = found.split() if found is not None else []
            row = row_for(sources, sid)
            ok = (
                found == quote
                and 1 <= len(words) <= 25
                and quote.encode() in blob
                and digest == fetch["sha256"]
                and row is not None
                and entry_rel in used_by(row)
            )
            if ok:
                closed_rows += 1
            else:
                open_cites += 1
                entry_closed = False
        if entry_closed:
            closed_entries += 1
    target = spec["target"]
    met = (
        closed_entries == target["closed_entries"]
        and closed_rows == target["closed_rows"]
        and open_cites == target["open_cites"]
    )
    verdict = "TARGET_MET" if met else "TARGET_MISSED"
    print(
        f"PRED-C1-r33-v1 closed_entries={closed_entries} closed_rows={closed_rows} "
        f"open_cites={open_cites} verdict={verdict}"
    )
    raise SystemExit(0 if met else 1)


if __name__ == "__main__":
    main()
