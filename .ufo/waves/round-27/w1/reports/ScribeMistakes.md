# ScribeMistakes — round 27 findings

## Scope and provenance

Read-only source review of `corpus/lessons/round-26-verifier-spotcheck.md`, `corpus/lessons/round-26.md`, and `corpus/QUALITY.md`. The draft rows are at `.ufo/waves/round-27/drafts/mistakes.md`. No product code, QUALITY policy, or lesson file was edited. No tool was installed. No gate, build, test, or checker was run; the findings below are from the committed spot-check and lesson text, not fresh executions.

The draft contains the four requested findings and one directly related M26-8 row on the surviving population-checker mutants. Each row records whether a checker failure was actually evidenced. Main criterion mapping:

- The unsupported SCORECARD claim that `check-population.py` passed on both after-receipts maps to QUALITY 13’s committed-evidence rule. QUALITY 37 defines population equality but does not establish that the claimed after-receipt runs exist.
- The stale PROVINCE environment-seeding sentence is covered only indirectly by QUALITY 28, which applies after a present-tense supersession is identified. For the specified missing link from behavior-changing tool edits to their corresponding PROVINCE row, the draft says `none`; the rule does not expressly require that crosswalk.
- The three absent SKILL registry entries have no general QUALITY criterion. QUALITY 36 concerns control evidence/order, not universal SKILL registration. The sentence near QUALITY 21 is local to that criterion, not a general registry rule.
- The Q36 successor’s rejection of actual `.txt` receipts has no exact existing criterion requiring acceptance of its own round’s receipt paths. QUALITY 36 is related, but specifies negative chronology/shape behavior rather than a positive current-format run.
- QUALITY 37 is the normative population contract for MutQ37, but the round-26 mutation evidence shows that the checker/suite did not enforce all of it: three of six probes survived.

The proposed criterion treats gate registration and positive current-round-format acceptance as one gate-delivery requirement. This is the most systemic uncaught gap in the requested set: all three landed gates lacked registry rows, and the Q36 successor rejected valid receipts in its own round.

## Evidence and observed limits

The round-26 verifier spot-check reports that the SCORECARD’s `check-population.py` pass sentence has no committed run for the two after-receipts; the existing red/green file covers base receipts only (`corpus/lessons/round-26-verifier-spotcheck.md:146-148`). It reports the PROVINCE line `:36-39` still says the tool seeds from the process environment, while round-26’s `a496b02a` tool no longer references `environ`; an environment-using probe produced three binds rather than the round-25 tool’s four (`:107-119`). The same spot-check lists no SKILL row for `counter-selftest.py`, `check-population.py`, or `check-control-receipts.py` (`:138-148`). It reports that the Q36 successor expects `controls/*.md` and exits 1 on round-26 `.txt` receipts; round-26 M26-8 records the same defect and the 17-second valid chronology (`corpus/lessons/round-26.md:32`). The spot-check also records that three of six MutQ37 mutants survive (`corpus/lessons/round-26-verifier-spotcheck.md:143-144`).

The coredump count was read before and after this report task with the required command, `timeout 15 prlimit --as=4000000000 -- sh -c 'coredumpctl list --no-pager --no-legend | grep -c /usr/bin/Hyprland'`: before `1338`, after `1338`, delta `0`. No Hyprland was started. No new run was performed to decorate the report, and there are no claims here that the unrun gates passed.

## Affected surfaces and out of scope

Written outputs only: `.ufo/waves/round-27/drafts/mistakes.md` and `.ufo/waves/round-27/w1/reports/ScribeMistakes.md`. No source, gate, registration, QUALITY, or lesson file was changed. The proposed criterion is a draft, not an adopted QUALITY change. The report does not re-verify any round-26 receipt or independently measure the tool behavior; those observations remain attributed to the cited verifier spot-check and lesson.
