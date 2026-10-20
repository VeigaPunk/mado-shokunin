# ScoutRuleBMap — map complete: an `evidence` key plus two top-level counts breaks no existing consumer (proof below); the breakable surfaces are exact-key-set validators, a lost-lead exit change, and five suite cases that a literal reading of E1/E3 would flip

Lane HEAD `e629f731172b8238caffe50f152217ce56535fb4`; `tools/mado-tripwire.py` sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d` (same bytes at `1f7f995`). Pre-harm baseline `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`, tool sha256 `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`. All experiments ran on byte copies under `/tmp/r20s/` (clone `/tmp/mado-r20-ScoutRuleBMap` HEAD `e629f73`); no lane file was written except this report. Fixture code was never executed — only `--scan` parsing.

## 1. Every row from an eval cell has one constructor

`scan_file` is the only place a finding dict is built: `tools/mado-tripwire.py:1596-1604` (`findings.append({file, line, tool_call_id, timestamp, tool, class, rule, argv0, command})`). `line` is the 1-based JSONL line of the assistant message, never an AST line. Rows are deduped per tool call on `(class, rule)` at `:1590-1594`. Anything that adds `evidence` must add it here (and, for `--frozen`, the same dict is reused at `:1949-1957`).

`hits` is a list of `(class, rule, argv0, segment_text)` tuples. There are exactly three producers of tuples for an `eval` cell:

| Path | Site | Contract reading |
|---|---|---|
| `%%bash` first line → `classify_shell(rest)` | `:1311-1312` | observed (bash text stated) |
| `!`/`x = !` lines → `classify_shell`, line replaced by `pass` | `:1314-1318` | observed |
| AST `spawn_scan` over the cell | `:1374-1376` → `:1393-1474` | see below |

Inside `spawn_scan`, the branches are: same-text helper with literal-bound args `:1411-1417`; alias rewrite `:1418-1421`; spawn-function test `:1422-1427`; **rule B `:1429-1433`**; `tool.bash` dict `:1434-1445`; exec-family `:1446-1452`; subprocess/shell-string `:1453-1473`. Every hit is produced by `classify_segment`'s `hit()` (`:902-916`) or by another `classify_shell`/`nested_eval` recursion; `nested_eval` (`:216-220`) re-enters `classify_eval` for python heredocs/`-c`, with a fresh env, and its counters are folded into the enclosing bash call's entry (`:1588-1589`).

The contract's "observed" is therefore the union of: bash cells, `%%bash`, `!` lines, and the four AST spawn branches (helper-resolved, `tool.bash`, exec-family, subprocess/shell-string) when their argv is literal; rule B is the only "lead" source today (with the E1 gaps in §3).

## 2. Rule B anatomy (why `frozenset([...])` fires)

- `PURE_ARG_CALLS` `:1252-1259` is a closed 27-name set of *builtins*: `print, list, tuple, set, dict, sorted, reversed, repr, str, bytes, len, any, all, min, max, sum, enumerate, zip, map, filter, open, exec, eval, compile, isinstance, getattr, hasattr, setattr, iter, next, input`. `frozenset`, `type`, `format`, `deque`, exception types (`RuntimeError`, …) and every dotted stdlib name are absent.
- Rule B branch `:1429-1433`: `if (isinstance(node.func, ast.Name) and helper is None and name not in PURE_ARG_CALLS): hits.extend(helper_argv_leads(node, env))`. Consequences:
  - Attribute callees never reach rule B (`json.dumps([...])`, `shlex.join([...])`, `functools.partial(...)` are all invisible — the docstring's `json.dumps` example at `:46-49` never exercises `PURE_ARG_CALLS`).
  - An imported bare name is rewritten to its dotted alias at `:1418-1421` *before* the `PURE_ARG_CALLS` test, so `from json import dumps; dumps([...])` fires too (`name == "json.dumps"`, not in the set).
  - `helper_argv_leads` `:1379-1391` reads only **positional** args, folds them with `literal_value` against the *helper* env (`env`), and joins each literal list with `shlex.join` before `classify_shell`. At module scope `env` is `{}` (classify_eval calls `spawn_scan(..., {}, ...)` at `:1374`), so a module variable argv is deliberately not resolved for leads (documented), while an enclosing same-text helper's bound parameters are.
  - No marker: the row is emitted with the same dict shape as a real spawn, and `verdict_of` `:1617-1623` counts it as unpermitted → exit 1, label `findings`.

Reproduced harm (fixture envelope copied from `tripwire/r19-helperfn/py-lead-cross-cell-literal.jsonl`, code replaced by `BLOCK=frozenset(['pacman','-Q','hyprland'])`; parsing only, code never run):

```
9c54c56: MADO_TRIPWIRE: clean      {"exit": 0, ... "findings": []}
e629f73: MADO_TRIPWIRE: findings   {"exit": 1, ... "counts": {"package_query": 1, ...}}
```

This matches `corpus/lessons/round-19-verifier-spotcheck.md:66-84` and `.ufo/waves/round-19/w2/reports/AdvHelperFn.md:58-59` (b16b/b23). The docstring already calls this a “lead” (`:40-49`); the JSON never carried a marker — the repair closes a doc/code gap rather than inventing a semantic.

## 3. `funcs` index and env carry — exact gaps against E1/E2/E3

`funcs` is built at `:1368-1372`:

```python
funcs = {}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and not node.decorator_list:
        funcs[node.name] = None if node.name in funcs else (node.lineno, node)
