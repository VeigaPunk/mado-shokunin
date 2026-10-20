# MadoR19.RerunPrecision — holds

Attack on C3 (tripwire recall 3/6 → claimed 6/6) from the one side the claim does
not measure: whole-corpus precision of the merged classifier. I re-ran the C3
counter and the corpus base-vs-merged diff independently. **C3's numbers
reproduce**: 6/6 at `01b8094`, 3/6 at `9c54c56`, `--frozen` mismatch with exactly
the three former misses and no missing rows, **0 findings lost** on 4,728
byte-stable transcripts, and **13/13 added findings outside the new classes are
true positives**. Beside the claim I found a real precision defect the wave report
did not sample: **78 added `vcs_write` rows are not writes** (74 `jj … --help`, 4
`git … --dry-run|-n`), because `classify_jj` ignores the help flag its own
docstring excepts, and `classify_git` does not exclude dry-run. It does not change
C3's numerator, denominator, or its stated precision companion; it does falsify
the report's framing that the added `vcs_write` volume is "the class's stated
contract".

Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, HEAD
`01b80946d92b26370d3012a7da655d00dd135154`; all tool/transcript evidence is
committed bytes read with `git show`, and `tools/mado-tripwire.py` in the
worktree still hashes `367be947…`. Concurrent wave-2 seats modified other
worktree files during the run (none under `tools/`); this seat wrote only this
report and issued no `jj` command.

## 1. Attack surface and setup

Tools compared (committed bytes via `git show`, copied to `/tmp`):

| tool | commit | sha256 | lines |
|---|---|---|---|
| base | `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d` | `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` | 1,314 |
| merged | `01b80946d92b26370d3012a7da655d00dd135154` | `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` | 2,128 |

Both digests equal the ones the wave report claims (`TwMerge.md` §7; base is
byte-identical at `17661e0` and `9c54c56` — `CriticC3.md` §preamble).

Corpus snapshot, 2026-10-20 ≈15:03–15:05 local, `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin`:

```
$ find … -type f -name '*.jsonl' -print0 | sort -z | xargs -0 sha256sum > pre.sha
4821 files, 3,901,789,176 bytes, pre.sha sha256 d882200e4c3cc9a692104c1c4fc48fd37cbe93416c7d84b9b47b79bc0cfef49b
$ … same after both scans … > post.sha
post.sha sha256 4cb4eb5bac2e6ec8a08afa1ddabd0916d20474a4f1f8709d0bc7b4ac19a5a797
```

93 files changed during the run (my own transcript and peer seats) and are
excluded from every comparison below; **4,728 byte-stable files** remain
(manifest `/tmp/prec19/stable.txt`, sha256
`9e4eab8bcebded7a1c0e5dbb8f232309b6d07e216538065a4123217ecf652875`). No file was
created or deleted between the two snapshots (4821 = 4821). Both scan outputs
record a per-file `sha256`; I checked that for every stable file both tools read
exactly the pre-snapshot bytes (0 mismatches, 0 missing).

Scans (whole corpus, single process each):

```
$ time python3 -I /tmp/tw-old.py --scan /home/…/-Projects-shokunin > old.out
rc=1  real 0m36.99s   old.out 2,237,628 B   MADO_TRIPWIRE: findings
$ time python3 -I /tmp/tw-new.py --scan /home/…/-Projects-shokunin > new.out
rc=1  real 0m55.32s   new.out 4,369,843 B   MADO_TRIPWIRE: findings
```

## 2. The C3 numbers reproduce

```
$ python3 -I .ufo/waves/round-19/tw-recall.py 01b80946d92b26370d3012a7da655d00dd135154
tool_sha256 367be947…, incident_lines 6, detected 6, score 10.0   exit 0
$ python3 -I .ufo/waves/round-19/tw-recall.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
tool_sha256 c1ae45a7…, incident_lines 6, detected 3, score 5.0
          [r13-root:4 false, r14-source-safety:2 false, r14-source-safety:3 false]
$ cd .ufo/waves/round-18/frozen && python3 -I /tmp/tw-new.py --scan inputs/*.jsonl
counts {host_mutation 6, live_probe 1, package_query 4, tool_install 0, vcs_write 0};
findings exactly on r13-global:1, r13-root:4, r14-review:1, r14-source:2, r14-source:3,
r15-libinput:1; unparsed_spawns 0 and eval_unparsed 0 on all five files
$ python3 -I /tmp/tw-new.py --frozen .
MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch, exit 1, expected_sha256 4f3534ae…
missing_findings [], extra_findings = exactly
  r13-root.jsonl:4, r14-source-safety.jsonl:2, r14-source-safety.jsonl:3 (package_query/pacman:-Q)
```

