#!/usr/bin/env python3
"""Proposal, not a replacement: a document-anchored variant of PRED-C1-r35-v1.

REBUILT 2026-10-25 ~03:47 from this seat's transcript after an external sweep
removed all of .ufo/waves/round-35/scratch/ at ~03:45. Behaviour is unchanged.

The frozen predicate scores a row when its anchor cell *contains the receipt
digest*. It never asks whether the row names a document a reader can open, and
it never verifies a file-level digest or a line span. This checker adds those
checks, read-only, so the YAGNI surface becomes observable.

Two independent columns:
  A  source-names-document   the row's `source` tail resolves to a regular file
                             outside the fetch tree (a document, not a transcript)
  B  anchor-names-document   the `anchor` cell carries a digest for a non-receipt
                             file (e.g. `hypridle.conf sha256 <hex>`)
  V  digest-verified         every named file digest that resolves re-hashes equal
  L  line-span-in-file       the anchor's `lines N[-M]` fits the named document

Exit 0 only when every scored row has A or B. Usage:
  python3 -I propose_strict.py --root <lane>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
from pathlib import Path

FROZEN = Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/c1/frozen.json")
ROW_RE = re.compile(r"^ {0,3}\|\s*(S[0-9]+)\s*\|")
DIGEST_PAIR = re.compile(r"([\w./-]+) sha256 ([0-9a-f]{64})")
LINES = re.compile(r"lines? (\d+)(?:-(\d+))?")


def cells(line: str) -> list[str]:
    parts = line.split("|")
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [p.strip() for p in parts]


def is_receipt_path(text: str) -> bool:
    return "/fetch/" in text and text.endswith(".receipt.txt")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    spec = json.loads(FROZEN.read_text())
    rows: dict[str, list[str]] = {}
    for line in (root / "corpus/SOURCES.md").read_text().splitlines():
        m = ROW_RE.match(line)
        if m:
            rows.setdefault(m.group(1), []).append(line)

    bad = 0
    sids = [sid for ids in spec["entries"].values() for sid in ids]
    for sid in sids:
        cs = cells(rows[sid][0])
        src, anchor = cs[1], cs[5]
        tail = src.rsplit(" - ", 1)[-1].strip()
        col_a = bool(tail) and not is_receipt_path(tail) and (
            Path(tail).is_file() if tail.startswith("/") else (root / tail).is_file()
        )
        doc_pairs = [
            (name, digest) for name, digest in DIGEST_PAIR.findall(anchor)
            if not is_receipt_path(name) and name not in ("receipt",)
        ]
        col_b = bool(doc_pairs)
        # V: every named file digest must resolve and re-hash equal
        digests_ok = True
        resolved = 0
        doc_path = None
        if col_a:
            doc_path = Path(tail) if tail.startswith("/") else root / tail
        for name, digest in doc_pairs:
            cand = None
            if name == "file":
                cand = doc_path
            elif Path(name).is_absolute():
                cand = Path(name) if Path(name).is_file() else None
            elif doc_path and doc_path.name == Path(name).name:
                cand = doc_path
            elif (Path("/home/vgpnk/.config/hypr") / name).is_file():
                cand = Path("/home/vgpnk/.config/hypr") / name
            if cand is None:
                digests_ok = False  # a digest the checker cannot tie to bytes is unverified
                continue
            resolved += 1
            doc_path = doc_path or cand
            digests_ok = digests_ok and sha256_file(cand) == digest
        digests_ok = digests_ok and resolved >= 1
        # L: line span must fit the named document
        span_ok = True
        mlines = LINES.search(anchor)
        if doc_path and doc_path.is_file() and mlines:
            total = len(doc_path.read_text(errors="replace").splitlines())
            span_ok = int(mlines.group(2) or mlines.group(1)) <= total
        ok = (col_a or col_b) and digests_ok and span_ok
        print(
            f"{sid}  {'PASS' if ok else 'FAIL'}  A={int(col_a)} B={int(col_b)} "
            f"V={int(digests_ok)} L={int(span_ok)}"
        )
        bad += not ok
    print(f"document_anchored_rows={len(sids) - bad}/{len(sids)}")
    raise SystemExit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
