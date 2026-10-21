# OraclePrintLambda — scoped advisory finding

## Axis and finding

- **Axis:** C1 precision (operability residual repair).
- **Severity:** No actionable finding; the requested negative expectation is semantically sound.

The proposal at `.ufo/waves/round-21/w1/oracles/PrintLambda.json` contains one minimal inert Python transcript and expects no findings. The lambda expression creates a function object without evaluating `subprocess.run`; builtin `print` formats that object and does not invoke the lambda or pass it to a callback. Thus the spawn is not reached. This is a static language-semantics judgment, consistent with the round-20 precision review's explicit `print(lambda)` false-lead example (`CriticPrecisionV3.md:5-13`) and the review's pure-builtin explanation and expected clean result (`ReviewV3Diff.md:46-57`).

The import of `subprocess` is the only preamble needed. The exact inline-lambda shape requires no named `f` and no class `C`; adding either would make the fixture less minimal. No constructor or unrelated method is introduced.

## Residual risk and verification gaps

This is static reasoning only. The transcript was not executed and the tripwire was not run; no scanner outcome or measurement is claimed. C2 artifact-integrity behavior is outside this fixture's scope. No tools were installed or updated.
