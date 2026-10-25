# ScribeFrontier — `Sources & frontier` section draft for the round-35 report

Seat: ScribeFrontier (round-35 w1). Scope: draft the report's `Sources &
frontier` section as text — not into the lane — under
`.ufo/waves/round-35/scratch/ScribeFrontier/draft.md`, with lane numbers
re-derived, not copied.

## Deliverable

`.ufo/waves/round-35/scratch/ScribeFrontier/draft.md` — the section text:
registry before→after with counting command, rows added by tier, rows touched
old→new, frontier rows advanced (incl. a frontier-bullet draft), and the
assimilation line.

## Numbers re-derived (every count run by this seat)

- **Before: 192.** `git show 19e4ab3171c1540c40d6b12097745af98053b07d:corpus/SOURCES.md | grep -c '^| S[0-9]'` → 192; identical 192 at r34 tip `dff394109f3c`.
- **After: 200.** Simulated land (base registry + the normalized append block `scratch/ExecAppendBlock/append-block.md`, insertion after the S202 row at `corpus/SOURCES.md:204`): `grep -c '^| S[0-9]'` → 200; `diff` shows **8 added, 0 removed** — insertion-only. Post-land re-run of the same `grep -c` on the real file is the report's verification.
- **Tier: 8/8 `own-work`, all tier A, all `status=mined`, opened 2026-10-24** (`awk -F'|' '{print $4"|"$5}' | sort | uniq -c` → `8  own-work | A`). Id space contiguous from S202 — no gap (contrast r34's S196→S201 jump).
- **Id remap, derived from the adopted entries' own `source:` lines** (package `merge/mado/knowledge/corpus/knowledge/`): S315→S203, S316→S204 (`idle-lock-never-asked-r12.md`); S327→S205 (`idle-lock-chain-armed-r14.md`); S335→S206, S336→S207, S337→S208, S340→S209, S342→S210 (`idle-lock-offered-in-the-bar-r15.md`). Cross-agrees with `reports/ExecAppendBlock.md`.
- **Rows touched old→new: 0.** The three entries cite only the eight new rows (package `source:` lines; also golden fixture `gate-quote:` lines); the append inserts 8 lines, deletes 0. No `status`/`recheck`/`used-by` cell of any existing row changes; no queued row flips to mined this round.
- **Index rows advanced: 47 → 50 (+3)** — `git ls-tree --name-only 19e4ab…:corpus/knowledge | grep -c '\.md$'` → 47; `ExecIndex.md` independently expects `indexed=50/50` post-land. Plus one frontier bullet (drafted in the section), which corrects — not supersedes — the earlier "never offers" over-read; the round-17 transition items stay open.
- **Assimilation: 3 entries admitted of 69 proposed** (`ls merge/mado/knowledge/corpus/knowledge | wc -l` = 65 new files + `find merge/mado/amendments -name '*.md' | wc -l` = 4 amendments = 69 items, `MERGE-REPORT.md`). **139 of 147 staged rows refused** (`grep -c '^| S[0-9]' merge/mado/SOURCES.append.md` = 147 − 8 = 139); **62 new-file proposals + 4 amendments refused** (65−3). Reason and flip in the draft: none cited by an admitted entry and the frozen predicate counts exactly `closed_rows=8, open_cites=0`; flip = a later round freezing a claim over those documents.
- **Entry delta re-grounded, not copied**: adopted `idle-lock-offered-in-the-bar-r15.md` §5 supersedes the package's `2026-10-06` oldest-copy figure with this round's measured `2026-10-03` (golden fixture `:42,:57,:64-65`; receipt `.ufo/waves/round-35/fetch/S209.receipt.txt`).

## Residuals for the integrator

- The **after=200** and the insertion-only claim are proven on the simulated
  union; re-run the two commands post-land (both quoted verbatim in the draft).
- The drafted frontier bullet is marked `>` quoted draft — tone matched to the
  README's per-round bullets; the scribe/lesson seats may trim it, but its
  facts are the three receipts plus the two-entry correction chain.
- `MERGE-REPORT.md` says "proposed rows refused: 0" — that is the *package's*
  count, not the lane's; the lane refuses 139 at admission time. Both numbers
  are cited in the draft without conflating them.
