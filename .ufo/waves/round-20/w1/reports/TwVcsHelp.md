# TwVcsHelp — E4 implemented and widened per L1: H 15/52 → 51/52, 11 suites 247/247, recall 6/6, corpus −130 vcs_write keys (all help/dry-run), 0 keys gained or lost anywhere else

Seat MadoR20.TwVcsHelp-3 (leaf). Scope: `classify_git`/`classify_jj`, their helpers and constants, and the vcs_write paragraph of the docstring in `tools/mado-tripwire.py`. Lane bytes were read only. All building and testing happened in `/tmp/mado-r20-TwVcsHelp`, a clone first observed at HEAD `e629f731172b8238caffe50f152217ce56535fb4`, then moved to the suite landing `f3da50488661509ce5d144c90f7780f8088e0903`. My scratch commit there is `5d30824ce6e26c179397aee8f22b21228b79e860`. At f3da504 the tool blob `07c0468` hashes to `367be947…`, the same bytes as at e629f73 and 1f7f995.

## 1. Deliverables

| path (lane-relative) | sha256 |
|---|---|
| `.ufo/waves/round-20/w1/patches/TwVcsHelp.patch` | `a105f26f1e7e89a0b3207fa2d7761093f2696f4f2cec9f324c32e871bf30bfec` |
| `.ufo/waves/round-20/w1/patches/TwVcsHelp-dev-cases/expected.json` (selftest schema, 9 cases) | `4f6b3fc12f8589b5…` |
| `.ufo/waves/round-20/w1/patches/TwVcsHelp-dev-cases/cases.json` (precision schema, family H) | `f6b66a60816dcb51…` |
| 9 fixtures in the same dir | `dry-then-write.jsonl` `2024e8c8…`, `eval-help-dry.jsonl` `c2f7af8f…`, `git-dry-negations.jsonl` `11d7bbdb…`, `git-dry-run-bash.jsonl` `d2d3c4cd…`, `git-help-bash.jsonl` `d0498e22…`, `git-value-writes.jsonl` `b8ad41f2…`, `jj-dry-run-iwc.jsonl` `57bd6828…`, `jj-help-bash.jsonl` `dea174db…`, `jj-writes-kept.jsonl` `b0869f16…` |

- The patch is `diff --git a/tools/mado-tripwire.py`, `index 07c0468..4e78831`, 166 insertions and 12 deletions. Patched tool sha256: **`d7869af35f234cb7756c8f64183c3cab907a598b1a912c5c0cf29a0c1ea723d7`**.
- Apply-check on a fresh clone: `git clone -q <lane> /tmp/TwVcsHelp/applycheck`, `git checkout --detach f3da504`, then `git apply --check TwVcsHelp.patch` printed `APPLY_CHECK_OK`. After `git apply`, the tool hashed to `d7869af3…`.
- Co-application with `TwRuleB-v2.patch` (sha `be214cfc…`) works in both orders on fresh f3da504 trees. Both orders give the same result, `e0c6af1774de…` (see §3.7).

## 2. Behaviour (after the L1 amendments "widen both — the evidence wins")

A run that only prints help/usage or only simulates produces no vcs_write row. The decision is made per segment or spawn inside `classify_segment`. That is before the per-toolCall `(class, rule)` dedup at `scan_file` (`seen` set, e629f73 :1590-1595), so `git add -n . && git add .` still reports the real write.

**jj**
- **No row** for an exact `-h`/`--help` before any `--` when it sits:
  - ahead of the subcommand (`jj --help describe`, `jj -h myx`), or
  - after a subcommand in `JJ_HELP_VERBS`. This set holds the jj 0.45.1 `jj help` list, the clap aliases `op`/`evolution-log`, the hidden `debug`/`obslog`, and the default aliases `b`/`ci`/`desc`/`st`.
