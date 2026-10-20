# ScoutCorpusLeads — the real corpus holds 36 rule-B hits in 3 eval-cell groups: 2 emitted rows are *observed* (cross-cell spawning helpers), 33 are pure-data `RuntimeError(argv)` hits that dedup shadows; zero leads

Seat `MadoR20.ScoutCorpusLeads-3`. Question answered: every eval line where the harmed
tool (e629f73, `tools/mado-tripwire.py` sha256 `367be947…`) emits a row from HelperFn
rule B (`helper_argv_leads`: bare `ast.Name` callee, no same-cell `def`, name not in
`PURE_ARG_CALLS`, handed a literal `['prog', …]` argv that classifies as a host command),
plus, for each callee, what the same transcript says about an earlier cross-cell
definition, and the resulting verdict under E1–E3.

Corpus scanned: `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin` (read-only, data
only). **5,714 `.jsonl` files / 6,272 eval cells / 241 bare-name literal-argv call sites /
18 distinct callees / 36 rule-B hits.** The corpus is live: it grew 5559 → 5623 → 5714 files
during the session; the final numbers above are the 2026-10-20T19:54Z reading, and every
result below was stable across all three readings.

## 1. Rule-B rows that are actually emitted (2 rows, both with an executed cross-cell spawning body → E1 `observed`)

| # | file (transcript) | jsonl line | code line | callee | argv handed to it | earlier cross-cell definition | E1/E2/E3 verdict | emitted row at e629f73 / at 9c54c56 |
|---|---|---|---|---|---|---|---|---|
| 1 | `…/2026-10-20T01-48-55-258Z_01a156ff…/MadoR13.jsonl` | 470 | 3 | `run_record` | `['pacman','-Q','wayland-utils','wayland','wayland-protocols','hyprland']` | **visible spawning body**: same file, eval cell at jsonl **437**, code line 4 `def run_record(name,args,expected=None,stdin=None,extra_env=None,timeout=300)`, body code line 6 `subprocess.run(args, cwd=root, …, capture_output=True, timeout=timeout, …)`; the literal list is the 2nd positional → parameter `args` → reaches the spawn | **E1 → `observed`** (body visible in an earlier py eval cell, no reset between: every cell in 437…470 carries `reset=False`; E3: only binding is that def; E2 n/a: body spawns). Execution corroborated: toolResult at jsonl 472 prints `packages exit 0 expected 0` with the pacman output. | emitted / **absent** (file scans `clean` at 9c54c56) |
| 2 | `…/2026-10-20T12-57-31-587Z_01a15963…/MadoR18/MadoR18.CriticC2W2.jsonl` | 56 | 4 and 9 (two identical hits, one row after dedup) | `run` | `['git','checkout','-q','4c103b55b1ea5c3c555884afe3eb69b5189701b7']` | **visible spawning body**: same file, eval cell at jsonl **53**, code line 4 `def run(cmd,**k): return subprocess.run(cmd,cwd=C,text=True,capture_output=True,**k)`; argv is the 1st positional → `cmd` → reaches the spawn | **E1 → `observed`** (earlier py eval cell, no reset: all cells `reset=None`; E3: no other binding of `run` in the file — AST check over every eval cell). Execution corroborated: the checkout runs inside the same cell and the cell's result (jsonl 58) shows the measured commit `4c103b5`. | emitted / **absent** (file scans `clean` at 9c54c56) |

Both rows are *true positives* in the verdict sense (the command was issued through a
wrapper whose body is in the transcript). The harm the round-19 lesson describes is
visible here in its minimal form: e629f73 emits them as ordinary findings with **no
`evidence` key**, where E1 requires `observed`. A round-20 tool must keep both rows and
label them `observed` — demoting them to `lead` would mislabel two executed commands, and
dropping them would fail the whole-corpus no-harm comparison against e629f73.

