# C1 CaptureLocalReassign — fresh delivered-byte falsification

**Verdict: agree, scoped to this exact sealed case.** No actionable defect was found in its complete class/command/evidence result. This is author-lane advisory evidence, not non-author admission, integration approval, host clearance, or a change to the prior r19/r20/r21 rejected-harmed receipts or streak. Target: delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, measured through the assigned C1 tool bytes.

## Findings, by severity

None in the assigned case. The scanner neither invents the initial query command nor loses or downgrades the true rebound command. The verdict rests on independent source-semantics reasoning plus the retained complete output, not on the runner's green label alone.

## Axes

1. Exact command and mutation-class truth.
2. Lexical lifetime and returned-callable identity.
3. Honest evidence tier, complete row multiset, and explicit error/uncertainty accounting.
4. Pinned artifact identity and the single-case/resource boundary.

## Independent semantic expectation

The original proposal is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureLocalReassign.json`, lines 2–18. The selected inert transcript is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CaptureLocalReassign.jsonl`, line 1. The sealed entry is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json`, JSON pointer `/cases/22`; it is exact, has no correction or addendum, and has `accept_exact_want: null`.

Reasoning about the fixture, without executing its payload:

- Calling `make` initially binds its parameter `cmd` to the literal initial query list. Defining nested `run` does not execute its body.
- `run` refers to the enclosing function's `cmd`. The assignment inside `make` rebinds that same enclosing binding to `["pacman", "-S", "r22-local-rebound"]` before returning `run`.
- The returned name is not conditionally selected or rebound. `runner` is this specific nested function, and the subsequent unconditional `runner()` call reads the rebound binding. There is one reachable subprocess invocation, with exactly that three-string argv.
- The initial `pacman -Q r22-local-initial` list is never passed to a subprocess. It is not justified as observed or as a separate lead. There is no dynamic expansion, missing argument, opaque mutation, conditional target, external callback, or scheduling ambiguity in this case.

The language-reference authority is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-executionmodel.rst`: lines 89–115 establish local/free-variable and nearest-enclosing-scope resolution; lines 322–329 explicitly state runtime free-variable resolution. The independent expected multiset is therefore exactly:

| Class | Command | Evidence | Multiplicity |
|---|---|---|---:|
| `host_mutation` | `pacman -S r22-local-rebound` | `observed` | 1 |

Both unparsed counters must be zero. Here `observed` is the scanner's statically followed-source evidence tier, not a claim that this reviewer ran pacman or witnessed a host mutation.

## Sole authorized measurement and actual rows

Executed once, with the exact requested outer argv:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CaptureLocalReassign
```

Receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC123/result.json`. It retains outer and scanner argv, exits, complete stdout/stderr, parsed measurement, and before/after artifact hashes. There was no second scanner run or new source-shaped probe.

- Outer process exit **0**; runner status `complete`; totals **1 pass / 1 executed case**; integrity errors `[]`.
- Scanner child exit **1**, correctly meaning one unpermitted finding, not evaluation failure. Outer and scanner stderr are both empty; `scanner_error` is null and reasons are `[]`.
- Actual complete row multiset: **one `host_mutation` / `pacman -S r22-local-rebound` / `observed`**, exactly as above. Counts: observed 1, lead 0, host_mutation 1; package_query, live_probe, tool_install and vcs_write all 0.
- Raw finding identity: selected fixture path, line 1, tool `eval`, tool-call id `CaptureLocalReassign-0`, argv0 `pacman`, rule `pacman:-S`.
- Exactly one file and one eval call; `eval_unparsed: 0`, `unparsed_spawns: 0`, aggregate unparsed 0. No initial query command occurs at either evidence tier.
- Runner integrity checks verified **57 input fixtures, 52 proposal files and 106 sealed source files** before and after. Those are artifact-validation counts, **not 57 scanner executions** or a full-population semantic pass.
- Scanner child resource enforcement is the canonical runner's `RLIMIT_AS = 402653184` bytes and 15-second subprocess timeout, at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:26-27,643-661`. Its selected-case loop is at lines 803–810 and 828–852. Only one child was selected. Measured outer elapsed time was approximately 0.109 seconds; this is not a scaling or saturation claim.

## Identity and truth timing

All listed artifacts had identical hashes immediately before and after the sole measurement; receipt `hash_drift` is `[]`.