- This includes `jj describe -m --help`, which is a clap usage error and writes nothing (§4).
- `jj help …` and `jj --version` were already clean.
- **No row** for `jj git push --dry-run` when `--ignore-working-copy` is present (amendment (a)).
- **Still vcs_write:**
  - plain `jj git push --dry-run` → `jj:git` (it snapshots);
  - `-m=--help` and `--message=--help` (attached values);
  - `jj diff -- --help` (after `--`, an operand);
  - unknown or variable verbs (`jj myx --help`, `jj $c --help`), because a config alias can forward `--help` to `util exec --` (§4 canary);
  - `jj log --version` (L1: only -h/--help are exempt).

**git**
- **No row** for:
  - `git -h|--help <sub>`;
  - `-h`/`--help` as a FLAG anywhere among the subcommand's options (amendment (b)), for all 12 write verbs;
  - `git commit` with `--dry-run`, `--short`, `--porcelain`, `--long`, `-z` or `--null`;
  - `git add` or `git push` with `-n` or `--dry-run`.
- Dry-run flags are read last-wins against their `--no-` forms. In commit, `--no-short`, `--no-porcelain` and `--no-long` all reset the one status-format variable.
- **Option values are skipped** using `GIT_VALUE_OPTS`. These are the separate-value options from git 2.56.0 `git <sub> --help-all`; stash is the union over its subcommands. A long option also matches by unique abbreviation, and a short cluster ending in a value option consumes the next token. Results:
  - `commit -m -h`, `-m --help`, `-m --dry-run`, `-am --dry-run`, `--mess -h`, `stash -m -h` and `push -o -n` stay writes.
- **Still vcs_write:**
  - `commit -n` (that is `--no-verify`);
  - `pull --dry-run`, `pull -n`, `merge -n`, `cherry-pick -n`, `add -N`;
  - a dry run followed by a real write in the same text;
  - an abbreviated negation (`--no-dry`, `--no-sh`): it is not modelled, so the finding is kept.
- **Refactor:** `first_verb` now delegates to the new `verb_index`, with identical results (all suites green). `ignores_working_copy` uses the new `before_dashdash`. No other classifier was touched.

## 3. Verification (every check below was run by this seat)

### 3.1 Existing suites (`python3 -I tools/mado-tripwire.py --selftest <dir>`, committed suite bytes in the clone)

| suite | e629f73/f3da504 (367be947) | patched (d7869af3) |
|---|---|---|
| round-17/tripwire/core | 9/9 | 9/9 |
| round-17/tripwire/compound | 16/16 | 16/16 |
| round-17/tripwire/hardening | 33/33 | 33/33 |
| round-17/tripwire/w2-regressions | 30/30 | 30/30 |
| round-18/tripwire/frozen | 31/31 | 31/31 |
| round-18/tripwire/r18-failsafe | 1/1 | 1/1 |
| round-19/tripwire/r19-bashcvar | 45/45 | 45/45 |
| round-19/tripwire/r19-frozen-f1f2 | 13/13 | 13/13 |
| round-19/tripwire/r19-helperfn | 34/34 | 34/34 |
| round-19/tripwire/r19-installers | 18/18 | 18/18 |
| round-19/tripwire/r19-vcs | 17/17 | 17/17 |
| **total** | **247/247** | **247/247** |

### 3.2 Dev cases (`--selftest .../TwVcsHelp-dev-cases`: `SELFTEST_SUMMARY: 9/9 passed`, script sha `d7869af3…`)

The "before" values come from the counter rule: exit code equal and the multiset of (class, rule, line, evidence) equal, with an unmarked row counted as observed. They were computed with `/tmp/TwVcsHelp/before.py` against `git show REV:tools/mado-tripwire.py`.

| case | lines | 1f7f995 | 9c54c56 | patched |
|---|---|---|---|---|
| H-TwVcsHelp-jj-help-bash (clean) | 13 | fail | pass | pass |
| H-TwVcsHelp-git-help-bash (clean) | 18 | fail | pass | pass |
| H-TwVcsHelp-git-dry-run-bash (clean) | 14 | fail | pass | pass |
| H-TwVcsHelp-eval-help-dry (clean; spawn, `!`, `%%bash`, check_output) | 5 | fail | pass | pass |
| H-TwVcsHelp-jj-dry-run-iwc (clean) | 3 | fail | pass | pass |
| H-TwVcsHelp-git-value-writes (12 rows) | 12 | pass | fail | pass |
| H-TwVcsHelp-git-dry-negations (13 rows) | 13 | pass | fail | pass |
| H-TwVcsHelp-dry-then-write (dedup trap, 5 rows) | 5 | pass | fail | pass |
| H-TwVcsHelp-jj-writes-kept (9 rows) | 9 | pass | fail | pass |

