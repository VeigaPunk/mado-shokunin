# FalsifyC139 — C1 case ThreadConstructorCapture (author-lane advisory critic)

Verdict: **agree**. This is advisory only and grants no admission. It is not non-author falsification, and it closes no defect family beyond this exact source shape.

## Identities (checked before and after the run; no drift)

| item | sha256 |
|---|---|
| C1 tool `tools/mado-tripwire.py` | 36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce (= fixed identity; runner before/after equal) |
| oracle `expected.json` | b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357 (= fixed identity) |
| `expected.sha256` pin file | 7cc4aae9017a157faea3d66e47b5bc0181ec9093a3160d1c41d8e2e93b1567f6 |
| runner `oracle/measure.py` | 41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7 |
| producer `oracle/assemble.py` | 0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600 |
| fixture `inputs/ThreadConstructorCapture.jsonl` | 491c627ae11220b31eb9951a016a956f5b8a105f1a45df02538bf65428b9720c (= sealed `input_sha256`) |
| proposal `w1/proposals/ThreadConstructorCapture.json` | 10fe568f07cd4e1c24d2659a76d4d0c61bf359a369f76c76a5a44d89fb8cc53e |
| population | 046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad |
| truth seal | 47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4 |
| pinned CPython `w1/sources/SourceThread/threading-v3.14.8.py` | 5323909624ec2165e70b6d31333e4191b63d383d2dc5a7d7d516a3475ea2b7e3 (= receipt) |

The runner validated the full population both before and after the case: 106 sealed source files, 52 proposal files and 57 inputs. It ran one case. `integrity_errors` is empty.

## Sealed case (`cases[38]`)

- `expected_kind` is `exact` and `accept_exact_want` is `null`, so the uncertain/accept-alternate branch does not apply. `require_signal` is `true`, and the `observed` want row satisfies it.
- `want` is exactly `[{host_mutation, "pacman -S r22-ctor", observed}]`. `want_input_order` is the same row, identical to the proposal's raw `want`.
- `forbid_observed_commands` is `["pacman -Q r22-ctor-late"]`. `forbid_commands_any_tier` is `[]`, with no addenda and no correction.
- The fixture has one inert eval cell with `reset=false`. Its call id is `ThreadConstructorCapture-0`, and its code is byte-equal to the proposal cell (the runner enforces both).

## Independent semantic reasoning (static; the payload was never executed)

1. `threading.Thread(target=worker, args=(cmd,))` evaluates `(cmd,)` at the call. The tuple holds the list object that `cmd` names at that moment: `["pacman","-S","r22-ctor"]`. The pinned `Thread.__init__` (lines 880-881 signature, 925-928) stores `self._target = target` and `self._args = args` by reference, with no copying and no name capture.
2. `cmd = ["pacman","-Q","r22-ctor-late"]` rebinds the module name to a new list object (simple_stmts.rst lines 83-84). It does not mutate the tuple's element, and nothing mutates the first list.
3. `t.start()` → `_bootstrap_inner` → `self._context.run(self.run)` (line 1082) → `self._target(*self._args, **self._kwargs)` (lines 1023-1024) → `worker(["pacman","-S","r22-ctor"])` → `subprocess.run(argv)`. That call has a list argv and no shell.
4. The thread is non-daemon by inheritance, and its start comes after the rebinding, so there is no race over the captured object.
5. The result is exactly one spawn, with command `shlex.join` = `pacman -S r22-ctor`. `pacman -S` is a sync/install, so the class is `host_mutation`, and the evidence is `observed` because the literal argv is statically determined.
6. The decoy `pacman -Q r22-ctor-late` is never passed to any callable. A row naming it at any tier would be invented, and would also break exact multiset equality.
7. Every argument is literal, so zero unparsed is the right truth. Requiring uncertainty here would be wrong.

I agree with the sealed truth on class, command, evidence, cardinality and the zero-error requirement.

Residual uncertainty is environmental, not static, and does not overturn the exact truth:
- A module named `threading` or `subprocess` could shadow the stdlib on the kernel's `sys.path`.
- `start()` could raise `RuntimeError` if thread creation fails.

The oracle's static model properly excludes both, consistent with every other case.

