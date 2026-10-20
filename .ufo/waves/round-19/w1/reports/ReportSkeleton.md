# ReportSkeleton — round-19 report skeleton drafted with placeholders only

Axes named (godspeed step 1): (a) required-section completeness against the round-prompt §4 contract;
(b) placeholder discipline (no invented values); (c) fidelity to the round-18 model. Only (a) and (b)
were scored; (c) was read against the model, not measured.

## Findings

- Draft written: `.ufo/waves/round-19/drafts/ReportSkeleton.md` (7936 bytes). `drafts/` did not exist; created in the lane.
- Required sections present in order: Work performed (opens with C1/C2/C3), Landed changes, Before → after
  measurements, Sources & frontier, Trend verdicts, SHONEN (4 boxes, matching `SHONEN.md` 4 boxes), then
  Stale-lane, Installs, Open L0 questions, Host, waves table, planner mapping. Source for section order and
  marker rule: `templates/round-prompt.md` §4.
- Declared baselines (18/26 = 6.9231; 2/13 = 1.5385; 3/6 = 5.0000) are shown only as declared values from
  `SCORECARD.md` "Round 19 — declared claims". Measured before and all after cells are `⟨…⟩`.
- Reserved SOURCES ids (S096, S097, S098, S099–S105) are carried as in the brief; none are verified here.
- Planner mapping: `scripts/hyaku/lane-addendum.md:63-66` (L1 holds the planner seat; validator rejects `planner`).
  [INFERENCE] `scripts/hyaku/ufo-wave-policy-v2.json` still defines a `planner` role at lines 99–100 and 212–213.
  That is a policy-definition versus validator-ruling inconsistency for L1 to reconcile; I did not change it.
- Wave table left as placeholders: `w1/spec.json` and `w1/dispatch.json` exist, but seat counts, role mix and
  dead seats are outcome data and wave 1 was still running at drafting time. Not counted.
- Current baseline and pre-registration commits resolve: `9c54c56` and `17661e0` (`git cat-file -t`, read-only).
- No validator script was found under `scripts/` or `templates/` by grep for `planner`; the validator itself was not located.

## Commands run

- `read` on `.ufo/reports/round-18/mado.md`, `SHONEN.md`, `SCORECARD.md` (round-19 section), `templates/round-prompt.md`, `scripts/hyaku/lane-addendum.md`, `scripts/hyaku/ufo-wave-policy-v2.json` (grep).
- `git cat-file -t 9c54c56` and `git cat-file -t 17661e0`: both `commit` (read-only).
- `mkdir -p .ufo/waves/round-19/drafts` inside the lane (filesystem only, no git or jj write).

## Installs

none

## Limits

- Did not run any measure, census, gate, harm watch or tripwire command; the draft contains no measured values.
- Did not read `w1/spec.json` role entries or `task-result.json`; wave counts left open.
- Did not verify the host walker bytes, `/var/log/pacman.log:2929`, or the outside-input routing text; cited as given in the brief.
- Did not locate the planner validator; the rejection rule is taken from `lane-addendum.md`.
- Did not touch `SHONEN.md`, `SCORECARD.md`, `LOG.md` or any fleet file.
