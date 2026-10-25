#!/usr/bin/env python3
"""Standalone reproducer for the SimplifyRows findings (round 35, wave 2).

Run from the lane root:   python3 -I simplifyrows_repro.py
Prints: (1) the frozen C1 baseline, (2) a deletion proof, (3) a source-class
audit of the eight scored rows. Exit 0 iff every expectation holds.
Writes only under a tempdir; the lane is read-only.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path.cwd()
C1 = LANE / ".ufo/waves/round-35/c1/count.py"
FROZEN = LANE / ".ufo/waves/round-35/c1/frozen.json"
SRC = "corpus/SOURCES.md"
ROW = re.compile(r"^ {0,3}\|\s*(S[0-9]+)\s*\|")
DIGEST = re.compile(r"([\w./-]+) sha256 ([0-9a-f]{64})")


def cells(line: str) -> list[str]:
    parts = line.split("|")
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [p.strip() for p in parts]


def run(root: Path) -> tuple[str, int]:
    proc = subprocess.run(
        [sys.executable, "-I", str(C1), "--root", str(root), "--frozen", str(FROZEN)],
        capture_output=True, text=True,
    )
    return (proc.stdout.strip() + proc.stderr.strip()).strip(), proc.returncode


def main() -> int:
    ok = True

    out, rc = run(LANE)
    print(f"[baseline] exit={rc} {out}")
    ok &= rc == 0 and "closed_rows=8" in out and "TARGET_MET" in out

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        shutil.copytree(LANE / "corpus", root / "corpus")
        shutil.copytree(LANE / ".ufo/waves/round-35/fetch", root / ".ufo/waves/round-35/fetch")
        p = root / SRC
        lines = p.read_text().splitlines(keepends=True)
        p.write_text("".join(l for l in lines if not l.lstrip().startswith("| S204 |")))
        out2, rc2 = run(root)
        print(f"[drop S204] exit={rc2} {out2}")
        ok &= rc2 == 1 and "closed_rows=7" in out2 and "open_cites=1" in out2

    rows: dict[str, list[str]] = {}
    for line in (LANE / SRC).read_text().splitlines():
        m = ROW.match(line)
        if m:
            rows.setdefault(m.group(1), []).append(cells(line))
    sids = [sid for ids in json.loads(FROZEN.read_text())["entries"].values() for sid in ids]
    transcript_only = []
    for sid in sids:
        cs = rows[sid][0]
        src, anchor = cs[1], cs[5]
        tail = src.rsplit(" - ", 1)[-1].strip()
        is_transcript = "/fetch/" in tail and tail.endswith(".receipt.txt")
        doc_digest = [
            n for n, _ in DIGEST.findall(anchor)
            if not n.endswith(".receipt.txt") and n != "receipt"
        ]
        doc_source = (not is_transcript) and (
            Path(tail).is_file() if tail.startswith("/") else (LANE / tail).is_file()
        )
        if not (doc_source or doc_digest):
            transcript_only.append(sid)
        print(
            f"[audit] {sid} source={'transcript' if is_transcript else 'document'} "
            f"document_digest={int(bool(doc_digest))}"
        )
    print(f"[audit] transcript-only rows: {' '.join(transcript_only)}")
    ok &= transcript_only == ["S204", "S209", "S210"]

    print("REPRO", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