funcs = {k: v for k, v in funcs.items() if v is not None}
```

Observed consequences (each is `[INFERENCE]` only where marked; the code paths are direct):

1. `async def` and decorated `def` are not indexed → a literal-argv call to them yields a **lead** although E1 says “decorated or not, async def” is observed. The body's own spawns are still seen (the whole tree is walked at `:1374`), but with an empty env, so parameter-driven argv is unparsed.
2. Duplicate `def`s collapse to `None` and are filtered out → the call is treated as an undefined bare name, so rule B judges it (a literal **list** would become a lead; `py-helper-redefined` passes a string, which rule B ignores, so it stays clean). E3's “latest preceding binding wins” would resolve the call instead and emit `host_mutation/pacman:-S`, flipping that suite case (see §5.3).
3. Only top-level `tree.body` defs; lambdas are never indexed; `run = subprocess.run`, `functools.partial(subprocess.run, …)` are not aliases (aliases come only from `import`/`from … import` at `:1339-1350`) → all become leads, contradicting E1's explicit “spawn alias bound in the text”.
4. Cross-cell: `funcs` is per cell; the only carried state is `envs` (`:1544`), a literal environment dict, cleared on `reset` (`:1580-1581`) and passed to `classify_eval` (`:1583`). E1's earlier-cell helper visibility needs a second carried table (defs/classes/import bindings) cleared by the same `reset`; there is no such state today.
5. Ordering: `node.lineno > helper[0]` (`:1412`) means a call on a line before the def is never resolved. Such a call emits **no row at all** — not even a lead — because the rule-B branch also requires `helper is None` (`:1429-1431`) and the def *is* in the index. That is why `py-helper-defined-after-call` is clean today even though its call hands over a literal `['pacman','-Q','wayland']`. If the repair keeps the def in the index but lets an order-guard failure fall through to rule B (or if the guard is dropped and the body is resolved), that case flips to exit 1.
6. `del name` and `import` rebinding do not touch `funcs`/`aliases`: `del` only pops `env` via `module_unsafe_names` (`:1135-1188`, applied at `:1337-1338`). E3's “`del` unbinds → literal-argv call is a lead” is not implemented for functions/aliases; today a deleted alias still resolves as a spawn (observed row), and a deleted `def` still resolves as a helper.
7. Depth: helper recursion stops at `depth < 4` (`:1412`); E2 allows transitive depth ≤ 4 — consistent.
8. `bind_literal` (`:1260-1299`) refuses varargs, non-literal required params, and unresolvable defaults; on refusal `spawn_scan` does `continue` (`:1417`) → no row and no lead (correct for `py-helper-vararg`, `py-helper-default-nonliteral`; these are the cases a “scan the body anyway” fallback would flip).

## 4. Consumer inventory and breakage (the asked list)

Only these code paths read the verdict JSON. Everything else that mentions the tool is docs/receipts/generators.

| Consumer | Reads | Tolerates `evidence` on rows? | Tolerates top-level count keys? | Breaks if… |
|---|---|---|---|---|
| `run_scan` / `--scan` `:1630-1647` | emits payload | n/a (producer) | n/a | — |
| `verdict_of` `:1617-1623` | `class`/`permit` only | yes | yes | lead rows leave `findings` or stop being unpermitted (exit 1/label `findings` required by E1) |
| `run_frozen` compare `:1960-1976` | `key=(file,line,class,rule)`; `missing/extra` rows built as 4-key dicts | yes (ignored) | not read (frozen payload has its own keys) | any row's (class,rule,line) changes, any row added/removed on the pinned inputs, or exit/label changes |
| `emit_frozen` `:1654-1683` | fixed key set | n/a | n/a | adding keys is safe; no consumer enumerates the set |
| `validate_frozen` `:1702-1785` | `FROZEN_KEYS` `:1688-1690`, unknown-key reject `:1716-1719` | rows: yes (only 4 fields required) | — | **any new top-level expected.json key** → `frozen_error` exit 2 for every baseline |
| `run_selftest` scan compare `:2055-2068` | `(class, rule, line[, basename file])`; `want_ids` | yes — a `want_findings` row's `evidence` is ignored | verdict keys not inspected | any (class,rule,line,file) set change in a suite case |
| `run_selftest` frozen compare `:2031-2038` | `(outcome, exit, len(missing), len(extra))`, schema | yes | not inspected | outcome/exit/count changes |
| `.ufo/waves/round-19/tw-recall.py:73` | `{(file,line)}`, requires rc ∈ {0,1} | yes | yes | a lead row leaves `findings` → 6/6 → 5/6 |
| `.ufo/waves/round-20/tw-recall-split.py:18,85-87` | `finding.get("evidence","unmarked")`, allowed `{observed,lead,unmarked}`; one line may carry several markers | yes | yes | any other marker string → `could_not_evaluate` exit 2 (`:87`); missing marker is bucketed as `unmarked`, not observed |
| `.ufo/waves/round-20/tw-precision.py:71-93` | `row.get("evidence","observed")`, compares `(class,rule,line,evidence)` multiset + exit | yes (missing = observed, as the declared comparison rule says) | yes | marker outside `{observed,lead}` → `CouldNotEvaluate` exit 2 (`:81-86`); also requires `verdict.exit == returncode` and schema `mado-tripwire-verdict-v1` (`:177-182`) |
| `.ufo/waves/round-20/corpus-diff.py:127-140,197-238` | lost rows key `(file,line,class,rule)`; added grouped by `(class,rule,evidence)`; missing marker = observed | yes; re-labelling is **not** a lost row | yes | exit/schema mismatch (`:122`); a marker outside the two values only affects grouping labels |
| `.ufo/waves/round-19/frozen-repin.py:240-303` | schema, `exit`, `findings[].file/line/class/rule`, `unpermitted`; tolerates extra keys | yes — and **drops** it: derived `expected_findings` rows have only `{file,line,class,rule}` (`:171-181`, observed on a real re-pin, §5.2) | tolerates extra (only `unpermitted` is cross-checked) | nothing from the two additions; a re-pin cannot carry the marker |
| `.ufo/waves/round-18/recut-receipts.sh:241,394,423-424` | committed receipt JSONs: `findings` multiset (4 fields) and exact `counts` dict equality | yes | not present in those receipts | if the new integers were put **inside `counts`**, `counts_identical` flips to false; top-level keys are safe |
| `.ufo/waves/round-19/harm-watch.sh`, `.ufo/waves/round-20/harm-watch.sh:307-357,370-390` | line-1 labels, exit codes, frozen outcome/label | yes | yes | suite exit≠0; round-18 frozen outcome outside `{frozen_match, frozen_verdict_mismatch}`; **round-19/round-20 frozen must exit 0** (run_pinned), so those baselines must keep matching or be re-pinned |
| `.ufo/waves/round-19/final-receipts.sh:32-35` | writes receipts verbatim (no parsing) | yes | yes | never |
| `.ufo/waves/round-17/measure.py:298` | presence of `tools/mado-tripwire.py` at REV only | n/a | n/a | never |
| **the gate** `tools/mado-verify.sh` | **nothing** — `grep -n 'mado-tripwire\|MADO_TRIPWIRE' tools/mado-verify.sh` is empty (0 matches) | n/a | n/a | never; it neither invokes nor parses the tripwire |

## 5. Measured blast radius (commands + output)

### 5.1 Marker + counts added to a byte copy: nothing breaks

Copy `/tmp/r20s/tool/tool-keys.py` = e629f73 bytes with `"evidence": "observed"` in the row dict and top-level `observed_findings`/`lead_findings` ints.

```
for d in <11 suites>; do python3 -I /tmp/r20s/tool/tool-keys.py --selftest $d | tail -1; done
  16/16, 9/9, 33/33, 30/30, 31/31, 1/1, 45/45, 13/13, 34/34, 18/18, 17/17   (247/247, none dropped)
