# FalsifyC230 — C2 case AuditRawTamperMalformed (author-lane advisory)

Seat: `MadoR22.FalsifyC230` · wave `.ufo/waves/round-22/w2` · delivered revision
`71228fd582d6d9338d7916cc64e69bd4c2e928b5` (as stated in assignment) · advisory only:
this is author-lane attack, **not** non-author admission, not host recovery, not a streak change.
All production/fixture/expected bytes read-only. No installs or upgrades were performed.

Scope: one bounded artifact check of `.ufo/waves/round-22/audit/fixtures/cases/AuditRawTamperMalformed`
against `tools/mado-evidence-audit.py` (C2). C1 tool was not run, imported or read for this verdict.

## Fixed identities and drift

| Anchor | Expected | Measured |
|---|---|---|
| C2 tool `tools/mado-evidence-audit.py` | `277eced2…458fca` | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` before **and** after |
| C1 tool `tools/mado-tripwire.py` | `36fdc459…79badce` | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` (hash only) |
| auditexpected (`audit/fixtures/expected.json`) | `b5df74b5…c2fd09` | matches; `expected.sha256` file consistent |
| oracleexpected (`oracle/expected.json`) | `b5cd4cf3…c59c4357` | matches |

No drift; the target did not move between hash checks.

## Case under test

- `bundle.json` 217 B, sha256 `01d93b6e44093c06f28b8830bade0f33612fd26bff3715e8a7aedea4646158c1`.
  Fields: `snapshot="snapshot.json"`, `sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"`,
  `claim={"clean":true,"errors":0,"lead":0,"observed":0,"total":0}`.
- `root/snapshot.json` 13 B, sha256 `e1645cb225fd5c9d477c4990847699459e446fc7bc03405ed1b6962dd7501e32`,
  bytes `7b2266696e64696e6773223a5b` = `{"findings":[` — truncated JSON, no complete array/document.
- Sealed expectation: `{"code":2,"finding_ids":["snapshot_tampered"]}`; `kind="raw"`, `claim_kind=null`.

## Independent derivation (from declared rules and raw bytes, not from tool output)

1. `sha256(b"") = e3b0c442…b855`, i.e. the bundle declares the digest of the **empty** byte string.
   The actual snapshot is 13 nonempty bytes, so declared ≠ actual with certainty
   (`declared_equals_sha256_of_empty=True`, `digest_mismatch=True`).
2. The declared value is exactly 64 lowercase hex, so it is a well-formed digest to compare
   (contrast `AuditRawDigestUppercase`/`AuditRawDigestShort`, which are bundle-format failures).
3. `.ufo/waves/round-22/audit-clarifications.md:6`: “Read bounded snapshot bytes and verify digest
   before JSON decoding/shape/verdict comparison. Digest mismatch gives code2, finding_id
   snapshot_tampered; do not compare malformed bytes as semantic results.”
   `inputs/audit-contract.json` rule: “Snapshot digest is checked before verdict comparison.”
4. Therefore the derived verdict is **code 2, finding_ids exactly `["snapshot_tampered"]`,
   result `could-not-evaluate`** — one id, no added `evidence_audit_input_invalid`.
5. The competing decode-first path is excluded *for these bytes*: `json.loads` on the 13 bytes
   raises `JSONDecodeError` (“Expecting value: line 1 column 14 (char 13)”); that is a `ValueError`,
   which `evaluate()` (tool lines 165-169) converts to `2/evidence_audit_input_invalid`.
   Both paths exit 2, so **exit status alone is non-discriminating**; `finding_ids` is the sole
   observable that separates correct digest-first from parse-first behaviour.
6. Strict-schema/claim evaluation is unreachable after the digest gate: the truncated JSON cannot
   supply `findings`/`files`, and `files` would also be missing. Nothing about the declared counts
   can be validated on this case.

## Observed measurement

One child only, address-space cap 384 MiB (`RLIMIT_AS=402653184`), 15 s timeout, exact mandated argv:

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py \
  --check .../cases/AuditRawTamperMalformed/bundle.json \
  --root  .../cases/AuditRawTamperMalformed/root
