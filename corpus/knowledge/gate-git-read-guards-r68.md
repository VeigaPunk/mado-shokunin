source: S437 — git v2.56.0 `Documentation/git-cat-file.adoc` (tag v2.56.0, fetched 2026-11-03, sha256 6c32dbda8c2106be08bda471592db50b5afaf185de32f2e513e80d802b4a95b2, 16099 bytes) — the object-read contract behind the round-68 census vocabulary, its rev-parse naming delegation, and the one documented mode that bypasses replacement
verified-at: 2026-11-03
recheck: 90d — re-fetch the tag's adoc and re-hash it; also when the host git leaves 2.56.0, when the census population regex or its frozen verb vocabulary changes, or when the repaired gate set moves

# Lane gate git reads: the object-read surface, the census's environment shapes, and what the guard cannot prove (MADO-R68-1)

## Scope

Lane-tooling scope only. This entry explains the mechanics behind round-68
claim C2 (`claims-declaration-r68.md:82-136`): which git verbs the standing
lane gates use to read repository objects, why a planted `refs/replace`
changes what such a read returns, which environment constructions the census
`quality/counters/c2-r68-reader-guard.py` counts as a guard, where the
counted population begins and ends, what the round repaired, and what the
resulting `guarded=13 unguarded=0` line does not establish. It is not a
desktop claim, not a state-cell truth claim, and not an authenticity claim
about repository objects. The replacement rule itself is anchored in the
held row S436 (`corpus/knowledge/replace-ref-citation-boundaries-r67.md`);
this entry opens S437 for the object-read side the census vocabulary turns
on, and states explicitly which sentence comes from which source.

Host git measured for the fetch: `git --version` → `git version 2.56.0`.

## 1. The object-read verb family (`[INF-docs]`, tag v2.56.0)

`git-cat-file` is the documented canonical object read: its NAME line says
it provides "contents or details of repository objects" (L6), and the
DESCRIPTION says it will

> "Output the contents or other properties such as size, type or delta
> information of one or more objects." (L21-22)

The option set splits that output into the forms a gate actually uses
(L39-56, L295-296):

| form | returns | line |
|---|---|---|
| `<type> <object>` | "the raw (though uncompressed) contents of the `<object>`" | L295-296 |
| `-p` | "Pretty-print the contents of `<object>` based on its type." | L54-55 |
| `-t` | "the object type identified by `<object>`" | L40 |
| `-s` | "the object size identified by `<object>`" | L44 |
| `-e` | exit zero iff `<object>` "exists and is a valid object" | L50 |

Naming is not cat-file's own: in batch mode each input line is
"considered as an object, as if it were fed to
linkgit:git-rev-parse[1]" (L303-304). That sentence is the documented
join between the two verbs: `rev-parse` is the name-resolution front door
and `cat-file` is the byte/type/size read behind it. Round-68's census
vocabulary (`show`, `cat-file`, `ls-tree`, `rev-parse`, `diff-tree`, `log`,
`merge-base`, `for-each-ref`, frozen at
`quality/counters/c2-r68-reader-guard.py:41-43`) is wider than this one
document; the four direct object-read verbs in it are `show`, `cat-file`,
`ls-tree` and `rev-parse`. `show` prints an object (or a `rev:path`
resolved through tree objects), `ls-tree` lists the entries of a tree
object, and `rev-parse` resolves a revision to an object name and peels
`^{type}` — all of them reach the same object store that `cat-file`
documents, which is why the census groups them rather than treating any
one as the read surface. The other four verbs reach objects through the
commit graph and refs; counting them broadens the guard requirement, it
does not narrow it. The `show`/`ls-tree` role descriptions in this
paragraph are `[INF-docs]` from the commands' names and the vocabulary;
they are not quoted from S437.

