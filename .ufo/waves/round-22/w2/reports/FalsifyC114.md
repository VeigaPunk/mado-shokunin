# FalsifyC114: C1 case CXPartialMethodTiming (round 22, Mado)

Seat: MadoR22.FalsifyC114 (leaf member, advisory). Delivered tool `tools/mado-tripwire.py` sha256 `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce`, which matches the fixed C1 identity and was unchanged before and after the run.

**Verdict: AGREE** with the sealed expectation for this one case: exact `host_mutation / "pacman -S r22-cxpm" / observed`, zero unparsed, zero errors. Scope is this single case on this tool hash. No admission is granted, and nothing here changes the streak or disposition.

## 1. Identities checked

| Item | Lane-relative path | sha256 (prefix) | Check |
|---|---|---|---|
| C1 tool | tools/mado-tripwire.py | 36fdc459 | equals fixed C1 identity; before = after |
| Expected | .ufo/waves/round-22/oracle/expected.json | b5cd4cf3 | equals fixed oracle identity; equals pin-file content |
| Pin file | .ufo/waves/round-22/oracle/expected.sha256 | 7cc4aae9 | binds b5cd4cf3 |
| Runner | .ufo/waves/round-22/oracle/measure.py | 41b021bb | equals `expected.runner_sha256` |
| Producer | .ufo/waves/round-22/oracle/assemble.py | 0270c10b | equals `expected.producer_sha256` |
| Fixture | .ufo/waves/round-22/oracle/inputs/CXPartialMethodTiming.jsonl | 9fe25d9d | equals `case.input_sha256` |
| Original proposal | .ufo/waves/round-22/w1/proposals/CXPartialMethodTiming.json | 000f42e9 | equals `case.proposal.sha256` |
| Truth seal | .ufo/waves/round-22/truth-seal.json | 47f403f6 | equals pinned truth seal |
| Population | runner integrity | 04616857 | equals `expected.population_sha256` |
| C2 audit tool (identity only, not run or assessed) | tools/mado-evidence-audit.py | 277eced2 | equals fixed C2 identity |

Runner verified 106 sealed sources, 52 proposal files and 57 inputs before and after the run.

## 2. Run: one command, one scanner child

- Invocation: `python3 -I .ufo/waves/round-22/oracle/measure.py --tool tools/mado-tripwire.py --case CXPartialMethodTiming`, cwd lane root. Process exit 0; stderr empty.
- Runner-recorded argv: `[/usr/bin/python3, measure.py, --tool, <tool>, --case, CXPartialMethodTiming]`. The `-I` flag is not recorded (see R6).
- Scanner child: exactly one. argv `[/usr/bin/python3, -I, -c, WRAPPER, tool, fixture]`; exit 1 (one unpermitted finding, which is the expected scanner exit for findings); stderr empty; no scanner error.
- Caps, enforced by `measure.py scan()`: RLIMIT_AS 402653184 (384 MiB), timeout 15 s, concurrency 1.
- Receipts in `.ufo/waves/round-22/w2/receipts/FalsifyC114/`: `result.json` (argv, exit, stdout, stderr, before/after hashes, drift), `measure.stdout` (5442 B, sha256 14f48658), `measure.stderr` (empty), `measure.exit`, `before.sha256`, `after.sha256`.
- Drift: none. Tool, expected, runner, producer and fixture hashes were identical before and after. The runner's own before/after checks agree.

## 3. Actual rows

- `got_rows`: `[{class: host_mutation, command: "pacman -S r22-cxpm", evidence: observed}]`
- `want`: identical.
- `unparsed`: 0 (eval_unparsed 0, unparsed_spawns 0). `reasons`: []. `pass`: true.
- Scanner payload: one file row (lines 1, eval_calls 1, bash_calls 0, sha256 and path equal the fixture). One finding: line 1, tool eval, call id `CXPartialMethodTiming-0`, rule `pacman:-S`, argv0 `pacman`. observed_findings 1, lead_findings 0, unpermitted 1, counts host_mutation 1.
- Forbidden `pacman -Q r22-cxpm-late`: absent at every evidence tier.

## 4. Independent expected semantics (not taken from the tool or runner)

Sources: `/usr/lib/python3.14/functools.py` (sha 9db56d38; `_partial_new` 313–357 with `self.args = tot_args` at 353; `partialmethod.__get__` 472–489 with `partial(new_func, *self.args, **self.keywords)` at 480). CPython 3.14.8 reference `compound_stmts.rst` (sha 35e6dfbf; line 1434: the class suite executes in a new frame when the `class` statement runs). The sealed `source` citations check out. The cited `__get__` range ends at 488, and `return result` is line 489, which does not matter.

