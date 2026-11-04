# R75ScoutSources — the two sources the round-75 C2 claim rests on

Seat: R75ScoutSources (round 75, wave 1). Read-only sweep; no lane file was edited.
Base revision of the measured repository: `b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6`.
Tag pin verified read-only this run:

```
$ git ls-remote https://github.com/python/cpython refs/tags/v3.14.8 'refs/tags/v3.14.8^{}'
992560c2cc62d47b308cec662feb485456847931	refs/tags/v3.14.8
8e6e75d9102e39bed2a2b279203a396741180f12	refs/tags/v3.14.8^{}
```

So every fetch below resolves `v3.14.8` → annotated tag object
`992560c2cc62d47b308cec662feb485456847931`, peeled commit
`8e6e75d9102e39bed2a2b279203a396741180f12` — the pin S105–S122, S440–S452 already record.

## Source A — `Doc/reference/simple_stmts.rst`, § The ``del`` statement

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst`
- Fetched three times (`simple_stmts.rst.1/.2/.3`), each `curl -sS -f -L`.
- **Byte length: 41,375 bytes** (identical on all three).
- **sha256: `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`** (identical on all three; `cmp` exit 0 for 1-vs-2 and 1-vs-3).
- Section head located: `simple_stmts.rst:439` `.. _del:`, `:441` `The :keyword:`!del` statement`, `:442` underline.
- **Line span of the located sentence: `simple_stmts.rst:468-469`** (the sentence continues its
  subordinate clause onto `:469`; the governing clause is exactly `:468`+first half of `:469`).

Quote, markup stripped (the span carries no RST inline markup at all — verbatim):

> Deletion of attribute references and subscriptions is passed to the primary object involved
> — `Doc/reference/simple_stmts.rst:468-469`, **13 words**
> (`python3 -c 'q="…"; print(len(q.split()))'` → `13`).

Why it grounds the C2 branch: `del env[KEY]` is a *subscription* deletion, and this sentence makes
it a call into the primary object — the mapping `env` itself — rather than an unlinking of a name,
so the key is removed from the very mapping later copied or handed as `env=` to the child; the
round-75 C2 rule that reads a `del` between the guard construction and the launch as a
cancellation is therefore grounded in the language reference, not in an assumption about
dictionaries.

Adjacent scope note (not part of the quote): `:461-464` covers *name* deletion, which is a
different object (`NameError` on an unbound name) and is why the rule is scoped to a literal key
in the same scope rather than to `del name`.

## Source B — `dict(mapping, **kwargs)`

### B0. The requested path is absent at this tag (three attempts, all 404)

`https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/stdtypes.rst`
`curl -sS -f -L`, three attempts:

```
attempt1 rc=22 The requested URL returned error: 404
attempt2 rc=22 The requested URL returned error: 404
attempt3 rc=22 The requested URL returned error: 404
```

This is not a transient failure and it is not new: `corpus/SOURCES.md:396` (row S446) already
records the identical result — the round-71 citation `Doc/library/stdtypes.rst` returned HTTP 404
on all three attempts, which is the round-71 routed defect that S446 repairs by anchoring at
`Doc/builtins/stdtypes.rst`; `corpus/SOURCES.md:865` restates it. The 3.14 documentation tree moved
`Doc/library/stdtypes.rst` to `Doc/builtins/stdtypes.rst`.

### B1. Real 3.14.8 path, three byte-identical fetches

- URL: `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/stdtypes.rst`
- Fetched three times (`builtins_stdtypes.rst.1/.2/.3`), each `curl -sS -f -L`.
- **Byte length: 248,201 bytes** (identical on all three).
- **sha256: `5a6951b72ecc630a87f45a650fc11c186cfeb4251bedd1ea28f45bcb3116e8e1`** (identical on
  all three; `cmp` exit 0 for 1-vs-2 and 1-vs-3). This is exactly the digest and length S446
  records for this document, re-derived independently this round.

Constructor signatures located: `builtins_stdtypes.rst:5325` `.. class:: dict(**kwargs)`, `:5326`
`dict(mapping, /, **kwargs)`, `:5327` `dict(iterable, /, **kwargs)`.

- **Line span of the located paragraph: `builtins_stdtypes.rst:5350-5352`** (the `dict(mapping,
  **kwargs)` argument-form paragraph, immediately below the three signatures).

Quote, markup stripped (the span carries no RST inline markup — verbatim):

> If keyword arguments are given, the keyword arguments and their values are added to the
> dictionary created from the positional argument
> — `Doc/builtins/stdtypes.rst:5350-5352`, **21 words**
> (`python3 -c 'q="…"; print(len(q.split()))'` → `21`).

Why it grounds the C2 branch: this is the sentence that makes `dict(env, KEY="1")` a *copy that
carries the keyword pair* — the keyword arguments are added to the dictionary created from the
positional mapping `env`, so the resulting object is a new mapping that holds `KEY` in key
position. That is why the successor C2 rule counts a copy carrying the guard key in key position,
bound to a name that is not env-named and handed as `env=`, as guarded: the guard key is present
in the mapping the child receives, independently of the name it is bound to.

Scope note (not part of the quote): `:5340-5348` is the positional-argument path (a `keys()`
mapping is copied by `__getitem__` per key), and `:5352-5353` is the collision rule (the keyword
value replaces the positional value for an existing key) — which is the precise reason a later
`dict(env, KEY=…)` copy *re-asserts* the key rather than dropping it, and the reason a copy built
without the key does not.

## Existing rows in `corpus/SOURCES.md` for these URLs (before any append)

| URL | existing rows | same-document scope of each |
|---|---|---|
| `.../v3.14.8/Doc/reference/simple_stmts.rst` | **S440**, **S447**, **S451** | S440 assignment statements `:190-194`; S447 the `global` statement `:972-973`; S451 attribute-reference targets `:160-165` |
| `.../v3.14.8/Doc/library/stdtypes.rst` | **S446** (records the URL as 404'd; anchors at `Doc/builtins/stdtypes.rst`) | S446 mapping methods `update(**kwargs)`/`setdefault`, `Doc/builtins/stdtypes.rst:5299,5523,5529`; status `rejected` |
| `.../v3.14.8/Doc/builtins/stdtypes.rst` | **S446** | same row; the § Mapping Types --- dict scope |

- `simple_stmts.rst` is already held by S440, S447 and S451, all at *different* scopes than § The
  ``del`` statement (`:439-471`). Per the maintained census rule recorded at
  `corpus/SOURCES.md:502-509`, an URL collision is a merge-review trigger / non-failing **W04**
  warning; it becomes an error only when a `supersedes S###` marker is present. The round-75 row
  for Source A is a new scope at the same document, so it must **not** carry `supersedes` and
  stays a non-failing W04 warning — the same posture S451 took against S447.