**Why replacement turns on this family.** S436 K05 states the default:
replacement refs are used "by default by all Git commands except those
doing reachability traversal" (`git-replace.adoc:34`). The three named
exceptions are prune, pack transfer and fsck; the object-read verbs are
none of them, so a `refs/replace` entry named for an object changes the
bytes `show`/`cat-file` return for that object and, at tree and commit
level, the listing and resolution `ls-tree`/`rev-parse` perform (S436;
round-67 host fixtures H01-H07). S437 corroborates the same boundary from
the read side: the only mode the
cat-file page calls out as not honouring replacement is
`--batch-all-objects` —

> "Objects are presented as-is, without respecting the "replace" mechanism
> of linkgit:git-replace[1]." (L198-199)

— the explicit exception makes the ordinary object-read path the rule.
A gate that builds its own environment without `GIT_NO_REPLACE_OBJECTS`
therefore scores the replacement's bytes while believing it read the
stored object; the round-68 repair is to construct that key at every
reader's child environment.

Two further documented limits matter for reading the census:

- A batch line that does not resolve prints `<object> SP missing LF`
  (L379), and an ambiguous short sha prints `<object> SP ambiguous LF`
  (L392); neither is an object read, so a gate that scores a missing name
  is scoring a resolve failure, not forged content.
- `-t`/`-s` are type and size reads, not content reads (L40, L44). The
  census does not distinguish them: any quoted verb in the vocabulary
  makes the blob a reader, so a size-only read is guarded like a content
  read.

## 2. The four environment shapes the census recognizes

The census decides "guard" with an AST walk
(`quality/counters/c2-r68-reader-guard.py:88-125`, docstring `:12-17`).
Its anchor rule is stated in the code: an environment is "a value reaching
an `env=` keyword, or a value bound to a name that says `env` (`env`,
`GIT_ENV`, `git_env` locals) — including a subscript store on that name."
The name test is a case-insensitive substring: `env_named` accepts any
`ast.Name` whose id contains `env` (`:100-101`). Inside that anchor, the key
string must appear in one of four constructions:

| # | construction | code shape | control case |
|---|---|---|---|
| 1 | dict-literal key bound to an env-named target | `env = {"PATH": ..., "GIT_NO_REPLACE_OBJECTS": "1"}` | `guarded-env-dict` |
| 2 | subscript store on an env-named target | `env["GIT_NO_REPLACE_OBJECTS"] = "1"` | `subscript-store-guard`, `module-const-guard` |
| 3 | `dict()`/`update()` keyword | `dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")` | `dict-keyword-guard` |
| 4 | key constant anywhere in the value expression of an `env=` keyword | `subprocess.run([...], env={"GIT_NO_REPLACE_OBJECTS": "1"})` | no frozen case isolates this shape (see below) |

The frozen control set `.ufo/waves/round-68/controls/c2-controls.json`
(sha256 `b7a1c939e5a715792d2969eb4ca86d8119cd5a72ef930d00d57338c62faf6a91`)
scores 11 cases and the counter requires all 11 correct. The three shapes
it rejects are:

| rejected shape | why it is not a guard | control case |
|---|---|---|
| comment-only mention | comments are not in the AST | `comment-only-mention` |
| docstring-only mention | docstrings are string statements, not env construction | `docstring-only-mention` |
| unrelated dict handed to `env=` | the literal is bound to `labels` (not an env-named target) and the `env=` value is a bare `ast.Name`; `carries_key` walks that Name and never follows it to the aliased literal, so the key is not seen | `unrelated-dict-as-env` |

Control-set coverage and the callee gap:

- None of the eleven frozen cases isolates shape 4. `guarded-env-dict` is
  guarded by its `env`-named dict, not by its `env=git_env()` call;
  `subscript-store-guard` and `module-const-guard` also carry env-named
  bindings; the negative cases carry none. The classifier's `env=` branch
  would accept a key literal written directly at the call, but no case
  scores that path on its own.
- The `env=` branch does not follow a callee. `env=git_env()` is a bare
  `ast.Call`, so the call site contributes nothing; the guard must be
  visible in a helper's own env-named binding. A helper that builds
  `e = dict(os.environ)` then `e["GIT_NO_REPLACE_OBJECTS"] = "1"` and is
  called as `env=git_env()` classifies as **unguarded** even though the
  child would be guarded — an under-inclusion symmetric to the
  value-position over-inclusion above. Conversely, a key-shaped literal
  anywhere in an `env=` value expression (even in a value position, not a
  key) reads as guarded.
