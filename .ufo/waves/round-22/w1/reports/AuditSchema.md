# AuditSchema — round 22 w1 scout report (C2 audit-contract)

Scope: read-only review of how `audit-contract.json` handles emptiness, the digest, error sums and negative counts, plus two independent proposals. I made no production edits, ran no detector, measured nothing and executed no payloads. `tools/mado-evidence-audit.py` does not exist (observed with `ls`), so no candidate code was read.

## Inputs (observed)

| File | SHA-256 |
|---|---|
| `.ufo/waves/round-22/audit-contract.json` (11 lines, valid JSON) | `e65d165a1599c2d8743509bfb09ef46df9b8cc9038246b80cdef1780b5fdf23f` |
| `.ufo/waves/round-22/registration.md` | `315b48ee7105e3cd543849aa775c7b5743057aa3bdca6bcd76dea4e4bdfb13fa` |

## Proposals written

| File | SHA-256 | Expected |
|---|---|---|
| `w1/audit-proposals/AuditNegative.json` | `80f4cdd1563d335ed652c0114bea1d6a787547a7a4462d3b354f1864c15fbd2b` | code `2`, `["evidence_audit_input_invalid"]` |
| `w1/audit-proposals/AuditNoFiles.json` | `687c69cf4854bc3b8bfe8020b70397196b0ac00535ff9dc4a3f7cf16dc9b3267` | code `2`, `["evidence_audit_input_invalid"]` |

- **AuditNegative:** the snapshot has `files:[{eval_unparsed:-1, unparsed_spawns:1}]`, and the claim is all zeros with `clean:true`. The negative value cancels in the sum, so an auditor that sums without checking signs returns `0/evidence_audit_clean` and hides one real unparsed spawn. This kills a "sign check missing" mutant. The negative is in the snapshot, not the claim, because `AuditBoolCount` already covers claim-side type errors.
- **AuditNoFiles:** `files:[]` (present but empty), `findings:[]`, and the claim is all zeros with `clean:true`. Every arithmetic check passes vacuously. This kills a "population check missing" mutant.
- Both were checked as strict JSON with no duplicate keys and exactly the keys `id`, `snapshot`, `claim`, `expected` and `rationale`. They were not run against any auditor.

## Python behaviors confirmed (Python 3.14.8 on this host)

These are default-parser results, not candidate behavior:

- `json.loads` accepts `NaN`, `Infinity` and `1e400` (which becomes `inf`). Rejecting nonfinite numbers needs an explicit `parse_constant` hook plus a float check.
- `json.loads("-0")` returns int `0`, so a textual negative zero becomes a valid count.
- `{"a":1,"a":2}` silently becomes `{'a': 2}`. Detecting duplicates needs `object_pairs_hook`.
- `isinstance(True, int)` is `True`, so count checks need `type(x) is int`.
- An integer literal over 4300 digits raises `ValueError`, not `JSONDecodeError`. Code that catches only `JSONDecodeError` will crash.
- `json.loads(b"\xef\xbb\xbf{}")` returns `{}` (bytes input accepts a BOM), while `json.loads("\ufeff{}")` raises. The result depends on whether bytes or a decoded string are parsed.
- An uncaught exception exits with status `1`, the same as verdict `1` ("failed"). A crash is therefore indistinguishable from a contradiction verdict if only the exit code is checked.

## Concerns and ambiguities

### Emptiness
1. **Absent versus empty `files`.** The rule says "at least one files member is required", but the verdict for a missing `files` key versus `files:[]` is not stated separately. [INFERENCE] Both should be `2`. `AuditNoFiles` covers only the present-but-empty case.
2. **Missing `findings` key.** "Findings may legitimately be empty" does not say whether an absent `findings` key equals `[]` or is invalid. Recommendation: invalid (`2`). A missing list is not a declared empty population.
3. **"Nonempty" strings.** It is unspecified whether whitespace-only `class`/`command` values count as nonempty. The same goes for non-object rows, extra keys in rows, files, the snapshot top level, the bundle, and the claim (strict versus permissive). Each of these changes the verdict between `0` and `2`.
4. **Zero-byte or non-object snapshot.** [INFERENCE] These are malformed, so `2`. That is not explicit.

