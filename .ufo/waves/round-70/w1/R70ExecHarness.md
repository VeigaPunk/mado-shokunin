# R70ExecHarness — `c1-r70-landing-controls.py`: exact behavioural delta vs the frozen r69 harness

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` @ `5144a6b5f43225d8021a469f4d24c19558026b9e`
(base `b37a5aec4ea03f2223d8e09dd5d386d055c24179`). Declaration read first and not edited.
No production file, control JSON or baseline receipt was touched; the only lane write is this report.

| instrument | bytes | sha256 |
|---|---|---|
| `quality/counters/c1-r69-landing-controls.py` | 38461 | `9461a059466e723ba0ae88c86dea2fc97eb5f4fdfb15ef6c6646acce69649a73` |
| `quality/counters/c1-r70-landing-controls.py` | 41677 | `71a7b6c45b904a734f194be9a8de6cc2eeb5f5ea1922760f908f5637f1d4db58` |
| `.ufo/waves/round-70/proto/fixture-lane.tmpl` | — | `9e31681dd95976af4b107566b1710a50d962b9af36d3e5db6b73078393c91b6f` |

The r69 harness is byte-identical at `5144a6b` and at the base:
`git diff --quiet b37a5aec… 5144a6b… -- quality/counters/c1-r69-landing-controls.py` → **rc 0**.

## 1. Diff classification

Command: `diff -u quality/counters/c1-r69-landing-controls.py quality/counters/c1-r70-landing-controls.py`
(rc 1 = differ; 23 hunks; 93 insertions, 39 deletions; r69 875 lines → r70 929 lines).

| # | hunk (r69 → r70) | class | content |
|---|---|---|---|
| 1 | `-1,9 +1,17` | docstring only | title rewrite + new "Difference from r69" paragraph |
| 2 | `-12,7 +20,7` | docstring only | extraction dir `r69-c1` → `r70-c1` in prose |
| 3 | `-23,7 +31,9` | docstring only | M-Z rule text now says "AND a parseable `<p>/<n>` with p < n" |
| 4 | `-36,9 +46,9` | docstring only | contract-line/evidence marker text R69 → R70 |
| 5 | `-49,11 +59,12` | docstring only | "Declared limits" rewritten (real children moved to the new counter) |
| 6 | `-65,7 +76,7` | marker/name only | `TOOL = "c1-r70-landing-controls.py"` (usage-error text; `argparse` prog) |
| 7 | `-84,7 +95,7` | selftest only | `CONTRACT_RE` R69 → R70 (regex used only in `_selftest_checks`, lines 681/699/798) |
| 8 | `-301,6 +312,21` | **measurement** | new `summary_shows_failure()` predicate |
| 9 | `-324,7 +350,7` | marker only | `contract_line()` string R69 → R70 (printed receipt) |
| 10 | `-357,8 +383,8` | measurement-adjacent (metadata) | R-fixture commit identity `r69-c1` → `r70-c1` (user.name/email/message) |
| 11 | `-403,7 +429,7` | measurement-adjacent (path) | work dir `<scratch>/r69-c1` → `<scratch>/r70-c1` |
| 12 | `-411,15 +437,15` | marker only | emit markers EXTRACT ×3, SELFTEST |
| 13 | `-449,10 +475,10` | **measurement** | the credit expression + emit marker M-Z |
| 14 | `-464,19 +490,19` | marker only | emit markers GUARDS, R_CONTROL, CHILD_ENV, R_CHILD |
| 15 | `-507,7 +533,7` | marker only | emit marker MUTANT M-R |
| 16 | `-619,7 +645,7` | selftest only | captured-contract filter R69 → R70 |
| 17 | `-640,7 +666,7` | selftest only | expected `both-killed` line string |
| 18 | `-648,7 +674,7` | selftest only | expected `none-killed` line string |
| 19 | `-657,7 +683,7` | selftest only | expected `mr-crash` line string |
| 20 | `-666,11 +692,39` | selftest only | expected `mz-unparseable` line + 2 new scripted cases (`mz-crash`, `mz-allpass`) + 5 predicate asserts |
| 21 | `-744,7 +798,7` | selftest only | `contract_line()` unit-test string |
| 22 | `-828,8 +882,8` | selftest only | selftest FAIL/summary markers |
| 23 | `-839,7 +893,7` | selftest only (path) | selftest scratch dir `r69-c1-selftest` → `r70-c1-selftest` |

Totals: 5 docstring-only, 5 marker/name-only (production), 9 selftest-only, 2 measurement, 2
measurement-adjacent (scratch path, fixture commit identity).

**Every measurement-body difference, named (exhaustive):**

- **M1 — the credit decision** (`quality/counters/c1-r70-landing-controls.py:478`):
  `mz_killed = mz_rc != 0` → `mz_killed = bool(mz_rc != 0 and summary_shows_failure(mz_out))`.
  Both gates are needed: a nonzero exit *and* a parsed failed-assertion summary.
- **M2 — the new predicate** (`:315-328`): `summary_shows_failure()` takes `last_summary(out)`
  (last line starting `MADO_LANDING_COUNTERS_SELFTEST:` in stdout+stderr), `re.fullmatch`es
  `MADO_LANDING_COUNTERS_SELFTEST: (\d+)/(\d+) assertions passed`, and returns
  `total > 0 and passed < total`; anything else (no summary, garbled, `0/0`) is `False`.
- **M3 — scratch work dir** `r69-c1` → `r70-c1` (`:429`). Path only; no effect on any verdict.
- **M4 — R-fixture commit identity** `r69-c1` → `r70-c1` (`:386-387`). Fixture metadata inside a
  throwaway repo the harness creates; no effect on the decision.

Not measurement: the `TOOL` constant (usage text), every emitted marker, the printed contract
line text, `CONTRACT_RE`, the module docstring (it does feed `argparse(description=__doc__…,
line 907)`, so `--help` text changed, nothing else), and the 9 added selftest assertions.
Unchanged: env scrubbing, extraction, `last_summary`/`summary_fraction`/`count_fails`, the whole
M-R leg, `outcome_verdict`, `BASELINE="0/2"`, exit map (0 iff selftest rc 0 and killed 2/2).
`mz_fails` and `mz_summary` are still computed and printed but are **evidence only** — the
decision reads neither.

## 2. Selftests

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I quality/counters/c1-r69-landing-controls.py --selftest --scratch-root /fast/scratch/hyaku/mado-r70/R70ExecHarness/a
  MADO_R69_LANDING_CONTROLS_SELFTEST: 59/59 assertions passed     rc 0
python3 -I quality/counters/c1-r70-landing-controls.py --selftest --scratch-root /fast/scratch/hyaku/mado-r70/R70ExecHarness/b
  MADO_R70_LANDING_CONTROLS_SELFTEST: 68/68 assertions passed     rc 0
```

