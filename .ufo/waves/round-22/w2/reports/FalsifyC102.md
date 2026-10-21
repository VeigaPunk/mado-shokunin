# FalsifyC102 — CX1AnyTierLeak

## Verdict and findings, by severity

**Recommendation: AGREE with the sealed uncertain-case expectation for this case on the delivered C1 identity.** No actionable semantic defect was found in the assigned case. The single authorized measurement passed **1/1 executed case**, with actual finding rows **`[]`** and **`unparsed_spawns = 1`**. This is explicit uncertainty, not an exact clean result, proof of host safety, or an admission grant.

**Informational — the displayed `clean` label is not parsed-clean.** The child printed `MADO_TRIPWIRE: clean` and exited 0, while retaining one unresolved spawn in its JSON file row. The canonical label logic considers findings, not unresolved-spawn counters: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2909-2914`; `run_scan` preserves the file counters in its emitted payload at lines 2922-2940. The documented meaning at lines 30-36 explicitly excludes a claim that no host command ran. Consequently this receipt must not be summarized as a zero-error exact result. The uncertainty is visible and satisfies this case's contract; it is not a newly demonstrated classifier defect.

## Axes and scope

Axes: **lexical-binding/returned-callable correctness; argv and evidence-tier honesty; uncertainty retention versus false clean; frozen artifact identity and provenance; bounded execution and scope honesty.**

Target revision: `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. I reviewed the relevant actual C1 diff from registered base `741122d177ae8ff68a73768777f20484d5bdcbe4` to that revision, including replacement of invocation-time `capture_owner`/`capture_call` replay with creation-time `factory_result` closure overlays. Current selected tool bytes matched the fixed delivered identity both before and after the measurement. This review concerns only CX1AnyTierLeak and its reachable binding/call path; it does not establish the complete C1 target, C2, no-harm corpus results, resource scaling, scheduled-call correctness, or any recovery/admission decision.

## Independent semantic expectation

Authority read:

- Exact case CX1AnyTierLeak in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json`.
- Original proposal `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CX1AnyTierLeak.json:2-18` and original CX1 attack in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/notes/CriticScope.json:93-103`.
- Original r21 F2 red and mechanism, `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:55-60,78-83`. This historical red was read, not rerun with an old tool.
- Retained Python reference `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-executionmodel.rst:90-115,322`: free-variable binding resolves through the nearest enclosing scope, at runtime.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/supported-forms.md:13-22` and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/guard-clarifications.md:5-12`.

Static reasoning, without executing payload source: `parts = os.environ.get(..., "").split()` binds a runtime-dependent list. `make(parts)` is a valid ordinary positional call, not a definitely missing/invalid argument call. Its local parameter `argv` denotes that list. The returned nested `run` closes over the factory's `argv`, not the same-named module literal. Calling `runner()` therefore reaches a known subprocess callable with an unknown argument list. The module's `['pacman', '-Q', 'r22-cx1-global']` supplies no evidence about that list.

Thus there is **no statically justified concrete class/command/evidence row**. Depending on the environment, the subprocess call may attempt a command or fail on an empty/invalid command list; the scanner cannot certify either a concrete execution or no execution. An explicit uncertainty signal is required. Even if an environment happened to contain the decoy command, that coincidence is not source evidence permitting the scanner to borrow its value from the module global.

The sealed case therefore correctly states:

- `expected_kind = uncertain`, `want = []`, `require_signal = true`.
- `accept_exact_want = null`: no alternate exact result is authorized. Empty `want` is **not** an exact-empty/zero-unparsed expectation.
- Both `pacman -Q r22-cx1-global` (**package_query**) and `pacman -S r22-cx1-global` (**host_mutation**) are forbidden at **every evidence tier**, as well as specifically forbidden as observed. Downgrading a borrowed command to lead would still fail.

## Actual rows and bounded measurement

Only this measurement command was executed; no additional scanner invocation or new source-shaped probe was used:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CX1AnyTierLeak
```

| Receipt fact | Actual value |
|---|---|
| Outer measurement exit/status | `0` / `complete` |
| Executed case count | `1`, CX1AnyTierLeak |
| Child scanner exit | `0` |
| Complete actual finding row multiset | `[]` |
| Observed / lead finding totals | `0 / 0` |
| All five class counts / unpermitted | `0 / 0` |
| `eval_calls` / `eval_unparsed` | `1 / 0` |
| `unparsed_spawns` / combined unparsed | `1 / 1` |
| Child stderr / outer stderr | empty / empty |
| Scanner error / comparison reasons / integrity errors | `null` / `[]` / `[]` |
| Comparison result | `pass: true`, totals `1/1` |

The receipt retains the exact launch argv, outer exit/stdout/stderr, runner output, child argv/exit/stdout/stderr/payload, and artifact hashes at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC102/result.json`. The outer capture separately retains `-I`; the runner's reconstructed display argv omits that interpreter flag, while the actual nested scanner argv includes it.

