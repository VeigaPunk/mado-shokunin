# R72MutBattery — round-72 instrument mutation battery (wave 1)

Seat: R72MutBattery (leaf; no subagents dispatched). Date: 2026-11-04.
Axes probed: C1 calibration (kill credit needs the run's own failure detail) and C2 operability
(outcome verdict reads the gate's own summary).

## Method

- Instruments under test (frozen, never modified):
  `quality/counters/c1-r72-landing-controls.py` sha256 `d0d3bfd2b8306062e7ea7323377dea1371df93c4a9447a7a28c4927becfe7c62`
  at instruments rev `9bcb4fd5b598844f168230dc05e441721d95b272`; base harness
  `c1-r71-landing-controls.py` sha256 `f836499594fb4fa8898336b1a47241614bb2b9ddb6f93c369a9e00ece0f185f1`
  at `--base-rev 976684a27e99c2508037a60eec415f550f53d70e`.
- Mutants were built from the frozen harness bytes (copies in `mutants/`), committed with git
  plumbing (read-tree/update-index/write-tree/commit-tree) into a scratch clone
  `/fast/scratch/hyaku/mado-r72/R72MutBattery/mutrepo`; `git rev-parse --show-toplevel` was
  asserted to equal the clone before every write block. Each mutant commit changes exactly
  `quality/counters/c1-r72-landing-controls.py` (verified with `git diff-tree --name-only`).
- Counters ran with `--repo <clone> --rev <mutant commit> --base-rev 976684a2…`; the mutated
  M5 counters ran directly from `mutants/` against pristine and dead-candidate revs.
- Kill rule (claims declaration): a mutant is caught iff the matching counter prints
  `correct < 8` or `verdict=TARGET_MISSED`. Git writes never touched anything but the scratch
  clone; the scratch tree was deleted after receipt capture (twice; see receipts note).

## Baseline (rig validation — reproduces the frozen receipts byte-for-byte)

| run | counter last line | rc |
|---|---|---|
| C1 @ 9bcb4fd | `MADO_R72_SUMMARY_CREDIT: cases=8 correct=8 base_correct=6 verdict=TARGET_MET rev=9bcb4fd5b598844f168230dc05e441721d95b272` | 0 |
| C2 @ 9bcb4fd | `MADO_R72_OUTCOME: cases=8 correct=8 base_correct=4 verdict=TARGET_MET rev=9bcb4fd5b598844f168230dc05e441721d95b272` | 0 |

Both equal the last lines of the frozen `measurement-c1-r72.txt` / `measurement-c2-r72.txt`;
the embedded do-nothing controls reproduced `base_correct=6` (C1) and `base_correct=4` (C2).
The baseline is green, so every verdict below is a killed/survived finding, not an
inconclusive baseline.

## Battery

| id | operation (harness unless noted) | mutant commit | candidate sha256 | counter output last line | rc | caught? |
|---|---|---|---|---|---|---|
| M1 | `credit()` drops the arithmetic check: `return count_fails(out) == total - passed` → `return True` | `4f05a7484c97e9ae9da773b33e33dc197326846f` | `cc11b353e22076bed88af71b1ab1bda3f74a6e8ff1d7276ea4b9a31d6bb55461` | `MADO_R72_SUMMARY_CREDIT: cases=8 correct=6 base_correct=6 verdict=TARGET_MISSED rev=4f05a7484c97e9ae9da773b33e33dc197326846f` | 1 | **KILLED** (C1) — `bare-failing` and `mismatch-detail` both flip to a false credit |
| M2 | `credit()` accepts a bare summary: arithmetic relaxed `==` → `<=` | `8ead092e0348d59dd34bc0f845321faaae804fc7` | `72a1dc1ac4b525548d8e6fa950872c6747f47494982f735852b5a68b16347038` | `MADO_R72_SUMMARY_CREDIT: cases=8 correct=7 base_correct=6 verdict=TARGET_MISSED rev=8ead092e0348d59dd34bc0f845321faaae804fc7` | 1 | **KILLED** (C1) — `bare-failing` flips; `mismatch-detail` (3 FAIL lines > n−p=2) still refused |
| M3 | `summary_green()` drops the `n > 0` guard: `return total > 0 and passed == total` → `return passed == total` | `c8101c1732318d91075de8cf73c2a09bfe9888f7` | `81904fdaf8e0918c5dd48e13b103feb9f2d0ea2a736b3ddea419a022a0514527` | C1: `MADO_R72_SUMMARY_CREDIT: cases=8 correct=8 base_correct=6 verdict=TARGET_MET rev=c8101c1732318d91075de8cf73c2a09bfe9888f7` (rc 0); C2: `MADO_R72_OUTCOME: cases=8 correct=8 base_correct=4 verdict=TARGET_MET rev=c8101c1732318d91075de8cf73c2a09bfe9888f7` (rc 0) | 0/0 | **SURVIVED both frozen sets — real gap (GAP-1)** |
| M4 | `outcome_verdict()` reverts to exit-status/kill-count-only: `return "TARGET_MET" if killed == 2 else "TARGET_MISSED"` (summary gate dropped; the round-71 signature took `gate_rc`, which no longer exists) | `4414e3d3afbcfc41c0e02c18313d069f44baf886` | `ce1baec4b5c123c0ea2066fded852c0f09d644452004a0b32d865c839c7e8808` | `MADO_R72_OUTCOME: cases=8 correct=3 base_correct=4 verdict=TARGET_MISSED rev=4414e3d3afbcfc41c0e02c18313d069f44baf886` | 1 | **KILLED** (C2) — `failing-summary-exit0`, `no-summary-exit0`, `garbled-summary-exit0`, `failing-summary-exit2`, `no-summary-exit2` all flip to a false green |
| M5 | counter's `score()` accepts `None`: `return got is not None and got == expect(ed)` → `return True if got is None else …` (both counters mutated) | candidate commits `ea5c28805d9478e05c7e69019761ffbf4d4e0580` (C1 probe) / `23483386d0cbfb863d7a2aeb6b75828da24b6ecd` (C2 probe) | `f6aec5761eada45f29a43d2c2458a9b3e3fa66315d1c0047b070e89343a9c70d` / `78dcb1ca05f8c49153307b895395fd5c6b192e8ddb8109d9079d9d904ed226a2` | pristine instruments: C1 `…correct=8 base_correct=6 verdict=TARGET_MET rev=9bcb4fd…` rc 0, C2 `…correct=8 base_correct=4 verdict=TARGET_MET rev=9bcb4fd…` rc 0 (byte-identical to baseline) | 0 | **SURVIVED the frozen sets (vacuous) — real gap (GAP-2)** |

### Cross-coverage (mutant run under the non-matching counter, for the record)

| mutant | non-matching counter | last line | caught there? |
|---|---|---|---|
| M1 | C2 | `…correct=8 base_correct=4 verdict=TARGET_MET rev=4f05a748…` | no (by design: C2 never reads `credit()`) |
| M2 | C2 | `…correct=8 base_correct=4 verdict=TARGET_MET rev=8ead092e…` | no |
| M3 | C1 | `…correct=8 base_correct=6 verdict=TARGET_MET rev=c8101c17…` | no (C1 scores only `mz=`, which `credit()` drives) |
| M4 | C1 | `…correct=8 base_correct=6 verdict=TARGET_MET rev=4414e3d3…` | no (C1 scores only `mz=`; C2 catches M4) |

## GAP-1 (M3 survivor) — the frozen controls never exercise `n = 0`

Neither the eight C1 modes nor the eight C2 cases contain a summary with total `0`
(`MADO_LANDING_COUNTERS_SELFTEST: 0/0 assertions passed`), so deleting the `n > 0` guard from
`summary_green()` changes no frozen outcome and both counters still print `TARGET_MET` rc 0.
Direct function probe over the same bytes (receipt `runs/m3-function-probe.txt`):

```
pristine summary_green(0/0)          = False
mutant-M3 summary_green(0/0)         = True
pristine outcome_verdict(0/0, k=2)   = TARGET_MISSED
mutant-M3 outcome_verdict(0/0, k=2)  = TARGET_MET
pristine summary_green(12/12)        = True
mutant-M3 summary_green(12/12)       = True
```

A `0/0` summary greens the run under the mutant. Coverage finding, not a contract change: one
extra C2 case (`gate_out = "MADO_LANDING_COUNTERS_SELFTEST: 0/0 assertions passed"`,
`killed=2`, expected `TARGET_MISSED`) would kill this mutant class. Recording this does not
change the frozen predicates; it names what the frozen eight-case denominators do not cover.

## GAP-2 (M5 survivor) — an absent observation scores as correct

Against healthy instruments the M5 counters are byte-identical to baseline (the frozen sets
contain no mode/case where the candidate emits no parseable line, so `got` is never `None`).
The hazard appears the moment the candidate dies. Same probes, mutated counter vs pristine
counter, each over a candidate that produces no observation:

```
C1, candidate exits 2 with no contract line:
  mutated counter: MADO_R72_SUMMARY_CREDIT: cases=8 correct=8 base_correct=6 verdict=TARGET_MET rev=ea5c28805d9478e05c7e69019761ffbf4d4e0580   rc 0
  pristine counter: MADO_R72_SUMMARY_CREDIT: cases=8 correct=0 base_correct=6 verdict=TARGET_MISSED rev=1816e3a2fe1d3d36ed90c67b4afd8e93cf9bfb24  rc 1
C2, candidate's outcome_verdict returns None:
  mutated counter: MADO_R72_OUTCOME: cases=8 correct=8 base_correct=4 verdict=TARGET_MET rev=23483386d0cbfb863d7a2aeb6b75828da24b6ecd   rc 0
  pristine counter: MADO_R72_OUTCOME: cases=8 correct=0 base_correct=4 verdict=TARGET_MISSED rev=55ccd5f6113398e98f037b96cafbaee9363ed364   rc 1
```

(The pristine reprobe used fresh plumbing commits `1816e3a2…` / `55ccd5f6…` carrying the same
dead-candidate blobs `f6aec576…` / `78dcb1ca…` — commit ids differ only by committer
timestamp.) The frozen control sets cannot catch this class because they never starve the
candidate; the guards in `score()` are the counters' only defense, and mutating them greens a
dead instrument.

## Restoration evidence

- Fleet worktree instrument hashes before the battery = after the battery =
  `d0d3bfd2…` (harness), `4b3e1e89…` (`c1-r72-summary-credit.py`), `c955ae2c…`
  (`c2-r72-outcome.py`) — identical to the frozen receipts. The harness was only ever read via
  `git show` from the scratch clone; no lane file was opened for writing.
- `git status --porcelain -- quality/ tools/` in the mado repo: empty (0 lines) after all runs.
- Mutant bytes live only in `mutants/` (this dir) and the deleted scratch clone.
- Scratch `/fast/scratch/hyaku/mado-r72/R72MutBattery/` deleted; verified absent.
- No tool installs were needed (stock git/python3 sufficed); nothing was written outside this
  seat dir and the scratch tree. Read-only `git` was used against the fleet repo; all git write
  commands ran inside the scratch clone with the toplevel asserted each time.

## Receipts (all under this dir, `runs/`)

`baseline-c1`, `baseline-c2`, `m1-c1`, `m1-c2-cross`, `m2-c1`, `m2-c2-cross`, `m3-c1`, `m3-c2`,
`m3-function-probe`, `m4-c1`, `m4-c2`, `m5-c1-pristine`, `m5-c1-dead`, `m5-c2-pristine`,
`m5-c2-dead`, `p1-c1-dead-pristine`, `p2-c2-dead-pristine` — each `<tag>.txt` holds the full
counter stdout+stderr for the run cited above.

Verdict summary: M1 killed by C1; M2 killed by C1; M3 survived both frozen sets (GAP-1,
`0/0`-summary hole); M4 killed by C2; M5 survived the frozen sets with a demonstrated
dead-candidate green (GAP-2, `score()` None-guard is load-bearing).

Report: .ufo/waves/round-72/w1/R72MutBattery/R72MutBattery.md
