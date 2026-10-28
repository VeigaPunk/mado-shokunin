# R55CritChronology — w1 report (chronology attack and freeze-order critique)

Full deliverable: `.ufo/waves/round-55/w1/R55CritChronology/chronology.md`. Receipts: `.ufo/waves/round-55/w1/R55CritChronology/receipts/chronology-receipts.txt` and `…/receipts/fooling-runs.txt`.

## Verdict
- **Chronology claim holds from committed objects, with one undisclosed rewrite.** The round-55 frozen content first committed as `59e3763f` (committer 2026-10-28 18:46:50-03, parent base `3b55b6e9`). jj rebased the same change to `54dacbd8` (committer 18:46:52-03, parent `a3795fdd`). The named freeze `54dacbd8` has no `.ready` in its tree, and its `frozen-tables.json` is byte-identical to the worktree (sha256 `bf46c889…9490`). The registry `createdAt` is 21:50:15.231Z, 3 min 23 s after the freeze's committer time.
- **The freeze-order checker can be fooled and also false-fails.** Committer time is unauthenticated. Backdating (S3) and a post-launch edit-then-revert (S7) pass as OK; rebasing a pre-launch freeze after launch (S2) and rewording it (S8) fail as `freeze_after_launch`. Absent `createdAt` fails closed (S5).

## What I ran (read-only)
- `git log -3 --format='%H %an %cI %s'` on HEAD → `dbc2eefe`, `54dacbd8`, `a3795fdd` (see receipts).
- `git cat-file -p 54dacbd8` → parent `a3795fdd`, author 2026-10-27 15:22:20-03, committer 2026-10-28 18:46:52-03, jj `change-id`.
- `git ls-tree -r --name-only 54dacbd8 | grep round-55.*\.ready` → 0 matches.
- `cmp` / `sha256sum` of `frozen-tables.json` (worktree vs `54dacbd8`) → identical, `bf46c889…9490`. `claims-frozen.md`, `registration.md`, `freeze-verify.py` also identical.
- `git status --porcelain --untracked-files=no -- .ufo/waves/round-55/` → empty. `git diff --name-status 54dacbd8 HEAD -- .ufo/waves/round-55/` → only five `A` entries.
- `git reflog` and `git cat-file -p 59e3763f` → same change-id, pre-rebase committer 18:46:50.
- Ran `R55ExecFreezeOrder/check-freeze-order.py` (read-only, `--work` scratch) at HEAD (OK, rc 0), at `54dacbd8` (no_registry, rc 1), and round-54 at `fe03bb3b` (freeze_after_launch, rc 1).
- Built 9 constructed repos in scratch (controls, rebase, forged committer, forged createdAt, absent createdAt, edit-then-revert, reworded freeze) and ran the checker on each.

## Defects and ambiguities
1. **`R55ExecFreezeOrder.md` margin is wrong.** It says "3h03m before launch". From the objects it is 3 min 23 s (21:46:52Z vs 21:50:15.231Z). The OK verdict stands; the number must be fixed before citation.
2. **Chronology carve-out not met as written.** "nothing under round-55/ other than w1/ and the generator changed" — no frozen file changed, but five non-w1 paths were added after the freeze and are not covered by the wording: `w1-spec.json`, `w1-dispatch.json`, `w1-run.err` (committed in `dbc2eefe`), and untracked `w1.ready`, `w1.ready.dispatched`.
3. **Named freeze is a jj rewrite.** The claims and registration cite `54dacbd8` with no mention of the rebase from `59e3763f` (2 s earlier, different parent).
4. **Launch is not witnessed in git.** `.ready` markers are untracked; the only in-repo launch time is registry `createdAt`, a self-written value.
5. **Checker S7 hole.** Post-launch edit followed by revert passes OK because the anchor is the earliest commit whose blobs match REV. The seat report calls this an "interpretation choice"; for a freeze-order gate it is a bypass.
6. **Checker REV ambiguity.** Run at the freeze itself it reports `no_registry`. The spec does not say which REV the L1 passes.
7. **Reflog is not independent evidence.** All HEAD reflog entries are `export from jj`.

## Critique of the M54-2/M54-4 fix (committer-time checker)
- **Rebased commits:** a legitimate rebase after launch produces a false FAIL (S2, S8); the lane's own 2 s rebase shows the mechanism.
- **Amended committer dates:** fooled by `GIT_COMMITTER_DATE` (S3). Unsigned commits, no external witness.
- **jj rewrites:** the checker measures the last rewrite, not the original freeze; it cannot tell pre-launch rewrite from post-launch forgery.
- **createdAt absent:** fail-closed (`no_registry`, rc 1). createdAt present but false is not detectable (S4).
- **Recommended fix:** make graph ancestry primary (registry-introducing commit must descend from the freeze anchor); record the freeze hash in the registry at launch and require equality with the anchor; flag any post-anchor commit touching freeze paths as `freeze_edited` even if the final blob matches; keep committer time only as a secondary check; document the REV rule. Limit to state: git cannot prove wall-clock launch time against an author with repo write access.

## Not verified / not run
- The jj operation log was **not read**: `jj` is at `/home/vgpnk/.local/bin/jj`, but even read-only jj commands may snapshot or import into the lane. The L1 should read it through an approved method to confirm the rewrite history.
- The freeze-order checker's selftest was not rerun by me; I used the sibling's committed-at-REV behaviour and my own fixtures.
- No hold-out path was opened or referenced.
- The first round-54 invocation used a non-existent path (`round-54/w1/R55ExecFreezeOrder/`); corrected and rerun. No other errors.
- No tools installed; no pacman, hyprctl, config or service access.
- No subagent dispatched (leaf member).
- Scratch `/fast/scratch/hyaku/mado-r55/R55CritChronology/` removed before yield.
