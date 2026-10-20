# SimplifyRuleB — rule B carries no evidence marker at all; one ordered binding map deletes `funcs` and rule-B's second name authority, and 82 lines go with them

Lane HEAD observed `e629f731172b8238caffe50f152217ce56535fb4`; tool
`tools/mado-tripwire.py` sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`
(2128 lines), byte-identical at `1f7f995`. No lane edit was made: every prototype below
lives in `/tmp/r20-simplify/` (`git show` + `git archive` only). The only working-tree
change in the lane is `SCORECARD.md` (+33), which is L1's, not mine.

## 1. What e629f73 actually does (measured)

- **E1 is absent, not approximate.** `grep -c '"evidence"' tools/mado-tripwire.py` → 0.
  Every finding row is built at one site, `classify_segment`'s `hit()`
  (`tools/mado-tripwire.py:902-903`), and `helper_argv_leads` (`:1379-1390`) feeds the
  same 4-tuple through `classify_shell`, so a lead row is byte-indistinguishable from a
  real spawn. The round-19 harm reproduces at tip:
  `BLOCK=frozenset(['pacman','-Q','hyprland'])` → `MADO_TRIPWIRE: findings`, exit 1,
  one `package_query/pacman:-Q` row, **no marker**
  (`/tmp/r20-simplify/probes/p-frozenset.jsonl`, shasum `7570876fa0d8…`).
- **E3 is absent.** `PURE_ARG_CALLS` (`:1252-1259`) is consulted by bare spelling only,
  `name not in PURE_ARG_CALLS` (`:1430-1434`), never against a binding; `frozenset` and
  `type` are not in the table at all, and a rebinding never revokes the exemption
  (`rename` probes below).
- **E1's helper clause is per-cell and undecorated-only.** `funcs` is built inside
  `classify_eval` (`:1368-1372`) with `not node.decorator_list`, and the guard is
  `node.lineno > helper[0]` (`:1411-1412`): decorated, `async def`, `lambda`, and
  cross-cell helpers are all leads today (probe matrix, §4).
- **Authored round-20 suite** (the 187 cases the seats have written into
  `.ufo/waves/round-20/w1/cases/*/` at the time of writing): tip **29/187**;
  pre-harm `9c54c56` (tool `c1ae45a7…`) **113/187** — it passes every P case only
  because it has no lead rule at all, and fails every L/W case.

## 2. Smallest design that satisfies E1-E3

Three authorities instead of seven:

1. **One ordered, scope-recursive binding map.**
   `name → Literal(value) | Callable(node) | Imported(module, attr) | SpawnAlias(canonical) | PURE | OPAQUE`,
   written by `bind_stmt(stmt, env)` in statement order and carried across cells in the
   existing `envs["py"]`. Each call is classified by `scan_block(stmts, env, params, depth)`
   with the map as of its own statement, so "the binding in effect at the call wins"
   (E3) is structural instead of re-derived from line numbers.
   `params` is separate and holds only literal-bound same-text parameters, so folding an
   argument never reaches through a module variable (keeps the r19 negatives).
2. **One purity predicate.** `pure_call(name, snapshot)`: unbound → builtin table (now
   with `frozenset`, `type`, `ascii`, `bool`, `callable`, `format`); `PURE` → exempt;
   `Imported` → exempt iff its module is in `PURE_STDLIB_MODULES`; anything else is
   judged by its binding. `pure_callable_value`/`pure_target` extend the same rule to a
   straight-line assignment (`d = json.dumps`, `p = functools.partial(json.dumps, …)`,
   `s = '{!r}'.format`, `P = namedtuple('P', …)`).
3. **One call enumerator.** `scope_calls(stmts)` returns the calls made in a scope;
   `nested_bodies(stmt)` returns the bodies one statement defines. A body is scanned
   with a fresh map when uncalled (still read, never guessed) and rescanned at a same-text
   call with the caller map + its parameters masked `OPAQUE` + the literal-bound ones.
   This is what makes E1's decorated/async/lambda/cross-cell helpers observed and E2's
   transitive pure bodies clean.

E1 marking lives in exactly two places: `hit()` appends the 5th field `"observed"`, and
`helper_argv_leads` re-tags the rows it gets from `classify_shell` as `"lead"`. The
per-tool-call dedupe key becomes `(class, rule, evidence)` (otherwise an observed and a
lead row of one class/rule in one cell collapse — measured, `x-mixed-observed-lead`),
the finding gains `"evidence"`, and `--scan` adds `observed_findings` / `lead_findings`.
`--selftest` keys on `(class, rule, line)` and `--frozen` on `(file, line, class, rule)`,
so the new key disturbs no suite and no pin (measured at proto2: 127/127).

`spawn_alias` binds E1's named alias shapes (`run = subprocess.run`,
`functools.partial(subprocess.run, …)`, plus os/asyncio/exec forms) and resolves dotted
heads through `Imported`; that deletes the order-insensitive `aliases`/`from_subprocess`
pre-pass, which made an import anywhere in a cell a spawn everywhere.

## 3. Per-candidate verdicts and line counts (e629f73 → proto8, 2128 → 2303)

| mechanism at e629f73 | lines | verdict | counted delta |
|---|---|---|---|
| `funcs` index `:1368-1372` + lookup `:1411-1412` | 7 | **delete** — `Callable` in the carried map; the per-call map already gives call-site order, so the `lineno >` guard and the duplicate-def kill both go | inside `classify_eval` −39 |
| `scoped_call_ids` `:1190-1217` | 28 | **delete** — its rule ("a body resolves no module name at its definition point") becomes `nested_bodies`(10) + `scan_block`'s fresh-map scan; the id set and the `scoped` threading disappear | replaced by `scope_calls`(32)+`nested_bodies`(10) → +14 |
| `bind_literal` `:1260-1298` | 39 | **keep the binder, delete the defaults**: E1's observed test is only whether *the argv* reaches a spawn in the visible body; a non-literal `timeout` default cannot change that, and an unresolvable non-argv parameter must not abort the binding | −7 (32 lines) |
| `helper_argv_leads` `:1379-1390` | 12 | **keep** — the single lead emitter needs exactly one tag site; its gate `name not in PURE_ARG_CALLS` becomes `pure_call(name, env)` | +1 (13) |
| `module_unsafe_names` `:1135-1187` | 53 | **shrink** — def/class, import and delete branches move to the ordered binder; the cell-start purge becomes `env[name] = OPAQUE` so a rebound pure name loses its exemption (E3); for/with/except/aug/walrus/global/match/comprehension stay (E3 does not order them) | −8 (45) |
| `classify_eval` `:1301-1376` | 76 | **shrink** — the funcs block, `call_env`, the alias/`from_subprocess` pre-pass and the statement loop all leave; it keeps parse, cell-start unsafe mark, one `scan_block` call | −39 (37) |

Totals: **82 lines of mechanism deleted** (28 `scoped_call_ids` + 39 `classify_eval` +
7 `bind_literal` + 8 `module_unsafe_names`). Additions required by E1-E3 and counted in
the prototype: `bind_stmt` 30, `scan_block` 24, `scope_calls` 32, `nested_bodies` 10,
`param_names` 9, `spawn_alias` 27, `pure_call` 15, `pure_callable_value` 16,
`pure_target` 10, `spawn_scan` +17, `literal_value` +3, marker/counts ~5, binding classes
and tables ~40. **Net +175** at `/tmp/r20-simplify/proto8.py`.

I also measured a smaller, weaker variant (`proto5b`, 2183 lines, +55): the same
deletions, but the binding map stays module-level (no nested scope), lambdas and
pure-callable assignments are not bound, and the old alias pre-pass is extended by 16
lines instead of `spawn_alias`. It scores **99/187** — it fails the E1/E2 lambda,
nested-def, transitive-class and pure-callable cases because a module-only map cannot see
a nested scope — so it is not contract-complete. The recursive map is the smallest shape
I found that satisfies the authored E1-E3 receipts, not the smallest possible diff.

Nothing in the deleted set is provenance: every line above is live rule-B machinery at
`e629f73`, and each deletion is exercised by a suite case, so none is "unreachable by
inspection only".

## 4. Measured prototype (no lane edit)

Prototype `/tmp/r20-simplify/proto8.py`, sha256 `92a1c5420df2a2b6ec75a2ee2dfa344b689496e4b9c90f6709e904e30ce30823`
(**not** a lane artifact); scoring helper `/tmp/r20-simplify/score.py`, sha256
`39ebb110182bd03e9b408a3a159e2c30a3c4f0d623e3929e42a6ec59a013515e`.

- **Committed suites** (extracted from `e629f73`): `r19-bashcvar` 45/45,
  `r19-frozen-f1f2` 13/13, `r19-installers` 18/18, `r19-vcs` 17/17; `r19-helperfn`
  **31/34** with exactly the three contract collisions below. Tip baseline: 127/127.
- **Authored round-20 suite**: **132/187**. Every non-E4 seat is full: PureBuiltins 8/8,
  PureCallables 14/14, PureCollections 6/6, PureCrossCell 7/7, PureFormatters 13/13,
  Shadowing 16/16, LeadsInvisible 6/6, WrapperCrossCell 8/8, WrapperForms 9/9. All 55
  remaining failures are H families (DryRunBash 7, HelpBash 12, HelpDryRunEval 13,
  AdoptW2 23) = **E4**, which is unimplemented at tip: `git commit --dry-run`,
  `git add -n`, `git push -n` and `git commit -h` all emit `vcs_write`
  (`/tmp/r20-simplify/probes/x-git-dryrun.jsonl`), while `git commit -n` must keep
  emitting. E4 is additive (~10-15 lines in `classify_git`), outside this ticket's scope.
- **Corpus no-loss**: all **369** committed `*.jsonl` at `e629f73` scanned by tip and by
  proto8 → **0 rows lost vs tip, 0 rows lost vs `9c54c56`**, 6 rows gained, only in the
  three flipped case files (`r18` draft + `r19` copy each). No frozen input and no
  control file gains a row. `unparsed_spawns` differs on **0/369** files.
- **Frozen r18 baseline**: same outcome as tip — `frozen_verdict_mismatch`, 0 missing /
  3 extra. The pin is already stale at tip (round-19 detection), so this design adds no
  drift; re-pin is L1's decision.
- **Probe matrix** (tip → proto8; `evidence` key shown when present):

| probe | tip | proto8 |
|---|---|---|
| `frozenset(['pacman','-Q',…])`, `type`, `from shlex import join` | row, no marker / row / row | clean / clean / clean |
| `from mymod import frozenset; frozenset([...])` | row, no marker | `lead` |
| `def print(argv): subprocess.run(argv); print([...])` | row, no marker | `observed` |
| `print([...]); del print; print([...])` | clean | clean (builtin restored — CPython reading, matches the S case) |
| plain class / `@dataclass` constructed with a literal argv | row, no marker | clean |
| `@decorator def run`, `async def`, `run = lambda`, def in an earlier cell | row, no marker | `observed` |
| `run = subprocess.run`, `run = functools.partial(subprocess.run, …)` | row, no marker | `observed` |
| helper (observed) + unknown callee (lead), same cell | 1 row | 2 rows: `observed` + `lead` |

## 5. Contract collisions — three case edits, each with its reason

1. `r19-helperfn/py-helper-default-nonliteral` (and `r18` draft twin): 0 → observed.
   E1's observed test is "the argv reaches a spawn in that body"; a non-literal `timeout`
   default cannot change that. Keeping the old reading costs the 11-line defaults block
   and leaves E1 unmet.
2. `py-helper-defined-after-call`: 0 → observed. The body is visible in the same cell;
   textual position of the `def` does not change whether the argv is stated. Keeping it
   requires reinstating the `lineno >` guard this design deletes.
3. `py-helper-redefined`: 0 → observed. E3: the latest preceding binding wins, and both
   defs spawn.

All three sit in the round-19 helperfn negative set only; the C1 guard allows a case edit
with its reason, and the corpus no-loss guard is unaffected (0 lost).

## 6. Sibling artifact — one implementation already exists, with two divergences

A sibling seat has already written patches for this area
(`.ufo/waves/round-20/w1/reports/TwRuleB.md`; `w1/patches/TwRuleB.patch` sha256
`9d3487c68ea8e9ff…`, `TwRuleB-v2.patch` sha256 `be214cfcc7574f52…`). Its structure
agrees with mine on the marker, the dedupe key `(class, rule, evidence)`, `del` restoring
builtin lookup, and spawn aliases/`functools.partial`. Three readings differ, and two of
them are measurably against authored receipts:

1. **`W-CaseWrapperForms-class-method-instance`** — the authored case is an explicit
   control: `CaseWrapperForms/cases.json` says "E1 lists def/async def/lambda helpers
   only and E2 keeps attribute/method calls unflagged, so it stays clean
   (unparsed_spawns 1)" and pins `want_exit 0`. TwRuleB proposes to report
   `Runner().run([...])` as observed and edit the case. Doing so fails the C1 receipt as
   written; this design keeps 0 (proto8 scores CaseWrapperForms 9/9).
2. **Call-site literal folding into helper arguments** — TwRuleB V2 folds a literal
   assigned before the call into the helper body, which flips
   `r19-helperfn/py-helper-nonliteral-arg` and `py-lead-defined-nonliteral` to observed.
   Both are pinned 0, and E1 conditions observed on "a call **with literal argv**"; a
   module variable is not literal at the call. This design keeps both 0 (measured: the
   `r19-helperfn` suite fails only the three cases in §5).
3. **`py-helper-defined-after-call`** — both seats agree exit 1, TwRuleB as `lead`, this
   design as `observed` (the body is visible in that cell). L1 must pick one marker
   before editing the expectation; the row's class/rule/line are identical either way.

## 7. Boundaries and residuals

- E4 untouched (§4). Keyword argv (`subprocess.run(args=[…])`), starred exec argv and
  `**kwargs` helpers are read by the prototype because authored W cases demand them
  (E1's "literal spawn"), and are counted in the additions, not the deletions.
- A class instantiated with a literal argv is not followed into `__init__`: E1 names
  def/async def/lambda helpers, and E2's class clause only requires the class body be
  read (it is). The authored `transitive-class` case agrees (0).
- `[UNK]` whether L1 wants `observed_findings`/`lead_findings` in the frozen verdict
  payload too (+2 lines if yes). `--frozen`/`--selftest` ignore the evidence key today.
- The body of a `def` never called is still counted as a finding when it spells a literal
  spawn; E1 has two states only, so it stays `observed`. If the suite later reads that as
  `lead`, it is a one-line change in the `nested_bodies` scan (tag `"lead"` when there is
  no invocation), not a structural one.

## Limits

- I did not run the official counters: `tw-precision.py` reads the suite at "the commit
  that first lands it", and the suite is still uncommitted working-tree data; I
  reimplemented its comparison rule (exit code + multiset of `(class, rule, line,
  evidence)`, missing key = observed) in `/tmp/r20-simplify/score.py` and scored the
  working-tree cases. `tw-recall.py`'s 6/6 and the "20 control lines" were not run; I
  proved the stronger no-loss property over all 369 committed transcripts instead.
- The prototype is unreviewed by another seat and was measured against case files that
  were still being written while I read them (`w1/cases/*` at 16:44-17:05); cases landing
  later are not covered. `CaseAdoptW2`'s H set is counted as E4-dependent without
  case-by-case verification beyond the dry-run/help probes.
- The +175 net is my prototype's count, not a line budget for L1's patch: a smaller
  contract-complete variant may exist that keeps `scoped_call_ids` (measured +4 lines
  over deleting it, one extra authority). I did not search below the measured design.

## Installs

none
