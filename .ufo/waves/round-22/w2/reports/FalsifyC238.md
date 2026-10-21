# FalsifyC238 — HistoricalC3.D2.line-claim-5-observed-1-lead

## Scope and axes

Author-lane advisory probe only; no admission authority. Axes: (1) arithmetic and row/line grain integrity, (2) exact bytes/strict schema/path bounds, (3) truthful derived provenance and authority, (4) reproducible capped read-only evidence. Only the assigned case was measured, once. No source, fixture, expectation, registry or shared documentation was changed.

## Independent derivation before measurement

The selected entry in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json` identifies a **DERIVED** six-line aggregate, not unchanged original r19 output or a new detector run. Its original and materialized expectations are both code 0 with `['evidence_audit_clean']`; `normalizations` is empty. The selected provenance attributes labels to the later split receipt. Historical source artifacts and chronology were not independently authenticated by this one-case probe.

I independently parsed the exact bundle and snapshot bytes without importing the candidate auditor or consulting old classifier outputs:

- Six finding objects identify six distinct file/line pairs: five `observed`, one `lead` (the `inputs/r13-root.jsonl:4` metadata label).
- Five file objects provide ten explicit nonnegative, non-boolean integer error counters, all zero. Population is nonempty.
- Claim is `total:6, observed:5, lead:1, errors:0, clean:false`. Every asserted count agrees. `clean:false` is conservative non-clearance, not an assertion of no findings.
- Classes and commands are nonempty strings; labels are explicit valid strings. UTF-8, duplicate-key rejection, finite numbers, exact integer count types and boolean `clean` all passed independent parsing/inspection.
- Source-index groups are `[0,1,2,3]`, `[4]`, `[5,6]`, `[7]`, `[8]`, `[9,10]`: eleven unique referenced source rows, grouped into six line-level findings. The derived observed groups cover ten indices and the lead group one. **5/1 is this six-line aggregate's split; 10/1 is the explicitly derived source-index split, not an original r19 evidence assertion.** The auditor counts finding objects, not `source_row_indices`, command fragments or class labels.

Therefore the independently derived result is **code 0, `['evidence_audit_clean']`**, limited to artifact arithmetic and supplied labels.

The candidate's relevant implementation is `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py`: lines 127–131 bind raw snapshot bytes by SHA-256 before decoding; lines 132–149 validate/count the population; lines 151–160 compare all four counts and condition clean-claim failures on `clean:true`. These checks agree with the independent derivation.

## Single authorized measurement

Executed exactly the assigned `python3 -I` auditor command with its absolute `--check` bundle and `--root` arguments. The child received `RLIMIT_AS=402653184` bytes (384 MiB), a 15-second parent wall timeout and a 15-second CPU limit. One scanner child; elapsed 0.033938141001272015 seconds; no timeout.

Observed exit: **0**. JSON code: **0**. Finding IDs: **`['evidence_audit_clean']`**. Counts: **6 total / 5 observed / 1 lead / 0 errors**. Stderr: empty. **Observed match: true.**

Full stdout (including its trailing newline), full stderr, byte counts, base64 encodings, process result, command and digests are retained in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC238/result.json`.

## Relevant boundary findings and authority

- Bundle is 218 bytes; snapshot is 2,438 bytes, each below the 2,097,152-byte bound. Both are regular files. The relative snapshot name is `snapshot.json`, resolves beneath the supplied root and contains no traversal. No symlink component was found in the selected file/root paths or ancestors.
- Independent snapshot hashing preceded snapshot decoding. Candidate source has the same ordering. This valid fixture does **not** dynamically exercise mismatched digests, invalid UTF-8, duplicate/nonfinite JSON, signed/boolean count rejection, symlink escapes or the exact size cutoff. No extra counterfactual was created or run, so no coverage for those rejection branches is claimed.
- Independent semantic verdict: **consistent derived-artifact arithmetic and explicit labels**, not semantic precision, authenticated execution truth, calibration/admission credit or desktop clearance. No local expectation contradiction was observed.
- The original markerless r19 receipt remains **code 2, could-not-evaluate**, per the fixed task authority and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/guard-clarifications.md:9`; it was not rerun. This derived green does not satisfy or rewrite a literal unchanged-row historical green target. All-observed inflation claims would be new counterfactuals, not actual r19 claims. Prior rejection authority remains unchanged.

## Minimal proposed check-removal mutant — not executed

Source: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:159`.

Remove only the `clean and ` precondition:

```python
# before
    if clean and actual['total']:
# proposed faulty replacement
    if actual['total']:
```

Leave line 160's `failures.append('findings_claimed_clean')` unchanged. This is a plausible over-rejection defect: treating any nonzero findings as a contradiction even when the bundle explicitly declines to claim clean.

Expected detector: the same exact CLI contract, requiring process exit 0, JSON code 0, IDs `['evidence_audit_clean']` and empty stderr for this fixed case.

[INFERENCE] With `clean:false` and six findings, the proposed fault would enter the failure branch and return exit/code 1 with `['findings_claimed_clean']` and unchanged counts. Thus this case should detect the removed clean precondition. **Mutant verdict: NOT RUN; no killed or survived claim.** No source was edited, no scratch source was created, and neither a mutant nor a restored scanner run was authorized or performed.

## Hashes and restoration evidence

Each selected artifact had identical before/after SHA-256; all matched fixed identities:

| Artifact | Before = after SHA-256 |
| --- | --- |
| Auditor | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| Expected manifest | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| Selected bundle | `9b82fbc83721949146cb4928adf4f0bdf9d1d6ff4134fcc0f979ad065474cbc3` |
| Selected snapshot | `0bd4e3f6aff600082e65fd0d8a280f65ca2b1556b66758fb11d04122b4ed9e81` |

Stdout SHA-256: `c6e1fadb207bfcbbc9f6fed083e8ddc5684684619fa6bb498886981a23ac91c7` (363 bytes). Stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

Restoration was unnecessary: no mutation was applied and all selected bytes remained identical. No suite, selftest, measurement driver, historical classifier, build, lint, formatter, live probe, background job or delegated work ran. No tools were installed or updated.

Report: .ufo/waves/round-22/w2/reports/FalsifyC238.md
