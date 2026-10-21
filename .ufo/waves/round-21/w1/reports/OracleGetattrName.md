# OracleGetattrName — scoped advisory report

## Finding

**C1 precision — no semantic finding expected for this case.** The proposed transcript is exactly the requested shape:

```python
import subprocess
f = subprocess.run
getattr(f, "__name__")
```

`f` refers to the process-spawning function, but nothing calls it. The final expression reads its `__name__` metadata through `getattr`; it does not invoke the function. Therefore `want: []` is semantically correct. The `subprocess.run` documentation describes process creation as the effect of calling `run`; Python's `getattr` and function metadata documentation support the value-only lookup reasoning. No class `C` is relevant, so no constructor or unused method is introduced.

The round-20 precision review records this same shape as a false lead (case 14, `CriticPrecisionV3.md:10-13`); that report establishes shape provenance only, not the expected result. The expectation above is independently derived from Python semantics.

## Residual risk and verification gaps

This is a proposal for the registered C1 precision oracle, not evidence that any tripwire revision handles it correctly. Per the wave contract, the transcript and tripwire were not executed; no implementation behavior or measurement is claimed. Public semantic references and the prior-review shape provenance are recorded in `GetattrName.json`.

Report: .ufo/waves/round-21/w1/reports/OracleGetattrName.md
