# MadoR20.CorpusRemovedAudit — holds: all 144 command-level rows removed between 1f7f995 and 28c6837 are help (130), dry run (10), or pure data (1), plus 3 same-key representative substitutions that keep their file:line:class:rule finding; no lost true finding.

Scope: every finding row present with tool `1f7f995` and absent with tool `28c6837` over the real corpus `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin` (recursive `*.jsonl`). Transcripts were parsed as JSONL data only; no transcript content was executed. Both tools were scanned from `/tmp` copies of committed bytes.

## Receipts

- Clone: `git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado-r20w2-CorpusRemovedAudit`, HEAD `a4046a8`, origin removed.
- Harmed tool: `git show 1f7f995:tools/mado-tripwire.py` → `/tmp/tw-harm.py`, sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`.
- Repaired tool: `git show 28c6837:tools/mado-tripwire.py` → `/tmp/tw-repair.py`, sha256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`; the same digest is `a4046a8:tools/mado-tripwire.py`.
- Corpus at scan time: 5,978 `.jsonl` files, 4,966,130,696 bytes (recursive walk, regular files only).
- Method: for every file, `python3 -I <tool> --scan <file>` with each tool, per-file (49 files contained removals); all scans exited 0/1 with a valid `mado-tripwire-verdict-v1` payload; 0 scan errors.
- Totals: base 7,823 findings; repaired 8,045 findings.
- Removed set: 144 strict rows keyed `(file, line, class, rule, command)`; re-scanned all 49 affected files with fresh processes and re-checked every one of the 144: `base-missing 0, new-still-present 0`.
- Under the lane harness' row key `(file, line, class, rule)` (no command/evidence, as in `.ufo/waves/round-20/corpus-diff.py:_finding_key`): 129 lost keys, 132 lost instances.

## Adjudication summary

| class | rows | verdict |
|---|---|---|
| help form (`-h`/`--help`), key disappears at that line | 118 | correct removal |
| help form, same key still reported at that line | 12 | correct removal |
| dry run (`--dry-run`, `git add|push -n`) | 10 | correct removal |
| pure data (`pacman -Q` passed to a pure callable) | 1 | correct removal |
| real command, same key still reported at that line | 3 | NOT LOST (see below) |

Key-level loss (the number a corpus-diff run reports as lost keys): 115 help + 9 dry-run + 1 data + 7 mixed-key instances = 132 instances over 129 keys. I inspected all 7 mixed-key instances (5 keys) individually; every lost instance in them is the help/dry-run row while the real command in the same cell is still reported:

- `JjDocOpLogGrowth-2.jsonl:14` `jj:op`: base `jj op --help`, `jj op abandon --help`; new 0 (both help).
- `MadoR20.SrcGitHelpSource-3.jsonl:75` `git:commit`: base `git commit --help`, `git commit --allow-empty -m --help --dry-run`; new 0 (help + dry run).
- `MadoR20.SrcGitHelpSource-3.jsonl:82` `git:commit`: base `git commit -q -m init` (kept), `git commit --help` (removed).
- `MadoR20.SrcGitHelpSource-3.jsonl:97` `git:commit`: base `git commit -q -m init` (kept), `git commit -h` (removed).
- `TameshiR18.C03FleetJjPractice.jsonl:80` `jj:git`: base `jj -R repoA git init --colocate`, `jj git init --colocate` (both kept), `jj git init --help` (removed).

## Controls that would have shown the opposite

**jj help (jj 0.45.1-7c41cdeb, `/home/vgpnk/.local/bin/jj`).** Throwaway repo `/tmp/lab/jjvcs/repo` created with `jj git init --colocate`, `HOME`, `XDG_CONFIG_HOME` and `JJ_CONFIG` redirected under `/tmp/lab/jjvcs/home`; before each command a tracked file was dirtied; the check is `jj --ignore-working-copy log --no-graph -r @ -T commit_id` before vs after. All 44 distinct jj help command strings from the removed jj rows (after normalizing `~/.local/bin/jj` to the absolute binary): rc=0, help text, `@` commit_id unchanged — 0 snapshots. Examples:

