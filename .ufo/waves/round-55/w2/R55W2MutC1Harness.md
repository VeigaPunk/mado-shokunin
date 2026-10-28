# R55 w2 — seat R55W2MutC1Harness report (mutation test of the C1 control harness)

## What I attacked
Target: `quality/r55_ctl_c1.py` (C1 control harness, lane rev 57584ed67716340b3d466fa04333ac0bab3fb79e), with 15 mutants
of the HARNESS (not the counter), run against the real counter and four stub counters (always-green, always-red minimal,
always-red shotgun, silent). The seat asked specifically which mutants the harness still scores OK on the always-green stub.

## What ran (and what did not)
- Read-only export of the lane rev (`git -C <lane> archive 57584ed… quality corpus .ufo/waves/round-55/frozen-tables-v2.json .ufo/waves/round-55/fetch | tar -x -C <scratch>`).
- Scratch repo `git init` of the export; `rev-parse --show-toplevel` asserted equal to the scratch dir; one commit with `-c user.name=ctl -c user.email=ctl@ctl`.
- Unmutated harness baseline on the real counter: `good=ok controls=7/7 verdict=OK` (exit 0). Also run through `quality/check-r55-controls.py --claim c1`: same result.
- 15 mutants (+ base) written as scratch COPIES and edited with the edit tool; 80 runs (16 harness × 5 counters). All ran; zero tracebacks.
- Not run: the c2/c3 harnesses; the holdout fixtures; the counter's own selftest; any lane write or git mutation in the lane. No tools installed (no `uv`/`pacman`/binary installs): none needed.
- Scratch `/fast/scratch/hyaku/mado-r55/R55W2MutC1Harness/` removed before yield; receipts are in the deliverable directory.

## Decisive output
- Unmutated harness, always-green stub: `MADO_R55_CONTROLS: claim=c1 good=ok controls=0/7 verdict=FAIL` (rc 1). Unmutated, always-red-shotgun: `controls=1/7 verdict=FAIL` (rc 1). So the base harness does reject both always-green and always-red counters.
- **M11** (always-green): `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK` rc 0. Stderr shows each control `ok - counter missed=` (empty).
- **M05** (real counter): `MADO_R55_CONTROLS: claim=c1 good=ok controls=6/7 verdict=OK` rc 0 (control 5 `dropped-row` absent from stderr).
- **M15** (always-red shotgun): `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK` rc 0.
- **M04** (always-red shotgun): `good=bad controls=7/7 verdict=FAIL`, i.e. the collateral check is what keeps shotgun counters off controls 2–7.
- **M10** (real counter): `good=ok controls=5/7 verdict=FAIL`, so a swap of mutations is detected.

## Verdicts per target
1. **Harness vs always-green stub, unmutated harness** — NOT-REPRODUCED. Scores 0/7 FAIL (`results/base.green.out`).
2. **Always-green survivors (the seat's question)** — SURVIVES for one mutant: **M11** (a single shortcut "a counter that names no leg is treated as having localised" passes all 7 controls on always-green). No check in the export would catch it: the export has no self-test that runs this harness against an always-green or always-red stub. Re-opens M54-6 under that weakening; does not reopen it in the unmutated harness.
3. **Skip-a-control** — BROKEN on the real counter. M05 gives `controls=6/7 verdict=OK`: the verdict compares against `len(CONTROLS)` and the printed denominator is the literal `/7`, so a dropped control is never counted. Evidence: `mutants/results/M05.real.out` and `mutants/diffs/M05.diff`.
4. **Drop the good-tree check (M01)** — survives the real counter only as an equivalence (real counter is green on the good tree). Against stubs it is not sufficient to pass alone: M01 scores FAIL on always-green (0/7) and always-red (1/7). It is a survivor only with the collateral check gone (M15, always-red shotgun: OK 7/7).
5. **Accept empty / duplicate stdout (M06, M07)** — both killed by every stub (FAIL), since neither a duplicate-first-line nor a no-legs miss satisfies the required leg. Not a stub-reachable survivor.
6. **Ignore exit status (M02, M08)** — killed by the verdict/leg checks on every stub; the exit check is redundant on these stubs (no stub returns a verdict that the leg check would accept with the wrong exit).
7. **Hard-wire control 4 to ok (M09)** — killed on all stubs (1/7 or 2/7), because controls 1–3, 5–7 still fail. Would need all 7 hard-wired to survive.
8. **Swap mutations of controls 2 and 3 (M10)** — killed on the real counter (5/7).
9. **Weakened required leg by kind prefix (M12)** — killed on always-red shotgun (1/7). Only the collateral check catches it; the required-leg check itself is not an independent defence.
10. **Drop revision check (M13), drop control verdict check (M14)** — killed on all stubs; the always-green stub echoes the rev, and the required-leg check independently rejects green (legs empty).
11. **Observation (not a mutant)**: C1-CTL-1 has `owned=None`, so the collateral check is skipped. The unmutated harness scores control 1 OK for always-red-minimal and always-red-shotgun (`results/base.red_shot.err`: `C1-CTL-1 absent: ok - counter missed=entry_absent,provenance,index,…`). Overall FAIL still holds because the good tree is red. Severity: low; a counter that names row legs on an absent-entry tree is dishonest, but the harness accepts it for that control.

## Evidence pointers
- Deliverable: `.ufo/waves/round-55/w2/R55W2MutC1Harness/mutants.md` (grid, survivors, files).
- `.ufo/waves/round-55/w2/R55W2MutC1Harness/mutants/mutants/{base,M01..M15}.py` (copies), `mutants/diffs/M01..M15.diff`, `mutants/stubs/*.py`, `mutants/results/<label>.<counter>.{out,err}`, `mutants/runone.sh`.

## Anything not verified
- Only single-edit mutants; combinations beyond M15 not tried.
- Stubs are constant counters. A tree-aware cheating counter (that prints the right leg per control by inspecting its input) was not built; the harness's resistance to that was not measured.
- I did not check the wider `quality/check-*.py` suite for any other path that runs this harness. The grep was limited to `quality/` in the export (only `check-r55-controls.py` and `tool-ledger.md` reference it).
- Harness exit-code semantics on setup errors (exit 2) were not mutated.

## Hygiene
- Lane: no writes; no git mutation in the lane (only `git archive`, read-only). The only lane paths written are under `.ufo/waves/round-55/w2/R55W2MutC1Harness/` and this report.
- Mutants are copies; the lane harness file is unchanged.
- No credentials or network reads in the deliverables.
