# RevQuality2122 — QUALITY criteria 1–22 vs R16-V1, and whether criterion 24 is inflation

Seat `MadoR17.RevQuality2122`. Read-only review. No edits outside this report; no tools
installed or updated; no `pacman`/`sudo`/`systemctl`/`hyprctl`/live probe, and no transcript
read. `corpus/QUALITY.md` read at `0175f13`; its blob `b45e5bda24bcc2f74bb4e8d600edee51790e7c24`
equals `27cd06f:corpus/QUALITY.md`, and `git diff --stat 27cd06f 0175f13` touches only
`SCORECARD.md` and `.ufo/waves/round-17/evidence/census-start.txt`.

## Verdicts

1. **C1's "captured-by none" is wrong.** QUALITY criterion **9 already captures R16-V1's
   class**: the cited receipt is a failed run (`exit` 2, `frozen_error`, measured `9dcf248`)
   that the sentence labels as a settled `snapshot_tampered` result. That is simultaneously
   an unbound verdict and an in-flight failure labelled settled. Both clauses of 9 bite, and
   the lane's own precedent applies 9 to the same class twice (round-12 M6, round-14 M2).
2. **Criterion 23 is a specification of 9, not a wholly uncovered class.** No criterion states
   the mechanical *outcome-field token* check; 23 supplies it. That can be admitted on the
   recurrence (R14-M2 + R16-V1), but the lesson must name 9 as the capture and 23 as the
   specification — not "none".
3. **A numbered criterion 24 for tripwire use is inflation this round.** Keep it as an
   unnumbered candidate and a SKILL registry row; numbering it changes the pre-registered
   denominator and counts a process obligation the bar explicitly does not govern.

---

## 1. Does an existing criterion capture R16-V1?

Fact pattern re-read, not inferred:

- `corpus/lessons/round-16.md:131-132` at `27cd06f`:
  "Input tamper control returns **2 snapshot_tampered**, retained in `frozen-tampered.json`."
- `.ufo/waves/round-16/evidence/frozen-tampered.json` (committed at `1e31681`): top-level
  `measured_commit` `9dcf248993a9622a5b016edec0003187141745d2`, `exit` 2, `stdout`
  `MADO_PLAN: frozen_error` with embedded verdict JSON `"finding": "frozen_error"`,
  detail `expected.json pair 1/'denied_executable:sudo' is unreachable`.
- `.ufo/reports/round-16/mado.md:64` (fleet report) carries the same sentence:
  "Tampered frozen input returns2 `snapshot_tampered`; original receipt retained."
- `.ufo/waves/round-16/evidence/action-selftest-final.json` (measured `1e31681`, exit 0)
  carries the token the sentence wanted: `frozen-tampered-plan: want 2/snapshot_tampered
  got 2/snapshot_tampered` (and the `-policy` sibling). So the correct receipt exists; it is
  not the one cited.

### Criterion 9 — the capture

`corpus/QUALITY.md:15`:

> 9. Bind each audit verdict to a commit or frozen-copy sha; label mid-edit failures
> in-flight, never as settled defects.

Applied to the fact pattern:

- Clause 1 (binding): the verdict `snapshot_tampered` is bound to no commit at which the
  cited receipt records it. At the revision the receipt names (`9dcf248`) the receipt records
  `frozen_error`; the only receipt that records `snapshot_tampered` is
  `action-selftest-final.json` at `1e31681`, which the sentence does not cite.
