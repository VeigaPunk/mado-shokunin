#!/usr/bin/env python3
"""Build the four forged-receipt fixture repos under /tmp/mado-r36-forge/fixtures/.

Each fixture is a minimal C2 input tree: the round-36 clause ledger (for the
r35 counter, a copy whose receipt/control references stay as committed), the
round-35 blob ledger, and a receipt directory with exactly one forged receipt
replacing the committed `c1-entry-symlink.txt` (victim clause entry-regular).
All other commits are real bytes. The r35 counter reads `spec['clause_ledger']`
and `spec['blob_ledger']` from the adapted spec (identical predicate/target), so
the fixture carries the ledger at both paths.

Forge (a) exact gate bytes but wrong clause id: `clause=row-well-formed` on the
instrument line. Forge (b) right clause, wrong control id: `control=c1-row-extra-field`
on the instrument line. Forge (c) right tokens embedded in prose with no measured
verdict: `clause=entry-regular` + `control=c1-entry-symlink` present, `verdict=`
token replaced by a hash. Forge (d) the real receipt of a different clause:
the committed `c1-digest.txt` bytes (clause digest-match), verbatim.
"""
import json
import shutil
from pathlib import Path

WORK = Path("/tmp/mado-r36-forge")
FIX = WORK / "fixtures"
LEDGER = WORK / "clauses.json"
REAL = WORK / "receipts-r36"
BLOB = WORK / "RevFrozenBlobs-r35.md"
BLOB36 = WORK / "RevFrozenBlobs-r36.md"
REAL_TEXT = (REAL / "c1-entry-symlink.txt").read_text()

forges = {
    "a-wrong-clause-id": REAL_TEXT.replace("clause=entry-regular", "clause=row-well-formed", 1),
    "b-wrong-control-id": REAL_TEXT.replace("# control c1-entry-symlink", "# control c1-row-extra-field").replace("/controls/c1-entry-symlink", "/controls/c1-row-extra-field"),
    "c-prose-no-measured-verdict": REAL_TEXT.replace("expected=TARGET_MISSED observed=TARGET_MISSED",
                                                     "expected=TARGET_MISSED observed=hash:8f14e45fceea167a5a36dedd4bea2543", 1),
    "d-real-receipt-other-clause": (REAL / "c1-digest.txt").read_text(),
}

for name, text in forges.items():
    d = FIX / name
    if d.exists():
        shutil.rmtree(d)
    (d / ".ufo/waves/round-36/c2").mkdir(parents=True)
    (d / ".ufo/waves/round-35/ledger").mkdir(parents=True)
    (d / ".ufo/waves/round-36/ledger").mkdir(parents=True)
    (d / ".ufo/waves/round-36/controls/receipts").mkdir(parents=True)
    (d / ".ufo/waves/round-36/c2/clauses.json").write_text(LEDGER.read_text())
    (d / ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md").write_text(BLOB.read_text())
    (d / ".ufo/waves/round-36/ledger/RevFrozenBlobs-r36.md").write_text(BLOB36.read_text())
    # real receipts for the other 9 load-bearing clauses
    for rel in ["c1-row-duplicate.txt", "c1-row-extra-field.txt", "c1-row-moved-out.txt",
                "c1-usedby-extra.txt", "c1-status-queued.txt", "c1-recheck-prose.txt",
                "c1-fabricated-payload.txt", "c1-quote-absent.txt", "c1-quote-long.txt"]:
        (d / f".ufo/waves/round-36/controls/receipts/{rel}").write_bytes((REAL / rel).read_bytes())
    (d / ".ufo/waves/round-36/controls/receipts/c1-entry-symlink.txt").write_text(text)
    ok = "clause=entry-regular" in text
    ok = ok and "control=c1-entry-symlink" in text
    ok = ok and "observed=TARGET_MISSED" in text and "verdict=TARGET_MISSED" in text
    print(f"fixture={name} forged-receipt-bytes={len(text)} fully-real-receipt={ok}")
print(f"fixtures written under {FIX}")