```
no-snap rc=0 | /home/vgpnk/.local/bin/jj util snapshot --help
      Snapshot the working copy if needed
no-snap rc=0 | jj -R /tmp/mado-r20-RevSpecVcsHelp diff --stat -h
      Compare file contents between two revisions
no-snap rc=0 | jj commit --help
      Update the description and create a new change on top [default alias: ci]
```

The `-R` target did not exist, yet clap printed help and exited 0, supporting the repair's "help is answered before the workspace is loaded" rule. `jj util snapshot --help`, `jj debug reindex --help`, `jj git push --help`, `jj bookmark set --help`, `jj op abandon --help`, `jj config path -h`, `jj workspace add --help`, `jj file track --help`, `jj metaedit --help`, `jj rebase --help`, `jj st --help`, `jj log --help` and the rest were each exercised, not just sampled.

Positive control (proves the check detects snapshots): the two non-help jj commands in the removed set, run as their real argv, **did** change `@`:

```
SNAPSHOT rc=0 | jj op log --no-graph -n 1 -T 'id.short()'
SNAPSHOT rc=0 | jj log --no-graph -r 'all()' -T 'commit_id.short() ++ " " ++ bookmarks ++ "\n"'
```

**git (git 2.56.0).** Throwaway `/tmp/lab/gitvcs/repo` with an initial commit and a bare `origin`; after each command: `git rev-parse HEAD`, `git --git-dir <remote> rev-parse main`, and `git diff --cached --name-only` compared before/after. All 22 distinct non-jj commands from the removals (journalctl/pacman excluded by the host pause): 0 state changes. Examples:

```
no-write rc=0 | git add -A --dry-run
      add 'a.txt'
      add 'newfile1'
no-write rc=0 | git push --dry-run
      Everything up-to-date
no-write rc=0 | git commit --allow-empty -m --help --dry-run
      On branch main ...        (HEAD unchanged; --help is -m's value, --dry-run blocks the commit)
no-write rc=0 | git -C /tmp/mado-r20-RevSpecVcsHelp --help commit
      GIT-COMMIT(1)                      Git Manual                     GIT-COMMIT(1)
no-write rc=128 | git add --dry-run -n tests/vault/vadv54-run/p/p6repo
      fatal: pathspec ... did not match any files
```

`git push --dry-run` was tested against a live bare remote and left `main` byte-identical.

**pure data.** `MadoR20.CaseWrapperForms-3.jsonl:120`, eval cell verbatim:

```python
import functools
f = functools.cache(lambda a: len(a))
try:
    f(['pacman', '-Q'])
    print('no error')
except TypeError as e:
    print('TypeError:', e)
print('tuple ok:', f(('pacman', '-Q')))
```

The only callable is a `functools.cache`-wrapped `lambda a: len(a)`; the list is unhashable and raises `TypeError`, the tuple returns 2. No subprocess exists in the cell. The old row was HelperFn rule B exactly (command-shaped data passed to a pure callable) and its removal is correct.

## The three "real command" rows (not lost)

Each removed string is a real invocation, and the repaired tool still emits the same `file:line:class:rule` at that line, with a different representative command from the same cell. Both tools report only one representative per key per line, so these are attribution substitutions, not lost findings.

