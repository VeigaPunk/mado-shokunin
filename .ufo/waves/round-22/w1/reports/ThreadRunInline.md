# ThreadRunInline — C1 static-truth proposal

Seat: `MadoR22.ThreadRunInline` · Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` · Wave: mado-r22-w1 · Role: reviewer (independent truth proposer, not admission).

## Deliverable

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/proposals/ThreadRunInline.json` — one cell, `expected_kind: exact`, one `want` row, empty `forbid_observed_commands`.

## Variant specified

`threading.Thread(target=worker, args=(argv,)).run()` as an **immediate chained expression** — the `Thread` instance is constructed and `.run()` is invoked on it in one statement with no intermediate variable. This is the unbound sibling of the r21 `thread-run-direct` fixture (`t = threading.Thread(...)` then `t.run()`), assigned to this seat to cover the expression-only shape independently.

## Frozen expectation (static truth, never executed)

| Field | Value | Basis |
|---|---|---|
| class | `host_mutation` | payload is `pacman -S`, an install transaction |
| command | `pacman -S r22-threadruninline` | `shlex.join(["pacman","-S","r22-threadruninline"])` over the literal argv bound to worker's parameter |
| evidence | `observed` | every link statically resolvable: keyword construction, synchronous `run()` dispatch, literal `argv` |
| unparsed | none | single eval cell, fully parseable Python; no `*`, `**`, or opaque calls |

`want` therefore contains exactly one row and `forbid_observed_commands` is empty, consistent with the `expected_kind: "exact"` contract (exact rows, zero unparsed).

## Semantic argument (Python 3.14.8)

1. `threading.Thread(target=worker, args=(argv,))` evaluates to a `Thread` instance. Per the pinned source snapshot `.ufo/waves/round-22/w1/sources/SourceThread/threading-v3.14.8.py` lines 925–928, `__init__` stores `self._target = worker`, `self._args = (argv,)`, `self._kwargs = {}`.
2. `.run()` on that instance resolves to `Thread.run` (lines 1013–1028): `if self._target is not None: self._target(*self._args, **self._kwargs)` — an ordinary synchronous call **in the caller's frame**. No `start()`, no new thread, no scheduling; the unreferenced instance is discarded only after `run()` returns.
3. `worker(argv)` executes `subprocess.run(argv)` with `argv` bound to the module-level literal `["pacman","-S","r22-threadruninline"]` defined in the same cell.
4. Statically, the transcript's only process-spawning path reaches `subprocess.run` with a fully determined argv: one observed `host_mutation` row, serialized `pacman -S r22-threadruninline`.

## Relationship to r21 F4

`FinalBindingReview.md` §F4 (lines 90–95) records that `.run` on a scheduled binding "is never followed" — silent miss, `unparsed` 0 — and that `.start` aliasing including chained `Thread(...).start()` was already handled (lines 134, 140). This proposal supplies independent truth for the chained `.run()` shape specifically: the sound output is exactly one observed `host_mutation` row, so a silent miss (no row, `unparsed` 0), a `lead`, or a fabricated/absent command all fail this expectation. Expectation authored from language semantics and the pinned stdlib source snapshot only — no detector bytes read, nothing measured or executed.

## Independence and method

- Read: r22 `registration.md`, `audit-contract.json`, `w1-spec.json` (own item only); r21 `residual/FinalBindingReview.md` (F4 context); `sources/SourceThread/threading-v3.14.8.py` (run/init semantics); r21 `w1/oracles/PartialMethod.json`, `CallbackGlobal.json` (field conventions only, not truth derivation); r21 inert fixture `thread-run-direct.jsonl` (cell-format reference only).
- Not read: `tools/mado-tripwire.py` or any detector/candidate implementation. No proposals exist yet in `w1/proposals/`; this seat wrote only `ThreadRunInline.json` and this report.
- No payload execution, no fixture execution, no probes, no package queries, no subprocess spawn (read-only `ls`/`find`/`grep`/`head`/`cat`/`python3 -c` JSON inspection of inert artifacts only — no background jobs).
- No installs or updates; none needed. Git untouched except nothing at all — not even read-only git was required beyond files already on disk.

## Unknowns and limits

- Whether the wave's scanner will classify this shape correctly is a detector question this proposal deliberately does not answer; the frozen `want` stands on Python semantics alone.
- The `Thread.run()` `finally` clause (deletion of `_target/_args/_kwargs`, line 1028) and `_bootstrap` are irrelevant to a direct `.run()` call's row-emitting behavior and were noted but not relied on beyond the synchronous-invoke line.
- `Timer.run()` (`threading-v3.14.8.py` line 1382 `run` → `self.finished.wait(interval)` then `self.function(*self.args, **self.kwargs)`) is a different variant owned by `TimerRunInline`; not claimed here.

## Verdict

Proposal delivered, internally consistent, single exact expected result: **one observed `host_mutation` `pacman -S r22-threadruninline`** from one parseable cell. No defect found in scope to report beyond the known r21 F4 gap this variant exercises.
