# RevTrendDiscernment — round-30 discernment trend verdict

Advisory seat report. Not admission, not a closure verdict, not a mutation of any artifact.

Scope: attack the round-30 `discernment` trend verdict (report only). Three questions put to
this seat: (1) are M30-1/M30-2 real mined mistakes with `captured-by='none'` honestly stated;
(2) does criterion 52's fix demonstrate it can fail; (3) verify the outside-spot-check
disclosure (none at report time).

Revision reviewed: lane `274f735` (lane moved during review: `92d3c86` → `d72243e` → `2db0c44`
→ `15ddd7d` → `a0dd664` → `274f735`; findings re-checked at the last). Fleet report
`bbae16bf` at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/mado.md`.

Method note: no `lsp` device is exposed to this seat and no language server applies to these
Markdown/record artifacts, so semantic checks were made by executing the canonical counters
over committed bytes (`git show`) and reading the named artifacts — not by text grep. The C2
counter was run at `8f51071b`, `446dc39`, `15ddd7d`, `274f735` with both the frozen blob
(`451e8b3`) and the repaired blob; outputs are byte-identical (see §Verified holds).

---

## Verdict on the verdict

`discernment — improved` is **not established by its stated evidence**, and at write time it
was **premature**. It is **narrowly supportable only after the fact** by the outside
spot-check's agreement on the round's single new gate decision (S185 admit), with two
qualifications (standing reject leg, unresolved S185 quote defect).

- The fleet report's basis is `mado.md:132-136`: "M30-1/M30-2 are honest self-mined mistakes
  with `captured-by` gaps named and fixes demonstrated; criterion 52 grounds the
  record-then-claim discipline … Outside non-author spot-check … rides the closure pass."
- `LEARNING.md:31-35` defines the observable: *"gate decisions vs the outside spot-check;
  `QUALITY.md` criteria"*; `improved` when *"the spot-check agrees with the gate on admits
  and rejects, or a disagreement becomes a lesson that adds a grounded `QUALITY.md`
  criterion."* Self-mined mistakes plus demonstrated fixes are **calibration/record**
  evidence, not this observable. Criterion 52 codifies a practice the round already followed;
  no outside disagreement became a criterion this round (the wave findings are routed to
  round 31 — `corpus/lessons/round-30.md:56-71`).
- Timing: report commit `bbae16bf` is 2026-10-24 04:00:43; the outside spot-check commit
  `d72243e` is 04:03:37. The report says the sample "rides the closure pass" — an implicit
  disclosure that none existed yet — but states the verdict as final.
- Post-hoc the sample agrees on the S185 admit and on S062, but S062 is a **standing** reject,
  not a round-30 decision; round 30 made no reject decision (`corpus/lessons/round-30.md:30`,
  "no new rejection considered"). `LEARNING.md:42-46` asks for a sample of *that round's*
  gate decisions, at least one admit and one reject. The reject leg is precedent (r29 did the
  same) but is not literally this round's decision.

**Recommended correction (report only):** keep `improved` only as *narrow* — "outside
spot-check agrees on the round's only new gate decision (S185 admit); no round-30 reject
exists (standing S062 used, disclosed); the self-mined-mistakes / criterion-52 material is
calibration/record evidence, not discernment" — or report `unchanged` for the self-mined
part and credit only the outside agreement. Do not cite M30-2 as self-mined.

---

## Findings by severity

### HIGH

**H1. M30-2 is not a round-30 mined mistake; the trend's "self-mined" basis is inflated, and
the outside spot-check repeats the claim.**

Evidence:
- Round-30 registration §Routed queue item 1 routes the index gap **from**
  `corpus/lessons/round-29-verifier-spotcheck.md`:
  `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-30/registration.md:10-15`.
- M30-2's own evidence cell says the round-29 sweep row "records the navigation counter at
  41/43 … and correctly routed it instead of repairing under the table"
  (`corpus/lessons/round-30.md:14`). A defect already recorded and routed in round 29 is not
  mined in round 30.
- The r29 spot-check names the routing explicitly: "Round 30: close the inherited
  coverage-index gap by adding index rows for `mutation-testing-r28.md` and
  `workspace-rules-r27.md`" (`corpus/lessons/round-29-verifier-spotcheck.md:85-87`).
- The fleet report itself calls it inherited in one line — "M30-2 (the index gap's two-round
  persistence — the sweep recorded it, no gate caught it)" (`mado.md:116-118`) — then calls
  both "self-mined" in the trend line (`mado.md:132`).
- The outside spot-check verbatim repeats the trend line: "M30-1/M30-2 are honest self-mined
  mistakes" (`corpus/lessons/round-30-verifier-spotcheck.md:88`). It did not check provenance.

Convention check: carried defects keep their original round id in this corpus — r28 carries
`M27-3`, r29 carries `M27-4` (`corpus/lessons/round-28.md:11`,
`corpus/lessons/round-29.md:14`). M30-2 assigns a new round-30 id to a round-29 finding,
which is the one convention break.

Impact: the discernment basis is **one** honest self-mined mistake (M30-1), not two. The
outside check's discernment line inherits the error, so the "outside agreement" on the
mistakes leg is circular.

---

### MEDIUM

**M1. M30-1's `captured-by='none'` is honest, but its `MINT.md` ground is false.**

Verified honest parts:
- No gate required per-criterion citation: criterion 22 audits axis/rubric *selection*
  (`git show 8f51071b:corpus/QUALITY.md:107-110`); `tools/mado-verify.sh` contains no
  `QUALITY` check (`grep -n QUALITY tools/mado-verify.sh` → no match); the literal rubric is a
  measurement, not a gate.
- The base red reproduces exactly: literal 28/40 = 0.7000, active 39, resolved 31 = 0.7949,
  `UNRESOLVED criterion 1..5, 38..40`, `TARGET_MISSED`, exit 1 (I ran the frozen counter at
  `8f51071b`; same bytes as `controls/C2K1-donothing.txt`).
- Criteria 18/19/32 do cite only on continuation lines at base (e.g. `QUALITY.md` base
  line 43 starts criterion 18; its `(lesson: …)` is line 49) — M30-1's description is
  accurate.

The defect: M30-1 says "The seed block's true ground is `MINT.md`, never recorded"
(`corpus/lessons/round-30.md:13`), and criteria 41–45 repeat "its grounds are `MINT.md` (the
mint evidence…)" (`corpus/QUALITY.md:347-351`). `MINT.md` contains **no** admission bar at
the mint commit `74d3b7b` or at base `8f51071b`: it is 20 lines of cause / two demand
instances / roster scan / domain boundary (`git show 74d3b7b:MINT.md`; `git show
8f51071b:MINT.md`). The five seed rules are the fleet-wide generic "Admission bar (probation
draft)" (`corpus/QUALITY.md:1`) present in at least six lanes (`tameshi`, `tsukuroi`,
`tabi`, `mori`, and others), i.e. a mint-template artifact, not a MINT.md statement.

The C2 counter cannot see this: it checks file existence, anchor substring and M-id presence
(`count.py:138-160`), and the resolving citation for rows 41–45 is
`lessons/round-30.md#mistakes M30-1` — so 40/40 is syntactically true while the prose
provenance is unsupported. The lane's own addendum acknowledges the adjacent circularity
("resolvability ≠ derivation", `corpus/lessons/round-30.md:86`) but not the false `MINT.md`
ground. The outside spot-check did not check it either.

