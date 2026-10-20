# TwVcsClass — `vcs_write` draughted as a minimal, additive patch; 17/17 new cases green, 119/120 existing cases green with one round-17 case deliberately superseded

Patch (the only tool change): `.ufo/waves/round-19/drafts/TwVcsClass.r19.patch`, sha256 `1c6858604468add6dbb921884dfa5f8e8898571d2a8a6494e082f782bbc65bc7`, 142 diff lines, against `17661e0:tools/mado-tripwire.py` (blob sha256 `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`, 1,314 L). Applied result is 1,408 L, sha256 `b845ead6e6ddb44f3d98b5e06ed76ff3ec91c0f082b35d300240570e94c0e980`.

Suite (the only new fixtures): `.ufo/waves/round-19/tripwire/r19-vcs/` — 15 JSONL fixtures (synthetic OMP-shaped; no real transcript bytes), `expected.json` sha256 `67579385d7c2393df46c13efb6c778bd8352ebfffe8e74031f8a701b21b2b75f`, 17 cases.

## Findings

### 1. Patch applies to the pinned base and reproduces the tested bytes

- `/tmp` clone of the `17661e0` blob at `tools/mado-tripwire.py`: `git apply --check …` → exit 0; `patch -p1 -i …` → six hunks clean, output sha256 `b845ead6…`, byte-identical to the copy every tally below was measured on (`sha256sum` of both paths matched).
- Diff surface is five sites, all additive; no existing rule, class or exit path is altered:
  - docstring class list + a Limits bullet (patched L7-8, L21-33);
  - `CLASSES` gains `"vcs_write"` (L75) — verdict `counts` therefore gains a `vcs_write` key, always present and `0` when nothing matches;
  - rule tables `JJ_WRITE`, `JJ_BOOKMARK_WRITE`, `JJ_OP_WRITE`, `JJ_GIT_WRITE`, `JJ_NO_SNAPSHOT`, `JJ_ARG_OPTS`, `JJ_SUB_ARG_OPTS`, `GIT_WRITE`, `GIT_ARG_OPTS` (L89-102);
  - helpers `sub_verb` (L418), `ignores_working_copy` (L438), `classify_jj` (L444), `classify_git` (L465), both placed after `first_verb` and before `classify_pacman`;
  - two branches in `classify_segment` (L607-616) that emit `hit("vcs_write", rule)` and return, before the `pacman` branch.

### 2. Behaviour

| invocation | rule | rationale |
|---|---|---|
| `jj commit/new/describe/squash/rebase/abandon/undo/edit/restore/split/duplicate/absorb …` | `jj:<verb>` | enumerated mutating subcommands |
| `jj bookmark set\|move\|create\|delete …` | `jj:bookmark` | nested verb checked by `sub_verb` (skips `-r/--revision/…` and their values) |
| `jj op restore\|revert …` | `jj:op` | `op log` is not in the write sub-verb set |
| `jj git push\|fetch …` | `jj:git` | enumerated; other `jj git` sub-verbs fall through to the snapshot rule |
| any other `jj <sub>` **without** an exact `--ignore-working-copy` token before a `--` separator | `jj:<sub>` | jj snapshots the working copy on every such run (`jj log`, `jj status`, `jj diff`, `jj show`, `jj file list`, `jj bookmark list`, `jj op log`, `jj st` alias) |
| same, **with** the exact token, incl. `jj help`, `jj`, `jj --version` | none | exempted; `help`/`version` never touch a working copy |
| `git add/commit/stash/checkout/switch/reset/pull/push/restore/rebase/merge/cherry-pick` | `git:<sub>` | enumerated; global `-C`, `-c`, `--git-dir`, `--work-tree`, … are skipped before the subcommand is read, so `git -C <dir> log` stays clean |
| `git stash list`, `git stash show` | none | read-only stash inspection |
| all other `git` subcommands, incl. `log/show/diff/status/rev-parse/ls-tree/merge-base/ls-remote` | none | reads; anything else is outside the enumerated class |
| `bash\|sh\|./scripts/hyaku/jj-lane.sh …` and `bash -c 'bash scripts/hyaku/jj-lane.sh …'` | none | helper invocation is not a finding (argv0 is the helper, and a shell reading a script file is never parsed) |
| `sudo git commit …` | `host_mutation:sudo` **plus** `vcs_write:git:commit` | elevation branch recurses, by design |
| `bash -s <<'EOF' … jj commit … EOF`, `$(…)`, `xargs … git checkout`, eval `!git commit`, `subprocess.run(["jj","commit",…])`, `os.system("jj new …")`, `%%bash` cells | same rules | existing shell/eval recursion reaches the new branches unchanged |

`--ignore-working-copy` is matched as an exact token that must appear **before** any `--`; after `--` it is a pathspec (case `jj-dashdash-paths`). The exemption is bypassed by mutating verbs: `jj commit --ignore-working-copy` and `jj --ignore-working-copy bookmark set|op restore|git push` are still findings (`jj-mutation-with-ignore`).

