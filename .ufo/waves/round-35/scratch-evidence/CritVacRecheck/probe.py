#!/usr/bin/env python3
"""Dump the tuple PRED-C1-r35-v1 actually reads, for a given --root.

Replicates c1/count.py's read path (read_regular eligibility, rows_for, cells,
gate_quote, valid_recheck) and prints, per cite, only the values the predicate
compares. Two trees with the same dump are indistinguishable to the counter.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SPEC = json.loads(Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/c1/frozen.json").read_text())
ROW_RE = re.compile(r"^ {0,3}\|\s*(S[0-9]+)\s*\|")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CADENCE = re.compile(r"^\d+d$")
SYMBOLIC = re.compile(r"^[A-Za-z][A-Za-z0-9 _-]*$")


def cells(line):
    parts = line.split("|")
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [p.strip() for p in parts]


def valid_recheck(c):
    return bool(ISO_DATE.match(c) or CADENCE.match(c) or SYMBOLIC.match(c))


def gate_quote(entry, sid):
    needle = f"gate-quote: {sid} "
    found = None
    for line in entry.splitlines():
        if line.startswith(needle):
            if found is not None:
                return None
            found = line[len(needle):]
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    root = Path(a.root)
    sources = (root / "corpus/SOURCES.md").read_text(errors="replace")
    for entry_rel, ids in SPEC["entries"].items():
        p = root / entry_rel
        entry = p.read_text(errors="replace") if p.is_file() else ""
        for sid in ids:
            receipt = SPEC["receipts"][sid]
            rp = root / receipt["path"]
            blob = rp.read_bytes() if rp.is_file() else None
            quote = gate_quote(entry, sid)
            words = quote.split() if quote is not None else []
            rows = [l for l in sources.splitlines() if (m := ROW_RE.match(l)) and m.group(1) == sid]
            row = rows[0] if len(rows) == 1 else None
            cs = cells(row) if row is not None else []
            used_by = sorted(t.strip() for t in cs[10].split(",") if t.strip()) if len(cs) == 11 and cs[10] else []
            citing = sorted(rel for rel, rids in SPEC["entries"].items() if sid in rids)
            ok = (blob is not None and row is not None and len(cs) == 11
                  and used_by == citing and cs[7] == "mined" and valid_recheck(cs[9])
                  and receipt["sha256"] in cs[5] and quote is not None
                  and 1 <= len(words) <= 25 and quote.encode() in blob)
            print(json.dumps({
                "cite": sid,
                "entry": entry_rel,
                "entry_is_file": p.is_file(),
                "rows_for_id": len(rows),
                "nf_cells": len(cs),
                "status": cs[7] if len(cs) == 11 else None,
                "recheck_valid": valid_recheck(cs[9]) if len(cs) == 11 else None,
                "frozen_sha_in_anchor": (receipt["sha256"] in cs[5]) if len(cs) == 11 else None,
                "used_by_equals_citing": used_by == citing,
                "quote_words": len(words),
                "quote_in_blob": (blob is not None and quote is not None and quote.encode() in blob),
                "ok": ok,
            }, sort_keys=True))


if __name__ == "__main__":
    main()
