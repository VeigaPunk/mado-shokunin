#!/usr/bin/env python3
"""PRED-C1-r35-v1 counter. One command over a tree.

Contract: exit 0 TARGET_MET, 1 TARGET_MISSED, 2 usage or predicate drift.

PRED-C1-r35-v1: TARGET_MET iff closed_entries=3 AND closed_rows=8 AND open_cites=0,
where a frozen cite is closed only when the entry path is a regular file inside the
scored root, the registry holds exactly one well-formed row for that id whose used-by
token set is exactly the admitted entries citing it, whose status is `mined`, whose
recheck cell is a valid cadence token, whose cells contain no literal or escaped pipe,
and whose anchor cell carries the sha256 of the named receipt; and the entry carries
exactly one gate-quote line for that id whose quote is a contiguous substring of the
receipt bytes and is 1-25 words long.

The r34 clause `quote-equals-frozen` is NOT carried over: with a frozen quote the
1-25 word bound can never fail, so it was dead code under its own frozen spec. Here
the entry's quote is a free variable, so `gate-quote-word-bound` is failable and is
covered by a named control. The `S_ISLNK`/`O_NOFOLLOW` pair remains in `read_regular`
as TOCTOU-only defence in depth; it is NOT a load-bearing clause of this predicate
and is declared as such in c1/clauses.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

PREDICATE = (
    "PRED-C1-r35-v1: TARGET_MET iff closed_entries=3 AND closed_rows=8 AND open_cites=0, "
    "where a frozen cite is closed only when the entry path is a regular file inside the "
    "scored root, the registry holds exactly one well-formed row for that id whose used-by "
    "token set is exactly the admitted entries citing it, whose status is `mined`, whose "
    "recheck cell is a valid cadence token, whose cells contain no literal or escaped pipe, "
    "and whose anchor cell carries the sha256 of the named receipt; and the entry carries "
    "exactly one gate-quote line for that id whose quote is a contiguous substring of the "
    "receipt bytes and is 1-25 words long."
)
EXPECTED_TARGET = {"closed_entries": 3, "closed_rows": 8, "open_cites": 0}
MAX_BYTES = 8_000_000
ROW_RE = re.compile(r"^ {0,3}\|\s*(S[0-9]+)\s*\|")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CADENCE = re.compile(r"^\d+d$")
SYMBOLIC = re.compile(r"^[A-Za-z][A-Za-z0-9 _-]*$")


def die(msg: str) -> None:
    print(f"PRED-C1-r35-v1 error={msg}", file=sys.stderr)
    raise SystemExit(2)


def read_regular(root: Path, rel: str) -> bytes | None:
    """Read a file only if it is a regular, non-symlinked, single-link path inside root.

    The S_ISLNK walk and the O_NOFOLLOW open are TOCTOU-only defence in depth: they
    cannot kill a static tree, so they are not counted as load-bearing clauses.
    """
    if not rel or rel.startswith("/") or rel.startswith("\\"):
        return None
    parts = Path(rel).parts
    if not parts or any(p in ("", ".", "..") for p in parts):
        return None
    try:
        root_stat = root.lstat()
    except OSError:
        return None
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        return None
    cur = root
    for i, part in enumerate(parts):
        cur = cur / part
        try:
            st = cur.lstat()
        except OSError:
            return None
        if stat.S_ISLNK(st.st_mode):
            return None
        last = i == len(parts) - 1
        if not last:
            if not stat.S_ISDIR(st.st_mode):
                return None
            continue
        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
            return None
    try:
        fd = os.open(cur, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError:
        return None
    try:
        chunks: list[bytes] = []
        total = 0
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            total += len(block)
            if total > MAX_BYTES:
                return None
            chunks.append(block)
    finally:
        os.close(fd)
    return b"".join(chunks)


def cells(line: str) -> list[str]:
    parts = line.split("|")
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [p.strip() for p in parts]


def rows_for(sources: str, sid: str) -> list[str]:
    out = []
    for line in sources.splitlines():
        m = ROW_RE.match(line)
        if m and m.group(1) == sid:
            out.append(line)
    return out


def gate_quote(entry: str, sid: str) -> str | None:
    needle = f"gate-quote: {sid} "
    found = None
    for line in entry.splitlines():
        if line.startswith(needle):
            if found is not None:
                return None
            found = line[len(needle):]
    return found


def valid_recheck(cell: str) -> bool:
    """The census's own rule (scripts/sources-census.sh: E09): ISO date, NNd, or symbolic."""
    if ISO_DATE.match(cell):
        return True
    if CADENCE.match(cell):
        return True
    return bool(SYMBOLIC.match(cell))


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
    if spec.get("target") != EXPECTED_TARGET:
        die("target-drift")

    sources_bytes = read_regular(root, "corpus/SOURCES.md")
    sources = sources_bytes.decode("utf-8", "replace") if sources_bytes is not None else ""
    closed_entries = 0
    closed_rows = 0
    open_cites = 0
    for entry_rel, ids in spec["entries"].items():
        entry_bytes = read_regular(root, entry_rel)
        entry = entry_bytes.decode("utf-8", "replace") if entry_bytes is not None else ""
        entry_closed = entry_bytes is not None
        for sid in ids:
            receipt = spec["receipts"][sid]
            blob = read_regular(root, receipt["path"])
            digest = hashlib.sha256(blob).hexdigest() if blob is not None else ""
            quote = gate_quote(entry, sid)
            words = quote.split() if quote is not None else []
            rows = rows_for(sources, sid)
            row = rows[0] if len(rows) == 1 else None
            cs = cells(row) if row is not None else []
            nf_ok = len(cs) == 11
            used_by = set()
            if nf_ok and cs[10]:
                used_by = {t.strip() for t in cs[10].split(",") if t.strip()}
            citing = {rel for rel, rel_ids in spec["entries"].items() if sid in rel_ids}
            ok = (
                blob is not None
                and row is not None
                and nf_ok
                and used_by == citing
                and cs[7] == "mined"
                and valid_recheck(cs[9])
                and receipt["sha256"] in cs[5]
                and quote is not None
                and 1 <= len(words) <= 25
                and quote.encode() in blob
            )
            if ok:
                closed_rows += 1
            else:
                open_cites += 1
                entry_closed = False
        if entry_closed:
            closed_entries += 1
    met = (
        closed_entries == EXPECTED_TARGET["closed_entries"]
        and closed_rows == EXPECTED_TARGET["closed_rows"]
        and open_cites == EXPECTED_TARGET["open_cites"]
    )
    verdict = "TARGET_MET" if met else "TARGET_MISSED"
    print(
        f"PRED-C1-r35-v1 closed_entries={closed_entries} closed_rows={closed_rows} "
        f"open_cites={open_cites} verdict={verdict}"
    )
    raise SystemExit(0 if met else 1)


if __name__ == "__main__":
    main()
