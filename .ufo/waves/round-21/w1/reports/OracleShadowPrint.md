# OracleShadowPrint

Axes: **C1 operability residual repair**; **C2 calibration through independent artifact integrity**.

## Scoped result

Authored `.ufo/waves/round-21/w1/oracles/ShadowPrint.json` as an independent C1 recall/binding case. It includes the required `subprocess` import and the minimal Python transcript with `print` rebound to a lambda. Expected finding: `package_query`, command `pacman -Q r21`, evidence `observed`.

The expected class and command follow from the literal argv and `pacman -Q` query semantics. Assignment rebinds `print`; the immediate call passes the literal list to the lambda's `x`, which directly calls `subprocess.run(x)`. There is no unresolved callback or recursive path, so `lead` would understate the exact execution path. This case is data-only and was not executed.

## Evidence and limits

The rationale cites Python 3.14 assignment, lambda, and `subprocess.run` documentation. No scanner/tool was opened or run, and no measurements, builds, tests, or formatter checks were performed. No tools were installed or updated. C2 is named as context only; this case makes no C2 claim.
