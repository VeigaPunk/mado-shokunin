# OracleUnusedAdd — scoped report

Axes: C1 operability (precision residual repair); C2 calibration (independent artifact integrity). This seat supplies one C1 precision oracle only and makes no C2 claim.

Wrote `.ufo/waves/round-21/w1/oracles/UnusedAdd.json` with one inert Python eval cell and `want: []`. It defines `f` with a visible `subprocess.run` query and defines only `C.__add__`; the sole terminal expression is `C()`. No explicit constructor is defined, so construction does not call `f`. No addition or explicit `__add__` call occurs, leaving the subprocess call unreachable. This negative expectation is consistent with the Python operator protocol and matches the prior round-20 review's cited false lead for constructing `C` without using `__add__` (`.ufo/waves/round-20/a2/review/CriticPrecisionV3.md:10-13`).

Assessment was static only. The fixture and tripwire were not executed; no build, test, lint, formatter, or tool installation was run.
