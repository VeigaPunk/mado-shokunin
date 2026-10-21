# FalsifyC205 - C2 AuditMissingEvidence (one bounded artifact measurement)

Seat: MadoR22.FalsifyC205, leaf member, author-lane advisory. Not a non-author admission. No semantic precision credited. No expectation changed.

## Result

| Item | Sealed expected (normalized) | Observed | Independent derivation |
|---|---|---|---|
| exit code | 2 | 2 | 2 |
| finding_ids | `["evidence_audit_input_invalid"]` | `["evidence_audit_input_invalid"]` | `["evidence_audit_input_invalid"]` |
| verdict word | could-not-evaluate | could-not-evaluate | could-not-evaluate |
| stderr | n/a | 0 bytes | n/a |

- Observed match: yes. Exit code, stdout code, and finding ID set all equal expected.
- Independent semantic verdict: code 2 with the single ID `evidence_audit_input_invalid`. It agrees with expected and observed.
- Contradictions found in this case: none.
- Residual uncertainty: mechanism observability (U1 below). The match is verdict and ID level.

## Identities (checked before and after the run)

- `tools/mado-evidence-audit.py` sha256 `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca`, before and after. Equal to the fixed C2 identity. Drift: none.
- `fixtures/expected.json` sha256 `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09`. Equal to the fixed audit expected identity.
- Contract: `.ufo/waves/round-22/audit-contract.json` and `fixtures/inputs/audit-contract.json` both have sha256 `e65d165a1599c2d8743509bfb09ef46df9b8cc9038246b80cdef1780b5fdf23f`, 2129 bytes. Equal to the expected.json contract entry.
- Truth seal: `fixtures/inputs/truth-seal.json` sha256 `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4`, 22311 bytes. Equal to `raw_truth_seal`. Its entry for the case proposal (`.ufo/waves/round-22/w1/audit-proposals/AuditMissingEvidence.json`) is sha256 `dbcbe4843039a741c0c9ecec99616fe8ded7cec531000203fb6a972d2c79db43`, 2417 bytes. Equal to the current file.
- `cases/AuditMissingEvidence/bundle.json`: 218 bytes, sha256 `ea864709af6c076a39232fd0d0cbe5eba2ee5e5bdb0bb6dddd544af9e04e04b3`. Equal to expected `bundle_sha256`.
- `cases/AuditMissingEvidence/root/snapshot.json`: 340 bytes, sha256 `55339d4c6be5303f73e13b0a973817ce227e49766899ad58236f03b60a8d85e7`. Equal to expected `snapshot_sha256` and to the bundle claim `sha256`.
- Case tree types from `find -printf`: two directories and two regular files. No symlink components.

## Measurement (one capped child, one run)

Command:
`prlimit --as=402653184 timeout 15 python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check .../cases/AuditMissingEvidence/bundle.json --root .../cases/AuditMissingEvidence/root`

