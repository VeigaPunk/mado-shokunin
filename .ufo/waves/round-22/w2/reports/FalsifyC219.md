# FalsifyC219 — C2 AuditRawOversizedSnapshot

## Findings by severity

**No new actionable defect found in this assigned case.** The delivered candidate rejects the one-byte-oversized snapshot as **2 / could-not-evaluate**, with exactly `['evidence_audit_input_invalid']`. This is neither a clean result nor an evaluated assertion failure. The observed expectation match and the independently derived semantic verdict agree; no expectation/provenance contradiction was found for this case.

This is an author-lane advisory result, not non-author admission or integration authority. No semantic-precision, historical-repair, saturation, or admission credit follows.

## Axes and scope

1. Raw-byte size boundary and rejection precedence.
2. Artifact digest, declared-count, and strict-schema fidelity.
3. Truthful authority and preservation of uncertainty.
4. One reproducible capped measurement, without production mutation.

Reviewed delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, the fixed case's expectation/provenance, raw bundle/snapshot bytes, and relevant candidate source. No alternate case, new source-shaped probe, mutant, old classifier, selftest, measurement driver, build, lint, formatter, or generic smoke was run. No fixture code was executed.

## Independent derivation, recorded before scanner execution

- The bundle is 217 bytes, with SHA-256 `204064fed00f9c59cd578a3d32d6ed9bf67931045ef757149e26377e305c1c0a`. It declares snapshot `snapshot.json`, all four counts as integer zero, and `clean` as boolean true.
- The snapshot is a regular file with no symlink component in its absolute path. It contains **2,097,153 bytes**, exactly **one byte over** the 2,097,152-byte maximum. Its 65-byte JSON object is followed by 2,097,088 ASCII spaces. Trailing whitespace remains part of the bounded raw artifact.
- Independent strict JSON inspection found `findings: []` and one `files` row with integer `eval_unparsed: 0` and `unparsed_spawns: 0`. The declared counts match those rows if size is ignored; no boolean count substitution, negative count, duplicate key, or nonfinite value is present. This inspection is not an audit acceptance: the raw-byte limit has already been exceeded.
- The complete padded snapshot's SHA-256 is `d792253418b76a9be109a860da902797ad709f54e7ea364a9176de89e8904ecb`, equal to the bundle's declared digest. Thus a digest mismatch is not the reason for refusal.
- The canonical candidate logic establishes the decisive ordering: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:20,56-64` reads at most `MAX_BYTES + 1` and raises `Invalid` when the raw length exceeds the maximum. The snapshot `bounded(...)` call at lines 121-131 precedes snapshot hashing, digest comparison, and decoding. Lines 165-169 convert that exception into code 2 with `evidence_audit_input_invalid`. The later row/count assertion code at lines 132-162 is not reached. For an accepted-size snapshot, hashing precedes decoding; this oversized input is rejected before either operation.

**Independent semantic verdict:** this artifact cannot be evaluated under the bounded-input contract, even though its padded JSON and declared arithmetic are otherwise consistent. Therefore derive **code 2**, not `snapshot_tampered`, clean 0, or failed 1. This conclusion was fixed before running the candidate, not taken from an old classifier output.

## Fixed expectation and provenance

Only this case's expected/provenance entry was selected for substantive review: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json:895-938`. Its original and normalized expectations both specify code 2 and the same single finding ID; `normalizations` is empty. It binds the same bundle and snapshot digests measured above. Its proposal/source digest is `1b762b179fea657081f08ff663348dde869459c3968e3fb70b8bfa35124228f9`; the manifest declares a 1,081-byte source proposal.

The audit expected manifest hashes to the assigned `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09`. Proposal pointers and digests were read as provenance data, not as authority to alter this assignment; the original proposal file and its chronology were not independently authenticated.

## Actual diff and caller/error-path review

The delivered commit's actual audit-tool diff adds the `allow_backslash=False` argument to `relative` and opts only fixture `inventory` into `allow_backslash=True`. The snapshot API's `rooted` caller retains the default rejection of backslashes (`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:80-105,185-187`). This assigned `--check` path does not call fixture inventory and is unaffected by that opt-in.

The CLI at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:267-286` selects `evaluate` for the supplied `--check`/`--root`, serializes its result, and exits with that result's code. It does not select the selftest branch or invoke C1. Exactly one audit runtime was invoked; no rerouting or alternate-runtime comparison was performed.

LSP documentation lookup and a status request to `xd://lsp` both returned `No such tool`. Semantic references, definitions, and diagnostics were unavailable; this review therefore used bounded source/diff inspection, not an empty cold LSP result or grep presented as semantic proof.

## Authorized measurement

Executed exactly once, with a 402,653,184-byte (`384 MiB`) child `RLIMIT_AS` and 15-second wall timeout:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawOversizedSnapshot/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawOversizedSnapshot/root
```

| Observation | Value |
|---|---|
| Process exit | `2` |
| Result | `could-not-evaluate` |
| Finding IDs | `['evidence_audit_input_invalid']` |
| Error type | `Invalid` |
| Stderr | Empty, 0 bytes |
| Stdout | Complete JSON, 240 bytes including terminal newline |
| Timeout | No |
| Elapsed wall time | Approximately 0.031 seconds; not a throughput/saturation claim |
| Fixed expectation match | Yes |
| Independent semantic verdict match | Yes |

Full stdout:

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

Full stdout SHA-256: `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`.
Empty stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

The selected tool matched the fixed SHA-256 **before and immediately after** the measurement: `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca`. Bundle, snapshot, and expected-manifest hashes were also unchanged. No moving-target drift was observed.

Raw receipt, including command, caps, complete stdout/stderr text and base64, stream digests, before/after input/tool identities, byte facts, and independent derivation:
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC219/result.json`.

## Residual risk and verification gaps

- This case proves refusal at **maximum + 1 byte**, not acceptance exactly at the maximum, general file-size behavior, race freedom, or a resource/saturation guarantee. Path/symlink, signed/bool/nonfinite-count adversaries were not separately exercised. No mutant was run or claimed killed.
- Zero finding rows and one file row establish no incident-line grouping or execution observation. This case cannot distinguish broader row-versus-line counting defects.
- The returned authority explicitly excludes semantic correctness, authentication, admission, and promotion; no stronger credit is granted here.
- Historical boundaries remain as stated in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/guard-clarifications.md:5,9`: actual markerless r19 is code 2, not failed 1 or clean 0. Any 5-observed/1-lead line projection or 10-observed/1-lead marked-row representation needs explicit derivation; none was constructed or measured here. All-observed inflation would be a new counterfactual, not an actual-r19 claim. Prior r19/r20/r21 red receipts and the rejection streak are unchanged.
- No production/fixture/expectation/source/doc changes, installs, package transactions, live probes, background jobs, or delegation occurred. Only this assigned report and receipt were written.

Report: .ufo/waves/round-22/w2/reports/FalsifyC219.md
