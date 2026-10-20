# AdvLeadMarks — partly falsified: lead/observed marks diverge from CPython binding reality in 11 shapes, and `globals()` reads fabricate lead rows on pure builtins

Attacked: the C1 precision claim "every finding row carries `evidence: observed|lead`" is
literally satisfied, but the *distinction* mis-describes the execution for the named
shapes. Contract under attack (tools/mado-tripwire.py:35-49 doc + corpus/knowledge/
tripwire-precision-r20.md:18-20,30-31): `observed` = "the transcript states the command
**and the path that runs it** … a helper whose body is visible in the same file";
`lead` = "a literal host argv handed to a callee whose body is not visible"; and "the
binding in effect at the call wins" (S111). Several shapes violate exactly that contract.

Tool scanned: /tmp clone @ a4046a8, `tools/mado-tripwire.py` sha256
9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c (matches the repair
hash). Command run, --scan only, fixtures never executed:

```
cd /tmp/mado-r20w2-AdvLeadMarks
python3 -I tools/mado-tripwire.py --scan /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w2/AdvLeadMarks
→ MADO_TRIPWIRE: findings   (every row listed below reproduced verbatim)
```

Runtime semantics for every shape were verified separately with `/bin/touch` canaries in
/tmp only (results quoted per item). No fixture contains a live command; `pacman -Q` is
inert text in data.

## A. `observed` although the visible body does not run the command

| # | Fixture (sha256) | Scan row | Runtime proof (canary) | Why the mark is wrong |
|---|---|---|---|---|
| A1 | obs-decorator-no-forward.jsonl `e8c3e370` | `observed pacman:-Q` | canary absent | `@dead` where `def dead(fn): return lambda *a: None`. The bound name resolves to the *decorator's return*, never the def's body. The tool follows the raw FunctionDef regardless of decorator (mado-tripwire.py:1554 binds `stmt` itself). Pinned `@functools.cache` cases hide this because `cache` is passthrough; a non-forwarding decorator is the counterexample. |
| A2 | obs-global-rebind.jsonl `a68c3478` | `observed pacman:-Q` | canary absent; `TypeError` | `def swap(): global run; run = print`; `swap()` then `run([...])`. The binding in effect at the call is `print`. `update_bindings` returns early for FunctionDef (line 1554) and never descends into `Global`, so the module binding is never invalidated even though the helper *was called*. `module_unsafe_names` does see `global x` (line 1318) — but only pops the literal `env`, not `bindings`. Asymmetric: env is protected, bindings are not. |
| A3 | obs-nonlocal-rebind.jsonl `b93dfffe` | `observed pacman:-Q` | canary absent; `TypeError` | Same defect one scope in: `nonlocal run; run = print` inside the called helper `outer`; the enclosing-scope binding survives in the tool. |
| A4 | obs-unbound-sp-alias.jsonl `5f54cad7` | `observed pacman:-Q` | NameError | Bare `sp.run([...])` with **no import at all** is treated as `subprocess.run` via the hardcoded `head == "sp"` rewrite (line 1498). An undocumented alias assumed bound; the command's path is invisible here. Same hole: `sp = print; sp.run([...])` is a *silent miss* while `sp.run` unbound is `observed`. |
| A5 | obs-unbound-subprocess.jsonl `4b049e98` | `observed pacman:-Q` | NameError | `subprocess.run([...])` with no `import subprocess` anywhere resolves through the unbound-dotted fallback (lines 1500-1501). The eval kernel likely has it imported, so this is a weak item — but it proves `observed` does not require a visible path. |
| A6 | obs-dead-if-false.jsonl `30a13137` | `observed pacman:-Q` | canary absent | `if False: subprocess.run([...])` collected by `eager_calls` (line 1664) with no condition evaluation. Consistent with "issued ≠ executed", but worth naming: `observed` currently means "textually present", not "reachable". |

## B. `lead` although the executing body is visible in the same file

Each fixture's call provably executes the visible spawn-bearing body (`/bin/touch`
canary present). The row is emitted as `lead`, i.e. "callee's body is not visible".

