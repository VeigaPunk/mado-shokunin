# CaseWrapperForms — 9 W cases: 7 red at 1f7f995 (also red at 9c54c56), 2 controls; every want equals 1f7f995's own rows on a one-feature desugared twin

## Deliverables

Dir `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CaseWrapperForms/` (one single-cell `eval` line per file, envelope copied from `round-19/tripwire/r19-helperfn/py-lead-cross-cell-literal.jsonl`; no paths, tokens or IPs in fixture text):

| file | sha256 |
|---|---|
| `cases.json` | `1653be7cfb2b6450c2724693ddd26a5a7599bd46d02ff5f1a1c5763c8b60d345` |
| `spawn-kwarg-args.jsonl` | `e6adcd650ca909aff9b7640e9611671afb1ae02157c8b7b0c8b050ed6f95eb0e` |
| `alias-assign-shell.jsonl` | `5d3fe7418c722cddec11f187dcf19f469cfd2bee4ea198a12f9ddac7dee1791a` |
| `partial-shell-sudo.jsonl` | `d2b5a731af14647c97aed86035fc053fdb4f05287f81fc47f32ee2e7c4964849` |
| `decorated-cache-param.jsonl` | `e29b190abe2eafd907ba0593d9b640974441d0170b4e7ac4d9974420faf7bef5` |
| `decorated-lrucache-call.jsonl` | `e623560fedc799edfca682475b80324eb0bc76d5f963f722e06f1f1c5675ba9b` |
| `async-def-exec-param.jsonl` | `285816c678ce3ff7b716be4b31f25483199784aaec9447e3b8d0b6e8c850ac7a` |
| `lambda-param-argv.jsonl` | `4016503d4342ac1c4c04dae95c69877a4c030f57d967d96716b946f5da631599` |
| `class-method-instance.jsonl` | `e9162d138c3560b430b7cfe58061cc206fc6c8c95c7f771a9b67579810ee4135` |
| `async-def-exec-starred.jsonl` | `851d261fd563a8d23bcc3c0cc8f1d323ea9f26b6d516103d22d42e42ec9d5f14` |

