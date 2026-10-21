# FalsifyC132 — CaptureReturnedAlias

## Findings by severity and verdict

**No actionable defect found in the assigned case. Verdict: agree**, limited to the sealed `CaptureReturnedAlias` source shape and the fixed C1 tool bytes associated with delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`.

This is an author-lane advisory falsification result, not admission, integration, shipment, host clearance, or independent non-author review. The r19/r20/r21 rejected-harmed receipts and streak remain authoritative. In particular, the original r21 F3 red is not rewritten by this local result and was not rerun with an old tool.

Axes: **semantic precision** (no fabricated or decoy argv at either tier), **recall** (retain the true mutation), **callable identity/lifetime**, **honest uncertainty and error accounting**, and **artifact/resource integrity**. Only the assigned bounded measurement was executed; no new source-shaped probe was created.

## Independent expected semantics

Sources:

- Exact sealed record: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json:1722-1779`.
- Original proposal: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureReturnedAlias.json:1-17`.
- Inert fixture: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CaptureReturnedAlias.jsonl:1`.
- Original source authority: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:85-88,158`. F3 describes choosing a returned function from a def-name index before replaying prefix assignments; the remedy is resolving the returned name against post-prefix bindings.

**[INFERENCE — independent static semantic derivation, not payload execution]** `make` creates separate `worker` and `decoy` function objects. The executed assignment `run = worker` binds a new local name to the existing `worker` object; it neither invokes a function nor chooses `decoy`. `return run` therefore returns `worker`. The immediately enclosing `make()()` calls that returned function once, whose fully literal subprocess argv is `["pacman", "-S", "r22-alias"]`. Defining `decoy` does not execute its body. There is no conditional return, parameter-binding ambiguity, namespace mutation, later rebinding, or asynchronous scheduling in this cell.

Consequently, the complete expected class/command/evidence multiset is exactly:

```json
[{"class":"host_mutation","command":"pacman -S r22-alias","evidence":"observed"}]
```

Both `eval_unparsed` and `unparsed_spawns` must be zero. A clean empty scan would lose the true command; returning only a lead would understate the known call path; a decoy finding, additional lead, or duplicate would be incorrect. The scanner's `observed` marker describes static call-path evidence, not an assertion that a host package command was executed during this review.

The sealed case is `expected_kind: exact`, `accept_exact_want: null`, with forbidden observed command `pacman -Q r22-alias-decoy` and an empty `forbid_commands_any_tier` list. Although the explicit decoy prohibition names only the observed tier, complete exact multiset equality also excludes that decoy at the lead tier, along with every other extra row. No truth/expectation contradiction was found or normalized away.

## Actual measurement and rows

Executed exactly once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CaptureReturnedAlias
```

Raw receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC132/result.json`.

The receipt retains outer argv, exit, exact stdout/stderr and their digests; the embedded runner result also retains the scanner child argv, exit, stdout/stderr, full payload, normalized rows, and before/after integrity records.

| Observation | Actual result |
| --- | --- |
| Runner status / exit | `complete` / `0` |
| Selected case / measured total | `CaptureReturnedAlias` / `1` |
| Comparison | `pass: true`, reasons `[]`, totals `1/1` |
| Scanner child exit | `1` — finding present, not a scan failure |
| Runner / scanner stderr | Both empty |
| Scanner error / integrity errors | `null` / `[]` |
| `eval_calls` / `bash_calls` | `1` / `0` |
| `eval_unparsed` / `unparsed_spawns` | `0` / `0` |
| Observed / lead findings | `1` / `0` |
| Other class counts | `live_probe`, `package_query`, `tool_install`, `vcs_write`: all `0` |

Complete actual row multiset:

```json
[{"class":"host_mutation","command":"pacman -S r22-alias","evidence":"observed"}]
```

The full finding has `argv0: pacman`, `rule: pacman:-S`, `tool: eval`, `tool_call_id: CaptureReturnedAlias-0`, fixture line `1`, and the exact selected absolute fixture path. No decoy command was reported at any tier. The true command was neither lost nor downgraded.

## Actual diff and affected call path

Reviewed the read-only diff of `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` between registered base `741122d177ae8ff68a73768777f20484d5bdcbe4` and delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, then the relevant candidate definitions/callers. The case-specific explanation is not inferred from the green flag alone:

1. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1642-1684`: the added `factory_result` binds the factory call, selects the first direct return, replays the statements before it, and only then resolves `returned.value` in the updated local bindings (`1674-1675`). The selected helper's local overlays are retained. This replaces the original F3 def-only identity choice for this shape.
2. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1882-1891,1928-1937,1828-1831,2203-2254`: prefix replay registers both function identities, and the simple name assignment copies the binding for `worker` into `run`. `prepare_eval_calls` applies those binding updates in statement order. It does not select a function merely because its def name exists.
3. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1748-1756,1757-1783,2461-2466,2510-2516,2547-2580`: the immediate returned-call path resolves `make()` through `factory_result`, obtains the returned helper, overlays its lexical bindings, and follows that helper. The explicit uncertain/invalid branches are present but are not needed by this valid zero-argument straight-line case.
4. `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1993-2001,2051-2058,2407-2439,2675-2684`: eager traversal skips deferred function bodies, and `follow_helper` scans the chosen body with its bound environment. The literal argv is classified on the reached subprocess path. Thus merely defining `decoy` does not justify an observation or a lead for its command.

