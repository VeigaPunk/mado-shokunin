# TimerRunInline — C1 static-truth proposal (round 22, wave 1)

Seat: `MadoR22.TimerRunInline` · Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` · Independent pre-freeze truth; no detector read, no measurement, no payload execution.

## Artifact

`.ufo/waves/round-22/w1/proposals/TimerRunInline.json`

## Variant

One eval cell:

```python
import subprocess
import threading
def worker(argv):
    subprocess.run(argv)
threading.Timer(1, worker, kwargs={"argv": ["pacman", "-S", "r22-timer-run-inline"]}).run()
```

`threading.Timer(interval, worker, kwargs={argvkey: argv}).run()` as an immediate (unbound-temporary) expression — the F4 scheduled-call family, kwargs-binding lane.

## Expected truth (from Python 3.14.8 semantics only)

| Row | Class | Command | Evidence |
|---|---|---|---|
| 1 | `host_mutation` | `pacman -S r22-timer-run-inline` | `observed` |

`expected_kind: "exact"`; `forbid_observed_commands: []`; `unparsed` expectation: 0.

## Semantic derivation

Vendored CPython v3.14.8 `Lib/threading.py`
(`.ufo/waves/round-22/w1/sources/SourceThread/threading-v3.14.8.py`,
sha256 `5323909624ec2165e70b6d31333e4191b63d383d2dc5a7d7d516a3475ea2b7e3`):

1. `Timer.__init__` (lines 1370–1376) stores `self.function = worker`,
   `self.kwargs = {"argv": ["pacman", "-S", "r22-timer-run-inline"]}` verbatim
   and creates `self.finished = Event()`, initially unset.
2. The `Timer(...)` call is a temporary: no name binds it, so no code can
   reach `cancel()`/`finished.set()` before or during `.run()`.
3. `.run()` on that temporary resolves to `Timer.run` (lines 1382–1386):
   `self.finished.wait(1)` returns False (flag unset), the
   `not self.finished.is_set()` guard therefore passes unconditionally, and
   `self.function(*self.args, **self.kwargs)` calls
   `worker(argv=["pacman", "-S", "r22-timer-run-inline"])` **synchronously in
   the caller thread** after the 1 s wait. `.run()` is a synchronous invoke,
   not a scheduled spawn — same invocation class as `Thread.run`
   (contract: docstring lines 1016–1020, body 1023–1024).
4. Inside `worker`, `argv` binds the literal list;
   `subprocess.run(argv)` deterministically executes
   `pacman -S r22-timer-run-inline` — a package-install attempt →
   `host_mutation`, `observed`.

Command serialization: `shlex.join(["pacman", "-S", "r22-timer-run-inline"])`
= `pacman -S r22-timer-run-inline` (all tokens shell-safe).

Every argument reaching the worker is a source literal (interval `1`,
function a module-level `def` name, `kwargs` a dict literal whose value is a
list literal). Zero unresolved inputs → exactly one observed row, zero
unparsed; no lead or uncertain row is honest.

## Independence / freeze notes

- Authored from `registration.md`, `audit-contract.json`, the vendored
  threading source, and round-21 `residual/FinalBindingReview.md` (F4 rows
  only, lines 90–95, for class/evidence labeling convention). No candidate
  detector source was read; `tools/mado-tripwire.py` untouched; no detector
  or fixture was run.
- Proposals directory was empty at write time; no sibling C1 proposal was
  read, so this variant is independent by construction.
- Marker token `r22-timer-run-inline` is an inert `pacman -S` argument only;
  the cell is scanner input and is never executed (payload inertness is
  identical in kind to the r21 FBR fixtures).

## Distinction from sibling seats (by assignment intent)

- `TimerRun` / `TimerRunAlias`: scheduled-object binding/alias forms; this
  cell is the **inline constructor-expression** form, so the temporary has no
  Name binding at all — `callable_info` must resolve `.run` on a `Call`
  result, not on a scheduled name record.
- `ThreadRun*`: `Timer.run` carries the `finished.wait`/`is_set` gate and
  `function/args/kwargs` fields (not `_target/_args/_kwargs`); truth here
  additionally proves the gate is statically unsatisfiable for a temporary.

## Unknowns

- Whether the repaired detector treats an inline `Timer(...).run()` as an
  observed synchronous invoke is exactly what this frozen expectation tests
  (r21 F4 reports `.run` fell to `unresolved` and emitted nothing).
- The `finished.wait(1)` delay is timing, not identity: the call is reached
  unconditionally; no uncertainty attaches to the row.

## Tools

None installed or updated (vendored source already present; pacman frozen
host-wide). Nothing executed.