1. `OomClassTaxonomy.jsonl:130`, `live_probe/journalctl`. Removed `journalctl --user -b -g dumped core ...` (a literal argv passed to visible helper `entries(args)` whose body calls `subprocess.run`). New row at the same line: `journalctl --user -b MESSAGE_ID=<redacted> -o json --output-fields=MESSAGE,MESSAGE_ID,...` — one of the other literal `entries([...])` calls in the same cell. `live_probe` is still reported at 130; the command was not executed here (host pause forbids journalctl), only read as data.
2. `W2jScribe.jsonl:93`, `vcs_write/jj:op`. Removed `jj op log --no-graph -n 1 -T id.short()`, a `subprocess.run("jj op log ...", shell=True, ...)` in the cell (empirically snapshots, above). New row at 93: `jj op log --no-graph -n 1 -T id.short() ++ " " ++ description.first_line() ...` from the earlier `run()` call in the same cell.
3. `TameshiR18.X06DispositionGuards.jsonl:93`, `vcs_write/jj:log`. Removed `jj log --no-graph -r all() -T ...`; the same cell also calls `jj log ... -r @-`, which is the new row at 93, and the removed `-r all()` string is still reported by the new tool in the same file at line 96. Empirically both forms snapshot; the line keeps its `jj:log` finding.

If MadoR20 adopts strict per-command identity rather than the lane's `(file,line,class,rule)` row key, these 3 rows are the only counterexamples to "every removal is data/help/dry-run"; none removes a finding key, and I found no case where a harmful command's class disappeared.

## Non-removal observation

Two rows changed evidence, not presence: `MadoR20.ReopenExecModel.jsonl` lines 63 and 70, `package_query/pacman:-Q` `pacman -Q hyprland`, `observed` → `lead`. The cell calls `run(['pacman','-Q','hyprland'])` before `def run` is defined, so that call raises `NameError` at runtime and the argv is never executed; `lead` is the conservative marker. Both rows remain findings.

Separately, the repaired tool emits duplicate `observed` + `lead` rows for the same command at `TameshiR18.X06DispositionGuards.jsonl` lines 60, 81, 87, 93, 96. That is addition-side inflation, outside this removal audit, but it will affect any count-based no-harm metric; flagged for the integrator.

## The 144 removed rows

Paths are relative to the corpus root. Bases `1f7f995`; comparisons `28c6837`. Every row was re-verified present-then-absent by fresh scans.