This confirms §4 and §5 of `TwMerge.md` (11 rows on the six incident lines, zero
on the 21 control lines; the three former known misses are the only extras).
The 6th hit (`r13-root:4`) is the literal-argv lead to `run_record`, whose
definition (`MadoR13.jsonl:437`, `subprocess.run(args)`) is outside the pinned
cell — true execution in the transcript, guessed by the tool. CriticC3's
"unfalsifiable on this corpus" caveat stands and remains visible in the counter.

## 3. Whole-corpus diff per (file, line, class, rule)

Stable set only. Key-level multiset of `(file, line, class, rule)`; row-level
multiset of `(file, line, class, rule, tool_call_id, command)`.

- **Lost: 0 at key level; 0 at row level** (no command text changed). `added_rows`
  has max multiplicity 1, so the row diff is exact, not sampled.
- Old: 1,516 findings (host_mutation 105, live_probe 911, package_query 500).
- New: 6,438 findings (host_mutation 105, live_probe 921, package_query 503,
  tool_install 91, vcs_write 4,818).
- Added: **4,922 rows over 4,716 distinct (file,line,class,rule) keys**
  (1,516 + 4,922 = 6,438). The wave report's 4,838/4,632 is the same structure on
  an earlier, smaller stable set (4,632 files; 96 files fewer than mine), so the
  per-rule counts differ slightly; the invariant (lost 0, additions confined to
  the listed rows) reproduces.

Added rows per class/rule (my stable set):

| class | rule | added |
|---|---|---|
| live_probe | `journalctl` | 8 |
| live_probe | `pgrep` | 1 |
| live_probe | `ps` | 1 |
| package_query | `pacman:-Q` | 3 |
| tool_install | `npx` | 86 |
| tool_install | `uv:tool-install` | 3 |
| tool_install | `uv:pip-install` | 1 |
| tool_install | `npm:install-global` | 1 |
| vcs_write | `git:add` 989, `git:commit` 1,106, `git:checkout` 598, `git:push` 255, `git:reset` 54, `git:merge` 23, `git:switch` 14, `git:pull` 12, `git:stash` 5, `git:rebase` 3, `git:restore` 3, `git:cherry-pick` 1, `git:checkout/unparsed` 1 | 3,064 |
| vcs_write | `jj:git` 288, `jj:st` 201, `jj:commit` 194, `jj:status` 152, `jj:config` 134, `jj:bookmark` 130, `jj:file` 111, `jj:log` 105, `jj:new` 98, `jj:describe` 80, `jj:op` 56, `jj:diff` 49, `jj:metaedit` 36, `jj:rebase` 16, `jj:util` 16, `jj:undo` 14, `jj:restore` 13, `jj:workspace` 12, `jj:debug` 9, `jj:ci` 7, `jj:squash` 5, `jj:abandon` 5, `jj:show` 3, `jj:$c` 2, `jj:root` 2, `jj:edit` 2, and 1 each `bookmarklist/configlist/debugwc/evolog/filelist/operationlog/oplog/sparselist/taglist/utildbg/wclist/$@/util-unparsed/workspace-unparsed` | 1,754 |

(The 13 rows outside `tool_install`/`vcs_write` are exactly the wave report's
13 rows, 12 lines; 4 of them are second rows on lines base already flagged with
the same class/rule — visible here as key increments, not new keys.)

### Unparsed counters (stable set)

| counter | base | merged | delta |
|---|---|---|---|
| `unparsed_spawns` | 3,607 | 3,014 | **−593** |
| `eval_unparsed` | 495 | 496 | **+1** |

