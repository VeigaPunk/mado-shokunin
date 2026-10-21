# C2 assessment: `shonen_duplicate_box`

**Verdict: the frozen ambiguous assessment is rejected, and a nearby four-row duplicate variant is also rejected.** The frozen artifact returns code/exit `2`, `could-not-evaluate`, and `assessment_input_invalid`, as required by the oracle's code/result row and the selftest's fallback finding-ID mapping. The nearby variant reaches the explicit duplicate-identity check and returns the same tuple. This is artifact validation only, not verification of the assertions inside the artifact.

Axes: **coverage** (frozen five-row case plus four-row duplicate variant), **classification calibration** (reject ambiguous structures without treating malformed input as a failed semantic assessment), and **isolation** (C2-only source path, no C1 execution).

## Evidence and bounded execution

- Tested production source: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py`; SHA-256 before and after the checks: `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7`.
- Frozen case: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/shonen_duplicate_box.json`; actual SHA-256 `f592163ec6dc5719846539a3199e01c1ca8a86a29ced94d262bfe743ff5e1b3a`, matching the `seal.json` entry. Its oracle row at `expected.json:109-114` expects code `2`, result `could-not-evaluate`, for the duplicate-box ambiguity.
- Frozen inputs read from actual bytes: `expected.json` SHA-256 `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e`; `snapshots/population-baseline.txt` SHA-256 `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed`. Both matched the exact-byte copies in the private probe root.
- Probe: two direct `--check` invocations, each isolated with `-I -B`, `RLIMIT_AS=384 MiB`, and a 15-second timeout. No selftest, suite, corpus, C1 code, or fixture payload was run.

| Artifact | Exact bytes / shape | CLI exit | JSON code | Result | Finding IDs | Observed reason |
| --- | --- | ---: | ---: | --- | --- | --- |
| Frozen case | SHA-256 `f592163ec6dc5719846539a3199e01c1ca8a86a29ced94d262bfe743ff5e1b3a`; rows `[1,2,3,4,1]` | 2 | 2 | `could-not-evaluate` | `["assessment_input_invalid"]` | `canonical four-box assessment incomplete` |
| Nearby inert variant | `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/GateShonenDuplicateBox-2/cases/duplicate_four_rows.json`, SHA-256 `a29c0904e2569c8bb4e97a112cf3128e4f6b6055b7d886cb8d92f9467b8ded10`; rows `[1,2,3,1]` | 2 | 2 | `could-not-evaluate` | `["assessment_input_invalid"]` | `duplicate or invalid assessment box` |

The variant is the frozen artifact with its box-4 row removed, so the remaining four records still duplicate box 1. It exercises the duplicate check rather than only the earlier row-count guard. The frozen tuple matches the oracle's expected code/result, and the selftest maps that uncatalogued code-2 case to `assessment_input_invalid`. The nearby variant is not a frozen oracle row; its direct output is the same generic invalid-input tuple, consistent with that mapping (`mado-assessment.py:193-197`).

## C1 dependency and authority boundaries

The exercised source path is `main()` → `evaluate()` → `check()` (`mado-assessment.py:206-226,158-163,91-155`). Its imports at lines 8-15 are Python standard-library modules. `check()` reads the supplied JSON, declared population file(s), and root `expected.json`; it does not import/call the C1 classifier or look up/consume C1 results. The only `subprocess.run` is in the separate `selftest()` implementation at lines 190-191; that mode was not run. No C1 source was executed.

No `lsp` device is mounted (`read xd://lsp` reported no such tool). I used selected source reads for the call path; text search was navigational only, not semantic-reference proof.

The case's timestamp strings and oracle fields are artifact assertions. The parser can check timestamp syntax/order and the oracle's declared values, but this does not authenticate chronology, authorship, or independence. No named-verifier assertion is present in this case; a verifier string in other artifacts would likewise be only an assertion. The gate output itself labels its authority as artifact assertions, not authenticated evidence or promotion authority.

No production or frozen file was edited; only the advisory report and uniquely named inert probe fixture were written. No tools were installed. Full selftest/corpus checks were not run.

Report: .ufo/waves/round-21/w2/reports/GateShonenDuplicateBox.md
