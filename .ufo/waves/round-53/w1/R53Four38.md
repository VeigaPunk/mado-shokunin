# R53Four38 — adversarial review of frozen C1/C2

## Result and axes

Axes: **operability** (C1) and **coverage** (C2). This is an independent critic report, not a non-author review, admission, or implementation. I found no current r53 candidate counter or repaired entry in the inspected wave tree, so neither claim is shown to pass. Historical r52 attacks are evidence to construct falsifiers, not proof of r53 behavior.

## C1 — minimum counterexample set

Frozen predicate (`.ufo/waves/round-53/claims-frozen.md:5-7`) requires a newly committed scratch-aware counter, explicit selftest, production-ledger TARGET_MET, no-work and every frozen forgery TARGET_MISSED, exact population coverage and non-self pointers. It expressly limits this to structural accountability, not semantic proof.

The strongest local counterexamples to any claimed r53 pass are the already-reproduced predecessor classes:

- Round-52 closure records r51 counter returned `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET` while forged descriptions were accepted; a separate attack accepted nine self-pointer laundering spellings including a symlink alias (`corpus/lessons/round-52-verifier-spotcheck.md:29-32,57`). Thus cardinality equality and a reported selftest success do not establish semantic row accountability or non-self pointer identity.
- An especially cheap adversarial fixture is a selftest function that prints `ok` without invoking controls, paired with a production ledger that passes and a no-work fixture that incorrectly returns TARGET_MET. The test falsifies operability unless the selftest actually runs each frozen fixture and checks expected outcome plus exit status. A second minimal fixture keeps row count constant but changes a single pointer to an alias resolving to the counter/ledger itself; it targets non-self semantics without confounding population count.

These cases are historical attack evidence and proposed falsifiers, not execution against an r53 candidate. The r53 wave directory as inspected has reports and registry only, no counter/fixture/receipt to test. Therefore C1 remains unproven, not currently falsified. Smallest safe correction if a candidate claims green: require revision-bound receipts for each fixture, invoke the candidate's own selftest, and independently resolve canonical ledger pointers (including symlink/path aliases) before accepting population equality. Do not infer semantic ledger correctness from the frozen structural predicate.

## C2 — minimum counterexample set

Frozen C2 (`claims-frozen.md:9-11`) requires append-only correction of P16–P18 against opened pinned bytes, a frozen counter rejecting old bytes and accepting corrected proposition/quote/pin bindings, independent source-truth review, and no expansion credit without newly opened source-row evidence plus uncovered ground.

The routed r52 defects supply three distinct counterexamples to a superficial green result:

1. **Quote splice:** P16 joins calls from separate locations while omitting an intervening conditional; the joined quote is not contiguous in the pin.
2. **Subject swap:** P17 attributes repeat logic at `:619-622` to `sendshortcut`, although those lines are in `sendkeystate`.
3. **False localization:** P18 locates an error return inside the scan after the loop closed at `:571`.

These are documented in `corpus/lessons/round-52-verifier-spotcheck.md:38-40,59,74`, not re-opened source truth in this round. Additional historic counter attacks are important: entry grammar mismatch yielded `props=0 TARGET_MISSED`, while fabricated quote text at real pins passed TARGET_MET (`:39`). Thus a counter can both reject a valid-shape candidate and accept false evidence if it merely checks pin/name presence. A useful concrete mutant suite preserves old P16–P18 bytes, inserts a spliced P16 quote, swaps P17's subject, shifts P18's location, and replaces quote text with fabricated words while retaining a valid pin. Require each mutant to miss, and a corrected entry to meet, with exact located quote bytes and proposition-to-row/pin identity; then a genuinely independent reviewer must assess entailment. A correction to old ground alone is not expansion credit.

No corrected entry, counter, opened-this-round source receipt, or independent-review artifact was present in the inspected round-53 wave tree. Do not carry the old defects forward as a finding about an uninspected correction; they are controls the new claim must beat. Smallest safe correction is to freeze the old bytes and these isolated mutants alongside a positive corrected fixture, and keep source-truth and novelty decisions separate from structural counter output.

## Evidence and limits

Attacked predicates: frozen C1 production-ledger pass/no-work and every-forgery misses, explicit selftest, exact coverage/non-self pointers; frozen C2 old-entry rejection/corrected-entry acceptance with proposition-bound quote/pin bindings, independent truth review, and provenance-qualified expansion.

Exact local inspection actions and outputs: `read` of `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-53/claims-frozen.md` → C1 lines 5–7 and C2 lines 9–11; `glob` of `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-53/w1` → reports/registry, no candidate counter or C2 repair artifact; `read` of `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-52-verifier-spotcheck.md:27-75` → predecessor counter outcomes and routed P16–P18 issues quoted above. No candidate counter or producer executed, no new fixture built, and no target predicate was run; no execution result is claimed. Disk check: `df -P /fast/scratch/hyaku/mado-r53` → `/dev/nvme1n1p2 842131708 219761340 622370368 27% /fast`; no disk-guard marker was found by the bounded local filename search. No scratch directory or artifacts were created.

Newly opened external sources: none; no URL fetch or source-code pin opened, so no source URL/date/quote applies. Evidence is local and dated 2026-10-27.

Smallest safe correction: do not admit either claim on structural receipts alone; require exact negative-control matrix and source-grounded independent C2 review. Treat any counter pass as structural only, consistent with the frozen scope.

## Report

Attacked predicates and exact inspection output are listed above. No claim of execution, source truth, admission, or non-author review. Report path (relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`): `.ufo/waves/round-53/w1/R53Four38.md`
