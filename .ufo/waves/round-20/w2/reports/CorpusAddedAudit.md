# CorpusAddedAudit — partly falsified: the 27 added non-vcs rows hold (24 observed, 3 lead), but the vcs_write class carries ≥53 confirmed false-positive rows on the live corpus (0.86% of 6,195 added rows), including help/usage forms the docstring says are excepted, and 78 more rows with no working-copy write (131 of 6,195 = 2.11%).

Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, tip `a4046a8216080d4004de3f268c62cf142095ac07`. All reads and commands used absolute paths; no tracked lane file was modified.

## Method and receipts

Whole-corpus scan of `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin` (5,978 `.jsonl`, 4,968,687,236 bytes), one process per tool version, no per-file isolation needed because neither scan hit an invalid line (both exit 1 = `findings`, not 2):

```
$ python3 -I /tmp/r20-caa-base.py  --scan /home/vgpnk/.omp/agent/sessions/-Projects-shokunin
MADO_TRIPWIRE: findings        # exit 1
$ python3 -I /tmp/r20-caa-repair.py --scan /home/vgpnk/.omp/agent/sessions/-Projects-shokunin
MADO_TRIPWIRE: findings        # exit 1
```

Byte identities (tools extracted with `git show <rev>:tools/mado-tripwire.py`; repair hash matches the claim `9613f510…`):

