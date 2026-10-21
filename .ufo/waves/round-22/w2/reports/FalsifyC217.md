# FalsifyC217 — AuditRawOverflowCounter

## Axes and scope

Axes: exact-count/finite-number schema fidelity; digest-before-decode and invalid-input verdict fidelity; reproducible bounded evidence and truthful authority.

Reviewed delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, confined to the assigned fixed case. This is an author-lane advisory review, not non-author admission. No routing, canonical-runtime, resume, or saturation claim is made; no other runtime was invoked. L1 retains planner/integration authority.

## Findings by severity

**No actionable defect found in this fixed case.** Observed result matches the frozen expectation **and** the independently derived semantic verdict: **exit 2, `could-not-evaluate`, exactly `['evidence_audit_input_invalid']`**. This is a successful refusal measurement, not an audit-clean verdict and not assertion-failed code 1.

### Independent derivation

- The raw snapshot at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawOverflowCounter/root/snapshot.json` contains `{"findings":[],"files":[{"eval_unparsed":0,"unparsed_spawns":1e400}]}`. There are zero finding rows and one file row. The invalid counter must not be discarded or converted into zero errors.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-contract.json:5-8` and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-clarifications.md:6-9` require exact nonnegative integer counters, finite decoded numbers, and code 2 for invalid input. `1e400` is a valid JSON numeric token, but Python's default JSON decoding yields a nonfinite float, not an exact `int`. Its mathematical integrality does not satisfy the required runtime type.
- The bundle claim is `total=observed=lead=errors=0`, `clean=false`; see `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawOverflowCounter/bundle.json:2-10`. A conservative `clean:false` does not waive schema validity. Actual error totals cannot be established from the invalid counter, so this is neither a clean 0 nor a contradicted-assertion 1.
- The measured raw snapshot SHA-256 equals the bundle declaration: `996f1e4b190fbda1df83c51f4e2b537acc18fb6c2a3689a2c402c73f2a6f0379`. Therefore the correct stable ID is invalid input, not `snapshot_tampered`.
- The fixed expectation and its provenance at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json:807-849` agree. `original_expected` is unchanged and `normalizations` is empty. The frozen proposal copy at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/inputs/proposals/AuditRawOverflowCounter.json:3-9` preserves the literal exponent token. The independent expectation was recorded before the scanner invocation; no old classifier output was used.

### Candidate path and actual diff

Source-level reasoning, not a runtime branch trace:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:121-131` reads bounded bytes and verifies SHA-256 **before** snapshot decoding. The 218-byte bundle and 69-byte snapshot are below the 2 MiB bound.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:38-53` recursively rejects decoded nonfinite floats. `parse_constant` alone would not cover an otherwise standard exponent token; the explicit `finite` walk does.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:67-77,145-149` also requires exact integer counter types before aggregation/comparison. No integer coercion, zero default, or `int(inf)` is used.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:165-169,267-286` converts `Invalid` into the controlled code-2 JSON result and returns that code as the process status. The observed output reports `error: Invalid`, not an uncaught overflow traceback.
- The actual delivered-revision diff changes only `relative`'s optional `allow_backslash` argument and enables it for fixture inventory names. Textual callsites are at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:99,187,238`: snapshot `rooted` and selftest root-path parsing retain the strict default; inventory opts in. The assigned `--check` does not invoke inventory/selftest. This change does not weaken the fixed case's path validation or numeric refusal.

## Observed evidence

Exactly one scanner child ran, with the exact assigned `python3 -I ... --check ... --root ...` argv preserved in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC217/result.json`. Child address-space soft/hard limits were both **402653184 bytes (384 MiB)**; `subprocess.run(timeout=15)` enforced the wall cap. No background job was used.

- Exit: **2**. Timed out: **false**. Elapsed: **0.03210346099513117 s**.
- Full stdout (240 bytes, including terminal newline):

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

- Full stderr: empty (0 bytes).
- stdout SHA-256: `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`.
- stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Receipt preserves full text plus base64 stream bytes and both stream digests.

All following digests were measured before and after the scanner run and remained identical:

| Artifact | SHA-256 |
| --- | --- |
| Selected C2 tool | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| Audit expected manifest | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| Assigned bundle | `d3257ba9de2eb48b74310a517aa6a2f177588bac2c00fe57b47135f62b0357f0` |
| Assigned raw snapshot | `996f1e4b190fbda1df83c51f4e2b537acc18fb6c2a3689a2c402c73f2a6f0379` |
| Frozen proposal copy | `38a4f4d8d6b9c05f36a0ae2c0985877e41c412e2eb9c2a6fd9422608cd2331be` |

Selected tool and audit expected manifest match the assignment's fixed identities. **No drift or expectation contradiction observed.**

## Residual risk and verification gaps

- LSP is unavailable: both `read xd://lsp` and an explicit status request returned `No such tool`. References, definition, and diagnostics could not run. Literal searches were the fallback; their output is not semantic-reference proof.
- This case has no finding rows. It cannot establish row-versus-line aggregation correctness, evidence-tier classification, signed/bool counter behavior, path/symlink attack rejection, or size-boundary behavior. Those were not added as probes. The precise rejecting branch is inferred from the inspected source; stdout exposes only the exception class.
- Only the assigned bounded check ran. No 46-case selftest, measurement driver, original tool rerun, whole-corpus/oracle rerun, extra source-shaped probe, mutation, build, lint, formatter, generic smoke, or host/live probe was performed. No install/update was needed. Writes are confined to the assigned report and receipt.
- No semantic precision, authentication, admission, promotion, or historical C3 repair is established. Per `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/guard-clarifications.md:5-9`, markerless actual r19 remains code-2 could-not-evaluate; 5/1-line or 10/1-row forms require explicit derivation. No all-observed inflation claim is attributed to actual r19, and prior r19/r20/r21 rejected-harmed authority/streak is unchanged.

Recommendation: retain this narrow refusal match as bounded C2 evidence only; it supplies no admission authority.
