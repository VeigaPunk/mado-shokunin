# FalsifyC201 — C2 AuditBoolCount

## Findings, severity ordered

**No actionable defect found in the assigned case.** The sole authorized invocation returned process exit **2**, JSON code **2**, result **`could-not-evaluate`**, and exactly **`["evidence_audit_input_invalid"]`**, with empty stderr. This matches both the selected expectation and the independent schema-based verdict recorded before execution. This is a successful invalid-input rejection, **not** a clean audited receipt, a code-1 contradicted assertion, semantic-precision credit, or admission.

Assigned revision: `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. The selected C2 tool and audit expectation hashes matched the assignment before and after the invocation. No drift was observed.

### Axes

1. Strict schema and finding-row count grain.
2. Frozen byte identity, bounded regular-file inputs, and path confinement.
3. Could-not-evaluate versus failed/clean verdict honesty.
4. Single-case evidence and artifact-only authority.

### Independent semantic derivation

The normative contract requires `claim.total` to be a **nonnegative exact int**, explicitly makes booleans-as-counts invalid, and assigns invalid input to code 2: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-contract.json:5-9`.

The raw bundle has `"total": true`, not integer `1` or `2`: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditBoolCount/bundle.json:2-10`. JSON `true` is a boolean, so the claim is not eligible for arithmetic comparison.

Independently counting the actual snapshot rows yields:

| Quantity | Derivation |
| --- | --- |
| Total | 2 finding objects, not a per-class summary or snapshot exit value |
| Observed | 1 row explicitly marked `observed` |
| Lead | 1 row explicitly marked `lead`; it is not observed execution |
| Errors | `(0 + 0) + (0 + 0) = 0` from the two files members |
| Population | 2 files members, nonempty |

Evidence: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditBoolCount/root/snapshot.json:10-54`. The snapshot's top-level `exit`, class counts, and `observed_findings`/`lead_findings` summaries are not used as oracle outputs. Its printed commands remain inert artifact strings and were never executed.

All of this leaves `claim.total:true` malformed. It must produce **2 / `evidence_audit_input_invalid`**, not `finding_count_mismatch`, other mismatch IDs, or a clean-claim ID. That reasoning does not depend on an old classifier result. The selected expected record discloses only normalization of expected code string `"2"` to integer `2`; its claim remains boolean and no expectation was changed by this review.

The independent premeasurement derivation is retained at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC201/independent-before.json`.

### Candidate check and actual diff

The relevant candidate logic agrees with that independent derivation:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:67-77`: `count` calls `require(..., int)`, and `require` checks exact `type(value) is int`, rejecting bool rather than coercing it.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:121-149`: bounded raw snapshot bytes are hashed at lines 127-130 **before snapshot decoding** at line 131; rows and file counters are validated before declared claim counts. `total` is the first declared count and rejects the boolean before mismatch generation at lines 150-160.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:25-26,165-169`: `Invalid` inherits `ValueError`; `evaluate` catches it and returns only `evidence_audit_input_invalid` with code 2.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:267-286`: the canonical `--check` route calls `evaluate`, prints its result, and returns the same code. No alternate audit runtime or selftest route was invoked.

The actual delivered-commit diff was inspected with `git show --format=fuller --no-ext-diff --no-renames 71228fd582d6d9338d7916cc64e69bd4c2e928b5 -- tools/mado-evidence-audit.py`. It adds `allow_backslash=False` to `relative`; the inspected `rooted` check caller still uses the strict default at lines 97-105. Only fixture `inventory` opts into literal POSIX backslash filenames at lines 185-187; its inspected callers are in `selftest` at lines 226 and 257, not this invocation. This plain `snapshot.json` case neither exercises nor establishes the changed inventory behavior.

### Observed execution and identity

Exactly one scanner child was run, with this argv and no shell:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditBoolCount/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditBoolCount/root
```

The controller set soft and hard `RLIMIT_AS` to **402653184 bytes (384 MiB)** in the child's pre-exec function and applied a **15-second** subprocess timeout. The invocation completed in approximately **0.0315 seconds**, without timeout. This is one bounded observation, not a memory-saturation or resource-scaling claim.

Full stdout, including its terminal newline, is retained in `result.json` as both text and base64; stderr is empty. The observed stdout was:

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

Stdout: 240 bytes, SHA-256 `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`.

| Artifact | SHA-256, identical before and after |
| --- | --- |
| Selected C2 tool | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| Audit `expected.json` | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| Selected bundle | `23c8c809c30eeb07ced352a1ea140aedee3cd2437c4dd5c06e01491674463915` |
| Selected snapshot | `c0d3bd9bee06d4397dc408e1a257cebd7f4a80369d0f8f11c20de832e7ca93f3` |

The bundle and snapshot are regular files of **221** and **1508** bytes, both below 2097152 bytes. `namei -l` showed no symlink in either selected absolute input path. The bundle names plain root-relative `snapshot.json`; its declared digest matches the exact snapshot bytes and the selected expected record. Thus there is no relevant missing-file, escaping-path, symlink, size, or digest contradiction masking the boolean-count defect.

Raw receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC201/result.json`.

## Residual risk and verification gaps

- **Scope is one malformed total claim.** The two findings occupy distinct file/line pairs, so this case cannot discriminate row counting from line deduplication. It does not independently exercise bool rejection in every other count field, signed/nonfinite counts, digest-mismatch/invalid-JSON precedence, symlink/path rejection, or the exact 2 MiB boundary. The cited code order is static evidence, not an additional runtime experiment.
- **LSP unavailable.** Reading `xd://lsp` returned `No such tool`; no LSP status, references, definition, or diagnostics request could be made. Source and actual-diff inspection are literal static fallback, not semantic-reference or diagnostics proof.
- **Expectation-selection exposure disclosed.** The initial JSON selector retained the enclosing cases array and returned unrelated expectation records. It was corrected to `.cases[]|select(.id=="AuditBoolCount")`. No other case was measured or used to derive this verdict.
- **Provenance is not authentication.** Proposal SHA-256 `75f575d1c7f51a054255bfbdcf67ac829c5a5e0110ae569321d0a2b2ccad5bf3` is recorded by the selected expected record; this seat did not independently rehash that proposal or authenticate chronology. No rawtruth/normalization chronology was invented.
- **Historical limitation remains intact.** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/guard-clarifications.md:9` states that the actual markerless r19 receipt is code 2, not failed 1 or clean 0. No r19 input or old tool was rerun here. This case demonstrates neither an actual-r19 inflation claim nor derived 5-observed/1-lead incident-line or 10-observed/1-lead finding-row projections. Prior red receipts and the rejection streak remain unchanged.
- No full 46-case selftest, measurement driver, build, lint, formatter, generic smoke, new source-shaped probe, mutant run, C1 invocation, package/process/live probe, install/update, delegation, background job, or production/fixture/expected/source mutation was performed. Only this seat's report and raw receipts were written. No admission judgment is made.

Report: .ufo/waves/round-22/w2/reports/FalsifyC201.md
