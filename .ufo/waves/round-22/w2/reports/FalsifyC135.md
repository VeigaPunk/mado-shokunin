# C1 CaptureSameCell — fresh recovery falsification

**Verdict: agree, for this sealed case only.** No actionable defect found in the measured class/command/evidence multiset, callable or input identity, or error accounting. This is author-lane advisory evidence, not admission or a judgment of the whole recovery.

## Axes and scope

- Semantic fidelity: complete command/class/evidence multiset; no invented argv or lost true command.
- Lifetime and identity: creation-time factory parameter binding versus later module-name rebinding; returned helper and transcript attribution.
- Uncertainty honesty: exact truth versus lead/unparsed alternatives; no parsed-clean substitution.
- Evidence integrity and bounded operation: fixed tool/fixture/runner identities, one capped scanner child, retained raw output.

Target: delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`, with the assigned C1 tool hash below. Reviewed the relevant production diff from registered base `741122d177ae8ff68a73768777f20484d5bdcbe4` to that revision and the current candidate path. All production, fixture, expectation, proposal, and historical source artifacts remained read-only.

## Findings by severity

None within the assigned `CaptureSameCell` case. The attempted falsifications and their evidence are below; a green comparison is not the semantic rationale.

## Independent semantic determination

Original proposal: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CaptureSameCell.json:2-12`. Sealed input: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CaptureSameCell.jsonl:1`.

`make(spec)` is called while `spec` denotes the list `['pacman', '-Q', 'r22-samecell-held']`. That call binds the local parameter `argv` to that object. The returned `run` closes over this local parameter, not the module-level name `spec`. The subsequent plain assignment to `spec` creates a different module binding; it does not mutate the held list or rebind `argv`. The unconditional `slot()` therefore reaches exactly one visible `subprocess.run(argv)` with the held query argv. The decoy list is never passed to a spawn. The returned callable is specifically the nested `run`, with no conditional return, scheduled callback, unresolved expansion, or invalid argument binding in this input.

Complete independent expected multiset:

```json
[{"class":"package_query","command":"pacman -Q r22-samecell-held","evidence":"observed"}]
```

Expected error counters are both zero. No lead row is warranted. Here `observed` is the detector's statically followed-call tier, not proof that a host process actually ran; the production contract explicitly distinguishes issued from executed at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:30-45`.

This reasoning agrees with, rather than replaces, the original r21 F1 authority: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:55,70-76`. Its creation-time binding rule remains authoritative. The older tool and original red fixtures were not rerun.

### Relevant changed behavior

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1642-1684`: `factory_result` binds the factory call immediately, replays the prefix before the return, resolves the returned helper from the resulting bindings, and stores its lexical overlay. For this source, the stored `argv` is the held list.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2089-2116,2203-2254`: literal arguments are bound from the call-site environment; statement snapshots precede updates. The later assignment to the name `spec` replaces that name's literal binding. The mutation invalidation at lines 2233-2242 applies to attribute/subscript targets, not this plain-name rebinding.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2510-2516,2547-2580,2407-2439`: invoking the stored helper overlays its captured lexical values before following its body. It does not reevaluate `make(spec)` against the later decoy binding.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2632-2679,738-780`: the resolved literal argv reaches shell classification; `-Q` is `package_query`, whereas the unused `-S` decoy would be `host_mutation` if incorrectly borrowed.

## Authorized measurement and actual rows

Executed exactly once:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CaptureSameCell
```

Runner exit **0**, status `complete`, totals **1/1**, integrity errors `[]`, runner stderr empty. Scanner exit **1** means one unpermitted finding, not scanner failure or clean. Scanner stderr was empty; `scanner_error` was null.

Actual complete normalized multiset:

```json
[{"class":"package_query","command":"pacman -Q r22-samecell-held","evidence":"observed"}]
```

Actual finding provenance: `argv0="pacman"`, `rule="pacman:-Q"`, `tool="eval"`, `tool_call_id="CaptureSameCell-0"`, line `1`, file `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CaptureSameCell.jsonl`. The reported file digest matched the sealed fixture. Counts: `package_query=1`; `host_mutation=live_probe=tool_install=vcs_write=0`; `observed_findings=1`; `lead_findings=0`; `eval_unparsed=0`; `unparsed_spawns=0`; aggregate `unparsed=0`.

The runner enforces the child limits at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:643-680`: **402653184 bytes (384 MiB)** address space and **15 seconds**. Exact case selection at lines 803-810 produced one scanner child. Its before/after validation checked 57 input artifacts, 52 proposal files, and 106 sealed source files; those integrity checks are not 57 scanner runs or 57 semantic passes. Fixture code was inert AST input, not executed; the parser path uses `ast.PyCF_ONLY_AST` at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:2280-2293`.

### Falsification outcomes

- **False observed/lead argv:** no decoy finding at either tier; the only row is the held query. Although this case's explicit decoy ban names the observed tier, complete exact multiset comparison also rejects any additional decoy lead.
- **Lost true command / wrong class:** the held command occurs exactly once as `package_query`, matching the complete expected multiset, not a subset.
- **Wrong callable/input identity:** the lexical helper flow above matches the fixture's returned `run`; actual file path, digest, line, tool, and call ID all identify the selected input.
- **Lifetime:** creation-time `argv` survives later `spec` rebinding. There is no captured-object mutation in this case.
- **Conditional-target / parsed-clean ambiguity:** neither applies to this unconditional exact source. Actual output is a nonempty observed finding with zero error counters, not an empty or error-bearing clean result.
- **Exact versus uncertainty:** sealed `expected_kind="exact"`, `accept_exact_want=null`. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:736-766` checks any-tier bans before either acceptance path and requires full multiset equality plus zero unparsed for exact cases. This result did not use an uncertain alternate. Unknown-case any-tier exclusion or genuine uncertainty signaling was not exercised and is not claimed.

## Fixed identities and retained evidence

All five independent before/after SHA-256 checks were identical; no drift was observed.

| Artifact | SHA-256 |
|---|---|
| C1 tool | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| CaptureSameCell fixture | `8660586c1113284e8a34387aa8edc962ca37e13b7e2eccc872f0bd6a1d1ab6be` |
| Runner | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Oracle expected | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| Original proposal | `2bb59834bdd843460eb7671a6490fc505cb76e2be41821c24f49fd80e2135f2d` |

Raw receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC135/result.json`. It retains the exact outer argv including `-I`, runner exit/stdout/stderr, complete runner JSON, nested scanner argv/exit/stdout/stderr/payload, before/after hashes, and stated caps. The runner's own reconstructed `argv` omits its interpreter's `-I`; the outer receipt preserves the actual requested invocation.

## Residual risk and verification gaps

- This is one same-cell straight-line captured-parameter variant, not evidence for all C1 forms, all F1 triggers, multiple factory instances, cross-cell state, partials, mutable/nonlocal changes, conditional returns, cancellation, or scheduled targets. It does not establish C2, corpus no-harm, historical-suite recovery, resource scaling, or saturation.
- `xd://lsp` returned **No such tool**. LSP status, references, definition, and diagnostics were unavailable. Used direct source reads and literal search only as navigation fallback; no grep result is offered as semantic proof.
- No additional scanner runs, new source-shaped probes, old-tool reruns, builds, full suites, linters, formatters, installs, package commands, live probes, or orchestration runtimes were invoked. No rerouting or resume path was involved. No tools were installed or updated.
- Prior r19/r20/r21 rejected-harmed receipts and the streak remain unchanged. This author-lane recommendation grants no non-author admission, host clearance, or next-round authority; L1 retains planner/integration authority.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC135.md
