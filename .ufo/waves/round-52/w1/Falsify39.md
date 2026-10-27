# Falsify39 — C2 held-ground novelty

## Deliverables
- This report: `.ufo/waves/round-52/w1/Falsify39.md`

## Attack
- **Item/predicate:** C2 coverage, frozen registration §Frozen predicates: new indexed entry absent at base must produce `TARGET_MISSED`; the no-work control must test a distinct new target slug.
- **Concrete named control hazard:** reusing the round-51 target selector/slug as the round-52 no-work control. The base contains the prior dispatcher entry, so this selector can pass without any round-52 work. This is not a hypothetical semantic distinction: the frozen receipt `.ufo/waves/round-52/receipts/c2-base.txt` reports for `rev=85d57a818c3707397e21c840b6498b105ba798aa`: `a ok=1 index_row=knowledge/hyprland-dispatcher-dispatch-r51.md`, then `clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET` (exit 0). Registration §Frozen controls explicitly says this old-counter receipt is not trusted for C2 because the preceding entry already exists and the new counter must name a separate slug.
- **Reproducible evidence/setup:** read the committed frozen control definition `.ufo/waves/round-52/controls/c2-do-nothing.md` alongside the base receipt. The control states the claimed *new* entry is absent; the receipt demonstrates that a selector aimed at the existing R51 entry yields `TARGET_MET` on that same base. No source code, tracked files, or control bytes were changed; no detector was available/ran here to test whether the proposed R52 counter actually has this selector defect.
- **Actual result:** observed existing base receipt output above: `TARGET_MET`, exit 0 for R51 slug. Control definition says new R52 target absent and must miss.
- **Reproduced:** **yes**, for the named stale-selector control hazard; **not established** for any R52 counter implementation. This is a control/coverage attack, not a claim or predicate amendment.

## Limits / source provenance
No new external source candidate or source truth claim. Read only the frozen R52 claim/registration/control/receipt and the prior R51 entry/lesson for context; no web access, package query, producer execution, or live host read. Since the R52 counter and target entry were not available in the accessible round artifacts, the stale-selector attack is not a mutation of that detector; its verdict against the frozen C2 implementation is **inconclusive**. No scratch files or tools installed.

## Report trailer
[Report]
.ufo/waves/round-52/w1/Falsify39.md