| # | Fixture (sha256) | Mechanism |
|---|---|---|
| B1 | lead-closure-factory.jsonl `bfd26513` | `run = make()` where `make` returns the nested `def run`: `assignment_binding` sees a Call with unknown callee kind → `{"kind":"unknown"}`. Body visible, executes, marked lead. |
| B2 | lead-conditional-lambda.jsonl `cf938152` | `run = (lambda a: subprocess.run(a)) if True else print`: `IfExp` is not in `assignment_binding`'s literal whitelist → unknown → lead. |
| B3 | lead-multi-target.jsonl `9efe0de0` | `run = helper = lambda a: subprocess.run(a)`: `len(names) > 1` → `{"kind":"unknown"}` (line 1586). The same literal binds both names; folding is blocked only by target count. |
| B4 | lead-if-true-def.jsonl `361ad7b4` | `if True: def run(a): return subprocess.run(a)`: `visit()` (line 1603) marks any def under a branch `unknown` unconditionally. The `if True:` condition is foldable — this is the sharpest guard-blindness case. |
| B5 | lead-try-def.jsonl `8ab0a41e` | `try: def run…except: pass`: try-with-trivial-body poisoned the same way; the def executes whenever the body doesn't raise. |
| B6 | lead-star-import-no-rebind.jsonl `95db5e2b` | `from collections import *` (a *pure* stdlib module) clears every binding via `opaque_statement` (line 1391). `collections.__all__` cannot export `run`; the earlier def still executes. `opaque_module_mutation` does not consult the module's purity or `__all__`. |
| B7 | lead-exec-literal-noop.jsonl `b27037d2` | `exec('pass')` — a *literal, provably non-binding* payload — still clears all bindings (OPAQUE_PY_DOTTED matched by name only, line 1373). The tool's own doc at line 54 claims opaque clearing happens for `exec/globals/import *` "statements", but nothing requires the payload to be opaque. |
| B8 | lead-opaque-dead-branch.jsonl `bf08a0d5` | `if False: exec(input())` — opaque call in a provably dead branch still clears everything that follows. |
| B9 | lead-globals-read.jsonl `e720b788` | `names = globals()` — a *read* — is `opaque_statement` (globals is in OPAQUE_PY_DOTTED). The visible def's binding is destroyed by a statement that binds nothing. |
| B10 | lead-dead-branch-shadows-def.jsonl `0c3af163` | `def run` (live) then `if False: def run` (dead): the *dead* def poisons the *live* binding → lead while the live def runs. Same for `lead-dead-except-def.jsonl` `888ea263` (unreachable except-def) and `lead-while-false-def.jsonl` `ed8c05a9` (zero-iteration def). |
| B11 | lead-call-before-def.jsonl `e05dbc3b` | Call before its def → `lead` — **contract-sanctioned** (knowledge doc line 31), listed for completeness only. |
| B12 | lead-tuple-rebind-pure.jsonl `5ca94450` | `run, other = print, 42` then `run([...])` → `lead` on a call that is `print`. Tuple targets → unknown (correct conservatism), but the row still asserts an invisible *callable* — the callee is a builtin. Mark wrong even if a row is kept. |

## C. Bonus regression: pure builtins demoted to `lead` rows — the round-19 shape returns

`opaque_statement` poisons `PURE_ARG_CALLS` to `{"kind":"unknown"}` (lines 1746-1748);
`callable_info` then classifies the builtin `unresolved` instead of `pure`, and
`helper_argv_leads` fabricates a command finding for a call that is provably
`builtins.print`:

- lead-builtin-after-exec.jsonl `23a71882`: `exec('pass')` then `print(['pacman','-Q','hyprland'])` → `package_query pacman:-Q lead`.
- lead-builtin-after-globals-read.jsonl `a51a4dbd`: `snapshot = dict(globals())` then `print(['pacman','-Q','hyprland'])` → `package_query pacman:-Q lead`.
- lead-builtin-after-globals-print.jsonl `54621e59`: even `print(sorted(globals()))` — a read nested inside a print — poisons the *next* statement's `print`.

This is the same structural bug round 19's `frozenset` finding attacked: an ordinary
`print(argv_list)` is emitted as a command row (lead instead of observed — the bug
survived by changing costume). The contract's own no-row rule — "a builtin not rebound
in the text" — is violated; `globals()` read-only is not a rebinding, and even
`exec('pass')` provably binds nothing.

## D. Adjacent silent misses (no row at all — out of the asked axis, reported for completeness)

