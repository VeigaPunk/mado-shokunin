# mado round 73 — frozen claims declaration

author: mado L1 (hyaku run 15, attempt 1)
date: 2026-11-04 (America/Sao_Paulo)
base: `d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce` (round-72 closure tip; lane clean at freeze:
`tracked=0 untracked=0`)
round: mado lane counter 73. Shape: ONE v1 wave of 13 seats (band 8–16); the L1 holds the
planner seat (the validator rejects `planner` as a swarm role).

This file is written **before** any candidate measurement. The pre-freeze do-nothing receipt is
`.ufo/waves/round-73/control-baseline-r73.txt`, produced by the uncommitted prototype
`.ufo/waves/round-73/proto/held-r73.py` (not a scored counter) at the base revision. Frozen
control sets: `.ufo/waves/round-73/controls/c1-outcomes-r73.json` and
`.ufo/waves/round-73/controls/c2-cases-r73.json` (digests in the receipt). Nothing here changes
after the first candidate run; a miss is an honest stop.

## Axis posture

At the base rev every published finite sub-axis sits at its measured maximum (navigation 87/87,
calibration resolved-active 86/86, operability selftest 12/12, ledger 125/125; gate
`MADO_SELFTEST: 460/460`). No axis is distinctly lowest, so the lowest-axis obligation has no
distinct target; the stagnation nudge does not apply either (last capability row entered round
72, window N=3, gap 0). Both claims take **new finite denominators** rather than re-scoring a
held rule on new inputs: C1 scores the frozen outcome set's discriminating power over named rule
mutations; C2 scores the guard census's carrier grammar.

## C1 — calibration: the frozen outcome set separates the four named rule mutations

- **Target surface.** The frozen summary/outcome control set that decides whether the landing
  instrument's outcome rule is correct: round 72's eight cases passed a rule with the `n > 0`
  guard deleted (its own mutation battery recorded the survivor as GAP-1) and passed the
  pre-repair prefix-matching parse (its F1 repair was selftest-only). The set could not tell a
  correct rule from two broken ones.
- **Before.** The held round-72 eight-case denominator, scored against the four named mutations
  of the round-72 outcome rule: `killed=2/4` — N1 (`n > 0` guard dropped) and N2 (last
  prefix-matching parse) survive (`control-baseline-r73.txt`).
- **After (frozen sentence).** Each of the four named mutations of the committed round-72 rule
  answers at least one case of the round-73 ten-case set differently from the case's frozen
  truth, and the whole four are separated: `killed=4/4`; the held eight-case set separates only
  two. The ten cases are the round-72 eight carried byte-identically (hash-checked) plus
  `zero-denominator` (a `0/0` summary must not be green) and `valid-then-garbled` (a malformed
  trailing marker must not suppress the last parsed summary).
- **Counting command.** `python3 -I quality/counters/c1-r73-summary-mutants.py --repo . --rev
  REV --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce --scratch-root DIR`; last line
  `MADO_R73_MUTANT_KILL: cases=10 mutants=4 killed=4 base_killed=2 verdict=TARGET_MET rev=<sha>`,
  exit 0.
- **Named mutations** (literal substitutions of the committed harness bytes, each asserted to
  apply exactly once and to be the only delta): N1 `return passed == total`; N2 the prefix-match
  `last_parsed_summary`; N3 `return total > 0 and passed <= total`; N4 `outcome_verdict` on the
  kill count alone. Each mutation is the round-72 record's own named variant (M3, F1, M2-family,
  M4).
- **Kill rule.** `TARGET_MET` iff `cases == 10`, `mutants == 4`, `killed == 4` and
  `base_killed == 2`; `TARGET_MISSED` otherwise. Exit 0 iff met; 1 iff measured and missed (an
  absent candidate harness prints `killed=absent`); 2 on usage/setup error with the reason on
  stderr and no contract line. Bounded score `10 × killed / 4` → 10.0000 (held 5.0000).
- **Do-nothing control.** The held eight-case denominator scored in the same run; it must kill
  exactly two (`base_killed=2`) or the counter or the target is wrong.
- **Declared limits.** Four named mutations of one rule family are not fault coverage; the
  sub-wait is a bounded syntactic mutation of the committed source, not an arbitrary program
  mutation; the counter scores the committed decision functions, not a harness execution; a
  mutation that changes behaviour only outside these ten cases is not counted.

## C2 — operability: the guard census counts the global-declared guard and the mutated-environment transport

- **Target surface.** `quality/check-*.py` guard census (`c2-*-shapes.py` chain): the round-71
  classifier counts a guard only through a literal/mapping/alias/attribute environment. Two real
  idioms escape it: a module mapping guarded from inside a function that declares the name
  `global`, and the process environment mutated with the key and then copied into the child with
  `{**os.environ}` or `dict(os.environ)`.
- **Before.** The held round-71 classifier on the round-73 twenty-eight-case set: `25/28`,
  missing exactly `global-rebind-guard`, `environ-splat-guard`, `environ-call-guard`
  (`control-baseline-r73.txt`).
- **After (frozen sentence).** The successor counts (a) a `global`-declared name that a function
  stores the guard key into (or rebinds to a mapping carrying it) and that a later git launch
  hands as `env=`, and (b) a store of the guard key into `os.environ` before a git launch whose
  `env=` is a dict-splat of `os.environ` or a `dict(os.environ)` call; the twenty-three
  round-71 cases stay byte-identical and the two round-71 bypass fixtures stay refused.
