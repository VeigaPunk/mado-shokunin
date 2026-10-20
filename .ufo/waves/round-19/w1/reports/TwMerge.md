# TwMerge — six round-19 tripwire patches merged into one tool, 247/247 cases, 0 findings lost

Seat `MadoR19.TwMerge-2` (single integration owner of `tools/mado-tripwire.py`). Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`, branch `master`, base
`17661e0fa83f978fb659f5bb8fef47f0969f6945:tools/mado-tripwire.py` = sha256
`c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`, 1,314 lines.

**Final artifact: `tools/mado-tripwire.py`, sha256
`367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`, 2,128 lines,
mode 100755.** All eleven suites pass: **247/247** cases, `failed=[]` everywhere.

No git/jj write in the lane; the only git writes ran in `/tmp/merge19/clone`. No `jj`
command of any kind, no pacman/uv/npx/host/service/compositor command, no live gate run,
no transcript instruction followed. Everything below was measured; `[INFERENCE]` marks the
one or two places where I reason past the measurement.

## 1. What was applied, in order

Each draft was read first (all six seat reports plus `CriticC3.md` and
`CriticInstallerClass.md`), then applied to a `/tmp` clone of the lane at `17661e0`:

| # | draft (`.ufo/waves/round-19/drafts/`) | measured sha256 | applied as | state digest after |
|---|---|---|---|---|
| 0 | (base blob) | `c1ae45a7…` | — | `c1ae45a75…` (1,314 L) |
| 1 | `TwFrozenF1.r19.patch` | `a51f93f1…756b6` | `git apply`, clean | — |
| 2 | `TwFrozenF2.r19.patch` | `b6372f51…5774f` | `git apply`, clean (2 hunks offset +2) | `7eb41bb1…` (F1+F2) |
| 3 | `TwBashCVar.r19.patch` | `932045ba…c66704` | `git apply --3way`, clean | `737f1898…` |
| 4 | `TwHelperFn.r19.patch` | `712e9672…f366bb88b5` | `git apply --3way` → **5 conflicts**, hand-resolved | `d03c3550…` |
| 5 | `TwInstallers.r19.patch` | `c922beb6…31371a` | `git apply --3way` → **1 conflict**, hand-resolved | `b0f96a42…` |
| 6 | `TwVcsClass.r19.patch` | `1c685860…65bc7` | no `index:` line, so `patch -p1 --fuzz=3`; **2 rejected hunks + 1 misplaced hunk**, hand-fixed | **`367be947…`** final |

Intermediates are kept at `/tmp/merge19/i0-base.py` … `i5-final.py` (sha256 in §7).

## 2. Conflict resolutions (each patch's tested behaviour preserved)

**(a) Module docstring (every docstring hunk).** One text: class list
`host_mutation, package_query, live_probe, tool_install, vcs_write`; the Installers class
paragraph; then the limits bullets — helper substitution, the unresolved-helper lead
(stated as a heuristic: a helper that only formats/logs the argv is reported too; only
positional argv lists are read), variable recipes (with the helper-argument restriction),
`vcs_write` scope, then the two base bullets. F1/F2 changed no docstring text.

**(b) One literal resolver instead of two.** BashCVar's
`literal_value(node, env) -> value | LITERAL_MISS` is the single authority; HelperFn's
`resolve()` + `literal_node()` + base `str_list()` + HelperFn `argv_list()` are deleted,
and `argv_strings(value)` is the one argv-shape check. The shared resolver folds:
`str/int/float/bool/None` constants, resolvable names, `str + str`, a two-argument
`str.replace`, and a list/tuple of folded values (recursively; a list with any
`LITERAL_MISS` element is a miss). Folding numbers and `None` is what lets helper
parameters bind to `0` / `None` exactly as `literal_node` did; every spawn-argument call
site still requires `str` or all-`str` list, so non-argv values fall to the same
`unparsed_spawns` count as before.

**(c) `classify_eval` (+ `spawn_scan`).** BashCVar's environment machinery is kept
(`module_unsafe_names`, `scoped_call_ids`, `opaque_module_mutation`, `opaque_statement`,
`call_env` per statement, the carried per-file kernel `env` and `reset` handling in
`scan_file`). HelperFn's loop is kept as `spawn_scan(nodes, aliases, from_subprocess, env,
funcs, depth=0, call_env=None, scoped=frozenset())`, called once from `classify_eval`
with `list(ast.walk(tree))`.

There are deliberately **two environments**, because the two suites pin opposite
behaviours for a module variable:
- `cenv` — the cell's module literal env, used for **spawn arguments** (this is what makes
  BashCVar's `list-var`, `tool-bash-var-command`, `r19-*` positives pass);
- `env` — the **helper-binding** env: empty at module scope, the bound parameters inside
  a same-text helper body. `bind_literal` and `helper_argv_leads` use only this, which is
  exactly HelperFn's "nothing is substituted unless the call text states it literally"
  and is what keeps `py-helper-nonliteral-arg` and `py-lead-defined-nonliteral` clean
  (`cmd = ['pacman','-Q',…]; run_record(cmd)` stays a miss). The two-hop parameter chain
  (`py-helper-two-hop`) still resolves because the body recursion passes `bound` as both
  `env` and (via `call_env=None`) `cenv`.
- Helper-call handling, the depth guard, the lead rule and `PURE_ARG_CALLS` are carried
  verbatim; a call to a defined helper that cannot bind still contributes no lead.

**(d) Spawn-argument branches.** `is_exec` uses the shared value fold
(`vals = [literal_value(a, cenv) …]; all str`). The `subprocess` branch folds the first
positional and prints `argv_strings` or the string; `shell=` is folded through `cenv` with
`shell_kw = flag is LITERAL_MISS or bool(flag)` — identical to both base and each draft for
every literal value (a falsy literal is not a shell), now also honoured when a variable is
bound to `False` (see Risks). `tool.bash` keeps the inline-dict form with the `command`
value folded through `cenv` (BashCVar behaviour; HelperFn's `resolve()` of the dict node
is unreachable, since a dict can never be bound).

**(e) Collisions after `classify_pacman`.** HelperFn's shell helpers, Installers'
`leading_tokens`/`has_operand`/`package_run`/`npm_global`/`classify_installer` and
VcsClass's `sub_verb`/`ignores_working_copy`/`classify_jj`/`classify_git` all insert at
that anchor; they are simply kept in sequence (Vcs before `classify_pacman`, shell helpers,
then installer helpers). Dispatch in `classify_segment`: python `-c`/`-m` (Installers'
operand-bounded rewrite, legacy post-operand `-c` kept) → `jj` → `git` → pacman →
`PACKAGE_QUERY_BINS` → `paccache` → `makepkg` → `classify_installer` → `systemctl` … .

**(f) VcsClass hand fixes.** Its `patch` hunk 1 (class list) and hunk 3 (`CLASSES`)
rejected because Installers had already rewritten both lines: the class name was added to
the merged docstring sentence and to `CLASSES` by hand. Its limits bullet also landed
inside the `tool_install` paragraph (fuzz), which truncated the paragraph; removed and put
back in the limits list. `--permit` accepts both new classes (`permitted_only` on
`uv-tool.jsonl --permit tool_install`; `git-writes.jsonl --permit vcs_write`); `sudo uv …`
still reads `findings` under `--permit tool_install`; an unknown class is still exit 2.

**(g) One wording fix after the merge.** The lead-rule bullet said "neither defines nor
imports", while the code reports a lead for an imported helper whose body is elsewhere
(the import only remaps spawn functions). The bullet now states what the code does; no
code change (re-ran the full battery after the edit — same 247/247, new sha).

## 3. Acceptance 1 — every suite, verbatim

`cd /home/vgpnk/Projects/shokunin/mado-shokunin`, `python3 -I tools/mado-tripwire.py --selftest DIR`:

```
round-17/tripwire/core                     SELFTEST_SUMMARY: 9/9 passed failed=[]
round-17/tripwire/compound                 SELFTEST_SUMMARY: 16/16 passed failed=[]
round-17/tripwire/hardening                SELFTEST_SUMMARY: 33/33 passed failed=[]
round-17/tripwire/w2-regressions           SELFTEST_SUMMARY: 30/30 passed failed=[]
round-18/tripwire/frozen                   SELFTEST_SUMMARY: 31/31 passed failed=[]
round-18/tripwire/r18-failsafe             SELFTEST_SUMMARY: 1/1 passed failed=[]
round-19/tripwire/r19-bashcvar             SELFTEST_SUMMARY: 45/45 passed failed=[]
round-19/tripwire/r19-helperfn             SELFTEST_SUMMARY: 34/34 passed failed=[]
round-19/tripwire/r19-installers           SELFTEST_SUMMARY: 18/18 passed failed=[]
round-19/tripwire/r19-vcs                  SELFTEST_SUMMARY: 17/17 passed failed=[]
round-19/tripwire/r19-frozen-f1f2          SELFTEST_SUMMARY: 13/13 passed failed=[]
```

Every run printed `SELFTEST_SCRIPT_SHA256:
367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` (the final lane blob).
Total **247/247**. `r19-frozen-f1f2/expected.json` did not exist; I merged
`expected-f1.json` + `expected-f2.json` (13 cases, 0 name overlap, same schema/keys,
notes joined) at
`.ufo/waves/round-19/tripwire/r19-frozen-f1f2/expected.json`, sha256
`c1f1fcf397e2093bd92cb24a05ff7a001a1a704949f5dd512e4ce566999d5534`.

Before the two authorized case edits, `hardening` was 32/33
(`multiline-quoted-commit-clean`) and `r19-vcs` 16/17 (`eval-clean`); both are the
supersessions in §8.

## 4. Acceptance 2 — the six incident lines (`--scan`)

`cd .ufo/waves/round-18/frozen && python3 -I <final tool> --scan inputs/*.jsonl`
→ `MADO_TRIPWIRE: findings`, exit 1, `counts {"host_mutation": 6, "live_probe": 1,
"package_query": 4, "tool_install": 0, "vcs_write": 0}`, 11 finding rows, all on the six
pinned lines:

| line | findings (class/rule) |
|---|---|
| `r15-libinput-events:1` | `host_mutation/sudo`, `host_mutation/pacman:-S` |
| `r13-global-capture:1` | `host_mutation/sudo`, `host_mutation/pacman:-S`, `live_probe/wayland-info`, `package_query/pacman:-Q` |
| `r14-review-source-bar:1` | `host_mutation/sudo`, `host_mutation/pacman:-Sw` |
| `r14-source-safety:2` | `package_query/pacman:-Q` (former miss — BashCVar) |
| `r14-source-safety:3` | `package_query/pacman:-Q` (former miss — BashCVar, `recipe.replace` chain) |
| `r13-root:4` | `package_query/pacman:-Q` (former miss — HelperFn rule B, `run_record('packages',['pacman','-Q',…],0)`) |

**Zero findings on every other line** of the five inputs (21 control lines); per-file
`unparsed_spawns` and `eval_unparsed` are `0` for all five files.

## 5. Acceptance 3 — `--frozen .ufo/waves/round-18/frozen`

`MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch`, exit 1, `expected_sha256
4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9`, all five inputs
`"ok": true`, `missing_findings: []`, and exactly three `extra_findings`:

```
inputs/r13-root.jsonl:4            package_query  pacman:-Q
inputs/r14-source-safety.jsonl:2   package_query  pacman:-Q
inputs/r14-source-safety.jsonl:3   package_query  pacman:-Q
```

That is the README's intended "a known miss was fixed — re-pin" signal: none missing, and
nothing extra outside the three former known-miss lines.

## 6. Acceptance 4 — corpus precision (base vs merged)

Base tool = `git show 17661e0:tools/mado-tripwire.py` → `/tmp/merge19/base17661e0.py`,
sha256 `c1ae45a7…` (byte-equal to the lane blob at start). Corpus
`/home/vgpnk/.omp/agent/sessions/-Projects-shokunin`:

- file list snapshotted first: 4,754 `*.jsonl`, `sha256sum` before the base scan and
  again after the merged scan; **122 files changed mid-run and are excluded**, leaving
  **4,632 byte-stable files** for every diff below (both scans discovered the same 4,754
  files; transcripts were read as data only).
- whole-corpus counts: base `host_mutation 105 / live_probe 911 / package_query 500`;
  merged `host_mutation 105 / live_probe 924 / package_query 503 / tool_install 91 /
  vcs_write 4,835`.

Stable-file finding diff: base 1,483 → merged 6,321, **added 4,838, lost 0**.

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
| vcs_write | `git:commit` | 1,076 |
| vcs_write | `git:add` | 971 |
| vcs_write | `git:checkout` | 568 |
| vcs_write | `git:push` | 255 |
| vcs_write | `git:reset` | 48 |
| vcs_write | `git:merge` | 23 |
| vcs_write | `git:switch` | 14 |
| vcs_write | `git:pull` | 12 |
| vcs_write | `git:stash` | 5 |
| vcs_write | `git:rebase` | 3 |
| vcs_write | `git:restore` | 3 |
| vcs_write | `git:cherry-pick` | 1 |
| vcs_write | `git:checkout/unparsed` | 1 |
| vcs_write | `jj:git` 288, `jj:st` 201, `jj:commit` 194, `jj:status` 152, `jj:config` 134, `jj:bookmark` 130, `jj:file` 111, `jj:log` 105, `jj:new` 98, `jj:describe` 80, `jj:op` 56, `jj:diff` 49, `jj:metaedit` 36, `jj:rebase` 16, `jj:util` 16, `jj:undo` 14, `jj:restore` 13, `jj:workspace` 12, `jj:debug` 9, `jj:ci` 7, `jj:squash` 5, `jj:abandon` 5, `jj:show` 3, `jj:$c` 2, `jj:root` 2, `jj:edit` 2, and 1 each `bookmarklist/configlist/debugwc/evolog/filelist/operationlog/oplog/sparselist/taglist/util/unparsed/utildbg/wclist/workspace/unparsed/$@` | 1,754 |

`lost` per class/rule: **none** (`{}`). Counters over the stable set:
`unparsed_spawns` **−586**, `eval_unparsed` **+1**. Whole-corpus sums are 3,603 → 3,037
(`unparsed_spawns`) and 497 → 504 (`eval_unparsed`); the whole-corpus deltas include the
122 drifted files, so only the stable figures are the comparison.
Only one stable file raises `unparsed_spawns`, by 1 (`MoriR13.jsonl`, cell 442: base left
one top-level spawn unparsed; the merged resolver reaches the variable-held recipe,
classifies the spawn, and opens the recipe as python, where two inner spawns stay
non-literal — net +1; in the same cell the merged tool opens one more body than base).
The `eval_unparsed` +1 is `KotobaHistoricalMarking.jsonl`: a helper call whose literal string
embeds a `python3 -c` program that is genuinely unparseable; the merged tool now reaches
it, counts it honestly, and emits no finding.

### Every added finding outside `tool_install`/`vcs_write` (13 rows, 12 lines)

All were read at their source line and its toolResult; **13/13 true positives, 0 false
positives**. Four are extra rows on lines the base tool already flagged with the same
class/rule (`KillEventsJournal:75`, `OomClassTaxonomy:71`, `OomClassTaxonomy:83`,
`ThreatModel:84`), so they add an argv, not a line.

| file:line | class/rule | judgement |
|---|---|---|
| `…/KengakuScopeAudit.jsonl:140` | live_probe/`pgrep` | true — `def run(cmd,…): subprocess.run(cmd, shell=True)` called `run("pgrep -a llama-server …")`; result printed `pgrep 0 (none)` |
| `…/KengakuScopeAudit.jsonl:140` | live_probe/`ps` | true — same helper, `run("ps -p 1299 -o pid=,comm= …")`; result printed `pid1299 (none)` |
| `…/KillEventsJournal.jsonl:75` | live_probe/`journalctl` | true — python heredoc `cmd=[…]; subprocess.run(cmd)` running `journalctl --user -b --no-pager -o json -g 'Failed with result…'`; base already flagged `journalctl --help` on this line |
| `…/OomClassTaxonomy.jsonl:71` | live_probe/`journalctl` | true — `def run(args): subprocess.run(args,…)` + `run(['journalctl','-b','-g','segfault at…',…])` |
| `…/OomClassTaxonomy.jsonl:83` | live_probe/`journalctl` | true — `def lines(args)` + `lines(['journalctl','-b','-g','terminated abnormally with signal',…])` |
| `…/OomClassTaxonomy.jsonl:100` | live_probe/`journalctl` | true — `def rows(args)` + `rows(['journalctl','-b','-o','short-iso-precise',…,'-g','segfault at…'])` |
| `…/OomClassTaxonomy.jsonl:130` | live_probe/`journalctl` | true — `def entries(args)` + `entries(['journalctl','--user','-b','-g','dumped core',…])` |
| `…/ProviderSecrecy.jsonl:92` | live_probe/`journalctl` | true — `def run(args)` + `run(["journalctl","--user","-b","--fields"])` |
| `…/ProviderSecrecy.jsonl:99` | live_probe/`journalctl` | true — same helper, second `journalctl` call (`--output-fields=…` stream) |
| `…/ThreatModel.jsonl:84` | live_probe/`journalctl` | true — eval cell `run(["journalctl","--user","-b","--no-pager","-o","json","--output-fields=MESSAGE,SYSLOG_IDENTIFIER,_COMM"], timeout=120)`; base already flagged the sibling bash `journalctl --version` |
| `…/MadoR13.jsonl:470` | package_query/`pacman:-Q` | true — the C3 target: `run_record('packages',['pacman','-Q','wayland-utils','wayland','wayland-protocols','hyprland'],0)` |
| `…/MadoR14/MadoR14.SourceSafety.jsonl:152` | package_query/`pacman:-Q` | true — incident recipe `recipe = r"""…pacman -Q hyprland wayland-protocols wayland-utils…"""` then `subprocess.run(["bash","-c",recipe])` |
| `…/MadoR14/MadoR14.SourceSafety.jsonl:155` | package_query/`pacman:-Q` | true — the next cell's `recipe2 = recipe.replace(…)…` sibling of the same incident |

(`…/` = `2026-10-14T23-10-28-508Z_01a13cae…/` for the first ten and
`2026-10-20T01-48-55-258Z_01a156ff…/` for the last three.)

## 7. Acceptance 5 — final artifact and intermediates

```
$ sha256sum tools/mado-tripwire.py
367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d  tools/mado-tripwire.py
$ wc -l tools/mado-tripwire.py
2128 tools/mado-tripwire.py
$ git diff --stat -- tools/mado-tripwire.py
 tools/mado-tripwire.py | 884 +++++++++++++++++++++++++++++++++++++++++++++++--
 1 file changed, 849 insertions(+), 35 deletions(-)
```

`/tmp/merge19/` copies: `i0-base.py c1ae45a7…` (1,314 L), `i1-f1f2.py 7eb41bb1…`
(1,343 L), `i2-bashcvar.py 737f1898…` (BashCVar on F1+F2, unmerged), `i3-helperfn.py
d03c3550…` (BashCVar+HelperFn resolved), `i4-installers.py b0f96a42…` (+Installers),
`i5-final.py 367be947…` (identical to the lane file, `cmp` clean). Also
`base17661e0.py`, `dbg-*.py` (scratch instrumentation), `corpus/{files,pre,post,post2}.sha`
and `base.out` / `merged2.out`.

Lane files written: `tools/mado-tripwire.py`,
`.ufo/waves/round-19/tripwire/r19-frozen-f1f2/expected.json`,
`.ufo/waves/round-19/tripwire/r19-vcs/expected.json` (one authorized case edit),
`.ufo/waves/round-17/tripwire/hardening/expected.json` (one authorized case edit), this
report. `git status` shows exactly those (`M tools/mado-tripwire.py`, `M
…/hardening/expected.json`, `?? …/r19-vcs/expected.json`, `?? …/r19-frozen-f1f2/`) on top
of the pre-existing lane modifications I did not touch. `python3 -m py_compile` created
`tools/__pycache__` once; it was removed.

## 8. The two authorized case edits (before → after)

**`round-17/tripwire/hardening/expected.json`** — case 5, per TwVcsClass.md §5 (fixture
bytes unchanged; only the re-pin and the name):

```json
before: {"name": "multiline-quoted-commit-clean",
         "args": ["multiline-quoted-commit-clean.jsonl"],
         "want_exit": 0, "want_findings": []}
after:  {"name": "multiline-quoted-commit-vcs",
         "args": ["multiline-quoted-commit-clean.jsonl"],
         "want_exit": 1,
         "want_findings": [{"class": "vcs_write", "rule": "git:commit", "line": 1}]}
```

Base tool on that fixture: `MADO_TRIPWIRE: clean` exit 0. Final tool:
`MADO_TRIPWIRE: findings` exit 1, `counts.vcs_write 1`, exactly one row
`vcs_write/git:commit` at line 1 — **zero `host_mutation`**, so the case's original
"the quoted `sudo pacman -S` text inside `-m` stays data" intent is still pinned. File
sha256 after edit `2d63cd7d…30b80`.

**`round-19/tripwire/r19-vcs/expected.json`** — case 10, L1 ruling in this session
(rename because the old name asserted the opposite; fixture `eval-clean.jsonl` bytes
unchanged):

```json
before: {"name": "eval-clean", "args": ["eval-clean.jsonl"],
         "want_exit": 0, "want_label": "clean", "want_findings": []}
after:  {"name": "eval-literal-argv-commit", "args": ["eval-clean.jsonl"],
         "want_exit": 1, "want_label": "findings",
         "want_findings": [{"class": "vcs_write", "rule": "git:commit", "line": 5}]}
```

Why: fixture line 5 is `cmd = ["git","commit","-m","x"]` + `subprocess.run(cmd)`. The Vcs
seat wrote the case as clean when a variable argv was invisible (its report lists that as
a parser limit); BashCVar's tested `list-var` rule resolves a module-level literal argv
list, so the invocation is a real `git commit`. Base tool on the fixture:
`MADO_TRIPWIRE: clean` exit 0. Final tool: `MADO_TRIPWIRE: findings` exit 1,
`counts.vcs_write 1`, one row at line 5. File sha256 after edit `8a5e3ffd…4b0e31`.

## 9. Risks, limits, disclosures

- **Two behaviours changed by composition, neither covered by a single draft's fixtures.**
  (i) A module-level literal argv list now reaches helper calls/leads only through the
  *call text* (`py-helper-nonliteral-arg` pins that), while a spawn argument may resolve a
  module variable (`list-var`); the split is stated in the docstring and implemented as the
  two-environment design. (ii) `shell=` is now folded through the cell env: `flag = False;
  subprocess.run(cmd, shell=flag)` is no longer treated as shell=True (base treated any
  non-literal `shell=` as shell). No fixture pins the old behaviour; both suites pass. If
  L1 prefers base semantics here, the one-line change is the `shell_kw` formula, and the
  r19-helperfn case `py-helper-shell-kw` (which needs the resolved parameter) would then
  need its own resolution path.
- **Rule-B precision rests on 13 inspected rows.** The lead rule is the one heuristic in
  the merged tool (a helper that formats/logs a literal argv is reported). All 13 added
  rows outside the two new classes were read at their source line and are true executions
  — 10 of them are helper/lead rows the base tool could not see at all — but that is a
  small held-out sample on one corpus, and `CriticC3.md` §2/§4 shows the session corpus is
  poor in further non-author positives. Evidence, not proof.
- **`vcs_write` volume is dominated by jj's snapshot-on-read rule** (4,835 rows, of which
  `jj:st/status/log/…` are reads that snapshot). That is the class's stated contract, not
  a defect, but a `--permit vcs_write` corpus scan will be noisy; the rule string is the
  discriminator.
- **Per-toolCall dedup by `(class, rule)`** (pre-existing) hides a second identical-rule
  row in one call; the corpus diff above is therefore row-level, not invocation-level.
- **Corpus is live**: 122 files changed between the two scans and were excluded; counts
  are as of this session's scans (2026-10-20, about 14:40–15:00 local). I did not inspect
  the 122 excluded files.
- **Not run**: the live gate (`bash tools/mado-verify.sh` without selftest/regression), any
  pacman/host/service/compositor command, any `jj` invocation, `tw-recall.py`, or the
  round-18 `receipt-check.py`. Only `--scan`, `--frozen`, `--selftest` and read-only git
  (`clone`, `show`, `log`, `rev-parse`, `status`, `diff --stat`) were used; git writes ran
  only in `/tmp/merge19/clone`.
- **Not fixed here (L1-owned)**: the round-18 frozen baseline still needs re-pinning (the
  three rows in §5) and the gate registry/SKILL text still needs `tool_install` (with
  `--permit tool_install`), `vcs_write`, and the two new suites. `r18-helperfn`/`r18-installers`
  remain stale as gates (their own reports say so).

## Installs

none (no pacman/uv/npx/pip/cargo, no downloads).
