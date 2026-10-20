# JjDisposition — fix-or-why-not for JjAuditMado and JjTrialMado

Scope: every finding F1–F17, audit §9 recs 1–6, and trial hazards H1–H7 and recs 1–5.
Observed 2026-10-20 ~15:40–15:50Z, read-only. Lane HEAD `d3a0000` (detached); `master` = `origin/master` = `d3a0000` (local remote-tracking ref, not re-fetched). `tools/mado-verify.sh` sha256 `fba82a66…`, mtime 03:03 -0300 (same identity the audit recorded).

Status key: **HOLDS** = already true, evidence cited · **FIXED-LANDED** = change is in the tree and verified by bytes · **PENDING** = owned by a named sibling, not in the tree at read time, re-check at integration · **OPEN** = not fixed this round, why-not stated · **NOT-RE-RUN** = needs jj or live host probes, forbidden here · **CONFLICT** = sources disagree, orchestrator decision.

## JjAuditMado findings

| ID | Finding (short) | Disposition | Evidence (read-only) |
|---|---|---|---|
| F1 | `mado-action-plan.py` has no git content; only `_self_invoke` | HOLDS | `grep -c git tools/mado-action-plan.py` → 0 |
| F2 | Three executed git calls in `mado-verify.sh` (:3382, :3391, :3406), precondition :3347 and fixture stub | HOLDS (inventory) | All four sites present at the audited lines in sha `fba82a66…` |
| F3 | omarchy checkout is plain git, not colocated | HOLDS | `~/.local/share/omarchy/.git` is a directory; no `.jj`. `.git/HEAD` = `ref: refs/heads/master`; `packed-refs` holds `8fcc9d60… refs/heads/master` and `8fcc9d60… refs/tags/v3.8.4`. Read as bytes; no git run in that checkout. |
| F4 | Live gate's three git rows PASS | NOT-RE-RUN | Live layer invokes `omarchy version` and `hyprctl`; forbidden under the host pause. Tag and HEAD inputs reproduce by bytes (F3). Walker red not re-observed. |
| F5 | Colocated sandbox behaviour (`fixA`) | NOT-RE-RUN | Evidence-only; jj is forbidden in the lane and the sandbox was not rebuilt. Consequences are covered by F6. |
| F6 | HEAD-as-tip rows (:3382, :3391) misreport after `jj new` | OPEN (armed, not firing) | Target omarchy checkout is plain git (F3), so the rows read commit bytes correctly today. The fix changes gate bytes, so PIN_MADO must be re-cut after GateRcFix lands. Recommended: `git -C "$tree" rev-parse --verify refs/heads/master`. Lane's own HEAD is detached, but no verify row reads it (grep). |
| F7 | No class-A markers (`symbolic-ref`, `@{u}`, `--abbrev-ref`, `branch --show-current`) in tooling | HOLDS | Grep of `tools/mado-verify.sh` for these plus `--porcelain` and `git status`: only the comment at :3262. |
| F8 | Class-C index recipes unsafe across jj mutations | OPEN (SKILL.md only) | No class-C call in `tools/`. SKILL.md still carries `git diff --numstat` (3 sites) and `git status --porcelain` (1666). Owner L1. Why not: doc rewrite is outside claims C1–C3. Recommended: commit-to-commit ranges, `git diff --numstat <base> <tip>`. |
| F9 | `[ -d "$tree/.git" ]` misses git worktrees | OPEN (latent) | Both targets are directories today: lane `.git` and omarchy `.git`. :3347 unchanged. Why not: no live target is a worktree, and the fix changes gate bytes. Recommended: `git -C "$tree" rev-parse --git-dir`. |
| F10 | `vs_head` turns an unreadable HEAD blob into a false "local edit" | PENDING — GateRcFix | Not landed at read time: :3406 is still `tmo git … show … \| sha256sum` with no rc capture, and the sha is unchanged. Re-check at integration: rc capture present at :3406, and an OM scenario with a failing git stub. |
| F11 | No hooks in use | HOLDS | Lane `.git/hooks`: no non-sample entries. `core.hooksPath` rc=1. omarchy hooks: no non-sample entries. |
| F12 | No attributes or eol; LFS filters inert | HOLDS, with correction | `.gitattributes` and `info/attributes` absent in both trees. CORRECTION: `filter.lfs.*` comes from the global `~/.config/git/config` (`git config --show-origin`), not from the omarchy repo's `.git/config`. Effect is the same; the audit wording was imprecise. |
| F13 | jj bypasses hooks and eol | HOLDS (latent) | No hooks and no attributes (F11, F12), so nothing is bypassed today. The eol demonstration was not re-run. |
| F14 | Selftest git stub cannot fail | PENDING — GateRcFix | :667–670 still `describe)/rev-parse)/show)` each `exit 0`. No `STUB_GIT_RC` present. |
| F15 | Selftest hardcodes `/tmp` paths; PIN_MADO drift | OPEN | :395 and :1860 still hardcode `/tmp` mktemp templates, which ignore `TMPDIR`. PIN_MADO still `cd1d73d7…` at :1639. Why not: the PIN re-cut must follow the GateRcFix byte changes, and the `/tmp` paths are outside GateRcFix's announced scope (F10, F14). |
| F16 | No landedness check; lane 8 ahead at 14:16Z | HOLDS for helper; OPEN for gate | Now `ahead=0 behind=0`, `is-ancestor(origin/master, master)` rc=0 (remote-tracking, not re-fetched). Fleet helper `print_state` (`scripts/hyaku/jj-lane.sh:69–81`) reports ahead/behind. No verify row checks landedness (grep for `is-ancestor`, `merge-base` → none). Caveat: `print_state` runs `git status --porcelain`, which the verify gate's own rule (:3262) forbids on checkouts. |
| F17 | jj has been run in the live lane | CONFLICT (not holding) | Lane reflog (-0300): `reset: moving to HEAD` 12:18:08; `export from jj` 12:28:10 (`d9a5a18`, author protocol-shokunin); `export from jj` 12:34:53 (`d3a0000`, author mado-shokunin). `.jj/` recreated 12:18; `.jj/working_copy/checkout` 12:34. So jj wrote refs in the lane after the audit's last op-log entry. Operator commit `67a3123` ("jj as git manager from now on on shokunin runs") conflicts with audit rec 6 and this round's no-jj rule. Which command ran each jj write is not determined [INFERENCE]. |