The runner defines a **384 MiB (402653184-byte) address-space cap and 15-second timeout**, applies RLIMIT_AS in the scanner child, captures its streams, and runs the selected case only: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:26-27,643-680,803-810,828-851`. It loads the selected scanner's `main(["--scan", fixture])` through its fixed isolated child wrapper; it does not execute fixture Python. No alternative classifier identity or runtime was substituted.

Integrity before and after validated **57 input files, 52 proposal files, and 106 sealed source files**. These are artifact-validation counts, **not 57 scanner executions or 57 semantic passes**. Full-population validation and proposal/fixture correspondence are implemented at runner lines 467-542; exact-case selection and the one selected scan are at lines 803-839.

## Relevant changed-path reasoning and attempted falsification

The green comparison is corroboration, not the semantic argument:

1. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1345-1404,2089-2116` keeps non-literal `parts` unresolved and binds ordinary positional `argv` to `LITERAL_MISS`, rather than treating a valid unknown-valued argument as an invalid call.
2. `factory_result` at lines 1642-1684 overlays the factory parameter into the local literal and callable environments before resolving `return run`; it retains that local entry in `closure_env`/`closure_bindings`. `bound_callables` at lines 1608-1626 retains an unresolved parameter marker rather than a same-named module callable/value.
3. `callable_info` resolves the returned binding and routes factory calls through that result at lines 1748-1783. On `runner()`, the closure overlay is applied before following the helper at lines 2510-2516 and 2547-2580. The no-argument inner helper does not replace the captured unknown with a module literal; see `follow_helper`, lines 2407-2437.
4. The subprocess argument stays unresolved through literal resolution, then reaches the unresolved-spawn increment at lines 2632-2684. Actual `findings=[]` and `unparsed_spawns=1` match that reasoning.

| Attack dimension | Result for this exact case |
|---|---|
| False observed command | No observed rows; no borrowed Q/S command. |
| False lead argv | No lead rows; any-tier prohibition is satisfied, not merely downgraded. |
| Lost true command | No fixed command is statically available to retain; the unresolved reachable spawn remains explicitly counted. This does not prove no runtime command. |
| Wrong returned identity | Straight-line `return run` retains the visible nested helper; there is no competing rebound return or conditional target in this input. |
| Lifetime | Unknown factory-local `argv` remains in the closure overlay at invocation; module `argv` cannot fill its place. No mutable alias/rebinding variant was added or run. |
| Conditional/scheduled target | Neither exists in this case; no conditional-return, Thread, Timer, cancellation, or scheduling claim is tested. |
| Parsed-clean ambiguity | The label/exit alone look clean, but the retained unresolved-spawn counter explicitly prevents an exact parsed-clean interpretation. |

The oracle itself checks forbidden commands at all tiers before considering alternatives; exact cases compare the **complete sorted class/command/evidence multiset plus zero unparsed**, not subset containment. Uncertain cases reject observed rows outside a complete permitted exact alternate and require a lead or positive unparsed signal when specified: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:732-778`. Here the sole signal is the positive unresolved-spawn counter, with no exact alternate.

## Identity evidence

Each of the first four hashes below was independently checked with `sha256sum` before and after the one measurement and did not drift. The runner also reported matching before/after identity records.

| Artifact | SHA-256 |
|---|---|
| Selected C1 tool | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| Measurement runner | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Assigned fixture | `2b04b1a8af1153de492cadfb095fa9a65729bdac06d7bf02c6d3b84188e60f9b` |
| Normalized expected manifest | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| Original proposal | `10f4d4e61577f5b2120105112fa455c4a00830f40b2f033facc998b51e22456c` |
| Retained execution-model reference | `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89` |

The runner retained truth-seal SHA-256 `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4` and population SHA-256 `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad`. This validates the current materialized expected manifest against retained raw proposal/source bytes; it does not pretend that normalized expected bytes existed at the earlier raw-truth seal commit.

## Residual risk and verification gaps

- `xd://lsp` was unavailable: documentation discovery returned **“No such tool: xd://lsp”**. No LSP server/status, references, definition, or diagnostics operation could be obtained. Targeted literal searches and source/diff reads were used as the permitted fallback; their results are not presented as semantic-server proof. No replacement diagnostics/build/lint/smoke execution was performed.
- Environment-derived argv remains genuinely unknown. The classifier pass does not establish the actual command, its class, process success, or safety. Consumers must inspect file uncertainty counters rather than use `clean`/exit 0 alone.
- Only this finite bound-nonliteral-positional closure form was measured. Full-suite, historical 175-case, 1356-fixture no-harm, closure-heavy resource, C2 evidence-audit, and other supported-form results remain outside this seat's verification. No saturation or universal F2-repair claim follows.
- Prior r19/r20/r21 **rejected-harmed** receipts and streak remain authoritative. This author-lane advisory result supplies no non-author admission, closure, rerouting, integration, or next-round authority; L1 retains planner/integration authority.
- Production, fixtures, expected data, registries, and documentation were left read-only. Only this assigned report and its receipt were created. No installs, background jobs, delegation, payload execution, host/live probes, or mutation tests were used.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC102.md
