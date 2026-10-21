# FalsifyC222 — C2 AuditRawPathDot

## Findings, by severity

**No actionable delivered-code defect identified in this fixed case.** The sole authorized candidate invocation exited **2**, emitted exactly `finding_ids=["evidence_audit_input_invalid"]`, and classified the result as **could-not-evaluate**. This matches both the selected frozen expectation and the independent contract-based verdict below. It is neither clean/0 nor contradicted-assertion/1. This is an author-lane advisory observation, not admission or semantic-precision credit.

## Axes

1. Independent raw-path and strict-schema verdict correctness.
2. Frozen candidate/input/expectation identity and provenance.
3. Single-child, resource-bounded reproducibility.
4. Honest result classification, evidence grain, and authority limits.

## Independent derivation

The oracle is the frozen contract plus the selected raw input, not an old classifier result:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-clarifications.md:5` explicitly rejects dot/dotdot path components, even when filesystem resolution would stay inside the explicit root. Lines 7–10 separately define nonempty file population, exact nonnegative integer counters, row counting, and verdict distinctions.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathDot/bundle.json` contains the literal snapshot name `./snapshot.json`. Its raw slash-separated components are `.` and `snapshot.json`. The first component is forbidden; normalization must not erase it before validation.
- The existing snapshot at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathDot/root/snapshot.json` contains zero finding rows and one file member with `eval_unparsed=0` and `unparsed_spawns=0`. Independently counted totals are **0 total / 0 observed / 0 lead / 0 errors**, with a nonempty file population. The bundle declares the same exact integer counts and an exact Boolean `clean:true`. No signed, Boolean-as-count, nonfinite-number, missing-marker, or row/line ambiguity is present in these bytes.
- The snapshot's actual byte SHA-256 equals the bundle's declared lowercase SHA-256. Bundle and snapshot are regular files of 219 and 104 bytes; the root and every relevant ancestor were observed as directories, not symlinks. The valid contained file and consistent arithmetic do **not** legalize its forbidden raw API name.

Therefore the independently derived verdict, established before the candidate invocation, is **2 / `["evidence_audit_input_invalid"]`**. Code 1 would misdescribe an invalid input as an evaluated arithmetic contradiction; code 0 would incorrectly accept an invalid raw path.

The selected record in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json:1027-1070` retains that exact original expectation and `normalizations:[]`. Its original proposal and frozen provenance copy have identical bytes by SHA-256. No expectation was changed.

## Actual diff and canonical logic

Reviewed `git show --format=fuller --no-ext-diff 71228fd582d6d9338d7916cc64e69bd4c2e928b5 -- tools/mado-evidence-audit.py` read-only. The delivered change adds `allow_backslash=False` to `relative` and passes `True` only for inventory filenames. It does not relax dot-component validation.

Manual caller/definition review of `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py` establishes:

- **Lines 80–85:** `relative` checks raw `name.split('/')` for empty, dot, and dotdot components **before** constructing a `Path`. This remains unconditional regardless of `allow_backslash`.
- **Lines 97–105, 121–127:** the snapshot API goes through `rooted(root_path(root), name)` and calls `relative(name)` without the inventory exception. Here the raw dot rejection precedes snapshot reading.
- **Lines 172–209:** only the inventory caller opts into literal POSIX backslash filenames; it still uses the unchanged raw dot guard. **Line 238:** the selftest's case-root caller also retains the default policy. The selftest was not executed.
- **Lines 25–26, 165–169:** `Invalid` is a `ValueError`, and the canonical `evaluate` handler maps it to code 2 and the required stable ID. **Lines 267–286:** the CLI prints that result and returns its code.
- **Lines 127–131:** after a valid path, snapshot bytes would be bounded and hashed before JSON parsing. This case stops earlier, so it does not dynamically test digest-before-decode.

The CLI gives only `error:"Invalid"`, not a branch-specific trace. Attribution to the dot guard follows from the inspected source and the otherwise valid preceding bytes/path metadata; it is not claimed as runtime instrumentation.

**Unexecuted fault recipe [INFERENCE]:** replace `name.split('/')` in the component guard with `PurePosixPath(name).parts`. That normalization discards this leading dot before inspection. Given this otherwise valid, digest-matching, zero-row receipt, the remaining canonical checks predict code 0 / `evidence_audit_clean`. This is a concrete sensitivity hypothesis only: no mutant was written, run, or claimed killed.

## Sole authorized measurement

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathDot/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathDot/root
```

One scanner child, with inherited soft/hard `RLIMIT_AS=402653184` bytes (384 MiB), soft/hard CPU limit 15 seconds, and `subprocess.run(timeout=15)` wall cap. Observed elapsed time: 31,683,012 ns. No timeout. Exit: **2**. Stderr: empty. Full stdout, including its trailing newline, is retained in the raw receipt:

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

Stdout: 240 bytes, SHA-256 `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`.
Stderr: 0 bytes, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

### Frozen identities

All following digests were observed both before and after the sole scanner invocation; no drift was observed:

| Artifact | SHA-256 |
| --- | --- |
| Selected C2 tool | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| Sealed audit expectations | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| Selected bundle | `a960a81994ecad9f5f5c862de49acbeb7e8e5b9613e99c894ec11532dc7d1423` |
| Selected snapshot | `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c` |
| Original proposal and frozen provenance copy, each | `d1b6a91d668d51558854e624fba5c0728074c832a4c5d34fce7a0a0eba087832` |

The tool and expectation identities equal the fixed assignment identities. Absolute artifact paths, pre/post digests, full stdout/stderr, Base64 byte preservation, limits, and interpretation are in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC222/result.json`.

## Residual risk and verification gaps

- **LSP unavailable:** `read xd://lsp` returned `No such tool`; there was no available status/reference/definition/diagnostics server to start or warm. Source and caller review is manual. Literal searches located definitions/records only and are not presented as semantic proof.
- **Read-scope deviation:** an initial substring JSON query also returned the adjacent `AuditRawPathDotDotInternal` metadata record; a non-raw line-range response later exposed neighboring context. Exact-ID selection was subsequently used. No neighboring case was executed or used to derive this verdict.
- This is one fixed lexical dot-path check, not a 46-case result or saturation claim. It does not establish handling at the 2 MiB boundary, symlink races, nonfinite/signed/Boolean counter attacks, row-versus-line deduplication on nonempty findings, or malformed snapshot digest/decode ordering. Those behaviors were not probed.
- No old tool, whole-corpus selftest, measurement driver, generic smoke, build, lint, formatter, fixture code, alternate runtime, or mutation tester was executed. No production, fixture, expected, source, registry, or shared documentation file was changed. No tools were installed or updated. Only this seat's receipt and report were written.
- No r19 artifact was measured. The limitation in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/guard-clarifications.md:9` remains: original markerless r19 is code 2, not clean/0 or failed/1; any 5/1 line or 10/1 row representation requires its stated derivation. This case supplies no new historical count or all-observed-inflation claim.
- No runtime rerouting, resume-continuity, semantic precision, historical rehabilitation, round admission, or promotion conclusion follows. The observed authority text expressly disclaims those conclusions. Prior red receipts and rejection streak remain unchanged.
