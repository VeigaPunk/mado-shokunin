# mado round 72 — frozen claims declaration

author: mado L1 (hyaku run 15, attempt 1)
date: 2026-11-04 (America/Sao_Paulo)
base: `976684a27e99c2508037a60eec415f550f53d70e` (round-71 closure tip; the lane tree is clean
at freeze: `tracked=0 untracked=0`, `jj-lane.sh state`)
round: mado lane counter 72. Shape: ONE v1 wave of 13 seats (band 8–16); the L1 holds the
planner seat (the validator rejects `planner` as a swarm role) and works the axis data-walk as
part of its own round work.

This file is written **before** any candidate measurement at the scored revision. The pre-freeze
receipts are `.ufo/waves/round-72/control-baseline-c1-r72.txt` and
`.ufo/waves/round-72/control-baseline-c2-r72.txt` (the held round-71 legs on the frozen control
sets), the control sets themselves
(`.ufo/waves/round-72/controls/c1-modes-r72.json` sha256
`18144745d65a00e1d812c663dbace402a5714fde74506f54d9adabe858268c13`;
`.ufo/waves/round-72/controls/c2-controls-r72.json` sha256
`640fb44fdb1f31b4706b381c905fde4b5dae769bfd3e5b656bdb374bad58a793`), and
`.ufo/waves/round-72/proto/held-lanes-r72.py` (the prototype that produced the baselines; it is
not a scored counter). Nothing in this declaration changes after the first candidate run; a miss
is an honest stop.

Two claims, distinct axes, causally separable **by verification**: both rule deltas live in one
successor harness file (`quality/counters/c1-r72-landing-controls.py`, the r72 generation of the
lane's harness chain) because the lane's convention is one harness per round; C1's counting
command imports and scores only the credit function, C2's only the outcome function, and neither
counter reads the other's control set. Each rule is independently revertible inside the file and
each has its own frozen denominator.

## Axis posture

At the base rev every published finite sub-axis sits at its measured maximum (navigation 85/85,
calibration resolved-active 86/86, operability selftest 12/12, ledger 122/122; gate
`MADO_SELFTEST: 460/460` — the round-71 closure's own measurements, re-run in this round's harm
watch). No axis is distinctly lowest and the stagnation nudge does not apply (last capability
row entered in round 71, window N=3, gap 0). Both claims therefore take **new finite
denominators** rather than re-scoring a held rule on new inputs.

## C1 — calibration: the kill credit requires the run's own failure detail, not just a summary line

- **Target surface.** The landing kill-credit rule in the harness chain
  (`c1-*-landing-controls.py`): the round-71 line `mz_killed = summary_shows_failure(out)`
  credits any parsed `MADO_LANDING_COUNTERS_SELFTEST: p/n assertions passed` with `p < n`,
  including a summary line that no assertion of this run produced (a bare echo) and a summary
  whose failure count is not backed by this run's `SELFTEST FAIL` lines.
- **Before.** The held round-71 harness scoring the frozen eight-mode set (`PROTO_R72_C1` lines):
  `correct_for_held=yes` on six modes and `NO` on exactly `bare-failing` and
  `mismatch-detail` — `held_mz=pass` where the truth is no credit. 6/8.
- **After (frozen sentence).** At `REV`, `python3 -I quality/counters/c1-r72-summary-credit.py
  --repo . --rev REV --base-rev 976684a27e99c2508037a60eec415f550f53d70e --scratch-root DIR`
  prints as its last line
  `MADO_R72_SUMMARY_CREDIT: cases=8 correct=8 base_correct=6 verdict=TARGET_MET rev=<sha>` and
  exits 0.

  Frozen predicate: the M-Z kill is credited iff the **last** parsed
  `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed` summary has `n > 0` and `p < n`,
  **and** the run's own `SELFTEST FAIL` lines number exactly `n − p`; both captured streams are
  read (the round-71 rule is preserved).
- **Counting command.** The command above, over the eight fixture modes of
  `controls/c1-modes-r72.json`: four carried from the round-71 real-child set (`liar-success`,
  `stderr-genuine`, `liar-kill`, `crash-stderr`, expectations unchanged) and four new
  (`bare-failing`, `mismatch-detail`, `last-wins-pass`, `last-wins-fail`). The counter builds a
  scratch git fixture lane whose M-Z behaviour is selected by the mode; it is not the lane's real
  landing instrument.
- **Kill rule.** `TARGET_MET` iff `correct == 8` and `base_correct == 6`; `TARGET_MISSED`
  otherwise. Exit 0 iff met; 1 iff measured and missed; 2 on usage/setup error with the reason on
  stderr and no contract line. Bounded score `10 × correct / 8` → 10.0000 (held 7.5000).
- **Do-nothing control.** The held round-71 harness at `--base-rev`, scored on the same eight
  modes in the same run; it must score exactly 6/8 or the counter/target is wrong.
- **Declared limits.** A captured summary replayed with its own matching detail lines remains
  byte-indistinguishable from a genuine run — the rule reads the child's report, it does not
  authenticate it; the eight modes are a finite control set, not fault coverage; the fixture lane
  is the counter's own instrument.

## C2 — operability: the outcome verdict reads the gate's own summary, not its exit status

- **Target surface.** The landing harness's contract outcome (`outcome_exit` /
  `outcome_verdict` in the harness chain): the round-71 line greens the run whenever the extracted
  instrument's `--selftest` exits 0, whatever its `MADO_LANDING_COUNTERS_SELFTEST: p/n` summary
  says, and reds a run whose summary is fully green but whose exit status disagrees.