## Actual measurement (the only scanner run; one child, 384 MiB, 15 s)

- Invoked: `python3 -I .../oracle/measure.py --tool .../tools/mado-tripwire.py --case ThreadConstructorCapture`. Outer exit 0, stderr empty, status `complete`, totals 1/1.
- The runner recorded its own argv as `sys.executable` plus `sys.argv`, so `-I` is absent from that field. This is cosmetic.
- Scanner child argv: `/usr/bin/python3 -I -c <WRAPPER> .../tools/mado-tripwire.py .../inputs/ThreadConstructorCapture.jsonl`. Exit 1, which the runner accepts as "findings present". stderr empty, no `scanner_error`.
- Rows: `[{host_mutation, "pacman -S r22-ctor", observed}]`, rule `pacman:-S`, tool_call_id `ThreadConstructorCapture-0`.
- File row: `eval_calls=1`, `eval_unparsed=0`, `unparsed_spawns=0`, sha256 equal to the sealed digest.
- `pass=true`, with no reasons.

## Falsification checks for this case

| attack | outcome |
|---|---|
| false observed/lead decoy (`-Q r22-ctor-late`) | absent at both tiers |
| lost true command | present, exactly one |
| wrong identity | target resolves at construction to the `worker` FunctionDef; args are a construction-time value snapshot |
| lifetime | correct: the args snapshot is taken in `assignment_binding` at the `Thread(...)` call, not re-resolved at `.start()` |
| conditional target | not present in this case |
| parsed-clean ambiguity | the clean counters come with a real observed row, so this is not an empty "clean" scan |

How the tool gets this right (read-only source inspection):
- At construction, `assignment_binding` (`tools/mado-tripwire.py` 1841-1853) records a `scheduled` binding. That binding holds `target=callable_info(target)` plus `args=literal_value(arguments, env)`, evaluated in the construction env. The later rebinding of `cmd` creates a new value in `env`, and the snapshot keeps the old list.
- At `.start()`, `callable_info` (1788-1790) returns `scheduled_invoke`. `spawn_scan` (2470-2489) then replays `worker(*snapshot)` once, using the shared `state["done"]` flag.
- Before replaying, it checks `mutated_literal(arguments, cenv)` at the start site. The check is by object id, so in-place mutation after construction becomes unparsed rather than a stale observed row. Rebinding does not trip it.
- The Thread-parent reference skip (2733-2734) stops the `worker` body from also being swept as a free reference. That sweep would otherwise add a parameter-argv lead and break the exact multiset.

## Scope and boundaries (no claim beyond this case)

This green certifies only one shape:
- a single cell;
- a module-level Name-bound list wrapped in a literal tuple and passed as the `args=` keyword;
- a plain name rebinding between construction and start;
- `.start()` on a stored instance.

It does not exercise:
- in-place mutation of the captured list before `.start()` (the mutated_literal path; supported-forms says no stale observed row and allows uncertainty);
- positional `Thread(None, worker, None, (cmd,))`;
- `kwargs=` capture;
- rebinding `worker` after construction;
- cross-cell persistence;
- `.run()` and aliased start;
- Timer, cancel or repeated start;
- subclasses that override `run`.

Those belong to other cases or remain outside the exact-result support declared in `supported-forms.md`. Per the contract, this one passing case is not evidence that the F1/F4 families are closed. Prior r19/r20/r21 rejected-harmed receipts and the streak are unaffected.

Counterexample: none found for this case. Smallest safe correction: none required.

## Receipts

`.ufo/waves/round-22/w2/receipts/FalsifyC139/`:
- `result.json`: sha256 614ac87c32e5edbc512058365ebdaf937b2de534f552cf3ed8c932a789b2862d. Holds argv, exit, stdout and stderr for both the runner and the scanner child, plus all hashes.
- `raw-stdout.json`: sha256 53854292fb0449e660064275f7659293f1ac8791ef6b5f10e9e71bbfb4b028e2.
- `raw-stderr.txt`: empty.
- `raw-exit.txt`: `0`.
- `hashes-before.txt` and `hashes-after.txt`: identical.

Additional scanner runs: 0. New probes: 0. Installs/updates: none. No production, fixture, expected or proposal edits were made.

Report: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC139.md
