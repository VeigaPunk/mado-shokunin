# ScoutCorpusVcsNonWrites — 180 of 5,586 `vcs_write` rows at e629f73 are not writes; 72 are neither help nor dry-run

Corpus-wide enumeration (not a sample) of every `vcs_write` row the pre-registration
tool emits whose command is help, dry-run, or otherwise not a write, grouped by form,
plus the forms the round-20 target contract E4 does not cover. All counts are **emitted
rows** from `--scan` over every `*.jsonl` transcript; no fixture command was executed.

Headline: the 74 `jj … --help` rows `RerunPrecision` found are one form of a larger
family. At `e629f73` the corpus emits **180 non-write `vcs_write` rows** (170 historical,
10 in this wave's own probe transcripts). **102** are genuine help flags and **6** are
dry runs — both inside E4's stated scope. The remaining **72 are neither help nor
dry-run**: **70 `jj config list|get|path` rows** and **2 `jj root` rows**, each proven
read-only and snapshot-free from jj 0.38.0 source, and **not covered by E4 at all**.
The tool's own docstring justifies `jj:<sub>` on "jj snapshots the working copy on all
of them"; for these 72 rows that premise is false.

## 1. Provenance and method

| item | value |
|---|---|
| measured tool | `e629f73:tools/mado-tripwire.py`, sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`, 2,128 lines |
| same bytes as | `1f7f995:tools/mado-tripwire.py` (identical sha256); lane worktree `tools/mado-tripwire.py` also `367be947…` |
| pre-harm baseline | `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`, tool `c1ae45a7…`; its `CLASSES` has no `vcs_write` (`tool-base.py:61`), so every `vcs_write` row is new relative to the baseline by construction |
| lane state (read-only) | HEAD detached `e629f731172b8238caffe50f152217ce56535fb4` = `refs/heads/master` |
| corpus | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin`, 5,559 `*.jsonl` files |
| pre-scan manifest | `/tmp/scoutvcs/pre.sha` (5,559 lines), sha256 `f35815d9db1cf25ce992e3a1fe7a00fe3fbcb38d18b90266722360e22bbe97e1` |
| post-scan manifest | `/tmp/scoutvcs/post.sha`, sha256 `8c5795c3147595b93c05efb487db408c27801fb6e930747d04c66cdae0f40e8b` |
| drift during scan | 139 paths changed, 0 added, 0 removed; **5,420 byte-stable files** |
| scan | `python3 -I /tmp/scoutvcs/tool-629.py --scan /home/vgpnk/.omp/agent/sessions/-Projects-shokunin > /tmp/scoutvcs/scan629.out` |
| scan result | exit 1, 59.5 s, 4,993,780 B, sha256 `18f20ba19277357a514f76aabe23ba6e5c184d80c9e7d42e832f9a2ec8b495a8` |
| counts | 7,347 findings total; `vcs_write` 5,586; 5,561 with a stable rule; 5,425 of those on byte-stable files |

Row schema at this revision: `{argv0, class, command, file, line, rule, timestamp,
tool, tool_call_id}` — there is **no `evidence` key**, so under the round-20 comparison
rule every one of these rows counts as `observed`.

`scan_file` keeps at most **one row per `(class, rule)` per line**
(`tool-629.py:1590-1600`, `seen` set). Counts below are rows, not invocations; a line
that runs the same subcommand twice shows only the first. A same-line repeat is
invisible to any row-level enumeration, this one included (see Limits).

Text occurrences of a form in the corpus are not invocations: e.g. `git pull --dry-run`
appears 161 times as prose/fixture text and emits **0** rows; `jj log --version` appears
45 times as prose and emits **0** historical rows.

## 2. Enumeration by form

Summary of every row in the judged families (181 rows total, 180 of them
non-writes; the one write is the `-m --help` option-value row that E4 explicitly keeps):

| family | rows | historical | round-20 probe rows | E4 covers? |
|---|---|---|---|---|
| genuine help flag (`-h`/`--help`) | 102 | 94 | 8 | yes |
| dry run (`--dry-run`, `-n` on add/push) | 6 | 4 | 2 | yes (pull omitted from its list) |
| `jj config list\|get\|path` | 70 | 70 | 0 | **no** |
| `jj root` | 2 | 2 | 0 | **no** |
| `git commit -m --help` (message, a write) | 1 | 0 | 1 | E4 says keep |
| **non-write total** | **180** | **170** | **10** | |

Of the 170 historical non-write rows, 168 are on byte-stable files; the 2 exceptions are
`jj git init --help` and `jj edit --help` on
`…/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:53`, a file that changed during the
scan. The 10 probe rows live in `…/MadoR20/…` (this wave's own seats), which also drifted.

### 2.1 Help — 102 genuine rows (94 historical, 8 probe), all E4-covered

Rule totals, historical only (94 rows, 43 distinct command strings, 7 use `-h`, 87 use
`--help`; every one is `<jj|git> <write-sub> --help|-h`, never an option value):

| rule | rows | rule | rows | rule | rows |
|---|---|---|---|---|---|
| `jj:describe` | 22 | `jj:metaedit` | 8 | `jj:op` | 3 |
| `jj:git` | 18 | `jj:bookmark` | 6 | `jj:workspace` | 2 |
| `jj:commit` | 17 | `jj:rebase` | 4 | `jj:config` | 2 |
| `jj:squash` | 1 | `jj:util` | 3 | `jj:debug` | 3 |
| `jj:$c` | 1 | `jj:new` | 1 | `jj:st` | 1 |
| `jj:file` | 1 | `jj:edit` | 1 | | |

Representative exact strings (counts over all 104 flag rows): `~/.local/bin/jj describe
--help` 11, `jj describe --help` 10, `~/.local/bin/jj commit --help` 9,
`jj git init --help` 5, `jj commit --help` 5, `jj git push --help` 5,
`jj metaedit --help` 4, path-prefixed `jj git push --help` 2, `git commit -h` 2,
`git commit --help` 2, `git push -h` 1. No historical
`git <sub> --help` row exists; every git help row is a current-wave probe row. 39 of the
94 historical rows are on subcommands that are themselves reads (`bookmark list --help`,
`config path --help`, `op log --help`, …) — still help, still non-writes.

The 8 genuine probe help rows are `jj st --help`, `jj log --help` (`…/MadoR20/MadoR20.ScoutJjHelpEmpirical-3.jsonl:39`),
`jj git push --help` (`…/MadoR20.ScribeKnowledge-3.jsonl:36`), `git commit -h` ×2 and
`git push -h` (`…/MadoR20.ScribeKnowledge-3.jsonl:27`), `git commit -h` (`…/MadoR20.SrcGitHelpSource-3.jsonl:68`),
`git commit --help` ×2 (`…/MadoR20.SrcGitHelpSource-3.jsonl:75,82`). The remaining two
help-flag probe rows are option-value/dry-run rows, below.

### 2.2 Dry runs — 6 rows (4 historical, 2 probe)

| # | file:line | rule | command |
|---|---|---|---|
| 1 | `…/2026-10-19T20-36-43…/W2jProbeKengaku.jsonl:90` | `git:push` | `git push --dry-run` |
| 2 | `…/2026-10-20T12-57-31…/JjRevengerLaneJjState-2.jsonl:165` | `git:commit` | `git commit -a --dry-run --short` |
| 3 | same line | `git:add` | `git add -A --dry-run` |
| 4 | `…/SoujiR17-3/SoujiR17-3.RevengeStubOrigin.jsonl:32` | `git:add` | `git add --dry-run -n tests/vault/…/p6repo` |
| 5 | `…/MadoR20/MadoR20.ScribeKnowledge-3.jsonl:36` (probe) | `git:add` | `git add -n nf` |
| 6 | `…/MadoR20/MadoR20.SrcGitHelpSource-3.jsonl:75` (probe) | `git:commit` | `git commit --allow-empty -m --help --dry-run` |

Forms 1–4 are exactly RerunPrecision's four historical dry-run rows; the corpus grew by
two probe rows. No historical `jj git push --dry-run`, `git pull --dry-run`,
`git push -n`, or bare `git add -n` invocation exists.

### 2.3 `jj config list|get|path` — 70 rows, read-only and snapshot-free

All 70 on byte-stable files, none in the wave's probe tree. Rule `jj:config`.

| subcommand | form (trailing tokens) | rows |
|---|---|---|
| `list` | `--include-defaults` | 19 |
| `list` | `--repo` (incl. one `jj --no-pager config list --repo`) | 16 |
| `list` | none | 4 |
| `list` | `--repo --include-defaults=false` | 2 |
| `list` | `--user` | 2 |
| `list` | positional filter (`user`, `user.name user.email`, `--include-defaults snapshot`, `--repo revset-aliases."trunk()"`, `--include-defaults --repo`) | 6 |
| `get` | `<key>` (`user.name` 3, `snapshot.max-new-file-size` 3, `git_head` 2, `snapshot.auto-track` 2, `--repo snapshot.auto-track` 1) | 11 |
| `path` | `--repo` (incl. `--repo -R .`) 8, none 1, `--user` 1 | 10 |

Source proof that none of these writes or snapshots (jj v0.38.0, tag → commit
`2508982cde5c7e4db0933e0b6469f9e778e71e28`; fetched bodies in
`lane/.ufo/waves/round-20/fetch/ScoutCorpusVcsNonWrites/`):

- `cli/src/commands/config/list.rs:78-122` reads `command.settings().config()` only; the
  file contains **no** `workspace_helper`/`workspace_loader` call.
- `config/get.rs:45-64` reads `command.settings().get_value(&args.name)`; no workspace call.
- `config/path.rs:42-53` calls `args.level.config_paths(ui, command.config_env())` only.
- `config/mod.rs:81-108` — `config_paths(&self, ui, config_env: &ConfigEnv)` has no
  `CommandHelper`, so it structurally cannot snapshot; `--repo`/`--workspace` only
  resolve config-file paths through `ConfigEnv`.
- Contrast: `config/set.rs:102` *does* call `command.workspace_helper(ui)` (inside
  `check_wc_author`, for `user.name`/`user.email`), so `jj config set` rows (69) are
  writes and are correctly excluded here; `config/unset` (1) writes the config file.

### 2.4 `jj root` — 2 rows, read-only

| file:line | command | note |
|---|---|---|
| `…/JjDocAutoTrack-2.jsonl:109` | `jj root root` | mis-expansion of a `check root root` shell-function call, §2.5 |
| `…/JjDocWorktrees-2.jsonl:54` | `~/.local/bin/jj root` | literal |

`cli/src/commands/root.rs:35` uses `command.workspace_loader()`, not
`workspace_helper`; `cli/src/cli_util.rs:411-418` returns the loader without touching the
working copy, while `:430-452` documents and performs the snapshot in
`workspace_helper`. `jj workspace root` is likewise snapshot-free
(`cli/src/commands/workspace/root.rs:45` `workspace_helper_no_snapshot`, `:69` loader).

### 2.5 Shell-function expansion artifacts — 11 rows at one line (separate defect)

`tool-629.py` resolves shell functions defined in the same text and substitutes call
arguments for `$@`/`$1…` (`shell_functions`, `shell_expand`, `:616-702`), but does not
honour `shift`. `…/JjDocAutoTrack-2.jsonl:109` defines
`check() { local name=$1; shift; … jj "$@" … }` and calls `check <label> <cmd words>`;
the expansion keeps the label as a positional, producing 11 wrong commands:
`jj bookmarklist bookmark list`, `jj filelist file list`, `jj configlist config list`,
`jj oplog op log`, `jj root root`, `jj debugwc debug working-copy`,
`jj sparselist sparse list`, `jj wclist workspace list`, `jj taglist tag list`,
`jj operationlog operation log`, `jj utildbg util snapshot` (rules `jj:<label>`).
Two are reads even as intended (`config list`, `root`); the rest would be snapshot
writes if expanded correctly. They are reported separately, not added to the 180.

The same `shift` shape in `…/MadoR20/MadoR20.ScoutJjHelpEmpirical-3.jsonl:27,30,36`
(`run_form() { local label="$1"; shift; … jj "$@" … }` and a fixture-writer `b(name,
cmd)`) produces 25 further rows whose rule strings contain spaces, e.g. `vcs_write` rule
`jj:jj st --help` for command `jj jj st --help st --help`. The 18 unique commands are
`jj jj --help --help`, `jj jj --version --version`, `jj jj -V -V`,
`jj jj describe -h describe -h`, `jj jj describe -m --help describe -m --help`,
`jj jj git push --dry-run git push --dry-run`, `jj jj git push --help git push --help`,
`jj jj help git push help git push`, `jj jj help log help log`, `jj jj log --bogus log
--bogus`, `jj jj log --help log --help`, `jj jj st --help st --help`, `jj jj st -h st
-h`, `jj jj st (positive control) st`, `jj jj st --help again st --help`,
`jj jj log (POSITIVE) log -n`, `jj jj st (POSITIVE) st`, and `jj bad subcommand
boguscmd`. These are pre-expansion probe labels, not invocations; they are the
difference between 5,586 and 5,561 stable-rule rows and are excluded from every count
above (they are not a help/dry-run family).

## 3. E4 coverage map

E4 covers: `git <sub> -h|--help`, `git --help <sub>`, `jj … -h|--help` as a flag,
`jj help …`, and the dry-run shapes `git commit --dry-run`, `git add -n|--dry-run`,
`git push -n|--dry-run`, `jj git push --dry-run`. The tool currently violates every one
that occurs in the corpus: **102 genuine help rows** (all flag forms, none an option
value) and **6 dry-run rows**. `git help …` and `jj help …` are already clean
(`git:help`/`jj:help` are not write subs), and `git stash list|show` is already
carved out (`classify_git`, `tool-629.py:524-529`).

**New non-write forms E4 does not cover:**

1. **`jj config list|get|path` — 70 rows.** E4 is silent; the class premise ("jj
   snapshots … on all of them") is false for these subcommands (§2.3). This is the
   largest new defect and is independent of the help-flag bug.
2. **`jj root` — 2 rows.** No snapshot (`workspace_loader`), no write.
3. **`jj <sub> --version` (flag after a write sub).** Probe 6: `jj log --version` emits
   `vcs_write/jj:log`. The docstring says "`help` and `--version` excepted" but the code
   excepts only the *verbs* (`JJ_NO_SNAPSHOT = {"help","version"}`, `:133`), and
   `first_verb` skips leading flags only (`:462-474`). 0 historical rows; `jj --version`
   itself is clean (probe 5). [INFERENCE] clap rejects the flag before dispatch, so no
   working-copy load.
4. **`jj util completion`, `jj util config-schema`, `jj util markdown-help`.** Probes 38
   and 39 emit `vcs_write/jj:util`; source shows no workspace use
   (`util/completion.rs` builds the clap app; `util/config_schema.rs` and
   `util/markdown_help.rs` contain no `workspace_helper`/`workspace_loader`). 0 corpus
   rows.
5. **`jj workspace root`.** Snapshot-free by source (`workspace/root.rs:45,69`); 0
   corpus rows.
6. **`jj debug <read-only>` family.** Not adjudicated individually. The only `debug`
   rows in the corpus are `jj debug watchman status` ×3 (workspace_helper at
   `debug/watchman.rs:52` → snapshots; true positive) and `jj debug reindex` ×3
   (`debug/reindex.rs` calls `load_workspace()` and rebuilds the index — a repo write,
   no working-copy snapshot; true positive under the class name, wording mismatch under
   the docstring). [UNK] for other debug subcommands.

Not new (the brief's examples): `git stash list` emits **no** row (probe 12; also
`git stash show`, `git stash list -p` clean; the five `git:stash` rows are stash pushes:
`git stash -u -- …`, `git stash --include-untracked -m jjprobe`, `git stash -q` ×3);
`jj --version` emits **no** row (probe 5; also `jj --help`, `jj -V`, `jj help log`);
`git push --porcelain -n` **does** emit `vcs_write/git:push` (probe 20) and is a dry run
covered by E4's `git push -n` rule — no corpus row; `git push --porcelain` alone is a
write and has no corpus row either.

## 4. Traps in the other direction — writes a naive fix would clear

These are writes (or erroring commands) that a help/dry-run implementation can wrongly
suppress. None has a historical corpus row; all were probed against the tool; `-n`
meanings are from `git <sub> -h` on git 2.56.0 (read-only help output):

| form | truth | tool today | E4 |
|---|---|---|---|
| `git commit -n` | `-n` = `--no-verify`; commits | `git:commit` (correct) | named as still-writes |
| `git pull -n` | `-n` = no diffstat; pulls and merges | not in corpus or probe | **unnamed** |
| `git merge -n` | `-n` = no diffstat; merges | not in corpus or probe | **unnamed** |
| `git rebase -n` | `-n` = `--no-stat`; rebases | `git:rebase` (correct) | **unnamed** |
| `git cherry-pick -n` | `-n` = `--no-commit`; applies to index/worktree | `git:cherry-pick` (correct) | **unnamed** |
| `git add -N` | `--intent-to-add`; index write | `git:add` (correct) | unnamed |
| `git commit -m --help` | message is the literal `--help`; commits | `git:commit` (correct) | named (`-m --help`) |
| `jj describe -m "--help"` | message value; describes | `jj:describe` (correct) | named (`-m --help`) |
| `--no-dry-run`, `--dry-run=false` | negation; performs the write | not present in corpus | unnamed |
| `git add -An` | short cluster = `-A -n` = dry run | not present in corpus | unnamed (clusters) |
| `git commit -an` | cluster = `-a -n` = no-verify; commits | not present in corpus | unnamed (clusters) |

Observed probe instances of the `-m --help` option-value form are only current-wave rows:
`git commit -m --help` (`…/MadoR20.ScoutJjHelpEmpirical-3.jsonl:39`) and
`git commit --allow-empty -m --help --dry-run`
(`…/MadoR20.SrcGitHelpSource-3.jsonl:75`). Any fix that suppresses on the presence of a
`--help` token anywhere in argv would wrongly clear the first (a real commit) and would
also be wrong for `-m --help --dry-run` if it ignored the dry-run flag.

## 5. Empirical tool matrix (44 probes, `--scan` only; no command executed)

Fixture: `/tmp/scoutvcs/probe.jsonl` (one bash `toolCall` per line), scan output
`/tmp/scoutvcs/probe629.out` (sha256 `0f4ad30f…`), exit 1. Selected results
(`line → emitted row`); every command below was parsed as text only:

- clean: `jj help log`, `jj --help`, `jj --version`, `jj -V`, `git help commit`,
  `git stash list`, `git stash show`, `git stash list -p`, `git stash list --help`
- emitted, help: `jj log --help` → `jj:log`; `jj commit -h` → `jj:commit`;
  `git commit --help` → `git:commit`; `git --help commit` → `git:commit`;
  `git stash --help` → `git:stash`; `jj config path --help|-h` → `jj:config`
- emitted, help flag after a write sub and *not* help: `jj log --version` → `jj:log`
- emitted, dry run: `git commit --dry-run`, `git add -n|--dry-run`,
  `git push -n|--porcelain -n|--porcelain --dry-run`, `git pull --dry-run`,
  `git commit -m x --dry-run`
- emitted, write (correct): `git add -N`, `git commit -n`, `git rebase -n`,
  `git cherry-pick -n`, `git commit -m --help`, `git merge --dry-run` (invalid option;
  errors before any write)
- emitted, `jj` reads: `jj config list|get|path` → `jj:config`; `jj op log` → `jj:op`;
  `jj file list` → `jj:file`; `jj bookmark list` → `jj:bookmark`; `jj status` →
  `jj:status`; `jj root` → `jj:root`; `jj util gc`/`util completion`/`util
  config-schema` → `jj:util`; `jj debug reindex` → `jj:debug`; `jj git colocation
  status` → `jj:git`; `jj log -r @` → `jj:log`

Of those `jj` reads, only `config list|get|path` and `root` (and the latent `util`
forms/`workspace root`) are non-writes; the rest call `workspace_helper` and snapshot
(`operation/log.rs:102`, `file/list.rs:63`, `file/show.rs:85`, `file/annotate.rs:74`,
`bookmark/list.rs:129`, `status.rs:66`, `log.rs:136`, `diff.rs:121`, `show.rs:72`,
`evolog.rs:107`, `tag/list.rs:124`, `workspace/list.rs:51`, `sparse/list.rs:38`,
`util/gc.rs:59`, `debug/watchman.rs:52`, `git/colocation.rs:97`), or write the index
(`debug/reindex.rs`).

## 6. Ground truth used

- Installed client: `/home/vgpnk/.local/bin/jj`, sha256
  `cd5efc3eb281d606bf9b5523167f79661da0f8c76a5aa32d61c07c7a351b6b44`, version string
  `jj 0.38.0` read from the file bytes (no `jj` command was run; the lane bans all jj
  invocations).
- Source: GitHub `jj-vcs/jj` tag `v0.38.0` → commit
  `2508982cde5c7e4db0933e0b6469f9e778e71e28` (`git ls-remote`, lightweight tag — no
  `^{}` line); all quotes are from raw bodies at that commit saved under
  `lane/.ufo/waves/round-20/fetch/ScoutCorpusVcsNonWrites/` with 50 receipts
  (`receipts.jsonl` sha256 `ab565293f0584ba62ed30581807196f2f55f10bd8d5f2552fb5e4db17106a2d7`;
  41 × HTTP 200, 9 × HTTP 404 navigation attempts; e.g. `cli_src_commands_config_list.rs`
  sha256 `14fca24a7d1025fee670be56eb545ad053c062d84624016939a4751adb4498c6`,
  `cli_src_cli_util.rs` sha256 `1aac0dfcf00d18be609bb583ea91c1529734de7f32a94e81d8f90f9555125b9f`).
- git: version 2.56.0; flag meanings from `git <sub> -h` output (read-only).

No SOURCES row was drafted: this seat adds no new host/source fact requiring an S-id,
only tool-behaviour evidence and a pinned upstream source check (receipts above).

## Appendix — every judged row (181 rows; 180 non-writes)

`schema: verdict | file:line | rule | command`. Paths are relative to the corpus root
`/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/` (`…/` is elided there); commands
are whitespace-collapsed and truncated at 110 chars.

| dry-run | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKengaku.jsonl:90` | `git:push` | `git push --dry-run` |
| dry-run | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjRevengerLaneJjState-2.jsonl:165` | `git:commit` | `git commit -a --dry-run --short` |
| dry-run | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjRevengerLaneJjState-2.jsonl:165` | `git:add` | `git add -A --dry-run` |
| dry-run | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScribeKnowledge-3.jsonl:36` | `git:add` | `git add -n nf` |
| dry-run | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.SrcGitHelpSource-3.jsonl:75` | `git:commit` | `git commit --allow-empty -m --help --dry-run` |
| dry-run | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/SoujiR17-3/SoujiR17-3.RevengeStubOrigin.jsonl:32` | `git:add` | `git add --dry-run -n tests/vault/vadv54-run/p/p6repo` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99.jsonl:1713` | `jj:git` | `jj git init --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jConnectProtocol.jsonl:161` | `jj:describe` | `~/.local/bin/jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jConnectProtocol.jsonl:164` | `jj:describe` | `~/.local/bin/jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jConnectProtocol.jsonl:164` | `jj:commit` | `~/.local/bin/jj commit --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:80` | `jj:commit` | `jj commit -h` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:83` | `jj:commit` | `jj commit -h` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:86` | `jj:commit` | `jj commit --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:86` | `jj:describe` | `jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:89` | `jj:describe` | `jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:89` | `jj:squash` | `jj squash --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:92` | `jj:describe` | `jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:95` | `jj:describe` | `jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:98` | `jj:metaedit` | `jj metaedit --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeChousa.jsonl:69` | `jj:commit` | `~/.local/bin/jj commit --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeChousa.jsonl:72` | `jj:describe` | `~/.local/bin/jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeChousa.jsonl:72` | `jj:metaedit` | `~/.local/bin/jj metaedit --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeFleetRoot.jsonl:61` | `jj:git` | `jj git init --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeFleetRoot.jsonl:61` | `jj:describe` | `jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeFleetRoot.jsonl:61` | `jj:metaedit` | `jj metaedit --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:74` | `jj:describe` | `~/.local/bin/jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:77` | `jj:$c` | `~/.local/bin/jj $c --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:80` | `jj:describe` | `~/.local/bin/jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:80` | `jj:commit` | `~/.local/bin/jj commit --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:83` | `jj:describe` | `~/.local/bin/jj describe -h` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:83` | `jj:commit` | `~/.local/bin/jj commit -h` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:86` | `jj:metaedit` | `~/.local/bin/jj metaedit -h` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKaidoku.jsonl:95` | `jj:describe` | `~/.local/bin/jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKaidoku.jsonl:95` | `jj:commit` | `~/.local/bin/jj commit --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKaidoku.jsonl:98` | `jj:describe` | `~/.local/bin/jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKaidoku.jsonl:98` | `jj:commit` | `~/.local/bin/jj commit --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKaidoku.jsonl:101` | `jj:describe` | `~/.local/bin/jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKaidoku.jsonl:104` | `jj:describe` | `~/.local/bin/jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKaidoku.jsonl:104` | `jj:new` | `~/.local/bin/jj new --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKake.jsonl:84` | `jj:commit` | `~/.local/bin/jj commit --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKake.jsonl:84` | `jj:describe` | `~/.local/bin/jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeMado.jsonl:55` | `jj:commit` | `~/.local/bin/jj commit --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeMado.jsonl:55` | `jj:describe` | `~/.local/bin/jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeMado.jsonl:58` | `jj:commit` | `~/.local/bin/jj commit --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTabi.jsonl:83` | `jj:describe` | `jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTabi.jsonl:86` | `jj:describe` | `jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTabi.jsonl:89` | `jj:describe` | `jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTabi.jsonl:93` | `jj:describe` | `jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTabi.jsonl:93` | `jj:metaedit` | `jj metaedit --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTsukuroi.jsonl:68` | `jj:describe` | `jj describe --help` |
| non-write (help) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTsukuroi.jsonl:68` | `jj:commit` | `jj commit --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjAuditKasegi-2.jsonl:76` | `jj:util` | `~/.local/bin/jj util gc --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjAuditPromptText-2.jsonl:131` | `jj:git` | `jj git push --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjAuditPromptText-2.jsonl:135` | `jj:git` | `jj git push --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjCriticRollback-2.jsonl:98` | `jj:git` | `~/.local/bin/jj git colocation --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocConcurrency-2.jsonl:226` | `jj:bookmark` | `jj bookmark list --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocHeadAttachment-2.jsonl:115` | `jj:git` | `~/.local/bin/jj git colocation status --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocIdentity-2.jsonl:126` | `jj:git` | `jj git push --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocImmutable-2.jsonl:43` | `jj:rebase` | `~/.local/bin/jj rebase --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocImmutable-2.jsonl:68` | `jj:rebase` | `~/.local/bin/jj rebase --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocImmutable-2.jsonl:87` | `jj:git` | `~/.local/bin/jj git push --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocLargeRepo-2.jsonl:34` | `jj:debug` | `/home/vgpnk/.local/bin/jj debug --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocLargeRepo-2.jsonl:49` | `jj:util` | `/home/vgpnk/.local/bin/jj util snapshot --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocLargeRepo-2.jsonl:49` | `jj:debug` | `/home/vgpnk/.local/bin/jj debug watchman --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocLargeRepo-2.jsonl:141` | `jj:st` | `/home/vgpnk/.local/bin/jj st --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocOpLogGrowth-2.jsonl:14` | `jj:util` | `jj util gc --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocOpLogGrowth-2.jsonl:14` | `jj:op` | `jj op abandon --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocOpLogGrowth-2.jsonl:14` | `jj:op` | `jj op --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocOpLogGrowth-2.jsonl:105` | `jj:debug` | `jj debug reindex --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocOpLogGrowth-2.jsonl:116` | `jj:git` | `jj git push --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocPush-2.jsonl:49` | `jj:git` | `~/.local/bin/jj git push -h` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocRecovery-2.jsonl:313` | `jj:bookmark` | `~/.local/bin/jj bookmark set --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocWorktrees-2.jsonl:19` | `jj:workspace` | `~/.local/bin/jj workspace --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocWorktrees-2.jsonl:24` | `jj:workspace` | `~/.local/bin/jj workspace add --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocWorktrees-2.jsonl:24` | `jj:git` | `~/.local/bin/jj git init --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:39` | `jj:git` | `~/.local/bin/jj git init --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:39` | `jj:commit` | `~/.local/bin/jj commit --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:39` | `jj:rebase` | `~/.local/bin/jj rebase --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:44` | `jj:file` | `~/.local/bin/jj file track --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:44` | `jj:git` | `~/.local/bin/jj git push --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:44` | `jj:bookmark` | `~/.local/bin/jj bookmark set --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:65` | `jj:metaedit` | `~/.local/bin/jj metaedit --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:68` | `jj:metaedit` | `~/.local/bin/jj metaedit --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjRevengerLaneJjState-2.jsonl:34` | `jj:op` | `jj op log --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/KaidokuR18.ScoutJjColocation.jsonl:63` | `jj:git` | `/home/vgpnk/.local/bin/jj git colocation --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/KaidokuR18.ScoutJjColocation.jsonl:84` | `jj:git` | `/home/vgpnk/.local/bin/jj git colocation --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScoutJjHelpEmpirical-3.jsonl:39` | `jj:st` | `jj st --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScoutJjHelpEmpirical-3.jsonl:39` | `jj:log` | `jj log --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScribeKnowledge-3.jsonl:27` | `git:commit` | `git commit -h` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScribeKnowledge-3.jsonl:27` | `git:push` | `git push -h` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScribeKnowledge-3.jsonl:36` | `jj:git` | `jj git push --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.SrcGitHelpSource-3.jsonl:68` | `git:commit` | `git commit -h` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.SrcGitHelpSource-3.jsonl:75` | `git:commit` | `git commit --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.SrcGitHelpSource-3.jsonl:82` | `git:commit` | `git commit --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.HelperFailureWindows-5.jsonl:55` | `jj:bookmark` | `jj bookmark set --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.HelperFailureWindows-5.jsonl:55` | `jj:rebase` | `jj rebase --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.HelperFailureWindows-5.jsonl:55` | `jj:commit` | `jj commit --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.HelperFailureWindows-5.jsonl:58` | `jj:bookmark` | `jj bookmark set --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.JjEnvFacts-5.jsonl:13` | `jj:config` | `~/.local/bin/jj config path --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.JjEnvFacts-5.jsonl:20` | `jj:config` | `~/.local/bin/jj config path -h` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.SrcJjMetaedit-5.jsonl:28` | `jj:commit` | `jj commit --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.SrcJjMetaedit-5.jsonl:28` | `jj:metaedit` | `jj metaedit --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.C03FleetJjPractice.jsonl:80` | `jj:git` | `jj git init --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X03DefectProbes.jsonl:52` | `jj:git` | `jj git init --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X03DefectProbes.jsonl:61` | `jj:bookmark` | `jj bookmark --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X03DefectProbes.jsonl:61` | `jj:commit` | `jj commit --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:53` | `jj:git` | `jj git init --help` |
| non-write (help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:53` | `jj:edit` | `jj edit --help` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jConnectProtocol.jsonl:179` | `jj:config` | `~/.local/bin/jj config list --user` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:80` | `jj:config` | `jj config list user.name user.email` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeChousa.jsonl:48` | `jj:config` | `~/.local/bin/jj config list` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeChousa.jsonl:69` | `jj:config` | `~/.local/bin/jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeChousa.jsonl:85` | `jj:config` | `~/.local/bin/jj config list --repo` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeChousa.jsonl:88` | `jj:config` | `~/.local/bin/jj config path --repo` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:71` | `jj:config` | `~/.local/bin/jj config list user` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:86` | `jj:config` | `~/.local/bin/jj config path --repo` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:102` | `jj:config` | `~/.local/bin/jj config list --include-defaults snapshot` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKake.jsonl:68` | `jj:config` | `~/.local/bin/jj config list` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKake.jsonl:71` | `jj:config` | `~/.local/bin/jj config list` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKake.jsonl:77` | `jj:config` | `~/.local/bin/jj config path --repo` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKake.jsonl:102` | `jj:config` | `~/.local/bin/jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKama.jsonl:74` | `jj:config` | `jj config get user.name` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKama.jsonl:81` | `jj:config` | `jj config list --repo` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKimiShokunin.jsonl:63` | `jj:config` | `jj config get snapshot.max-new-file-size` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKumitate.jsonl:94` | `jj:config` | `jj config list` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeLore.jsonl:82` | `jj:config` | `jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeMado.jsonl:52` | `jj:config` | `~/.local/bin/jj config list user` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeMori.jsonl:80` | `jj:config` | `~/.local/bin/jj config get user.name` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeMori.jsonl:102` | `jj:config` | `~/.local/bin/jj config get snapshot.max-new-file-size` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTameshi.jsonl:85` | `jj:config` | `~/.local/bin/jj config get snapshot.max-new-file-size` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTsukuroi.jsonl:68` | `jj:config` | `jj config get user.name` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jSentinel.jsonl:18` | `jj:config` | `~/.local/bin/jj config get snapshot.auto-track` |
| non-write (jj config read) | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jSentinel.jsonl:23` | `jj:config` | `~/.local/bin/jj config list --user` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07.jsonl:218` | `jj:config` | `jj --no-pager config list --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjAuditKake-2.jsonl:124` | `jj:config` | `~/.local/bin/jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjAuditMado-2.jsonl:139` | `jj:config` | `jj config list --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjAuditTameshi-2.jsonl:133` | `jj:config` | `~/.local/bin/jj config list --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjAuditTameshi-2.jsonl:141` | `jj:config` | `~/.local/bin/jj config list --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjAuditTameshi-2.jsonl:152` | `jj:config` | `~/.local/bin/jj config path --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjAuditTsukuroi-2.jsonl:90` | `jj:config` | `~/.local/bin/jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjAuditTsukuroi-2.jsonl:95` | `jj:config` | `~/.local/bin/jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjCriticRollback-2.jsonl:46` | `jj:config` | `~/.local/bin/jj config path --user` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocAutoTrack-2.jsonl:196` | `jj:config` | `jj config get snapshot.auto-track` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocHooksAttributes-2.jsonl:19` | `jj:config` | `jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocHooksAttributes-2.jsonl:24` | `jj:config` | `jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocHooksAttributes-2.jsonl:29` | `jj:config` | `jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocHooksAttributes-2.jsonl:85` | `jj:config` | `jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocHooksAttributes-2.jsonl:103` | `jj:config` | `jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocIdentity-2.jsonl:32` | `jj:config` | `jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocIdentity-2.jsonl:32` | `jj:config` | `jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocImmutable-2.jsonl:106` | `jj:config` | `~/.local/bin/jj config path --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjRevengerLaneJjState-2.jsonl:24` | `jj:config` | `jj config path` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjRevengerPriorProbe-2.jsonl:53` | `jj:config` | `jj config list --repo --include-defaults=false` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjRevengerPriorProbe-2.jsonl:53` | `jj:config` | `jj config list --repo --include-defaults=false` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjRevengerPriorProbe-2.jsonl:59` | `jj:config` | `jj config list --include-defaults --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjRevengerPriorProbe-2.jsonl:76` | `jj:config` | `jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjRevengerPriorProbe-2.jsonl:120` | `jj:config` | `jj config path --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjTrialChousa-2.jsonl:40` | `jj:config` | `jj config list --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjTrialKagi-2.jsonl:43` | `jj:config` | `jj config list --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjTrialKake-2.jsonl:44` | `jj:config` | `jj config list --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjTrialKama-2.jsonl:43` | `jj:config` | `jj config list --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjTrialKasegi-2.jsonl:56` | `jj:config` | `jj config list --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjTrialKengaku-2.jsonl:52` | `jj:config` | `jj config list --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjTrialKengaku-2.jsonl:55` | `jj:config` | `jj config list --repo revset-aliases."trunk()"` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjTrialKotoba-2.jsonl:64` | `jj:config` | `~/.local/bin/jj config list --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjTrialKotoba-2.jsonl:75` | `jj:config` | `~/.local/bin/jj config path --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjTrialKotodama-2.jsonl:52` | `jj:config` | `jj config list --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjTrialKumitate-2.jsonl:33` | `jj:config` | `jj config list --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/KaidokuR18.ScoutJjRevsetsTrunk.jsonl:26` | `jj:config` | `jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/KaidokuR18.ScoutJjRevsetsTrunk.jsonl:57` | `jj:config` | `jj config list --repo` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/KaidokuR18.ScoutJjRevsetsTrunk.jsonl:103` | `jj:config` | `jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.SentinelJjSandbox-5.jsonl:31` | `jj:config` | `jj config path --repo -R .` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TabiR17/TabiR17.RevF3Repro-2.jsonl:44` | `jj:config` | `/home/vgpnk/.local/bin/jj config get --repo snapshot.auto-track` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR17/TameshiR17.HeadSweepRecheck-2.jsonl:39` | `jj:config` | `jj config get git_head` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR17/TameshiR17.HeadSweepRecheck-2.jsonl:44` | `jj:config` | `jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR17/TameshiR17.HeadSweepRecheck-2.jsonl:49` | `jj:config` | `jj config get git_head` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR17/TameshiR17.HeadSweepRecheck-2.jsonl:54` | `jj:config` | `jj config list --include-defaults` |
| non-write (jj config read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR17/TameshiR17.HeadSweepRecheck-2.jsonl:57` | `jj:config` | `jj config list --include-defaults` |
| non-write (jj root read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocAutoTrack-2.jsonl:109` | `jj:root` | `jj root root` |
| non-write (jj root read) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocWorktrees-2.jsonl:54` | `jj:root` | `~/.local/bin/jj root` |
| write (option value --help) | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScoutJjHelpEmpirical-3.jsonl:39` | `git:commit` | `git commit -m --help` |

## Limits

- **Rows, not invocations.** `scan_file` dedupes per `(class, rule)` per line
  (`tool-629.py:1590-1600`). A line that runs `jj log --help` and later `jj log` in the
  same text keeps only the first row for `jj:log`; same-line repeats of one rule are
  invisible to this enumeration. Example: `…/JjAuditPromptText-2.jsonl:131` contains
  several `--help` mentions in its command text and emits a single `jj:git` row.
- **Live corpus.** 139 of 5,559 transcripts changed during the scan (0 added, 0 removed);
  5,420 were byte-stable. 5,425 of 5,561 stable-rule rows and 168 of the 170 historical
  non-write rows are on stable files; the two exceptions are the help rows on
  `…/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:53`. The 10 current-wave probe rows
  are in `…/MadoR20/…` files that also drifted; they are this wave's own probes, not
  historical usage.
- **Semantics are source-level, not execution.** No `jj` command was run (lane ban);
  `jj` 0.38.0 snapshot behaviour comes from the pinned source tree. `jj <sub> --version`
  being snapshot-free is [INFERENCE] from clap parse-before-dispatch, supported by the
  tool's own docstring ("`--version` excepted") but not executed. `jj debug` subcommands
  other than `watchman status` and `reindex` were not adjudicated ([UNK]); nor were
  `jj git remote list`-style reads that do not occur in the corpus.
- **`jj config set`/`unset`** are treated as writes (they modify a config file; `set`
  on `user.name`/`user.email` also snapshots via `config/set.rs:102`). They are not
  working-copy writes, so the docstring's wording does not describe them either.
- **Not adjudicated:** `jj:$@` (4 rows), `jj:$c`/`jj:$C` (3), `jj:ci` (7, alias
  expansion unknown), and the 11 mis-expanded shell-function rows as write-vs-read.
  `jj:root/unparsed`, `jj:util/unparsed`, `jj:op/unparsed`, `jj:workspace/unparsed`,
  `git:checkout/unparsed` (5 rows) were parsed with the `/unparsed` suffix and were not
  separately classified.
- **No base measurement.** `9c54c56` has no `vcs_write` class (`tool-base.py:61`), so
  every row here is new by construction; a row-level base-vs-e629f73 diff adds nothing
  for this class and was not run. The other-class corpus diff was not re-measured.
- **Text counts are not emissions.** Grep occurrences of `git stash list` (19),
  `git pull --dry-run` (161), `git push --porcelain` (70 text matches), `jj --version`
  (1,694) etc. include prose, docs and fixture generators; only `--scan` rows are
  claimed as tool emissions.
- Fixture code was never executed; the only commands this seat ran were `--scan`,
  read-only `git` (`rev-parse`, `status --porcelain`, `<sub> -h`, `--version`),
  `sha256sum`, `grep`, `curl` (pinned raw source) and `python3` over scan output. No
  pacman/uv/npx/jj/systemctl/compositor command, no gate.

## Installs

none
