# FalsifyC210: C2 `AuditRawDigestTamper` (round-22 w2, advisory)

Seat `MadoR22.FalsifyC210`. Leaf member, no subagent dispatch. Advisory falsification only: not a non-author admission, no semantic-precision credit, no closure or streak disposition. No production, fixture, expected, proposal, doc, or registry edits. No other cases, no selftest, no measurement driver, no reruns of the original tool.

## Result

- **Observed match: yes.** Exit 2. stdout: `code: 2`, `finding_ids: ["snapshot_tampered"]`, `result: "could-not-evaluate"`. stderr empty. No timeout.
- **Independent semantic verdict: code 2, `["snapshot_tampered"]` (could-not-evaluate).** Derived from raw snapshot bytes, the declared digest, the strict bundle schema, and the digest rule in `.ufo/waves/round-22/audit-clarifications.md` (line 6). The derivation ran in code before the tool was executed and did not use the tool output or the expected rationale.
- **Contradictions: none** among expected, independent derivation, and observed output.
- **Uncertainties retained:** U1 to U4 (section 6). Several attack dimensions are not exercised by this fixture (section 4).

## 1. Identities and drift

| Item | sha256 before = after | Drift |
|---|---|---|
| `tools/mado-evidence-audit.py` (C2 tool) | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` | none |
| `audit/fixtures/expected.json` | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` | none |
| `cases/AuditRawDigestTamper/bundle.json` (217 B) | `01d93b6e44093c06f28b8830bade0f33612fd26bff3715e8a7aedea4646158c1` | none |
| `cases/AuditRawDigestTamper/root/snapshot.json` (104 B) | `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c` | none |
| `w1/audit-proposals/AuditRawDigestTamper.json` (982 B) | `d72f1d39059c4bc5245ac787e97e85f3e5473e46714f9f68ed894640b634c3fa` | none |

Provenance checks all pass: the expected entry's `bundle_sha256`, `snapshot_sha256`, `proposal_sha256`, and `provenance.source` sha/size match the files. All 7 path/sha/size entries for this case in `expected.json` match the files on disk. The case tree is unchanged after the run.

Not checked (outside this lane): oracle expected `b5cd4cf3…`, C1 tripwire `36fdc459…`.

## 2. Measurement (single bounded run)

- argv: `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check .../cases/AuditRawDigestTamper/bundle.json --root .../cases/AuditRawDigestTamper/root`
- Caps: RLIMIT_AS 384 MiB (402653184 B), timeout 15 s, one child. Wall 0.035 s. Exit 2.
- stdout (303 B, sha256 `0922d1a6d04a9f14b504320ef666b88d920768c1fc1e80b8e0343e0855dd839b`), verbatim:

```
{"actual_snapshot_sha256": "3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c", "authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "finding_ids": ["snapshot_tampered"], "result": "could-not-evaluate"}
```

