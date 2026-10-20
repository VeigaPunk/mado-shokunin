# ScoutGitDryEmpirical — help and dry-run git forms change no VCS content; `git commit -n` and `-m --help` do commit; `git pull -n` is a real pull

Empirical probe on the host git (2.56.0) in /tmp scratch repositories with a bare /tmp remote.
Every row below is observed on this host unless marked [INFERENCE]/[UNK]. No lane file was
modified; this report is the only lane write.

## Environment and method

- Lane HEAD (read-only): `e629f731172b8238caffe50f152217ce56535fb4` (detached); `tools/mado-tripwire.py`
  sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`.
  Scratch clone `/tmp/mado-r20-ScoutGitDryEmpirical/lane-clone` observed HEAD `e629f731…`, 0 status lines.
- `/usr/bin/git` = `git version 2.56.0`; `/usr/bin/man` present; bash 5.3.20. Host global config was
  observed (`alias.ci=commit`, `pull.rebase=true`, `commit.verbose=true`, …); scratch repos set local
  `user.*`, `commit.gpgsign=false`, `core.hooksPath=.git/hooks`, `core.excludesfile=/dev/null`,
  `push.default=simple`. `--help` forms ran with `MANPAGER=cat GIT_PAGER=cat`; every form ran via
  `timeout 120 bash -c '<form>'`.
- Fixtures: bare remote `…/remote.git` + clone `…/repo` (plus a second clone to move the remote ahead).
  A `pre-commit` hook appends to `…/hook.log` and exits 0, so hook execution is observable and cannot
  block a commit.
- Per-form before/after capture: `git rev-parse HEAD`; `.git/index` sha256; `git ls-files -s` hash;
  `git status --porcelain=v1`; worktree file-content hash; `refs/heads,tags,remotes`;
  `.git/FETCH_HEAD`; bare-remote `for-each-ref` + `count-objects`; hook-log line count.
- Primary harness `/tmp/mado-r20-scoutgd-run.sh` (sha256 `faf7ded2028480f2cd1cf7706b4ce67bd8dd1594450d8687cb5b3aab5c2bdeaf`);
  15 forms → 90 files in `/tmp/mado-r20-ScoutGitDryEmpirical/results/` (`<id>.before`, `.after`,
  `.stdout`, `.stderr`, plus empty `.err` capture files). Consolidated saved outputs:
  `/tmp/mado-r20-ScoutGitDryEmpirical/supp4-all.txt` (sha256 `39a0ed31…`),
  `supp4-e2.txt` (`68e01e26…`), `supp4-h.txt` (`1aa647a1…`); supp scripts shas
  `d2d2ae30…` (supp), `4bbd1edb…` (supp2). Pinned tool copies and scan receipts are listed below.
- Fixture transcripts were only parsed by the tripwire; no fixture code was executed.

## Table: form → wrote? → exit code

"Wrote?" means a VCS content-state change (HEAD/branch or remote ref/index **entries**/worktree/FETCH_HEAD).
Index **bytes** can change without content change (cache-tree; see F4).

| # | form | fixture | exit | wrote? | observed delta |
|---|---|---|---|---|---|
| 1 | `git commit --dry-run -m x` | staged mod. | 0 | no | HEAD `2663885…`→same; staged hash `3e13c866…` both; status `?? c.txt;M  a.txt;` both; `.git/index` bytes `8f9693ec…`→`3626af34…` (TREE cache-tree only) |
| 2 | `git commit -n -m x` | staged mod. | 0 | YES | HEAD `2663885…`→`ccc66484…`; branch ref moved; hook lines 0→0 (`--no-verify`); stdout `[main ccc6648] x` |
| 3 | `git add -n .` | unstaged mod.+new | 0 | no | index sha `6e0effc6…` identical; HEAD same; stdout `add 'a.txt'` / `add 'c.txt'` |
| 4 | `git add --dry-run .` | unstaged mod.+new | 0 | no | index sha `1f5ab4c6…` identical; HEAD same |
| 5 | `git push -n origin HEAD` | 1 unpushed commit | 0 | no | local HEAD `0bfb801…` stays; bare refs hash `92352d6e…` both; bare objects count 4; stderr lists `2663885..0bfb801  HEAD -> main` |
| 6 | `git push --dry-run` | 1 unpushed commit | 0 | no | same; stderr `2663885..0bfb801  main -> main`; index/refs unchanged |
| 7 | `git pull --dry-run` | normal clone, remote ahead 1 | 0 | no | HEAD/origin-main/index/staged/FETCH_HEAD/logs identical (supp4-all.txt:29-56); stderr lists `03ce5a2..ccf4768  main -> origin/main`; empty-clone edge in F8 |
| 8 | `git commit -h` | unstaged mod.+new | 0 | no | usage 3551 B on stdout, stderr 0; all state hashes identical (results t08) |
| 9 | `git commit -a -h` | unstaged mod.+new | 0 | no | usage on stdout; nothing staged (index `83805ebf…` both) |
| 10 | `git commit --help` | unstaged mod.+new | 0 | no | `GIT-COMMIT(1)` man page on stdout; no state delta |
| 11 | `git --help commit` | unstaged mod.+new | 0 | no | same man page; no state delta |
| 12 | `git help commit` | unstaged mod.+new | 0 | no | same man page; no state delta |
| 13 | `git commit -m --help` | staged mod. | 0 | YES | subject `--help`; HEAD `264aecc…`→`47d5070…`; hook runs (supp4-all.txt:139-167). With nothing staged: rc 1, no commit (F6) |
| 14 | `git commit -a --dry-run -m x` | unstaged mod.+new | 0 | no | prints an as-if-staged view; index `0a755fb2…` both, staged hash `bfc172e5…` both (no staging) |
| 15 | `git push -n` (upstream) | 1 unpushed commit | 0 | no | stderr `2663885..0bfb801  main -> main`; nothing pushed |
| x | `git pull -n` | normal clone, remote ahead 1 | 0 | **YES** | real fast-forward: HEAD `03ce5a2…`→`ccf4768…`, origin/main advanced, FETCH_HEAD written, index/staged changed (supp4-all.txt:92-121) |
| x | `git fetch --dry-run` | normal clone, remote ahead 1 | 0 | no | all state identical (supp4-all.txt:1-28) |
| x | `git push --dry-run` (up to date) | clean clone | 0 | no | stderr `Everything up-to-date`; no delta (supp4-all.txt:134-138) |
| x | `git commit --dry-run` (nothing staged) | unstaged mod.+new | 1 | no | stdout ends `no changes added to commit`; no delta (supp4-all.txt:168-203) |
| x | `git add -n .` (clean tree) | clean clone | 0 | no | empty stdout/stderr (supp P8) |

## Findings

**F1 — All help forms are content-non-writing and exit 0 (not 129).** `git <sub> -h` for
add/commit/push/pull/stash/log/status: rc 0, usage on **stdout** (720–3658 bytes), stderr 0, and
identical head/index/staged/status/refs/FETCH_HEAD before and after every invocation
(`supp4-h.txt:2-15`; `supp/h.*.out`). `git commit -h`, `git commit -a -h`, `git commit --help`,
`git --help commit`, `git help commit`: rc 0, no state delta (`results/t08-commit-h.*` through
`t12-help-commit.*`); `--help` prints the `GIT-COMMIT(1)` man page because `/usr/bin/man` is present.

**F2 — `git add -n` / `--dry-run` are byte-clean.** rc 0; index sha256 identical before/after
(`results/t03-add-n.before:2` vs `.after:2` = `6e0effc6…`; `t04-add-dryrun.before:2` vs `.after:2` =
`1f5ab4c6…`); stdout is only `add 'a.txt'` / `add 'c.txt'`.

**F3 — `git push -n` / `--dry-run` send nothing.** With local HEAD `f80784a…` and bare
`refs/heads/main` `264aecc…`, the dry run prints `264aecc..f80784a  main -> main` on stderr, rc 0, and
bare refs are `264aecc…` before **and** after; `count-objects` stays `count: 4` (`supp4-all.txt:122-133`).
Up-to-date: rc 0, stderr `Everything up-to-date`, no delta (`supp4-all.txt:134-138`). Primary harness
t05/t06 show the same by hash (`results/t05-push-n.before:8` = `.after:8`, `bare_objs` unchanged).

**F4 — `git commit --dry-run` writes no content, but rewrites the index cache-tree extension.**
Staged fixture: HEAD `2663885…` unchanged, `git ls-files -s` hash `3e13c866…` unchanged, status unchanged,
rc 0, stdout is the would-commit report (`results/t01-commit-dryrun.*`). The index bytes change once:
118 → 137 bytes, 26 differing bytes; parsed v2 index shows entries byte-identical and only the `TREE`
extension changing (`002d3120300a`, invalidated `-1 0`, → `003120300a` + tree OID `6218aaa5…`);
`git ls-files -s` and `git ls-files --debug` diffs are empty (`supp2/index.pre`, `index.post`,
`ls.pre`, `ls.post`, `lsdebug.pre`, `lsdebug.post`). [INFERENCE] the extension is git's cache-tree
(the `TREE` signature and invalidated `-1` entry are observed; the semantic label is standard git
format). A second dry run changes nothing further (`supp2` P13 `idx_post == idx_post2`). With `-a` and
nothing staged, rc 0 and no index change at all (t14); with nothing staged, rc 1 (counts differ from
the staged case, so an H-family case must pick its fixture accordingly).

**F5 — `git commit -n` is `--no-verify`, and it commits.** rc 0, HEAD `2663885…`→`ccc6648…`, branch
ref moves, stdout `[main ccc6648] x`, and the instrumented pre-commit hook does **not** run
(hook lines 0→0). `git commit -h` usage confirms `-n, --no-verify` (`supp/h.commit.out:50`) and a
separate `--[no-]dry-run` (`supp/h.commit.out:52`). Control: the same hook runs for a normal commit
(F6), so the 0→0 delta is the `--no-verify` effect.

**F6 — `git commit -m --help` treats `--help` as the message value.** With a staged change: rc 0,
subject `--help`, HEAD `264aecc…`→`47d5070…`, hook lines 1 (supp4-all.txt:139-167). With nothing staged:
rc 1, stdout ends `no changes added to commit`, hook lines 0→1 (hook ran), no commit
(`results/t13-commit-m-helpval.*`). The earlier `-h` help forms never run the hook, so the hook firing
here proves `--help` was consumed as `-m`'s value, not as an option.

**F7 — `git commit -a -h` prints help and does not stage.** rc 0, usage on stdout, index sha
`83805ebf…` and staged hash unchanged before/after (`results/t09-commit-a-h.*`). `-a` does not win
over `-h`.

**F8 — `git pull --dry-run` is content-clean in a normal clone, with one symref edge case.**
Normal clone (origin/HEAD present), remote ahead 1: rc 0 and every captured state line identical
before/after, including `FETCH_HEAD absent` (`supp4-all.txt:29-56`); only stderr reports the update it
did not apply. Edge: a repository cloned from an **empty** remote has no `refs/remotes/origin/HEAD`;
`git pull --dry-run` (and `git fetch --dry-run`) then creates `refs/remotes/origin/HEAD` →
`refs/remotes/origin/main` plus `.git/logs/refs/remotes/origin/HEAD`, while `origin/main`, HEAD, index,
staged set and FETCH_HEAD stay unchanged (`supp4-all.txt:57-91`; `supp4-e2.txt`). [INFERENCE] the
creation is fetch's remote-HEAD setup for a missing symref, not a merge side effect; a normal clone
shows no change. The contract does not enumerate pull; a generic "dry run → clean" rule is correct
for content but not byte-identical in this edge.

**F9 — `git pull -n` is NOT a dry run.** `git pull -h` says `-n  do not show a diffstat at the end of
the merge` (`supp/h.pull.out:12`). Measured: rc 0 and a real fast-forward, HEAD `03ce5a2…`→`ccf4768…`,
origin/main advanced, FETCH_HEAD written, index/staged changed (`supp4-all.txt:92-121`). `-n` is
dry-run for `add`/`push` but not for `pull`; only `--dry-run` is dry.

**F10 — `git fetch --dry-run` is clean in a normal clone.** rc 0, all state identical, only a stderr
preview line (`supp4-all.txt:1-28`); the empty-clone edge behaves like F8 (`supp4-e2.txt`).

## Contract E4 cross-check

- `git <sub> -h|--help` → no row: **matches** (F1; exit 0, not 129).
- `git --help <sub>` and `git help ...` → no row: **matches** (F1).
- `git commit --dry-run` → no row: **matches for VCS content**; caveat F4 (index cache-tree bytes are
  rewritten on the first run). Case comparison uses findings/exit, not index bytes.
- `git add -n|--dry-run` → no row: **matches byte-for-byte** (F2).
- `git push -n|--dry-run` → no row: **matches**, including a remote that would move (F3).
- `git commit -n` still writes: **matches** — it commits and skips hooks (F5).
- `-m --help` (option value) still writes: **matches when a change is staged** (F6); with an empty
  index it exits 1 and writes nothing, and it is never a help display.
- `git pull --dry-run` (mandated probe, not in E4's enumeration): content-clean in a normal clone;
  the empty-clone symref edge is the only byte-level delta (F8).
- Warning for any shared `-n` handling: `git pull -n` is a real merge (F9); never generalize
  "`-n` = dry run" across git subcommands.

## Scanner cross-check at pinned revisions

Transcript `/tmp/mado-r20-ScoutGitDryEmpirical/forms.jsonl` (sha256 `673cf9e8…`, 15 lines; line N is
the Nth form above, one `bash` toolCall per line). Tool copies via read-only `git show`:

- `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d:tools/mado-tripwire.py` sha256
  `c1ae45a7…` → `python3 -I tool-9c54c56.py --scan forms.jsonl`: `MADO_TRIPWIRE: clean`, exit 0,
  `counts {host_mutation:0, live_probe:0, package_query:0}` — **no `vcs_write` class exists at this
  revision**. Control `git commit -m x` (a real write) is also clean (`scan-9c54c56-control.json`).
  So "before 9c54c56 = pass" for any git-write case is clean-by-blindness, not agreement.
- `1f7f995` and `e629f73`: identical tool sha256 `367be947…` →
  `python3 -I tool-1f7f995.py --scan forms.jsonl`: `MADO_TRIPWIRE: findings`, exit 1, 14 rows, all
  `vcs_write`; lines 1–11 and 13–15 flagged (rules `git:commit` on 1,2,8,9,10,11,13,14; `git:add` on
  3,4; `git:push` on 5,6,15; `git:pull` on 7); line 12 (`git help commit`) is clean. Findings at this
  sha carry no `evidence` key, so under the round-20 comparison rule those rows count as `observed`.
- Against the measured table, 12 of those 14 rows are false positives for the E4 forms
  (1,3,4,5,6,7,8,9,10,11,14,15); only rows 2 and 13 are true writes. `scan-1f7f995.json` sha256
  `47a36cd4…`; `scan-9c54c56.json` `18ab1e95…`.

## Limits

- One git version only (`2.56.0`, `/usr/bin/git`); `-h` exit codes and index cache-tree behaviour may
  differ on older git. `man` exists; the `--help` path without `man` was not tested.
- Local bare remote only: no network/auth, no rejected/non-fast-forward push dry run, no server-side
  hook effects. Only a `pre-commit` hook was instrumented; `commit-msg`/`post-commit`/`post-rewrite`
  and merge/rebase hooks were not.
- Not tested: submodules, sparse checkout, partial clone, unmerged/conflict index, linked worktrees,
  `.git` file (gitdir indirection), split index, `commit --amend`, `push --force` dry run.
- `git pull -n`/`git fetch --dry-run` are extras beyond the mandated forms; `jj` forms were not
  measured (out of this ticket).
- Host global config was observed but not normalized away; relevant keys were overridden locally.
  [UNK] exact behaviour under a different `pull.rebase`/`commit.verbose` combination (the global
  `pull.rebase=true` was present in every run; the dry-run path never merged).
- The cache-tree reading in F4 is [INFERENCE] from the parsed `TREE` extension; entry-level and
  byte-level deltas are observed.
- The scanner cross-check used a minimal one-`bash`-toolCall-per-line transcript; multi-cell/eval
  transcripts and other tool names were not exercised.

## Installs

none
