# C1 CaptureReturnedRebound — FalsifyC134

## Findings by severity and recommendation

**No actionable defect found in this assigned case. Verdict: agree.** The delivered detector returns exactly the independently justified one-row multiset, with zero unparsed counters and no extra observed or lead argv. This is an author-lane advisory recommendation about one finite source shape, **not admission**, host clearance, or a saturation claim.

Target: delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`; the selected current scanner matched the assigned SHA-256 before and after the measurement. The relevant actual source diff was read from registered base `741122d177ae8ff68a73768777f20484d5bdcbe4` to that revision. The historical r21 F3 red remains source authority; no old scanner was run to reconfirm it.

## Axes

1. **Precision / evidence honesty:** no invented command at either evidence tier; no unsupported promotion to observed.
2. **Recall / complete result:** retain the true host-mutation command and compare the complete row multiset, including multiplicity and evidence.
3. **Callable identity / lifetime:** select the function bound to the returned name after the executed factory prefix, not the original definition bearing that name.
4. **Uncertainty calibration:** distinguish an exact direct invocation from unknown arguments, conditional targets, and parsed-but-unresolved source.
5. **Artifact identity / bounded execution:** measure one pinned scanner and fixture, retain raw streams, and respect the runner's one-child 384 MiB / 15 s bounds.

C2 audit behavior, other C1 cases, resource saturation, and fleet/admission decisions are outside this seat.

## Independent semantic assessment

The sealed fixture contains one inert Python eval cell [S1, S2]. Its only source-level execution chain is `make()()`:

- Defining `make` does not run its body. Calling it defines two local function objects, F1 under `first` and F2 under `second`. Defining either nested function does not execute its `subprocess.run` body. The cited language reference explicitly specifies both the local binding and deferred body execution [S4].
- The straight-line statement `first = second` binds the local name `first` to F2. There is no decorator, branch, default expression, descriptor, dynamic expansion, or intervening mutation. The language-reference binding and nearest-scope rules apply to these names [S5].
- `return first` therefore returns F2, and the outer immediate call invokes F2 once. F1 is never called. This is callable-object identity, not a def-name lookup. There is no later factory-frame mutation or mutable captured argv to reconstruct in this fixture.
- The only process-call argv is the literal `['pacman', '-S', 'r22-rebound-second']`. The token-safe command is `pacman -S r22-rebound-second`. Under the registered command-class convention, plain `pacman -S` is a host mutation; the visible literal and unconditional direct invocation support the scanner's **observed** tier. Here “observed” is a static evidence marker, not evidence that a package transaction actually ran. No fixture code or printed command was executed.

Thus the complete independently expected result is exactly:

```json
[{"class":"host_mutation","command":"pacman -S r22-rebound-second","evidence":"observed"}]
```

Expected error counters: `eval_unparsed = 0`, `unparsed_spawns = 0`. The dead F1 command `pacman -Q r22-rebound-first` has no reachable invocation and should not appear as observed **or lead** in this exact result.

This agrees with the original proposal, not merely its normalized copy. The sealed record has `expected_kind: exact`, `accept_exact_want: null`, no addenda, and no correction [S1, S2]. Although its explicit any-tier forbid list is empty and its observed-only forbid names F1, full exact multiset equality independently rejects an extra F1 lead as well. The exact branch requires equality plus zero unparsed counters [S7]. The uncertain-case `accept_exact_want` alternate is not applicable, and neither an empty parsed-clean result nor a lead-only substitute would satisfy this case. The normalized `require_signal: true` does not convert an exact case into uncertainty.

## Actual changed behavior and relevant callers

The read base-to-delivery diff removes the old local def-name index and `capture_owner` / `capture_call` return selection. It introduces `factory_result`, routing a visible helper call through that resolver. The historical defect is stated at [S3]: choosing the def node before replaying the prefix could report the query from F1 instead of the transaction from F2.

The selected current path addresses that mechanism for this fixture [S6]:

1. `callable_info` resolves the outer call's callee expression `make()` through `factory_result` (lines 1757–1783).
2. `factory_result` binds the zero-argument factory, replays statements before the first direct return, and **then** resolves `returned.value` against the resulting local bindings (lines 1642–1684, especially 1674–1675).
3. `prepare_eval_calls` applies `update_bindings` in statement order; nested defs install their helper nodes, and `assignment_binding(Name)` returns the current binding. Therefore `first = second` replaces `first` with F2's helper identity (lines 1828–1834, 1882–1891, 1928–1937, 2203–2254).
4. `eager_calls` skips nested function bodies rather than treating their mere definitions as execution (lines 2051–2063). `follow_helper` follows the selected zero-argument F2 body (lines 2407–2439). The known-callee bookkeeping avoids sweeping an already resolved immediate-call reference as an additional lead (lines 2564–2580, 2685–2687).
5. The `subprocess.run` path folds the literal argv and classifies its serialized command (lines 2632–2684); plain sync maps to `host_mutation` (lines 775–780).

No unsupported conditional target, binding-failure path, recursion fallback, or delayed callback is needed to explain the measured row. Those paths are not certified by this case.

## Sole authorized measurement and actual rows

Exactly one scanner case was run, via the assigned command:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CaptureReturnedRebound
```

