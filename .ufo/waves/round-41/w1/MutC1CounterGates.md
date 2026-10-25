# MutC1CounterGates — C1 counter mutation probe (round 41, w1) — COMPLETE

Question: do the committed C1 controls notice a regressed counter? Method: 20 single-edit mutants of
`quality/counters/c1-r41-globals.py` (pristine sha256 `e43dc235925635ffc2008a3af4872f33b9be6a461a5cea77a98e008ae2a3f32a`,
never modified — verified equal to the HEAD blob after all runs), each scored on the FULL 47-control suite
(`.ufo/waves/round-41/ctl/run-c1-controls.py --counter <mutant> --ref .ufo/waves/round-41/c1/ctl-ref-tool.py.txt`).
Baseline first: pristine counter = 47/47 correct, rc 0 (`logs/BASELINE-pristine.log`).

## Result: 8 killed, 12 SURVIVED

**Killed (controls react):** K01 clause-g-always (all 4 cheat controls flip MET), K02 STR_DENY drop (C4),
K04 CALL_DENY drop (C1), K05 OS_DENY drop (C2), K06 marker-check off (M14), K11 TOTAL=23 (P-reference; counter
assert-crashes), K12 sandbox launcher no-op (P-reference 0/24), K13 stdin pipe off (M11).

**Survivors — counter regressions the committed controls cannot see (all 47/47, full suite):**

1. **K07 rc-check off** — judge stops comparing rc; M15/M33 still MISSED because the *tool's own selftest*
    (clause b) catches those defects (`fixtures=24/24 … TARGET_MISSED`). The counter's rc gate is redundant.
2. **K08 livewritable0 neutered** — M12 caught by its selftest, not by the fixture (`fixtures=24/24` MISSED).
3. **K09 nosess0 neutered** — M34 stays MISSED (22/24) without it.
4. **K10 CR-ending noise variant dropped** — M38 caught by selftest (`fixtures=24/24` MISSED); fixture-level
    CR coverage is not load-bearing for any control.
5. **K03 STDLIB_DENY check deleted** — dead code: denied modules are outside STDLIB_ALLOW anyway (socket cheat
    still rejected via the allow-list).
6. **S01 stderr-emptiness check off** — no control tool writes stderr on rc 0/1/3; clause has no detector.
7. **S02 clause b always passes** — b2 teeth still gates the fake-selftest control M39; D1–D3 fail on fixtures.
8. **S03 ambient GIT_* passthrough** — only benign GIT_* present; bwrap `--clearenv` guards tools; the docstring's
    "ambient GIT_* removed" is untested.
9. **S04 constant nonce** — nonce freshness/replay exercised by no control.
10. **S05 base-lacks-tool check off** — no control exercises BASE (all use `--tool`); clause a's BASE half untested.
11. **S06 wrong-program noise variant dropped** — no control loosens program-name matching; verdict-invariant.
12. **S07 counter exit code always 0** — the runner requires `rc==0` AND `TARGET_MET` in the line, so the exit
    code is a redundant channel; a counter that always exits 0 scores identically on all 47 controls.

## Side finding — the control suite itself is nonce-flaky (~2/22 runs)

M27-boot-uppercase and M39-selftest-echo each flipped to MET exactly once across 22 full-suite draws — in runs
whose counter edits (S02 clause-b; K09 nosess0) cannot mechanistically cause those flips (M27 depends on gen3's
`rng.choice` noise sampling; M39 on b2's nonce-chosen flips crashing a constant-selftest tool). Neither reproduced
on retry (both 47/47), and 40 targeted pristine `--only` draws (20 each) produced zero flips. Consequence: a
*correct* counter fails its own suite as `correct=46/47` roughly 1-in-10 runs overall, and the same lottery can
fake a "kill" in mutation testing.

## Artifacts

- Matrix with per-mutant edits, verdicts, killers, log citations: `.ufo/waves/round-41/w1/MutC1CounterGates/matrix.md`
- Mutants: `.ufo/waves/round-41/w1/MutC1CounterGates/mutants/*.py` (20 files, one edit each)
- Raw logs: `.ufo/waves/round-41/w1/MutC1CounterGates/logs/` (baseline, 20 mutants, 2 retries, 40 lottery draws)
- Restoration: pristine counter sha256 unchanged and equal to `git show HEAD:` blob; `git status --porcelain`
  clean on that path. Tooling installed: none (pacman untouched).
