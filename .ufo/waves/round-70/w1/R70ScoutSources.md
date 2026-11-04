# R70ScoutSources — independent source opening + registry reconnaissance (read-only)

- lane/round: mado r70, w1, seat `R70ScoutSources`; axes **C1 calibration** and **C2 operability**.
- base rev (frozen): `b37a5aec4ea03f2223d8e09dd5d386d055c24179`.
- lane HEAD observed twice during the seat: `5144a6b5f43225d8021a469f4d24c19558026b9e`, then
  `71caa8b7d3eb6efa1d5a701a1467b1cfec50f0ab` (L1 integrating concurrently). `corpus/SOURCES.md` is
  byte-identical at base and HEAD: `git diff --stat b37a5aec..HEAD -- corpus/SOURCES.md` → no output,
  rc 0; base blob `3f751b380913e90ff75e20dcaee34786e0864cdd` == `git hash-object corpus/SOURCES.md`.
- frozen declaration: `.ufo/waves/round-70/claims-declaration-r70.md`, 8,921 B, sha256
  `01aa0d23d726f836d142e513e73ff70ee5b3d3618c8d8fe185f63585f731501a` (read first; not edited).
- receipt: `.ufo/waves/round-70/w1/R70ScoutSources/sources-r70.json`.
- writes: only the receipt + this report + `/fast/scratch/hyaku/mado-r70/R70ScoutSources/` (removed
  before yield). No production path, no git/jj mutation, no package manager, no desktop probe.

## 1. Fetch — three times each, byte-identical

Command shape: `curl -sS -L --max-time 60 -o <out> -w '%{http_code}' <URL>`; sha256 via
`sha256sum`; identity via `cmp -s <a> <b>`.

### F1 — `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst`

| attempt | curl rc | HTTP | bytes | sha256 |
|---|---|---|---|---|
| 1 | 0 | 200 | 61,603 | `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd` |
| 2 | 0 | 200 | 61,603 | same |
| 3 | 0 | 200 | 61,603 | same |

`cmp` 1v2 → 0, 2v3 → 0. 1,622 lines.

### F2 — `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/expressions.rst`

| attempt | curl rc | HTTP | bytes | sha256 |
|---|---|---|---|---|
| 1 | 0 | 200 | 92,034 | `e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a` |
| 2 | 0 | 200 | 92,034 | same |
| 3 | 0 | 200 | 92,034 | same |

`cmp` 1v2 → 0, 2v3 → 0. 2,407 lines.

