# FalsifyC206 — C2 AuditNegative

## Findings, by severity

**No actionable defect or expectation contradiction found in this fixed case.** Observed exit/code `2`, result `could-not-evaluate`, and exactly `['evidence_audit_input_invalid']` match both the independent schema derivation and the unchanged frozen expectation. This is a bounded artifact-input rejection result, not scanner semantic precision, clearance, or admission.

## Axes

1. Exact-byte identity and frozen provenance.
2. Per-counter strict schema and resistance to signed-count cancellation.
3. Honest tri-state verdict and artifact-only authority.
4. Single-child resource bounds and read-only source scope.

## Independent semantic verdict

The derivation was recorded before the sole candidate execution in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC206/derivation.json`.

- Raw snapshot: one `files` member with `eval_unparsed: -1` and `unparsed_spawns: 1`; `findings: []`. Evidence: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditNegative/root/snapshot.json:1-9`.
- Declared claim: `total=0`, `observed=0`, `lead=0`, `errors=0`, `clean=true`. The bundle names `snapshot.json` and declares the matching raw-byte digest. Evidence: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditNegative/bundle.json:1-11`.
- The strict contract requires **each** file counter to be a nonnegative exact integer; negative counters are invalid, and invalid input is code 2. Findings may legitimately be empty and the file population is nonempty here. Evidence: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-contract.json:5-8` and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-clarifications.md:7-9`.
- Therefore `-1` invalidates the input **before aggregation or claim comparison**. Unchecked `-1 + 1 = 0` is only the cancellation counterfactual; it is not a valid actual error count. There is no trustworthy count against which to decide assertion-failure code 1, and no basis for clean code 0. The required independent verdict is code 2 with only `evidence_audit_input_invalid`.
- The positive counter is declared artifact data, not independently demonstrated execution truth. No old classifier output was used to derive this verdict.

The fixed case's provenance copy has SHA-256 `80f4cdd1563d335ed652c0114bea1d6a787547a7a4462d3b354f1864c15fbd2b`, matching its frozen case metadata. Its original expected verdict is also code 2 with the same ID; the selected expected entry has `normalizations: []`. Source: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/inputs/proposals/AuditNegative.json:3-11` and the `AuditNegative` entry in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json`.

## Relevant canonical logic and delivered diff

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:67-77`: `require` uses exact type identity, and `count` raises `Invalid` on a negative integer. `Invalid` subclasses `ValueError` at lines 25-26.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:127-131`: bounded snapshot bytes are hashed and compared before snapshot JSON decoding. The actual digest matches, so this case is not `snapshot_tampered`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:132-149`: the finding grain is JSON rows (`len(findings)`), not incident lines. The nonempty file population is required. At line 146, the left operand `count(row, 'eval_unparsed')` raises before the second counter, the addition, or claim comparison can complete.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:165-169`: `evaluate` catches that `Invalid` through `ValueError` and returns code 2 with exactly the input-invalid ID.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:267-286`: the authorized `--check` path calls `evaluate`, prints its JSON once, and exits using `output['code']`. No selftest path was selected.

Inspected the actual selected-file delta of delivered commit `71228fd582d6d9338d7916cc64e69bd4c2e928b5`: it adds `allow_backslash=False` to `relative` and explicitly enables that option only for fixture inventory names. The canonical `--check` snapshot route still goes through `rooted` → `relative(name)` with the restrictive default (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:80-105,185-187`). This case has the ordinary relative path `snapshot.json`; the altered inventory branch is not exercised. No claim is made about unexecuted selftest cases.

LSP availability was checked first by requesting `xd://lsp`; the device is not mounted (`No such tool`). Status, references, definition, and diagnostics were consequently unavailable. Bounded source reads and the actual commit diff are the fallback evidence; no text search is represented as semantic-LSP proof.

## Sole bounded execution and identities

Executed exactly once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditNegative/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditNegative/root
```

The child had soft/hard `RLIMIT_AS=402653184` bytes (384 MiB) and a 15-second wall timeout. Observed elapsed time was `0.03318456100532785` seconds; no timeout occurred. Exit was `2`; stderr was empty. Full 240-byte stdout, full stderr, base64 encodings, stream digests, exact command, caps, and input identity records are saved in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC206/result.json`.

Full stdout:

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

Before/after SHA-256 checks were identical for all five inputs below. The tool and expected hashes also match the assigned fixed identities; bundle, snapshot, and proposal hashes match the selected frozen metadata.

| Input | SHA-256, before = after |
| --- | --- |
| Selected audit tool | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| Frozen audit expected manifest | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| Bundle, 217 bytes | `d43d04e2fe84f6d7092acfbb748b63271db63f68ae2165eb5b4bbeb63cd80cfa` |
| Snapshot, 105 bytes | `5434a72fd22ac904ec9412a4192845909c925681683973df4761a37b40e22120` |
| Frozen proposal copy, 1397 bytes | `80f4cdd1563d335ed652c0114bea1d6a787547a7a4462d3b354f1864c15fbd2b` |

Stdout SHA-256: `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`. Empty stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Residual risk and verification gaps

- This case exercises rejection of the first signed per-file counter. It does not independently exercise the second counter's rejection, boolean/nonfinite counts, finding evidence markers, duplicate keys, claim mismatches, or the clean-claim branches; no saturation or complete schema-coverage claim follows.
- Its ordinary path and small matching-digest files are not path/symlink/size-boundary or malformed-byte adversarial probes. Digest-before-decode ordering is established by the canonical source, not by an extra runtime probe.
- One fixed tool identity and one scanner child were used; no alternate runtime, reroute, full 46-case selftest, measurement driver, source-shaped variant, old-tool replay, build/lint/format/smoke run, or live probe was performed. The cap is an enforced address-space ceiling, not a measured peak-memory or scaling result.
- This is not the actual r19 receipt. Markerless actual r19 remains code 2 under the strict schema. Any 5/1 incident-line or 10/1 finding-row projection requires its explicit derivation, and an all-observed inflation assertion would be a new counterfactual, not an original r19 claim. No such projection or historical remeasurement was performed here. The boundary remains as stated in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/guard-clarifications.md:5-9`.
- Matching hashes establish byte consistency with declared metadata, not authenticated chronology. No semantic precision or non-author admission is credited; prior red receipts and the rejection streak are unchanged. This author-lane advisory result does not exercise or authorize orchestration, resume continuity, integration, or promotion.

No production, fixture, expected, registry, or documentation source was modified. Only this assigned report and this seat's receipt directory were written. No tools were installed or updated.

Report: .ufo/waves/round-22/w2/reports/FalsifyC206.md
