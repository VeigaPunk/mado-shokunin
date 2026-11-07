# R94MMutC1 — frozen C1 mutant set for the candidate `mado-mimeglob.c1.py`

**Status: DRAFT.** No frozen scoring was run. Nothing was written under
`.ufo/waves/round-94/receipts/`; the lane `tools/`, `quality/` and `corpus/` trees are untouched.
The candidate was never modified in place: every mutant is a copy under my scratch, so its bytes
are unchanged before and after (`sha256 0700915a260627cd521ea14b61dbb15aa7c3b067c0d287f04c07b39dfa72d63e` at the start and at the end of the run).

## Deliverables

| artifact | path | sha256 |
|---|---|---|
| mutant set (mine, 57 mutants) | `.ufo/waves/round-94/controls/mimeglob-mutants-r94.json` | `f67848dbcd84427020eb8a33390ea74da3398edd5a8352d227d3b49468d899ca` |
| case set used for the kill matrix (55 cases, delivered for the L1 to merge) | appendix B of this file | — |

* candidate under test: `.ufo/waves/round-94/build/mado-mimeglob.c1.py` — `0700915a260627cd521ea14b61dbb15aa7c3b067c0d287f04c07b39dfa72d63e`
* oracle source: `.ufo/waves/round-94/controls/mimeglob-oracle-r94.c` — `9c4337b36f93fa71bce13938f93d2e9758bb752815a67c57eb934a70bbfa6b11`
* host: glib2 2.90.1-1, shared-mime-info 2.5.1-2, gcc 16.2.1, python 3.14.8 (LC_ALL=C everywhere)

## Result

* **57 mutants** (requirement: ≥ 40), each a single `find`/`replace` that occurs **exactly once** in
  the candidate and changes one modelled rule named below.
* **53 killed**, **0 crashed-not-killed**, **4 survived**; all four survivors are argued
  equivalent and recorded in the mutant file's `equivalent_not_counted` (with the argument).
* Baseline: the pristine candidate equals the live oracle on **55/55** draft cases, so no kill in the
  matrix below rests on a baseline failure (no inconclusive case).

Caveat on the count: every killed mutant is killed on a case where the pristine candidate agrees
with the oracle, i.e. the case is a real detector for that rule.

## Method (every command with its exit code)

| # | command | rc |
|---|---|---|
| 1 | `mkdir -p $HYAKU_SCRATCH/mado-r94/R94MMutC1` | 0 |
| 2 | `gcc -O1 -o $S/oracle .ufo/waves/round-94/controls/mimeglob-oracle-r94.c $(pkg-config --cflags --libs gio-2.0)` | 0 |
| 3 | `python3 $S/run.py` (materialise 55 cases, oracle-label them, verify the pristine candidate) → `CASES=55 PRISTINE_MISMATCH=0` | 0 |
| 4 | `python3 $S/probe.py` (apply each mutant to a copy, run all cases, diff (type, uncertain) against the labels) → `MUTANTS=57 KILLED=53 CRASH_ONLY=0 SURVIVED=4` | 0 |
| 5 | equivalence harness for the four survivors (26 newline-offset fixtures + 6 NUL fixtures) → divergences 0 and 0 | 0 |
| 6 | JSON replay: every `find`/`replace` in the delivered file applied to the candidate reproduces the probed file byte-for-byte (`JSON_REPLAY_MISMATCH []`), `find` occurs exactly once for all 57, every mutant compiles (`compile(...)` → no SyntaxError) | 0 |
| 7 | candidate re-hash | 0 |

Cases were materialised under `$S/cases/<case-id>/`, each run with
`env -i LC_ALL=C HOME=<h> [XDG_DATA_HOME=<d>] [XDG_DATA_DIRS=<l>] oracle NAME...` and with
`python3 -I <tool> --json --home <h> [--data-home <d>|--data-home-unset] [--data-dirs <l>|--data-dirs-unset] NAME...`.
`XDG_DATA_DIRS` is set to a non-existent `{root}/none` directory in every case except
`dirs-05-default-data-dirs`, so that the host `/usr/share/mime` cannot leak into a label (an earlier
build of the cases did leak it — `x.zz` came back `application/zlib`; the leak was found and fixed
before any number above was taken).

Cache bytes are stored in the case files, never regenerated at measurement: each cache was built once
in scratch with `update-mime-database <dir>` from a generated `packages/*.xml`. Two caches are not
straight from the tool: `mode-04-size-min` stores a 32-byte synthetic header (magic-less version 1.1,
all section offsets 0 — the size rule needs a file below 40 bytes) and `mode-02-version-minor` /
`mode-03-version-major` store a real cache with its version bytes patched to (1,3)/(2,1).

## Kill matrix

