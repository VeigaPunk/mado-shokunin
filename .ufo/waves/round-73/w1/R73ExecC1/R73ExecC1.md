# R73ExecC1 — independent drive of claim C1 (round mado 73)

Seat: leaf executor, wave 1, round 73. No committed lane file touched; all work under
`.ufo/waves/round-73/w1/R73ExecC1/` and scratch `/fast/scratch/hyaku/mado-r73/R73ExecC1/`
(deleted after copying cited receipts here). No tool installed or upgraded (none needed).

## 1. Exact commands run (cwd `/home/vgpnk/Projects/shokunin/mado-shokunin`)

```
python3 -I quality/counters/c1-r73-summary-mutants.py --repo . \
  --rev 1459cca11fb5d3956a6e9a128217852dd0c28cb9 \
  --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce \
  --controls .ufo/waves/round-73/controls/c1-outcomes-r73.json \
  --scratch-root /fast/scratch/hyaku/mado-r73/R73ExecC1/run
```
rc=**0**; stderr empty; stdout archived at `c1-run-r73.txt` (this dir). Last line:

```
MADO_R73_MUTANT_KILL: cases=10 mutants=4 killed=4 base_killed=2 verdict=TARGET_MET rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9
```

```
python3 -I quality/counters/c1-r73-summary-mutants.py --selftest \
  --scratch-root /fast/scratch/hyaku/mado-r73/R73ExecC1/run
```
rc=**0**; last (only) line: `MADO_R73_MUTANT_KILL_SELFTEST: 24/24 assertions passed`
(archived at `selftest-r73.txt`). The selftest is hermetic as documented: it installs a
no-spawn guard for its body and writes only `cases-tampered.json` under the given scratch root.

Full stdout of the measurement run (rc 0):

```
MADO_R73_CONTROLS path=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-73/controls/c1-outcomes-r73.json cases=10 sha256=263b3c5a288c45a59587890a7e4c2e6dc3389630e5dd4a5cd1731976b5d2832b
MADO_R73_REVS rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9 base=d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce
MADO_R73_HELD_CONTROLS path=.ufo/waves/round-72/controls/c2-controls-r72.json cases=8 sha256=640fb44fdb1f31b4706b381c905fde4b5dae769bfd3e5b656bdb374bad58a793 carried=yes
MADO_R73_HARNESS role=candidate path=quality/counters/c1-r72-landing-controls.py present=yes sha256=b6108c86e8e03befce50256e2381ec08f199a1ab7fe192aeedef70459c45857d
MADO_R73_PRISTINE correct=10/10 misses=-
MADO_R73_MUTANT mutant=N1-zero-guard-dropped new=9/10 killed=yes misses=zero-denominator | held=8/8 killed=NO misses=-
MADO_R73_MUTANT mutant=N2-last-prefix-match new=9/10 killed=yes misses=valid-then-garbled | held=8/8 killed=NO misses=-
MADO_R73_MUTANT mutant=N3-pass-le-total new=8/10 killed=yes misses=failing-summary-exit0,failing-summary-exit2 | held=6/8 killed=yes misses=failing-summary-exit0,failing-summary-exit2
MADO_R73_MUTANT mutant=N4-kill-count-only new=4/10 killed=yes misses=failing-summary-exit0,no-summary-exit0,garbled-summary-exit0,failing-summary-exit2,no-summary-exit2,zero-denominator | held=3/8 killed=yes misses=failing-summary-exit0,no-summary-exit0,garbled-summary-exit0,failing-summary-exit2,no-summary-exit2
MADO_R73_KILLED killed=4/4 base_killed=2/4 (the held eight-case set must separate only two)
MADO_R73_MUTANT_KILL: cases=10 mutants=4 killed=4 base_killed=2 verdict=TARGET_MET rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9
```

## 2. Reconciliation with the committed receipt `measurement-c1-r73.txt`

Mechanical: `diff -u .ufo/waves/round-73/measurement-c1-r73.txt <my run stdout>` →
byte-identical (`DIFF_IDENTICAL`); rc 0 both; my run's stderr 0 bytes. Digests re-confirmed
independently: frozen controls `263b3c5a…`, held controls `640fb44f…`, harness at the rev
`b6108c86…` (extracted via `git show 1459cca…:quality/counters/c1-r72-landing-controls.py`
and sha256'd — matches the receipt's `MADO_R73_HARNESS` line; read-only git only).

**Differences: none.** Every receipt line reproduces, same order, same last line, same rc.
The committed receipt contains no selftest line, so there is nothing to reconcile there; the
frozen sentence's `--selftest` expectation (hermetic, 0 rc) is satisfied at 24/24.

