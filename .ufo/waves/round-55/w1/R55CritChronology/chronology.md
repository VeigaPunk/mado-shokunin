# R55CritChronology — chronology claim and freeze-order checker

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, HEAD `dbc2eefe`. Checks were read-only (git objects, `git reflog`, `sha256sum`, `cmp`) plus the seat-sibling checker run with `--work` in scratch. Raw output: `receipts/chronology-receipts.txt`, `receipts/fooling-runs.txt`.

## 1. Chronology claim: holds, with two qualifications

| Check | Result (committed objects unless noted) |
|---|---|
| Branch log -3 | `dbc2eefe` mado-shokunin 18:50:20-03 (generator); `54dacbd8` mado-shokunin 18:46:52-03 (freeze); `a3795fdd` João Pedro Veiga 2026-10-28 09:56:53-03 (considerthese) |
| Freeze `54dacbd8` | parent `a3795fdd`; author date 2026-10-27 15:22:20-03; committer 2026-10-28 18:46:52-03; carries `change-id` header (jj) |
| `.ready` at freeze | `git ls-tree -r` shows no round-55 `.ready` (count 0). Round-39/40/41/43 `.ready` files exist, round-55 none |
| `frozen-tables.json` | blob `54dacbd8:…/frozen-tables.json` sha256 `bf46c889…9490` = worktree sha256; `cmp` identical; `git diff --stat 54dacbd8 -- …/frozen-tables.json` empty. `claims-frozen.md`, `registration.md`, `freeze-verify.py` also byte-identical |
| Round-55 tracked changes vs HEAD | `git status --porcelain --untracked-files=no -- .ufo/waves/round-55/` empty (no tracked file edited since commit) |
| Round-55 changes freeze→HEAD | `A` only: `make-w1-spec.py`, `w1-spec.json`, `w1-dispatch.json`, `w1-run.err`, `w1/swarm-registry.json`. No `M`/`D` anywhere in the frozen set |
| Untracked, outside `w1/` | `w1.ready` (18:50:27 local) and `w1.ready.dispatched` (19:52:17 local). Not in any commit |
| Registry `createdAt` | `w1/swarm-registry.json` = `2026-10-28T21:50:15.231Z` = 18:50:15 -03 |

**Qualification 1 — the freeze named in the brief is a rewrite.** The reflog (`HEAD@{…}: export from jj`) and the object store show the same jj change (`change-id nmopvmwrmzuqwznrmwkptpryunwnspkw`) at two commits:

- `59e3763f` — parent `3b55b6e9` (the base), committer 2026-10-28 18:46:50-03, same round-55 frozen files (blobs identical to `54dacbd8`).
- `54dacbd8` — parent `a3795fdd` (inserted by the rebase), committer 18:46:52-03, round-55 content identical to `59e3763f` (`git diff --stat 59e3763f 54dacbd8 -- .ufo/waves/round-55/` empty).

So the frozen content was first committed 2 s earlier than the named freeze, and the rebase moved the parent onto an operator's unrelated considerthese commit. The chronology claim survives (both commits precede the registry's createdAt by ~3m25s), but the registration/claims text names only `54dacbd8` and does not disclose the rewrite. [INFERENCE: jj's rebase reset the committer timestamp; the author timestamp was kept from change creation on 2026-10-27 15:22:20, which equals the base commit's committer timestamp to the second.]

**Qualification 2 — the margin is 3 min 23 s and rests on committer timestamps alone.** `21:50:15.231Z − 21:46:52-03 = 0:03:23.231`. Nothing in git is an independent witness of launch: `.ready` files are untracked, and the registry's `createdAt` is a self-written value in a file committed 5 s later (`dbc2eefe`, 18:50:20).

## 2. Freeze-order checker (M54-2/M54-4 fix): critique

The checker (`R55ExecFreezeOrder/check-freeze-order.py`) decides OK iff the committer time of the first-parent "freeze anchor" is strictly earlier than the registry `createdAt` at REV. It fails closed on missing registry and rejects equality. It reads only git objects. Its selftest and the round-54 and round-55 runs are real and reproduce (round-54 `350d30e4`: committer 14:11:10-03 vs createdAt 17:05:25.338Z → FAIL `freeze_after_launch`; round-55 at HEAD → OK).

I ran it on constructed repos (scratch, `--work`, git commit-tree/`GIT_COMMITTER_DATE`; receipts `receipts/fooling-runs.txt`):

| Scenario | Truth | Checker verdict | Verdict is |
|---|---|---|---|
| S1 control: freeze 10:00Z, createdAt 11:00Z | pre-launch | OK | correct |
| S2 same trees re-committed at 12:00Z (rebase) | pre-launch | FAIL `freeze_after_launch` | **false positive** |
| S8 freeze tree unchanged, message reworded at 11:30Z | pre-launch | FAIL | **false positive** |
| S3 freeze made after launch, committer forged to 09:00Z | post-launch | OK | **fooled** |
| S4 createdAt rewritten to 13:00Z in a later commit, freeze 12:00Z | post-launch | OK | **fooled** |
| S7 contract file edited after launch, reverted in a later commit | edited | OK (`freeze_edited` not raised) | **fooled** |
| S5 `createdAt` absent / S5b no offset | — | FAIL `no_registry` | correct, fail-closed |

