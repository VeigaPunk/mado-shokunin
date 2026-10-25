#!/usr/bin/env python3
"""Read-only source-class audit of S203-S210: document vs transcript.

Splits each row's `source` cell into its title and its trailing path, then
classifies the path: live document (regular file, outside the fetch tree),
fetch transcript (.ufo/waves/*/fetch/*), or unresolvable. Also reports whether
the row's `scope` is a proposition the receipt can address, as a hand-coded
column justified in the report (never inferred from the path class alone).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
IDS = [f"S{n}" for n in range(203, 211)]


def cells(line: str) -> list[str]:
    parts = line.split("|")
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [p.strip() for p in parts]


def main() -> None:
    rows = {}
    for line in (LANE / "corpus/SOURCES.md").read_text().splitlines():
        for sid in IDS:
            if line.lstrip().startswith(f"| {sid} |"):
                rows[sid] = cells(line)
    for sid in IDS:
        cs = rows[sid]
        src = cs[1]
        anchor = cs[5]
        # Path is the token after the last ' - ' in the source cell.
        tail = src.rsplit(" - ", 1)[-1].strip()
        if "/.ufo/waves/" in tail and "/fetch/" in tail:
            cls = "transcript"
        elif "ufo/waves/" in tail and "/fetch/" in tail:
            cls = "transcript"
        elif tail.startswith("/") or tail.startswith(".ufo") or tail.startswith("corpus"):
            cls = "document" if (LANE / tail).is_file() else "unresolvable"
        else:
            cls = "non-path"
        has_receipt_sha = ".ufo/waves/" in anchor and "receipt" in anchor
        print(f"{sid}  class={cls:12s} receipt_in_anchor={has_receipt_sha}  path={tail}")


if __name__ == "__main__":
    main()
