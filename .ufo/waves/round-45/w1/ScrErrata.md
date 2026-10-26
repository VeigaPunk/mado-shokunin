# ScrErrata — round-44 closure D2, D3, D7 errata (round 45, w1)

Seat: `ScrErrata` (scribe). Lane `mado-shokunin`, base `0c89478af821a6424c9ac922eafe02e39630cf4f`, round-45 freeze
`22a8dedd02f507689c567777e0f20b5e645c8ce0`. Deliverable: `.ufo/waves/round-45/w1/ScrErrata/errata.md` — append-ready
text for the Round 45 SCORECARD errata, one block per routed defect, nothing rewritten.

## Behavior

Read-only seat. No lane file edited; no counter, control, registration, reference or pin touched; no product code; no
mutation of the lane's git index; the only writes are this report, the seat directory, and one `/fast/scratch` clone.

1. **D2 (after values).** Verified the Round 44 claim rows answer with pointers (the C1 cell "see
   `receipts/c1-after-data.txt`", C2 "see `receipts/c2-after-data.txt`", both self-verdict cells "recorded in the round
   report from the receipts", `SCORECARD.md:2570`, `:2571`) and extracted the values: C1 `fixtures=26/26 tool=present
   verdict=TARGET_MET` (clauses a/b/b4/b5/e/g/r 1) and C2 `admitted=1/1 verdict=TARGET_MET` (clauses a-j 1), exit 0, at
   the data commit `e4678921` (`receipts/c1-after-data.txt:53`, `c2-after-data.txt:29`) and at `74c606a`
   (`*-after-tip.txt:53` / `:29`); axis `checked=3 mismatched=0` (61/61, 71/71, 12/12) at both. Tip receipts are
   byte-identical between the round-44 tip and the round-45 base.
2. **D3 (tip-receipt equivalence).** `8ac15c41^` = `74c606a`; `git rev-list --count 74c606a..8ac15c41` = 1;
   `git diff --name-only 74c606a 8ac15c41` = 599 files, **0** outside `.ufo/waves/round-44/`; the seven counted surfaces
   (tool, entry, `SOURCES.md`, `SKILL.md`, lesson, `QUALITY.md`, `SCORECARD.md`) have an empty `git diff --stat`. Rather
   than rest on that, I **measured the tip** in a `--shared` clone at `8ac15c41`: C1 `26/26 TARGET_MET`, C2 `1/1
   TARGET_MET`, axis `3/3 MATCH`, all exit 0 (fixed nonce `4515d3c3e0e0` for C1 so the line reproduces).
3. **D7 (`w2/ConnCalibration.md`).** Re-checked all six findings. F1 stands (LOG says M44-1..7, the lesson holds 9,
   SCORECARD:2583 says M44-1..9); **F2 is withdrawn — the artifact exists** (`git ls-tree e4678921 --
   .ufo/waves/round-44/assimilation/renumber-map.tsv` → blob `c9639ce8…`, landed in the freeze `e2289516`; the finding's
   own commands were lane-root-relative and printed empty); **F3 is reclassified** (the SKILL paragraph quotes the
   round-43 receipt's `clients=4` and is byte-unchanged from base `6a1a905`; the round-44 run is `clients=3` — the
   adjacency, not the number, is the defect); F5 stands (0 w1 files at `e4678921` and `03fa5c61`, 848 at `290cddea` and
   `8ac15c41`); F6 stands (`check83.py` absent at `e4678921`, present from `290cddea`); F4 is closed by the tip commit and
   its "tip" premise corrected (`290cddea` is two commits behind `8ac15c41`). Added one coverage erratum: the calibration
   never flagged D2 itself.

## Gates exercised

- Quote gate: every quoted fragment is ≤ 25 words, located by a computed `grep -nF` locator, and must appear verbatim in
  the errata text — `python3 .ufo/waves/round-45/w1/ScrErrata/verify-quotes.py` → `QUOTES: 28/28 verified`, exit 0
  (`receipts/quotes-verify.txt`, `receipts/quotes-grep.txt`).
- Localisation gate: the lesson's cited line numbers (5, 26, 71, 82) are identical at `e4678921` and at the base (the
  data→base diff is +14 lines, all appended) — `receipts/lesson-lines.txt`.
- QUALITY 83, executed at the data commit: `CHECK83: verdict=FAIL citations=13 violations=1 outside=7 rev=e467892`,
  exit 1; the single violation is the `w1-results.json` LATE row, which corroborates F5 (`receipts/d7-check83.txt`).

## Touched surfaces

- Wrote: `.ufo/waves/round-45/w1/ScrErrata.md` (this report), `.ufo/waves/round-45/w1/ScrErrata/` (`errata.md`,
  `quotes.tsv`, `make-receipts.sh`, `verify-quotes.py`, `receipts/` — 10 files).
- Scratch: `/fast/scratch/hyaku/mado-r45/ScrErrata/` (shared clone at `8ac15c41`, counter work dir), deleted before
  yielding. No `/tmp` artifact is cited.
- Read-only: `SCORECARD.md`, `LOG.md`, `SKILL.md`, `corpus/lessons/round-44.md`,
  `corpus/lessons/round-44-verifier-spotcheck.md`, `corpus/QUALITY.md`, `.ufo/waves/round-44/**`,
  `quality/counters/c1-r44-geometry-states-v2.py`, `quality/counters/c2-r44-gkeep-size-request-v2.py`,
  `quality/check-axis-scores.py`. Host: untouched (no `hyprctl`, no compositor or service call).

## Findings (what each attacks)

- **D2 closed**: after values and verdicts exist and reproduce at the data commit, at `74c606a` and at the tip; the
  published rows (`SCORECARD.md:2570-2571`) stay byte-identical, the errata appends the values.
- **D3 closed**: the tip receipts measure `74c606a`, the tip's parent; the equivalence is now both structural (599/599
  files inside the wave dir, counted surfaces byte-identical) and measured at `8ac15c41`.
- **D7-1 (F2, the consequential one)**: `.ufo/waves/round-44/w2/ConnCalibration.md:38` asserts "no `assimilation/`
  directory or any `renumber-map*` file exists in the repo" — false, and the lesson's three citations are resolvable.
  A round-44 lesson correction based on that finding would have been wrong; the errata records the withdrawal.
- **D7-2 (F3)**: `.ufo/waves/round-44/w2/ConnCalibration.md:50` compares two different host runs; the SKILL number
  matches `.ufo/waves/round-43/receipts/live-geometry-host.txt:10`, so the fix is one attribution word.
- **D7-3 (F1, F5, F6, F4, tip definition, D2 gap)**: confirmed/corrected as in `errata.md` ER-D7.1/4/5/6/7.

## Out of scope / not attempted

Entry content, pins, controls, the round-45 claims (C1 tool, C2 entry), the host, and any rewrite of
`SCORECARD.md`/lesson/calibration text. D4 (nonce-dependent base share) and D1/D5/D6 are other seats' items; the C1
base share was not re-run here.

## Tooling

None installed. `python3` (stdlib only) and read-only `git`; no `pacman`, no package transaction, no network fetch.

Artifacts: `.ufo/waves/round-45/w1/ScrErrata/errata.md`,
`.ufo/waves/round-45/w1/ScrErrata/receipts/{d2-after-values,d3-structure,d7-truths,d7-check83,lesson-lines,quotes-grep,quotes-verify,c1-tip-8ac15c41,c2-tip-8ac15c41,axis-tip-8ac15c41}.txt`.
