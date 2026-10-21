# ConnLifetime: shared lifetime contracts across the capture, partial and thread routes

Seat: `MadoR22.ConnLifetime` (connector). This is author-lane advice; it does not judge, admit or close anything. I read source only. I made no production edits, ran no measurements, executed no payloads and ran no probes. Git use was read-only.
Notes: `.ufo/waves/round-22/w1/notes/ConnLifetime.json` (sha256 `8269d02d…8ebe`). Tool bytes: `tools/mado-tripwire.py` `46c82902…c8c1`, which is the same at `741122d` and at lane head `a963ce6`. All line numbers below refer to these bytes.

## Outcome

F1, F2 and F3 are not three bugs; they are one contract violation that seven deferred-call routes share. Three routes freeze argument values when the object is created: partial-of-spawn, stored `methodcaller`, and the `args`/`kwargs` of Thread/Timer. Four routes store unevaluated AST and evaluate it later, in the caller's environment: closure capture, returned `functools.partial`, partial-of-helper and `partialmethod`. The Thread route inherits that defect whenever its target is itself a capture or partial record.

Proposed move: **freeze the overlay, not the frame.** Every deferred route should use the representation Thread args already use, extended to both namespaces. When the object is created, resolve a small overlay of `name → (literal | MISS, binding | parameter)` for the factory parameters and the factory's own local names. Choose the callable's identity from the bindings in effect at the `return`, under an owner-id guard. When the object is called, lay that overlay over the caller's env and bindings.

Three source findings bear on that move. They are inferences; I did not probe them:
- **V3, current counterexample.** A capture parameter can shadow a module-level callable binding, and this fabricates an observed row even when argument binding succeeds. FinalBindingReview's F2 remedy (set factory parameters to `LITERAL_MISS` on bind failure) does not cover it.
- **V1 and V2, regression traps.** These pass today. A fix that snapshots the whole env or binding map at creation, as SimplifyCapture's ClosureFrame proposes, would break them.
- **V6, regression trap that no guard covers.** A fix that freezes literals only would turn this observed row into a lead. No corpus case exercises this shape, so the no-harm guards would not notice.

## Axes

| Axis | Effect of the move |
|---|---|
| C1 agreement (frozen F1–F5 expectations and variants) | Improves: closes F1, F2, F3, V3, V4, V5, V8 and V9 under a single rule. |
| C1 no-harm (oracle35+17, incident recall, existing suites, 1356-fixture removal/relabel/error comparison) | Protected: the caller's env stays the base layer, so V1 and V2 keep passing. Carrying bindings in the overlay keeps V6 observed. |
| C1 soundness | Improves: a binding that fails becomes a mask, not a fall-through to module globals. |
| Resource (1000/2000/4000 assignment recipes) | Cost grows with the number of overlay names per record, not with the size of the whole env plus bindings. |
| C2 independence | Not touched. |

## Repeated dataflow contracts

1. **Deferred-call record** (spawn_scan 2333–2344 and 2384–2391; callable_info 1635–1659; class_method_info 1581–1591; assignment_binding 1718–1755). Every route produces a record of (identity, fixed positional arguments, fixed keyword arguments) that is used later. The F1 class is exactly the set of routes that carry AST in that record.
2. **Two namespaces** (the literal env and the bindings map):
   - `follow_helper` shadows names in both (2241–2263).
   - `sweep_body` masks bindings and uses an empty env (2193–2199).
   - The capture overlay updates the env only (2336–2337); this is V3.
   - `thread_start` injects into bindings only (2299–2300); this is F5.
3. **What happens when arguments cannot be bound:**
   - `follow_helper` falls back to a sweep, so the row becomes a lead.
   - `thread_start` counts the call as unparsed.
   - The capture route uses the caller's env and reports observed; this is F2.
   - A stored `methodcaller` whose method name is not a literal drops through every branch and produces nothing; this is V12.
4. **Identity selection.** The returned closure is chosen as the last top-level `def` with that name (1646–1647). A returned partial's wrapped function is resolved against module bindings (1657). The prefix replay (2338–2343) runs only after identity is already fixed; this is F3.
5. **Ownership exemption.** The refs sweep skips any value passed to `Thread(...)`/`Timer(...)` unconditionally (2550–2553). Ownership exists only when a `.start` consumer is recognized (1666–1667 for named threads, 2294–2297 for inline ones). Every unrecognized consumer is therefore silent with unparsed 0: `.run` (F4), V10, and threads that are never started.

