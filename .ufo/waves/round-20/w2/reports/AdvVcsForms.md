# AdvVcsForms — partly falsified: E4's git dry-run parser misses clustered `-n`/abbreviated `--dry`, and the jj "snapshots on all of them" fallback flags measured non-snapshotting verbs

Attacked: E4 / TwVcsHelp git+jj help-and-dry-run carve-outs at `28c6837` (tool sha256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`, verified at lane tip `a4046a8`). Method: every named form measured as a real command in a fresh `git init` / `jj git init --colocate` repo under `/tmp` with `HOME`, `XDG_CONFIG_HOME`, `GIT_CONFIG_NOSYSTEM` redirected (git 2.56.0, jj 0.45.1 — the exact versions the tool docstring cites); mutation detected by hashing `.git`/`.jj`/bare-remote file bytes plus HEAD, `for-each-ref`, `ls-files -s`, `jj op log` ids across the command. Then a single-line transcript fixture per form (`--scan` only, fixtures never executed) was compared with the final tool. Harnesses and outputs under `.ufo/waves/round-20/w2/AdvVcsForms/` (`run_git.sh` cf06fdd9…, `run_jj.sh` 91f58bff…, `measure-git.txt` 9b48230d…, `measure-jj.txt` 3a8f6791…, `scan-all.json` e7e183a2…, `scan-divergences.txt` 40fa62ea…, `fixtures/manifest.json` fe4debcb…).

## Result: 31 of 74 outside-suite forms are flagged `vcs_write` against a measured non-write

`python3 -I tools/mado-tripwire.py --scan fixtures` on the seat dir → `counts.vcs_write: 51` over 74 fixtures; 30 of the 51 flagged rows correspond to measured non-writes (plus `git-add-dd-n` added late, 31 divergences total; `scan-divergences.txt` has all rows).

### F1 — clustered short options containing `n`/`z` escape the dry-run test (8+ cases)

`git_option_flags` (tools/mado-tripwire.py:614-637) appends the whole token `"-nv"` to `flags` and never sees `-n`/`-z` inside it. Measured in fresh repos, all real dry runs / non-commits:

| command | measured | tool |
|---|---|---|
| `git add -nv .` | index untouched (mut=no; prints `add 'seed.txt'`) | `vcs_write git:add` |
| `git add -An .` | mut=no | `vcs_write git:add` |
| `git add -vn .`, `git add -nvf .`, `git add -Nn .` | mut=no | `vcs_write git:add` |
| `git add -pn .` | rc=128 "options '--dry-run' and '--interactive/--patch' cannot be used together" | `vcs_write git:add` |
| `git push -nv` | mut=no (pre-push canary runs — still no ref move) | `vcs_write git:push` |
| `git commit -zn -m c4` | rc=0, no commit (prints porcelain status) | `vcs_write git:commit` |

Same miss through eval surfaces: `subprocess.run(["git","add","-nv","."])`, `!git commit -zn -m c4`, `%%bash\ngit add -An .` all flagged. `git add -n -v .` (separate flags) is correctly clean — the defect is specifically the cluster.

### F2 — abbreviations asymmetric: negation abbreviations kept, `--dry`/`--porcel` dropped (5 cases)

git accepts unique abbreviations of any long option. Measured: `git add --dry .` mut=no (dry), `git push --dry` mut=no, `git commit --porcel -m c8` mut=no — the tool flags all three (`git_option_flags` models abbreviation only for GIT_VALUE_OPTS, not for dry/format options, while the code *does* model abbreviated negations at line 658). So the suite's declared rule "abbreviated negation stays a finding" is honoured but the mirror case — abbreviation of the dry/form itself — is an unhandled false positive. Related: `git add --dry-run=false`, `git commit --dry-run=false`, `git push --dry-run=false` all error rc=129 "option 'dry-run' takes no value"; flagged anyway (weaker FP: the command cannot write at all).

### F3 — jj "snapshots the working copy on all of them" is measured false for an enumerable set (7 cases)

Docstring/E4 basis (tools/mado-tripwire.py:61-67): every jj subcommand outside help/version snapshots the working copy, so the fallback `return "jj:" + verb` (line 611) flags them all. With a dirty working copy, `.jj` file-hash and op-id diffs show these do **not** snapshot or write:

| command | measured | tool |
|---|---|---|
| `jj root` | mut=no (prints path, no op) | `vcs_write jj:root` |
| `jj config list` | mut=no | `vcs_write jj:config` |
| `jj util config-schema` | mut=no | `vcs_write jj:util` |
| `jj util exec -- true` | mut=no | `vcs_write jj:util` |
| `jj util exec -- git status` | mut=no | `vcs_write jj:util` |
| `jj op log` — **correctly** flagged: measured mut=yes (snapshot op `…snapshot working copy`) | | confirms the claim holds for *some* readers |
| `jj file list`, `jj prev`, `jj log` | mut=yes | consistent |

`util exec` is a deliberate conservative note in the docstring ("past `util exec --`, so it stays a finding"), but `root`, `config list`, `config-schema` and `op log` show the blanket claim is wrong in both directions of specificity: it over-covers (root/config/util do nothing) and is wrong about *which* subcommands snapshot (`op log` does, `root` doesn't). Criterion-30′ precision: these are ordinary H-family misses — rows claimed `observed` for commands that provably change nothing.

### F4 — `--dry-run` scoped to the wrong clap level inside `jj git` and on verbs that lack it (5 cases)

`classify_jj` line 606-608 checks `"--dry-run" in before_dashdash(args)` over the *whole* argv, not the tokens after `push`. Measured:

| command | measured | tool |
|---|---|---|
| `jj git --dry-run push` | rc=2 `error: unexpected argument '--dry-run'` (it is a `push` option, not a `git`-group option); no mutation | `vcs_write jj:git` |
| `jj git fetch --dry-run` | rc=2 `error: unexpected argument '--dry-run'` | `vcs_write jj:git` |
| `jj git push --dry-run -- --ignore-working-copy` | rc=2 `error: unexpected argument '--ignore-working-copy'` | `vcs_write jj:git` |
| `jj describe --dry-run -m x` | rc=2 `error: unexpected argument '--dry-run'` (describe has no dry-run; not in fallback's carve-out) | `vcs_write jj:describe` |

A `jj` run that clap rejects before doing anything is flagged as a write that "snapshots the working copy" — it never reaches workspace load (rc=2, mut=no in every case).

### F5 — confirmed correct behaviour (E4 stands on these)

Measured AND flagged correctly:
- `git add --dry-run --no-dry-run` → real write (last-wins), flagged; reversed order clean. `git commit --dry-run --no-dry-run -m c9` → real commit, flagged.
- `git commit --porcelain --no-dry-run -m c6` → measured **no** commit (the status-format options force dry-run even through `--no-dry-run`), tool clean. Same reversed. So the tool's fmt/dry split happens to match git's stickier semantics.
- `git push --porcelain` (alone) → measured real push (mut=yes) and flagged; `git push --porcelain -n` → dry, clean. `--porcelain` on *push* is not a dry-run flag — opposite of commit.
- `git add --no-dry .`, `git commit --no-dry -m c20`, `git push --no-dry` → measured writes, flagged (abbreviated negation rule holds).
- `git commit -m -n` → commits with message `-n`; flagged. `git commit -am c10 -h` → usage, clean. `git commit -an -m c1` → real commit (`-n` = --no-verify), flagged.
- `jj --help describe`, `jj describe -h -m x` → help, clean; `jj describe -m -h` → rc=2 clap error, clean; `jj describe -- -h` → snapshots wc *then* fails revset parse (mut=yes) → correctly flagged.
- `jj git push --dry-run` → measured mut=yes (snapshot) → flagged; `--ignore-working-copy` in either order → mut=no → clean. `jj --ignore-working-copy log` / `jj log --ignore-working-copy` → clean. `jj --ignore-working-copy describe -m hi` / `jj describe --ignore-working-copy -m hi` → mut=yes (describe always writes) → flagged.
- `jj git push -b main` → real push to file:// remote → flagged `jj:git`.
- `git stash push -m st1` → real stash → flagged `git:stash`.

### F6 — declared boundary, verified, no falsification but worth recording

`git -c alias.x=commit x -m c15` → measured real commit (new HEAD), tool silent — docstring explicitly puts "git subcommands hidden in aliases" outside the class, so this is a declared miss, not a falsification. Same for `git clean -f` (deleted the untracked file — my index/ref probes show mut=no only because they don't watch the worktree) and `git revert --no-edit HEAD`. `git -c alias.x=commit` is statically visible inside the transcript though — the boundary is *cheaper* to close than the docstring implies. [INFERENCE: L1 may have weighed this; the miss is disclosed, so I score it a tradeoff the judge may still reject on cost, not a hidden defect.]

`git -n add .` (rc=129, `unknown option: -n`), `git checkout -n seed.txt` (rc=129, `unknown switch 'n'`), `git push --repo --dry-run` (rc=128, `--dry-run` consumed as the `--repo` value — the GIT_VALUE_OPTS skip works correctly, flag survives anyway and the command errors) — all flagged against commands that cannot execute; weakest FP class, same conservative-family pattern as F4.

## Smallest safe corrections (fixable defects, not design rejections)

1. In `git_option_flags`, expand short clusters into letters before the dry/format/null tests (keep the existing last-letter value-skip for `-U`/`-m`/`-F` etc.): closes F1 without touching the `commit -n` = `--no-verify` rule (cluster `-an` still yields `-a`,`-n` where `-n` is correctly ignored for commit).
2. Treat abbreviations symmetrically: extend the "starts-with" test at line 658 to the *positive* dry/format options (`--dry` → dry, `--porcel` → fmt) so F2 closes the same way negation abbreviations are kept.
3. In `classify_jj`, restrict the `--dry-run` test to tokens after the `push` sub-verb and add a small measured no-snapshot list (`root`, `config`, `util config-schema`, `util exec`) alongside `help`/`version` — or flip the docstring to enumerate snapshotters; the current blanket claim is empirically wrong on F3's list.
4. [INFERENCE] Scope `jj git` flag checks to post-`push`/`fetch` tokens (F4).

## Limits

- Mutation = HEAD/remote-refs/`ls-files -s`/file-byte diffs + `jj op log` ids; a write that touches none of these (e.g. `COMMIT_EDITMSG` on a *failed* commit) is excluded by design — verified on `h-commit-an`/`h-commit-m-n` where real commits show mut=yes.
- `jj` snapshot claims measured on a dirty working copy at jj 0.45.1 colocated; a clean working copy snapshots nothing (state-dependent hazard) — consistent with the tool's stated semantics either way.
- Fixtures were scanned, never executed; equivalent commands ran only in `/tmp` repos with redirected config. No lane writes, no pacman/sudo/compositor ops.
- I did not rerun the precision/selftest counters (Rerun* seats own those); this seat's contribution is the 74-form outside-suite battery.

## Installs

none (git 2.56.0 and jj 0.45.1 were already on PATH).
