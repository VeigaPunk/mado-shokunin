#!/usr/bin/env python3
"""Round-36 control-fixture generator — one mutation kind, one committed input.

The round-36 discrimination manifest freezes eight `c2` mutation *kinds*
(`.ufo/waves/round-36/controls/manifest.json`). This generator materialises each
kind against whichever evidence ledger a profile names, so the same kind scores
the round-35 counter (before) and the round-36 counter (after) on the same
declared input.

Every fixture differs from the accept control in exactly one committed input, and
the difference is recorded beside it in `mutation.txt`. Fixtures are written
outside the lane repo (default `/tmp/mado-r36-mutants-<profile>`) because they are
deterministically regenerable from committed bytes — the committed artifacts are
this generator, its profile table and the discrimination receipt that cites it.

Usage:
  gen-mutants.py --profile r35|r36 --repo <lane> --out <dir>
Prints one line per fixture: `mutant=<id> profile=<p> dir=<path>`.
Exit 0 on success, 2 on setup error.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

PROFILES = {
    "r35": {
        "clause_ledger": ".ufo/waves/round-35/c1/clauses.json",
        "blob_ledger": ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md",
    },
    "r36": {
        "clause_ledger": ".ufo/waves/round-36/c2/clauses.json",
        "blob_ledger": ".ufo/waves/round-36/ledger/RevFrozenBlobs-r36.md",
    },
}

# The round-34 defect's own stale label (spot-check D4: the pinned tip was
# disputed; `fa7ba113` is the round-34 *data* commit, labelled a tip by mistake).
STALE = "fa7ba11346116672352b5d41494141c5c4d738d0"
HEX40 = re.compile(r"\b[0-9a-f]{40}\b")
TIP = re.compile(r"tip", re.I)
TABLE_ROW = re.compile(r"^\s*\|\s*`([^`]+)`\s*\|\s*`?([0-9a-f]{40})`?\s*\|")


def die(msg: str) -> None:
    print(f"GEN-MUTANTS error={msg}", file=sys.stderr)
    raise SystemExit(2)


def tip_lines(text: str) -> list[str]:
    return [ln for ln in text.splitlines() if TIP.search(ln) and HEX40.search(ln)]


def load(path: Path):
    return json.loads(path.read_text())


def clause_paths(ledger: dict) -> list[str]:
    out = []
    for clause in ledger.get("live", []):
        control = clause.get("control") or {}
        if control.get("receipt"):
            out.append(control["receipt"])
    return out


def load_bearing(ledger: dict) -> list[dict]:
    return [c for c in ledger.get("live", []) if not c.get("not-load-bearing")]


def build(kind: str, ledger: dict, blob: str, repo: Path) -> tuple[dict, str, dict[str, bytes]]:
    """Return (mutated_ledger, mutated_blob_text, {receipt_path: new bytes})."""
    receipts: dict[str, bytes] = {}
    lb = load_bearing(ledger)
    if kind == "clause-deleted":
        if not lb:
            die("clause-deleted needs a load-bearing clause")
        victim = lb[-1]["id"]
        ledger["live"] = [c for c in ledger["live"] if c["id"] != victim]
        return ledger, blob, receipts
    if kind == "retired-also-live":
        retired = ledger.get("retired") or []
        if not retired:
            die("retired-also-live needs a retired clause")
        ledger["live"].append(
            {"id": retired[0]["id"], "why": "mutant: retired clause re-entered the live set",
             "not-load-bearing": {"reason": "mutant"}}
        )
        return ledger, blob, receipts
    if kind == "receipt-token":
        if not lb or not (lb[0].get("control") or {}).get("receipt"):
            die("receipt-token needs a controlled clause")
        receipts[lb[0]["control"]["receipt"]] = b"verdict=TARGET_MISSED\n"
        return ledger, blob, receipts
    if kind == "receipt-unbound":
        if len(lb) < 2:
            die("receipt-unbound needs two controlled clauses")
        src = (lb[1].get("control") or {}).get("receipt")
        dst = (lb[0].get("control") or {}).get("receipt")
        if not src or not dst or not (repo / src).is_file():
            die("receipt-unbound needs two readable receipts")
        receipts[dst] = (repo / src).read_bytes()
        return ledger, blob, receipts

    if kind == "tip-stale":
        lines = blob.splitlines(keepends=True)
        changed = 0
        for i, ln in enumerate(lines):
            if "supersedes" in ln.lower() or not TIP.search(ln):
                continue
            new = HEX40.sub(STALE, ln)
            if new != ln:
                changed += 1
                lines[i] = new
        if not changed:
            die("tip-stale found no tip line")
        return ledger, "".join(lines), receipts
    if kind == "tip-one-copy":
        lines = blob.splitlines(keepends=True)
        for i, ln in enumerate(lines):
            if "supersedes" in ln.lower():
                continue
            m = HEX40.search(ln)
            if m and TIP.search(ln):
                lines[i] = ln[: m.start()] + STALE + ln[m.end():]
                return ledger, "".join(lines), receipts
        die("tip-one-copy found no tip line")
    if kind in ("blob-corrupt", "blob-row-deleted"):
        lines = blob.splitlines(keepends=True)
        rows = [i for i, ln in enumerate(lines) if TABLE_ROW.match(ln)]
        if not rows:
            die("no table row")
        if kind == "blob-corrupt":
            i = rows[0]
            m = TABLE_ROW.match(lines[i])
            lines[i] = lines[i].replace(m.group(2), "0" * 40)
        else:
            del lines[rows[-1]]
        return ledger, "".join(lines), receipts
    die(f"unknown kind {kind}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True, choices=sorted(PROFILES))
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
    prof = PROFILES[args.profile]
    ledger_p = repo / prof["clause_ledger"]
    blob_p = repo / prof["blob_ledger"]
    if not ledger_p.is_file():
        die(f"missing {prof['clause_ledger']}")
    if not blob_p.is_file():
        die(f"missing {prof['blob_ledger']}")
    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    base_ledger = load(ledger_p)
    base_blob = blob_p.read_text()
    receipt_rels = sorted(set(clause_paths(base_ledger)))

    manifest = json.loads((repo / ".ufo/waves/round-36/controls/manifest.json").read_text())
    kinds = [c for c in manifest["controls"] if c["instrument"] == "c2" and c["kind"] == "mutant"]
    for control in kinds:
        kind = control["mutation"]
        ledger = json.loads(json.dumps(base_ledger))
        ledger, blob, receipts = build(kind, ledger, base_blob, repo)
        dest = out / control["id"]
        (dest / Path(prof["clause_ledger"]).parent).mkdir(parents=True, exist_ok=True)
        (dest / Path(prof["blob_ledger"]).parent).mkdir(parents=True, exist_ok=True)
        (dest / prof["clause_ledger"]).write_text(json.dumps(ledger, indent=1) + "\n")
        (dest / prof["blob_ledger"]).write_text(blob)
        for rel in receipt_rels:
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if rel in receipts:
                target.write_bytes(receipts[rel])
            else:
                target.write_bytes((repo / rel).read_bytes())
        (dest / "mutation.txt").write_text(
            f"control={control['id']}\nprofile={args.profile}\nmutation={kind}\n"
            f"changed={sorted(receipts) if receipts else [prof['clause_ledger'], prof['blob_ledger']]}\n"
        )
        print(f"mutant={control['id']} profile={args.profile} dir={dest}")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
