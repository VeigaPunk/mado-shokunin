# FalsifyC207 — C2 AuditNoFiles

## Findings by severity

**No actionable defect found in the assigned fixed case.** The one authorized candidate run returned exit **2**, `result: could-not-evaluate`, and exactly `finding_ids: ["evidence_audit_input_invalid"]`, with empty stderr. This matches both the frozen case expectation and an independent schema-based derivation. It is neither clean0 nor failed1. This is an author-lane advisory result, not admission or semantic-precision credit.

Axes: (1) nonempty scan-population validity and rejection of vacuous cleanliness; (2) frozen raw-byte/provenance integrity; (3) truthful verdict/authority within the bounded execution contract.

## Independent derivation and canonical run logic

- The actual 36-byte snapshot at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditNoFiles/root/snapshot.json:1-4` is exactly `{"files": [], "findings": []}` apart from formatting. There are zero finding rows **and zero scanned-file records**. This is array cardinality, not source-line counting.
- The 217-byte bundle at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditNoFiles/bundle.json:2-10` declares exact integer zeros for total/observed/lead/errors, `clean: true`, the relative snapshot path `snapshot.json`, and SHA-256 `fdc47dd34ff271dfa3910e38c428d0894820cc5ee293a6626f3876f74f87742f`. Independent hashing of the actual snapshot bytes matches that digest before and after the run.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-contract.json:5-8` requires a **nonempty** files list and defines invalid input as code2. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-clarifications.md:6-9` independently confirms digest-before-decode and the nonempty-files rule. Empty findings are allowed; empty files are not. Therefore the declared zeros do not contradict any finding rows, but they cannot turn absence of a scan population into a valid clean scan. The correct independent verdict is code2 with `evidence_audit_input_invalid`, not code1 or code0.
- The relevant delivered diff adds `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py` as a new 286-line tool. Its actual `--check` path hashes bounded snapshot bytes before decoding (`:127-131`), requires both arrays and raises `Invalid('empty file population')` on this input (`:132-135`). `Invalid` inherits `ValueError` (`:25-26`); the canonical `evaluate` handler converts it to code2 and the single invalid-input ID (`:165-169`). The CLI routes `--check` to that handler and returns the output code (`:274-282`). The empty-population guard runs **before** actual-count construction and count/clean comparison (`:136-162`), preventing a vacuous clean result.
- No old classifier output was used. Only AuditNoFiles records were selected from `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json`. Its original and materialized expectations agree, its normalizations list is empty, and its frozen-proposal inclusion is explicit. The corresponding source proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/audit-proposals/AuditNoFiles.json` hashes to its declared provenance value.

## Observed bounded measurement

Exactly one scanner child ran, using the assigned `python3 -I` command and absolute tool/bundle/root paths recorded in the receipt. The supervisor set RLIMIT_AS to **402653184 bytes (384 MiB)**, RLIMIT_CPU to 15 seconds, and a **15-second wall timeout**. It finished in approximately 0.03185 seconds without timeout. No fixture payload was executed.

Full stdout (240 bytes, including the terminal newline):

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

Exit: `2`. Full stderr: empty (0 bytes). Stdout SHA-256: `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`. Empty-stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

The selected tool SHA-256 is unchanged before/after and matches fixed C2 identity: `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca`. The audit expected file is unchanged and matches fixed identity: `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09`. Bundle SHA-256 is unchanged: `a9396900b29708b1197bded46a7bd5d6c091f96d4d39d03a69628f8aadb92061`. Proposal SHA-256 is unchanged: `687c69cf4854bc3b8bfe8020b70397196b0ac00535ff9dc4a3f7cf16dc9b3267`. No moving-target drift was observed.

## Residual risk and verification gaps

- This single rejection establishes only the fixed empty-population behavior. With no finding rows or file counters, it cannot establish observed/lead semantic correctness, per-file error accounting, or finding deduplication behavior. The declared counts here are ordinary exact integer zeros; signed/bool/nonfinite counter variants were neither present nor probed.
- The snapshot path is a simple legal relative path, and both artifacts are far below the 2 MiB bound. This run is not evidence for symlink/escape rejection, size-boundary behavior, malformed decoding, or a digest-mismatch branch. Digest-before-decode is supported by the cited source ordering, not by an extra adversarial run.
- The returned JSON does not include an actual snapshot digest or actual_counts on this invalid-input path. The independently measured receipt digests bind the reviewed inputs; no unsupported claim that stdout itself authenticates them is made.
- LSP was unavailable: `read xd://lsp` returned **No such tool**. Status/references/definition/diagnostics could not be obtained. Relevant source and the scoped added-file diff were reviewed directly; no text grep was treated as semantic proof.
- [INFERENCE — proposed fault recipe only] Removing the `if not files: raise Invalid(...)` guard at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:134-135`, while leaving the rest intact, would let the empty arrays and zero claims reach code0/`evidence_audit_clean`. No mutant was created or run, and this proposal is **not a killed mutant**.
- No original r19 output was rerun or reclassified. Its markerless receipt remains code2 could-not-evaluate; derived 5/1 line or 10/1 row populations require explicit derivation and are not actual r19 claims. This case provides no historical correction, non-author admission, saturation claim, or clearance. Prior r19/r20/r21 rejected-harmed receipts and the streak remain untouched.

Only the assigned receipt and this report were written. No source, production, fixture, expectation, gate, registry, or shared configuration was changed. No builds, lints, formatters, whole-suite selftest, measurement driver, additional source-shaped probes, live probes, installs, or updates were run.

Receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC207/result.json`