- The selftest adds the complementary negative: a key literal in a call
  keyword that is not named `env` is not a guard
  (`quality/counters/c2-r68-reader-guard.py:292-294`).

Two precision points for anyone reusing the classifier:

- The guard is **presence-tested, not key-position-tested**.
  `carries_key` returns true for any `ast.Constant` whose value equals the
  key string anywhere in the accepted subtree, and for any keyword with
  that name (`:103-109`). A value position such as
  `env = {"NOTE": "GIT_NO_REPLACE_OBJECTS"}` would therefore read as
  guarded even though no environment variable is set. The census does not
  interpret the assigned value either: `"0"`, `"false"` and `"1"` all
  count, and S437/S436 do not define value semantics, so the classifier
  cannot distinguish a disabled guard from an enabled one.
- Reader detection is lexical, not semantic: a blob is a reader if it
  contains the word `git` and a quoted verb from the vocabulary
  (`GIT_TOKEN_RE`/`VERB_RE`, `:40-44`, `is_reader` `:84-85`). A quoted
  verb in a comment or docstring therefore still makes the blob a reader
  (the control set encodes exactly that for `comment-only-mention`), and a
  verb-shaped string in a list without a git token does not. The census is
  deliberately over-inclusive on the reader side and strict on the guard
  side.

## 3. Population boundary

Population is defined by path, read from git objects:

- pattern `quality/check-[^/]+\.py` (`POPULATION_RE`, `:39`): the lane's
  standing gate files only, no subdirectories;
- enumerated with `git ls-tree -r --name-only <sha> -- quality` and read
  with `git show <sha>:<path>` (`measure()`, `:138-144`), never from the
  worktree;
- `quality/counters/*` is outside the pattern. Frozen per-round counters
  and their pinned history are not touched by this claim and cannot be
  counted as repaired readers;
- the frozen predicate pins `population=20 readers=13` as part of the
  target, so a repair may not shrink the denominator by deleting a read or
  dropping a gate file.

At the base `510100c81e6cf63fec6be380c2f2f9c670f32cbc`: population 20,
readers 13 (seven files have no `git` + verb pair: `check-counter-discrimination`,
`check-locators`, `check-population`, `check-r38-discrimination`,
`check-r55-controls`, `check-r56-controls`, `check-state-cite`), guarded 1
(`quality/check-tool-ledger.py`), unguarded 12.

## 4. What the round repaired

The repair set is the twelve files that were readers without a guard at
the freeze revision. They are the entire unguarded list in the baseline
receipt, in its order:

`check-anchor-cover.py`, `check-axis-scores.py`, `check-control-receipts.py`,
`check-deliverables.py`, `check-evidence-pointers.py`, `check-freeze-order.py`,
`check-index-rows.py`, `check-index.py`, `check-landed-contract.py`,
`check-round-outcome-first.py`, `check-session-material.py`,
`check-wave-done.py`.

The census line **before**, measured pre-freeze
(`.ufo/waves/round-68/control-baseline-r68.txt:57`, rc 1):

```
MADO_R68_READER_GUARD: population=20 readers=13 guarded=1 unguarded=12 controls=11/11 verdict=TARGET_MISSED rev=510100c81e6cf63fec6be380c2f2f9c670f32cbc
```

The census line **after**, frozen as the predicate at
`claims-declaration-r68.md:101` (rc 0), where `REV` is the measured
revision:

```
MADO_R68_READER_GUARD: population=20 readers=13 guarded=13 unguarded=0 controls=11/11 verdict=TARGET_MET rev=<REV>
```

