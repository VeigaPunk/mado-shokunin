# C2 review: tool-generated oracle

## Verdict

**Recommendation: retain `failed` / `oracle_not_independent` for the assigned case.** No actionable defect was found in this scoped check. This is an advisory C2 assessment, not an admission or an authentication of the oracle's actual authorship.

## Exact inputs and observed results

- Tested production bytes: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py`, SHA-256 `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7` (same before and after the probes).
- Frozen case: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/oracle_tool_generated_not_independent.json`, SHA-256 `a02406394d9d1ff45f2206ce925c4d3ec4c0ffb46ee988ca9148e914c6e316c3`. The actual bytes match the entry in `assessment-fixtures/seal.json` (lines 45–46). `expected.json` lines 92–95 expect exit/code 1 and result `failed`.
- Actual-byte hashes of the expectation and population files: `expected.json` `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e`; `snapshots/population-baseline.txt` `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed`.
- Original fixture invocation: production `--check`, Python `-I -B`, `ulimit -v 393216` (384 MiB), `timeout --signal=KILL 15s`. Observed CLI exit `1`; JSON `code: 1`, `result: "failed"`, `finding_ids: ["oracle_not_independent"]`. The computed expectation and population digests matched the actual hashes above.
- One nearby altered artifact was written only under this seat's inert-fixture namespace: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/MadoR21-2.GateCase5OracleToolGenerate-2/tool_generated_independent_true.json`, SHA-256 `e60a7646c82fecdf1738158d1b441952b14f296c18356c1b4112e17274790896`. It changes only `oracle.independent` from `false` to `true`; `oracle.author` remains `tool-generated`, and the other assessment inputs are unchanged. Under the same bounds, observed exit `1`; JSON `code: 1`, `result: "failed"`, `finding_ids: ["oracle_not_independent"]`.

The original and altered observations therefore agree on the requested stable finding ID, exit code, and result. No full selftest, corpus, or C1 execution was run; no tools were installed.

## Behavior and C1 dependency

At `tools/mado-assessment.py:117–122`, the gate rejects when either `independent` is false **or** the case-folded author string contains `tool-generated`. The altered case tests that the author-string condition still rejects if the Boolean assertion is flipped. The failure ID is returned through the ordinary accumulated-failure path at lines 152–155, and `main()` returns that code at lines 206–226.

The exercised `--check` path is source-local: `main()` selects `evaluate()` and `check()` (`:206–226`, `:158–163`); `check()` validates the supplied bundle and reads the rooted population/`expected.json` artifacts (`:91–155`). Imports at `:8–15` are Python standard-library modules only. The only `subprocess.run` is in the separate `selftest()` path (`:166–203`, call at `:190–191`), which was not invoked; `--check` and `--selftest` are mutually exclusive (`:208–210`). The fixed historical assertion `history.c2_independent == false` at `:147–151` compares supplied round-20 data to a constant; it is not a lookup or consumption of a current C1 classifier/result. No C1 classifier/result dependency was observed in the exercised code path.

## Residual risk and verification gaps

The fixture's author, independence, timestamps, and named-verifier text are artifact assertions, not independently authenticated facts. The tool itself limits its authority to artifact assertions and disclaims authenticated chronology, authorship, or semantic proof (`:142–155`). Thus the observed result establishes how this artifact is classified, not whether a real oracle was authored by a tool or whether its declared independence is true.

No `lsp` device was mounted: `read xd://lsp` returned “No such tool.” Consequently LSP status, references, definition, and diagnostics were unavailable. Literal text search was used only for navigation, not as semantic proof; the C1 conclusion above rests on the inspected check-path definition and the bounded `--check` runs. No full suite/corpus or broader adversarial author-string variants were checked.
