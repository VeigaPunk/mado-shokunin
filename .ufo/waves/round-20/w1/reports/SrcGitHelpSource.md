# SrcGitHelpSource — `git <sub> --help` is rewritten to `git help` before dispatch (exit 0); `-h` stays in parse-options (exit 0); 129 is the parse-error path, not help

Confidence: A for the source lines (raw files at tag v2.56.0, commit a0189536) and for host behavior (host `/usr/bin/git` reports `git version 2.56.0`, sha256 `2912a2a32f408c9b8122e476251b32f4b35f4c3f0c15961686ae87ca456d384c`, 4,968,112 B).

Source identity: annotated tag `refs/tags/v2.56.0` = tag object `2478544319491bbd2a42cc57a83e3d2f4730a280`, peeled commit `a018953688f1b10bddf91bff8747068f5f4746a4` (`git ls-remote https://github.com/git/git refs/tags/v2.56.0 'refs/tags/v2.56.0^{}'`). Raw files fetched from `https://raw.githubusercontent.com/git/git/a018953688f1b10bddf91bff8747068f5f4746a4/...`; receipts and bodies under `.ufo/waves/round-20/fetch/SrcGitHelpSource/`.

## Findings

### 1. `--help` as the first argument after the subcommand is rewritten before any subcommand lookup

`git.c:762-770` (handle_builtin):

> `/* Turn "git cmd --help" into "git help --exclude-guides cmd" */`
> `if (args->nr > 1 && !strcmp(args->v[1], "--help")) {`
> `... strvec_replace(args, 1, args->v[0]); strvec_replace(args, 0, "help"); cmd = "help"; ...`

The rewrite happens before `get_builtin(cmd)` (`git.c:773`), so the requested subcommand is never resolved or executed. handle_builtin is called from `run_argv()` (`git.c:869`) before `execv_dashed_external()` (`git.c:904-905`), so this also covers names that are not builtins, and it precedes ordinary alias expansion (alias handling is only reached after the builtin attempt, `git.c:907-915`).

Observed on host git 2.56.0 (scratch repo, `GIT_TRACE=1 git commit --help`):

```
16:44:58.693679 git.c:506               trace: built-in: git help commit --exclude-guides
exit=0, stdout begins GIT-COMMIT(1)                      Git Manual                     GIT-COMMIT(1)
```

Outside a repository `git commit --help` also exits 0 and prints the man page. The condition is strictly `args->v[1]`: a later `--help` is not rewritten (finding 4).

### 2. `-h` is not rewritten; it is the subcommand parser's internal help

`git.c:478-481` (run_builtin) special-cases only the lone `-h`/`--help-all` to allow help outside a repo:

> `help = argc == 2 && (!strcmp(argv[1], "-h") || !strcmp(argv[1], "--help-all"));`
> `if (help && (run_setup & RUN_SETUP))`
> `/* demote to GENTLY to allow 'git cmd -h' outside repo */`

`parse-options.c` then handles the flag itself:

- `parse-options.c:1049-1050`: `/* lone -h asks for help */` / `if (internal_help && ctx->total == 1 && !strcmp(arg + 1, "h")) goto show_usage;`
- `parse-options.c:1070` and `:1089`: an unmatched short `h` anywhere in the argument list still goes to `show_usage`.
- `parse-options.c:1171-1173`: `show_usage` prints `USAGE_NORMAL` to stdout.
- `parse-options.c:1207-1208`: `case PARSE_OPT_HELP: exit(0);`

Observed on host git 2.56.0, all exit 0 with usage on stdout: `git commit -h` (inside and outside a repo), `git commit -m x -h`, `git commit -h -m x`, `git status -h extra`, `git log -h`, `git -h`. `git -h` is the top-level pseudo-help (`git.c:171-172`, `git.c:973-974` maps `--help`/`-h` to the `help` command).

### 3. Exit 129 belongs to `usage_with_options`, the parser-error path

`parse-options.c:1492-1497`:

> `void NORETURN usage_with_options(...)`
> `{ usage_with_options_internal(NULL, usagestr, opts, USAGE_NORMAL, USAGE_TO_STDERR); exit(129); }`

