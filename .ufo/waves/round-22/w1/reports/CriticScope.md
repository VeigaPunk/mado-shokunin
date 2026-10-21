# CriticScope — bounded C1 target vs general repair wording

Seat `MadoR22.CriticScope` · critic · author-lane advice, not judgment, admission or outside-lane falsification. Machine-readable form: `.ufo/waves/round-22/w1/notes/CriticScope.json`.

## Answer

**The planned set can falsify only part of the r21 objections.** The original six fixtures plus the 28 planned C1 variants can fail an overfit or cheap repair for these:
- the exact F1, F3 and F4 shapes;
- the observed-tier F2 leak for three of its four triggers;
- the one known F5 key name.

The set has good anti-overcorrection guards: CaptureGlobalLate, ThreadGlobalLate, CapturePartialGlobal and CaptureDefault.

The set **cannot** falsify these, as planned:
- a lead-tier F2 leak;
- the repair designs' own new failure modes: object aliasing, `nonlocal` cell mutation, `Timer.cancel`, repeated `run`, and rebinding after return;
- the F2 unknown-keyword trigger;
- capture × thread composition;
- the `reset:true` boundary;
- any F5 key other than the known name.

Its admission-defeating clause also points at "declared supported forms" that are declared nowhere.

## Axes

Scope honesty · falsification power · repair regression · evidence tier · provenance independence.

## Scope findings

| ID | Severity | Finding | Smallest correction |
|---|---|---|---|
| S1 | High | The registration says "a new counterexample to the declared supported forms … defeats admission", but neither `registration.md` nor `audit-contract.json` declares any forms. The w1-spec seat lines are the only list. A wave2 counterexample could be ruled "unsupported" after the fact, which silently shrinks scope. | Before seal, freeze `supported_forms` (the originals plus every eligible variant id) and `unsupported_forms` (list below) into the sealed expected.json or a dated addendum. |
| S2 | High | F1–F5 are labels for whole mechanisms. Closing them by ID on a finite pass reads as a general repair. The r21 knowledge note already says the findings "falsify the general binding-repair claim". | Report per form, for example "F1 listed forms N/N". Keep each F-ID open for every unsupported trigger. |
| S3 | Medium | The originals' truths are author-lane reasoning (FinalBindingReview header). `thread-key-control` is a passing control, so "every original red" means five reds plus one no-harm control. | Label the provenance in expected.json. Independence credit rests on the variants. |
| S4 | Medium | L1 chose every variant from the FinalBindingReview taxonomy, and each seat was told to read it. The variants are near neighbours of known shapes: they catch overfitting but cannot discover new mechanism classes. Only the 4 revenger seats are partly open-ended. | Disclose this as a near-neighbour set. |
| S5 | Medium | "Exact" must stay as in r21: multiset equality on (class, command, evidence), unparsed 0, no extra rows (`round-21/oracle/measure.py:42,64`). Otherwise a repair that emits both the old and new rows passes. The r22 oracle harness was not delivered when I reviewed. | Keep the r21 `rows_key` rule in the sealed measure.py, and have wave2 check it. |

## Counterexamples

All source text below is inert data. None of it was run. Truths are static Python 3.14.8 reasoning.

- **CX1 (High, F2, fixable): lead-tier borrowing passes.** The cheap wrong patch keeps resolving the factory parameter from the module global and marks the rows lead. On `capture-unbound-global` it then emits lead `pacman -Q r21-global`. The planned rule ("uncertain requires no observed rows + at least lead/unparsed") accepts that, yet it is still the F2 mechanism. Correction: add an any-tier `forbid_commands` list to uncertain proposals, holding the shadowed global's command.
- **CX2 (Medium, F2, tradeoff): the signal rule diverges from the registration.** The planned rule *requires* a lead or unparsed signal, but the registration says unknown capture arguments "may" produce one. CaptureMissingRequired and CX9 raise TypeError at the factory call, so producing no row is correct, and that correct output would fail. For `capture-unbound-global`, `parts` might exist in unknown prior session state, so requiring a signal is defensible there. Correction: give each uncertain proposal a `require_signal` flag with a rationale.
- **CX3 (High, the F1 repair regresses): aliasing mutation.** Run `cmd = ["pacman","-Q","r22-alias"]; runner = make(cmd); cmd[1] = "-S"; runner()`. Truth: observed host_mutation `pacman -S r22-alias`, because the closure holds the object, not a copy (simple_stmts.rst:146; executionmodel.rst:322).
  - SimplifyCapture's `ClosureFrame.literal_env` freezes values at creation, so it would report `pacman -Q` observed. That is the inverse of F1, with the host mutation hidden.
  - Thread `args=(cmd,)` mutated before `start`/`run` has the same defect under SimplifyThread's construction-time folding.
  - Correction: add CaptureAliasMutation and ThreadArgsMutation variants. Any in-place mutation of a captured name sends the result to uncertain, never to an observed pre-mutation row.
