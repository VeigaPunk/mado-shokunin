# R77ExecRepairs — carried-defect repair pack (r76 spot-check D1–D8) + cited-revision probe

Seat: R77ExecRepairs (executor), round mado 77 wave 1. Date 2026-11-04.
Lane HEAD when the pack was built: `0fa69f41d81275db102bbe08cf5d6a86a5dfe8f7`.
Scratch: `/fast/scratch/hyaku/mado-r77/R77ExecRepairs/` (created, used, deleted before finish).

## Axes

- **Coverage (C1 lineage)** — the repair pack closes the round-76 closure's routed provenance and
  pointer defects as append-only text: D1 provenance trios, D2 revision label, D3 declaration and
  docstring text, D4 mistake count, D7/D8 pointers.
- **Operability (C2 lineage)** — one executable check turns the D2 class into a check that fails
  on the defect and passes after correction: `check-cited-revisions-probe.py`, red on
  `SCORECARD.md:4339` as landed, green on the corrected row.

## State discovery (ground: current bytes, not assumption)

The lane already carries the round-77 integration commit
`3e35d0a9672b49cd1d908cf821c8a3c6e33e6696` ("… r76 D1-D4/D7-D8 corrections and docstring
parity"). Verified landed at HEAD:

| defect | landed at | verification |
|---|---|---|
| D1 | `corpus/knowledge/outcome-field-r76.md:112`, `interprocedural-del-r76.md:96` | `grep -n 'Correction (round 77)' …` → both headings |
| D2 | `SCORECARD.md:4393-4398` (append under the round-76 section) | `git log -1 --format=%H -- quality/counters/c2-r76-shapes.py` → `3588a527…` |
| D3 numeric text | `.ufo/waves/round-76/claims-declaration-r76.md:191` errata; counter lines 38/52; `receipts/parity-r76-docstring.txt` | `git diff 2308e12a HEAD -- quality/counters/c1-r76-outcome-field.py` = 2 insertions / 2 deletions |
| D4 | `corpus/lessons/round-76.md:185` D4 item | `grep -c '^\| M76-' corpus/lessons/round-76.md` → `5` |
| D7/D8 | `corpus/lessons/round-76.md:185` D7/D8 items | `git diff-tree` / `git ls-tree` outputs in `correction-d7-d8.md` |
| D5/D6 | dispositioned in the round-77 LOG/declaration; D6 files are tracked (`git ls-files -- .ufo/waves/round-76/w1.ready …` prints all three) | not this seat's repair |

**Still open at HEAD — the delta this seat closes:**

1. **D3 stale mutant list.** The landed fix replaced only the two numeric strings; docstring lines
   26–29 still name the superseded mutants (`outcome-term-dropped`, `prefix-match`,
   `first-witness-wins`, `case-insensitive`). Replaced on my copy with the four frozen observable
   mutants and a parity run.
2. **No executable cited-revision check exists in the tree** (grep for `cited-revisions` finds only
   the round-77 spec/lesson text naming `R77ExecRepairs` as its author). Delivered here.

## Deliverables (in this dir)

- `correction-d1.md` — both `## Correction (round 77)` blocks verbatim; rows and fields named;
  landed-state verification. Rows: S450 + S455 (C1 entry), S453/S454/S455/S456 (C2 entry).
- `correction-d2.md` — stale `5dade9b3` → `3588a527`, with the re-derivation command, the file's
  history and the landed append.
- `correction-d3.md` — declaration:26 errata quote; exact docstring lines; the four-line text-only
  replacement; parity reference; landing note.
- `correction-d4.md` — count = **five** mined mistakes (M76-1…M76-5), derived by
  `grep -c '^| M76-' corpus/lessons/round-76.md` → `5`; the wrong counts (report six, LOG/commit
  four); the separate six-said/eight-listed repair tally; the landed lesson item and a LOG append.
- `correction-d7-d8.md` — D7 `git diff-tree -r 2308e12a` → only the harm-watch receipt, census at
  `e160d18e`; D8 `git ls-tree` proofs for the tally paths; both landed lesson items quoted.
- `check-cited-revisions-probe.py` — executable check (read-only; one `git log -1` per run;
  exit 2 on "no claim", never a green on an empty find).
- `red-row.txt` / `green-row.txt` — the exact `SCORECARD.md:4339` row (sha256 `8cc73b67…`) and the
  single-hash correction (sha256 `22819aeb…`); the only diff is `5dade9b3` → `3588a527`.
- `red.txt` — probe on the r76:4339 text: `RESULT red claims=1 mismatched=1`, exit 1.
- `green.txt` — probe on the corrected text: `RESULT green claims=1 mismatched=0`, exit 0.
- `parity.txt` — counter before/after the four-line docstring substitution: identical contract
  lines, rc 0 both; source diff touches docstring lines 26–29 only.

## Retained evidence (exact)

- `git log -1 --format=%H -- quality/counters/c2-r76-shapes.py` →
  `3588a527eba555a94e497097b0467efc04274c6d`; history `3588a527` (last), `5dade9b3`, `755b339f`.
- `git diff-tree --no-commit-id --name-status -r 2308e12a` →
  `M .ufo/waves/round-76/receipts/harm-watch-r76.txt` (only).
- `git diff-tree --no-commit-id --name-status -r e160d18e` → `A census-end-r76.txt` (+ the C2 final
  measurement and harm-watch; `LOG.md`, `SCORECARD.md`, the C2 entry modified).
- Probe: `instrument=quality/counters/c2-r76-shapes.py last_change=3588a527…`; red claim
  `5dade9b3 match=no`; green claim `3588a527 match=yes`.
- Parity: before sha256 `e6ce2a48…`, after sha256 `5984477a…`; both print
  `MADO_R76_OUTCOME_FIELD: cases=16 correct=16 mutants=4 killed=4 base_killed=0 verdict=TARGET_MET rev=3588a527eba555a94e497097b0467efc04274c6d`, rc 0.
- D4: rows at `corpus/lessons/round-76.md` lines 48, 49, 50, 51, 53; distinct ids M76-1…M76-5.
- D6: `git ls-files -- .ufo/waves/round-76/w1.ready .ufo/waves/round-76/w1.ready.dispatched
  .ufo/waves/round-76/w1-run.err` prints all three (tracked).

## Risks / blockers

- **Duplicate-landing risk.** D1/D2/D4/D7/D8 are already landed at `3e35d0a9`; the pack texts are
  byte-matched to the landed blocks. A re-landing should adopt them only where absent; the
  genuinely new bytes are the D3 four-line docstring fix and the probe with its receipts.
- The green fixture is corrected row *text*; the historical row stays stale (append-only), and the
  correction names it. The probe proves the class, not a row rewrite.
- No host probe, no config/compositor/service write, no package transaction, no install.
- Scratch deleted; the parity copies lived there and are identified by sha256 above.

## Report

Report: .ufo/waves/round-77/w1/R77ExecRepairs.md
