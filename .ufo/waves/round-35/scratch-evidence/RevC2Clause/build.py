#!/usr/bin/env python3
"""RevC2Clause fixture builder. Constructs scratch frozen specs + clause ledgers
that make PRED-C2-r35-v1 print TARGET_MET without the repair it claims to
measure. All artifacts land beside this script; nothing committed is touched."""
import json
import shutil
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
SC = LANE / ".ufo/waves/round-35/scratch/RevC2Clause"
SC.mkdir(parents=True, exist_ok=True)
(SC / "receipts").mkdir(exist_ok=True)

spec = json.loads((LANE / ".ufo/waves/round-35/c2/frozen.json").read_text())
PRED, TGT = spec["predicate"], spec["target"]

S = ".ufo/waves/round-35/scratch/RevC2Clause"

def frozen(name, **kw):
    s = {
        "id": "PRED-C2-r35-v1",
        "predicate": PRED,
        "target": TGT,
        "clause_ledger": kw["clause_ledger"],
        "blob_ledger": kw["blob_ledger"],
        "r34_tip": kw["r34_tip"],
        "toctou_clause": kw["toctou_clause"],
        "frozen_blobs": kw["frozen_blobs"],
    }
    (SC / name).write_text(json.dumps(s, indent=1) + "\n")

def ledger(name, live, retired):
    (SC / name).write_text(
        json.dumps({"id": "CLAUSES-scratch", "live": live, "retired": retired}, indent=1) + "\n"
    )

# --- attack 1: every clause controlled, receipts kill nothing ----------------
# fake receipt: a comment line containing the magic string; records no run.
(SC / "receipts" / "fake-kill.txt").write_text(
    "# RevC2Clause fake receipt - never ran anything\n"
    "# the next line exists only to satisfy MISSED.search\n"
    "verdict=TARGET_MISSED\n"
)

live_fake = [
    {
        "id": f"clause-{i:02d}",
        "why": "claims a control kills it; the receipt is a handwritten string",
        "control": {"tree": "controls/nonexistent-tree", "receipt": f"{S}/receipts/fake-kill.txt"},
    }
    for i in range(1, 10)
]
# o-nofollow-open must be the single not-load-bearing clause for toctou_declared.
live_fake[8] = {
    "id": "o-nofollow-open",
    "why": "declared, not controlled",
    "not-load-bearing": {"reason": "scratch declaration; no control exists"},
}
ledger("clauses-fake-receipts.json", live_fake, [{"id": "invented-retired-id", "why": "string, not a repair"}])
frozen(
    "frozen-fake-receipts.json",
    clause_ledger=f"{S}/clauses-fake-receipts.json",
    blob_ledger=f"{S}/blob-ledger-one-line.md",
    r34_tip=spec["r34_tip"],
    toctou_clause="o-nofollow-open",
    frozen_blobs=spec["frozen_blobs"],  # honest: real blobs verify at the real tip
)

# --- attack 2: receipts = the committed do-nothing receipt --------------------
# controls/c2-donothing.txt is committed bytes containing verdict=TARGET_MISSED.
live_borrowed = [
    {
        "id": f"clause-{i:02d}",
        "why": "receipt borrowed from the committed do-nothing control",
        "control": {"tree": "controls/nothing", "receipt": ".ufo/waves/round-35/controls/c2-donothing.txt"},
    }
    for i in range(1, 9)
]
live_borrowed.append(
    {
        "id": "o-nofollow-open",
        "why": "declared",
        "not-load-bearing": {"reason": "scratch"},
    }
)
ledger("clauses-borrowed-receipt.json", live_borrowed, [{"id": "x", "why": "w"}])
frozen(
    "frozen-borrowed-receipt.json",
    clause_ledger=f"{S}/clauses-borrowed-receipt.json",
    blob_ledger=f"{S}/blob-ledger-one-line.md",
    r34_tip=spec["r34_tip"],
    toctou_clause="o-nofollow-open",
    frozen_blobs=spec["frozen_blobs"],
)

