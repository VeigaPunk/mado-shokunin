---
source: S447 (CPython v3.14.8 Doc/reference/simple_stmts.rst:972-980, global), S448 (Doc/library/os.rst:184-198, os.environ), S449 (Doc/library/subprocess.rst:88-91, env); S-ids assigned by L1.
verified-at: 1459cca11fb5d3956a6e9a128217852dd0c28cb9 (instrument and frozen control bytes; receipt provenance qualified below)
recheck: `python3 -I quality/counters/c2-r73-shapes.py --repo . --rev 1459cca11fb5d3956a6e9a128217852dd0c28cb9 --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce --controls .ufo/waves/round-73/controls/c2-cases-r73.json --scratch-root <scratch>`; expected TARGET_MET, not rerun by this scribe.
---

# Guard carriers: global declarations and mutated process environment (r73)

## Claim and axes

| item | bounded statement |
|---|---|
| C2 axis | Operability: widen the census carrier grammar, not the production population. |
| C1 companion axis | Calibration is independently declared; this entry does not claim its mutation result. |
| New carrier A | A function declares a name `global`, stores the guard key into that mapping, and a later git launch hands it as `env=NAME`. |
| New carrier B | A store into `os.environ` reaches a launch through either of two exact environment-copy spellings. |
| Guard key | `GIT_NO_REPLACE_OBJECTS`; key presence is counted, not its value's effectiveness. |
| Measurement | Successor 28/28; held round-71 classifier 25/28 on the same frozen cases. |
| Population | Twenty `quality/check-*.py` files; thirteen readers, thirteen guarded, zero unguarded. |

The three extra positives are carrier recognition, not three additional production readers.

## Provenance and evidence classes

| surface | provenance | what it supports |
|---|---|---|
| Declaration | `.ufo/waves/round-73/claims-declaration-r73.md`, C2 and declared limits | Frozen target, counting command, kill rule and scope. |
| Base | `d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce` | Held round-71 classifier reference. |
| Freeze | `87e4c61ac90e9ac587c9f65ac7844ded268d9046` | Frozen declaration, control sets and baseline. |
| Instrument | `quality/counters/c2-r73-shapes.py` at `1459cca11fb5d3956a6e9a128217852dd0c28cb9` | Implemented syntax and line-order approximation. |
| Control bytes | `.ufo/waves/round-73/controls/c2-cases-r73.json` at the instrument revision | Twenty-eight expected reader/guard pairs. |
| Measurement receipt | `.ufo/waves/round-73/measurement-c2-r73.txt:1-81`, read from disk | Recorded candidate/base classifications; not a fresh scribe execution. |
| Baseline receipt | `.ufo/waves/round-73/control-baseline-r73.txt:8` | Pre-freeze held classifier's three named misses. |

Receipt provenance caveat: the scribe's `git show HEAD:.ufo/waves/round-73/measurement-c2-r73.txt`
returned rc 128: `fatal: path '.ufo/waves/round-73/measurement-c2-r73.txt' exists on disk, but not in 'HEAD'`.
The receipt reports the instrument revision; that is not proof the receipt itself is committed.
The L1 confirms the measurement receipts are on disk, uncommitted at read time; their evidence commit follows.

## Two carrier families, three frozen positives

| family | frozen case | construction | launch transport |
|---|---|---|---|
| Global mapping | `global-rebind-guard` | `global ENV` then `ENV["GIT_NO_REPLACE_OBJECTS"] = "1"` in `setup()` | Later git call has `env=ENV`. |
| Process environment | `environ-splat-guard` | `os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"` | `env={**os.environ}`. |
| Process environment | `environ-call-guard` | Same direct subscript store | `env=dict(os.environ)`. |

Control fixture locations: `c2-cases-r73.json:143-159` (path above).
The case named `global-rebind-guard` actually uses a subscript store, not a plain-name rebind.
The instrument additionally recognizes a global name rebound to a mapping carrying the key.
That extra syntax is implementation evidence, not a fourth scored positive.

## Carrier A: global-declared name

| stage | implementation evidence | constraint |
|---|---|---|
| Find declaration | `c2-r73-shapes.py:905-913` | Function or async-function contains a `global` declaration. |
| Find store | `:914-925` | Assignment subscript has the guard key, or global name receives a key-carrying mapping. |
| Find replacement | `:928-935` | Plain assignment of a non-key-carrying expression records a replacement line. |
| Find consumer | `:936-945` | Recognized git call, explicit `env=` keyword, bare matching name. |
| Order | `:943-944` | Store line strictly precedes launch; no recorded replacement strictly between. |
| Frozen envelope | Declaration C2 limits | One `global` declaration, no cross-module producer. |

`global` affects name interpretation; it does not prove that `setup()` executes before a call.
The census uses source-line order across functions, like the held attribute-flow approximation.
A function body can appear before the launch in the source but execute only after the launch.
Its store still counts under this approximation when the other syntactic conditions hold.
This is an explicit false-positive boundary, not execution-order or control-flow proof.

## Carrier B: direct os.environ store and copy

