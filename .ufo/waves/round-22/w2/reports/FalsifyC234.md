# FalsifyC234 — C2 HistoricalC3.D1.line-claim-on-row-snapshot

Seat `MadoR22.FalsifyC234`. This is an advisory attack from the author lane only, not admission by a non-author. Delivered revision: `71228fd582d6d9338d7916cc64e69bd4c2e928b5`.

## Result

- **Observed result matches expected.** The run exited 1 with result `failed` and finding IDs `["finding_count_mismatch","observed_count_mismatch"]`. Stderr was empty. `actual_counts` were total 11, observed 10, lead 1, errors 0. The receipt is `.ufo/waves/round-22/w2/receipts/FalsifyC234/result.json`.
- **Independent derivation gives the same verdict.** I derived it from the raw bytes, the declared counts and the contract, not from the old classifier's output.
- **Semantic verdict:** code 1 is truthful, but it only means a grain mismatch. The claim of 6 total, 5 observed and 1 lead is correct when counted by line. The contract counts rows, and this snapshot has 11 rows. The `failed` result does not mean any evidence was invented or promoted. It earns no credit for semantic precision or admission.
- **Retained contradiction:** the `rationale` stored for this case in the fixture file is wrong. The expected code and finding IDs are not affected. Details below.

## Identities (checked before and after the run; no drift)

| Input | sha256 |
|---|---|
| `tools/mado-evidence-audit.py` | `277eced2…badce`, the fixed C2 identity |
| `audit/fixtures/expected.json` | `b5df74b5…2fd09`, the fixed audit-expected identity |
| case `bundle.json` (218 B, regular file, one link) | `105a636b…a6c99`, matching the `bundle_sha256` in expected.json |
| case `root/snapshot.json` (3140 B, regular file, one link) | `f9cf3c64…6c608`, matching the bundle's `sha256` and the expected.json `snapshot_sha256` |
| `w1/historical-c3.json` (proposal) | `9ee6144d…bed7a`, matching expected.json |

The run used `prlimit --as=402653184 -- timeout 15 python3 -I <tool> --check <bundle> --root <root>`. `prlimit` executes `/usr/bin/timeout` directly, not the shell builtin. The interpreter was Python 3.14.8, and only one child process ran.

## Independent derivation

The contract and clarifications set the counting rule. `total` is the number of validated finding rows, with no deduplication. `observed` and `lead` count explicit marker rows. `errors` sums `eval_unparsed` and `unparsed_spawns` across all files. `clean:false` is a conservative assertion that the scan is not cleared.

These counts come from the snapshot bytes:

- **Rows:** 11, of which 10 are observed and 1 is lead. The single lead row is `inputs/r13-root.jsonl:4`, rule `pacman:-Q`.
- **Files:** 5 entries. All 10 counters are 0, so errors = 0.
- **Distinct (file, line) pairs:** 6. They are r13-global:1 (4 rows), r13-root:4 (1 row), r14-review:1 (2 rows), r14-source-safety:2 and :3 (1 row each), and r15:1 (2 rows). That gives 5 observed lines and 1 lead line.

The bundle claims total 6, observed 5, lead 1, errors 0, `clean:false`. Comparing claim to actual:

- total: 6 ≠ 11, giving `finding_count_mismatch`.
- observed: 5 ≠ 10, giving `observed_count_mismatch`.
- lead: 1 = 1, and errors: 0 = 0.
- clean is false, so neither clean-contradiction ID applies.

Verdict: code 1 with `["finding_count_mismatch","observed_count_mismatch"]`. This matches the expected result and the output.

The materialized snapshot matches the proposal's `D1_row_level_with_later_markers` (proposal lines 163–188). The values and order of all 11 rows and 5 file entries are identical; only key order differs, because the file is pretty-printed with sorted keys. I did not recompute the proposal's canonical digest `9507e816…`, because only one execution was authorized. That equality is unverified.

## Attacks relevant to this case

- **Row vs. line grain:** the tool counts `len(findings)` rows, which matches the contract text ("ACTUAL validated row/error counts … no deduplication"). The `file` and `line` fields are not part of the normative schema (`audit-contract.json` line 6), so a line-grain claim cannot be expressed or validated. It can only be judged at row grain. Here that is correct behaviour, not a defect. The `lead` count matches at both grains only because the single lead line has exactly one row. Every finding's `file` appears in `files[]`, so the population is not mismatched.
- **Digest before decode:** the tool hashes the bounded raw bytes before `parse()` (tool lines 127–131). The digest matches here, so the tamper path was not exercised.
- **Signed, bool and nonfinite counts:** all claim counts are plain non-negative ints, and `clean` is a real bool. `count()` requires `type(...) is int`, rejects negatives, and the parser rejects nonfinite numbers. The defect paths for these are not exercised by this case.
- **Path, symlink and size boundary:** the snapshot is named by the plain relative path `snapshot.json`. Both files are regular, have one link each, and are far below 2 MiB, with no symlinks in the case directory. These defect paths are not exercised.
- **Truthful authority:** the output's `authority` string disclaims semantic correctness, authentication, admission and promotion, which is consistent with this being a derived input. The case's `claim_kind` ("Derived historical C3 comparison; not an r19 claim") and `derivation_kind` are honest. Per the guard clarifications, the actual markerless r19 receipt remains code 2 (could-not-evaluate). This case does not reinterpret it.

## Counterexample (provenance defect; does not change the verdict)

The `rationale` in `audit/fixtures/expected.json` line 1897 is the D2 headline text, copied verbatim from `w1/historical-c3.json` line 23. That text says "Six rows = the six frozen incident lines … total 6 = 6 rows … -> code 0 evidence_audit_clean". It contradicts the case's own `snapshot_sha256`, which points to the 11-row snapshot, and its `expected` (code 1). The expected code and IDs agree with the proposal's D1 case list (line 192) and with my derivation, so the verdict is unaffected. The case's human-readable provenance, however, asserts the opposite outcome on the wrong snapshot.

The same copied text appears on 5 cases in total:

- It is wrong on 3 D1 cases: this one, `D1.row-claim-matches-derived` and `D1.row-counts-claimed-clean`.
- It is accurate on 2 D2 cases: `D2.line-claim-5-observed-1-lead` and `r19-c3-derived-six-row-5obs-1lead`.

- **Affected axes:** provenance truthfulness and reviewability of C2 fixtures. Arithmetic correctness and the expected verdict are not affected.
- **Type of defect:** fixable, not a trade-off.
- **Smallest safe correction (owned by L1, not done here):** re-materialize the `rationale` for the three D1 cases from the proposal's D1 `cases[]` entries plus the D1 derivation text. This changes no `expected` value and no snapshot or bundle bytes. The audit-expected digest would change and would need resealing by the owner.

## Scope

- No edits to the tool, fixtures, expectations or proposals.
- Nothing was installed.
- No selftest, measurement driver or other execution beyond the one authorized check and read-only hashing and counting.
