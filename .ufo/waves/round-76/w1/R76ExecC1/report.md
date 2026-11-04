# R76ExecC1 — independent C1 execution

Axes: calibration (both scored fields), operability (real harness and both selftests), no-harm (read-only lane; private scratch only).

## Result

C1 reproduced at freeze `cb713254ee9926e036e594312fdc61b57825526b`, against base `c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf`: 16/16 cases correct, four named outcome mutations killed, held mz-only score kills none. Real-lane harness passes, as do both requested selftests. No dead or absent execution leg; no implementation repaired.

All commands below ran with cwd `/home/vgpnk/Projects/shokunin/mado-shokunin`. Receipts retain the exact command, full merged stdout+stderr, and explicit exit code. Receipt paths in this report are relative to this report directory. The measurement command's last output line matches the frozen 16-case target sentence including the revision suffix.

## Command table

| command | rc | contract line / selftest tally | unexpected output |
|---|---:|---|---|
| `python3 -I quality/counters/c1-r76-outcome-field.py --repo . --rev cb713254ee9926e036e594312fdc61b57825526b --base-rev c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf --controls .ufo/waves/round-76/controls/c1-outcome-cases-r76.json --scratch-root /fast/scratch/hyaku/mado-r76/R76ExecC1/run` | 0 | `MADO_R76_OUTCOME_FIELD: cases=16 correct=16 mutants=4 killed=4 base_killed=0 verdict=TARGET_MET rev=cb713254ee9926e036e594312fdc61b57825526b` | None; full output: `count.txt` |
| `python3 -I quality/counters/c1-r76-landing-controls.py --repo . --rev cb713254ee9926e036e594312fdc61b57825526b --scratch-root /fast/scratch/hyaku/mado-r76/R76ExecC1/real` | 0 | `MADO_R76_LANDING_CONTROLS: selftest=62/62 mz=pass mr=pass killed=2/2 baseline=0/2 witness=ok verdict=TARGET_MET rev=cb713254ee9926e036e594312fdc61b57825526b` | None; full output: `real.txt` |
| `python3 -I quality/counters/c1-r76-outcome-field.py --selftest --scratch-root /fast/scratch/hyaku/mado-r76/R76ExecC1/counter-selftest` | 0 | `MADO_R76_OUTCOME_FIELD_SELFTEST: 19/19 assertions passed` | None; full output: `counter-selftest.txt` |
| `python3 -I quality/counters/c1-r76-landing-controls.py --selftest --scratch-root /fast/scratch/hyaku/mado-r76/R76ExecC1/harness-selftest` | 0 | `MADO_R76_HARNESS_SELFTEST: 23/23 assertions passed` | None; full output: `harness-selftest.txt` |
| `python3 -I /fast/scratch/hyaku/mado-r76/R76ExecC1/run/r76-c1/candidate.py --repo /fast/scratch/hyaku/mado-r76/R76ExecC1/run/r76-c1/fixtures/right --rev HEAD --scratch-root /fast/scratch/hyaku/mado-r76/R76ExecC1/labels/right` | 0 | `MADO_R76_LANDING_CONTROLS: selftest=2/2 mz=pass mr=pass killed=2/2 baseline=0/2 witness=ok verdict=TARGET_MET rev=7e1f70c2f4c2e60f947977edf3ee6d8fec6bd527` | None; negative fixture rc is expected; full output: `label-right.txt` |
| `python3 -I /fast/scratch/hyaku/mado-r76/R76ExecC1/run/r76-c1/candidate.py --repo /fast/scratch/hyaku/mado-r76/R76ExecC1/run/r76-c1/fixtures/always-red --rev HEAD --scratch-root /fast/scratch/hyaku/mado-r76/R76ExecC1/labels/always-red` | 1 | `MADO_R76_LANDING_CONTROLS: selftest=1/2 mz=pass mr=pass killed=2/2 baseline=0/2 witness=ok verdict=TARGET_MISSED rev=508a348e92e2f75013eda5479473d85d776701f1` | None; negative fixture rc is expected; full output: `label-always-red.txt` |
| `python3 -I /fast/scratch/hyaku/mado-r76/R76ExecC1/run/r76-c1/candidate.py --repo /fast/scratch/hyaku/mado-r76/R76ExecC1/run/r76-c1/fixtures/green-absent --rev HEAD --scratch-root /fast/scratch/hyaku/mado-r76/R76ExecC1/labels/green-absent` | 1 | `MADO_R76_LANDING_CONTROLS: selftest=2/2 mz=fail mr=pass killed=1/2 baseline=0/2 witness=absent verdict=TARGET_MISSED rev=93e6bc291da21abf0eabd07804e8a8ccaf7ce7db` | None; negative fixture rc is expected; full output: `label-green-absent.txt` |

