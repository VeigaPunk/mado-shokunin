# ExecSweepEscape — design note: escape-gated callback sweep

Seat `MadoR23.ExecSweepEscape`, round 23, lane `mado-shokunin`, base
`a28e4815aabfa85f55274884000fb2608355f8cf` (classifier sha256
`cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`).

Candidate: `tools/mado-tripwire.py`, sha256
`3daf01e34467942f71ff8c5fb9547e0fa797c5a6a7cedf2a7a5501b965ecae8d`,
clone branch `round-23/exec-sweep-escape`, commit
`f860c1e8834397bcf42309c121d7630ef32cb7dc`.

## 1. The defect this item owns

`sweep_body` gives a `lead` row for every spawn in a visible body the scan
does not follow. A callable handed to a consumer as an argument is such a
body: the consumer call is *followed*, so the consumer's own use of the
callback is already accounted for, but the callback body is *also* swept.

That double count is not harmless. Three shapes appear in the frozen
round-23 repair set:

| case | redundant sweep | effect at base |
|---|---|---|
| `ForwarderPassesCallerArgument` | sweep of `run` (the argument of `forward`) | false `unparsed_spawns: 1` — the sweep cannot bind `actual`, the follow can |
| `ForwarderInvokesFactoryClosure` | sweep of the nested `run` reached through the factory call | same false unparsed |
| `ReturnedGlobalCallableShadow` | sweep of `other_launch` (the argument of `make`) | a **false foreign lead** `pacman -S r22-foreign-callable`: `make` never uses the value it is handed, so that body never runs |
| `ForwardExistingClosureWithoutFrameContamination` | sweep of `run` (reached through `saved = original()`) | same false unparsed |

Round 22's v3 suppression (`4d308e5`, withdrawn in `579109a`) removed the
sweep whenever the consumer was followed. That is too coarse: it also removed
the sweep for a callback that *escapes* the consumer, and so lost recall for
`hooks["k"] = cb` / `obj.cb = cb` (round-22 `residual/ResidualForward.md`,
gap 2). The rule below keeps every escape and removes only the redundant
sweep.

## 2. The rule

For a consumer call `C` of a visible helper `H` that the scan **followed**:

* the follow must have produced **no unparsed row** (`result[1] == 0`), and
  `H`'s body must contain no `opaque_statement` (an `exec`/`import *`/
  namespace-mutating statement can rebind names behind the scan's back);
* then, for each argument of `C` that binds to a parameter `P` of `H`, the
  scan classifies how `H`'s body uses `P`:

| class | condition | sweep |
|---|---|---|
| `unused` | the name `P` never appears in `H`'s body (nested defs and lambdas included) | **skipped** |
| `call` | `P` appears only as the direct call target `P(...)` of calls the scan followed with no unparsed row | **skipped** |
| `returned` | `P` appears only as the value of a `return` | skipped **only if** the body it was bound to was itself followed with no unparsed row |
| `escape` | anything else | **kept** |

`escape` covers every form the assignment lists: a store into a subscript or
an attribute, a `global`/`nonlocal` declaration, a container literal, a
`return`, a `yield`, an alias assignment, a pass-on as an argument, a
`*args`/`**kwargs` capture, and a `locals()`/`vars()`/`globals()` read. A
nested scope that binds the name itself (its own parameter, an assignment, a
`global`/`nonlocal` statement) shadows it and is not counted as a use of the
consumer's parameter; a nested scope that does not bind it reads the
consumer's parameter and is analysed.

The `returned` class is the returned-callback case. It is handled only when
the hand-back is *shown* to be followed: the value the consumer returns is
resolved through the same bindings the follow used, and the body it names must
be one the scan followed with no unparsed row (`ctx["clean_bodies"]`). In
`ForwardExistingClosureWithoutFrameContamination` that proof holds —
`job = forward(...)` binds the returned `callback`, `job()` follows `run`, and
`run`'s body is followed with zero unparsed — so the sweep is skipped and the
case passes. When the returned body is never followed, the sweep is kept: a
consumer that only hands the value back may still be the only path that
reaches it.

The rule never fires for an argument the scan could not bind (a starred
argument, an unknown `**kwargs`), for a consumer that was not followed, for a
consumer whose follow produced an unparsed row, or for a body with an opaque
statement.

## 3. How it is implemented

Four helpers, all in `tools/mado-tripwire.py`:

* `consumer_body(fn)` — the statements of a body, or a lambda's expression.
* `bound_param_names(fn, call, skip_first)` — the parameter each argument
  binds to, using the same positional/keyword/`*args`/`**kwargs` mapping as
  `bind_literal`. A starred argument aborts the mapping (it expands to an
  unknown number of values), so the rule does not fire for that call.
* `scope_binds_name(scope, name)` — whether a nested scope binds the name
  itself (parameter, assignment, `global`/`nonlocal`).
* `parameter_escape(fn, name, ctx)` — the classification above; it walks the
  body with a parent map and a shadow flag, and consults `ctx["clean_calls"]`
  for the "followed with no unparsed" test of each `P(...)` call.
* `note_consumer_args(...)` — called from `spawn_scan` right after a consumer
  is followed; it records the argument nodes whose later sweep is redundant
  (`ctx["safe_args"]`) and the ones a consumer only hands back
  (`ctx["returned_args"]`, mapped to the body the hand-back must reach).

The sweep itself changes in one place: the reference loop in `spawn_scan` now
skips `sweep_body` for a helper reference whose argument node is in
`ctx["safe_args"]`, or whose returned body is in `ctx["clean_bodies"]`.

`new_scan_context()` gained `clean_calls`, `clean_bodies`, `safe_args` and
`returned_args`. All four are per-cell state, like the existing `swept`,
`stack` and `descents`.

## 4. Discrimination, measured

Thirteen probe fixtures (scratch, not committed; source in the seat report)
run through the candidate with `follow_helper`/`sweep_body` traced:

| probe | consumer body | sweep | rows |
|---|---|---|---|
| A subscript store | `hooks["k"] = cb` | kept | `pacman -S pA` lead |
| B pass-on | `sink(cb)` | kept | `pacman -S pB` lead |
| C unbindable call arg | `cb(makeup())` | kept | none, `unparsed 2` |
| D never read | `return 1` | skipped | none |
| E clean direct call | `cb(["pacman","-Q","pE"])` | skipped | `pacman -Q pE` observed |
| F yield | `yield cb` | kept | `pacman -S pF` lead |
| G alias | `alias = cb` | kept | `pacman -S pG` observed (lead deduped) |
| H `locals()` | `print(locals())` | kept | `pacman -S pH` lead |
| I container literal | `box = [cb]` | kept | `pacman -S pI` lead |
| J attribute store | `box.cb = cb` | kept | `pacman -S pJ` lead |
| K nested def calls it | `def inner(): cb()` | skipped | `pacman -S pK` observed |
| L returned then called | `return cb` + `job()` | skipped | `pacman -S pL` observed |
| M returned, never called | `return cb`, no call | kept | `pacman -S pM` lead |

## 5. What this item does **not** fix

* **The caller-frame leak.** `follow_helper` starts the callee body from the
  caller's environment snapshot instead of the callee's defining frame. That
  produces the false `observed` rows in `ForwarderInvokesCallback`
  (`pacman -S r23-forward-foreign`) and `CallerLocalShadowsHelperGlobal`
  (`pacman -S r23-local-foreign`), and it is what the round-23 repair set
  still fails on after this change. It is the frame-environment item, not
  this one.
* **`EscapeSecondForwarder`** (critic neighbour) stays red for the same
  reason plus one: `outer` passes the callback on as an argument
  (`inner([...], callback)`), which the assigned rule classifies as an
  escape, so the redundant sweep of `run` survives and still reports one
  unparsed spawn. The false `observed` row there is the frame leak. With a
  defining-frame fix that also gives the *sweep* its own defining frame, the
  surviving sweep would resolve `argv` to the module global, produce a
  duplicate `pacman -Q r23x-chain-global` lead and be dropped against the
  observed row (same-command lead dedup, `mado-tripwire.py:2883`), leaving
  the case exact-rule clean.
* **`EscapeListAppendThenCalled`** and **`EscapeTupleNestedClosureLater`**
  are unchanged from base. The first stores the callback with
  `hooks.append(cb)` — a container store, an escape, so the sweep is kept,
  and the sweep still cannot resolve the module-global `argv` (one unparsed
  spawn, no row). The second needs a tuple-returning factory to be resolved
  and unpacked (`callback, _ = pair`), which no part of this rule touches.
* **`*args`/`**kwargs` capture** is treated as an escape in the sense that
  the parameter a `*args`/`**kwargs` consumer receives is analysed like any
  other parameter: a read of it that is not a clean direct call target keeps
  the sweep.
