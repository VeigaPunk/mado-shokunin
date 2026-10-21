# FalsifyC142 — C1 case ThreadReuseName (author-lane advisory falsification)

Seat `MadoR22.FalsifyC142` · round 22 w2 · delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5` · 2026-10-21.
Advisory attack only. This report is **not** a non-author admission and grants nothing. L1 keeps planner and integration authority.

## Verdict: AGREE, scoped as a no-harm control, not as repair evidence

The delivered tool emits exactly the sealed multiset, with zero unparsed and zero errors. I could not falsify the observed rows, the command identity, the class, the lifetime binding, or a clean parse for this case. However, the same case already passed on the r21 delivered tool `46c82902…` in the existing `oracle-before-new50` receipt. So this green shows that nothing regressed. It does **not** show that F1–F5 were repaired, and it cannot count toward "every original red resolves".

## Sealed truth (read from `oracle/expected.json`, case index 41)

- `expected_kind` is `exact`; `accept_exact_want` is null, which is correct for an exact case; `forbid_observed_commands` and `forbid_commands_any_tier` are both empty; `require_signal` is true; there is 1 cell with reset false.
- `want` (sorted) is the same as `want_input_order`, and both match the raw proposal `w1/proposals/ThreadReuseName.json` (sha `abbf3154…`):
  - `host_mutation | pacman -S r22-reuse-a | observed`
  - `package_query | pacman -Q r22-reuse-b | observed`
- Fixture `inputs/ThreadReuseName.jsonl` has sha `7540c66c…5a096`, which matches the sealed `input_sha256`. Its call id is `ThreadReuseName-0`, and its code equals the proposal cell byte for byte (the runner enforces this).

## Independent semantic reasoning, without trusting the green result

I checked the cited source `w1/sources/SourceThread/threading-v3.14.8.py` (sha `53239096…` matches the cited value). Lines 925–928 store `self._target`, `_args` and `_kwargs` by reference in `__init__`. Lines 1023–1024 have `run()` call `self._target(*self._args, **self._kwargs)`. Line 1082 has `_bootstrap_inner` run `self.run` in the new thread.

- **Lifetime and late binding.** `target=target` is evaluated at each constructor call. `t1` captures `run_install` and `t2` captures `run_query`. Rebinding the module name `target` afterwards does not change either instance. Both `.start()` calls come after the rebind, so a detector that resolves the target at start time would produce `-Q r22-reuse-b` twice and would fail this case. The case therefore genuinely discriminates late binding.
- **Command and class.** Both argv lists are literal. `shlex.join` produces the sealed strings. `pacman -S` is `host_mutation` and `pacman -Q` is `package_query`, matching the r21 convention (`pacman -S r21-thread-run` → `host_mutation`).
- **Evidence tier.** Both targets are visible top-level `def`s that call `subprocess.run(argv)` on their parameter. There is no conditional, opaque, starred or dynamic input, so `observed` is the right tier for both rows, and no lead is warranted.
- **Exact versus uncertain.** Non-daemon threads are joined at interpreter shutdown, so both spawns are reached. The only way they would not run is a `RuntimeError` from resource exhaustion in `start()`. That is outside the declared static scope and is no reason to downgrade the case to uncertain. Because the case is exact, `accept_exact_want` correctly stays null. No uncertainty signal is semantically warranted. With the exact-equality rule, `require_signal: true` is not used for exact cases (`measure.py` lines 752–756), so it is harmless here.
- **Supported form.** "Newly constructed stdlib Thread target/args/kwargs, stored … standard .start, distinct instance target capture" is a claimed exact form in `supported-forms.md`.

**Conclusion:** the expected multiset is correct as sealed, and I found no truth contradiction.

## Mechanism check (delivered `tools/mado-tripwire.py`, read only)

- For the `Assign` statement `t1 = threading.Thread(...)`, `assignment_binding` (lines 1839–1853) builds a `scheduled` record whose `target` is `callable_info(target, bindings, env)`. That is resolved against the bindings in effect at that statement, so it captures construction-time identity. `args` is `literal_value(...)`, evaluated at the same moment. Each constructor call produces its own record, with its own `state` dict.
- The rebind `target = run_query` replaces `bindings['target']` with a new dict (line 1935). It does not mutate the record already captured in `t1`.
- At `t1.start()`, `callable_info` for the attribute (lines 1784–1790) gets the receiver from the statement snapshot taken by `prepare_eval_calls`/`statement_snapshot` (lines 2203–2225). It returns `scheduled_invoke`. `spawn_scan` (lines 2470–2488) then synthesizes the call `<scheduled target>(*literal args)` using the captured target and recurses into the helper body. That body resolves `subprocess` using start-time bindings, which is correct because globals are read when the function is invoked.
- In the refs sweep, a Name passed as an argument to `Thread`/`Timer` is skipped (lines 2731–2734), so the uncalled `def` bodies and the `target=target` references produce no stray leads. The measured output confirms this: `lead_findings` is 0.

## Measurement (the one authorized scanner child)

Command: `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case ThreadReuseName`. The runner exited 0 with empty stderr; the scanner child exited 1, which means findings are present.

| Item | Value |
|---|---|
| Population validated | 57 inputs, 52 proposal files, 106 sealed sources; status `complete`; `integrity_errors` empty |
| Tool sha, before and after | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce`, unchanged |
| Runner / producer | `41b021bb…628c7` / `0270c10b…5600` |
| Expected / population | `b5cd4cf3…4357` / `04616857…86ad` |
| Rows | `host_mutation pacman -S r22-reuse-a observed`, `package_query pacman -Q r22-reuse-b observed` |
| `eval_unparsed` + `unparsed_spawns` | 0 + 0 |
| `pass`, `reasons` | true, [] |
| Scanner file row | path is the fixture, sha `7540c66c…`, both findings carry `tool_call_id` `ThreadReuseName-0` and rules `pacman:-S` / `pacman:-Q` |