### Digest
5. **Proposals cannot express tampering.** Each proposal provides a raw snapshot object, and the harness computes the actual digest. So `snapshot_tampered` cannot be expressed by any proposal and is not covered by the w1 audit seats. The same applies to duplicate keys, malformed JSON, `NaN`/`Infinity`, integers over 4300 digits, a BOM, symlinks, path escape and the 2 MiB bound, because a parsed JSON object cannot carry any of them. These need harness-authored byte fixtures or must be disclosed as uncovered.
6. **Uppercase or malformed `sha256`.** "Actual lowercase SHA256" does not say whether an uppercase or wrong-length digest is invalid input (`2`) or tampering (`1`).
7. **Ordering of digest versus validation.** "Snapshot digest is checked before verdict comparison" does not order the digest against snapshot validation. If the digest mismatches and the snapshot is also malformed, the contract allows either `1` or `2`. Recommended order:
   1. Bundle shape and path safety (`2`).
   2. Size bound (`2`).
   3. Digest over the raw bytes (`1 snapshot_tampered`, then stop without interpreting the untrusted content).
   4. Strict snapshot parse and schema (`2`).
   5. Claim comparison (`1`/`0`).
8. **Path base and size bound.** The bundle's `snapshot` path is "relative", but it is not stated whether it is relative to `--root` or to the bundle's directory. "2MiB" does not say whether it is inclusive (2097152 bytes allowed?) or whether the bundle file is also bounded.

### Error sums
9. **What is summed.** It is not explicit whether `errors` means the sum of counter values or the number of files with a nonzero counter. [INFERENCE] It is the sum of values. It is also unspecified whether one failure can appear in both `eval_unparsed` and `unparsed_spawns`. The audit can only check the declared arithmetic, not that double-counting is absent.
10. **Actual or claimed counts for clean checks.** It is unspecified whether `uncertain_scan_claimed_clean` and `findings_claimed_clean` use actual or claimed counts. Recommendation: actual counts. For example, if the actual errors are 1, the claim says `errors:0` and `clean:true`, the expected IDs should be both `error_count_mismatch` and `uncertain_scan_claimed_clean`.
11. **Finding-ID set semantics.** `AuditLeadInflated` expects two IDs, which implies that all contradictions are reported. However, it is unspecified whether the list is ordered (for example, in contract order) or compared as a set. For code `2`, it is unspecified whether the list is exactly `["evidence_audit_input_invalid"]` with no mixed code-1 IDs. I assumed it is exact.
12. **Understated `clean`.** `clean:false` on a clean receipt has no finding ID, so [INFERENCE] it gives `0`. The rule is only one-directional, so this conservative understatement is allowed. That should be stated.

### Negative and type handling
13. **Negative zero.** `-0` arrives as int `0` from Python's parser. The contract does not say whether textual `-0` is negative (`2`) or zero (valid). This is not expressible as a proposal, so it is harness-only.
14. **Float-valued counts.** It is unstated whether `0.0`, `1.0` and `1e0` count as "exact int". [INFERENCE] They do not, so `2`.
15. **Crash versus verdict.** Integers over 4300 digits must map to `2`. An uncaught `ValueError` exits `1`, which silently looks like "failed". `measure.py` should require both the exit code and the exact finding IDs, never the exit code alone.
16. **Where nonfinite numbers are banned.** It is unspecified whether "nonfinite numbers are invalid" applies anywhere in the document (including extra keys) or only to counts.