Bounded score `10 × guarded / readers`: 0.7692 → 10.0000. The twelve repairs use three
constructions. Seven files carry the subscript store after their own purge
(`env["GIT_NO_REPLACE_OBJECTS"] = "1"`, the shape
`quality/check-tool-ledger.py:109` already carried) in
`check-axis-scores.py` (its two helpers), `check-control-receipts.py`,
`check-evidence-pointers.py`, `check-freeze-order.py`, `check-index.py`,
`check-index-rows.py` and `check-wave-done.py`. Four pass the inline
`env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")` keyword at their
object-read calls (`check-deliverables.py`, `check-landed-contract.py`,
`check-round-outcome-first.py`, `check-session-material.py`), and
`check-index.py`/`check-index-rows.py` carry the same keyword form in
their fixture environment. `check-anchor-cover.py` adds the key to the
fresh dict literal it already built. The store must follow the purge:
a file that builds `dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")` and then
filters every `GIT_*` name reads as guarded while executing unguarded
(the dominance case in §5). The census scores committed source text at
`REV`; it does not execute the gates.

## 5. What the guard does not prove

- **No authenticity.** `GIT_NO_REPLACE_OBJECTS` makes a process ignore
  `refs/replace`; it does not make the stored objects genuine, signed, or
  the ones the author intended. A repository whose objects were physically
  rewritten reads as "real" with or without the guard.
- **No protection against an already-rewritten repo.** The guard stops the
  indirection being honoured in this process; S436 K02/K05 describe
  replacement as a name-to-name indirection over stored objects. Objects
  already rewritten are simply the stored bytes.
- **No dominance check.** The classifier sees the key constructed in an
  environment, not whether that environment survives to the call. A blob
  that builds `env = {k: v for k, v in dict(os.environ, GIT_NO_REPLACE_OBJECTS="1").items() if not k.startswith("GIT_")}`
  reads as guarded while the filter drops the guard and the child reads
  forged bytes. This is measured in
  `.ufo/waves/round-68/aux-dominance-r68.txt`: the repaired
  `check-index.py` reads `original bytes` under a planted replacement, the
  dominance variant reads `forged bytes`, and the census reports both
  `guard=yes`. The round's repaired files place the store after the purge
  (verified in the Gate2 drafts), but the count does not prove that order.
- **No runtime dataflow.** The classifier is a static AST walk of the
  committed blob. A guard set in a branch never taken reads as guarded; an
  env built by a helper far away and passed in is classified by the
  construction at the call site, not by tracing the value to the child; a
  module constant that is never used still counts.
- **Presence, not semantics.** As in §2: the value is not interpreted and
  the key's position is not checked. The guard is a construction test.
- **Lexical reader detection.** The reader count is "blobs that look like
  readers". A comment containing `"show"` plus the word git counts; a gate
  that reads objects through a wrapper whose body never spells a vocabulary
  verb in that blob does not.
- **Bounded population.** Only `quality/check-*.py` is counted. Tools,
  counters, wave scripts and seat drafts are outside the denominator, and
  the guard does not claim every lane object read is repaired.
- **No desktop, compositor, session, socket or service surface** was read
  or written for this entry.

## 6. Recheck and provenance

- Fetch command:
  `curl -sSfL -o git-cat-file.adoc https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-cat-file.adoc`
  (2026-11-03) → sha256
  `6c32dbda8c2106be08bda471592db50b5afaf185de32f2e513e80d802b4a95b2`,
  16099 bytes, 470 lines; tag `v2.56.0`; host `git version 2.56.0`.
- Line numbers in §1-§2 were checked against those bytes; the quote at
  L198-199 spans a line break in the source (the phrase begins at the end
  of L198).
- Control set: `.ufo/waves/round-68/controls/c2-controls.json`, sha256
  `b7a1c939e5a715792d2969eb4ca86d8119cd5a72ef930d00d57338c62faf6a91`,
  11 cases.
- Before/after lines: baseline receipt line 57 (rc 1) and the frozen
  predicate at declaration line 101 (rc 0). This entry did not re-run the
  census; the after line is the frozen target, not a measurement copied
  from a landing run.
- Cadence: 90d. Re-fetch the tag's adoc and re-hash it; re-check the
  census vocabulary and population regex if the counter changes; re-run
  the classification cases if the control JSON moves; re-measure the
  guarded count when the gate set changes.
