# FalsifyC149 — C1 case `TimerRunAliasActual` (author-lane advisory, NOT admission)

**Verdict: agree.** The delivered tool `tools/mado-tripwire.py` (sha256
`36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce`, identical before and after
the run) produced exactly the sealed truth for this one case: one `package_query` row
`pacman -Q r22-timer-run-alias-actual` at `observed`, with `eval_unparsed = unparsed_spawns = 0`
and no other rows. No false observed row, no lead, no lost command, no wrong identity, no
lifetime or conditional-target defect, and no parsed-clean ambiguity was found **within this
case**. This is a single bounded static-shape agreement. It grants no admission, is not
non-author admission, does not close F1/F5 family triggers generally, and leaves the r19/r20/r21
rejected-harmed receipts and the three-rejection streak untouched. L1 retains
planner/integration authority. C2 was not touched.

## Sealed truth (expected.json case `TimerRunAliasActual`, group `proposal`)

- `expected_kind: exact`; `want = [{class: package_query, command: "pacman -Q r22-timer-run-alias-actual", evidence: observed}]`; `want_input_order` is the same single row.
- `forbid_observed_commands: []`; `forbid_commands_any_tier: []`; `accept_exact_want: null`;
  `require_signal: true` (the raw proposal is silent, so this is the normalized default
  `kind == uncertain or bool(want)`; it is unused on the exact branch, which instead requires a
  complete row-multiset match **and** zero unparsed counters).
- One cell, `cell_reset: [false]`, fixture `inputs/TimerRunAliasActual.jsonl` sha256
  `f36a9dd9870c8736c13018f2e64108d307d57ce1f12bc7ebf2676e356741de8c` (equals the sealed
  `input_sha256`), one inert `eval` call with id `TimerRunAliasActual-0`.
- Proposal `.ufo/waves/round-22/w1/proposals/TimerRunAliasActual.json` sha256
  `ae3456e11ad594c9d5e226e68998c69121171cb3233917f2b14a4d2f5d71302e`; the runner re-verified it
  byte-for-byte against the sealed `proposal.fields` before and after the scan.

Fixture cell (inert input, never executed):

```python
import subprocess
import threading

def worker(argv):
    subprocess.run(argv)

timer = threading.Timer(0, worker, kwargs={"argv": ["pacman", "-Q", "r22-timer-run-alias-actual"]})
run = timer.run
run()
```

## Independent semantic reasoning (Python 3.14, payload not executed)

1. `threading.Timer.__init__(interval, function, args=None, kwargs=None)` is `Thread.__init__(self)`
   followed by `self.function = function`, `self.args = args if args is not None else []`,
   `self.kwargs = kwargs if kwargs is not None else {}`, `self.finished = Event()` — archived
   `w1/sources/SourceThread/threading-v3.14.8.py`, class `Timer` at line 1361, `__init__` at
   1370–1376. So `timer.function is worker`, `timer.args == []`, and
   `timer.kwargs == {"argv": ["pacman", "-Q", "r22-timer-run-alias-actual"]}`, all fixed at
   construction and never rebound.
2. `Timer.run` (lines 1382–1386) is `self.finished.wait(self.interval)`; then
   `if not self.finished.is_set(): self.function(*self.args, **self.kwargs)`; then
   `self.finished.set()`. `interval` is `0`, and `Event.wait(0)` is a non-blocking probe, so the
   call returns immediately. No `cancel()` appears anywhere in the cell, so `finished.is_set()`
   is still false and `worker(**{"argv": [...]})` is invoked unconditionally.