| mutant | rule it flips | verdict | killed by (case ids; first 3) |
|---|---|---|---|
| `dirs-01-home-default` | dirs: XDG_DATA_HOME unset falls back to $HOME/.local/share | KILLED | `dirs-01-home-default` |
| `dirs-02-first-order` | dirs: XDG_DATA_HOME is the first element of the directory list | KILLED | `dirs-02-empty-element`, `dirs-03-order` |
| `dirs-03-empty-element` | dirs: empty XDG_DATA_DIRS elements are skipped | SURVIVED→equivalent | see §Survivors |
| `dirs-04-data-home-empty` | dirs: a set-but-empty XDG_DATA_HOME is used as-is, not the HOME default | KILLED | `dirs-04-data-home-empty` |
| `dirs-05-default-dirs` | dirs: XDG_DATA_DIRS unset means /usr/local/share/:/usr/share/ | KILLED | `dirs-05-default-data-dirs` |
| `mode-01-version-minor` | mode: a cache is valid for major 1 and minor 1..2 | KILLED | `mode-02-version-minor` |
| `mode-02-version-major` | mode: a cache is valid only for major version 1 | KILLED | `mode-01-mixed-cache-only`, `mode-03-version-major`, `mode-06-cache-ignores-globs` (+10) |
| `mode-03-size-40` | mode: a cache shorter than 40 bytes is rejected | KILLED | `mode-04-size-min`, `mode-07-cache-unreadable-trunc` |
| `mode-04-cache-only` | mode: any loaded cache means only the caches are consulted | KILLED | `mode-01-mixed-cache-only` |
| `mode-05-cache-continue` | mode: a dir with a valid cache does not also read its globs | SURVIVED→equivalent | see §Survivors |
| `mode-06-globs2-before-globs` | mode: globs2 is read instead of globs in one dir | KILLED | `mode-05-globs2-before-globs` |
| `fgets-01-chunk-find` | text: fgets line chunks are at most 254 bytes (newline search window) | SURVIVED→equivalent | see §Survivors |
| `fgets-02-chunk-end` | text: fgets chunk without a newline ends at 254 bytes | KILLED | `fgets-01-chunk-254` |
| `fgets-03-comment-skip` | text: a line starting with '#' is a comment | KILLED | `comment-01-hash-skip` |
| `fgets-04-nul-skip` | text: a chunk starting with NUL is skipped | SURVIVED→equivalent | see §Survivors |
| `atoi-01-sign` | atoi: a leading '-' negates the weight | KILLED | `weight-02-sign` |
| `atoi-02-whitespace` | atoi: leading whitespace is skipped | KILLED | `weight-03-whitespace` |
| `v1-01-weight-50` | text v1: a globs line has weight 50 | KILLED | `weight-01-v1-default` |
| `cs-01-prefix` | cs flags: a flag token starts at 0 or after a comma | KILLED | `cs-01-prefix-token` |
| `cs-02-suffix` | cs flags: a flag token ends at the end or before a comma | KILLED | `cs-02-suffix-token` |
| `cs-03-second-colon` | cs flags: the flag field ends at a second colon | KILLED | `cs-03-second-colon` |
| `glob-01-any-star` | glob classification: only a leading '*' sets maybe-simple | KILLED | `full-02-unfolded-name`, `full-04-second-star`, `full-06-star-not-first` (+1) |
| `glob-02-second-star` | glob classification: a second '*' makes a full glob | KILLED | `full-02-unfolded-name`, `full-04-second-star`, `full-06-star-not-first` (+1) |
| `glob-03-question` | glob classification: '?' makes a full glob | KILLED | `full-01-question` |
| `glob-04-backslash` | glob classification: '\\' makes a full glob | KILLED | `full-05-backslash` |
| `glob-05-first-k` | glob classification: a '*' at index 0 only | KILLED | `full-02-unfolded-name`, `full-04-second-star`, `full-06-star-not-first` |
| `literal-01-dedupe` | text literals: the duplicate key is the (glob, mime) pair | KILLED | `literal-04-dedupe` |
| `literal-02-fold-first` | text literals: the exact pass runs before the folded pass | KILLED | `literal-02-exact-before-folded`, `literal-04-dedupe` |
| `literal-03-fold-cs` | text literals: the folded pass skips cs literals | KILLED | `literal-03-cs-not-folded`, `literal-04-dedupe` |
| `trie-01-deepest` | trie: a deeper match suppresses the node's own mime and extra types | KILLED | `simple-03-deepest` |
| `trie-02-extra-order` | trie: extra types precede ordinary children | KILLED | `simple-06-extra-before-child` |
| `trie-03-extra-break` | trie: the extra-type scan stops at the first non-zero child | KILLED | `simple-06-extra-before-child` |
| `trie-04-signed-char` | trie: a name byte >= 0x80 widens to a negative 32-bit char | KILLED | `bytes-01-signed-char` |
| `trie-05-sibling-merge` | trie: an equal character reuses the existing sibling node | KILLED | `dirs-02-empty-element`, `dirs-03-order`, `simple-03-deepest` (+7) |
| `pass-01-second-threshold` | text: the case-sensitive second pass runs while fewer than 2 types | KILLED | `simple-01-pass2-threshold` |
| `pass-02-second-check` | text: the second pass includes cs globs | KILLED | `simple-01-pass2-threshold`, `simple-02-pass1-cs`, `cs-03-second-colon` (+1) |
| `pass-03-first-check` | text: the first (folded-name) pass excludes cs globs | KILLED | `simple-02-pass1-cs`, `cs-03-second-colon`, `cs-04-after-comma` |
| `pass-04-full-threshold` | text: full globs run only while fewer than 2 types | KILLED | `full-03-threshold` |
| `pass-05-full-unfolded` | text: fnmatch receives the unfolded name | KILLED | `full-02-unfolded-name` |
| `cache-01-fnmatch-threshold` | cache: the fnmatch pass runs only when the suffix pass found nothing | KILLED | `cache-04-fnmatch-threshold` |
| `cache-02-literal-cs-stop` | cache literals: a cs hit on the folded pass ends the literal search | KILLED | `cache-01-literal-cs-stop` |
| `cache-03-weight-mask` | cache: a suffix entry weight is the low 8 bits | KILLED | `cache-02-weight-mask`, `cache-04-fnmatch-threshold` |
| `cache-04-cs-bit-suffix` | cache: 0x100 in a suffix weight is the case-sensitive flag | KILLED | `cache-02-weight-mask`, `cache-04-fnmatch-threshold`, `cache-06-cs-bit-suffix` |
| `cache-05-cs-bit-fnmatch` | cache: 0x100 in an fnmatch weight is the case-sensitive flag | KILLED | `cache-07-cs-bit-fnmatch` |
| `cache-06-per-cache` | cache: every cache adds its own deepest suffix match | KILLED | `cache-03-per-cache`, `dupe-01-max-weight`, `dupe-02-swap-from-end` |
| `cache-07-fnmatch-unfolded` | cache: the second fnmatch pass receives the unfolded name | KILLED | `cache-04-fnmatch-threshold`, `cache-07-cs-bit-fnmatch` |
| `cache-08-literal-order` | cache literals: the folded pass runs before the exact pass | KILLED | `cache-08-literal-order` |
| `dupe-01-max-weight` | dupes: the merged weight is the larger of the two | KILLED | `dupe-01-max-weight` |
| `dupe-02-swap-from-end` | dupes: the duplicate slot is refilled from the end of the list | KILLED | `cache-02-weight-mask`, `dupe-02-swap-from-end` |
| `dupe-03-sort-descending` | sort: higher weight sorts first | KILLED | `weight-01-v1-default`, `weight-02-sign`, `weight-03-whitespace` (+5) |
| `dupe-04-cap-10` | cap: at most 10 mime types are returned | KILLED | `dirs-02-empty-element`, `dirs-03-order`, `simple-01-pass2-threshold` (+12) |
| `guess-01-trailing-slash` | guess: a trailing '/' is inode/directory, uncertain | KILLED | `slash-01-trailing`, `noglobs-01-empty` |
| `guess-02-one-certain` | guess: exactly one type is certain | KILLED | `dirs-02-empty-element`, `dirs-03-order`, `simple-01-pass2-threshold` (+12) |
| `guess-03-none-uncertain` | guess: no type is application/octet-stream, uncertain | KILLED | `dirs-03-order`, `dirs-04-data-home-empty`, `literal-01-basic` (+16) |
| `guess-04-several-uncertain` | guess: several types means the first, uncertain | KILLED | `dirs-02-empty-element`, `dirs-03-order`, `simple-01-pass2-threshold` (+12) |
| `guess-05-basename` | basename: only the last path element is looked up | KILLED | `literal-01-basic` |
| `guess-06-empty-name` | basename: an empty path becomes '.' | KILLED | `literal-05-empty-name` |

