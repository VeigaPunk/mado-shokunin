# ThreadRun — C1 static-truth proposal

Seat: `MadoR22.ThreadRun` (reviewer, leaf). Proposal: `.ufo/waves/round-22/w1/proposals/ThreadRun.json`. Authorization: round-22 attempt-1 recovery (registration.md); prior r19/r20/r21 rejections stand; this is a frozen pre-implementation truth, not admission.

## Variant

Stored `threading.Thread(target=worker, args=(argv,)).run()` — direct synchronous invocation of a scheduled binding through `.run` on the instance held in variable `t`. One inert eval cell; `argv` is a literal list bound before construction. The only spawned command inside `worker` is `subprocess.run(cmd)`.

## Expected (declared before any implementation/measurement)

| Field | Value |
|---|---|
| `expected_kind` | `exact` |
| `want` | `host_mutation` `pacman -S r22-thread-run`, evidence `observed` |
| `forbid_observed_commands` | `[]` |
| unparsed | zero (no `eval_unparsed`, no `unparsed_spawns`) |

Command serialization: `shlex.join(["pacman","-S","r22-thread-run"])` → `pacman -S r22-thread-run`. Class basis: `pacman -S` is the inert host-mutation marker used across r21 fixtures (`pacman -Q` marks `package_query`).

## Static-truth reasoning (Python 3.14.8)

1. `Thread.__init__` binds `self._target=target`, `self._args=args`, `self._kwargs=kwargs` at construction — `/usr/lib/python3.14/threading.py:925-928`. The args tuple object `(argv,)` is fixed at that moment; later rebindings of `argv` (none here) could not retroactively alter it.
2. `t.run()` is an ordinary attribute call. `Thread.run` executes `self._target(*self._args, **self._kwargs)` in the calling thread — `threading.py:1023-1024`. Its docstring (1014-1019): "invokes the callable object passed to the object's constructor as the target argument". No `start()` is involved and no new thread exists; the `finally` refcycle cleanup (1028) runs after the call and does not change semantics.
3. `worker` is a module `def` bound before the `Thread` construction; `argv` is a module literal. So the reached call is `subprocess.run(["pacman","-S","r22-thread-run"])` with a fully determined argv → exactly one `observed` `host_mutation` row, zero unparsed. Any silent absence (the r21 F4 mode), any `lead` downgrade, or any fabricated row fails this exact expectation.

## Relation to r21 findings

- **F4 (the repaired defect):** final-bytes scanner mapped only `.start` on a scheduled binding to `thread_start`; `.run` fell through to `unresolved`, and spawn-attribute leads require a literal argv argument, so the `thread-run-direct` fixture emitted no row with `unparsed` 0 — a silent miss. This proposal pins the correct synchronous-call truth so the miss cannot recur.
- **F5 adjacency:** no `__mado_thread_target__` name appears in this fixture; the reserved-key shadowing path is out of scope here (covered by sibling seats ThreadHygiene/ThreadRunHygiene).
- Distinct from sibling `ThreadRunInline` (immediate `threading.Thread(...).run()` expression, no stored variable) and `ThreadRunAlias` (`run = thread.run` method-alias). This seat's distinguishing shape is the stored instance invoked via `.run` as a plain method call.

## Independence and inertness

Expectation derived from installed CPython 3.14.8 source and Python call semantics only; no detector code read, no detector run, no payload executed (cells are parse-only scanner input). Payload contains no live action: only the inert `pacman -S r22-thread-run` marker inside unparsed-as-data source. `forbid_observed_commands` is `[]` because `expected_kind: exact` already fails on any extra, substituted, downgraded, or fabricated row; adding token strings would add no axis.

## Scope limits

- Does not claim `Thread` subclass `run` overrides, `Timer`, alias `.run`, cross-cell persistence, or `**kwargs` variants — each is a sibling seat's cell.
- No tools installed or updated; no installs needed. No package queries, transactions, probes, or service access performed. Git untouched.
- `lsp` device unavailable for this artifact format; evidence is direct file reads plus `grep` on `/usr/lib/python3.14/threading.py`.
