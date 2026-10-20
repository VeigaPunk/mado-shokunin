# CriticC1 — attack on round-17 C1 (calibration: one more lesson-cited criterion)

Seat: MadoR17.CriticC1 (critic, leaf, lane-dispatched; this is not outside review).
Date 2026-10-20. I read: corpus/lessons/round-16-verifier-spotcheck.md (required),
SCORECARD.md:821-865 (round-17 declaration @0175f13), corpus/QUALITY.md,
corpus/lessons/round-16.md:10-20,120-140 @27cd06f, .ufo/waves/round-16/evidence/
{frozen-tampered,action-selftest,action-selftest-final,action-frozen,action-frozen-final,calibration-readings}.json,
the fleet report .ufo/reports/round-16/mado.md:64, w1/spec.json items, and drafts
QualityDraft.md / LessonDraft.md (as they stood when read). Commands: git show/log, grep, python3 -c json reads.
Not run: any test/build/gate, pacman, sudo, jj, live probe. No tools installed or updated.

## Verdict

As declared, C1 is **count inflation unless three fixable defects are closed**. The criterion
text drafted (QualityDraft 23) names a real discernment that QUALITY 7/9/13 miss, but the
planned able-to-fail check (ReceiptLabelCheck spec) is weaker than the criterion, and as
specified would (a) go red on the seed for the wrong reason and (b) go green on an
R16-V1-class mutant. The metric itself rewards any appended numbered line carrying
`lessons/` on its first line, so the score move proves nothing on its own.

## Counterexamples

### CE1 — the literal counter measures placement, not discernment (impacted: calibration)
At 27cd06f and 0175f13: `grep -cE '^[0-9]+\. '` = 22, `... .*lessons/` = 14. The uncounted
criteria are 1–5 and **18, 19, 20** (QUALITY.md:43, 50, 72) — all three *do* cite lessons,
on a continuation line (:49, :55, :77). Re-wrapping those three so `lessons/` lands on line 1
gives 17/22 = 7.73 with zero new discernment; the planned +1 gives 15/23 = 6.52. The
round-16 semantic counter (`evidence/calibration-readings.json`) already reads 17/22 = 7.7273.
Tell: QUALITY21 (round 16) carries its citation on the first line *and* repeats it at :100-101;
the QualityDraft seat prompt mandates the citation on the FIRST line. Format is being driven by
the counter. Any criterion, discerning or not, moves the number (14/22 < 1).

### CE2 — QUALITY22 non-compliance in the declaration itself (calibration)
QUALITY22: "Report literal versus semantic citation counters separately". SCORECARD:829-847
declares only literal 14/22 → ≥15/23; no semantic baseline/target. Expected: semantic
17/22 = 7.7273 → 18/23 = 7.8261 under the round-16 block counter.

### CE3 — "≥ 15/23" admits cross-claim credit from candidate 24 (calibration, operability)
QualityDraft criterion 24 ("Candidate, not admitted: … (lesson: lessons/round-17.md#mistakes M2 …)")
is a single `^24\. ` line containing `lessons/`. If L1 appends it as numbered text, the literal
counter counts a self-described non-admitted candidate → 16/24 = 6.67, and calibration is
credited with C3's tripwire work, contradicting SCORECARD's own "C3 needs no note or criterion".

### CE4 — the label check, as specified, is red for the wrong reason (calibration)
Spec (w1/spec.json ReceiptLabelCheck): "asserts the doc line at that revision … contains both
the receipt basename and the token". At 27cd06f, round-16.md:131 is
`Input tamper control returns **2 snapshot_tampered**, retained in` and the basename
`frozen-tampered.json` is on **:132**. Seed (a) at line 131 therefore fails on the *doc side*
before the receipt is ever consulted. A MISMATCH would be printed, but it would not show the
R16-V1 discernment (receipt does not carry the token). "Shown able to fail" would be false
provenance unless the checker reports which side failed and the claim uses range 131-132.

### CE5 — substring-in-stdout goes green on an R16-V1-class mutant (calibration — strongest)
The red, superseded receipt `action-selftest.json` (measured 9dcf248, exit 1) contains
`frozen_match` 3× in stdout, including
`SELFTEST FAIL frozen-denied-match: want 0/frozen_match got 2/frozen_error`.
Mutant sentence: "the frozen denied plan returns `frozen_match`, retained in
`action-selftest.json`". The spec'd rule ("receipt JSON contains the token in its stdout/finding
fields") passes it — yet that receipt records frozen_match **failing**. Same for
`snapshot_tampered`: it appears 4× in both the red and the final selftest receipts, so a
token search cannot tell a superseded receipt from the current one. QualityDraft 23 correctly
says only the outcome/`got` side counts and the revision must match; the checker spec does
not implement that. Criterion and check disagree, so the check is not evidence for the criterion.

