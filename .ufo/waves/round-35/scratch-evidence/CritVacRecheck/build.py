#!/usr/bin/env python3
"""CritVacRecheck: build differential trees from the REAL round-35 corpus.

Reads the lane tree read-only. Writes ONLY under
.ufo/waves/round-35/scratch/CritVacRecheck/<arm>/.

Arms:
  T0-real-copy            byte-identical copy of the 12 scored inputs
  T1-prose-deleted        entries = only their gate-quote lines
  T2-receipts-replaced    receipts same length, every byte outside the cited
                          gate-quote span different (quote span preserved)
  T3-both                 T1 + T2  (the assignment's headline copy)
  T4-receipts-all-diff    receipts same length, EVERY byte different (quote
                          destroyed) -> isolates the one receipt-content the
                          counter can see
  T5-both-all-diff        T1 + T4
  T6-unread-junk          all c1-unread row cells (0-4,6,8) = "junk"; entry prose
                          replaced by junk lines; checked cells and receipts real

Also emits manifest.json with per-receipt length / sha256 / differing-byte
counts and quote presence, so every claim below is backed by numbers.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
SCRATCH = LANE / ".ufo/waves/round-35/scratch/CritVacRecheck"
SPEC = json.loads((LANE / ".ufo/waves/round-35/c1/frozen.json").read_text())


def q(text: str, sid: str) -> str:
    """Replica of c1/count.py gate_quote (same startswith rule, same return)."""
    needle = f"gate-quote: {sid} "
    found = None
    for line in text.splitlines():
        if line.startswith(needle):
            if found is not None:
                return None
            found = line[len(needle):]
    return found


def transform(data: bytes, keep: tuple[int, int] | None) -> bytes:
    """Same length. Byte i -> ASCII letter, guaranteed different from data[i]."""
    out = bytearray()
    for i, b in enumerate(data):
        if keep is not None and keep[0] <= i < keep[1]:
            out.append(b)
            continue
        c = 0x41 + ((b * 7 + 13 + i) % 26)
        if c == b:
            c = 0x42 if b != 0x42 else 0x43
        out.append(c)
    assert len(out) == len(data)
    if keep is None:
        return bytes(out)
    assert all(out[i] != data[i] for i in range(len(data)) if not (keep[0] <= i < keep[1]))
    return bytes(out)


def copy_real(dst: Path) -> None:
    (dst / "corpus/knowledge").mkdir(parents=True)
    (dst / ".ufo/waves/round-35/fetch").mkdir(parents=True)
    shutil.copyfile(LANE / "corpus/SOURCES.md", dst / "corpus/SOURCES.md")
    for entry in SPEC["entries"]:
        shutil.copyfile(LANE / entry, dst / entry)
    for sid, r in SPEC["receipts"].items():
        shutil.copyfile(LANE / r["path"], dst / r["path"])


def squash_prose(dst: Path, junk: bool) -> None:
    for entry, ids in SPEC["entries"].items():
        text = (LANE / entry).read_text()
        lines = [ln for ln in text.splitlines() if ln.startswith("gate-quote: ")]
        if junk:
            lines = ["JUNK PROSE LINE - asserts nothing, cites nothing."] + lines
        (dst / entry).write_text("\n".join(lines) + "\n")


def junk_row_cells(dst: Path) -> None:
    src = (LANE / "corpus/SOURCES.md").read_text().splitlines()
    out = []
    for line in src:
        parts = line.split("|")
        lead = parts and parts[0] == ""
        if lead:
            parts = parts[1:]
        tail = parts and parts[-1] == ""
        if tail:
            parts = parts[:-1]
        cells = [p.strip() for p in parts]
        if len(cells) == 11 and cells[0] in SPEC["receipts"]:
            # cell 0 is the id (read by ROW_RE); cells 5,7,9,10 are checked.
            for i in (1, 2, 3, 4, 6, 8):
                cells[i] = "junk"
            line = "| " + " | ".join(cells) + " |"
        out.append(line)
    (dst / "corpus/SOURCES.md").write_text("\n".join(out) + "\n")


def build_arm(name: str, prose: str, receipts: str) -> dict:
    dst = SCRATCH / name
    if dst.exists():
        shutil.rmtree(dst)
    copy_real(dst)
    if prose == "deleted":
        squash_prose(dst, junk=False)
    elif prose == "junk":
        squash_prose(dst, junk=True)
    if prose == "junk":
        junk_row_cells(dst)

    manifest = {"arm": name, "receipts": {}, "entries": {}}
    for entry, ids in SPEC["entries"].items():
        raw = (LANE / entry).read_bytes()
        new = (dst / entry).read_bytes()
        manifest["entries"][entry] = {
            "real_bytes": len(raw),
            "arm_bytes": len(new),
            "gate_quotes": [q(raw.decode(), s) for s in ids],
            "non_quote_lines": [ln for ln in new.decode().splitlines()
                                if not ln.startswith("gate-quote: ")],
        }
    for sid, r in SPEC["receipts"].items():
        entry = next(e for e, ids in SPEC["entries"].items() if sid in ids)
        quote = q((LANE / entry).read_text(), sid)
        assert quote is not None, (sid, "no gate quote in real entry")
        real = (LANE / r["path"]).read_bytes()
        qb = quote.encode()
        occurrences = real.count(qb)
        span = None
        if receipts == "replaced":
            idx = real.find(qb)
            assert idx >= 0, (sid, "quote not a substring of real receipt")
            span = (idx, idx + len(qb))
            new = transform(real, keep=span)
        elif receipts == "all-diff":
            new = transform(real, keep=None)
        else:
            new = real
        (dst / r["path"]).write_bytes(new)
        diff = sum(1 for a, b in zip(real, new) if a != b)
        manifest["receipts"][sid] = {
            "path": r["path"],
            "real_bytes": len(real),
            "arm_bytes": len(new),
            "length_preserved": len(real) == len(new),
            "diff_bytes": diff,
            "diff_pct_of_unchanged": round(100.0 * diff / max(len(real), 1), 1),
            "quote_occurrences_real": occurrences,
            "quote_in_arm": qb in new,
            "sha256_real": hashlib.sha256(real).hexdigest(),
            "sha256_arm": hashlib.sha256(new).hexdigest(),
            "sha256_frozen": r["sha256"],
            "sha256_matches_frozen_real": hashlib.sha256(real).hexdigest() == r["sha256"],
            "sha256_matches_frozen_arm": hashlib.sha256(new).hexdigest() == r["sha256"],
        }
    return manifest


def main() -> None:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    plans = [
        ("T0-real-copy", "kept", "kept"),
        ("T1-prose-deleted", "deleted", "kept"),
        ("T2-receipts-replaced", "kept", "replaced"),
        ("T3-both", "deleted", "replaced"),
        ("T4-receipts-all-diff", "kept", "all-diff"),
        ("T5-both-all-diff", "deleted", "all-diff"),
        ("T6-unread-junk", "junk", "kept"),
    ]
    manifests = {}
    for name, prose, receipts in plans:
        manifests[name] = build_arm(name, prose, receipts)
        print("built", name)
    (SCRATCH / "manifest.json").write_text(json.dumps(manifests, indent=1, sort_keys=True))
    print("wrote", SCRATCH / "manifest.json")


if __name__ == "__main__":
    main()
