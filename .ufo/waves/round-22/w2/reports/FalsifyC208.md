# FalsifyC208 — AuditRawClaimInfinity

## Findings by severity

**No actionable candidate defect found in this fixed case.** The one authorized child exited **2**, with exactly `finding_ids: ["evidence_audit_input_invalid"]`, `result: "could-not-evaluate"`, and `error: "Invalid"`. This matches the independently derived invalid-input outcome and the sealed case entry. It is neither clean/0 nor a contradicted comparable assertion/failed/1.

This is an author-lane advisory observation, not non-author admission, semantic-precision credit, promotion, or reversal of the prior rejection receipts/streak.

## Axes

1. Strict finite count/schema refusal.
2. Frozen artifact identity and provenance.
3. Honest could-not-evaluate versus failed/clean authority.
4. Bounded resources and read-only isolation.

## Independent semantic derivation

- Raw input: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawClaimInfinity/bundle.json:1` contains bare `Infinity` at `claim.errors`, not a quoted string and not an integer. The other declared finding counts are zero and `clean` is false. `Infinity` is not a valid JSON number; it cannot be accepted as a finite, nonnegative exact integer claim count.
- The independently inspected snapshot, `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawClaimInfinity/root/snapshot.json:1-9`, has **zero finding rows**, **one file row**, and both `eval_unparsed` and `unparsed_spawns` equal to zero. Thus its artifact counts are `total=0, observed=0, lead=0, errors=0`. This is a row-count derivation, not an incident-line projection or evidence of execution truth.
- The 104-byte snapshot hashes to `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c`, exactly the bundle's declared snapshot digest. The bundle is 178 bytes. Point-in-time `namei -l` inspection showed ordinary files and no symlink components on these two fixture paths; neither artifact is near the candidate's 2 MiB bound.
- Therefore the independent expected result is **2 / `["evidence_audit_input_invalid"]`**. Comparing infinity to zero and returning `error_count_mismatch`/1 would treat a malformed claim as a comparable assertion. Returning clean/0 would also be wrong. Zero artifact counts do not rescue an invalid enclosing bundle.
- Selected expectation/provenance: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json:411-454` records the same original and materialized expected result, `normalizations: []`, bundle digest `6293e7feea15ba53d359eff4a28bf06b1f369552beab4bb420357224973a14d4`, and proposal/source digest `402ed534701d8ba0159f97dacd91e36ba56604c6cbd6e8d4d268004bcd2b14ea`. The proposal digest is manifest provenance, not a claim that its separate source file was rehashed here. The verdict above follows from raw bytes, counts and strict schema, not an old classifier output. No expectation was changed.

## Candidate control flow and actual delivered diff

LSP was unavailable: `read xd://lsp` returned `No such tool`. No status, references, definition or diagnostics request could be served. The following is textual source/control-flow evidence, not semantic-reference proof.

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:51-53` supplies a `parse_constant` hook that raises `Invalid` for the bare nonfinite token; `finite` at lines 38-48 separately rejects decoded nonfinite floats. The current case is the former path.
- Static control-flow inference: the canonical `--check` branch at lines 267-282 calls `evaluate` at lines 165-169, then `check` at lines 121-122 parses the bounded **bundle** first. Consequently its `Infinity` refusal precedes snapshot loading, digest comparison, decoded finding counting and claim comparison. `evaluate` converts `Invalid` to code 2 and exactly `evidence_audit_input_invalid`; `main` prints that output and returns its code.
- The count contract at lines 67-77 requires `type(value) is int` and nonnegative values. Claim construction/comparison at lines 147-156 must not turn invalid numeric input into a mismatch result. This case is already refused at parsing, so it does **not** dynamically exercise the later exact-int check.
- The actual file diff from `git show 71228fd582d6d9338d7916cc64e69bd4c2e928b5 -- /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py` changes `relative` to accept an opt-in `allow_backslash=False` parameter and enables it only in fixture `inventory`. The snapshot API's `rooted` call still uses the default. The selected `--check` route does not call `inventory`; no alternate runtime or identity rerouting was used for this measurement.

## Observed measurement and identity

Exactly one child ran the assigned `python3 -I` command, using the assigned absolute tool, bundle and root paths. Address-space soft/hard limits were both **402653184 bytes (384 MiB)**, with a **15-second** subprocess timeout. It finished in **0.030858 seconds**, without timeout; stderr was empty.

Full stdout, including its terminal newline, and full stderr are retained in the raw JSON receipt, with base64 copies and byte digests. Stdout was 240 bytes, SHA-256 `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`.

Before **and** after the child, the selected tool matched `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` and the expectation file matched `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09`. Bundle and snapshot digests also matched before/after. No identity drift or input drift was observed.

## Residual risk and verification gaps

- This is one small malformed-bundle refusal, not saturation, whole-suite agreement, complete strict-schema coverage, semantic correctness or resource scaling. No new source-shaped probe, mutant, selftest, measurement driver, original old tool, C1 scan, full test suite, build, lint or formatter ran. No mutant was killed or claimed killed.
- The early bundle parse refusal does not exercise snapshot digest-before-decode behavior, digest mismatch classification, findings-versus-lines aggregation, observed/lead labeling, signed or boolean counts, path escapes, adversarial symlinks, size-boundary rejection, or mutation/race resistance. The source places snapshot hash comparison before snapshot decode at lines 127-131, but this execution does not establish that behavior. The file population here is nonempty and the finding population is empty; that distinction is preserved.
- The correct historical boundary remains `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/guard-clarifications.md:9`: actual markerless r19 is code 2/could-not-evaluate, not failed/1 or clean/0. Derived 5-observed/1-lead incident-line or 10-observed/1-lead row populations require explicit derivation; all-observed inflation claims are new counterfactuals, not actual-r19 claims. This case measures none of those historical populations and grants no semantic-precision or admission credit.
- No resume path or `resume_continuity_v1` implementation is in this assigned artifact-audit case; no resume-preflight guarantee is asserted.
- Production, fixture, expected, registry and shared checkout sources remained read-only. Writes were confined to this assigned report and receipt. No installs, package operations, live probes, fixture execution or background jobs occurred.

Raw receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC208/result.json`

Report: .ufo/waves/round-22/w2/reports/FalsifyC208.md
