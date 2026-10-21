# FalsifyC211 — AuditRawDigestUppercase

## Findings, by severity

**No actionable defect found in this fixed case.** The delivered candidate returned exit **2**, JSON code **2**, result **`could-not-evaluate`**, and exactly **`["evidence_audit_input_invalid"]`**, with empty stderr. This matches both the selected sealed expectation and the independent pre-execution derivation below. It is a correct refusal to evaluate malformed input, **not** a clean artifact audit, assertion failure/code 1, semantic-precision result, or admission.

Axes: (1) strict digest representation/error taxonomy; (2) raw-byte identity and row-grain arithmetic; (3) bounded single-runtime reproducibility and honest authority.

## Independent semantic derivation

The frozen input at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDigestUppercase/bundle.json:2-10` declares `total=observed=lead=errors=0`, `clean=true`, snapshot name `snapshot.json`, and this digest:

```text
3972B1F5D92CB5A2FF347D11CBE2861765E10E0954764A87931195E17EEAE99C
```

Independently hashing the **104 raw snapshot bytes**, without importing or executing a classifier, gives:

```text
3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c
```

The digest value is the uppercase spelling of the right byte digest, but not its required representation. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/inputs/audit-contract.json:5-8` requires a lowercase SHA-256 and classifies invalid input as code 2. Normalizing the supplied value would silently relax that contract; calling this `snapshot_tampered` would confuse malformed digest syntax with a well-formed digest mismatch.

The raw snapshot at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDigestUppercase/root/snapshot.json:1-9` has an empty findings list and **one files member**, with both error counters integer zero. Thus independent row-grain counts are total 0, observed 0, lead 0, errors 0; the file population is nonempty. The count values are neither booleans, negative numbers, nor nonfinite numbers, and `clean` is a proper boolean. Those otherwise consistent counts do not cure the malformed digest. There is no incident-line/row conversion in this case.

The relevant candidate path is explicit:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:20-22,121-131`: the anchored lowercase-only SHA regex rejects the uppercase characters at lines 125-126, **before** snapshot path resolution, reading, digest comparison, decoding, or finding/count comparison.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:25-26,165-169`: `Invalid` subclasses `ValueError`; `evaluate` maps this exception to code 2 and `evidence_audit_input_invalid`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:267-286`: the canonical `--check` route calls `evaluate`, prints its JSON, and returns the same code. No alternate implementation or rerouted identity was used.

This establishes the expected code and ID independently of old classifier output. The branch explanation is static source reasoning, not an instrumented execution trace.

## Observed bounded measurement

Exactly one candidate child was launched, synchronously, with the assigned command:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDigestUppercase/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDigestUppercase/root
```

Hard address-space limit: **402653184 bytes (384 MiB)**. Wall timeout: **15 seconds**; CPU limit: 15 seconds; concurrency: 1. Observed elapsed time was approximately **0.0324 seconds**, without timeout. Exit was **2**. Full stdout was 240 bytes, including its final newline:

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

Stderr was empty (0 bytes). Full streams, their base64 encodings, input-byte encodings, limits, timestamps, derivation, and before/after hashes are retained at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC211/result.json`.

| Identity | SHA-256, unchanged before/after |
| --- | --- |
| Selected C2 tool | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| Audit expected manifest | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| Selected bundle | `ed3fc72f41bf48116943f03188c627ac7e7a9d3e614530cf1f49a792aff4eadb` |
| Raw snapshot | `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c` |
| Frozen audit contract | `e65d165a1599c2d8743509bfb09ef46df9b8cc9038246b80cdef1780b5fdf23f` |
| Original selected proposal | `3db3a9461705c01616041865c61ab7110beaf7dabd0e61f9459d0a2a64aa2b38` |

Stdout SHA-256: `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`. Empty stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. No selected tool/input drift was observed.

## Diff and provenance boundaries

Reviewed the auditor diff for delivered commit `71228fd582d6d9338d7916cc64e69bd4c2e928b5`: it adds an explicit backslash allowance for fixture inventory names, while retaining the strict default for snapshot API paths. Relevant definitions/callers are `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:80-85,97-105,185-187,238`. This malformed-digest case exits before those snapshot checks and does **not** measure that compatibility change or the selftest inventory route.

Only the assigned case's expected/provenance record was selected from `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json`. Its original and materialized expectations both specify code 2 and the same sole ID, with `normalizations: []`. The frozen source proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/inputs/proposals/AuditRawDigestUppercase.json:4-9` has the same raw snapshot structure, uppercase-digest transform, and expectation. No expectation contradiction was found or changed. The proposal's asserted mutant kills were **not executed or credited**.

The assignment states raw truth landed at `9185f1f9` before implementation and the normalized expected manifest materialized later; this scoped check does not independently authenticate chronology. The manifest's raw-truth seal digest is provenance metadata here, not a newly verified full-seal inventory.

## Residual risk and verification gaps

- The result supports only this exact uppercase-digest refusal. Zero finding rows cannot demonstrate nonempty row-vs-line counting, observed/lead separation, error-bearing clean-claim refusal, or saturation. No broad coverage or semantic precision is credited.
- The digest-format guard prevents reaching snapshot decoding/path/symlink/size-boundary logic. The 217-byte bundle and 104-byte snapshot are not boundary tests; no such coverage is inferred from code 2. No additional payload was created.
- `xd://lsp` was unavailable (`No such tool`). Consequently LSP status, references, definition, and diagnostics could not be obtained. Targeted source reads and literal grep were fallback evidence only, not semantic LSP proof.
- No selftest, measurement driver, whole-corpus/oracle rerun, old-tool run, fixture-code execution, mutation execution, build, lint, formatter, or generic smoke was performed. No installs/updates were needed. Only the assigned report and receipt were written.
- This is author-lane advisory evidence, not non-author admission. Prior r19/r20/r21 rejected-harmed receipts and streak remain unchanged. Markerless actual r19 remains code 2/could-not-evaluate; no historical 5/1-line or 10/1-row derivation or new inflation claim is made by this case.

**Scoped reviewer recommendation:** record the observed match and correct malformed-input refusal, with the above limits; do not promote it to clean-audit, semantic-precision, chronology-authentication, or admission credit.
