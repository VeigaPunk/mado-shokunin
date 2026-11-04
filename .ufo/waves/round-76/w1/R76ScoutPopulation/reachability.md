# R76 C2 — runtime reachability of the twelve new cases, and D3/D4 false-positive risk

Seat: R76ScoutPopulation. Control set: `.ufo/waves/round-76/controls/c2-cases-r76.json`
(sha256 `df9e8984…`, 59 cases). Rule under audit: `quality/counters/c2-r76-shapes.py` at
`755b339f…`, functions `cancelling_functions`, `call_cancellations`, `keyed_names`,
`unguarded_rebindings`, `has_guard`.

## Method

1. Static read of every `src` in the twelve appended cases (names starting `callee-` or
   `dynamic-key-`).
2. Runtime observation: each `src` compiled and executed in an isolated namespace with a
   stubbed `subprocess` that records `(argv, env)`; `run("repo")` invoked once. Recorded
   output: `reachability-observed.json` (this directory). This tests **the delete's
   reachability**, not module importability (the fixtures are snippets: `subprocess` is not
   imported, which matches the carried round-75 convention; a `NameError` there would occur
   after the delete and cannot change the launch env).
3. Rule probes: the counter's own `classify()` run on eleven synthesised shapes that are *not*
   in the control set, to expose false-positive channels (`probe-d3-d4.txt`).

## Per-case result

| case | label (reader, guard) | runtime status | launches observed | guard key present at launch | label matches runtime |
|---|---|---|---|---|---|
| `callee-del-literal` | yes, no | ok | 1 | no | yes |
| `callee-del-store` | yes, no | ok | 1 | no | yes |
| `dynamic-key-del` | yes, no | ok | 1 | no | yes |
| `dynamic-key-module-const` | yes, no | ok | 1 | no | yes |
| `callee-del-param-rebound-live` | yes, yes | ok | 1 | yes | yes |
| `callee-del-other-key` | yes, yes | ok | 1 | yes | yes |
| `callee-del-dead-branch` | yes, yes | ok | 1 | yes | yes |
| `callee-never-called` | yes, yes | ok | 1 | yes | yes |
| `callee-called-after-launch` | yes, yes | ok | 1 | yes | yes |
| `dynamic-key-other` | yes, yes | ok | 1 | yes | yes |
| `dynamic-key-rebound` | yes, yes | ok | 1 | yes | yes |
| `callee-del-param-rebound` | yes, yes | **KeyError `'GIT_NO_REPLACE_OBJECTS'`** | **0** | n/a | **no** |

## Finding 1 (P2, same class as M75-3): `callee-del-param-rebound` cannot execute as written

```
def drop(m):
    m = {"PATH": "/usr/bin"}                 # fresh dict, no guard key
    del m["GIT_NO_REPLACE_OBJECTS"]          # KeyError here
def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    drop(env)                                # caller mapping untouched (correct)
    subprocess.run([...], env=env)           # never reached
```

