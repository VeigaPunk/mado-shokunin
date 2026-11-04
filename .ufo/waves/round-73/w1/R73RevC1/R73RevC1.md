# R73RevC1 — adversarial C1 review

Axes: calibration (truth labels and mutant discrimination), reproducibility (pinned command and held baseline), no-harm (read-only production and unchanged carried bytes).

Recommendation: the frozen C1 **sentence survives**: the pinned ten cases separate all four specified mutations, and the held eight separate two. The originally printed counting command does not run. No finding below changes the frozen truth labels or the observed kill counts. This recommendation is not admission, integration, or a global saturation judgment.

## Findings, severity order

### F1 — P2 / conformance-reproducibility: frozen counting command omits mandatory controls

Location: `.ufo/waves/round-73/claims-declaration-r73.md`, C1 Counting command; pinned `quality/counters/c1-r73-summary-mutants.py:458`.

At instrument revision `1459cca11fb5d3956a6e9a128217852dd0c28cb9`, replaying the declaration's argument list without `--controls` exits **2**, emits no stdout/contract line, and prints `c1-r73-summary-mutants.py: --repo, --rev and --controls are required` on stderr. The counter handles missing input correctly; the declaration is incomplete. Its docstring usage example also omits this argument.

Adding `--controls` with the controls bytes extracted from that same revision produces rc **0**, `cases=10 mutants=4 killed=4 base_killed=2 verdict=TARGET_MET`. The explicit-controls selftest returns rc **0**, `MADO_R73_MUTANT_KILL_SELFTEST: 25/25 assertions passed`. Full commands, outputs, and exit codes are in `receipts.json` beside this report. The L1 acknowledged this defect and reported an append-only E1 erratum; this review does not claim to have verified that subsequent edit. The measurement sentence survives; the original invocation did not.

Corrected invocation, from the mado repository root, with an existing seat scratch directory:

```sh
python3 -I quality/counters/c1-r73-summary-mutants.py --repo . --rev 1459cca11fb5d3956a6e9a128217852dd0c28cb9 --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce --controls .ufo/waves/round-73/controls/c1-outcomes-r73.json --scratch-root /fast/scratch/hyaku/mado-r73/R73RevC1
```

### F2 — P3 / provenance weakness: `--base-rev` is displayed, not used

Location: pinned `quality/counters/c1-r73-summary-mutants.py:234-248` (`measure`) and `:197-222` (`held_check`).

Precise reading: only `args.rev` goes through `rev_parse`; `args.base_rev` is interpolated in the REVS line. Both the harness and held control set are extracted at the candidate SHA. Repro: substitute `--base-rev NO_SUCH_BASE_R73REVC1` in the corrected command. Observed rc **0** and the same `killed=4 base_killed=2 TARGET_MET` contract. The displayed base therefore does not establish baseline provenance. Recommendation: do not treat that field as proof of independently extracting the base; validate provenance separately or remove the misleading argument in a later contract revision.

This does **not** refute the frozen comparison: I independently extracted the held file and harness at the real base and instrument revisions and compared their bytes. Both are exactly equal (hashes below). In this pinned experiment the candidate-revision held leg is therefore equivalent to the real-base leg. No production repair is requested within this read-only seat.

### F3 — informational / bounded mutation coverage, not a false kill

Location: pinned `quality/counters/c1-r73-summary-mutants.py:65-83` (`MUTANTS`); harness `:320-330`, `:365-372`, `:393-394`.

All four named deltas apply exactly once. They genuinely implement the named rule changes:

| Mutation | Actual change | Frozen killing cases | Held kills? |
|---|---|---|---|
| N1 | Removes only `total > 0` from green-summary predicate | zero-denominator | no |
| N2 | Replaces reverse full-parse selection with reverse raw-prefix selection | valid-then-garbled | no |
| N3 | Changes `passed == total` to `passed <= total`, retaining positive total | failing-summary-exit0, failing-summary-exit2 | yes |
| N4 | Removes summary gate, retaining `killed == 2` | failing/no/garbled summaries and zero denominator | yes |

N3 is the declared **M2-family**, not literally the prior M2 mutation: round-72 `w1/R72MutBattery/R72MutBattery.md` records M2 changing arithmetic in `credit()`, whereas N3 changes `summary_green()`. The frozen declaration explicitly names the new literal substitution, so this lineage shorthand does not invalidate its denominator. N1 matches round-72 M3; N4 matches M4; N2 recreates the prior parser defect (including its broader raw-prefix behavior).

