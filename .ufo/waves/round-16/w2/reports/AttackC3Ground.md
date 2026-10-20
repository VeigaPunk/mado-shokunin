# AttackC3Ground — round 16 w2, C3 calibration grounding

Seat: `MadoR16.AttackC3Ground` (reviewer, leaf member, no subagent dispatch, no commits, no installs).
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
Scope: attack QUALITY criterion 22 (grounding on M3), the actual planning error, lesson-path independence, and preservation of the original literal rubric.
Method: source reading only. Read-only `git show`/`git diff`, `grep` and `sed` counts over committed or worktree bytes. Nothing executed: no `measure.py`, no gate, no selftest, no build, no package, service, compositor, input or producer command. Counts below are hand or grep counts; expected `measure.py` values are predictions for L1 to confirm.

## Verdicts

| Question | Verdict | Anchor |
|---|---|---|
| Criterion 22 grounded on M3 | PASS | `corpus/QUALITY.md:106` cites `lessons/round-16.md#mistakes M3`; the M3 row exists at `corpus/lessons/round-16.md:16` and states the same error |
| M3 describes the actual planning error | PASS for round 16, PARTIAL overall | `selection-initial.json:3-6` declares `[coverage, operability]`; `SCORECARD.md:696` says coverage is lowest; corrected at `SCORECARD.md:719-735`. M3 omits the round-15 recurrence and its cause (see F3) |
| Independent lesson path | PARTIAL | C2 (criterion 21 → M1/M2) and C3 (criterion 22 → M3) cite disjoint rows, and U7 cites no lesson. But "outside" is wrong, the cited evidence seat is lane-dispatched, and the red/green falsification M3 promises has no artifact (F1, F2, F5) |
| Original literal rubric preserved | PASS | Details below |
| Literal fraction improves with QUALITY21/22 | PASS, with a layout caveat | 12/20 → 14/22 (6.0000 → 6.3636); the gain depends on criterion 21's citation sitting on its first line (F4) |

## Rubric preservation (verified)

- `SCORECARD.md:234` (round-12 calibration row) and `:286` (round-12 C1 result row) are unchanged from baseline text. Both still say `grep -cE '^[0-9]+\. .*lessons/'` over `grep -cE '^[0-9]+\. '`.
- `git diff 32c4fda -- corpus/QUALITY.md` is append-only: hunk `@@ -76,3 +76,31 @@`. Criteria 1–20 are byte-unchanged; criteria 21 and 22 are added after line 76.
- `measure.py:343-344` uses the same two regexes as the round-12 published grep. Denominator includes criteria 1–5, as the published rule requires. Its C3 block (`measure.py:328-358`) is observation only and is not folded into coverage.
- Counts (grep over bytes, reproduced against the regexes):
  - `32c4fda` (baseline): numbered 20, literal 12 (ids 6–17) → **6.0000**.
  - `ea0446f` (round-15 baseline): numbered 19, literal 12 → **6.3158**. Matches MetricInflation.md:34.
  - Worktree (uncommitted, 22 criteria): literal ids `6–17, 21, 22`, 14/22 → **6.3636**.
- Lowest-axis correction is explicit: `SCORECARD.md:721-725` supersedes the coverage-lowest assertion and retires nothing. Calibration stays below coverage 8.5714 on every reading.

## Findings

### F1 — HIGH — M3's promised red/green selection audit does not exist

- `round-16.md:16` (M3 "Fix and falsification") says: "Demonstrate a red selection audit on the initial C1/C2-only declaration and green on the corrected C1/C2/C3 declaration."
- `grep` for `selection.*(audit|red|green)` across the lane and the fleet `round-16` tree returns no audit artifact. `selection-initial.json` and `selection-corrected.json` are static `declared_axes` lists with no predicate, no pass/fail and no script. `measure.py` never reads them.
- The round-16 lesson appends receipts only for M1 ("Exact observed receipts are appended below"); no receipts follow the M3 row.
- Consequence: criterion 22 is grounded on a lesson row whose stated falsification has no evidence. Criterion 22 itself does not require the audit, but the lesson does.
- Fix (L1): either run and commit a deterministic red-initial / green-corrected selection check, or amend M3 by append-only erratum to say the audit was not performed and the grounding rests on the counts.