- **CX4 (Medium, tradeoff): `nonlocal` retarget.** A sibling inner function rebinds the shared cell after the closure is created, so a frozen frame reports the stale command as observed. Correction: add a variant, or declare the form unsupported and require uncertainty.
- **CX5 (Medium, F3, fixable): rebinding after return.** In `return a` followed by `a = b`, the second line is dead code. A full-body "post-prefix" replay would pick `b`. Every planned F3 variant rebinds *before* the return. A conditional rebinding on an unresolved condition must be uncertain, with both commands forbidden as observed. Correction: add CaptureReturnBeforeRebind and CaptureConditionalRebind.
- **CX6 (High, the F4 repair regresses): `Timer.cancel()` before `run()`.** `threading.py:1378-1386`: `cancel` sets `finished`, so `run` skips the function. SimplifyThread's unified `.run`/`.start` path, which marks both observed, would fabricate an observed host_mutation. No variant seat covers this, although the SourceThread scout was asked to flag it. Correction: add TimerCancelRun with an empty `want`.
- **CX7 (Medium, F4, fixable): repeated `run()`.**
  - `Thread.run` deletes `_target` in its `finally` (`threading.py:1025-1028`), and `_target` is only an instance attribute (line 925). So a second `t.run()` cannot call the target again.
  - A second `Timer.run()` finds `finished` already set (line 1386).
  - The truth is one row; a repair that follows every call site emits two.
  - `start()` followed by `run()` races, so it is uncertain.
  - Correction: add ThreadRunTwice, or declare the form unsupported.
