# FalsifyC220 — C2 AuditRawPathAbsolute

Axes: strict input/path soundness; raw-byte/digest and row/count fidelity; honest verdict/authority; bounded reproducibility and immutability.

## Findings, severity ordered

### P2 — C2-ABS-1: relocated fixture does not isolate the absolute-path guard it claims to attack

The frozen rationale says the absolute snapshot points **inside the supplied ROOT**, and that removing the absolute-path check makes this case return `0/evidence_audit_clean`. The delivered bytes contradict that premise:

- Bundle `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathAbsolute/bundle.json:10` embeds `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/.audit-assemble-15l8absm/fixtures/cases/AuditRawPathAbsolute/root/snapshot.json`.
- The assigned `--root` is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathAbsolute/root`. The embedded staging pathname is outside this root, regardless of whether the staging target exists.
- The contradictory rationale and declared root are retained at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json:942,975-978`; original proposal intent is visible at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/inputs/proposals/AuditRawPathAbsolute.json:6,10`.
- The source materializes `{{ROOT_ABS}}` using the staging root at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/assemble.py:351`; it creates a temporary staging tree at lines845-846 and publishes it with `os.rename(stage, OUT)` at line952. The embedded pathname remains the pre-publication path in the actual frozen bundle.

**Impact:** [INFERENCE] removing only `PurePosixPath(name).is_absolute()` at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:82` still cannot produce the rationale's clean result: `rooted()` retains the missing-or-escaping-input rejection at lines103-104. A missing staging target fails `is_file()`; an existing target at that outside-root pathname fails the containment guard. Consequently, the observed expected match is valid but is not evidence that this fixture independently detects loss of the absolute-only guard.

No mutant was created or executed; no kill or survival is claimed. This is an artifact evidence-strength defect, **not a demonstrated production CLI verdict defect**. Recommendation to L1: preserve the frozen truth and explicitly disposition this relocation contradiction before crediting the claimed discriminating power. No fixture, expectation or source was changed here.

## Residual risk and verification gaps

- This was one small case, not path-boundary saturation. No symlink adversary, 2MiB edge, signed/bool/nonfinite count variant, duplicate-row variant, digest mismatch or additional source-shaped probe was run.
- `namei -l` showed no symlink component in the assigned bundle/current snapshot ancestry; `stat` showed regular files of353B/104B. The embedded staging target's existence was deliberately not probed; the finding does not depend on it.
- `xd://lsp` returned `No such tool`; no server/status/references/definition/diagnostics interface was available. Relevant literal searches and direct source inspection were used as fallback, not represented as LSP semantic proof.
- The delivered commit diff for this tool was inspected read-only. Its changes add `allow_backslash=False` to `relative()` and opt in only from fixture inventory; `--check` still calls the default through `rooted()` at lines97-105. This assigned case exercises the unchanged absolute rejection, not the inventory exception.
- No full selftest, measurement driver, build, lint, formatter, generic smoke, alternate scanner/runtime, old classifier, mutation run or historical-r19 rerun occurred. No semantic precision, admission, saturation, clearance or closure credit follows. The r19/r20/r21 rejected-harmed receipts/streak remain untouched.

## Independent semantic derivation

This derivation used raw case bytes and the strict contract, not old classifier output.

1. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-contract.json:5-8` requires a relative snapshot path and defines invalid/unavailable input as code2. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-clarifications.md:5` explicitly rejects absolute paths even if they would name valid data inside ROOT.
2. The raw bundle declares exact integer `total=observed=lead=errors=0` and exact boolean `clean=true`; no negative, bool-as-count or nonfinite counter occurs.
3. The separately stored snapshot at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathAbsolute/root/snapshot.json:2-8` has zero finding rows and one file row with `eval_unparsed=unparsed_spawns=0`. Its population is nonempty, row-based totals are0/0/0, and summed errors are0. No row/line projection or observed/lead relabeling is involved. These data would not independently contradict the clean/count claim, but that does not cure an invalid pathname.
4. Its104 raw bytes hash to `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c`, equal to the bundle's declared digest. This was an independent parent-side digest observation, **not** a digest verification performed by the scanner on this case.
5. The canonical candidate path is `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:121-127` → `rooted():97-105` → `relative():80-85`. The absolute pathname raises `Invalid` before snapshot read/hash/decode or count comparison. `evaluate():165-169` maps that exception to `2/[evidence_audit_input_invalid]`; `main():274-282` prints that JSON and returns its code. For a valid path, lines128-131 place snapshot digest comparison before snapshot decoding; this case does not dynamically test that later ordering.

**Independent verdict:** `2`, exactly `['evidence_audit_input_invalid']`, meaning **could-not-evaluate**, never clean0 or contradicted-assertions failed1. The current frozen expected code/IDs are semantically correct despite the separate rationale/coverage defect.

No r19 count derivation was performed. Per the authoritative guard clarification, actual markerless r19 remains code2;5/1 incident-line and10/1 finding-row representations require explicit derivation and cannot be substituted for it. No all-observed counterfactual was attributed to actual r19.

## Single authorized observation

Exactly one scanner child ran, with `RLIMIT_AS=402653184` bytes and a15s wall timeout:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathAbsolute/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathAbsolute/root
```

Exit **2**; elapsed approximately0.031s; no timeout; stderr empty. Full stdout, including its newline, is retained in the raw receipt:

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

**Observed match:** yes, both frozen expected code/IDs and independently derived code/IDs. No current CLI mismatch was found. The semantic judgment remains scoped to correct refusal of this input, not to the invalid rationale's claimed mutation sensitivity.

## Identity and raw evidence

All following SHA256 values were identical before and after the single scanner invocation:

| Artifact | SHA256 |
| --- | --- |
| Selected C2 tool | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| Audit expected manifest | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| Assigned bundle | `39de4c960d323dc09058eda6a8bab8a118d65b1c78a8faddf668eb942c42df4c` |
| Separately stored snapshot | `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c` |
| Frozen case proposal | `dcbcee2de990f63e81413482357a2c7d0f07809e5487338580fad8e12372c4bb` |

The selected tool and manifest match their fixed assignment identities. Stdout is240B, SHA256 `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`; empty stderr SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Full streams, base64 bytes, caps, command, timestamp, before/after digests and the retained contradiction are in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC220/result.json`.

Only this assigned report and receipt were written. No installs or updates. This is an author-lane advisory recommendation, not non-author admission.