- **Before.** The held round-71 `outcome_verdict(gate_rc, killed)` scoring the frozen eight cases
  (`PROTO_R72_C2` lines): 4/8 — wrong on `failing-summary-exit0`, `green-summary-exit2`,
  `no-summary-exit0` and `garbled-summary-exit0`.
- **After (frozen sentence).** At `REV`, `python3 -I quality/counters/c2-r72-outcome.py --repo .
  --rev REV --base-rev 976684a27e99c2508037a60eec415f550f53d70e --controls
  .ufo/waves/round-72/controls/c2-controls-r72.json --scratch-root DIR` prints as its last line
  `MADO_R72_OUTCOME: cases=8 correct=8 base_correct=4 verdict=TARGET_MET rev=<sha>` and exits 0.

  Frozen predicate: the contract verdict is `TARGET_MET` iff the kill count is `2/2` **and** the
  extracted instrument's **last** parsed `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions
  passed` summary has `n > 0` and `p == n`; a missing or garbled summary earns no green, and the
  exit status is recorded but does not gate the outcome.
- **Counting command.** The command above over `controls/c2-controls-r72.json`, scoring the
  successor and the held function on the same eight `(gate_out, gate_rc, killed)` cases.
- **Kill rule.** `TARGET_MET` iff `correct == 8` and `base_correct == 4`; otherwise
  `TARGET_MISSED`; same exit map as C1. Bounded score `10 × correct / 8`.
- **Do-nothing control.** The held round-71 `outcome_verdict` at `--base-rev`, scored in the same
  run; it must score exactly 4/8.
- **Declared limits.** The eight cases are a finite set over the summary grammar the production
  instrument prints; the counter scores the committed functions, not the whole harness execution;
  a case where the summary and the exit status contradict is scored by the summary by design —
  the exit status cannot carry the assertion result (held ground S441/S435).

## No-harm obligations (both claims)

`bash tools/mado-verify.sh --selftest` stays 460/460; the frozen round-71 instruments stay
byte-identical; the index, ledger, axis table and navigation checks stay at their measured
values; the new counters enter `quality/tool-ledger.md` and the `SKILL.md` Gate registry in the
same round (`quality/check-tool-ledger.py` `uncovered=0`). Neither claim touches configuration,
the compositor, a service, a sibling repo or `~/.config`.

## Sources plan (frontier step)

Two new rows opened this round, fetched three times each with receipts under
`.ufo/waves/round-72/fetch/`: CPython 3.14.8 `Doc/library/unittest.rst` (§ `TestResult`,
`wasSuccessful`) and CPython 3.14.8 `Lib/unittest/main.py` (the runner's exit is derived from
`wasSuccessful()`). Both claims' knowledge entries cite them. One rejection is curated as a
`rejected` row (the round-71 verifier's routed defect: `stdtypes.rst` under the 3.14 tree lives
at `Doc/builtins/stdtypes.rst`, re-opened this round). Duplicate-id and duplicate-URL checks run
before any append; the registry census must exit 0 at round end.

## Erratum against the frozen declaration (round 72; append-only)

Written after the wave's reviews, before the round report. No predicate, counter, kill rule,
target or control label above is changed; the frozen eight-case scores stand at the repaired
content (`.ufo/waves/round-72/receipts/re-measure-r72.txt`).

1. **"Last parsed" is implemented literally.** `RevC1` F1 and `CriticClaims` Counterexample B
   showed the first implementation selected the last *prefix-matching* line and then rejected
   it, so a trailing `MADO_LANDING_COUNTERS_SELFTEST: runner cleanup complete` suppressed an
   earlier valid summary. The repair scans backward for the last line that fully parses; both
   repros are pinned as harness selftest regressions (87/87). Red-before/green-after:
   `.ufo/waves/round-72/receipts/c1-r72-repair.txt` (`credit` False→True, `summary_green`
   False→True).
2. **The failure-line grammar is the production emitter's.** `RevC1` F2 showed
   `count_fails`'s `startswith("SELFTEST FAIL")` accepted `SELFTEST FAILURE: …`. The repair
   counts only `^SELFTEST FAIL [0-9]+: ` (the grammar `quality/landing-counters.sh:18` emits);
   red-before/green-after in the same receipt (`credit` True→False; `count_fails` 1→0).
3. **Stream precedence is a declared limit, not a claim.** `RevC2`'s Medium finding: the harness
   reads `stdout + stderr` (the r71 capture order), so an stderr summary precedes every stdout
   summary in the concatenation whatever the real emission order; "last" means last in that
   captured concatenation, not interleaved chronological last. Separate pipes cannot be
   interleaved after the fact; an interleaving witness is future ground.
4. **The C2 eight-case set is finite.** It contains no zero-denominator case and no
   valid-then-garbled tail (`CriticClaims` Counterexample A/B): the successor's `total > 0`
   guard and the repaired parse are covered by its selftest (25/25), not by the frozen eight.
   A later round adds those controls under a new frozen denominator, never by widening this one.
5. **Setup failure after a green summary is `TARGET_MET` by design** (`RevC2` informational):
   the verdict is the summary-and-kills predicate, never a claim that the child's whole
   execution succeeded; the receipt records the rc as evidence.
