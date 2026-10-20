# RevPrecisionCounterSpec — Counter needs enforced suite identity and breadth

Axes reviewed: suite nonvacuity, canonical pin identity, and baseline discrimination.

## Findings

### High — A nonempty but undersized or duplicated suite can score 10/10

The pre-registration requires all five families and at least four cases per family (SCORECARD.md:1250–1253); case authors are instructed to provide at least six cases per family, with at least four red against the old tool (round-20/gen_w1.py:42). The counter does not enforce those requirements. It rejects an empty case list and validates that each family label is one of the five values, but it only checks name uniqueness (tw-precision.py:117–149). It does not require a minimum total, any minimum for an individual family, or distinct `file` paths/content. Aggregation initializes missing families to zero but still returns success and calculates `10 * passed / N` over whatever cases were supplied (tw-precision.py:200–227).

[INFERENCE] A one-case `L` suite whose expected result is a lead can yield `score: 10.0` for a tool that emits that expected lead; the `P`, `S`, `W`, and `H` families would not be present to catch an always-lead implementation. Repeating the same case file under unique case names can also inflate N without adding stimuli. The counter output would show the omitted families or repeated cases, but exit 0 / score 10.0 does not reject them. Thus the registered family breadth is an external review obligation, not a property of a passing counter result.

The exact empty-suite attack is already blocked by the nonempty checks at tw-precision.py:117–120 and :199–201. That does not prevent the undersized or duplicated-suite cases above. Require all registered families and their predeclared minimum case counts, and reject duplicate fixture paths/content before allowing a successful score.

### Medium — `--suite-rev` can bypass the canonical landing pin

The registered claim says to read the suite at the commit that first lands it, with that commit containing no tool change (SCORECARD.md:1240–1244). The executor task permits `--suite-rev PIN`; the implementation lets that argument replace `SUITE_PIN` even after the constant is populated (tw-precision.py:56–68). `resolve_commit` accepts any revision expression that Git resolves to a commit, not only the registered full object ID (tw-precision.py:42–53). The output reports the resolved `suite_pin` (tw-precision.py:218–226), but there is no check that it equals the canonical landing commit.

[INFERENCE] A caller can ask for a suite revision other than the registered landing commit—including a later revision—and obtain a normally scored result. The reported pin makes the substitution auditable, but a bare N/N or 10.0 is not intrinsically proof that the canonical suite was used. Reject overrides different from the configured full immutable pin, or make override runs explicitly non-admissible/test-only. In the admitted run, require the output `suite_pin` to equal the first suite-landing commit.

### Medium — Baseline red/clean requirements are not part of the counter verdict

Case authors must record and compute `before` outcomes for both old revisions, and each family must have at least four cases red at the round-19 tool (gen_w1.py:42). The registered claim also requires every P case to pass at the pre-harm baseline and names measurements at both old tool revisions (SCORECARD.md:1254–1257). However, the counter's expected-suite schema and loaded case records contain only the target `want_exit`/`want_findings`; the counter accepts one `REV` per invocation and compares only that revision to those expectations (tw-precision.py:117–152, 155–190). It neither reads the case-author `before` statuses nor asserts baseline fail/pass minima.

As a result, case-author `before` labels are not re-derived by this counter, and a final-tool N/N result does not establish that the suite detects the prior behavior or that P cases pass at 9c54c56. Have the counter (or a required aggregate checker) scan the pinned suite at both fixed old revisions, emit per-case baseline results, and fail admission unless the registered per-family red threshold and P clean-baseline guard hold. The suite should remain pinned to its first landing commit for all three scans.

## Residual risk

The precision suite directory was not present in the inspected round-20 tree, so I could not assess its eventual case count, unique fixture content, or whether individual expectations faithfully encode E1–E4. A digest establishes which case bytes were used; it does not establish that the authored expectation is semantically correct or independent of the implementation. The pre-registration's commit-before-tool-edit ordering helps constrain post-hoc edits, but still needs review of the suite contents and the stated baseline results.

## Limits

Static review only: SCORECARD.md, the stored PrecisionCounter task, round-20/gen_w1.py, and the current tw-precision.py. I did not run the counter, scan fixtures, or verify a merged precision suite. No LSP device is mounted (`read xd://lsp` returned “No such tool”), so no references/definition/diagnostics requests were available; no semantic conclusion is based on grep output. I did not inspect the tripwire implementation or the corpus-diff evidence.

## Installs

None.
