# C2 `expectation_digest_changed` assessment

**Verdict: PASS — the frozen case's expected rejection is correct, and the one-field clean control does not false-positive.** The reviewed behavior is bound to the actual production source bytes below. No production or frozen file was changed.

## Observed bytes and gate result

- Production: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py`, SHA-256 `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7`.
- Frozen case: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/expectation_digest_changed.json`, SHA-256 `458242922de73614141d43d581f0bb728dadfb60ac6cdd1dc4428610affe2a3c`, matching `seal.json:49-50`.
- Actual bytes: `expected.json` hashes to `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e`; `expectations-changed.json` hashes to `c084335adf5c2191e2561c5207faaaf565e3cfe69f0e9e04ee6a94e6adf1a266`; `snapshots/population-baseline.txt` hashes to the case's declared `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed`.
- The fixture declares `expectations_sha256=c084…` and `registered_expectations_sha256=aa69…`. Its frozen expected row (`assessment-fixtures/expected.json:97-101`) specifies code `1`, result `failed`, for this mismatch.
- Ran only the production `--check` path on that case, with a 15-second timeout and `RLIMIT_AS=402653184` bytes (384 MiB). Observed CLI exit `1` and JSON `{code: 1, result: "failed", finding_ids: ["expectations_changed"]}`. The output's `actual_expectations_sha256` is `aa691e…`, computed from the actual `expected.json` bytes.

## Nearby false-positive control

Created one inert per-seat fixture at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/MadoR21-2.GateExpectationDigestChanged-2/expectation_digest_registered.json` (SHA-256 `72db0d2afd4f74ee176f7fb5c532f494bee59039e9f87641e1c8048656ddff7d`). It is otherwise the frozen case, with only `oracle.expectations_sha256` changed from the altered-source digest to the registered digest. With the frozen root unchanged, the same bounded `--check` returned CLI exit `0`, JSON `{code: 0, result: "clean", finding_ids: ["assessment_clean"]}`, and actual expectation digest `aa691e…`. Thus the finding is not emitted when the declared current digest agrees with both the registered value and the root file's actual bytes.

## Source path and C1 independence

`check()` at `tools/mado-assessment.py:91-155` hashes the root's `expected.json` bytes (`:123-126`) and appends `expectations_changed` if either the current declaration differs from the registered digest or the actual file digest differs from it. It returns the deduplicated finding ID (`:152-155`). The selftest mapping at `:175-197` maps this case ID to `expectations_changed` and compares exit code, result, and finding ID; I did not run `--selftest` or any corpus/full suite. CLI `main()` routes `--check` through `evaluate()` to `check()` (`:158-163,206-230`).

This path imports only Python standard-library modules (`:8-15`) and reads the supplied bundle, its declared population file(s), and root `expected.json`; it does not invoke or consume a C1 classifier/result. The `subprocess` use is confined to the unrun `selftest()` path, which invokes this same gate on fixtures. The historical `history.c2_independent` value is compared to the fixed required `false` at `:147-151`; it is not read from current C1 output. No C1 code was run.

## Limits and confidence

Confidence is high for the exact tested bytes, the digest comparison, and the observed code/result/finding tuple. The nearby control changes only the bundle declaration; it does not separately exercise a changed root `expected.json` with a matching declaration. No full selftest was run. The fixture's timestamp strings, oracle author/`independent` fields, and Shonen evidence are assertions: this gate does not authenticate chronology, authorship, verifier identity/independence, or the semantic truth of those claims. Its output itself describes its authority as artifact assertions only.

No `lsp` device is mounted (`read xd://lsp` returned “No such tool”); definition/caller tracing therefore used the selected source sections, with grep only for navigation—not as semantic-reference proof. No tools were installed or updated.
