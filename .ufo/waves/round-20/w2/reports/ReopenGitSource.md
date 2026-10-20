# ReopenGitSource — holds: S102's tag pin, six sha256s, the git.c:762 quote and every cited line reproduce at v2.56.0; the note and SKILL git-help claims hold for the tripwire's write-verb scope, with one over-broad note-table sentence for config aliases

Item: re-open SOURCES row S102 (`corpus/SOURCES.md:114`) and its Gate line
(`corpus/lessons/round-20.md:39`): fetch each pinned URL, compare sha256 with the
row and `.ufo/waves/round-20/fetch/*/receipts.jsonl`, check the quote verbatim at the
stated lines and ≤ 25 words, check the tag→commit pin with `git ls-remote`, and ask
whether the row supports what the knowledge note and SKILL say it supports.

Files opened (absolute):
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:114` (S102)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-20.md:39` (GATE S102)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/fetch/SrcGitHelpSource/receipts.jsonl`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/tripwire-precision-r20.md:1,45-46`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/SKILL.md:555-559`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` (committed tool, sha256 `9613f510…`)

Reproduction bytes: `.ufo/waves/round-20/w2/ReopenGitSource/fetch/` (six bodies +
`receipts.jsonl`, sha256 `027774b7aa5a65062a5966871ce340dd461bc69fbf76e041c94f299d19c29bc6`)
and `.ufo/waves/round-20/w2/ReopenGitSource/evidence.txt` (sha256
`53e1658b6a504e4d624c2c2ac9c3904e47806b7c12598e7078ee8769e52f584b`), which holds every
command excerpt below. Lane checkout touched read-only; experiments in `/tmp`.

## 1. Tag → commit pin — matches the row exactly

```
$ git ls-remote https://github.com/git/git refs/tags/v2.56.0 'refs/tags/v2.56.0^{}'
2478544319491bbd2a42cc57a83e3d2f4730a280	refs/tags/v2.56.0
a018953688f1b10bddf91bff8747068f5f4746a4	refs/tags/v2.56.0^{}
```
Row S102: "annotated object 2478544319491bbd2a42cc57a83e3d2f4730a280 → peeled commit
a018953688f1b10bddf91bff8747068f5f4746a4". Gate: same. Observed: both ids identical.

## 2. Fetches at tag `v2.56.0` — every sha256 matches row and receipt

`curl -sSL --max-time 60` on `https://raw.githubusercontent.com/git/git/v2.56.0/<path>`,
all HTTP 200, bodies under `.ufo/waves/round-20/w2/ReopenGitSource/fetch/`:

| file | bytes | sha256 (first 16) | row | receipt |
|---|---|---|---|---|
| `git.c` | 30,923 | `0e1bbafb1fa791d0` | `0e1bbafb…` ✓ | ✓ |
| `parse-options.c` | 42,814 | `8ff610bf58103a83` | `8ff610bf…` ✓ | ✓ |
| `parse-options.h` | 19,624 | `87e2be30e5463181` | (receipt only) ✓ | ✓ |
| `help.c` | 23,071 | `5c62ecb43cf09f02` | (receipt only) ✓ | ✓ |
| `builtin/help.c` | 20,408 | `8eb0ef101125861c` | `8eb0ef10…` ✓ | ✓ |
| `Documentation/gitcli.adoc` | 11,312 | `19829855b2982e1b` | `19829855…` ✓ | ✓ |

Stronger than a hash compare: the round-20 receipts were fetched at the **peeled
commit** URL, mine at the **tag** URL, and `cmp` reports `IDENTICAL` for all six —
so tag-resolved bytes equal commit-resolved bytes for every file in the row. The
receipts also carry one 404 (`Documentation/gitcli.txt`, 14 B); it is an abandoned
probe, not cited by the row, and does not affect the sixth file.
Gate says "per-file sha256 in the receipts" — the receipts hold all six, and every
one matches.

## 3. Quote — verbatim at the stated line; word count miscounted by one

`git.c:762` is exactly (repr):
```
'\t/* Turn "git cmd --help" into "git help --exclude-guides cmd" */'
```
The gate/row quote `Turn "git cmd --help" into "git help --exclude-guides cmd"` is
contained verbatim, once. Tokens: **9** (`Turn "git cmd --help" into "git help
--exclude-guides cmd"`), not the gate's "(8 words)". Still ≤ 25, so the policy check
passes; the count is the only numeric slip found. [OBS]