## Survivors (4) — argued equivalent, not counted

Each argument is also in the delivered file under `equivalent_not_counted`.

### `dirs-03-empty-element` — dirs: empty XDG_DATA_DIRS elements are skipped

The mutant keeps the empty element and appends the literal directory '/mime/' (d + '/mime/' with d = ''). The only way that changes an answer is if a database exists under /mime; the case schema materialises files only below {root}, and /mime does not exist on the measurement host (tested: `test -d /mime` false), so the extra directory is inert. Order of the real directories is unchanged, so no case can distinguish it. Measured: identical (type, uncertain) on all 55 cases.

### `mode-05-cache-continue` — mode: a dir with a valid cache does not also read its globs

Without the `continue`, a dir with a valid mime.cache also parses its globs2 into TextDB. TextDB is only consulted when `caches` is empty (`self.db = CacheDB(caches) if caches else text`), and a dir that produced a cache guarantees `caches` is non-empty; `self.mode` is computed from the same list. The extra parse therefore cannot reach any answer. Measured: identical on all 55 cases, including mode-06-cache-ignores-globs (cache + globs2 in one dir).

### `fgets-01-chunk-find` — text: fgets line chunks are at most 254 bytes (newline search window)

The 255-byte window differs only when a '\n' sits at exactly offset 254 of a chunk: the 254-window then ends the chunk before it (end = i+254) and the next chunk is the bare '\n'; the 255-window ends the chunk after it (end = nl+1 = i+255). Both parse to the same globs, because a chunk ending in '\n' has that byte stripped and a one-byte '\n' chunk is neither a comment nor a ':' line, so it is skipped, and the following chunk starts at the same byte in both models. Measured: identical (type, uncertain) for newline offsets 240..265 in a 400-byte line, over 4 names (eq harness, 26 fixtures). fgets-02 (the 254-byte chunk end) IS killed by fgets-01-chunk-254, so the chunk length itself stays covered.

### `fgets-04-nul-skip` — text: a chunk starting with NUL is skipped

A chunk whose first byte is NUL is truncated to b'' by `line = chunk.split(b'\0', 1)[0]`, then fails `k = p.find(b':') < 0` and is skipped, exactly as the explicit NUL test would do. The mutation only removes an early exit, not a parse. Measured: identical on NUL bytes at offsets 0, 1, 253, 254, 255, 508 of a globs2 file (eq harness, 6 fixtures, 2 names each) and on all 55 cases.

No distinguishing case was added for these four: an oracle-labelled case cannot exist that separates
them, because the code paths they bound are unreachable for any input that reaches a (type, uncertain)
answer. Coverage of the surrounding rule is kept by `fgets-02-chunk-end` (killed by
`fgets-01-chunk-254`), `mode-04-cache-only` (killed by `mode-01-mixed-cache-only`) and
`mode-06-globs2-before-globs` (killed by `mode-05-globs2-before-globs`).

## Notes for the L1 (case-file merge)