The raw receipt is `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC142/result.json` (sha `f956f17c28ded774f40a0f0e52b907a06045d52d2d72aee3fe1c6a22c70ded45`). Next to it are `stdout.raw`, `stderr.raw` (0 bytes), `exit.txt`, and `hashes-before.txt`/`hashes-after.txt`. The tool, runner and fixture hashes were identical before and after. No other scanner runs were made.

## Attacks attempted for this case

| Attack | Result |
|---|---|
| Invented observed row, or an argv promoted from a lead | None. There are exactly 2 observed rows, both true. |
| Lost true command | None. Both start-ordered commands are present. |
| Wrong identity (late binding or collapsing to `-Q` twice) | Not reproduced. Rows are distinct, and the target is captured at construction. |
| Lifetime (rebind leaking into an existing instance) | Not reproduced, and the mechanism is explained above. |
| Conditional target | Not applicable. The cell is straight-line. |
| Clean-looking parse hiding errors | No. Unparsed is 0, there is no scanner error, and stderr is empty. |
| Forbidden commands at any tier | The lists are empty, which is correct for exact truth, so there was nothing to ban. |

## Findings and boundaries (none block this case)

1. **This case is a control, not a repair.** In the existing receipt `evidence/first/oracle-before-new50.json` (sha `73f9dcef…`), the payload's `tool_sha256_before` is `46c82902…`, the r21 delivered tool. That run passed ThreadReuseName with the same two rows and 0 unparsed. The proposal's "discriminating power" text says a late-binding detector would fail this case. That is true in principle, but no measured tool ever failed it. Counting this case toward the repair or "original reds resolve" target would be premature saturation. It is valid only as a guard showing that construction-time binding was not regressed. Impacted axis: C1 operability credit. Smallest correction: when grading, tag ThreadReuseName as a "pre-green control" in the 13/50 → 50/50 delta, and do not count it as one of the resolved reds.
2. **Known label defect, already disclosed.** The outer wrapper field `selected_tool_sha256` in that "before" receipt reads `36fdc459…`, the current tool, while the run actually used `--tool evidence/tool-before.py`. `evidence/first-metadata-correction.json` already records this, and names `tool_sha256_before` as the authoritative field. I treated the payload field as authoritative. Anyone reading only the wrapper would wrongly conclude that the delivered tool scored 13/50.
3. **What this case does not cover:** Thread `.run()` direct calls (F4), `Timer`, aliased `.start`, positional `Thread(None, target, None, args)`, conditional or rebinding-in-branch targets, reusing the instance variable, and persistence across cells. A pass here closes only this one finite form.
4. **Out of scope and not examined:** the C2 audit receipt `audit-after.json` lists `56091de7…` as the actual audit tool, while the fixed C2 identity is `277eced2…`. The file `audit-after-corrected.json` exists, but I did not grade it.

## Scope compared to the current target

This covers only this one sealed exact case on the delivered C1 tool `36fdc459…`. It says nothing about the other 56 cases, the 175-case historical guard, the 1356-fixture removal comparison, the resource recipes, or C2. It is not an admission, a waiver, or a reset of the r19, r20 or r21 rejected-harmed streak.

## Tools

None installed or updated. One capped scanner child, run through the runner. No payload was executed, and no production, fixture or expected file was modified.

Report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC142.md`
