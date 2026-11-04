source: S439:514-517,1161-1165; S440:190-192 — CPython v3.14.8 `Doc/reference/expressions.rst` (sha256 `e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a`, 92034 bytes, 2407 lines) and `Doc/reference/simple_stmts.rst` (sha256 `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`, 41375 bytes, 1079 lines), both tag `v3.14.8`, fetched 2026-11-03 local / 2026-11-04Z — the dictionary-display, subscription-target and assignment-target grammar that makes a `**` operand and a name-valued subscript key real carriers of the environment key rather than mentions of its spelling; rows adopted by the L1 as S439:514-517 and S440:190-192
verified-at: 2026-11-03 (local, −03:00; 2026-11-04Z)
recheck: 90d — both URLs are tag-pinned, so re-fetch and re-hash on the 90-day cadence and immediately when a new CPython tag is adopted; also re-check when the census population regex or either frozen control set changes, or when the repaired gate set moves

# Lane gate guards: the four carrier shapes a name-level rule missed (MADO-R70-1)

## Scope

Lane-tooling scope only. This entry explains the mechanics behind round-70 claim
C2 (`claims-declaration-r70.md`, C2 §): which four environment constructions the
round-70 guard census accepts that the round-69 rule missed, why each is a carrier
of the key rather than a mention of its spelling, and what the frozen 17-case set
does and does not pin. It is not a desktop claim, not a state-cell truth claim, and
not an authenticity claim about repository objects. The round-69 key-position rule
and the three dominance flows stay in force and are restated here only where the
new carriers depend on them; the replacement rule and the object-read surface stay
in the held rows S436:20-24 and S437:198 (locators per the round-69 entry).

## 1. The documented ground (`[INF-docs]`, tag v3.14.8)

Three sentences from two pages of the CPython 3.14.8 language reference carry the
argument. The bytes are the lane's own fetches — `expressions.rst` (sha256
`e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a`, 92034 bytes,
2407 lines) and `simple_stmts.rst` (sha256
`d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`, 41375 bytes,
1079 lines), both at tag `v3.14.8`; the line numbers below are against those bytes.

The dictionary display says an unpacking is not a string occurrence but a
construction of the mapping:

> A double asterisk ``**`` denotes :dfn:`dictionary unpacking`.
> Its operand must be a :term:`mapping`.  Each mapping item is added
> to the new dictionary.  Later values replace values already set by
> earlier dict items and earlier dictionary unpackings.
> (S439:514-517, quoted verbatim including the document's inline role markup)

The subscription section says a subscript in *target* position stores through
`__setitem__`, so the key is the subscript expression's value, not its text:

> Subscriptions may also be used as targets in :ref:`assignment <assignment>` or
> :ref:`deletion <del>` statements.
> In these cases, the interpreter will call the subscripted object's
> :meth:`~object.__setitem__` or :meth:`~object.__delitem__`
> :term:`special method`, respectively, instead of :meth:`~object.__getitem__`.
> (S439:1161-1165, quoted verbatim including the document's inline role markup)

The assignment statement's target rules carry the store side of the same fact — a
subscript target is evaluated before the store, so the key is a value, not a
spelling:

> If the target is a subscription: The primary expression in the reference is
> evaluated.
> Next, the subscript expression is evaluated.
> Then, the primary's :meth:`~object.__setitem__` method is called with
> two arguments: the subscript and the assigned object.
> (S440:190-194, quoted verbatim; the list marker is elided)

The read-side counterpart on the expression page says the same of a read, with
`__getitem__` in place of `__setitem__`:

> At runtime, the interpreter will evaluate the primary and
> the subscript, and call the primary's :meth:`~object.__getitem__` or
> :meth:`~object.__class_getitem__` :term:`special method` with the subscript
> as argument.
> (S439:1137-1140, quoted verbatim including the document's inline role markup)

The consequence the census turns on is documentary. A `**GUARD` operand adds the
operand's items to the display even when `GUARD` is only a module-level name, so
the guard key is in the resulting mapping; a store `env[KEY] = "1"` with
`KEY` bound to the key's string stores that key because the subscript is evaluated
to a value (S440:190-194; S439:1161-1165). Both are carriers under the syntax, not
idioms the census invents. What
still has to be shown is delivery: the held row S438:928 (git.adoc:928) records
that the variable acts when it is "setting and exporting", so a carrier counts only
when the mapping it produces reaches `env=` at a call whose argv contains `git`.

## 2. What the held rule missed

The held round-69 classifier scores `13/17` on the round-70 frozen set and misses
exactly four cases, the four carriers below
(`.ufo/waves/round-70/control-baseline-r70.txt` § C2: `score=13/17`; the same
receipt shows the round-69 set itself at `11/11`). Each block is the frozen case's
`src` text reproduced verbatim from
`.ufo/waves/round-70/controls/c2-controls-r70.json` (sha256
`29947b4ce5890f5c977f3ec74bafd14ba12b0d581dcb03ef1e3b637017a778ff`, 17 cases).
Reader is `yes` in every case; the pair below is the frozen expectation against the
held rule's measured verdict.

| carrier | frozen expectation | held r69 measured | verdict |
|---|---|---|---|
| `alias-carried` | reader yes, guard yes | reader yes, guard no | MISS |
| `attribute-carried` | reader yes, guard yes | reader yes, guard no | MISS |
| `splat-carried` | reader yes, guard yes | reader yes, guard no | MISS |
| `constant-key` | reader yes, guard yes | reader yes, guard no | MISS |

### alias-carried

```python
def run(repo):
    base = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env = base
    alias = env
    alias["GIT_NO_REPLACE_OBJECTS"] = "1"
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
```

`env` and `alias` name the same mapping object; the store through `alias` mutates
the mapping later handed to the call as `env=env`. The held rule followed only
stores whose subscript base was itself env-named, so a guard applied through a
second name was invisible. The round-70 counter accepts the shape when a
non-env-named name is bound to an env-named mapping and the key is stored through
that alias, provided the env-named name reaches `env=` with no later unguarded
rebinding (`quality/counters/c2-r70-carriers.py:572-592`, the alias clause).

### attribute-carried

```python
class Runner:
    def __init__(self):
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env["GIT_NO_REPLACE_OBJECTS"] = "1"

    def head(self, repo):
        return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=self.env)
```

The guard key is stored on an attribute and the attribute is the `env=` value at
the launch. The held rule had no attribute clause at all; the round-70 counter
records the dotted attribute target and accepts the shape when that attribute is
handed to the call as `env=` (or first bound to an env-named name and then used),
again subject to dominance (`quality/counters/c2-r70-carriers.py:613-640`, the
attribute clause, whose dotted lookup is one dotted name).

### splat-carried

```python
GUARD = {"GIT_NO_REPLACE_OBJECTS": "1"}


def run(repo):
    env = {**os.environ, **GUARD}
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
```

`GUARD` is a module-level mapping literal that carries the key; the `**GUARD`
operand adds its items to the display that becomes `env`. The held rule counted a
dict literal's own keys and did not follow `**` into another name, so this shape
was missed. The round-70 counter expands one level of `**` when the operand is a
module-level name bound once to a mapping literal that carries the key
(`quality/counters/c2-r70-carriers.py:529-540` for the name set, `:595-610` for the
expansion), and `mapping_has_key` follows the same operand when the display is the
`env=` value directly (`:167-171`).

### constant-key

```python
KEY = "GIT_NO_REPLACE_OBJECTS"


def run(repo):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env[KEY] = "1"
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
```

`KEY` is a module-level string constant whose value is the guard key; the subscript
store evaluates `KEY` and stores under that value (S440:190-194,
S439:1161-1165). The held rule accepted a subscript store only when the subscript
was the literal string, so a name bound once to that literal was missed. The
round-70 counter resolves the subscript through module-level literals bound exactly
once (`quality/counters/c2-r70-carriers.py:504-520` for the binding rule,
`:523-526` for the key-valued name set, `:543-547` for the subscript test) — a
module-level constant counts only when the module binds it once to a literal.

The two other new cases in the 17 are not carriers but git-launch negatives:
`guarded-env-for-a-non-git-call` (a guarded mapping handed to `ls`, while the git
call receives a keyless mapping) and `git-called-without-env` (a guard constructed
and never handed to the launch). Both were already `(reader yes, guard no)` under
the held rule and stay there; they pin that the carrier clauses cannot be reached
without one of the three dominance flows.

## 3. The rule as one sentence

Round-69 key position and the three dominance flows stay in force; each new carrier
must still reach the `git` launch; a module-level constant counts only when the
module binds it once to a literal.

The four clauses that sentence adds are: (a) *alias* — a name bound to an env-named
mapping, guarded through that alias while the env-named name is the one handed to
the call; (b) *attribute* — the key stored on a dotted attribute and that attribute
handed as `env=`; (c) *splat* — a module-level literal mapping carrying the key,
expanded with `**` into the env display; (d) *constant key* — a module-level string
constant equal to the key, used as the subscript key.

## 4. The seventeen frozen cases

All seventeen at `.ufo/waves/round-70/controls/c2-controls-r70.json` (sha256
`29947b4c…`, 17 cases). "Reader" is the frozen reader rule (a `git` token plus one
of the object-read verbs); "guard" is the frozen classifier verdict. The first
eleven are the round-69 set carried forward byte-identically
(`.ufo/waves/round-69/controls/c2-controls-r69.json`, sha256 `975ca3ba…`, 11
cases); the last six are new.

| case | reader | guard | what it pins | set |
|---|---|---|---|---|
| `guarded-inline` | yes | yes | flow (a): inline `env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")` on the launch | held |
| `value-position-only` | yes | no | key position: the same string as a *value* constructs no guard | held |
| `dead-branch-only` | yes | no | a store under `if False:` is not a live construction | held |
| `uncalled-helper` | yes | no | a helper that builds a guard and is never called guards nothing | held |
| `overwritten-env` | yes | no | an env-named binding rebound to a keyless mapping before use carries no guard | held |
| `update-guard` | yes | yes | key position through the `env.update(KEY="1")` keyword | held |
| `subscript-guard` | yes | yes | key position through `env[KEY] = "1"` in a local producer used as `env=env` | held |
| `module-constant` | yes | yes | flow (b) with a module-level mapping constant guarded by subscript | held |
| `producer-helper` | yes | yes | flow (b) producer call: `env = git_env(work)` then `env=env` | held |
| `argv-name-flow` | yes | yes | argv bound to a name and `env=` a producer call at the launch | held |
| `mention-only` | yes | no | the key in a docstring and a comment with `env=dict(os.environ)` is a mention | held |
| `alias-carried` | yes | yes | carrier (a): guard applied through a non-env-named alias of the env-named mapping | new |
| `attribute-carried` | yes | yes | carrier (b): key stored on `self.env`, attribute handed as `env=` | new |
| `splat-carried` | yes | yes | carrier (c): module-level literal mapping carrying the key, expanded with `**` | new |
| `constant-key` | yes | yes | carrier (d): module-level string constant equal to the key, used as the subscript key | new |
| `guarded-env-for-a-non-git-call` | yes | no | dominance is per launch: a guarded env handed to `ls` does not guard the git call | new |
| `git-called-without-env` | yes | no | a guard built but not handed to the `git` launch is not a guard | new |

A case is correct iff both fields match its frozen expectation. The held rule
scores `13/17` (the four carriers missed); the round-70 target is `17/17` with
`base_controls=13/17` (declaration C2 §, "After"). The counter asserts both control
digests before scoring and refuses with rc 2 on a mismatch
(`quality/counters/c2-r70-carriers.py:709-717`), and re-checks that the round-69
file still carries the same eleven cases.

## 5. Population boundary

Population: every tracked file matching `^quality/check-[^/]+\.py$`
(`quality/counters/c2-r70-carriers.py:74`), read through a scrubbed git environment
(`:104-109`). At the base rev `b37a5aec…` the regex matches 20 files; the frozen
predicate requires the same 20 at the measured rev, with `readers=13`,
`guarded=13`, `unguarded=0` (`:79-81`, `:696-699`), because a stricter rule that
reclassified a real file is reported, not tolerated.

```
quality/check-anchor-cover.py      quality/check-landed-contract.py
quality/check-axis-scores.py       quality/check-locators.py
quality/check-control-receipts.py  quality/check-population.py
quality/check-counter-discrimination.py
                                   quality/check-r38-discrimination.py
quality/check-deliverables.py      quality/check-r55-controls.py
quality/check-evidence-pointers.py quality/check-r56-controls.py
quality/check-freeze-order.py      quality/check-round-outcome-first.py
quality/check-index-rows.py        quality/check-session-material.py
quality/check-index.py             quality/check-state-cite.py
quality/check-tool-ledger.py       quality/check-wave-done.py
```

What stays outside the population, and is therefore not counted either way:

- **Container and deeper attribute flow.** A mapping held in a list, dict or
  object attribute beneath the one dotted name (`holder.env[KEY] = …`,
  `cfg["env"][KEY] = …`, `self.runner.env`) is not followed; the attribute clause
  covers one dotted name only.
- **The `dict(**GUARD)` call form.** The committed classifier counts a `dict(…)`
  call by *named* keywords only (`kw.arg == KEY`, `:176-178`) and expands `**`
  only inside an `ast.Dict` display (`:595-610`); a `**` keyword unpacking into a
  `dict(...)` call has `kw.arg is None`, so that spelling of the splat carrier is
  not followed and a guard written only that way would be counted unguarded.
- **Two-module producers.** An env mapping imported from another module, or a
  guard producer living in another module, is not followed; the census is one
  module, one hop.
- **Non-`check-` instruments.** `quality/counters/*.py`, `tools/*.py` and
  `tools/mado-receipt-citecheck.py` are outside the regex. The r67 wider lexical
  reader set is likewise outside.
- **Shell scripts.** `quality/landing-counters.sh:8` guards by a shell `export`,
  which is dominant at runtime and invisible to this census — a declared
  population boundary, not a claim that those instruments are unguarded.

## 6. What the green line does not prove

- It does not interpret the guard's value: `GIT_NO_REPLACE_OBJECTS=0` also
  disables replacement, and any non-empty value counts.
- It does not authenticate objects and does not repair a repository whose objects
  were already rewritten; it refuses the documented replacement channel only.
- It is a bounded syntactic approximation: one module, one hop, no container flow
  beyond a one-level `**` of a module-level literal mapping, no cross-module
  producer, no path-sensitivity beyond a literal-false branch, and no attribute
  chain longer than one dotted name in the guarded position
  (`quality/counters/c2-r70-carriers.py:54-58`).
- It scores committed source text at a revision: a dead but reachable guard still
  counts, and a guard wired into a call that never runs at runtime still counts.
- The four shapes are *named* ones, not an enumeration of the remaining Python
  constructions; a fifth unlisted spelling is not covered by the claim.
- It says nothing about the desktop, compositor, session, service or package
  state, and nothing about other lanes' instruments.

## Evidence rows

One row per proposition this entry turns on. The rows citing
S439:514-517,1137-1140,1161-1165 pin the fetched
`expressions.rst` bytes at tag `v3.14.8` (sha256
`e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a`, 92034 B, 2407
lines); the held S438:928 row pins the exported-environment sentence already landed in
the round-69 entry, not re-fetched here.

| id | claim the row grounds | source | locator |
|---|---|---|---|
| K01 | A `**` operand in a dictionary display is dictionary unpacking whose mapping items are added to the new dictionary, so a module-level mapping name is a real carrier. | S439 | expressions.rst:514 |
| K02 | Later unpackings replace earlier values, so a `**GUARD` placed after other operands leaves the guard key in the display. | S439 | expressions.rst:516 |
| K03 | A subscript used as an assignment target stores through `__setitem__`; the key is the evaluated subscript, not its spelling. | S439 | expressions.rst:1161 |
| K04 | An assignment to a subscription evaluates the subscript expression before `__setitem__` is called, which is why a module-level string constant can name the guard key. | S440 | simple_stmts.rst:190 |
| K05 | The variable acts when it is "setting and exporting": a guard is the environment that reaches the child, so every new carrier still needs dominance. | S438 | git.adoc:928 |

## 7. Recheck and provenance

- Fetch: `curl -sSfL -o expressions.rst https://raw.githubusercontent.com/python/
  cpython/v3.14.8/Doc/reference/expressions.rst` (2026-11-03 local, −03:00; 2026-11-04Z)
  → sha256
  `e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a`, 92034 bytes,
  2407 lines; tag `v3.14.8`.
- Line numbers were checked against those bytes: the dictionary-unpacking
  paragraph is L514-517, the subscription-target paragraph L1161-1165, and the
  runtime-evaluation paragraph L1137-1140.
- Control sets: `.ufo/waves/round-70/controls/c2-controls-r70.json` sha256
  `29947b4ce5890f5c977f3ec74bafd14ba12b0d581dcb03ef1e3b637017a778ff`, 6142 bytes,
  17 cases; `.ufo/waves/round-69/controls/c2-controls-r69.json` sha256
  `975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9`, 3723 bytes,
  11 cases. The eleven held cases compare equal, in order, to the first eleven of
  the round-70 file; the key field is identical.
- Before/after: the held rule scores `controls=13/17` on the frozen set and misses
  `alias-carried`, `attribute-carried`, `splat-carried`, `constant-key`
  (`.ufo/waves/round-70/control-baseline-r70.txt` § C2). That receipt is
  pre-freeze evidence; the measured verdict at `REV` is the counter's own line,
  not restated here.
- Scored instrument: `quality/counters/c2-r70-carriers.py` at
  `5144a6b5f43225d8021a469f4d24c19558026b9e` (blob sha256
  `87ca466432302feaabf2c504dc131184178afe199d8b84fa492ad3b5211af9f7`); the
  line numbers above are against those bytes. The only later change to the file
  relabels the per-case receipt with `leg=candidate|base`; no classification
  clause moved.
- Population: `git ls-tree -r --name-only b37a5aec…` filtered by the frozen regex
  prints 20 paths; the frozen reader and guarded counts (`13`, `13`, `0`) are the
  counter's declared predicate, re-derived at `REV`, not a number this entry
  measured.
- Cadence: on-release (the reference URL is tag-pinned; a new tag is the change
  event), with the re-fetch triggers above: re-check both control digests and the
  population regex if any of them moves, and re-run the 17 cases when a gate's env
  construction changes.