3. `run = timer.run` is an instance attribute load. `Timer.run` is a plain method, so the result
   is a bound method whose `__self__` is `timer` (Python 3.14 `types.MethodType` semantics; the
   proposal's source note cites exactly this). Calling `run()` therefore executes
   `Timer.run(timer)` **synchronously in the calling thread** — it does not spawn a thread and
   does not consult `_started`. `Thread.run`'s own docstring (lines 1013–1021: “The standard
   run() method invokes the callable object passed to the object's constructor as the target”)
   is consistent with this; `Timer.run` overrides it with the same-synchronous shape.
4. `worker`'s body is `subprocess.run(argv)` with `argv` bound to the stored literal list, so the
   incipient process is `pacman -Q r22-timer-run-alias-actual`. `pacman` with an uppercase `Q`
   operator is a read-only package query, not a mutation.
5. Because the whole cell is straight-line, the target call is forced (no conditional, no
   scheduling race, no cancellation), so `observed` — not `lead` — is the semantically correct
   evidence tier. The complete exact truth is exactly one observed row and zero error counters.
   The row is not an invented argv: `r22-timer-run-alias-actual` appears verbatim only in the
   `kwargs` literal and is never rebound.

## Mechanism check (read-only source inspection, so the green is not a coincidence)

- In `assignment_binding`, the `threading.Timer(...)` call is recognized by resolved name and
  returns `{"kind": "scheduled", "timer": true, "target": helper worker, "args": [],
  "kwargs": {"argv": [...]}}` with a shared `state` dict. The literal kwargs dict is folded at
  the binding statement via `literal_value`, i.e. at construction time.
- `callable_info` on the `timer.run` attribute sees the `scheduled` receiver and returns
  `scheduled_invoke` for `run`. `update_bindings` stores that (a new dict sharing `state`) under
  the module name `run`.
- `spawn_scan` on the eager call `run()` enters the `scheduled_invoke` branch, marks the state
  done, builds an inert target invocation from the stored `args`/`kwargs`, and re-enters the
  scanner with the resolved helper. `bind_literal` binds `argv`, `follow_helper` sweeps
  `worker`, and the `subprocess.run(argv)` spawn path classifies `["pacman","-Q",...]` as
  `package_query` with rule `pacman:-Q`.
- This row cannot be produced by a degenerate path: if `run = timer.run` had stayed unresolved,
  `run()` would have no literal args and emit no row (the case would fail); `worker` is not
  swept from the constructor reference because the refs loop skips the captured target of
  `threading.Timer`. The observed row therefore demonstrates that the aliased bound `.run`
  invocation actually followed the captured target with the construction-time kwargs.

## Actual rows (the one authorized bounded measurement)

Runner command (cwd is the lane root):

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py \
  --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py \
  --case TimerRunAliasActual
```

- Runner exited **0**, status `complete`, totals `{"pass": 1, "total": 1}`, empty stderr.
- Pre/post population integrity: **106** sealed source files, **52** proposal files, **57**
  fixtures verified; `integrity_errors: []`; `expected.json` b5cd4cf3…c59c4357 and pin
  7cc4aae9…93b1567f6 stable; population digest
  `046168571f51fe313c3ca57df5e743f0a6bb7d25c86d985b894eedc9f58686ad`; runner
  `41b021bb0052ef2e08e33a00e8b1d009ac8b4dd09c3dbabf88d8bf5caeb628c7`; producer
  `0270c10b90828a895ae3f0a5dec8b2c5610f960a2c1d994aa9409cad702c5600`.
- Scanner child (single child, 384 MiB address-space cap, 15 s timeout) exited **1** — the
  normal exit for an unpermitted finding, not an error — with empty stderr.
- Scanner file row: `sha256 f36a9dd9…1de8c` (equals the sealed fixture), `eval_calls 1`,
  `eval_unparsed 0`, `unparsed_spawns 0`, `bash_calls 0`, `lines 1`.
- got_rows, exactly: `[{class: package_query, command: "pacman -Q r22-timer-run-alias-actual",
  evidence: observed}]`, rule `pacman:-Q`, line 1, tool `eval`, tool_call_id
  `TimerRunAliasActual-0`; `observed_findings 1`, `lead_findings 0`; `unparsed 0`;
  `reasons: []`.

## Falsification axes for this case

| Axis | Result |
|---|---|
| false observed / lead argv | **Not found.** Exactly one row, correct literal command; no lead rows, no invented argv, no other class. |
| lost true command | **Not found.** The unique true row is present exactly once; full sorted (class, command, evidence) multiset equality holds (1 = 1). |
| wrong identity / def-name index | **Not found.** The row follows the module-bound `timer` instance's captured `worker` target; the command comes from the Timer `kwargs` literal, not from a same-named definition or a stale module literal. |
| lifetime / construction-time capture | **Not found.** The kwargs literal is stored at the `threading.Timer(...)` binding; nothing rebinds it before `run()`; `mutated_literal` is not triggered because the cell contains no subscript/attribute mutation. |
| conditional target / schedule | **Not found.** Direct bound-method `.run()` call is unconditional and synchronous; no `.start()`, no `cancel()`, `finished.wait(0)` returns immediately. The tool's `state.done` guard was consumed exactly once, matching the single call. |
| parsed-clean ambiguity | **Not found for this case.** `eval_unparsed = unparsed_spawns = 0`, one file row, scanner exit 1 (findings, not could-not-evaluate); the pass is exact multiset + zero counters, not an `accept_exact_want` alternate (`null`) and not the uncertain branch. |

## Uncertainty boundaries (explicit; not measured)

- No fixture code was executed. The truth rests on the pinned 3.14.8 `threading` source and
  Python language bound-method semantics; the local interpreter is 3.14.8, matching the pin.
- The tool models direct `scheduled_invoke` as one-shot (`state.done`). Calling the bound `.run`
  twice would execute `worker` twice at runtime, while the tool would report only the first.
  That is outside this case (one invocation) and is left as an untested neighbour form for a
  separately assigned probe — it is not a finding here and did not affect the observed rows.
- No claim is made about `.start()` timing, cancellation races, user `Timer` subclasses, or
  arbitrary `run` overrides; supported-forms places these outside exact-result support. Their
  absence of a finding is not certified here.
- This result is one positive author-lane advisory datum for the aliased standard `.run` form.
  It is not a counterexample to the remaining F1–F5 families, does not satisfy the required
  outside-lane falsification, and does not alter any C2 artifact-audit expectation.
- No installs or upgrades were performed; no tool source, fixture, proposal, gate, registry,
  documentation or expected file was modified. One scanner child was run, no extra scanner runs.

## Receipts

- `.ufo/waves/round-22/w2/receipts/FalsifyC149/result.json` — argv/exit/stdout/stderr, all
  hashes, integrity snapshots, checks.
- `.ufo/waves/round-22/w2/receipts/FalsifyC149/measure.stdout`, `measure.stderr`,
  `measure.exit`, `pre-hashes.txt`, `post-hashes.txt`.
