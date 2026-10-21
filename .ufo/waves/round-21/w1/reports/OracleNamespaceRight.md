# OracleNamespaceRight

Axis: C1 operability — recall/binding.

The proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/NamespaceRight.json` contains one minimal Python transcript with `import subprocess` and a module-level `cmd` binding. The discarded `{} == globals()` comparison reads the module namespace; it does not rebind or erase `cmd`. The subsequent direct `subprocess.run(cmd)` receives `['pacman', '-S', 'r21']`, so the expected finding is `host_mutation`, command `pacman -S r21`, evidence `observed`. The call is explicit and its argument is bound in the same module block, so a `lead` expectation would understate the visible execution path.

The expectation is from static Python semantics, not from a detector result. The source receipts establish module/block binding and name resolution (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceNamespace/cpython-v3.14.8-executionmodel.rst:84-96,127-143`), `globals()` returning the module namespace (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/fetch/SrcPyBuiltins/cpython-3.14.8-Doc-builtins-functions.rst:895-899`), and `subprocess.run(args)` accepting an argument sequence (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/fetch/SrcPyShlex/subprocess.rst:38-44`). The prior review's reversed-comparison control is cited only as shape provenance (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/a2/review/ReviewV3Diff.md:43-44`); it is not the authority for the expected result.

The transcript is data only and was not run; executing it would attempt a package-install transaction. No scanner, classifier, build, test, or tool installation was used.
