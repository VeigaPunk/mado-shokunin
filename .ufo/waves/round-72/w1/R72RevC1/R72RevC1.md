# R72RevC1 — adversarial C1 review

Axes: C1 calibration (failure-detail attribution, false credit and false rejection); C2 operability noninterference (C1 scoring reads `mz`, not the whole harness verdict).

Recommendation: the frozen eight-case improvement is supported, but do not describe it as assertion provenance. Two grammar/wording discrepancies remain outside those eight cases. No production edits.

## Reproduction and evidence

All findings below reproduce with this exact command; the JSON `PROBE` name identifies the individual case:

```sh
mkdir -p /fast/scratch/hyaku/mado-r72/R72RevC1
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-72/w1/R72RevC1/review_probe.py --scratch-root /fast/scratch/hyaku/mado-r72/R72RevC1
```

Observed output is preserved in `probe-receipt.txt` beside this report; exit 0. The driver loads the exact instrument revision `9bcb4fd5b598844f168230dc05e441721d95b272` and base `976684a27e99c2508037a60eec415f550f53d70e` with read-only `git show`, not working-tree imports. `harness-delta.diff` records the actual r71/r72 comparison. No tool installation, git mutation, network access, host inspection, or production write was performed. Scratch was removed after receipt capture.

## Findings (severity order)

### F1 — P2 / defect: “last parsed summary” means last prefixed line in code

Location: `quality/counters/c1-r72-landing-controls.py:298-302,337-340`.

Repro: common command above, `PROBE valid-then-garbled`:

```text
SELFTEST FAIL 2: zero citations refused want=1 got=0
MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed
MADO_LANDING_COUNTERS_SELFTEST: runner cleanup complete
```

Frozen sentence: credit iff the **last parsed** `p/n assertions passed` summary is failing and the failure-line count equals `n-p`. This output has exactly one parsed summary, `1/2`, and one failure line.

Code: `last_summary()` selects the last line beginning with the marker without parsing it; `credit()` subsequently fullmatches only that selected line. Observed `credit=false`, despite the earlier valid summary and consistent detail. Thus the implemented rule is “last marker-prefixed line must parse,” not “last parsed summary.” This behavior is inherited from r71, not introduced by D1, but the newly frozen predicate still overstates it. It does not falsify the finite 8/8 receipt. The separate prose that a garbled summary earns no credit creates wording ambiguity; resolve the contract explicitly rather than claiming these two policies are equivalent. If final malformed markers are intentionally invalidating, that policy should replace “last parsed.”

### F2 — P3 / defect: failure-token prefix collisions satisfy the new arithmetic

Location: `quality/counters/c1-r72-landing-controls.py:311-312,344`.

Repro: common command, `PROBE prefix-not-fail-line`:

```text
SELFTEST FAILURE: wrapper logging only
MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed
```

Frozen sentence requires `SELFTEST FAIL` lines. The production assertion emitter (`quality/landing-counters.sh:18`) emits `SELFTEST FAIL <index>: ...`. Here no `FAIL` token or assertion detail exists; a different token, `FAILURE`, is present. Nevertheless observed `fails=1 credit=true`, because `startswith("SELFTEST FAIL")` accepts `FAILURE`, `FAILED`, and other prefix extensions.

This is a grammar boundary discrepancy, not a request for report authentication: reject non-token prefix collisions before counting failure details. If the intended frozen grammar deliberately means arbitrary lines beginning with those bytes, reclassify this as a declared syntactic limit and state that weaker grammar. It does not alter the frozen eight-mode score.

### F3 — informational / limit-already-declared: nested, unrelated, or wrapper detail earns credit

Location: `quality/counters/c1-r72-landing-controls.py:311-312,330-344,503-507`; declaration C1 declared limits.

Repro: common command, `PROBE nested-detail`, `wrapper-echo`, and `unrelated-detail`. Each prints `credit=true`. The nested example has a nested run's one failure line, a wrapper that asserts nothing, and a wrapper `1/2` summary; the unrelated example counts failure index 88 against a two-assertion summary.

Frozen sentence says the run's **own** failure detail. Code only counts matching lines over the entire concatenated child output, without block/run identity or association to the selected summary. This defeats a strong provenance reading of the heading. However, the declaration expressly disclaims authentication and recognizes matching detail replay as indistinguishable. These attacks fall within that admitted boundary; they are not grounds to reject the finite target. “Own” means captured child report, not proof its assertions produced the detail. No new provenance mechanism is recommended within this assignment.

### F4 — informational / false positive: alternative spelling and omitted detail are genuine failures but not qualifying kills

