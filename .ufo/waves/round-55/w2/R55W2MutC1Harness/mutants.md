# R55 w2 — mutation test of `quality/r55_ctl_c1.py` (seat R55W2MutC1Harness)

Base: `quality/r55_ctl_c1.py` at lane rev 57584ed67716340b3d466fa04333ac0bab3fb79e (exported with `git archive`, read-only).
Scratch repo: a fresh `git init` of that export, one commit (`91767e543e36b7c53d400eb0bf9fa3421a84b3bb`, a re-commit; blob
contents are identical to the lane). Every mutant is a COPY at `mutants/Mnn.py` made in scratch and edited with the edit tool.
The lane was never written to; no lane git mutation was run. Diffs against the base: `diffs/Mnn.diff`.

Harness invocation for each cell:
`python3 -I mutants/Mnn.py --repo <scratch repo> --rev HEAD --work <scratch dir> [--counter stubs/<stub>.py]`
(`real` = no `--counter`, the counter is read from the repo at rev; the real counter is `quality/counters/c1-r55-kbd-entry.py`.)

Stubs (`stubs/`):
- `always_green.py`: prints `rev=<rev> rows=18/18 hosts=6/6 sources=3/3 new_rows=3/3 verdict=TARGET_MET missed=none`, exit 0.
- `always_red_minimal.py`: prints `verdict=TARGET_MISSED missed=entry_absent,provenance,index`, exit 1.
- `always_red_shotgun.py`: prints `verdict=TARGET_MISSED` naming all 6 generic legs plus all 24 row/anchor/quote/source_cell/host ids, exit 1.
- `silent.py`: prints nothing, exit 0.

Cell format: `MADO_R55_CONTROLS` verdict line from the harness (`good=… controls=k/7 verdict=…`), exit code in `results/`.

## Grid (verdict as printed; `results/<mutant>.<counter>.out|err`)

| Mutant | Change to the harness | real counter | always-green | always-red-min | always-red-shotgun | silent |
|---|---|---|---|---|---|---|
| base | none | OK 7/7 | FAIL 0/7 | FAIL 1/7 | FAIL 1/7 | FAIL 0/7 |
| M01 | `judge_good` returns None (good-tree check dropped) | OK 7/7 | FAIL 0/7 (good=ok) | FAIL 1/7 (good=ok) | FAIL 1/7 (good=ok) | FAIL 0/7 |
| M02 | good-tree exit status ignored | OK 7/7 | FAIL 0/7 | FAIL 1/7 | FAIL 1/7 | FAIL 0/7 |
| M03 | control required-leg check dropped | OK 7/7 | FAIL 0/7 | FAIL 1/7 | FAIL 1/7 | FAIL 0/7 |
| M04 | control collateral (owned-id) check dropped | OK 7/7 | FAIL 0/7 | FAIL 1/7 | **FAIL 7/7** (good=bad) | FAIL 0/7 |
| M05 | control 5 (`dropped-row`) removed from `CONTROLS` | **OK 6/7** | FAIL 0/7 | FAIL 1/7 | FAIL 1/7 | FAIL 0/7 |
| M06 | duplicate stdout lines accepted (first line used) | OK 7/7 | FAIL 0/7 | FAIL 1/7 | FAIL 1/7 | FAIL 0/7 |
| M07 | empty stdout accepted as a miss with no legs | OK 7/7 | FAIL 0/7 | FAIL 1/7 | FAIL 1/7 | FAIL 0/7 |
| M08 | control exit status ignored | OK 7/7 | FAIL 0/7 | FAIL 1/7 | FAIL 1/7 | FAIL 0/7 |
| M09 | control 4 hard-wired ok | OK 7/7 | FAIL 1/7 | FAIL 2/7 | FAIL 2/7 | FAIL 1/7 |
| M10 | mutations of controls 2 and 3 swapped | FAIL 5/7 | FAIL 0/7 | FAIL 1/7 | FAIL 1/7 | FAIL 0/7 |
| M11 | counter with `missed=none` accepted as having localised (control passes) | OK 7/7 | **OK 7/7** | FAIL 1/7 | FAIL 1/7 | FAIL 0/7 |
| M12 | required leg matched on kind prefix only | OK 7/7 | FAIL 0/7 | FAIL 1/7 | FAIL 1/7 | FAIL 0/7 |
| M13 | control revision check dropped | OK 7/7 | FAIL 0/7 | FAIL 1/7 | FAIL 1/7 | FAIL 0/7 |
| M14 | control verdict check dropped | OK 7/7 | FAIL 0/7 | FAIL 1/7 | FAIL 1/7 | FAIL 0/7 |
| M15 | M01 + M04 combined | OK 7/7 | FAIL 0/7 (good=ok) | FAIL 1/7 (good=ok) | **OK 7/7** (good=ok) | FAIL 0/7 (good=ok) |

Counts: 15 mutants + base, 5 counters each, 80 runs, 0 tracebacks (`results/*.err`).

## Survivors (mutants the harness scores OK on the always-green stub)

- **M11** only: `always_green` → `good=ok controls=7/7 verdict=OK`, exit 0 (`results/M11.green.out`).
  The unmutated harness on the same stub: `controls=0/7 verdict=FAIL` (`results/base.green.out`). So M11 is a
  one-line weakening that re-opens M54-6 for C1. No check in the export exercises the harness against an always-green stub
  (grep of `quality/` for always-green/always-red self-tests: only the docstring line 11), so nothing would catch M11.

## Other survivors / non-kills (summary, detail in the report)

- **M05 survives the REAL counter**: `controls=6/7 verdict=OK` (`results/M05.real.out`). The verdict is
  `passed == len(CONTROLS)`, and the printed denominator is the literal `/7`, so a truncated table passes silently.
- **M15 survives always-red-shotgun**: `controls=7/7 verdict=OK` (`results/M15.red_shot.out`): the good-tree check plus
  the collateral check are jointly sufficient for a shotgun counter to pass.
- **Harness observation (not a mutant)**: C1-CTL-1 has `owned=None`, so the collateral check is skipped. The unmutated
  harness passes control 1 for always-red-minimal and always-red-shotgun (`results/base.red_shot.err`:
  `C1-CTL-1 absent: ok - counter missed=entry_absent,provenance,index,…`). Overall FAIL still holds (good=bad).
- Mutants M01, M02, M03, M04, M06, M07, M08, M12, M13, M14 are OK on the real counter: they weaken checks that the real
  counter never trips, so they are equivalent on the real counter and only detectable with wrong counters (see the grid).

## Files

- `mutants/base.py`, `mutants/M01.py` … `mutants/M15.py`: the harness copies as run.
- `diffs/M01.diff` … `diffs/M15.diff`: `diff -u` against base.
- `stubs/`: the four stub counters. `runone.sh`: the runner used for the grid.
- `results/`: `<label>.<counter>.out` (verdict line + exit status), `<label>.<counter>.err` (per-control stderr).