68 − 59 = **+9**, exactly the added scripted cases `mz-crash` (2), `mz-allpass` (2) and the five
`summary_shows_failure` unit asserts.

## 3. Fixture lane, real children, both harnesses

Own scratch fixture (git repo under `…/R70ExecHarness/step3/fx`, `git init` in that dir, toplevel
asserted equal before the first commit, `-C` on every git call, explicit
`user.name=r70-probe / user.email=r70-probe@example.invalid`). Children extracted at `5144a6b`
(`c3-r56-used-by.py`, `check-tool-ledger.py`, `mado-receipt-citecheck.py`); lane generated from
`.ufo/waves/round-70/proto/fixture-lane.tmpl` per mode, one commit per mode, clause count 1 in
every commit. The `genuine`/`crash`/`garbage` branches are the frozen template text unchanged;
`signal` and `falsegreen` are modes I added (extra `case` arms) for this audit.

Direct child behaviour (mutated = the exact frozen clause `[ "$citations" -gt 0 ] && ` deleted once):

| mode | unmutated | mutated |
|---|---|---|
| genuine | rc 0, `2/2 assertions passed` | rc 1, `1/2 assertions passed` |
| crash | rc 0, `2/2 assertions passed` | **rc 2, no summary** |
| signal (mine) | rc 0, `2/2 assertions passed` | **rc −15 (SIGTERM), no summary** |
| garbage | rc 0, `2/2 assertions passed` | rc 1, `??? assertions passed` |
| falsegreen (mine) | rc 0, `2/2 assertions passed` | **rc 0, `1/2 assertions passed`** |