Location: `quality/counters/c1-r72-landing-controls.py:311-312,338-344`.

Repro: common command, `PROBE different-spelling` and `no-details`; both `credit=false`. A genuine assertion failure reported as `SELFTEST failed ...`, or only summarized, is excluded. That exclusion is expressly required by the frozen exact `SELFTEST FAIL` detail predicate, not a defect. The real landing instrument's emitter at `quality/landing-counters.sh:18,216` uses the supported spelling and prints newline-terminated detail/summary. `PROBE summary-before-detail` and an actual failing bash assertion (`REAL_SUMMARY_FIRST`) both receive credit, so summary-before-detail is not a counterexample.

### F5 — informational / limit-already-declared: multiple runs and stream boundaries are not normalized

Location: `quality/counters/c1-r72-landing-controls.py:298-312,504`; r71 knowledge entry limits 4.

Repro: common command, `PROBE two-genuine-run-blocks` returns false: the last `1/2` summary is checked against both runs' two detail lines. This follows the frozen whole-output arithmetic, not per-summary-block accounting.

`REAL_NO_NEWLINE_SPLIT` runs a real bash child exiting 1, with a valid summary lacking its final newline on stdout and genuine detail on stderr. It returns `credit=false`: concatenation glues the detail onto the summary, invalidating both parsing/counting. This is an inherited output-shape limit; the production emitter always supplies newlines. Both streams are captured, but that is not a promise of chronology or boundary repair. The r71 entry explicitly discloses stdout-then-stderr ordering. No claim of universal child-output support is justified.

## Base 6/8 and carried r71 expectations

The driver executes each guarded and guard-deleted **real bash fixture child**, then feeds its actual captured output and exit code through both committed harnesses' actual `measure()` bodies using their own `_measure_case` dispatch. Non-MZ children (git/extraction/M-R) are scripted, not real; no git mutation is executed. This is a direct execution of the base harness's M-Z decision path, not just a reimplementation of its predicate.

Observed `DERIVED_COUNTS {"base": 6, "candidate": 8}`. Base misses exactly `bare-failing` and `mismatch-detail`; all eight guarded children exit 0. The eight expected labels in the frozen JSON agree with the counter's hardcoded labels.

| Carried mode | Real mutant exit | Base / candidate mz | Reason, matching r71 entry |
|---|---:|---|---|
| liar-success | 0 | pass / pass | Failed assertion and failing summary; exit does not gate credit. |
| stderr-genuine | 1 | pass / pass | Failure detail on stdout plus summary on stderr both read. |
| liar-kill | 1 | fail / fail | Green summary, unrelated nonzero exit, no failed assertion. |
| crash-stderr | 2 | fail / fail | No summary; crash is not an assertion kill. |

Rationale source: `corpus/knowledge/kill-credit-exit-disagreement-r71.md:15-26,34-49`. The successor changes the M-Z call to `credit()` while preserving its exit-status independence (`:503-507`); the counting command reads `mz` from each harness contract regardless of the whole harness exit (`c1-r72-summary-credit.py:262-269,314-326`). C2 outcome changes therefore do not carry C1's score in this path.

## Residual risks and verification gaps

- No full counting-command rerun: its fixture builder performs `git init/add/commit` (`c1-r72-summary-credit.py:224-245`) and both full harnesses construct M-R git fixtures. The assignment prohibits git write commands anywhere. The permitted run above independently exercises the actual base and successor measure bodies with real M-Z child outputs, while explicitly not claiming real extraction/M-R execution. Frozen full-run receipt remains separately read-only evidence.
- LSP unavailable: reading `xd://lsp` returned `No such tool`; therefore no semantic references/definition/diagnostics results exist. Text searches, source inspection, actual generation comparison, and executed path probes are the fallback, not semantic proof.
- Frozen receipt establishes 8/8 versus 6/8 only; no saturation or fault-coverage claim follows. No runtime routing/resume code is affected by this scoped diff.
- Report is inside the seat-owned directory rather than the shorter conflicting trailer destination, honoring the hard write boundary.

Self-evaluation: accuracy 4/5 (F1/F2 depend on literal contract grammar, explicitly qualified); completeness 4/5 (full git-mutating counter cannot run under bounds); clarity 4/5 (separates defects, admitted limits, and false positives); actionability 4/5 (exact reproduction and locations, no production edits); conciseness 4/5 (multiple required attack classes retained). Overall 4.0/5. Highest-impact clarification: specify final-marker validity and the failure-token boundary without expanding the finite claim into authentication.
