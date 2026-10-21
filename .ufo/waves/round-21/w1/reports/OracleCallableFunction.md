# OracleCallableFunction

## Axis and finding

- **Axis:** C1 precision (operability residual repair).
- **Severity:** No actionable finding; the requested empty expectation is semantically sound.
- **C2 calibration (independent artifact integrity):** out of scope for this C1 precision oracle.

The proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/CallableFunction.json` contains one minimal Python eval transcript. `f` visibly contains `subprocess.run`, but only its definition is evaluated; the body is deferred. The builtin `callable(f)` tests whether the function object appears callable and does not invoke it, so this transcript has no path reaching the subprocess call. `import subprocess` is the required preamble. No class `C` is needed for the exact `callable(f)` shape, so the fixture defines no unrelated methods or constructor.

This is consistent with the independent round-20 precision review: it identifies `callable(f)` as one of the false leads and says the expected result is no row because the function bodies are not called (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/review/CriticPrecisionV3.md:10-13`). The Python 3.14 builtins documentation describes `callable` as returning whether the object appears callable, rather than calling it (`https://docs.python.org/3.14/library/functions.html#callable`). These sources support the fixture shape and semantics; they do not supply a tripwire measurement.

## Residual risk and verification gaps

Static reasoning only, as assigned. The transcript was not executed; no classifier or gate was invoked and no build, test, or measurement was performed. No tools were installed or updated.
