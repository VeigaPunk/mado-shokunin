# FalsifyC110 — CXCallableShadow (round22 w2, delivered 71228fd582d6d9338d7916cc64e69bd4c2e928b5)

## Verdict: AGREE

One authorized measurement only. The delivered tool's observed result matches the sealed truth
for the right semantic reason; every assigned falsification angle failed to break the case.

## Sealed truth (read independently before measurement)

- `oracle/expected.json` case `CXCallableShadow` (group `proposal`, lines 486–519):
  `expected_kind=exact`, `want=[]`, `forbid_observed_commands=["pacman -S r22-cxshadow"]`,
  `forbid_commands_any_tier=[]`, `accept_exact_want=null`, `require_signal=false`,
  `cell_count=1`, `cell_reset=[false]`, fixture `inputs/CXCallableShadow.jsonl`
  sha256 `c74d563c2f825f4279f7ab99efff061e0ceb0b85fdc6853f1988849bd7a3e10c` (verified on disk).
- Original proposal `.ufo/waves/round-22/w1/proposals/CXCallableShadow.json`
  sha256 `3004c5130890f921d872456949bef021659ccb89e1e359e1d1d95e16ed65e8e1` preserved byte-identical
  (runner re-verified against the sealed inventory).
- Source cell: `make(f)` returns nested `run` closing over parameter `f`; module-level decoy
  `f = subprocess.run`; `runner = make(print)`; `runner()` invokes `print(["pacman","-S","r22-cxshadow"])`.
- Independent semantic reasoning: in CPython scoping, `f` inside `run` is a free variable resolving
  to the nearest enclosing function scope — `make`'s parameter cell, bound to builtin `print` at
  `make(print)` — never the module binding `f`. `print(list)` writes a repr to stdout, returns None,
  starts no process, raises nothing. True population = empty row multiset, zero uncertainty.
  The sealed truth is correct; no truth/expectation contradiction found, nothing normalized away.

## Actual measurement (the one authorized run)

`python3 -I .ufo/waves/round-22/oracle/measure.py --tool tools/mado-tripwire.py --case CXCallableShadow`
- Runner argv/exit/stdout/stderr retained verbatim in
  `.ufo/waves/round-22/w2/receipts/FalsifyC110/result.json` (includes the full scanner child
  argv/exit/stdout/stderr and payload).
- Population validation before and after: 57 inputs / 52 proposals / 106 sealed source files
  verified; expected.json sha `b5cd4cf3…` matches the fixed identity; integrity_before ==
  integrity_after; zero integrity errors. Scanner child: one process, RLIMIT 384 MiB, 15 s cap.
- Scanner result: `got_rows=[]`, `unparsed=0`, scanner `exit=0`, stderr empty,
  payload `findings=[]`, `observed_findings=0`, `lead_findings=0`, `eval_unparsed=0`,
  `unparsed_spawns=0`, `eval_calls=1`, verdict `MADO_TRIPWIRE: clean`.
- Evaluation: exact kind → multiset `[] == []`, unparsed 0, no parse errors, no forbidden rows.
  Runner `totals={pass:1, total:1}`, exit 0.
- Hashes (receipt): tool `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce`
  before and after (no drift, not a moving target); runner measure.py
  `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7`; fixture `c74d563c…`.

## Falsification attempts (all failed to break the case)

Source-audited against delivered `tools/mado-tripwire.py` (sha `36fdc459…`), path by path:

1. Wrong identity (decoy resolution). In `factory_result` the call-time copy of module bindings
   (which contains decoy `f → {"kind":"spawn","name":"subprocess.run"}`) is overlaid by
   `bound_callables`, mapping parameter `f → {"kind":"pure","name":"print"}`; that parameter
   binding is snapshotted into `closure_bindings` and, at the `runner()` call site, the closure
   overlay is applied to the callee bindings *after* the module copy, so `f` resolves through
   `callable_info`'s Name branch to the closure binding before any global/dotted lookup. Had the
   decoy won, the spawn dispatch would have classified the literal argv into an observed
   `pacman -S r22-cxshadow` host_mutation row (forbid_observed + multiset violation). Absent.
