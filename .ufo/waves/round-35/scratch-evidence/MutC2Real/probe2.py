#!/usr/bin/env python3
"""Follow-up probes on the dead observable found by M3a.

M3c: stale tip label in every prose occurrence, keeping only the hash inside the
     recorded re-derivation command (a doc that names the wrong tip everywhere but
     still prints the right hash in its repro snippet).
M3d: corrupt one blob id in the ledger's frozen-blob table (the doc's own claim),
     leaving every other byte alone.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent / "repo"
COUNTER = ".ufo/waves/round-35/c2/count.py"
LEDGER = ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md"
TIP = "dff394109f3cc3d851309ad7c67dd3b35b46adf2"
STALE = "fa7ba11346116672352b5d41494141c5c4d738d0"
TABLE_BLOB = "4ab3db435dd2e396402d1d83039e35082f1138fe"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def detect() -> tuple[str, int]:
    r = subprocess.run(
        [sys.executable, "-I", COUNTER, "--repo", str(REPO), "--frozen",
         ".ufo/waves/round-35/c2/frozen.json"],
        cwd=REPO, capture_output=True, text=True,
    )
    return r.stdout.strip(), r.returncode


def m3c_stale_prose_keep_repro(raw: bytes) -> bytes:
    text = raw.decode()
    lines = text.splitlines(keepends=True)
    code_fence = False
    out = []
    for line in lines:
        if line.lstrip().startswith("```"):
            code_fence = not code_fence
            out.append(line)
            continue
        if not code_fence:
            line = line.replace(TIP, STALE)
        out.append(line)
    return "".join(out).encode()


def m3d_corrupt_table_blob(raw: bytes) -> bytes:
    text = raw.decode()
    assert TABLE_BLOB in text
    return text.replace(TABLE_BLOB, "0" * 40, 1).encode()


CASES = [
    ("M3c-stale-label-except-repro", m3c_stale_prose_keep_repro),
    ("M3d-corrupt-table-blob-id", m3d_corrupt_table_blob),
]


def main() -> None:
    target = REPO / LEDGER
    for name, fn in CASES:
        before = target.read_bytes()
        before_sha = hashlib.sha256(before).hexdigest()
        pre, pre_c = detect()
        target.write_bytes(fn(before))
        mut_sha = sha(target)
        mut, mut_c = detect()
        target.write_bytes(before)
        after_sha = sha(target)
        post, post_c = detect()
        print(f"## {name}")
        print(f"   before {before_sha}")
        print(f"   mutant {mut_sha}")
        print(f"   detector(pristine)  exit={pre_c} {pre}")
        print(f"   detector(mutant)    exit={mut_c} {mut}")
        print(f"   restored {after_sha} identical={after_sha == before_sha}")
        print(f"   detector(restored)  exit={post_c} {post}")
        print()
    # show that the surviving mutants still contain the tip hash somewhere
    m3c = m3c_stale_prose_keep_prose = m3c_stale_prose_keep_repro((REPO / LEDGER).read_bytes())
    print("tip occurrences in M3c mutant:", m3c.decode().count(TIP))
    print("stale occurrences in M3c mutant:", m3c.decode().count(STALE))


if __name__ == "__main__":
    main()
