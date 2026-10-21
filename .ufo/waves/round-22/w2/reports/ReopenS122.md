# ReopenS122 — public tagged-source reopening (author lane)

Scout seat `MadoR22.ReopenS122`, round 22 attempt 1 wave 2, leaf. Delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. I re-opened only the official tagged URL plus the retained S122 row and lesson quote. No scanner, oracle, audit, gate, build, test, fixture or payload was run. No registry, production, fixture, tool, lesson or docs edit. All Git and network actions were read-only.

## Outcome

The retained S122 identity, quotes, line locations and scope are reproducible from the public tag. The only defect found is a loose range label in the assignment text, not in the source or retained row: `1378-1386` covers `Timer.cancel` plus `Timer.run`; `Timer.run` itself is `1382-1386` (with `cancel` at `1378-1380`).

## Actual retrieval result

| Field | Observed |
|---|---|
| URL | `https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/threading.py` |
| Channel | actual HTTP via `curl 8.23.0 -sS -fL --max-time 60` (no reader fallback) |
| HTTP | `HTTP/2 200`, `date: Wed, 21 Oct 2026 15:37:44 GMT` |
| Bytes / lines | 56,923 / 1,642 |
| SHA-256 | `5323909624ec2165e70b6d31333e4191b63d383d2dc5a7d7d516a3475ea2b7e3` |
| git blob | `c03b0b5370c933680bd04c8934d17dfa211bbf54` (`git hash-object`) |
| Retained byte comparison | `cmp` identical to `w1/sources/SourceThread/threading-v3.14.8.py` |
| Tag | `refs/tags/v3.14.8` → annotated `992560c2cc62d47b308cec662feb485456847931`, peeled `8e6e75d9102e39bed2a2b279203a396741180f12` |

Tag identity was re-verified with `git ls-remote` (exit 0). The receipt's HTTP ETag `09c0e8b4…` is only an HTTP validator, not the content hash.

## Range and quote verification

**`Thread.run` 1023–1028 — verified.** `def run` is at 1013, `try:` at 1022; the claimed slice is the executed gate/call/finally/delete body:

- 1023 `if self._target is not None:`
- 1024 `self._target(*self._args, **self._kwargs)`
- 1025 `finally:`
- 1028 `del self._target, self._args, self._kwargs`

`Thread.__init__` stores `self._target` at 925, `_args` at 927, `_kwargs` at 928; `kwargs=None` becomes `{}` at 912–913; `start` reaches `run` at 1082. The row's anchor does not list 925–928, but the retained receipt cites them as supporting locations, so this is a provenance nuance, not a contradiction.

**`Timer` 1378–1386 — content verified, label imprecise.** 1378–1380 is `cancel()` (`self.finished.set()`), 1381 is blank, and 1382–1386 is `run()`:

- 1383 `self.finished.wait(self.interval)`
- 1384 `if not self.finished.is_set():`
- 1385 `self.function(*self.args, **self.kwargs)`
- 1386 `self.finished.set()`

The combined span matches the retained row anchor `1370–1386` and the receipt's separate locations `1378–1380` / `1383–1385`. Calling the combined span “Timer.run” is loose, but no retained receipt or registry row asserts it.

**Quotes — verified.** The newline-preserving receipt quotes are byte-exact contiguous substrings at `1023–1024` and `1383–1385`. The lesson's single-line renderings match after whitespace normalization and each occurs exactly once in the file; they are not contiguous byte substrings because the lesson joins indented lines. Word counts using `len(quote.split())` are **7** (Thread) and **6** (Timer), total 13, both ≤25. This confirms the lesson's append-only 7/6 correction and the retained `quote_word_count_total: 13`.

## Scope verdict

The reopened source supports the retained row's bounded scope:

- A direct `.run()` on a base `Thread` synchronously calls the stored target with stored args/kwargs in the calling frame, gated only by `self._target is not None`.
- `Timer.run` waits, then calls its function only if `finished` is unset, and always sets `finished` afterwards; `cancel()` only sets the Event.
- User subclasses overriding `run` are outside the claim (docstring at 1016); runtime scheduling, concurrent cancellation, host execution and complete detector/instrument behavior are outside.
- The source cannot prove instrument completeness or that any scanner implements these forms.

## Admit/reject sample agreement — AUTHOR-LANE ADVICE ONLY

I compared the reopened source against the frozen oracle cases whose stated mechanism includes these source lines (`.ufo/waves/round-22/oracle/expected.json`, SHA-256 `b5cd4cf3…c4357`, read-only).

- **13 of 13 in-scope samples agree** in their S122-dependent portion: `ThreadRun`, `ThreadRunInline`, `ThreadRunAlias`, `ThreadRunHygiene`, `TimerRun`, `TimerRunInline`, `TimerRunAlias`, `TimerRunAliasActual`, `CX6TimerCancel`, `CX7ThreadRepeatedRun`, `ThreadReuseName`, `ThreadConstructorCapture`, `ThreadGlobalLate`.
- **0 source disagreements.** Qualifiers: `ThreadRunAlias` and `ThreadGlobalLate` depend partly on late global binding (S121/language semantics), `ThreadRunHygiene` on legal-name resolution, and `CX7ThreadRepeatedRun` on a source-inferred second-run `AttributeError` that was not executed. `ThreadConstructorCapture` relies on constructor storage lines cited only as supporting locations.
- **1 out-of-scope sample**: `CXInlineStartAlias` uses a captured `.start` and asynchronous start path; no S122 verdict.
- **1 rejected proposal**: `CaptureNestedFactory`, rejected pre-seal for an author typo. It does not depend on `threading.py`; the source neither supports nor contradicts that rejection.

This is author-lane advice, not outside-lane falsification and not admission. It cannot clear C1, cannot establish detector output, and cannot prove instrument completeness.

## Remaining unknowns

`Condition.wait`/timeout internals, non-numeric or negative intervals, concurrent cancellation during `Timer.wait`, `Event.clear()` reopening the gate, and the unexecuted second-run `AttributeError` remain unresolved. Whether any scanner implements these shapes is outside this receipt.

## Artifacts

- `.ufo/waves/round-22/w2/receipts/ReopenS122/source.json` — SHA-256 `55d7d155dccec29c73bce3b509931de4c3f96867e3feeb71984d807b5342606d`
- `.ufo/waves/round-22/w2/receipts/ReopenS122/threading-v3.14.8-reopen.py` — SHA-256 `5323909624…b7e3`
- `.ufo/waves/round-22/w2/receipts/ReopenS122/headers.txt` — SHA-256 `d87899a4…c767`
- `.ufo/waves/round-22/w2/receipts/ReopenS122/ls-remote.txt` — SHA-256 `6549cb7c…d0ac`

No installations or updates. No registry edit. No scanner/gate run.
