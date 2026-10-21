# OracleReprFunction — scoped advisory finding

## Axis and finding

- **Axis:** C1 precision (operability residual repair).
- **Severity:** No actionable finding; the requested negative expectation is semantically sound.

The proposal at `.ufo/waves/round-21/w1/oracles/ReprFunction.json` contains one inert Python eval transcript and expects no findings. It imports `subprocess` and defines a visible function whose deferred body calls `subprocess.run`, then evaluates `repr(f)`. Defining `f` does not execute its body. The unshadowed builtin `repr` formats the ordinary function object without invoking `f` or handing it to a callback, so the spawn call is not reached. The round-20 independent precision review explicitly lists `repr(f)` among the value-only cases expected to have no row (`.ufo/waves/round-20/a2/review/CriticPrecisionV3.md:5-13,18`).

No class `C` is needed for this exact shape; omitting it also avoids constructor or unrelated method behavior. The fixture's required preamble is `import subprocess`.

## Residual risk and verification gaps

This is static semantic reasoning only, as required. The transcript and tripwire were not executed; no measurement or scanner result is claimed. This expected result applies to the ordinary function object in this fixture, not arbitrary values with custom representation behavior.

No tools were installed or updated.