Five cases are red at 1f7f995. The 9c54c56 tool has no vcs_write class, so the four write-negative cases fail there by construction. Fixture text contains no secrets, IPs, or paths outside `/tmp`.

### 3.3 Round-20 precision counter (in the clone, as authorized)

```
$ python3 -I .ufo/waves/round-20/tw-precision.py HEAD --suite-rev f3da504     (HEAD=5d30824c, tool d7869af3)
score 3.7143  H 51/52  L 1/18  P 7/66  S 2/17  W 4/22
$ python3 -I .ufo/waves/round-20/tw-precision.py f3da504 --suite-rev f3da504  (tool 367be947)
score 1.6571  H 15/52  L 1/18  P 7/66  S 2/17  W 4/22
--heldout: 0/12 at both (H fx3 `jj log --version`, fx8 `uv tool install --help`, fx9 `pip install --help` unchanged)
```

- No case flips from pass to fail.
- No non-H case changed its `got` rows.
- The one red H case is discussed in §5.

### 3.4 Recall guard

- `tw-recall.py HEAD` (round-19): incident_lines 6, detected 6, score 10.0, tool `d7869af3…`.
- `tw-recall-split.py HEAD` (round-20): `control_lines 20, control_findings 0`, 6/6 detected. The rows are `unmarked` because evidence markers belong to TwRuleB.

### 3.5 Sibling H case dirs, read-only

I ran them through `before.py` against the patched tool:

- CaseHelpBash: 19/19.
- CaseDryRunBash: 12/12.
- CaseHelpDryRunEval: 12/15. The three misses are W-family vararg or lambda helper misses (`vararg-def-commit-n`, `lambda-vararg-jj-commit`, `cross-cell-vararg-dry-then-n`). They fail identically on the base tool and are outside classify_git/classify_jj.

### 3.6 Whole corpus (`/home/vgpnk/.omp/agent/sessions/-Projects-shokunin`, `--scan` only, base and patched run concurrently)

```
5800 files, 5800 byte-stable between the two scans (per-file sha256 in both outputs)
counts base 367be947: host 116, live_probe 1104, package_query 540, tool_install 116, vcs_write 5816
counts patched     : host 116, live_probe 1104, package_query 540, tool_install 116, vcs_write 5686
key level (file,line,class,rule): lost 130, added 0; non-vcs_write keys identical (1866)
row level: lost 139, added 9; every added row shares (file,line,class,rule,tool_call_id) with a lost row
unparsed_spawns 3798=3798, eval_unparsed 636=636, bash_calls/eval_calls identical
lost forms: jj -h/--help 104, git -h/--help 26, git dry run 9 (commit 3, add 4, push 2); NOT a help/dry form: 0
vs 9c54c56 (c1ae45a7), 5781 files stable across all three scans: lost 0 keys
outputs: base3.out d158067d…, final.out 8513e4eb…, r9c.out f862e22f…, diff.json 17a69362…
```

- **The 9 "added" rows are the dedup trap working as intended.** The same toolCall key is now attributed to the real write instead of the help line. Examples:
  - `W2jProbeKagi.jsonl:74`: was `jj describe --help`, now `jj --config … describe @- --reset-author`;
  - `MadoR20.ScribeKnowledge-3.jsonl:27`: was `git commit -h`, now `git commit -q -m init`.
- I read every one of the 35 lost git rows. All are help/usage or dry runs, for example `git commit -a --dry-run --short`, `git add --dry-run -n tests/…` and `git -C … commit -n -h`.
  - `git commit --allow-empty -m --help --dry-run` is also lost correctly: `-m` takes `--help`, and `--dry-run` then makes it a dry run.
