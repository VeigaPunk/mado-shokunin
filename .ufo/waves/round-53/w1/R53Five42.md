# R53Five42 — connector synthesis

## Evidence and axes

Axes: **operability** (C1) and **coverage** (C2). Frozen C1 is a structural accountability counter: production ledger must yield `TARGET_MET`, while no-work and every frozen forgery yield `TARGET_MISSED`, with exact population coverage and non-self pointers; it explicitly is not semantic proof (`.ufo/waves/round-53/claims-frozen.md:5-7`). Frozen C2 separately requires append-only P16–P18 correction, a counter rejecting old and accepting corrected bytes with quote/pin/proposition bindings, and independent source-truth review. Expansion credit additionally requires a source row opened this round and uncovered ground (`claims-frozen.md:9-13`).

The round-52 spot-check reports P16's quote splice, P17's misattribution, P18's mislocalization and no valid admission counter (`corpus/lessons/round-52-verifier-spotcheck.md:36-40,74`). This is routed historical evidence, not a claim about any r53 candidate. A peer report notes the round-52 registry rows and hashes establish source identity/provenance, not proposition entailment (`R53Four33.md:8-10`). The round-53 wave has no established pass in the evidence reviewed here; this proposal makes no verdict or admission.

## One bounded move

Use a single compact, revision-bound **evidence receipt format** for the final demonstrations, but enforce disjoint C1 and C2 predicate records. Each record carries predicate/control ID, input revision and digest, exact command and output, and artifact/source-row locator. C1 records the independently derived population denominator, per-row identity/uniqueness, pointer resolution/non-self result, and expected-vs-observed control verdict. C2 records each P16/P17/P18 proposition ID, immutable source-row/pin and exact contiguous quote locator, counter outcome on old/corrected entry, and the independent review outcome. The common receipt header makes evidence reproducible and attributable; separate typed records prevent a structural C1 pointer check from being mistaken for C2 truth or a C2 quote match from being mistaken for entailment.

## Risks and verification

This improves **operability** via exact, revision-tied, rerunnable receipts and **coverage** via proposition-by-proposition lineage, with no axis tradeoff if C1 and C2 remain independent acceptance gates. Risks: a shared envelope could blur predicate boundaries; recorded quotes can still fail to entail their propositions; receipts alone do not establish new/uncovered ground. Mitigate by making the record type explicit and prohibiting cross-claim substitution; preserve independent source-truth review and require coverage-map novelty evidence before any expansion claim. This is bounded evidence packaging, not a substitute for the counter, correction, controls, or reviewer.

Verification on the final committed revision: rerun C1 selftest, production ledger, no-work and every frozen forgery; independently confirm exact population and non-self pointers. For C2 compare old and corrected entry outcomes and check each proposition's quote against source bytes opened this round, then obtain independent non-author source-truth review. Separately inspect the coverage map before claiming expansion.

## Evidence boundary and report trailer

Source-only local reads; no producer/campaign execution, live reads, package queries, external fetch, source mutation, or tracked edits. No tool installations. Disk capacity: exact command `df -P /fast/scratch/hyaku/mado-r53 /home/vgpnk/Projects/shokunin/mado-shokunin` output showed `/fast` 622,578,168 1K-blocks available and `/home` 616,953,868 available. `command -v disk-guard || true` produced no path. No scratch artifacts were created; therefore none required cleanup. External sources newly opened: none (URL/date/quote not applicable).

- Attacked predicate: the risk of conflating C1 instrument-ledger structural accountability with C2 proposition-grounding/source truth and expansion coverage.
- Exact command/output: `df -P /fast/scratch/hyaku/mado-r53 /home/vgpnk/Projects/shokunin/mado-shokunin && command -v disk-guard || true` → `/fast` available `622578168`; `/home` available `616953868`; no disk-guard path printed. Frozen predicates and routed reports inspected using repository read tools as cited above; no target counter/fixture command run.
- Source URL/date/located quote for any newly opened source: none; no external source opened.
- Report: `.ufo/waves/round-53/w1/R53Five42.md`