Harness contract lines (`--repo <fx> --rev <mode-rev> --scratch-root <fresh>`):

```
genuine  r69 rc 0  MADO_R69_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET rev=ed62c1274a3b208ec7d5f9fd3a97937b1af45649
genuine  r70 rc 0  MADO_R70_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET rev=ed62c1274a3b208ec7d5f9fd3a97937b1af45649
crash    r69 rc 0  MADO_R69_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET rev=5279846784a3b08629d767340caae4fcc158f693
crash    r70 rc 1  MADO_R70_LANDING_CONTROLS: selftest=0 mz=fail mr=pass killed=1/2 baseline=0/2 verdict=TARGET_MISSED rev=5279846784a3b08629d767340caae4fcc158f693
signal   r69 rc 0  MADO_R69_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET rev=9e4aae4a37a5761b581ca8000e1173a7e2c63b7d
signal   r70 rc 1  MADO_R70_LANDING_CONTROLS: selftest=0 mz=fail mr=pass killed=1/2 baseline=0/2 verdict=TARGET_MISSED rev=9e4aae4a37a5761b581ca8000e1173a7e2c63b7d
garbage  r69 rc 0  MADO_R69_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET rev=1a06198cb0ebbfd91cd916cdc8445f1f0747e51a
garbage  r70 rc 1  MADO_R70_LANDING_CONTROLS: selftest=0 mz=fail mr=pass killed=1/2 baseline=0/2 verdict=TARGET_MISSED rev=1a06198cb0ebbfd91cd916cdc8445f1f0747e51a
falsegreen r69 rc 1 MADO_R69_LANDING_CONTROLS: selftest=0 mz=fail mr=pass killed=1/2 baseline=0/2 verdict=TARGET_MISSED rev=e08fe5bb3411e79b9ecc50c2b14125ebcd92cb3e
falsegreen r70 rc 1 MADO_R70_LANDING_CONTROLS: selftest=0 mz=fail mr=pass killed=1/2 baseline=0/2 verdict=TARGET_MISSED rev=e08fe5bb3411e79b9ecc50c2b14125ebcd92cb3e
```

The r70 M-Z evidence line on the crash rev, which carries the whole delta:

```
MADO_R70_MUTANT M-Z path=quality/landing-counters.sh clause_count=1 recipe=clause-delete
  removed='[ "$citations" -gt 0 ] && ' rc=2 failed_assertions=0 assertions=none killed=no sha256=bd0c0b2b…
MADO_R69_MUTANT M-Z … rc=2 failed_assertions=0 assertions=none killed=yes sha256=bd0c0b2b…
```

Required properties hold: genuine credited by both; on the exit-2/no-summary mode the r70 harness
does **not** credit and the r69 harness **does**; the delta is visible not just in `mz=` but in
the verdict (`TARGET_MISSED` rc 1 vs `TARGET_MET` rc 0). The r69 harness therefore *passes the
claim* on a lane that merely broke. `signal` shows the same split for a signal death (rc −15), and
`garbage` for an unparseable summary.

## 4. Frozen r69 recipes R1/R2/R3 applied to a scratch copy of the r70 harness

Recipe texts taken verbatim from `quality/counters/c1-r69-paired-recipes.py` (`R1_OLD`/`R1_NEW`,
`("R2", "mz_killed = mz_rc != 0", …)`, `("R3", "subprocess.run = _no_spawn", …)`), each applied
once to a copy under `…/R70ExecHarness/step4/<R>/candidate.py`.

