# FalsifyC140 — C1 case ThreadGlobalLate (author-lane advisory falsification)

Seat: `MadoR22.FalsifyC140` · leaf, no delegation · revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`.
Scope: this one sealed case against the current target `tools/mado-tripwire.py`. Advisory attack only; **no admission grant**, not a non-author judgment. L1 keeps planner/integration authority.

## Verdict: AGREE (no counterexample found for this case)

The sealed expectation is semantically right. The tool's output matches it exactly, and it gets there through the mechanism the case is designed to test, not by accident.

## Identities (before = after, no drift)

| artifact | sha256 |
|---|---|
| `tools/mado-tripwire.py` (C1) | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` (fixed identity ✓) |
| `.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` (fixed identity ✓) |
| `.ufo/waves/round-22/oracle/measure.py` (runner) | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` (= `runner_sha256` sealed in expected) |
| `.ufo/waves/round-22/oracle/inputs/ThreadGlobalLate.jsonl` | `e6559cdb31c82459501954236479bace6112e558b9431d73a4ccd8afd9fdd86c` (= case `input_sha256`) |
| proposal `w1/proposals/ThreadGlobalLate.json` | `a374fec705be81a0b7a574540500f3b4ece5173dbb68a57fdc53bdbcbb5c5b4c` (runner-verified) |
| producer `assemble.py` | `0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600` |
| population | `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad` |

The runner checked the whole population before and after the run: 106 sealed sources, 52 proposal files and 57 inputs, with `integrity_errors: []`. It ran exactly one case.

## Sealed case (expected.json `cases[39]`)

- `expected_kind: exact`, `accept_exact_want: null`, `forbid_commands_any_tier: []`, `require_signal: true`, no addenda, one cell, `reset: false`.
- `want` = `want_input_order` = the original proposal's `want`: `[{host_mutation, "pacman -S r22-tglate-late", observed}]`.
- `forbid_observed_commands: ["pacman -Q r22-tglate-early"]`.
- The rationale and source are byte-identical to the original proposal (the runner validates this). There is no normalization drift away from the raw truth.

Cell (inert, never executed):

```python
def worker():
    subprocess.run(command)
command = ["pacman", "-Q", "r22-tglate-early"]
t = threading.Thread(target=worker)
command = ["pacman", "-S", "r22-tglate-late"]
t.start()
```

## Independent semantic derivation

1. **Lifetime.** `worker` never binds `command` (no parameter, assignment, `global` or `nonlocal`), so `command` is a module-global free name. It is looked up when `worker()` runs, not when `def` or `Thread(...)` runs.
2. **Callable identity.** `Thread.__init__` stores only `_target = worker`, and `args`/`kwargs` default to empty. The target is the function object itself, with no captured value of `command`.
3. **Scheduled call.** `worker` runs only through `start()` → `run()` → `_target()`. That happens on or after line `t.start()`, which comes after the late rebind in program order. Nothing rebinds `command` after `start()`, and this is the only cell, so no later cell can rebind it either. The read is therefore deterministic under every thread interleaving: there is no race and no conditional target.
4. **Command identity.** The argv is a literal list, so `shlex.join` gives `pacman -S r22-tglate-late`, which classifies as `host_mutation`.
5. **Evidence tier.** The worker is started unconditionally and its argv is literal, so the correct tier is `observed`, not `lead`.
6. **No real uncertainty.** `exact` is the correct kind. Expecting zero unparsed rows is correct, and `accept_exact_want` should be null.
7. **Forbidden rows.** The early value `pacman -Q r22-tglate-early` reaches no call. Reporting it as observed would be a stale construction-time snapshot, wrong in both command and class.

   Leaving `forbid_commands_any_tier` empty is defensible. Even a lead row for the early command would still fail this exact case, because the case compares the complete row multiset. So the any-tier ban is already implied for this case.

## Actual rows (one scanner run, receipt `w2/receipts/FalsifyC140/result.json`)

- Runner exit `0`, `status: complete`, `totals: 1/1`. The scanner child exited `1` (findings present, an allowed exit code), and stderr was empty.
- `got_rows`: `[{host_mutation, "pacman -S r22-tglate-late", observed}]`. The scanner also reported `rule: pacman:-S` and `tool_call_id: ThreadGlobalLate-0`.
- `unparsed = 0` (`eval_unparsed 0`, `unparsed_spawns 0`), and the file digest matched the sealed input.
- The full multiset equals `want`, there are zero error counters, and the forbidden observed command is absent.

### Checks against each failure mode

| failure mode | result |
|---|---|
| false observed row | none |
| false lead row | none |
| true command lost | not lost |
| wrong identity (class, command or tool call) | correct |
| stale lifetime (early value reported) | not reported |
| conditional or wrong target | n/a |
| parsed-clean ambiguity | none |

## Why green is mechanism-aligned (candidate path read, not executed)

Code reference: `tools/mado-tripwire.py`.

- At lines 1840–1853, `assignment_binding` turns `Thread(target=worker)` into `{"kind": "scheduled", "target": callable_info(worker)}`. That is a `helper` reference to the function node, not a snapshot of its free names. `args`/`kwargs` are evaluated at construction, which matches CPython.
- At lines 1784–1790, `t.start` resolves to `scheduled_invoke`.
- At lines 2470–2486, `spawn_scan` builds the invocation with `cenv = call_env[id(start_call)]`.
- At lines 2221–2225, that environment is the per-statement snapshot taken at the `t.start()` statement, where `command` is the late literal. The helper body is then scanned under that environment, so the global is read when the thread is invoked. This matches the supported-forms rule "globals are read at invocation" for newly constructed stdlib `Thread` with a stored `.start`.

A tool that snapshotted the environment at `Thread(...)` construction would emit the early row and fail the forbidden check. One that never followed the started worker would emit nothing and fail the exact row. Both naive defects are therefore discriminated by this case.

## Uncertainty boundary (not exercised, not claimed)

- **[INFERENCE] Rebind after start.** If `command` were rebound *after* `t.start()` without a `join()`, the thread's read would race. In that variant the same start-statement snapshot would emit the pre-start value as `observed`, but supported-forms says races must not become an invented or stale observation.

  That variant is not this case and is not in my assignment. I ran no probe for it. It is a candidate for a separate sealed boundary case, not a defect against ThreadGlobalLate.
- **Out of scope by the declared exclusions.** Subclasses that override `run`, a `Thread` alias outside the `threading` path, and multi-cell rebinding between `start` and thread execution are not covered by this green.
- **Scope of this green.** It closes only this finite static source shape. It is not general Python thread semantics, and it is not desktop clearance.

## Compliance

- Exactly one authorized scanner child ran, through the runner's 384 MiB / 15 s cap. Fixture code and printed commands were never executed.
- No production, fixture, expected or proposal edits. I wrote only this report and `w2/receipts/FalsifyC140/`, which contains `result.json`, `stdout.json`, `stderr.txt`, `exit.txt` and `hashes-{before,after}.txt`.
- I did not rerun the old r21 tool. The prior r19/r20/r21 red receipts and the streak are untouched.
- No installs or updates.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC140.md
