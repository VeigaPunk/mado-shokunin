# R55W2MutFreeze -- report (falsify wave w2)

Scope: mutation test of `quality/check-freeze-order.py` at lane revision `57584ed67716340b3d466fa04333ac0bab3fb79e`.
Full table, commands and survivor analysis: `.ufo/waves/round-55/w2/R55W2MutFreeze/mutants.md`.
Mutants: `.ufo/waves/round-55/w2/R55W2MutFreeze/mutants/M01.py`..`M17.py` (+ `.diff`). Receipts: `.../R55W2MutFreeze/receipts/`.

## What ran
- 17 one-edit mutants of the instrument, made in scratch and never in the lane. No lane file or git state changed; the lane was read only (`git clone --bare --no-local` into scratch, `git archive`, `git show`, `git ls-tree`, `git cat-file`, `git log`).
- Each mutant: instrument `--selftest`; the three real runs against a bare clone of the lane (round 54 w1 FAIL, round 54 w2 OK, round 55 w1 OK, all matched the unmutated baseline); and the independent harness `check-r55-controls.py --claim c1` on a scratch repo carrying the mutant.
- Probes: `receipts/probes.py` (reproducible; run output in `receipts/probes-out.json`).
- Tooling: none installed or upgraded. Host `git` and `python3 -I` only.

## Verdicts
| target | verdict | evidence |
|---|---|---|
| Selftest kill power over 17 mutants | **BROKEN** | 12 killed by selftest, 1 killed only by real runs (M14), 4 survive (M05, M06, M07, M12). `mutants.md` table. |
| Survivor M06: missing `createdAt` key read as OK | **BROKEN** (reproduced) | `probe A`: late freeze 17:11Z, registry without createdAt: base `FAIL reason=no_registry` rc 1; mutant `OK reason=ok` rc 0. `receipts/probes-out.json` `A_base_M06`. |
| Survivor M07: naive `createdAt` read as UTC | **BROKEN** (reproduced) | `probe B`: `createdAt "2026-10-27T18:00:00"`: base `FAIL no_registry` rc 1; mutant `OK` rc 0. `B_base_M07`. |
| Survivor M12: swallowed git failure | **BROKEN** (masks errors; no false OK found) | `probe C`: base `SETUP git_failed:ls-tree -z` rc 2; mutant `FAIL reason=no_freeze` rc 1. The false-OK path is [INFERENCE] from code. `C_base_M12`. |
| Survivor M05: drop `--full-history` | **UNVERIFIED** (candidate equivalent) | Two probe graphs gave identical output under base and mutant (`D_graph1_*`, `E_graph2_*`). No distinguishing graph found; not proven equivalent. |
| "Independent harness" `check-r55-controls.py` as a control for this instrument | **BROKEN** (not a control) | `grep -ci freeze` over the harness modules at `57584ed6` = 0; 17/17 mutants leave it at `controls=7/7 verdict=OK`. |
| Real runs as a control | **SURVIVES** for the baseline; kills M01, M08, M09, M14 | Baseline reads match the required verdicts. M01/M08/M09 flip 54w1 FAIL->OK; M14 flips 54w2 OK->FAIL. |

## Proposed kill tests (text only; not applied to the lane)
1. M06: selftest case with FZ at 10:00-03:00 and registry `{"schema": "x"}` (no createdAt), expect `launch=none verdict=FAIL reason=no_registry`, rc 1.
2. M07: selftest case with registry `createdAt "2026-10-27T14:00:00"` (no offset), expect `launch=none verdict=FAIL reason=no_registry`, rc 1.
3. M12: assert `git(d, ["no-such-subcommand"], work)` raises `Setup`, or the probe C corrupted-object repo expecting `SETUP git_failed:ls-tree -z` rc 2.
4. M14: selftest case with the registry at `round-9/w2/` and `wave="w2"`.
5. M05: no kill test proposed; either document the flag as a no-op under `--first-parent` after checking git docs, or find a graph where the flags diverge.

## Not verified / limits
- M05 equivalence is not proven; only two graphs were probed.
- M12's "no false OK" is by code reading, not by execution.
- The real runs used `lane.git`, a bare clone of the lane at the same revision (same objects, same committer dates).
- The harness step used `--claim c1` only because the instruction required a claim argument; that harness does not exercise the freeze instrument at all, so its column is structurally "nothing" for every mutant.
- Scratch under `/fast/scratch/hyaku/mado-r55/R55W2MutFreeze/` is removed at the end of this seat, after receipts were copied.
