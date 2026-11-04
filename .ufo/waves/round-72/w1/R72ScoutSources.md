# R72 scout — sources (CPython v3.14.8)

seat: R72ScoutSources · date: 2026-11-04 · write dir:
`.ufo/waves/round-72/w1/R72ScoutSources/` (bodies `fetch/`, digests
`receipts.jsonl`, located quotes `quotes.md`) · scratch
`/fast/scratch/hyaku/mado-r72/R72ScoutSources/` created, used, deleted.

## What was done

Three URLs fetched three times each with `curl -fsSL`, 2026-11-04
(01:39 -0300 / 04:39 UTC); each triple asserted byte-identical with `cmp`; sizes
and sha256 recorded; the round-71 rejected address probed three times for its HTTP
code. Tag pinned by `git ls-remote`: `refs/tags/v3.14.8` → object
`992560c2cc62d47b308cec662feb485456847931`, peeled commit
`8e6e75d9102e39bed2a2b279203a396741180f12`.

| URL (v3.14.8) | HTTP | Bytes | sha256 | 3× identical |
|---|---|---|---|---|
| `Doc/library/unittest.rst` | 200 | 107,372 | `d6522f68c29c8ced8d2d81c91cb41ac739f855e6c0b9831f4a0e5a81f7ae5b86` | yes |
| `Lib/unittest/main.py` | 200 | 11,660 | `12de7da0fea92dbff8713ebe9904ada6dbd1e0a334d58861c6287ccfc0a261d2` | yes |
| `Doc/builtins/stdtypes.rst` | 200 | 248,201 | `5a6951b72ecc630a87f45a650fc11c186cfeb4251bedd1ea28f45bcb3116e8e1` | yes |
| `Doc/library/stdtypes.rst` (r71 path) | **404** | 14 | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` | yes |

The three 200 digests are byte-equal to the copies already sitting in
`.ufo/waves/round-72/fetch/*.1` (independent fetch, same bytes). Source:
`sha256sum` on both sets.

## Located quotes (≤25 words, file:line)

1. `unittest.rst:2129-2130` — "Return ``True`` if all tests run so far have passed,
   otherwise returns ``False``." (`.. method:: wasSuccessful()` at `:2127`, inside
   § `TestResult` opened at `:2041`; `versionchanged:: 3.4` at `:2132-2134` adds the
   `unexpectedSuccesses` → False case.)
2. `unittest.rst:134` — "Ran 3 tests in 0.000s" (also `:146`, `:575`).
3. `main.py:272-273` — "if not self.result.wasSuccessful():" / "sys.exit(1)"
   (context `:270-277`: `run()` → `if self.exit:` → `wasSuccessful()` →
   `_NO_TESTS_EXITCODE` (`= 5` at `:11`) → `sys.exit(0)`; `main = TestProgram` at
   `:280`).
4. `stdtypes.rst:5529` — ".. method:: update(**kwargs)" (signatures `:5529-5531`,
   body `:5533-5534`).
5. `stdtypes.rst:5523` — ".. method:: setdefault(key, default=None, /)"
   (`Mapping Types --- :class:`dict`` opens at `:5299`).

## Findings

**F1 — the r71 reject's address does not resolve; its content does.**
`Doc/library/stdtypes.rst` returns **404** at v3.14.8 on all three probes (14 B,
`404: Not Found`). `Doc/builtins/stdtypes.rst` returns **200**, 248,201 B, and holds
exactly the mapping-methods block the reject described (`update` `:5529`,
`setdefault` `:5523`, `dict` section `:5299`). So the r71 row was unprovable *as
addressed* and provable at the real path — the same conclusion the round-71
verifier spotcheck reached by tree listing, now reproduced by direct fetch.
Confidence: high (byte receipt + HTTP codes).

**F2 — `wasSuccessful` is a whole-run boolean, specified as such.**
The docs state only the True/False sentence and the unexpected-success downgrade;
no count, no failure text, no stream. Confidence: high.

**F3 — the summary line is not a documented `TextTestResult` contract.**
`grep -c summary Doc/library/unittest.rst` = 0. `TextTestResult` (`:2255-2264`) is
described only as "A concrete implementation of :class:`TestResult` used by the
:class:`TextTestRunner`"; `TextTestRunner` (`:2273-2324`) documents stream defaults,
`_makeResult()` and `run(test)` ("the results printed to stdout"). The
`Ran N tests in …` text occurs only in example program output (`:134`, `:146`,
`:575`). The exact `OK` / failure-summary wording is an implementation detail of
`Lib/unittest/runner.py`, which this round did not fetch. Confidence: high for the
absence in this file; unknown for runner.py wording.

**F4 — the exit status is a distilled boolean, documented as such.**
`unittest.rst:2355-2357`: "By default ``main`` calls :func:`sys.exit` with an exit
code indicating success (0) or failure (1) of the tests run.  An exit code of 5
indicates that no tests were run or skipped." `main.py:272-277` is the code path:
three-way map of `wasSuccessful()`, zero-tests, success. The exit carries no
assertion counts and no failure detail. This is the static-stdlib ground for both
axes' direction (C1 reads the run's own report; C2 reads the summary rather than
`gate_rc`). Confidence: high, and it is a tag fact only.

**F5 — citation status versus the r71 lesson.** The r71 lesson cited
`Doc/library/subprocess.rst` (`corpus/lessons/round-71.md:73`) and
`Doc/reference/expressions.rst` (`:89`), and rejected `Doc/library/stdtypes.rst`
(`:102`). `Doc/library/unittest.rst` and `Lib/unittest/main.py` are **new files**
this round, not re-citations. The stdtypes document is the same one r71 named, at
the corrected path. Its stated flip condition — "a claim whose subject is
mapping-method behaviour (not call syntax) re-opens it then" — is the gate any
stdtypes row must pass; this scout does not append rows. Confidence: high.

## Remaining unknowns

- `Lib/unittest/runner.py` (summary/`FAILED (failures=N)` wording, stream choice)
  was not fetched; no quote here supports a specific summary grammar.
- `.rst` is source text, not the rendered page; Sphinx role rendering differs.
- Static tag facts say nothing about the host's installed Python.
- No registry/SOURCES write attempted (leaf seat; not my write surface).

## Tooling

No installs, no pacman transactions, no service or config touches. Tools used:
`curl`, `cmp`, `sha256sum`, `stat`, `git ls-remote` (read-only).
