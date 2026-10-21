# Gate review: `shonen_x_with_named_nonauthor`

**Axes:** verdict correctness; adjacent malformed-input robustness; independence from C1; limits of artifact authority.

## Verdict

**No actionable finding.** The positive control's expected verdict is robust to the tested adjacent malformed-name variant. This is a structural artifact-gate result only, not evidence that the claimed verifier or assessment is real.

## Evidence and exact tested bytes

- Frozen expectation: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/expected.json`, case `shonen_x_with_named_nonauthor`: `code: 0`, `result: clean`. Its reason explicitly labels the verifier and assessment synthetic.
- Frozen fixture SHA-256: `fe6f4971067167a6e2368e4182936220e66c8a670751c37cb663956f3af6b0ae` (`cases/shonen_x_with_named_nonauthor.json`). The copied positive-control bytes in the isolated test root had the same digest.
- Tested production file: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py`, SHA-256 `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7` at both pre-run and post-run reads. Initial HEAD was the handoff candidate `f499a8db7171b7476fe9f204ab9edbac5a956fa9`; final hash capture observed HEAD `a8da015624c92f4cb4a7de92adbf6643a3f8b38a`. `git diff 2ac0f9ba69051aea22cab3b6cfebe4d906b72d17 HEAD -- tools/mado-assessment.py` was empty, and the tested file bytes retained the same SHA-256 across the HEAD advance.
- Isolated workspace: `/tmp/mado-r21-shonen.cxLQvP/`; copied `expected.json` SHA-256 `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e` and baseline population input SHA-256 `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed` matched their frozen bytes.
- Probe used `/usr/bin/python -I` on the production CLI, `ulimit -v 393216` (384 MiB) and `timeout 15s`; no C1 code and no selftest/corpus was run.

## Observed outcomes

1. Frozen positive control, tested from the isolated copy: exit `0`; JSON `code: 0`, `result: "clean"`, `finding_ids: ["assessment_clean"]`. The output's actual expectations and population digests matched the frozen bytes and the frozen expected code/result.
2. One altered inert artifact, SHA-256 `3757b8d87e88d85e2f98669a78596d1d0a36398909090d680d87c561581b164f`, at `/tmp/mado-r21-shonen.cxLQvP/cases/shonen_x_empty_verifier_name.json`: changed only box 1's evidence from the claimed verifier name to the empty value `named non-author verifier: `. Exit `1`; JSON `code: 1`, `result: "failed"`, `finding_ids: ["unnamed_nonauthor_verifier"]`. This is the expected rejection of an `x` whose evidence contains no verifier name. Exit code, result, and stable finding ID agree with the check's contract.

## C1 dependency check

No LSP device/server was available: `read xd://lsp` returned “No such tool” and command lookup found neither `lsp` nor `pyright-langserver`. Thus LSP `status`, references, definition, and diagnostics could not be obtained; literal source inspection/search is only the fallback, not semantic-LSP proof.

The complete 230-line source was inspected. In the `--check` route, `main` calls `evaluate`, which calls `check`; `check` loads the supplied bundle, expected digest and rooted population bytes, and uses only local validation/hash helpers. There is no C1 classifier/result import, invocation, or result-file read in that route. The only `subprocess.run` call is in `selftest` to replay fixture cases; it is not reached by either `--check` invocation. The isolated CLI run also required no C1 process or output. No C1 code was executed.

## Residual risk and verification gaps

The gate checks assertions, not truth: syntactically valid timestamp strings and the name `FixtureVerifier-Q7` do not authenticate chronology, authorship, non-author status, semantic proof, or promotion authority. This matches the source's explicit artifact-only authority declaration and the fixture's stated synthetic-data limitation; the `clean` result must not be read as a real verification claim. LSP-backed caller/definition/diagnostic evidence was unavailable as noted above. No install or update was performed.