| recipe | occurrences | hit line(s) | inside docstring? | `py_compile` | selftest rc / tally | killed |
|---|---|---|---|---|---|---|
| R1 | 1 | 530 | no (code) | rc 0 | rc 1, 66/68 | **yes** (`mr-crash` decision + exit assertions fail) |
| R2 | **1** | **8** | **yes (docstring spans 2–68)** | rc 0 | rc 0, 68/68 | **no** |
| R3 | 1 | 866 | no (selftest guard) | rc 0 | rc 1, 66/68 | **yes** (`spawn guard installed` + `spawn under guard raises` fail) |

`bash -n` is not applicable to a Python source; `python3 -m py_compile` was used (rc 0 on all
three mutants).

**R2 is superseded in behaviour, but not absent as text.** The executable branch is
`mz_killed = bool(mz_rc != 0 and summary_shows_failure(mz_out))`; no `mz_killed = mz_rc != 0`
statement exists anywhere in the r70 body. The single textual occurrence is a prose quotation of
the round-69 line in the module docstring (`(``mz_killed = mz_rc != 0``), so a child that
crashes…`). Applying R2 therefore rewrites a sentence and changes nothing semantically: the mutant
still prints 68/68 and exits 0. Classified as **expected supersession**, not a defect.

Consequence of the docstring decoy: if the r69 recipe counter were pointed at a file containing
only the r70 harness, it would report `recipe=R2 occurrences=1 … killed=no`, i.e.
`killed=2/3` → `TARGET_MISSED`, rather than declaring the recipe inapplicable. The r70 claim does
not inherit those recipes, so nothing in round 70 is scored wrong; the only cost is that the old
suite cannot say "the hazard is gone", only "the mutant survived". Advisory (no edit made): the
docstring quotation is the reason, and it could be reflowed to break the exact byte string if a
future round ever wants the old suite to read `occurrences=0`.

`c1-r69-paired-recipes.py` hard-codes `CANDIDATE = "quality/counters/c1-r69-landing-controls.py"`
and never follows the successor. Measured on a scratch clone of the lane at a rev whose only
change was `git rm quality/counters/c1-r69-landing-controls.py` (clone at
`…/R70ExecHarness/clone/lane`, toplevel asserted, explicit identity, HEAD `c66ca6897b0f…`):

```
python3 -I quality/counters/c1-r69-paired-recipes.py --repo . --rev HEAD --base-rev b37a5aec… --scratch-root …
MADO_R69_EXTRACT path=quality/counters/c1-r69-landing-controls.py present=no sha256=absent
…
MADO_R69_PAIRED_RECIPES: selftest=absent killed=0/3 applied=0/3 base=0/3 verdict=TARGET_MISSED rev=c66ca6897b0f10a0bd1c90e14cbad3855ee2e181
rc 1
```

So the r69 counter degrades to a clean miss (rc 1, not a setup error rc 2) on an r70-only rev: it
does not silently re-target the successor and does not crash.

## 5. Frozen r69 counter at the scored rev

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I quality/counters/c1-r69-paired-recipes.py --repo . --rev 5144a6b5f43225d8021a469f4d24c19558026b9e \
  --base-rev b37a5aec4ea03f2223d8e09dd5d386d055c24179 --scratch-root /fast/scratch/hyaku/mado-r70/R70ExecHarness/r69