Trace:
1. `argv = ["pacman","-S","r22-cxpm"]` binds global L1.
2. The `class C:` suite runs immediately. `functools.partialmethod(worker, argv)` reads global `argv` = L1 and stores it by reference in `args`.
3. `argv = ["pacman","-Q","r22-cxpm-late"]` rebinds the global name to L2. L1 is not mutated.
4. `C().run` calls `partialmethod.__get__`. `worker.__get__` returns a bound method, which is not `self.func`, so the result is `partial(bound_worker, L1)`.
5. The call runs `worker(instance, L1)`, which runs `subprocess.run(L1)` and so `pacman -S r22-cxpm`. This is the last statement. `C()` has no `__init__`, and nothing raises before the spawn.

Expected: exactly one observed host_mutation row, zero unparsed, no -Q row. `classify_pacman` (tool 738–781) maps `-S` with no y/u/w/c/s/i/l/g/p flags to host_mutation, and `-Q` to package_query.

Kind and uncertainty: `exact` is correct. The spawn is unconditional at module top level, with a literal argv and no mutation, so there is no true uncertainty. `accept_exact_want` is null, which is correct. A lead-only or uncertain answer fails this case, as the sealed rationale intends. `require_signal: true` is inert for exact cases (measure.py 752–756).

## 5. Why the delivered tool produces -S, by code path (tool 36fdc459)

- Class-time capture: the `update_bindings` ClassDef branch (1892–1907) sets `descriptor.mado_fixed` via `captured_node` (1417–1425). That node carries `mado_literal` = L1, taken from the class-time env.
- Statement order: `prepare_eval_calls` processes statements in order (2217–2251). The class is handled before `argv = [-Q]` updates env (2250).
- Call site: `callable_info` Attribute path with receiver = instance of C (1785–1796) calls `class_method_info` (1687–1714), which reads `mado_fixed` (1711), not the raw `args`.
- Precedence: `literal_value` returns `mado_literal` before consulting the call-site env (1355–1357). The call-site `argv = -Q` (statement snapshot, 2197) is never used for the fixed argument.
- Merge and bind: `spawn_scan` merges fixed nodes into a bound call (2557–2563). `bind_literal` binds argv = L1 with self skipped (2089–2160). `follow_helper` overwrites `body_env["argv"]` with the bound value (2430–2431). The spawn branch classifies `subprocess.run` with the literal argv (2630–2683). Evidence defaults to observed (scan_file 2876–2880).
- No lead and no unparsed: `worker` is never swept. Its only refs are arguments to `functools.partialmethod`, which is pure (`pure_stdlib_path` 1586–1593; spawn_scan 2727–2728), and consumer filtering (2691–2700) skips them. The call-time identity check at 1706 passes only because `statement_snapshot` keeps `functools` through the ClassDef walk (2172–2182). The observed -S row shows that it did.

## 6. Falsification attempts for this case

| Attack | Result |
|---|---|
| False observed -Q (late binding) | Not reproduced. The fixed argument comes from `mado_literal`, and body_env is overwritten by the bound parameter. The baseline late-binding route (`tool-before.py` 1581–1591 and 2384–2388, raw `descriptor.args[1:]`) is not reached on the delivered path for this text. |
| Lost true -S | Not reproduced. The row is emitted through `follow_helper`. |
| Wrong identity | `worker` is captured at class time (1902). `C` comes from the statement binding. No duplicate row; no other `worker` or `run` definition. Call-time `functools` check: see R2. |
| Lifetime | Class-time capture plus statement order. Rebinding does not mutate L1. The mutated-literal guard (1329–1342, 2238–2242) would fail closed if it had. |
| Conditional target | None in the text. One `run` member. |
| Parsed-clean ambiguity | Zero counters are produced by resolved nodes, not by silence. Every call node here resolves: partialmethod is pure, `C()` is a class, `C().run` resolves through class_method_info, and `subprocess.run` is a spawn. |
| accept_exact_want vs true uncertainty | No alternate exists for this case. An uncertain or lead-only result is a fail. |
| Any-tier forbids | Empty list. The observed-only forbid is satisfied, and the exact multiset already excludes any -Q row. |

## 7. Prior receipts (read only, not re-executed)

- No round-21 original red exists for this case. It is a round-22 W1 proposal, not an F1–F5 fixture.
- Round-22 before receipt `evidence/first/oracle-before-new50.json`, inner `tool_sha256_before` 46c82902 (baseline `evidence/tool-before.py`): this case returned `package_query pacman -Q r22-cxpm-late`, observed, pass false (reason: forbidden observed command). That matches the predicted lifetime defect, so the case does discriminate the baseline defect.
- Round-22 after receipt `evidence/first/oracle-after-all57.json`, inner `tool_sha256_before` 36fdc459: this case `host_mutation pacman -S r22-cxpm`, observed, pass; all 57 passed. The all-57 claim is not re-verified here.

