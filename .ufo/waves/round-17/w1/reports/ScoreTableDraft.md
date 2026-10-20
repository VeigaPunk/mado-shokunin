# ScoreTableDraft — round 17 scoped report

## Behavior
Wrote an unmeasured SCORECARD results skeleton for round 17 at
`.ufo/waves/round-17/drafts/ScoreTableDraft.md` (only file written besides this report).
Shape follows the round-16 section (SCORECARD.md lines 737–819): committed-results
header, claim table, capability table, harm-watch and admission block. Every
measured value is a `<…>` placeholder. No number was invented.

## Sources read
- SCORECARD.md lines 736–865 (round-16 style and the round-17 declared-claims tail,
  lines 821–865; pre-registration C1 target ≥15/23, C2 target 4/6, C3 capability).
- Existence checks: `PROVINCE.md`, `corpus/lessons/round-16-verifier-spotcheck.md`,
  `corpus/QUALITY.md` present. `tools/mado-tripwire.py` and
  `.ufo/waves/round-17/measure.py` absent at time of check; the skeleton lists them
  as to-be-run commands and does not claim they run.

## Gates and harm watch
Skeleton harm-watch rows: hermetic 372/372, classifier 52/52, U 7/7, navigation,
census. Each is marked for re-observation at `<REV-after>`; none is asserted.

## Findings for L1
1. `tools/mado-tripwire.py` and `.ufo/waves/round-17/measure.py` do not yet exist.
   The skeleton's command block depends on both; L1 must confirm they land before
   measurement.
2. The pre-registration names the 14/22 literal baseline but the skeleton does not
   recompute it; L1 should decide whether the measured-run receipt recomputes it.
3. Round-16 table used `Before → after` with the delta inline; the skeleton keeps
   that, with `<delta>` placeholders.

## Host-pause compliance
No pacman, yay, paru, sudo, systemctl, hyprctl, libinput, evtest, omarchy-*, or
live probe was run. No tool was installed. No `jj` command was run in the lane.
Tooling record: none (no install performed).

## Out of scope
No edits to SCORECARD.md, LOG.md, PROVINCE.md, corpus, or tools. No delegation.
