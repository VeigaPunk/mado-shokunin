# SourceThread — S122 proposal: CPython v3.14.8 `Thread.run` / `Timer.run`

Seat `MadoR22.SourceThread`, round 22 attempt 1, wave 1. Leaf, source-only. I opened one official tagged file and wrote only under `w1/sources/SourceThread/` and this report. No registry, production, harness or shared-lesson edits. No detector measurement, scanner child, fixture or payload execution. No installs. All Git and network actions were read-only.

## Outcome

The tagged source supports F4's premise for `Thread.run` directly. A direct `t.run()` on a base `Thread` calls the stored target with the stored arguments in the calling thread. The only condition is `target is not None`.

`Timer.run` is different. It calls its function only if the timer's `finished` Event is still unset after waiting `interval`. Source shape alone therefore does not decide whether the call happens. S122 is proposed and not registered.

## Retained source (raw bytes plus receipt)

Directory: `.ufo/waves/round-22/w1/sources/SourceThread/`

| File | What it is | sha256 |
|---|---|---|
| `threading-v3.14.8.py` | raw body, 56,923 B, 1,642 lines | `5323909624ec2165e70b6d31333e4191b63d383d2dc5a7d7d516a3475ea2b7e3` |
| `http-headers.txt` | response headers: HTTP/2 200, `date: Wed, 21 Oct 2026 14:19:12 GMT` | `7c6d524cfc4f87a9b4864463640ec85831c06e4e45b698bd02074f4dff253afe` |
| `ls-remote.txt` | `git ls-remote` for the tag and the peeled commit | `6549cb7c3492366c3440e8b774e38c2642d153ce3e3f660ac6d8e94b5447d0ac` |
| `blob-api.json` | GitHub contents API response for `Lib/threading.py?ref=v3.14.8` | `2db4ee402a5f2b07a8f2b4bd80855b5dcae67454ccf889aabd03999a49eca8a9` |
| `receipt.json` | URL, date, digests, located quotes, supporting anchors | — |
| `S122-proposal.md` | proposed SOURCES row, in the table's column order | — |

