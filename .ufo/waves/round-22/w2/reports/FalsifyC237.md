# FalsifyC237 — C2 HistoricalC3.D2.counterfactual-line-observed6-inflation

**Observed match: yes. Independent artifact verdict: reject the new counterfactual, code 1, exactly `lead_count_mismatch` and `observed_count_mismatch`.** This is author-lane advisory evidence, not non-author admission, semantic precision, execution truth, authentication, or promotion. No production/fixture/expected/source bytes were changed.

## Axes and scope

- Exact finding-row arithmetic and evidence-label split.
- Derived-versus-original provenance and truthful authority.
- Frozen input/tool identity and bounded reproducibility.
- Minimal count-check removal sensitivity, proposed only.

One assigned `--check` child was run, with 384 MiB soft/hard `RLIMIT_AS` (402653184 bytes) and a 15-second wall timeout. No other scanner, historical classifier, selftest, measurement driver, new source-shaped probe, build, formatter, install, dispatch, or judging runtime was run. Payload command strings were treated as inert data and never executed. This leaf operated in advisory mode outside the UFO runtime checkout.

## Independent derivation

Sources inspected were the selected case object/provenance in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json`, the fixed `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/HistoricalC3.D2.counterfactual-line-observed6-inflation/bundle.json`, its `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/HistoricalC3.D2.counterfactual-line-observed6-inflation/root/snapshot.json`, and relevant strict-input/count checks in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:20-169,267-286`. The expected answer was visible, but the derivation below comes from the bundle/snapshot content and the relevant candidate implementation, not old classifier output. No old classifier was invoked.

The bundle declares `total=6, observed=6, lead=0, errors=0, clean=false`. Direct enumeration of the snapshot gives:

| Finding index | File label in inert JSON | Line | Explicit marker | Source row indices |
| --- | --- | ---: | --- | --- |
| 0 | `inputs/r13-global-capture.jsonl` | 1 | observed | 0,1,2,3 |
| 1 | `inputs/r13-root.jsonl` | 4 | lead | 4 |
| 2 | `inputs/r14-review-source-bar.jsonl` | 1 | observed | 5,6 |
| 3 | `inputs/r14-source-safety.jsonl` | 2 | observed | 7 |
| 4 | `inputs/r14-source-safety.jsonl` | 3 | observed | 8 |
| 5 | `inputs/r15-libinput-events.jsonl` | 1 | observed | 9,10 |

These are **six derived finding rows representing six distinct file/line groups**, not eleven original finding rows and not a count of individual commands inside aggregate strings. The candidate uses `len(findings)` and increments once per explicit marker (`check`, lines 136–144); it neither expands `source_row_indices` nor deduplicates incidents. This D2 population is therefore **5 observed / 1 lead**. Its displayed projection metadata has observed source multiplicities `4+2+1+1+2=10`, and lead multiplicity `1`, with indices 0–10 covered once. That explains the relationship to the **derived 10/1 row split** without presenting it as a fresh original-r19 classification or execution observation.

The `files` population contains five entries. Every `eval_unparsed` and `unparsed_spawns` is integer zero; error sum is zero. Every finding has a valid explicit marker and nonempty class/command strings. The supplied counts are nonnegative integer literals, not booleans, signed-negative counts, float counts, or nonfinite tokens; `clean` is boolean false. The strict parser rejects duplicate keys/nonfinite numbers, and `count` requires exact `int` (excluding `bool`); this one case does not adversarially exercise those rejection branches.

Raw snapshot SHA-256 is `0bd4e3f6aff600082e65fd0d8a280f65ca2b1556b66758fb11d04122b4ed9e81`, matching both bundle and selected expected metadata. Candidate lines 127–131 compare the **raw-byte digest before UTF-8/JSON snapshot decoding**. The bundle's snapshot name is the simple relative `snapshot.json`; `namei -l` showed directory components and a final regular file, not symlinks. Bundle (218 bytes) and snapshot (2438 bytes) are below the 2097152-byte input cap. No alternate symlink, size-boundary, malformed-number, digest-mismatch, or decoding probe was run, and none is credited as tested coverage.

Consequently:

- `observed`: declared 6 versus actual 5 ⇒ `observed_count_mismatch`.
- `lead`: declared 0 versus actual 1 ⇒ `lead_count_mismatch`.
- `total`: 6 equals 6; `errors`: 0 equals 0 ⇒ no other arithmetic IDs.
- `clean=false` ⇒ neither clean-claim violation applies.
- Valid evaluable input ⇒ **code 1**, not code 2. Code 2 remains could-not-evaluate and must never be called false-clean or failed-1.