### F2 — HIGH — the cited evidence seat mislabels its calibration figure as "literal"

- `.ufo/waves/round-16/w1/reports/PlanningWalk.md:17` and `:25` report "16/21 = 7.6190 literal upper bound" and "Criteria 6–21 each carry a (lesson: …) citation (16 of 21). Literal rubric: 16/21."
- That count treats criteria 18, 19 and 20 as grounded. Their citations sit on wrapped continuation lines (baseline lines 49, 55, 77), so the literal same-line rule does not see them. The literal value for the state PlanningWalk describes (21 criteria, criterion 21 still wrapped) is **12/21 = 5.7143**. With criterion 21 relocated to its first line, it is **13/21 = 6.1905**.
- `PlanningWalk.md:28` and `:103` then assert "7.6190 is an upper bound" for the literal reading. That bound holds only for the block reading.
- Same wave, correct separation: `MetricInflation.md:32-36` gives literal 12/21 = 5.7143 and block 16/21 = 7.6190; `ClaimsSeparable.md:46-49` gives literal and block separately.
- QUALITY criterion 22's second sentence ("Report literal versus semantic citation counters separately") is violated by the seat it cites.
- Risk: L1 transcribes 7.6190 into the SCORECARD result. The delivered literal value is **14/22 = 6.3636** (block 17/22 = 7.7273, hand count). Neither 7.6190 nor 16/21 should appear as literal.
- Fix: correct `PlanningWalk.md` §1 row and §2 bullet by append-only erratum; L1 records only committed `measure.py` output.

### F3 — MEDIUM — M3 omits the round-15 recurrence and its root cause

- `.ufo/waves/round-15/w1/reports/PlanningWalk.md:27` reports calibration "12/17 = 7.0588" and cites `corpus/QUALITY.md:6-38`.
- At `ea0446f` criteria 18 and 19 sit at lines 43 and 50, outside that range. The file has 19 numbered criteria; the correct literal is 12/19 = 6.3158 (MetricInflation.md:34 agrees).
- So round 15 already had calibration below coverage (round-15 coverage 7.1429). The round-15 walk also declared coverage "uniquely lowest" (its §1.2), contradicting its own table.
- Root cause: a range-truncated read of a numbered file. M3 records only the round-16 omission. Its "Captured-by" does not name the truncated read.
- Fix: M3 erratum recording the round-15 instance and cause, and a rule that counters read the whole file (`grep` over the full file, not a line range).

### F4 — MEDIUM — the literal gain depends on the layout of criterion 21

- Counterexample (bounded): with criterion 22 present and criterion 21's citation on its wrapped line (its pre-fix placement, `ClaimsSeparable.md:60`), literal = 13/22 = **5.9091 < 6.0000**. C3 would then report a decrease while a lesson-grounded criterion was added.
- The delivered increase exists only because criterion 21's citation was moved to line 82 (`QUALITY.md:82`) after the literal reading showed −0.2857 (`ClaimsSeparable.md:57`, fix at `:95`; accepted at `adjudication.json:3`). The criterion's text is otherwise unchanged. The relocation is a formatting edit made in response to a counter reading, so it must be disclosed as such.
- The SCORECARD says "Criterion 21 also carries its own lesson on its first line" (`SCORECARD.md:732`) but does not say the move was motivated by the counter, and does not name criteria 18–20 as lesson-grounded but literal-blind (wrapped citations at baseline lines 49, 55, 77).
- Fix: SCORECARD must state (a) the relocation and its motive, (b) that 18–20 are literal-blind, (c) that the literal delta is wrap-sensitive. Do not present the 6.0000 → 6.3636 delta without these.