- `/tmp/r20-caa-base.py` (9c54c56) sha256 `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`
- `/tmp/r20-caa-repair.py` (28c6837) sha256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`
- repair verdict `/tmp/r20-caa-repair-verdict.json` sha256 `84a5fba4eac10dce7f1cd8707cff928a57e553444a9f3cb470d1fd9c972aa6de` — 8,094 findings (8,070 observed + 24 lead); `counts` {host_mutation 116, live_probe 1119, package_query 540, tool_install 121, vcs_write 6174} (observed-only, sums to 8,070).
- base verdict `/tmp/r20-caa-base-verdict.json` sha256 `d26fae829a71eed03674fd18b7eac646af6fdccde27556e7259a32e762787476` — 1,751 findings, `counts` {host_mutation 116, live_probe 1099, package_query 536}; no `vcs_write`/`tool_install` key (those classes do not exist at 9c54c56).

Diff is a multiset difference keyed on `(corpus-relative path, line, class, rule)` and, separately, `+ (evidence)`. Added: **6,343 rows** — live_probe 20, package_query 7, tool_install 121, vcs_write 6,195 (6,174 observed + 21 lead). **Lost rows: 0** (no baseline row disappeared anywhere in the corpus; the repair is monotonic on this snapshot).

## 1. The 27 added rows outside vcs_write/tool_install — all hold

27 rows = 20 `live_probe` + 7 `package_query`. Detail dossier per row at `/tmp/r20-caa-27/` (raw toolCall text extracted from the transcript bytes; nothing from the transcripts was executed).

| class / rule | rows | verdict |
|---|---|---|
| live_probe `journalctl` | 16 | 16 true observed |
| live_probe `ps` | 2 | 2 true observed |
| live_probe `pgrep` | 1 | 1 true observed |
| live_probe `systemctl:show` | 1 | 1 true observed |
| package_query `pacman:-Q` | 6 | 3 true observed, 3 true lead |
| package_query `pacman:-Qo` | 1 | 1 true observed |

**No false positive in this set.** Per-row ledger (TO = true observed, TL = true lead; `delta` is the repair-minus-base row count, all 1):

```
TO  KengakuScopeAudit.jsonl:140          pgrep        (run("pgrep -a llama-server || true"), shell=True helper in cell)
TO  KengakuScopeAudit.jsonl:140          ps           (run("ps -p 1299 -o pid=,comm= || true"))
TO  KillEventsJournal.jsonl:64           journalctl   (subprocess list in heredoc)
TO  KillEventsJournal.jsonl:69           journalctl   (subprocess list; a second tool call on the same line also literal)
TO  KillEventsJournal.jsonl:75           journalctl   (literal `journalctl --user …`; also `journalctl --help` at top level — in-class by convention)
TO  KillEventsJournal.jsonl:124          journalctl   (subprocess list)
TO  OomClassTaxonomy.jsonl:71            journalctl   (bash literals + run(list))
TO  OomClassTaxonomy.jsonl:83            journalctl   (lines(['journalctl',…]) with spawning body)
TO  OomClassTaxonomy.jsonl:100           journalctl   (rows(['journalctl',…]))
TO  OomClassTaxonomy.jsonl:130           journalctl   (entries(['journalctl',…]))
TO  ProviderSecrecy.jsonl:92             journalctl   (run(["journalctl",…]) with spawning body)
TO  ProviderSecrecy.jsonl:99             journalctl   (same)
TO  ThreatModel.jsonl:84                 journalctl   (in-cell def run + subprocess.run(list))
TO  2026-10-18T14-15-00-878Z_….jsonl:35  ps           (sh("ps …") with earlier def sh shell=True)
TO  MadoR13.jsonl:470                    pacman:-Q    (run_record(…['pacman','-Q',…]) with visible run_record)
TL  MadoR13.jsonl:470                    pacman:-Q    (duplicate lead for the same call)
TO  MadoR14.SourceSafety.jsonl:152       pacman:-Q    (recipe passed to bash -c)
TO  MadoR14.SourceSafety.jsonl:155       pacman:-Q    (recipe2 via .replace, then bash -c)
TO  TsukuroiR12.MatrixCriticR.jsonl:44   pacman:-Qo   (r("pacman -Qo …"), r shell=True)
TO  TsukuroiR12.MatrixCriticR.jsonl:44   journalctl   (r("journalctl …"))
TO  TsukuroiR12.MatrixCriticR.jsonl:49   journalctl   (r("journalctl --list-boots …"))
TO  TsukuroiR12.MatrixCriticR.jsonl:52   journalctl   (r("journalctl … -u limine-snapper-sync.service"))
TO  TsukuroiR12.MatrixCriticR.jsonl:55   journalctl   (r("journalctl … -k -g 'Command line:'"))
TO  TsukuroiR12.MatrixCriticR.jsonl:59   journalctl   (r("journalctl … _TRANSPORT=kernel …"))
TO  TsukuroiR13.SecurityBoundary.jsonl:56 systemctl:show (run("systemctl show …"), run shell=True)
TL  MadoR20/MadoR20.ReopenExecModel.jsonl:63 pacman:-Q  (run([...]) before def run → NameError; lead only)
TL  MadoR20/MadoR20.ReopenExecModel.jsonl:70 pacman:-Q  (same, second experiment)
```

Every `observed` row is a literal argv reached through a visible spawning body, checked one by one:

- `ps`/`pgrep`: `sh(cmd)` / `run(cmd)` are defined in the same (or an earlier) cell with `subprocess.run(..., shell=True)` — e.g. `2026-10-18T14-15-00-878Z_…jsonl:35` uses `def sh(c): print(subprocess.run(c,shell=True,...))` at cell line 18; `KengakuScopeAudit.jsonl:140` defines `run(cmd, shell=True)` in the cell and calls `run("pgrep -a llama-server || true")`, `run("ps -p 1299 -o pid=,comm= || true")`.
- `journalctl` 16: literal `["journalctl", …]` inside `subprocess.run` / heredoc helpers (`KillEventsJournal.jsonl:64` `cmd=["journalctl","--user",…]`; `OomClassTaxonomy.jsonl:83` `def lines(args): p=subprocess.run(args,…)` then `lines(['journalctl',…])`; `ProviderSecrecy.jsonl:92` `def run(args): p=subprocess.run(args,…)` then `run(["journalctl","--user","-b","--fields"])`; `ThreatModel.jsonl:84` `def run(cmd): p=subprocess.run(cmd,…)` then the journal argv). One of the 16 is `journalctl --help` (KillEventsJournal:75) — a help invocation, but the class has no help carve-out and base already emits `journalctl --version`/`pgrep --version` rows, so it is in-class by the tool's own convention, not an added false positive.
- `systemctl:show` (`TsukuroiR13.SecurityBoundary.jsonl:56`): `def run(c): subprocess.run(c,shell=True,…)` at cell 44, call `run("systemctl show -p User …")`.
- `pacman:-Qo` (`TsukuroiR12.MatrixCriticR.jsonl:44`): `r(cmd)` shell=True at cell 39, call `r("pacman -Qo …")`.
- `pacman:-Q` observed (`MadoR13.jsonl:470`, `MadoR14.SourceSafety.jsonl:152/155`): `def run_record(name,args,…): subprocess.run(args,…)` at cell 437 → `run_record('packages',['pacman','-Q',…],0)`; the SourceSafety rows are inside a `recipe` string passed to `subprocess.run(["bash","-c",recipe])` (152), and the `recipe2 = recipe.replace(…"pacman -Q hyprland"…)` variant re-passed to `bash -c` (155).
- `pacman:-Q` lead ×3: `MadoR13.jsonl:470` is a **duplicate** lead on a row already reported observed (same key, same call); `MadoR20/MadoR20.ReopenExecModel.jsonl:63` and `:70` are the round-19 lesson case — `run(['pacman','-Q','hyprland'])` called before `def run(a): pass` (`call_before_def`), so nothing executes. These are exactly right as `lead`: the literal argv is stated and execution is not established. The repair no longer reports them as ordinary findings; the R19-V2 harm is fixed.

[INFERENCE] The MadoR13 lead row is emitted by the same dual path demonstrated in §2; it is not an independent claim.

## 2. Lead rows overall: 24 — but only 2 are lead-only

`lead` rows in the whole corpus verdict: **24** = 21 `vcs_write` + 3 `package_query`.

- **22 of 24 are shadowed**: an `observed` row with the identical `(file, line, class, rule)` exists in the same verdict (21/21 vcs leads, 1/3 package leads). The lead marker therefore overstates "unverified" commands: it usually duplicates a command the tool already followed.
- **2 lead-only rows**: `MadoR20/MadoR20.ReopenExecModel.jsonl:63` and `:70` (the round-19 `BLOCK=…['pacman','-Q','hyprland']` shape). These are the two rows in the whole corpus that are genuinely "stated, not established".

Minimal reproduction of the duplicate-evidence path (`/tmp/r20-caa-synth/case.jsonl`; one cell with a visible same-cell helper):

```
$ python3 -I /tmp/r20-caa-repair.py --scan /tmp/r20-caa-synth/case.jsonl
vcs_write git:add    observed git add -A
vcs_write git:add    lead     git add -A
vcs_write git:commit observed git commit -qm initial pin
vcs_write git:commit lead     git commit -qm initial pin
vcs_write jj:log     observed jj log --no-graph -r all()
vcs_write jj:log     lead     jj log --no-graph -r all()
```

One `run(['git','add','-A'])` yields two rows: the followed-helper `observed` and an unexplained `lead` for the same literal argv. Same shape at `TameshiR18/TameshiR18.X06DispositionGuards.jsonl:60/81/87/93/96` (defines `def run(argv, check=True): p=subprocess.run(argv,…)` then calls it) — all 21 vcs leads there are these duplicates.

## 3. vcs_write sample — false positives

### 3a. Requested sample: every added vcs row whose command carries help/dry-run/version (32 rows, a census, not a random draw)

23 false positives / 9 true positives. True positives first, because they confirm the intended rules:

| row | transcript evidence | verdict |
|---|---|---|
| `git:commit` ReopenGitSource:86 | `git commit -m --help` → `rc=0 commits=2 subject=--help` (result line 90) | TP (real commit) |
| `git:commit` ReopenGitSource:112 | `git commit -m -h` → `subject=-h commits=4` (line 116) | TP (real commit) |
| `git:commit` ScoutJjHelpEmpirical-3:39 | `git commit -m --help` → `commits=1 last_msg=--help` (line 43) | TP |
| `git:commit` line 112's sibling `git commit -m x --help` | `commits_before=3 after=3 out=3551` → help, **no finding** | correctly clean |
| `jj:git` ×4 (AtkCasesH2:81,90; Scout:50; SrcJjHelp:92) | `jj git push --dry-run`; Scout:52 measures `ops=14->15`, i.e. snapshot YES | TP by the model |
| `jj:diff` ×2 (RevSpecVcsHelp-3:95,118) | `jj … diff -- --help` where `--help` is a tracked file (`touch -- …/--help`) | TP |

False positives, with the transcript text that would have shown the opposite:

| # | row | transcript fact | why FP |
|---|---|---|---|
| 1 | `jj:$c` W2jProbeKagi:77 | `for c in commit new squash describe; do ~/.local/bin/jj $c --help …; done`; result prints each help's option list | all four are help forms; help delta=0 (Scout:29) |
| 2 | `jj:<sub>/unparsed` MadoR19:554 | `echo "… 74 \`jj <sub> --help\` …" >> corpus/lessons/round-19.md` — escaped backticks inside double quotes | literal text, never a command |
| 3 | `jj:log` AtkHeldout:114 | `jj log --version` → `rc=2 before=3 after=3`, `error: unexpected argument '--version' found` (line 117) | usage error, no snapshot |
| 4 | `git:commit` RevToolDiffVcs:69 | `git commit --fi --dry-run` → `error: ambiguous option: fi (could be --file or --fixup)` (line 75) | aborts, no commit |
| 5–21 | 17 `jj:jj …` rows, Scout:27 (7), :30 (2), :36 (8) | the script is `run_form() { local label="$1"; shift; jj "$@" … }` with calls `run_form 'jj st --help' st --help`; the tool's own `command` field is the impossible `jj jj st --help st --help` | fabricated argv; every real form is help/version with measured `delta=0` (Scout:29,38) |
| 22–23 | `git:stash` TwVcsHelp-3:149,152 | `for s in push save …; do git stash $s --help-all …`; result prints `usage: git stash …` for every s | `--help-all` is help; no stash created |

### 3b. Random 30 added vcs rows (seed 20261020)

29 true positives (real literals: `git commit/add/checkout/push/merge`, `jj st/log/ci/new/bookmark/config/git init`, all resolved verbs), **1 false positive** — `jj:$c` W2jProbeKagi:77, already in the census above.

### 3c. Additional confirmed false positives outside the help-token census (30 rows)

Splice artifacts (same `$1`/`shift` bug, `JjDocAutoTrack-2.jsonl:109` `check() { local name=$1; shift; jj "$@" … }`): `jj:bookmarklist`, `jj:filelist`, `jj:configlist`, `jj:oplog`, `jj:sparselist`, `jj:wclist`, `jj:taglist`, `jj:operationlog`, `jj:utildbg`, `jj:debugwc` (each `jj <label> <real sub…>`, e.g. `jj taglist tag list` — jj has no `taglist` subcommand) and one `jj:root` (`jj root root`, invalid positional). Plus the non-help `jj:jj` rows (7: `help log`×2, `help git push`, `st (positive control)`, `st (POSITIVE)`, `log (POSITIVE)`, `log --bogus`), `jj:bad subcommand` (Scout:30, real `jj boguscmd` → `exit=2 delta=0`), `jj:$c` JjDocHooksAttributes-2:112 (`for c in "commit --help" "git push --help" "git clone --help" "run --help"; do jj $c …`, all help), `jj:/tmp/…/bookmark` RevToolDiffVcs:63 (`jj -C …` → `error: unexpected argument '-C' found`, exit 2), `jj:user.name=t` KaidokuR19.ReviewRevpin:26 (`jj -c … commit` → jj 0.45.1 `error: unexpected argument '-c' found`, exit 2; same binary sha256 `cd5efc3e…`), `jj:$@` Scout:30 (the only probes in that call are `-V`, `log --bogus`, `boguscmd`, `describe -m --help`; all `delta=0`), and 7 of the 8 escaped-backtick prose rows (SrcJjHelp-3:106 and :114×2 `grep "## \`jj help\`"…`; SoujiR17-3:566 `printf` prose containing `\`jj util gc\`` and `\`jj op abandon\``; JjDocOpLogGrowth-2:202 `grep … "\`jj util gc\` command"`; TabiR17.DraftLessonGate:83 `printf` prose containing `\`jj workspace update-stale\``).

