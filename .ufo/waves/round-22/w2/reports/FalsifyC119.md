# FalsifyC119 — C1 `CaptureGlobalLate`

## Verdict and findings, by severity

**Agree, narrowly scoped. No actionable defect found in this sealed case on the fixed delivered scanner.** The independent semantic expectation and the actual complete finding multiset agree: exactly one `host_mutation` / `pacman -S r22-globallate` / `observed` row, with zero uncertainty/error counters. No early-value row, extra lead, wrong callable, or missing late command appeared.

This is author-lane falsification advice on delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, not non-author admission, integration approval, or a safety clearance. Prior r19/r20/r21 rejected-harmed receipts and their streak remain authoritative.

## Axes

1. Complete class/command/evidence fidelity, including extra rows and duplicates.
2. Callable identity and factory-time versus invocation-time name lifetime.
3. Honest evidence tiers and uncertainty, rather than parsed-clean inference.
4. Sealed-byte integrity and one bounded reproducible scanner child.
5. Scope honesty and read-only discipline.

## Independent semantic assessment

The authority read was the original proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureGlobalLate.json:2-18`, preserved in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json:969-1026`. Its exact inert input is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CaptureGlobalLate.jsonl:1`.

**[INFERENCE — Python lexical-scope and execution-order reasoning, not payload execution]:**

- `CMD` initially names `['pacman', '-Q', 'r22-early']` at module scope. Neither `make_runner` nor its nested `runner` has a `CMD` parameter or local assignment. Thus `CMD` in the nested body is a module-global lookup, not a captured factory-argument cell.
- `make_runner()` creates and returns the visible nested `runner`; creating/returning that function does not call `subprocess.run`.
- The later module assignment replaces `CMD` with `['pacman', '-S', 'r22-globallate']` before the single `runner()` invocation. Rebinding the module name must affect this free-global lookup; no factory-time snapshot of `CMD` is semantically justified.
- The invocation therefore passes exactly `['pacman', '-S', 'r22-globallate']` to the unmodified, visibly imported `subprocess.run`. The bounded static-source classification is one observed host mutation. There is no conditional target, unresolved operand, invalid argument binding, concurrent schedule, or additional spawn in this source.

The complete semantic multiset is:

```json
[{"class":"host_mutation","command":"pacman -S r22-globallate","evidence":"observed"}]
```

The early query is never passed to a spawn, so it must not be invented as either observed or lead. Although this proposal's explicit `forbid_commands_any_tier` list is empty and its observed blacklist names the early query, **complete exact multiset equality also rejects any extra early-query lead**. `expected_kind` is `exact`; `accept_exact_want` is null. The uncertain-case allowance is not applicable, and neither a lead-only result nor an empty zero-counter result would satisfy this case. `require_signal: true` does not relax the exact branch.

Historical contrast remains `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:70-83`: F1 binds an actual factory argument too late; F2 borrows a same-named module global for an unresolved lexical parameter. This case instead guards the symmetric over-repair: freezing a genuinely global name too early. The preimplementation design note's lifetime map at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/notes/SimplifyCapture.json:17-46` was read as historical design evidence, not as a substitute for the original truth or as an instruction to edit anything. No old detector was rerun.

## Actual diff and relevant candidate path

Read the recovery delta from registered base `741122d177ae8ff68a73768777f20484d5bdcbe4` to delivered `71228fd582d6d9338d7916cc64e69bd4c2e928b5` for `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`, restricting substantive review to this case's binding/snapshot/follow path. The relevant cutover replaces deferred `capture_owner`/`capture_call` replay with creation-time `factory_result` and explicit closure overlays, and replaces whole-map statement snapshots with reachable-name snapshots.

The candidate's concrete path is consistent with the semantic expectation:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1642-1684`: `factory_result` binds factory arguments and replays the pre-return prefix, then selects the actual returned binding. Only parameters, inherited closure bindings, and prefix-bound names enter the closure overlay. Here the prefix defines `runner`, but does not locally bind `CMD`, so the early global `CMD` is not frozen into that overlay.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1859-1861,1882-1885,1928-1936`: the assigned factory result retains the resolved helper identity rather than reselecting a def by name at invocation.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2163-2200,2217-2225,2243-2253`: statement snapshots traverse visible callable bodies, retaining the reachable global `CMD`; module literal assignments advance in source order. The final invocation snapshot therefore contains the late list.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2456-2461,2510-2516,2547-2579`: invocation uses that statement's environment plus only the explicit closure overlay; `CMD` is not overwritten by the factory environment.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2407-2439,2623-2643,2675-2684`: the zero-argument synchronous helper is followed, its literal argv is classified, and no unresolved/fallback branch is required. Deferred-body handling and lead fallback were also read at `1993-2001,2051-2063,2358-2385,2685-2751` of that same absolute source path.

These are source-level explanations, not a claim of exhaustive semantic caller coverage. `xd://lsp` is unavailable: the device read returned `No such tool: xd://lsp`. Consequently references, definition, diagnostics, and an indexing-status retry could not be obtained. Literal search was used for navigation only, never presented as semantic proof.