- Caps: 384 MiB address space, 15 s wall clock, one child. Exit status propagated (observed 2, not a wrapper code).
- Start and end: 2026-10-21T15:42:24Z.
- Python: 3.14.8, `/usr/bin/python3`. prlimit: util-linux 2.42.4.
- Exit: 2.
- Stdout: 240 bytes, sha256 `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`.
- Stderr: 0 bytes, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Stdout content: `{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}`
- Receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC205/` containing `result.json` (full stdout and stderr, digests, input digests, match fields), `stdout.txt`, `stderr.txt`, `exit.txt`, `tool-before.sha256`, `tool-after.sha256`, `start.utc`, `end.utc`.

## Independent derivation

Derived from bytes, the contract, and the clarifications. Written before the run. The tool source was not read.

1. Bundle: JSON object. Counters total 2, observed 1, lead 0, errors 0 are exact non-negative ints. `clean` is the bool `false`. `snapshot` is the relative path `snapshot.json`, which resolves under ROOT to `root/snapshot.json`.
2. Digest first: sha256 of the snapshot bytes equals the claim `sha256`. The digest check passes, so `snapshot_tampered` is not triggered.
3. Size bounds: 340 and 218 bytes, far below 2 MiB.
4. Strict schema:
   - `files`: nonempty, one object, `eval_unparsed` 0 and `unparsed_spawns` 0. Valid.
   - Finding row 1: `evidence` "observed", nonempty `class` and `command`. Valid observed row.
   - Finding row 2: nonempty `class` "os.system" and `command`, but no `evidence` member at all. The contract rule "each explicit evidence observed|lead" fails. Clarifications line 7 says absence is invalid uncertainty 2, not an inferred observed row. Clarifications line 8 maps invalid shapes to `evidence_audit_input_invalid`.
5. Validation fails before count comparison. Clarifications line 9 compares counts only against validated rows. No count ID is produced.

Result: code 2, `["evidence_audit_input_invalid"]`.

Note on the sizes: the byte counts equal the displayed content with one trailing newline. That is consistent with no BOM or hidden content [INFERENCE from size arithmetic].

## Why this fixture discriminates (counterfactuals, NOT run, [INFERENCE])

The declared counts (total 2, observed 1, lead 0, errors 0) are exactly what a verifier gets by counting the unmarked row toward total only. Such a verifier would emit code 0 `evidence_audit_clean`, a false clean. Other wrong handlings:

- Dropping the row: total 1 against claim 2, `finding_count_mismatch`, code 1.
- Counting it as observed: observed 2 against claim 1, `observed_count_mismatch`, code 1.
- Counting it as lead: lead 1 against claim 0, `lead_count_mismatch`, code 1.

Expected code 2 excludes all four. Observed code 2 excludes them for this input only.

## Uncertainty and contradiction ledger (retained, no expectation changes)

- U1, mechanism not separable from this receipt. stdout names no row, key, or path. Only the verdict and ID are observed. The contract's ID list has no separate ID for unavailable input, so an unavailable-input failure would also map to code 2 with `evidence_audit_input_invalid` [INFERENCE, not measured]. For example, resolving the snapshot against the bundle's parent directory (where no `snapshot.json` exists) would plausibly produce the same output [INFERENCE, not measured]. This case alone cannot exclude that. The root-resolution boundary belongs to other cases, which were not run.
- U2, ID-set interpretation for invalid input. The contract does not say whether count IDs accompany a verdict 2. Under an all-rows reading, total, observed, lead, and errors are all consistent (2/1/0/0), so no count ID arises. Under a validated-rows-only reading, no count comparison runs. Both readings give exactly `evidence_audit_input_invalid`. No conflict.
- U3, undocumented stdout key. stdout carries `"error": "Invalid"`, which the contract does not define. Non-normative. Not a contradiction.
- U4, axes not exercised by this case. Digest-before-decode ordering (digest matches, so ordering is not discriminated). Bool, signed, and nonfinite counters (none present). Size boundary (far below 2 MiB). Symlink rejection (no symlink components exist).
- U5, provenance rendering. Bundle and snapshot keys are sorted (`class` before `evidence`, `files` before `findings`). The proposal's snapshot object has the same content in a different key order. Semantically identical. The digest-bearing bytes are the case file. Not a contradiction.
- U6, normalization. Proposal `expected.code` "2" (string) is normalized to 2 (int). The original is retained in expected.json `normalizations` and `original_expected`. Allowed by audit-clarifications line 10. No semantic change.
- U7, r19 linkage. This fixture is synthetic. It does not evaluate the actual r19 receipt, and nothing here is an r19 claim.

## Authority

- stdout `authority` is identical to the contract `authority` (jq string compare). Advisory only. No semantic correctness, admission, or promotion is credited.

## Constraints observed

- Did not read `tools/mado-evidence-audit.py` source. Did not run the 46-case selftest, the measurement driver, any other case, or any sibling counterfactual.
- No builds, lints, tests, package, service, process, compositor, or live-probe queries. No codewriter edits. Old tools not rerun.
- Installs and updates: none. Tools used were already present: python3 3.14.8, prlimit 2.42.4, timeout, jq, sha256sum, find, stat.

## Optional for L1 (proposed, NOT run, not a kill claim)

To separate the marker mechanism from U1, L1 could run two private sandbox variants of the same bytes, changing only row 2's evidence. Predicted: `lead` gives code 1 `lead_count_mismatch`, and `observed` gives code 1 `observed_count_mismatch` [INFERENCE]. Neither was measured here.

## Verdict on this attack item

The observed match and the independent semantic verdict agree with expected. No defect found in this case. The only residual is mechanism observability (U1).