**No 404 occurred** on either URL; no fallback tag was needed. Tag pin
(`git ls-remote https://github.com/python/cpython 'v3.14.8' 'v3.14.8^{}'`, rc 0): tag object
`992560c2cc62d47b308cec662feb485456847931`, peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12`
— identical to the pin already recorded in registry row S108.

### F3/F4 — supporting fetches (not named by the declaration)

- `.../Doc/reference/simple_stmts.rst` — 3 attempts, curl rc 0, HTTP 200, 41,375 B,
  sha256 `d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc`, `cmp` 1v2 → 0.
  Fetched because the assignment-target sentence the brief places in `expressions.rst` is not there.
- `.../Doc/library/ast.rst` — 1 attempt, curl rc 0, HTTP 200, 92,619 B,
  sha256 `9908f4f029c3258bdfb9ffa6af69d2bca5bd17ff2f175f92a71303d43699ab85`. Reject candidate.

## 2. `Popen.returncode` (subprocess.rst) — the negative value is a signal death

Block header `.. attribute:: Popen.returncode` at **:949**; quote at **:958-959**:

```
955|    A ``None`` value indicates that the process hadn't yet terminated at the
956|    time of the last method call.
957|
958|    A negative value ``-N`` indicates that the child was terminated by signal
959|    ``N`` (POSIX only).
960|
961|    When ``shell=True``, the return code reflects the exit status of the shell
962|    itself (e.g. ``/bin/sh``), which may map signals to codes such as
```

Quote (15 words): "A negative value ``-N`` indicates that the child was terminated by signal
``N`` (POSIX only)." — **occurs twice in the file** (:141-142 in the `CompletedProcess` block,
:958-959 here). A row must say *Popen* to be unambiguous.

**The "exit status is the child's" sentence is present** — the paragraph's first sentence,
**:951**: "The child return code." The more explicit wording "Exit status of the child process."
is in the `CompletedProcess.returncode` block at **:138**. Both attribute the status to the child,
not to any assertion layer.

Two further nonzero causes sit in the same document:

- **:722-726** (`Popen` `versionchanged:: 3.8`): "no longer raise an exception on errors like
  missing program, but the child process fails with a non-zero returncode" (19 words) — the
  *ordinary missing program* cause.
- **:961-963**: under `shell=True` the code is the shell's own exit status, "which may map signals
  to codes such as ``128+N``" (24 words).
- **:1508** doctest: `(127, 'sh: /bin/junk: not found')`, contrast **:1510** `(-15, '')`.
- **:162** (`check_returncode`): "If :attr:`returncode` is non-zero, raise a
  :exc:`CalledProcessError`." — the library's own failure predicate is exactly `rc != 0`.

### What this grounds about "nonzero rc = failed assertion"

**Grounds (the negative the C1 claim needs).** Status is the *child's* (:951, :138). Status space
is many-to-one: signal death is reported as `-N` (:958-959), a missing program yields nonzero
(:725-726, :1508), and under `shell=True` the code is the shell's (:961-963). So `rc != 0` is
consistent with a crash, a signal death and a missing program — it cannot *mean* "the mutant's
assertions failed". A harness whose kill credit is `rc != 0` inherits that ambiguity.

**Does NOT ground.**
1. The claim's third enumerated cause, **"a usage error", is not in this document**:
   `grep -w -i usage subprocess.rst` → rc 1 (zero matches). Two of three named causes are located;
   the third is unsupported here and must be dropped or sourced elsewhere (shell/argparse).
2. Nothing about tests, assertions, harnesses or an `mz=` field appears. The *positive* half of the
   C1 design — credit only on a parsed failed-assertion summary — is a **design choice**, not a
   documented fact, and `grep` for "assert" finds no test-framework material.
3. It does not establish that a parsed summary is *sufficient*; it only removes the sufficiency of
   rc alone.
4. It says nothing about the lane's own `MADO_LANDING_COUNTERS_SELFTEST:` grammar.

## 3. `expressions.rst` — dictionary display `**` and the subscription target

### (a) Dictionary display, quote at :515-516 (block :510-517)

```
511|    unpacking; dictionary
512|    single: **; in dictionary displays
513|
514| A double asterisk ``**`` denotes :dfn:`dictionary unpacking`.
515| Its operand must be a :term:`mapping`.  Each mapping item is added
516| to the new dictionary.  Later values replace values already set by
517| earlier dict items and earlier dictionary unpackings.
```

Quote (15 words): "Its operand must be a :term:`mapping`.  Each mapping item is added to the new
dictionary." (definitional sentence at :514; grammar at :499,
`dict_item: expression ":" expression | "**" or_expr`).

### (b) Subscription as an assignment target — **the requested sentence is NOT in this file**

What `expressions.rst` actually says, **:1161-1165**:

```
1158| See :meth:`~object.__getitem__` documentation for how built-in types handle
1159| subscription.
1160|
1161| Subscriptions may also be used as targets in :ref:`assignment <assignment>` or
1162| :ref:`deletion <del>` statements.
1163| In these cases, the interpreter will call the subscripted object's
1164| :meth:`~object.__setitem__` or :meth:`~object.__delitem__`
1165| :term:`special method`, respectively, instead of :meth:`~object.__getitem__`.
```

Quote (12 words): "Subscriptions may also be used as targets in :ref:`assignment <assignment>` or
:ref:`deletion <del>` statements."

Read-path analogue, **:1137-1140**: "At runtime, the interpreter will evaluate the primary and the
subscript, and call the primary's `__getitem__` or `__class_getitem__` special method with the
subscript as argument."

The **evaluation-order sentence** the brief quoted ("the primary and the index expression are
evaluated, then the item is assigned") is in **`Doc/reference/simple_stmts.rst:190-194`**, not here:

```
187|      pair: subscription; assignment
188|      pair: object; mutable
189|
190| * If the target is a subscription: The primary expression in the reference is
191|   evaluated.
192|   Next, the subscript expression is evaluated.
193|   Then, the primary's :meth:`~object.__setitem__` method is called with
194|   two arguments: the subscript and the assigned object.
```

Quote (20 words): "If the target is a subscription: The primary expression in the reference is
evaluated. Next, the subscript expression is evaluated."

### What these ground about a splat carrier and a name-valued key

- **Splat carrier** — :514-516: the `**` operand must be a mapping and each mapping item is added
  to the new dictionary *at that site*. A module-level literal-name mapping constant expanded with
  `**` therefore contributes its items (including a guard key) to the env mapping being built: it
  is a value carrier, not a textual mention.
- **Name-valued key** — simple_stmts.rst:190-194 (and expressions.rst:1163-1165, 1137-1140): the
  primary is evaluated, then the subscript expression is evaluated, and `__setitem__`/`__getitem__`
  receives the *subscript object*. A literal-name string constant used as the subscript key lands
  by value, not by spelling.

**Does NOT ground.** That the constructed mapping reaches a `git` child as its environment (that is
held S438, `git.adoc:928-929`); that the four carrier shapes are the only remaining ones; or that a
static reader can decide dominance soundly — the shape list and dominance flows are the lane's
frozen rule, not CPython semantics. It also says nothing about aliasing/attribute mutation order or
computed `**` operands beyond the one-hop forms the rule admits.

## 4. Registry reconnaissance (lane head)

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```
rc **0**; 38 output lines = **36 × W04** (duplicate url across scopes) + **1 × W01** + the summary
line:

