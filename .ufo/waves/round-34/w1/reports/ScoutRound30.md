# ScoutRound30 — byte provenance of the five round-30 reports rewritten at d40b35f

Scout leaf, report only. Lane tip at report time: `fa7ba11346116672352b5d41494141c5c4d738d0`
(`git rev-parse HEAD`). Full table with quoted reality lines:
`.ufo/waves/round-34/scratch/ScoutRound30/table.md`.

## Method

- `git log --follow -- .ufo/waves/round-30/w1/reports/<name>.md` per file → last touching
  commit is `d40b35f` for all five; nothing between it and HEAD touched them.
- `git merge-base --is-ancestor d40b35f 69f72100…` → true: `d40b35f` (`round-33: correct the
  false r32 C1 row…`) is the round-33 repairs commit; `69f72100` sits one commit after it.
- Byte counts via `git show <rev>:<path> | wc -c` at `9a46ccf` (= `d40b35f^`, pre-rewrite),
  `69f72100`, HEAD; worktree sizes cross-checked with `wc -c` — all equal.
- Provenance classified by the `d40b35f` diff status (`M` vs `A`) plus in-text self-statements;
  shared-line counts from `comm -12` on sorted unique nonblank lines of old/new blobs.

## Findings

| File | @9a46ccf (pre) | @69f7210 | @fa7ba11 tip | Current bytes are… |
|---|---|---|---|---|
| RevRecordsChain.md | 21687 | 19058 | 19058 | rewrite of the r30 committed file (274f735); self-declared final pass, 1 shared line |
| RevTrendExpansion.md | 12100 | 12991 | 12991 | rewrite of the r30 committed file (274f735); self-declared supersede, 5 shared lines |
| RevTrendDiscernment.md | 0 (absent) | 18207 | 18207 | other source — `A` at d40b35f; finished r30 seat report never committed during r30 |
| SentScope.md | 15568 | 23730 | 23730 | rewrite of the r30 committed file (15ddd7d); 21 shared lines (F-skeleton kept) |
| SimplifierC2.md | 0 (absent) | 11431 | 11431 | other source — `A` at d40b35f; finished r30 seat report never committed during r30 |

Key corrections to the task premise, evidenced:

1. Two of the five (`RevTrendDiscernment.md`, `SimplifierC2.md`) were **added**, not modified,
   at d40b35f (`git diff-tree` shows `A` entries). Neither exists at any round-30 commit
   (checked `a0dd664`, `274f735`, `15ddd7d`, `d40b35f^`). Their content is complete round-30
   seat work — both seats are registered in `swarm-registry.json` @274f735, and both texts
   reference only round-30 artifacts (`274f735`, `15ddd7d`, `d72243e`) — so the likely source
   is each seat's uncommitted working-tree file, not a rewrite of committed bytes.
   `SimplifierC2` says so in effect: "worktree `M` entries below belong to the L1's in-flight
   addendum."
2. The other three are genuine rewrites of round-30 committed files, not edits:
   `RevRecordsChain` shares 1 unique nonblank line with its predecessor, `RevTrendExpansion`
   5, `SentScope` 21. All three self-declare the supersession in their own text.
3. The rewrite commit `d40b35f` is the round-33 repairs commit **after** `9a46ccf`
   (`9a46ccf` = `d40b35f^`); the task's "rewritten at the round-33 repairs commit" checks out
   for all five paths.

## Verdict

All five current files are real seat reports (findings tables, re-run counters with exit
codes, sha256-anchored blobs, per-revision outputs) — none is filler. Three are rewrites of
committed round-30 bytes; two are first-time commits of round-30 seat output that was never
committed during round 30.

## Evidence pointers

- Table: `.ufo/waves/round-34/scratch/ScoutRound30/table.md`
- Commits: `d40b35f90ad8bf630ad9404d25aeee1d9737f300`, `9a46ccf` (its parent),
  `69f72100bee31a60b811f8fbbe7796db883e17b3`, tip `fa7ba11346116672352b5d41494141c5c4d738d0`,
  round-30 anchors `a0dd664`, `274f735`, `15ddd7d`.
- Commands re-run for this report: `git show <rev>:<path> | wc -c`, `git diff-tree -r d40b35f`,
  `git log --follow`, `git merge-base --is-ancestor`, `comm -12` on sorted unique lines.
