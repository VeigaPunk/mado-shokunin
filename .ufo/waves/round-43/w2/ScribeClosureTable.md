# ScribeClosureTable — w2 closure-table falsification (criterion 81)

Seat `ScribeClosureTable`, mado round 43, wave `w2`, 2026-10-26. Leaf seat, no dispatch. Lane repo
`/home/vgpnk/Projects/shokunin/mado-shokunin`, lane tip at report time `2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa`;
criterion 81 read at the data commit `1959770657f1f8665097c1aed4be6c1cbb07139f` (base `a35cfdf`).

## Behavior

Ran the two things criterion 81 names and the colocated W command, read-only, from the lane root:

1. `bash .ufo/waves/round-43/w1/ScrConsiderthese/check78.sh --selftest` → `SELFTEST: PASS (12 assertions)`, `exit=0`.
2. The criterion's own Check, rounds 36-42, with `w1/ScrConsiderthese/tips.txt` →
   `TALLY rounds=7 launches=8 dead=1 complete=7 clean=3 dirty=4 relayed=7 unknown=0`, `VERDICT: TABLE_COMPLETE`, `exit=0`,
   every row `source=spotcheck`. Re-run twice as the digest grew: log sha256 `2a917544` (w1 receipt) → `4ae5c062`
   (seat run) → `69ec6152` (report time); the only differing line across the three is the digest hash the tool prints,
   and the tallies/rows are identical.
3. Criterion 81's second range 32-37 → `TALLY rounds=6 launches=8 dead=2 complete=6 clean=2 dirty=4 relayed=6`, `exit=0`.
4. Wave column recomputed with the receipt's own `git ls-tree` command at all seven tips: `114/190/37/73/96/136/0`,
   `all_files` `381/550/87/337/425/1252/29`, `closure-status.txt` ABSENT ×7 — row-for-row identical to
   `w1/ScrConsiderthese/receipt-78-wave-column.txt`.
5. Round 28 attempt field: `launches=9`, dead `7`, dead-line multiset `1×3, 2×2, 3×2` = `1,1,1,2,2,3,3`.
6. `--from 43 --to 43` on the live digest → `UNEXPLAINED round=43 launches=1 != complete+dead=0`, `TABLE_INCOMPLETE`, `exit=1`.

Artifacts: `.ufo/waves/round-43/w2/ScribeClosureTable/table.md` (the closure table and the numbered comparison),
`receipt-selftest.txt`, `receipt-t1-36-42.txt`, `receipt-t1b-36-42.txt`, `receipt-t2-32-37.txt`,
`receipt-wave-column.txt`, `receipt-unexplained-demo.txt`, `verify-quotes.sh`, `receipt-quotes.txt` (`QUOTES: PASS`).

## Gates

- **Numbers: all reproduce.** Every numeric claim in criterion 81 matches the run — both tallies, the 12-assertion label,
  the round-28 multiset, the seven-tips-ABSENT statement, `wave_md=0` beside the round-42 `complete` line
  (`watchdog.log:1462`), the `closure`/`source` value sets, `exit=1` on an `ABSENT` row, the criterion-63 pointer
  (`QUALITY.md:373`) and the M43-6 ground (`round-43.md:161`).
- **proposal.md §3.1: every number reproduces** (8 launches/7 rounds; 1 dead, round 37; 4 dirty = 36/38/40/41; 3 clean =
  37/39/42; `relayed=7`; round 42 `complete` + `wave_md=0`). No correction is needed to that sentence.
- **Two non-numeric overclaims in criterion 81 do not hold** (F1, F2 below) and one frozen-tool comment is wrong (F3).

## Findings

- **F1 — the named Check omits the `work` count it mandates.** Criterion 81 requires three separately counted things
  (attempts, cleanliness, work) but its `Check:` names only `check78.sh`, whose header is
  `round launches dead complete closure source cite` — no wave column — and which contains no `ls-tree` call. The
  `wave_md=0` figure it quotes comes from the separate W command in `proposal.md` §1 that §3.1 names and criterion 81
  drops. Under criterion 10 the `work` cell of the criterion has no re-derivation command.
- **F2 — `--selftest` does not show the `UNEXPLAINED` rejection it is credited with.** The "Shown able to fail" list
  credits `--selftest` with "rejects a launch with no outcome line"; the fixture's five in-range rounds all satisfy
  `launches == complete + dead` (r2 is 2 = 1 dead + 1 complete), so that branch is never entered. The branch is real and
  fires on the live digest (round 43, `exit=1`); the selftest's `exit 1` assertion rests on the `ABSENT` row instead.
  The other credited rejections (ABSENT/`TABLE_INCOMPLETE`, prefix collision, later dirty behind earlier clean,
  non-empty witness → DIRTY) do hold in the fixture.
- **F3 — `check78.sh:17-18` repeats the figure the criterion corrected.** It says "round 28 carries attempt=1 seven times,
  corpus/lessons/round-40.md:150"; measured, `attempt=1` appears 8 times across round-28 lines, 3 times on the seven dead
  lines, and the cited sentence is at `round-40.md:148-149` (`:150` reads "the known round-31"). Criterion 81's own text
  carries the corrected multiset, so the criterion is right and the frozen tool's comment is wrong in number and locator.
- **Observation, not a defect:** the label's `12` counts distinct assertions; 13 `ok=0` guards exist and two (`tally4`,
  `tally`) repeat the same TALLY grep. The printed string is what the criterion quotes, verbatim.
- Corrected sentences for F1/F2 and for the tool comment are drafted in `table.md` §5; criterion 81's numbers are
  unchanged by the correction.

## Touched surfaces

Wrote only inside the seat directory: `table.md` plus six receipts, `verify-quotes.sh`, `receipt-quotes.txt`. No tracked
file edited, no counter/control/registration/fetch touched, no git/jj mutation, no pacman, no `hyprctl`/compositor
command, no host-service interaction. Scratch `(/fast/scratch/hyaku/mado-r43/ScribeClosureTable)` removed after copying
receipts. No tools installed.

## Out of scope

- No re-registration and no edit of `QUALITY.md`/`check78.sh` — w2 reports holes as open defects of the landed data; the
  fix belongs to the L1.
- Criterion 81's `proposal.md` §2 figures were spot-checked only where they support §3.1 (`§2.2` `0`/`22`;
  `§2.3` `inline.sh:172` WARN / `:176` complete / `5f4fa8d8^:126`); no full §2 audit.
- The tool's token classifier was not adversarially re-fuzzed beyond the selftest's five fixture cases and the seven
  live row classifications, which were re-read against their cited lines.
- Seats-versus-files mapping for the `work` column: not attempted (criterion 81 defines it as a markdown count).

Report: `.ufo/waves/round-43/w2/ScribeClosureTable.md`
