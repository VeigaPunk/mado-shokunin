# FalsifyC239 — HistoricalC3.r19-c3-original-markerless-invalid

## Scope and axes

Author-lane advisory probe only; no orchestration, integration, admission or streak authority. Axes: independent strict-schema validity; finding-row versus incident-line grain; fixed artifact identity and bounded execution; truthful provenance and mutation discrimination.

Exactly one assigned C2 check ran. No C1/old classifier invocation, whole-corpus/selftest/measurement driver, fixture execution, alternate case, source mutation, build, lint, formatter, install or background job ran. Only this report and the assigned receipt were written.

## Independent derivation, before the detector

Inputs:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/HistoricalC3.r19-c3-original-markerless-invalid/bundle.json`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/HistoricalC3.r19-c3-original-markerless-invalid/root/snapshot.json`
- Only this case's entry/provenance in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json` was selected. No other case's expectations were inspected.

The bundle is 220 bytes and its snapshot is 2,814 bytes. Raw snapshot SHA-256 exactly matches the bundle declaration. Both decode as UTF-8 JSON without duplicate keys or nonfinite numbers. The snapshot has a nonempty population of **5 file rows and 11 finding rows; all 11 finding rows lack `evidence`**. Its file counters sum to zero. The claim is `{total: 11, observed: 11, lead: 0, errors: 0, clean: false}`; the case metadata explicitly calls it a **placeholder counterfactual assertion, not an r19 claim**.

Relevant candidate source is `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py`:

- Lines 127–131 read bounded snapshot bytes, hash them, compare the declared digest, and only then parse/decode the snapshot. The bundle itself necessarily parses first to obtain the snapshot declaration.
- Lines 132–138 require list populations and an explicit string `evidence` on every finding. The first row fails `require(row, 'evidence', str)` at line 138; absence is not a label that can be recovered from class/command/counts.
- Lines 165–169 map this `Invalid` exception to **code 2**, `finding_ids == ['evidence_audit_input_invalid']`. It does not reach the assertion-mismatch comparison at lines 147–161.

Thus the independently derived result is **could-not-evaluate (2)**, not failed assertion (1), nor clean (0). This was derived from the fixed bytes and the required-marker check, not from an old classifier verdict. The fixed expectation agrees and has no recorded normalization.

### Grain and historical authority

Independent grouping of the actual rows gives:

| Artifact row reference | Incident line | Finding rows |
| --- | ---: | ---: |
| `inputs/r13-global-capture.jsonl` | 1 | 4 |
| `inputs/r13-root.jsonl` | 4 | 1 |
| `inputs/r14-review-source-bar.jsonl` | 1 | 2 |
| `inputs/r14-source-safety.jsonl` | 2 | 1 |
| `inputs/r14-source-safety.jsonl` | 3 | 1 |
| `inputs/r15-libinput-events.jsonl` | 1 | 2 |
| **Total** | **6 distinct file/line pairs** | **11** |

These are inert row references, not files executed by this probe. Eleven finding rows are not six incident lines. No observed/lead split can be inferred from the missing markers. In particular, neither 5/1 at line grain nor 10/1 at row grain is a label split present in these bytes.

The selected provenance records original r19 as claiming detection of 6/6 incident lines with no evidence split, plus disclosing 5/6 without the HelperFn rule-B lead. It identifies this fixture as `historical-derived`, with source pointer `#/derived_audit_inputs/A_original_projection_markerless (construct: D1 snapshot with every evidence key removed)`. It is **not the original r19 output or a new detector run**. Listed historical source hashes are provenance declarations; those other artifacts were not reopened or independently reauthenticated here.

The historical target limitation in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/guard-clarifications.md:9` remains: literal unchanged markerless r19 rows cannot yield a valid 5-observed/1-lead green under this required-marker, finding-row schema. Later markerful 10/1 rows or selected 5/1 incident-line representatives require explicit derivation and are not interchangeable with the original markerless case. This probe constructs neither. No all-observed inflation claim is attributed to actual r19.

### Other input guards, limited to this case

The numeric claim/error counters here are exact nonnegative `int` values, not booleans, negative values or nonfinite numbers; `clean` is an exact bool. The source's exact-type and sign checks are therefore not the failing condition, and the candidate never reaches its count-validation loop for this input. The declared snapshot path is plain relative `snapshot.json`; both input leaves are regular files, with no symlink at either leaf/root or their ancestor chains. Both artifacts are below the source's 2 MiB bound. No signed/bool/nonfinite, symlink, traversal or size-boundary variant was created or tested; this case cannot establish those guards' discriminating power.

## Actual bounded execution

The only scanner child command was:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/HistoricalC3.r19-c3-original-markerless-invalid/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/HistoricalC3.r19-c3-original-markerless-invalid/root
```

The child had `RLIMIT_AS` soft/hard 402,653,184 bytes (384 MiB), applied before exec, and a 15-second subprocess timeout. It completed without timeout in 0.032275161996949464 seconds. **Exit: 2.** Full stdout (240 bytes, including final newline):

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

Full stderr: empty (0 bytes).

- Stdout SHA-256: `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`.
- Stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Raw text, base64 bytes, exit, cap, timing, input/output digests and derivation are preserved at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC239/result.json`.

**Observed match:** yes, exactly code 2 and the singleton input-invalid ID.

**Independent semantic verdict:** correct preservation of missing-label uncertainty for this fixed schema input. It is not a false clean or failed arithmetic assertion. Matching this result is not classifier semantic precision, execution truth, authentication, C2's literal historical-green target, admission or retroactive r19 credit. No new expectation contradiction was found in this case; the already-declared historical-green limitation remains unresolved by this measurement.

## Minimal proposed mutant — not applied or run

At `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:138`, remove the required-marker presence/type check by making this one-line replacement:

```text
original:    marker = require(row, 'evidence', str)
replacement: marker = row.get('evidence', 'observed')
```

Keep the allowed-value check and every other line unchanged. This is a plausible missing-label-as-observed defect, not a fixture or expectation change.

**Expected detector:** the same assigned command, expecting code 2 with only `evidence_audit_input_invalid`.

**[INFERENCE] Predicted mutant output:** defaulting each missing marker to `observed` would produce counts `{total: 11, observed: 11, lead: 0, errors: 0}`. Those match this fixture's explicitly counterfactual placeholder claim; with `clean: false`, no arithmetic failure remains, so the inferred result is code 0 with `['evidence_audit_clean']`. This erroneous default would be distinguishable from the required code 2.

**Mutation verdict:** proposal only, NOT RUN. No killed/survived claim is made. No pristine/mutated/restored triple was authorized or attempted; this seat was explicitly limited to the unmodified single-case check.

## Identity and restoration evidence

The following hashes matched the fixed identities/selected expectation and were unchanged before versus after the scanner. The wrapper also compared the complete before/after byte strings, with exact equality for all four files.

| Artifact | SHA-256 before = after |
| --- | --- |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py` | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json` | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/HistoricalC3.r19-c3-original-markerless-invalid/bundle.json` | `cca140705cde2633bedb7198e0a3d5ca386f7ea998a5f35e74cc54632da16494` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/HistoricalC3.r19-c3-original-markerless-invalid/root/snapshot.json` | `f722632dbe464fd7547e6c30700e76f2652b555adcc1292f7d04ba1676892a27` |

No source/fixture/expected bytes were changed, so no restoration action was needed. No moving-target drift or install/update occurred. Prior r19/r20/r21 red receipts and streak are untouched. This report is advisory evidence for L1, not a non-author admission decision.
