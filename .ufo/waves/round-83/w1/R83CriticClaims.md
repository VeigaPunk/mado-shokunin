# R83CriticClaims — scoped claims review

STATUS: defect

Axes: C1 coverage; C2 operability. Review dimensions: count integrity, oracle independence, causal separability, source provenance, no-work controls, and freeze integrity. This is not an admission vote.

## Findings

### F1 — high: frozen C1 target population is inconsistent

At measured revision `dbc09269fe547ab13541e722dd7d2ba33015f348`, the counter has `MUTANTS = 38` but 39 enumerated mutations. The measurement receipt contains 58 case lines, 39 mutant lines, and `cases=58 correct=58 mutants=38 killed=39 ... verdict=TARGET_MISSED`. The working-tree amendment changes only `MUTANTS = 38` to `39`; it was uncommitted when inspected.

Counterexample: all enumerated mutants die, but the frozen target misses. Conversely, its `killed == MUTANTS` comparison could accept exactly 38 kills out of the actual 39; thus the miscount is not merely a display typo. The observed receipt honestly stops and does not demonstrate that hypothetical false pass.

Impacted axis: C1 coverage / population integrity. Smallest safe correction: preserve the original missed receipt; reconcile the successor constant, declaration predicate, and target line to the actual 39-member population under an explicit forward amendment. The current declaration still says 38. A successor result must identify its actual instrument generation, not reinterpret the old receipt.

### F2 — high: C2 diagnostic flag can claim the full target without mutations

In `quality/counters/c2-r83-runbook.py` main, the mutation loop is skipped under `--no-mutants`, but target includes `(args.no_mutants or killed == MUTANTS)`. The final label still selects `TARGET_MET` when the remaining clauses pass, printing `mutants=0 killed=0`. This contradicts C2's declared unconditional predicate that all 27 named matcher mutants die before TARGET_MET.

Evidence: static branch inspection; no bypass run executed. The recorded default measurement did exercise 27 mutants and reports 27 kills, so this does not invalidate those observed kills.

Impacted axis: C2 operability / target-label integrity. Smallest safe correction: use an explicitly diagnostic verdict for skipped mutations, as C1 already does with `MUTANTS_SKIPPED`; never label that path the full target.

### F3 — medium: C2 frozen controls have post-measurement byte drift

The declaration, committed controls, and recorded C2 receipt agree on sha256 `a0fba389676a87f2ceaf4933535057587b4ba7f1b2e0b63c00de256df3ae3f86`. The working-tree controls and generator instead regenerate sha256 `22ca4c1c495274f797d1eec8abb804974a02054d55657fd896507d972c05b3bf`. The diff changes only synthetic-looking unique-name suffixes in tray-items' negative array-output sample. Both variants remain non-integer negatives; no semantic loss was established.

Counterexample: the counter reads controls from the supplied disk path and merely prints their hash. Its `tree=bound` checks SKILL.md, the tool, and declared fixtures, not the controls or running counter. Therefore `tree=bound` is not a claim that the complete instrument/control tree equals the revision. The current control drift would not be caught by that binding check.

Impacted axis: C2 operability / reproducible provenance. Smallest safe correction: retain the original receipt/hash as historical evidence; either restore the frozen controls or explicitly amend their hash and generation before citing a successor result. Narrow the declaration's whole-working-tree binding wording to what is actually checked, or bind the missing instrument/control bytes.

### F4 — medium: source registration lags the frozen citation

Frozen SOURCES.md contains S457, S464, S470, S481, and S482, but no S484. The frozen declaration nevertheless cites S484 for busctl output shapes. S484 and S485 were additions in the working-tree SOURCES.md diff; the round-83 fetch directory was untracked when inspected.

The source content is reachable and supports the relevant arithmetic/output format: S482.xml lines 17/21 declare the two properties as `as`/`b`; fetched busctl XML lines 159–167 describe terse get-property output, 489–496 describe boolean/array parameter formatting, 521–524 connect that format to returned data, and 552 onward contains the terse/verbose example. Thus this is a snapshot/provenance defect, not evidence that the shapes were invented.

Impacted axis: C2 source provenance. Smallest safe correction: land the source registry/fetch provenance with the successor generation and explicitly disclose the pre-freeze citation gap. No assertion about upstream legal-license compliance was established by this review.

### F5 — medium: causal separability is stated more strongly than implemented

C1 extracts `tools/mado-barfoot.py` at candidate/base revisions. C2 explicitly checks that same tool's working-tree bytes equal its revision and includes the tool's four refusal probes (visible in the receipt). Thus the two claims have distinguishable primary outputs, but C2 does depend on C1's changed tool bytes/behavior. Neither counter was observed reading the other's receipt or controls.

Impacted axes: C1/C2 attribution. Smallest safe correction: describe the shared-tool dependency honestly and distinguish conceptual claim separation from fully independent byte/behavior dependencies. Do not infer independent acceptance from separate counter filenames.

### F6 — low: receipt provenance wording overclaims recorded hashes

The freeze paragraph says the two receipts record tool/counter sha256s. C1 records the candidate/base tool hashes and controls hash, not its counter hash. C2 records its controls hash and revision, not a counter hash. Git revision recovery remains possible, but the executing counter is not itself revision-bound by these labels.

Smallest safe correction: state the actual receipt fields, or attach explicit instrument hashes to successor evidence.

## Controls and counts that withstood inspection

- Frozen C1 generator reproduced exactly `e4409dabcf74f32307f14b31afb85091bca7d584771076bdb9a3b336bc9512c4`: 47 carried + 11 new = 58. It imports json/sys and constructs arithmetic expectations rather than invoking the model. The counter checks parsed equality of the 47-case carried prefix.
- C1 base receipt has exactly six incorrect new-class cases, yielding 52/58. The five gap-closure cases pass there as declared. The candidate receipt reports all 58 correct and tool selftest 136/136.
- Both box-reader mutants report 57/58 and killed=yes. The two live-disagreement cases distinguish allocation 34 from observed height 40; expectations do not simply echo the live box.
- Frozen C2 generator reproduced exactly `a0fba389...`: 29 carried + 2 new = 31, one declared supersession. Default receipt has 31 probe lines and 27 mutant lines, matching 31/31 and 27/27; four exact rows plus one empty row explain 26 shape rows.
- C2 exact row-cell matching, unique binding, and executed-command equality support the reported 31/31 anchors. Boolean matcher uses fullmatch `b (true|false)`; G2 object/array and G3 stage-prefix regression assertions exist.
- C2 held-r82 receipt contains the declared setup refusal for zero round-82 section rows versus expected 29. This is a named external receipt, not an in-run control verification; the counter's control line is a literal citation.

## Freeze/amendment limits

Read-only history shows initial freeze `4e48d8e7`, then E1 `4208c24a`, E2 `aeeb5e54`, E3 `dbc09269`; changes explicitly follow discovered regressions/survivors. This is adaptive pre-wave instrument development, not a clean pre-data freeze. Current bookkeeping also acknowledges that distinction and preserves C1's honest stop. The earlier 54/55 and 55/55 measurement narratives were not independently replayed or validated from retained receipts here.

No lane admission, saturation judgment, instrument edits, git/jj mutations, installations, host probes, service changes, or dispatch were performed. Verification exercised: read-only revision/diff/hash/count inspection and regeneration of control JSONs in seat scratch. No model/counter measurement or mutation suite was rerun. Scratch was removed before yield.

Report: .ufo/waves/round-83/w1/R83CriticClaims.md