```
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

`... census --root /home/vgpnk/Projects/shokunin mado` (rc 0): `rows 375`, `tier.A 361`, `tier.B 7`,
`tier.C 7`, `status.mined 354`, `status.queued 10`, `status.rejected 11`, `FLEET.missing 0`.

Data rows under the census's own **0-3 leading ASCII space** rule (`sources-census.sh:40,573`;
`^ {0,3}\|` inside `## Registry`, header + separator skipped), counted independently with a `gawk`
replica of `row_pass()`: **375** — agrees with the census. Base rev `b37a5aec` also **375**
(blob identical).

- id range: **S001 … S438**, 375 unique, 0 duplicates. **Highest S-id = S438. Next free = S439.**
- `grep -rn 'S439\|S440\|S441' .ufo/waves/round-70/` → 0 hits (no sibling has proposed one).
- **`subprocess.rst` URL already has a row: S108** (`grep -n` → line 120), `docs | A | mined`, with
  the *same* sha256 `05cd782c…` and byte count 61,603. Its anchor is `run :38-43, Popen :359-366,
  Popen.args :898-900` — it does **not** cover the returncode block (:949-965) or :722-726.
- **`expressions.rst` URL has no row** (`grep -n` → rc 1). Same for `ast.rst`.
- same family: S111/S120/S121 are `Doc/reference/executionmodel.rst` (`spec`, tier A).

## 5. Rejection — `Doc/library/ast.rst`

Fetched (HTTP 200, 92,619 B, sha256 `9908f4f0…`). It documents the **`ast` module**: "helps Python
applications to process trees of the Python abstract syntax grammar" (:18-19), the abstract grammar
from `Parser/Python.asdl` (:32-36), and the node classes. For a `**` display it says, at **:450-452**:
"the expression to be expanded goes in the ``values`` list, with a ``None`` at the corresponding
position in ``keys``" (19 words); `Subscript(value, slice, ctx)` at :757.

**Rejected**: it documents the *parse-tree representation* — the classifier's implementation shape —
not runtime behaviour. It says nothing about mapping items entering a constructed dict, nothing
about `__setitem__`, and nothing about an environment reaching a child process. A **runtime**
carrier claim cannot be grounded by a document about AST node shapes.

**Flip condition**: admit only if the claim becomes the reader-implementation form — "a static
reader must recognise `**` as a `Dict` node whose `keys` list holds `None` at that position, and a
subscript as `Subscript(value, slice, ctx)`" — i.e. a claim about the reader's own walk.

## 6. Corrections the L1 must apply

1. **C1**: drop or separately source the "usage error" cause — `usage` occurs **0 times** in
   subprocess.rst. The other two causes and the child-attribution are located. Present "credit only
   on a parsed failed-assertion summary" as design, not as sourced fact.
2. **C2**: the declaration's sourced-ground sentence points at expressions.rst for "the dictionary
   display and subscription-assignment grammar". The dictionary display is fully there (Q7); the
   **assignment evaluation-order sentence is in `simple_stmts.rst:190-194`**. Either cite both
   documents in the lesson's `## Gate`, or quote only expressions.rst:1161-1165 + :1137-1140 and do
   not claim the order sentence from it.
3. **Row ids**: subprocess URL is not a new URL — S108 already carries it at the identical sha256.
   The returncode passage needs a **new row at a distinct scope** (the header allows no in-place
   edit of scope/anchor/teaches), which will raise **W04** (cross-scope duplicate URL) — a warning;
   validate stayed rc 0 with 36 W04 rows already. Adoption: **S439** for one of the two, **S440**
   for the other, subject to L1 ordering. Keep scopes distinct from S108's to avoid **E04**.

## 7. Commands and exit codes

| command | rc |
|---|---|
| `curl ... subprocess.rst` ×3 | 0,0,0 (HTTP 200 ×3) |
| `curl ... expressions.rst` ×3 | 0,0,0 (HTTP 200 ×3) |
| `curl ... simple_stmts.rst` ×3 | 0,0,0 (HTTP 200 ×3) |
| `curl ... ast.rst` ×1 | 0 (HTTP 200) |
| `cmp -s` F1 pairs, F2 pairs, F3 pair | 0 each |
| `git ls-remote ... v3.14.8` | 0 |
| `sources-census.sh validate ... mado` | 0 |
| `sources-census.sh census ... mado` | 0 |
| `grep -n 'Doc/library/subprocess.rst' corpus/SOURCES.md` | 0 (1 hit) |
| `grep -n 'Doc/reference/expressions.rst' corpus/SOURCES.md` | 1 (0 hits) |
| `grep -w -i usage subprocess.rst` | 1 (0 hits) |
| `jq -e . sources-r70.json` | 0 |

Scratch `/fast/scratch/hyaku/mado-r70/R70ScoutSources/` removed before yield (verified absent).
