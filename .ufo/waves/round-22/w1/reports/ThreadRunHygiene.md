# ThreadRunHygiene — C1 truth proposal report

Seat: `MadoR22.ThreadRunHygiene` · leaf reviewer, no delegation · wave r22 w1, freeze-before-implementation.

## Deliverable

Wrote `.ufo/waves/round-22/w1/proposals/ThreadRunHygiene.json` — one independently specified static-truth C1 variant. No code read beyond citations below, no detector output consulted, nothing executed, no production edits.

## Variant

Same legal synthetic-reserved name used by a direct `.run()` worker — the F4 × F5 intersection:

```python
import subprocess
import threading

__mado_thread_target__ = subprocess.run

def worker():
    __mado_thread_target__(["pacman", "-Q", "r22-runhyg"])

t = threading.Thread(target=worker)
t.run()
```

One eval cell, matching the six-fixture convention of one toolCall per file.

## Truth (static Python 3.14 semantics; not executed)

- `threading.Thread(target=worker)` binds `self._target = worker` at construction (`/usr/lib/python3.14/threading.py:925`, verified on the installed interpreter).
- `t.run()` invokes `self._target(*self._args, **self._kwargs)` **synchronously in the calling thread** (lines 1013, 1024). No `start()`, no new thread.
- Inside `worker`, the bare name `__mado_thread_target__` has no local binding → global load (LEGB) → the module assignment `__mado_thread_target__ = subprocess.run`. The dunder spelling is a legal identifier; it merely collides with the r21 scanner's reserved injection key.
- Call resolves to `subprocess.run(["pacman", "-Q", "r22-runhyg"])`; `shlex.join` → `pacman -Q r22-runhyg`.

**Expectation:** `expected_kind: "exact"`, `want: [{class: package_query, command: "pacman -Q r22-runhyg", evidence: observed}]`, zero unparsed/error counters. `forbid_observed_commands: ["pacman -S r22-runhyg"]` — the mutation spelling of my marker must never appear; any additional fabricated observed row already violates exact matching.

## Why this variant earns its seat

- **F4 coverage** (r21 `thread-run-direct`, sha256 `1cc1188d…`): a `.run()`-scheduled target was silently missed (`unparsed 0`). This fixture requires the direct-invocation path to be followed.
- **F5 coverage** (r21 `thread-key-hygiene`, sha256 `4ea8ccc8…`): the injected `__mado_thread_target__` bindings-map key shadowed a same-named source global, downgrading observed → lead. Under `.run()`, a key-injection repair would reproduce the same collision on this fixture; the parent-requested node-carried fix (carry `mado_resolved` on the synthetic node) resolves it. The alias form `__mado_thread_target__ = subprocess.run` reproduces r21's exact defect mechanism rather than ThreadHygiene's def-form.
- **Independent of siblings:** ThreadRun = plain `.run()` with literal argv arg (no reserved name); ThreadHygiene = `.start()` + reserved-name *function def* (no `.run()`); TimerRun* = Timer path. This is the only seat covering the reserved-name global under synchronous `.run()` invocation.

## Contract compliance

- Inert argv only: `pacman -Q` is a read-only query class marker; never executed — cells are ast-scanner input.
- Git read-only; no lane, fleet, sibling, or host config mutation; no installs, probes, services, or package transactions.
- No detector measurement, no detector-source-derived expectations; rationale cites Python 3.14 stdlib source and r21's public review document only.

## Unknowns / limits

- None blocking. Exactness rests on the established class convention (`pacman -Q` → `package_query`) shared with r21 fixtures and r22 siblings.
- `forbid_observed_commands` is non-empty for defense-in-depth only; truth remains a single exact row.
- Tools installed: none. Report file: `.ufo/waves/round-22/w1/reports/ThreadRunHygiene.md`.