| # | file:line | row | command | verdict |
|---|---|---|---|---|
| 1 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99.jsonl:1713` | vcs_write/jj:git | `jj git init --help` | correct — help |
| 2 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jConnectProtocol.jsonl:161` | vcs_write/jj:describe | `~/.local/bin/jj describe --help` | correct — help |
| 3 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jConnectProtocol.jsonl:164` | vcs_write/jj:commit | `~/.local/bin/jj commit --help` | correct — help |
| 4 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jConnectProtocol.jsonl:164` | vcs_write/jj:describe | `~/.local/bin/jj describe --help` | correct — help |
| 5 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:80` | vcs_write/jj:commit | `jj commit -h` | correct — help |
| 6 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:83` | vcs_write/jj:commit | `jj commit -h` | correct — help |
| 7 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:86` | vcs_write/jj:commit | `jj commit --help` | correct — help |
| 8 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:86` | vcs_write/jj:describe | `jj describe --help` | correct — help |
| 9 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:89` | vcs_write/jj:describe | `jj describe --help` | correct — help |
| 10 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:89` | vcs_write/jj:squash | `jj squash --help` | correct — help |
| 11 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:92` | vcs_write/jj:describe | `jj describe --help` | correct — help |
| 12 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:95` | vcs_write/jj:describe | `jj describe --help` | correct — help |
| 13 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeAudio.jsonl:98` | vcs_write/jj:metaedit | `jj metaedit --help` | correct — help |
| 14 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeChousa.jsonl:69` | vcs_write/jj:commit | `~/.local/bin/jj commit --help` | correct — help |
| 15 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeChousa.jsonl:72` | vcs_write/jj:describe | `~/.local/bin/jj describe --help` | correct — help |
| 16 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeChousa.jsonl:72` | vcs_write/jj:metaedit | `~/.local/bin/jj metaedit --help` | correct — help |
| 17 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeFleetRoot.jsonl:61` | vcs_write/jj:describe | `jj describe --help` | correct — help |
| 18 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeFleetRoot.jsonl:61` | vcs_write/jj:git | `jj git init --help` | correct — help |
| 19 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeFleetRoot.jsonl:61` | vcs_write/jj:metaedit | `jj metaedit --help` | correct — help |
| 20 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:80` | vcs_write/jj:commit | `~/.local/bin/jj commit --help` | correct — help |
| 21 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:80` | vcs_write/jj:describe | `~/.local/bin/jj describe --help` | correct — help |
| 22 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:83` | vcs_write/jj:commit | `~/.local/bin/jj commit -h` | correct — help |
| 23 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:83` | vcs_write/jj:describe | `~/.local/bin/jj describe -h` | correct — help |
| 24 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:86` | vcs_write/jj:metaedit | `~/.local/bin/jj metaedit -h` | correct — help |
| 25 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKaidoku.jsonl:95` | vcs_write/jj:commit | `~/.local/bin/jj commit --help` | correct — help |
| 26 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKaidoku.jsonl:95` | vcs_write/jj:describe | `~/.local/bin/jj describe --help` | correct — help |
| 27 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKaidoku.jsonl:98` | vcs_write/jj:commit | `~/.local/bin/jj commit --help` | correct — help |
| 28 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKaidoku.jsonl:98` | vcs_write/jj:describe | `~/.local/bin/jj describe --help` | correct — help |
| 29 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKaidoku.jsonl:101` | vcs_write/jj:describe | `~/.local/bin/jj describe --help` | correct — help |
| 30 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKaidoku.jsonl:104` | vcs_write/jj:describe | `~/.local/bin/jj describe --help` | correct — help |
| 31 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKaidoku.jsonl:104` | vcs_write/jj:new | `~/.local/bin/jj new --help` | correct — help |
| 32 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKake.jsonl:84` | vcs_write/jj:describe | `~/.local/bin/jj describe --help` | correct — help |
| 33 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeMado.jsonl:55` | vcs_write/jj:commit | `~/.local/bin/jj commit --help` | correct — help |
| 34 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeMado.jsonl:55` | vcs_write/jj:describe | `~/.local/bin/jj describe --help` | correct — help |
| 35 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeMado.jsonl:58` | vcs_write/jj:commit | `~/.local/bin/jj commit --help` | correct — help |
| 36 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTabi.jsonl:83` | vcs_write/jj:describe | `jj describe --help` | correct — help |
| 37 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTabi.jsonl:86` | vcs_write/jj:describe | `jj describe --help` | correct — help |
| 38 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTabi.jsonl:89` | vcs_write/jj:describe | `jj describe --help` | correct — help |
| 39 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTabi.jsonl:93` | vcs_write/jj:describe | `jj describe --help` | correct — help |
| 40 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTabi.jsonl:93` | vcs_write/jj:metaedit | `jj metaedit --help` | correct — help |
| 41 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTsukuroi.jsonl:68` | vcs_write/jj:commit | `jj commit --help` | correct — help |
| 42 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeTsukuroi.jsonl:68` | vcs_write/jj:describe | `jj describe --help` | correct — help |
| 43 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjAuditKasegi-2.jsonl:76` | vcs_write/jj:util | `~/.local/bin/jj util gc --help` | correct — help |
| 44 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjAuditPromptText-2.jsonl:131` | vcs_write/jj:git | `jj git push --help` | correct — help |
| 45 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjAuditPromptText-2.jsonl:135` | vcs_write/jj:git | `jj git push --help` | correct — help |
| 46 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjCriticRollback-2.jsonl:98` | vcs_write/jj:git | `~/.local/bin/jj git colocation --help` | correct — help |
| 47 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocConcurrency-2.jsonl:226` | vcs_write/jj:bookmark | `jj bookmark list --help` | correct — help |
| 48 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocHeadAttachment-2.jsonl:115` | vcs_write/jj:git | `~/.local/bin/jj git colocation status --help` | correct — help |
| 49 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocIdentity-2.jsonl:126` | vcs_write/jj:git | `jj git push --help` | correct — help |
| 50 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocImmutable-2.jsonl:43` | vcs_write/jj:rebase | `~/.local/bin/jj rebase --help` | correct — help |
| 51 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocImmutable-2.jsonl:68` | vcs_write/jj:rebase | `~/.local/bin/jj rebase --help` | correct — help |
| 52 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocImmutable-2.jsonl:87` | vcs_write/jj:git | `~/.local/bin/jj git push --help` | correct — help |
| 53 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocLargeRepo-2.jsonl:34` | vcs_write/jj:debug | `/home/vgpnk/.local/bin/jj debug --help` | correct — help |
| 54 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocLargeRepo-2.jsonl:49` | vcs_write/jj:debug | `/home/vgpnk/.local/bin/jj debug watchman --help` | correct — help |
| 55 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocLargeRepo-2.jsonl:49` | vcs_write/jj:util | `/home/vgpnk/.local/bin/jj util snapshot --help` | correct — help |
| 56 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocOpLogGrowth-2.jsonl:14` | vcs_write/jj:op | `jj op --help` | correct — help |
| 57 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocOpLogGrowth-2.jsonl:14` | vcs_write/jj:op | `jj op abandon --help` | correct — help |
| 58 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocOpLogGrowth-2.jsonl:14` | vcs_write/jj:util | `jj util gc --help` | correct — help |
| 59 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocPush-2.jsonl:49` | vcs_write/jj:git | `~/.local/bin/jj git push -h` | correct — help |
| 60 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocRecovery-2.jsonl:313` | vcs_write/jj:bookmark | `~/.local/bin/jj bookmark set --help` | correct — help |
| 61 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocWorktrees-2.jsonl:19` | vcs_write/jj:workspace | `~/.local/bin/jj workspace --help` | correct — help |
| 62 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocWorktrees-2.jsonl:24` | vcs_write/jj:git | `~/.local/bin/jj git init --help` | correct — help |
| 63 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocWorktrees-2.jsonl:24` | vcs_write/jj:workspace | `~/.local/bin/jj workspace add --help` | correct — help |
| 64 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:39` | vcs_write/jj:commit | `~/.local/bin/jj commit --help` | correct — help |
| 65 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:39` | vcs_write/jj:git | `~/.local/bin/jj git init --help` | correct — help |
| 66 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:39` | vcs_write/jj:rebase | `~/.local/bin/jj rebase --help` | correct — help |
| 67 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:44` | vcs_write/jj:bookmark | `~/.local/bin/jj bookmark set --help` | correct — help |
| 68 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:44` | vcs_write/jj:file | `~/.local/bin/jj file track --help` | correct — help |
| 69 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:44` | vcs_write/jj:git | `~/.local/bin/jj git push --help` | correct — help |
| 70 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:65` | vcs_write/jj:metaedit | `~/.local/bin/jj metaedit --help` | correct — help |
| 71 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjRevengerLaneJjState-2.jsonl:34` | vcs_write/jj:op | `jj op log --help` | correct — help |
| 72 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/KaidokuR18.ScoutJjColocation.jsonl:63` | vcs_write/jj:git | `/home/vgpnk/.local/bin/jj git colocation --help` | correct — help |
| 73 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/KaidokuR18/KaidokuR18.ScoutJjColocation.jsonl:84` | vcs_write/jj:git | `/home/vgpnk/.local/bin/jj git colocation --help` | correct — help |
| 74 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.CaseDryRunBash-3.jsonl:83` | vcs_write/git:add | `git add -h` | correct — help |
| 75 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.CaseDryRunBash-3.jsonl:83` | vcs_write/git:commit | `git commit -h` | correct — help |
| 76 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.CaseDryRunBash-3.jsonl:83` | vcs_write/git:push | `git push -h` | correct — help |
| 77 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.CaseDryRunBash-3.jsonl:83` | vcs_write/jj:git | `jj git push --help` | correct — help |
| 78 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.CaseHelpBash-3.jsonl:70` | vcs_write/jj:git | `jj git init --help` | correct — help |
| 79 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.CaseHelpDryRunEval-3.jsonl:97` | vcs_write/jj:commit | `jj commit --help` | correct — help |
| 80 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.CaseHelpDryRunEval-3.jsonl:97` | vcs_write/jj:git | `jj git push --help` | correct — help |
| 81 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ReopenGitSource.jsonl:81` | vcs_write/git:push | `git push -h` | correct — help |
| 82 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.RevSpecVcsHelp-3.jsonl:33` | vcs_write/git:add | `git -C /tmp/mado-r20-RevSpecVcsHelp add -h` | correct — help |
| 83 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.RevSpecVcsHelp-3.jsonl:33` | vcs_write/git:commit | `git -C /tmp/mado-r20-RevSpecVcsHelp commit -h` | correct — help |
| 84 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.RevSpecVcsHelp-3.jsonl:33` | vcs_write/git:push | `git -C /tmp/mado-r20-RevSpecVcsHelp push -h` | correct — help |
| 85 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.RevSpecVcsHelp-3.jsonl:62` | vcs_write/git:add | `git -C /tmp/mado-r20-RevSpecVcsHelp add -n -h` | correct — help |
| 86 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.RevSpecVcsHelp-3.jsonl:62` | vcs_write/git:commit | `git -C /tmp/mado-r20-RevSpecVcsHelp commit -n -h` | correct — help |
| 87 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.RevSpecVcsHelp-3.jsonl:62` | vcs_write/git:push | `git -C /tmp/mado-r20-RevSpecVcsHelp push -n -h` | correct — help |
| 88 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.RevSpecVcsHelp-3.jsonl:95` | vcs_write/git:commit | `git -C /tmp/mado-r20-RevSpecVcsHelp --help commit` | correct — help |
| 89 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.RevSpecVcsHelp-3.jsonl:109` | vcs_write/git:add | `git -C /tmp/mado-r20-RevSpecVcsHelp add -h` | correct — help |
| 90 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.RevSpecVcsHelp-3.jsonl:109` | vcs_write/git:commit | `git -C /tmp/mado-r20-RevSpecVcsHelp commit -h` | correct — help |
| 91 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.RevSpecVcsHelp-3.jsonl:109` | vcs_write/git:push | `git -C /tmp/mado-r20-RevSpecVcsHelp push -h` | correct — help |
| 92 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.RevSpecVcsHelp-3.jsonl:109` | vcs_write/jj:diff | `jj -R /tmp/mado-r20-RevSpecVcsHelp diff --stat -h` | correct — help |
| 93 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.RevSpecVcsHelp-3.jsonl:132` | vcs_write/git:add | `git -C /tmp/mado-r20-RevSpecVcsHelp add -n -h` | correct — help |
| 94 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.RevSpecVcsHelp-3.jsonl:132` | vcs_write/jj:diff | `jj -R /tmp/mado-r20-RevSpecVcsHelp diff --stat -h` | correct — help |
| 95 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScoutCorpusVcsNonWrites-3.jsonl:49` | vcs_write/git:add | `git add -h` | correct — help |
| 96 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScoutCorpusVcsNonWrites-3.jsonl:49` | vcs_write/git:pull | `git pull -h` | correct — help |
| 97 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScoutCorpusVcsNonWrites-3.jsonl:49` | vcs_write/git:rebase | `git rebase -h` | correct — help |
| 98 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScoutJjHelpEmpirical-3.jsonl:39` | vcs_write/jj:log | `jj log --help` | correct — help |
| 99 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScribeKnowledge-3.jsonl:27` | vcs_write/git:push | `git push -h` | correct — help |
| 100 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScribeKnowledge-3.jsonl:36` | vcs_write/jj:git | `jj git push --help` | correct — help |
| 101 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.SentinelPause20-3.jsonl:307` | vcs_write/git:push | `git -C /tmp/mado-r20-SentinelPause20/push-probe/clone push -h` | correct — help |
| 102 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.SentinelPause20-3.jsonl:307` | vcs_write/git:push | `git -C /tmp/mado-r20-SentinelPause20/push-probe/clone push -h` | correct — help |
| 103 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.SrcGitHelpSource-3.jsonl:75` | vcs_write/git:commit | `git commit --help` | correct — help |
| 104 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.HelperFailureWindows-5.jsonl:55` | vcs_write/jj:bookmark | `jj bookmark set --help` | correct — help |
| 105 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.HelperFailureWindows-5.jsonl:55` | vcs_write/jj:commit | `jj commit --help` | correct — help |
| 106 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.HelperFailureWindows-5.jsonl:55` | vcs_write/jj:rebase | `jj rebase --help` | correct — help |
| 107 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.HelperFailureWindows-5.jsonl:58` | vcs_write/jj:bookmark | `jj bookmark set --help` | correct — help |
| 108 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.JjEnvFacts-5.jsonl:13` | vcs_write/jj:config | `~/.local/bin/jj config path --help` | correct — help |
| 109 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.JjEnvFacts-5.jsonl:20` | vcs_write/jj:config | `~/.local/bin/jj config path -h` | correct — help |
| 110 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.ReopenJjAuthor-4.jsonl:25` | vcs_write/jj:metaedit | `jj metaedit --help` | correct — help |
| 111 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.SrcJjMetaedit-5.jsonl:28` | vcs_write/jj:commit | `jj commit --help` | correct — help |
| 112 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MoriR17/MoriR17.SrcJjMetaedit-5.jsonl:28` | vcs_write/jj:metaedit | `jj metaedit --help` | correct — help |
| 113 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X03DefectProbes.jsonl:52` | vcs_write/jj:git | `jj git init --help` | correct — help |
| 114 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X03DefectProbes.jsonl:61` | vcs_write/jj:bookmark | `jj bookmark --help` | correct — help |
| 115 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X03DefectProbes.jsonl:61` | vcs_write/jj:commit | `jj commit --help` | correct — help |
| 116 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X03DefectProbes.jsonl:288` | vcs_write/jj:bookmark | `jj bookmark set --help` | correct — help |
| 117 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:53` | vcs_write/jj:edit | `jj edit --help` | correct — help |
| 118 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:53` | vcs_write/jj:git | `jj git init --help` | correct — help |
| 119 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKagi.jsonl:74` | vcs_write/jj:describe | `~/.local/bin/jj describe --help` | correct — help (same key still reported) |
| 120 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKake.jsonl:84` | vcs_write/jj:commit | `~/.local/bin/jj commit --help` | correct — help (same key still reported) |
| 121 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocLargeRepo-2.jsonl:141` | vcs_write/jj:st | `/home/vgpnk/.local/bin/jj st --help` | correct — help (same key still reported) |
| 122 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocOpLogGrowth-2.jsonl:105` | vcs_write/jj:debug | `jj debug reindex --help` | correct — help (same key still reported) |
| 123 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjDocOpLogGrowth-2.jsonl:116` | vcs_write/jj:git | `jj git push --help` | correct — help (same key still reported) |
| 124 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjLaneHelper-3.jsonl:68` | vcs_write/jj:metaedit | `~/.local/bin/jj metaedit --help` | correct — help (same key still reported) |
| 125 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScoutJjHelpEmpirical-3.jsonl:39` | vcs_write/jj:st | `jj st --help` | correct — help (same key still reported) |
| 126 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScribeKnowledge-3.jsonl:27` | vcs_write/git:commit | `git commit -h` | correct — help (same key still reported) |
| 127 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.SrcGitHelpSource-3.jsonl:68` | vcs_write/git:commit | `git commit -h` | correct — help (same key still reported) |
| 128 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.SrcGitHelpSource-3.jsonl:82` | vcs_write/git:commit | `git commit --help` | correct — help (same key still reported) |
| 129 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.SrcGitHelpSource-3.jsonl:97` | vcs_write/git:commit | `git commit -h` | correct — help (same key still reported) |
| 130 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.C03FleetJjPractice.jsonl:80` | vcs_write/jj:git | `jj git init --help` | correct — help (same key still reported) |
| 131 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jProbeKengaku.jsonl:90` | vcs_write/git:push | `git push --dry-run` | correct — dry run |
| 132 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjRevengerLaneJjState-2.jsonl:165` | vcs_write/git:add | `git add -A --dry-run` | correct — dry run |
| 133 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/JjRevengerLaneJjState-2.jsonl:165` | vcs_write/git:commit | `git commit -a --dry-run --short` | correct — dry run |
| 134 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.CaseAdoptW2-3.jsonl:118` | vcs_write/git:commit | `git commit --dry-run -m x` | correct — dry run |
| 135 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.CaseAdoptW2-3.jsonl:121` | vcs_write/git:add | `git add -n newfile1` | correct — dry run |
| 136 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.CaseAdoptW2-3.jsonl:121` | vcs_write/git:commit | `git commit -a --dry-run --short` | correct — dry run |
| 137 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.CaseAdoptW2-3.jsonl:121` | vcs_write/git:push | `git push --dry-run` | correct — dry run |
| 138 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.ScribeKnowledge-3.jsonl:36` | vcs_write/git:add | `git add -n nf` | correct — dry run |
| 139 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.SrcGitHelpSource-3.jsonl:75` | vcs_write/git:commit | `git commit --allow-empty -m --help --dry-run` | correct — dry run |
| 140 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/SoujiR17-3/SoujiR17-3.RevengeStubOrigin.jsonl:32` | vcs_write/git:add | `git add --dry-run -n tests/vault/vadv54-run/p/p6repo` | correct — dry run |
| 141 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.CaseWrapperForms-3.jsonl:120` | package_query/pacman:-Q | `pacman -Q` | correct — pure data |
| 142 | `2026-10-14T23-10-28-508Z_01a13cae-749c-7300-bea2-c15efc22cf7a/OomClassTaxonomy.jsonl:130` | live_probe/journalctl | `journalctl --user -b -g dumped core --case-sensitive=true -o json --output-fields=MESSAGE,MESSAGE_ID --no-pager -q` | NOT LOST — real command, same key still reported |
| 143 | `2026-10-19T20-36-43-523Z_01a155e1-7d83-74e9-8383-9ee7c15d7c99/W2jScribe.jsonl:93` | vcs_write/jj:op | `jj op log --no-graph -n 1 -T id.short()` | NOT LOST — real command, same key still reported |
| 144 | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/TameshiR18/TameshiR18.X06DispositionGuards.jsonl:93` | vcs_write/jj:log | `jj log --no-graph -r all() -T commit_id.short() ++ " " ++ bookmarks ++ "\n"` | NOT LOST — real command, same key still reported |

## Limits

- [INFERENCE] Corpus liveness: 5,978 files at scan time; running seats may append. All 144 rows were re-verified by rescanning the 49 files that contain them after the full sweep (0 mismatches), so those rows were stable at the line level.
- I did not run the committed `corpus-diff.py` over the corpus (a sibling w2 seat owns the whole-corpus no-harm diff; running it would duplicate an ~20-minute serial scan). My key-level numbers replicate its row key from its source; [UNK] only whether its stable-file filter drops any of the 49 (none changed during my two passes).
- Baseline is the ticket's 1f7f995→28c6837 delta. The pre-harm 9c54c56→28c6837 direction was not scanned here.
- `journalctl` and `pacman` were not executed (host pause forbids both); those two rows were adjudicated from transcript data and code semantics.
- jj/git controls ran in /tmp with HOME/XDG/JJ_CONFIG and git config redirected; jj 0.45.1, git 2.56.0, matching the versions in the corpus rows. A handful of `-C` targets were created as empty non-repos to reproduce the removed invocations.
- The duplicate `observed`+`lead` rows noted above are additions, not removals, and are outside this audit's falsification scope.

## Installs

none.
