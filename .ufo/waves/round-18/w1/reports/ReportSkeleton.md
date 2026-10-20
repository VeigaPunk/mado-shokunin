# ReportSkeleton — scoped findings (round 18, wave w1)

## Behavior

Drafted the fleet round-report skeleton at
`.ufo/waves/round-18/drafts/ReportSkeleton.md` (new file; the `drafts/` directory
did not exist and was created by the write). Only that file and this report were
written. No product, corpus, SCORECARD, README, or lesson file was touched.

Section order in the draft:

1. Header and lane identity (HEAD, baseline `d9a5a18`, pre-registration `d3a0000`, admission not asserted).
2. Work performed — declared C1/C2/C3, routed jj-fix line, R17-V1..V5 disposition table, Stale-lane line, Tool installs line, jj notes line, host/fetch file-read line.
3. Landed changes — commit table with `d3a0000` as the only pre-filled row.
4. Before → after measurements — C1, C2, C3, R17-V1/V2, JJ-F10 rows; separability, harm-watch, freshness placeholders.
5. Sources & frontier — SOURCES counts placeholders, reserved S072-S099 convention, route-note credit table for `walker-route-r18.md` (P3) and `theme-route-r18.md` (P5), census block.
6. Trend verdicts — expansion, quality, discernment.
7. SHONEN — the four round-17 checklist items as placeholders.
8. Waves, seats, dead seats, misroots, L0 — wave counts/role mix/dead seats, round total, misroot sweep, seat conduct, host file-read line, jj seat note, L0 lines.

Shape was taken from `.ufo/reports/round-17/mado.md` (sections, table
layouts, Stale-lane/Tool-installs/L0 line style) and `SHONEN.md` (four
checklist items with `[~]`/`[x]` state and historical-assertion style).

## Inputs read (read-only)

- `SHONEN.md` (full).
- `.ufo/reports/round-17/mado.md` (full).
- `corpus/lessons/round-17-verifier-spotcheck.md` §6, lines 183-208 (R17-V1..V5
  wording, via grep plus a single range read context).
- `.ufo/waves/round-18/w1/spec.json` item `ReportSkeleton` (prompt matched the
  assignment; output path `.ufo/waves/round-18/w1/reports`).
- Directory listings of `.ufo/waves/round-18/` (existing `evidence/`, `gen_w1.py`,
  `w1/`) and `evidence/` (`census-start.txt`, `measure-before.json`).

## Choices and limits

- Declared inputs (baseline `d9a5a18`, pre-registration `d3a0000`, claim IDs,
  C1 before 15/23 = 6.5217, C2 before 4/6, C1 target ≥18/26) are named in the
  skeleton because the assignment declares them. Every outcome, count, and sha
  is a `<PLACEHOLDER>`. Nothing was measured or re-run.
- Measurement commands used in the skeleton are the ones named in the
  assignment and in round-17's table. They were not executed by this seat.
- Wave-2 rows are present as `<W2_COUNT_OR_NONE>` because the round-18 spec in
  this seat's inputs names only one wave directory (`w1`); the round total is a
  placeholder.
- `drafts/` was not previously present; the path requested by the assignment
  was used exactly.
- The round-17 report's `Waves` section mentions L0 lines `.ufo/l0-questions.md`
  L54/L55; the skeleton keeps that reference as a placeholder for current state
  rather than asserting it.

## Tool installs

None. This seat installed or updated nothing. The host pacman pause was not
touched; no pacman, yay, paru, sudo, or systemctl call was issued.

## jj / git

No `jj` command and no git write was issued. Read of the lane was by file read
(`read`, `grep`, `ls`) only.

## Findings for L1 integration

- The skeleton's disposition table keeps R17-V1..V5 as separate rows with
  `<..._STATUS>` placeholders; L1 must fill each status only from a committed
  receipt or failing-control commit (the round-17 erratum precedent).
- Round 17 cited `tool sha 7a98720e…` in its before→after table while the landed
  tool was `962919ce…`; the skeleton's C3 and R17-V1/V2 rows require both shas
  to be cited with labels. This is a carry-over rule, not a claim about round 18.
- Route-note credit rules (first-15-lines `source:`, `surface:` line, four
  sections, `[UNK]` in last section, raw fetch receipts) are restated in the
  Sources & frontier section so a later reader can check them without the
  SCORECARD.

## Out of scope / not done

- No section content beyond placeholders; no outcome values.
- No check of whether `measure.py`, `mado-tripwire.py --frozen`, or the route
  notes exist yet; the skeleton names them only as the declared artifacts.
