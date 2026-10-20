# CaseHelpBash — 19 H cases written (12 red at 1f7f995, 2 controls, 6 write negatives); a /tmp run shows jj does not write on `jj describe -m --help`

## Verdict

- I wrote 19 family-H cases on the bash surface to `.ufo/waves/round-20/w1/cases/CaseHelpBash/`: 19 `.jsonl` files and `cases.json`, schema `mado-tw-precision-cases-v1`.
- Results under the counter rule (exit code equal AND the multiset of (class, rule, line, evidence) equal, where a row without `evidence` counts as `observed`):
  - **1f7f995: 7/19 pass, 12 red.**
  - **9c54c56: 13/19 pass.** All 6 failures are write negatives. 9c54c56 has no `vcs_write` class at all: `CLASSES = ("host_mutation", "package_query", "live_probe")`, `/tmp/CaseHelpBash/tool-9c54c56.py:61`.
  - e629f73 has the same tool sha256 as 1f7f995 and gives the same 7/19.
- **Contract contradiction (E4).** E4 says "Still writes: … `-m --help` (option value)". In my runs this holds for git 2.56.0. It does **not** hold for jj 0.45.1:
  - `jj describe -m --help` exits with rc=2: `error: a value is required for '--message <MESSAGE>' but none was supplied`.
  - The op log stays 6→6 and the repo tree is byte- and mtime-identical, even with a dirty working copy.
  - jj takes a hyphen value only when it is attached to the option: `--message=--help` and `-m--help` both wrote, setting the description to `--help`.
  - So per E4's evidence clause, the item's write negative `jj describe -m --help` ships as a **want-clean red case**. The "option value" intent is carried by three write negatives instead: `git commit -m -h` (named in the item), `git commit -m --help` and `jj describe --message=--help`.
  - I sent this to `MadoR20.TwVcsHelp-3`. They replied that their own /tmp runs agree and their patch follows the evidence: jj `-m --help` is clean; git `-m --help`/`-m -h`, jj `--message=--help` and jj `-- --help` stay `vcs_write`. `MadoR20.CaseHelpDryRunEval-3` independently reported the same jj rc=2 behaviour. Both are their claims; I did not re-run their harnesses.

## Files written