python3 -I tool-keys.py --frozen .ufo/waves/round-18/frozen  → frozen_verdict_mismatch (same extra rows as stock)
python3 -I tool-keys.py --frozen .ufo/waves/round-19/frozen  → frozen_match, exit 0
python3 -I frozen-repin.py --from .ufo/waves/round-19/frozen --to /tmp/r20s/repin --tool tool-keys.py
  → MADO_FROZEN_REPIN: written, exit 0; replay of the re-pin → frozen_match
```

A `want_findings` row with `"evidence": "lead"` added in a copy of `r19-helperfn/expected.json` was silently ignored: `CASE py-lead-cross-cell-literal ok`, `34/34`. So **`--selftest` cannot pin the marker**; only `tw-precision.py` can.

### 5.2 Rule-B attribution over every committed suite and both frozen baselines

An instrumented import (rule prefixed `B[<callee>]:rule`) over all 283 `scan` cases across every `mado-tripwire-selftest-v1` `expected.json` in the lane (the 11 admitted suites plus the round-17 `w2/` and round-18 `drafts/` suites) and over both frozen `inputs/`:

- Suites: exactly **2** cases contain rule-B rows — `r19-helperfn/py-lead-cross-cell-literal` (`B[run_record]:pacman:-Q`, line 1) and `r19-helperfn/py-lead-two-calls` (`B[record_command]:pacman:-Qi`, line 1). No other case in 247 assertions is rule-B, so E2/E1 markers alone cannot move any suite.
- Frozen `round-19/frozen`: exactly **1** rule-B row, `inputs/r13-root.jsonl:4` (`B[run_record]:pacman:-Q`). The other 10 expected rows are bash cells (r15-libinput-events:1, r13-global-capture:1, r14-review-source-bar:1) and literal-spawn eval cells (r14-source-safety:2,3 — `subprocess.run(["bash","-c",recipe])` with `recipe` a folded literal). `round-18/frozen` has **0** rule-B rows; its replay already mismatches with the same three extra rows before and after the key change.
- Consequence for the C1 guard “tw-recall 6/6 and reported split”: at `e629f73` the recall is `6/6, score 10.0` (`python3 -I .ufo/waves/round-19/tw-recall.py e629f73`), and under a compliant tool the split is **5 observed + 1 lead** (r13-root:4). If leads were moved out of `findings`, recall drops to 5/6 and `round-19/frozen` flips to mismatch.
- `round-19/frozen` must keep matching: `round-20/harm-watch.sh:347-357` replays `round-19` and `round-20` frozen dirs with `run_pinned` (nonzero exit = FAIL).

### 5.3 Suite cases that a *literal* reading of E1/E3 would flip (contract–fixture collisions)

All are `scan` cases in `.ufo/waves/round-19/tripwire/r19-helperfn/` and currently pass:

| Case | Fixture shape | Today | Literal E1/E3 reading | Risk |
|---|---|---|---|---|
| `py-helper-redefined` (clean) | two identical `def run(cmd): os.system(cmd)`, call `run('pacman -S wayland')` | clean (duplicate defs filtered) | E3 latest-binding ⇒ second def resolves ⇒ observed `host_mutation/pacman:-S` | suite FAIL (exit 0→1) |
| `py-helper-binop-body` (clean) | body `subprocess.run(args + ['--noconfirm'])`, call with literal list | clean (list+list folds to LITERAL_MISS → unparsed) | “argv reaches a spawn in that body” ⇒ observed | suite FAIL if list concatenation is folded |
| `py-helper-default-nonliteral` (clean) | `def run(args, timeout=T): subprocess.run(args, timeout=timeout)` | clean (`bind_literal` refuses non-literal default) | a body-only fallback scan emits a row | suite FAIL if the refused binding is bypassed |
| `py-helper-defined-after-call` (clean) | `run_record(['pacman','-Q','wayland'])` then `def` | clean — the def is indexed, so the order guard fails *and* `helper is None` is false; no row at all | resolving defs regardless of order emits a row | suite FAIL if the `lineno >` guard is dropped |
| `py-helper-vararg` (clean) | `def run(*a): subprocess.run(a)` | clean (`bind_literal` refuses varargs) | ambiguous | suite FAIL if varargs are folded |

The contract's E1 wording (“body visible … where the argv reaches a spawn in that body”) does not carve out these five; the fixtures do. L1 must either keep the current conservative behavior (recommended: it is what “all 11 existing suites pass” requires) or edit a case with its reason — the SCORECARD guard allows the latter only “with its reason” (`SCORECARD.md:1239-1262`).

### 5.4 Corpus: what rule B sees today

In-process instrumented scan of every `.jsonl` Python `glob` returned under `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin` (5623 paths, 0 `CouldNotEvaluate`; `find` reports 5714 matching names of which 5559 are regular files — the rest are non-regular entries/hidden-dir differences, `[INFERENCE]` on the cause): **23 rule-B rows**, callees `RuntimeError` 21, `run_record` 1, `run` 1.

- The 21 `RuntimeError` rows are the *same* harm class as `frozenset`: exception classes are builtins absent from `PURE_ARG_CALLS`, and the fixture constructs them with a literal argv (`.ufo/waves/round-19/tripwire/...` sibling transcript `TameshiR18.X06DispositionGuards.jsonl:60,81,87,93,96`). E2's “a Python builtin not rebound (frozenset, set, tuple, list, dict, type, …)” must be read to include exception types/`format`, or 21 of 23 corpus B rows stay false positives.
- The 1 `run` row (`MadoR18.CriticC2W2.jsonl:56`, `vcs_write/git:checkout`) and the 1 `run_record` row (`MadoR13.jsonl:470`, `package_query/pacman:-Q`, the round-19 recall row) are genuine leads.
- [INFERENCE] Dedupe: `scan_file` drops a second hit with the same `(class, rule)` in one tool call; a probe run of the corpus counted **1876** such suppressed tuples. Extending the dedupe key with `evidence` is not required by E1 and can only add rows (then every frozen baseline needs a re-pin).

## 6. Exact break list (what L1 must not do)

1. **Do not remove lead rows from `findings` and do not make leads permitted** — E1 keeps them in `findings`/exit 1; otherwise `tw-recall.py` 5/6, `round-19/frozen` mismatch, `round-20/harm-watch.sh` FAIL.
2. **Do not put the new counts inside `counts`** — `recut-receipts.sh:423-424` compares the `counts` dict exactly (also `corpus-diff`/`tw-precision` never read it). Top-level integers are safe.
3. **Do not add a top-level key to `expected.json`** — `FROZEN_KEYS` `:1688-1690` + `:1716-1719` turn every frozen baseline into `frozen_error` exit 2. Row-level `evidence` keys are accepted but never read (`run_frozen` `:1960-1961`), so hand-adding them to a baseline is inert; a re-pin via `frozen-repin.py` silently drops them.
4. **Keep the marker value domain to exactly `observed`/`lead` (or omit the key)** — `tw-precision.py:81-86` and `tw-recall-split.py:85-87` exit 2 on anything else; `tw-precision` treats a missing key as observed, `tw-recall-split` as `unmarked`, `corpus-diff` as observed.
5. **Do not change any `(class, rule, line)` on the 5 round-19 pinned inputs or the 2 rule-B suite cases** — reproduce with `python3 -I <tool> --frozen .ufo/waves/round-19/frozen` and `--selftest .../r19-helperfn` before landing.
6. **Gate untouched** — `tools/mado-verify.sh` has no tripwire reference, so C1 cannot break the gate; only the 11 suites + two frozen dirs + three counters need re-running (`round-20/harm-watch.sh` covers them).

## Limits

- Did not re-measure the whole-corpus base-vs-new diff (CorpusDiff seat owns it); my corpus numbers are the e629f73 tool only.
- Did not run the live gate, any host probe, pacman, jj, or any transcript content.
- Did not evaluate E4 (vcs help/dry-run) paths; the `vcs_write` classifier is outside this question except where rule-B rows carry `vcs_write` (21 `RuntimeError` rows above).
- Field-set equality of the `--scan`/`--frozen` payloads was checked against every in-lane reader I could find by grep of the whole lane (including `.ufo/waves/round-20/` counters landed by peers); `grep -rl 'mado-tripwire' /home/vgpnk/Projects/shokunin/scripts /home/vgpnk/Projects/shokunin/templates` returns 0 files, so no fleet script consumes the verdict. A consumer outside those trees remains `[UNK]`.
- `[INFERENCE]` items: the file-count reconciliation; the claim that the 1876 deduped tuples would be the only source of new rows if the dedupe key changes; that no existing suite case has an alias/`partial`/async/decorated-def shape (checked by grep for those tokens in every suite `.jsonl`, 0 true matches).

## Installs

none
