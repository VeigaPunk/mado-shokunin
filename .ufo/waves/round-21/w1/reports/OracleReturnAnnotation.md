# OracleReturnAnnotation — scoped advisory

## Axis and finding

- **Axis:** C1 precision (operability residual repair).
- **Severity:** No actionable finding; the requested negative expectation is semantically sound.

The proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/ReturnAnnotation.json` contains one inert Python eval transcript and expects no findings. It imports `subprocess` and defines `f` with a visible `subprocess.run` call in its deferred body. Defining `g` evaluates the return annotation expression `f` to the function object, but does not invoke `f`; neither `f` nor `g` is called. Thus no process-spawning path is reached. No class `C` is needed for this exact shape.

The round-20 precision review lists a return annotation naming `f` as a false lead at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/review/CriticPrecisionV3.md:11` (case 16). That source supports the counterexample shape, not its expected result; the empty expectation follows from Python semantics.

## Residual risk and verification gaps

Static reasoning only, as required. Neither transcript nor tripwire was executed; no classifier/gate measurement, build, test, or installation was performed.