Fix: state "no recorded lesson exists; the bar is the fleet mint template's generic probation
draft; `MINT.md` records only the demand, not the rules" — or ground rows 41–45 solely on
M30-1 and drop the MINT.md parenthetical.

**M2. Criterion 52 has no demonstrated failure.**

`corpus/QUALITY.md:358` (criterion 52) has no `Check:` line, no counter, no control, and no
red artifact. Its lesson row (M30-2) documents **compliance** — the sweep recorded class,
pointer and disposition, and the repair was a declared claim (C1) — not a violation. The
nearest real failure artifact is the r29 sweep's post-commit false line ("the navigation
counter does NOT stay exit 0", `corpus/lessons/round-29.md:15`), but (a) criterion 52 does not
cite it, and (b) it cannot be reconstructed from lane history: `git log -S 'does NOT stay
exit 0' --all -- corpus` returns only commits carrying the *correction*, and the false text
is not in the tree (`git show cb4e1c0:LOG.md` already carries the corrected reading).

Answering the question directly: **the M30-2 fix (C1 rows + C3 gate) demonstrates that the
gap is measurable — fence red at base, gate red at base — not that criterion 52's predicate
can fail.** The fix cell cites only the green receipt (`evidence/c1-after-*.txt`,
`corpus/lessons/round-30.md:14`), although the red legs exist and predate data
(`controls/C3K1-base-red.txt`, `evidence/c1-before-8f51071b.txt`); ScribeLesson B/C
independently found the same under-citation. Under the r17–r19 critic bar ("a new criterion
counts only if its red on a real artifact is not already produced by an existing check"),
criterion 52 is a codification, not a discernment gain.

**M3. The discernment verdict was written before its evidence, on an observable the contract
does not define.**

- Report `bbae16bf` 04:00:43 says "Outside non-author spot-check … rides the closure pass";
  spot-check `d72243e` 04:03:37. The disclosure that none exists yet is present but implicit,
  and the verdict is stated as `improved` in the same sentence.
- The stated basis (self-mined mistakes + criterion 52) is not `LEARNING.md:31-35`'s
  observable. No outside disagreement became a grounded criterion this round; the wave
  findings (fence/gate table laxity, C2 resolves-citation-not-grounding, kill-rule
  bypasses, own-work circularity) are routed to round 31
  (`corpus/lessons/round-30.md:56-71`; `SCORECARD.md` w1 erratum).
- Post-hoc the outside sample agrees on S185; that is the only qualifying event, and it is
  not cited by the report.

**M4. The outside sample's S185 agreement is not a clean conformance agreement.**

- The S185 row's "located quote (≤25 words, verbatim)" is `revision=$rev indexed=$covered/$total
  missing=$missing dangling=$dangling duplicates=$duplicates coverage=$score/10`
  (`corpus/lessons/round-30.md:24-27`). That string occurs **0** times in `SCORECARD.md`
  (`grep -c`) and `git log -S 'indexed=$covered/$total' --all -- SCORECARD.md` finds no commit
  containing it. The actual f-string is `indexed={covered}/{len(notes)} … coverage=
  {10*covered/len(notes):.4f}/10` (`SCORECARD.md:84`).
- The outside spot-check noticed the quote is "a schematic rendering … not byte-exact quote
  text" and routed it, but still **agreed** with the S185 admit
  (`corpus/lessons/round-30-verifier-spotcheck.md:74-77`). The lane's own ScribeLesson rates
  the same item **FAIL** ("quote never existed in the file or its history"). The lane's
  addendum routes "3 formality defects" (`SCORECARD.md` w1 erratum; lesson line 67).
- Discernment effect: the outside agreement is on the admission decision, not on the row's
  conformance. A known-false quote field is an unresolved routed defect, so the agreement
  should be stated with that condition, not as a clean agree.

---

### LOW

**L1. "Through two closures" understates: three closures.**

M30-2 says the gap persisted "through two closures that re-ran the census but never the
navigation counter" (`corpus/lessons/round-30.md:14`). Verified:
- The r27 note commit `43fdd7e` is an ancestor of the r27 closure `767b12d`; the note exists
  at `767b12d` and `git show 767b12d:corpus/README.md | grep -c workspace-rules-r27` = 0.
- `767b12d`'s harm watch runs the census and no navigation counter ("Census `validate` exit 0
  at end (rows 177 → 182)", `SCORECARD.md` round-27 results).
- r28 (`77cdda86`) and r29 (`cb4e1c0`) harm watches do the same (census only; the r29
  navigation reading appears only in the inherited-finding sentence).

So the gap was unindexed at **three** closures (r27, r28, r29), each of which ran the census
and not the navigation counter. The r27 case is the originating round's own closure, which is
the most pointed miss.

**L2. "fence (harm watch)" describes a declared rubric the closures did not execute.**

M30-2's `captured-by` reason says "the navigation counter is a fence (harm watch), not a gate"
(`corpus/lessons/round-30.md:14`). `SCORECARD.md:236` does label coverage navigation "harm
watch only", but none of the r27/r28/r29 harm watches ran it, and round 30's registered harm
watch does not list it either (`registration.md` §Harm watch; it runs as C1's claim counter).
The reason reads as an excuse where the row's own text states the failure: the fence existed
and was not run. `captured-by='none'` is still defensible (no gate), but the reason should say
"the r29 sweep self-caught it post-commit; no gate did".

**L3. M30-2's fix cell cites only the green receipt.**

The red legs predate data and are committed (`controls/C3K1-base-red.txt` at freeze
`451e8b3`; `evidence/c1-before-8f51071b.txt` at data `446dc39`), but the fix cell names only
`evidence/c1-after-*.txt` (green). "Fixes demonstrated" is true on bytes, not from the row as
written. ScribeLesson B independently rates M30-2 "PARTIAL — row cites green only".

**L4. Lane records do not acknowledge the outside sample.**

The outside sample is recorded in a lesson file (`corpus/lessons/round-30-verifier-spotcheck.md`),
which satisfies `LEARNING.md:42-46`'s "in the round's lesson". But `SCORECARD.md` round-30,
`LOG.md`'s round-30 block, and the three lesson addenda contain no discernment verdict and no
pointer to the sample; the only trend statement is the fleet report that predates it
(`grep -n 'spot-check' SCORECARD.md LOG.md corpus/lessons/round-30.md` → only the r29 route
source and the SKILL-row routing). The closure package should point at the sample and restate
the narrowed verdict.

**L5. Report-count disclosure drifts.**

The w1 addendum says "24 seat reports" (`corpus/lessons/round-30.md:58`); the commit `15ddd7d`
carries 27 `.md` reports (`git ls-tree 15ddd7d .ufo/waves/round-30/w1/reports/ | grep -c`),
and the outside digest says "21 reports" (`round-30-verifier-spotcheck.md` post-closure
section). Stale snapshots are plausible, but the counts are not reproducible from the commits.

**L6 (record identity, not a verdict defect).** The canonical C2 counter blob changed after
data: frozen `451e8b3` blob `74a4859`, repaired `a0dd664` blob `bf798a0`. The C2 receipts
were produced by the frozen blob. The repair is disclosed ("counter rubric repair (identical
output)", `a0dd664`; lesson addendum part 2) and I verified byte-identical output at
`8f51071b`, `446dc39`, `274f735` with both blobs — so no reading moved. The closure should
state the two blob ids explicitly so a re-run at HEAD is known to be the repaired instrument,
not the frozen one.

---

## What holds (verified, so the attack is bounded)

- `PRED-C2-r30` at base `8f51071b`: literal 28/40 = 0.7000, active 39, resolved 31 = 0.7949,
  `UNRESOLVED {1..5, 38..40}`, `TARGET_MISSED`, exit 1. Exact match to
  `controls/C2K1-donothing.txt` and `evidence/c2-before-8f51071b.txt`.
- At data `446dc39` and at `15ddd7d`/`274f735`: literal 40/52 = 0.7692, active 40, resolved
  40 = 1.0000, superseded `[1,2,3,4,5,18,19,20,32,38,39,40]`, `TARGET_MET`, exit 0.
- Frozen vs repaired counter: byte-identical output at `8f51071b`, `446dc39`, `274f735`
  (both blobs; exit codes equal). The repaired counter's new position guard and `act_n>0`
  guard do not move the committed corpus.
- `corpus/README.md` rows 76 → 78 (+2), exactly the two named notes; QUALITY diff at data is
  append-only (+22 lines, 0 deletions).
- M30-1 is a real mined defect: criteria 1–5 cite nothing at base; 18/19/32 cite on
  continuation lines; 38–40 cite bare M-ids with no path. The base red is a genuine red on a
  real artifact.
- `captured-by='none'` for M30-1 is honest (no gate; criterion 22 is rubric selection only;
  `mado-verify.sh` has no QUALITY check). For M30-2 it follows the M28-3 precedent
  (`none — the frozen counter itself caught both`), though L2's reason caveat applies.
- The outside sample is non-author (hyaku closure, `@m_kfc`) and is committed into the lane
  as a lesson file; it records agree/disagree with reasons for both sampled items.
- The S185 block sha256 (`8b59b503…`) matches what RevC1Fence and the spot-check report.

---

## Residual risk and verification gaps

- **Outside agreement is thin and partly circular.** One this-round admit (S185) + one
  standing reject (S062, r29 precedent). The spot-check's discernment line repeats the
  "self-mined" assertion without checking M30-2's provenance, so the mistakes leg of the
  verdict is not independently confirmed.
- **S185 quote defect is unresolved.** The outside check and the lane's ScribeLesson disagree
  on severity ("schematic" vs "never existed"). The lane routes it; the trend verdict should
  not cite the S185 agreement as clean until the row/lesson quote is corrected.
- **Criterion 52's failability remains unproven** in every artifact I could read. If the lane
  keeps it, it should either cite the r29 false-line artifact explicitly (if recoverable) or
  label it a codification with no red, as the round's own standard would require.
- **The C2 counter resolves syntax, not derivation.** The seed-five rows 41–45 are "resolved"
  by the audit row that records their lack of grounding (lane addendum part 2 acknowledges
  "resolvability ≠ derivation"). That is a stated rubric limit, not a 40/40 semantic claim;
  the trend should not read it as stronger.
- **The lane moved during this review.** Findings are anchored at `274f735`; if further
  commits land (a part-4 discernment erratum is plausible), re-check H1/M1/M2 against the new
  tip. I did not edit any artifact and did not run the C1 fence or C3 gate (RevC1Fence and
  RevC3Gate own those).
- **Worktree observation (outside this item):** RevC1Fence reported
  `M quality/q36-successor-receipts.txt`; the lane's addendum says it was reverted to
  committed bytes. Verify at closure.
- No tools were installed or updated by this seat.