| stage | implementation evidence | constraint |
|---|---|---|
| Store | `c2-r73-shapes.py:968-975` | Direct `os.environ[KEY]` assignment; literal key or recognized module constant. |
| Replacement | `:976-977` | Assignment replacing exact `os.environ` cancels an earlier store before use. |
| Copy spelling 1 | `:951-952` | Exactly one dict-splat entry: `{**os.environ}`. |
| Copy spelling 2 | `:953-955` | Bare `dict` call, one positional `os.environ` argument, no keywords. |
| Consumer | `:980-988` | Recognized git call, `env=` is the copy expression, store line before call. |
| Frozen envelope | Declaration C2 limits | One direct store and these two copy spellings. |

No alias of `os.environ` is followed by this new transport rule.
`dict(os.environ, EXTRA="1")` is outside this exact copy predicate.
A held carrier may independently recognize another expression; new-rule refusal is not universal refusal.

## Frozen discrimination receipt

| frozen case | successor guard | held r71 guard | receipt lines |
|---|---|---|---|
| `global-rebind-guard` | yes | no | `measurement-c2-r73.txt:46,75` |
| `environ-splat-guard` | yes | no | `:47,76` |
| `environ-call-guard` | yes | no | `:48,77` |
| `global-rebind-value-only` | no | no | `:49,78` |
| `environ-store-after-call` | no | no | `:50,79` |
| Held unguarded dict splat | no | no | `:44,73` |
| Held env copy without key | no | no | `:45,74` |

All five added cases remain readers; only the first three should count as guarded.
The value-only case puts the key text in `LABEL`'s value, not in key position.
The after-call case puts the direct environment store after the launch in source order.
The two held round-71 negatives remain refused, rather than being swept into the wider grammar.

## Denominators and recorded gates

| quantity | recorded value | evidence |
|---|---|---|
| Population | 20 | `measurement-c2-r73.txt:3-22,81` |
| Readers | 13 | Per-file reader flags, `:3-22`; contract `:81`. |
| Guarded readers | 13 | Per-file guard flags, `:3-22`; contract `:81`. |
| Unguarded readers | 0 | Contract `:81`. |
| Candidate controls | 28/28 | Candidate classifications `:23-50`; contract `:81`. |
| Held controls | 25/28 | Base classifications `:52-79`; summary `:80`. |
| Exact held misses | Three named positives above | `:75-77`; pre-freeze `control-baseline-r73.txt:8`. |
| Carried round-71 cases | 23 | `measurement-c2-r73.txt:2`, `carried=yes`. |
| Verdict | `TARGET_MET` | `measurement-c2-r73.txt:81`. |
| Execution status | Assignment reports rc 0 | Receipt text has no standalone exit-status line; scribe did not rerun. |

`TARGET_MET` requires exactly population 20, readers 13, guarded 13, unguarded 0,
candidate correct 28, and held correct 25 (`c2-r73-shapes.py:1002-1005`).
The finite control score is `10 × controls / 28`: recorded successor 10.0000, held 8.9286.
These scores are not measured coverage over arbitrary Python programs.

## Integrity anchors

| bytes | pinned SHA-256 |
|---|---|
| Round-73 controls | `65e9464450d58f803ca626f7b7ce6bc4712f46710ac5707602601cee9ecf230d` |
| Held round-71 controls | `d7814de8815bb0d4146ceed612ddd3e03029763b7cbf769d868a96ce5cefe7df` |
| Held round-71 classifier | `253dee5db9d4372a28b857337857b134a7618c7cf5d8b4fc66ef417aa2658f45` |

Evidence: measurement receipt lines 1, 2, 51; pre-freeze baseline line 8 repeats classifier hash.
The first twenty-three fixture sources and expected pairs are carried forward unchanged.
The counter checks the frozen held file hash and corresponding case contents.

## Sourced semantics versus classifier claims

| source | upstream URL | inspected fetched lines | grounded fact |
|---|---|---|---|
| S447 | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst | `fetch/Doc_reference_simple_stmts.rst.1:972-980` | `global` interprets listed identifiers as globals throughout the scope. |
| S448 | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/os.rst | `fetch/Doc_library_os.rst.1:184-198` | `os.environ` represents process environment; direct modification updates it. |
| S449 | https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst | `fetch/Doc_library_subprocess.rst.1:88-91` | Explicit `env` mapping supplies the child environment instead of default inheritance. |

Fetch paths above are relative to `.ufo/waves/round-73/`.
The L1 assigned these S-ids; S449 shares its document with S442 but scopes the `env` paragraph.
Upstream semantics explain the carriers, not the classifier's soundness or measurement outcome.

## Limits and non-claims

| bound | consequence |
|---|---|
| One `global` declaration | No general interprocedural name-resolution claim. |
| Cross-function source-line order | A store executed after launch can still count if its source line comes first. |
| One direct `os.environ` store | No general mutation-history or environment-state analysis. |
| Two exact copies | No arbitrary constructor, extra-keyword copy, or inferred copy operation. |
| No `os.environ` alias | Aliased process-environment stores are outside the new rule. |
| No value interpretation | A present key with an ineffective value can still count. |
| No cross-module producer or new deeper alias chain | Held carrier bounds remain in force. |
| Syntactic git-reader rule | Not an audit of every possible subprocess or dynamic command construction. |
| Existing repository state | Guard recognition neither authenticates Git objects nor repairs earlier rewriting. |
| Evidence-only drafting | No tests, counter reruns, host probes, source fetches or product edits by this seat. |
