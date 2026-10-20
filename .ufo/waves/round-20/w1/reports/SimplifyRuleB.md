# SimplifyRuleB — at e629f73 rule B has no evidence marker; one ordered, scope-recursive binding map deletes `funcs`, `scoped_call_ids` and the alias pre-pass (82 lines), and 4 of the 9 case edits the lane later made fall out of it

Target: `e629f731172b8238caffe50f152217ce56535fb4`, tool
`367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`, 2128 lines (identical at
`1f7f995`). No lane edit was made: every prototype lives in `/tmp/r20-simplify/` (built from
`git show` / `git archive` only). §8 records what has since landed at HEAD, because the lane
moved while this was measured and two readings differ.

## 1. What e629f73 does (measured, official counter)

`python3 .ufo/waves/round-20/tw-precision.py <REV> --suite-rev f3da504` (175 scored cases):

| revision | score | passed | P | S | W | H | L |
|---|---|---|---|---|---|---|---|
| `e629f73` = `1f7f995` | 1.6571 | 29/175 | 7/66 | 2/17 | 4/22 | 15/52 | 1/18 |
| `9c54c56` (pre-harm) | 6.2857 | 110/175 | 66/66 | 7/17 | 1/22 | 35/52 | 1/18 |

- **E1 absent, not approximate.** `grep -c '"evidence"' tools/mado-tripwire.py` → 0. Every row
  is built at one site, `classify_segment`'s `hit()` (`:902-903`); `helper_argv_leads`
  (`:1379-1390`) feeds the same 4-tuple through `classify_shell`, so a lead is byte-identical
  to a real spawn. The round-19 harm reproduces: `BLOCK=frozenset(['pacman','-Q','hyprland'])`
  → exit 1, one `package_query/pacman:-Q`, **no marker**
  (`/tmp/r20-simplify/probes/p-frozenset.jsonl`, sha256 `7570876fa0d8…`).
- **E3 absent.** `PURE_ARG_CALLS` (`:1252-1259`) is consulted by bare spelling only
  (`:1430-1434`), never against a binding; `frozenset` and `type` are not in the table, and no
  rebinding ever revokes the exemption.
- **E1's helper clause is per cell and undecorated-only.** `funcs` is built inside
  `classify_eval` (`:1368-1372`, `not node.decorator_list`) with the order guard
  `node.lineno > helper[0]` (`:1411-1412`): decorated, `async def`, `lambda` and cross-cell
  helpers are all leads today.

## 2. Smallest design that satisfies E1-E3

Three authorities instead of seven:

1. **One ordered, scope-recursive binding map.** `name → Literal(value) | Callable(node) |
   Imported(module, attr) | SpawnAlias(canonical) | PURE | OPAQUE`, written by
   `bind_stmt(stmt, env)` in statement order, carried across cells in the existing
   `envs["py"]`, and read by `scan_block` per statement — so E3's "the binding in effect at the
   call wins" is structural, not re-derived from line numbers. `params` is a separate map of
   literal-bound same-text parameters only, so folding an argument never reaches through a
   module variable.
2. **One purity predicate.** `pure_callable_value(node, env)`: builtin table when unbound (now
   incl. `frozenset`, `type`, `ascii`, `bool`, `callable`, `format`); `PURE`; `Imported` iff its
   module is in `PURE_STDLIB_MODULES`; a bound method of a literal string (`STR_METHODS`).
   `pure_target` extends it to straight-line assignments (`d = json.dumps`,
   `p = functools.partial(json.dumps, …)`, `s = '{!r}'.format`, `P = namedtuple('P', …)`).
   The lead side is one predicate, `leads(binding)`: absent, `OPAQUE`, or `Imported` from
   outside the pure set. A name bound to a stated literal cannot spawn — no row
   (`S-…-b09`'s `record = None`).
3. **One call enumerator.** `scope_calls(stmts)` yields calls made in a scope; `nested_bodies`
   returns `(body, parameter names)` for the scopes a statement defines. An uncalled body is
   read with the block's **late** callables (every def/class/lambda the block binds at any
   position) and its own parameters masked `OPAQUE` — globals resolve at call time, outer
   literal values never — so an uncalled body is read without being guessed at. A called body is
   rescanned with the caller map + masked params + literal-bound params.

E1 marking is two behaviors: `hit()` appends `"observed"`; `helper_argv_leads` re-tags its
`classify_shell` rows `"lead"`. The per-tool-call dedupe key becomes `(class, rule, evidence)`
(without it an observed and a lead row of one class/rule collapse — measured
`x-mixed-observed-lead`, same shape as committed `c03`), the finding gains `"evidence"`, and
`--scan` adds `observed_findings` / `lead_findings`. `--selftest` keys on `(class, rule, line)`
and `--frozen` on `(file, line, class, rule)`, so the key disturbed no suite or pin (127/127 at
the marker-only step).