- obs-partial-helper-silent.jsonl `0bc400bb`: `functools.partial(run)(['pacman',…])` — runtime spawns (canary ✓); `assignment_binding` only wraps `kind:"spawn"` partials, helper-wrapped partials → unknown → call skipped, not even lead.
- miss-starred-helper-call.jsonl `c40f03ab`: `run(*['pacman','-Q','x'])` — literal starred argv, body executes (canary ✓); `bind_literal` returns `None` on any `Starred` arg (line 1677) → whole call skipped. Tension with the doc "starred and vararg forwarding are resolved only when the call states literal values" (knowledge doc:88-89).
- miss-inherited-method.jsonl `257655ff`: `B().run([...])` where `run` is defined on base `A` — executes (canary ✓); `class_method_info` scans only the class's own body (documented limit).
- miss-attribute-lead.jsonl `b7e26e1e`: `import helpers; helpers.run([...])` — external Attribute callee gets **no row**, while the identical bare-name shape `run([...])` gets `lead` (line 1876 `isinstance(node.func, ast.Name)`). Asymmetric lead policy.
- miss-asyncio-run.jsonl `70965538`: `asyncio.run(run([...]))` — executes (canary ✓); the inner call isn't directly awaited so it's skipped (documented: "direct `await`").
- miss-module-shadowed-by-def.jsonl `e8faac69`: `def subprocess(a)` after `import subprocess` → runtime `AttributeError`; silent, consistent.
- miss-getattr-call.jsonl `361128cb`: produced `lead` (globals() cleared the binding) — subsumed under B9.

## Impacted axes

Precision of the `evidence` field (the new criterion-30 machinery): `lead` over-marks
(B1-B10, B12 all visible-body calls), `observed` over-credits (A1-A3 wrong body; A4-A5
invisible binding; A6 unreachable). Recall: D items are silent misses, so `clean` bounds
shrink further than documented. Frozen/suite numbers are unaffected — verdicts still
exit 1 — so this attacks the *semantics* C1 advertises, not the 172/175 tally itself.
The suite's pinned cases (reset-lead, del-run, param-shadow, import-rebound) still mark
correctly; nothing here contradicts a pinned expectation.

## Smallest safe corrections

1. In `update_bindings`, descend into FunctionDef/ClassDef bodies for `Global`/`Nonlocal`
   statements only (mirroring `module_unsafe_names` line 1318-1320) and mark those names
   `unknown` — fixes A2, A3.
2. In `update_bindings` for FunctionDef, treat the name as `unknown` whenever
   `decorator_list` contains a callable that is not a proven passthrough (`functools.cache`,
   `lru_cache`, `wraps`-preserving forms) — or document decorators as blindly trusted.
   Fixes A1.
3. In `opaque_module_mutation`/`opaque_statement`, require a mutation-capable call:
   `exec`/`eval`/`__import__`/`compile` keep clearing; bare `globals`/`locals`/`vars` reads
   clear only under a subscript/attribute *assignment* target; literal `exec(<foldable
   str>)` can fold the payload's binding effect. Fixes B7, B9, C entirely.
4. In `visit()`, skip folding for `if`/`while`/`except` bodies only when the condition is
   not statically foldable (`if True:` → apply the def; `if False:` → don't poison).
   Fixes B4, B10, B8.
5. Fold `IfExp`, multi-target assignment, and `Starred` call args where every element is
   literal — fixes B2, B3, D-starred.
6. Extend `helper_argv_leads` to `ast.Attribute` callees whose head resolves to a
   `module` binding (`external` kind) — makes B/D's lead policy symmetric.
7. Decide and document whether `observed` means "reachable" or merely "textual" (A4-A6);
   if textual, the `sp`→`subprocess` alias needs documenting.

## Limits

- Fixtures are single-cell (except where the shape required otherwise); multi-cell
  variants of the same bugs exist trivially (state persists across cells, so every
  cross-statement shape also composes across cells).
- I did not re-run the 175-case suite or recall counters; those are sibling seats' lanes.
- [INFERENCE] A1-A3 assume the canonical judge agrees `observed` requires the *bound*
  body, not merely a same-named visible def; the knowledge doc's "binding in effect at
  the call wins" (line 30-31) supports it.
- A5/A6 are tradeoffs (kernel prelude imports subprocess; "issued ≠ executed"), flagged
  weak; A1-A4 and all of C are straight contract violations.
- No verdict harm: every mis-marked row still exits 1, so recall of *verdicts* is
  unharmed; only evidence-label fidelity and the no-row guarantee are.

## Installs

none — `python3 -I` on host (CPython 3.x, no installs), `/bin/touch` canaries only.
