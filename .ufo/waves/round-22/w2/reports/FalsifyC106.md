# FalsifyC106 — CX6TimerCancel

## Findings and verdict

**Verdict: agree, limited to this sealed case on the pinned delivered C1 bytes.** No actionable defect was found in this case. This is an author-lane advisory recommendation, not admission, integration authority, desktop clearance, or a claim that C1 is universally correct. The r19/r20/r21 rejected-harmed receipts and streak remain unchanged.

Target: delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`; selected tool `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`, matching the assigned SHA-256 before and after measurement. Relevant delivered changes were inspected against base `741122d177ae8ff68a73768777f20484d5bdcbe4`, limited to scheduled identity, cancellation, invocation, and the preparation/lead-ownership paths affecting this case.

Axes: (1) complete class/command/evidence truth, including false observed and false lead rows; (2) callable and scheduled-instance identity/lifetime; (3) honest exact-versus-uncertain treatment; (4) frozen-input/tool provenance and bounded execution. No source-shaped variant was created.

## Independent expected result

The sealed entry in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json`, `cases[id=CX6TimerCancel]`, retains the original proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CX6TimerCancel.json:1-13` without correction or addendum:

- One inert Python eval cell, `reset=false`.
- `expected_kind="exact"`; complete wanted class/command/evidence multiset **`[]`**.
- `accept_exact_want=null`; `require_signal=false`.
- Explicit observed-only exclusion: `pacman -S r22-cx6-cancel`.
- `forbid_commands_any_tier=[]`. Nevertheless, exact empty multiset equality rejects **every** extra row, including a lead for the cancelled command; the observed-only exclusion does not make such a lead acceptable.
- Required error counters: `eval_unparsed=0` and `unparsed_spawns=0`.

The one-line inert transcript `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CX6TimerCancel.jsonl:1` constructs `t = threading.Timer(0, worker, args=(["pacman", "-S", "r22-cx6-cancel"],))`, then calls `t.cancel()`, then `t.run()`. Merely defining `worker` does not execute its `subprocess.run(argv)` body.

This expected empty result follows independently from the cited frozen standard-library source, not from the green scanner result:

1. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceThread/threading-v3.14.8.py:1370-1376` creates a distinct `finished = Event()` for the Timer and captures its function/arguments.
2. The same source at `:1378-1380` implements cancellation by setting that event. `Event.set()` sets `_flag=True` at `:630-639`; `Event.is_set()` returns that flag at `:615-617`.
3. `Timer.run()` at `:1382-1386` waits, tests `not self.finished.is_set()`, and invokes the function only if the test is true. `Event.wait()` at `:651-671` returns without waiting when the flag is already true; it does not clear the flag.
4. Here cancellation precedes direct synchronous `.run()`, with no `.start()`, second thread, event clearing, subclass override, or opaque mutation. The test is therefore false and `worker` is not called. There is no true process command to preserve and no genuinely unresolved execution requiring a lead/unparsed signal. The command literal is not an execution.

The original r21 F4 authority remains `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:90-95`: an **uncancelled** direct `.run()` was missed. This cancelled negative guard is distinct; passing it does not establish repair of that positive recall case. The historical tool was not rerun.

## Candidate path and identity review

Manual source review supports the measured result:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1840-1853` recognizes the stdlib Timer constructor and creates fresh scheduled state, retaining the resolved worker identity and literal arguments. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1928-1936` stores the assigned binding using a shallow copy; its nested state remains the same object's state.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2193-2200` retains the target and the existing binding objects in each statement snapshot. `:2217-2225` appends statement calls in source order. Thus the cancel and run calls on `t` resolve to the same scheduled-state object; this case has no second instance or name rebinding that could justify routing elsewhere.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1784-1792` maps `.cancel` only on a Timer scheduled binding to `scheduled_cancel`, and maps its `.run` to `scheduled_invoke`. `:2456-2473` processes cancellation first, sets `state["cancelled"]`, then skips the subsequent invocation. The target invocation construction at `:2480-2486` is not reached for this case.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2051-2058` does not eagerly visit a function definition's body. `:2731-2734` leaves Timer constructor target references to the explicit invocation path rather than independently sweeping the worker as a lead. This avoids an invented lead after a definite cancellation.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2280-2293` parses with `PyCF_ONLY_AST`, then prepares and statically scans the AST. The fixture code and its printed command were never executed.

The reviewed diff introduces Timer cancellation state and the cancellation-before-invocation guard; this is not a case-specific command-string suppression. This review establishes only the direct, straight-line path above, not arbitrary scheduling or repeated invocation semantics.

## Authorized measurement and actual rows

Exactly one measurement command was executed:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CX6TimerCancel
```