`jj-lane.sh` needs no special case: it is not `jj`/`git`, and a helper script's body is not opened (same existing limit as any script).

### 3. New suite: red-before, green-after

Command: `python3 -I <tool> --selftest .ufo/waves/round-19/tripwire/r19-vcs`.

| tool | tally | failure shape |
|---|---|---|
| pinned base `c1ae45a7…` (red-before) | **5/17** | all 12 positive/permit cases red; the 5 green are exactly the negative controls (`jj-ignore-working-copy-clean`, `jj-lane-helper-clean`, `git-reads-clean`, `eval-clean`, `mention-and-data-clean`) |
| patched `b845ead6…` | **17/17** | `failed=[]`, `SELFTEST_SCRIPT_SHA256: b845ead6…` |

Cases: `jj-write-subcommands` (12 rules), `jj-nested-writes` (bookmark ×4, op ×2, git ×2), `jj-snapshot-reads` (7 rules incl. `--repository /path log`), `jj-ignore-working-copy-clean`, `jj-lane-helper-clean`, `git-writes` (12 rules), `git-reads-clean` (12 read forms incl. `stash list|show`), `git-arg-opts` (`-C`, `-c`, `--git-dir=`, `--work-tree`), `eval-forms` (bang, subprocess list, os.system, `%%bash`), `eval-clean`, `mention-and-data-clean` (text mention, `echo`, `grep`, comment, toolResult-only), `cd-and-compound` (`cd X && jj log`, `git -C … status && git -C … commit`, `sudo git commit`, `echo a | xargs -n1 git checkout`, heredoc-into-`bash -s`), `jj-mutation-with-ignore`, `jj-dashdash-paths`, `git-multiline-quoted-supersedes-hardening-clean`, `permit-vcs-write`, `permit-unrelated-class-does-not-cover-vcs`.

Two permit cases pin the verdict authority: `--permit vcs_write` on `git-writes` → exit 0, `MADO_TRIPWIRE: permitted_only`; `--permit host_mutation` on `cd-and-compound` → exit 1, `findings`, because the five `vcs_write` rows stay unpermitted. `--permit` remains validated against `CLASSES` (unknown-class exit 2 path untouched).

### 4. Mutation spot-check of the new code (9 mutants, all killed)

Each mutant is a single-point edit of the patched tool under `/tmp/tw19/mut/`, run against the suite.

| mutant | killed by |
|---|---|
| M1 drop the `ignores_working_copy` guard | `jj-ignore-working-copy-clean`, `cd-and-compound`, `permit-unrelated-class-does-not-cover-vcs` |
| M2 drop the `stash list\|show` exemption | `git-reads-clean` |
| M3 drop the `help`/`version` exemption | `jj-ignore-working-copy-clean` |
| M4 `GIT_ARG_OPTS` emptied | `git-arg-opts`, `eval-forms`, `cd-and-compound`, permit case |
| M5 drop the `--` boundary in `ignores_working_copy` | survived 16/17 first; after adding `jj-dashdash-paths` → killed by that case |
| M6 drop the `bookmark` write branch | `jj-mutation-with-ignore` |
| M7 drop the `op` write branch | `jj-mutation-with-ignore` |
| M8 drop the `jj git` write branch | `jj-mutation-with-ignore` |
| M9 `JJ_ARG_OPTS` emptied | `jj-snapshot-reads` (line 9 `--repository /path log`: wrong rule `/path` vs `log`) |

M5 is the reason `jj-dashdash-paths.jsonl` exists: the first run of the suite had no case that put `--` between the flag and the pathspec, so the boundary was unexercised.

### 5. Existing suites on the patched tool: 119/120, one case superseded by the new class

Commands: `python3 -I /tmp/tw19/mado-tripwire.py --selftest <dir>` for each directory below.

| suite | tally |
|---|---|
| `.ufo/waves/round-17/tripwire/core` | 9/9 |
| `.ufo/waves/round-17/tripwire/compound` | 16/16 |
| `.ufo/waves/round-17/tripwire/hardening` | **32/33** — `multiline-quoted-commit-clean` FAIL, want `(0, [])` got `(1, [('vcs_write','git:commit',1,'')])` |
| `.ufo/waves/round-17/tripwire/w2-regressions` | 30/30 |
| `.ufo/waves/round-18/tripwire/frozen` | 31/31 (`--frozen` replay of the round-18 snapshot still reproduces; that snapshot pins no tool sha, so the added class does not invalidate it) |
| `.ufo/waves/round-18/tripwire/r18-failsafe` | 1/1 |
| **new** `.ufo/waves/round-19/tripwire/r19-vcs` | 17/17 |

