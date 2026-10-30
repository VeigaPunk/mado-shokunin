# R56W3ExecFixDivA

- **Attack:** Four documented parser limitations/approximation constructs in `tools/mado-watchplan.py` at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`: variable-only `source = $VAR`, brace expression option value, device category block, and an absolute source outside home.
- **Action:** Added runnable C2-format fixtures under `.ufo/waves/round-56/fixtures/c2-divergences/{variable-source,expression-value,device-block,external-absolute-source}/`, including args, tree, byte-exact expected stdout and expected rc. Exported the pinned tool to scratch and ran it on each fixture.
- **Exact retained evidence:** `.ufo/waves/round-56/w3/R56W3ExecFixDivA/receipts/divergences-a.txt`; for all four runs it records rc=0, expected_rc=0, `cmp=0` byte-equality proof and decisive output. Tool source used: pinned revision `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`.
- **Defects:** None observed against the documented behavior (severity: none). The variable-source result is an `ERROR nomatch` rather than recognizing variable expansion, as specified by the model's treatment of `$` LHS and ordinary source path expansion. Device block options are ignored by this subset.
- **Could not verify:** None for the four selected fixtures. No tests, builds, linters or formatters were run.
- **Tooling:** No installs or updates.