## Real-lane evidence and field meanings

Full `MADO_R76_*` evidence is retained in `real.txt`, including all extraction hashes, replacement-ref controls, environment shape and redacted challenge. Key observed evidence:

```text
MADO_R76_SELFTEST instrument=quality/landing-counters.sh rc=0 summary=62/62 green=yes
MADO_R76_MUTANT M-Z path=quality/landing-counters.sh clause_count=1 recipe=clause-delete removed='[ "$citations" -gt 0 ] && ' from_sha256=b0612f111f3b676ffe42694c19802a34a623cc22076f32cf0ab750b803c73f1f rc=1 failed_assertions=3 assertions=59/62 killed=yes sha256=6d1a73b14c6e17cedf5cd6399fe58de246591682cb3a3518a2c7163711738216
MADO_R76_MUTANT M-R path=tools/mado-receipt-citecheck.py guard_count=1 recipe=line-delete removed_line='            env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"),\n' from_sha256=3b61fa42b77e9c8065ab05668247c330b537910b06f7209caba7afbd0b102ad0 rc=0 verdict=TARGET_MET missing=0 forged_credit=yes killed=yes sha256=414ca759232a3d31451f86060f4b0ba3382dd151f4bffe797793cb2ced5cee11
MADO_R76_LANDING_CONTROLS: selftest=62/62 mz=pass mr=pass killed=2/2 baseline=0/2 witness=ok verdict=TARGET_MET rev=cb713254ee9926e036e594312fdc61b57825526b
```

- `selftest=62/62`: the extracted landing instrument's own reported assertion fraction, not either Python harness selftest.
- `mz=pass`: the M-Z zero-citation clause deletion is credited as killed: mutant evidence reports three failed assertions and 59/62. It requires the held arithmetic credit rule plus the correct witness echo.
- `mr=pass`: deleting citecheck's replacement-ref guard makes the forged citation receive credit; the unmutated comparison refuses it. This is a successful defect kill, not a production success verdict.
- `killed=2/2`: both named baseline defects M-Z and M-R were killed, not the four outcome-rule mutations scored by the outer counter.
- `witness=ok`: the last parsed 16-or-more-hex witness equals the per-run challenge byte-for-byte. `absent` means no parsed witness; `mismatch` means parsed but unequal.
- Contract `verdict=TARGET_MET`: the extracted summary is green with witness credit and both baseline mutants are killed. `baseline=0/2` is the contract's fixed baseline field, not an independently executed historical counter in this leg.

Both selftests were directly executed: counter `19/19`, rc 0; successor harness `23/23`, rc 0. These are distinct from the real instrument's `62/62`.

## Labels independently re-derived

Only `MADO_R76_SELFTEST` and `MADO_R76_MUTANT M-Z/M-R` lines were consumed for derivation; the contract row was not consumed. `mz` derives from M-Z `killed=yes`; outcome derives from SELFTEST `green=yes` AND both mutants `killed=yes`. Raw source evidence and comparison are retained in `label-derivation.txt`; full individual command transcripts are `label-right.txt`, `label-always-red.txt`, `label-green-absent.txt`.

