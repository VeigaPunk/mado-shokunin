# OracleResetBoundary

Axis: C1 binding / operability.

The proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/ResetBoundary.json` contains two inert Python eval cells. The first imports `subprocess` and defines `invoke(argv)` with a visible `subprocess.run(argv)` body, but does not invoke it. The second cell has `reset: true` and calls `invoke` with the opaque literal argv `['pacman', '-Q', 'r21']`.

Expected findings are empty. The reset precedes the second cell, so its interpreter namespace lacks the earlier `invoke` binding. Resolving the call raises `NameError`; the earlier helper body is not reached, and the literal argv alone is data rather than evidence of process execution. Python's execution-model source states that a name not found raises `NameError` at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceNamespace/cpython-v3.14.8-executionmodel.rst:113-124`. This semantic expectation was derived independently of detector behavior.

Verification: static reasoning only. The transcript was not executed; no tool/scanner was opened or run, and no build, test, measurement, or installation was performed.
