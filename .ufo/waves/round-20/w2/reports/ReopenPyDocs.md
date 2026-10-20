# ReopenPyDocs — holds: S105/S106 re-fetch byte-identical to row and receipt, all six quotes verbatim at the cited lines, tag pin exact, and the rows support the note/SKILL callee-classification claim — with two scoped caveats

Item: re-open SOURCES rows S105 and S106 (`corpus/SOURCES.md:117-118`) and their Gate lines
(`corpus/lessons/round-20.md:42-43`): fetch each pinned URL, compare sha256 with row/receipt,
check the located quote verbatim at the stated lines and <= 25 words, check the tag→commit pin
by `git ls-remote`, and say whether the row supports what `corpus/knowledge/tripwire-precision-r20.md`
and `SKILL.md` say it supports.

Lane tip `a4046a8216080d4004de3f268c62cf142095ac07`; tool pinned `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`
(`tools/mado-tripwire.py` at `28c6837`, and identical at tip). My fetch bodies and receipts are under
`.ufo/waves/round-20/w2/ReopenPyDocs/fetch/`; my /tmp clone is `/tmp/mado-r20w2-ReopenPyDocs`.

## 1. Fetch bytes match the row and the stored receipt exactly

Command (bodies in my seat dir; full command lines in `fetch/receipts.jsonl`):

```
curl -sSL --max-time 60 -o s105-builtins-functions.rst -w '%{http_code} %{url_effective}\n' \
  https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/functions.rst
curl -sSL --max-time 60 -o s106-collections.rst -w '%{http_code} %{url_effective}\n' \
  https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/collections.rst
```

```
200 https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/functions.rst
200 https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/collections.rst
f1b72170e6893ee6315108f74244df56a9725f2be2b8bf396f22cd6dcbd5d9de  s105-builtins-functions.rst   (97,140 B)
be2f90d14d3f488a9d5a6f23423e494a46b10a030d83d9308fd71af1f8eed7a7  s106-collections.rst           (54,628 B)
```

* S105 row (`corpus/SOURCES.md:117`) pins `file 97,140 B sha256 f1b72170…` — **equal**, both size and digest.
* S106 row (`corpus/SOURCES.md:118`) pins `file 54,628 B sha256 be2f90d1…` — **equal**.
* The wave-1 receipt `.ufo/waves/round-20/fetch/SrcPyBuiltins/receipts.jsonl` (fetched_at
  `2026-10-20T19:45:15Z`) contains the same URL, same 200, same size, same digest for both bodies.
  No URL conflict: both are `raw.githubusercontent.com` tag URLs, not commit-range or mutable-branch aliases.
* `Doc/library/functions.rst` at this tag is 404 in that same receipt; I reproduced it myself:
  `404 https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/functions.rst`
  (body 14 B, sha256 `d5558cd4…`).
* The row's `on-release` recheck is current: `.ufo/waves/round-20/fetch/SrcPyBuiltins/host-python-version.txt`
  records `3.14.8 (main, Oct  2 2026, 10:23:31)`, the same release as the pinned docs tag, so no newer
  CPython release has invalidated the row.

## 2. Tag→commit pin is exact

```
$ git ls-remote https://github.com/python/cpython refs/tags/v3.14.8 'refs/tags/v3.14.8^{}'
992560c2cc62d47b308cec662feb485456847931	refs/tags/v3.14.8
8e6e75d9102e39bed2a2b279203a396741180f12	refs/tags/v3.14.8^{}
```

Row text: tag v3.14.8 → annotated tag object `992560c2…`, peeled commit `8e6e75d9…`. **Both match.**
The URL is served at the tag ref, so the fetched bytes are the tag's bytes.

## 3. Every located quote is verbatim at the stated lines and <= 25 words

Checked programmatically: join the cited line span, normalise whitespace, test the row's quoted
string as a substring; `grep -n` confirms the anchor line numbers.

| Row | location | cited lines | verbatim | words (whitespace / `\w+`) |
|---|---|---|---|---|
| S105 frozenset signature | `.. class:: frozenset(iterable=(), /)` | 865 | yes | 3 / 3 |
| S105 frozenset quote | "Return a new :class:`frozenset` object, optionally with elements taken from *iterable*." | 868-869 | yes | 11 / 12 |
| S105 set signature | `.. class:: set(iterable=(), /)` | 1821 | yes | 3 / 3 |
| S105 set quote | "Return a new :class:`set` object, optionally with elements taken from *iterable*." | 1824-1825 | yes | 11 / 12 |
| S105 tuple signature | `.. class:: tuple(iterable=(), /)` | 2079 | yes | 3 / 3 |
| S105 tuple quote | "Rather than being a function, :class:`tuple` is actually an immutable sequence type" | 2082-2083 | yes | 12 / 13 |
| S106 deque signature | `.. class:: deque([iterable, [maxlen]])` | 459 | yes | 4 / 4 |
| S106 deque quote | "Returns a new deque object initialized left-to-right (using :meth:`append`) with data from *iterable*." | 461-462 | yes | 13 / 16 |
| S106 Counter signatures | `.. class:: Counter(**kwargs)` / `Counter(iterable, /, **kwargs)` / `Counter(mapping, /, **kwargs)` | 243-245 | yes | 9 / 9 |
| S106 Counter quote | "A :class:`Counter` is a :class:`dict` subclass for counting :term:`hashable` objects." | 247 | yes | 10 / 13 |
| S106 namedtuple signature | `.. function:: namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)` | 860 | yes | 8 / 11 |
| S106 namedtuple quote | "Returns a new tuple subclass named *typename*." | 862 | yes | 7 / 7 |

