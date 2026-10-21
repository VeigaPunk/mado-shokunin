# FalsifyC235 — C2 `HistoricalC3.D1.row-claim-matches-derived`

Author-lane advisory attack only. This is not a non-author admission. It credits no semantic precision and no C2 or C3 admission.

## Outcome

- **Observed:** exit `0`, `code 0`, `finding_ids ["evidence_audit_clean"]`, `actual_counts {total 11, observed 10, lead 1, errors 0}`, empty stderr. This matches expected.
- **Independent verdict:** `code 0`, `["evidence_audit_clean"]`. This also matches expected. No falsifying counterexample was found for the verdict.
- **Retained contradiction:** the case's `rationale` text is false for its own bytes, and the case is duplicated byte-for-byte by another case. Details are below. No expectation changes are proposed.

Receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC235/result.json`, with raw `stdout.txt`, `stderr.txt`, `exit.txt` and before/after hashes alongside it.

## Identities

| Item | sha256 | Before = after |
|---|---|---|
| `tools/mado-evidence-audit.py` | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` | yes; matches the fixed identity, no drift |
| `audit/fixtures/expected.json` | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` | matches the fixed identity and `expected.sha256` |
| `bundle.json` (220 B) | `2390cf9cab3e052f1d2fa079bd244e16fdf6a03bffee150618f34dcd3a028b56` | yes; equals `bundle_sha256` |
| `root/snapshot.json` (3140 B) | `f9cf3c643213c085a5031c15ea314458b18aca0d7312df01a86d5f87ce46c608` | yes; equals the bundle `sha256` |
| stdout (365 B) | `962922a71dbb959495db0790ee834117c2ecc359b792e70f797bd6d097d74265` | — |

There was one run: `prlimit --as=402653184 -- timeout 15 python3 -I …/mado-evidence-audit.py --check <bundle> --root <root>`. No selftest, measurement driver or other case was executed.

## Independent derivation from the raw bytes

1. **Digest before decode.** sha256 of the raw snapshot bytes is `f9cf3c64…c608`. The bundle declares the same 64-character lowercase hex value. The tool hashes the bytes before `parse(raw)`, at lines 127–131.
2. **Strict schema.** The bundle has `snapshot` (str), `sha256` (str) and a `claim` dict. The snapshot has a non-empty `files` list (5 entries) and a `findings` list (11 entries). Every finding has an explicit `evidence` value in {observed, lead} and non-empty `class` and `command` strings. There are no duplicate keys and no floats.
3. **Row grain.** There are 11 rows: 10 `observed` and 1 `lead`. The lead row is `inputs/r13-root.jsonl:4`, `package_query`, `pacman:-Q`.
4. **Line grain, for reference only.** There are 6 distinct file:line pairs: 5 observed lines and 1 lead line. The contract says "no deduplication is implied", so line grain is not what this claim asserts. The sibling case `line-claim-on-row-snapshot` covers the 6/5/1 claim on these bytes.
5. **Errors.** All five files have `eval_unparsed` = 0 and `unparsed_spawns` = 0, so the sum is 0.
6. **Claim.** The claim is `total 11, observed 10, lead 1, errors 0`, all exact non-negative ints with no bool-as-int, and `clean false` as an exact bool. Every count equals the actual count. Neither clean:true clause applies, because `clean:false` is a conservative non-clearance assertion. The result is `code 0`, `["evidence_audit_clean"]`.

## How the 10/1 row split was derived

Markerless actual r19 output would be code 2. These row counts need an explicit derivation, and I checked that it exists and holds:

- The snapshot bytes parse to exactly `w1/historical-c3.json` → `derived_audit_inputs.D1_row_level_with_later_markers.snapshot`. The proposal sha256 is `9ee6144d…bed7a`, which matches the case provenance.
- The recomputed D1 canonical sha256 (`sort_keys`, compact separators) is `9507e816…fae94b`, which equals the declared value. The file bytes are that object serialized with sorted keys, indent 2 and a trailing newline.
- For every i from 0 to 10, row i of the snapshot equals original row i projected to {file, line, class, rule, command}, plus `later_interpretation.markers_by_original_row[i]`. None of the 11 original rows carries an `evidence` key, so the r19 receipt stays markerless and unchanged.
- The marker source is the r20 `recall-split-final.txt` (`5165b728…`). It records `finding_totals {observed 10, lead 1, unmarked 0}`, so the row-level 10/1 split comes from that receipt and is not inferred here.
- `claim_kind` says "Derived historical C3 comparison; not an r19 claim", and `r19_original_claim` is kept separately. This is honest framing.

## Attack surface relevant to this case

- **Row vs line grain:** consistent. The tool uses `len(findings)` and per-row markers, which agrees with the row-grain claim. Line grain would fail, and that is a separate case.
- **Digest before decode:** satisfied for this snapshot. The bundle itself is necessarily decoded first to obtain the digest, which the contract allows.
- **Signed, bool and nonfinite counts:** none are present. `type(v) is int` with `v >= 0` would reject bools and negatives. This case does not exercise those paths.
- **Path, symlink and size:** the snapshot name is the plain relative `snapshot.json`. The case tree has no symlinks, and both files are regular and far below 2 MiB. Not stressed by this case.
- **Truthful authority:** the tool output limits its authority to "artifact arithmetic and evidence labels only". The case **rationale**, however, is not truthful for this case (see below).

## Retained contradictions

1. **The rationale is false for this case's bytes.** The case `rationale` in `expected.json` is the proposal's top-level six-row rationale, copied verbatim. It says: "Six rows = the six frozen incident lines … each aggregated … total 6 = 6 rows, observed 5, lead 1 … → code 0". The bound snapshot actually has **11** unaggregated rows and the claim is 11/10/1. The same text is attached to five HistoricalC3 cases, three of which are D1 row-level cases: this one, `line-claim-on-row-snapshot` and `row-counts-claimed-clean`. The verdict and expectation are unaffected; the issue is provenance text. Impacted axis: truthful provenance.
2. **Duplicate case.** `HistoricalC3.r19-c3-derived-row-level-green` binds a byte-identical bundle (`2390cf9c…`), the same snapshot `f9cf3c64…`, the same claim and the same expectation. The case population therefore counts one input twice. Impacted axis: independent case and evidence count. It must not be credited as two independent observations.

## Smallest safe correction

These are for L1 to decide; no expectation changes are proposed.

- Give the three D1 cases a D1-specific rationale: "11 rows = original_rows 1:1 plus r20 markers_by_original_row; r20 finding_totals observed 10 / lead 1; errors 0". Keep the six-row text only on D2 and top-level cases.
- Either deduplicate `r19-c3-derived-row-level-green` against this case or mark the pair as one input, so evidence and case counts do not count it twice.

## Installs

None.
