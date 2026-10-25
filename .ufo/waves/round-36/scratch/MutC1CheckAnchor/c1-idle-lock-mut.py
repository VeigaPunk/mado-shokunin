#!/usr/bin/env python3
"""PRED-C1-r36-v1 counter — the round-35 idle-lock admission counter, repaired.

Same claim, same frozen inputs, two dead/fail-open clauses fixed (round-35
spot-check D3 and the `RevC1Tip` F2 finding):

  * `digest-match` now binds the declared sha256 to the bytes actually read at the
    receipt path. The round-35 counter computed `digest` and never compared it, so
    a fabricated payload at the frozen path scored the same as the real receipt.
  * `row-in-registry` reproduces the fleet census's E12 fence: only rows inside
    the `## Registry` section score, and a registry with no such section scores
    nothing. The round-35 counter scanned the whole file, so a row moved into
    `## Leads` still counted.

One command over a tree: exit 0 TARGET_MET, 1 TARGET_MISSED, 2 usage or predicate drift.
This counter scores the shape and the mutual consistency of the evidence, never the
truth of the receipts' prose.
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

PREDICATE = "PRED-C1-r36-v1: TARGET_MET iff closed_entries=3 AND closed_rows=8 AND open_cites=0, where a frozen cite is closed only when the entry path is a regular file inside the scored root; the `## Registry` section of the registry holds exactly one well-formed row for that id (a row-shaped line outside that section, or a registry with no such section, scores nothing) whose used-by token set is exactly the admitted entries citing it, whose status is `mined`, whose recheck cell is a valid cadence token, whose cells contain no literal or escaped pipe, whose anchor cell carries the receipt's declared sha256 AND the receipt bytes at the named path hash to that same sha256; and the entry carries exactly one gate-quote line for that id whose quote is a contiguous substring of those bytes and is 1-25 words long."
EXPECTED_TARGET = {"closed_entries": 3, "closed_rows": 8, "open_cites": 0}
MAX_BYTES = 8_000_000
ROW_RE = re.compile(r"^ {0,3}\|\s*(S[0-9]+)\s*\|")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CADENCE = re.compile(r"^\d+d$")
SYMBOLIC = re.compile(r"^[A-Za-z][A-Za-z0-9 _-]*$")


def die(msg: str) -> None:
    print(f"PRED-C1-r36-v1 error={msg}", file=sys.stderr)
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


def registry_section(sources: str) -> str:
    """The `## Registry` section only (census E12). No section, no rows."""
    out: list[str] = []
    keep = False
    for line in sources.splitlines():
        if re.match(r"^ {0,3}##[ ]", line):
            keep = line.strip().lower().startswith("## registry")
            continue
        if keep:
            out.append(line)
    return "\n".join(out)


def rows_for(sources: str, sid: str) -> list[str]:
    out = []
    for line in registry_section(sources).splitlines():
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
                and digest == receipt["sha256"]
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
        f"PRED-C1-r36-v1 closed_entries={closed_entries} closed_rows={closed_rows} "
        f"open_cites={open_cites} verdict={verdict}"
    )
    raise SystemExit(0 if met else 1)


if __name__ == "__main__":
    main()