## JjAuditMado §0 incident (fleet root; not a numbered finding)

| Item | Disposition | Evidence |
|---|---|---|
| Fleet-root residue: `.jj`, `version`, `hookprobe3.txt`, `hookprobe4.txt`, `hooktest`, `attrtest` | HOLDS for listed residue | Existence check only: all absent in `/home/vgpnk/Projects/shokunin`. Fleet reflog, fsck, and the untracked-`version` question are NOT verified; fleet root is out of this lane's scope. Orchestrator-owned. |

## JjAuditMado §9 recommendations

| Rec | Recommendation | Disposition | Evidence |
|---|---|---|---|
| R1 | Fix :3406 rc handling; add failing-git OM scenario | PENDING — GateRcFix | See F10. |
| R2 | Resolve tip instead of HEAD at :3382/:3391 | OPEN | See F6. |
| R3 | `rev-parse --git-dir` in place of `[ -d .git ]` at :3347 | OPEN (latent) | See F9. |
| R4 | Landedness row in gate | OPEN (helper covers the `state` view) | Why not: adding a gate row changes gate bytes and needs a PIN re-cut. Helper `print_state` covers ahead/behind (F16). |
| R5 | `init` must handle a pre-existing `.jj` | HOLDS in helper code; NOT HOLDING live | Helper (`scripts/hyaku/jj-lane.sh:142–158`, commit `67a3123`, 11:08 -0300) re-applies `snapshot.auto-track`, `user.name/email`, and `trunk()` with `--repo`, and warns on pre-added paths. Live lane: `.jj/repo/config.toml` is absent [INFERENCE: this is jj's repo-config path], and `.jj` was recreated 12:18. Re-running `init` is a jj mutation in the live lane, so it is an operator decision. |
| R6 | Keep jj out of live lanes entirely | CONFLICT | See F17. Operator directive `67a3123` says the opposite for shokunin commits. Orchestrator decision. |

## JjTrialMado hazards

| ID | Hazard | Disposition | Evidence |
|---|---|---|---|
| H1 | Unignored `.ufo/` growth | PARTIAL | `.ufo/state/` closed by L1 (H4). Untracked-unignored paths now 259 (`git ls-files -o --exclude-standard`), mostly round-18 fetch receipts and w1 reports, committed by pathspec. Live `snapshot.auto-track="none()"` is UNVERIFIED (no repo config file, R5). |
| H2 | `git add` staging destroyed by jj mutations | OPEN | No `git add` guidance in SKILL.md (grep → none). See T3. |
| H3 | Detached HEAD after every mutation | HOLDS (observed) | `.git/HEAD` = `d3a0000…` detached; `symbolic-ref -q HEAD` rc=1. No tool uses `symbolic-ref` or `@{u}` (F7). |
| H4 | `.ufo/state/` not ignored | FIXED-LANDED (L1) | `.gitignore` line 2 `.ufo/state/`, mtime 12:40:04 -0300. `git check-ignore -v .ufo/state/deep/x.json` → `.gitignore:2`, rc=0. |
| H5 | Unignored >1 MiB scratch refused by jj | HOLDS | `stat` over the 259 untracked-unignored paths: none above 1 MiB. |
| H6 | No symlinks, nested `.git`, or generated dirs | CORRECTION | One tracked symlink: `.ufo/waves/round-17/tripwire/hardening/symlink-target.jsonl` → `/etc/hostname` (index mode 120000). No nested `.git` found. The symlink is tracked; its location suggests a tripwire fixture [INFERENCE]. No action. |
| H7 | `@` author identity | OPEN (live-unverified) | User config `~/.config/jj/config.toml` sets `[user]` to the operator. No repo config in the live lane. A jj commit made outside the helper would be authored as the operator. Helper sets identity per command; `d3a0000` is authored mado-shokunin. |

## JjTrialMado recommendations

| Rec | Recommendation | Disposition | Evidence |
|---|---|---|---|
| T1 | Adopt `jj-lane.sh` for mado lane writes | CONFLICT | Operator directive `67a3123` already makes jj the git manager for shokunin runs. `d3a0000` (mado-shokunin author, "export from jj") is consistent with the helper path [INFERENCE]. Conflicts with audit R6 and this round's no-jj rule. |
| T2 | Add `.ufo/state/` to `.gitignore` | FIXED-LANDED (L1) | See H4. |
| T3 | Fleet doc note: lane seats must not `git add` | OPEN | SKILL.md has no `git add` guidance. Owner L1 (SKILL.md is L1-owned). Recommended text: "seats never `git add`; use `jj file track` or the helper's pathspec commit." |
| T4 | No per-lane jj config beyond `init` | CONTRADICTED for live lane | Trial verified its sandbox copy only. Live `.jj/repo/config.toml` is absent (R5), so the `--repo` keys are not confirmed live. |
| T5 | No tooling installs; jj 0.45.1 already present | HOLDS | This seat installed nothing. No pacman, sudo, or package command run. No jj command run. |