**Confirmed false-positive total in added vcs rows: 53** (23 + 30) = **0.86%** of 6,195; precision 99.14% on this corpus. The 3 `(POSITIVE)` label rows correspond to real writes at the same transcript line, but the row's `command` is a command that never ran; they are counted as FP rows and should not be read as "the tool found the write".

## 4. Reproductions (minimal, in /tmp; nothing from a transcript executed)

Each is a synthetic one-call transcript scanned with the 28c6837 tool:

1. `$1`/`shift` splice — `run_form() { local label="$1"; shift; jj "$@"; }; run_form 'jj st --help' st --help` yields
   `[('vcs_write','jj:$@','observed','jj $@'), ('vcs_write','jj:jj st --help','observed','jj jj st --help st --help')]`.
   `shell_expand()` (`tools/mado-tripwire.py:851-899` at 28c6837) substitutes `$@` with *all* call args and has no `shift` handling (no `shift` token anywhere in the file).
2. Escaped backticks — `echo "docs: \`jj help\` is the help form; also \`jj util gc\`"` yields
   `[('vcs_write','jj:help\\/unparsed','jj help\\'), ('vcs_write','jj:util/unparsed','jj util gc\\')]`,
   while a real substitution `echo "now: \`jj st\` done"` yields the correct `jj:st`. `\`` inside double quotes is literal in bash; the tokenizer drops the backslash and treats it as command substitution.