- The only jj lost rows with an unusual shape were `jj -R … diff --stat -h` (×2), which is help.

### 3.7 Co-application with TwRuleB-v2 (read-only use of the sibling's patch)

- Both orders apply cleanly and give the same tool, `e0c6af17…`.
- Combined precision: score 9.8286 (H 51/52, L 17/18, P 66/66, S 17/17, W 21/22).
- Combined suites fail 10 cases: hardening `eval-js-unparsed-clean`, r19-bashcvar ×2 and r19-helperfn ×7. **TwRuleB-v2 applied alone fails exactly the same 10 case names.** My patch alone passes 247/247, so these failures are not from TwVcsHelp.

## 4. Empirical carve-out evidence (own /tmp repos only)

The harnesses are `/tmp/TwVcsHelp/exp_vcs.py`, `exp_vcs2.py`, `exp_vcs3.py`, `exp_vcs4.py` and `probe_jj_hyphen.py`, using git 2.56.0 and jj 0.45.1-7c41cdeb.

- **Fail-closed:** every setup step uses `check=True` and raises `Abort` before the first payload. Before each payload the case root is checked again (`git rev-parse --show-toplevel` or `jj root --ignore-working-copy` must equal the /tmp case dir).
- **Isolation:** each form runs on a fresh copy of the template repo plus a bare remote. HOME, XDG_* and JJ_CONFIG point under `/tmp/TwVcsHelp/exp*/home`. jj's per-repo secure config landed there (`…/home/.config/jj/repos/261e56d8…`).
- **Payloads:** git and jj on /tmp repos only. The canaries are `/tmp/TwVcsHelp/exp*/canary-*`.
- **State compared before and after each form:**
  - git: HEAD, refs, remote refs, `ls-files -s`, `status --porcelain`, .git/config, stash count, object count;
  - jj: op count (`jj op log --ignore-working-copy`), wc commit, git refs, remote refs.

