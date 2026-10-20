# AdvRecallShapes — falsified: 51 real-execution spawn shapes found by 1f7f995/9c54c56 are silently missed by 28c6837

## What was attacked

C1's recall half: that the 28c6837 repair (`eager_calls` + binding-resolved descent)
keeps detecting shapes the harmed (1f7f995) and pre-harm (9c54c56) tools detected.
The claimed recall guard (`tw-recall.py` 6/6 = 5 observed + 1 lead) covers only six
shapes; it never exercises implicit-dispatch execution.

## Method

- Wrote 70 NEW `.jsonl` transcript fixtures (one `eval` toolCall each; cf06 has two)
  under `.ufo/waves/round-20/w2/AdvRecallShapes/fixtures/` — payloads are
  `pacman -Q w2shape` (package_query; flaggable at all three revisions) and
  `git commit -m w2shape` (vcs_write; flaggable only where the class exists).
  Fixtures are data; never executed.
- Extracted tool bytes only via `git show` in a /tmp clone:
  `/tmp/tw-1f7f995.py` (sha 367be947…), `/tmp/tw-9c54c56.py` (sha c1ae45a7…),
  `/tmp/tw-28c6837.py` (sha 9613f510…, matches the assignment's pin).
- Command per revision: `python3 -I /tmp/tw-<REV>.py --scan <fixtures-dir>`;
  JSON verdicts preserved at `w2/AdvRecallShapes/scan-<REV>.json`;
  per-file result table in `w2/AdvRecallShapes/manifest.json`.

## Counterexamples (the falsification)

**51 of 70 fixtures produce a finding at 1f7f995 and/or 9c54c56 and ZERO rows —
not even `lead`, not even `unparsed_spawns` — at 28c6837.** Totals:

| revision | findings over the 70 files | evidence field |
|---|---|---|
| 1f7f995 | 60 (58 package_query + 2 vcs_write) | n/a (field does not exist) |
| 9c54c56 | 56 (package_query only; rev has no vcs class) | n/a |
| 28c6837 | 13 (all observed, 0 lead) | observed only |

Every regression shape is REAL execution: the spawn statement provably runs when
the cell runs (callbacks registered then started/run, dunder methods triggered by
the same statement, decorator bodies at def time, closures invoked, coroutines
driven by `asyncio.run`). Representative minimal cases:

1. `asyncio.run(m())` where `m` awaits `create_subprocess_exec('pacman','-Q','w2shape')`
   — fixture `ar01-asyncio-run-cse.jsonl`. 1f7f995 + 9c54c56 → package_query;
   28c6837 → nothing. Root cause: `async def` helpers are only descended when the
   Call node is the direct value of an `Await` (`spawn_scan` line ~1844:
   `isinstance(helper, ast.AsyncFunctionDef) and id(node) not in awaited_calls`),
   so *scheduled* coroutines are silently skipped.
2. `threading.Thread(target=w).start()` where `w` runs `subprocess.run(['pacman','-Q','w2shape'])`
   — fixture `ar11-thread-target-def.jsonl`. The `w` in `target=` is an argument
   Name, not a call; no machinery inspects registered callables.
3. `(lambda: subprocess.run(['pacman','-Q','w2shape']))()` — fixture
   `ar20-iife-lambda.jsonl`. `eager_calls.visit_Lambda` visits only default args,
   so an immediately-invoked lambda body is invisible.
4. `with C(): pass` where `__exit__` spawns — `ar37-with-exit-spawn.jsonl`;
   `__del__` on `C()` — `ar38-del-finalizer.jsonl`; `__getattr__`, `__repr__`,
   `__iter__`, `__eq__`, `__getitem__`, `__post_init__`, `__init_subclass__`
   — `ar39`–`ar45`. Only `__init__` and `__call__` get dispatch handling;
   every other implicit dunder entry is dropped.
5. `outer()()` returned-closure invocation — `ar24`; `f = outer(); f()` —
   `ar25`; decorator-returned wrapper (`@wrap def f` then `f()`) — `ar33`;
   bare `@deco`/`@deco class` whose decorator body spawns at def time — `ar34`, `ar35`.
6. `sp = importlib.import_module('subprocess'); sp.run(['pacman','-Q','w2shape'])`
   — `ar46`. Both olds hardcode the `sp`→subprocess alias; the new assignment
   resolver binds `sp` to "unknown", losing the OLD recall (ironic: the new tool
   gains other alias forms — see confirmations — but regresses this one).
7. vcs_write variants: `threading.Thread(target=w)` + `asyncio.run(m())` spawning
   `git commit` — `ar50`, `ar51` (found by 1f7f995 only, since 9c54c56 lacks the
   vcs class; still missed by 28c6837).

Full regression list: ar01–ar18, ar20–ar51 (49 files) + gap04 = 51 raw misses.
Of these, `gap04` is an intentional old-FP fix and `ar49` is signal-contingent,
leaving **49 certain recall regressions** (47 package_query + 2 vcs_write)
plus 1 contingent.

## Impact

Any seat that hides a spawn behind a thread target, an executor/scheduler
callback, `atexit`/`ExitStack`/`weakref.finalize`, `functools.partial` of a local
helper, `map`/`sorted`/`reduce` lambdas, a returned closure, an unawaited coroutine
handed to `asyncio.run`/`create_task`/`ensure_future`/`gather`/`wait_for`/`to_thread`,
a `call_soon` loop callback, a decorator body, or any dunder other than
`__init__`/`__call__` produces ZERO findings at the repaired revision where both
predecessors emitted one. These are not "dead code" cases (the precision target):
each spawn executes when the cell executes. The R20 repair traded flat-walk
recall for eager-path precision and the recall guard suite (6 cases) is too thin
to see it. Axis impacted: tripwire recall / C1's "no recall loss" implication;
the whole-corpus no-harm diff (deferred to wave 2) would surface the same.

## Smallest safe correction

Do not re-walk all bodies (that re-imports the dead-code findings the repair
removed). Instead, when `spawn_scan`/`eager_calls` *drops* a reference to a
same-text callable or non-eager call site that the scanner can see — i.e.
(a) `AsyncFunctionDef` helper calls not under `Await`,
(b) Name/Attribute/Call args of known callable bindings inside external call
    argument lists (`Thread(target=…)`, `register(…)`, `map(…)`, `partial(…)`),
(c) lambda bodies appearing in call argument/dispatch positions,
(d) `with` targets whose class defines `__enter__`/`__exit__`, and `ClassDef`s
    defining `__init_subclass__`/`__post_init__`/`__del__` —
classify the visible literal argv inside those bodies the same way
`helper_argv_leads` does and emit rows with `evidence: "lead"` instead of nothing.
That restores old-revision recall on real-execution indirections while preserving
the observed/lead precision split (and keeping never-called-def bodies silent,
which is the actual precision win).

## Confirmations (new revision wins; kept for balance)

15 cf-shapes: all three find cf01/cf08/cf10–cf15; only 28c6837 finds
cf02 (param argv through body), cf05 (`__call__` arg), cf06 (cross-cell alias),
cf07 (`s = subprocess` assignment alias), cf09 (`functools.partial(subprocess.run)`).
1f7f995 uniquely over-reported gap04 (`helper_argv_leads` fired on a literal argv
handed to a lambda that only prints — the R19-V2 fix working as intended; it is
excluded from the regression count).

## Shared gaps (all three miss — information, not regressions)

`getattr(subprocess,'run')(argv)` (gap01), `importlib.import_module('subprocess').run`
(gap02), `os.execvp('pacman',[...])` (gap03; 28c6837 counts it as
`unparsed_spawns=1`), `loop.run_in_executor(None, os.system, …)` (ar19), and
vararg/kwarg argv folded through `list(a)` / `k['c']` (cf03/cf04 — the claim's
"vararg/keyword argv resolve" covers only *direct* `subprocess.run(a)` / splat
forms; verified: `vararg-direct`, `kwarg-dict-splat`, `starred-*` probes DO find
at 28c6837 only).

## Boundary / exclusions

- `ar49-signal-handler-lambda` counts as a regression under the assignment rule
  (old found, new missed) but the spawn is signal-contingent rather than
  guaranteed-by-running-the-cell; flagged separately so the judge can discount it.
- `gap04` (old false-positive now fixed) and `ar19`/`gap03` (all-miss) are not
  recall regressions.

## Limits

- Recall judged by fixture text + scan output only; "real execution" asserts the
  spawn statement is reached when the code runs — verified by reading semantics,
  not by executing fixture code (contract: never executed). [INFERENCE] on
  runtime reachability, all shapes are textbook-reachable.
- `9c54c56` has no `vcs_write` class, so ar50/ar51 are 1f7f995-vs-28c6837
  regressions only.
- Old revisions carry no `evidence` field; comparison is presence-of-row.
- Fixture dir scanned standalone per revision; outputs in `scan-*.json` are the
  raw tool verdicts.

## Installs

none — system python3 only; no package transactions (host pause honored).