`spawn_alias` binds E1's alias shapes (`run = subprocess.run`,
`functools.partial(subprocess.run, …)`, os/asyncio/exec forms) and resolves dotted heads through
`Imported`; that deletes the order-insensitive `aliases`/`from_subprocess` pre-pass.

## 3. Deletions and unifications (e629f73 → `/tmp/r20-simplify/proto8.py`, 2128 → 2323)

| mechanism at `e629f73` | lines | verdict | counted |
|---|---|---|---|
| `funcs` index `:1368-1372` + lookup `:1411-1412` | 7 | **delete** — `Callable` in the carried map; the per-call map already gives call-site order, so the `lineno >` guard and the duplicate-def kill both go | inside `classify_eval` −39 |
| `scoped_call_ids` `:1190-1217` | 28 | **delete** — its rule ("a body resolves no module name at its definition point") becomes `nested_bodies`(12) + `scan_block`'s own scan; the id set and `scoped` threading disappear | replaced by `scope_calls`(32)+`nested_bodies`(12) |
| `bind_literal` `:1260-1298` | 39 | **keep the binder, delete the defaults**: E1's observed test is whether *the argv* reaches a spawn in the visible body; a non-literal `timeout` default cannot change that, and one unresolvable non-argv parameter must not abort the binding | −7 (32) |
| `helper_argv_leads` `:1379-1390` | 12 | **keep** — the single lead emitter needs exactly one tag site; its gate becomes `not pure_callable_value(...) and leads(binding)` | +1 (13) |
| `module_unsafe_names` `:1135-1187` | 53 | **shrink** — def/class, import and delete move to the ordered binder; the purge becomes `env[name] = OPAQUE` so a rebound pure name loses its exemption; for/with/except/aug/walrus/global/match/comprehension stay (E3 does not order them) | −8 (45) |
| `classify_eval` `:1301-1376` | 76 | **shrink** — funcs, `call_env`, the alias/`from_subprocess` pre-pass and the statement loop leave; it keeps parse + one `scan_block` call | −39 (37) |

**Deletions: 82 lines** (28 + 39 + 7 + 8). Additions: `bind_stmt` 30, `scan_block` 34,
`scope_calls` 32, `nested_bodies` 12, `callables` 7, `param_names` 9, `leads` 13,
`pure_callable_value` 16, `pure_target` 10, `spawn_alias` 27, `spawn_scan` +18, `literal_value`
+3, marker/counts ~5, binding classes and tables ~50, docstrings/blanks the rest: **290 added,
net +195**. A `pure_call` predicate was written and then deleted (13 lines) once measurement
showed `pure_callable_value` already covers the purity test.

## 4. Measured prototype (pinned suite f3da504)

`/tmp/r20-simplify/proto8.py`, sha256
`d6a76c8c5432462c0a273576ba75ef860c562bce8df7995cddc2b0d5a2fc3820`, not a lane artifact. The
scorer `/tmp/r20-simplify/replica.py` implements the counter's exact rule (digest-checked suite
bytes, `Counter((class, rule, line, evidence))`, missing key = observed, exit equality) and
reproduced the official baselines exactly (29/175, 110/175).

- **134/175 = 7.6571** — P 66/66, S 17/17, L 18/18, W 18/22, H 15/52. The 41 failures are all
  E4 (`vcs_write` help/dry-run, absent at e629f73): 37 H and 4 W that need `git commit -n` /
  `jj commit -n` inside vararg helpers.
- **Held-out 0/12**, at tip and at the prototype. All 12 are self-labelled "EDGE (outside the
  TwRuleB/TwVcsHelp patch scope)": shell-function shadowing and shell multi-hop, `xargs`/pipe to
  bash, `jj --version`, `uv tool install --help`, `pip install --help` — a shell-side and
  installer-help signal, not rule-B.
- **Corpus no-loss**: all **369** committed `*.jsonl` at e629f73 → **0 rows lost vs tip and vs
  `9c54c56`**, 6 rows gained only in three flipped case files (r18 draft + r19 copy each),
  `unparsed_spawns` differs on **0/369**.
- **Frozen r18 baseline**: same as tip (`frozen_verdict_mismatch`, 0 missing / 3 extra); the pin
  is already stale at tip, and this design adds no drift.
- Probes: `frozenset`/`type`/`from shlex import join` clean; `from mymod import frozenset` lead;
  `def print(argv): subprocess.run(argv)` observed; `del print` clean; class/`@dataclass` with a
  literal argv clean; decorated/async/lambda/cross-cell helper observed; spawn aliases observed;
  helper + unknown callee in one cell → two rows (`observed` + `lead`).

## 5. Contract collisions the design implies (pre-integration reading)