## 4. Every cited line range — content verified

| row claim | observed |
|---|---|
| git.c 762-770 rewrite | 762 comment; 763 `if (args->nr > 1 && !strcmp(args->v[1], "--help"))`; 766-770 replace + splice `--exclude-guides` ✓ |
| git.c 478-481 setup demote | 478 `help = argc == 2 && (!strcmp(argv[1], "-h") \|\| !strcmp(argv[1], "--help-all"));`; 480-481 demote to `RUN_SETUP_GENTLY` "to allow 'git cmd -h' outside repo" ✓ |
| git.c 973-974 top-level | 973 `else if (!strcmp("--help", argv[0]) \|\| !strcmp("-h", argv[0]))`; 974 `argv[0] = "help";` ✓ |
| parse-options.c 1049-1050 lone `-h` | 1049 comment, 1050 `if (internal_help && ctx->total == 1 && !strcmp(arg + 1, "h"))`, 1051 `goto show_usage;` — range ends one line before the `goto` (nit) |
| 1070 and 1089 mid-list `-h` | 1070-1071 and 1089-1090 `if (internal_help && *ctx->opt == 'h') goto show_usage;` ✓ |
| 1130-1131 `--help` | `if (internal_help && !strcmp(arg + 2, "help"))` → `goto show_usage;` ✓ |
| 1171-1173 stdout usage | `show_usage: return usage_with_options_internal(ctx, usagestr, options, USAGE_NORMAL, USAGE_TO_STDOUT);` ✓ |
| 1207-1211 exit 0 vs 129 | `PARSE_OPT_HELP: exit(0);` / `PARSE_OPT_HELP_ERROR: case PARSE_OPT_ERROR: exit(129);` ✓ |
| 1492-1497 `usage_with_options` exits 129 | `USAGE_TO_STDERR` then `exit(129)` ✓ |
| builtin/help.c 591-603 exclude-guides | 591-597 comment naming handle_builtin's rewrite; 599 `if (!exclude_guides \|\| alias[0] == '!')` → print alias, `exit(0)` ✓ |
| gitcli.adoc 129-148 `-h` contract | `-h::` "gives a pretty printed usage of the command", `git describe -h` sample, 145-148 "`git subcmd -h` without anything else … consistently give the usage" ✓ |

## 5. Behaviour on the host git 2.56.0 — the row's semantics hold

Host `git --version` → `git version 2.56.0` (equals the pin; `on-release` recheck is
satisfied). Home/git config redirected under `/tmp`, scratch repo in `/tmp`.

- **Rewrite**: `GIT_TRACE=1 git commit --help` → rc 0,
  `git.c:506 trace: built-in: git help commit --exclude-guides`; commit count 1 → 1.
  Same trace through a pre-option (`git -C repo commit --help`) and with trailing
  args (`git commit --help -- x` → `… --exclude-guides -- x`).
- **`-h` on every `GIT_WRITE` verb** (`add commit stash checkout switch reset pull
  push restore rebase merge cherry-pick`): all `rc=0`, usage on **stdout**
  (1,095–3,658 B), 0 B stderr, and `HEAD`+`git status --porcelain` unchanged
  (`STATE_UNCHANGED`). This is the row's "prints usage to stdout and exits 0".
- **Mid-list help**: clean-room, staged change before each — `git commit -m x --help`
  rc 0, commits 1 → 1, usage on stdout; `git commit --help` rc 0, commits 1 → 1.
- **`-h`/`--help` as an option value**: `git commit -m --help` → subject `--help`;
  `git commit -m -h` → subject `-h`. So the note's "the token is the message" row is
  right (my first attempt saw rc 1 only because the tree was clean — with a staged
  change the commit is written).
- **129 only for parse errors**: `git commit --badopt -h` → rc 129, usage on
  **stderr** (`error: unknown option 'badopt'`); `git commit -h --badopt` → rc 0,
  usage on stdout. Matches 1207-1211 / 1492-1497.
- **Demote**: `git commit -h` outside a repository → rc 0, 3,551 B stdout.
- **`git -h <sub>` = `git help <sub>`**: `git -h add` and `git help add` are
  byte-identical (19,314 B), rc 0 — both non-writes, as SKILL says.

