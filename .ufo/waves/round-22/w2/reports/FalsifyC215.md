# FalsifyC215 — C2 `AuditRawInfinityMetadata` (artifact-only evidence audit)

Scope: one fixed case, one bounded `--check` child (384 MiB address space, 15 s). No selftest, no measurement driver, no edits, no installs. Authority is artifact arithmetic only; nothing here is semantic precision, admission, or r19 evidence.

## Observed match

| Field | Expected (`expected.json` entry, lines 719–762) | Observed (receipt `result.json`) | Match |
|---|---|---|---|
| exit / code | 2 | exit 2; stdout `"code": 2` | yes |
| finding_ids | `["evidence_audit_input_invalid"]` | `["evidence_audit_input_invalid"]` | yes |
| result | could-not-evaluate (verdict 2) | `"result": "could-not-evaluate"` | yes |
| stderr | n/a | 0 bytes | n/a |
| timeout / elapsed | — | not timed out; 0.033 s | n/a |
| tool sha256 before / after | `277eced…fca` (fixed C2 identity) | `277eced…fca` / `277eced…fca` | yes (no drift) |
| expected.json sha256 | `b5df74b5…2fd09` (fixed audit-expected identity) | `b5df74b5…2fd09` (full digest in receipt) | yes |

Observed stdout (240 bytes, sha256 `9956a6a7…b4756`): `{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}`

The observed verdict is code 2. It is not clean (0) and not failed (1).

## Independent semantic verdict (derived from bytes and schema, not from tool output)

1. **Bundle (217 bytes, sha256 `f97f5852…81e2`).** Valid strict JSON object with unique keys `claim`, `sha256`, `snapshot`. Counters `total/observed/lead/errors` are `0` (exact non-bool nonnegative ints). `clean` is `true` (exact bool). `sha256` is 64 lowercase hex. `snapshot` is `"snapshot.json"`: relative, no traversal, resolves under the explicit ROOT to `root/snapshot.json`, which is a regular file (not a symlink). Size is 90 bytes, far below 2 MiB. No input-level defect.
2. **Digest before decode.** sha256 of the 90 raw bytes is `ad30af77…54f4`, equal to the declared `sha256`. The gate passes, so `snapshot_tampered` does not apply and decoding proceeds. This step does not discriminate in this case.
3. **Strict decode of the raw bytes** `{"scan_seconds":-Infinity,"findings":[],"files":[{"eval_unparsed":0,"unparsed_spawns":0}]}`. Under RFC 8259 a number is `-` followed by `0` or `[1-9]digits`; `-I` is not a number, and `Infinity`/`NaN` are not JSON literals. The document is malformed JSON, which the clarifications map to code 2 `evidence_audit_input_invalid`. Independently, "JSON numbers must be finite" (clarifications) and "nonfinite numbers are invalid" (contract rules) reject it even under a lenient decoder that would read `-Infinity` as `-inf`.
4. **Consistency, had decoding succeeded (hand-derived counterfactual, not run).** `findings` is an empty list, which is legitimate. The single `files` entry has `eval_unparsed=0` and `unparsed_spawns=0`, so errors sum to 0. Actual total/observed/lead/errors are 0, which match the claim, and `clean:true` is allowed because findings and errors are both zero. The only defect is the nonfinite token in an extra metadata key.
5. **Verdict:** code 2, `["evidence_audit_input_invalid"]`. This agrees with the expectation and with observation.

## Counterfactual (NEW, hand-derived, not run, not an actual r19 claim)

A decoder that accepts `-Infinity` (default `json.loads`), or a finiteness check applied only to counters, would evaluate this bundle to code 0 / `evidence_audit_clean`. This case forbids that outcome, so it discriminates that mutant. No mutant was executed. Proposed for L1 only, not run.

## Uncertainties and contradictions (retained, expectation unchanged)

- **U1 (interpretive, not observed).** The clarifications' bullet also says "Extra metadata keys are permitted and ignored". That could be read as exempting the value of `scan_seconds` from the finiteness rule. I judge that reading contradicted by the same bullet ("JSON numbers must be finite"), by the contract rules ("nonfinite numbers are invalid", no metadata carve-out), and by "malformed JSON gives 2". If the exemption reading were adopted, the expectation would be 0, so this is recorded as a live interpretive risk.
- **U2 (attribution limit).** The observed stdout is code-only (`"error": "Invalid"`) with no reason field. The match on code and ID is observed. The cause is attributed by elimination: I independently verified that the digest, bundle shape, counters, and path all pass, leaving the nonfinite token as the only defect. No other cause was found.
- **U3 (boundary not exercised in this case).** No finding rows, so row/line grain is not exercised. No negative, bool-counter, or nonfinite counter, so those are not exercised. Digest mismatch is not exercised. The 2 MiB size boundary is not exercised (90 bytes). Symlinks were checked only inside the case tree (none); ancestor path components above the case directory were not checked.
- **U4 (read scope disclosure).** A broad grep over round-22 records surfaced sibling wave records and other seats' assignment text. Those were not used for the derivation. Inputs used: the fixed expected entry, the frozen proposal (sha `6aac0a…359a`, 875 bytes, matches provenance), the bundle and snapshot bytes, `audit-contract.json`, and `audit-clarifications.md`.

## Attack outcome

- Observed code 2 `evidence_audit_input_invalid` equals the independent semantic verdict and the expectation. No false clean (0), no false failed (1).
- Nothing is credited as semantic precision or admission. The tool's own authority line says so explicitly.
- No expectation change proposed. U1 is flagged for Main, not resolved in the expectation.

## Receipts

Directory: `.ufo/waves/round-22/w2/receipts/FalsifyC215/`
- `result.json` (argv, cap, exit, full stdout/stderr, digests before/after, tool drift flag)
- `exit.txt` = `2`; `stdout.txt` (240 bytes, sha256 `9956a6a7…b4756`); `stderr.txt` (0 bytes, sha256 `e3b0c442…b855`)
- `inputs-before.sha256`, `inputs-after.sha256` (identical: tool, expected.json, bundle.json, snapshot.json)

Installs or updates: none. `prlimit` and `timeout` were already present (`/usr/bin/prlimit`, `timeout`); `python3` is 3.14.8.

Verification run by this agent: one `--check` child only. Not run: selftest, measurement driver, sibling cases, mutants.
