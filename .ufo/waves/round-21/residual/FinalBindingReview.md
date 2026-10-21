# Final binding review: captured closures and scheduled threads

Seat: `MadoR21-2.FinalBindingReview` · Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` · Author-lane advice, not independent promotion or admission.

## Verdict (recommendation)

Do not admit the captured-closure and scheduled-thread binding paths in `tools/mado-tripwire.py` at `46c82902…` as final. The single allowed scanner child reproduced four wrong or missing rows and one wrong evidence label across six inert variants. The control variant passed. Every affected file reported `eval_unparsed` 0 and `unparsed_spawns` 0, so these defects are silent.

- **F1, High:** factory arguments are bound at invocation time, not at factory-call time.
- **F2, High, failed W2 repair:** an unbindable factory call lets the closure's parameters resolve to same-named module globals, which are then reported as observed.
- **F3, Medium:** a returned closure's identity comes from its `def`, ignoring a later rebinding inside the factory.
- **F4, Medium, recall:** a scheduled `Thread.run()` (and `Timer.run()`) is never followed.
- **F5, Low, hygiene (parent-requested):** the reserved key `__mado_thread_target__` shares the source binding namespace and can shadow a same-named source global inside the thread body. Confirmed by probe. Fix in the hygiene section.

W2 repairs on final bytes, by source reading (W2 fixtures were not rerun):
- Present for the reported shape: CallbackBoundArgs, CallbackGlobal (`.start` alias), PartialMethod, SaveFunction, NamespaceBinding #2.
- Partial: CalledClosure (owner-body reassignment is repaired; F1 and F3 are open). NamespaceBinding #1 (bindable factories are repaired; F2 is open).

## Identity (exact, read-only)

| Item | Value |
|---|---|
| `tools/mado-tripwire.py`, working tree | `46c82902896da0ec0ebd54254b1891667fa5da48f8cb297ee08bfb337e34c8c1` |
| Same bytes at lane HEAD `a6cef8984d3815775587ab634ce558e13338b0eb` | `git show a6cef898:tools/mado-tripwire.py \| sha256sum` = `46c82902…`. `git status --porcelain` is empty for the tool and `oracle/`. |
| Frozen truth `oracle/expected.json` | `fd2bfbc86897e1ee7a79302f6ccf6c3403709b132180864a0674f8212925576f`, equal to the pin in `oracle/expected.sha256` |
| `oracle/measure.py` | `4eb893d2337a4aa758d14c064a855032737c6e2b2b1239d7ca3502042c6c82da` |
| `oracle/assemble.py` | `be4ee5fc5c27719d9e82d2b0d342fae13af4bb129c0f2818780b3fbf02715edf` |
| `oracle/expected.sha256` | `e8c5dfc9584c50cdef0fc16bd03bf9f095c8ee44c9a7c27a3a6ef15eb9a1d37e` |
| W2 tested candidate (not final) | commit `f499a8db…`, tool `2e152f6d…`. W2 line numbers refer to it. This review cites final-byte line numbers. |
| Interpreter | `/usr/bin/python3`, 3.14.8 (existing; nothing installed) |

## Scope and method

- Read-only. Final binding code read at: docstring 1–160; `literal_value` 1327; `literal_node` 1377; `callable_info` 1603; `assignment_binding` 1700; `update_bindings` 1771; `eager_calls` 1868; `bind_literal` 1964; `prepare_eval_calls` 2038; `sweep_body` 2179; `follow_helper` 2228; `spawn_scan` 2274 (thread_start 2298, capture 2333, helper 2375, refs 2504); `discover` 2593; `scan_file` 2626; `run_scan` 2741; `main` 3198.
- Read the six W2 reports, the frozen rows for CallableFunction, CallbackBoundArgs, CallbackGlobal, CalledClosure, PartialMethod and SaveFunction, and the frozen input `oracle/inputs/CalledClosure.jsonl`.
- **One probe, one child.** Command: `python3 -c` with `runpy.run_path(oracle/measure.py)` and then `scan(tool, fixture_dir)`. That spawns `sys.executable -I -c WRAPPER tool dir` with `RLIMIT_AS` 402653184 and a 15 s timeout. It is not `main()`, not the frozen replay, not the corpus, and not a W2 fixture rerun.
- Six inert JSONL fixtures, each with one `eval` toolCall. One file per variant, because the scanner persists bindings per file. The scanner parses with `ast`. No Python payload was executed.
- Hygiene check: F5 and its control were covered by the same probe. The source reasoning in the hygiene section was not probed separately.

| Fixture (under `.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/`) | sha256 |
|---|---|
| `capture-invoke-time.jsonl` | `6b21d584710878f5e486f3e9fcd737c6a6e573c629c2f75d30b45f55b6a317f7` |
| `capture-unbound-global.jsonl` | `9ab845d4a8886714cfea0b16203328b67335013f00b21b18ba23e9b7175e1d9d` |
| `returned-rebound.jsonl` | `774e2946d16c23d9ebdd557ccf279143f6d2249dc7132aa567fb34d12d3d7573` |
| `thread-run-direct.jsonl` | `1cc1188dc4e0c37ecba97d34bdf546113d888c62a9cba0bcfe06d44201a2407f` |
| `thread-key-hygiene.jsonl` | `4ea8ccc8724de011e19dcc1e69da1f4078ac74544f554e39ccda66dc42065c9e` |
| `thread-key-control.jsonl` | `00ecb83fabddfd002d703bc1fbaa449b24e1edf935d0f6792a773c96007162be` |

## Probe result

Exit 1 (5 unpermitted, permit empty). `stderr` empty. Counts: `host_mutation` 0, `package_query` 5. Observed findings 4, lead findings 1.

| Variant | Truth from Python semantics (static, not executed) | Scanner row | Outcome |
|---|---|---|---|
| `capture-invoke-time` | host_mutation `pacman -S r21-factory`, observed | package_query `pacman -Q r21-invoke`, observed | Wrong command. Host mutation missing. **F1** |
| `capture-unbound-global` | argv is the unresolved `parts`. No statically determined observed row exists. | package_query `pacman -Q r21-global`, observed | Fabricated observed row from a module global. **F2** |
| `returned-rebound` | host_mutation `pacman -S r21-b`, observed | package_query `pacman -Q r21-a`, observed | Wrong closure body. Host mutation missing. **F3** |
| `thread-run-direct` | host_mutation `pacman -S r21-thread-run`, observed | no row, `unparsed` 0 | Silent miss. **F4** |
| `thread-key-hygiene` | package_query `pacman -Q r21-hyg`, observed | package_query `pacman -Q r21-hyg`, lead | Evidence downgraded by shadowing. **F5** |
| `thread-key-control` | package_query `pacman -Q r21-hyg`, observed | package_query `pacman -Q r21-hyg`, observed | Pass |

Raw payload from the single child (verbatim):

```json
{"exit": 1, "payload": {"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 5, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/capture-invoke-time.jsonl", "sha256": "6b21d584710878f5e486f3e9fcd737c6a6e573c629c2f75d30b45f55b6a317f7", "unparsed_spawns": 0}, {"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/capture-unbound-global.jsonl", "sha256": "9ab845d4a8886714cfea0b16203328b67335013f00b21b18ba23e9b7175e1d9d", "unparsed_spawns": 0}, {"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/returned-rebound.jsonl", "sha256": "774e2946d16c23d9ebdd557ccf279143f6d2249dc7132aa567fb34d12d3d7573", "unparsed_spawns": 0}, {"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/thread-key-control.jsonl", "sha256": "00ecb83fabddfd002d703bc1fbaa449b24e1edf935d0f6792a773c96007162be", "unparsed_spawns": 0}, {"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/thread-key-hygiene.jsonl", "sha256": "4ea8ccc8724de011e19dcc1e69da1f4078ac74544f554e39ccda66dc42065c9e", "unparsed_spawns": 0}, {"bash_calls": 0, "eval_calls": 1, "eval_unparsed": 0, "lines": 1, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/thread-run-direct.jsonl", "sha256": "1cc1188dc4e0c37ecba97d34bdf546113d888c62a9cba0bcfe06d44201a2407f", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q r21-invoke", "evidence": "observed", "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/capture-invoke-time.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "None", "tool": "eval", "tool_call_id": "FBR-capture-invoke-time"}, {"argv0": "pacman", "class": "package_query", "command": "pacman -Q r21-global", "evidence": "observed", "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/capture-unbound-global.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "None", "tool": "eval", "tool_call_id": "FBR-capture-unbound-global"}, {"argv0": "pacman", "class": "package_query", "command": "pacman -Q r21-a", "evidence": "observed", "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/returned-rebound.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "None", "tool": "eval", "tool_call_id": "FBR-returned-rebound"}, {"argv0": "pacman", "class": "package_query", "command": "pacman -Q r21-hyg", "evidence": "observed", "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/thread-key-control.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "None", "tool": "eval", "tool_call_id": "FBR-thread-key-control"}, {"argv0": "pacman", "class": "package_query", "command": "pacman -Q r21-hyg", "evidence": "lead", "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/residual/MadoR21-2.FinalBindingReview/thread-key-hygiene.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "None", "tool": "eval", "tool_call_id": "FBR-thread-key-hygiene"}], "lead_findings": 1, "observed_findings": 4, "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 5}, "stderr": ""}
```

## Findings

### F1 (High): factory arguments are bound at invocation time

- **Mechanism.** `spawn_scan` line 2334 evaluates the factory call's AST arguments (`capture_call`, recorded at 1652 and 1659) in `cenv`. `cenv` is the snapshot of the invoking statement (2291; snapshots at 2052–2060). Python binds the factory parameter to the object passed at creation. Rebinding `cmd` afterwards does not change the closure's cell.
- **Reach.** Same-cell in the probe. Cross-cell by source: per-file `envs` and `binding_envs` persist across eval cells (2643–2644, 2685–2686), so a factory created in one cell and invoked in a later one hits the same defect. This is by source, not probed.
- **Contract.** The docstring (38–41) says a followed def runs "with those values bound". Here the bound values are the wrong ones.
- **Same class, by source, not probed.** A returned `functools.partial` evaluates its fixed arguments in the invocation env (1635–1638, 2384–2388).
- **Origin.** Introduced with the round-21 capture mechanism. The W2 report cites that mechanism at candidate lines 1613–1622 and 2231–2235, and it is still present.

### F2 (High, failed W2 repair): an unbindable factory call leaks module globals into the closure

- **Mechanism.** Line 2335, `if captured is not None:`. When `bind_literal` returns None, the closure is followed with the invocation env unchanged, and its factory parameter resolves to any same-named module literal. Triggers: starred non-literal argument (1972–1976), non-literal `**` mapping (1998–2000), unknown keyword (2017–2018), missing required parameter (2027–2028).
- **Repro.** `capture-unbound-global` reports observed `pacman -Q r21-global`. No statically determined argv exists, because `parts` is unresolved. The sound output is unparsed or lead.
- **Contract.** `sweep_body` (2179–2186): "Its parameters are unknown; every row it finds is a `lead`." W2 NamespaceBinding finding #1 gave the remedy: "Preserve the closure's lexical bindings, or avoid claiming an observed literal when those bindings cannot be resolved." This branch does neither.
- **Consequence.** An observed row names a fabricated command. It can also hide a real host mutation behind that row.

### F3 (Medium): a returned closure's identity comes from the `def`, not from the binding in effect at return

- **Mechanism.** Lines 1645–1652 build `local` from top-level `def`s only and select `local[returned]`. A later `Assign` rebinding that name inside the factory body is ignored. The prefix replay at 2338–2343 updates `captured_bindings`, but the node has already been chosen.
- **Repro.** `returned-rebound` reports observed `pacman -Q r21-a`. Truth is `pacman -S r21-b`.

### F4 (Medium, recall): scheduled `Thread.run()` (and `Timer.run()`) is never followed

- **Mechanism.** Lines 1666–1667 map only `.start` on a scheduled binding to `thread_start`. `.run` falls through to `unresolved` (1677–1697). Spawn-attribute leads need a literal argv argument (2128–2139), so nothing is emitted. Thread targets handed to `Thread(...)` are skipped by the refs sweep (2517–2519), and the start path is the only owner.
- **Contract.** The module docstring (47–59) lists a thread target handed on as a value among bodies swept as leads. `t.run()` calls the target synchronously in the caller. It is not a `start()` case.
- **Repro.** `thread-run-direct` yields no row and `unparsed` 0.
- **W2 status.** AtkCallbackGlobal was repaired for `.start` only. The `.run` sibling is open. `Timer.run()` shares the path by source.

### F5 (Low, hygiene): the reserved key shares the source binding namespace (parent-requested)

- **Mechanism.** Lines 2299–2300 copy the caller's bindings and inject `__mado_thread_target__`. Line 2304 synthesizes `Name("__mado_thread_target__")`. `follow_helper` copies the map into the body (2241).
- **Scope.** Repo-wide grep finds the literal only at tripwire 2300 and 2304, and in my own `thread-key-hygiene.jsonl`. No frozen or W2 input references it. `local_bindings` appears only at 2299, 2300 and 2308. The caller's map is not mutated, so the effect stays inside the thread-start subtree.
- **Probe.** `thread-key-hygiene` reports `pacman -Q r21-hyg` as lead. The body's call resolves to the worker already on the stack (2376–2383), which takes the recursion branch and emits a lead. `thread-key-control`, with a non-reserved name, reports observed.

## Parent-requested hygiene answer (thread_start reserved key)

**Yes.** Carry the resolved callable on the synthetic node, and consult it before any bindings lookup. Then no key is injected, no map copy is needed, and no global or module state changes.

Suggested shape (not applied; no production edits):

```python
# callable_info: first statement
resolved = getattr(node, "mado_resolved", None)
if resolved is not None:          # synthetic thread invocation, never a source name
    return resolved

