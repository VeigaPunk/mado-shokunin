# CaptureTwoInstances — C1 truth proposal

Seat: `MadoR22.CaptureTwoInstances` · Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` · Wave: round-22 w1.
Authored artifact: `.ufo/waves/round-22/w1/proposals/CaptureTwoInstances.json`. Independent static-truth proposal; no production edits, no detector reads, no measurements, no payload execution.

## Variant

One eval cell. Factory `make_runner(argv)` returns `run` closing over the per-call `argv` cell. The module caller passes the same name `conf` to two factory calls, rebound between calls so each creation captures a different literal argv, then performs a third rebind of `conf` before invoking both closures:

1. `conf = ["pacman","-S","r22-ti-a"]`; `first = make_runner(conf)` — first closure's cell holds the a-list.
2. `conf = ["pacman","-Q","r22-ti-b"]`; `second = make_runner(conf)` — second closure's cell holds the b-list.
3. `conf = ["pacman","-Q","r22-ti-c"]` — third caller rebind; touches only the module name, neither cell.
4. `first()`; `second()` — invoked after the rebind.

## Expected (exact)

| Order | class | command | evidence |
|---|---|---|---|
| 1 | host_mutation | `pacman -S r22-ti-a` | observed |
| 2 | package_query | `pacman -Q r22-ti-b` | observed |

`forbid_observed_commands`: `pacman -Q r22-ti-c` — the post-rebind decoy must never appear as observed. Zero unparsed expected: only defs, Assigns, and Name calls.

## Semantic argument (Python 3.14)

- Function calls create fresh frames; parameters bind to the argument object at call time. Nested `def` closes over the enclosing frame's `argv` cell. Source: docs.python.org/3.14 executionmodel, resolution of names.
- Rebinding `conf` assigns a new object to the module name; it cannot mutate the list objects already bound in either closure's frame.
- Therefore `first()` runs `subprocess.run(["pacman","-S","r22-ti-a"])` and `second()` runs `subprocess.run(["pacman","-Q","r22-ti-b"])`; `shlex.join` serializes both exactly (no shell specials). Classes follow frozen r21 convention: `-S` → host_mutation, `-Q` → package_query.

## Discriminating power (vs r21 F1)

FinalBindingReview F1: the scanner re-evaluates the recorded factory-call argument expression in the invocation-statement env. Under that defect both invocations resolve `conf` to the c-binding → wrong rows `package_query pacman -Q r22-ti-c` and a missing host_mutation. A correct (creation-time) binding yields exactly the two expected rows. Two instances with a shared argument name also catch per-closure state bleed (one captured env reused for both calls would collapse one row onto the other's argv).

## Independence and limits

- Derived from Python semantics and prior frozen conventions only; no candidate/changed code exists to read and none was read. No detector output consulted; the proposal does not depend on any repair shape.
- Deliberately single-cell: cross-cell captured-binding persistence is a different assigned variant (`CaptureCrossCell`); kept out to isolate the two-instance/rebind axis.
- Unknowns: none in the semantics. Whether any implementation emits these exact rows is the measurement this truth exists to judge — not predicted here.
- Tools installed: none. Pacman transactions paused host-wide; nothing needed.

Report: .ufo/waves/round-22/w1/reports/CaptureTwoInstances.md