## Sole authorized measurement and actual rows

Executed exactly once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CaptureGlobalLate
```

The one canonical scanner child used `/usr/bin/python3 -I -c` with the runner's fixed import wrapper, the selected absolute detector path, and only the selected absolute fixture path. No alternative detector/runtime or extra source-shaped probe was invoked. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:643-680` enforces `RLIMIT_AS = 402653184` bytes and a 15-second child timeout. The fixture code was parsed as inert scanner input, never executed.

| Item | Actual result |
|---|---|
| Measurement exit / status | `0` / `complete` |
| Selected cases measured | `1`, `CaptureGlobalLate` only |
| Complete actual row | `host_mutation`, `pacman -S r22-globallate`, `observed` |
| Finding identity | selected fixture, JSONL line `1`, tool `eval`, call ID `CaptureGlobalLate-0` |
| Finding rule / argv0 | `pacman:-S` / `pacman` |
| Observed / lead findings | `1` / `0` |
| All other class counts | `0` |
| Scanner exit / label | `1` / `MADO_TRIPWIRE: findings` |
| `eval_calls` / `bash_calls` | `1` / `0` |
| `eval_unparsed` / `unparsed_spawns` | `0` / `0` |
| Parser errors / scanner error | none / null |
| Scanner stderr / measurement stderr | empty / empty |
| Comparison | pass `1/1`, no reasons |
| Integrity errors | empty |

Scanner exit `1` is the expected finding-bearing result, not a scanner failure. The evidence marker `observed` denotes a statically followed source call, not a package command actually executed during review.

The runner's exact-result rule is the canonical logic at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:683-756`: explicit finding markers, selected file path and digest, nonnegative counters, then sorted complete class/command/evidence multiset equality **and zero unparsed counters**. The any-tier blacklist is checked first (`740-748`), before either exact or uncertain acceptance; `accept_exact_want` and genuinely uncertain outcomes remain distinct at `758-778`. Full-population integrity validation (`467-640`, invoked before and after at `798-824,854-869`) checked 106 sealed source files, 52 proposal files, and 57 inputs; it did **not** execute 57 scanner cases. Both integrity snapshots agree.

Raw outer argv/exit/stdout/stderr, the complete inner argv/exit/stdout/stderr and payload, and all hashes are retained at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC119/result.json`. The outer recorded argv explicitly retains `-I`; the runner's self-reported `sys.argv` naturally omits interpreter flags.

## Identity observations

All five SHA-256 values below were observed before and after the sole measurement and were unchanged. The selected detector matches the fixed assignment identity; the expected manifest matches its fixed identity. Runner integrity independently confirmed the detector and runner before/after, and the scanner-reported fixture path/digest matches the selected fixture.

| Absolute artifact | SHA-256, before = after |
|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py` | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CaptureGlobalLate.jsonl` | `cc8b1e4efa6148f78d7e361dd6c084f82cc12cd030afec91397150b0309e6f4c` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureGlobalLate.json` | `11271248c056ee182146b849443e9a36f12093890426f8812a5a86563119fd4c` |

## Residual risk and verification gaps

- Agreement closes only this straight-line, same-cell, unshadowed-global lifetime contrast at these bytes. It does not establish all F1/F2 repairs, same-name shadowing variants, cross-cell/reset behavior, mutable closure cells, conditional returns, scheduled targets, or whole-corpus no-harm. No saturation or complete-Python-semantics claim is made.
- No resume path is present in this assigned source shape; `resume_continuity_v1` is not exercised or asserted.
- The green comparison is evidence of this exact multiset agreement, not proof that a parsed-clean scan means safe. Here independent source reasoning positively identifies the one spawn and explains why the early value and extra leads are wrong.
- LSP semantic references/definitions/diagnostics remain unavailable as recorded above. No language-server diagnostics, builds, lints, formatters, generic smokes, full suite, corpus scan, C2 audit run, mutation test, or old-tool rerun was performed. No proposed mutant is claimed killed.
- Raw preimplementation truth and the later normalized expected artifact were not conflated or modified. No truth/expectation contradiction was found for this case. Nothing here changes the original prior-red authority or grants admission.
- Only this assigned report and its unique receipt were written. Production, fixtures, expectations, tools, proposals, gates, registries, and shared configuration were left read-only. No delegation, background job, installation, update, live probe, package query, or payload execution occurred.

Report: [.ufo/waves/round-22/w2/reports/FalsifyC119.md](/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC119.md)
