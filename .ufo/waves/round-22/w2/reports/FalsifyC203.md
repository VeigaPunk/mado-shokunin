# FalsifyC203 — AuditFindingsClean

## Findings by severity

No actionable implementation defect found in this fixed case. The delivered audit correctly rejects a valid, internally count-consistent artifact whose `clean:true` assertion contradicts its nonempty findings. This is an expected **code 1 / failed assertion**, not an input-evaluation failure and not a false-clean result.

Independent artifact-semantic verdict: **code 1**, exactly **`["findings_claimed_clean"]`**. Observed verdict: **the same**, with process exit 1 and empty stderr. No expectation or source bytes were changed.

## Axes and independent derivation

Axes: independent raw-byte/schema arithmetic; exact diagnostic/exit fidelity; bounded immutable reproducibility; truthful authority.

The derivation was fixed before invoking the candidate. It uses the selected bundle and raw snapshot, not any old classifier output:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditFindingsClean/bundle.json:2-10` declares `clean:true`, total 1, observed 1, lead 0, errors 0, relative snapshot `snapshot.json`, and its lowercase SHA-256.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditFindingsClean/root/snapshot.json`, at JSON pointers `/findings/0` and `/files/0`, contains exactly one explicitly `observed` finding with nonempty class/command and exactly one file member with integer counters `eval_unparsed:0` and `unparsed_spawns:0`. The command string is inert artifact data; it was not executed.
- Thus the actual row counts are total 1, observed 1, lead 0; actual errors are `0 + 0 = 0`. Every declared count agrees. The only contradiction is `clean:true` with one finding. No count-mismatch ID or `uncertain_scan_claimed_clean` applies.
- The raw JSON contains no duplicate keys, negative/bool/nonfinite counters, missing evidence marker, empty required string, or empty file population. Bundle and snapshot were regular files with no symlink in any path component, sized 217 and 296 bytes respectively, below the 2 MiB limit. The snapshot digest equals the bundle declaration. There is consequently no reason to downgrade this case to code 2.
- The normative rule is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-contract.json:5-9`: count exact rows and per-file errors; `clean:true` requires empty findings and zero errors; invalid/unavailable input is code 2, not failed 1 or clean 0. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-clarifications.md:6-10` fixes digest-before-decode and actual-count comparison.

Selected provenance in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json` is bound to `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/inputs/proposals/AuditFindingsClean.json` (SHA-256 `3d78ae1110e37c7ddb93aaf61ac2f3432753e03d95fb13bf4e7c7916155dd1d7`). The proposal retains original expected code string `"1"`; assembly materialized integer `1` with an explicit representation-normalization record. The semantic verdict and finding ID are unchanged. This review independently agrees; it did not rewrite or normalize an observed contradiction away.

## Relevant canonical check and exit path

Literal source inspection of `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py`:

- Lines 121-131 read bounded snapshot bytes, compute/check SHA-256, return code 2 on mismatch, and only then decode the snapshot JSON.
- Lines 29-53 reject duplicate keys and nonfinite values; lines 67-77 require exact integer, nonnegative counts, excluding bool. Lines 80-105 enforce relative paths and reject symlinks/escape.
- Lines 132-149 require nonempty files, explicit observed/lead markers and nonempty strings, count findings as rows, sum both error counters, and require an exact bool clean assertion.
- Lines 150-162 compare each actual count, append `uncertain_scan_claimed_clean` only for actual errors, and append `findings_claimed_clean` for the actual nonempty findings population. Here only the last condition is true; `result` at lines 116-118 preserves the sorted unique ID and failed label.
- Lines 165-169 route invalid input exceptions to code 2. The requested `--check` route at lines 274-275 calls that evaluator directly, and lines 281-286 print the JSON and exit using its code. It does not invoke the classifier or selftest on this route.

The `lsp` device was unavailable: reading `xd://lsp` returned `No such tool: xd://lsp`, and the mounted device inventory had no LSP. References, definition and diagnostics could not be obtained; the source checks above are the literal fallback, not a claim of semantic call-graph proof.

## Single authorized measurement and integrity

Executed exactly one isolated candidate check:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditFindingsClean/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditFindingsClean/root
```

The child had a 402653184-byte (384 MiB) address-space limit, a 15-second wall timeout, and a 15-second CPU limit. It exited 1 without timeout; measured elapsed time was approximately 0.030 seconds. This is a bounded completion observation, not a resource/saturation guarantee.

Full stdout was one JSON line (366 bytes, including newline):

```json
{"actual_counts": {"errors": 0, "lead": 0, "observed": 1, "total": 1}, "actual_snapshot_sha256": "7ad71f4ca0e17a80994b16a88e5d9b1cedbd60dc43519bcfbd1a6b20bd683ca1", "authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 1, "finding_ids": ["findings_claimed_clean"], "result": "failed"}
```

Stderr was empty (0 bytes). Full stdout/stderr, their byte encodings/digests, exit status, limits, input sizes, and before/after input hashes are retained in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC203/result.json`.

All five recorded input digests were identical before and after:

| Artifact | SHA-256 |
| --- | --- |
| Selected C2 tool | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| Audit expected manifest | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| Selected bundle | `6f00f86b6dd3ba2d5a619a33bb81804193b0e63dd8f4935a3b84e2f8f4ddd511` |
| Selected raw snapshot | `7ad71f4ca0e17a80994b16a88e5d9b1cedbd60dc43519bcfbd1a6b20bd683ca1` |
| Selected frozen proposal | `3d78ae1110e37c7ddb93aaf61ac2f3432753e03d95fb13bf4e7c7916155dd1d7` |

The assigned revision was `71228fd582d6d9338d7916cc64e69bd4c2e928b5`; this seat verified the specified tool/content hashes, not checkout history or chronology. No drift was observed. No installs or updates were performed.

## Residual risk and verification gaps

- This single-row, single-source-line case cannot distinguish general row-versus-incident-line aggregation behavior. It supplies no multirow/deduplication evidence.
- Signed/bool/nonfinite rejection, mismatched or malformed snapshot handling, symlink/escape rejection, and the exact 2 MiB boundary were inspected only where relevant to these valid bytes; their adversarial branches were not dynamically exercised. Digest-before-decode is established here by source ordering, not by an additional malformed/digest-mismatch probe.
- No old tools, historical r19 receipt, measurement driver, whole 46-case selftest, full suite, build, lint, formatter, source-shaped extra probe, live probe, or mutant was run. No semantic precision, actual execution truth, authentication, resume continuity, same-identity rerouting, saturation, or admission follows from this observation.
- Historical scope remains unchanged: markerless actual r19 is code 2 could-not-evaluate; derived 5/1 incident-line or 10/1 row populations require explicit derivation; all-observed inflation assertions are new counterfactuals, not original r19 claims. This case is not any of those historical artifacts. The prior r19/r20/r21 red receipts and streak are untouched.
- An initial manifest JSON query mistakenly treated `cases` as an object and failed; the corrected ID filter selected this case. Unsolicited unrelated-case text in that error was not used as evidence or measured.

This is author-lane advisory evidence only. It identifies no actionable defect within the assigned case and grants no non-author admission or planner/integration authority.
