# mado round 100 — plan and pre-file amendments

Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, branch `master`, base
`43309e6af9a3b57f1bc839a826bef1f8eb7495e4` (round-99 closure tip, the non-author verifier
spot-check commit). L1 `MadoR100` (attempt 1). Round contract:
`.ufo/waves/round-100/claims-declaration-r100.md`. This file records the round plan and every
amendment made under the pre-file falsification rule (lane addendum §8 / Amendment 59) BEFORE the
report is filed. Nothing in the declaration above its `## Freeze block` is rewritten; the amendments
below narrow what the round files and each names the wave artifact that forced it.

## Round plan (as executed)

Two claims, two distinct axes, causally separable; no exploratory claim.

- **C1 — coverage (the surface it moves: the PATH-unset default branch of the launch load gate).**
  Round 99's A8 residual: `tools/mado-launchenv.py` models `g_find_program_for_path`'s unset-PATH
  default (`/bin:/usr/bin:.`, `gutils.c:370-382`) but no frozen case reaches it — both
  `path-unset` cases carry an absolute `Exec` and return at `gutils.c:331-357` before the PATH
  source is read. This round freezes a `path-default` case class measured against the installed
  `/usr/bin/gio`, plus a seeded fresh leg and a counted mutant population, and proves the model on
  the whole set. Counter `quality/counters/c1-r100-launchenv-path.py`; predicate
  `PRED-C1-r100-v1`; sourced by S533 (`gutils.c`, re-opened this round).
- **C2 — operability (the surface it moves: the cross-round harm watch's per-leg cap and its
  timing evidence).** Round 99's A9 routed defect: the frozen 28-leg panel's 600 s per-leg cap has
  no headroom and the gate records no per-leg timing, so two legs time out under this host's load
  and the panel reports `mismatches=2`. This round makes elapsed time a gate output, re-freezes the
  panel cap at twice the largest leg measured on this host at committed bytes, and re-runs the full
  panel at committed bytes. Counter `quality/counters/c2-r100-harm-watch.py`; predicate
  `PRED-C2-r100-v1`.
- **Frontier step (§2b).** `corpus/SOURCES.md` census before/after; S533 re-opened with a located
  quote (the sourced claim); mistakes mined into `corpus/lessons/round-100.md` `## Mistakes`;
  one `qual`/`recheck` change logged.
- **Assimilation (§10).** `merge/mado/` re-swept for this round's theme; verdict recorded.
- **considerthese (§10).** At most one unimplemented proposal from `considerthese/2026-11-07.md`
  (proposal 3: a library-semantics port carries a small-domain sweep) mined to a `QUALITY.md`
  criterion, grounded by opening the M95-1 evidence it points at.
- **Record repairs (not claims):** round-99 spot-check routed defects 1 (the off-by-one pointer in
  `corpus/lessons/round-99.md` M99-3 and `corpus/QUALITY.md` 172), 2 (attack-share arithmetic in
  SCORECARD/report), 4 (C1 A8 residual — this round's C1), 5 (unreceipted measured line practice).
- **Wave:** one v1 wave `w1`, 15 seats, band 8–16; ≥25 % attack roles. No planner seat in the wave —
  the L1 holds the canonical planner seat (`PROTOCOL` orchestrator ruling 2026-10-19); the bounded
  planning data-walk rides the two scouts and the connector. No residual call expected.

## Pre-file amendments (Amendment 59)

(empty until the wave returns; each amendment names its triggering artifact under
`.ufo/waves/round-100/`)