## 3. The MUTANTS table and which rule each mutation breaks

Verified against the rule bodies extracted at the pinned rev (`last_parsed_summary` uses a
strict `re.fullmatch(r"MADO_LANDING_COUNTERS_SELFTEST: [0-9]+/[0-9]+ assertions passed")`
filter; `summary_green` ends `return total > 0 and passed == total`; `outcome_verdict` is
`"TARGET_MET" if summary_green(out) and killed == 2 else "TARGET_MISSED"`), and against the
case bytes of both frozen control files — not by trusting the printed per-mutant lines. The
measure loop itself asserts each `old` substitution applies exactly once and changes the bytes
before scoring, and the pristine module answers 10/10 (case gate_out/killed bytes drive every
verdict through `exec`-loaded functions; the harness is never executed).

- **N1-zero-guard-dropped** — `summary_green`'s `total > 0 and passed == total` becomes
  `passed == total` (the round-72 battery's M3): the zero-denominator guard is gone, so a
  `0/0` summary greens because 0==0. The only case in the ten where equality holds with
  `total == 0` is `zero-denominator` (`0/0 assertions passed`, frozen truth TARGET_MISSED);
  every other parseable summary has total=12, so nothing else moves. Separated by exactly
  `zero-denominator` → new 9/10, killed. The held eight cases contain no `0/0` case, so the
  held set cannot tell this rule from the correct one: held 8/8, killed=NO — the declared
  GAP-1 survivor.
- **N2-last-prefix-match** — the reversed scan's strict fullmatch filter becomes a bare
  `line.startswith("MADO_LANDING_COUNTERS_SELFTEST:")` (the pre-repair F1 parse): the scan
  stops at the last line that merely starts with the marker, even when it is not a summary.
  Only `valid-then-garbled` ends with a prefixed non-summary line (`…: runner cleanup
  complete` after a valid `12/12`), so the mutant returns the cleanup line, the parse fails,
  and the verdict flips to TARGET_MISSED against frozen truth TARGET_MET. `garbled-summary-exit0`
  (`twelve/twelve`) matches neither spelling and stays MISSED either way; the held set has no
  trailing marker line, so held 8/8, killed=NO — the selftest-only-F1-repair story.
- **N3-pass-le-total** — `==` becomes `<=` (the M2 family): a summary with fewer passes than
  assertions still greens. Separated by the two failing cases carrying `killed=2`,
  `failing-summary-exit0` (3/12) and `failing-summary-exit2` (11/12). Both live in the held
  set too, so the held set kills it as well (held 6/8, same two misses) — killed by both
  denominators, hence not a GAP case.
- **N4-kill-count-only** — `outcome_verdict` drops the `summary_green(out) and` conjunct (the
  battery's M4): green iff `killed == 2`. It then disagrees with the frozen truth on every
  case whose truth depends on the summary while killed=2: `failing-summary-exit0`,
  `no-summary-exit0`, `garbled-summary-exit0`, `failing-summary-exit2`, `no-summary-exit2`,
  `zero-denominator` (six misses; `green-summary-exit2` and `green-summary-killed1` agree by
  coincidence). On the held set the same five minus `zero-denominator` exist → held 3/8,
  killed=yes.

Tally re-derived from those case bytes: killed 4/4 (N1–N4 each miss ≥1 frozen case);
base_killed 2/4 (only N3 and N4 move on the held set) → kill rule `cases=10 ∧ mutants=4 ∧
killed=4 ∧ base_killed=2` met → `TARGET_MET`, rc 0. Exactly what both my run and the
committed receipt print.

## 4. Retained evidence (copied into this dir before scratch deletion)

- `c1-run-r73.txt` — full stdout of the measurement command (rc 0, byte-identical to the
  committed receipt).
- `selftest-r73.txt` — selftest line, rc 0.
- `harness-r1459.py` sha256 = `b6108c86e8e03befce50256e2381ec08f199a1ab7fe192aeedef70459c45857d`
  (rule bodies quoted in §3 are read from this extraction).

## 5. Risks / limits (declared, observed)

- The counter scores the committed decision functions (`exec` of harness bytes at the rev),
  not a harness execution — a mutant that only changes runtime behaviour outside
  `outcome_verdict`'s inputs is invisible to it (declared limit, confirmed by construction).
- Four named mutations of one rule family are not fault coverage; `base_killed=2` is itself a
  frozen predicate — a future held-set edit that adds a separating case would fail the
  do-nothing control rather than flatter the claim (the counter hard-checks the held file's
  sha and byte-carriage).
- No difference from the committed receipt found; no blocker.
