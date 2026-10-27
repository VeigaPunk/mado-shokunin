# Initial M01–M06 attempts — INCONCLUSIVE, not scored

Each initial receipt contained exactly:
`run_one.sh: line 35: he: command not found`
The counter was never invoked; do not count any as killed/survived. The driver was edited while these shells were executing, producing a transient command line. Afterward the stable driver passed `bash -n` and a direct `env -i ... python3 -c 'print("env-ok")'` probe (`env-ok`, `syntax-ok`). All six scratch clones had committed the mutant and then restored `tools/mado-keysym.py`; each parent blob and restored worktree hash equaled pristine `dcc13cce3b7134946208116cd98599fb8f56a2b81fc6f26b9598ac5429b40265`.

Actual wrapper outputs:
- M01: `rc=127 mutant_sha=c23a246afa7f358f0ce93fbffdaf9438b38371d1f622c9ee21b698ffde9ac1a8`, rev `81e565409f0d6f22619107a755aa9b72743c01c6`, restored-equal.
- M02: `rc=127 mutant_sha=bf30a5e03c3d3fcf4f0ee477f1de7954dd6d2bf42f67207ae7c85d7bd33d7dd0`, rev `16249179260c53b1b74dc6f7ccf81049613285c3`, restored-equal.
- M03: `rc=127 mutant_sha=95e4f5e14ccc6ac1b9a2048431b8629acce6401d921d44a827bef7498c109c4f`, rev `e2f9c367e3c46d7fd5d1e9ffb41c0740a454841a`, restored-equal.
- M04: `rc=127 mutant_sha=570d7ac6916cd428e8b5222a8bb88a49ea0f0bfdb1bcce93404797c768ccf8bb`, rev `243e00c91112fcb346ceb290ae1468f46ac4fa41`, restored-equal.
- M05: `rc=127 mutant_sha=7f8ff4781bcddb4cbe7f3beacf921b83f6430dace2e6fc76a26c77b51b39ce35`, rev `d8db7cbdd824e1c073dbf5a6c3fb9b84b67e37bd`, restored-equal.
- M06: `rc=127 mutant_sha=0fd3912d2af023a9e73df1501cee2ed820ace32fd771ba5fa1efb0518efc1531`, rev `c4fafa8599bb1a30a66f1c47dc50d42e9ceed2c4`, restored-equal.

A clean re-run of M01–M06 with the stable driver is required; only its detector outputs count for verdicts.
