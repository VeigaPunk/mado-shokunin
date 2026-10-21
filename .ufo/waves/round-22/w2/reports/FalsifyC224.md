# FalsifyC224 — C2 AuditRawPathEmpty

## Findings, by severity

No actionable candidate defect found in this assigned case. The sole authorized check returned **exit 2 / could-not-evaluate / `['evidence_audit_input_invalid']`**, matching both the frozen expectation and the independently derived semantic verdict. This is a controlled refusal, **not clean 0 and not failed 1**.

This author-lane advisory result does not admit round22, establish semantic precision, retire earlier reds, or alter planner/integration authority.

## Axes and evidence identity

Axes: (1) strict empty-path refusal and honest error classification; (2) raw-byte identity and finding-row/count arithmetic; (3) bounded execution without production mutation; (4) artifact-only authority with explicit limits.

Assigned revision: `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. Identity was pinned to the assigned selected-tool digest, not inferred from a different runtime or a whole-revision diff.

The following SHA-256 values were measured before and after the single check, with no observed drift:

| Absolute artifact | SHA-256 | Size where measured |
| --- | --- | --- |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py` | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` | — |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json` | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` | — |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathEmpty/bundle.json` | `f1e84ca08940bbd68d6e734a7ac72377ae14fa4d8d410d6277d83c3fd003a101` | 204 bytes |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathEmpty/root/snapshot.json` | `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c` | 104 bytes |

Only the fixed case record/provenance was targeted in the expected manifest. Its record at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json:1115-1158` preserves original and normalized expectation 2 with this exact finding ID, with `normalizations: []`. The proposal hash `04bbf06f0f3ccacf77aa9ac281841db8635a0681221458e4be2bcbaab1e08214` is declared provenance, not independently authenticated proposal chronology or an independently rehashed proposal file.

## Independent semantic derivation

The derivation was recorded before execution in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC224/preflight.json`; no old classifier output was consulted.

1. The raw bundle at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathEmpty/bundle.json:2-10` declares integer `total=observed=lead=errors=0`, Boolean `clean=true`, a syntactically valid SHA-256, and **`snapshot: ""`**. A zero-length path cannot identify a relative snapshot file. Count consistency cannot repair that input defect.
2. Independently reading the sibling snapshot gives one file row, zero finding rows, zero observed rows, zero lead rows, and error sum `0 + 0 = 0`. Its raw-byte digest matches the bundle's declared digest. This file is nevertheless **unaddressed by the bundle**; substituting its filename would change the fixed case and was not done. Counts are finding-row counts, not incident-line counts.
3. The canonical check in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:121-127` parses the bounded bundle, obtains the empty string, validates the digest syntax, and calls `rooted(root_path(root), name)`. At `:97-105`, `rooted` invokes `relative(name)` before any snapshot file read. At `:80-85`, `not name` rejects the empty string with `Invalid('invalid relative path')`. Filesystem ancestry inspection showed directory ancestors without symlinks and regular bundle/sibling snapshot files, so no observed competing path-type defect was needed to derive this refusal.
4. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:25-26,165-169` makes `Invalid` a `ValueError` and converts that exception to exactly code 2 with `evidence_audit_input_invalid`. The canonical CLI at `:267-286` selects this check/evaluate path, prints its JSON, and returns the same code. No classifier or second scanner runtime is invoked by this check path.

Therefore the independently required outcome is **2 / could-not-evaluate**, irrespective of the valid zero-count arithmetic in the unaddressed sibling snapshot.

## Observed single bounded execution

The only scanner command executed was:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathEmpty/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathEmpty/root
```

The child used `RLIMIT_AS` soft=hard=402653184 bytes (384 MiB) and a 15-second `subprocess.run` timeout, with captured stdout/stderr and no shell. Exactly one scanner child ran; it completed in approximately 0.0303 seconds, without timeout, with exit **2**, 240 stdout bytes, and zero stderr bytes. This is a bounded observation, not a saturation or asymptotic-performance claim.

Full stdout, including its final newline, and full empty stderr are retained losslessly in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC224/result.json`, together with exact argv, caps, stream digests, base64 stream bytes, artifact digests, and the independent verdict. Parsed stdout was:

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

Stdout SHA-256: `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`. Stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

**Observed match: yes. Independent semantic verdict: correct controlled refusal for this fixed input.**

## Residual risk and verification gaps

- **Provenance caveat / non-discrimination:** the rationale at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json:1151` discusses a mutant normalizing the empty path to the root directory and crashing or otherwise differing. That is not an exercised kill. A hypothetical fault returning `Path('.')` for an empty name in `relative` would still encounter the `rooted` regular-file check at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:103-104`; even a later `IsADirectoryError` is an `OSError` caught at `:168-169`. Thus this output alone does not distinguish the intended early refusal from downstream controlled refusal. No mutant was created, executed, or called killed; the present source does contain the proper early guard.
- **Digest-before-decode:** `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:127-131` visibly hashes snapshot bytes before decoding on a valid path. This empty-path run never reaches that step. The separately measured sibling digest is not evidence that this scanner run validated a snapshot.
- Both input artifacts are far below the 2 MiB limit. No size-boundary, symlink race, malformed encoding, signed/bool/nonfinite count, duplicate-key, or alternate-path probe was authorized or run. Numeric claims here are ordinary nonnegative integer zeros, with a separate Boolean clean field. No broadened guard-coverage claim follows.
- LSP was unavailable: reading `xd://lsp` returned `No such tool`, so status/references/definition/diagnostics could not be obtained. Bounded source reads and literal expected-record location were the fallback; neither is presented as semantic proof of caller absence. Review is limited to the fixed case's canonical check path, not every caller or the whole diff.
- No whole46-case selftest, measurement driver, full corpus, generic smoke, old-tool rerun, source-shaped probe, fixture execution, production edit, install/update, or background job was performed. The only writes were this assigned report and this seat's raw receipt directory.
- Historical boundary remains unchanged: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/guard-clarifications.md:9` says actual markerless r19 is code 2; it is not failed 1 or clean 0. Derived 5/1 incident-line or 10/1 markerful-row populations require explicit derivation, and all-observed inflation examples would be new counterfactuals. This case neither remeasures those artifacts nor credits semantic precision or admission.

Report: .ufo/waves/round-22/w2/reports/FalsifyC224.md
