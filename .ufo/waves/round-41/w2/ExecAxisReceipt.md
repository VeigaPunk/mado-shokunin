# Report — ExecAxisReceipt (round-41 w2, axis calibration attack)

Seat: ExecAxisReceipt. Assignment: attack 'calibration' — the published axis table must match the
observed repo state; reproduce what `quality/check-axis-scores.py` derives at the DATA commit
`07f2641696b5ac73de1404ea737a9f27e9819aa1`, publish the exact SCORECARD.md sentence that makes the
gate print `checked=3 mismatched=0` at the final tip, and a ready-to-commit receipt.

## Derived fractions at 07f2641 (reproduced)
- navigation **59/59** (`python3 -I quality/check-index.py --rev 07f2641… --repo .` → indexed=59/59 missing=0 dangling=0 duplicates=0)
- calibration **55/55** (`python3 -I .ufo/waves/round-31/c2/count.py 07f2641…` → active=55 resolved_active=55, TARGET_MET, exit 0)
- operability **12/12** (`python3 -I quality/check-index.py --selftest`)
- Gate at 07f2641: navigation STALE (published 58/58 vs derived 59/59 — the data commit added the
  focus-grab entry; the last publication is round 40's line, SCORECARD.md:2493); calibration and
  operability MATCH → `checked=3 mismatched=1`, exit 1. This is the expected data-stage red half
  (precedent `quality/receipts/red-axis-publication-stale-at-data-commit.txt`), not a defect.

## Final-tip values (validated in a disposable git fixture; criteria 69–72 appended byte-exact from
`w1/ScrQualityCriteria/criteria.md`)
- Calibration counter at tip: **active=59 resolved_active=59** (68 − 13 superseded + 4 new; 69–72
  resolve: 69/70 via bare non-empty `lessons/round-40-verifier-spotcheck.md`, 71/72 via
  `lessons/round-40.md#mistakes` M40-6/M40-1 present in the Mistakes section). literal 60/72,
  TARGET_MET, exit 0.
- Index at tip: 59/59 (entry row present; no new notes). Selftest 12/12.

## Exact sentence for SCORECARD.md (verified end-to-end in the fixture)
```
Axis table re-derived at `<TIP>` plus the round-41 records commit (one new indexed entry, criteria 69-72): navigation 59/59; calibration resolved-active 59/59; operability selftest 12/12.
```
`<TIP>` = final records-commit hash. Gate at the fixture tip printed `checked=3 mismatched=0`, exit 0.

## Receipt (ready to commit at `quality/receipts/axis-<tip>.txt`)
Body in `w2/ExecAxisReceipt/axis.md` §F5 (axis + index + suite transcript, axis-520c631d format;
rev tokens to be filled by the real run at the tip).

## Instrument verification
`quality/check-axis-scores.py --selftest` → 18/18; `quality/check-index.py --selftest` → 12/12.
Working-tree instruments/corpus/SCORECARD clean (`git status --porcelain` empty for those paths).

## No defects found
No data or predicate defect found in scope; the only red reading is the expected data-stage
navigation staleness, resolved by the records-commit publication above. Conditional: if the L1
extends the new criteria's lesson citations with `round-41.md#mistakes M41-n`, re-derive the
calibration count before landing.

## Tooling
No tools installed/updated; no package transactions; no host/compositor/Wayland/journal mutation.
