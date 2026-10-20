# SrcPyBuiltins — CPython v3.14.8 confirms the builtin/collections constructors; the assigned `Doc/library/functions.rst` path is absent at that tag, so two S1xx-pending source rows are drafted from `Doc/builtins/functions.rst` + `Doc/library/collections.rst`

All paths below are relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`. Fetch bodies and receipts are in `.ufo/waves/round-20/fetch/SrcPyBuiltins/`. Nothing here is host behaviour: the fixture/interpreter code was never executed; quotes are documentary.

## Findings

### F1. Tag → commit resolved (observed, high confidence)
Command and full output:

```
$ git ls-remote https://github.com/python/cpython refs/tags/v3.14.8 'refs/tags/v3.14.8^{}'
992560c2cc62d47b308cec662feb485456847931	refs/tags/v3.14.8
8e6e75d9102e39bed2a2b279203a396741180f12	refs/tags/v3.14.8^{}
```

`v3.14.8` is an annotated tag: tag object `992560c2cc62d47b308cec662feb485456847931`, peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12`. Saved: `fetch/SrcPyBuiltins/git-ls-remote-v3.14.8.txt` (121 B, sha256 `6549cb7c3492366c3440e8b774e38c2642d153ce3e3f660ac6d8e94b5447d0ac`).

### F2. The assigned path is absent at the tag; the content lives at `Doc/builtins/functions.rst` (observed, high confidence)
- `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/functions.rst` → HTTP **404**, 14-byte body `404: Not Found\n`, sha256 `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` (`assigned-functions-404.txt`; `receipts.jsonl` line 1). `final_url` equals the requested URL — no redirect.
- Same path at the peeled commit `8e6e75d…` → HTTP **404**, same 14-byte body (`peeled-functions-404.txt`; `receipts.jsonl` line 5).
- Corroboration of a docs-tree move, not a transient miss: `Doc/library/stdtypes.rst` is also 404 at the tag (`doc-library-stdtypes-404.txt`; `receipts.jsonl` line 4), while the v3.14.8 contents listing shows `Doc/builtins/` (constants.rst, exceptions.rst, functions.rst, index.rst, stdtypes.rst, threadsafety.rst, time-complexity.rst) beside `Doc/library/` (`discovery-Doc-contents.json`, 25,842 B, sha256 `fb6c0876de1edc6bacaea53b268abecb14eebb7b3b372470a99028d830e934c0`; `receipts.jsonl` line 6).
- `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/functions.rst` → HTTP **200**, 97,140 B, sha256 `f1b72170e6893ee6315108f74244df56a9725f2be2b8bf396f22cd6dcbd5d9de` (`cpython-3.14.8-Doc-builtins-functions.rst`; `receipts.jsonl` line 2).

`Doc/library/collections.rst` is where the assignment says: HTTP **200**, 54,628 B, sha256 `be2f90d14d3f488a9d5a6f23423e494a46b10a030d83d9308fd71af1f8eed7a7` (`cpython-3.14.8-Doc-library-collections.rst`; `receipts.jsonl` line 3).

So the row anchors the upstream tag and the real file path; the 404 is recorded rather than silently substituted.

### F3. `Doc/builtins/functions.rst` — located quotes (observed, high confidence)
Verbatim RST, each quote ≤ 25 words (markup tokens not counted as words):

| constructor | signature | quote | words |
|---|---|---|---|
| `frozenset` | `:865` `.. class:: frozenset(iterable=(), /)` | `:868-869` "Return a new :class:`frozenset` object, optionally with elements taken from *iterable*." | 11 |
| `set` | `:1821` `.. class:: set(iterable=(), /)` | `:1824-1825` "Return a new :class:`set` object, optionally with elements taken from *iterable*." | 11 |
| `tuple` | `:2079` `.. class:: tuple(iterable=(), /)` | `:2082-2083` "Rather than being a function, :class:`tuple` is actually an immutable sequence type" | 13 |

Note the `tuple` wording: the reference explicitly says `tuple` is not a function but an immutable sequence type. That does not weaken the E2 exemption (the name is still a callable builtin constructor over an iterable); it only means the page cannot be quoted as calling `tuple` a "function".

### F4. `Doc/library/collections.rst` — located quotes (observed, high confidence)
Verbatim RST:

| constructor | signature | quote | words |
|---|---|---|---|
| `deque` | `:459` `.. class:: deque([iterable, [maxlen]])` | `:461-462` "Returns a new deque object initialized left-to-right (using :meth:`append`) with data from *iterable*." | 14 |
| `Counter` | `:243-245` `.. class:: Counter(**kwargs)` / `Counter(iterable, /, **kwargs)` / `Counter(mapping, /, **kwargs)` | `:247` "A :class:`Counter` is a :class:`dict` subclass for counting :term:`hashable` objects." | 11 |
| `namedtuple` | `:860` `.. function:: namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)` | `:862` "Returns a new tuple subclass named *typename*." | 7 |

### F5. Host interpreter matches the pinned docs version (observed, high confidence)
`python3 -I -c 'import sys; print(sys.version)'` → `3.14.8 (main, Oct  2 2026, 10:23:31) [GCC 16.2.1 20260810]`. Saved: `fetch/SrcPyBuiltins/host-python-version.txt` (59 B, sha256 `214f9bf27d811a825f46edce52b5dceef6565dd113e4f4e82cd0b94fbd065e2f`). This is a version read only; the source row is anchored to the upstream tag, not the host binary.

### F6. Why two rows instead of one (inference, from the registry contract)
[INFERENCE] The 11-column row (S004 contract) carries one source and one anchor cell with one located quote/line range. Here there are two files at the same tag with distinct digests and disjoint line ranges (`Doc/builtins/functions.rst` for the builtin constructors, `Doc/library/collections.rst` for the stdlib ones); a single anchor cell would have to fuse two digests and two quote locations, making independent re-derivation ambiguous. Splitting keeps each row's anchor re-derivable on its own. This is a reading of the row shape, not a quoted rule.

### F7. Context: the pinned tool's pure table (observed, read-only)
At `e629f73`, `tools/mado-tripwire.py` is 367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d; its `PURE_ARG_CALLS` (`:1252-1256`) lists `tuple`, `set`, `dict`, `list` but **not** `frozenset` — the shape of the round-19 harm. Not this seat's file to change; the `frozenset` quote in F3 is the identity evidence such a repair can lean on. No judgement of the in-flight repair is made here.

## Draft rows (id `S1xx-pending`; L1 assigns S099-S110)

Both rows are opened but not yet mined: `status` is `queued`, `used-by` `—`. If the round-20 knowledge note lands citing them, L1 flips `status` to `mined` and `used-by` to `corpus/knowledge/tripwire-precision-r20.md` per the registry lifecycle.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S1xx-pending | CPython 3.14.8 built-in functions reference (the 3.14 docs tree; `Doc/library/functions.rst` is absent at this tag, content at `Doc/builtins/functions.rst`) — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/functions.rst | docs | A | the built-in container constructors named in the tripwire E2 exemption — `frozenset`, `set`, `tuple` — as documented for CPython 3.14.8 | tag v3.14.8 → annotated tag object `992560c2cc62d47b308cec662feb485456847931`, peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12`; file 97,140 B sha256 `f1b72170e6893ee6315108f74244df56a9725f2be2b8bf396f22cd6dcbd5d9de`; `Doc/builtins/functions.rst:865` `.. class:: frozenset(iterable=(), /)`, quote `:868-869` "Return a new :class:`frozenset` object, optionally with elements taken from *iterable*."; `:1821` `.. class:: set(iterable=(), /)`, quote `:1824-1825` "Return a new :class:`set` object, optionally with elements taken from *iterable*."; `:2079` `.. class:: tuple(iterable=(), /)`, quote `:2082-2083` "Rather than being a function, :class:`tuple` is actually an immutable sequence type" | defines `frozenset` and `set` as built-in class constructors returning a new object from an optional iterable, and `tuple` as an immutable sequence type — the identity facts the tripwire's E2 pure-callee exemption leans on when those names are not rebound; the no-spawn conclusion belongs to the tripwire contract, not the page | queued | 2026-10-20 | on-release | — |
| S1xx-pending | CPython 3.14.8 collections reference — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/collections.rst | docs | A | the stdlib container constructors/factories named in the tripwire E2 known-pure list — `deque`, `Counter`, `namedtuple` — as documented for CPython 3.14.8 | tag v3.14.8 → annotated tag object `992560c2cc62d47b308cec662feb485456847931`, peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12`; file 54,628 B sha256 `be2f90d14d3f488a9d5a6f23423e494a46b10a030d83d9308fd71af1f8eed7a7`; `Doc/library/collections.rst:459` `.. class:: deque([iterable, [maxlen]])`, quote `:461-462` "Returns a new deque object initialized left-to-right (using :meth:`append`) with data from *iterable*."; `:243-245` `.. class:: Counter(**kwargs)` / `Counter(iterable, /, **kwargs)` / `Counter(mapping, /, **kwargs)`, quote `:247` "A :class:`Counter` is a :class:`dict` subclass for counting :term:`hashable` objects."; `:860` `.. function:: namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)`, quote `:862` "Returns a new tuple subclass named *typename*." | documents `deque`, `Counter` and `namedtuple` as constructors/factories that build container objects from their arguments — the identity ground for the tripwire's known-pure `collections.*`/`namedtuple` exemption when those names are not rebound; the no-spawn conclusion belongs to the tripwire contract, not the page | queued | 2026-10-20 | on-release | — |