### Evidence markers and the C3 representation
17. **Missing markers: invalid or uncertain?** The schema requires an explicit `observed|lead` marker, and `AuditMissingEvidence` expects `2`. But the rule "missing/invalid evidence markers are uncertainty" could also be read as a countable uncertainty, not refusal. The registration also mentions "explicit unknown/error totals", but the contract has no `unknown` tier, so an honest `evidence:"unknown"` row can only be refused (`2`). This affects the historical C3 case: if original r19 rows lack markers, adding them changes the rows, while leaving them out gives `2`. That is neither the registered "red" nor "green". `HistoricalC3` must disclose which happened.
18. **Name of the clean verdict ID.** `evidence_audit_clean` labels a code-`0` "artifact consistent" result even when the claim says `clean:false` (for example, `AuditValidObserved`). The name invites confusion with scan cleanliness, so reports should say "consistent", not "clean".
19. **Type of `expected.code`.** The contract shape writes `"code": "0|1|2"`, which is a string placeholder, and the verdict keys are strings. My proposals use JSON integer `2`. The harness must compare consistently.

## Confidence
- High: the proposal verdicts follow directly from the schema text ("nonnegative exact int", "nonempty list") and the rules ("negative counts … invalid", "at least one files member is required").
- High: the Python parser behaviors were observed directly on this host.
- Medium: the recommended orderings and set semantics are inference and need a Main or contract decision.

## Remaining unknowns
- Concerns 1–4, 6–8 and 10–19 above need contract decisions.
- Whether `AuditHarness` uses integer or string codes.
- I sent `MadoR22.AuditHarness` a short note covering concerns 19, 15 and 5. The write reported success, but delivery could not be confirmed.

## Addendum — raw negative proposals (Main IRC request after clarifications)

Basis: `.ufo/waves/round-22/audit-clarifications.md`, read at 14:22 UTC. The clarifications resolve concerns 1, 2, 3, 6, 7, 8, 10, 11, 12, 16, 17 and 19 above. Notable change: a digest mismatch is now code **2** with `snapshot_tampered`, checked before JSON decoding. My earlier `AuditNegative`/`AuditNoFiles` expectations are unchanged by the clarifications.

### Schema extension `audit-proposal-raw-v1` (confirmed by `MadoR22.AuditHarness` via IRC)
The extension adds optional fields to `preimplementation_proposal_shape`. The fixture layout is: FIX is the per-fixture directory, ROOT is `FIX/root` (passed as `--root`), and the bundle lives at `FIX/bundle.json`, outside ROOT.
- `raw_snapshot`: the snapshot bytes are the exact UTF-8 encoding of this string, with nothing appended. When it is present, `snapshot` is `null`.
- `pad`: `{target: snapshot|bundle, byte: " ", total_bytes: N}`. The file is padded to exactly N bytes. For the snapshot, padding happens before the digest is computed.
- `setup`: `{snapshot_at: [FIX-relative paths], mkdir: [...], symlinks: [{path, target}]}`. Symlink targets are taken literally. The default `snapshot_at` is `["root/snapshot.json"]`.
- `path_overrides.snapshot`: the literal string to put in the bundle's `snapshot` field. `{{ROOT_ABS}}` is replaced with the absolute ROOT. The default is `"snapshot.json"`.
- `digest_override`: `{literal: hex}`, `{transform: "upper"}` or `{truncate: 63}`. The default is the actual lowercase digest.
- `raw_bundle`: a template with the placeholders `{{SNAPSHOT_PATH}}` and `{{SNAPSHOT_SHA256}}`. When it is present, `claim` is documentation only.
- `eligibility`: `frozen` or `contingent: <reason>`.

### Raw proposals written (23 files; all codes are JSON ints; finding IDs sorted)
Every fixture uses a clean, otherwise-valid receipt and claim, so an auditor that skips the targeted check returns a wrong `0`/`evidence_audit_clean`.