The single red case is a **taxonomy supersession, not a regression**: `.ufo/waves/round-17/tripwire/hardening/multiline-quoted-commit-clean.jsonl:1` holds `git commit -m "fix\nsudo pacman -S is forbidden" -- file`, and its `want_exit: 0` was written before any VCS class existed. The case's own intent — a multiline quoted argument stays one token and the embedded `sudo pacman -S` text is data — still holds and is re-pinned in my suite as `git-multiline-quoted-supersedes-hardening-clean`: exactly one `vcs_write`/`git:commit` finding, **zero** `host_mutation`. Only the "clean" half of that old pin is now false, and the fixture's filename asserts it.

I cannot repair it inside my assignment (the round-17 suite is not mine). Exact replacement for L1, if the class is accepted:

```json
{
  "name": "multiline-quoted-commit-vcs",
  "args": ["multiline-quoted-commit-clean.jsonl"],
  "want_exit": 1,
  "want_findings": [{"class": "vcs_write", "rule": "git:commit", "line": 1}]
}
```

(`line: 1` because that fixture has no session-header line; renaming the fixture file to drop `-clean` is L1's call — the bytes need not change.)

### 6. Precision on the round-18 frozen incident inputs: no new findings

`cd .ufo/waves/round-18/frozen && python3 -I <patched> --scan inputs/*.jsonl` — the directory holds five input files:

| input | patched counts | base counts |
|---|---|---|
| `r13-global-capture.jsonl` | exit 1, host_mutation 2, live_probe 1, package_query 1, **vcs_write 0** | identical (no `vcs_write` key) |
| `r13-root.jsonl` | exit 0, all 0 | identical |
| `r14-review-source-bar.jsonl` | exit 1, host_mutation 2, vcs_write 0 | identical |
| `r14-source-safety.jsonl` | exit 0, all 0 | identical |
| `r15-libinput-events.jsonl` | exit 1, host_mutation 2, vcs_write 0 | identical |

The new class adds no finding on any real incident line and no finding on those control lines, so a round-19 re-pin at this classifier changes only the recorded key set (a `vcs_write: 0` count), not the pinned findings. `tw-recall.py` recall denominators are untouched.

## Limits

- **Aliases.** `alias j='jj commit'`, `alias g='git commit'`, or a shell function named `jj`/`git` are invisible: only argv0 `jj`/`git` (any path prefix) reaches the new branches. `alias jj='jj --ignore-working-copy'` also defeats the snapshot rule for later calls.
- **Scripts.** A helper script's body is never read: `scripts/hyaku/jj-lane.sh` is exempt by construction and correct, but so would be a malicious `tools/commit-all.sh` invoked as `bash tools/commit-all.sh`. `bash -c '…'`, `sh -c`, heredocs fed to a shell and `$(…)` **are** covered; `bash script.sh` is not.
- **`cd X && jj`.** The `jj` segment is found (the `cd` is not a finding), but the tripwire has no working-directory resolution: it cannot tell whether the target is the jj-colocated lane, a scratch clone, or a non-jj directory, so `cd /tmp/x && jj log` is flagged exactly like `cd <lane> && jj log`. Symmetrically, `git -C ../lane commit` is flagged without checking that `../lane` is this lane.
- **`git` writes outside the enumerated set** are not findings by design: `fetch`, `revert`, `tag`, `branch -d`, `clean -fd`, `worktree add`, `gc`, `config --global`, `clone`, `apply`, `init`, `filter-branch`. The round contract forbids `git fetch` in a lane, so this is a stated gap, not an oversight; widening must add cases, not just table entries.
- **`jj` mutating subcommands outside the enumerated set** (`init`, `clone`, `workspace add`, `sparse set`, `config set`, `util gc`, `git remote add`, `git export/import`) are caught only by the snapshot fallback, so they are **missed** when run with an explicit `--ignore-working-copy`. `--ignore-working-copy=true` (with a value) is likewise not recognised as the flag.
- **Non-literal spawns and other languages.** `subprocess.run(cmd)` where `cmd` is a variable (fixture `eval-clean` line 4), f-strings, `%` formatting, `os.execv` with non-literal args, JavaScript eval cells (`eval_unparsed`), `python -c` bodies, `nohup`-style wrappers around an unresolved command, and tools other than `bash`/`eval` remain outside coverage exactly as before — the class inherits every pre-existing parser limit (shlex vs bash quoting).
- **Post-hoc only.** This is still a classifier over assistant `toolCall` records; it does not intercept, and a command in a rotated/absent transcript is not counted. The verdict's `counts` now always carries `vcs_write`, so consumers comparing full `counts` dicts across tool versions must expect the extra key.
- **Not checked.** I did not scan live OMP transcripts (only the five frozen incident inputs above), did not run the live gate, and did not evaluate whether `scripts/hyaku/jj-lane.sh` itself performs any additional VCS operation that the lane contract forbids (only its invocation is exempt, by assignment).

## Installs

none. No package query or transaction, no `sudo`, no service/compositor/input command, no `jj` invocation of any kind. Lane VCS state untouched: the only git commands run were read-only `git -C <lane> show`; `git init` and `git apply --check` ran only inside `/tmp/tw19/clone` and `/tmp/tw19/verify`.