- stderr: 0 B (sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
- Receipts: `.ufo/waves/round-22/w2/receipts/FalsifyC210/`: `result.json` (sha256 `6cc2ce214e239c8fd2a5de4da005e6dd4ebdad09ddb65eddf3c6055004a8f568`; exit, full stdout/stderr, digests, drift, derivation), `stdout.bin`, `stderr.bin`.
- The verdict is not a resource-failure artifact. The tool reported an actual digest that equals the independently computed raw-byte digest, and stderr is empty.

## 3. Independent derivation (before running the tool)

| Step | Result |
|---|---|
| Bundle is a JSON object with keys exactly `claim`, `sha256`, `snapshot`; no duplicate keys; no nonfinite constants | pass |
| Declared sha: 64 chars, lowercase hex | pass (`e3b0c442…b855`) |
| Claim keys exact; total/observed/lead/errors are nonnegative exact ints; `clean` is bool | pass (`clean: true`, zeros) |
| Snapshot path `snapshot.json`: relative to ROOT; no leading `/`, backslash, empty, `.`, or `..` component; no symlink in the ROOT chain | pass (regular file; ROOT is a directory) |
| Sizes ≤ 2 MiB | pass (217 B, 104 B) |
| Raw SHA-256 of snapshot bytes equals declared | **fail**: `3972b1f5…99c` ≠ `e3b0c442…b855` |
| Verdict | **code 2, `["snapshot_tampered"]`**, decided before JSON decoding |

Supporting facts:

- `e3b0c442…b855` is the SHA-256 of the empty byte string (computed). The declared digest is the empty-input digest, so a nonempty snapshot cannot match it.
- Alternate digests of the snapshot do not equal the declared digest: raw minus trailing newline, and canonical sorted compact JSON.
- Manual check of the raw bytes (`cat -A`): findings `[]`; one files row with `eval_unparsed` 0 and `unparsed_spawns` 0. The claim (0/0/0/0, clean true) is therefore consistent with the bytes. [INFERENCE] A skipped digest check would return 0 / `evidence_audit_clean`, as the expected rationale states.
- Rule sources in `audit-clarifications.md`: line 5 (path base, symlink, 2 MiB, 64-hex sha), line 6 (digest before decode; mismatch gives code 2 `snapshot_tampered`), line 8 (exact counters, bool invalid, duplicate keys), line 9 (actual counts), line 10 (sorted ID set).
- The verdict is the same whether the tool stops after the digest or continues comparing, because the claim agrees with the bytes and no count or clean ID can fire.

## 4. Observed vs expected, and attack coverage

| Field | Expected | Independent | Observed | Match |
|---|---|---|---|---|
| code | `2` (JSON int; `normalizations: []`) | 2 | 2 (stdout and exit) | yes |
| finding_ids | `["snapshot_tampered"]` | `["snapshot_tampered"]` | `["snapshot_tampered"]` | yes, exact list |
| result label | n/a | could-not-evaluate | could-not-evaluate | yes |
| No `evidence_audit_clean` and no claim-derived IDs | n/a | n/a | absent | yes |
| actual digest | `3972b1f5…99c` | `3972b1f5…99c` | `3972b1f5…99c` | yes |

Attack dimensions, scoped to this case:

- **Path base (ROOT, not bundle parent):** exercised positively. The bundle is at `CASE/bundle.json` and the snapshot at `CASE/root/snapshot.json`; no `CASE/snapshot.json` exists. The observed actual digest proves resolution against ROOT. [INFERENCE] A bundle-parent-resolving mutant would read different or missing bytes and would not reproduce this digest-based verdict. Its exact output was not observed.
- **Digest before decode:** not discriminated. The snapshot is well-formed JSON, so decode-then-digest gives the same output [INFERENCE]. The discriminating fixture is sibling `AuditRawTamperMalformed`, which is not in this assignment and was not run.
- **Raw bytes vs canonical re-serialization:** the verdict is not discriminated, since a canonical-form digest also mismatches. The tool's self-reported actual digest equals the raw-byte digest. A canonical-form hash would differ because the file bytes (indentation, newlines) differ from compact canonical JSON, so raw hashing is observed for this input.
- **Row/line grain:** not exercised. Zero finding rows; one zero-count files row.
- **Signed, bool, and nonfinite counters:** not exercised. All counters are nonnegative exact ints; `clean: true` is a legal bool; no bool-as-count, negative, or nonfinite value.
- **Path, symlink, and size boundary:** nominal only. No traversal, no symlink component, no 2 MiB boundary.
- **Truthful authority:** the self-asserted `clean: true` with zero counts does not produce `evidence_audit_clean`. The authority string disclaims admission and semantic correctness. Because the claim agrees with the bytes, this fixture does not separate a "claim comparison after digest mismatch" mutant.

## 5. Proposed mutant recipes (advisory; NOT executed; L1 owns any run)

- **M1, digest check skipped:** [INFERENCE] predicted 0 / `evidence_audit_clean`. Caught by exit code and IDs.
- **M2, read failure yields empty bytes:** the empty digest equals the declared digest, so the digest passes. Empty bytes fail JSON decoding and yield exit 2 with `evidence_audit_input_invalid` [INFERENCE]. Exit code alone does not catch this; the harness must compare finding_ids exactly.
- **M3, decode before digest:** [INFERENCE] same output on this fixture. Blind spot here.
- **M4, canonical-JSON hashing:** [INFERENCE] same verdict on this fixture. Caught only if the harness compares `actual_snapshot_sha256` to the raw-byte digest.
- **M5, extra IDs added after a digest mismatch:** blind spot here, because the claim agrees with the bytes.

## 6. Uncertainties and contradictions retained (not normalized)

- **U1 (superseded advisory, not a contradiction of the current expected):** `w1/reports/AuditSchema.md` line 49 (ordering item 3) recommended "digest mismatch gives 1 `snapshot_tampered`". The later clarifications (line 6) set code 2, and `AuditSchema.md` line 83 records that change. The expected and the observed output both follow the clarifications.
- **U2:** code 2 for a digest mismatch is a deliberate exception to the general "1 = contradicted assertion" pattern. I followed the clarifications and did not evaluate that design choice.
- **U3:** the expected `code` is a JSON int (2), while the contract placeholder reads `"0|1|2"`. `AuditSchema.md` item 19 flagged this type question. Expected and observed are both int here, so there is no mismatch in this case. The harness must still compare types consistently across fixtures; this case does not resolve that.
- **U4:** `expected.json` was parsed in full to select this single entry and its provenance paths. No other case's values were printed or used.

## 7. Installs and scope

- Installs or updates: none. Present and used: python3 3.14.8, prlimit, timeout, jq.
- No expectation changes, no tool changes, no reruns of other cases, no new probes, no credit for semantic precision, no admission.