The delete raises `KeyError` in the callee, so the launch is never reached and the file never
demonstrates a guarded launch. The label (`guarded`) is true only of the caller's mapping in a
counterfactual continuation. This is exactly the round-75 M75-3 defect ("a fixture whose
source cannot execute as written; the label pins the syntactic ordering rule, not a reachable
runtime state"), and the round-75 closure's stated repair ("the successor shape initialises
the key before the delete") was applied to the carried `del-before-store` family but not to
this newly appended callee case.

Scope of harm: the case is a negative for D3 (a delete on a mapping that is not the caller's
must not cancel). Both the successor and the held counter classify it `guarded`, so it is not
one of the four cases where the held rule fails (`base_controls=55/59` is produced by
`callee-del-literal`, `callee-del-store`, `dynamic-key-del`, `dynamic-key-module-const`), and
the 59/59 score is unaffected. Repair would initialise the key in the rebound dict
(`m = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}`) so the delete executes and the
caller's mapping still keeps its guard — but the file is frozen, so this is a recorded limit,
not an edit.

## Finding 2 (P3): two of the twelve pins are syntactic constant-folds or liveness facts, not reachability analysis

- `callee-del-dead-branch` — the only delete sits under `if False:`. The label is a correct
  *runtime* state (guarded), but the counter proves it by constant-folding a literal false test
  (`false_guarded_lines`), not by a reachability analysis. A callee whose delete is guarded by
  a non-literal condition (`if flag:`) is treated as cancelling; see probe T7/T20.
- `callee-never-called` / `callee-called-after-launch` — correct runtime labels, but they are
  liveness/ordering pins (no call; call after the first launch), and the rule answers them from
  line numbers. A second launch after the cancellation is not modelled: probe T21 (guarded first
  launch, unguarded second launch) is classified `guarded`, which is true of the first launch
  only. No frozen case has a second launch.
- `dynamic-key-rebound` — correct under both the frozen D4 wording ("bound exactly once") and
  under a runtime last-binding reading (`k = "PATH"` before the delete). It therefore does not
  discriminate between the two rationales; `dynamic-key-other` covers the value-mismatch half.

None of these is a reachable-state defect in the M75-3 sense (no crash, no unreachable launch).

## Finding 3 (P2, latent in the rule, no frozen case): D3 cancels the wrong mapping in three shapes

Probes run through the shipped `classify()` (`probe-d3-d4.txt`):

| probe | shape | runtime truth | rule verdict | assessment |
|---|---|---|---|---|
| T3 | `drop(env.copy())` | env guarded | guarded | ok — a copy at the call site is not credited |
| T10 | `drop(env)` before the store | env guarded | guarded | ok — dominance works in the forward direction |
| T19 | `if False: drop(env)` in the caller | env guarded | guarded | ok — dead call excluded |
| T4b | `def drop(m, extra): del extra[KEY]` called as `drop(env, other)` | `env` guarded, `other` cancelled | **unguarded** | **false positive** |
| T4c | same callee, `drop(env, env.copy())` | `env` guarded | **unguarded** | **false positive** |
| T5 | `alt = dict(env); drop(env); run(env=alt)` | `alt` still carries the key → guarded | **unguarded** | **false positive** (credits a delete on a mapping that is not the launched one) |
| T2 | nested `def b(): env = {...no key}; drop(env)` between `a()`'s guard and launch | `a`'s `env` guarded | **unguarded** | **false positive** (cancellations are collected whole-tree and merged by bare name into every scope) |
| T7 | `if cond: del env[k]` | guarded when `cond` false | unguarded | declared approximation (line order ≠ execution order) |
| T20 | `if cond: pass else: del env[k]` | guarded when `cond` true | unguarded | same over-approximation |
| T22 | callee deletes from a module-level dict that is then launched | unguarded | unguarded | ok |
| T11 | `del env[K]` with module constant `K` in a function | unguarded | unguarded | ok |

Root causes, from the implementation:

- `cancelling_functions` marks a function cancelling when **any** parameter is deleted from,
  but `call_cancellations` credits the **first** positional argument's name. When the deleted
  parameter is not the first positional parameter, the caller's first argument is cancelled
  although the callee deleted a different mapping (T4b/T4c). The frozen declared limit says the
  callee is "matched by simple call shape (a positional first argument)"; the implementation
  does not require the deleted parameter to *be* that first argument.
- `call_cancellations(tree, ...)` walks the whole tree and the result is merged into every
  scope's `rebinds` by name, so a call in one function can cancel a same-named guard in another
  scope when line numbers straddle (T2).
- Neither D3 nor D4 checks that the cancelled mapping is the one handed to the launch; a
  pre-taken copy (`alt = dict(env)`) launched after the delete is not seen as guarded (T5),
  because `mapping_has_key` does not treat `dict(env)` as carrying the key.

## Direct answer to the seat question (item 3)

- **A copy at the call site** (`drop(env.copy())`): not credited — correct (T3).
- **A rebinding after the call**: the callee-side rebind check only looks before the delete, and
  caller-side rebindings are ordered by the dominance test; no false credit found (T10, and a
  caller rebinding to a fresh guarded literal re-establishes the guard).
- **A callee that receives a different argument**: **yes, credited wrongly** (T4b/T4c). This is
  a real false-positive channel of the frozen D3 rule.
- **A mapping that is not the one launched**: **yes** when the launched mapping is a copy taken
  before the cancel (T5), and when a same-named call in a sibling scope lands between guard and
  launch (T2).

The four frozen positives are **not** false positives as written: each reaches exactly one
launch, that launch's mapping is the same name the callee/dynamic delete targets, no copy or
rebind intervenes, and the runtime observation shows the key absent (`callee-del-literal`,
`callee-del-store`, `dynamic-key-del`) or present-by-constant (`dynamic-key-module-const` is a
true positive too — the module constant resolves to the guard key and the delete is live).
The risk is latent in untested shapes, not realised in the scored set.

## Coverage gaps the twelve cases leave open

1. Caller passes a copy to the cancelling callee and launches the original (T3 covers only the
   copy-as-argument half; the launched-original half of T5 is uncovered).
2. Callee with more than one parameter where the deleted one is not the first positional (T4b/T4c).
3. Same-named mapping in two scopes with a cancelling call in the sibling (T2).
4. Non-literal conditional delete (`if cond:`) for D3 and D4 (T7/T20).
5. A second launch after the cancellation (T21) — "guarded" is per-file, not per-launch.
6. Caller-side rebinding of the mapping *after* the call but *before* the launch to another
   guarded literal (sound in the rule; untested in the frozen set).