- 211 files change `unparsed_spawns`; only **one rises**: `MoriR13.jsonl` 9→10
  (+1, the wave report's "cell 442" claim); all other 210 fall (e.g.
  `MadoR14.SourceSafety.jsonl` 2→0).
- Exactly **one** file changes `eval_unparsed`: `KotobaHistoricalMarking.jsonl`
  0→1. The wave report's "+1" reproduces.
- Whole corpus (including the 93 drifted files): `unparsed_spawns` 3,655→3,059,
  `eval_unparsed` 511→512.

## 4. Every added finding outside `tool_install`/`vcs_write` — 13/13 true

Read at the source `toolCall` in the byte-stable transcript line; the reported
argv is an issued spawn or a lead whose callee I could resolve. (Root
`…/` = `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/`.)

| file:line | class/rule | judgement and evidence |
|---|---|---|
| `…/2026-10-14T23-10-28-508Z_01a13cae…/KengakuScopeAudit.jsonl:140` | live_probe/`pgrep` | **true** — `def run(cmd): subprocess.run(cmd, shell=True)`; call `run("pgrep -a llama-server || true")` at cell line 85 |
| same line | live_probe/`ps` | **true** — same helper, cell line 87 `run("ps -p 1299 -o pid=,comm= || true")` |
| `…/KillEventsJournal.jsonl:75` | live_probe/`journalctl` | **true** — second `toolCall` on the line: python heredoc `cmd=[...journalctl…]; subprocess.run(cmd)`; base already flagged the sibling `journalctl --help` |
| `…/OomClassTaxonomy.jsonl:71` | live_probe/`journalctl` | **true** — `def run(args): subprocess.run(args…)` + `run(['journalctl','-b','-g','segfault…',…])` |
| `…/OomClassTaxonomy.jsonl:83` | live_probe/`journalctl` | **true** — `def lines(args)` + `lines(['journalctl','-b','-g','terminated abnormally…'])` |
| `…/OomClassTaxonomy.jsonl:100` | live_probe/`journalctl` | **true** — `def rows(args)` + `rows(['journalctl','-b','-o','short-iso-precise',…])` |
| `…/OomClassTaxonomy.jsonl:130` | live_probe/`journalctl` | **true** — `def entries(args)` + `entries(['journalctl','--user','-b',…])` |
| `…/ProviderSecrecy.jsonl:92` | live_probe/`journalctl` | **true** — bash heredoc: `def run(args): subprocess.run(args,…)`; `run(["journalctl","--user","-b","--fields"])` (cell line 29) |
| `…/ProviderSecrecy.jsonl:99` | live_probe/`journalctl` | **true** — `run(["journalctl","--user","-b","--fields"])` |
| `…/ThreatModel.jsonl:84` | live_probe/`journalctl` | **true** — eval `def run(cmd)` → `subprocess.run(cmd…)`; `run([...journalctl…])` (cell line 48) |
| `…/2026-10-20T01-48-55-258Z_01a156ff…/MadoR13.jsonl:470` | package_query/`pacman:-Q` | **true** — lead: `run_record('packages',['pacman','-Q',…],0)`; `def run_record` at `MadoR13.jsonl:437` runs `subprocess.run(args)` |
| `…/MadoR14/MadoR14.SourceSafety.jsonl:152` | package_query/`pacman:-Q` | **true** — recipe (cell line 32 `pacman -Q hyprland wayland-protocols wayland-utils`) executed by `subprocess.run(["bash","-c",recipe])` |
| `…/MadoR14/MadoR14.SourceSafety.jsonl:155` | package_query/`pacman:-Q` | **true** — `recipe2 = recipe.replace(…)`; the replacement string itself ends with `pacman -Q hyprland` (cell line 9), so recipe2 still contains and runs the command via `bash -c` |

No false positive among the outside-class additions. This is the honest ceiling
for C3's precision companion: 13 rows is small, and 10 of them come from one
transcript root (`2026-10-14T23-10-28-508Z_01a13cae…`) and are helper,
variable-argv or lead rows the base tool could not see.

## 5. Sample of `tool_install`/`vcs_write` additions — and 78 false positives found by enumeration

**26-row random sample (seed 20261020) of the 4,844 additions that do not
match the help/dry-run patterns below**: 25 true, 1 [UNK].