- **CX8 (Medium, fixable): capture × thread composition.** The shape is `Thread(target=make(cmd))`, then the caller rebinds `cmd`, then `t.run()`. The two simplifier designs call themselves orthogonal, and each passes its own fixtures alone. Correction: add ThreadTargetClosure.
- **CX9 (Medium, F2, fixable): no variant for the unknown-keyword trigger.** FinalBindingReview lists four F2 triggers. The unknown keyword (cited lines 2017–2018) has no variant: CaptureKeyword is an F1 rebinding shape. Positional overflow is a sibling shape. Correction: add CaptureUnknownKeyword (uncertain, `require_signal:false`, forbid the global's command), or keep F2 open for that trigger.
- **CX10 (Medium, F5, tradeoff): fixtures cannot prove F5.** Both hygiene variants use the literal `__mado_thread_target__`. Renaming the key to any other identifier passes every fixture and keeps the defect. Correction: close F5 only on a structural source check by a non-author wave2 seat: no synthetic bindings key is a valid identifier, or the callable is carried on the node.
- **CX11 (Low, fixable): `reset:true` across cells.** CaptureCrossCell relies on the namespace persisting between cells. If a reset clears it, the closure name is undefined. A frame persisted across the reset would fabricate an observed row. Correction: pin `reset:false` and add a `reset:true` counter-variant that expects no observed row.

## Unsupported forms to declare (not silently dropped)

- Each item below stays unsupported unless its variant is added:
  - in-place mutation of a captured object or Thread argument (CX3);
  - `nonlocal` cell mutation (CX4);
  - rebinding of the returned name after `return`, under a condition, or in a loop (CX5);
  - `Timer.cancel` before `run`, repeated `run`, and `start` plus `run` (CX6, CX7);
  - capture × thread composition (CX8);
  - the F2 unknown-keyword and positional-overflow triggers (CX9);
  - the `reset:true` boundary (CX11).
- Non-Name factory returns: conditional expressions, tuples, a returned call, a returned lambda.
- Closures stored in a container, attribute or dict; closures passed as callbacks; decorators.
- Lambda, generator, async, class-body and bound-method closures.
- Factory bodies with try/with/loop control flow before the return.
- `global` declarations inside a factory.
- Imported factories; `functools.wraps`; partial of partial; partial with unknown `*args`/`**kwargs`.
- Thread subclass or inherited `run`; `Thread.run(t)`; `getattr(t, "run")()`.
- Other schedulers: `concurrent.futures`, `multiprocessing.Process.run`, `asyncio.to_thread`, `_thread`.
- F5 key names other than the known one (structural check only, CX10).
- Python profiles other than CPython 3.14.8.

## Which failures are fixable before seal and which the judge must reject

- **Fixable before seal:** S1, S2, S5, CX1, CX5–CX9 and CX11. Fix them by adding frozen variants or schema fields. No existing proposal's expectation changes.
- **Judge must reject if violated:** CX2, where the signal rule must match the registration text. CX3/CX4: if object mutation stays unsupported, any observed pre-mutation row defeats admission. CX10: the F5 fixtures are not proof.
- **Disclosure only:** S3 and S4.

## Unknowns

- `[INFERENCE]` I have not established whether the scanner invalidates its tracked value on a subscript store or a mutating method call. I read no production code.
- Whether the r22 harness keeps the r21 exact rule; it had not been delivered.
- `[INFERENCE]` Whether the scanner deduplicates rows per receiver, which decides whether CX7 is detectable.
- The contents of the 28 C1 variant proposals. Only ThreadHygiene.json and ThreadRun.json existed, and I did not read them.

## Method and receipts

I only read files: the registration, the audit contract, the w1-spec seat list, FinalBindingReview, and the six originals (parsed as JSON; digests match the review). I also read the r21 dispositions, final summary and outcomes, the r21 `measure.py` lines 42 and 64, the r21 knowledge note, and the SimplifyCapture and SimplifyThread notes. CPython quotes come from the scout-retained bytes:
- `threading-v3.14.8.py`: `5323909624ec…a7e3`
- `executionmodel.rst`: `11f99f83d785…eb89`
- `simple_stmts.rst`: `d43206423b32…29dc`

I made no measurements, no scanner runs, no payload execution and no production edits. All Git access was read-only. No tools were installed or updated.

## Addendum (2026-10-21, at MadoR22's request): CX proposals authored before seal

Nine new data-only C1 proposals are now in `.ufo/waves/round-22/w1/proposals/`. No existing proposal was changed. I ran no detector, executed no payload and edited no production code. Each cell was checked with `ast.parse` only.

| File | Kind | Truth | sha256 |
|---|---|---|---|
| `CX1AnyTierLeak.json` | uncertain, signal required | A bound but lexically unknown positional argument; the same-named global is forbidden at every tier | `10f4d4e6…456c` |
| `CX3CaptureMutation.json` | uncertain, signal required, exact accepted | Truth is `pacman -S r22-cx3-mutation` observed; the stale `-Q` is forbidden at every tier | `74d66361…e456` |
| `CX4NonlocalMutation.json` | uncertain, signal required, exact accepted | Truth is `pacman -S r22-cx4-nonlocal` observed; the stale `-Q` is forbidden at every tier | `d82343f9…0e06` |
| `CX5AfterReturn.json` | exact | `pacman -Q r22-cx5-early` observed; the rebinding after `return` is dead code | `98925a43…e241` |
| `CX6TimerCancel.json` | exact, empty | `cancel()` then `run()` never calls the function | `9593ed60…bdb2` |
| `CX7ThreadRepeatedRun.json` | exact | One row; the second `run()` raises AttributeError | `cf7029dc…5679` |
| `CX8ClosureThread.json` | exact | `pacman -S r22-cx8-compose` observed; tests capture × direct `run` | `335eacd8…fe97` |
| `CX9UnknownKeyword.json` | exact, empty | TypeError at the factory call | `374b2312…bc75f` |
| `CX11Reset.json` | exact, empty | NameError after the reset (rests on a premise, see below) | `1ab019a3…fac` |

Main must decide three things before freezing the spec:
- **`accept_exact_want` (CX3 and CX4) is a new field.** The truth in both cases is a definite observed row. Under the planned rule that an uncertain proposal has no observed rows, a correct exact answer would fail. The harness must accept either a correct exact result or a signal-only result, and the stale command is forbidden in both.
- **`cell_reset` (CX11) is a new field.** OracleHarness must emit `arguments.reset` for each cell. If it drops the flag, the truth flips to one observed row, and CX11 must be marked ineligible rather than re-scored.
- **CX11 rests on a premise, not retained bytes.** It assumes that `reset: true` means a fresh namespace. The only on-disk description I found is the detector's own docstring, which I did not use as truth. CX9's TypeError rule cites the Language Reference "Calls" section by name, because `expressions.rst` is not among the retained bytes.

CX3 and CX4 also forbid the stale command at every tier, which is stricter than the directive's observed-only requirement. The reason is that the stale command definitely never runs. Main may relax this to observed-only.

Still not authored: ThreadArgsMutation (the Thread sibling of CX3), CaptureConditionalRebind (the CX5 sibling) and `start()` plus `run()`, which races. Until those exist they stay on the unsupported list above.

## Checks for Main (not run by me)

1. Confirm that the sealed oracle's `measure.py` uses the r21 `rows_key` multiset rule for the exact kind.
2. Confirm that uncertain expectations carry an any-tier `forbid_commands` list and a per-proposal `require_signal`.
3. Confirm that `supported_forms` and `unsupported_forms` are frozen before the seal digest is taken.
