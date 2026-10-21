# OracleCalledClosure

Axis: C1 operability — callable returned closure and argument binding.

The proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/CalledClosure.json` is one Python transcript. `outer(argv)` receives the literal argv list and returns `inner`; `inner` closes over that parameter. The final `outer(["pacman", "-Q", "w2shape"])()` both constructs the closure and invokes it, so the path reaches `subprocess.run(argv)` with the exact command `pacman -Q w2shape`. The semantic expectation is one `package_query` finding with `evidence: observed`: no unresolved callback or recursion lies between the visible call and the process call.

The command and classification are derived from Python call/closure semantics and the literal argv, independently of detector behavior. The prior round-20 returned-closure fixture at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w2/AdvRecallShapes/fixtures/ar25-returned-closure-bound.jsonl:1` supports the provenance of this shape; the proposed case specifically tests binding a literal at the outer call. The code is inert stored transcript data; it was not executed, and no scanner/tool was opened or run.

Verification: static reasoning only, as assigned. No build, test, measurement, or tool installation was performed.
