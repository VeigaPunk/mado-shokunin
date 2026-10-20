# AttackC3Metric — round 16 w2: C3 literal counter, direction and lowest axis

Seat: `MadoR16.AttackC3Metric` (critic, read-only, lane-authored advice, not outside verification).
Read first: `corpus/lessons/round-15-verifier-spotcheck.md` (all 291 lines).
Method: I did **not** run `measure.py`, any gate, selftest, or live/host probe.
I reimplemented the two published regexes, `^[0-9]+\. ` and `^[0-9]+\. .*lessons/`, and
the round-12 resolver predicate (`.ufo/evidence/round-12/after-measure.sh:12`) in an in-memory
Python session. Inputs: `git show <rev>:corpus/QUALITY.md` for revisions
`5174e15 6e3b75f 95cbc41 32118fc 5f13870 32c4fda` and the working-tree QUALITY.md and lessons.
The working-tree values are **pre-commit** (QUALITY/LOG/SCORECARD modified; `corpus/lessons/round-16.md`
untracked, `git ls-files --error-unmatch` → 1). L1 must still measure the committed candidate.
No tools installed or updated.

Axes: calibration (C3 direction), the honesty of the lowest-axis selection, and the provenance of the counter.

## Re-derived numbers

| Revision | Literal (same-line) | Block (criterion body) | Literal ungrounded ids |
|---|---|---|---|
| `5174e15`/`6e3b75f` r12 | 11/16 = 6.8750 | 11/16 = 6.8750 | 1–5 |
| `95cbc41` r13 | 12/17 = **7.0588** | 12/17 = 7.0588 | 1–5 |
| `32118fc` r14 | 12/19 = **6.3158** | 14/19 = 7.3684 | 1–5, 18, 19 |
| `5f13870` r15 = `32c4fda` baseline | **12/20 = 6.0000** | 15/20 = 7.5000 | 1–5, 18–20 |
| working tree (21, 22 added) | **14/22 = 6.3636** | 17/22 = 7.7273 | 1–5, 18–20 |

Other readings for baseline → tree:
- Strict (excluding external-trap criteria 15–16, per QUALITY.md:26-30): 10/20 = 5.0000 → 12/22 = 5.4545.
- Duplicate or missing numbering: none (ids 1..22 contiguous).

**Direction verified: C3 improves, +0.3636 literal.** It also improves under the block reading
(+0.2273) and the strict reading (+0.4545). The 12/20 baseline matches MetricInflation:35 and
ClaimsSeparable:46. The 14/22 tree value matches MeasureBuild:28.

**Lowest axis verified.** Baseline scored active rows:
- calibration 6.0000 (7.5000 block)
- coverage, sourced current-art: 6/7 = 8.5714
- navigation: 10 (saturated)
- freshness, file-plane: 29/29 = 10 (spotcheck:142-143)
- operability, selftest: 372/372 = 10
- operability, finite subsets: 10/10

Depth and adjacency are unscored. Calibration is the lowest under every reading. After C1 lands
(coverage 10), calibration at 6.3636 stays lowest. So the correction at SCORECARD.md:719-723 is
right, and the "lowest active finite rubric" label for C1 at SCORECARD.md:696 is false. It is
superseded append-only, which is acceptable.

## Counterexamples

### F1 — High: round-16 lesson rows do not resolve under the round-12 delivered rubric's own row predicate

**Evidence.**
- The round-12 delivered C1 rubric is "counting only criteria whose cited paths and `#mistakes M<n>`
  rows resolve" (SCORECARD.md:286). Its resolver tests `grep -qE "^\| $m \|"` (after-measure.sh:12).
- Rounds 12–15 use a separate id cell, e.g. round-15.md:12 `| id | class | …`, rows `| M1 |`.
- `corpus/lessons/round-16.md:12-18` merges the cells: `| Id / class |`, rows `| M1 — host-safety … |`.
  The strict pattern `^\| M[0-9]+ \|` finds **0** rows in round-16.md, against 5/4/3 in rounds 13/14/15.

**Result.**
- Applied per cited file, criteria 21 (`round-16.md#mistakes M1`) and 22 (`#mistakes M3`) fail to resolve.
  The resolved count becomes 12/22 = **5.4545 < 6.0000**, a harm on the round-12 delivered reading.
- The original loop hard-codes `corpus/lessons/round-12.md`, so 21 and 22 pass only vacuously
  (round-12 has M1/M3). That is a resolver defect, not real resolution.
- ClaimsSeparable:60 ("rows M1 and M2 exist") checked existence, not this predicate.

**Smallest safe correction (L1, lesson is uncommitted).** Split the round-16 table header into
`| id | class | evidence | captured-by | fix |` with rows `| M1 | host-safety harm … |`. This
matches rounds 12–15. Content stays unchanged and the literal counter is unaffected.