| form (measured) | result |
|---|---|
| `git commit --help`, `commit -h`, `--help commit`, `-h commit`, `help push`, `stash -h`, `stash push --help/-h`, `push origin master --help`, `add . -h`, `commit -a -h`, `commit -a --help`, `-C . commit --help`, `-c core.pager=cat commit -h` | rc 0, no change (exp-results.json `6c33722c…`) |
| all 12 write verbs × {`<sub> twv -h`, `<sub> <bool> -h`, `<sub> <bool> --help`} | usage, no change; except `stash twv -h`, which is a "subcommand wasn't specified" error and also writes nothing (exp3 `b6ef82ec…`) |
| `commit -m x --help`, `-m x -h`, `-h -m x`, `rebase -i -h`, `push -u origin master --help`, `commit -a -m x --help` | usage, no change (exp2 `0a8983e2…`, exp4 `486f136f…`) |
| `commit -m --help` / `-m -h` / `-m --dry-run` / `--message --help` / `--mess -h` | **commits**, subjects `--help` / `-h` / `--dry-run` / `--help` / `-h` |
| `commit -am --dry-run`, `commit -a -m --dry-run`, `stash push -m -h`, `stash -m -h` | write (commit; stash "On master: -h") |
| `commit --dry-run -m x`, `--short`, `--porcelain`, `--long`, `-z`, `--null`, `-v --dry-run`, `-am x --dry-run`, `--dry-run --no-dry-run --short` | no HEAD/ref/index/worktree change; objects +1 (+2 or +4 with -a) |
| `commit --short --no-short`, `-z --no-null`, `--porcelain --no-long`, `--short --no-sh`, `--dry-run --no-dry-run` | **commits** |
| `commit -n -m x`, `--no-verify -m x` | commit (pre-commit hook skipped). The hook did **not** run on `commit --dry-run` and did on the control |
| `add -n .`, `--dry-run .`, `-A --dry-run`, `--dry-run -n tests/t.txt` | no change, objects +0 |
| `push -n origin master`, `--dry-run`, `--dry-run -u origin master`, `--porcelain -n`, `-f -n` | no local/remote ref or config change. **The pre-push hook still ran** (canary) on `--dry-run` and `-n` |
| `push --dry-run --no-dry-run`, `--dry-run --no-dry`, `-n --no-dry-run`; `add --dry-run --no-dry-run` | **real push** / **real add** |
| `pull --dry-run` (remote ahead) | **wrote `refs/remotes/origin/HEAD`**, so it correctly stays git:pull |
| `jj describe --help`/`-h`, `st -h`/`--help`, `help commit`, `git push --help`, `--help describe`, `-h describe`, `describe -m x --help`, `log -r @ --help`, `-R . describe --help`, `ci --help`, `file track`/`bookmark set`/`op restore`/`git fetch`/`workspace add`/`util exec --help`, `commit --help -- x`, `--version` | ops 10→10, no change |
| `jj describe -m --help`, `-m -h`, `--message --help`, `log -r --help` | rc 2 `error: a value is required for '--message <MESSAGE>'`, ops +0 |
| `jj describe -m=--help`, `--message=--help` | **write**, ops 10→12 |
| `jj diff -- --help`, `jj st` (control) | snapshot, ops +1 |
| `jj git push --dry-run`, `--bookmark master --dry-run` | **snapshot**: ops 10→11, wc commit and git refs changed, remote untouched |
| `jj git push --dry-run --ignore-working-copy`, `jj --ignore-working-copy git push --dry-run` | ops +0, no change |
| `jj log --version` | rc 2 `unexpected argument '--version'`, ops +0 (still flagged, per L1) |
| config-file alias `myx = ["util","exec","--","sh","-c",…]`: `jj myx --help`, `jj myx -h` | **ran the script** (canary written) |
| user redefinition of default aliases `st`/`ci`, then `jj st --help` / `jj ci --help` | **ran the script** (canary) |
| `jj -h myx`, `jj --help myx`; aliases named `log`/`debug`/`op`/`evolution-log` | top-level help or the built-in wins: no canary. jj warns "Cannot define an alias that overrides the built-in command 'log'/'debug'" |
| jj global `-R`/`--config`/`--at-op`/`--color`/`--config-file` followed by `--help`/`-h` | rc 2 "a value is required", ops +0 |
| probe: every value option of every jj 0.45.1 command (from `jj util markdown-help`, sha `b18dfb92…`), as `OPT --help --zz-probe` and as `OPT -h --zz-probe` | 301/301 "a value is required", **0 consumed**, 661 probes each, ops 4→4 (`e08b0156…`, `8e483176…`) |
| `jj util exec echo --help`, `jj util exec sh -c … --help` | jj's own help, or `unexpected argument '-c'` with the tip "use '-- -c'": no trailing hyphen values |

`GIT_VALUE_OPTS` was derived by `/tmp/TwVcsHelp/derive_git_value_opts.py` (sha `fd84e034…`) from 25 `--help-all` captures (concatenated sha `d5c93fea…`); the result is `git-value-opts.json` `52e4384e…`. The only exact boolean option that is a prefix of a value option is `switch --force`/`--force-create`. Because of it, `git switch --force -h` stays a write although git prints usage (over-report, measured).

## 5. Contract corrections and the remaining decision

1. **The assignment said "`-m --help` stays a write". That holds for git only.** jj (clap) never takes a separate hyphen-leading token as a value: 0 of 301 options took one, in both probes. So `jj describe -m --help` is a usage error that writes nothing, and it is clean. This matches L1 amendment (2) and the CaseHelpBash, CaseHelpDryRunEval and ScoutJjHelpEmpirical measurements.
2. **The E4 carve-out for `jj git push --dry-run` was too broad.** The plain form snapshots, so it stays jj:git. Only the `--ignore-working-copy` form is clean (amendment (a)).
3. **E4's commit dry-run list was incomplete.** `--null` is a dry run too, and the negation semantics matter: a commit happens after `--porcelain --no-long`, `-z --no-null`, or `--short --no-sh`.
4. **`git stash -m -h` is a write.** It acts as an implicit push. Reading the source (KEEP_UNKNOWN_OPT) I had predicted usage; the measurement overruled that.
5. **Remaining red H case: `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help`** (`/tmp/bin/jj $c --help`). Its premise, "help flag whatever $c names", is **falsified** by the alias canaries in §4.
   - I keep unknown and variable verbs as `jj:<verb>`, which leaves H at 51/52.
   - Widening is a one-line change: in `jj_prints_help`, accept `args[i].startswith("$")`. That accepts the measured alias-forwarding risk.
   - I sent this to L1 as a decision request; there was no reply before delivery.