### F5 — MEDIUM — C2/C3 coupling on the calibration object is under-disclosed

- With criterion 21 first-line: criterion 21 alone gives 13/21 = 6.1905 (+0.1905), and criterion 22 alone gives 13/21 = 6.1905 (+0.1905). Both together give 14/22 = 6.3636 (+0.3636).
- `SCORECARD.md:732-733` states only that 22 alone still increases calibration if C2's criterion is removed. That is true, but C3's measured delta is also obtainable from C2's criterion alone. The SCORECARD's separability sentence (`:711`) does not mention calibration.
- `ClaimsSeparable.md` §2.2 documents the coupling; the SCORECARD does not carry it forward.
- Fix: SCORECARD records that both criteria move the same calibration object, with the per-criterion deltas above.

### F6 — LOW — "outside" is inaccurate and the cited path has no anchor

- QUALITY `:106` says "PlanningWalk outside the L1's initial selection." PlanningWalk is `MadoR16.PlanningWalk`, a lane-dispatched w1 seat in the same authoring lane and wave. The lesson header (`round-16.md:1`) reads "L1 + lane-dispatched L2 advice". QUALITY criterion 12 says a lane-dispatched seat is not independent clearance. The lesson's own outside spot-check is still "pending" (`round-16.md:75-77`).
- Three w1 seats (PlanningWalk, ClaimsSeparable, MetricInflation) reached the same selection conclusion. That is intra-lane agreement, not outside verification.
- QUALITY criterion 2 requires a measured anchor. M3 and criterion 22 cite the seat by name only.
- Fix: criterion 22 wording becomes "lane-dispatched PlanningWalk seat (`.ufo/waves/round-16/w1/reports/PlanningWalk.md` §2), not L1; no non-author verification." Keep the anchor in the lesson.

### F7 — LOW — criterion 22 has no fallback for execution-bound rubrics, and "active" is undefined for unscored axes

- Criterion 22 requires re-deriving every active axis "under its recorded counting rule." Operability (selftest) and freshness (file-plane gate) require execution, which this round forbids. PlanningWalk §1 used last-recorded round-15 values ("not re-run (no-check rule)").
- Depth and adjacency are "unscored: no bounded rubric exists" (`SCORECARD.md:239-240`). Whether they are "active" is undefined.
- Fix (append-only criterion text): where a counting rule requires a forbidden execution, record the last-measured value with its date and label it not re-derived; define "active" for unscored axes.

### F8 — LOW — the block reading is not produced by the committed counter

- `measure.py` emits only the literal reading. Block values (7.5000 baseline; 7.7273 delivered by hand count) live only in `ClaimsSeparable.md`.
- If the SCORECARD records block values it must label them as seat observations, or the counter must be extended under a separately named reading.

## Expected values for L1 (not executed here)

Run `python3 .ufo/waves/round-16/measure.py <rev>` at the baseline and at the committed delivered revision. Expected `calibration` fields:

- baseline `32c4fda`: `criteria_total` 20, `lesson_grounded` 12, `ids` 6–17, `score` 6.0;
- delivered (after commit of criteria 21–22, with 21's citation on line 82): `criteria_total` 22, `lesson_grounded` 14, `ids` 6–17, 21, 22, `score` 6.3636.

Confirm the worktree equivalents with the grep counts above before commit. QUALITY is uncommitted; `measure.py` reads only committed bytes, so commit first.

## Limits

- This seat did not run `measure.py`, so all counts are grep or hand counts over the same regexes. Python `re` and `grep -E` equivalence for these patterns is reasoned, not executed.
- The delivered calibration numbers are worktree counts; they bind only after commit.
- I did not assess criteria 18–20's lesson content, only their literal-counter visibility.
- No finding touches C1 coverage or C2 gate behavior, which are other seats' scope.

## Tooling record

No tools installed, updated or removed. No `pacman`, package query, service, compositor or input command was run. Only `git show`, `git diff`, `grep`, `sed` and `ls` over lane and fleet files.