`grep -n` anchors (on my fetched bytes): S105 `865:.. class:: frozenset`, `868:   Return a new
:class:`frozenset``, `1821:.. class:: set`, `1824:...set...`, `2079:.. class:: tuple`,
`2082:   Rather than being a function`; S106 `243:.. class:: Counter`, `247:    A :class:`Counter``,
`459:.. class:: deque`, `461:    Returns a new deque`, `860:.. function:: namedtuple`,
`862:    Returns a new tuple subclass`.

*(My first pass counted lines from a `read` display and appeared off by one for S105; `grep -n`
against the same bytes is authoritative and the row's numbers are correct. Recorded so no reader
re-derives the false lead.)*

**Nit on the Gate line, not on the row.** `corpus/lessons/round-20.md:43` declares the S106 gate
quote "(14 words)". The same sentence measures 13 whitespace tokens and 16 `\w+` tokens; neither
convention yields 14. The binding requirement (<= 25 words) holds under every counting method, and
the S105 gate's "(11 words)" is reproducible exactly. [UNK] which convention produced "14" — it does
not affect admission.

## 4. The "functions.rst moved" claim is true, not a raw-path artifact

Positive and negative control at the previous tag (my fetches, receipted):

```
200 https://raw.githubusercontent.com/python/cpython/v3.13.9/Doc/library/functions.rst   (95,637 B, sha 3ce8bc5f…)
404 https://raw.githubusercontent.com/python/cpython/v3.13.9/Doc/builtins/functions.rst
```

So the same URL pattern succeeds where the file is supposed to be and 404s where it is not; at
v3.14.8 the pattern is reversed. The row's parenthetical "`Doc/library/functions.rst` is absent at
this tag, content at `Doc/builtins/functions.rst`" is corroborated, not merely a 404. The GitHub
contents API (`/repos/python/cpython/contents/...`) returned **403 rate-limit**, not 404/200, so I
did **not** use it as evidence; it is receipted as a non-200 body only.

## 5. Independent instrument agrees

`fetch-verify.py` is the lane's probe for exactly this join; I ran the copy from my `/tmp` clone
(committed bytes at tip, `.ufo/waves/round-18/fetch-verify.py`) over the wave-1 fetch root:

```
$ python3 -I .ufo/waves/round-18/fetch-verify.py \
    --fetch-root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/fetch \
    --sources /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md --rows S105,S106 \
    --quote 'S105=Return a new :class:`frozenset` object, optionally with elements taken from' \
    --quote 'S106=Returns a new deque object initialized left-to-right (using :meth:`append`) with'
ROW S105 receipted
ROW S106 receipted
QUOTE S105 ok
QUOTE S106 ok
SUMMARY receipts=100 ok=99 bad=1 digest_only=0 non200=13 conflicts=0 rows=2 unreceipted=0 quotes=2 quote_bad=0
```

The run exits 1 solely because of an unrelated body, `SrcBashErrexit/bash-5.3.tar.gz MISSING`
(another seat's item); both of my rows credit and both quotes are found in the 200 body. My own
seven receipts also re-hash: `SUMMARY receipts=7 ok=7 bad=0 ... rc=0`.

## 6. Do the rows support what the knowledge note and SKILL say?

What is claimed by them:

* `corpus/knowledge/tripwire-precision-r20.md:1` lists S105 (CPython 3.14.8 builtins) and S106
  (collections) as the identity sources; `:20` says no row when "the callee is provably data: a
  builtin not rebound in the text (S105; `frozenset`, `tuple`, …), a pure stdlib callable (S106,
  S107; `deque`, `Counter`, `namedtuple`, `shlex.join`, `json.dumps`)".
* `SKILL.md:553`: "Pure data gives no row: builtins and pure stdlib callables (frozenset, deque,
  `shlex.join`, `json.dumps`, S105–S107) unless the text rebinds the name".
* The tool implements exactly this name-based rule: `PURE_ARG_CALLS` includes `tuple`, `set`,
  `frozenset` (`tools/mado-tripwire.py:1396-1407`); `PURE_STDLIB_MODULES` includes `collections`
  as a whole prefix (`:1408-1410`); `callable_info` consults the binding in effect before the
  builtin fallback (`:1451-1503`).

I ran the pinned tool bytes (sha `9613f510…`) in my `/tmp` clone on purpose-built transcript cells,
each as an `eval` py tool call (same shape as the precision suite):

