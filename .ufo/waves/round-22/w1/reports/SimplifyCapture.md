# SimplifyCapture — one immutable `ClosureFrame` at factory time replaces the invoke-time capture overlay

Target: `tools/mado-tripwire.py` at `46c82902896da0ec0ebd54254b1891667fa5da48f8cb297ee08bfb337e34c8c1` (3282 lines). Round-22 wave 1: source-only design; no production edits, no measurements, no fixture execution. Ground truth for defects: `.ufo/waves/round-21/residual/FinalBindingReview.md` (F1–F3).

## Axes

| Axis | Today | Design direction |
|---|---|---|
| Correctness | Invoke-time `cenv` re-binds factory parameters (F1); failed bind leaves invocation env so module globals become “observed” (F2); returned nested `def` chosen before factory-body rebind (F3) | Single creation-time frame; miss → sweep, never global borrow |
| Authority count | Six overlapping env/binding stores (see §2) | One frame per closure/partial at bind time; statement snapshots unchanged for ordinary calls |
| Size | `spawn_scan` capture block + prefix `prepare_eval_calls` duplicate factory replay | Delete ~12–18 lines from `spawn_scan`; optional later merge of env quadruple |
| Contract | Docstring promises values bound at follow time (38–41) | Frames make “follow time” unambiguous: creation statement for captures, invoke statement for ordinary helpers |

## 1. What production code does today

**File-level persistence** (`scan_file` 2643–2686): `envs["py"]` (literal recipes) and `binding_envs["py"]` (callable map) survive across eval cells until `reset`.

**Statement snapshots** (`prepare_eval_calls` 2038–2075): Before each statement mutates outer `env`/`bindings`, every eager call/ref in that statement receives a shared shallow copy (`call_env[id(node)]`, `binding_env[id(node)]`). This is the correct clock for “what names meant when this line ran.”

**Ordinary follow** (`follow_helper` 2228–2271): `bind_literal(helper, node, cenv)` at the **invocation** statement, then `body_env = dict(cenv)` updated with bound params. Correct for plain helpers whose parameters are not closed-over factory formals.

**Capture path** (`callable_info` 1643–1659 attaches `capture_owner` + `capture_call`; `spawn_scan` 2333–2344): On invoke, `bind_literal(owner, capture_call, cenv)` uses **invocation** `cenv`, then replays factory prefix statements into `captured_env`/`captured_bindings`. That is a second, conflicting lifetime authority: factory formals are meant to be fixed at factory call time (Python closure semantics), but literals are read from the later invoke environment (F1). When `bind_literal` returns `None`, the branch is skipped and parameters resolve through unchanged invocation bindings—including module-level literals (F2). Returned nested function identity is fixed in `callable_info` from top-level `def`s in the factory body before prefix replay can rebind the name (F3).

**Partial** (`spawn_scan` 2385–2391): `fixed_nodes`/`fixed_keywords` merged at invoke; same invoke-time literal folding class as F1.

## 2. Minimal coherent snapshot-lifetime design

**Name:** `ClosureFrame` (immutable value carried on a binding entry).

**Fields:**

- `literal_env`, `binding_map`: shallow copies from `call_env[id(capture_call)]` / `binding_env[id(capture_call)]` at the **factory call** statement (same `prepare_eval_calls` pass that already exists for the cell).
- `bound_params`: result of `bind_literal(owner, capture_call, literal_env, …)` at that site, or explicit all-`LITERAL_MISS` map when bind fails.
- `node`: helper AST to follow—after running prefix statements on copies (today’s 2338–2343 logic), so factory-body reassignment before `return` selects the body (F3).
- `bind_status`: `bound` | `miss`.

**Creation (once):** When `update_bindings` / `assignment_binding` records a helper that `callable_info` marked as factory-produced (`capture_owner`), build the frame immediately using the factory call node’s statement snapshot keys. Same hook for `functools.partial`-style fixed arguments at partial **construction** (not invoke).

**Consumption:** `follow_helper` checks `cbindings[name].get("closure_frame")`. If present, seed `body_env`/`body_bindings` from the frame; bind only invoke-time arguments atop `bound_params`. If `bind_status == "miss"`, return `None` so `sweep_body` emits leads—matching docstring 47–55 and C1’s “never observed from module globals.” **`spawn_scan` 2333–2344 is deleted**; no invoke-time re-bind.

**Ordinary helpers:** unchanged—no frame; `follow_helper` still uses invocation `cenv`/`cbindings`.

**Optional unification (not required for F1–F3):** thread `(env, call_env, bindings, binding_env)` as `SiteEnv` + `get_site(node)` to stop `spawn_scan` defaulting empty dict when a snapshot is missing (2291–2292). Defer until closure frames land.

## 3. Deletions and candidates

| Item | Lines (approx.) | Verdict | Evidence |
|---|---|---|---|
| `spawn_scan` capture overlay + prefix replay | 2333–2344 (~12) | **delete** after frame creation moves to bind time | `capture_owner`/`capture_call` only referenced at 1652, 1659, 2333–2344 (text grep; LSP unavailable) |
| Invoke-time re-bind of factory formals | (same block) | **delete** | F1 mechanism in FinalBindingReview |
| `capture_owner` / `capture_call` on info dict | 1652–1659 | **candidate** → `closure_frame` only | After bind-site creation exists |
| Dual `env`/`call_env` lookup | 2291–2292 | **candidate** | Cosmetic; no F1–F3 dependency |

**Net:** ~12–18 lines removed from hot path; ~15–25 added once at binding site (frame builder extracting today’s prefix replay). No new parallel convention—frames subsume the overlay authority.

## 4. Preserved contract

- Per-file eval persistence, reset, opaque-statement clearing (`prepare_eval_calls` 2061–2065; `scan_file` 2680–2684).
- Statement snapshots for all non-closure eager calls.
- `bind_literal`, depth/budget, `sweep_body` / lead downgrade for unbound bodies.
- Thread `scheduled` binding: args/kwargs still literal-folded at **construction** (`assignment_binding` 1719–1730)—orthogonal to closure frames; seat `SimplifyThread` owns `.run`/`.start` unification.
- Evidence tiers and dedupe behavior unchanged.
- No change to `--frozen` / oracle pins in this wave.

## 5. Mapping to r21 F1–F3

| Finding | Frame rule |
|---|---|
| F1 invoke-time argv | `bound_params` frozen at factory call statement |
| F2 global leak on bind fail | `bind_status miss` → no follow; sweep/lead only |
| F3 returned def vs rebind | `node` resolved after prefix replay at creation |

## 6. Tradeoffs and unknowns

- **Cross-cell** factory in cell *n*, invoke in cell *m*: frame must live on the binding map entry (same persistence as today’s stored helper node). Source says same defect class applies; frame design supports it; not measured here.
- **Conditional factory returns** (`return a if c else b`): may need `bind_status` uncertain or two-frame merge—explicit unknown.
- **Deletion proof:** semantic references unavailable (`xd://lsp` not present); grep-only caller check recorded in `w1/notes/SimplifyCapture.json`.

## 7. Tools

None installed or updated.

## 8. Artifacts

- Machine notes: `.ufo/waves/round-22/w1/notes/SimplifyCapture.json`
- This report: `.ufo/waves/round-22/w1/reports/SimplifyCapture.md`