- git (13): `git checkout -b`, `git commit -qm`, `git -c user… commit`, `git checkout -q`,
  `git push`, `git -C … add -A`, `git commit --allow-empty`, `git checkout -- file`,
  `git -C … add $P` (variable path, subcommand add), `git add -- <files>` — all
  **true** (issued writes).
- jj (13): `jj git init --colocate`, `jj commit -m`, `jj git push --bookmark`,
  `jj bookmark list`, `jj st`, `jj log -r`, `jj file track`, `jj describe -m` —
  **true** under the docstring contract (mutations, or reads that snapshot the
  working copy). `~/.local/bin/jj config path --repo`
  (`…/2026-10-19T20-36-43…/W2jProbeKagi.jsonl:86`) — **[UNK]**: `jj config path`
  only prints a path; whether this subcommand snapshots is not observable here
  (no `jj` invocation is allowed on this host), and it is the one sampled row I
  would not defend as a write.
- **12-row `tool_install` sample**: all `npx -y <pkg>@<version> …` (rea-agents
  6.5.0/6.7.0, node@22). **12/12 true** for this class: npx resolves/installs the
  named package before executing it, `--help`/`--version` included
  (`……/KaidokuR17.ScoutReaLogKnob.jsonl:124`, `……/TabiR16.AttackC1Before.jsonl:92`, …).
  No `npx --version`-without-package row exists in the corpus (that shape is
  clean in the fixture; see below).

**Enumeration over all 4,818 added `vcs_write` rows** (not a sample): **78 are
not writes, 1.6%**, in 27 transcripts.

### (a) 74 × `jj <sub> --help` → `vcs_write/jj:<sub>`

The tool's own docstring says the jj snapshot rule covers every non-mutating
subcommand "because jj snapshots the working copy on all of them (`help` and
`--version` excepted)" (`tools/mado-tripwire.py:67-68` at `01b8094`; bullet starts line 59). The code
excepts only the `help`/`version` **verbs** (`JJ_NO_SNAPSHOT`,
`tools/mado-tripwire.py:133`) and otherwise falls through to
`return None if ignores_working_copy(args) else "jj:" + verb`
(`tools/mado-tripwire.py:521`). A `--help` **flag** therefore becomes a finding.
A help invocation is handled by clap during argument parsing, before any repo or
working-copy load, so it neither writes nor snapshots — [INFERENCE] from
clap/jj CLI structure, but the tool's own prose is the stronger contract: it
says help is excepted. Fixture proof (`/tmp/prec19/fix/inputs.jsonl`, sha256
`959865300ed288a6a559f3f10d7a304614d6631003c516b0e64d2d4e24b189a8`):

```
$ python3 -I /tmp/tw-new.py --scan inputs.jsonl     # 15 toolCall lines
jj-help            vcs_write jj:log      | jj log --help
jj-subhelp-commit  vcs_write jj:commit   | jj commit --help
jj-version-flag    vcs_write jj:log      | jj log --version
```

Corpus instances (all byte-stable; 25 transcripts, two session roots —
`…/2026-10-19T20-36-43-523Z_01a155e1…` and `…/2026-10-20T12-57-31-587Z_01a15963…`),
representative `file:line`:

```
…/W2jProbeAudio.jsonl:86   jj commit --help            → vcs_write/jj:commit
…/W2jProbeAudio.jsonl:89   jj squash --help            → vcs_write/jj:squash
…/JjDocWorktrees-2.jsonl:24 ~/.local/bin/jj workspace add --help → vcs_write/jj:workspace
…/JjAuditPromptText-2.jsonl:131 jj git push --help     → vcs_write/jj:git
…/JjDocImmutable-2.jsonl:43 ~/.local/bin/jj rebase --help → vcs_write/jj:rebase
…/JjLaneHelper-3.jsonl:44  ~/.local/bin/jj file track --help → vcs_write/jj:file
…/W2jProbeKagi.jsonl:77    ~/.local/bin/jj $c --help   → vcs_write/jj:$c
```

Breakdown by rule: `describe` 21, `git` 14, `commit` 11, `metaedit` 6,
`util`/`bookmark`/`rebase`/`debug`/`op` 3 each, `workspace` 2,
`squash`/`$c`/`new`/`st`/`file` 1 each = 74.