| Proposal | Defect | Expected |
|---|---|---|
| AuditRawDupNestedConflict | Duplicate `eval_unparsed` (values 1, 0) inside a files member | 2 input_invalid |
| AuditRawDupMetadataSame | Duplicate key with identical values inside ignored metadata | 2 input_invalid |
| AuditRawDupBundleClaim | Duplicate `claim.clean` in the bundle (`raw_bundle`) | 2 input_invalid |
| AuditRawOverflowCounter | Counter `1e400` (overflows to inf) | 2 input_invalid |
| AuditRawNaNCounter | Counter `NaN` token | 2 input_invalid |
| AuditRawInfinityMetadata | `-Infinity` in an ignored metadata key | 2 input_invalid |
| AuditRawClaimInfinity | Bundle `claim.errors` is `Infinity` | 2 input_invalid |
| AuditRawDigestTamper | Well-formed but wrong digest (SHA-256 of empty input) | 2 snapshot_tampered |
| AuditRawTamperMalformed | Malformed snapshot bytes plus wrong digest: tests that the digest is checked first | 2 snapshot_tampered |
| AuditRawDigestUppercase | Correct digest, uppercased | 2 input_invalid |
| AuditRawDigestShort | Correct digest truncated to 63 characters | 2 input_invalid |
| AuditRawPathEscape | `../outside.json`, which exists outside ROOT | 2 input_invalid |
| AuditRawPathDotDotInternal | `sub/../snapshot.json`, which resolves inside ROOT | 2 input_invalid |
| AuditRawPathAbsolute | `{{ROOT_ABS}}/snapshot.json` | 2 input_invalid |
| AuditRawPathBackslash | `sub\snapshot.json`; a file with that literal name exists | 2 input_invalid |
| AuditRawPathDot | `./snapshot.json` | 2 input_invalid |
| AuditRawPathEmpty | `""` | 2 input_invalid |
| AuditRawSymlinkFile | Leaf symlink pointing inside ROOT | 2 input_invalid |
| AuditRawSymlinkDir | Intermediate directory symlink pointing inside ROOT | 2 input_invalid |
| AuditRawSymlinkEscape | Lexically clean leaf symlink pointing to `../outside.json` | 2 input_invalid |
| AuditRawOversizedSnapshot | Valid snapshot padded to 2097153 bytes, with the actual digest | 2 input_invalid |
| AuditRawOversizedBundle | Valid bundle padded to 2097153 bytes | 2 input_invalid |
| AuditRawSnapshotAtLimit | Exactly 2097152 bytes | 0 evidence_audit_clean, **contingent** on the bound being inclusive |

**Self-check (observed; own fixtures only, no candidate code).** All 25 of my proposals are strict JSON with no duplicate keys, and each `id` matches its file name. Every `raw_snapshot`/`raw_bundle` meant to be invalid fails a strict loader (duplicate-rejecting, no nonfinite constants, no overflow) for the intended reason. The two padded snapshots' base text parses strictly. Per-file SHA-256s are listed in the shell output of this turn and can be reproduced with `sha256sum w1/audit-proposals/AuditRaw*.json`.

### Still unresolved (not proposed)
- **Huge integers:** a count of more than 4300 digits is a finite, exact, nonnegative int, but Python's default decoder raises `ValueError` on it. The truth could be `2` (decoder limit) or a real comparison. Main must rule before a fixture is frozen.
- **Negative zero:** whether textual `-0` is valid zero or a negative count.
- **Symlinked ROOT:** whether ROOT itself being a symlink (or having a symlinked ancestor) counts as a "symlink component".
- **Inclusive size bound:** exactly 2 MiB; this is why `AuditRawSnapshotAtLimit` is contingent.
- **Bundle-side rules:** applying duplicate, nonfinite and size rules to the bundle relies on "duplicate keys anywhere" and "Inputs" (plural). [INFERENCE] I treated these as covering the bundle.
- **Harness confirmation resolved:** `MadoR22.AuditHarness` confirmed the exact optional field names, semantics, eligibility handling, and pinning of actual files/symlink targets. All hazardous paths stay inside each case's FIX tree: `../outside.json` escapes ROOT only into FIX, absolute templates name ROOT files, and symlinks never target unrelated host files. This confirms schema agreement, not implementation or exercised behavior.

## Tooling
No installs or updates.
