# JjDisposition — report (round-18 w1, leaf seat)

Draft table: `.ufo/waves/round-18/drafts/JjDisposition.md`. This report carries the summary, conflicts, disclosures, and checks for the integrator. Nothing here was verified by running a gate.

## Summary

- Of 17 audit findings, 6 recommendations, 7 trial hazards, and 5 trial recommendations:
  - **Fixed and landed, verified by bytes:** H4/T2, `.ufo/state/` ignored by L1 (`.gitignore:2`, 12:40:04 -0300; `check-ignore` rc=0).
  - **Pending GateRcFix, not in the tree at read time:** F10/R1 (:3406 rc capture) and F14 (stub rc knob). `tools/mado-verify.sh` is still sha `fba82a66…`, mtime 03:03 -0300, with no rc capture and no `STUB_GIT_RC`.
  - **Already holds:** F1, F2 (as inventory), F3, F7, F11, F13 (latent), F16 for the helper, R5 in helper code, H3, H5, T5.
  - **Holds with correction:** F12 (the LFS filter is global in `~/.config/git/config`, not repo-local), H6 (one tracked symlink exists, to `/etc/hostname`).
  - **Open, with stated why-not:** F6/R2, F8, F9/R3, F15, R4, H2/T3, H7.
  - **Not re-run:** F4 and F5. They need the live gate or jj, which are forbidden.
  - **Conflicts for the orchestrator:** F17, R6, T1, and the live-lane jj config state (R5, T4).

## Conflicts (not resolved here)

1. **jj in live lanes.** Audit rec 6 and this round's rule say no jj in the lane. Operator commit `67a3123` (fleet `scripts/hyaku/jj-lane.sh`, 11:11 -0300) says "jj as git manager from now on on shokunin runs". The lane reflog shows jj writes after the audit's last op-log entry: `export from jj` at 12:28:10 (`d9a5a18`, author protocol-shokunin) and 12:34:53 (`d3a0000`, author mado-shokunin). `.jj/` was recreated 12:18:08. Which command produced each write is not determined.
2. **Live `.jj` has no repo config file.** `.jj/repo/config.toml` is absent, so the helper's `--repo` keys (`snapshot.auto-track="none()"`, identity, `trunk()`) are not confirmed in the live lane. The trial's "confirmed correct" applied to a sandbox copy. [INFERENCE: jj's repo-config path is `.jj/repo/config.toml`; I could not read the config-id or op store, and did not run jj.] Repairing this means re-running `jj-lane.sh init` in the live lane, which is a jj mutation, so it needs an operator decision.
3. **Helper `state` runs `git status --porcelain`** (fleet `jj-lane.sh:79`). The verify gate's own rule (:3262) forbids `git status` on checkouts because it refreshes the index. The helper is fleet-owned; flagged only.
4. **SKILL.md still prescribes `git status --porcelain`** (around line 1666, "worktree clean"), contrary to the same rule. L1 owns SKILL.md.

## Commands run (all read-only)

- Lane git: `cat .git/HEAD`; `rev-parse HEAD master origin/master`; `reflog -8 --date=iso`; `rev-list --left-right --count`; `merge-base --is-ancestor`; `check-ignore -v`; `config --get` / `--get-regexp` / `--show-origin`; `ls-files -s` / `-o --exclude-standard`; `worktree list`; `log -3`; `find`; `stat`.
- Lane files: `stat`; `ls`; `cat -A .gitignore`; `cat .git/config`; `find .jj -maxdepth 3` (names and mtimes only; config-id and op store not read); grep of `tools/mado-verify.sh` and `tools/mado-action-plan.py`; `sed -n` on verify lines 3398–3412.
- omarchy checkout (bytes only, no git run): `ls -ld .git .jj`; `cat .git/HEAD`; `grep -a` on `packed-refs`; `cat .git/config`; `ls` of `hooks`, `.gitattributes`, `info/attributes`.
- Fleet root (existence only): `.jj`, `version`, `hookprobe3.txt`, `hookprobe4.txt`, `hooktest`, `attrtest`; `scripts/hyaku/jj-lane.sh` by grep and `sed` on read-only ranges; `git -C` fleet root `log -1 -- scripts/hyaku/jj-lane.sh`.
- User config bytes: `~/.config/jj/config.toml` (user identity and ui; not credentials). `~/.config/git/config` was read only through `git config --show-origin`.

**Disclosure:** the first command in this seat was `git status --porcelain | head -20` in the lane. The lane's own rule (:3262, SKILL.md ~1635) forbids `git status` on the checkout because it can refresh the index stat cache. I did not run it again. I did not write to any repo, the index, or any ref.

**Not run and why:** no jj command of any kind (the lane forbids it); no `mado-verify.sh` run, live or file-only (the live layer calls `omarchy` and `hyprctl`, forbidden under the host pause; I did not run the file-only mode either, as the disposition rests on bytes); no sandbox rebuild.

## Installs and updates

None. This seat installed or updated nothing. No pacman, sudo, yay, or paru command was run. The operator tooling directive was read; no tool was needed for this task.

## Checks for the integrator (run once after GateRcFix, L1, and the PIN re-cut land)

1. `grep -n 'grc\|PIPESTATUS' tools/mado-verify.sh` shows rc capture at the `vs_head` site (~:3406), and `grep -n STUB_GIT_RC tools/mado-verify.sh` is non-empty. Re-run `bash tools/mado-verify.sh --selftest` once, in the lane. Note that the selftest hardcodes `/tmp` paths (F15) and may not run cleanly in a sandboxed `TMPDIR`.
2. `git check-ignore -v .ufo/state/x` → `.gitignore:2` (already true).
3. Confirm PIN_MADO matches the re-cut sha after the byte change (F15). Do not re-cut by hand.
4. Decide CONFLICT items 1 and 2 with the orchestrator before any jj command is allowed in the lane.
5. Re-check `git rev-list --left-right --count master...origin/master` after the next push; the 0/0 result is from the local remote-tracking ref and was not re-fetched.

## Limits

- `.ufo/state/` gitignore and the helper's pre-existing-`.jj` handling are the only fixes that landed. Everything else is either pending GateRcFix or open.
- Attribution of jj writes at 12:28 and 12:34 is inference from reflog messages and commit authors.
- The F12 correction (global LFS filter) is measured. The audit's "inert" wording is unchanged in effect.
