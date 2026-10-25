# MutC1NoFence — mutation-tester report (mado round 36, wave 1)

Seat: `L1Mado36.MutC1NoFence`. Role: mutation-tester.
Mutant: **C1 counter with the `## Registry` section fence removed** (whole-file
scan: `rows_for` iterates the whole `corpus/SOURCES.md` instead of only the
`## Registry` section).

## Mutant (smallest behavior-bearing point)

`quality/counters/c1-idle-lock.py` (`PRED-C1-r36-v1`), one line, in scratch copy:

```
-    for line in registry_section(sources).splitlines():   # fenced: only `## Registry` section
+    for line in sources.splitlines():                      # whole-file scan
```

`registry_section()` (lines 106–116) is left in place but becomes dead code.
The predicate string in the file is unchanged, so the counter still passes its
own `predicate-drift` self-check — the difference is only in what it scans.

Hash evidence:
- pristine bytes: `2ee6d0de76dfe756a9bbb03a4f96ae9bd3e48d4dfe37564b46e6e696047f4ce7`
  (`LANE/quality/counters/c1-idle-lock.py`)
- mutated bytes: `d2ce56e461a19ccbc45a7ac813498fcb8b17dfd80f83b14e9d45e44e50653d02`
  (reproduced from pristine by applying exactly the line change above)
- restored bytes: `2ee6d0de76dfe756a9bbb03a4f96ae9bd3e48d4dfe37564b46e6e696047f4ce7`
  (identical to pristine)

## Method

Detector: `LANE/quality/check-counter-discrimination.py`
(sha256 `421deda5956f8005967b10d4721b2bddead68a610704b1b2c705297236662544`,
copied into scratch; r36 `c1` script path patched to the scratch mutant copy —
everything else byte-identical). The detector runs both instruments against the
frozen 25-control manifest (`.ufo/waves/round-36/controls/manifest.json`), the
same command family as the lane's counting command, with receipts written only
under `scratch/MutC1NoFence/` and c2 fixtures generated under `/tmp`. No
production file was written; `quality/`, `corpus/`, `tools/`, `.ufo/waves/
round-36/{registration.md,controls,receipts,c1,c2,ledger}` untouched.

Commands (all from `LANE`):

```sh
python3 -I .ufo/waves/round-36/scratch/MutC1NoFence/check-counter-discrimination.py \
  --profile r36 --manifest .ufo/waves/round-36/controls/manifest.json --repo . \
  --receipts .ufo/waves/round-36/scratch/MutC1NoFence/receipts-pristine \
  --mutants /tmp/mado-r36-mutants-MutC1NoFence-pristine
# same with --receipts .../receipts-mutant --mutants /tmp/mado-r36-mutants-MutC1NoFence-mutant
# same with --receipts .../receipts-restored --mutants /tmp/mado-r36-mutants-MutC1NoFence-restored
```

## Results

| Run | Bytes | Score | Verdict | Exit |
|---|---|---|---|---|
| Pristine | `2ee6d0…` | correct=25/25 | TARGET_MET | 0 |
| **Mutated** | `d2ce56…` | **correct=23/25** | **TARGET_MISSED** | **1** |
| Restored | `2ee6d0…` | correct=25/25 | TARGET_MET | 0 |

Mutated run, quoted output (exact lines, `mutant-run.out`):

```
control=c1-no-registry-heading instrument=c1 clause=row-in-registry expected=TARGET_MISSED observed=TARGET_MET ok=0
control=c1-row-moved-out instrument=c1 clause=row-in-registry expected=TARGET_MISSED observed=TARGET_MET ok=0
...
clause=row-in-registry controls=2 missed=0
MADO_DISCRIMINATION: profile=r36 instruments=c1,c2 controls=25 correct=23/25 label='round-36 repaired counters' verdict=TARGET_MISSED
```

All other 23 controls keep their pristine verdicts, including both accept
controls (`c1-live`, `c1-golden-r36` → TARGET_MET) and the other 20 reject
controls (→ TARGET_MISSED).

## Verdict: KILLED

The mutant is **killed**: the discrimination gate drops from 25/25 to 23/25
(TARGET_MISSED, exit 1), then returns to 25/25 on restored bytes. Baseline was
clean (25/25), so the kill is conclusive, not inconclusive.

**Load-bearing kills (both):** `c1-no-registry-heading` and `c1-row-moved-out`
are the two controls that flip MISSED→MET under the whole-file scan. Both are
bound to the `row-in-registry` clause (the manifest's binding), whose missed
count drops 2 → 0.
- `c1-no-registry-heading` (root `.ufo/waves/round-35/controls/golden`): the
  round-35 golden has all eight S-rows and no `## Registry` heading. The fence
  sees no section → MISSED; the whole-file scan finds the rows → MET.
- `c1-row-moved-out` (root `.ufo/waves/round-36/controls/c1-row-moved-out`):
  S206's row is moved from `## Registry` to `## Leads (unopened)` (diff vs
  `c1-golden-r36`: `12d11` / `16a16,19`). Fenced scan misses S206 → MISSED;
  whole-file scan finds it → MET.

Both flip for the same reason (rows are found outside the `## Registry`
section), so both are equally load-bearing for this mutant.

## Notes

- The other two `row-in-registry`-adjacent cribs (`c1-shape-only`,
  `c1-fabricated-payload`) stay MISSED under the mutant because their receipts
  hash differently and their gate-quotes are not substrings of the receipt
  bytes (verified: `c1-shape-only` S203 receipt = `f114cf88…` ≠ declared
  `1b7fa87f…`; fabricated quotes `fabricated attestation for Sxxx` are not in
  the receipts), so they fail `digest-match`/`gate-quote-substring` regardless
  of the fence. The kill is specific to the fence controls.
- No tool installed; no system changes. Scratch used: `scratch/MutC1NoFence/`
  (detector copy, mutant copy, receipts dirs) and `/tmp/mado-r36-mutants-MutC1NoFence-*`.