3. Usage/help forms — `jj log --version`, `git stash push --help-all`, `jj -c user.name=t commit -m x`, `jj -C /tmp/x git init --colocate` yield `jj:log`, `git:stash`, `jj:user.name=t`, `jj:/tmp/x`; the same jj 0.45.1 binary rejects `-c` and `-C` with `unexpected argument` (exit 2), and `git stash push --help-all` prints `usage:` and creates nothing (while `git stash list --help-all` is correctly clean — the dynamic `$s` in the corpus row removes that safety).
4. Ambiguous abbreviation — `git commit --fi --dry-run` yields `git:commit`; real git: `error: ambiguous option: fi` (`--file` vs `--fixup`), exit 2.
5. `jj -c`/`-C` transcripts: `KaidokuR19/KaidokuR19.ReviewRevpin.jsonl:26` and `MadoR20/MadoR20.RevToolDiffVcs.jsonl:63` show the same exit-2 errors in their own tool results.

## 5. Class-model block found while adjudicating: no working-copy snapshot

The docstring's jj rule rests on "jj snapshots the working copy on all of them". Measured with the transcript's own jj (`jj 0.45.1-7c41cdeb…`, HOME/XDG under /tmp, fresh colocated repo, op-heads before/after each command with one pending file change):

```
jj config list              rc=0 no-snapshot
jj config get user.name     rc=0 no-snapshot
jj config path              rc=2 no-snapshot
jj config path --repo       rc=0 no-snapshot
jj config unset --repo …    rc=0 no-snapshot
jj root                     rc=0 no-snapshot
jj debug working-copy       rc=0 no-snapshot
jj debug reindex            rc=0 no-snapshot
jj config set --repo …      rc=0 SNAPSHOT
jj status / log -n 1 / diff --summary / file list / bookmark list / tag list / show  rc=0 SNAPSHOT
jj debug watchman status    rc=255 SNAPSHOT
```

