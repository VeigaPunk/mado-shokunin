# FalsifyC143 — C1 case ThreadRun (author-lane advisory, NOT admission)

**Verdict: AGREE** for this one sealed case on delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. The scanner's complete row multiset equals the independently derived truth, and both unparsed counters are zero. This is bounded static-source-shape agreement on one fixture. It is not proof of Python semantics, does not close family F4, and grants no admission. Outside-lane falsification is still required.

## Identities (checked before and after; no drift)

| artifact | sha256 |
|---|---|
| `tools/mado-tripwire.py` (C1) | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` (matches fixed identity) |
| `oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` (matches fixed identity) |
| `oracle/expected.sha256` | `7cc4aae9017a157faea3d66e47b5bc0181ec9093a3160d1c41d8e2e93b1567f6` |
| `oracle/measure.py` (runner) | `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7` (equals `runner_sha256` in expected) |
| `oracle/assemble.py` (producer) | `0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600` |
| `oracle/inputs/ThreadRun.jsonl` | `143d2a4f183586d979cede3766a547ffe180593dfe07fba9139c8fe1f72e0e69` (equals sealed `input_sha256`) |
| proposal `w1/proposals/ThreadRun.json` | `78e7aeb758929a30e33d2a794d7c86c62373b554cd5d9f574685f7fc23cceb0f` (verified by the runner) |
| population | `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad` |
| truth seal | `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4` (106 sources verified) |
| CPython `/usr/lib/python3.14/threading.py` (3.14.8) | `5323909624ec2165e70b6d31333e4191b63d383d2dc5a7d7d516a3475ea2b7e3` |

The C2 tool `tools/mado-evidence-audit.py` hash is `277eced2…8fca`, matching its fixed identity. This seat did not exercise C2.

## Sealed case

- Kind is `exact`. Group is `proposal`. There is one cell, with `cell_reset=[false]`. The case has no addenda and no correction, and `accept_exact_want` is null.
- `want`, which equals `want_input_order`, is `[{host_mutation, "pacman -S r22-thread-run", observed}]`.
- `forbid_observed_commands` and `forbid_commands_any_tier` are both empty. `require_signal` is true, but the exact branch of `evaluate` does not consult it.
- The source cell is:

```python
import subprocess
import threading

def worker(cmd):
    subprocess.run(cmd)

