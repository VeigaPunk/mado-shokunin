# ThreadGlobalLate — independent C1 static-truth variant

Seat: `MadoR22.ThreadGlobalLate` · Lane: leaf reviewer, single proposal, no delegation.
Artifact: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/ThreadGlobalLate.json` (3132 B, written this session; validated JSON + `ast.parse` of the cell).

## Variant

Worker references the module-global `command`, which is rebound after `threading.Thread` construction and before `start()`. One eval cell, inert argv markers only:

```python
import subprocess
import threading


def worker():
    subprocess.run(command)


command = ["pacman", "-Q", "r22-tglate-early"]
t = threading.Thread(target=worker)
command = ["pacman", "-S", "r22-tglate-late"]
t.start()
```

## Frozen expectation

- `expected_kind: "exact"` — exactly one row: `host_mutation` `pacman -S r22-tglate-late`, evidence `observed`; zero unparsed demanded by the exact contract.
- `forbid_observed_commands: ["pacman -Q r22-tglate-early"]` — the pre-rebind value is passed to no call; a construction-time namespace snapshot that reports it is wrong on both command and evidence class.

## Static truth (Python 3.14 semantics, no execution)

1. `worker` performs no binding operation on `command`, so the name is a free variable resolved in the module's global namespace (vendored `executionmodel.rst` 92–93, 138–143). "Name resolution of free variables occurs at runtime, not at compile time" (line 322) — the read happens inside `worker()`'s invocation, not at `def` or `Thread` construction.
2. `Thread.__init__` only stores `self._target = worker` (vendored `threading-v3.14.8.py:925`); `start()` arranges `run()` on a new thread (978–979, 1003–1006); `run()` invokes `self._target(*self._args, **self._kwargs)` (1023–1024).
3. Therefore `worker()` executes only at or after `t.start()`, which follows `command = ["pacman","-S","r22-tglate-late"]` in program order, and nothing rebinds `command` afterwards. The observed binding at invocation is unambiguously the late value → `subprocess.run(["pacman","-S","r22-tglate-late"])` → `host_mutation`, `shlex.join` = `pacman -S r22-tglate-late`, `observed` per the r21 thread-key-control convention (literal argv inside an unconditionally started thread body).
4. The rebinding precedes `start()`, so no scheduling race exists; the result is deterministic for any thread interleaving.

## Discrimination and independence

- Complements sibling `CaptureGlobalLate` (closure free variable): this variant places the late-bound global read on the *scheduled-thread* path (`thread_start`), the F4/F5 mechanism, not the factory-capture path (F1–F3).
- A detector that snapshots the caller/module namespace at `Thread(...)` construction reports the forbidden early row; a correct one resolves globals at the start-time invocation and reports the late row. A detector that never follows started workers reports nothing and fails the exact row.
- Authored solely from `FinalBindingReview.md` (F4 mechanism, lines 90–95; observed convention, 58–60 and 99–101) plus the vendored CPython v3.14.8 sources opened by the wave's Source seats. No detector source, detector output, fixture rerun, measurement, or sibling proposal bytes consulted for the expectation.

## Citations verified

- `.ufo/waves/round-22/w1/sources/SourceThread/threading-v3.14.8.py` sha256 `5323909624ec2165e70b6d31333e4191b63d383d2dc5a7d7d516a3475ea2b7e3` — recomputed this session, equals `receipt.json`; lines cited: 925, 978–979, 985–986, 1023–1024.
- `.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-executionmodel.rst` lines cited: 92–93, 138–143, 322.

## Compliance and unknowns

- No production edits, no detector measurement, no payload execution, no package queries, no live probes, no installs, no background jobs. Git untouched. One file authored under my seat path, plus this report.
- Validation performed: proposal parses as JSON; the cell parses via `ast.parse`; the `want` command is exact `shlex.split`/`shlex.join` tokenization of the literal argv. The cell was never executed.
- Unknowns reported honestly: none. Semantics are fully determined by program order; `expected_kind` is `exact`, so no `lead`/unparsed allowance is requested.
- Residual scope: the variant assumes the standard library `Thread` (no subclass `run` override, matching the r21 review's declared not-attacked set). It does not exercise `args`/`kwargs` construction-time evaluation, which r21 already cleared; the global read inside the body is the axis under test.
