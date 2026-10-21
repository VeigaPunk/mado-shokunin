# TimerRunAlias — C1 static-truth proposal: `timer.run()` with literal kwargs at construction

Seat: `MadoR22.TimerRunAlias` · Wave: round-22 w1 · Mode: source-only proposal. No production edits, no detector measurements, no payload execution. Frozen independently of detector results, per registration C1.

## Deliverable

`.ufo/waves/round-22/w1/proposals/TimerRunAlias.json` — one eval cell, `expected_kind: "exact"`, one `want` row, empty `forbid_observed_commands`.

## Variant shape

```python
import subprocess
import threading

def worker(argv):
    subprocess.run(argv)

timer = threading.Timer(0, worker, kwargs={"argv": ["pacman", "-Q", "r22-timer-run-alias"]})
timer.run()
```

Single cell; one inert `subprocess.run` argv; `pacman -Q` marker only. The cell is never executed — it is ast-scanner input.

## Static truth (Python 3.14 semantics)

1. `threading.Timer.__init__` binds `function=worker`, `args=[]`, `kwargs={"argv": [...]}` at construction (Lib/threading.py v3.14.8, lines 1370–1376; args/kwargs storage 927–928).
2. `timer.run()` is synchronous in the calling thread: `finished.wait(0)` returns immediately; `finished.is_set()` is False (no `cancel()` exists in the program); the guarded call `self.function(*self.args, **self.kwargs)` fires (lines 1382–1386).
3. `worker(argv=["pacman", "-Q", "r22-timer-run-alias"])` calls `subprocess.run(["pacman", "-Q", "r22-timer-run-alias"])`. `shlex.join` of the tokens is `pacman -Q r22-timer-run-alias`.

Exact expectation: one `package_query` observed row `pacman -Q r22-timer-run-alias`; zero host_mutation rows; `eval_unparsed` 0 and `unparsed_spawns` 0 implied by "exact".

## Why this variant

- Attacks the **F4-open sibling**: r21 FinalBindingReview (lines 90–95) found scheduled `Thread.run()` unfollowed and stated `Timer.run()` shares the path by source, unreprobed. This is a `Timer.run()` instance with **kwargs at construction** — a distinct supported form from the r21 `args=`-tuple fixture (`thread-run-direct`, sha256 `1cc1188d…`).
- Literal kwargs at construction are the correct binding moment (W2 repair AtkCallbackBoundArgs covers kwargs literal invocation; FinalBindingReview line 134 marks it repaired for `.start`), so kwargs exercise the repaired binding machinery on the still-open `.run` dispatch.
- `interval=0` is irrelevant to argv truth — `run` invokes the function synchronously regardless of scheduling.

## Independence

Truth derived only from pinned CPython source (tag v3.14.8, ls-remote `992560c2…`, archived copy under `w1/sources/SourceThread/`) and the r21 residual review's defect statement. No candidate detector code was read; no scan was run.

## Unknowns reported

- Whether the repaired `.run` path routes through the same kwargs-binding machinery as `.start` is a detector question, outside this proposal; the *truth* is exact regardless.
- `Timer.run`'s `finished` event: vacuously unset here since no `cancel()`/`set()` call exists; a variant introducing cancellation would be `uncertain`, and this fixture deliberately excludes it.

## Tools

None installed or updated. No package queries, probes, or subprocess jobs run; payload bytes were syntax-checked with `ast.parse` only (never executed).

## Addendum — shape correction (`TimerRunAliasActual`)

The assignment specified the alias form `run = timer.run; run()`; the first delivery above used the direct call `timer.run()`. The kwargs-at-construction axis was correct, but the callable-identity axis (invoking through a stored bound-method alias rather than an attribute call site) was missing — reviewer `MadoR22` flagged the mismatch before seal. Corrected per instruction, original proposal retained unchanged as a separate case.

New deliverable: `.ufo/waves/round-22/w1/proposals/TimerRunAliasActual.json`, marker `r22-timer-run-alias-actual`:

```python
import subprocess
import threading

def worker(argv):
    subprocess.run(argv)

timer = threading.Timer(0, worker, kwargs={"argv": ["pacman", "-Q", "r22-timer-run-alias-actual"]})
run = timer.run
run()
```

**Static truth (unchanged axis, added alias step).** `run = timer.run` loads the attribute on a module-local `Timer` instance, yielding a bound method whose `__self__` is `timer` (Python 3.14 bound-method semantics). `run()` therefore executes `Timer.run(timer)` synchronously: `finished.wait(0)` returns at once, `is_set()` is False (no `cancel()` anywhere), so `self.function(*(), **self.kwargs)` → `worker(argv=["pacman","-Q","r22-timer-run-alias-actual"])` → `subprocess.run` with that argv. `shlex.join` gives `pacman -Q r22-timer-run-alias-actual`. Expectation: exactly one `package_query` **observed** row; `expected_kind: "exact"`.

Both cases now stand for seal: `TimerRunAlias` (direct `timer.run()`) and `TimerRunAliasActual` (aliased `run = timer.run; run()`), each a distinct supported `.run` dispatch shape on the F4-open path with literal construction-time kwargs.
