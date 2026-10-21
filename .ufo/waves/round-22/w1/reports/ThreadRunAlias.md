# ThreadRunAlias — C1 static-truth proposal

Seat: `MadoR22.ThreadRunAlias` (leaf, no delegation). Proposal written: `.ufo/waves/round-22/w1/proposals/ThreadRunAlias.json`. Authorization: round-22 attempt-1 recovery (`registration.md`); prior r19/r20/r21 rejections remain authoritative — this frozen pre-implementation truth is not admission.

## Variant

One inert eval cell. `run = thread.run` binds a bound-method alias to the module name `run`; the caller then rebinds the global `command` (a new list object, not a mutation of the old one) and finally invokes `run()`. The only spawned command lives inside `worker`, which loads the global `command` at call time.

```python
import subprocess
import threading

command = ["pacman", "-Q", "r22-tralias-stale"]

def worker():
    subprocess.run(command)

thread = threading.Thread(target=worker)
run = thread.run
command = ["pacman", "-S", "r22-tralias-live"]
run()
```

## Expected (declared before any implementation/measurement)

| Field | Value |
|---|---|
| `expected_kind` | `exact` |
| `want` | `host_mutation` `pacman -S r22-tralias-live`, evidence `observed` |
| `forbid_observed_commands` | `["pacman -Q r22-tralias-stale"]` |
| unparsed | zero (`eval_unparsed` 0, `unparsed_spawns` 0) |

Serialization: `shlex.join(["pacman","-S","r22-tralias-live"])` → `pacman -S r22-tralias-live`. Class convention: `pacman -S` is the inert host-mutation marker, `pacman -Q` the inert package-query marker, matching r21 fixture conventions.

## Static-truth reasoning (Python 3.14.8, semantics only)

1. `Thread.__init__` binds `self._target`, `self._args`, `self._kwargs` at construction — `/usr/lib/python3.14/threading.py:925-928` (verified by direct read). `worker` takes no parameters, so the stored args tuple is empty and immutable by later statements.
2. `run = thread.run` performs one attribute load producing a bound method and binds it to the global `run`. The alias dispatches to `Thread.run` on that fixed instance; rebinding `command` afterward cannot reach it.
3. `command = [...]` rebinds the module-global name to a new list object. The earlier `['pacman','-Q','r22-tralias-stale']` list becomes unreachable; it is not mutated.
4. `run()` → `Thread.run` executes `self._target(*self._args, **self._kwargs)` synchronously in the calling thread — `threading.py:1013-1024`, docstring "invokes the callable object passed to the object's constructor". No `start()`, no new thread.
5. Inside `worker`, `command` has no local binding → global load resolved at call time → the post-rebinding list. Reached call: `subprocess.run(["pacman","-S","r22-tralias-live"])` → exactly one observed `host_mutation` row, zero unparsed.

## Failure modes pinned

- **Stale-row fabrication:** a scanner that snapshots the module env at Thread construction or alias time, then follows `worker` under that env, reports observed `pacman -Q r22-tralias-stale` — wrong command and wrong class. Explicitly forbidden.
- **Silent miss:** the r21 F4 defect — `.run` on a scheduled binding fell through to `unresolved` and spawn-attribute leads need a literal argv argument, so nothing was emitted. The `run = thread.run` alias adds indirection on top of F4: a scanner that cannot propagate callable identity through the assignment `run = thread.run` loses the row entirely, which fails `exact`.
- **Lead downgrade:** the argv is fully determined; no uncertainty exists, so a `lead` evidence label fails.

## Relation to r21 findings and siblings

- F4 (FinalBindingReview.md lines 90-96): `thread-run-direct` fixture emitted no row, `unparsed` 0. This proposal extends the recall to the method-alias shape plus call-time global rebinding.
- F5 not exercised: no `__mado_thread_target__` name appears.
- Distinct shapes: `ThreadRun` = stored instance `.run()` with args tuple and no rebinding; `ThreadRunInline` = immediate `threading.Thread(...).run()` expression; `ThreadGlobalLate` = global-rebinding without the alias; this seat = alias + global rebinding combined. No shared edits; expectations frozen independently.

## Independence and inertness

Expectation derived from installed CPython 3.14.8 stdlib source (read statically) and Python call/name-resolution semantics only. No detector code read, no detector run, no payload executed — cells are parse-only scanner input. Payload contains only inert `pacman -S`/`-Q` marker strings inside unparsed-as-data source; no external actions.

## Unknowns and scope limits

- Exact single preferred result declared; no alternate truth claimed. `forbid_observed_commands` lists the stale decoy as defense-in-depth even though `exact` already fails on any extra/fabricated row.
- Does not claim: `Thread` subclass `run` overrides (threading.py docstring notes inherited methods unresolved), `Timer.run` alias, cross-cell binding persistence, `**kwargs` thread construction, or detection of alias chains beyond one level.
- No tools installed or updated; none needed. No package queries/transactions, live probes, services, or compositor access. Git untouched. `lsp` device unavailable for this artifact format; verification is direct file reads plus `grep` on `/usr/lib/python3.14/threading.py` (line numbers confirmed: 925-928, 1013-1024).
