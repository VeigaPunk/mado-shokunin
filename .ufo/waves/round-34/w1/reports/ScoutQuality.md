# ScoutQuality — round 34 w1 report

## Scope

Read `corpus/QUALITY.md` (mado lane) and `~/Projects/shokunin/CORPUS.md`
(fleet contract). Extracted the bar a new `corpus/knowledge/` entry and a new
`corpus/SOURCES.md` row must meet, covering the seven named items:

1. SOURCES contract version
2. Required Gate fields
3. Quote word bound
4. Accepted recheck forms
5. Used-by rule
6. Append-only row rule
7. Rule on quoting a source the lane did not open

## Deliverable

Checklist written to
`.ufo/waves/round-34/scratch/ScoutQuality/bar.md` — 22 numbered items, each a
verbatim quote with file and line citation.

## Findings (key lines)

- **Contract version**: CORPUS.md:66-68 pins "Contract v1 (kaika, 2026-10-19,
  frozen)"; changes require a new version, never an edit. QUALITY.md:24 defers
  tier/registry definitions to SOURCES.md under that same v1.
- **Gate fields**: CORPUS.md:113-115 — for every new row the round lesson's
  `## Gate` records URL, access date, and a ≤25-word quote with location
  grounding `teaches`; non-author verification re-opens a sample. Gate section
  shape (candidates / admitted / rejected-with-reasons / spot-check) at
  CORPUS.md:19-20.
- **Quote bound**: ≤25 words — CORPUS.md:114.
- **Recheck forms**: ISO date or cadence `90d` / `180d` / `on-release` —
  CORPUS.md:105-106.
- **Used-by**: repo-relative paths of citing knowledge entries or lessons,
  comma-separated or `—` — CORPUS.md:107-108; `mined` needs ≥1 path
  (CORPUS.md:103-104) and census requires all such paths exist
  (CORPUS.md:146-147).
- **Append-only**: only `status`, `recheck`, `used-by` mutate in place, logged
  old→new in the round lesson; corrections are new rows opening
  `supersedes S0NN —` — CORPUS.md:116-118; ids never reused — CORPUS.md:89.
- **Unopened-source quote**: barred — a row is written "only after opening the
  source in the round that writes the row" (CORPUS.md:112-113); unopened
  material is a lead, "not evidence and never a row" (CORPUS.md:83); `opened`
  records the author's own open date (CORPUS.md:105).

Plus the shared admission floor from both files (falsifiability, source
anchor, observation/inference/unknown separation, append-only errata,
rejections kept, no secrets) and the knowledge-entry provenance trio
(`source:`/`verified-at:`/`recheck:`, `S###` citation for external sources —
CORPUS.md:18, 163-166).

## Method note

No commands run beyond the two file reads; all citations re-read at write time
from the current working tree. No new sources opened; no rows written.
