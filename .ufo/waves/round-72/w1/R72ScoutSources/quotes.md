# R72 source quotes — CPython v3.14.8

Fetched 2026-11-04 (01:39 America/Sao_Paulo / 04:39 UTC), three times per URL,
`curl -fsSL`, byte-identical; bodies at `fetch/`, digests at `receipts.jsonl`.
Tag: `refs/tags/v3.14.8` -> object `992560c2cc62d47b308cec662feb485456847931`,
peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12` (`git ls-remote`).

Line numbers are line numbers of the raw `.rst` / `.py` files as fetched
(`fetch/unittest.rst.1`, `fetch/main.py.1`, `fetch/stdtypes.rst.1`).

## (1) Doc/library/unittest.rst — 107,372 B, sha256 d6522f68…

§ `TestResult` opens at `unittest.rst:2041`; `wasSuccessful` is declared at
`unittest.rst:2127`.

**Quote 1** — `unittest.rst:2129-2130` (13 words):
> Return ``True`` if all tests run so far have passed, otherwise returns ``False``.

Its `versionchanged:: 3.4` note (`:2132-2134`) adds that it "Returns ``False`` if
there were any :attr:`unexpectedSuccesses`" — i.e. the method is a boolean over the
whole run so far, not a count and not a per-assertion report.

**Quote 2** — `unittest.rst:134` (5 words):
> Ran 3 tests in 0.000s

**Summary-printing documentation — finding: absent.** `grep -c summary unittest.rst`
is `0`. The `TextTestResult` class block (`:2255-2264`) says only that it is "A
concrete implementation of :class:`TestResult` used by the
:class:`TextTestRunner`"; the `TextTestRunner` block (`:2273-2324`) documents only
stream/defaults, `_makeResult()` and `run(test)` ("the results printed to stdout").
The `Ran N tests in …` line therefore appears in this file **only** as example
program output (`:134`, `:146`, `:575`), never as a specified summary format. What
the file does specify is the exit contract: `unittest.rst:2355-2357` — "By default
``main`` calls :func:`sys.exit` with an exit code indicating success (0) or failure
(1) of the tests run.  An exit code of 5 indicates that no tests were run or
skipped."

Same file as the r71 lesson cited? **No.** The r71 lesson cited `subprocess.rst`
(:73) and `expressions.rst` (:89) and rejected `Doc/library/stdtypes.rst` (:102);
`Doc/library/unittest.rst` is a new surface this round.
Resolves at v3.14.8? **Yes — HTTP 200**, 107,372 B, identical across three fetches.

## (2) Lib/unittest/main.py — 11,660 B, sha256 12de7da0…

**Quote 3** — `main.py:272-273` (2 code lines; the `wasSuccessful` call and the exit
it drives):
> if not self.result.wasSuccessful():
>     sys.exit(1)

Context: `main.py:270` `self.result = testRunner.run(self.test)`; `:271` `if
self.exit:`; `:274-275` `elif self.result.testsRun == 0 and len(self.result.skipped)
== 0: sys.exit(_NO_TESTS_EXITCODE)`; `_NO_TESTS_EXITCODE = 5` at `main.py:11`;
`:276-277` `else: sys.exit(0)`; `main = TestProgram` at `:280`. So the process exit
is a three-way map of `wasSuccessful()`, zero-tests, and success — a boolean
distilled from the run, carrying no failure count and no failure text.

Same file as the r71 lesson cited? **No** — new surface this round.
Resolves at v3.14.8? **Yes — HTTP 200**, 11,660 B, identical across three fetches.

## (3) Doc/builtins/stdtypes.rst — 248,201 B, sha256 5a6951b7…

The mapping-methods block the round-71 reject described: `Mapping Types ---
:class:`dict`` at `stdtypes.rst:5299`.

**Quote 4** — `stdtypes.rst:5529` (2 tokens):
> .. method:: update(**kwargs)

**Quote 5** — `stdtypes.rst:5523` (2 tokens):
> .. method:: setdefault(key, default=None, /)

Block context (not one of the five counted quotes): `update`'s signatures run
`:5529-5531` (`update(**kwargs)`, `update(mapping, /, **kwargs)`,
`update(iterable, /, **kwargs)`) and its body at `:5533-5534` reads "Update the
dictionary with the key/value pairs from *mapping* or *iterable* and *kwargs*,
overwriting existing keys."

Same file as the r71 lesson cited? **The same document, at a different path.** The
r71 lesson (`corpus/lessons/round-71.md:102`) cited
`…/v3.14.8/Doc/library/stdtypes.rst`; that URL returns **HTTP 404** on all three
probes (14 B body `404: Not Found`, sha256 d5558cd4…, `fetch/bad.1`–`bad.3`). The
3.14 tree places the page at `Doc/builtins/stdtypes.rst`, which returns **HTTP 200**
on all three fetches. So the reject's *content* was real and re-openable, its
*address* was not — and its stated flip condition ("a claim whose subject is
mapping-method behaviour (not call syntax) re-opens it") is the condition this
round's C1/C2 knowledge entries must satisfy before any row is appended.

## Resolution summary

| # | URL path at v3.14.8 | HTTP | Bytes | Same file r71 cited? |
|---|---|---|---|---|
| 1 | `Doc/library/unittest.rst` | 200 | 107,372 | no (r71: subprocess, expressions) |
| 2 | `Lib/unittest/main.py` | 200 | 11,660 | no |
| 3 | `Doc/builtins/stdtypes.rst` | 200 | 248,201 | yes, content; cited path 404 |
| — | `Doc/library/stdtypes.rst` (r71 path) | 404 | 14 | the r71 address, unresolvable |

## Remaining unknowns

- The fetched `.rst` is the source, not the rendered page; Sphinx may rewrite
  cross-reference roles in output. The quoted prose is source text.
- `TextTestResult`'s summary text is an implementation detail of
  `Lib/unittest/runner.py`, which was **not** fetched this round; nothing here
  establishes the exact `FAILED (failures=N)` wording or its stream.
- These are static tag facts; they say nothing about the host's installed Python.