- Clause 2 (in-flight): the cited receipt is a failed run (`exit` 2, `frozen_error`). The
  sentence relabels that failure as a settled control outcome. The lesson's own M6 paragraph
  records the frozen run as red ("frozen run **2 frozen_error**; original
  `action-frozen.json` retains the red evidence"), and the tamper receipt is another run of
  the same pre-fix content recording `frozen_error`; the status was in hand.

Two precedents in this lane apply 9 to the same class:

- `corpus/lessons/round-12.md:18` M6, whose class is "A verdict from a moving tree or
  truncated harness output was treated as a stable judgment", captured-by "9".
- `corpus/lessons/round-14.md:15` M2, class "attribution / evidence precision", captured-by
  "QUALITY 9", fixed by an appended clarification — not by a new criterion.

The round-14 M2 row is the closest structural analogue: a sentence attributed to a receipt an
outcome that receipt did not record, and the lane's remedy was a correction under criterion 9.

### Criterion 6 — the value half

`corpus/QUALITY.md:12`:

> 6. Publish each pinned value with a re-derivation command and named revision; any shortened
> hash must be a true suffix, with corrections preserving old and new values.

`snapshot_tampered` is published as a pinned value. A re-derivation command against the cited
receipt (`git show 1e31681:.ufo/waves/round-16/evidence/frozen-tampered.json` plus a token
grep) returns `frozen_error`, not `snapshot_tampered`. Criterion 6 also supplies the fix shape
the draft already uses: corrections preserve old and new values. But 6 was satisfied in form
by publishing a value with a path; it does not require the path to be the carrier, which is
the missing element.

### Adjacent criteria, with exact text

| # | `corpus/QUALITY.md` line | Exact wording (relevant part) | Relation |
|---|---|---|---|
| 2 | 4–5 | "Every claim carries a source: a measured anchor (path:line, command, evidence id) — never oral knowledge." | Anchor exists; the rule tests presence/provenance, not that the anchor records the claim. Partial. |
| 3 | 6 | "Observation, inference, and unknown stay separate." | The sentence presents a `1e31681` observation through a `9dcf248` receipt. Partial. |
| 7 | 13 | "Hash committed artifacts from `git show <commit>:<path>`; label work-window hashes provisional and bind them again at the commit." | Governs hashing artifacts, not binding a verdict. Does **not** support the lesson's parenthetical "7/9/13 (receipt bound to committed revision)". |
| 13 | 19 | "Evidence meant to outlive a round is a committed path or quoted lines plus sha; `/tmp` records provenance only." | The path is committed, so 13 is satisfied in form; it is durability, not content. |
| 19 | 50–55 | "Keep diagnostic requests, retained evidence and behavioral conclusions separate." | The receipt (retained evidence) is used for a behavioural conclusion it does not show. Partial. |

Remaining criteria were checked and do not engage: 1 (falsifiability — the claim is
falsifiable, which is why R16-V1 was caught), 4/5 (errata/rejection format), 8 (the path
exists at `1e31681`), 10 (counts), 11 (tool-help absence), 12 (independence), 14 (set census),
15/16 (docs vs host), 17 (URL duplicates), 18 (file types), 20/21 (install/pause), 22
(calibration counters — the draft itself says "not citations").

### What the lesson draft currently says, and why it fails

`LessonDraft.md:11` (M1 Captured-by):

> none in QUALITY: no criterion requires a cited receipt to match the revision and finding it
> is cited for. Closest named criteria: QUALITY 7/9/13 (receipt bound to committed revision)
> `[L1-VERIFY]`; QUALITY 22 governs calibration counters, not citations.

This is wrong in three ways:

1. It names 9 in the same cell but concludes "none". Criterion 9's second clause is exactly
   the frozen-error-to-settled-token relabel.
2. "7/9/13 (receipt bound to committed revision)" mislabels 7 and 13; only 9 binds a verdict.
3. It omits 2, 3, 6 and 19, which are the actual adjacent rules, and leaves `[L1-VERIFY]` on
   wording that is directly readable at `corpus/QUALITY.md:12-19`.

`QualityDraft.md:11` is more careful:

> Criteria 9 and 13 bind a receipt to a sha and a committed path; they do not bind the token a
> sentence attributes to it.

That is true for the *token mechanism* but understates 9's in-flight clause, which covers the
relabel independently of any token-field rule. The two drafts therefore disagree; L1 must
reconcile them in the lesson cell.

Correct cell, proposed:

> 9 (binding + in-flight labelling; precedents round-12 M6, round-14 M2); 6 (pinned value
> re-derivation and corrections append); 2/3/19 adjacent. No criterion states the mechanical
> outcome-field token check; criterion 23 specifies it.

Criterion 23 itself is then legitimate as a **specification** (cf. 19 sharpening 3, 18
sharpening 14) — but if L1 keeps the word "none", 23 is a duplicate provenance criterion of
the kind the lane refused in the round-14 block ("No duplicate provenance criterion or
generic wrapper is introduced", `corpus/QUALITY.md:60-61`), and the calibration gain rests on
a false premise.

---

## 2. Is criterion 24 (tripwire use) inflation?

**Yes, if it is appended as a numbered, lesson-cited criterion and counted this round.** The
draft already labels it "Candidate, not admitted" (`QualityDraft.md:13`); that label does not
protect the metric.

Concrete reasons:

1. **It counts anyway.** `measure.py:92-93` uses
   `^[0-9]+\. ` for criteria and `^[0-9]+\. .*lessons/` for the cited subset; a line reading
   `24. Candidate, not admitted: ... (lesson: lessons/round-17.md#mistakes M2; ...)` matches
   both. Appending both 23 and 24 yields 24 criteria / 16 cited = **6.6667**, against the
   pre-registered 15/23 = **6.5217** (`SCORECARD.md:841`). An explicitly unadmitted candidate
   would raise the calibration reading.
2. **It exceeds the pre-registration.** C1 declares *one* append-only lesson-cited criterion
   and a target of "≥ 15/23" (`SCORECARD.md:836-841`). C3 says "needs no note or criterion"
   (`SCORECARD.md:863`). Numbering 24 changes the declared denominator and the target after
   the waves — the post-hoc rubric growth criterion 22 was added to prevent
   (`corpus/QUALITY.md:107`).
3. **It is process, not claim admission.** `corpus/QUALITY.md:24`: "this bar governs claim
   admission only." Criterion 24 is an obligation to run a scan and cite its first line,
   digests and permit set before a conduct claim; that is a verification procedure for C3's
   capability. The lane's convention for a runnable check is the SKILL registry — criterion
   21's own closing line says "The runnable check and its failure evidence are registered in
   SKILL.md", and `SkillRegistryDraft.md` already contains the `mado-tripwire` row.
4. **No false conduct claim is on record to ground it.** M2's members are breaches, not
   misstatements: the libinput transaction (round-15 M2), `pacman -Q waybar` (round-16 M5,
   disclosed; the same row says "No flawless-compliance claim"), and the fleet-root report
   (round-16 M4, disclosed and copied back). The red anchor proves *detection of a command*,
   not falsification of an admission claim. A rule whose red case is a breach is testing the
   instrument, not the bar.
5. **The instrument cannot see one of M2's three members.** The tripwire parses only `bash`
   toolCall `arguments.command` and `!`-prefixed `eval` `arguments.code` (shared interface,
   and `LessonDraft.md:12` states the same). Round-16 M4 is a report-path resolution under
   the fleet root: a file-write class for which the tripwire has no classification rule, and
   which it does not parse at all if the write came through a non-bash tool. A criterion
   phrased "before any admission claim about a seat's conduct" would appear to cover M4's
   class while remaining blind to it. The draft states this limit, which mitigates overclaim
   but does not change the category.
6. **It double-counts criterion 21's anchor.** The libinput call is already the red anchor
   for criterion 21 and for C3. Reusing the same incident as the red case for a second
   numbered criterion is the duplication the lane has refused before (round-12 disposition:
   "no second quality rule is needed"; round-14 M3: "no duplicate criterion added").

Non-inflating form, recommended:

- Keep 24 out of the numbered sequence. Leave it in the draft or as an unnumbered candidate
  note; register `mado-tripwire` in SKILL.md (already drafted) and cite that row from lesson
  M2 (`captured-by: 21` plus the registry).
- If L1 later admits it, do it before measurement with a re-declared target of 16/24, ground
  it in an actual false conduct claim (none exists today), and keep the draft's limits
  verbatim: post-hoc only, clean bounds only parsed bash/`!`-eval calls, exit 2 is never
  clean, permits named, findings are evidence to adjudicate rather than automatic conduct
  findings.

---

## 3. Minor precision findings (same scope)

- **Receipt field shorthand.** `LessonDraft.md:11` says the receipt records "`finding`
  `frozen_error`" and "detail ...". The receipt's top-level keys are `label`,
  `measured_commit`, `action_gate_sha256`, `command`, `exit`, `stdout`, `stderr`,
  `expected_exit`, `matched_exit`; `finding` and `detail` live inside the JSON embedded in
  `stdout`. The draft should say "`stdout`'s verdict JSON records `finding` `frozen_error`".
  The label checker is compatible (`label-check.py` collects `stdout`), so this is prose
  precision under criteria 2/6, not a checker defect.
- **Placement risk for criterion 23.** Criteria 18, 19 and 20 are uncited under the literal
  counter only because their `(lesson: ...)` tags sit on continuation lines (criteria start
  at `QUALITY.md:43`, `:50`, `:72`; tags at `:49`, `:55`, `:77`). Criterion 23's draft keeps
  its tag on the first physical line (`QualityDraft.md:9`), so it counts. If L1 wraps it,
  the reading is 14/23 = **6.087**, below the baseline, not 15/23.
- **`[L1-VERIFY]` on 7/9/13 is unnecessary.** The wording is directly readable at
  `QUALITY.md:12-19`; I quote it above. L1 can drop the marker or resolve it from this
  report.
- **`snapshot_tampered` "only" claim is supported for the receipts I opened.**
  `action-selftest-final.json` carries `frozen-tampered-plan` and `frozen-tampered-policy`;
  `frozen-tampered.json` carries `frozen_error`. I did not sweep every round-16 receipt —
  RevR16V1Facts owns that.

## Residual risk and verification gaps

- I did not execute `label-check.py`, `measure.py` or `tools/mado-tripwire.py`; the seat rule
  reserves execution to the executors and L1's single verification. The red/green cases are
  read, not re-run.
- I did not read the round-15 OMP transcript: my item does not name it, so the red anchor
  (line 54, `call_38165`) remains `[L1-VERIFY]`, as the lesson draft itself says.
- I did not audit every round-16 evidence receipt; my receipt checks are limited to
  `frozen-tampered.json`, `action-selftest-final.json` and `action-frozen-final.json`.
- Host versions remain `[UNK]`: no package query was run, per the host-wide pause.

## Bottom line for L1

- Replace M1's "captured-by none" with **9 (capture: binding + in-flight labelling), 6/2/3/19
  adjacent, 23 as the token-level specification**. Quote 9 in the lesson cell; the lane has
  applied it to this class twice.
- Do not number criterion 24. Keep the tripwire in SKILL.md and lesson M2; if it is ever
  admitted, re-declare the target as 16/24 and keep the limits in the criterion text.
- Keep criterion 23's citation on its first physical line, and reconcile the lesson and
  QualityDraft wording before the single measurement.