| case | SELFTEST summary / green | M-Z killed | M-R killed | derived mz / outcome | frozen mz / outcome | agrees |
|---|---|---|---|---|---|---|
| right | 2/2 / yes | yes | yes | pass / pass | pass / pass | yes |
| always-red | 1/2 / no | yes | yes | pass / fail | pass / fail | yes |
| green-absent | 2/2 / no | no | yes | fail / fail | fail / fail | yes |

Important: `green-absent` reports arithmetic 2/2 but evidence `green=no`; the installed green rule also requires witness credit. Deriving green from the fraction alone would mislabel this case.

## Four outcome mutations

```text
MADO_R76_MUTANT name=outcome-summary-only score=15/16 base_score=16/16 killed=yes base_killed=no
MADO_R76_MUTANT name=outcome-killed-only score=15/16 base_score=16/16 killed=yes base_killed=no
MADO_R76_MUTANT name=outcome-killed-any score=15/16 base_score=16/16 killed=yes base_killed=no
MADO_R76_MUTANT name=outcome-killed-or score=14/16 base_score=16/16 killed=yes base_killed=no
```

## Findings, limits and dispositions

- **Documentation inconsistency (non-blocking execution finding):** the declaration's C1 prose still says fifteen-case expectation / below-fifteen kill threshold, while its frozen set and target say sixteen. The counter docstring, lines 10–40 and 51, likewise retains obsolete fifteen-case examples and an obsolete mutant list. Actual implementation uses `FROZEN_CASES=16` and `score < len(cases)`; observed mutant scores 15/16, 15/16, 15/16, 14/16 demonstrate the executed below-sixteen threshold. Under the literal prose below-fifteen threshold, only the final mutant would die. No source/doc fix made under this seat's bounds.
- **Historical-control qualification:** committed `control-baseline-r76.txt` records 15/15 and four earlier mutant names, not the final outcome-summary-only / killed-only / killed-any / killed-or cohort. The independent count's same-cohort mz-only `base_score=16/16` for each final mutation supplies the direct 0/4 comparison; the historical receipt alone does not.
- The counter mutates only the outcome helper; this does not prove unrelated kill-path fault coverage. An echo-dropping outcome mutation remains unobservable through the published verdict as disclosed in the declaration.
- Execution uses live counter/harness entrypoints with extracted fixture/harness bytes pinned at the requested revision; no claim that every live entrypoint was itself extracted from that revision.
- No supported LSP tool is exposed in this seat; no symbol edit/refactor attempted. No tools installed or upgraded. No host/session/service/config/credential probing, fleet git mutations, subagents or background jobs were initiated.
- The requested sibling report path `.ufo/waves/round-76/w1/R76ExecC1.md` conflicts with the repeated **only write directory** restriction. This report is instead retained at `.ufo/waves/round-76/w1/R76ExecC1/report.md`, wholly inside the permitted directory. The final trailer names that actual file.

## Retained files / cleanup

Only this report and eight receipts were written in the exclusive seat directory: `count.txt`, `real.txt`, `counter-selftest.txt`, `harness-selftest.txt`, `label-right.txt`, `label-always-red.txt`, `label-green-absent.txt`, `label-derivation.txt`. No production implementation, committed evidence, corpus or shared documents changed. Private scratch was deleted after retaining receipts. No further verification is requested by this seat.

Self-review: accuracy 4/5 (entrypoints live, measured bytes revision-pinned); completeness 4/5 (all executions and derivations complete; report path adjusted to honor write boundary); clarity 4/5 (long command table retained for exact reproducibility); actionability 4/5 (prose threshold and historical-control qualifications identified without forbidden fixes); conciseness 4/5 (full raw evidence separated into receipts). Overall 4.0/5. Improvements: parent can correct stale fifteen-case prose and align the historical-control narrative; parent can reconcile the report-path instruction. Would the user agree? Execution results are directly evidenced; report-path precedence remains explicitly disclosed.
