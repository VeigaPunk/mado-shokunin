# Round 16 — OutsideLearning (w1): prior outside agreements and routed defects

Seat: `MadoR16.OutsideLearning` (connector, leaf, read-only). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Scope: map prior outside agreements and routed defects to grounded QUALITY criteria, and state what is still pending.
Status: **DRAFT. Not an outside review. Fresh non-author round-16 spot-check PENDING.**

## Limits of this seat

- Lane-dispatched (`MadoR16.*`). Per QUALITY 12 and the round-1 lesson, a mado-dispatched seat is not an outside reviewer. Nothing below is an outside agreement, and nothing here clears SHONEN.
- Source reading only: `read`, `glob`, `grep`. No `measure.py`, selftest, gate, build, package query, service, compositor, or input command was run. No `~/.omp/agent/agent.db*` or credential file was opened.
- No installs or updates. Tool record: none. `RULES.md` was not needed.
- No sibling or fleet file was edited. I did not read the sibling round-16 reports (`QualityGround.md`, `SafetyLearning.md`, etc.) to avoid duplicating their ownership.
- Anchors are the lines read at the time of this seat. L1 integration may move them.

## 1. Fresh outside review: status

**PENDING for round 16. Not satisfied by anything in the lane.**

- Round-16 has no non-author admit/reject sample, no source reopen, and no re-measurement. `SCORECARD.md:690-717` (Round 16 declared claims) states the round is an explicit operator round that "authorizes source-only learning, not host remediation or live-health clearance." It does not claim outside admission.
- The round-15 closure (`corpus/lessons/round-15-verifier-spotcheck.md`, verdict `rejected-harmed`) is a round-15 verdict. It says it "does not promote, mint or authorize a next round" (line 66-67). It does not cover round 16.
- The fleet L0 (`.ufo/l0-questions.md:53`, tsukuroi round-12) requires "spot-check one admit and one reject after lane landing, including source re-open: author-dispatched seats are advisory, so admission and SHONEN verification remain pending outside closure."
- SHONEN is unchanged: four `[~]` lines (`SHONEN.md:5,7,9,11`). No `[x]` exists, which is consistent with QUALITY 12.

## 2. Ledger of prior outside reviews

| Round | Non-author reviewer (anchor) | Agreed | Disagreed / rejected | Routed defect | Current status |
|---|---|---|---|---|---|
| 1 | none supplied (`round-1.md:19-22, 50-51, 117-121`) | — | — | Outside spot-check required; "Mado-dispatched L2s are not outside reviewers" (`.ufo/continuations/fleet-round-1.json:114`) | **OPEN.** No closure artifact in `corpus/lessons/` (no round-1 spotcheck file). Not closed here. |
| 10 | none recorded. Round-10 "non-author" seats are lane-internal (`round-10.md` spot-check block ~lines 163-172; synthesis line 35 "no non-author spot-check ever recorded") | — | — | none | **OPEN, historical.** Not an outside review per QUALITY 12. |
| 12 | kaika orchestrator (`round-12-verifier-spotcheck.md:8-13`; `round-12.md:114-125`) | U1 `window-rule-effects-getprop.md` admit; S012 reject | **S030** admitted as duplicate of S017 (same URL, same scope) | S030 duplicate admission | **GROUNDED → QUALITY 17** (`round-13.md` M1). S030 rejected in place; S045 correction. Red/green collision screen recorded in round-13. |
| 13 | hyaku closure (`round-13-verifier-spotcheck.md:178-183`) | U4 admit; "staging is a frozen stable API" reject; advertised-manager-proves-HDR reject; S045 correction | — | R13-V1 retained-data wording; R13-V2 within-run vs cross-revision boundary; R13-V3 selftest provenance | R13-V1 → **C19** (`round-14.md` M1). R13-V2 → **C7/C9** (`round-14.md` M2; standing-use clarification). R13-V3 → **C7/C9/C13** (`round-14.md` M3). All grounded; no new criterion added. |
| 14 | hyaku closure (`round-14-verifier-spotcheck.md:134-140`) | U5 admit; test-guarantees-apply reject; apply-guarantees-all-properties reject; HDR/luminance reject; S049 correction | — | R14-V1 ancillary receipt precision (line 169) | → **C7/C9/C13** plus `round-15.md` M1 correction. Standalone full-gate authority permanently withheld (`round-15-verifier-spotcheck.md:279-283`; `SKILL.md:493-496`). Grounded as a correction. |
| 14 (in-wave) | not outside: ReviewResolver / GateRecon findings adjudicated by the closure | — | — | regular-target false-green | **C18** (`round-14.md` M4). Grounded in in-round reviewer evidence, not outside disagreement. Its "from mined mistakes" label is accurate. |
| 15 | hyaku closure (`round-15-verifier-spotcheck.md:183-190`) | U6-route admit-local; list-devices defaults reject; seat/global inventory delivery reject; replay/recording-anonymous reject; R14-V1 correction admit; no-harm reject | — | R15-V1 host partial upgrade (lines 252-262); R15-V2 procedural (lines 263-278) | R15-V1 → operator, not a criterion (correct; see §3). R15-V2 → **C21** text (see §3); lesson citation dangling. |