### F2 — Medium: the C3 gain depends on criterion 21's first-line placement, and that is only half-disclosed

**Evidence.**
- QUALITY.md:82 puts `(lesson: lessons/round-16.md#mistakes M1/M2)` mid-sentence on line one,
  duplicating :95-96. adjudication.json:3 records that this was added for the counter.
- If 21 followed the wrapped style of 18–20, the literal value would be 13/22 = **5.9091**,
  a decrease from 6.0000. Criterion 22 alone gives 13/21 = 6.1905, and criterion 21 hoisted alone
  gives 13/21 = 6.1905. SCORECARD.md:732-733 states the "22 alone" independence but not the
  formatting counterfactual.

**Judgement.** This is not false provenance: M1/M2 exist and match the criterion's content.
It is a counter artifact, fixable by disclosure.

**Correction.** In the round-16 result, state that the literal +2/+2 holds only because the
citation sits on line one, and give the 5.9091 counterfactual.

### F3 — Medium: unreported historical calibration regression in r14 and r15

**Evidence.**
- The recorded literal rubric fell 7.0588 (r13) → 6.3158 (r14) → 6.0000 (r15), because criteria
  18–20 carry wrapped citations.
- SCORECARD.md:572-573 (r14, "calibration … no additional scored move and no retained harm observed")
  and SCORECARD.md:675 (r15, "calibration | unchanged") contradict the recorded rubric.
- The block reading rose over the same rounds (7.0588 → 7.3684 → 7.5000).
- Lesson M3 (round-16.md:16) frames the problem only as an omitted row, not as a regression.
  LOG/SCORECARD contain no `7.0588` or `6.3158`. MetricInflation:34 saw only the r15 step.

**Correction.** Append one sentence or an erratum in the round-16 SCORECARD C3 result giving the
literal series 6.8750/7.0588/6.3158/6.0000 at the four commits, with the block series beside it.
Do not rewrite the r14/r15 rows.

### F4 — Medium: QUALITY22 asks for literal and semantic counters reported separately; neither the probe nor the record does that yet

**Evidence.**
- QUALITY.md:102 says "Report literal versus semantic citation counters separately".
- measure.py:328-358 emits only the literal counter. LOG.md:1184-1185 says the semantic count is
  "not substituted"; not substituting is different from reporting.
- SCORECARD.md:731 has the result still pending.

**Correction.** The SCORECARD result must list:
- literal 12/20 → 14/22
- block 15/20 → 17/22
- strict 10/20 → 12/22

Each must be labelled, with the literal reading as the scored rubric. No measure.py change is
required. If L1 adds a field, it must be a separate key and never feed `calibration.score`.

### F5 — Low/Medium: lesson M3's promised red/green selection audit is not falsifiable as built

**Evidence.**
- round-16.md:16 promises a "red selection audit on the initial C1/C2-only declaration and green on
  the corrected".
- selection-initial.json and selection-corrected.json hold only `declared_axes` string lists.
  No tool, SKILL row or measure code references them (grep of tools/, measure.py, SKILL.md: none).
- A membership check would stay green if calibration were listed while not lowest.

**Correction.** Either record the per-axis rule, revision and value in the corrected JSON and audit
argmin, or downgrade M3's wording to "selection correction recorded". Do not claim an audit receipt
that was never produced.

### F6 — Low: provenance wording in criterion 22

QUALITY.md:102 says "PlanningWalk outside the L1's initial selection". PlanningWalk is a lane w1
seat, and round-16.md:75-77 says all seats remain the authoring lane. The phrase can be misread as
outside-lane provenance.

**Correction.** Write "lane seat PlanningWalk (w1), omitted from the L1's initial selection".

### F7 — Info: the "verbatim" label in the probe

measure.py:329 says "original published literal rubric, kept verbatim". It matches the
pre-registered command (SCORECARD.md:234) but drops the delivered resolver qualifier
(SCORECARD.md:286). At baseline both give the same set ({6..17}). After F1 is fixed, both give
14/22. Disclose this as "pre-registered command; delivered resolver qualifier not re-applied".

## Impacted axes

- **Calibration:** the direction holds on all readings except F1's resolver reading. That reading
  flips to harm until the lesson table is fixed.
- **Discernment/quality:** F2–F4 are disclosure items. Not fixing them would leave a rubric-gaming
  appearance and an unrecorded r14/r15 regression.
- **Coverage/operability:** untouched by this seat.

## Recommended checks for L1 (not run by me)

- On the committed candidate, run `python3 .ufo/waves/round-16/measure.py <rev>` and read the
  `calibration` block. Expect 14/22, with ungrounded ids [1,2,3,4,5,18,19,20].
- Run `grep -cE '^\| M[0-9]+ \|' corpus/lessons/round-16.md`. Expect 5 after the F1 fix (now 0).