Raw receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC134/result.json`.

| Observation | Actual |
| --- | --- |
| Oracle status / exit | `complete` / `0` |
| Selected-case pass / total | `1 / 1` |
| Scanner exit / label | `1` / `MADO_TRIPWIRE: findings` |
| Complete actual rows | one `host_mutation`, `pacman -S r22-rebound-second`, `observed` |
| Finding identity | selected fixture, JSONL line `1`, tool `eval`, call id `CaptureReturnedRebound-0`, argv0 `pacman`, rule `pacman:-S` |
| Observed / lead findings | `1 / 0` |
| Dead F1 command at any tier | absent |
| Eval calls / bash calls | `1 / 0` |
| `eval_unparsed` / `unparsed_spawns` | `0 / 0` |
| Comparison reasons / scanner error | `[]` / `null` |
| Runner stderr / scanner stderr | empty / empty |
| Integrity errors | `[]` |

Scanner exit `1` is the expected finding-positive policy result, **not** a scan failure and not a clean verdict; the common verdict logic makes this explicit [S6, lines 2909–2940]. The oracle separately returns `0` for agreement.

The receipt preserves the exact requested outer argv (including `-I`), outer exit/stdout/stderr, the runner's complete JSON, and the capped scanner child's argv/exit/stdout/stderr and payload. The runner imports only the selected scanner and calls its scan entrypoint; fixture code is AST input. Cap and timeout enforcement are at [S7, lines 26–27 and 643–661]. No alternative scanner identity, old tool, baseline rerun, new source-shaped probe, or additional measurement was used.

The runner validated all **57 input artifacts**, **52 proposal artifacts**, and **106 sealed source artifacts** before and after, but executed **only one case**. Integrity validation is not 57-case semantic measurement. Its population digest was `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad`; truth-seal digest was `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4`.

### Independent SHA-256 checks

The following were checked with `sha256sum` before and after the sole measurement; every value was unchanged. Full absolute paths are retained in the receipt.

| Artifact | SHA-256, before = after |
| --- | --- |
| Selected scanner [S6] | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| Runner [S7] | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Fixture [S2] | `30e36ffbd9ab99cae544b4fddc68eaf81de474ccdd2babb2bce473a78d15c018` |
| Expected manifest [S1] | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| Original proposal [S8] | `e68a96a050a7c392bb90312e284f3140fb7e5855138fd137341b94786ad910ad` |

## Residual risk and verification gaps

- **No semantic contradiction found for this fixture.** Independent source reasoning and the measured complete result agree; the green comparison alone was not treated as semantics proof.
- This is one straight-line, immediate returned-callable rebound, not proof of all lifetime, late-global, nonlocal, mutable-capture, cross-cell, conditional-return, Thread/Timer, cancellation, or recursion semantics. It does not close all of F3, much less all of F1–F5.
- No no-harm corpus, historical 175-case comparison, C2 audit, resource population, or admission gate was run. There is no claim of saturation or universal agreement. The registration's all-eligible population target and independent non-author admission requirements remain outside this seat. Prior r19/r20/r21 rejected-harmed receipts and the rejection streak remain unchanged.
- The `lsp` device was unavailable: requesting `xd://lsp` returned “No such tool,” so no server status, semantic references/definition result, or diagnostics could be obtained. Literal search was used only to locate relevant source/diff sections, followed by manual caller and definition reasoning. Search results are not represented as semantic proof; no LSP diagnostics clearance is claimed.
- The source-defined canonical path was reviewed and exercised once. No resume route or `resume_continuity_v1` behavior is implicated or assessed by this case.
- Only this assigned report and this seat's raw receipt were written. Production, fixtures, proposals, expectations, registries, and other documentation were not edited. No installs, builds, linters, formatters, full suites, generic smokes, live probes, or fixture execution occurred.

## Evidence source map

All source citations refer to read-only artifacts:

- **[S1]** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json`, lines 1838–1895: exact sealed case, original fields/provenance, one expected row, no alternate/addenda/correction.
- **[S2]** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CaptureReturnedRebound.jsonl`, line 1: complete inert source, language, reset flag, and call identity.
- **[S3]** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md`, lines 85–88 and 158: original F3 mechanism, authoritative prior red, and post-prefix identity requirement.
- **[S4]** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-compound_stmts.rst`, lines 1247–1254 and 1363–1373: local function-object binding, deferred execution, first-class returned functions. Upstream citation supplied by the proposal: https://github.com/python/cpython/blob/v3.14.8/Doc/reference/compound_stmts.rst .
- **[S5]** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-executionmodel.rst`, lines 55–96 and 113–124: binding constructs, local names, nearest-scope resolution. Upstream citation supplied by the proposal: https://github.com/python/cpython/blob/v3.14.8/Doc/reference/executionmodel.rst .
- **[S6]** `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`, line ranges identified above: selected candidate identity resolver, binding replay, reachable-call follower, argv classification, and verdict contract. Relevant delivered diff inspected between the registered base and assigned revision.
- **[S7]** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py`, lines 237–334, 409–443, 467–640, 643–778, and 789–874: proposal/fixture/population identity, capped scan, exact/uncertain evaluation, one-case selection, complete receipt and post-run integrity checks.
- **[S8]** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureReturnedRebound.json`, lines 1–17: original independent truth, source citation, and rationale.

Rendered report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC134.md`.
