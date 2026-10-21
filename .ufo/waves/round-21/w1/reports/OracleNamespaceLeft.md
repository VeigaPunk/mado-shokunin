# OracleNamespaceLeft

Axis: C1 operability — recall/binding.

The proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/NamespaceLeft.json` is a single-cell Python transcript containing the requested `cmd` binding, `globals() == {}` expression, and direct `subprocess.run(cmd)` call. At module scope, the assignment binds `cmd` in the module namespace. `globals()` returns that namespace, and equality against `{}` reads it without changing the binding; the expression value is discarded. Therefore the final call receives exactly `["pacman", "-S", "r21"]`.

Expected finding: `host_mutation`, command `pacman -S r21`, evidence `observed`. The command's exact argv and direct process-spawning path are statically resolved, without a callback or recursive path left opaque, so `lead` would understate the evidence. `pacman -S` is package synchronization/install mode. These expectations follow Python name-binding, `globals()`, and `subprocess.run` semantics plus the pacman manual, not any detector or tool outcome.

The transcript remains inert data: it was not executed. No scanner, classifier, package manager, build, test, or tool installation was used. No production file was opened or changed.