- **URL:** https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/threading.py ([HTML view](https://github.com/python/cpython/blob/v3.14.8/Lib/threading.py)).
- **Accessed:** 2026-10-21T14:19:12Z, using curl 8.23.0 with `-sS -fL`.
- **Tag:** `v3.14.8` resolves to annotated tag object `992560c2cc62d47b308cec662feb485456847931`, which peels to commit `8e6e75d9102e39bed2a2b279203a396741180f12`. This matches the tag recorded for S111/S113.
- **Integrity cross-check:** `git hash-object` of the saved body gives `c03b0b5370c933680bd04c8934d17dfa211bbf54`. That equals the API blob sha at the tag. The byte count equals the API size, 56923.
- **Quote check:** I ran one inert, read-only Python check. Both quotes are byte-exact at their stated line ranges, and the sha256 and length match. They total 13 words, under the 25-word limit.

## Located quotes

- `Lib/threading.py:1023-1024` (`Thread.run`): "if self._target is not None: self._target(*self._args, **self._kwargs)"
- `Lib/threading.py:1383-1385` (`Timer.run`): "self.finished.wait(self.interval) if not self.finished.is_set(): self.function(*self.args, **self.kwargs)"

## Direct worker semantics: `Thread.run` (observed in the source)

1. **Synchronous call in the caller.** The `run` body (1022–1028) contains no thread creation. It calls `self._target(*self._args, **self._kwargs)` directly. The new thread exists only on the `start()` path: `_bootstrap_inner` calls `self._context.run(self.run)` (1082). So `t.run()` runs the same body inline, as F4's contract text says.
2. **Single gate.** The only condition is `self._target is not None` (1023). With `target=None`, `run()` does nothing.
3. **Read at call time.** `__init__` stores `target`, `args` and `kwargs` by reference (925–928). The defaults are `args=()` and `kwargs=None`, and `None` becomes `{}` (880–881, 912–913). `run` reads these attributes when it executes, not at construction. This is relevant to F1-style invocation-time binding: a mutable `args` list that changes between `Thread(...)` and `.run()` changes the call.
4. **At most one target call per object.** The `finally` block deletes `_target`, `_args` and `_kwargs` (1025–1028). The only assignment of `_target` is at 925, and the class has no class-level `_target`. A second `run()` on the same object would therefore raise `AttributeError` before calling anything. That last step is **[INFERENCE]** from Python attribute lookup; it was not executed.
5. **Applies only to the base method.** The docstring says "You may override this method in a subclass" (1016). The semantics above hold only when the receiver's `run` is `threading.Thread.run`. A user subclass that defines `run` needs its own body resolution. The source does not support mapping every `.run()` on a Thread-like object to the target.

## Timer: what is certain versus what is uncertain

**Observed in the source:**
- `Timer.__init__` calls `Thread.__init__(self)` with no target. It stores `interval`, `function`, `args` (default `[]`) and `kwargs` (default `{}`) as public attributes, and creates `self.finished = Event()` (1370–1376).
- `Timer.run` overrides `Thread.run` completely. It never reaches `Thread.run`'s `_target` path or its `finally`/`del`.
- `run` first blocks in `self.finished.wait(self.interval)`. It then calls `self.function(*self.args, **self.kwargs)` only if `not self.finished.is_set()`. After that it always calls `self.finished.set()` (1383–1386).
- `cancel()` is exactly `self.finished.set()` (1378–1380).
- `Event.wait` returns immediately if the flag is already set (654).
- A direct `t.run()` is still synchronous in the caller, including the blocking wait. `function`, `args` and `kwargs` are read at call time and are public, so they can be reassigned after construction.

**Decidable from source shape alone:**
- If `t.cancel()` (or `t.finished.set()`) runs sequentially before `t.run()` on the same object, with nothing clearing the Event in between, the wait returns immediately and the function is not called.
- After one `t.run()` returns, `finished` is set (1386). A later `t.run()` on the same object does not call the function again.

**Uncertain and not decidable from straight-line source:**
- Whether `finished` is unset when the wait ends. Any other thread holding the timer can call `cancel()` during the `interval` wait and suppress the call.
- What happens with a concurrent `t.start()` followed by `t.run()`. Both paths run the same gated body, and one may set `finished` before the other checks it.
- An `Event.clear()` on `t.finished` reopens the gate.
- Whether an unknown, non-literal `interval` affects reaching the check at all, for example by raising inside `wait`. I did not trace `Condition.wait`, so this is an **open gap**, not a claim.

**Consequence for C1 truth seats (recommendation, not a measured result):**
- A statically bound base `Thread(...).run()` with a resolved target and arguments is source-supported as a direct synchronous invocation. It is eligible for the observed tier, under the same binding rules as `.start()`.
- `Timer(...).run()` is source-supported only as a call gated on Event state. Unless the frozen truth explicitly scopes the case to "no cancel, set, clear, escape or concurrent start on any path", it should produce a lead, not an observed row.
- A cancel that runs sequentially before `run()` should produce no observed row for that function.
- Unknown `function`, `args` or `interval` values must stay lead or unparsed. Under the C1 rule, they must never be filled from module globals.

## What S122 does not support

- User subclass `run` overrides.
- Process or host execution of any kind. `threading` starts threads, not processes.
- Runtime timing or scheduling guarantees.
- Admission of the C1 F4 repair. Source support is not an outside-lane falsification.

## Remaining unknowns

- I did not open `Condition.wait` or the lock timeout behavior behind `Event.wait`. Non-numeric or negative `interval` behavior is unverified.
- I did not check other CPython tags. S122 is pinned to v3.14.8, with recheck on release.
- Registering S122 in `corpus/SOURCES.md`, and choosing its `used-by` targets, is left to the registry owner or Main.

## Tooling

No tools were installed or updated. I used curl 8.23.0, git and python3, all already present.

## Checks for Main

Recompute sha256 and `git hash-object` of `w1/sources/SourceThread/threading-v3.14.8.py` against `receipt.json`. Re-slice lines 1023–1024 and 1383–1385 against the quotes.