| probe | verdict | matches note/SKILL? |
|---|---|---|
| `BLOCK=frozenset(['pacman','-Q','hyprland'])` | `clean`, rc 0 | yes |
| `set([...])`, `tuple([...])` plain | `clean`, rc 0 | yes |
| `from collections import deque; deque([...])` | `clean`, rc 0 | yes |
| `import collections; collections.deque([...])` | `clean`, rc 0 | yes |
| `import collections as c; c.deque([...])` | `clean`, rc 0 | yes |
| `Counter(['pacman','-Q','hyprland'])` | `clean`, rc 0 | yes |
| `namedtuple('Case','name argv')('m',[...])` | `clean`, rc 0 | yes |
| rebind `frozenset` / `deque` / `Counter` / `namedtuple` to `lambda a: subprocess.run(a)` | 1 `package_query` finding, `evidence: observed`, rc 1 in each | yes ("unless the text rebinds the name") |
| nested spawn inside a pure callee: `set(subprocess.run([...]))`, same for `frozenset`/`deque`/`tuple` | 1 `package_query` finding, `observed`, rc 1 in each | yes (exemption does not swallow the argument) |

The scored suite already carries the same cases and verdicts:
`P-CasePureBuiltins-frozenset-closure`, `P-AdoptW2-CriticC3W2-dc-{frozenset,deque,namedtuple}`
(`want_exit: 0`) and the rebinding controls `S-CaseShadowing-frozenset-def-spawn`,
`S-CaseShadowing-run-as-frozenset-control` (`want_exit: 1`, `package_query`/`pacman:-Q`,
`evidence: observed`) in `.ufo/waves/round-20/precision/expected.json`.

**Verdict on the support question: the rows support the claims as they are scoped.** The S105/S106
"teaches" cells only establish *identity* — `frozenset`/`set`/`tuple` are built-in class
constructors, `deque`/`Counter`/`namedtuple` are stdlib container constructors/factories — and both
rows explicitly refuse to extend that to behaviour: "the no-spawn conclusion belongs to the tripwire
contract, not the page". The note's no-row table row and SKILL's sentence are statements about the
*callee*, and the tool behaves that way in every probe above.

### Caveat 1 (prose precision, not a row defect): "provably data" is true of the callee, not of the expression

The documented constructor contract is itself a dispatch hook: set/frozenset take "elements taken
from *iterable*" (`:868-869`, `:1824-1825`), deque is "initialized … with data from *iterable*"
(`:461-462`). A locally defined iterable's `__iter__`/`__hash__` therefore runs inside `set(...)`.
With a *visible* spawner in that method the pinned tool still emits no row:

```
class X:
    def __iter__(self):
        return iter(subprocess.run(['pacman','-Q'], capture_output=True).stdout.splitlines())
s = set(X())
→ MADO_TRIPWIRE: clean   rc=0   (also clean: set(iter(X())); class E: def __hash__(self): subprocess.run(['pacman','-Q']) …; set([E()]))
```

That is consistent with the note's fourth clause ("a visible … class whose body has no spawn") if
"body" means the class body executed at definition, but a reader who takes "provably data" or
"Pure data gives no row" to mean "this expression cannot spawn" would be wrong. Suggested one-clause
addition to the SKILL "Still unanalysed" list: *protocol dispatch into a local class's
`__iter__`/`__hash__`/`__call__` reached through a pure constructor*. [INFERENCE] that this is out of
scope for round 20 (no counter in the suite exercises it); it is not evidence against S105/S106,
whose "teaches" cell states only identity and explicitly disclaims the no-spawn step.

### Caveat 2 (scope, acknowledged by the row): the exemption is broader than the three evidenced names

`pure_stdlib_path` exempts every `collections.*` path (`tools/mado-tripwire.py:1408-1410`,
`:1419-1420`), not only `deque`/`Counter`/`namedtuple`; `frozenset`/`set`/`tuple` sit in a list that
also contains `open`, `exec`, `eval`, `input` (`:1396-1407`). The S106 row's wording ("the identity
ground for the tripwire's known-pure `collections.*`/`namedtuple` exemption") acknowledges the
prefix breadth, and the collections page is the module reference, so the citation is in kind; but
the row evidences three names, not each member of the prefix. No counterexample found where a
`collections.*` callable executes a command. [INFERENCE] the `exec`/`eval` members of
`PURE_ARG_CALLS` are a separate, higher-risk design choice outside this item's two rows.

## Limits

* I did not re-run the C1/C2 counters or the recall split — other wave-2 seats own those; nothing
  here depends on their totals.
* The absence claim for `Doc/library/functions.rst` rests on the tag's raw 404 plus the 3.13.9
  positive/negative control; the GitHub contents API was rate-limited (403) and was not used.
* The protocol-dispatch probes are my own, built with the pinned tool bytes in `/tmp`; they are not
  scored cases and I did not modify the suite.
* Host pause respected: no pacman/expac/checkupdates, no sudo/systemctl/hyprctl/compositor probes,
  no live gate. Web access was `curl` only, receipted. Lane git was read-only (clone/show/log);
  no `jj` was run.

## Installs

none.