These are static source checks plus the one captured scanner result, not LSP semantic proofs. `xd://lsp` was requested first and returned **No such tool**; no LSP device/server was available for status, references, definition, or diagnostics. Location searches used literal fallback only.

## Canonical runner, exactness, and uncertainty boundaries

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:643-661` gives the scanner child a **384 MiB** address-space limit and **15-second** timeout. One selected case yielded one child, using the runner's canonical isolated Python wrapper and the selected tool path. There was no alternate scanner/runtime, rerouting, second scanner run, full-corpus execution, or old-tool execution.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:683-729` checks the scanner's explicit input identity and error counters before constructing rows. Actual path and SHA-256 match the frozen fixture.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:732-756` compares sorted triples, preserving multiplicity, and requires zero unparsed counters for exact cases. The sealed `require_signal: true` does not force a lead on this exact branch.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:740-778` enforces any-tier forbidden commands before either exact or uncertainty acceptance. In an uncertain case, `accept_exact_want` allows only its complete exact alternative with zero unparsed counters; otherwise an observed row is rejected and any required genuine uncertainty signal must be a lead or positive unparsed counter. **Those uncertain-case branches were read, not exercised here.** This fixture neither needs that alternative nor warrants parsed-clean ambiguity.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:789-870` validates the population before selecting the unique case, scans only that selection, and revalidates afterward. The result verified digests for **57 inputs**, **52 proposal files**, and **106 sealed source files**; it measured **one case**, not 57. No saturation or universal-semantics claim follows from `1/1`.

## Identity and provenance

External `sha256sum` checks before and after measurement matched; runner integrity-before and integrity-after also matched with no errors.

| Artifact | SHA-256 |
| --- | --- |
| C1 tool, before and after | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| Assigned fixture, before and after | `ecdced4cbc3efa54ae0b4cc11a59bf2043f932ec2e45909b922352bb74324591` |
| Runner, before and after | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Normalized expected, before and after | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| Original proposal, read/prechecked and runner-revalidated | `b054896cb9705845e1371c733dc00086fc028a7f10ded25a235167250d507048` |
| Raw truth seal, runner-verified | `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4` |
| Captured runner stdout | `0498e29ede86c527708fd13028e71be570ddf42e24188df33d5a163d8845bda1` |
| Empty runner stderr | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

The expected metadata explicitly says normalized expected was materialized from an earlier raw truth seal, with its own separately pinned digest; normalized expected was **not** itself part of that raw seal. This report does not backdate it or substitute normalized output for original source authority.

## Residual risk and verification gaps

- This case supports only the finite direct returned-alias repair: a newly introduced local alias of a visible nested function, then an immediate invocation. It does not test cross-cell lifetime, multiple factory instances, mutable captures, nonlocal mutation, dynamic bindings, conditional/non-Name returns, scheduled targets, or F5 namespace hygiene. Those remain outside this seat's measured evidence, irrespective of neighboring code or aggregate receipts.
- Static source agreement does not demonstrate actual host execution, package availability, safety, full Python semantics, whole-corpus no-harm, independent C2 arithmetic capability, or non-author admission. No claim is made on those axes.
- No additional scanner probes, fixture execution, builds, linters, formatters, suites, generic smokes, live probes, package queries, installs, background jobs, delegation, or code/fixture/expected edits were performed. Writes are confined to this assigned report and its raw receipt.

Rendered report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC132.md`
