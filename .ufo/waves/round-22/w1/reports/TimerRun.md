# TimerRun — C1 static-truth proposal report

Seat: `MadoR22.TimerRun` · Lane: leaf reviewer, no delegation · Deliverable: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/TimerRun.json`

## Assignment

Independently specify ONE static-truth C1 variant: stored `threading.Timer(interval, worker, args=(argv,)).run()`. Static source reading only — no production edits, no detector measurements, no payload execution.

## What was written

One-eval-cell proposal, `expected_kind: "exact"`:

```python
import subprocess
import threading


def worker(argv):
    subprocess.run(argv)


argv = ["pacman", "-S", "r22-timer-run"]
t = threading.Timer(1, worker, args=(argv,))
t.run()
```

- `want`: exactly one row — `host_mutation`, `pacman -S r22-timer-run`, `observed`.
- `forbid_observed_commands`: `[]` — the argv is a fully determined module-scope literal; no unparsed or lead outcome is statically defensible, so no forbidden list is needed to express uncertainty.
- JSON validated; the cell parses with `ast`; `shlex.join(["pacman","-S","r22-timer-run"])` = `pacman -S r22-timer-run`, matching `want[].command` byte-for-byte.

## Independent static reasoning (no detector consulted)

Verified against the installed interpreter's own source, `/usr/lib/python3.14/threading.py` (CPython 3.14.8), read-only:

1. `class Timer(Thread)` at line 1361; `__init__` (1370–1376) binds `self.function`, `self.args`, `self.kwargs` at construction and creates `self.finished = Event()` (unset).
2. `t.run()` is a plain synchronous method call on the stored object. `Timer.run` (1382–1386) executes `self.finished.wait(self.interval)`, then — `finished` still unset — calls `self.function(*self.args, **self.kwargs)` **in the calling thread**.
3. `finished` can never be set in this program: `cancel()` (1378–1380) is the only pre-`run` setter, `t` has no other reference, and `run()` itself only sets it *after* the function call. `start()` is never called, so no new thread exists. Interval value is irrelevant to which call is owed.
4. `argv` is bound to a literal list before construction and never rebound → deterministic `subprocess.run(["pacman","-S","r22-timer-run"])` → `host_mutation`, `observed`, zero `eval_unparsed`/`unparsed_spawns`.

## Defect exercised

Round-21 `FinalBindingReview.md` **F4** (Medium, recall): "a scheduled `Thread.run()` (and `Timer.run()`) is never followed" — the r21 `thread-run-direct` fixture produced a silent miss (no row, `unparsed` 0), and the review states `Timer.run()` shares the `.run` path by source. The contract note: "`t.run()` calls the target synchronously in the caller." This variant is the Timer sibling of that counterexample: correct handling owes exactly one observed `host_mutation`; the F4 defect yields zero rows with zero unparsed counters.

## Distinctness from sibling slices (roster-checked)

- `ThreadRun` — `threading.Thread` base class; mine is `Timer` (subclass with `finished`-gate).
- `TimerRunAlias` — `run = timer.run` aliasing + literal kwargs at construction; mine is direct `.run()` + positional `args`.
- `TimerRunInline` — immediate-expression `Timer(1, worker, kwargs={k: argv}).run()`; mine is a stored instance with `args=(argv,)`.

## Scope compliance

- No production reads/edits; only `registration.md`, `audit-contract.json`, r21 `FinalBindingReview.md`, the r21 `thread-run-direct.jsonl` fixture bytes (as data), and `/usr/lib/python3.14/threading.py` line numbers were consulted.
- Nothing executed, no probes, no installs, no pacman transactions, no git writes.
- Unknowns: none for this shape — the call is fully determined statically. Not claimed: absence of other defects, cross-cell behavior, `.start()` semantics, or any detector outcome.

Report: .ufo/waves/round-22/w1/reports/TimerRun.md
