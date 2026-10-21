# FalsifyC214 — AuditRawDupNestedConflict

## Findings by severity

No actionable candidate defect identified in this fixed case. The sole authorized measurement returned exit **2**, JSON code **2**, result **could-not-evaluate**, and exactly `['evidence_audit_input_invalid']`, with empty stderr. This matches both the frozen expectation and the independently derived strict-schema verdict. It is neither a clean result nor a code-1 contradiction verdict.

This is author-lane advisory evidence only. It establishes a bounded invalid-input rejection, not C1 semantic precision, C2-wide completeness, saturation, historical repair, admission, or non-author approval.

## Axes and scope

1. Strict duplicate-key rejection and honest uncertainty.
2. Exact-byte identity and digest-before-decode ordering.
3. Bounded, read-only execution and truthful authority.

Reviewed the added audit-tool diff from base `741122d177ae8ff68a73768777f20484d5bdcbe4` to delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`: the tool is a new 286-line file. Only the assigned artifact/check path was measured. No other case expectation was read, no old classifier was run, and no fixture payload was executed. No subagents, alternate runtime/rerouting, measurement driver, selftest, mutant, build, lint, formatter, generic smoke, installation, or live-host probe was used.

## Independent verdict, derived before execution

Raw evidence:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDupNestedConflict/root/snapshot.json:1` is exactly:

  ```json
  {"findings":[],"files":[{"eval_unparsed":1,"unparsed_spawns":0,"eval_unparsed":0}]}
  ```

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDupNestedConflict/bundle.json:2-10` declares `total=0`, `observed=0`, `lead=0`, `errors=0`, `clean=true`, the exact snapshot digest, and relative path `snapshot.json`.
- The independently authored proposal preserves the same raw string and claim at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/audit-proposals/AuditRawDupNestedConflict.json:2-9`. Its digest matches the selected case's frozen provenance. The selected `AuditRawDupNestedConflict` record in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json` has original and normalized expectations both code 2 / `evidence_audit_input_invalid`, with no normalization.

The conflict is inside the single `files` object: the same `eval_unparsed` key appears with values **1** and **0**. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-clarifications.md:6-9` requires digest verification before decoding, rejects duplicate keys **anywhere** as code 2 / `evidence_audit_input_invalid`, and requires exact nonnegative integer counters. The raw digest matches the declared digest, so `snapshot_tampered` is not the applicable verdict. Duplicate-key invalidity precedes arithmetic comparison: there is no validated actual error total to compare with the zero claim.

A last-wins interpretation would erase the explicit `1` and permit false clean; a first-wins interpretation would produce a code-1 error-count/clean contradiction. These are reasoning-only counterfactuals, not executed results. Both violate the declared duplicate-key rejection rule. The independently derived verdict is therefore **code 2**, exactly **`['evidence_audit_input_invalid']`**.

### Relevant candidate call chain

All citations below are to `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py`:

- `main`, lines 267-282: the actual `--check` invocation calls `evaluate`, prints its JSON, and returns its code.
- `check`, lines 121-131: parses the bundle, reads the rooted bounded snapshot, hashes the raw bytes, rejects a mismatch, and only then parses the snapshot.
- `parse`, lines 51-53: installs `object_pairs_hook=pairs`, including for nested objects.
- `pairs`, lines 29-35: rejects a repeated key with `Invalid('duplicate JSON key')`, rather than selecting its first or last value.
- `Invalid`, lines 25-26, and `evaluate`, lines 165-169: `Invalid` is a `ValueError`; the caught error becomes code 2 / `evidence_audit_input_invalid`.
- `result`, lines 116-118: code 2 is explicitly named `could-not-evaluate`. The invalid parse does not reach the actual-count/claim comparisons at lines 132-162.

This directly supports the bounded rejection and honest uncertainty result; it does not import any C1 detector verdict.

## Authorized measurement and immutable identities

Exactly one scanner child was executed, with soft/hard `RLIMIT_AS = 402653184` bytes (384 MiB), a 15-second wall timeout, and no concurrent scanner child:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDupNestedConflict/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDupNestedConflict/root
```

Observed elapsed time: approximately **0.03384 seconds**. Exit: **2**. No timeout or launch error. Full stdout (240 bytes, including the final newline):

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

Stderr: empty (0 bytes).

All five hashes matched their fixed/provenance identities both immediately before and after the scanner invocation; **no drift**:

| Artifact | SHA-256 before = after |
| --- | --- |
| Selected audit tool | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| Audit expected file | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| Case bundle | `4b2cea193fed358f1a753ac84856df74a21e0ce2757cff77d485381bf93173d0` |
| Raw snapshot | `601e5405103f9a2af80498cf37be50b9e4435a9db4239f752cad9db8fb9171d2` |
| Original case proposal | `eac29afe762c735bd99abf4ce1040453100639c48d72990d17c922a37ee7e393` |

Stdout SHA-256: `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`.

Empty stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

The raw receipt, including the exact command/caps, full stdout/stderr, byte-preserving base64, raw snapshot, independent derivation, parsed observation, and before/after digests, is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC214/result.json`.

## Relevant boundaries, residual risk, and verification gaps

- **Row/line grain:** there are zero finding rows and one file-counter object. No incident-line projection or row deduplication is relevant or credited. Duplicate counters cannot be normalized into a valid actual count.
- **Signed/bool/nonfinite counts:** this case contains only literal nonnegative integers in count positions and an exact bool for `clean`; it does not exercise negative, bool-as-int, or nonfinite rejection. The duplicate key is the defect in the input.
- **Paths and size:** the bundle is 217 bytes and snapshot 83 bytes, both regular files; metadata inspection found no symlink component in their ancestor chains. `snapshot.json` is an ordinary relative name. These are not boundary or symlink attack results; no general path/size safety claim follows.
- **Digest-before-decode:** matching raw digest and candidate source ordering support the correct branch selection. No separate tracing/instrumentation was performed. Runtime output exposes only the generic error type `Invalid`; the exact duplicate-key throw-site is supported by the raw bytes and static call-chain reasoning, not separately observed instrumentation.
- **LSP gap:** `read xd://lsp` returned `No such tool`; the LSP device is not mounted. Status, semantic references, definitions, and diagnostics were therefore unavailable. The call-chain/diff review above is manual literal source inspection, not semantic-server proof; no empty cold-index result was treated as absence.
- **Historical/authority boundary:** actual markerless r19 remains code 2 under `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/guard-clarifications.md:9`. No r19 run, derived 5/1-line or 10/1-row input, or all-observed inflation counterfactual was measured here. Prior r19/r20/r21 rejected-harmed receipts and streak are unchanged. The output's limited artifact-only authority is accurate for this observation; no semantic precision, mutant kill, admission, or closure is claimed.

Only this assigned report and its assigned raw receipt were written. Production, fixture, expectation, proposal, registry, and shared documentation bytes were not edited. No remaining actionable finding is identified within the assigned single-case scope.
