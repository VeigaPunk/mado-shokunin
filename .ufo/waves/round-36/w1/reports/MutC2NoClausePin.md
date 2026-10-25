# MutC2NoClausePin — mutation-tester seat, mado round 36 wave 1

Task: write a `/tmp` variant of the round-36 C2 design with the frozen
`expected_live_clause_ids` cross-check removed (a deleted clause is skipped, as
in round 35), generate fixtures, run the variant against `c2-clause-deleted`,
and report whether `uncovered` stays 0 (fail-open reproduced) and what the pin
costs.

## Instrument

`/tmp/w36-m2/variant/c2-ledger-nopin.py` (sha256
`23f45648819db547208a3d6b67081f0b549208fd08a82b002175ca0bc549ce99`) — a line
copy of `quality/counters/c2-ledger.py` (sha256
`92db777e7573411835b8686f86520e1f891e8f5e44d6a9c3c18fe8c488193833`) with
exactly the clause pin removed:

```diff
-    expected = list(spec["expected_live_clause_ids"])
+    # MUTANT MutC2NoClausePin: expected_live_clause_ids pin removed — the ledger's
+    # own live list is the whole clause set (round-35 fail-open restored).
     detail: list[str] = []

     uncovered = 0
-    if sorted(live_ids) != sorted(expected):
-        missing = sorted(set(expected) - set(live_ids))
-        extra = sorted(set(live_ids) - set(expected))
-        uncovered += len(missing) + len(extra)
-        detail.append(f"clause-set: missing {missing} extra {extra}")
     declared = 0
```

Everything else (predicate/target drift checks, receipt binding, toctou
declared fence, retired count, tip/blob rule) is byte-identical. This is the
faithful "round-35 skip" mutation: the live id set is no longer compared to
anything, so a deleted clause deletes its obligation with it.

## Commands

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I .ufo/waves/round-36/c2/gen-mutants.py --profile r36 \
  --repo /home/vgpnk/Projects/shokunin/mado-shokunin --out /tmp/w36-m2
export GIT_DIR=/home/vgpnk/Projects/shokunin/mado-shokunin/.git
python3 -I quality/counters/c2-ledger.py \
  --repo /tmp/w36-m2/c2-clause-deleted \
  --frozen .ufo/waves/round-36/c2/frozen.json          # pristine
python3 -I /tmp/w36-m2/variant/c2-ledger-nopin.py \
  --repo /tmp/w36-m2/c2-clause-deleted \
  --frozen .ufo/waves/round-36/c2/frozen.json          # variant
python3 -I /tmp/w36-m2/variant/c2-ledger-nopin.py \
  --repo . --frozen .ufo/waves/round-36/c2/frozen.json # variant, live lane
```

Deviations from the prompt's command: the trailing `--` was dropped (argparse
rejects it: `gen-mutants.py: error: unrecognized arguments: --`, exit 2 — the
harness's own `ensure_mutants()` invocation also omits it). The counter was run
with the harness's exact `GIT_DIR=<lane>/.git` env so `git -C` in
`tip_observable` resolves lane history for the `/tmp` fixtures (fixtures are not
repos); this reproduces how `check-counter-discrimination.py` runs the counter.

## Results (actual output lines)

Fixture `c2-clause-deleted` = `mutation.txt` `changed=['.ufo/waves/round-36/c2/clauses.json', '.ufo/waves/round-36/ledger/RevFrozenBlobs-r36.md']`; live set drops `gate-quote-word-bound` (10 ids vs 11 expected).

Pristine counter on the fixture (baseline, killed):

```
PRED-C2-r36-v1 uncovered=1 retired=1 tip_ok=1 verdict=TARGET_MISSED
  clause-set: missing ['gate-quote-word-bound'] extra []
  tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows re-derived
exit=1
```

(This matches the committed receipt `controls/receipts/c2-clause-deleted.txt`:
`observed=TARGET_MISSED ok=1`.)

**Variant (no pin) on the fixture — fail-open reproduced:**

```
PRED-C2-r36-v1 uncovered=0 retired=1 tip_ok=1 verdict=TARGET_MET
  tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows re-derived
exit=0
```

Variant on the live lane (pin cost baseline, `TARGET_MET` preserved):

```
PRED-C2-r36-v1 uncovered=0 retired=1 tip_ok=1 verdict=TARGET_MET
  tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows re-derived
exit=0
```

## What the pin costs

- **Runs**: `time` on live lane: pristine 0.037s, variant 0.035s — the pin is
  a `sorted()` of ≤11 ids plus two set subtractions, sub-millisecond, below
  noise (runtime is dominated by the `git rev-parse`/`git log` calls).
- **Coverage**: it is the *only* observable that distinguishes the deleted
  clause. `c2-clause-deleted` is the sole control where it is the deciding
  check; every other clause-side observable (receipt binding, toctou declared
  fence, retired count) still fires without it.
- **Second-order gap (finding)**: the variant's predicate/target drift checks
  still compare the frozen spec's `predicate` string — which *asserts* the pin —
  so a spec edited to also drop `expected_live_clause_ids` would pass
  `predicate-drift` vacuously. The text check cannot re-derive that the live id
  set is compared.

## Extra probe: the pin's blind spot under set arithmetic

The pin implements "exact set" with set arithmetic: `missing/extra = set
difference`, **len = len(missing)+len(extra)`. A *duplicated* live id (clause
count 12, ids `entry-regular` twice) is detected as "extra" in detail but scores
zero uncovered:

```
# crafted /tmp/w36-m2/c2-clause-duplicated (lane ledger + duplicate entry-regular)
PRISTINE: uncovered=0 retired=1 tip_ok=1 verdict=TARGET_MET   # exit=0 — should be reject
VARIANT:  uncovered=0 retired=1 tip_ok=1 verdict=TARGET_MET   # exit=0
```

The duplicate is invisible to both because `set()` collapses it and
`sorted(live_ids)==sorted(expected)` fails only on distinct elements. This is a
genuine hole in the *frozen pin itself* (a kind the manifest does not exercise —
no `c2-*-duplicate` control exists), not in the pin's removal. The missing-clause
direction — the one the manifest pins — is fully closed by the pin.

## Verdict

- **Probe**: variant on `c2-clause-deleted` reads `uncovered=0 verdict=TARGET_MET
  exit=0` (pristine: `uncovered=1 TARGET_MISSED exit=1`; baseline receipt agrees)
  → **fail-open reproduced**: deleting the `expected_live_clause_ids` pin
  restores exactly the round-35 skip-a-deleted-clause hole D4 routed.
- **Pin cost**: negligible runtime (<1 ms, below noise); preserves the live-lane
  pass; it is the sole guard for the deleted-clause control. The pin itself has
  a separate duplication blind spot (set arithmetic), which the frozen manifest
  does not cover.
- **Restoration evidence**: the lane file was never edited. Pre-run sha256
  `92db777e7573411835b8686f86520e1f891e8f5e44d6a9c3c18fe8c488193833` == post-run
  sha256; `git status --porcelain -- quality/counters/c2-ledger.py` empty. The
  variant lives only in `/tmp/w36-m2/` (copy `c2-ledger-nopin.py`, fixtures
  `c2-clause-deleted{,-extra,-duplicated}`, scratch `variant/`). It is disposable
  by tasking. No production file touched; no tool installs (python3/git only).
