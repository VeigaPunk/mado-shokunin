# ScoutAxisScores — axis-selection table re-derivation at base `8f51071b`

Item: read-only reconnaissance. Re-ran every bounded sub-axis command named
by `.ufo/waves/round-30/registration.md` §Axis selection at base
`8f51071b5bc44c815eeb5da76bb7f1947994ffb8` on 2026-10-24. All measurements
read committed bytes (`git show`/`git ls-tree`/`git archive`); nothing in the
lane repo, fleet repo, git index, or jj state was written (this report file
excepted).

## Verdict: C2 lowest-axis claim REPRODUCES

Calibration is the lowest-scoring axis at base under every registered
rubric. No bounded sub-axis scores lower.

## Re-derived table

| # | Sub-axis | Command (as registered) | Registered base value | Re-derived at base | Match |
|---|---|---|---|---|---|
| 1 | coverage / admitted-note reachability | SCORECARD.md frozen literal fence (S185): `indexed/notes` over `corpus/knowledge/*.md` vs `corpus/README.md` rows | 41/43 = 9.5349/10, exit 1 | `revision=8f51071b5bc44c815eeb5da76bb7f1947994ffb8 indexed=41/43 missing=2 dangling=0 duplicates=0 coverage=9.5349/10`, exit 1; missing `mutation-testing-r28.md`, `workspace-rules-r27.md` | ✓ byte-identical to `evidence/c1-before-8f51071b.txt` |
| 2 | coverage / sourced current-art ground | `covers: U1..U7` entries in `corpus/README.md` whose `source:` cites a `mined` row in `corpus/SOURCES.md` | 7/7 = 10.0000 | 7/7 = 10.0000 (see S030 note below) | ✓ |
| 3 | calibration / literal lesson-citation | `grep -cE '^[0-9]+\. .*lessons/'` over `^[0-9]+\. '` QUALITY.md | 28/40 = 0.7000 | `literal=28/40` = 0.7000 | ✓ |
| 4 | calibration / resolved-active grounding | `python3 -I .ufo/waves/round-30/c2/count.py 8f51071b…` | 31/39 = 0.7949, TARGET_MISSED | `active=39 resolved_active=31 fraction=0.7949`; UNRESOLVED {1,2,3,4,5,38,39,40}; `verdict=TARGET_MISSED`, exit 1 | ✓ byte-identical to `evidence/c2-before-8f51071b.txt` |
| 5 | operability / hermetic suite | `bash tools/mado-verify.sh --selftest` | 460/460 = 10.0000 (harm watch) | `MADO_SELFTEST: 460/460 assertions passed`, exit 0 — run against the base-revision gate extracted via `git archive 8f51071b tools` to `/tmp/axscores` (hermetic; no lane bytes touched) | ✓ |

Lowest registered rubric values at base: calibration literal **0.7000**,
resolved-active **0.7949** — both strictly below coverage **0.9535**,
sourced-art **1.0000**, operability **1.0000**. The registered ordering and
the C2 "lowest axis" designation stand.

## Observed facts / details

- Row 1 fence is the SCORECARD.md `REV="${REV:-…}"` python block (the S185
  URL-equivalent). With `REV=8f51071b…` it prints exactly the receipt the
  registration cites, including both missing rows by name.
- Row 2 nuance (does not change the score): the U2 index row's literal text
  reads "S021–S029 and S017 (S030 rejected duplicate; …)". A naive S-id
  extraction includes **S030**, whose SOURCES.md row exists at base — status
  column value not `mined` (it is the rejected duplicate of S017 documented
  in `corpus/lessons/round-13.md`). Counting only *cited* sources as the
  rubric states — i.e. excluding the parenthetically-rejected S030 — every
  cited S-id per U-entry resolves to a `mined` row: U1 {S002,S016–S020},
  U2 {S017,S021–S029}, U3 {S031–S035,S037}, U4 {S005,S040–S043,S046},
  U5 {S041,S047,S048,S050}, U6 {S051,S052}, U7 {S053,S054} → 7/7.
  If a grader instead counts S030 as a cited source, the sub-axis scores
  6/7 = 8.5714 — **still above both calibration rubrics**, so the
  lowest-axis conclusion is robust to that reading.
- Row 3 non-`lessons/` criterion lines at base are 12: criteria 1–5, 18, 19,
  20, 32, 38, 39, 40. Counter 4 independently resolves criterion 18, 19, 20
  and 32 (their `lessons/` or `lesson round<NN>` citations appear on
  continuation lines, not the numbered line), which is why literal 28 and
  resolved-active 31 diverge; criterion 20 is counted out of both fractions
  as superseded by 21 (`superseded=[20]`).
- Row 5: the worktree's `tools/mado-verify.sh` at tip may differ; the
  measurement deliberately ran the base-extracted copy to keep the base
  measurement honest (460/460 exit 0, ~16s).
- The registration names no other bounded sub-axis commands; depth and
  adjacency are declared unscored in the table itself.

## Attack surface / gaps (for the frozen registration, never editing it)

- The row-2 rubric is stated loosely enough that the S030
  rejected-duplicate parenthetical needs a judgment call (documented above);
  the outcome is the same either way for the lowest-axis claim.
- "literal fraction ≥ 0.70" in PRED-C2 sits exactly **at** the base value
  0.7000 — a predicate with zero headroom above base; observed, not an error
  (the kill rule triggers only below 0.70).
- Not independently re-run: the evidence files' own provenance (taken as
  receipts); every receipt checked matched a fresh re-derivation anyway.

## Remaining unknowns

None within scope. All five bounded sub-axis commands re-derived at base
with identical numbers; the lowest-axis selection is confirmed.

## Tooling

No installs performed or needed (python3, git, bash all pre-existing).
Pacman untouched per the host-wide pause.

## Addendum — forwarded observation (confirmed, out of my item's scope)

Peer `RevC1Fence` flagged a worktree modification outside the registered
write scope; independently confirmed here (read-only): `git status` shows
`M quality/q36-successor-receipts.txt` (mtime 2026-10-24 04:06:46). The
diff rewrites only ephemeral run-dir paths (`/tmp/mado-r28-q36-ge5zx30t` →
`/tmp/mado-r28-q36-g3nfq53x`, plus same-classed scratch paths) across 8
changed lines (4+/4−); every rc/expected/PASS verdict line is unchanged.
No item names `quality/q36-successor-receipts.txt` as a write target, so
this is a scope violation — though no verdict moved. Not restored by this
seat (worktree mutation forbidden); flagged for the integrator.
