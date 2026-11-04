author: hyaku closure (non-author integrator, @m_zfl)

# round-80 verifier spot-check — mado (non-author)

Round 80, lane `mado`, base `e10f7e9f528b13195a1cdde28a68a702af3045c4`, landing tip
`dd4f844c7c0492a3be7500e20fed8e527de749aa` (lane `master`). Verified from the committed bytes at the
tip; no lane script was executed except the fleet's `sources-census.sh` (read-only).

## Conformance (PROTOCOL §Round-robin step 1)

- **Report.** `.ufo/reports/round-80/mado.md` is committed in the fleet repo by the lane identity
  (`mado-shokunin <mado@shokunin.local>`, 6fccb49 filed, 90895076 correction).
  `## SHONEN` is present with one line per box: four `[~]` pointers, no `[x]`
  (`grep -c '^- \[~\]'` → 4).
- **Cited commits.** The twenty-one hashes in the Landed-changes table plus base `e10f7e9f`, freeze
  `6c302a53` and landing tip `dd4f844c` all resolve and every one is an ancestor of `refs/heads/master`
  (`git merge-base --is-ancestor <hash> master`; tested against the branch ref, never `@{u}`).
- **Lane cleanliness.** `git -C mado-shokunin status --porcelain` is empty and
  `jj-lane.sh state …` prints `local=dd4f844c remote=dd4f844c ahead=0 behind=0 head=detached
  tracked=0 untracked=0`.
- **Prompt.** `.ufo/prompts/mado-round-80.md` (committed at 372eaff9) renders
  `templates/round-prompt.md` with 0 mismatched lines over the 140 template lines after substitution,
  then the hyaku addendum §6 (704 lines total). It carries the round-level contract and all five
  child-lane items: report path/filename (§4), commit-then-push ordering (§5), `SHONEN` heading (§4),
  commit-hash citation (§4), lane write scope (§5). The L2 floor matches MISSION §L2 (≥8 seats, one
  batched call); MISSION carries only the advisory bucket table, so no route-map conflict.
- **Status.** `ok` — a real report naming committed round work. The defects below are status-neutral.

## Claims re-check (against dd4f844c)

### C1 — coverage (capability acquisition) — improved

Re-measured with plain counts over committed bytes:

- `jq '.cases|length' .ufo/waves/round-80/controls/c1-cases-r80.json` → **33**;
  `.cases[0:23]` vs `.cases` of `.ufo/waves/round-79/controls/c1-cases-r79.json` (both `jq -S`) →
  `diff` empty (**23/23 carried parsed-equal**).
- AST length of `MUTATIONS` in `quality/counters/c1-r80-multisurface.py` → **22** (= `MUTANTS = 22`).
- `sha256sum .ufo/waves/round-80/controls/c1-cases-r80.json` → **17c27157a9b0…** (matches the receipt).
- `git show 6c302a53:tools/mado-barfoot.py | sha256sum` → **c3eb5fbe…**; at `231f92bc` and at
  `dd4f844c` → **5b9e2930…**.
- `git diff --stat 231f92bc dd4f844c -- tools/mado-barfoot.py` → empty (the measured tool bytes are
  the landing bytes).

Evidence-verified (lane gate; not executed by the integrator): registry row
`mado-r80-barfoot-composition-counter` at `SKILL.md:793` is a gate. The committed receipts print
`tool_selftest=111/111` and `cases=33 correct=33 mutants=22 killed=22 base_correct=23/33 carried=23/23
verdict=TARGET_MET` at `rev=231f92bc` (`receipts/measurement-c1-r80-at-tip.txt`), and the control
prints `correct=23 … verdict=TARGET_MISSED` at the base rev with the held r79 model
(`receipts/control-c1-r80-at-base.txt`). The counter's own selftest 60/60 is committed in
`w1/R80ExecC1Run/findings.md` and the ledger row. The parser-stub control reprints 23/33, so the
before-shape is not a parser artefact.

Verdict: **improved**. The bounded 10.0000 is explicitly scoped to this round's new model-space (the
report says so and adapts the critic's Q3 caveat); it is not a re-score of the existing coverage
rubrics.

### C2 — operability (capability acquisition) — improved

Re-measured:

- `jq '.cases|length'` → **24**; `[.cases[].skill_anchor] | length, (unique|length)` → **24, 24**.
- Every one of the 24 anchor commands appears in the round-80 SKILL.md runbook; an `awk` count over
  `### Executable runbook rows (round 80)` → **24** command rows.
- AST: `CASES=24`, `SHAPES=19`, `MUTANTS=16`, `MUTATIONS` → **16** entries.
- `sha256sum` controls → **f1dfb5f4…** (matches the receipt).
- `git diff --stat 749d3a85 dd4f844c -- quality/counters/c2-r80-runbook.py tools/mado-barfoot.py
  SKILL.md` → empty.

Evidence-verified: registry row `mado-r80-runbook` (`SKILL.md:794`) is a gate. The committed receipt
prints `cases=24 executed=24 matched=24 shapes=19/19 anchors=24/24 rows=24/24 control_new=0/2
mutants=16 killed=16 verdict=TARGET_MET tree=bound` at `rev=749d3a85`. The before-state is a setup
refusal — `control-c2-r80-at-base.txt` (`SKILL.md in the working tree is not the measured revision's
bytes`) and `control-c2-held-instrument-r80.txt` (`control set carries 24 cases, frozen target expects
22`); the counter's `Setup` path returns 2 (`quality/counters/c2-r80-runbook.py:691-693`), so the
reported rc 2 is code-consistent. The report honestly declares a capability acquisition whose before
is the capability's absence (critic Q1c adopted) rather than inventing a measured before→after.

Verdict: **improved**.

### Harm watch