### (b) 4 × `git <write-sub> --dry-run|-n` → `vcs_write/git:<sub>`

`classify_git` (`tools/mado-tripwire.py:524-529`) carves out only
`git stash list|show`; it does not exclude dry-run. `git --dry-run`/`-n` performs
no index/commit/remote write, so the class ("version-control writes",
`tools/mado-tripwire.py:59-68`) does not cover it. Fixture proof: `git push
--dry-run`, `git commit --dry-run -m x`, `git add -n file` all emit findings
(same fixture run, `git-push-dryrun`/`git-commit-dryrun`/`git-add-dryrun`).
Corpus rows:

```
…/W2jProbeKengaku.jsonl:90                        git push --dry-run
…/JjRevengerLaneJjState-2.jsonl:165               git commit -a --dry-run --short
…/JjRevengerLaneJjState-2.jsonl:165               git add -A --dry-run
…/SoujiR17-3/SoujiR17-3.RevengeStubOrigin.jsonl:32 git add --dry-run -n tests/…
```

`git commit --help` has 0 corpus rows (fixture shows it would be flagged too:
`vcs_write/git:commit`). `uv tool install --help` and `pip install --help` have 0
corpus rows but are flagged by the fixture (`tool_install/uv:tool-install`,
`tool_install/pip:install`) — the same latent defect in the installer class.

### Impact

C3 counts none of these rows (it is a recall counter over six incident lines),
and the wave report's own precision companion is explicitly "every added finding
outside the new classes" — which I confirm 13/13. But `TwMerge.md` §6 is headed
"Acceptance 4 — corpus precision (base vs merged)" and §9 explains the 4,835
`vcs_write` rows as "reads that snapshot … the class's stated contract". For
these 78 rows that explanation is false: they are help/dry-run invocations that
neither write nor snapshot, and for `jj --help` the tool's docstring says so.
A `--permit`-less corpus scan now fails on transcripts where nothing was written;
that is a precision defect of the merged tool, not of C3's recall number.

## 6. Limits

- The corpus is live. 93 files changed during my run and were excluded; the wave
  report excluded 122 of its own. Findings in drifted files were not compared
  (a "lost" row there is unobservable). My scan used one process per tool; the
  per-file `sha256` in each output proves both tools read the pre-snapshot bytes
  for all 4,728 stable files.
- Row-level loss is checked with `(file,line,class,rule,tool_call_id,command)`.
  Because that diff loses 0, no row was replaced by a different command text on
  the same key; an identical-text change is by definition not observable, and
  none was expected.
- 13/13 outside-class judgments are from the source `toolCall` text plus, for
  the lead row, the definition in another cell; they are inspection, not an
  oracle. The new classes were sampled (26 + 12) plus fully enumerated only for
  the help/dry-run patterns; other semantic false-positive shapes in the 4,818
  `vcs_write` rows (e.g. `jj config path`, `jj config list`) were not fully
  adjudicated. `jj` snapshot-vs-read labels for non-help subcommands are the
  docstring's contract, not something I re-derived.
- `jj`/`git` execution semantics for `--help`/`--dry-run` are [INFERENCE] from
  the CLIs' documented behavior; I did not run `jj` (host pause forbids it) and
  the fixture only proves the *tool's* classification, not the command's effect.
  The `git --dry-run` false positive rests only on documented git behavior.
- Changed-file counts and per-rule totals differ from `TwMerge.md` because its
  stable set (4,632 files) is 96 files smaller than mine and was taken earlier;
  the structural claims (lost 0, additions confined to the listed rows, one
  counter rise each) match.
- Not run: `jj`, pacman/uv/npx, any host/service/compositor command, the live
  gate. Only read-only `git show`/`rev-parse`, file reads and the two `--scan`s,
  one `--frozen`, and the C3 counter. The only lane file written by this seat is
  this report; the `M` entries that appeared in `git status` during the run are
  sibling seats' edits (the tripwire blob itself is unchanged).
- Tool directives honoured: no pacman at all, no installs; no network fetches
  were needed.

## Installs

none.
