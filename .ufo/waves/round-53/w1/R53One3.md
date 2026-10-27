# R53One3 — independent review

## Findings (severity order)

### S2 — C1's frozen predicate does not operationalize the claim it names

**Attacked predicate:** C1 requires the final counter to establish unique/exact ledger population, non-self pointers, and instrument-specific context; it expressly disclaims semantic proof. The production-ledger and forgery controls alone cannot establish pointer accountability if arbitrary existing, non-self files or generic prose pass. The frozen language does not specify how much context is instrument-specific or how a pointer must be instrument-relevant, leaving acceptance subjective and easy to game. This is a material residual criterion ambiguity, not evidence that an unobserved round-53 counter failed. The r52 work itself records analogous bypasses: `.ufo/waves/round-52/w1/C1Simplify.md` enumerates generic-description and ledger self-pointer controls; `.ufo/waves/round-52/w1/C1CounterDesign.md` and its receipts report bounded context/pointer checks, while round-52 verifier output in `.ufo/waves/round-52/w1-results.json` includes falsification of contextual/pointer attribution. A stricter defined structural relevance rule and controls for arbitrary unrelated targets/generic-context variants are needed before interpreting TARGET_MET as instrument accountability.

### S2 — C2 proposition-bound structure is necessary but not source-truth evidence

**Attacked predicate:** C2 requires quote/pin/proposition bindings and an independent truth review. Round-52 evidence shows why the latter is essential: the old P16 statement attached a correctly located quote to a false inference; `C2Novelty.md` lines 116-142 identifies the unquoted `xtract` helper and the counter's inability to detect false claims. The corrected r52 draft at `.ufo/waves/round-52/validate/corpus/knowledge/hyprland-synthetic-dispatch-r52.md` lines 27-30 changes P16–P18, but its own final table still needs a reviewer to establish truth. The current frozen claim correctly calls for an outside reviewer, but does not state a per-proposition verdict/receipt contract, freshness/identity of that reviewer, or resolution rule for dissent. Do not count structural counter success as coverage admission without recorded independent proposition-level source-truth review.

### S2 — C2 repair does not itself prove coverage expansion

**Attacked predicate:** frozen C2 says no expansion credit absent an admitted entry grounded in source opened this round and uncovered ground per coverage map. r52's own reports document held-ground overlap and source-row URL collisions: `.ufo/waves/round-52/w1/C2Novelty.md` lines 30-33 and `.ufo/waves/round-52/w1/C2PinAudit.md` lines 16-25. A repaired P16–P18 proposition binding demonstrates correction, not novel coverage. Require proposition-by-proposition mapping to the coverage map and independent confirmation of genuinely uncovered ground, distinguishing re-anchored/held claims from newly covered ground. This is consistent with the frozen limitation and should remain a gate, not be inferred from an accepted entry.

## Source truth and routed r52 defects

The frozen summary's P16 quote-spliced / P17 misattributed / P18 mislocalized routing is supported by the round-52 corpus and receipts: the corrected entry table at `.ufo/waves/round-52/validate/corpus/knowledge/hyprland-synthetic-dispatch-r52.md` maps P16 to ConfigActions.cpp:47-49, P17 to the surviving-null location, and P18 to the translator's key-not-found return; the same claims are reflected in `.ufo/waves/round-52/w1/C2CounterDraft.md` lines 246-254. These are local lane artifacts, not independent upstream verification by this seat. I opened no new external source; source truth remains subject to round-53's required independent review. No claims about runtime dispatch or host behavior are warranted.

## Verification gaps / method

No round-53 counter, final committed demonstration, frozen forgery fixtures, final C2 correction, source pins opened this round, or independent reviewer receipt were present in the inspected round-53 `w1/` directory at review time. Thus both claims remain provisional; no pass/fail verdict is justified. No semantic LSP device was available in this environment; conclusions cite local frozen artifacts and lane reports, not semantic search. Safety fence respected: no live probes, package queries, external fetches, producer execution, or source checkout mutation.

## Reproduction / evidence

Attacked predicates: C1 instrument-ledger accountability; C2 proposition-bound correction, independent truth review, and uncovered-ground expansion condition.

Exact inspection commands and outputs:
- `df -h /fast /tmp /home/vgpnk` → `/fast` 804G total, 208G used, 596G available; `/tmp` 128G total, 3.9G used, 125G available; `/home` 930G total, 307G used, 589G available.
- Read `/home/vgpnk/Projects/shokunin/mado-shokunin/SKILL.md` → lane forbids live reads, package queries, input capture, screenshots, producer execution and mutations this round.
- Read `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-53/claims-frozen.md` → C1 and C2 scope/limits as quoted above.
- `glob` round-53 `w1/` → only `R53Three22.md`, `R53One4.md`, `swarm-registry.json` existed before this report.
- Local source review: round-52 C2 correction table, C2Novelty, C2CounterDraft, C1CounterDesign, C1Simplify, and C2PinAudit artifacts cited above.

No source URL newly opened; therefore no new URL/date/quote claim. Scratch `/fast/scratch/hyaku/mado-r53/R53One3` created, no additional artifacts required; cleanup performed before yield.

Report: `.ufo/waves/round-53/w1/R53One3.md`
