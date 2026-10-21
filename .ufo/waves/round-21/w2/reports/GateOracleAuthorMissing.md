# C2 assessment: `oracle_author_missing`

**Verdict: expected rejection is robust to the tested nearby malformed variant.** The frozen case correctly returns `could-not-evaluate` (code/exit 2) because `oracle.author` is required and absent. The `author: null` variant also rejects as invalid input with the same stable finding ID, result, and code. This establishes structural completeness checks, not authentic authorship.

## Evidence

- Current lane revision: `f499a8db7171b7476fe9f204ab9edbac5a956fa9`.
- Exact tested production bytes: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py`, SHA-256 `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7`.
- Frozen case: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/oracle_author_missing.json`, SHA-256 `6ad03bb2b70e3479c0353c0dd6c12fa30fb63549c47e1b696a66b76352684c73`, matching its entry in `seal.json`.
- Frozen expected row in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/expected.json:157-162` specifies code `2`, result `could-not-evaluate`, and the reason that the oracle author field is absent. Its actual-byte SHA-256 is `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e`, matching `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/seal.json` and the tool's `SEAL_SHA`.
- Bounded probe: one child process, RLIMIT_AS 384 MiB, 15-second timeout; invoked the production `main()` against the original fixture and a single private-temp altered copy (`oracle.author = null`). The temp root contained byte-copied `expected.json` and `snapshots/population-baseline.txt`; computed hashes were respectively `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e` and `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed`. The latter matches the frozen case's `sha256` and the seal's baseline entry, confirming the path was hashed from actual bytes.
- Observed for **both** original and null variant: returned CLI code `2`; JSON `code: 2`, `result: "could-not-evaluate"`, `finding_ids: ["assessment_input_invalid"]`, error `"missing or invalid author"`. The original observed tuple agrees with the frozen expected code/result; `selftest()` derives `assessment_input_invalid` for this uncatalogued expected failure and checks the returned code, result, and finding ID (`mado-assessment.py:193-197`).

## C1 independence and evidence limits

The selected path is source-local: `main()` calls `evaluate()` then `check()` (`mado-assessment.py:206-226`, `158-163`); `check()` reads the bundle and rooted population/`expected.json` artifacts (`91-155`). The module imports only Python standard-library modules (`8-15`). Its self-test subprocess invokes this same script's `--check` path for fixture rows (`166-202`); the inspected production path does not import or call the C1 classifier or consume C1 classifier/results. The seal explicitly labels the fixture scope C2-only (`seal.json:2-6`). This was a source audit; no C1 code or full self-test was run.

No `lsp` device is mounted (`read xd://lsp` returned “No such tool”), so definition/call tracing used direct selected source reads; text search was only navigational, not semantic-reference evidence.

The source and fixture contract treat timestamp strings as synthetic ordering assertions, and named non-author-verifier strings as structural assertions. The timestamp parser checks formatting/timezone and ordering; the verifier regex checks only a name-like token. Neither independently authenticates time, identity, authorship, verifier independence, or semantic truth. A nonempty author string likewise satisfies a structural check and is not authenticated. No outside-lane authentication was established.

No production or frozen file was edited; no tool was installed. Full self-test/corpus checks were not run.
