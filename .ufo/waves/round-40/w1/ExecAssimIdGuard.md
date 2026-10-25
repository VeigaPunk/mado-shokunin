# ExecAssimIdGuard — id-collision guard (assimilation, §10)

Status: complete. Guard run exactly as §10 states; proof fixture built and run; K2 renumber map
candidate derived by document. Full commands/outputs: `w1/ExecAssimIdGuard/guard.md`.

## Result

- `$A/reg-ids` = 214 ids (lane `corpus/SOURCES.md`, sha256 `f99b6bf0…3e96`); `$A/staged-ids` = 147
  ids (`merge/mado/SOURCES.append.md`, sha256 `684efe8c…27c0`); `comm -12` → `$A/collisions` =
  22 ids: S203–S221, S253, S258, S277. Nonempty → any adoption of those staged ids renumbers in
  scratch; the lane itself is untouched.
- **K2 (`host-producer-outputs-r29`, ids S237–S241) does not collide**: each id has 0 occurrences
  in `reg-ids` and 1 in `staged-ids`. URL-level duplicate check (census E04) is also clean — 0
  occurrences of all five URLs/paths in the lane registry.
- Renumber map candidate for K2, by document (entry `source:` order), not arithmetic: identity is
  the correct disposition (no collision); if a renumber were forced, next free lane id = S278
  (registry max S277) → S237→S278, S238→S279, S239→S280, S240→S281, S241→S282, with URLs
  carrying the evidence.
- Proof (scratch, `/tmp/idguard.xSuOKi`): census-valid registry fixture carrying `  | S002 |`
  (`validate --file` exit 0, `file ok`) + staged copy holding S002 → guard `comm -12` prints S002
  (count 1); the column-zero-only pattern `^\|…` extracts 0 ids and `comm -12` is empty. Guard is
  not broken; the indented-collision family is caught.

## Files written

- `.ufo/waves/round-40/assimilation/reg-ids`, `staged-ids`, `collisions` (only §10-allowed writes
  in `$A`; no other assimilation file touched).
- `.ufo/waves/round-40/w1/ExecAssimIdGuard/guard.md` (evidence), this report.
- Scratch: `/tmp/idguard.xSuOKi` (fixtures only; no repo, no git), removed after hashing.

## Checks for main

- Re-run the §10 block verbatim: expect `214 / 147 / 22` (same three output hashes as guard.md §1).
- The guard output files are data for the integrator: `collisions` nonempty means the *colliding*
  staged ids (S203–S221, S253, S258, S277) must be renumbered in scratch; K2's ids are free.
- Round-end census (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`)
  is untouched by this seat — nothing outside `$A/{reg-ids,staged-ids,collisions}` was written.

