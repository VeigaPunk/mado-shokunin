# R76ScribeLesson — scoped findings (w1 scribe, round 76)

Seat: draft the round-76 lesson skeleton and propose QUALITY criteria. Write scope:
`.ufo/waves/round-76/w1/R76ScribeLesson/` plus this report file. Leaf member — no subagents
dispatched, no peer messages sent, no git/jj mutations, no installs.

## Read (all evidence-verified from committed bytes, 2026-11-04)

- `.ufo/waves/round-76/claims-declaration-r76.md` — frozen C1/C2 predicates, kill rules,
  targets, label-correction disclosure (v1 `ff97505f…`, v2 `5a91d69e…`, v3
  `320f7e6b54e71776f2d5b179b9a8b09ee9185886e2aeb045af0ecc9171cc77ea`), declared limits,
  R1–R8 dispositions.
- `.ufo/waves/round-76/control-baseline-r76.txt` — `HELD_R76_C1 held_mz_correct=15/15
  outcome_field_scored=no`; four `HELD_R76_C1_MUTANT` lines all `mz_score=15/15
  killed_by_held_rule=no`; `HELD_R76_C2 held_controls=55/59 missed=callee-del-literal,
  callee-del-store,dynamic-key-del,dynamic-key-module-const`.
- `.ufo/waves/round-76/receipts/label-derivation-r76.txt` — 16 rows, `expect==derived` on both
  fields, `DERIVATION: all labels re-derived`.
- `.ufo/waves/round-76/measurement-c1-r76.txt` — `MADO_R76_OUTCOME_FIELD: cases=16 correct=16
  mutants=4 killed=4 base_killed=0 verdict=TARGET_MET rev=cb713254…`; mutant scores 15/16,
  15/16, 15/16, 14/16 with `base_score=16/16 base_killed=no` each.
- `.ufo/waves/round-76/measurement-c2-r76.txt` — `MADO_R76_GUARD_SHAPES: population=20
  readers=13 guarded=13 unguarded=0 controls=59/59 base_controls=55/59 verdict=TARGET_MET
  rev=755b339f1f6ec18f45b494d40515aecdbe9ceb73`; base leg `correct=no` on exactly the four
  target misses.
- `corpus/lessons/round-75.md` — section shape and the class vocabulary used below (scope,
  landing, survivor, number-drift).
- `corpus/QUALITY.md:905-945` — landed criteria 128–131 (probation draft).
- `LEARNING.md:40-48` (fleet root) — non-author spot-check bar: ≥1 admit and ≥1 reject,
  `agree`/`disagree` with reason recorded in the round's lesson.

## Wrote

- `.ufo/waves/round-76/w1/R76ScribeLesson/lesson-skeleton.md` — round-76 lesson draft with:
  Outcome (both claims' measured receipts, mutant tables, do-nothing control dispositions,
  declared-limit "Not claimed" placeholder); Mistakes M76-1/M76-2/M76-3 each with class,
  evidence pointer (red and green), captured-by, and a fix that can fail; Gate placeholder
  listing the admit/reject/registry/assimilation duties; a provenance note per QUALITY 131;
  and two verbatim-conflict carries (below). No `corpus/` file was written.

## Proposed QUALITY criteria (at most three, as assigned) — and the coincidence already landed

`corpus/QUALITY.md` already carries a probation-draft block **"Criteria from the round-76
outcome-field and interprocedural census"** at lines 906–931 that lands exactly the assigned
trio (plus 131). To avoid a second convention, my proposals are stated once and mapped to the
landed rows; the lesson should cite the landed numbers.

- **(a) A frozen separator must be reachable through the field that is scored** — red state it
  catches: a frozen mutant whose scored fields equal the correct implementation on every
  reachable case (round 76's v2 echo-dropping mutation: `verdict=` green requires `killed==2`,
  the M-Z kill already requires the echo, mutant scored 16/16 everywhere). Lesson id: **M76-2**.
  Landed as **QUALITY 129** (`corpus/QUALITY.md:916-924`).
- **(b) A label derivation must read only the instrument's own evidence lines, never its
  contract row** — red state: a label justified by the contract row's summary semantics while
  the instrument's own per-case lines disagree (v1 modelled `verdict=` as summary-green only;
  first outcome-field measurement scored `correct=12/15` with `right`, `liar-success`,
  `green-mutant` mislabeled). Lesson id: **M76-1**. Landed as **QUALITY 128**
  (`corpus/QUALITY.md:906-914`).
- **(c) Every quoted tally names an operative regex/regex-free command** — red states: a
  tally whose generating command is unnamed, and a derivation/control leg that matched no rows
  yet reported a score (the pre-freeze control's end-of-line-anchored row regex met the rows'
  trailing `sha256=` and silently parsed nothing; four mutants were reported `0/15` — killed by
  a rule that had observed nothing). Lesson id: **M76-3**. Landed as **QUALITY 130**
  (`corpus/QUALITY.md:926-931`), with the naming/provenance half carried by **QUALITY 131**
  (`corpus/QUALITY.md:934-945`: every quoted number labels itself `re-executed` or
  `evidence-verified`).

Recommendation carried in the skeleton: the final lesson cites 128–131 as the captured-by
mechanisms rather than re-proposing duplicates.

## Conflicts carried verbatim (scribe duty; not resolved by this seat)

1. `control-baseline-r76.txt` prints `HELD_R76_C1 held_mz_correct=15/15` against the frozen
   16-case v3 set; the landed criteria's able-to-fail records use the same 15-denominator
   pre-v3 numbers (`correct=12/15`; four mutants `0/15`). The v1/v2→v3 population delta is not
   re-derived anywhere I read. Left verbatim in the skeleton for the closure to state.
2. The two claims measured at different revisions: C1 at `cb713254…` (the freeze-v2 rev), C2 at
   `755b339f1f6ec18f45b494d40515aecdbe9ceb73`. R5's disposition (state measurement revision and
   each instrument's last-change commit separately) is the cover; the skeleton marks it.

## Out of scope / not done by this seat

- No edits to `corpus/`, production instruments, SKILL.md, SCORECARD.md, LOG.md, README,
  SOURCES.md, `.ufo/state/`, `.scratch/`, `scripts/`, `templates/`, MANIFEST.json.
- No git/jj write commands anywhere; no fixture repos created (none needed).
- No tool installs (none needed); pacman untouched per the host-wide pause.
- Scratch `/fast/scratch/hyaku/mado-r76/R76ScribeLesson/` was created and is deleted before
  this report; no receipt was cited from it (everything cited is committed in the lane).

## Known limits of this draft

- Gate section is a placeholder: the actual candidates, quotes, fetch receipts, registry counts
  and the non-author spot-check result are the closure's to fill (≥1 admit, ≥1 reject per
  `LEARNING.md:40-48`).
- Which mode joined the label set at v3 (15→16) is unverified here; marked in the skeleton.
- The final lesson text, its author line, and the measured-content revision are placeholders.