# spawn_scan thread_start branch: replaces lines 2299-2300 and 2304
func = ast.Name(id="<thread target>", ctx=ast.Load())  # not a Python identifier
func.mado_resolved = info["target"]
invocation = ast.Call(func=func, args=..., keywords=...)
take(spawn_scan([invocation], cenv, cbindings, depth + 1, ctx=ctx))
```

- **Why it avoids the collision.** The resolved target never enters a bindings map, so no lookup by source name can reach it. The synthetic id is never consulted, because `callable_info` returns first.
- **Minimal alternative.** Keep the map, but use a key no source identifier can equal, such as `"<thread target>"`. That is collision-free, because parsed `Name` ids are identifiers. It still leaves synthetic state in the body map, so I prefer the node-carried form.
- **Behavior change for non-colliding source.** None expected. The returned dict is the same one `callable_info` returns today. The key and the copy matter only for the reserved name.
- **Verification status.** The collision is confirmed by the F5 probe against its control. The fix is not probed, because the contract forbids production edits and extra probes. It is a source-level recommendation for the author lane.

## W2 repair status on final bytes (source reading only; W2 fixtures not rerun)

| W2 atom | Final status | Evidence (final lines) | Open |
|---|---|---|---|
| CalledClosure | Partial | Prefix replay 2338–2344 handles owner-body reassignment before return | F1, F3 |
| NamespaceBinding #1 | Partial | Bindable factory: overlay at 2334–2344. Unbindable factory: no overlay. | F2 |
| NamespaceBinding #2 | Repaired | `namespace_read_only` 1455–1468 accepts compares only against empty dict literals | none found |
| AtkCallbackBoundArgs | Repaired | Thread kwargs literal invocation 2301–2307; keyword binding in `bind_literal` 1996–2018 | not probed |
| AtkCallbackGlobal | Repaired for `.start` | 1666–1667, 1713–1716, 2294–2297 | F4 (`.run`) |
| AtkPartialMethod | Repaired | 1585–1586 resolves by callable name, not by spelling | not probed |
| AtkSaveFunction | Repaired | 1808–1811 keeps the resolved binding for all-`Name` chained targets | not probed |

Checked by source, no gap found:
- Start aliasing, including `start = thread.start` and chained `Thread(...).start()` (1666–1667, 2294–2297).
- Timer positional indices (1719–1726).
- Thread `args` and `kwargs` are evaluated at construction (1719–1730), which is the correct timing for them.
- Factory-body spawn calls are scanned through the factory call's own follow (2375–2401). The prefix call result discarded at 2343 therefore does not drop rows.

## Limits

- **Not attacked, per scope.** Explicit annotation forcing. Arbitrary opaque namespace mutation, for example writes through `sys.modules[...]`, which `OPAQUE_PY_CALLS` does not cover. Inherited `Thread` subclass `run` (docstring 73–74: "inherited methods are not resolved").
- **No safety proof is inferred** from any clean result. The probe shows the presence of these defects, not their absence elsewhere.
- **Not examined.** Non-`Name` factory returns (for example `return a if c else b`). Subscript dispatch beyond one container level. `**` spread into `Thread(...)`. Cross-cell staleness, which is covered by source only.
- **Frozen replay not run.** The frozen rows are unchanged. The frozen CalledClosure input is `outer(["pacman","-Q","w2shape"])()`, a literal factory argument in the same statement, so F1–F3 do not reach it by source.
- **Probe truths are static reasoning** about Python semantics. Nothing was executed.
- **LSP unavailable.** `xd://lsp` returned "No such tool: xd://lsp". Caller checks used reads plus literal grep, which is text fallback and not semantic proof.
- **Git.** Read-only only (`show`, `status`, `log`, `rev-parse`). The only new untracked path is `.ufo/waves/round-21/residual/`.
- **Tools.** None installed or updated.

## Checks for the author lane (not run by me)

1. Fix F1–F3 in the capture path. Snapshot factory-call bindings at closure creation; `assignment_binding` already has the factory-time env. On bind failure, set factory parameters to `LITERAL_MISS` as `sweep_body` does. Resolve the returned name against post-prefix bindings.
2. Fix F4. Map `.run` on a scheduled binding to an in-place invoke that reports observed. Keep the refs exemption at 2517–2519.
3. Fix F5 as described above.
4. After the fix, re-run the six inert fixtures and the frozen replay. Leave `expected.json` unchanged.
