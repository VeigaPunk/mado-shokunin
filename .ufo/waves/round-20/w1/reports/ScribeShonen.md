# ScribeShonen — all four SHONEN boxes stay `[~]`: no named non-author verifier exists for round 20

Draft: `.ufo/waves/round-20/w1/drafts/ScribeShonen.md` (four `[~]` lines, each with a resolvable pointer). Nothing else written.

## Findings

1. **No `[x]` is earned in round 20.** The only non-author record for the round-19 lane is `corpus/lessons/round-19-verifier-spotcheck.md` (commit `1f7f995`, sha256 `dcb7a913…fea0a0`, integrator ClosureMadoR19, dispatched reviewers GateOm10Check, TripwireCaseCheck, IncidentCheck, DiscernmentCheck). Its own statement: "SHONEN boxes are **not all newly checkable from this review**: neither current no-oral-context execution nor end-to-end desktop behavior was verified here. No box was edited" (`:143`). Its adjacency verdict "unchanged … no new cross-domain absorption evidenced in this review" (`:139`) is not a PROVINCE accuracy check. Round 20 has no closure yet (the wave is in flight; `round-20/w1/reports/` is empty), and every round-20 seat is lane-dispatched (`MadoR20.*`), which the rules do not count as non-author.
2. **Round-20 changes touch no box's scope.** The pre-registration (`SCORECARD.md` at `e629f73`, `## Round 20 — declared claims`) names C1 (tripwire precision, tool/suite/counter) and C2 (QUALITY criteria 29/30). Neither claims SHONEN scope, so the expected SHONEN diff for round 20 is empty. The draft therefore keeps the round-19 state.
3. **Historical `[x]` do not carry forward.** Box 2 `[x]` (VER-M3, round 4) and box 4 `[x]` (VER-M4B, round 5) are cited in `SCORECARD.md` move-log rows 4–5. The round-5 box-4 receipt `corpus/knowledge/province-accuracy-selfaudit.md` predates the round-19 `PROVINCE.md:18` line (omarchy theme state IN/OUT split), so it does not cover the current PROVINCE text. Current `SHONEN.md` (`:5,7,9,11`, all `[~]`) is the authority and was not modified.
4. **Round-19 SHONEN lines are consistent with the closure, with two pointer-form defects for L1 to fix in the round-20 report:**
   - Box 3 cites `evidence/final/*.txt` with no root. Resolved against the lane, the path is `.ufo/waves/round-19/evidence/final/` (14 entries incl. `harm/`). The fleet-root report needs the lane-relative form so the pointer resolves from the fleet repo.
   - Box 3's "67 wave-2 seats" is correct as a count: `.ufo/waves/round-19/w2/reports/` holds 67 `.md` reports plus `swarm-registry.json`. The claim remains author-side (lane-dispatched), which the round-19 report already says.
5. **Pointer resolution (all checked present at `mado-shokunin` master, read-only):** `SKILL.md:572` and `:577` (registry rows `mado-anchor-durability` and `mado-fresh-pins`); `SKILL.md:1853-1855` (round-19 errata, walker 2.17.2, S090/S096); `LOG.md:1312` (round-19 entry header); `PROVINCE.md:18` (round-19 refinement); `corpus/knowledge/executor-test-sufficiency.md`, `config-health-report-r3.md`, `province-accuracy-selfaudit.md`, `output-colour-boundaries-r14.md` (all exist); `corpus/lessons/round-19-verifier-spotcheck.md:98-106` (the closure's source-reopen table), `:139`, `:143`; `.ufo/waves/round-19/w1/reports/ConnProvinceRoster.md`, `.ufo/waves/round-19/w2/reports/AtkProvinceLine.md`, `ProvinceScope.md` (exist).

## Evidence pointers (sha256, read-only)

- `SHONEN.md` working copy `c723b741…3e99` = `e629f73:SHONEN.md` (unchanged since the pre-registration).
- `corpus/lessons/round-19-verifier-spotcheck.md` `dcb7a913…fea0a0` = `1f7f995` blob.
- `PROVINCE.md` `1b25bb1e…7464b`; `LOG.md` `27f6bb64…769`; `SKILL.md` `41287d7e…1b84`.
- `/home/vgpnk/Projects/shokunin/.ufo/reports/round-19/mado.md` `117207f0…57c9` (SHONEN section at `:145-150`).
- Round-20 draft: `.ufo/waves/round-20/w1/drafts/ScribeShonen.md` (written by this seat).

## Judgement

- Box 1 `[~]`: the closure re-opened five cited source rows (S096, S097, S098, S084, S094) and agreed; decision tables, error patterns and checklists were not checked by any non-author seat.
- Box 2 `[~]`: the round-19 entry is a file-plane re-anchor; the closure says desktop behaviour was not verified.
- Box 3 `[~]`: 67 wave-2 reports re-ran the commands, all lane-dispatched; the closure did not re-run them.
- Box 4 `[~]`: lane-dispatched PROVINCE routing reports; the closure's adjacency verdict is not an accuracy check.

## Limits

- I did not verify the contents of `SKILL.md` decision tables, error patterns or checklists; I checked only that the cited rows and errata lines exist.
- I did not re-read the 67 wave-2 reports or the 14 `evidence/final` files for content; I checked existence and counts.
- I did not re-run any gate, selftest, regression, measure, probe, or census command. No `measure.py`, `tw-recall.py`, `fresh-pins.py`, `tools/mado-verify.sh`, or live `hyprctl`/`pacman`/`systemctl` action.
- I did not check round-20 SKILL or LOG text because round 20 has not landed it. Round-20 SHONEN lines must be re-drafted if a box-scope change lands and must still stay `[~]` unless a named non-author verifier checks the box.
- I did not verify the historical VER-M3 / VER-M4B receipts (`/tmp` verdicts are ephemeral per `SCORECARD.md` row 4–5).

## Installs

none