The same result appears inside the corpus itself: `JjDocAutoTrack-2.jsonl:109`'s own matrix prints `jj config list rc=0 not-snapshotted`, `jj root rc=0 not-snapshotted`, `jj debug working-copy rc=0 not-snapshotted`.

Rows affected among the 6,195 added vcs rows:
- `jj:config` **148** (`config set` 75, `list` 51, `get` 11, `path` 10, `unset` 1). `config set` **does** snapshot the working copy (measured, rc=0 SNAPSHOT) → the 75 `set` rows are TP. The 73 `list`/`get`/`path`/`unset` rows do not → FP (`unset` edits repo config but loads no workspace; `list`/`get`/`path` are pure reads).
- `jj:root` **1** genuine `~/.local/bin/jj root` (read-only; the other `jj:root` row is the splice artifact above).
- `jj:debug` **4** `jj debug reindex` (no snapshot) — the other 3 `debug watchman status` do snapshot and are TP.

So **78 additional rows** (72 `jj:config` reads + 1 `jj:config unset` + 1 `jj:root` + 4 `jj debug reindex`) assert a working-copy write that did not happen. Counting both blocks, **131 of 6,195 added vcs rows (2.11%)** have no working-copy write; 53 of them are fabricated or help/usage rows where no command executed at all.

## Limits

- I ran the whole-corpus scan, the diff, the 27-row dossier extraction, the lead shadow check, the 32-row help census, the random 30, and the five minimal reproductions. I did **not** re-run the precision suite (`tw-precision.py`), the recall suites, `isolation-check.sh`, `tally-check.py`, or `measure.py`; those are other seats' items. This report says nothing about the 172/175 fixture score or the tally.
- The 6,195-row vcs class was not adjudicated row by row. Adjudicated: the 43 odd-rule rows, all 32 help/dry/version-bearing rows, the 11 spliced label rows, the 8 prose rows, the 4 `jj:$@` rows, and a random 30. The 53 confirmed FPs are a floor for the patterns I proved, not an upper bound.
- `jj`/`git` semantics were measured with jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5 and the host git in `/tmp` with HOME/XDG redirected; the lane checkout was never used as a VCS workspace. `debug watchman status` returned rc=255 on this host (no watchman); the snapshot seen there may be an environment effect — [INFERENCE] its 3 rows are TP, but I did not re-measure in a watchman-equipped environment.
- Transcript text is data: I read bytes, parsed JSON, and never executed a transcript line. No host command from the corpus was replayed. `journalctl --help` is called true-observed because the class has no help carve-out; if the integrator wants one, that row and base's `--version` rows move together.
- `MadoR13.jsonl:470` publishes both an `observed` and a `lead` row for one call; I treat the observed row as the claim and the lead as duplicate evidence, not as a second finding.

## Installs

none. No pacman/sudo/systemctl/compositor command was run; jj and git were already present and were exercised only inside `/tmp` with redirected HOME/config.
