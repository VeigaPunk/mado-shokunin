# FalsifyC108 — CX8ClosureThread

## Findings by severity and verdict

**Verdict: agree**, limited to the sealed `CX8ClosureThread` case and the delivered C1 bytes identified below. No actionable high-, medium-, or low-severity defect was found in this case. The complete actual row multiset agrees with independently reasoned source semantics; this is not an inference from the runner's green result alone.

This is an author-lane advisory attack, **not non-author admission**. It does not clear C1 as a whole, establish C2, change the r19/r20/r21 rejected-harmed receipts or rejection streak, or grant admission/host recovery. L1 retains planner/integration authority.

Axes: **command precision; true-command recall; closure lifetime and callable identity; evidence/uncertainty honesty; immutable artifact identity; bounded resource and coverage honesty.** No frontier expansion or additional source-shaped probe was performed.

## Exact assigned scope and identities

Target revision: `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. The selected working-file C1 hash matched the assignment's fixed identity before and after the sole measurement. The actual relevant recovery diff was read from base `741122d177ae8ff68a73768777f20484d5bdcbe4` to the delivered revision, restricted to `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`; review conclusions below cover the CX8 execution path, not unrelated hunks.

The original proposal is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/CX8ClosureThread.json:2-16`. Its exact expectation is retained in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/expected.json` under case ID `CX8ClosureThread`: one cell, `reset=false`, `expected_kind=exact`, no correction/addenda, `accept_exact_want=null`. The inert scanner input is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/inputs/CX8ClosureThread.jsonl:1`.

| Artifact | SHA-256, identical before/after |
|---|---|
| C1 tool | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` |
| Case fixture | `cfc2a3929c63468e5864006eed834efd3d5f69ac7b273ecc93ce0d9edd01f24d` |
| Runner | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` |
| Oracle expected | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` |
| Original proposal | `335eacd8917fdde1b74a3366ae823a82cc86ecf95e1dc8c1f51355907e1cfe97` |
| Cited Thread source | `5323909624ec2165e70b6d31333e4191b63d383d2dc5a7d7d516a3475ea2b7e3` |
| Cited assignment source | `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc` |

Receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC108/result.json`. It retains the exact outer argv, exit, stdout and stderr, nested scanner argv/exit/stdout/stderr and complete scanner payload, before/after artifact hashes, timing, and empty identity-drift result. The original r21 F1/F4 red receipts remain source authority; no old tool was executed.

## Independent semantic expectation

The fixture's embedded source has this relevant sequence (payload source was never executed):

1. `make(argv)` defines `run`, whose sole effect when called is `subprocess.run(argv)`, then returns that particular helper.
2. `cmd` is first bound to `["pacman", "-S", "r22-cx8-compose"]`.
3. `threading.Thread(target=make(cmd))` evaluates `make(cmd)` while constructing the Thread. The factory parameter `argv` retains the original list object in the returned helper's cell; it is not a late lookup of the module name `cmd`.
4. The next assignment binds module `cmd` to a different list, `["pacman", "-Q", "r22-cx8-decoy"]`. It neither changes the original list nor the closure's cell.
5. The single unconditional `t.run()` invokes the captured closure synchronously. No `.start()` scheduling, Timer cancellation, conditional target, subclass override, unresolved argument expansion, or repeated invocation is present.

The proposal's canonical Python source supports the critical edges: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceThread/threading-v3.14.8.py:925-928` stores the target and arguments; lines `1013-1028` define direct `run()` as calling the stored target, then deleting its stored attributes. `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-simple_stmts.rst:143-156` specifies name binding/rebinding, rather than mutation of the former object.

Therefore the complete expected finding multiset is exactly:

```json
[{"class":"host_mutation","command":"pacman -S r22-cx8-compose","evidence":"observed"}]
```

`pacman -S` is the host-mutation command; none of the three excluded decoy/mixed commands is executed by this source path. A lead-only result, missing mutation, invented query, duplicate/extra row, or positive parsing/error counter would disagree. Here `observed` means the detector's resolved source execution path, **not a command actually executed during this review**; the tool expressly distinguishes issued from executed at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:30-45`.

## Candidate path and changed behavior

