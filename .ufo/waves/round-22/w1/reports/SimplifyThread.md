# SimplifyThread — one `scheduled_invoke` path for `.start()` / `.run()` without binding-map sentinels

Target: `tools/mado-tripwire.py` at `46c82902896da0ec0ebd54254b1891667fa5da48f8cb297ee08bfb337e34c8c1`. Round-22 wave 1: source-only proposal; no production edits, no measurements. Ground truth: `.ufo/waves/round-21/residual/FinalBindingReview.md` (F4, F5).

## Axes

| Axis | Today | Design direction |
|---|---|---|
| Correctness | `.start` followed via `thread_start`; `.run` unresolved (F4); sentinel name shadows source globals (F5) | Single resolver for `start`/`run`; `follow_helper` with node-carried target |
| Authority count | Three entry points (`callable_info` 1666–1667, `spawn_scan` 2294–2297, 2298–2311) | One `resolve_scheduled_invoke` + one `emit_scheduled_invoke` |
| Size | Copy bindings + inject key + nested `spawn_scan` on synthetic `Name` | ~14 lines removed; ~20 lines in one helper (net small) |
| Contract | Construction-time `args`/`kwargs` on `scheduled` binding (1719–1730) | Unchanged timing; both invoke flavors consume the same stored literals |

## 1. What production code does today

**Scheduled record** (`assignment_binding` 1719–1730): `threading.Thread` / `threading.Timer` assignments produce `kind: scheduled` with `target`, literal-folded `args`/`kwargs` at the **constructor** statement.

**Start only in `callable_info`** (1666–1667): `Attribute` on a `scheduled` binding maps `.start` → `kind: thread_start`. `.run` is not mapped, so `t.run()` after `t = Thread(...)` falls through to unresolved and emits nothing (F4).

**Chained start** (`spawn_scan` 2294–2297): `Thread(...).start()` re-derives `scheduled` via `assignment_binding` when `callable_info` did not tag the call—duplicate authority.

**Thread start body** (2298–2311): Copies `cbindings`, injects `__mado_thread_target__`, builds `Call(Name(__mado_thread_target__), literal args...)`, nested `spawn_scan`. The injected name participates in `follow_helper` body binding maps (2241), so a legitimate module global with the same spelling wins in the worker and changes evidence (F5 probe: observed → lead).

**Refs exemption** (2551–2553): Targets passed into `Thread(...)` are not swept because explicit/aliased start is supposed to own follow—`.run` was never added to that owner set.

## 2. Unified design (collision-free, no source-name sentinel)

**Name:** `scheduled_invoke_unified`

**Resolver** (single site at top of each `spawn_scan` call iteration):

- Match `Call` whose `func` is `Attribute` with `attr in ("start", "run")`.
- Resolve receiver: `Name` → `cbindings[id]` must be `scheduled`; inline `Call` → `assignment_binding(receiver, cbindings, cenv)`.
- Package `{**scheduled, "sync": attr == "run"}` (sync flag reserved; see §4).

**Emitter** (`emit_scheduled_invoke`, colocated with `follow_helper`):

1. **`callable_info` guard** (new first lines ~1603): if `getattr(node, "mado_resolved", None)` is set, return it—never consult `bindings` for the stub.
2. Read `helper = scheduled["target"]["node"]` when target kind is `helper`.
3. Same literal guard as today (2303–2310): construction `args`/`kwargs` must be literal-ready or `unparsed += 1`.
4. Build `bound_node = ast.Call(func=stub, args=[literal_node(...)], keywords=...)`, set `stub.mado_resolved = scheduled["target"]`.
5. **`follow_helper(helper, bound_node, cenv, cbindings, ...)`** directly—no `local_bindings`, no `__mado_thread_target__`, no nested `spawn_scan` solely for name resolution.
6. On `None`, **`sweep_body`** like the ordinary helper branch (2396–2398).

**Collision freedom:** The target callable never enters a binding map. Worker names (including a user-defined `__mado_thread_target__` function) resolve only through normal lexical/module rules—matching F5 control behavior.

**Direct-run / start unification:** `.run()` and `.start()` share the emitter; the only difference is how the resolver sets `sync`. Both use construction-time literals and the same follow/sweep pipeline—fixing F4 without a second code path.

## 3. Deletions

| Item | Lines (approx.) | Verdict |
|---|---|---|
| `local_bindings["__mado_thread_target__"]` | 2299–2300 | **delete** |
| Synthetic `Name(__mado_thread_target__)` + nested `spawn_scan` | 2304–2308 | **delete** → `follow_helper` |
| `thread_start` in `callable_info` | 1666–1667 | **delete** |
| Chained `.start` reassignment | 2294–2297 | **delete** (fold into resolver) |
| `if kind == thread_start` block | 2298–2311 | **replace** with resolver + emitter |

**Caller evidence:** `thread_start` / `__mado_thread_target__` appear only at the sites above in `tools/mado-tripwire.py` (text grep). LSP unavailable (`xd://lsp` missing); not recorded as semantic proof.

## 4. Preserved contract

- Literal `args`/`kwargs` frozen at `Thread`/`Timer` construction (1719–1730)—not at `.start()`/`.run()` statement.
- Refs skip for constructor `target=` (2551–2553); comment should mention `.run` as well as `.start`.
- **Evidence tier:** Do **not** downgrade `.start()` results to `lead` solely because `sync=False`; current `.start()` follow produces `observed` rows and frozen/W2 expectations depend on that. Async worker defs still use coroutine lead downgrade only on the existing helper branch (2392–2395).
- Independent from **SimplifyCapture** `ClosureFrame` (factory closures); no change to `capture_owner` (2333–2344).

## 5. Mapping to r21 F4–F5

| Finding | Unified rule |
|---|---|
| F4 `t.run()` silent miss | Resolver treats `run` like `start`; `emit_scheduled_invoke` → `follow_helper` on worker |
| F5 sentinel collision | No map injection; `mado_resolved` stub; global name in worker is real binding |

**Expected static outcomes (not measured this wave):**

- `thread-run-direct.jsonl`: observed `pacman -S r21-thread-run`
- `thread-key-hygiene.jsonl`: observed `pacman -Q r21-hyg` (same as control)
- `thread-key-control.jsonl`: unchanged

## 6. Tradeoffs and unknowns

- **Invalid stub `Name.id`:** Internal-only node; must never reach `bindings.get`. Guard at top of `callable_info` is mandatory.
- **Non-helper targets** (e.g. `Thread(target=subprocess.run, ...)`) already handled elsewhere; scheduled invoke path should require `target.kind == helper` or fall through to unparsed/sweep—same class as today when target is unknown.
- **Inherited `Thread.run`:** Still out of scope per module docstring (73–74).

## 7. Tools

None installed or updated.

Report: `.ufo/waves/round-22/w1/reports/SimplifyThread.md`  
Notes: `.ufo/waves/round-22/w1/notes/SimplifyThread.json`