The relevant source comparisons are in `check`, lines 151–156; `result` sorts/deduplicates IDs (lines 116–118). The independently derived exact result is `code=1, finding_ids=["lead_count_mismatch", "observed_count_mismatch"]`.

## Actual bounded output

Command executed once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/HistoricalC3.D2.counterfactual-line-observed6-inflation/bundle.json --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/HistoricalC3.D2.counterfactual-line-observed6-inflation/root
```

Exit **1**; no timeout; elapsed 0.03388806000293698 seconds. Full stdout (390 bytes including final newline):

```json
{"actual_counts": {"errors": 0, "lead": 1, "observed": 5, "total": 6}, "actual_snapshot_sha256": "0bd4e3f6aff600082e65fd0d8a280f65ca2b1556b66758fb11d04122b4ed9e81", "authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 1, "finding_ids": ["lead_count_mismatch", "observed_count_mismatch"], "result": "failed"}
```

Stderr: empty (0 bytes).

- Stdout SHA-256: `d9e4d03f282001c4e82cef0f48cb718202a691d568f6389b2fabe0a1730d48c9`.
- Stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Full raw stream strings, exit, caps, timestamps, and digests are preserved in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC237/result.json`.

The detector's `failed` means the **artifact's declared assertions are contradicted**; the assigned expected-result comparison matched. No contradiction with the selected fixed expectation was found.

## Provenance and independent semantic verdict

The selected manifest explicitly identifies this as a **NEW COUNTERFACTUAL**, on **DERIVED** D2 six-line aggregation with later markers, source pointer `#/derived_audit_inputs/D2_six_row_line_aggregate_with_later_markers/snapshot`. Its declared proposal is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/historical-c3.json`, SHA-256 `9ee6144d73342062fc1120afd2e4d4db4a52ec014f8a18744f116ab0dbebed7a`. That proposal and the manifest's original-source inventory were not independently re-audited here.

The all-observed declaration is false **relative to this artifact's explicit evidence labels**: its lead row cannot be counted as observed. This supports bounded arithmetic/label calibration, not a finding about whether the underlying commands executed or the scanner is semantically precise. It does not authenticate the projection, chronology, labels, or manifest's assertion that the original receipt is unchanged.

The markerless actual r19 remains **code 2 could-not-evaluate**, with eleven markerless findings on six incident lines; it was not rerun. The original r19 claim was detected 6/6 incident lines, with disclosed 5/6 without rule B—not the all-observed claim invented by this counterfactual. This derived 5/1-line result does not satisfy or rewrite the literal unchanged-row historical target, clear r19/r20/r21 red receipts, reset the streak, or grant admission. No expectations or normalizations were changed.

## Minimal mutation recipe — not executed

**Mutant:** In `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py`, frozen SHA-256 `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca`, delete only line 152's tuple entry `('observed', 'observed_count_mismatch'),` from the count-comparison loop. Leave the total, lead, and errors checks and the rest of `check` unchanged. This is a one-entry source-code check removal, with no fixture or expectation mutation.

**Expected detector:** The exact bounded case assertion must require both exit code 1 **and the complete two-ID list**, not just nonzero exit.

**[INFERENCE] Expected mutant output:** The same bytes still have a lead mismatch, so the mutant should return code 1 with only `["lead_count_mismatch"]`. The exact finding-ID detector should reject that missing observed-check ID. A code-only detector would not distinguish this defect.

**Mutation verdict:** Proposed only. No mutant was edited or run; **no killed/survived claim is made**. There is no measured mutant/restored output. This is a concrete sensitivity hypothesis for L1's private sandbox, not permission to alter the contract.

## Frozen-byte / restoration evidence

| Artifact | SHA-256 before **and** after the sole run |
| --- | --- |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py` | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json` | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/HistoricalC3.D2.counterfactual-line-observed6-inflation/bundle.json` | `8408155280fb2f70368666ce5c32ad84a18e16d8acafb12c3e5725477a81a66f` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/HistoricalC3.D2.counterfactual-line-observed6-inflation/root/snapshot.json` | `0bd4e3f6aff600082e65fd0d8a280f65ca2b1556b66758fb11d04122b4ed9e81` |

The selected tool and expected hashes match their fixed identities; no drift was observed. No source mutation occurred, so restoration was unnecessary; before/after identities are equal. The only writes were this assigned report and this seat's `result.json`. No installs/updates were performed.

Report: .ufo/waves/round-22/w2/reports/FalsifyC237.md