Committed tool cross-check (`/tmp` clone at `a4046a8`, tool `9613f510…`), synthetic
one-line transcripts:

| transcript line | tool verdict | git's actual behaviour |
|---|---|---|
| `git commit --help` | clean | help builtin, rc 0 |
| `git commit -m x --help` | clean | usage, rc 0, no commit |
| `git commit -m --help` | `vcs_write`, rule `git:commit`, observed | commit, subject `--help` |
| `git commit -m -h` | `vcs_write`, rule `git:commit`, observed | commit, subject `-h` |
| `git -h commit` | clean | man page, rc 0 |
| `git commit --badopt -h` | clean | rc 129, no write |
| `git add -- --help` | `vcs_write`, rule `git:add` | `--help` is a pathspec after `--` (flags stop at `--`, git_option_flags:626) |

So the note's rows 45-46 and SKILL's "git `-h`/`--help` as a flag, `git help` …
not writes" are implemented as written for the verbs the tool classifies.

## 6. The one real counterexample: a config alias makes `-h` run the alias

Measured (git 2.56.0, `/tmp` canary):

```
$ git -c alias.x='!echo RAN > /tmp/r20reopen/canary' x --help
rc=0  canary=ABSENT  stdout="'x' is aliased to '!echo RAN > /tmp/r20reopen/canary'"
$ git -c alias.x='!echo RAN > /tmp/r20reopen/canary' x -h
rc=0  canary=PRESENT (content "RAN -h")
      stderr="'x' is aliased to '!echo RAN > /tmp/r20reopen/canary'"
```

Source, in the row's own pinned `git.c`: `handle_alias` prints the alias for a lone
`-h` (385-387) **without returning**, then runs the shell alias with `-h` appended
(388-409, `run_command`). `--help` never reaches `handle_alias`: `handle_builtin`
(763) rewrites it to `git help --exclude-guides x`, and `builtin/help.c:599-602`
prints the definition and exits 0. So:

- The note's table row `git <sub> … -h … | no — usage, exit 0`
  (`corpus/knowledge/tripwire-precision-r20.md:46`) is **over-broad as written**: for
  a config alias, `-h` runs the alias. The jj rows in the same table already carry
  exactly this caveat ("a user alias runs its command"); the git row does not.
- This is **not** a tool false negative reachable through S102's exemption: alias
  names are not `GIT_WRITE` verbs, so `classify_git` returns `None` before the help
  test (`tools/mado-tripwire.py:678-686`), and an alias named after a write verb
  cannot take effect — `git -c alias.commit='!…' commit -h` ran the builtin
  (canary2 ABSENT). `SKILL.md:562-563` already limits the clean verdict ("Still
  unanalysed: … shell aliases"), so SKILL stands; only the note sentence needs the
  qualifier the jj row has.

Verdict on the item's question: S102 supports what the knowledge note and SKILL use
it for — the `--help` rewrite, the parse-options `-h` stdout/exit-0 path, and
129-only-for-parse-errors — and all six pinned files, the quote and the tag pin
reproduce. The row's one-sentence summary is silent on config aliases, and the note
drops the qualifier; that is a documentation-scope defect, not a measurement error,
and it changes no tool verdict for the classified verb set.

## Limits

- Only the six files named by S102 were re-fetched; `builtin/*.c` was not read, so
  per-builtin `PARSE_OPT_NO_INTERNAL_HELP` use is not established from source — the
  twelve write verbs were measured on the host instead. [INFERENCE] that other
  builtins outside `GIT_WRITE` behave as `git grep -h` does not apply to the tool.
- The receipts' `fetched_at` fields were read but not independently re-established;
  the byte identity (`cmp`) between my tag fetch and their commit fetch is the
  anchor used here.
- The alias counterexample uses `-c alias.x=…` on the command line; the same code
  path is reached from `~/.gitconfig` (alias lookup is config, not command-line
  specific) — [INFERENCE] for the file-based config, [OBS] for `-c`.
- Other rows' claims (S099-S101, S103-S112) were not rechecked here.
- `git ls-remote` and `curl` are the only network calls; no pacman/sudo/service/
  compositor command was run. [UNK] whether earlier rounds opened these files at a
  different tag.

## Installs

none (curl 8.23.0 and git 2.56.0 already present).