Raw runner JSON, including child argv/exit/stdout/stderr and integrity facts, is retained at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC106/result.json`. The exact outer invocation, including interpreter `-I`, is recorded at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC106/invocation.json`; the runner's own `sys.argv` representation naturally omits interpreter flags.

| Measurement fact | Actual |
| --- | --- |
| Runner status / exit | `complete` / `0` |
| Executed cases | `1`, filter `CX6TimerCancel` |
| Case result | `pass=true`, `reasons=[]` |
| Complete actual class/command/evidence rows | `[]` |
| Child exit / stderr / scanner error | `0` / empty / `null` |
| Observed / lead findings | `0` / `0` |
| `eval_calls` / `bash_calls` | `1` / `0` |
| `eval_unparsed` / `unparsed_spawns` | `0` / `0` |
| Counts | All five classes `0`; `unpermitted=0` |
| Reported fixture identity | Exact absolute selected path and matching SHA-256 |
| Integrity errors | `[]` |

Child stdout is exactly retained in the receipt: `MADO_TRIPWIRE: clean` followed by the JSON payload. The label alone is not treated as semantic proof: the full empty row multiset, two zero counters, matching fixture identity, no scanner error, and the source reasoning above are the basis of agreement.

The canonical runner logic at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:643-680` runs one scanner child with `RLIMIT_AS=402653184` bytes (384 MiB) and a 15-second timeout. `:803-810` selects exactly one case; `:828-852` records that case's child evidence. `:683-729` checks output shape, path/digest identity, counters, and explicit row markers. `:736-756` applies forbidden-command checks followed by complete multiset equality and zero unparsed for exact cases. The `accept_exact_want`/true-uncertainty branch at `:758-778` is **not** used here.

Before/after full-population integrity verification reported **57 input files, 52 proposal files, and 106 sealed source files verified**. These are integrity checks, **not 57 scanner executions or 57 semantic passes**. Only `1/1` measured cases passed. The child imported the one selected canonical tool path; there was no alternate tool, rerouting, retry, background scanner, old-tool run, or additional probe.

## Identity evidence

Independent `sha256sum` checks before and after measurement agreed for the selected tool, runner, fixture, and normalized expected file. The runner's own before/after integrity records also agreed.

| Artifact | SHA-256 |
| --- | --- |
| C1 tool, before and after | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| Runner, before and after | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Selected fixture, before and after | `517bd9aebeb76a2a38681941f7fac3288c5c7780fe71c0b36d01b113b6985557` |
| Normalized expected, before and after | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| Original proposal | `9593ed60c7920bf8d2088ba38380f82f4142713d1d247e6a0f638a595793bdb2` |
| Cited stdlib source | `5323909624ec2165e70b6d31333e4191b63d383d2dc5a7d7d516a3475ea2b7e3` |
| Original r21 report | `9caedd3d4c521b1a07e4206274e0b3041911caefbf845f85890737e1daef888f` |
| Raw truth seal, runner-verified | `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4` |
| Population, runner-verified | `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad` |

No drift was observed. The normalized expected file explicitly states that it was materialized after the prior raw truth seal and pinned separately; this report does not misrepresent its digest as part of that earlier seal.

## Residual risk and verification gaps

- Scope is one already-sealed, direct `cancel(); run()` negative guard. It cannot establish positive scheduled-target recall, multi-instance isolation, aliases, cross-cell state, event clearing, repeated invocation, conditional cancellation, `.start()` races, subclass overrides, or arbitrary external callback semantics. It grants no family-wide saturation claim and does not replace the historical/no-harm guards.
- The `lsp` device was unavailable: its documentation request returned `No such tool: xd://lsp`. Status, references, definition, and diagnostics therefore could not be requested from a mounted server. Literal search was used only to locate the cited source, with manual reading of definitions/callers and the relevant diff; grep results are not presented as semantic proof.
- No resume path is involved in the selected runner/scanner behavior; no `resume_continuity_v1` claim is made.
- C2, fleet state, admission gates, and non-author closure are outside this seat's scope. No builds, lints, formatters, generic smokes, full-suite/full-oracle execution, fixture execution, new source probe, or installs were performed. All production, source-authority, fixture, expectation, proposal, gate, registry, and shared documentation files remained read-only; writes are confined to this assigned report and its seat-specific receipt directory.

Rendered report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC106.md`

Report: .ufo/waves/round-22/w2/reports/FalsifyC106.md