Crosswalk of the round-15 pre-spot-check sample (`round-15/w1/reports/GateDecisions.md:77-83`, rows pending) to the round-15 closure:

- U6-1 (admit conditional on S007 superseding row) ↔ closure row 1: **agree**. S051 supersedes S007 (closure line 207-208).
- U6-2 (list-devices proves applied settings) ↔ closure row 2: **agree**, same source sentence.
- U6-3 (debug-events/record shows client delivery) ↔ **not individually sampled**. Closure row 3 covers seat/global inventory, a related but distinct claim. Analogous only.
- V1-1 (explanatory correction) ↔ closure row 6: **agree**.
- V1-2 (receipts not standalone full-gate receipts) ↔ closure row 6 scope clause: **agree**, analogous wording.

The round-15 closure is one non-author sample of six rows. It supports "discernment improved" only for the sampled rows.

Independence limit: the round-13, round-14 and round-15 closures are all the same "hyaku" closure persona (non-author of mado, but not independent of each other). The round-12 closure was the kaika orchestrator. These are non-author checks, not a multi-reviewer panel.

## 3. Routed defects → grounded criterion status

| Routed defect | Source | Grounded where | Status |
|---|---|---|---|
| R15-V2: keep new-only dry-run in every seat context; hard-coded fixtures are not package validation; carry the no-live-probe breach | `round-15-verifier-spotcheck.md:263-278` | `QUALITY.md:80-96` (C21: "Carry the pause and this round's no-live-probe scope into every seat context"; "a hard-coded new-only fixture never proves it ran"). `SKILL.md:483-491`. | **Grounded in text. Citation dangling.** C21 cites `lessons/round-16.md#mistakes M1/M2`. **That file does not exist at read time** (`corpus/lessons/round-16*` glob empty). See §4. |
| R15-V1: unresolved forbidden partial upgrade | `round-15-verifier-spotcheck.md:252-262`; L0 `.ufo/l0-questions.md:54` (orchestrator) | Not a criterion. Held by C21 + `SKILL.md:39-44, 483-491` (pause, no clearance). | **OPEN, operator-owned.** Correctly not a criterion. L0 line 54 offers three recovery options; none chosen. |
| Operator-pause request | `.ufo/l0-questions.md:55` (tsukuroi, round-15): "consider a host-wide pause on all pacman transactions until an operator-owned recovery/update plan clears the mkinitcpio42 hook compatibility risk" | Round-16 contract ("All pacman transactions PAUSED host-wide until operator recovery decision"); L0 line 57 (kaidoku) records the pause as in force. | Pause in force by contract. The underlying recovery decision remains operator-owned and unanswered in the L0 file. |
| **tsukuroi L0 critique of the dry-run guard** | `.ufo/l0-questions.md:55`: "The installed-name dry-run guard is necessary but not clearance: all-new targets can still combine newer binaries with unversioned older dependencies, and `--needed` is not a no-upgrade switch." Also: host is 413 packages behind its sync DB (`:54`, `:55`). | **Not grounded.** C20 (`QUALITY.md:72-78`) requires name-overlap on the real `-Sp` plan and treats it as sufficient. C21 defers to a future operator lift. Neither states that the guard is necessary-not-sufficient, that `--needed` is not a no-upgrade switch, or that a plan computed against a 413-behind sync DB is not a no-partial-upgrade proof. | **OPEN, ungrounded in criteria.** Proposed handling in §5 (lesson note and lift precondition, not a new criterion yet). |
| S006/S008/S009/S010 owed anchors | `round-12.md` search-log errata; `round-15/w1/reports/GateDecisions.md` U6-6 | S006 superseded by S042 (round-13). S008, S009, S010 still `queued` with access date only. | **OPEN** (source debt; C2 and C5 apply, no new criterion). |
| Legacy mado round-1 namespace/dispatch L0 question | `round-15-verifier-spotcheck.md:285-286` | — | **OPEN, operator-owned.** |

Lesson-to-criterion integrity checks (anchors read):

