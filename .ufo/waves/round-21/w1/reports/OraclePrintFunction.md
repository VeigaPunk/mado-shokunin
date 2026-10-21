# OraclePrintFunction — scoped advisory finding

## Axis and finding

- **Axis:** C1 precision (operability residual repair).
- **Severity:** No actionable finding; the requested negative expectation is semantically sound.

The proposal at `.ufo/waves/round-21/w1/oracles/PrintFunction.json` contains one inert eval transcript and expects no findings. Importing `subprocess` and defining `f` does not execute the function body. `print(f)` passes the ordinary function object to builtin `print`, which formats it without invoking `f` or handing it to a callback. Thus the visible `subprocess.run` call in `f` is not reached. This matches the independent round-20 precision review's discussion of `print(f)` as a value-only use (`CriticPrecisionV3.md:5-13`) and its pure-builtin analysis (`ReviewV3Diff.md:46-57`).

The requested `C` is unnecessary for this exact `print(f)` case; omitting it avoids unrelated methods and any constructor behavior. No class constructor is defined.

## Residual risk and verification gaps

This judgment is static only, as required. The transcript and tripwire were not executed; no measurement or scanner outcome is claimed. The rationale concerns this exact ordinary function-value print, not arbitrary objects with custom formatting behavior.

No tools were installed or updated.