| Artifact | SHA-256 before = after |
|---|---|
| C1 tool | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| Selected fixture | `b6eaef64acea9ec8fcf5259298136a7b85de137fb3c1726a96063944c91a99a6` |
| Measurement runner | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Normalized expected | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| Original proposal | `744cadda3aa69ee9eed2532f2d448cb9f5834fda72a57ca5bb19b4ae1b360032` |
| Cited language reference | `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89` |

Tool and expected hashes match the assignment's fixed identities. The runner's before/after tool hashes also match independently retained hashes. The measured identity is the assigned tool's bytes; no broader working-tree cleanliness claim is made.

The prior raw truth seal, identified by the assignment as landed at `9185f1f9` before implementation, remains distinct from the later normalized expected artifact. The expected file explicitly says its normalized digest was **not** part of the raw seal. The measurement verified raw seal digest `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4` and population digest `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad`. No later normalization is represented here as pre-implementation sealing, and no expectation was changed.

## Relevant changed behavior and canonical comparison

Reviewed the relevant C1 diff from registered base `741122d177ae8ff68a73768777f20484d5bdcbe4` to the delivered target. The delivered revision's immediate-parent diff for this tool is empty; the base-to-delivered comparison contains the lifetime repair. Relevant source trace:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1839-1861,1928-1936`: assignment resolution stores the resolved factory result under `runner` rather than deferring its argument interpretation until a later call.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1642-1683`: `factory_result` binds factory arguments, replays the pre-return prefix in the local environment, resolves the returned callable against the post-prefix bindings, and records the resulting lexical overlays. For this fixture that overlay contains the rebound `cmd`, not its initial value.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2203-2254,2510-2516,2547-2580`: statement snapshots and closure overlays carry this resolved identity/environment into the actual helper invocation. The helper-follow path at lines 2407–2439 then examines the body with those bindings. Deferred definition bodies are not traversed as eager calls merely because they are defined (lines 2051–2058).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2632-2679` folds the reachable literal argv and passes its joined form to shell classification; lines 775–780 classify this non-query `-S` form as host mutation. The raw row retains the correct source call identity.

The result is not subset matching. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:683-729` checks the one selected input's identity, row shape and counters; lines 732–756 require **complete sorted multiset equality and zero unparsed** for exact cases. Any extra stale lead, missing true command, wrong evidence marker or duplicate row would fail this exact comparison. The sealed any-tier exclusion list is empty, but that does not permit extra stale rows under exact equality.

For uncertainty, the same canonical evaluator checks any-tier exclusions before either branch (lines 740–748), and accepts a complete zero-error `accept_exact_want` only as a separate explicit uncertain-case alternate (lines 758–766). This fixture has no such alternate. A lead-only result, parsed-clean absence, or generic uncertainty signal would **not** satisfy its exact contract. The actual output presents none of those ambiguities.

## Residual risk and verification gaps

- This case establishes only the selected straight-line local-parameter reassignment shape, which is expressly supported by `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/supported-forms.md:5-11`. It does not exhaust callable lifetimes, shared mutable captures, nonlocal updates, conditional returns, late globals, scheduled targets, cancellation, or independent factory instances.
- In particular it has no caller-side argument rebinding and never rebinds the returned function's name. It therefore does not independently reproduce or close the original F1/F3 counterexamples. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:15-17,129-132` already describes owner-body reassignment as repaired in r21 while keeping F1/F3 open. This one pass is not evidence of a newly gained baseline result. No old tool or original red fixture was rerun.
- `xd://lsp` is not mounted: discovery returned `No such tool: xd://lsp`. LSP status/references/definition/diagnostics could not be obtained. Caller and definition review used focused source reads and literal search fallback, not claimed semantic-LSP proof.
- No payload code was executed: the scanner parses eval source with `ast.PyCF_ONLY_AST` at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2280-2283`. The single assigned runner/scanner path was used; no alternate scanner runtime, live probe, package query, full corpus, full oracle, baseline replay, build, lint, formatter, suite or generic smoke was run. Resume/rerouting contracts are not exercised by this fixture; no continuity or zero-mutation preflight claim is made.
- No production, fixture, expected, proposal, registry, gate or documentation changes were authored. Only this assigned report and its uniquely scoped raw receipt were written. No tools were installed or updated.

**Recommendation:** retain this exact result as bounded agreement with the sealed expectation. Do not elevate it into family-wide completeness, new baseline improvement, outside-lane independence, saturation, or admission.