```

- exit `2`; timed out `false`; elapsed 0.0318 s; stderr empty (`e3b0c442…b855`).
- full stdout (303 B, sha256 `8f1b3f8638eb5d5b0b1d8f1ffd8404245c346421f621a3b99d2d9ccf5321e86f`):
  `{"actual_snapshot_sha256": "e1645cb225fd5c9d477c4990847699459e446fc7bc03405ed1b6962dd7501e32",
  "authority": "artifact arithmetic and evidence labels only; not semantic correctness,
  authentication, admission or promotion", "code": 2, "finding_ids": ["snapshot_tampered"],
  "result": "could-not-evaluate"}`
- `actual_snapshot_sha256` equals the independent `sha256sum`/`hashlib` value.
- No `error` key (tamper branch, not exception branch) and no `actual_counts` key
  (decode and claim validation never ran).

Match: code 2 ✓, ids exactly `["snapshot_tampered"]` ✓, label `could-not-evaluate` ✓,
authority string exact ✓, stderr empty ✓, exit == code ✓.

## Surface-by-surface attack (only where relevant to this case)

- **Digest-before-decode — exercised, consistent.** Tool lines 125-131 compare `sha256(raw)` at
  128-130 and only then `parse(raw)` at 131; output confirms the tamper branch. Confidence: high.
- **Row/line grain — unreachable.** Zero complete rows exist in the 13 bytes; the claim
  (total/observed/lead/errors 0, `clean:true`) is never evaluated. This case can neither confirm nor
  refute any row count, observed/lead split, or marker handling. It provides **no** support for the
  r19 5/1-line or 10/1-row derivations, and it is not an r19 case (`claim_kind=null`).
- **Signed/bool/nonfinite/duplicate-key strictness — not exercised.** The bundle passes a strict
  duplicate-key/non-finite parse and the claim is well-formed (`clean` bool, counters exact ints ≥0),
  but none of it is read. A mutant that accepted `bool` counts would still emit `snapshot_tampered`.
- **Path/symlink/size boundary — traversed legitimately, not discriminated.** Root and snapshot have
  no symlink components, snapshot is a regular file of 13 B (< 2 MiB), name is a valid relative
  single segment. A mutant that omitted these checks would still print `snapshot_tampered`, so this
  case adds no kill power on that axis; it only shows legal inputs reach the digest gate.
- **Truthful authority — consistent.** The emitted authority text is exactly the contract string and
  `result="could-not-evaluate"` is the contract's label for code 2. `snapshot_tampered` is an
  input-integrity/could-not-evaluate outcome, never `failed`/`clean`; nothing here is a semantic
  claim about any detector.
- **Single-id rule — consistent.** Exactly one id observed, as the clarification prescribes.

## Provenance / independence

- Pre-implementation proposal `inputs/proposals/AuditRawTamperMalformed.json`
  sha256 `74545426f80767ba7ff0e73aa21cb0798bea0a42aab0cc01ddf87d9ae9e3675d`, listed in
  `inputs/truth-seal.json`, already declares `raw_snapshot="{\"findings\":["`,
  `digest_override.literal=e3b0c442…b855`, claim zeros/clean, and `2/snapshot_tampered`.
  The materialized `root/snapshot.json` bytes equal that sealed literal exactly.
- Materialized digest `e1645cb2…501e32` is **not** in `truth-seal.json`; it appears in the
  later-materialized `expected.json` and `input_entries`, with matching `sha256`/`size_bytes`.
  This is the honest “raw truth before implementation, normalized expectation materialized later”
  split, consistent with the wave context; I did not treat the normalized digest as sealed-early.
- `expected.json` binds both bundle and snapshot in `input_entries` (directory entries present, file
  digests/sizes match). The frozen contract `inputs/audit-contract.json` (2129 B) hashes to
  `e65d165a…df23f`, exactly `expected.json.contract`; `inputs/truth-seal.json` hashes to
  `47f403f6…b24d4`, exactly `expected.json.raw_truth_seal`. The check path itself reads only the
  bundle and `root/snapshot.json` (source-inspected), so the observed match is not circular through
  the expectation file.

## Uncertainties / contradictions retained

- No contradiction with the fixed expectation was found.
- Discrimination limitation: a harness comparing only exit codes would pass a parse-before-hash
  mutant here; only exact `finding_ids` comparison separates them. The selftest source compares
  `sorted(ids) == observed_ids` plus exit and empty stderr (tool lines 252-253) — read, not run.
- Precedence boundary (outside this case): bundle claim-shape errors and snapshot digest mismatch
  both yield code 2; the declared ordering only pins “digest before verdict comparison.” This case’s
  claim is well-formed, so the ambiguity does not affect its verdict. `[INFERENCE]`
- Determinism is inferred from source (no env/time/random in `check()`) plus `-I`; only one run was
  authorized/executed. `[INFERENCE]`
- The exact set of files read is source-derived; no syscall trace was taken (no live probes).
- The proposed parse-before-hash fault is a concrete recipe only: its outcome (`input_invalid`) is
  inferred from `JSONDecodeError` being a `ValueError`; **no mutant was executed and none is called
  killed.** L1’s private sandbox owns that step.

## Verdict

Observed output matches the independently derived verdict (code 2, single id `snapshot_tampered`,
could-not-evaluate). The case is a valid **ordering** probe whose only discriminator is the finding
id. It establishes nothing about count arithmetic, row/lead semantics, r19 handling, semantic
precision, admission or promotion. Confidence: high for the ordering/tamper path; the limitations
above are explicit and unresolved by design.

Raw receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC230/result.json`
(exit, full stdout/stderr, digests, caps, derivation, provenance, surface status).
