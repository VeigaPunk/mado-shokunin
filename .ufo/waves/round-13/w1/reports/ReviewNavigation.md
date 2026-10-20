# ReviewNavigation — report (MadoR13.ReviewNavigation, w1)

Date 2026-10-20. Baseline `7dcb785b7b943d03703181b218d7860a7b43007b`. Read-only; no builds, tests, lint, or `tools/mado-verify.sh` runs. Tooling installed or updated: none. External source opens: none. Full detail and fixtures: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/ReviewNavigation.md`.

## Baseline (OBS)
- Navigation fence sha `8b59b503…` matches `SCORECARD.md:236`; notes 26, README rows 26, distinct 26.
- Head-15 source-cited entries 4; `covers:` U1 (`corpus/knowledge/window-rule-effects-getprop.md:6`), U2 (`hyprland-config-era-r12.md:6`), U3 (`xdg-portal-routing-r12.md:6`). No U4 entry.
- `corpus/SOURCES.md`: 39 rows. Current histogram `mined=27 queued=9 rejected=3`; recorded round-12 histogram `mined=28 queued=9 rejected=2` (`.ufo/evidence/round-12/after.txt:58`) predates the S030 in-place flip (`SOURCES.md:91`). Same total, different statuses.
- U4 candidates today: S005 queued (`SOURCES.md:16`, anchor `main 3dac056d`), S006 queued, S010 tier C (never sole support).

## Findings
1. **MAJOR — numerator not intersected with mined join.** `after-measure.sh:24` counts `covers:` from any note with a head-15 S-token; `:25` checks mined status separately and prints only violations. Fixture `source: S011` (rejected) + `covers: U4` yields `covers: U4`.
2. **MAJOR — no tier check.** Nothing tests that a U4 claim has an A-tier row; S010 (C) or S008 (B) sole support passes. Contract `SOURCES-CONTRACT-v1.md:26-30` requires otherwise.
3. **MAJOR — working tree vs REV.** The C3 join reads the working tree; navigation reads committed REV (`SCORECARD.md:70-89`). Mixed state with a dirty tree.
4. **MODERATE — raw counter vacuous.** `SCORECARD.md:237` second command counts lines (F6 class, unfixed).
5. **MODERATE — token truncation.** `grep -oE '^covers: U[1-7]'` turns `covers: U10` into U1 and hides U4 in `covers: U1, U4`.
6. **MODERATE — silent exclusion.** `source: none` + `covers: U4` is counted by raw grep but dropped from the join with no violation line.
7. **MODERATE — whole-file reciprocity.** `grep -qw` over the body lets a body-only mention satisfy used-by; reciprocity must use the head-15 source line.
8. **MODERATE — census gaps.** Contract census line 80 skips used-by `—` on mined rows; census checks counts and enums but not ID-set equality, so a same-count replacement passes (same defect class as C2).
9. **MINOR** — substring `index()` path match; `sort -u` hides which file covers which item; navigation is silent about uncommitted notes (by design).

## Exact U4 joins for the final measurement
- J1 `corpus/knowledge/wayland-protocol-boundaries-r13.md` exists at REV (planned name from `spec.json` ProtocolPhases).
- J2 head-15 only: `verified-at`, valid `recheck:`, `source:` with ≥1 S-ID, exactly one `^covers: U4$`.
- J3 each cited ID: row `mined`; used-by exact-equal to the slug.
- J4 reciprocity: every mined row naming the slug is cited on its head-15 source line.
- J5 ≥1 A-tier row for the U4 scope; no C-only or B-only support.
- J6 registry ID-set equality (planned S040, S041, optional S042 superseding S006 with revision, optional S043) and re-recorded histogram.
- J7 exactly one README row `| \`knowledge/<slug>.md\``; navigation `indexed=27/27`, exit 0 at committed REV; Frontier `README.md:92-93` edited only for the closed part.
- J8 manual: `corpus/lessons/round-13.md` logs S005 queued→mined and each new row (no such file yet).
- J9 manual: S005 anchor SHA and `opened` date consistent with note `verified-at`.

## Same-count fixtures that must FAIL before accepting a 4/7
Rejected-only source; queued-only source; two `covers: U4` notes with one invalid (name the invalid file); `covers: U10`; `covers: U1, U4`; `source: none`; body-only mention; used-by `—` on a mined row; same-count registry replacement; dirty tree. Positive control: U1–U3 must still yield exactly 3 joined items.

## Gaps
Spec in the draft is not implemented or run here (main agent verifies once). Topical fit of sources to the three U4 sub-claims needs a named non-author reviewer. S041 host capture supports only host scope; advertisement ≠ bind/use needs S043 (core registry, A-tier), not S006 or S041 alone.
