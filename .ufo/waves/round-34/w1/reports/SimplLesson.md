# SimplLesson — shortest round-34 lesson structure

Seat: SimplLesson (simplifier). Date: 2026-10-24. Read-only analysis; deliverable
written to `.ufo/waves/round-34/scratch/SimplLesson/structure.md` (4,478 bytes).

## Proposed headings

```
# Round 34 lesson
## Gate
## Mistakes
## Census
```

Contract coverage, one element per heading:

- `## Gate` — SOURCES rule 1 (URL + access date + ≤25-word located quote per row
  opened; r34 expects S201, S202 → one quote table), rule 2 (in-place
  status/recheck/used-by changes logged old→new, or `none`), plus refusals as
  `reason`/`flip` pairs, the C2 SCORECARD publication line, and at most one
  bullet each for quarantine hand-checks and a mined considerthese item.
- `## Mistakes` — kaika rule fields verbatim (`class · evidence · captured-by ·
  fix`), fix shown able to fail with committed red-before output; `none mined
  this round.` if empty. Heading is written regardless.
- `## Census` — before/after `sources-census.sh validate` pair with exit code,
  verbatim W04 line list, receipts under `evidence/`, and a
  `rows <before>→<after>` delta that must equal the Gate append count (+2 if
  S201/S202 land).

## Evidence base

- Lane heading convention: `grep '^#' corpus/lessons/round-*.md` — lane-authored
  lessons consistently use `## Gate` + `## Mistakes` (r20–r33); census was
  written inside `## Gate` in r20–r24 ("Start census/End census") and was
  absent from the r33 lesson (r33-verifier-spotcheck:105 re-ran it externally —
  a gap the named `## Census` heading closes).
- Contract: `CORPUS.md` SOURCES rules 1, 2, 4, 5; kaika additions (`## Mistakes`
  row fields, fix-shown-able-to-fail, corrections-are-appends).
- Risk carried forward: routed defect M23-1 — a pasted census dropped W04 lines
  versus the committed receipt. The structure therefore requires byte-for-byte
  W04 paste from the receipt, not retyped id lists.
- Dropped safely: `### Frontier` (report/SCORECARD owns the verdict), all
  `###`-level Gate sub-blocks (r33's flat bullets sufficed), mass-append
  narrations (id-collision/validate-before-append collapse into the census end
  line for a two-row append).
- Alternative noted in the deliverable: folding the census pair into `## Gate`
  saves one heading and stays conformant (r20–r24 precedent); the separate
  `## Census` heading is recommended for spot-check visibility at ~10 chars.