- **Counting command.** `python3 -I quality/counters/c2-r73-shapes.py --repo . --rev REV
  --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce --controls
  .ufo/waves/round-73/controls/c2-cases-r73.json --scratch-root DIR`; last line
  `MADO_R73_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=28/28
  base_controls=25/28 verdict=TARGET_MET rev=<sha>`, exit 0.
- **Kill rule.** `TARGET_MET` iff population 20, readers 13, guarded 13, unguarded 0,
  `controls == 28` and `base_controls == 25`; `TARGET_MISSED` otherwise; same exit map as C1.
  Bounded score `10 × controls / 28` → 10.0000 (held 8.9286).
- **Do-nothing control.** The held round-71 classifier at `--base-rev` scored on the same
  twenty-eight cases in the same run; it must score exactly 25/28.
- **Declared limits.** One `global` declaration, line-order dominance across functions (the same
  cross-method approximation the attribute flow already declares); one `os.environ` store and
  the two copy spellings; no cross-module producer, no two-hop alias chain; a syntactic
  approximation that does not interpret values.

## No-harm obligations (both claims)

`bash tools/mado-verify.sh --selftest` stays 460/460; the frozen round-72 harness and the
round-71/70 classifiers stay byte-identical; the index, ledger, axis table and navigation checks
stay at their measured values; both new instruments enter `quality/tool-ledger.md` and the
`SKILL.md` Gate registry in the same round (`quality/check-tool-ledger.py` `uncovered=0`).
Neither claim touches configuration, the compositor, a service, a sibling repo or `~/.config`.

## Sources plan (frontier step)

Up to three new rows opened this round with three byte-identical fetches each (receipts under
`.ufo/waves/round-73/fetch/`): CPython 3.14.8 `Doc/reference/simple_stmts.rst` (the `global`
statement), `Doc/library/os.rst` (`os.environ`), and `Doc/library/subprocess.rst` (`env`
parameter) — the C2 entry cites them. Duplicate-id and duplicate-URL checks run before any
append; the registry census must exit 0 at round end.

## Erratum against the frozen declaration (round 73; append-only)

E1. **The §C1 counting-command line omits `--controls`.** The counter requires it and refuses
with exit 2, the reason on stderr and no contract line
(`--repo, --rev and --controls are required`); the frozen set argument is
`.ufo/waves/round-73/controls/c1-outcomes-r73.json`. The pinned invocation is:

    python3 -I quality/counters/c1-r73-summary-mutants.py --repo . --rev REV \
        --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce \
        --controls .ufo/waves/round-73/controls/c1-outcomes-r73.json --scratch-root DIR

No predicate, counter, kill rule, target, control label or measured value changes; the receipt at
`1459cca1` used this invocation. Found by the wave's `R73RevC1` seat (F1) before the report.

E2. **Wave-review repairs (both claims re-measured at `84fc266a5bf6db6cf12b6aa6106ad33121f391be`).**
The wave's `R73RevC1` and `R73RevC2` found five defects, all repaired without touching a frozen
predicate, control set, case label, kill rule or target; receipts
`.ufo/waves/round-73/receipts/repair-c1-r73.txt` and `repair-r73.txt`.

- **C1 F2 (provenance):** `--base-rev` was displayed but never resolved. The counter now resolves
  it, extracts the candidate harness at `--base-rev`, refuses a base/candidate byte difference, and
  scores the held eight-case set with the base harness (`held_set=8/8`), printing
  `MADO_R73_BASE_PROVENANCE`. Red: the old counter with `--base-rev NO_SUCH_BASE_R73` printed the
  contract line, rc 0. Green: the repaired counter exits 2 (`cannot resolve NO_SUCH_BASE_R73`) and
  rc 0 with the real base.
- **C1 F1 (usage example):** the module docstring's usage line omitted `--controls`; it now names it
  and the selftest asserts the docstring carries the flag (26/26).
- **C2 F1 (scope shadow):** a launch inside a function that binds the name as a parameter or a
  non-global local was credited as the module binding. The detector now refuses such a launch; the
  reviewer's `false-global-parameter-shadow.py` flips `(True, True)` → `(True, False)`, pinned as
  regression `r73-global-parameter-shadow`.
- **C2 F2 (over-broad cancellation):** any plain rebinding of the name anywhere cancelled the store.
  Cancellation is now restricted to assignments that resolve to the module binding (module level or
  another `global`-declaring function); the reviewer's `true-global-unrelated-local-rebind.py` flips
  `(True, False)` → `(True, True)`, pinned as `r73-global-unrelated-local-rebind`.
- **C2 F3 (key deletion):** `del os.environ[KEY]` between store and launch was ignored. A guarded
  delete now cancels the store; `false-environ-key-deleted.py` flips `(True, True)` →
  `(True, False)`, pinned as `r73-environ-key-deleted`.

C2 selftest 75/75 → 78/78, C1 25/25 → 26/26. Re-measurement at the repair commit: `cases=10
mutants=4 killed=4 base_killed=2 verdict=TARGET_MET` rc 0 and `population=20 readers=13 guarded=13
unguarded=0 controls=28/28 base_controls=25/28 verdict=TARGET_MET` rc 0 — the same verdicts and
counts as at `1459cca1`; the frozen 28-case and 10-case sets score identically before and after the
repair. The reviewer's two remaining line-order observations (F4) stay declared limits.