| Criterion | Cited lesson anchor | Present at read time? |
|---|---|---|
| C17 | `lessons/round-13.md#mistakes M1` (`round-13.md:10`) | Yes |
| C18 | `lessons/round-14.md#mistakes M4` (`round-14.md:17`) | Yes |
| C19 | `lessons/round-14.md#mistakes M1` (`round-14.md:14`) | Yes |
| C20 | `lessons/round-15.md#mistakes M2` (`round-15.md:15`) | Yes |
| C21 | `lessons/round-16.md#mistakes M1/M2` (`QUALITY.md:95`) | **No.** `corpus/lessons/round-16*` does not exist yet. |
| C12 (SHONEN gate) | `lessons/round-12.md#mistakes M9` (`round-12.md:21`) | Yes. SHONEN still four `[~]`, no `[x]`. |

## 4. Integration blockers (for L1, not fixed here)

1. **Dangling citation.** `QUALITY.md:95` and `SKILL.md:44, 490` cite `corpus/lessons/round-16.md` M1/M2. The file does not exist at read time. Until it lands, C21 is grounded in text only, and its lesson anchor is unverifiable.
2. **Unverified registration claim.** `QUALITY.md:98` says "The runnable check and its failure evidence are registered in SKILL.md." At read time, `tools/mado-action-plan*` does not exist, and `SKILL.md` has no `mado-action-plan` row (grep for `mado-action-plan|mado-round16` returned no matches). `.ufo/waves/round-16/measure.py` exists. The SCORECARD round-16 claims (`SCORECARD.md:703-709`) name `tools/mado-action-plan.py`. Either the tool and the SKILL row land before integration, or line 98 and the SCORECARD command must not claim registration. This seat did not verify the tool's behavior.
3. **Round-16 outside remains pending.** Any round-16 admission claim must say so. Round-15 agreement must not be carried forward as round-16 agreement.

## 5. Recommendations (proposed; L1 owns the files; no edits made here)

- **R-A (blocker).** Land `corpus/lessons/round-16.md` with `## Mistakes` rows M1 (R15-V2 procedural: hard-coded fixture ≠ validation; no-live-probe carry-forward) and M2 (R15-V1 host pause/process) before integration. Cross-check that each C21 claim maps to a row.
- **R-B (blocker).** Land the classifier and its SKILL registry row, or remove the "registered in SKILL.md" wording at `QUALITY.md:98` and the matching SCORECARD round-16 sentence. Do not claim registration that the tree does not show.
- **R-C.** Record tsukuroi's L0 critique (`.ufo/l0-questions.md:55`) in lesson M2 or as an explicit precondition in `SKILL.md:483-488`: a future operator lift requires (i) the operator's recovery decision, (ii) a sync-database state that the operator has reconciled, and (iii) a real `-Sp` plan with complete installed-name comparison. State that `--needed` is not a no-upgrade switch and that the overlap guard is necessary, not clearance. **Do not add a new QUALITY criterion yet**, following the round-14 V1-4 precedent: add one only after a failure mode criteria 20/21 cannot catch is observed.
- **R-D.** Keep SHONEN at four `[~]`. Round 16 is pending the fresh outside closure. State "outside review pending" in the round-16 SCORECARD/LOG entries.
- **R-E.** The next outside closure should sample at least one round-16 admit and one reject, reopen the source, and re-measure C1/C2. Non-mado-dispatched only.
- **R-F.** Carry forward open debts (§3): round-1 outside spot-check, S008/S009/S010 anchors, the legacy round-1 L0 question, and R15-V1.

## 6. Anchors summary

- Round-15 closure: `corpus/lessons/round-15-verifier-spotcheck.md` lines 11-14, 66-67, 183-190, 207-208, 252-262, 263-278, 279-283, 285-286.
- Round-14 closure: `corpus/lessons/round-14-verifier-spotcheck.md` lines 134-140, 169.
- Round-13 closure: `corpus/lessons/round-13-verifier-spotcheck.md` lines 178-183, 201-205.
- Round-12 closure: `corpus/lessons/round-12-verifier-spotcheck.md` lines 8-13; `corpus/lessons/round-12.md` lines 114-125.
- Round-15 pre-closure sample: `.ufo/waves/round-15/w1/reports/GateDecisions.md` lines 77-83.
- Criteria: `corpus/QUALITY.md` lines 32-34 (C17), 41-61 (C18-19), 63-78 (C20), 80-100 (C21).
- Lessons: `corpus/lessons/round-13.md:10`, `round-14.md:14,17`, `round-15.md:15`.
- SKILL: `SKILL.md:39-44`, `473-491`, `493-496`.
- SHONEN: `SHONEN.md:5,7,9,11`.
- SCORECARD round 16: `SCORECARD.md:690-717`.
- Fleet L0: `.ufo/l0-questions.md:53, 54, 55, 57`.
- Fleet round-1 continuation: `.ufo/continuations/fleet-round-1.json:114`.