## Bounded invariants

- **I1, freeze when created:** a record that outlives the statement that produced it holds no AST that is evaluated later.
- **I2, mask both namespaces:** names a frame binds are masked in the env and in bindings, on both the bind-success and bind-failure paths.
- **I3, identity in effect:** the returned identity is the factory-local binding in effect at the `return`, including the name wrapped by a returned partial.
- **I4, late globals:** names no frame masks are read when the caller runs the code. For asynchronous consumers (`Thread.start`, `Timer.start`), that read happens at an unbounded later time.
- **I5, synthetic isolation:** the resolved record travels on the synthetic AST node, never under a source-spelled name.
- **I6, downgrade, never fall through:** a binding failure becomes a lead or unparsed, never an observed row and never silence.
- **I7, bounded resolution:** identity resolution and prefix replay carry an owner-id stack.
- **I8, one read instant:** creation-time literals and bindings are read from the same pre-statement snapshot. Today `assignment_binding` sees the env after the statement's own update (2066–2074) but bindings before it (1805–1811).
- **I9, exemption only with ownership:** a Thread/Timer target is skipped by the sweep only when a recognized consumer followed it.

## Variant gaps

Cells are in the notes JSON. Every "today" result below is a source-reading inference, not a probe result.

| Variant | Invariant | Truth | Today, by source | Kind |
|---|---|---|---|---|
| V1 ClosureLateGlobal | I4 | observed `-S r22-late` | pass | trap: whole-env snapshot breaks it |
| V2 ClosureLateHelper | I4 | observed `-S r22-late-helper` | pass | trap: binding-map snapshot breaks it |
| V3 CaptureParamShadowsCallable | I2 | no row (`f` is `print`) | observed `-S r22-shadow`, fabricated | counterexample; survives an env-only F2 fix |
| V4 ThreadTargetFactoryLate | I1 × thread | observed `-S r22-tcap` | observed `-Q r22-tlate` | counterexample (may overlap the ThreadConstructorCapture seat) |
| V5 PartialMethodLate | I1 | observed `-S r22-pm` | observed `-Q r22-pm-late` | counterexample; no seat covers it |
| V6 PartialCallableFixed | I2 | observed `-S r22-pcall` | pass | trap: a literal-only freeze turns it into a lead; 0 of 18 corpus partial files guard it |
| V7 TimerCancelThenRun | F4 | no row (threading.py 1378–1386) | no row | trap for a naive `.run` fix |
| V8 ReturnedPartialLocalDef | I3 | observed `-S r22-local-inner` | observed `-Q r22-module-inner`; silent if the module-level `def` is absent | counterexample |
| V9 ReturnedUnreachableDef | I3 | observed `-S r22-reach` | observed `-Q r22-dead` | counterexample |
| V10 InlineThreadStartAlias | I9 | observed `-S r22-ialias` | silent, unparsed 0 | counterexample; a `.run` alias would inherit it |
| V11 SelfReferentialPartialFactory | I7 | no row | unbounded recursion, so the whole run becomes `could_not_evaluate` and every file's findings are lost | robustness |
| V12 MethodcallerUnknownName | I6 | lead or unparsed | silent | pre-existing, outside F1–F5 |
| V13 SelfRebindFactoryArg | I8 | observed `-S r22-self` | unparsed | recall loss in the safe direction |
| V14 TimerStartLateGlobal | I4 async | no single determined command | observed `-Q r22-early` | pre-existing over-claim, outside F1–F5 |

## Contradictions (stated, not resolved)

