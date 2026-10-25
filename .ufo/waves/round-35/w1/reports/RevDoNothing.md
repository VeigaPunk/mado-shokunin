# RevDoNothing — C2 do-nothing reachability test (round 35, w1)

Scope: build the smallest edit that makes PRED-C2-r35-v1 print `TARGET_MET` with no
real work, under `.ufo/waves/round-35/scratch/RevDoNothing/`. Report pass/fail and what
the resulting claim would mean.

## Counter under test

`.ufo/waves/round-35/c2/count.py` (committed at `19e4ab3`), frozen spec
`.ufo/waves/round-35/c2/frozen.json`. TARGET_MET iff
`uncovered=0 ∧ retired=1 ∧ toctou_declared=1 ∧ ledger_tip_ok=1`, where
`toctou_declared` requires the set of `not-load-bearing` clauses to be **exactly**
`["o-nofollow-open"]` (count.py:99-100 — an exact list equality, not a superset check).

Baseline on the real repo, re-run at write time:

```
$ python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
exit=0
```

Each variant = one scratch `frozen-*.json` (byte-level copy of the committed spec, only
`clause_ledger` repointed) + one scratch `clauses-*.json`. `--repo` stays the real
repo root, so `blob_ledger`, receipts and `.git` resolve as committed. Verified output:

## V1 — empty the live pool (PASSES)

`scratch/RevDoNothing/clauses-live-only-toctou.json`: `live` truncated to the single
`o-nofollow-open` clause, copied verbatim; `retired` untouched.

```
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
exit=0
```

This is the smallest vacuous edit found: one deletion of eight clause objects, zero new
files, zero fabricated content. `uncovered=0` holds vacuously — there are no clauses
left to cover. `retired=1` still holds because `r34-word-bound-1-25` remains absent
from `live`. `toctou_declared=1` holds because the surviving clause is exactly the one
the spec names. `ledger_tip_ok=1` is unaffected — it is git-verified against the r34
tip `dff394109f3cc3d851309ad7c67dd3b35b46adf2` independently of the clause ledger.

## V2 — the prompt's example: declare every clause not-load-bearing (FAILS)

`scratch/RevDoNothing/clauses-all-nlb.json`: all nine clauses carry
`not-load-bearing` + reason; controls dropped.

```
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=0 ledger_tip_ok=1 verdict=TARGET_MISSED
exit=1
```

`uncovered` goes to 0 — every NLB clause is skipped (count.py:83-85) — but
`toctou_declared` drops to 0 because `declared == [spec["toctou_clause"]]` demands the
singleton. The counter **requires** exactly one NLB clause and it must be
`o-nofollow-open`. The naive do-nothing move is defended; so is `live=[]` (declared
would be `[]`, not `[o-nofollow-open]`).

## V3 — repoint every receipt to one committed MISSED receipt (PASSES)

`scratch/RevDoNothing/clauses-repoint.json`: the eight controlled clauses each repoint
`control.receipt` to `.ufo/waves/round-35/controls/c2-donothing.txt` — a real committed
file (`19e4ab3`) whose text contains `verdict=TARGET_MISSED`. Zero new files; no
receipt is even fabricated.

```
PRED-C2-r35-v1 uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET
exit=0
```

The receipt check (count.py:90-92) is only `is_file()` plus regex
`verdict=TARGET_MISSED` anywhere in the file. No binding between receipt and clause,
no check that the receipt's header names the clause's control, no uniqueness, no
freshness. Eight clauses aliasing one receipt passes.

## What the claim would actually mean

A `TARGET_MET` from a scratch ledger claims only: *"the file at `clause_ledger` —
chosen by whoever wrote `--frozen` — describes a self-consistent ledger."* Under V1 it
asserts the lane's entire risk surface is one TOCTOU clause already declared
non-load-bearing: coverage of nothing, achieved by deletion. Under V3 it asserts nine
independently-controlled clauses while all evidence collapses to one receipt about a
different control.

Enforcement gaps this exposes in "one command over committed bytes":

- `clauses.json` is read from the **worktree** (`repo / path`, `is_file()`); nothing
  verifies it is committed or matches any hash. Same for every receipt. Only
  `ledger_tip_ok` touches git at all (`rev-parse r34_tip:path` vs recorded blob ids).
- The frozen spec pins `predicate`, `target`, `toctou_clause`, `r34_tip` and
  `frozen_blobs` — but not the *contents* of `clause_ledger`. The pointer is the only
  thing frozen; the ledger behind it is trusted input.
- `retired=1` is satisfied by any self-declared retired id absent from `live` — also
  fabricable.

Guards that do hold: the all-NLB blanket move (V2) is killed by the
`declared == [toctou]` exact-match; predicate/target drift exits 2; `ledger_tip_ok`
cannot be faked by editing the ledger doc alone — blobs must re-verify at the r34 tip.

**Verdict: do-nothing TARGET_MET is reachable.** Smallest passing edit = truncate
`live` to the TOCTOU clause (V1), 1-file diff vs the committed ledger, exercised above
with exit 0. The prompt's suggested all-NLB edit does **not** pass. The counter scores
the shape of a self-reported ledger, and the ledger's membership is unauthenticated —
so TARGET_MET is reachable but not sound as a coverage claim without an additional
binding from clause ids to committed, per-clause receipts.