Call sites that produce 129: `parse_options()` on `PARSE_OPT_HELP_ERROR`/`PARSE_OPT_ERROR` (`:1209-1211`); the unknown-option branch after printing `error("unknown option ...")` (`:1224-1233`); unknown subcommand (`:1036-1037`); `usage_msg_opt()` for invalid option combinations (`:1517-1523`). Normal help returns `PARSE_OPT_HELP` (`:1489`) and exits 0; only a failed print turns help into `PARSE_OPT_HELP_ERROR` (`:1376`, `:1489`).

Observed on host git 2.56.0: `git commit --badopt` → `error: unknown option 'badopt'` + usage on stderr, exit 129; `git help --badopt` → exit 129; `git help nonexistent-cmd` → `git: 'nonexistent-cmd' is not a git command. See 'git --help'.` on stderr, exit 1 (`help.c:660-662`).

### 4. A help token in value position is a value, not help

Observed on host git 2.56.0 in /tmp scratch repos:

- `git commit -m -h` with a staged change created a commit whose subject is `-h` (`[master 1d5f665] -h`, exit 0) — `-h` was consumed as the message.
- `git commit -m --help` with a staged change created a commit whose subject is `--help` (`[master 4b3e4c2] --help`, exit 0) — `--help` was consumed as the message, not as help.
- `git commit -m x --help` (help token at `argv[2]`, not `argv[1]`) was caught by parse-options (`:1130-1131`) and printed usage to stdout, exit 0. It never reaches `handle_builtin`'s rewrite.

Consequence for the tripwire: position/value role decides; `git <sub> --help` at `argv[1]` never runs the subcommand, while `-m --help`/`-m -h` are ordinary option values and the command can write.

### 5. `--help` on an alias: rewritten first, then the help command distinguishes `--exclude-guides`

`builtin/help.c:591-598` documents the coupling:

> `handle_builtin() in git.c rewrites "git cmd --help" to "git help --exclude-guides cmd", so we can use exclude_guides to distinguish "git cmd --help" from "git help cmd".`

Observed on host git 2.56.0 in a scratch repo:

- alias `foo = commit -m x`: `git foo --help` → stderr `'foo' is aliased to 'commit -m x'`, stdout is the `GIT-COMMIT(1)` man page, exit 0. The alias expansion's help is shown, not the alias run.
- `git help foo` → stdout `'foo' is aliased to 'commit -m x'`, exit 0, no man page.
- shell alias `bar = !echo hi`: `git bar --help` → stdout `'bar' is aliased to '!echo hi'`, exit 0; `hi` is not printed, so the shell alias body does not run.

### 6. Documented contract at the same tag

`Documentation/gitcli.adoc:129-130`:

> `-h::` / `gives a pretty printed usage of the command.`

`Documentation/gitcli.adoc:146-148`:

> `subcmd -h` without anything else on the command line is meant to consistently give the usage.

`Documentation/gitcli.adoc:150-153` documents `--help-all` as the full-option-list magic flag. In source, `--help-all` is not rewritten by handle_builtin; it is handled inside parse-options (`parse-options.c:1127-1129`, `USAGE_FULL`, stdout, exit 0) and is included in run_builtin's setup demotion (`git.c:478`).

## Evidence-vs-contract notes (reported, not edited)

1. The assignment's phrase pairing `git <sub> --help`/`-h` with "parse-options.c usage_with_options, exit 129" needs a correction on evidence: normal `--help` and `-h` exit 0. `usage_with_options` + 129 is the unknown-option/ambiguous/bad-usage path; `--help` at `argv[1]` does not even reach parse-options (it becomes the `help` builtin).
2. `git <sub> --help` can still exit 129 when extra arguments follow: `git commit --help --dry-run` → rewritten to `git help commit --exclude-guides --dry-run`; the help parser rejects `--dry-run` (`error: unknown option 'dry-run'`), exit 129 (observed). The subcommand still never runs, so exit 129 alone is not evidence of a write or of a failed help request.
3. E4's "not as an option's value" is confirmed for both spellings: `-m -h` committed with message `-h`; `-m --help` consumed `--help` as the message. `git commit -m x --help` (later position, not a value) does print usage and exits 0.
4. `--help-all` is not named in E4. Evidence: it is a real parse-options help flag (`USAGE_FULL`, stdout, exit 0), and a lone `--help-all` also demotes repository setup like `-h`.

## Drafted SOURCES row (11 columns; id left for L1)

