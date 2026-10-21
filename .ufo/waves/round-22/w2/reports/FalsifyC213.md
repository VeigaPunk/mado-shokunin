# FalsifyC213 — C2 AuditRawDupMetadataSame

## Findings by severity

No actionable implementation defect found in this fixed case. **Observed match:** exit `2`, JSON `code: 2`, `result: could-not-evaluate`, exactly `['evidence_audit_input_invalid']`. This is an invalid-input rejection, **not** a clean result, a contradicted-assertion/failed-1 result, semantic-precision evidence, or admission.

Axes: strict duplicate-key rejection; digest-before-decode and byte identity; count/verdict honesty; bounded execution and truthful authority.

## Independent semantic verdict

Derived before invoking the candidate, from the fixed raw bytes, declared counts, and canonical schema—not an old classifier output:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDupMetadataSame/root/snapshot.json:1` is 108 bytes and contains `"meta":{"tool":"fixture","tool":"fixture"}`. The repeated key is nested inside extra metadata, and both values are identical. A separate standard-library parse retaining every object pair confirmed both occurrences; no fixture code was executed.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-clarifications.md:6-9` requires hashing bounded snapshot bytes before decoding and rejects duplicate keys **anywhere**, despite permitting ignored extra metadata. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-contract.json:5-8` independently specifies duplicate-key invalidity and code 2 for invalid input. Equal duplicate values do not create an exception.
- The snapshot digest equals the bundle's declared digest. The bundle at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDupMetadataSame/bundle.json:2-10` declares exact integer zero for total/observed/lead/errors and exact boolean `clean: true`. The raw normative projection has **zero finding rows and one file row**, with both error counters zero. Those figures explain why silently ignoring metadata duplicates would be a false clean, but are not validated audit counts: strict parsing must fail first. No source-line or incident-line counting is involved.
- Therefore the independently derived verdict is **2 / could-not-evaluate / evidence_audit_input_invalid**. The selected expected entry and `original_expected` agree; `normalizations` is empty. Its fixed proposal provenance matches the sealed digest below. No expectation was changed.

## Actual diff and relevant candidate path

The delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5` changes `relative` to accept an optional `allow_backslash=False` and enables that exception only for fixture inventory filenames. In `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:80-105,185-187`, the snapshot API's `rooted` caller still uses the rejecting default. This case uses ordinary `snapshot.json`, so the new inventory allowance is not exercised.

The canonical check path is `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:267-286` (`main`), `:165-169` (`evaluate`), and `:121-131` (`check`). `check` hashes the exact bounded snapshot bytes before calling `parse`. At `:29-35,51-53`, the object-pairs hook rejects a key already present without comparing its values or limiting checks to normative fields. `Invalid` subclasses `ValueError` at `:25-26`; `evaluate` converts it to the sole invalid-input ID and code 2. Count comparison at `:132-162` is unreachable for this snapshot. The observable result contains no invented `actual_counts` or execution truth.

LSP unavailable: requesting `xd://lsp` returned `No such tool: xd://lsp`; status, references, definitions, and diagnostics could not be obtained. Scoped literal caller inspection and source reasoning are fallback evidence, not semantic-reference or diagnostics proof. No empty cold result was treated as absence.

## Authorized execution and identities

Exactly one scanner child ran, with `RLIMIT_AS` soft/hard **402653184 bytes (384 MiB)** and a **15-second wall timeout**:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDupMetadataSame/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawDupMetadataSame/root
```

Exit: **2**. Elapsed: **0.032658761 seconds**, no timeout. Full stdout (with terminating newline):

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

Full stderr: empty. Stdout SHA-256: `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`; stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

All identities matched before and after; **no drift**:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Selected audit tool | 11245 | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| Audit expected manifest | 228091 | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| Fixed bundle | 217 | `66df48fc94121ffb03a8a67d025d442c63eab60b2e21026662d1d7a9e14cc0d9` |
| Fixed snapshot | 108 | `e0bc05fdfce0e06392ff364a8d3e49e17177decbff9e44f7df0e9648030451cd` |
| Frozen proposal copy | 1018 | `68ccc8e11ffe6963d0cda0f035ec6615f32c41661435c6f1c556ba0087298dbe` |

The raw receipt at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC213/result.json` records all absolute input paths, pre/post digests, raw snapshot bytes, independently retained duplicate pairs, exact argv, caps, exit, and full stdout/stderr in text and base64. Byte identity is not authenticated authorship.

## Residual risk and verification gaps

- This is one fixed-case author-lane advisory observation, not saturation, general parser correctness, non-author admission, promotion, or C1 semantic precision. No alternate audit runtime or rerouted tool was used.
- Only identical duplicate metadata rejection was attacked. The selected paths have no symlink components and the inputs are far below 2 MiB; rejection boundaries, digest mismatch, signed/bool/nonfinite counters, and resource saturation were not dynamically tested. Digest-before-decode is supported by source order and matching bytes, not a separate mismatch experiment.
- The proposal's language about weaker mutants is not an observed kill: no mutant was applied or run. No additional source-shaped probe, full 46-case selftest, measurement driver, old tool, build, lint, formatter, host/live probe, or install/update was performed.
- No actual r19 artifact was rerun or reinterpreted. The historical boundary in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/guard-clarifications.md:9` remains: markerless actual r19 is code 2; 5/1 incident-line projections and 10/1 markerful-row populations require explicit derivation. This case makes no all-observed-inflation claim about actual r19.

No truth/expectation/output contradiction was found for this case. Production, fixture, expected, proposal, and other shared source files were not modified; writes are confined to this assigned report and receipt.