* 55 cases, schema version 1, every `labels` entry produced by the oracle in this run:
  {"text": 39, "cache": 11, "mixed": 5}. Classes used (all inside the union of the seat contract's list):
  `bytes`, `cache`, `cachefmt`, `cs`, `deep`, `dirs`, `dupe`, `fgets`, `fold`, `full`, `literal`, `mixed`, `mode`, `multi`, `noglobs`, `nomatch`, `order`, `simple`, `slash`, `v1`, `weight`.
* `dirs-05-default-data-dirs` deliberately leaves `XDG_DATA_DIRS` unset, so its labels depend on the
  host `/usr/share/mime` (`a.txt` → `text/plain`, `a.zz` → `application/zlib`). It is the only case
  that reads the system database; the counter re-runs the oracle, so a host change shows up as a
  label mismatch rather than a wrong answer. Drop it if the frozen set must be host-independent —
  it is the sole killer of `dirs-05-default-dirs`.
* `cache-01-literal-cs-stop` and `cache-04-fnmatch-threshold` only distinguish their rules because
  `update-mime-database` lowercases non-case-sensitive glob *patterns* and keeps case-sensitive ones
  as written; the two negative names (`ABC`, `X.zz`) are what reach the cs branches. Do not
  "normalise" those names.
* `simple-06-extra-before-child` needs the `*b.zz` line **first**: the ordinary child has to exist
  before the extra type is inserted, otherwise `insert(0, …)` and `append(…)` coincide.
* `fgets-01-chunk-254` relies on the 254-byte fgets split turning `a…a*` into a full glob;
  the two long names differ only by one trailing `a`.

## Report of the wave contract items

* Mutant set: 57 ≥ 40, one rule per mutant, `find` unique (verified on the delivered file).
* Survivors: 4, each equivalent, with argument and measurement (all 55 cases identical; plus the
  dedicated equivalence fixtures for the two fgets mutants).
* Installations: none. No package manager, no network, no PATH write. No `sudo`.
* Host safety: `update-mime-database` ran only on directories inside `$S/gen/`; no `xdg-mime`,
  no service, no sysctl, no credential material read.
* Scratch `$HYAKU_SCRATCH/mado-r94/R94MMutC1` (with the compiled oracle, generated caches, the 55
  materialised case roots and the 57 mutated copies) is deleted on exit after this report is written.

## Appendix A — mutant file shape

```text
{"mutants": [{"id": "...", "rule": "...", "find": "...", "replace": "..."}, ...],
 "equivalent_not_counted": [{"id": "...", "rule": "...", "argument": "..."}]}
```

`find` occurs exactly once in `.ufo/waves/round-94/build/mado-mimeglob.c1.py` for all 57 entries; the
file is 17 399 bytes and holds no case ids (the mapping is the matrix above).

## Appendix B — the 55 oracle-labelled cases (schema of `mimeglob-cases-r94.json`)

```json
{
 "cases": [
  {
   "class": "dirs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1",
    "XDG_DATA_HOME": null
   },
   "files": {
    "h/.local/share/mime/globs2": "NTA6dGV4dC9ob21lOiouaGgK"
   },
   "id": "dirs-01-home-default",
   "labels": [
    [
     "text/home",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS5oaA=="
   ]
  },
  {
   "class": "dirs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1::{root}/s3",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9hOioueHgK",
    "s1/mime/globs2": "NTA6dC9iOioueHgK",
    "s3/mime/globs2": "NTA6dC9jOioueHgK"
   },
   "id": "dirs-02-empty-element",
   "labels": [
    [
     "t/a",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS54eA=="
   ]
  },
  {
   "class": "dirs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9oOioueHgK",
    "s1/mime/globs2": "NTA6dC9hOioueHgK",
    "s2/mime/globs2": "NTA6dC9iOioueHgK"
   },
   "id": "dirs-03-order",
   "labels": [
    [
     "t/h",
     1
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS54eA==",
    "bm90aGluZw=="
   ]
  },
  {
   "class": "dirs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1",
    "XDG_DATA_HOME": ""
   },
   "files": {
    "h/.local/share/mime/globs2": "NTA6dGV4dC9ob21lOiouaGgK",
    "s1/mime/globs2": "NTA6dC9zMToqLnNzCg=="
   },
   "id": "dirs-04-data-home-empty",
   "labels": [
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS5oaA=="
   ]
  },
  {
   "class": "mixed",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC90ZXh0OioueHgK",
    "s1/mime/mime.cache": "AAEAAgAAADQAAAA4AAAAPAAAAEAAAAB4AAAAfAAAAIgAAACMAAAAkAAAAJR0L2NhY2hlAAAAAAAAAAAAAAAAAAAAAAEAAABIAAAAeAAAAAEAAABUAAAAeAAAAAEAAABgAAAALgAAAAEAAABsAAAAAAAAACwAAAAyAAAAAAAAAAAAAAAAAAAAiAAAAAAAAAAAAAAAAAAAAAEAAAAA"
   },
   "id": "mode-01-mixed-cache-only",
   "labels": [
    [
     "t/cache",
     0
    ]
   ],
   "mode": "mixed",
   "names_b64": [
    "YS54eA=="
   ]
  },
  {
   "class": "cachefmt",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC90ZXh0OioueXkK",
    "dh/mime/mime.cache": "AAEAAwAAADQAAAA4AAAAPAAAAEAAAAB4AAAAfAAAAIgAAACMAAAAkAAAAJR0L2NhY2hlAAAAAAAAAAAAAAAAAAAAAAEAAABIAAAAeQAAAAEAAABUAAAAeQAAAAEAAABgAAAALgAAAAEAAABsAAAAAAAAACwAAAAyAAAAAAAAAAAAAAAAAAAAiAAAAAAAAAAAAAAAAAAAAAEAAAAA"
   },
   "id": "mode-02-version-minor",
   "labels": [
    [
     "t/text",
     0
    ]
   ],
   "mode": "mixed",
   "names_b64": [
    "YS55eQ=="
   ]
  },
  {
   "class": "cachefmt",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC90ZXh0Oioud3cK",
    "dh/mime/mime.cache": "AAIAAQAAADQAAAA4AAAAPAAAAEAAAAB4AAAAfAAAAIgAAACMAAAAkAAAAJR0L2NhY2hlAAAAAAAAAAAAAAAAAAAAAAEAAABIAAAAdwAAAAEAAABUAAAAdwAAAAEAAABgAAAALgAAAAEAAABsAAAAAAAAACwAAAAyAAAAAAAAAAAAAAAAAAAAiAAAAAAAAAAAAAAAAAAAAAEAAAAA"
   },
   "id": "mode-03-version-major",
   "labels": [
    [
     "t/text",
     0
    ]
   ],
   "mode": "mixed",
   "names_b64": [
    "YS53dw=="
   ]
  },
  {
   "class": "cachefmt",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC90ZXh0Oioud3cK",
    "dh/mime/mime.cache": "AAEAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
   },
   "id": "mode-04-size-min",
   "labels": [
    [
     "t/text",
     0
    ]
   ],
   "mode": "mixed",
   "names_b64": [
    "YS53dw=="
   ]
  },
  {
   "class": "mode",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs": "dC92MToqLmdnCg==",
    "dh/mime/globs2": "NTA6dC92MjoqLmdnCg=="
   },
   "id": "mode-05-globs2-before-globs",
   "labels": [
    [
     "t/v2",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS5nZw=="
   ]
  },
  {
   "class": "mode",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC90ZXh0Oioua2sK",
    "dh/mime/mime.cache": "AAEAAgAAADQAAAA4AAAAPAAAAEAAAAB4AAAAfAAAAIgAAACMAAAAkAAAAJR0L2NhY2hlAAAAAAAAAAAAAAAAAAAAAAEAAABIAAAAawAAAAEAAABUAAAAawAAAAEAAABgAAAALgAAAAEAAABsAAAAAAAAACwAAAAyAAAAAAAAAAAAAAAAAAAAiAAAAAAAAAAAAAAAAAAAAAEAAAAA"
   },
   "id": "mode-06-cache-ignores-globs",
   "labels": [
    [
     "t/cache",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "YS5raw=="
   ]
  },
  {
   "class": "mixed",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC90ZXh0OiouamoK",
    "dh/mime/mime.cache": "AAEAAgAAADQAAAA4AAAAPAAAAEAAAAB4AAAAfAAAAIg="
   },
   "id": "mode-07-cache-unreadable-trunc",
   "labels": [
    [
     "t/text",
     0
    ]
   ],
   "mode": "mixed",
   "names_b64": [
    "YS5qag=="
   ]
  },
  {
   "class": "literal",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9tYWtlOk1ha2VmaWxlCg=="
   },
   "id": "literal-01-basic",
   "labels": [
    [
     "t/make",
     0
    ],
    [
     "application/octet-stream",
     1
    ],
    [
     "t/make",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "TWFrZWZpbGU=",
    "TUFLRUZJTEU=",
    "c3ViL01ha2VmaWxl"
   ]
  },
  {
   "class": "order",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9oaTpNYWtlZmlsZQo1MDp0L2xvOm1ha2VmaWxlCg=="
   },
   "id": "literal-02-exact-before-folded",
   "labels": [
    [
     "t/hi",
     0
    ],
    [
     "t/lo",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "TWFrZWZpbGU=",
    "bWFrZWZpbGU="
   ]
  },
  {
   "class": "cs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9tOm1ha2VmaWxlOmNzCg=="
   },
   "id": "literal-03-cs-not-folded",
   "labels": [
    [
     "application/octet-stream",
     1
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "TUFLRUZJTEU=",
    "TWFrZWZpbGU="
   ]
  },
  {
   "class": "literal",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9oaTptYWtlZmlsZTpjcwo1MDp0L2xvOm1ha2VmaWxlCg=="
   },
   "id": "literal-04-dedupe",
   "labels": [
    [
     "t/lo",
     0
    ],
    [
     "t/hi",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "TUFLRUZJTEU=",
    "bWFrZWZpbGU="
   ]
  },
  {
   "class": "literal",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9kb3Q6Lgo1MDp0L21ha2U6TWFrZWZpbGUK"
   },
   "id": "literal-05-empty-name",
   "labels": [
    [
     "t/dot",
     0
    ],
    [
     "t/dot",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "",
    "Lg=="
   ]
  },
  {
   "class": "simple",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dGV4dC9wbGFpbjoqLnR4dAo="
   },
   "id": "literal-06-plain-suffix",
   "labels": [
    [
     "text/plain",
     0
    ],
    [
     "text/plain",
     0
    ],
    [
     "text/plain",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS50eHQ=",
    "QS5UWFQ=",
    "c3ViL2Rpci50eHQvYS50eHQ="
   ]
  },
  {
   "class": "fold",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9hOiouenoKNTA6dC9iOiouWlo6Y3MK"
   },
   "id": "simple-01-pass2-threshold",
   "labels": [
    [
     "t/a",
     1
    ],
    [
     "t/a",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC5aWg==",
    "eC56eg=="
   ]
  },
  {
   "class": "cs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9hOioueno6Y3MK"
   },
   "id": "simple-02-pass1-cs",
   "labels": [
    [
     "application/octet-stream",
     1
    ],
    [
     "t/a",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC5aWg==",
    "eC56eg=="
   ]
  },
  {
   "class": "deep",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9nejoqLmd6CjUwOnQvdGd6OioudGFyLmd6Cg=="
   },
   "id": "simple-03-deepest",
   "labels": [
    [
     "t/tgz",
     0
    ],
    [
     "t/gz",
     0
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC50YXIuZ3o=",
    "eC5neg==",
    "eC50YXIuYXo="
   ]
  },
  {
   "class": "multi",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9vbmU6Ki56ego1MDp0L3R3bzoqLnp6Cg=="
   },
   "id": "simple-04-extra-types",
   "labels": [
    [
     "t/one",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS56eg=="
   ]
  },
  {
   "class": "multi",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "OTA6dC9mb3VyOipiLnp6CjUwOnQvb25lOiouenoKNTA6dC90d286Ki56ego="
   },
   "id": "simple-06-extra-before-child",
   "labels": [
    [
     "t/one",
     1
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS56eg==",
    "YS5ieno="
   ]
  },
  {
   "class": "nomatch",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dGV4dC9wbGFpbjoqLnR4dAo="
   },
   "id": "simple-05-nomatch",
   "labels": [
    [
     "application/octet-stream",
     1
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eno=",
    "YS50eA=="
   ]
  },
  {
   "class": "full",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9xOng/eQo="
   },
   "id": "full-01-question",
   "labels": [
    [
     "t/q",
     0
    ],
    [
     "t/q",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eHp5",
    "eHF5"
   ]
  },
  {
   "class": "full",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9mOkEqLlRYVAo="
   },
   "id": "full-02-unfolded-name",
   "labels": [
    [
     "t/f",
     0
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "QWIuVFhU",
    "YWIuVFhU"
   ]
  },
  {
   "class": "full",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9vbmU6Ki56ego1MDp0L3R3bzoqLnp6CjkwOnQvZnVsbDp4Ki56ego="
   },
   "id": "full-03-threshold",
   "labels": [
    [
     "t/one",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC56eg=="
   ]
  },
  {
   "class": "full",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9kZDoqKi50eHQK"
   },
   "id": "full-04-second-star",
   "labels": [
    [
     "t/dd",
     0
    ],
    [
     "t/dd",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS50eHQ=",
    "YSoudHh0"
   ]
  },
  {
   "class": "full",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9iOmFcYgo="
   },
   "id": "full-05-backslash",
   "labels": [
    [
     "t/b",
     0
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YWI=",
    "YVxi"
   ]
  },
  {
   "class": "full",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9zYjphKmIK"
   },
   "id": "full-06-star-not-first",
   "labels": [
    [
     "t/sb",
     0
    ],
    [
     "t/sb",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YXhi",
    "YWI="
   ]
  },
  {
   "class": "v1",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": null
   },
   "files": {
    "s1/mime/globs": "dC92MToqLnp6Cg==",
    "s2/mime/globs2": "NDA6dC92MjoqLnp6Cg=="
   },
   "id": "weight-01-v1-default",
   "labels": [
    [
     "t/v1",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC56eg=="
   ]
  },
  {
   "class": "weight",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "LTIwOnQvbmVnOiouenoKMTA6dC9wb3M6Ki56ego="
   },
   "id": "weight-02-sign",
   "labels": [
    [
     "t/pos",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC56eg=="
   ]
  },
  {
   "class": "weight",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "IDYwOnQvd3M6Ki56ego1MDp0L3BsYWluOiouenoK"
   },
   "id": "weight-03-whitespace",
   "labels": [
    [
     "t/ws",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC56eg=="
   ]
  },
  {
   "class": "weight",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9vbmU6Ki56ego5MDp0L3R3bzoqLnp6Cg=="
   },
   "id": "weight-04-descending",
   "labels": [
    [
     "t/two",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC56eg=="
   ]
  },
  {
   "class": "bytes",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9lOiouwqkK"
   },
   "id": "bytes-01-signed-char",
   "labels": [
    [
     "application/octet-stream",
     1
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS6p",
    "eC7DqQ=="
   ]
  },
  {
   "class": "cs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9hOioueno6eGNzCg=="
   },
   "id": "cs-01-prefix-token",
   "labels": [
    [
     "t/a",
     0
    ],
    [
     "t/a",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC5aWg==",
    "eC56eg=="
   ]
  },
  {
   "class": "cs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9hOioueno6Y3N4Cg=="
   },
   "id": "cs-02-suffix-token",
   "labels": [
    [
     "t/a",
     0
    ],
    [
     "t/a",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC5aWg==",
    "eC56eg=="
   ]
  },
  {
   "class": "cs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9hOioueno6Y3M6eAo="
   },
   "id": "cs-03-second-colon",
   "labels": [
    [
     "application/octet-stream",
     1
    ],
    [
     "t/a",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC5aWg==",
    "eC56eg=="
   ]
  },
  {
   "class": "cs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9hOioueno6eCxjcwo="
   },
   "id": "cs-04-after-comma",
   "labels": [
    [
     "application/octet-stream",
     1
    ],
    [
     "t/a",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC5aWg==",
    "eC56eg=="
   ]
  },
  {
   "class": "fgets",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9sb25nOmFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYSouenoK"
   },
   "id": "fgets-01-chunk-254",
   "labels": [
    [
     "t/long",
     0
    ],
    [
     "t/long",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh",
    "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYQ=="
   ]
  },
  {
   "class": "literal",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "Izp0ZXh0L3gtZmFrZToqLmZrCjUwOnRleHQvcGxhaW46Ki50eHQK"
   },
   "id": "comment-01-hash-skip",
   "labels": [
    [
     "application/octet-stream",
     1
    ],
    [
     "text/plain",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS5maw==",
    "YS50eHQ="
   ]
  },
  {
   "class": "v1",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs": "dC9vbGQ6Ki5vbGQK"
   },
   "id": "v1-01-basic",
   "labels": [
    [
     "t/old",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "Zi5vbGQ="
   ]
  },
  {
   "class": "v1",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs": "dC9jb2xvbjphOmIK"
   },
   "id": "v1-02-colon-in-glob",
   "labels": [
    [
     "t/colon",
     0
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YTpi",
    "YQ=="
   ]
  },
  {
   "class": "cache",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": null
   },
   "files": {
    "s1/mime/mime.cache": "AAEAAgAAADgAAAA8AAAAQAAAAFAAAABYAAAAXAAAAGgAAABsAAAAcAAAAHRhYmMAdC9jMQAAAAAAAAAAAAAAAAAAAAEAAAAsAAAAMAAAATIAAAAAAAAAWAAAAAAAAAAAAAAAAAAAAGgAAAAAAAAAAAAAAAAAAAABAAAAAA==",
    "s2/mime/mime.cache": "AAEAAgAAADgAAAA8AAAAQAAAAFAAAABYAAAAXAAAAGgAAABsAAAAcAAAAHR0L2MyAAAAAGFiYwAAAAAAAAAAAAAAAAEAAAA0AAAALAAAADIAAAAAAAAAWAAAAAAAAAAAAAAAAAAAAGgAAAAAAAAAAAAAAAAAAAABAAAAAA=="
   },
   "id": "cache-01-literal-cs-stop",
   "labels": [
    [
     "application/octet-stream",
     1
    ],
    [
     "t/c1",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "QUJD",
    "YWJj"
   ]
  },
  {
   "class": "cache",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/mime.cache": "AAEAAgAAADwAAABAAAAARAAAAEgAAACMAAAAkAAAAJwAAACgAAAApAAAAKh0L2xvAAAAAHQvaGkAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAFAAAABxAAAAAQAAAFwAAABxAAAAAQAAAGgAAAAuAAAAAgAAAHQAAAAAAAAANAAAAFoAAAAAAAAALAAAAVAAAAAAAAAAAAAAAAAAAACcAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAA"
   },
   "id": "cache-02-weight-mask",
   "labels": [
    [
     "t/hi",
     1
    ],
    [
     "t/hi",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "eC5xcQ==",
    "eC5RUQ=="
   ]
  },
  {
   "class": "cache",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": null
   },
   "files": {
    "s1/mime/mime.cache": "AAEAAgAAADAAAAA0AAAAOAAAADwAAAB0AAAAeAAAAIQAAACIAAAAjAAAAJB0L2EAAAAAAAAAAAAAAAAAAAAAAQAAAEQAAAB6AAAAAQAAAFAAAAB6AAAAAQAAAFwAAAAuAAAAAQAAAGgAAAAAAAAALAAAADIAAAAAAAAAAAAAAAAAAACEAAAAAAAAAAAAAAAAAAAAAQAAAAA=",
    "s2/mime/mime.cache": "AAEAAgAAADAAAAA0AAAAOAAAADwAAAB0AAAAeAAAAIQAAACIAAAAjAAAAJB0L2IAAAAAAAAAAAAAAAAAAAAAAQAAAEQAAAB6AAAAAQAAAFAAAAB6AAAAAQAAAFwAAAAuAAAAAQAAAGgAAAAAAAAALAAAADIAAAAAAAAAAAAAAAAAAACEAAAAAAAAAAAAAAAAAAAAAQAAAAA="
   },
   "id": "cache-03-per-cache",
   "labels": [
    [
     "t/a",
     1
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "eC56eg=="
   ]
  },
  {
   "class": "cache",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/mime.cache": "AAEAAgAAAEQAAABIAAAATAAAAFAAAACIAAAAmAAAAKQAAACoAAAArAAAALB0L3p6AAAAAHgqLnp6AAAAdC9mdWxsAAAAAAAAAAAAAAAAAAAAAAABAAAAWAAAAHoAAAABAAAAZAAAAHoAAAABAAAAcAAAAC4AAAABAAAAfAAAAAAAAAAsAAABMgAAAAEAAAA0AAAAPAAAAFoAAAAAAAAAAAAAAKQAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAA="
   },
   "id": "cache-04-fnmatch-threshold",
   "labels": [
    [
     "t/full",
     1
    ],
    [
     "t/zz",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "eC56eg==",
    "WC56eg=="
   ]
  },
  {
   "class": "cache",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/mime.cache": "AAEAAgAAADgAAAA8AAAAQAAAAEQAAABMAAAAXAAAAGgAAABsAAAAcAAAAHRhKi50eHQAAHQvYgAAAAAAAAAAAAAAAAAAAAAAAAAATAAAAAEAAAAsAAAANAAAADIAAAAAAAAAAAAAAGgAAAAAAAAAAAAAAAAAAAABAAAAAA=="
   },
   "id": "cache-05-fnmatch-unfolded",
   "labels": [
    [
     "t/b",
     0
    ],
    [
     "t/b",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "QWIuVFhU",
    "YWIuVFhU"
   ]
  },
  {
   "class": "cs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/mime.cache": "AAEAAgAAADgAAAA8AAAAQAAAAEQAAACIAAAAjAAAAJgAAACcAAAAoAAAAKR0ZXh0L3BsYWluAAAAAAAAAAAAAAAAAAAAAAABAAAATAAAAHQAAAABAAAAWAAAAHgAAAABAAAAZAAAAHQAAAABAAAAcAAAAC4AAAABAAAAfAAAAAAAAAAsAAABMgAAAAAAAAAAAAAAAAAAAJgAAAAAAAAAAAAAAAAAAAABAAAAAA=="
   },
   "id": "cache-06-cs-bit-suffix",
   "labels": [
    [
     "application/octet-stream",
     1
    ],
    [
     "text/plain",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "WC5UWFQ=",
    "eC50eHQ="
   ]
  },
  {
   "class": "cs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/mime.cache": "AAEAAgAAADwAAABAAAAARAAAAEgAAABQAAAAYAAAAGwAAABwAAAAdAAAAHh0L2ZuAAAAAHgqLnR4dAAAAAAAAAAAAAAAAAAAAAAAAAAAAFAAAAABAAAANAAAACwAAAEyAAAAAAAAAAAAAABsAAAAAAAAAAAAAAAAAAAAAQAAAAA="
   },
   "id": "cache-07-cs-bit-fnmatch",
   "labels": [
    [
     "application/octet-stream",
     1
    ],
    [
     "t/fn",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "WDEuVFhU",
    "eDEudHh0"
   ]
  },
  {
   "class": "order",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/mime.cache": "AAEAAgAAAFQAAABYAAAAXAAAAHgAAACAAAAAhAAAAJAAAACUAAAAmAAAAJxNQUtFRklMRQAAAAB0L21rAAAAAHQvTUsAAAAAbWFrZWZpbGUAAAAAAAAAAAAAAAAAAAACAAAALAAAAEAAAAEyAAAASAAAADgAAAAyAAAAAAAAAIAAAAAAAAAAAAAAAAAAAACQAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAA"
   },
   "id": "cache-08-literal-order",
   "labels": [
    [
     "t/mk",
     0
    ],
    [
     "t/mk",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "TUFLRUZJTEU=",
    "bWFrZWZpbGU="
   ]
  },
  {
   "class": "dupe",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2:{root}/s3",
    "XDG_DATA_HOME": null
   },
   "files": {
    "s1/mime/mime.cache": "AAEAAgAAADQAAAA4AAAAPAAAAEAAAACEAAAAiAAAAJQAAACYAAAAnAAAAKB0L2EAdC9iAAAAAAAAAAAAAAAAAAAAAAEAAABIAAAAcQAAAAEAAABUAAAAcQAAAAEAAABgAAAALgAAAAIAAABsAAAAAAAAACwAAABaAAAAAAAAADAAAAA8AAAAAAAAAAAAAAAAAAAAlAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAA==",
    "s2/mime/mime.cache": "AAEAAgAAADAAAAA0AAAAOAAAADwAAAB0AAAAeAAAAIQAAACIAAAAjAAAAJB0L2EAAAAAAAAAAAAAAAAAAAAAAQAAAEQAAABxAAAAAQAAAFAAAABxAAAAAQAAAFwAAAAuAAAAAQAAAGgAAAAAAAAALAAAAB4AAAAAAAAAAAAAAAAAAACEAAAAAAAAAAAAAAAAAAAAAQAAAAA=",
    "s3/mime/mime.cache": "AAEAAgAAADAAAAA0AAAAOAAAADwAAAB0AAAAeAAAAIQAAACIAAAAjAAAAJB0L2MAAAAAAAAAAAAAAAAAAAAAAQAAAEQAAABxAAAAAQAAAFAAAABxAAAAAQAAAFwAAAAuAAAAAQAAAGgAAAAAAAAALAAAAEYAAAAAAAAAAAAAAAAAAACEAAAAAAAAAAAAAAAAAAAAAQAAAAA="
   },
   "id": "dupe-01-max-weight",
   "labels": [
    [
     "t/a",
     1
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "eC5xcQ=="
   ]
  },
  {
   "class": "dupe",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2:{root}/s3:{root}/s4",
    "XDG_DATA_HOME": null
   },
   "files": {
    "s1/mime/mime.cache": "AAEAAgAAADAAAAA0AAAAOAAAADwAAAB0AAAAeAAAAIQAAACIAAAAjAAAAJB0L2EAAAAAAAAAAAAAAAAAAAAAAQAAAEQAAAB6AAAAAQAAAFAAAAB6AAAAAQAAAFwAAAAuAAAAAQAAAGgAAAAAAAAALAAAAAoAAAAAAAAAAAAAAAAAAACEAAAAAAAAAAAAAAAAAAAAAQAAAAA=",
    "s2/mime/mime.cache": "AAEAAgAAADAAAAA0AAAAOAAAADwAAAB0AAAAeAAAAIQAAACIAAAAjAAAAJB0L2EAAAAAAAAAAAAAAAAAAAAAAQAAAEQAAAB6AAAAAQAAAFAAAAB6AAAAAQAAAFwAAAAuAAAAAQAAAGgAAAAAAAAALAAAABQAAAAAAAAAAAAAAAAAAACEAAAAAAAAAAAAAAAAAAAAAQAAAAA=",
    "s3/mime/mime.cache": "AAEAAgAAADAAAAA0AAAAOAAAADwAAAB0AAAAeAAAAIQAAACIAAAAjAAAAJB0L2IAAAAAAAAAAAAAAAAAAAAAAQAAAEQAAAB6AAAAAQAAAFAAAAB6AAAAAQAAAFwAAAAuAAAAAQAAAGgAAAAAAAAALAAAAB4AAAAAAAAAAAAAAAAAAACEAAAAAAAAAAAAAAAAAAAAAQAAAAA=",
    "s4/mime/mime.cache": "AAEAAgAAADAAAAA0AAAAOAAAADwAAAB0AAAAeAAAAIQAAACIAAAAjAAAAJB0L2MAAAAAAAAAAAAAAAAAAAAAAQAAAEQAAAB6AAAAAQAAAFAAAAB6AAAAAQAAAFwAAAAuAAAAAQAAAGgAAAAAAAAALAAAACgAAAAAAAAAAAAAAAAAAACEAAAAAAAAAAAAAAAAAAAAAQAAAAA="
   },
   "id": "dupe-02-swap-from-end",
   "labels": [
    [
     "t/c",
     1
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "eC56eg=="
   ]
  },
  {
   "class": "slash",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dGV4dC9wbGFpbjoqLnR4dAo="
   },
   "id": "slash-01-trailing",
   "labels": [
    [
     "inode/directory",
     1
    ],
    [
     "text/plain",
     0
    ],
    [
     "inode/directory",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS50eHQv",
    "YS50eHQ=",
    "Lw=="
   ]
  },
  {
   "class": "noglobs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/none",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dGV4dC9wbGFpbjoqLnR4dAo="
   },
   "id": "noglobs-01-empty",
   "labels": [
    [
     "application/octet-stream",
     1
    ],
    [
     "inode/directory",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eno=",
    "ZC8="
   ]
  },
  {
   "class": "dirs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": null,
    "XDG_DATA_HOME": "{root}/{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9kaDoqLnp6Cg=="
   },
   "id": "dirs-05-default-data-dirs",
   "labels": [
    [
     "text/plain",
     0
    ],
    [
     "application/zlib",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS50eHQ=",
    "YS56eg=="
   ]
  }
 ]
}
```