Each mutation also changes outputs on inputs outside the ten literal cases. Executed probes in `receipts.json` show: N1 greens `0/0` followed by noise; N2 rejects an otherwise green summary with one leading space; N3 greens `1/2`; N4 greens unrelated output when kills=2. The N2 whitespace result arises because pristine selection strips before matching whereas mutant selection tests raw `startswith`. This is a broader semantic delta than malformed-tail selection alone, but is genuinely the named prefix-match mutation. No kill is caused by that extra whitespace behavior: its sole frozen killing case has no indentation. Outside-set differences do not make inside-set disagreements artifacts. The claim remains four explicitly named syntactic mutants, not four exhaustive fault classes.

## Independent truth and carry-forward checks

Canonical rule is the committed harness, not an invented replacement: `last_parsed_summary` at `:320-330` scans backward for a full summary parse; `summary_green` at `:365-372` requires positive total and equal passes; `outcome_verdict` at `:393-394` additionally requires exactly two kills. `gate_rc` is not an argument to this outcome function and is intentionally irrelevant.

- **zero-denominator:** last parsed summary is `0/0`; equality holds but positive-total condition fails. Frozen `TARGET_MISSED` is correct. N1 alone removes that condition and returns `TARGET_MET`.
- **valid-then-garbled:** trailing cleanup marker is not a parsed summary; the last parsed one remains `12/12`; total is positive, passes equal total, kills=2. Frozen `TARGET_MET` is correct. N2 selects the malformed marker and returns `TARGET_MISSED`.
- Carried cases have correct labels: green `12/12` with two kills is met regardless of rc 0/2; failing `3/12` or `11/12`, absent/garbled summary, or one kill is missed. None supplies a mislabeled kill.

Independent raw-byte SHA-256 of `.ufo/waves/round-72/controls/c2-controls-r72.json` at both base `d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce` and instruments `1459cca11fb5d3956a6e9a128217852dd0c28cb9`:

`640fb44fdb1f31b4706b381c905fde4b5dae769bfd3e5b656bdb374bad58a793`.

The files are byte-for-byte equal. All eight parsed case objects appear unchanged in the new ten-case set (including output strings, rc, kills, and expected verdict). The new containing JSON file necessarily differs; the counter's carry check compares case field values, not raw JSON whitespace or additional metadata. That distinction does not conceal any observed changed case.

The harness is also byte-for-byte unchanged at those revisions, SHA-256 `b6108c86e8e03befce50256e2381ec08f199a1ab7fe192aeedef70459c45857d`. The corrected pinned run directly scores that actual harness and its literal mutants: held N1/N2 score 8/8 and survive; held N3 scores 6/8 and N4 scores 3/8 and are killed. Thus held kills are exactly **2/4**, not inferred merely from the prior receipt. Frozen new controls hash: `263b3c5a288c45a59587890a7e4c2e6dc3389630e5dd4a5cd1731976b5d2832b`.

## Residual risk and verification gaps

- LSP device unavailable: reading `xd://lsp` returned `No such tool`. Consequently no server status/references/definition/diagnostics could be obtained. Pinned source inspection and executed function/counter probes are fallback evidence, not claimed semantic-server proof.
- These runs use the single pinned Python counter and committed harness functions, not another agent/runtime, full landing-harness execution, or a broader correctness/saturation test. No routing or resume-continuity code is in the C1 scope; no claims about those paths follow.
- Selftest exercises synthetic rules and selected labels; passing 25/25 is not independent validation of arbitrary supplied controls. All actual ten labels were independently re-derived above.
- No production, corpus, ledger, source registry, or sibling file was changed; no git write command or tool installation was used. Evidence was saved in this seat directory, then its scratch tree was removed. The conflicting shorter requested report trailer would have written outside the exclusive seat directory, so this report honors the stricter directory boundary.

Self-evaluation: accuracy 4/5 (no semantic-server evidence); completeness 4/5 (bounded functions, not full harness execution, as declared); clarity 4/5 (long pinned provenance details retained); actionability 4/5 (F1 exact fix; F2 explicitly bounded future recommendation); conciseness 4/5 (required case and mutant evidence makes this longer than a verdict). Overall 4.0/5. Highest-impact improvement is preserving a runnable declaration command; evidence already identifies the missing argument. The user should agree that the numeric claim survives while reproducibility wording needed repair.

Report: .ufo/waves/round-73/w1/R73RevC1/R73RevC1.md
Frozen invocation fails without --controls; corrected invocation is TARGET_MET, rc 0.
All four named mutations killed; independently unchanged held eight kill exactly two.
Selftest 25/25; provenance and broader mutation-coverage limits remain explicit.