Mechanism, verified in source: `funcs` in `classify_eval` is built from **same-cell**
`ast.FunctionDef` nodes only (tool-e629f73.py:1368-1372), so a helper defined in an
earlier cell of the same py kernel is invisible to `spawn_scan`'s `helper is not None`
branch (tool-e629f73.py:1411-1419) and falls into the rule-B lead branch
(tool-e629f73.py:1431-1433). This is exactly the cross-cell hole E1 closes.

## 2. Rule-B hits that never surface as emitted rows (33 hits, 5 eval cells, all `RuntimeError`)

| file | jsonl lines (eval cells) | code line of the `raise` | callee | argv (literal, bound from the caller's `run([...])`) | cross-cell definition | E1/E2/E3 verdict |
|---|---|---|---|---|---|---|
| `…/TameshiR18/TameshiR18.X06DispositionGuards.jsonl` | 60, 81, 87, 93, 96 | 11, 9, 8, 8, 8 | `RuntimeError` | 33 hits: `['git','add','-A']`, `['git','commit','-qm',…]`, `['jj','log','--no-graph',…]`, `['jj','file','track',…]`, `['jj','diff','--summary']`, `['jj','metaedit','--update-author']`, `['jj','commit','-m',…]` | **builtin, no body**: AST check over every eval cell of the file finds no `def`/assignment/import/`del`/`global` of `RuntimeError` (E3 clean) | **E2 → no row** (Python builtin not rebound: constructing an exception instance is provably pure data). E1 does not apply — the callee has no executable body, so nothing executes the argv. |

The shape in the transcript: each cell defines `def run(argv, check=True)` **in the same
cell** and ends it with `if check and p.returncode: raise RuntimeError(argv)`; the caller
hands `run([...])` a literal argv, `bind_literal` binds `argv` inside the helper body, and
rule B then classifies `RuntimeError(argv)` as if the argv were the callee's command.

Why no row difference appears: within each tool call, the helper's own
`subprocess.run(argv, …)` (visited earlier in BFS walk order than the `raise`) already
emits the same `(class, rule)`, and `scan_file` dedups on `(cls, rule)` per tool call
(tool-e629f73.py:1590-1596). Consequence, measured: disabling `helper_argv_leads` changes
**nothing** in this file (26 rows with and without rule B; same for lines 60/81/87/93/96).
So the pure-data harm is *latent* in the emitted output here — it is real in hit
generation and would become visible output the moment dedup order changes or the same
argv is raised without an accompanying `run([...])` call.

This is the corpus analogue of the round-19 harm instance `frozenset(['pacman','-Q',…])`:
`frozenset` never becomes a bare-name literal-argv site here (it is not among the 18
callees; the 95 files that merely *mention* the text carry it as fixture strings /
toolResult prose), and an AST census of all eval code finds only 5 real `frozenset(...)`
calls, none with a literal list of strings (`frozenset()`, two `frozenset(args.keys())`,
two `frozenset({...})`), so none could produce a row. By contrast, `RuntimeError([...])`
is a real call shape: 87 bare-name sites, 33 of them classifying. E2 must therefore exempt builtins generally (not just the 31
names in `PURE_ARG_CALLS`), or this file's hit stream stays wrong even though its emitted
row set is unchanged.

## 3. The other 15 callees (no row possible)

241 bare-name literal-argv call sites across 18 callees. Besides the three above:
`run_receipt` 18, `save_capture` 16, `receipt_run` 16, `soup` 14, `record_command` 6,
`runcheck` 4, `redispatch` 3, `run_check` 3, `fix_agent_task` 2, `record_run` 2, `cap` 1,
`sh` 1, `find` 1, `witness_detector` 1, `soup0` 1. Their argv0 values are
`python3|node|bash|/home/vgpnk/Projects/shokunin/scripts/sources-census.sh|sha256sum|…`,
i.e. none classifies as a host command, so `helper_argv_leads` returns `[]` and no row is
produced at any revision.

Measured cross-cell (AST check over every eval cell of each transcript): 14 of the 18
callees have a definition visible in an earlier — or, for one `redispatch`
(`W2RoundMori.jsonl:152`), the same — cell of their own transcript
(`run_record`, `run`, `record_command`, `runcheck`, `run_check`, `run_receipt`,
`receipt_run`, `save_capture`, `record_run`, `cap`, `sh`, `redispatch`,
`fix_agent_task`, `witness_detector`), so had their argv classified as host commands the
rows would be E1 `observed`, never `lead`. No visible definition exists for `RuntimeError`
(builtin, §2), for `find`/`soup`/`soup0` (11 sites; argv such as
`['size','path','bytes',…]`, `['script','style','noscript']` — element-name selectors, not
programs), and for `run` in `FleetIdentityAudit.jsonl` jsonl lines 37/40/46 (13 sites whose
argv are git **reads**: `rev-parse`, `status`, `config --list`, `log`, `diff --stat`,
`ls-files` — E4/`classify_git` produces no row for any of them). That is the only
"body not visible" helper shape in the corpus, and none of its argv classifies.

**Lead count in the real corpus: 0.** Every rule-B hit whose callee has a non-builtin
body resolves to a visible spawning body (E1 `observed`); the remainder are builtins
(E2). The nearest lead shape (`run` with no visible body in `FleetIdentityAudit.jsonl`)
hands only git reads, which classify as nothing. The lead path (E1's "body not visible"
with a host-command argv) is exercised only by suite cases, not by this corpus.

## 4. Adjacent contradiction with the round-20 contract (not rule B — reported because E4 is contradicted empirically)

`TameshiR18.X06DispositionGuards.jsonl` jsonl line 53 (two bash tool calls
`jj git init --help` and `jj edit --help`) is reported by e629f73 as
`vcs_write jj:git` and `vcs_write jj:edit`. E4 says no `vcs_write` row for
`jj ... -h|--help` **as a flag**, and `--help` is the last token in both. Source cause:
`classify_jj` (tool-e629f73.py:503-521) only exempts help when `first_verb` is None
(`jj --help` / `--version`); a subcommand-bearing help form falls through to
`"jj:" + verb` / `jj:git`. Two corpus rows contradict E4 as written. (Bash cell, so
independent of rule B; the round-20 E4 implementation and its suite need to cover
`jj <sub> --help` and `jj git <sub> --help`, not just `jj --help`.)

## 5. Method and reproducibility

- Tool copies: `git -C …/mado-shokunin show <rev>:tools/mado-tripwire.py > /tmp/ScoutCorpusLeads-3/tool-<rev>.py`
  - `e629f73` and `1f7f995` → sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` (byte-identical)
  - `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d` → sha256 `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`
  - isolation copy with `helper_argv_leads` returning `[]` → sha256 `94e4160025775f1aa5b2229541637e067d22549f7205e4f44f5afdaf424f2efc`
- Attribution: instrumented load of the stock module whose `helper_argv_leads` records
  `(jsonl_line, code_line, callee, argv, hits)` and returns the same hits; the only call
  site of `helper_argv_leads` is the rule-B branch (verified by source read). A
  line-tagged replica of `scan_file`'s record loop produced findings **identical to the
  tool's own `scan_file` for every file** (0 divergences over 5714 files; tuple key
  `(line, class, rule, tool, tool_call_id)`).
- Positive control: the harness records the rule-B row in
  `.ufo/waves/round-19/tripwire/r19-helperfn/py-lead-cross-cell-literal.jsonl`
  (`run_record(['pacman','-Q',…])` → `package_query pacman:-Q`, matching the stock
  tool's single finding), so the zero-lead corpus result is not a broken interceptor.
- Isolation experiment (the prescribed one): full-corpus scan at e629f73 vs the
  rule-B-disabled copy → **exactly 2 files differ**, each by one row
  (`MadoR13.jsonl` line 470 `package_query pacman:-Q`;
  `MadoR18.CriticC2W2.jsonl` line 56 `vcs_write git:checkout`); all other files identical.
- Baseline: `python3 -I tool-9c54c56.py --scan <file>` returns `MADO_TRIPWIRE: clean` for
  all three transcripts (0 findings), so the pre-harm baseline loses nothing when the
  round-20 tool keeps these two observed rows.
- Transcript sha256 at read (2026-10-20T19:51Z window):
  - `MadoR13.jsonl` `21126251c6154d5c97194a7a155abf2be33ae958506ba3f0383b92a1b6c59615`
  - `MadoR18.CriticC2W2.jsonl` `296cce13947b7e0dca67072e541aca5581218f8c8f20e99b837f5b65a83e08bf`
  - `TameshiR18.X06DispositionGuards.jsonl` `016391b16a4807bf6fc5d78cd29715f743ff465b6a864906094500112f7ee255`
- Counters: `corpus-v4.jsonl` (5714 records, 36 rule-B hits, 0 divergent) and
  `diff-corpus-v4.jsonl` (2 differing files) at the final reading; `corpus-v3.jsonl`
  (5623) and `diff-corpus.jsonl` reproduce the same hits/diff at the earlier reading.
  All under `/tmp/ScoutCorpusLeads-3/`. No fixture code was executed; `--scan` parses
  text only.

## 6. Consequences for the round-20 fix (C1)

1. **Must keep, label `observed`:** `MadoR13.jsonl:470` and `MadoR18.CriticC2W2.jsonl:56`.
   E1's cross-cell clause ("an earlier py eval cell of the same file with no reset cell
   between") is satisfied in both, with an executed argv.
2. **Must not row:** `RuntimeError([...])` in `TameshiR18.X06DispositionGuards.jsonl`
   lines 60/81/87/93/96 — builtin, provably pure data (E2). No net output change here
   (dedup shadows it), so a fix verified only by whole-corpus row diff would not catch
   this class; verify it at the hit/lead-attribution level or with a case that has no
   accompanying `run([...])`.
3. **Lead path unexercised by the corpus:** 0 leads in 5714 transcripts. Any claim that
   the corpus exercises `lead` rows is unsupported by this scan.
4. **E4 gap in the corpus:** `jj git init --help` / `jj edit --help` (X06:53) currently
   produce `vcs_write jj:git` / `jj:edit`; E4 as written forbids that row.

## Limits

- Scope is the assigned fleet-root corpus only. As a side check I also scanned
  `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin-mado-shokunin` (20 files, 9 eval
  cells): 0 rule-B hits, 0 differing files.
- The corpus is live and was still growing during the run (5559 → 5623 → 5714 files
  across three crawls; rule-B hits and the two-row diff were identical at 5623 and 5714;
  my own seat transcript is now inside it and contributed 0 eval cells). A file written
  after the 19:54Z reading is not covered.
- `frozenset`/`RuntimeError` counts in §2 come from an AST census over all eval cells in
  the 5714-file reading, independent of the rule-B wrapper.
- 584 eval cells across the corpus fail to parse (`eval_unparsed`); the tool emits nothing
  for them, so they cannot contain an e629f73 rule-B row, but a real call hidden there
  would be invisible to both the tool and this scan (same blind spot, not an additional
  one).
- Rule-B attribution relies on source reading that `helper_argv_leads` has exactly one
  call site; if a later revision adds another path, the wrapper would miss it (it would
  not miss emitted rows — those come from the tool's own `scan_file`).
- Verdicts are static (source + transcript), not executed: no fixture was run, and the
  "observed" determination rests on the visible body reaching a spawn plus the
  transcript's own printed result, not on host side effects.
- I did not edit the tool, author cases, or run any suite: this is evidence only.

## Installs

none