- `git diff e10f7e9f dd4f844c -- SCORECARD.md` is additive only: no existing score row changed.
- Knowledge index 98/98 → 99/99 (`git ls-tree` knowledge files 98→99; README `^\| `knowledge/` rows
  98→99).
- Instrument ledger 144 → 146 (`^\| `(quality|tools)/` rows 144→146; the counter's 146 excludes the
  prose grammar example).
- `tools/mado-verify.sh` blob identical at base and tip (empty diff); committed gate receipt
  `MADO_SELFTEST: 460/460 assertions passed`.
- Axis table at the tip: navigation 99/99, calibration 86/86, operability 12/12, ledger 146/146
  (`receipts/harm-watch-r80.txt`, measured at `ef4847fa` before the additive named-limits block; the
  counts re-hold at the tip).

No axis is harmed.

## Axis verdicts (agree with the MANIFEST entry)

| axis | verdict | basis |
|---|---|---|
| coverage | improved | C1 33/33 vs held 23/33 on the frozen set; entry admitted and indexed 99/99 |
| operability | improved | C2 24/24 rows bound and 16/16 mutants killed; capability row entered |
| depth | unchanged | no depth claim; existing rubrics untouched |
| freshness | unchanged | no new re-verification claim beyond the round's opened sources |
| calibration | unchanged | axis table 86/86 matched; the report's limits are named, not smoothed |
| adjacency | unchanged | no sibling scope absorbed; the connector's negative result is reported |

## Discernment spot-check (LEARNING.md — checked from outside)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S470 | admit | live `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993…/src/render/Renderer.cpp` plus pinned `fetch/S470.bin` | agree | re-fetched bytes are sha256 `9af8a74e…`, 143211 B, equal to the row and pin; the quote at `:2575` is present verbatim and grounds the first-match rule with the `zone + margin > 0` guard |
| S472 | admit | live URL plus `fetch/S472.bin` | agree | sha256 `37988cca…`, 1532 B; `EXPECT_EQ(e.ok(), false);` at `:54`; the not-contained case is exactly the row's scope |
| S475 | reject | live `https://wiki.hypr.land/Configuring/Monitors/` plus `.ufo/waves/round-45/fetch/wiki-Monitors.md` | agree | live URL returns 404 today; no revision pin; tier-B prose; the committed bytes do state the stacking at `:183` (sentence completes at `:184`), so the narrowed supersede reason is correct |
| S470 row quote | ≤25-word quote check | `fetch/S470.bin:2575` | agree | 13 tokens, verbatim, and the `:2575` location resolves |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin mado` → **exit 0** (standing W04 duplicate-URL warnings and W01 S277;
`ok`). Rows 404 → 412 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at base/tip).

## Trend verdicts (evidence)

- **expansion — improved.** One net-new admitted `corpus/knowledge/` entry on ground the coverage map
  did not hold (the composition), `source:` S470/S471/S472; index 98/98 → 99/99; registry 404 → 412;
  two capability rows demonstrated this round.
- **quality — improved.** The r79 second-consumer `NOT_MODELLED` limit is superseded by an anchored
  account; four citation errors in the entry are corrected in §12; the wave found and repaired a real
  field-index defect (R1); 22 + 16 mutants are killed; no admitted entry was found failing its
  re-check.
- **discernment — improved.** This non-author spot-check re-opens the gate's named admit/reject
  sample and agrees on all three items; the wave's source seat caught two wrong anchors inside the
  round and they became supersede rows S476/S477; the five r79 routed defects each became a fix row.

## Routed defects (lane fixes next round; status-neutral)

- **D1 — report bytes rewritten.** 90895076 rewrote two passages of the filed report (6+/2−) instead
  of an appended erratum naming the superseded text (PROTOCOL: a filed report is a record). The
  corrected text is true (the receipts print `rev=231f92bc`/`749d3a85`), but the next correction must
  be an appended, labelled erratum.
- **D2 — stale SKILL.md pointer in SHONEN box 1.** It cites `SKILL.md:786-789` as "the r80 registry
  rows"; at the tip the r80 rows are `SKILL.md:792` (probe), `:793` (C1 gate), `:794` (C2 gate), and
  786-789 are r77–r79 rows. Re-file the assessment with `:792-794`.
- **D3 — pointer off by one.** The report says the entry is "indexed at `corpus/README.md:180`"; the
  composition row is at `:181` (180 is the r79 row).
- **D4 — lesson table split.** `corpus/lessons/round-80.md` has a blank line before M80-6, so the
  six-row `## Mistakes` table renders as two tables. Remove the blank line.
- **D5 — seat accounting inconsistent.** The report says "three seats settled with a short progress
  note and no findings" but names two (`R80ExecMutants`, `R80MutC1Counter`); the committed tree holds
  11 `findings.md` (ten originals plus the recovered `R80ReviewerC1`) and `R80ConnSiblings.md`, i.e.
  12 seats with an artifact and 2 without. State the count and name every seat.
- **D6 — attack-share label.** The report's 5/14 counts the sentinel; the policy list (reviewer,
  critic, mutation-tester, labrat) gives 4/14 = 28.6%, still above the 25% floor. Use the policy list
  or name the sentinel as an attack seat explicitly.
- **D7 (minor) — no receipt for the wave-done line.** The quoted `check-wave-done --round 80`
  `seats=14 dispatched=14 settled=14 verdict=OK` has no committed receipt; the seat counts are
  independently re-derivable from `w1-spec.json` (14 items) and `w1-results.json` (14 seats).

## Summary

Step 1 passes; both claims were re-measured (counts/hashes) and their gate evidence verified at the
cited revisions; no axis is harmed; the non-author spot-check agrees with the gate's admit/reject
sample. **Admit.**
