# OraclePartialMethod

Axis: C1 operability — partialmethod call/binding recall.

The proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/PartialMethod.json` contains the minimal Python transcript with both imports and the requested `worker(self)`, `functools.partialmethod(worker)`, and `C().run()` shape. Its expected finding is `package_query`, command `pacman -Q r21`, evidence `observed`.

Static reasoning: `worker` is a function descriptor. Accessing the `partialmethod` through `C().run` binds that instance as `self`; calling the resulting partial invokes `worker`, whose body reaches `subprocess.run` with the exact literal argument vector. The execution path is direct and fully determined, not an unresolved callback or recursive body, so `observed` is the appropriate evidence level. The earlier round-20 report is cited only as provenance for the regression shape; it does not determine this proposal's expected result.

Verification: static reasoning only. The transcript was not executed; no scanner/tool was opened or run, and no build, test, installation, or measurement was performed.