## Re-derivation commands

```
git ls-remote https://github.com/python/cpython refs/tags/v3.14.8 'refs/tags/v3.14.8^{}'
curl -sSL --max-time 60 https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/functions.rst | sha256sum
curl -sSL --max-time 60 https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/collections.rst | sha256sum
```

Expect `f1b72170e6893ee6315108f74244df56a9725f2be2b8bf396f22cd6dcbd5d9de` (functions) and `be2f90d14d3f488a9d5a6f23423e494a46b10a030d83d9308fd71af1f8eed7a7` (collections), and the two ls-remote lines in F1. Line locations re-check with `grep -n 'class:: frozenset\|class:: set\|class:: tuple' functions.rst` and `grep -n 'class:: deque\|class:: Counter\|function:: namedtuple' collections.rst`.

## Fetch receipts inventory

`fetch/SrcPyBuiltins/receipts.jsonl` — 6 lines, sha256 `fa5b93f5e242f6a97e52c7e38fa033627401ea5ea6b0d710f078b4fbf650fcde`; fetched at `2026-10-20T19:45:15Z`; tool line `curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 OpenSSL/3.6.5 zlib/1.3.2 brotli/1.2.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.5 libssh2/1.11.1 nghttp2/1.70.0 ngtcp2/1.25.0 nghttp3/1.18.0 mit-krb5/1.22.2`.

| body | http | bytes | sha256 |
|---|---|---|---|
| assigned-functions-404.txt | 404 | 14 | d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed |
| cpython-3.14.8-Doc-builtins-functions.rst | 200 | 97,140 | f1b72170e6893ee6315108f74244df56a9725f2be2b8bf396f22cd6dcbd5d9de |
| cpython-3.14.8-Doc-library-collections.rst | 200 | 54,628 | be2f90d14d3f488a9d5a6f23423e494a46b10a030d83d9308fd71af1f8eed7a7 |
| doc-library-stdtypes-404.txt | 404 | 14 | d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed |
| peeled-functions-404.txt | 404 | 14 | d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed |
| discovery-Doc-contents.json | 200 | 25,842 | fb6c0876de1edc6bacaea53b268abecb14eebb7b3b372470a99028d830e934c0 |

The GitHub contents listing is a discovery aid only; the row anchors are the tag/peeled-commit identity plus the raw file sha256, never the API listing.

## Limits

- Did not check the HTML docs at docs.python.org, nor any other 3.14 patch tag (v3.14.0-v3.14.7): when in the 3.14 series `Doc/library/functions.rst`/`stdtypes.rst` moved to `Doc/builtins/` is [UNK]; only the v3.14.8 tree was measured.
- Did not read CPython `Lib/collections/__init__.py` or the C implementation of the builtin constructors; the rows cite the reference documentation only, not behavior.
- Did not execute any constructor or fixture; no interpreter behavior is claimed.
- Did not verify release signatures or the 3.14.8 tarball against the tag; the anchor is the tag→commit mapping plus raw body digest.
- Did not assign final SOURCES ids, edit `corpus/SOURCES.md`, or decide `status` beyond the observed `queued`; L1 integrates and may flip to `mined` with the note's used-by.
- Did not evaluate the in-flight tripwire repair; F7 is a read-only observation of the pinned `e629f73` file.
- [INFERENCE] The doc-to-E2 "identity ground" phrasing is my mapping of the round-20 contract onto the quoted text; the pages themselves name no tripwire rule.
- LSP unavailability recorded: the quoted files are remote raw docs fetched to `.ufo/waves/round-20/fetch/SrcPyBuiltins/`, not workspace source; no language server answered them, so line locations are a literal `grep -n` of the fetched bytes (`file:line`), not semantic navigation.

## Installs

none
