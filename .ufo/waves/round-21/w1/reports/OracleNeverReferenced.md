# OracleNeverReferenced

Axis: C1 precision.

The proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/NeverReferenced.json` is one inert Python eval transcript with expected `want: []`. Its preamble imports `subprocess`; it defines `f` with a visible `subprocess.run` body, then contains no reference to or call of `f`. Python binds the function at its `def` statement but defers its body until invocation, so the subprocess call is not reached. The expected empty result is derived from Python execution semantics and the Python 3.14 language documentation, not from a tripwire outcome.

No class `C` is part of this standalone unreferenced-function shape, so no class methods or constructor are included. Transcript code was not executed and the tripwire was not run. No build, test, measurement, or installation was performed.