- **K1.** SimplifyCapture's ClosureFrame captures `literal_env` and `binding_map` at creation. Python reads a closure's free globals when the closure is called. V1 and V2 pass today and would regress under that design.
- **K2.** FinalBindingReview check 1 says to set factory parameters to `LITERAL_MISS` on bind failure. V3 fails on the bind-success path, because `bind_literal` appends MISS values and returns None only for structural failures. The overlay touches only the env.
- **K3.** FinalBindingReview check 2 says to keep the refs exemption. The frozen CallbackBoundArgs rationale ("Mere stored targets without start remain distinct conservative leads") and docstring lines 47–50 say the opposite. The exemption at 2550–2553 is unconditional. FinalBindingReview cites it as 2517–2519 for the same file bytes; in these bytes, 2517–2519 is the argument-protocol consumer list.
- **K4.** `thread_start` follows the target with the env of the `start` statement and reports observed (2291, 2308). An asynchronous target reads globals later than that. This predates round 22 and sits outside F1–F5, but `.start` is a declared supported form.

## Risks

- I9 adds leads for threads that are constructed but never started. These must appear as reviewable additions in the 1356-fixture comparison.
- For `partialmethod`, no binding retains the env from when the class was defined. Either keep a reference to the ClassDef's pre-statement snapshot, or treat any fixed argument that is not a constant as MISS. The second option is sound but downgrades V5 to a lead.
- The I7 guard is a per-resolution stack. It must not suppress repeated factory calls with different arguments (the TwoInstances shape).

## Verification for other lanes (I ran none of this)

1. Independent oracle seats should freeze V3, V5, V6, V7, V8, V9, V10 and V11 before implementation, using the w1-spec proposal shape.
2. After implementation, replay the six r21 inert fixtures, oracle35+17 and the 1356-fixture comparison. V1, V2 and V6 must stay observed. V3, V8 and V9 must produce none of their forbidden observed rows.
3. Kill a mutant: drop the bindings half of the overlay mask. V3 must go red while V1 stays green.

## Addendum: proposals authored at MadoR22's request (2026-10-21)

These seven proposals live in `w1/proposals/` and use exactly the seven keys `assemble.py` accepts. Each one passed the harness's own `validate_proposal` (loaded with `-I -B`; this did not assemble anything or run the scanner). Cells were checked with `ast.parse` only. Each rationale opens with an execution classification; none of the seven raises a definite TypeError.

| ID | Kind | Want | Classification | sha256 |
|---|---|---|---|---|
| CXCallableShadow | exact | none (forbid observed `-S r22-cxshadow`) | definite no execution, no exception | `3004c513…e8e1` |
| CXPartialLocalFunction | exact | observed `pacman -S r22-cxlocal` | definite execution | `5001bb9b…6848` |
| CXReturnAfterDef | exact | observed `pacman -S r22-cxafterdef-live` | definite execution | `c3df6f70…5671` |
| CXInlineStartAlias | exact | observed `pacman -S r22-cxinline-alias` | definite execution | `bb76deac…5592` |
| CXRecursivePartialFactory | uncertain | none; forbid observed `-S r22-cxrec`; the uncertain rule requires a lead or unparsed signal | unknown: ValueError, execution, or RecursionError depending on the environment value | `58aa71a7…fb64` |
| CXPartialCallableArg | exact | observed `pacman -S r22-cxpcall` | definite execution | `09b7b64d…28cf6` |
| CXPartialMethodTiming | exact | observed `pacman -S r22-cxpm` | definite execution | `000f42e9…80ed` |

`require_signal` is expressed through `expected_kind: uncertain`, because the harness rule already requires zero observed rows plus at least one lead or a positive unparsed counter. An extra key would get the file rejected.

**Harness coordination finding.** `assemble.py` (PROPOSAL_KEYS, and the check that the id matches the filename stem) would reject 9 existing peer proposals at assembly:
- Extra keys: CX11Reset, CX1AnyTierLeak, CX3CaptureMutation, CX4NonlocalMutation, CX9UnknownKeyword, CaptureKwUnknown.addendum, CaptureMissingRequired (`language`), CaptureStarUnknown.
- Id does not match the filename: `CaptureNestedFactoryCorrected.json` carries id `CaptureNestedFactory`.

Their extra assertions (`forbid_commands_any_tier`, `accept_exact_want`, `cell_reset`) would not be scored even if the extra keys were stripped.

## Limits

- Every "today" result is a static inference. For V11, I did not determine whether it ends in a RecursionError or a C-stack overflow under a 64 MiB stack.
- No semantic call-graph tool was available; I traced callers with reads and literal grep.
- `w1/proposals` was empty when I read it, so overlap with seat contents is unknown beyond seat names.
- Tools installed or updated: none.