2. False lead / false observed argv. Had the closure not been tracked, `f` would carry
   `{"kind":"parameter"}`; the unknown-callee fallthrough emits a lead row via
   `helper_argv_leads` for the literal argv. Absent — zero leads proves the resolution machinery
   engaged rather than silently skipped.
3. Parsed-clean ambiguity (clean by dropping). Excluded: `eval_unparsed=0`/`unparsed_spawns=0`
   are consistent with the mechanism audit — `def make` body walk yields zero calls and zero refs
   (`eager_calls` records a Name ref only when it is a call argument, so `return run` sweeps
   nothing; deferred bodies are skipped), and the followed `run` body's single call resolves to a
   `pure` callee, which dispatches `continue` (no row, no unparsed). A silent under-approximation
   would have had to suppress a lead or observed row that the fallthroughs demonstrably produce
   for the adjacent failure modes; neither exists.
4. Invalid-shortcut false clean. `factory_result` returns `{"kind":"invalid"}` only when
   `bind_literal` returns None; for `make(print)` it returns `{"f": LITERAL_MISS}` (single
   positional parameter, no starred/kwargs edge), so the operative path is genuine closure
   resolution, not an invalid-call skip that would coincidentally also emit zero rows.
5. Lost true command. Truth is the empty multiset; there is no true command to lose, and `print`
   is correctly not a spawn sink (`PURE_ARG_CALLS`).
6. Lifetime. Single cell, `cell_reset=[false]`; identity captured at creation
   (`runner = make(print)` stores the returned helper plus closure snapshot in module bindings)
   and invoked in the same cell — the stored-and-immediately-invoked form of supported-forms.
   No cross-cell or reset interaction exists for this case.
7. Conditional target. N/A — no conditional or non-Name return in this fixture; the returned
   value is a plain Name resolved through `local_bindings`.
8. accept_exact_want vs true uncertainty. `accept_exact_want` is null and `expected_kind` is
   exact, so no uncertainty-escape tier was available or used; the pass is the full exact
   contract (complete multiset + zero errors + zero unparsed), not a permissive acceptance.
   `require_signal=false` is honored (a definite no-execution case needs no lead/unparsed signal).
9. Unknown-case any-tier bans. N/A — this is an exact case; `forbid_commands_any_tier` is empty,
   and `forbid_observed_commands` is satisfied vacuously (zero rows at any tier).

## Scope

- This verdict covers exactly the sealed case `CXCallableShadow` on delivered revision
  `71228fd582d6d9338d7916cc64e69bd4c2e928b5` with C1 tool sha `36fdc459…` (fixed identity
  confirmed). It validates the named finite form: a factory whose parameter lexically shadows a
  same-named module binding, with a resolvable builtin passed as the factory argument. Per
  supported-forms, a finite pass closes only the named tested form, never the whole defect
  family; the 56 sibling cases were population-validated but not measured here (forbidden).
- Original r21 red authority untouched: I did not rerun the old tool (sha `46c82902…`) against
  anything; the r21 defect mechanism cited by the proposal (capture overlay updating env only,
  captured bindings keeping the module binding) is structurally repaired in the audited path.

## Residual risk / verification gaps

- No new source-shaped probe was run (none assigned); the mechanism audit is static reading of
  the delivered bytes plus the single authorized measurement.
- `statement_snapshot`'s reachability pruning (`names`) was read only at the level needed for
  this case (`f` and `run` are retained in the closure overlay); exotic pruning interactions on
  other cases are out of this seat's scope.
- Green here is one seat's evidence, not an admission grant and not a whole-population result.

No production, fixture, oracle, registry, or sibling files were modified. Receipts:
`.ufo/waves/round-22/w2/receipts/FalsifyC110/result.json`.