## 8. Residual risks (reported, not normalized)

R1 through R10 are not triggered by this sealed text. They are listed for planner judgment.

- R1 Stale citation pointer. The sealed `source` field cites baseline tool lines 1581–1591 and 2384–2388. Those lines are accurate for `tool-before.py`. The delivered mechanism is at 1687–1714, 1892–1907, 2407–2439 and 2557–2570, and the truth does not name these. Documentation currency; no verdict change.
- R2 Silent drop from call-time bindings. [INFERENCE from code reading; not probed.] Two triggers:
  - (a) If `functools` is rebound after the class statement, the call-time check at 1706 fails. `class_method_info` returns None, and `C().run` becomes unresolved (1793–1799; `dotted` returns None for a Call base, 1279–1289). spawn_scan (2610–2613) then calls `spawn_attr_leads`, which emits nothing without literal args. The result is zero rows and zero unparsed, although real Python still runs the partial.
  - (b) Any eager opaque statement between the class and the call clears all bindings (2226–2230; `opaque_module_mutation` 1512–1530 treats `exec`, `eval`, `compile`, `setattr`, `delattr`, `__import__`, `import *`, and globals() writes as opaque). The same silent path follows. A variant with an intervening `exec("pass")` or `setattr(...)` would likely report clean despite a real `pacman -S`. This is the most serious family-level risk. It needs one authorized probe, which I did not run.
- R3 Scope declaration. `supported-forms.md` claims exact support for `functools.partial` returned from visible factories, and states that arbitrary descriptors stay outside exact support. It does not list `functools.partialmethod` class attributes. This case asserts exact support for that stdlib descriptor form. The planner must either claim the form explicitly or reclassify it. This verdict does not decide it.
- R4 Measured entry path differs from the CLI. The measure.py WRAPPER (34–38) calls `main` directly. The CLI `__main__` (3448–3463) runs through `run_with_stack` (3420–3445: 512 MiB thread stack, recursion limit 50000) and converts internal exceptions to could_not_evaluate with exit 2. Shallow input is unaffected. For deep input, an uncaught exception leaves no JSON, so the case errors (`scanner produced no JSON output`, measure.py 673–675). Direction is fail-closed on the paths traced, but verdicts can diverge from the CLI for deep inputs.
- R5 Partial runner checks. Exact cases check the multiset and unparsed == 0. They do not validate payload totals (observed_findings, lead_findings, counts, eval_calls). Those were consistent here (1/0/1).
- R6 Runner argv omits `-I`. measure.py 796 records `sys.argv`, not interpreter flags.
- R7 Receipt label mismatch. `evidence/first/oracle-before-new50.json` has top-level `selected_tool_sha256` = 36fdc459, but its `--tool` argument and inner `tool_sha256_before` are the baseline 46c82902. This is a wrapper metadata mislabel. The inner output is authoritative, and this verdict does not use the label.
- R8 Population not verified. This report covers CXPartialMethodTiming only. The prior all-57 receipt was not re-verified.
- R9 Cosmetic. Finding timestamps are the string "None" (scan_file 2890).
- R10 `require_signal: true` on an exact case is never evaluated.

Not checked: the sealed rationale's claim that the frozen round-21 PartialMethod input has no fixed argument, and the `ConnLifetime.json` citation.

## 9. Scope against current target

- The C1 target is: all eligible frozen expectations match (50 eligible + 7 originals = 57), every original red resolves, and the no-harm guards hold (oracle 35+17, incident recall, tw-precision 166/175 floor, 1356-fixture removal comparison, resource recipes).
- This case is one of the 50 eligible expectations. It is not a required proposal (REQUIRED_PROPOSALS: TimerRunAliasActual, CapturePartialGlobalLateActual, CaptureNestedFactory) and not an original red.
- This verdict covers 1 of 57 expectations on one tool hash, and only the partialmethod fixed-argument lifetime sub-claim.
- Not covered: the other 56 expectations, the no-harm guards, C2, the closure resource population, supported-form claims beyond this text, and any admission.

## 10. Not done

- No other scanner runs, no population rerun, no baseline tool run, no builds or tests, and no installs (none were needed).
- Before admission, the main agent should decide R2 and R3. An authorized single probe of R2(b) would settle the most serious family-level question.

Report: .ufo/waves/round-22/w2/reports/FalsifyC114.md
Report (absolute): /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC114.md
Receipt (absolute): /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC114/result.json