### CE6 — root cause sits in the receipt schema: exit-only matching (calibration)
`frozen-tampered.json` carries `"expected_exit": 2, "matched_exit": true` beside
`MADO_PLAN: frozen_error`. Exit 2 is shared by `frozen_error` and `snapshot_tampered`, so the
harness's own green flag hid the mislabel. The observable change a criterion should make is that
receipts cited for a verdict carry `expected_finding`/`matched_finding` (or a got-token), not
just an exit code. Neither draft names this.

### CE7 — the lane's own precedent rejects duplicate provenance criteria (calibration)
QUALITY.md:57-61 (R13-V2/V3) and :65-70 (R14-V1) routed receipt-application defects to existing
7/9/13, saying "No duplicate provenance criterion … is introduced". Reversing that precedent is
legitimate only if a non-author can see that 7/9/13 (and 19, retained-data field scope) all
*pass* round-16.md:131-132 while 23 fails it. My reading: 9 passes (receipt bound to 9dcf248),
13 passes (committed path), 7 not applicable, 19 is adjacent but scopes field class, not field
value. So a distinct discernment exists — but it has to be shown as a table, not asserted.

### CE8 — the new lesson would repeat the defect class (calibration, honesty)
LessonDraft M1 (and spot-check :169) say `snapshot_tampered` "is evidenced only by the final
fixture run `action-selftest-final.json`". The red `action-selftest.json` @9dcf248 also records
`SELFTEST PASS frozen-tampered-plan: want 2/snapshot_tampered got 2/snapshot_tampered` (and
`-policy`). The "only" is false; the tamper digest path worked at 9dcf248 in the selftest
fixtures; only the standalone frozen-tampered run hit the M6 pair defect first. Status-neutral
for C2/C1 but it must not be carried into lesson round-17 M1 unqualified.

## Is it calibration or inflation? What changes observably

It is a calibration improvement only if criterion 23 changes a decision a reviewer would make
that 1–22 do not, and that change is demonstrated by the check on real lane text. Observable
discernment change (the thing to show): a lesson/report sentence attributing a verdict token to a
receipt is rejected when the receipt's outcome field (stdout verdict line / `finding` / selftest
`got` side) differs, or when its `measured_commit` is not the revision the sentence describes —
where 7/9/13 accept it.

## What a non-author needs to see (acceptance)

1. Checker bytes committed, with a receipt carrying `measured_commit` and checker SHA-256.
2. Seed (a) at round-16.md:131-132 @27cd06f: doc side ok, **receipt side** MISMATCH, with the
   reason `got frozen_error, cited snapshot_tampered` printed.
3. Natural green: round-16-verifier-spotcheck.md:71-73 + `action-selftest-final.json` +
   `snapshot_tampered` ok via the `got` side of `frozen-tampered-plan`.
4. Mutant red (CE5): `frozen_match` ↔ `action-selftest.json` → MISMATCH (want-side only), and a
   superseded-receipt mutant (`snapshot_tampered` ↔ `action-selftest.json` cited for 1e31681
   content) → MISMATCH on revision.
5. Criterion table: 7/9/13/19 applied to :131-132 → pass; 23 → fail.
6. Both counters: literal 14/22 → 15/23, semantic 17/22 → 18/23; criteria 18-20 not re-wrapped;
   only criterion 23 credited to C1 (24 absent from numbered QUALITY text or excluded and stated).
7. Append-only erratum in round-16.md naming the superseded text at :131-132 and fleet report :64
   (QUALITY4), pointing at the TamperRecut re-receipt if it records `snapshot_tampered`.

## Smallest safe corrections

- Checker: parse the verdict, not substrings — first stdout line `MADO_PLAN: <token>` / JSON
  `finding`, or for selftest receipts the `got <exit>/<token>` of a named case; also compare
  `measured_commit` to the claimed revision; accept a line range; print the failing side.
- Add seeds per acceptance 3-4 (one natural green, two mutant reds).
- SCORECARD/report: add the semantic counter (QUALITY22); state C1 credits criterion 23 only.
- Keep candidate 24 out of `^[0-9]+\. ` QUALITY lines until it is admitted on its own lesson.
- Lesson M1: drop "only by the final fixture run"; say the standalone tamper receipt hit the M6
  pair defect, while selftest tamper fixtures returned `snapshot_tampered` at both 9dcf248 and 1e31681.
- Optional (CE6): criterion 23 asks that verdict-cited receipts record an expected verdict token,
  since exit codes are many-to-one.

Tradeoff for the judge (not fixable here): the literal rubric stays placement-sensitive by design;
even with all corrections, +1 criterion is a small score move whose value rests on items 2-5, not
on the fraction.