# --- attack 3: escape hatch dodges a live control -----------------------------
# o-nofollow-open carries BOTH a control whose receipt does not exist AND a
# not-load-bearing declaration. The counter skips before resolving the control.
live_dodge = [
    {
        "id": "clause-01",
        "why": "real coverage via committed receipt",
        "control": {"tree": "controls/x", "receipt": ".ufo/waves/round-35/controls/c2-donothing.txt"},
    },
    {
        "id": "o-nofollow-open",
        "why": "names a control AND the hatch; receipt path does not exist",
        "control": {"tree": "controls/ghost", "receipt": f"{S}/receipts/DOES-NOT-EXIST.txt"},
        "not-load-bearing": {"reason": "hatch wins; control never consulted"},
    },
]
ledger("clauses-dodge.json", live_dodge, [{"id": "x", "why": "w"}])
frozen(
    "frozen-dodge.json",
    clause_ledger=f"{S}/clauses-dodge.json",
    blob_ledger=f"{S}/blob-ledger-one-line.md",
    r34_tip=spec["r34_tip"],
    toctou_clause="o-nofollow-open",
    frozen_blobs=spec["frozen_blobs"],
)

# boundary: a second clause tries the same dodge -> declared list no longer equals
live_two_dodge = live_dodge + [
    {
        "id": "clause-02",
        "why": "second hatch attempt",
        "control": {"tree": "controls/ghost", "receipt": f"{S}/receipts/DOES-NOT-EXIST.txt"},
        "not-load-bearing": {"reason": "tries to dodge too"},
    }
]
ledger("clauses-two-dodge.json", live_two_dodge, [{"id": "x", "why": "w"}])
frozen(
    "frozen-two-dodge.json",
    clause_ledger=f"{S}/clauses-two-dodge.json",
    blob_ledger=f"{S}/blob-ledger-one-line.md",
    r34_tip=spec["r34_tip"],
    toctou_clause="o-nofollow-open",
    frozen_blobs=spec["frozen_blobs"],
)

# --- attack 4: vacuous ledger_tip_ok ------------------------------------------
# frozen_blobs: [] -> the rev-parse loop never runs -> ok stays True.
# r34_tip "" -> "" in text is always True -> blob ledger content irrelevant.
(SC / "blob-ledger-empty.md").write_text("")
(SC / "blob-ledger-one-line.md").write_text(
    "the tip is dff394109f3cc3d851309ad7c67dd3b35b46adf2 — no blob table re-issued\n"
)
frozen(
    "frozen-vacuous-blobs.json",
    clause_ledger=f"{S}/clauses-fake-receipts.json",
    blob_ledger=f"{S}/blob-ledger-empty.md",
    r34_tip="",
    toctou_clause="o-nofollow-open",
    frozen_blobs=[],
)
# variant: real tip string kept, one-line ledger file, still no blob checks
frozen(
    "frozen-noop-ledger.json",
    clause_ledger=f"{S}/clauses-fake-receipts.json",
    blob_ledger=f"{S}/blob-ledger-one-line.md",
    r34_tip=spec["r34_tip"],
    toctou_clause="o-nofollow-open",
    frozen_blobs=[],
)

# --- attack 5: toctou_clause is an unchecked spec field ------------------------
live_renamed = [
    dict(c) for c in live_fake[:8]
] + [
    {
        "id": "my-invented-clause",
        "why": "the declared clause id is whatever the scratch spec says",
        "not-load-bearing": {"reason": "arbitrary id accepted"},
    }
]
ledger("clauses-renamed-toctou.json", live_renamed, [{"id": "x", "why": "w"}])
frozen(
    "frozen-renamed-toctou.json",
    clause_ledger=f"{S}/clauses-renamed-toctou.json",
    blob_ledger=f"{S}/blob-ledger-one-line.md",
    r34_tip=spec["r34_tip"],
    toctou_clause="my-invented-clause",
    frozen_blobs=spec["frozen_blobs"],
)

# --- attack 6: absolute-path receipt escapes --repo ----------------------------
live_abs = [
    {
        "id": f"clause-{i:02d}",
        "why": "receipt resolved outside --repo via absolute path",
        "control": {"tree": "t", "receipt": str(SC / "receipts" / "fake-kill.txt")},
    }
    for i in range(1, 9)
]
live_abs.append({"id": "o-nofollow-open", "why": "d", "not-load-bearing": {"reason": "r"}})
ledger("clauses-abs-receipt.json", live_abs, [{"id": "x", "why": "w"}])
frozen(
    "frozen-abs-receipt.json",
    clause_ledger=f"{S}/clauses-abs-receipt.json",
    blob_ledger=f"{S}/blob-ledger-one-line.md",
    r34_tip=spec["r34_tip"],
    toctou_clause="o-nofollow-open",
    frozen_blobs=spec["frozen_blobs"],
)

print("built:", sorted(p.name for p in SC.iterdir()))