rc 0
MADO_R69_PAIRED_RECIPES: selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET rev=5144a6b5f43225d8021a469f4d24c19558026b9e
```

Supporting lines: candidate sha256 `9461a059…` (identical to base), selftest `59/59`, R1/R2/R3
each `occurrences=1 rc=1 killed=yes`; base r68 `25470bc4…` R1/R2/R3 `rc=0 killed=no`.
Harm-watch line holds exactly.

## 6. Fail-closed direction of the new predicate

Driven through the real `measure()` body with scripted children (import of the module,
`_measure_case`), plus a direct `summary_shows_failure` call on each input, rev `aaaa…`:

| input summary | child rc | `summary_shows_failure` | `mz=` | killed |
|---|---|---|---|---|
| `0/0 assertions passed` | 1 | **False** (total > 0 required) | fail | 0/2 |
| `1/2 assertions passed` | **0** | **True** | **fail** | 0/2 |
| `1/2 assertions passed` | 1 | True | **pass** | 1/2 |
| `62/62 assertions passed` | 1 | False | fail | 0/2 |
| no summary (crash) | 2 | False | fail | 0/2 |
| `??? assertions passed` | 1 | False | fail | 0/2 |

Resulting lines (all `… baseline=0/2 verdict=TARGET_MISSED rev=aaaa…`):
`MADO_R70_LANDING_CONTROLS: selftest=0 mz=fail mr=fail killed=0/2 …` for `0/0`-rc1 and
`1/2`-rc0; `MADO_R70_LANDING_CONTROLS: selftest=0 mz=pass mr=fail killed=1/2 …` for `1/2`-rc1.

Both requested constructions fail closed (`mz=fail`), for different reasons: `0/0` because the
predicate refuses a zero-total summary; `1/2` with rc 0 because the exit-status gate is still
required.

**Residual hazards (stated, not fixed):**

- A mutant that fails an assertion (summary `p<n`) but **exits 0 is not credited** — a false
  negative. This is by design (both gates), but it means the harness cannot credit a lane whose
  assertion failure does not propagate into its exit status.
- Symmetrically, a child that emits a failing summary and then exits nonzero **for an unrelated
  reason** (crash after printing, a broken pipe, a missing program) **is credited** — the harness
  proves "failed summary + nonzero exit", not "the nonzero exit was caused by the failed
  assertion".
- The decision uses only the *last* `MADO_LANDING_COUNTERS_SELFTEST:` line in combined
  stdout+stderr and ignores `count_fails(out)` (the `SELFTEST FAIL` lines are printed as evidence
  but never consulted). A child that prints a stale failing summary last, or a failing summary
  with no `SELFTEST FAIL` line, is credited on the summary alone.
- `last_summary` returns `"none"` when absent, so `re.fullmatch` cannot match by accident; an
  extra-precision suffix on the summary line (e.g. trailing text) would parse as *not* a failure,
  i.e. that direction is fail-closed too.

## 7. Risks / blockers

- No blocker. The r70 harness's only behavioural delta is M1+M2; nothing else in the measurement
  body moved, so the round-69 extraction/M-R leg carries over unchanged.
- R2 docstring decoy (§4) is the one finding that could surprise a later round: the frozen r69
  recipe text survives in the r70 docstring, so an old-recipe suite reports `killed=2/3` instead
  of `occurrences=0`. Advisory only; I did not edit the harness.
- `c1-r69-paired-recipes.py` cannot follow a successor (hard-coded candidate) — noted, by design.
- The harness itself still claims nothing about real children; that evidence lives in
  `c1-r70-real-children.py`. My step-3 run is an independent confirmation, not a substitute.

## 8. Hygiene / tooling

- Scratch `/fast/scratch/hyaku/mado-r70/R70ExecHarness/` (scripts `step3.py`, `step4.py`,
  `step6.py`, fixtures, clone) — **removed** before yield; `git` fixtures lived only there.
- No pacman/uv/npx install or upgrade was needed; no tool version changed.
- No mutation of the lane, the fleet repo, sibling lanes or config; no commit/stage/checkout in
  the lane; clone experiment confined to scratch (`git rm` + commit only inside that clone).
- Only lane write: this file, `.ufo/waves/round-70/w1/R70ExecHarness.md`.
- Observed concurrent, **not mine**: `git status` shows `M SCORECARD.md` (mtime 2026-11-03
  23:36:34, +61 lines, a "Round 70" section). Another seat wrote it during this wave; I did not
  touch, stage or revert it. No other tracked path is modified.