All are in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CaseHelpBash/`:

| file | sha256 |
|---|---|
| cases.json | `baa54919b80d15bef163a04a647722c6bf49f6756ceefd1d680f550c3d3f7b62` |
| HelpBash-jj-describe-help.jsonl | `abf316aedb59e506131054d49d30132d388a95a7cdb8f6040c45af20f4a1c73c` |
| HelpBash-jj-st-h.jsonl | `8162dc6f5c10caa5501d594ac5f9478288b40fa6aa7a9a01d179114894a6dc87` |
| HelpBash-jj-git-push-help.jsonl | `e5e7e730e621e6d5b1afd3fb887f041e83a2c09cce8bedf0f664c088faafcf33` |
| HelpBash-jj-help-flag-describe.jsonl | `f9b3e630a7185a0588f99a871f82d8841cca99e0198c0c9f5bed217d8308df7c` |
| HelpBash-jj-describe-m-x-help.jsonl | `6ddeac32f0d6355fd30b535dc2e8b9dc9ab7b707858e198df4cae522c8cf0971` |
| HelpBash-jj-describe-m-help-parse-error.jsonl | `cd25367e2f6de1f4267cabfd66a7fd4a7a52dc8b4e554ed600925a87be9b8318` |
| HelpBash-git-commit-help.jsonl | `a32c63250ea92ad38927ddd926ffeb938d0568003481d14ba6060a95a2111b2c` |
| HelpBash-git-commit-h.jsonl | `18371d58f3a75e47162b9f4780f80660dedd4a8e48c414c0594618da36d7a38a` |
| HelpBash-git-help-flag-commit.jsonl | `ddd52c51d966abadf0b8ec0648a33751b3384a89fb14ff554149368ffd32c663` |
| HelpBash-git-stash-h.jsonl | `cd6b6ae20d2a93b9fc0260d3e621db96e5c9d6a9ef0ff5bbb3ac54a48fb5f6a5` |
| HelpBash-git-commit-m-x-help.jsonl | `03e50124c78ef49b7156cc1cb4c998098362cfdc11277e9ebc491f60e9c23e43` |
| HelpBash-jj-help-commit.jsonl | `9aa2b40934c40a1b04de3136f3fcade6b2e9c693bad6765d8a28be037a49ed19` |
| HelpBash-git-help-push.jsonl | `3db16c88cc601380d43d3e1f082a54e4f10cfc827b8a6fcd4297caa676d51154` |
| HelpBash-git-commit-m-h.jsonl | `6906fb33bdc82d5e7cc729f034361560870c35605f04c7c6f3fa26051088559f` |
| HelpBash-git-commit-m-help.jsonl | `dd49d18e782b65c2e8c185534b678e4169ab2bc7ead0eca8d0977ea4c7fa3d37` |
| HelpBash-jj-help-then-describe.jsonl | `8a33360947451d414e564db0411bebedbd6df38e716aac8d602847639bf4d319` |
| HelpBash-jj-st-h-then-describe.jsonl | `f70227cb6f68c43118c15a4735e5cd5c20a5f83fcdc8293ebf18dae088234c5c` |
| HelpBash-jj-describe-message-eq-help.jsonl | `c4dce209c8e15b91d441a282749484177972c17df7a279fe3b69af20520d4efc` |
| HelpBash-jj-describe-dashdash-help.jsonl | `d3e9396c45df250406d99d72f984e50a90119015e4fdbf890530945e79f8063b` |

- Each file is one line holding one assistant `toolCall` named `bash` with `{command}`, in the envelope of `round-19/tripwire/r19-helperfn/py-lead-cross-cell-literal.jsonl`.
- Every `line` in `want_findings` is 1.
- The fixture text contains no paths.

## Cases: `before` under the counter rule, with per-case /tmp evidence

Evidence comes from run r3 of `/tmp/CaseHelpBash/emp.py` (jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5 and git version 2.56.0). Before each command the working copy was made dirty. "tree identical" means that for every file under the repo, including `.git/` and `.jj/`, these matched before and after the command: path, mode, size, mtime_ns and sha256.

| # | case | command | want | 1f7f995 | 9c54c56 | role | empirical result |
|---|---|---|---|---|---|---|---|
| 1 | H-HelpBash-jj-describe-help | `jj describe --help` | clean, exit 0 | **fail** | pass | red | rc 0; stdout "Update the change description or other metadata [default alias: desc]"; op log 5→5; tree identical |
| 2 | H-HelpBash-jj-st-h | `jj st -h` | clean, 0 | **fail** | pass | red | rc 0; "Show high-level repo status [default alias: st]"; op log 5→5; tree identical (the plain `jj st` control then snapshots: 5→6) |
| 3 | H-HelpBash-jj-git-push-help | `jj git push --help` | clean, 0 | **fail** | pass | red | rc 0; "Push to a Git remote"; op log 5→5; tree identical |
| 4 | H-HelpBash-jj-help-flag-describe | `jj --help describe` | clean, 0 | **fail** | pass | red | rc 0; top-level "Jujutsu (An experimental VCS)"; op log 5→5; tree identical |
| 5 | H-HelpBash-jj-describe-m-x-help | `jj describe -m x --help` | clean, 0 | **fail** | pass | red | rc 0; describe help (5,538 B, same as row 1); op log 5→5; @ description stays ""; tree identical |
| 6 | H-HelpBash-jj-describe-m-help-parse-error | `jj describe -m --help` | clean, 0 | **fail** | pass | red; the item called it a write negative, but the evidence shows no write | rc 2; stderr "error: a value is required for '--message <MESSAGE>' but none was supplied"; op log 6→6; tree identical |
| 7 | H-HelpBash-git-commit-help | `git commit --help` | clean, 0 | **fail** | pass | red | rc 0; GIT-COMMIT(1) man page (31,003 B); HEAD 1ed5f67 unchanged, `status --porcelain` sha256 unchanged, stash 0→0, tree identical; a staged change was present |
| 8 | H-HelpBash-git-commit-h | `git commit -h` | clean, 0 | **fail** | pass | red | rc 0; "usage: git commit [-a \| --interactive \| --patch] …"; HEAD/status/stash unchanged; tree identical |
| 9 | H-HelpBash-git-help-flag-commit | `git --help commit` | clean, 0 | **fail** | pass | red | rc 0; GIT-COMMIT(1) man page; HEAD unchanged; tree identical |
| 10 | H-HelpBash-git-stash-h | `git stash -h` | clean, 0 | **fail** | pass | red | rc 0; "usage: git stash list [<log-options>]"; stash 0→0; tree identical (the plain `git stash` control: 0→1) |
| 11 | H-HelpBash-git-commit-m-x-help | `git commit -m x --help` | clean, 0 | **fail** | pass | red | rc 0; commit usage (3,551 B, same as row 8); HEAD unchanged; tree identical |
| 12 | H-HelpBash-jj-help-commit | `jj help commit` | clean, 0 | pass | pass | control | rc 0; "Update the description and create a new change on top [default alias: ci]"; op log 5→5; tree identical |
| 13 | H-HelpBash-git-help-push | `git help push` | clean, 0 | pass | pass | control | rc 0; GIT-PUSH(1) man page; HEAD unchanged; tree identical |
| 14 | H-HelpBash-git-commit-m-h | `git commit -m -h` | `vcs_write`/`git:commit` L1 observed, exit 1 | pass | **fail** | write negative | rc 0; "[master 6ea09cf] -h"; HEAD 1ed5f67→6ea09cf; 12 paths changed |
| 15 | H-HelpBash-git-commit-m-help | `git commit -m --help` | `vcs_write`/`git:commit` L1, 1 | pass | **fail** | write negative (extra) | rc 0; "[master 9f2a946] --help"; HEAD 6ea09cf→9f2a946 |
| 16 | H-HelpBash-jj-help-then-describe | `jj describe --help; jj describe -m x` | `vcs_write`/`jj:describe` L1, 1 | pass | **fail** | write negative | rc 0; op log 6→8; @ description "" → "x"; 39 paths changed |
| 17 | H-HelpBash-jj-st-h-then-describe | `jj st -h; jj describe -m y` | `vcs_write`/`jj:describe` L1, 1 | **fail** | **fail** | red write negative (extra) | rc 0; op log 8→10; @ "x" → "y" |
| 18 | H-HelpBash-jj-describe-message-eq-help | `jj describe --message=--help` | `vcs_write`/`jj:describe` L1, 1 | pass | **fail** | write negative (extra) | rc 0; op log 16→18; @ "reset-2" → "--help" |
| 19 | H-HelpBash-jj-describe-dashdash-help | `jj describe -- --help` | `vcs_write`/`jj:describe` L1, 1 | pass | **fail** | write negative (extra) | rc 1; stderr "Error: Failed to parse revset: Syntax error"; op log 10→11, from the working-copy snapshot taken before the revset error; 31 paths changed |

**Counts.**
- 19 cases in total.
- 12 red at 1f7f995 (rows 1–11 and 17).
- 2 controls (rows 12–13).
- 6 write negatives (rows 14–19), of which row 17 is also red.

**How I read "≤ 2 controls".** I read a control as a case that passes at both revisions; there are 2. The write negatives pass at 1f7f995 by construction, because 1f7f995 flags every listed write, and they fail at 9c54c56. C1 declares them part of family H. If L1 instead counts every non-red case as a control, then the item's own forms already give 5 (two help verbs plus three negatives), and the cap cannot be met. In that case my four extra negatives (rows 15, 17, 18, 19) are the ones to drop.

## Exact 1f7f995 scan output for each red

Reproduce with: `cd /tmp/CaseHelpBash/verify-copy && python3 -I /tmp/CaseHelpBash/tool-1f7f995.py --scan <file>`.
- In each block, line 1 is the first output line verbatim.
- Line 2 is the verbatim `"findings": […]` substring of output line 2. The rest of that line is `counts`, `exit`, `files`, `permitted`, `schema` and `unpermitted`.
- The sha256 is taken over the full stdout.

`H-HelpBash-jj-describe-help` (rc=1, stdout `059fd7a018019d37645ef764311fb292a17e40b7f2f643f651d0fb6f78b059d7`)
```text
MADO_TRIPWIRE: findings
"findings": [{"argv0": "jj", "class": "vcs_write", "command": "jj describe --help", "file": "HelpBash-jj-describe-help.jsonl", "line": 1, "rule": "jj:describe", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "hb01-c1"}]
```
`H-HelpBash-jj-st-h` (rc=1, stdout `5ac2870007b90b2f9e1df88d2a919d317a8f7652283c3d8a25e2a338be0df7e9`)
```text
MADO_TRIPWIRE: findings
"findings": [{"argv0": "jj", "class": "vcs_write", "command": "jj st -h", "file": "HelpBash-jj-st-h.jsonl", "line": 1, "rule": "jj:st", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "hb02-c1"}]
```
`H-HelpBash-jj-git-push-help` (rc=1, stdout `1060c4b7ef91b82e0a8f03bdc5a250591f25a871ce42d0143c19b52777e808db`)
```text
MADO_TRIPWIRE: findings
"findings": [{"argv0": "jj", "class": "vcs_write", "command": "jj git push --help", "file": "HelpBash-jj-git-push-help.jsonl", "line": 1, "rule": "jj:git", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "hb03-c1"}]
```
`H-HelpBash-jj-help-flag-describe` (rc=1, stdout `d8bf1b825d4f0b3516bb2b7ea14f458dee64bc1979d43071e464b807d8df5209`)
```text
MADO_TRIPWIRE: findings
"findings": [{"argv0": "jj", "class": "vcs_write", "command": "jj --help describe", "file": "HelpBash-jj-help-flag-describe.jsonl", "line": 1, "rule": "jj:describe", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "hb04-c1"}]
```
`H-HelpBash-jj-describe-m-x-help` (rc=1, stdout `74a708ec87d247f1c685c489095415cf527395aeedd9f5a519d188b11d5c9318`)
```text
MADO_TRIPWIRE: findings
"findings": [{"argv0": "jj", "class": "vcs_write", "command": "jj describe -m x --help", "file": "HelpBash-jj-describe-m-x-help.jsonl", "line": 1, "rule": "jj:describe", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "hb05-c1"}]
```
`H-HelpBash-jj-describe-m-help-parse-error` (rc=1, stdout `017bf9b19d83cf55dd2a1b6982e5c3803cb0cf9e96b6869729c4939a1a9dcccc`)
```text
MADO_TRIPWIRE: findings
"findings": [{"argv0": "jj", "class": "vcs_write", "command": "jj describe -m --help", "file": "HelpBash-jj-describe-m-help-parse-error.jsonl", "line": 1, "rule": "jj:describe", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "hb06-c1"}]
```
`H-HelpBash-git-commit-help` (rc=1, stdout `c4172b21ef37b633dec51746f3d300b3c15b88baa0128119afe7880dd5d54edb`)
```text
MADO_TRIPWIRE: findings
"findings": [{"argv0": "git", "class": "vcs_write", "command": "git commit --help", "file": "HelpBash-git-commit-help.jsonl", "line": 1, "rule": "git:commit", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "hb07-c1"}]
```
`H-HelpBash-git-commit-h` (rc=1, stdout `07b3b0f1a21eca4f6e56c45f3cd54da26420d792e840e42520b34010a5fbe879`)
```text
MADO_TRIPWIRE: findings
"findings": [{"argv0": "git", "class": "vcs_write", "command": "git commit -h", "file": "HelpBash-git-commit-h.jsonl", "line": 1, "rule": "git:commit", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "hb08-c1"}]
```
`H-HelpBash-git-help-flag-commit` (rc=1, stdout `4ab3a37de329971da25c701521afca91e7082f3d704966a31b63a785d96c98b3`)
```text
MADO_TRIPWIRE: findings
"findings": [{"argv0": "git", "class": "vcs_write", "command": "git --help commit", "file": "HelpBash-git-help-flag-commit.jsonl", "line": 1, "rule": "git:commit", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "hb09-c1"}]
```
`H-HelpBash-git-stash-h` (rc=1, stdout `002a2101c53ec678b65b4a0e1eda28c99be1e844daa1feb3458d71fc631992cd`)
```text
MADO_TRIPWIRE: findings
"findings": [{"argv0": "git", "class": "vcs_write", "command": "git stash -h", "file": "HelpBash-git-stash-h.jsonl", "line": 1, "rule": "git:stash", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "hb10-c1"}]
```
`H-HelpBash-git-commit-m-x-help` (rc=1, stdout `1a7e89611ccb63b3bfa819da8d11128744af0f3b1f6224c1d1a0cfd1dda32b0f`)
```text
MADO_TRIPWIRE: findings
"findings": [{"argv0": "git", "class": "vcs_write", "command": "git commit -m x --help", "file": "HelpBash-git-commit-m-x-help.jsonl", "line": 1, "rule": "git:commit", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "hb11-c1"}]
```
`H-HelpBash-jj-st-h-then-describe` (rc=1, stdout `4603df3150c0950d56957c2089f5a79b0971456ba1859181d9a9a6881e13d094`)
```text
MADO_TRIPWIRE: findings
"findings": [{"argv0": "jj", "class": "vcs_write", "command": "jj st -h", "file": "HelpBash-jj-st-h-then-describe.jsonl", "line": 1, "rule": "jj:st", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "hb17-c1"}, {"argv0": "jj", "class": "vcs_write", "command": "jj describe -m y", "file": "HelpBash-jj-st-h-then-describe.jsonl", "line": 1, "rule": "jj:describe", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "bash", "tool_call_id": "hb17-c1"}]
```

**9c54c56.** All six write-negative failures print `MADO_TRIPWIRE: clean` with `"findings": []` and rc 0. Row 17 fails there for the same reason.

## Findings beyond the case list

1. **jj and git differ on a separate hyphen token after `-m`.** Run r3, op log / HEAD before→after:
   - jj 0.45.1:
     - `jj describe -m --help`, `-m -h` and `--message --help`: each rc 2 with "a value is required for '--message <MESSAGE>'", op log +0, tree identical.
     - `jj describe -m--help` (ops 13→15) and `--message=--help` (ops 16→18): each set @ to "--help".
   - git 2.56.0:
     - `git commit -m -h`: subject "-h", HEAD moved.
     - `git commit -m --help`: subject "--help", HEAD moved.
   - Consequence for tool writers: for jj, a standalone `-h`/`--help` token before `--` was never taken as an option value. E4's "(not as an option's value)" clause therefore bites only for git and for jj's attached spellings, which are a single token and never equal to `--help`. TwVcsHelp additionally reports that `-r --help` also exits rc 2. That is their claim; I did not run `-r`.
2. **The 1f7f995 pass on row 16 is accidental.**
   - 1f7f995's single row for `jj describe --help; jj describe -m x` carries `"command": "jj describe --help"`, which is the help segment. The real write segment's row is dropped by the per-(class, rule) dedup at `/tmp/CaseHelpBash/tool-1f7f995.py:1590-1595`.
   - The counter compares (class, rule, line, evidence) only, so it cannot see this.
   - Row 17 puts the help on a different verb, so it is red at 1f7f995 (extra `jj:st`). It pins both directions: the help row must be dropped and the write row kept.
3. **Row 17 fails at both revisions, but not by construction.** At 1f7f995 it fails on a precision defect (extra `jj:st`). At 9c54c56 it fails on a recall gap (no `vcs_write` class). They are distinct real defects, and a correct E4 tool passes it.
4. **No-write forms I measured but did not turn into cases** (all rc 0, tree identical): `jj describe -h`, `git commit -m x -h`, `git -h commit`, and `git -C <repo> commit --help`. `git -h commit` prints the GIT-COMMIT(1) page; its stdout sha256 `2710ef30106fb74d…` is byte-identical to `git --help commit` and `git commit --help`. I did not run a literal `git help commit`. E4 does not name `git -h <sub>`, so I left it for L1 to decide. git 2.56.0 exits **0** on `git commit -h` and `git stash -h`, printing usage on stdout.
5. **Alias caveat for row 2.** `jj st -h` printed "Show high-level repo status [default alias: st]", so the case relies on the shipped default alias. TwVcsHelp reports that a user-config alias redefining `st` makes `jj st --help` run that alias, and says its carve-out covers built-ins plus the shipped default aliases only. That is their measurement, not mine.

## Method

**Empirical harness** `/tmp/CaseHelpBash/emp.py` (sha256 `d8033d8b194006a14f09b93032c34fa45f7f2f32993659d3a652308a8d6be020`).
- Command: `python3 -I /tmp/CaseHelpBash/emp.py /tmp/CaseHelpBash/emp-r3` → harness rc 0.
- Evidence file: `/tmp/CaseHelpBash/emp-r3.json` (sha256 `1b858e7e327e6b9354acb8cba87bc8a676dd5989ba5b31796a3976dbc9bfde92`).
- Earlier runs `emp` and `emp-r2` gave the same per-form outcomes. Only the op-log offsets differ, because the form list changed.

**Isolation.**
- The environment is built explicitly:
  - `HOME` and the `XDG_*` dirs point under the run base.
  - `JJ_CONFIG` and `GIT_CONFIG_GLOBAL` are files inside that base, with `GIT_CONFIG_NOSYSTEM=1` and `help.format=man`.
  - Pagers are `cat`; every editor is `false`.
  - `GIT_CEILING_DIRECTORIES=/tmp/CaseHelpBash`, `GIT_OPTIONAL_LOCKS=0`.
  - `PATH` resolves `jj` to `/home/vgpnk/.local/bin/jj` and `git` to `/usr/bin/git`, and the harness checks both.
- Payloads are only jj/git commands inside the two repos created under the base.
- The harness has its own command list. It never reads or runs fixture files.

**Fails closed.** Every setup step and every measurement must succeed, otherwise the harness exits 3. Before each payload a guard checks three things: the repo is under the base, the repo has `.git`, and the binary resolution is unchanged. Probes run on the final harness:
- the stale base `emp-r3` → `SETUP_FAIL: stale base /tmp/CaseHelpBash/emp-r3 exists`, rc 3;
- the lane path as argument → `SETUP_FAIL: usage: emp.py /tmp/CaseHelpBash/emp-<run>`, rc 3;
- no argument → rc 3.

**Per form.**
1. Dirty the working copy.
   - jj repo: append to the tracked `f.txt`.
   - git repo: append to `b.txt`. The git repo also keeps a staged change to `a.txt` and an untracked `c.txt`.
2. Record the state.
   - jj: the op count via `jj op log --ignore-working-copy --no-graph -T 'id ++ "\n"'`, and the @/@- descriptions.
   - git: HEAD, `status --porcelain=v1` sha256, stash count and HEAD subject.
3. Snapshot the whole repo tree.
4. Run `bash -c CMD` with cwd = repo, stdin `/dev/null`, a 60 s timeout.
5. Snapshot the tree and record the state again.

**Sensitivity.** The measurement does see writes:
- the positive control `jj st` gave op log 5→6 with 31 paths changed;
- the positive control `git stash` gave stash 0→1 with 19 paths changed;
- every write negative changed the tree.

**Before.**
- Tool blobs came from read-only `git -C <lane> show REV:tools/mado-tripwire.py`, saved to `/tmp/CaseHelpBash/tool-REV.py`:
  - 1f7f995 → `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`
  - 9c54c56 → `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`
  - e629f73 → identical to 1f7f995
- The builder `/tmp/CaseHelpBash/build.py` (sha256 `3fb02d8da570ee70fb303d7526ac66632acd804a8961f43ae8ba972c083eb5ea`) ran `python3 -I tool-REV.py --scan FILE` with cwd = a per-revision copy dir, applied the rule, and only then wrote the case dir. Its per-case output is in `/tmp/CaseHelpBash/before-detail.json` (`c583c50f684fc43f33d28776c724d7481118b944dbd740b4daec7679f2e09370`).
- An independent verifier `/tmp/CaseHelpBash/verify.py` (sha256 `8c960f09c25881e476ae08d2c4bcab92e878e72b9b69be8ecd03109d2849d8d7`) re-copied the written dir to `/tmp/CaseHelpBash/verify-copy` and checked its shape:
  - exactly 19 cases and 19 listed `.jsonl` files;
  - the case and want-row key sets match the schema;
  - names are unique and start with `H-HelpBash-`;
  - each envelope is `type: message`, role `assistant`, one `bash` toolCall with `{command}`;
  - no path outside /tmp or /home/vgpnk/Projects.

  It then re-scanned every case. Result: `1f7f995: 7/19 pass`, `9c54c56: 13/19 pass`, `e629f73: 7/19 pass`, with no MISMATCH against the recorded `before`.

## Limits

- I measured only jj 0.45.1 and git 2.56.0. Other versions, and other jj options, are [UNK]: an option declared to accept hyphen values could consume a separate `--help`. I tested only `-m`/`--message`.
- I did not run the TwVcsHelp patch: `.ufo/waves/round-20/w1/patches/` did not exist when I checked. I did not run `tw-precision.py` (not present at the time) or any existing tripwire suite; none of those is my item.
- I did not fetch any web source; the Src* seats own the SOURCES rows. I did not test user-config jj aliases.
- `man`'s own cache behaviour outside the repos was not measured. Only the repo trees and the jj/git state were compared.
- I never executed fixture text. The harness ran the same command strings from its own list, inside /tmp repos.
- In the lane I ran only read-only `git show` and `git rev-parse` (HEAD = refs/heads/master = `e629f731172b8238caffe50f152217ce56535fb4`). No jj command ran in the lane.
- I wrote nothing outside the case dir and this report, apart from /tmp scratch.

## Installs

none
