#!/usr/bin/env python3
"""PRED-C1-r34-v1 counter. One command over a tree.

Contract: exit 0 TARGET_MET, 1 TARGET_MISSED, 2 usage or predicate drift.
Does not follow symlinks. A fetch or entry that is a symlink, a hardlink
(nlink!=1), or a path that leaves the scored root is not closed.

PRED-C1-r34-v1: TARGET_MET iff closed_entries=1 AND closed_rows=2 AND open_cites=0, where a frozen cite is closed only when the entry path and the fetch path are both regular files (not symlinks, nlink=1) whose every path component stays inside the scored root, the fetch bytes read with O_NOFOLLOW have sha256 equal to the digest in c1/frozen.json, the entry contains a 1-25 word gate-quote line for that id that is a contiguous substring of those bytes, and the registry row for that id lists the entry path as a whole used-by token.
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
    "PRED-C1-r34-v1: TARGET_MET iff closed_entries=1 AND closed_rows=2 AND open_cites=0, "
    "where a frozen cite is closed only when the entry path and the fetch path are both "
    "regular files (not symlinks, nlink=1) whose every path component stays inside the "
    "scored root, the fetch bytes read with O_NOFOLLOW have sha256 equal to the digest in "
    "c1/frozen.json, the entry contains a 1-25 word gate-quote line for that id that is a "
    "contiguous substring of those bytes, and the registry row for that id lists the entry "
    "path as a whole used-by token."
)
EXPECTED_TARGET = {"closed_entries": 1, "closed_rows": 2, "open_cites": 0}
MAX_BYTES = 8_000_000
ROW_RE = re.compile(r"^ {0,3}\|\s*(S[0-9]+)\s*\|")


def die(msg: str) -> None:
    print(f"PRED-C1-r34-v1 error={msg}", file=sys.stderr)
    raise SystemExit(2)


def read_regular(root: Path, rel: str) -> bytes | None:
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


def used_by_tokens(line: str) -> set[str]:
    parts = [p.strip() for p in line.split("|")]
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    if not parts:
        return set()
    return {t.strip() for t in parts[-1].split(",") if t.strip()}


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
            fetch = spec["fetches"][sid]
            quote = spec["quotes"][sid]
            blob = read_regular(root, fetch["path"])
            digest = hashlib.sha256(blob).hexdigest() if blob is not None else ""
            found = gate_quote(entry, sid)
            words = found.split() if found is not None else []
            rows = rows_for(sources, sid)
            ok = (
                blob is not None
                and found == quote
                and 1 <= len(words) <= 25
                and quote.encode() in blob
                and digest == fetch["sha256"]
                and len(rows) == 1
                and used_by_tokens(rows[0]) == {entry_rel}
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
        f"PRED-C1-r34-v1 closed_entries={closed_entries} closed_rows={closed_rows} "
        f"open_cites={open_cites} verdict={verdict}"
    )
    raise SystemExit(0 if met else 1)


if __name__ == "__main__":
    main()
