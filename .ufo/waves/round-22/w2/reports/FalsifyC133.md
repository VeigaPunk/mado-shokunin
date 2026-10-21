# FalsifyC133 — CaptureReturnedChain

**Verdict: agree, for this exact sealed case on the assigned delivered scanner bytes.** Author-lane advisory only; this is not an admission or a claim that C1, the historical guards, or the rejection streak is closed.

## Findings by severity

No actionable defect found within `CaptureReturnedChain`. The complete returned row multiset agrees with independent source semantics, not merely with the runner's green comparison. No alpha command occurs at either evidence tier; the true beta command is retained exactly once as observed. There are no parse/unparsed errors in this measurement.

## Axes

- Exact class/command/evidence multiset, including multiplicity and zero error counters.
- Returned callable identity, statement-order rebinding, and callable lifetime.
- Honest observed/lead/uncertainty boundaries without invented argv.
- Fixed tool/fixture/runner identity, one bounded scanner child, and accurately scoped evidence.

## Independent semantic derivation

The original proposal is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureReturnedChain.json:4-18`; the inert transcript is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CaptureReturnedChain.jsonl:1`. Its single Python eval cell defines `make`, then evaluates `make()()`.

1. Calling `make()` creates function objects A (`alpha`) and B (`beta`). Defining either does not execute its subprocess body.
2. `relay = alpha` binds relay to A; `relay = beta` replaces that binding with B; `chosen = relay` binds chosen to B. These names refer to objects, not to symbolic alias chains that should be re-resolved from a def-name index.
3. `return chosen` returns B. The second call in `make()()` invokes B once; the returned function remains alive for that call after the factory returns. B reads the unchanged module import `subprocess` and reaches the literal argv `["pacman", "-S", "r22-chain-beta"]`. Alpha is never invoked.
4. The bounded classifier contract therefore requires exactly one `host_mutation` / `pacman -S r22-chain-beta` / `observed` row, no other rows, and zero error counters. `observed` here denotes statically followed transcript source, not an actual package transaction performed by this review.

Authority: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-executionmodel.rst:55-66,89-96,113-115` states object-based binding and nearest-enclosing resolution; `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-simple_stmts.rst:143-156,494-497` establishes local assignment/rebinding and the evaluated return value.

This is the chained-alias sibling of the original F3 defect recorded at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:85-88` and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/returned-rebound.jsonl:1`. That historical red remains source authority; neither the original fixture nor an old scanner was executed here. The original proposal digest matches its sealed record; the later normalized expected artifact is a comparison artifact, not replacement semantic authority.

### Exact versus uncertainty boundary

The sealed case is `expected_kind: exact`, `accept_exact_want: null`, with no correction or addenda. There are no dynamic arguments, mutable captured objects, subsequent nonlocal mutation, conditional returns/targets, recursive returns, external callbacks, or scheduled invocations in this source. No uncertainty relaxation is warranted. A lead-only beta result, an alpha lead, an extra row, or an empty parsed-clean result would all fail the complete multiset contract. Although the explicit alpha prohibition names observed evidence only, full exact equality also excludes alpha at every other tier. The stored `require_signal: true` does not transform this exact case into an uncertainty case: the runner returns from its exact branch before the uncertain-case signal rule.

## Relevant delivered change and call path

Read the actual diff from base `741122d177ae8ff68a73768777f20484d5bdcbe4` to delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, limited to `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`, and the relevant live definitions. The old selection from a nested-def-name dictionary is removed. The current path is:

- `callable_info` dispatches a helper-valued factory call through `factory_result` at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1757-1783`.
- `factory_result` replays the prefix before the first visible return, then resolves the return expression against the resulting local bindings, at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1642-1684`. Thus `chosen`, not a def-adjacent name lookup, selects B.
- Ordered replay is `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2203-2254`; helper definitions and successive assignments update the map at `1882-1891,1928-1937`. Name assignments copy the current callable descriptor at `1828-1834`, so relay's rebinding and the final chosen binding preserve B's identity.
- The selected helper metadata is overlaid and followed at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2510-2516,2547-2580`; `follow_helper` binds the call and scans its body at `2407-2439`. This is consistent with exactly the returned beta body being classified for this case.

## Authorized single measurement

Executed once, with no additional scanner runs or new source-shaped probes:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CaptureReturnedChain
```

The runner's canonical child uses `/usr/bin/python3 -I -c` to import this same selected scanner and call `main(["--scan", selected_fixture])`; it does not invoke a substitute implementation. The child address-space cap is 402653184 bytes (384 MiB), with a 15-second timeout, implemented at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:26-27,643-660`. Case selection happens only after population validation at `789-837`. Exactly one scanner child scanned exactly one case; 57 input files were integrity-validated, not 57 scanner cases run.

| Actual class | Actual command | Actual evidence | Multiplicity |
|---|---|---|---:|
| host_mutation | pacman -S r22-chain-beta | observed | 1 |

Runner: exit **0**, status `complete`, totals **1/1**, reasons `[]`, integrity errors `[]`, stderr empty. Scanner: exit **1**, correctly meaning one unpermitted finding, not a runner/evaluation failure; `observed_findings=1`, `lead_findings=0`, `eval_unparsed=0`, `unparsed_spawns=0`, scanner error null, stderr empty. The finding identifies the exact sealed fixture, line 1, tool `eval`, call ID `CaptureReturnedChain-0`, rule `pacman:-S`, and argv0 `pacman`.

The canonical comparison and error handling are `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:683-729,732-778`: strict scanner output parsing, matching input identity, complete sorted class/command/evidence multiset, and zero unparsed counters. Unknown cases check forbidden commands at all tiers before considering `accept_exact_want` or genuine uncertainty. This case does not use that acceptance escape hatch.

### Identity evidence

External `sha256sum` before and after the measurement matched for every entry below; the runner independently retained matching before/after integrity records. No drift was observed.

| Artifact | SHA-256 before = after |
|---|---|
| Selected scanner | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| CaptureReturnedChain fixture | `efea216e17cac1b354b58a409776aec1d76a2b189c52e5f11b7300840910651e` |
| Measurement runner | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Oracle expected artifact | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |

Original proposal: `fc0ebdbf66bf363aa8e67d4bc56ce831662daa1f13896b7057a5c873228fc3a2`, matching the sealed case. Full outer and child argv/exit/stdout/stderr, parsed scanner rows, and integrity records are retained at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC133/result.json`.

## Residual risk and verification gaps

- This supports only this straight-line, immediate returned-chain form on the pinned current target. It does not establish all closure lifetimes, arbitrary conditional/recursive returns, scheduled targets, broader no-harm, C2, resource scaling/saturation, or admission. No resume path exists in this case; no `resume_continuity_v1` claim is made.
- LSP was unavailable: `read xd://lsp` returned `No such tool: xd://lsp`. Status, references, definitions, and diagnostics therefore could not be obtained. Text fallback located relevant definitions/callers; it is not presented as semantic proof. The semantic argument rests on the exact source and cited language rules.
- No fixture Python or printed command was executed. No production, fixture, expected, historical receipt, registry, or documentation file was edited. Only this assigned report and receipt were written. No installs/updates, background jobs, full suites, builds, linters, formatters, generic smokes, live probes, or extra scanner measurements were performed.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC133.md