- `builtins/stdtypes.rst` is held only by S446, whose admitted anchor is the mapping *methods*
  (`update`/`setdefault`); the `dict(mapping, **kwargs)` *constructor* paragraph is a separate
  scope, so the round-75 row for Source B is likewise a different-scope repetition, non-failing
  W04 warning, and must not carry `supersedes` (it does not overturn S446's `rejected` status —
  S446 was rejected for call-site/result-object semantics, which is still true).
- No row anywhere in `corpus/SOURCES.md` currently anchors `simple_stmts.rst:468-469` or
  `builtins/stdtypes.rst:5350-5352`; the two spans are unclaimed.
- `Doc/library/stdtypes.rst` appears in `corpus/SOURCES.md` only as the *404 record* inside S446
  (`:396`) and in the round-73/74 search-log prose (`:865`); it is held by no row as a fetched
  source, so nothing is being displaced by re-recording its absence.

## Facts vs inference

**Observed (this run, reproducible):** the three 404s at `rc=22`; the two documents' byte lengths,
digests and triple byte-identity; the tag→commit pin; the line spans and their exact text; the
13- and 21-word counts; the existing rows and their scopes; the W04 rule text at `:502-509`.

**Inference (labelled):** that the `del`-sentence and `dict(...)`-sentence jointly licence the
round-75 C2 rule shapes is an inference from the declaration's own wording (`claims-declaration-r75.md`
§ C2) to these two spans — the documents ground the *runtime semantics*, not the detector's
syntactic approximation. Nothing here asserts the census's correctness; the census result is the
counting command's to produce.

**Unresolved / not claimed:** no CPython source was executed; no host behaviour was probed; the
`dict` copy's identity/aliasing semantics beyond the documented copy are not claimed; `del` is
grounded for a literal key in the same scope only, matching the claim's declared limit.

## Scratch

Raw fetched bytes were kept at `/fast/scratch/hyaku/mado-r75/R75ScoutSources/`
(`simple_stmts.rst.1..3`, `builtins_stdtypes.rst.1..3`). Digests, lengths and commands are
recorded here and in `fetch-digests.txt` / `fetch-404.txt`, and the material is re-derivable by
re-fetch at the pinned tag (proven byte-identical three times this run), so the scratch tree is
deleted on seat exit.