Scratch `/tmp/CaseWrapperForms/` (no clone needed: no code built). Tool copies via `git -C <lane> show REV:tools/mado-tripwire.py`: `tool-1f7f995.py` sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` (identical bytes at e629f73), `tool-9c54c56.py` sha256 `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`. `before` was computed by scanning a byte copy of the delivered dir (`/tmp/CaseWrapperForms/lanecopy`) with `cd lanecopy && python3 -I /tmp/CaseWrapperForms/tool-REV.py --scan <file>`, one file per run, and applying the counter rule in code: exit equal AND multiset of (class, rule, line, evidence) equal, a row without `evidence` counted as `observed`. Lane `refs/heads/master` read as `e629f731172b8238caffe50f152217ce56535fb4` (read-only `git rev-parse`).

## Cases

All are one cell, so every want row has line 1.

| # | name | form (the cell's essence) | want | 1f7f995 | 9c54c56 |
|---|---|---|---|---|---|
| 1 | `W-CaseWrapperForms-spawn-kwarg-args` | `subprocess.run(args=['pacman','-Q','hyprland'], capture_output=True, text=True)` | exit 1; package_query `pacman:-Q` observed | **fail** | fail |
| 2 | `W-CaseWrapperForms-alias-assign-shell` | `run = subprocess.run` then `run('pacman -Qi hyprland', shell=True, ...)` | exit 1; package_query `pacman:-Qi` observed | **fail** | fail |
| 3 | `W-CaseWrapperForms-partial-shell-sudo` | `sh = functools.partial(subprocess.run, shell=True, check=True)` then `sh('sudo pacman -S --needed --noconfirm wayland-utils')` | exit 1; host_mutation `sudo` and host_mutation `pacman:-S`, both observed | **fail** | fail |
| 4 | `W-CaseWrapperForms-decorated-cache-param` | `@functools.cache def pkg_version(name): return subprocess.run(['pacman','-Q',name], ...).stdout`, then `print(pkg_version('hyprland'))` | exit 1; package_query `pacman:-Q` observed | **fail** | fail |
| 5 | `W-CaseWrapperForms-decorated-lrucache-call` | the same with `@functools.lru_cache(maxsize=None)` (a Call decorator, which is the real-corpus shape) and `-Qi` | exit 1; package_query `pacman:-Qi` observed | **fail** | fail |
| 6 | `W-CaseWrapperForms-async-def-exec-param` | `async def pkg_version(name): proc = await asyncio.create_subprocess_exec('pacman','-Q',name, stdout=...)`, then `print(await pkg_version('hyprland'))` | exit 1; package_query `pacman:-Q` observed | **fail** | fail |
| 7 | `W-CaseWrapperForms-lambda-param-argv` | `pkg = lambda name: subprocess.run(['pacman','-Q',name], ...).stdout`, then `print(pkg('hyprland'))` | exit 1; package_query `pacman:-Q` observed | **fail** | fail |
| 8 | `W-CaseWrapperForms-class-method-instance` (control) | `class Runner: def run(self, argv): return subprocess.run(argv, ...)`, then `Runner().run(['pacman','-Q','hyprland'])` | exit 0; no rows (stated miss) | pass | pass |
| 9 | `W-CaseWrapperForms-async-def-exec-starred` (control) | `async def run_argv(argv): ... create_subprocess_exec(*argv, ...)`, then `await run_argv(['pacman','-Q','hyprland'])` | exit 1; package_query `pacman:-Q` observed | pass | fail |

Count: 9 cases. 7 are red at 1f7f995, against a requirement of at least 4. There are 2 controls, against a limit of 2.

### Exact 1f7f995 scan output for each red

All 7 reds print `MADO_TRIPWIRE: clean` (rc 0), followed by:

```text
spawn-kwarg-args:        {"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "spawn-kwarg-args.jsonl", "sha256": "e6adcd650ca909aff9b7640e9611671afb1ae02157c8b7b0c8b050ed6f95eb0e", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
alias-assign-shell:      {"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "alias-assign-shell.jsonl", "sha256": "5d3fe7418c722cddec11f187dcf19f469cfd2bee4ea198a12f9ddac7dee1791a", "unparsed_spawns": 0}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
partial-shell-sudo:      {"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "partial-shell-sudo.jsonl", "sha256": "d2b5a731af14647c97aed86035fc053fdb4f05287f81fc47f32ee2e7c4964849", "unparsed_spawns": 0}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
decorated-cache-param:   {"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "decorated-cache-param.jsonl", "sha256": "e29b190abe2eafd907ba0593d9b640974441d0170b4e7ac4d9974420faf7bef5", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
decorated-lrucache-call: {"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "decorated-lrucache-call.jsonl", "sha256": "e623560fedc799edfca682475b80324eb0bc76d5f963f722e06f1f1c5675ba9b", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
async-def-exec-param:    {"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "async-def-exec-param.jsonl", "sha256": "285816c678ce3ff7b716be4b31f25483199784aaec9447e3b8d0b6e8c850ac7a", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
lambda-param-argv:       {"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "exit": 0, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "lambda-param-argv.jsonl", "sha256": "4016503d4342ac1c4c04dae95c69877a4c030f57d967d96716b946f5da631599", "unparsed_spawns": 1}], "findings": [], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}
```

At 9c54c56, all 7 also print `MADO_TRIPWIRE: clean`, with the same `unparsed_spawns` values (1, 0, 0, 1, 1, 1, 1).

The controls:
- `class-method-instance` prints `MADO_TRIPWIRE: clean` with `unparsed_spawns: 1` at both revisions.
- `async-def-exec-starred` prints `MADO_TRIPWIRE: findings` at 1f7f995, with one row: `{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", ..., "line": 1, "rule": "pacman:-Q", ...}`. That row has no `evidence` key. At 9c54c56 it prints `MADO_TRIPWIRE: clean`.

### Why each red is red (source lines refer to `/tmp/CaseWrapperForms/tool-1f7f995.py`)

- **Decorated and async defs (4, 5, 6).** At `:1369-1372`, only an undecorated `ast.FunctionDef` enters `funcs`. That leaves out every decorated def and every `AsyncFunctionDef`. Their body spawn is scanned with an empty environment, because it is a scoped call. The spawn is counted as `unparsed_spawns: 1`, and nothing binds `name='hyprland'`.
- **Lambda (7).** A lambda bound by assignment never enters `funcs`, so the same failure happens.
- **Rule B is silent on these calls.** The lead rule (`helper_argv_leads` `:1379-1390`, call site `:1431-1433`) only reads positional arguments that fold to a list or tuple of strings. That rules out `pkg('hyprland')`, `sh('sudo pacman ...')` and `run('pacman -Qi ...', shell=True)`.
- **Aliases (2, 3).** At `:1340-1352`, aliases come only from `import`/`from ... import`, plus a hard-coded `sp`. So `run = subprocess.run` and `functools.partial(subprocess.run, ...)` never make a spawn. These two cases are silent misses: `unparsed_spawns` is 0, so nothing records that a spawn was skipped.
- **Keyword argv (1).** The spawn path reads only `node.args[0]` (`:1456`). With `args=` as a keyword it falls through to unparsed. The docstring at `:49-50` states this only for leads.
- **9c54c56.** `classify_eval` (`:606-693`) has no helper resolution and no rule B. Its aliases are also import-only (`:632-644`), and it reads positional argv only (`:682`).

### Equivalence oracle: every want comes from 1f7f995's own output

For each non-clean want, I removed exactly one wrapper feature and scanned the resulting twin at 1f7f995. In every case the twin's rows equal the want multiset, so the red is caused by the wrapper form alone:

| case | desugared twin (scanned at 1f7f995) | rows | equal to want |
|---|---|---|---|
| 1 | positional `subprocess.run(['pacman','-Q','hyprland'], ...)` | package_query `pacman:-Q` | yes |
| 2 | `subprocess.run('pacman -Qi hyprland', shell=True, ...)` | package_query `pacman:-Qi` | yes |
| 3 | `subprocess.run('sudo pacman -S --needed --noconfirm wayland-utils', shell=True, check=True)` | host_mutation `sudo` + `pacman:-S` | yes |
| 4, 5 | same def with the decorator line removed | `pacman:-Q` / `pacman:-Qi` | yes |
| 6 | plain `def` returning `asyncio.create_subprocess_exec('pacman','-Q',name, ...)` | `pacman:-Q` | yes |
| 7 | plain `def pkg(name)` with the same body | `pacman:-Q` | yes |
| 9 | `await asyncio.create_subprocess_exec('pacman','-Q','hyprland', ...)` | `pacman:-Q` | yes |

The twin fixtures are in `/tmp/CaseWrapperForms/twins/`.

### Sibling consistency

I read sibling cases in `w1/cases/`. Several are pure counterparts of mine:

| sibling (want clean) | my spawning counterpart (want observed) |
|---|---|
| `P-CasePureCallables-functools-cache-def` | `decorated-cache-param` |
| `P-CasePureCallables-async-def-await` | `async-def-exec-param` |
| `P-CasePureCallables-lambda-same-cell` | `lambda-param-argv` |

Each pair discriminates in both directions:
- A tool that marks every decorated, async or lambda call `observed` fails the P twin.
- A tool that marks all of them clean fails my W case.

Two shadowing cases agree with my readings:
- `S-CaseShadowing-list-bound-to-spawn` (`list = subprocess.run` → observed) agrees with case 2.
- `S-CaseShadowing-print-lambda-spawn` (lambda spawner → observed) agrees with case 7.

No file names collide with any sibling directory as of this writing.

## Contract readings the cases rely on (for TwRuleB and L1)

1. **Literal arguments to a helper.** Cases 4–7 read "a call with literal argv to a helper (def, async def, lambda; decorated or not)" as covering scalar literal arguments that bind into an argv inside the body. For example, `pkg_version('hyprland')` binds into `['pacman','-Q',name]`. This is the existing same-text helper mechanism:
   - the 1f7f995 docstring at `:35-40`: "called there with literal arguments has its body classified with those arguments substituted";
   - the pinned cases `r19-helperfn` `py-helper-shell-string` (`run('pacman -Qi wayland')` is resolved) and `py-helper-keyword`.

   E1 extends that mechanism to decorated defs, async defs and lambdas. If L1 instead reads E1 as covering literal argv lists only, cases 4–7 need new expectations. **[decision point]**
2. **Aliases go through the spawn path.** Calls through `run = subprocess.run` and `functools.partial(subprocess.run, ...)` are literal spawns (E1). Cases 2 and 3 pass string literals, so they do not depend on module-variable folding through an alias.
3. **Keyword argv.** `args=` must be read on `subprocess.*` spawn functions (case 1).
4. **Starred argv.** Control 9 requires that `*argv` in `asyncio.create_subprocess_exec` folds once `argv` is bound by a visible helper call. The existing exec branch (`:1449-1455`) folds each positional arg and does not handle `ast.Starred`. Without that fold, the target would drop a row that 1f7f995 reports today. That loss is invisible to the 9c54c56 corpus diff, because 9c54c56 never had the row.
5. **Class method stays a miss.** Control 8 stays clean. E1 names only def, async def and lambda helpers, and E2 keeps attribute/method calls unflagged ("`' '.join(argv)` stay unflagged as before"). Resolving `Runner().run(...)` would need instance-type binding, which the scanner does not do. If a later tool resolves it, this case must be edited, with the reason recorded.

## Assigned literal-argv spellings are not red at 1f7f995 (why the cases use other spellings)

I scanned the assigned spellings verbatim as probes (`/tmp/CaseWrapperForms/probes/`). They are not cases:

| probe | 1f7f995 | 9c54c56 |
|---|---|---|
| `run = subprocess.run; run(['pacman','-Q'])` | rc 1 `pacman:-Q` (unmarked) | rc 0 clean |
| `r = functools.partial(subprocess.run, check=True); r(['sudo','pacman','-S','x'])` | rc 1 `sudo` + `pacman:-S` (unmarked) | rc 0 clean |
| `@functools.cache def q(argv): return subprocess.run(argv)`; `q(['pacman','-Q'])` | rc 1 `pacman:-Q` (unmarked) | rc 0 clean |
| `sh = lambda a: subprocess.run(a)`; `sh(['pacman','-Q'])` | rc 1 `pacman:-Q` (unmarked) | rc 0 clean |
| `async def q(argv): return subprocess.run(argv)`; `await q(['pacman','-Q'])` | rc 1 `pacman:-Q` (unmarked) | rc 0 clean |
| `subprocess.run(args=['pacman','-Q'])` | rc 0 clean | rc 0 clean |

Rule B attaches an unmarked row to any bare-name call that has a literal argv list. The counter treats an unmarked row as `observed`, so these spellings pass at 1f7f995 even though the tool never resolves the wrapper. They would therefore not count as red.

The `@functools.cache` spelling also cannot really run: a list argument raises before the body executes. I checked this with my own non-spawning probe, `functools.cache(lambda a: len(a))(['pacman','-Q'])`, which printed `TypeError: unhashable type: 'list'` (Python 3.14.8). A tuple argument is hashable, and rule B already reports `q(('pacman','-Q'))` as `pacman:-Q` at 1f7f995. That is why case 4 passes a str parameter.

Control 9 keeps one literal-list spelling as a regression guard.

## Real-corpus grounding

Method: `ast` parse only, nothing executed. I read the assistant `eval` toolCall cells (language py) in `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin`: 5,623 jsonl files, of which 2,461 cells mention subprocess and compile.

Spawning wrapper forms found:

| form | occurrences | files |
|---|---|---|
| plain `def` | 904 | 330 |
| `async def` | 30 | 21 |
| lambda | 6 | 5 |
| decorated `def` | 1 | 1 |
| alias assignment | 4 | 1 (monkeypatch `orig=subprocess.run`) |
| `functools.partial` over a spawn | 0 | 0 |
| `args=` keyword spawn | 0 | 0 |
| class-method spawner | 0 | 0 |

Calls to these wrappers usually pass strings or non-literal values rather than a literal argv list:
- lambda: 24 string-first calls, 3 other;
- async: 11 string-first, 24 other;
- decorated: 8 non-literal.

Rule B cannot see either kind. That is why cases 4–7 use string parameters. Pointers, relative to that sessions directory:

| shape | pointer | text |
|---|---|---|
| decorated | `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/ClosureTameshiR17.jsonl:99` | `@functools.lru_cache(None) def gb(rev,path): p=subprocess.run(['git','-C',L,'show',...])` |
| param lambda | `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/TsukuroiR14/TsukuroiR14.RedBeforeCritic.jsonl:104` | `blob=lambda p: subprocess.run(['git','-C',L,'show',f'{B}:{p}'],...)` |
| async with literal program plus params | `.../MadoR18/MadoR18.MutGateOM.jsonl:55,60,88` (same session dir) | `create_subprocess_exec('git','clone',...)` |
| starred async | `.../MadoR19/MadoR19.MutFrozenRepin.jsonl:50` | `create_subprocess_exec(*argv, ...)` |

## Routed residuals (not authored as cases)

1. **Real vararg wrappers remain missed.**
   - Where: `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR18/MadoR18.RevPreReg18.jsonl:102` and `:105`.
   - What: `run = lambda *a: subprocess.run(a, cwd=lab, check=True, ...)`, where `lab` is `/tmp/r18-revprereg-lab` or `-lab2`. It is called as `run('git','add','-A')`, `run('git',..., 'commit', ...)` and `run('git','reset','--hard','-q',rev)`.
   - Scan: a synthetic copy of the shape (`probes/probe-real-vararg-lambda.jsonl`) prints `MADO_TRIPWIRE: clean`, rc 0, at both revisions.
   - Why not a case: E1 does not list varargs, and `r19-helperfn` `py-helper-vararg` pins exit 0 for `def run(*a)`. A want-observed case would contradict an existing pin, so this needs an L1 decision. **[decision point]**
2. **Adjacent precision defect in S/E3 territory.** The hard-coded alias `sp` at `:1340` treats a user instance named `sp` as subprocess.
   - Probe: `class S: def run(self, a): return a` / `sp = S()` / `sp.run(['sudo','pacman','-S','libinput'])`.
   - Result: exit 1 with host_mutation `sudo` + `pacman:-S` at both 1f7f995 and 9c54c56. The body is pure.
   - First recorded at `.ufo/waves/round-17/w2/reports/ReviewEvalAst.md:215-218`.
   - Route to CaseShadowing/TwRuleB: under E3, the binding in effect at the call should win.
3. **Silent misses.** Cases 2 and 3 are missed with `unparsed_spawns: 0`, so the per-file counter gives no hint that a spawn was skipped. This is relevant to the SKILL/docstring limits text.

## Limits

- I did not see or run the target tool, so nothing here claims that TwRuleB passes these cases. The wants rest on E1–E3, the sibling-consistent readings, and the twin oracle.
- I never executed fixture code. I used only `--scan` (a text parse) with copies of the two pinned tool revisions. The only Python I executed besides the scans was the corpus `ast` census and the non-spawning `functools.cache` TypeError check.
- I did not read or run `tw-precision.py`. I applied its stated comparison rule in my own code.
- Census scope:
  - only `-Projects-shokunin` sessions;
  - only assistant py `eval` cells whose jsonl line contains `subprocess` or `create_subprocess` and that compile;
  - no bash-tool shell functions or aliases;
  - counts are AST occurrences per cell, so cells repeated across sub-session files are counted again. [UNK] I did not measure how much duplication that causes.
- I did not run the existing 11 suites. I only checked their fixture texts for conflicting wrapper pins. Two touch these shapes:
  - `round-17/tripwire/w2-regressions` `eval-import-alias` (import-as alias → finding);
  - `r19-bashcvar` `r19-lambda-deferred-clean` (an uncalled lambda using a module variable → clean).

  Neither conflicts with these cases.
- I made no git or jj writes, ran no host or package commands, and opened no web sources (so there are no fetch receipts).

## Installs

none
