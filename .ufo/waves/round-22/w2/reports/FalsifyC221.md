# FalsifyC221 — C2 AuditRawPathBackslash

## Findings by severity

**No actionable production defect found in this fixed case.** The single observed run agrees with both the independent raw-artifact derivation and the frozen expectation: exit **2**, result **could-not-evaluate**, IDs **`["evidence_audit_input_invalid"]`**. This is rejection of an invalid snapshot API path, not a clean artifact result and not an assertion contradiction (code 1).

This is an author-lane advisory result, not non-author admission. No semantic precision, authentication, promotion, closure, or saturation credit is claimed.

## Axes and scope

1. Snapshot API path rejection versus literal POSIX inventory filename identity.
2. Raw-byte digest, strict schema, and declared row/error arithmetic integrity.
3. One bounded canonical runtime, stable identities, and truthful uncertainty/authority.

Reviewed the audit-tool diff of delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, the relevant source paths, and only the `AuditRawPathBackslash` expected/provenance entry. Executed one assigned `--check` child; no additional case, mutant, source-shaped probe, measurement driver, or selftest was executed. Production, fixture, expectation, and source files were not edited.

## Independent derivation, before the scanner run

The normative rejection is explicit in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-clarifications.md:5`: snapshot API paths containing backslashes are invalid even where POSIX could open that literal filename. Lines 6–10 separately establish digest-before-snapshot-decode, strict counters, actual-row arithmetic, and the 0/1/2 result boundary.

Raw bundle evidence is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathBackslash/bundle.json:2-10`. Its JSON string `"sub\\snapshot.json"` decodes to one literal U+005C in the relative name, not a slash or a directory boundary. The actual basename bytes are hex `7375625c736e617073686f742e6a736f6e`.

Independent byte/filesystem inspection established:

- The root contains the regular, nonsymlink literal-backslash file at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathBackslash/root/sub\snapshot.json`; the nested slash-separated variant does not exist. No root ancestor examined was a symlink.
- The bundle is 222 bytes and the snapshot is 104 bytes, both below 2 MiB. Snapshot SHA-256 is `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c`, exactly the lowercase-hex digest declared in the bundle.
- The raw snapshot has one file row, zero finding rows, and exact integer zero values for both error counters. The claim has exact nonnegative integer zero counts for total/observed/lead/errors and boolean `clean: true`. Duplicate-key-rejecting parsing found no duplicate keys or nonfinite tokens. No signed-negative, boolean-counter, or nonfinite-count counterexample is present here.
- Therefore the hypothetical arithmetic, **if the API path were valid**, would be total/observed/lead/errors = **0/0/0/0** with one file row. That conditional arithmetic does not override the invalid path and is not the actual scanner result. No finding-line deduplication or row/line reinterpretation is involved in this empty-findings case.

Thus the independently derived outcome is **2 / could-not-evaluate / `evidence_audit_input_invalid`**, without consulting old classifier output. The selected frozen entry has that same expected outcome, `normalizations: []`, and unchanged `original_expected`. Its proposal digest matches the selected provenance at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/audit-proposals/AuditRawPathBackslash.json`.

## Candidate logic and actual delivered diff

All source references below are in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py`.

- Delivered diff: `relative` gains `allow_backslash=False` at lines 80–84; only fixture inventory explicitly passes `allow_backslash=True` at lines 185–187. This allows inventory to name the literal POSIX test file without weakening the snapshot API.
- Canonical assigned run: `main` selects `evaluate` for `--check` at lines 274–275; `evaluate` calls `check` at lines 165–169; `check` passes the supplied snapshot name into `rooted` at line 127; `rooted` invokes `relative(name)` with its default prohibition at line 99. The U+005C therefore raises `Invalid` at line 84. The handler at lines 168–169 produces code 2 with the required ID; lines 281–282 print that result and return its code.
- Snapshot hashing precedes snapshot parsing at lines 127–131 **when path validation succeeds**. In this case the invalid path is rejected before snapshot bytes are read by that expression, so the run does not exercise a tampered-digest or decode-order branch. Independent snapshot hashing above establishes the fixture bytes, not scanner execution of that branch.
- Textual caller inspection found the explicit inventory allowance and the default-rejecting snapshot/root paths. The inventory caller is the selftest path at lines 225–226 and 257, not the assigned `--check` path. That selftest was read, not executed.
- The authority string at line 22 and returned at lines 116–118 explicitly limits the tool to artifact arithmetic/evidence labels. No C1 classifier or other runtime was invoked by the assigned invalid-path branch.

## One bounded observation

Exact child argv:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathBackslash/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathBackslash/root
```

One direct child, no shell; `RLIMIT_AS` soft/hard = **402653184 bytes (384 MiB)** and wall timeout = **15 seconds**. Observed elapsed time was **0.032373332 seconds**; no timeout. Exit code **2**; stderr empty.

Full stdout (including a terminating newline in the raw receipt):

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

The full 240 stdout bytes have SHA-256 `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`; the zero stderr bytes have SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

### Identity pins

These digests were checked immediately before and after the child and did not drift:

| Artifact | SHA-256 |
| --- | --- |
| Selected C2 tool | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| Audit expected manifest | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| Assigned bundle | `0e154c84e54944f1367580056f233cfd4d65d7b146fbfc85161b06bb50f0e1f2` |
| Literal-backslash snapshot | `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c` |
| Selected proposal | `488295d5cce1de5551ae04e1fabf6c4bf57b63435f3d355a985f5ae3395ba0c1` |

Raw receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC221/result.json`. It contains full stdout/stderr, their digests, before/after identities, raw bundle/snapshot bytes in base64, the selected provenance, resource limits, and separate independent/expected/observed results. `observed_match` is true.

## Residual risk and verification gaps

- This one invalid-path observation neither proves all path/symlink/size boundaries nor dynamically tests strict counter, digest-mismatch, finding-evidence, or successful-arithmetic paths. Their reachable source behavior was distinguished from what this invocation actually exercised.
- `xd://lsp` is not mounted; its discovery request returned `No such tool`. LSP status/references/definition/diagnostics were unavailable. Caller/definition inspection used source reads and literal fallback search, not semantic-reference proof; no diagnostics pass is claimed.
- The `read` tool displayed the literal-backslash snapshot filename as a slash-separated path in its header. The raw filename bytes and snapshot identity were independently obtained using filesystem byte reads; this display issue was reported through `xd://report_issue` and does not change the artifact verdict.
- No builds, linters, formatters, generic smokes, full corpus, 46-case selftest, measurement driver, old-tool rerun, live-host probe, fixture payload execution, or mutant execution occurred. No fault was credited as killed. No tools were installed or updated.
- The historical boundary remains the stipulated one in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/guard-clarifications.md:9`: actual markerless r19 is code 2, not failed 1 or clean 0. It was not remeasured here. No derived 5/1-line or 10/1-row projection, or new all-observed counterfactual, was measured or substituted for it.

**Scoped recommendation:** retain this fixed case as matching evidence of invalid-backslash-path refusal only; no expectation change and no broader admission inference.