The inspected changes address the composition of the authoritative F1 capture-time and F4 direct-run failures described in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/FinalBindingReview.md:70-77,90-95`:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1642-1683` binds factory literals in the creation environment, replays the prefix, resolves the returned binding, and stores local closure overlays. It replaces invocation-time rebinding of the old factory-call AST. For CX8, the overlay retains `argv` and the correct nested `run` identity; module `cmd` is not the helper's free variable.
- Lines `1757-1783,1841-1853` resolve `make(cmd)` as the stored Thread target with the creation-time environment, while lines `1784-1790` resolve direct `.run()` as a scheduled invocation. Statement binding/snapshot propagation is at lines `1928-1936,2163-2253`.
- Lines `2470-2488` invoke the captured target once with the default empty arguments/keywords. The resolved callable is attached to the synthetic AST node (`mado_resolved`, honored at lines `1728-1730`), not injected under a legal source identifier. This prevents a source-name collision on this dispatch path.
- Lines `2510-2516` overlay captured locals before helper following at lines `2547-2580`; `follow_helper` at lines `2407-2437` preserves those values into the body. The literal spawn is then classified at lines `2623-2684`. This path neither needs unknown-argument fallbacks nor exceeds the descent budget.

Thus the source mechanism, not merely the pass bit, explains why later module rebinding does not change the reported argv and why this synchronous target is observed rather than silently missed or downgraded to a lead.

## Sole authorized measurement and actual rows

Executed once, without fixture execution:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case CX8ClosureThread
```

The runner's canonical enforcement is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:643-660`: one selected scanner child, 402653184-byte (384 MiB) address-space cap, 15-second timeout. The exact case filter and selection loop are at lines `803-837`. Only this one case was scanned; integrity validation of 57 input files, 52 proposals and 106 sealed sources is **not 57 executed test cases**.

Actual complete normalized multiset:

| Class | Command | Evidence | Multiplicity |
|---|---|---|---|
| `host_mutation` | `pacman -S r22-cx8-compose` | `observed` | 1 |

The actual finding identifies the selected absolute fixture path, JSONL line `1`, `tool=eval`, `tool_call_id=CX8ClosureThread-0`, `argv0=pacman`, and `rule=pacman:-S`. No wrong-identity row was present. Counts were `host_mutation=1`, every other class `0`; `observed_findings=1`, `lead_findings=0`, `eval_unparsed=0`, `unparsed_spawns=0`, `eval_calls=1`, `bash_calls=0`. Neither decoy/mixed commands nor extra leads appeared.

The scanner exited **1** with `MADO_TRIPWIRE: findings`, as expected for the detected mutation; that is not a measurement failure or parsed-clean result. Its stderr was empty and `scanner_error=null`. The measurement exited **0**, `status=complete`, `totals={"pass":1,"total":1}`, with empty reasons, empty integrity errors, and unchanged before/after identities. Outer stderr was empty. Measured outer elapsed time was approximately `0.112` seconds; this is not a memory benchmark or saturation claim.

The canonical evaluator at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py:683-756` checks selected fixture identity and parsing counters and compares the **complete sorted multiset**, preserving duplicates, with zero unparsed counters. For this exact case, `accept_exact_want=null`; no uncertain-case alternate was used. The separately scoped uncertain branch at lines `740-778` rejects named forbidden commands at every evidence tier before considering a complete accepted-exact alternate, and otherwise requires genuine lead/unparsed uncertainty when sealed truth requires a signal. Those branches were read, not exercised by CX8, and are not evidence that all unknown cases pass. Although CX8's explicit any-tier exclusion list is empty, its exact multiset requirement still rejects any additional decoy lead.

## Residual risk and verification gaps

- This one exact factory-closure plus direct-Thread-run case lies within the bounded supported composition in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/supported-forms.md:7-11,20-24`. It does not establish every F1/F4 variant, shared-object mutation behavior, nonlocal rebinding, conditional/opaque targets, arbitrary concurrency, or the whole frozen population.
- No C2 audit, full corpus/oracle scan, historical-suite rerun, resource-population run, build, lint, formatter, generic smoke, mutation execution, alternate runtime, same-identity rerouting, or resume-path measurement was performed. There is no saturation or universal Python-semantics claim.
- The `xd://lsp` device was unavailable: the attempted device read returned `No such tool`. Consequently no answering server/status, semantic references, definition, or diagnostics could be obtained. Literal search was used only to locate the relevant source; semantic conclusions above are based on directly inspected definitions/calls, the actual diff, cited Python source, and the retained bounded result, not grep as semantic proof.
- Only the assigned report and receipt were written. No production/fixture/expected/source edits, additional probe, old-tool confirmation, installations, package queries, live/host probes, delegation, or background jobs were used.

No actionable finding remains within the assigned CX8 case. Agreement here is a bounded recommendation, never an admission.