Against the r19 negatives as they stood at e629f73, this design yields: `defined-after-call` →
**lead** (the call precedes the def, so at the call the callee is unbound); `redefined` →
**observed** (latest preceding binding); `default-nonliteral` → **observed**. Those three were
the only flips it produced in the committed suites (31/34 in `r19-helperfn`, everything else
full: bashcvar 45/45, installers 18/18, vcs 17/17, frozen-f1f2 13/13).

## 6. Sibling artifact

`.ufo/waves/round-20/w1/reports/TwRuleB.md` (`TwRuleB.patch` sha256 `9d3487c68ea8e9ff…`,
`TwRuleB-v2.patch` sha256 `be214cfcc7574f52…`) implements the same marker, the same
`(class, rule, evidence)` dedupe, `del` restoring builtin lookup, spawn aliases, and agrees on
`defined-after-call` = lead. It differs on two readings: it reports
`W-CaseWrapperForms-class-method-instance` as observed (the authored case is an explicit control
pinning 0: "E1 lists def/async def/lambda helpers only"), and it folds call-site literal bindings
into helper arguments and class bodies, widening E1 beyond "a call with literal argv". §8 records
how that was resolved.

## 7. Boundaries

- **E4** (`git`/`jj` help and dry-run) is unimplemented at e629f73 and outside this design; it
  owns the 41 remaining pinned-suite failures. Additive, ~10-15 lines in `classify_git`.
- A class instantiated with a literal argv is not followed into `__init__` (E1 names
  def/async def/lambda helpers; E2's class clause only needs the body read).
- Keyword argv, starred exec argv and `**kwargs` forwarding are read (authored W cases demand
  them) and counted in the additions.
- `[UNK]` whether L1 wants the two integer counts in the frozen verdict payload; `--frozen` and
  `--selftest` ignore the evidence key today.

## 8. Post-integration state (observed after this design was measured)

HEAD moved to `28c68378eccbd5f227cdc28a62406ff390e3540a` (tool blob `5f0bac58…`, 2612 lines,
+484), pinning `SUITE_PIN = f3da504` in the counter. Measured with the official counter:
**172/175 = 9.8286** (H 51/52, L 17/18, P 66/66, S 17/17, W 21/22).

- Deletions taken there, per function: `scoped_call_ids` −28, `classify_eval` −44 (the `funcs`
  block and the alias/`from_subprocess` pre-pass, i.e. three of the four deletions above),
  `helper_argv_leads` −3, plus `first_verb` −10 and `ignores_working_copy` −1 for E4.
- Not taken: `bind_literal` grew +17 (vararg/class support, defaults kept), and
  `module_unsafe_names` is unchanged. Instead of one map it keeps two parallel environments
  (`update_bindings` +89, `callable_info` +54, `assignment_binding` +43, `prepare_eval_calls`
  +27, `eager_calls` +29, `spawn_scan` +50).
- It moved the contract in six places, each with an `r20_edit` reason in
  `r19-helperfn/expected.json` and `r19-bashcvar/expected.json`: `py-helper-nonliteral-arg`
  → observed, `py-helper-vararg` → observed, `py-helper-default-nonliteral` → observed,
  `py-lead-nonliteral-var` → lead, `py-lead-defined-nonliteral` → observed, and
  `r19-class-body-deferred-clean` → observed (a class body executes at the class statement;
  `r19-lambda-deferred-clean` stays 0). The class-body reading is the CPython execution model and
  is better evidence than the r19 "deferred" convention this design preserved.
- Consequence for the ledger: against HEAD's committed suites, `proto8` scores `r19-helperfn`
  30/34 (`py-helper-nonliteral-arg`, `py-helper-vararg`, `py-lead-nonliteral-var`,
  `py-lead-defined-nonliteral`) and `r19-bashcvar` 44/45 (`r19-class-body-deferred-clean`). The
  deletions above remain valid and were taken; the single-map unification is **not** required —
  HEAD reaches 172/175 with two environments — and the four "kept at 0" cases in this design are
  now contrary to the lane's contract.

## Limits

- The prototype is unreviewed by another seat. It was measured against the committed suite at
  `f3da504` (digest-checked) through a local reimplementation of the official counter, validated
  on both official baselines; `--heldout` was run only through that replica.
- `tw-recall.py`'s 6/6 split and the "20 control lines" were not run; the stronger no-loss
  property (369 transcripts, 0 rows lost vs tip and vs `9c54c56`, 0 unparsed-stat diffs) was.
- §8 was measured after the integration landed; I did not review the integrated patch beyond its
  per-function deltas, suite edits and counter score, so I cannot say whether its two
  environments are load-bearing or vestigial.
- `CaseAdoptW2`'s H set and the four W-vararg cases are classified E4-dependent from their
  expected `vcs_write` rows, not verified case by case beyond the dry-run/help probes.

## Installs

none
