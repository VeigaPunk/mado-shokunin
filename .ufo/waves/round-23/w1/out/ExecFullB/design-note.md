# ExecFullB — design note: defining-scope provenance for the tripwire classifier

Item: round-23 **C1 operability** — take the frozen 12-case repair set from
6/12 to 12/12 at `tools/mado-tripwire.py` with every no-harm guard holding.
Mechanism required by the L1: *not* "replace cenv with module env"; instead
**tag each helper binding with the identity of its defining scope (module, or
the function frame object that executed the def) and resolve a followed body's
free names through that scope chain**, and **gate the callback sweep on the
same provenance**.

Candidate: `tools/mado-tripwire.py`, sha256
`41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009`
(base `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`).
Diff: 257 insertions, 21 deletions, one file, all in `tools/mado-tripwire.py`.

---

## 1. The defect

`follow_helper` built the callee's body environment from the **caller's**
environment (`body_env = dict(cenv)`, `body_bindings = dict(cbindings)`). Any
free name of the callee — a module global, or a name closed over from an
enclosing function — was therefore read in the *caller's* frame. A caller
local that happened to share the name shadowed the callee's global, and the
scanner reported a command that never runs (H4, "caller-frame leak"), or
missed the command that does.

The same leak reached the callback sweep: every callable handed to a call was
swept as a `lead` even when the receiving call only *calls* it, and the swept
body was read with no scope at all (`prepare_eval_calls(body, {}, ...)`), so
its free global was unresolved and counted as `unparsed_spawns`.

## 2. Scope identity

Every helper binding now records the scope whose frame executed its `def`:

* `MODULE_SCOPE` — the module namespace (`classify_eval` sets it on the cell's
  bindings).
* `("frame", id(fn))` — the frame of the enclosing function (`frame_scope`).
* `("sweep", id(fn))` — the frame a swept body is read in (`sweep_scope`);
  kept apart from the real frame so a sweep never overwrites a followed
  frame's view.

The tag travels on the AST node (`node.mado_scope`) and in the binding dict
(`"scope"`), so it is available wherever the helper is later resolved —
`update_bindings` (function and class bodies), `assignment_binding` (lambdas),
`class_method_info` (methods close over the class's enclosing scope).

A frame's identity is the function object that owns it, which is the
"function frame object that executed the def" the L1 asked for: a `def`
nested in `F` is tagged with `F`'s frame; a `def` at module level is tagged
with the module scope.

## 3. The scope chain

`ctx["scopes"]` maps a scope id to its **own view** — the names that scope
binds — plus a `parent` link to the scope it closes over:

```
module scope  ──▶  frame(F)  ──▶  frame(G) ...
```

`scope_view(ctx, scope, …)` walks that chain and merges the views, innermost
first. The **calling frame is not in the chain**: it is neither the callee's
defining scope nor one of its ancestors, so a caller's local can no longer
shadow a callee's global.

`follow_helper` and `sweep_body` both read a body through that view, so a
followed body and a swept body agree on what a free name means.

### Own names vs inherited names (S121)

A scope's own view holds only the names *that scope binds*
(`own_names(fn)`: parameters, assignments, nested defs/classes, imports,
comprehension and loop targets). A name the scope does not bind is inherited
and is read in the scope it closes over — **late**, at the call.

That distinction is what keeps late global rebinding correct. `CaptureGlobalLate`
(round-22 oracle case) rebinds a module global *after* a nested closure is
built; the closure must see the new value. With a flattened frame view the
frame would have frozen the old value; with own names the frame does not own
the global at all, so the module scope answers, at the statement that calls
it.

`scope_entry` records a scope's own view per statement (the existing
per-statement snapshot), so the value read is the value at the call, not at
the definition.

## 4. Gating the callback sweep on the same provenance

A callable handed to a call is swept only when its reference **escapes** that
call:

* stored into a container or an attribute (`hooks["k"] = cb`, `box.cb = cb`,
  `hooks.append(cb)`),
