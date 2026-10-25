#!/usr/bin/env python3
"""Mutation probe driver for PRED-C2-r35-v1 against an isolated scratch clone.

For each mutant: hash pristine bytes, apply one mutation, run the detector,
restore exact pristine bytes, hash again, re-run the detector.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent / "repo"
COUNTER = ".ufo/waves/round-35/c2/count.py"
FROZEN = ".ufo/waves/round-35/c2/frozen.json"
CLAUSES = ".ufo/waves/round-35/c1/clauses.json"
LEDGER = ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md"
RECEIPT = ".ufo/waves/round-35/controls/c1-entry-symlink.txt"
TIP = "dff394109f3cc3d851309ad7c67dd3b35b46adf2"
STALE = "fa7ba11346116672352b5d41494141c5c4d738d0"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def detect() -> tuple[str, int]:
    r = subprocess.run(
        [sys.executable, "-I", COUNTER, "--repo", str(REPO), "--frozen", FROZEN],
        cwd=REPO, capture_output=True, text=True,
    )
    out = r.stdout.strip()
    if r.stderr.strip():
        out += " | stderr=" + r.stderr.strip()
    return out, r.returncode


def load_clauses():
    return json.loads((REPO / CLAUSES).read_text())


# ---- mutations: each takes the pristine bytes of the target file, returns mutant bytes ----

def m1_remove_missed_text(raw: bytes) -> bytes:
    text = raw.decode()
    assert " verdict=TARGET_MISSED" in text
    return text.replace(" verdict=TARGET_MISSED", "", 1).encode()


def m2_drop_reason(raw: bytes) -> bytes:
    data = json.loads(raw)
    for clause in data["live"]:
        if clause.get("not-load-bearing"):
            clause["not-load-bearing"]["reason"] = ""
    return json.dumps(data, indent=1).encode()


def m3a_alter_one_tip_label(raw: bytes) -> bytes:
    text = raw.decode()
    needle = "- Round-34 lane tip = `master` = `" + TIP + "`"
    assert needle in text
    return text.replace(needle, "- Round-34 lane tip = `master` = `" + STALE + "`", 1).encode()


def m3b_alter_all_tip_labels(raw: bytes) -> bytes:
    text = raw.decode()
    assert text.count(TIP) >= 1
    return text.replace(TIP, STALE).encode()


def m4_second_not_load_bearing(raw: bytes) -> bytes:
    data = json.loads(raw)
    for clause in data["live"]:
        if clause["id"] == "row-unique":
            clause["not-load-bearing"] = {
                "reason": "Mutation probe: declares a second non-load-bearing clause."
            }
    return json.dumps(data, indent=1).encode()


CASES = [
    ("M1-remove-control-missed-text", RECEIPT, m1_remove_missed_text),
    ("M2-drop-not-load-bearing-reason", CLAUSES, m2_drop_reason),
    ("M3a-alter-single-tip-label", LEDGER, m3a_alter_one_tip_label),
    ("M3b-alter-all-tip-labels", LEDGER, m3b_alter_all_tip_labels),
    ("M4-add-second-not-load-bearing", CLAUSES, m4_second_not_load_bearing),
]


def main() -> None:
    pristine = {p: sha(REPO / p) for _, p, _ in CASES}
    print("== pristine detector runs ==")
    for p in pristine:
        out, code = detect()
        print(f"  [{p}] {pristine[p][:16]} -> {out} exit={code}")
        break  # same counter state for all pristine files; one run suffices
    print()
    for name, rel, fn in CASES:
        target = REPO / rel
        before = target.read_bytes()
        before_sha = hashlib.sha256(before).hexdigest()
        pre_out, pre_code = detect()
        mutant = fn(before)
        target.write_bytes(mutant)
        mut_sha = sha(target)
        mut_out, mut_code = detect()
        target.write_bytes(before)
        after_sha = sha(target)
        post_out, post_code = detect()
        print(f"## {name}  [{rel}]")
        print(f"   before {before_sha}")
        print(f"   mutant {mut_sha}  ({len(mutant)} bytes, delta {len(mutant)-len(before)})")
        print(f"   detector(pristine)  exit={pre_code} {pre_out}")
        print(f"   detector(mutant)    exit={mut_code} {mut_out}")
        print(f"   restored {after_sha}  identical={after_sha == before_sha}")
        print(f"   detector(restored)  exit={post_code} {post_out}")
        print()


if __name__ == "__main__":
    main()