argv = ["pacman", "-S", "r22-thread-run"]
t = threading.Thread(target=worker, args=(argv,))
t.run()
```

## Independent semantic truth (derived before reading the tool output)

- **Construction.** `Thread.__init__` stores `self._target = target`, `self._args = args` and `self._kwargs = kwargs` at threading.py lines 925, 927 and 928. `kwargs=None` becomes `{}`. The proposal's citation of lines 925–928 is accurate.
- **Run.** `t.run()` is an ordinary synchronous method call. `Thread.run` (line 1013) calls `self._target(*self._args, **self._kwargs)` at line 1024, in the caller's thread. There is no `start()`, no new thread and no race.
- **Arguments.** `argv` is a module-scope literal list bound before construction. It is never rebound or mutated, so `worker(["pacman","-S","r22-thread-run"])` runs `subprocess.run` with a fully determined argv.
- **Serialization.** `shlex.join` gives `pacman -S r22-thread-run`. `pacman -S` is a host mutation.
- **Truth.** Exactly one observed `host_mutation` row, with zero `eval_unparsed` and zero `unparsed_spawns`. Exact no-uncertainty is the correct expectation because nothing is dynamic. A lead or a positive unparsed counter would be a wrong evidence tier, not acceptable caution.
- **Lifetime edge, not triggered here.** In the `finally` block (line 1028), `run()` deletes `_target`, `_args` and `_kwargs`. A second `t.run()` would raise `AttributeError`. A later `t.start()` would launch a thread whose `run` raises before any spawn. So "at most one execution per Thread object" is semantically right.

## Measurement (the only scanner run this seat made: one child, 384 MiB, 15 s)

- Command: `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --case ThreadRun`
- The runner exited 0, with `status=complete`, totals 1/1 and empty `integrity_errors`. Full-population validation passed before and after the run: 57 inputs, 52 proposals and 106 sealed sources.
- The scanner child exited 1, which means findings were present. The runner accepts exit 0 or 1. stderr was empty and `scanner_error` was null.
- **Actual rows:** `[{"class":"host_mutation","command":"pacman -S r22-thread-run","evidence":"observed"}]`. The row has `rule` `pacman:-S`, `tool_call_id` `ThreadRun-0`, `line` 1, and its file is the sealed fixture path.
- The file row reports `eval_unparsed=0`, `unparsed_spawns=0` and `eval_calls=1`. Its sha256 equals the sealed input digest.
- The receipt is `.ufo/waves/round-22/w2/receipts/FalsifyC143/result.json` (sha256 `bec93208c20e7a5319b9266e0c005636d608213f2ef58e2172d86b98d419cbb4`). It holds argv, exit codes, verbatim stdout and stderr, and the before/after hashes. The raw `stdout.raw` and `stderr.raw` files sit beside it.

## Falsification attempts for THIS case

| attack | result |
|---|---|
| False observed row, or a lead where a definite command exists | None. There is exactly one row, at the correct observed tier. |
| True command lost (the r21 F4 silent miss) | Not reproduced. The `.run` on a scheduled binding maps to `scheduled_invoke` (tripwire lines 1788–1790), which replays the target with literal args (2470–2486). |
| Duplicate row from the `worker` body also being swept as a referenced callable | None. The refs sweep skips `Thread`/`Timer` constructor arguments (2731–2734), and the multiset shows exactly one row. |
| Wrong identity (class, command, argv0, call id, file digest) | All match the truth and the sealed fixture. |
| Lifetime: args captured at construction versus read at invoke | `args` is folded at construction (`literal_value`, line 1852). The tuple holds the same env list object, so `mutated_literal` at the invoke site (1478) could still detect a later in-place mutation. Neither mutation nor rebinding occurs in this case, so no stale-command risk is exercised. |
| Conditional target | Not present in this case. |
| Parsed-clean ambiguity (zero unparsed hiding an unresolved spawn) | None. Every value is determined, and the exact branch requires `unparsed == 0` as well as an equal multiset. |
| F5 structural hygiene on this path | The synthetic callee is `ast.Name(id="<scheduled target>")` carrying `mado_resolved` (2480–2481). That id is not a legal Python identifier and is not inserted into the `bindings` namespace. It cannot collide with any legal source name. |

The two uncertain-only checks do not apply to this case. The any-tier forbidden-argv list is empty, so there is nothing to forbid. The case is exact, so `accept_exact_want` (an alternative accepted multiset) and real uncertainty do not arise. A lead or unparsed output would fail, which is the correct strictness.

## Scope and uncertainty boundaries

- This agreement covers one straight-line, module-scope, `t.run()` form. The following sibling forms were not exercised by this seat:
  - **Run variants:** inline `Thread(...).run()`, aliased `run`, and the `Timer.run` variants.
  - **Repeated or cancelled schedules:** repeated run (CX7), Timer cancel (CX6), and a closure as the Thread target (CX8).
  - **Capture forms:** constructor capture (`ThreadConstructorCapture`), late global (`ThreadGlobalLate`), and hygiene and name reuse.
- The `state` dict that holds the done/cancelled flags is shared only through shallow copies. If any cross-cell or `binding_env` snapshot path deep-copied a scheduled binding, a repeated `run` could be reported twice. That risk lies outside this case and is untested by this seat; it is an [INFERENCE] from source reading, not an observed defect.
- The original r21 `thread-run-direct` red (no row, unparsed 0, on the pre-r22 tool) remains source authority. It was not rerun with the old tool.
- Prior r19/r20/r21 rejected-harmed receipts and the three-rejection streak are unaffected. This green result is author-lane advisory evidence only, not non-author admission. L1 keeps integration and planning authority.

## Counterexample, evidence, impacted axes, smallest safe correction

- **Counterexample:** none found for ThreadRun.
- **Evidence:** the receipt above.
- **Impacted axes:** C1 operability (F4 recall), positive for this one form only. No harm observed.
- **Correction:** none required for this case.

No installs, no production, fixture or expected edits, no delegation, and one scanner child only.

Report: .ufo/waves/round-22/w2/reports/FalsifyC143.md
