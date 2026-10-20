# ScoreResultsDraft — report

Seat: MadoR18.ScoreResultsDraft (scribe, leaf). Scope: draft the round-18 SCORECARD
results skeleton only.

## Behavior
- Wrote `.ufo/waves/round-18/drafts/ScoreResultsDraft.md` (only assigned file). It holds
  the "Round 18 — committed results and bounded author verdicts" skeleton, in the layout of
  the round-17 section.
- Contents: claim table for C1/C2/C3 with before-values and `[PENDING]` after-values;
  C1 routed-defect table (R17-V1, R17-V2, R17-V5, JjAuditMado F10); C2 route table
  (`walker-route-r18.md` P3, `theme-route-r18.md` P5, S0xx-pending ids, fetch receipt
  paths); C3 frozen-gate check table; capability row skeleton; sources/saturation
  placeholders; harm-watch table; per-axis verdict placeholders; Planned round 19 candidates.
- No number was invented. Every after-value is `[PENDING: …]`.

## Baselines read (verified this seat)
- `.ufo/waves/round-18/evidence/measure-before.json` (rev d9a5a18): c1 15/23 = 6.5217;
  c2 4/6 = 6.6667 with P3 and P5 uncovered; c3 tool present, sha `962919ce…`.
- SCORECARD tail (lines 931–984) read: Round 18 pre-registration claims, targets and harm-watch list.
- SCORECARD lines 897–918: Round 17 results (sources 71; A 64; C 6; mined 56; rejected 7;
  saturation 9.0 / N=3; hermetic selftest 372/372; classifier 52/52; navigation 32/32; U 7/7;
  tripwire suites 9/16/33/30; census exit 0).
- SCORECARD lines 921–929: Round 18 planned items (source for round-19 candidates).

## Markings
- `[INFERENCE]` on the jj routed-fix baseline row: the pre-existing defect is taken from the
  JjAuditMado F10 finding and was not re-read in the lane this round.
- `[PENDING]` on every measured or verdict cell; `S0xx-pending` for draft source ids (L1 assigns).

## Not done (by design)
- No measurement, selftest or frozen run was executed; the commands in the draft are declared only.
- No fetch, no pacman/yay/systemctl or other host command, no jj, no git write. Git was used
  read-only once (`git log`, `git show --stat d3a0000`) to confirm the pre-registration commit.
- No edits to SCORECARD.md, LOG.md, lessons, or any corpus file.

## Out-of-scope items noted
- `.ufo/waves/round-18/drafts/` did not exist before this seat; the write created it.
- The round-17 SCORECARD line 915–916 names the "post-hoc transcript tripwire" capability with
  first-working round 17; the round-18 capability row is a new row and was not merged into it.

## Findings for L1 integration
1. The round-18 results headers should use `Round 18 — committed results and bounded author verdicts`.
2. Before-values in the draft are round-17 committed numbers; L1 should re-check them against
   the final SCORECARD tail when it integrates.
3. The draft says the frozen-gate row moves to `gate` only if the frozen run is demonstrated;
   keep that condition when filling it in.
4. The Round-19 candidate list cites the walker 2.17.2 and hyprland 0.56.2-4 pins; the
   hyprland version is taken from the wave brief and has not been checked against file bytes
   by this seat.

## Tools
- None installed or updated by this seat.
