# FalsifyC209 — C2 AuditRawDigestShort

## Findings by severity

**No actionable defect found in the assigned case.** The delivered auditor rejects the malformed 63-character digest as **2 / could-not-evaluate / `evidence_audit_input_invalid`**, matching both the frozen expectation and an independently derived semantic verdict. This is neither clean/0 nor contradicted-assertion/1, and it is not `snapshot_tampered`.

Axes: strict digest syntax; raw-byte identity before snapshot decoding; row/error-count honesty; fail-closed classification; authority and bounded isolation.

## Independent derivation

The normative schema requires exactly 64 lowercase hexadecimal digest characters and distinguishes malformed input from a well-formed digest mismatch: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-clarifications.md:5-8`; verdict meanings are fixed in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-contract.json:5-9`.

The assigned bundle, `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDigestShort/bundle.json:2-10`, declares:

- `sha256`: `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99` — **63**, not 64, lowercase hex characters.
- Snapshot path: `snapshot.json`.
- Claim: total/observed/lead/errors all exact integer zero, with `clean:true`.

Independent SHA-256 of the **104 raw snapshot bytes** is `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c`. The declared digest is exactly its 63-character prefix, omitting the final `c`. The snapshot has zero finding rows and one file row with `eval_unparsed:0` and `unparsed_spawns:0`; see `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDigestShort/root/snapshot.json:1-9`. Independent row arithmetic therefore gives `(total, observed, lead, errors) = (0, 0, 0, 0)`, not a physical-line count. Those arithmetic assertions would be consistent on their own, but they do not repair the malformed bundle field. The required verdict remains **2 / `evidence_audit_input_invalid`** before any count verdict.

This derivation was recorded in the orchestration state before the sole candidate run. It did not use old-classifier output or import candidate functions. The fixed-case entry from `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json` retains the same original and normalized expectation and an empty normalization list. Its proposal provenance matches `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/inputs/proposals/AuditRawDigestShort.json:4-9` and the proposal hash below.

## Delivered code and error-path evidence

The delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5` adds the 286-line auditor relative to registered base `741122d177ae8ff68a73768777f20484d5bdcbe4`. The relevant implementation and entrypoint hunks were reviewed.

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:20-26`: the digest pattern is `[0-9a-f]{64}\Z`; `Invalid` subclasses `ValueError`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:121-131`: `check` requires a string digest, rejects a failed full match at lines 125-126, and only afterward opens/hashes the snapshot. Digest comparison precedes snapshot decoding. For this case the format rejection occurs before snapshot access; the candidate did not establish snapshot counts or identity at runtime.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:165-169`: `evaluate` converts that `ValueError` subclass to exactly code 2 with `evidence_audit_input_invalid`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:267-286`: the `--check` route calls `evaluate`, prints the result, and returns its code. The independent process exit agrees with the emitted code; no alternate scanner runtime or rerouting was invoked.

These are direct source/diff and execution observations. `xd://lsp` is not mounted, so status, references, definition, and diagnostics were unavailable. Literal identifier search was fallback navigation only, not semantic proof or a claim that diagnostics passed.

## Sole authorized measurement

Executed once, without selftest or measurement driver:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDigestShort/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDigestShort/root
```

Child limits: `RLIMIT_AS` soft/hard 402653184 bytes (384 MiB), `RLIMIT_CPU` soft/hard 15 seconds, and a 15-second subprocess wall timeout. One scanner child total; elapsed wall time 0.034116840 seconds; no timeout.

Exit: **2**. Full stdout, including its final newline, is preserved in the receipt:

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

Stderr: empty. **Observed expectation match: yes. Independent semantic verdict match: yes.** No contradiction or tool/input drift was observed.

Raw exit, complete stdout/stderr, their byte lengths/hashes/base64, raw fixed-case inputs, caps, independent derivation, and before/after input hashes are recorded at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC209/result.json`.

| Artifact | SHA-256 before = after |
| --- | --- |
| Selected auditor | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| Audit expected manifest | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| Assigned bundle | `9fc0d5c6ee3463c87c0961322882df122464bc93268f96d50a1b68fbd9c13f29` |
| Assigned snapshot | `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c` |
| Frozen proposal | `e9306ca03eac50d3e00360a126ad7131397b1d4033cb6ccdf9d2973a7a88facb` |

The auditor and expected-manifest hashes match the fixed assignment identities both before and after the run.

## Residual risk and verification gaps

- This early-rejection case exercises malformed-digest refusal, not successful byte-digest comparison, decoding of a tampered/malformed snapshot, or dynamic count checking. The source ordering supports the former boundary; no broader runtime coverage is claimed.
- Zero finding rows and one zero-error file row provide no observed-versus-lead ambiguity. There are no negative, boolean-as-count, or nonfinite numeric inputs here. The 216-byte bundle and 104-byte snapshot do not test the 2 MiB size edge, path escape, or symlink rejection; the snapshot path checks are not reached on this execution. No extra probes were added.
- No mutant was executed. The proposal's wording about killing a prefix/`startswith` implementation is not credited as an observed mutant kill.
- This is bounded author-lane advisory artifact evidence only: no semantic precision, authenticated chronology, saturation, admission, non-author acceptance, or historical-rejection reset. Actual markerless r19 remains code 2; a 5/1 line or 10/1 row population would require explicit derivation, and an all-observed inflation claim would be a new counterfactual, not an actual r19 claim. None was measured here.
- An initial expected-JSON selector failed because it assumed an object rather than a case array; the tool error included unrelated JSON. The retry used exact-id filtering; unrelated error-output content was not used as evidence. This tool-output issue was reported through `xd://report_issue`.

No production, fixture, expected, proposal, gate, registry, or shared documentation files were changed. No installs/updates, old-tool reruns, builds, lints, formatters, generic smokes, full suites, source-shaped probes, or fixture-code execution were performed. Only this assigned report and receipt were written.

Recommendation: retain the case as a successful bounded invalid-input rejection; do not promote it into broader correctness or admission evidence.
