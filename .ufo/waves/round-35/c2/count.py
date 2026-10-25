#!/usr/bin/env python3
"""PRED-C2-r35-v1 counter. One command over committed bytes.

Contract: exit 0 TARGET_MET, 1 TARGET_MISSED, 2 usage or predicate drift.

PRED-C2-r35-v1: TARGET_MET iff uncovered=0 AND retired=1 AND toctou_declared=1 AND
ledger_tip_ok=1, where

  uncovered      counts live clauses of the round-35 admission counter that carry
                 neither a named control whose committed receipt records a
                 TARGET_MISSED verdict, nor a `not-load-bearing` declaration with a
                 reason;
  retired        counts live clause ids listed as retired in the ledger whose id is
                 absent from the live clause list (the r34 `quote-equals-frozen`
                 clause, dead code under its own frozen spec);
  toctou_declared counts live clauses carrying a `not-load-bearing` declaration with
                 a reason — exactly the S_ISLNK/O_NOFOLLOW pair, which no static tree
                 can kill, so it is never counted as a load-bearing clause;
  ledger_tip_ok  is 1 when the round-35 frozen-blob ledger names the round-34 tip
                 dff394109f3cc3d851309ad7c67dd3b35b46adf2 and every frozen blob it
                 lists re-verifies by git blob id at that revision.

This counter scores the lane's self-description of its own evidence, not the corpus.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

PREDICATE = (
    "PRED-C2-r35-v1: TARGET_MET iff uncovered=0 AND retired=1 AND toctou_declared=1 AND "
    "ledger_tip_ok=1, where uncovered counts live clauses of the round-35 admission "
    "counter that carry neither a named control whose committed receipt records a "
    "TARGET_MISSED verdict, nor a `not-load-bearing` declaration with a reason; retired "
    "counts live clause ids listed as retired in the ledger whose id is absent from the "
    "live clause list (the r34 `quote-equals-frozen` clause, dead code under its own "
    "frozen spec); toctou_declared counts live clauses carrying a `not-load-bearing` "
    "declaration with a reason — exactly the S_ISLNK/O_NOFOLLOW pair, which no static "
    "tree can kill, so it is never counted as a load-bearing clause; ledger_tip_ok is 1 "
    "when the round-35 frozen-blob ledger names the round-34 tip "
    "dff394109f3cc3d851309ad7c67dd3b35b46adf2 and every frozen blob it lists "
    "re-verifies by git blob id at that revision."
)
EXPECTED_TARGET = {"uncovered": 0, "retired": 1, "toctou_declared": 1, "ledger_tip_ok": 1}
MISSED = re.compile(r"verdict=TARGET_MISSED")


def die(msg: str) -> None:
    print(f"PRED-C2-r35-v1 error={msg}", file=sys.stderr)
    raise SystemExit(2)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--frozen", required=True)
    args = ap.parse_args()
    repo = Path(args.repo)
    frozen_path = Path(args.frozen)
    if not frozen_path.is_file():
        die("frozen-missing")
    spec = json.loads(frozen_path.read_text())
    if spec.get("predicate") != PREDICATE:
        die("predicate-drift")
    if spec.get("target") != EXPECTED_TARGET:
        die("target-drift")

    ledger_path = repo / spec["clause_ledger"]
    if not ledger_path.is_file():
        die("clause-ledger-missing")
    ledger = json.loads(ledger_path.read_text())
    live = ledger["live"]
    retired = ledger.get("retired", [])
    live_ids = {c["id"] for c in live}

    uncovered = 0
    for clause in live:
        nl = clause.get("not-load-bearing")
        if nl and nl.get("reason"):
            continue
        control = clause.get("control")
        if not control:
            uncovered += 1
            continue
        receipt = repo / control["receipt"]
        if not receipt.is_file() or not MISSED.search(receipt.read_text()):
            uncovered += 1

    retired_count = 0
    for clause in retired:
        if clause["id"] not in live_ids:
            retired_count += 1

    declared = [c["id"] for c in live if (c.get("not-load-bearing") or {}).get("reason")]
    toctou_declared = 1 if declared == [spec["toctou_clause"]] else 0

    ledger_tip_ok = 0
    ledger_doc = repo / spec["blob_ledger"]
    if ledger_doc.is_file():
        text = ledger_doc.read_text()
        if spec["r34_tip"] in text:
            ok = True
            for blob in spec["frozen_blobs"]:
                rev_path = f"{spec['r34_tip']}:{blob['path']}"
                try:
                    raw = subprocess.run(
                        ["git", "-C", str(repo), "rev-parse", rev_path],
                        capture_output=True,
                        check=True,
                        text=True,
                    ).stdout.strip()
                except subprocess.CalledProcessError:
                    ok = False
                    break
                if raw != blob["blob_id"]:
                    ok = False
                    break
            if ok:
                ledger_tip_ok = 1

    observed = {
        "uncovered": uncovered,
        "retired": retired_count,
        "toctou_declared": toctou_declared,
        "ledger_tip_ok": ledger_tip_ok,
    }
    met = all(observed[k] == EXPECTED_TARGET[k] for k in EXPECTED_TARGET)
    verdict = "TARGET_MET" if met else "TARGET_MISSED"
    print(
        "PRED-C2-r35-v1 uncovered={uncovered} retired={retired} "
        "toctou_declared={toctou_declared} ledger_tip_ok={ledger_tip_ok} "
        "verdict={verdict}".format(verdict=verdict, **observed)
    )
    raise SystemExit(0 if met else 1)


if __name__ == "__main__":
    main()