* returned (`return cb`),
* handed to another call.

A callable the receiving call only **calls** (`cb(value)`, `cb()`) does not
escape it: that call is followed, so the callback's body is already read, in
its own defining scope, and no separate lead is owed. `reference_escapes`
answers this from the receiving callee's body
(`parameter_escapes`, a small fixpoint over aliasing), and conservatively
answers "escapes" whenever the receiving body is not visible, the argument is
nested in a composite value, or the receiving call cannot be bound.

This removes the false lead of `ReturnedGlobalCallableShadow` (`make(launch)`
never uses its parameter) and the spurious `unparsed_spawns` of
`ForwarderPassesCallerArgument` (the callback is called, not stored), while
keeping the recall the repair set demands of `CallbackStoredInDict` and
`CallbackStoredOnAttribute` (stored → swept → `lead`).

## 5. Why the sweep still resolves globals

A sweep that escapes is still read in the defining scope, so
`ForwardExistingClosureWithoutFrameContamination` no longer reports an
unresolved spawn: the closure's free global is read in the module scope, the
resulting `lead` duplicates the `observed` row of the same command and is
dropped by the existing per-call de-duplication (`scan_file`: a `lead` equal
to an `observed` finding is not emitted).

## 6. Coverage

Round-23 repair set (frozen, byte-exact): **12/12**, `unparsed_spawns` 0 on
every case.

Routes the L1 relayed from the neighbours, all now correct on the same
mechanism (no special-casing):

| Route | Result |
|---|---|
| `CritFrameNeighbour` — helper called from a method, from a lambda, through a decorator wrapper | 3/3 `base-correct` |
| `CritScheduledNeighbour` — Thread target / Timer function started from a shadowing frame, `Thread.run` from a forwarder | 3/3 pass |
| `CritEscapeNeighbour` — `EscapeSecondForwarder` (one hop deeper) | pass (`observed`, no foreign row) |
| `CritEscapeNeighbour` — `EscapeListAppendThenCalled` | pass on the `present` rule (`lead`, no foreign row) |
| `CritEscapeNeighbour` — `EscapeTupleNestedClosureLater` | **still a pre-existing recall gap** (tuple value + unpacking + closure capture); unchanged from the base |

## 7. No-harm guards (all measured on the candidate)

| Guard | Result |
|---|---|
| round-23 repair set | 12/12 |
| round-22 residual truth | 4/4 |
| round-22 oracle | 57/57 |
| round-22 replay `--mode oracle` | 35/35 + 17/17 |
| eleven legacy selftest suites | 247/247 |
| 1356-file corpus comparator vs the base classifier | 1217 retained, **0 removed, 0 added**, 107 errors — every error string identical before and after, so **0 new error flips** |
| round-22 closure resource (`module-main`, `cli`) | 3/3 fixtures each: exit 0, clean, 0 unparsed, ≤0.29 s, ≤24 MiB RSS |
| round-21 resource (`module-main`, `cli`) | 3/3 fixtures each: exit 0, ≤0.11 s, ≤39 MiB RSS (base: same, ±0.5 MiB) |
| round-20 precision | 166/175 (P66/66 S17/17 W21/22 H47/52 L15/18) — **the identical passing-name set as the base** |

## 8. Known limits (stated, not hidden)

* A scope whose chain entry is missing (a factory result that is never
  followed, a decorator-built wrapper) falls back to the call-site view, i.e.
  the pre-change behaviour. The closure overlay still supplies the captured
  values in those cases.
* `EscapeTupleNestedClosureLater` needs tuple values, tuple unpacking and a
  closure captured through unpacking — a separate feature, out of this item's
  scope, and left untouched rather than half-built.
* The escape analysis is name-based: it does not follow a value through a
  subscript store (`d["k"] = cb` keeps `cb` in `d`), so a callback stored
  that way is not swept. It errs toward sweeping (no lost findings), which is
  the safe direction for a lead.
