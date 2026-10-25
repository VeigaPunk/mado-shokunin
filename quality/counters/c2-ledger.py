#!/usr/bin/env python3
"""PRED-C2-r36-v1 counter — the lane's evidence ledger, repaired against its own fail-opens.

Three observables of the round-35 counter were shown vacuous by the round-35
wave-2 seats and the closure spot-check (D4):

  * `uncovered` iterated the ledger's own `live` list, so deleting a clause and its
    control deleted the obligation with it. The live id set is now pinned by the
    frozen spec and must match exactly.
  * A "covered" clause only needed `verdict=TARGET_MISSED` to appear anywhere in a
    receipt file, so a one-line token file covered a clause. A receipt now counts
    only when it records `observed=TARGET_MISSED`, names the clause, and belongs to
    the control the clause names.
  * `ledger_tip_ok` was a substring test over prose plus a hardcoded tip. The tip is
    now computed from git by one frozen rule (the newest commit whose subject names
    `round-34`), every tip-labelled 40-hex token in the blob ledger must equal it
    (lines naming `supersedes` exempt, at least three such lines required), and the
    ledger's own table is parsed: its row set must equal the frozen path set and
    every row's blob id must re-derive at the computed tip.

Contract: exit 0 TARGET_MET, 1 TARGET_MISSED, 2 usage or predicate drift.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

PREDICATE = "PRED-C2-r36-v1: TARGET_MET iff uncovered=0 AND retired=1 AND tip_ok=1, where the clause ledger's live id set equals the frozen expected live id set exactly, so a deleted clause is uncovered and never silently skipped; each live load-bearing clause must name a control whose committed receipt in the frozen receipt directory records TARGET_MISSED and names that clause id, so a receipt that does not name its clause, or a one-line token file, does not cover it; exactly one live clause may carry a `not-load-bearing` declaration with a reason and it must be the frozen toctou clause; retired counts retired clause ids that are absent from the live set; and tip_ok is 1 when the round-34 tip is computed from git by the frozen rule (the newest commit whose subject names `round-34`), the blob ledger names the superseded round-35 ledger, every 40-hex token on a line naming a tip (other than a line containing `supersedes`) equals the computed tip with at least three such lines, and every table row of the blob ledger names a frozen path whose blob id at the computed tip equals the id in the row, with the row set equal to the frozen path set."
EXPECTED_TARGET = {"uncovered": 0, "retired": 1, "tip_ok": 1}
HEX40 = re.compile(r"\b[0-9a-f]{40}\b")
TIP = re.compile(r"tip", re.I)
ROW = re.compile(r"^\s*\|\s*`([^`]+)`\s*\|\s*`?([0-9a-f]{40})`?\s*\|")


def die(msg: str) -> None:
    print(f"PRED-C2-r36-v1 error={msg}", file=sys.stderr)
    raise SystemExit(2)


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    return proc.stdout if proc.returncode == 0 else ""


def compute_tip(repo: Path, rule: dict) -> str:
    for line in git(repo, "log", "--format=%H%x00%s").splitlines():
        sha, _, subject = line.partition("\x00")
        if rule["subject_pattern"] in subject:
            return sha.strip()
    return ""


def tip_observable(repo: Path, spec: dict) -> tuple[int, list[str]]:
    detail: list[str] = []
    rule = spec["tip_rule"]
    tip = compute_tip(repo, rule)
    if not HEX40.match(tip or ""):
        return 0, ["tip: rule produced no commit"]
    doc_path = repo / spec["blob_ledger"]
    if not doc_path.is_file():
        return 0, ["tip: blob ledger missing"]
    doc = doc_path.read_text()
    if spec["superseded_ledger"] not in doc:
        return 0, ["tip: ledger does not name the superseded round-35 ledger"]
    lines = [ln for ln in doc.splitlines()
             if TIP.search(ln) and HEX40.search(ln) and "supersedes" not in ln.lower()]
    if len(lines) < rule["min_tip_lines"]:
        return 0, [f"tip: {len(lines)} tip lines, minimum {rule['min_tip_lines']}"]
    for ln in lines:
        bad = [h for h in HEX40.findall(ln) if h != tip]
        if bad:
            return 0, [f"tip: stale token {bad[0]} on: {ln.strip()[:90]}"]
    rows = [ROW.match(ln) for ln in doc.splitlines()]
    rows = [m for m in rows if m]
    seen = []
    for m in rows:
        path, blob = m.group(1).strip(), m.group(2)
        if path not in spec["frozen_blobs"]:
            return 0, [f"tip: row path not frozen: {path}"]
        seen.append(path)
        derived = git(repo, "rev-parse", f"{tip}:{path}").strip()
        if derived != blob:
            return 0, [f"tip: blob drift {path}: doc {blob} tip {derived or 'absent'}"]
    if sorted(seen) != sorted(spec["frozen_blobs"]):
        missing = sorted(set(spec["frozen_blobs"]) - set(seen))
        return 0, [f"tip: row set differs, missing {missing}"]
    return 1, [f"tip: computed {tip}, {len(seen)} rows re-derived"]


def receipt_observable(text: str, clause_id: str, control_id: str) -> bool:
    if f"clause={clause_id}" not in text or "observed=TARGET_MISSED" not in text:
        return False
    if f"control={control_id}" not in text and f"# control {control_id} " not in text:
        return False
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--frozen", required=True)
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
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
    live = ledger.get("live") or []
    live_ids = [c["id"] for c in live]
    expected = list(spec["expected_live_clause_ids"])
    detail: list[str] = []

    uncovered = 0
    if sorted(live_ids) != sorted(expected):
        missing = sorted(set(expected) - set(live_ids))
        extra = sorted(set(live_ids) - set(expected))
        uncovered += len(missing) + len(extra)
        detail.append(f"clause-set: missing {missing} extra {extra}")
    declared = 0
    for clause in live:
        nl = clause.get("not-load-bearing")
        if nl and nl.get("reason"):
            declared += 1
            if clause["id"] != spec["toctou_clause"]:
                uncovered += 1
                detail.append(f"declared: {clause['id']} is not the frozen toctou clause")
            continue
        control = clause.get("control") or {}
        receipt_rel = control.get("receipt")
        control_id = control.get("control_id")
        if not receipt_rel or not control_id:
            uncovered += 1
            detail.append(f"uncontrolled: {clause['id']} names no control id and receipt")
            continue
        receipt = repo / receipt_rel
        if not receipt.is_file():
            uncovered += 1
            detail.append(f"uncovered: {clause['id']} receipt missing {receipt_rel}")
            continue
        if not receipt_observable(receipt.read_text(), clause["id"], control_id):
            uncovered += 1
            detail.append(f"uncovered: {clause['id']} receipt does not bind clause and control")
    if declared != 1:
        uncovered += 1
        detail.append(f"declared: {declared} not-load-bearing clauses, expected exactly one")

    retired_ids = [c["id"] for c in (ledger.get("retired") or [])]
    retired_count = sum(1 for cid in retired_ids if cid not in set(live_ids))
    unknown_retired = sorted(set(retired_ids) - set(spec["expected_retired_clause_ids"]))
    if unknown_retired:
        retired_count = 0
        detail.append(f"retired: ids not frozen: {unknown_retired}")

    tip_ok, tip_detail = tip_observable(repo, spec)
    detail.extend(tip_detail)

    observed = {"uncovered": uncovered, "retired": retired_count, "tip_ok": tip_ok}
    met = all(observed[k] == EXPECTED_TARGET[k] for k in EXPECTED_TARGET)
    print(
        "PRED-C2-r36-v1 uncovered={uncovered} retired={retired} tip_ok={tip_ok} "
        "verdict={verdict}".format(verdict="TARGET_MET" if met else "TARGET_MISSED", **observed)
    )
    for line in detail:
        print(f"  {line}")
    raise SystemExit(0 if met else 1)


if __name__ == "__main__":
    main()