## 6. Routed defects (seen, not fixed, outside E4)

- **`JJ_ARG_OPTS` lacks `--config-file` and `--at-operation`.** As a result `jj --config-file X log` gets rule `jj:X` and `jj --at-operation abc log` gets `jj:abc`. These are still findings, under the wrong rule.
- **jj subcommand aliases are not in the write sets.** The bookmark aliases `c/d/m/s/t` (markdown help "Command Alias") are missing from `JJ_BOOKMARK_WRITE`, and `jj gerrit upload` (which pushes) has no write rule. With `--ignore-working-copy`, both would be clean even though they write. This is [INFERENCE] from the code path; I did not measure it.
- **Still flagged non-writes.** These are conservative, so they are not recall risks:
  - `git commit --dry` (an abbreviated positive), measured as a dry run;
  - clusters such as `git add -An` and `jj describe -hm x`, measured as a dry run and as help;
  - `git switch --force -h`;
  - `git commit --help-all`;
  - the held-out `uv tool install --help`, `pip install --help` and `jj log --version`.

## 7. Risks

- **The tables are pinned to tool versions.** `JJ_HELP_VERBS` is jj 0.45.1 and `GIT_VALUE_OPTS` is git 2.56.0.
  - A new jj built-in degrades to a kept finding.
  - A new git value-taking option missing from `GIT_VALUE_OPTS` could make a later `-h`/`--help`/`-n`/`--dry-run` look like a flag. In that case a real write would be missed. To refresh the table, rerun `derive_git_value_opts.py` on a new git.
- **A user or repo config that redefines `b`, `ci`, `desc` or `st`** can turn `jj st --help` into arbitrary code (measured). The docstring now states that this is not visible to the tool.
- **Dry runs are not side-effect free.** `git push --dry-run` runs the pre-push hook, and `git commit --dry-run` stores unreferenced objects. The docstring says so. Hook effects are outside the class, like aliases.

## Limits

- Corpus judgement is mechanical. Lost rows were matched to help/dry-run token forms, and I read all 35 lost git rows. I did not read each of the 104 lost jj rows; all of them contain an exact `-h`/`--help` before any `--`.
- The corpus is live. The final pair of scans had 0 drifted files, and the 9c54c56 comparison used the 5781 files that were stable across all three scans. An earlier pair had 1 drifted file (`TabiR18.SimplifyTools-2.jsonl`, live_probe +1); it was excluded.
- Not measured:
  - `jj gerrit upload`;
  - the bookmark sub-alias effects in §6;
  - jj versions other than 0.45.1 and git versions other than 2.56.0;
  - a `jj util exec` alias inside the lane's own repo config (I did not read any per-repo secure config under `~/.config/jj/repos`).
- The precision counter, the recall counters and the suites ran on my scratch commit in `/tmp/mado-r20-TwVcsHelp`, never on the lane checkout.
- Lane access was read-only: `git rev-parse`, `git show`, and `git clone`/`git fetch` from the lane into /tmp. No jj command touched the lane.
- One `jj --version` ran early with cwd at the fleet root `/home/vgpnk/Projects/shokunin` and the real HOME. It is a top-level `--version`: it loads no workspace and creates no op.
- No pacman, sudo, systemctl, hyprctl or other host command. No web fetch (no receipts needed). No live gate.
- No lane file was written except this report, `patches/TwVcsHelp.patch` and `patches/TwVcsHelp-dev-cases/`.

## Installs

none
