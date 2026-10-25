# ScribeLesson — round-34 `## Mistakes` draft

Delivered: `.ufo/waves/round-34/scratch/ScribeLesson/mistakes.md`. The lesson file
was not edited; the L1 writes it.

Style: `corpus/lessons/round-33.md` `## Mistakes` — one row per mistake,
`class:` / `evidence:` / `captured-by:` / `fix:`, append-only corrections named
rather than edited. Class vocabulary extended only where the r33 set did not
cover the defect (`disclosure`, `overclaim`; `reference-drift` reused from the
r32 lesson's anchor row).

## Rows and their evidence

1. **ledger — the false SCORECARD r32-C1 row.** Persists as written: target met
   at `cited_entries=3`; independent counter prints `cited_entries=7`
   (`corpus/lessons/round-33-verifier-spotcheck.md` item 1; line 63).
   Correction is append-only `r33-claim-verdict` at `SCORECARD.md:2097`
   (verified: `grep -n r33-claim-verdict SCORECARD.md`), introduced by
   `d40b35f90ad8bf630ad9404d25aeee1d9737f300` (`git log -S`). captured-by: none
   at write time.
2. **instrument — frozen r33 counter accepts the symlink crib.** Spotcheck
   §Claims (lines 58–61): `TARGET_MET` on `scratch/CriticC1Junk`; the fix script
   was never substituted. Round-34 receipts verified in-tree:
   `controls/r33-counter-on-its-crib.txt` = `TARGET_MET`,
   `controls/c1-symlink-crib.txt` = `TARGET_MISSED` under `PRED-C1-r34-v1`.
3. **reference-drift — S189 line number.** Byte-verified: `.ufo/waves/round-32/fetch/S189.bin`
   line 169 is `const size_t MAX_QUEUED_EVENTS = 64;`; line 128 is the
   `eventString` assignment. `corpus/lessons/round-33.md` §Gate self-contradicts
   (169 at line 15, 128 at line 23). Correction marker `r34-s189-line: line=169`
   verified at `SCORECARD.md:2108`, introduced by `fa7ba11346116672352b5d41494141c5c4d738d0`.
4. **disclosure — 12 undisclosed scratch trees.** Spotcheck §Uncommitted paths:
   19 untracked dirs, report names 7. The 12 seat trees still exist on disk
   (`git status --porcelain` confirms). Size misclaim byte-verified:
   `du -sb .ufo/waves/round-33/scratch/ExecK2Receipts` = 495961904 vs the
   report's 547 MB (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/mado.md:58,131,173`).
5. **overclaim — quality trend.** Report §Trend verdicts (line 103) says
   improved; spotcheck §Trend verdicts (line 116) says unchanged. Both read
   directly; no third-party judgment substituted.

## Caveats for the L1

- `captured-by: none` appears three times. That is the honest answer — the r33
  lane had no gate for ledger falsity, disclosure completeness, or self-scored
  trends; each was caught only by the outside closure.
- The 12 trees are still present; the fix row says "dispose with a named
  disposition" per routed defect 4, not that they are gone. `ScoutScratch12.md`
  exists in this wave's reports if the L1 wants the seat's enumeration.
- Fleet-side report path is cited for the trend and 547 MB claims; those bytes
  live outside the lane repo.