Answers to the questions asked:

1. **Rebased commits.** Yes, both ways. A rebase rewrites committer time to the rebase moment: a pre-launch freeze rebased after launch fails (S2, S8). This is exactly what happened in the lane, two seconds apart. Wall-clock time lost its meaning once jj rewrites are involved; a later rebase of the same content would produce a false FAIL and invite a fix.
2. **Amended committer dates.** Yes. `GIT_COMMITTER_DATE` is unsigned and trivially set; S3 passes a post-launch freeze. Any operator who sees a false FAIL has an easy incentive to backdate. The checker explicitly does not read the author date, which is correct (round-54 author 13:42:45 would have passed), but the committer date is equally unauthenticated.
3. **Freeze that rewrites history (jj "rewritten").** The anchor is chosen on the current first-parent chain, so a rewritten freeze is measured by the rewrite's timestamp, not the original's. Here that is harmless (2 s), but it is not principled: the checker cannot distinguish "rewritten pre-launch", "rewritten post-launch", and "forged".
4. **`createdAt` absent.** Fail-closed (`no_registry`, exit 1). But `createdAt` present and wrong is not detectable (S4): the registry is a self-written file with no check that it was committed after the freeze commit, and the registry is not in the FREEZE set. The checker reads `createdAt` at REV, so it trusts whatever REV says.
5. **Edit-then-revert (S7).** Not a rewrite trick — the first-parent scan finds the earliest commit whose blobs equal REV's, so a revert hides a post-launch edit completely. The seat report calls this "an interpretation choice". For a freeze-order gate it is a hole: a post-launch edit is exactly what the gate exists to catch.
6. **REV choice.** Run at the freeze commit itself the checker returns `launch=none … reason=no_registry`, rc=1 (I ran it at `54dacbd8`). The verdict depends on REV being at or after the registry commit; the spec does not say which REV the L1 must pass.

Recommended correction (partial-order instead of wall-clock; smallest safe change):

- Make ancestry the primary test: the commit that introduces the registry must have the freeze anchor as a first-parent ancestor. Graph order survives rebases and cannot be backdated with `GIT_COMMITTER_DATE`.
- Record the freeze commit hash in the registry at launch (e.g. `freezeRev`) and require it to equal the computed anchor. A hash cannot name an object that did not yet exist. Cost: a rebase after launch now fails loudly (detectable, visible as a registry-edit diff) — accepted, and better than silent backdating.
- Close S7: any first-parent commit touching a freeze path after the anchor is `freeze_edited`, whatever the final blob is.
- Keep committer time only as a secondary consistency check, and state its limit in the output.
- Document the REV rule (the registry commit or later) and make the no-registry-at-REV case a distinct SETUP reason rather than a freeze failure.
- State the honest limit: git cannot prove wall-clock launch time against an author with write access to the repo. The defensible claim is "the freeze content is an ancestor of the dispatch commit and the registry names its hash."

## 3. Defects and ambiguities found

1. **`R55ExecFreezeOrder.md` arithmetic error.** It says the round-55 freeze is "3h03m before launch". From the committed times: freeze 18:46:52-03 = 21:46:52Z, launch createdAt 21:50:15.231Z → 3 min 23 s. The verdict (OK) is unaffected; the stated margin is off by ~2h40m and should be corrected before it is cited.
2. **The "nothing changed since except w1/ and the generator" wording is not met as written.** No frozen tracked file was edited. But round-55 root gained five non-w1 paths after the freeze: `make-w1-spec.py` (the generator, allowed), `w1-spec.json`, `w1-dispatch.json`, `w1-run.err` (all committed in `dbc2eefe`), and untracked `w1.ready` and `w1.ready.dispatched`. The spec's carve-out names neither the spec/dispatch/err files nor the `.ready` markers.
3. **Named freeze is a rewrite of `59e3763f`.** The registration/claims cite `54dacbd8` as the freeze with no mention of the jj rebase or the 2 s earlier original. Recommend recording both hashes.
4. **Launch marker not in git.** `.ready`/`.ready.dispatched` are untracked, so the only in-repo launch time is `createdAt`, which is self-reported.
5. **Reflog is not an independent witness.** All HEAD reflog entries read `export from jj`; they are local and mutable.
6. **Checker REV ambiguity** (see §2 item 6).
7. **Checker's S7 blind spot** (see §2 item 5), described as "interpretation choice" in `R55ExecFreezeOrder.md`.

## 4. Not verified / not run

- The jj operation log (`/home/vgpnk/Projects/shokunin/mado-shokunin/.jj`, binary `/home/vgpnk/.local/bin/jj`) was not read: even read-only jj commands can snapshot or import into the lane, so I stayed with git objects and the reflog. The jj op log is the authoritative record of the rewrite and should be read by the L1 with an approved read-only method.
- No hold-out path was opened or used.
- Round-54 freeze-order was run via `R55ExecFreezeOrder`'s script at its real path; my first attempt used a non-existent round-54 path and failed (rc=2) before I corrected it.
- No tools were installed; no hyprctl, pacman, or config access was needed.
- Fooling fixtures ran in `/fast/scratch/hyaku/mado-r55/R55CritChronology/`, which is removed before yield; the copy of the checker used there is also removed.