| S1xx-pending | git v2.56.0 source — `git.c`, `parse-options.c`, `builtin/help.c`, `Documentation/gitcli.adoc` — https://github.com/git/git/tree/v2.56.0 | code | A | how `git <sub> --help` and `git <sub> -h` are handled before the subcommand runs: the `--help` rewrite into the help builtin, the parse-options `-h` usage path, and which failures exit 129 | tag v2.56.0 annotated object 2478544319491bbd2a42cc57a83e3d2f4730a280 → peeled commit a018953688f1b10bddf91bff8747068f5f4746a4 (`git ls-remote`); git.c 30,923 B sha256 `0e1bbafb1fa791d07a91e9e714adb1274e1247ce5d7b9bde46562f0d55494432`, lines 762-770 rewrite, 478-481 setup demote, 973-974 top-level; parse-options.c 42,814 B sha256 `8ff610bf58103a838a82b8fb82f5738fc198fc83190b9b38a36b962988e25bed`, lines 1049-1050 lone -h, 1070 and 1089 mid-list -h, 1130-1131 --help, 1171-1173 stdout usage, 1207-1211 exit 0 vs 129, 1492-1497 usage_with_options exits 129; builtin/help.c 20,408 B sha256 `8eb0ef101125861c9e59c986782cf55a09c3a9bc2c9e2db400e6843f2d4a5aa1`, lines 591-603 exclude-guides distinguishes `git cmd --help` from `git help cmd`; Documentation/gitcli.adoc 11,312 B sha256 `19829855b2982e1b59e75d08fce4ac4a096510a6fcd1735a1bef163d8bc6031d`, lines 129-148 -h contract | `git <sub> --help` is rewritten in handle_builtin to `git help --exclude-guides <sub>`, so the subcommand never runs (trace `built-in: git help commit --exclude-guides`, exit 0); `git <sub> -h` is not rewritten — the subcommand's parse-options prints usage to stdout and exits 0; `usage_with_options()` prints to stderr and exits 129 only for parse errors, not for help. Quote: "Turn \"git cmd --help\" into \"git help --exclude-guides cmd\"" (git.c:762) | queued | 2026-10-20 | on-release | .ufo/waves/round-20/w1/reports/SrcGitHelpSource.md (draft; L1 assigns id) |

## Fetch receipts

`.ufo/waves/round-20/fetch/SrcGitHelpSource/receipts.jsonl` (7 lines, all bodies present, each sha256 re-verified):

| body | http | bytes | sha256 |
|---|---|---|---|
| git.c | 200 | 30,923 | `0e1bbafb1fa791d07a91e9e714adb1274e1247ce5d7b9bde46562f0d55494432` |
| parse-options.c | 200 | 42,814 | `8ff610bf58103a838a82b8fb82f5738fc198fc83190b9b38a36b962988e25bed` |
| parse-options.h | 200 | 19,624 | `87e2be30e54631812165cf2e489116fe476e5edce7b92221dd1f4cdfa0e2d6d1` |
| help.c | 200 | 23,071 | `5c62ecb43cf09f02e84c667b8b6fc67b4b933899d0e832c9af10fdfc7c94cf09` |
| builtin-help.c | 200 | 20,408 | `8eb0ef101125861c9e59c986782cf55a09c3a9bc2c9e2db400e6843f2d4a5aa1` |
| Documentation-gitcli.adoc | 200 | 11,312 | `19829855b2982e1b59e75d08fce4ac4a096510a6fcd1735a1bef163d8bc6031d` |
| Documentation-gitcli.txt | 404 | 14 | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` |

`Documentation/gitcli.txt` is 404 at this tag (the doc is `.adoc`); the 404 attempt is kept as a receipt, the `.adoc` body is the one cited.

## Limits

- I did not build git from `a0189536`; source quotes are from the raw files at that commit. The host binary reports `git version 2.56.0` and matched every tested path, but I did not verify the distro binary was compiled from that exact commit [INFERENCE].
- I did not test `--help-all` empirically, nor help-format `-w`/`-i` viewers; only the man path was exercised.
- `usage_with_options_internal`'s write-failure branch (`HELP_ERROR` → 129) was read, not exercised.
- jj help handling is out of this item's scope and was not checked.
- No lane files were edited; the row above is a draft only.

## Installs

none.
