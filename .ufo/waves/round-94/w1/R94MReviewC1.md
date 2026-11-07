# R94MReviewC1 — adversarial review of the C1 candidate

Seat: R94MReviewC1 (leaf, no dispatch). Lane: mado-shokunin, round 94, wave w1.
Read-only review: nothing was measured, nothing under `tools/`, `quality/`, `corpus/`, the
declaration or the candidate was touched. Every run below is labelled **DRAFT**.

* candidate `.ufo/waves/round-94/build/mado-mimeglob.c1.py` sha256
  `0700915a260627cd521ea14b61dbb15aa7c3b067c0d287f04c07b39dfa72d63e` — equals the item's pin.
* oracle `.ufo/waves/round-94/controls/mimeglob-oracle-r94.c` sha256
  `9c4337b36f93fa71bce13938f93d2e9758bb752815a67c57eb934a70bbfa6b11` — equals the item's pin.
* GLib tag 2.90.1 sources fetched from the five URLs in `receipts/sources-open-r94.txt`, HTTP
  **200** each, and their sha256 equal the digests the L1 recorded (`xdgmimeglob.c` 38ed8623…,
  `xdgmimecache.c` ccda4366…, `xdgmime.c` afb1c1c1…, `gcontenttype-fdo.c` 8a5b4f47…,
  `xdgmimeint.c` c2364aa8…). Host packages: glib2 2.90.1-1, shared-mime-info 2.5.1-2
  (`pkg-config --modversion gio-2.0` → 2.90.1).
* no install, no pacman, no host database write; `update-mime-database` ran only on directories
  under `$HYAKU_SCRATCH/mado-r94/R94MReviewC1/build/`.

## Method

1. Read `xdgmime.c`, `xdgmimeglob.c`, `xdgmimecache.c`, `xdgmimeint.c` and `gcontenttype-fdo.c`
   line by line against the tool (dirs, mode selection, text trie insert/lookup, cache literal
   search, cache suffix tree, fnmatch, dupe merge, weight sort, basename and the guess rules).
2. Differential harness: `env -i LC_ALL=C HOME=… [XDG_DATA_HOME=…] [XDG_DATA_DIRS=…] <oracle>`
   against `python3 -I <tool> --json --data-home/--data-dirs/--home …` on the same fixture,
   compared per name on (type, uncertain).
3. Fuzz: 460 random *text* fixtures and 370 random *cache* fixtures (caches produced by the real
   `update-mime-database`, then measured from the stored bytes) → **0** differing rows.
4. Host parity: 4111 names synthesised from `/usr/share/mime/mime.cache` alone (35 literals,
   1330 terminal suffix paths, 10 fnmatch patterns; `XDG_DATA_HOME` = an empty scratch dir,
   `XDG_DATA_DIRS` unset) → **0** differing rows.
5. 51 named cases in the round's case-file schema, labels from the oracle only, DRAFT answers
   from the candidate.

## Findings, by severity

### F1 — HIGH — wrong answer, and it depends on the process cwd (`HOME=""`)

* tool `.ufo/waves/round-94/build/mado-mimeglob.c1.py:451`
  `first = data_home_env if … else os.path.join(home, ".local/share")`
  (callers: `:448` `xdgmime_dirs`, `:573-577` where the default home is `env.get("HOME", "/")`).
* GLib `gio/xdgmime/xdgmime.c:255-262` (`xdg_init_dirs`, the `else if (home != NULL)` branch):
  `strcpy (guessed_xdg_home, home); strcat (guessed_xdg_home, "/.local/share/mime/")`.

`os.path.join("", ".local/share")` returns the **relative** path `.local/share`, while GLib always
builds an absolute `/.local/share/mime/` from an empty `HOME`. When `HOME` is set but empty and
`XDG_DATA_HOME` is unset, the tool therefore resolves the home mime dir against the *caller's*
cwd. This is not a refusal: it is a wrong type, and the same invocation gives different answers
from different directories.

Reproducing case `dirs-04-home-empty-relative` (in the case file below):
`HOME=""`, `XDG_DATA_HOME` unset, `XDG_DATA_DIRS="{root}/s1"`, files
`{root}/.local/share/mime/globs2 = "50:t/rel:*.rr\n"` and `{root}/s1/mime/globs2 = "50:t/abs:*.aa\n"`.

| name | oracle label | tool DRAFT (cwd = case root) | tool DRAFT (cwd elsewhere) |
|---|---|---|---|
| `x.rr` | `application/octet-stream` 1 | **`t/rel` 0 — wrong** | `application/octet-stream` 1 |
| `x.aa` | `t/abs` 0 | `t/abs` 0 | `t/abs` 0 |

Measured both ways (`cwd=<root>`: rc 0, `t/rel`; `cwd=/fast/scratch/...`: rc 0,
`application/octet-stream`). Because the case-file schema has no `cwd` field, this case is
**non-deterministic as stored**: a counter must set `cwd={root}` (where `{root}/.local/share/mime`
exists) or drop it. The defect itself is real and absolute: `home + "/.local/share"` is the fix.

Second, smaller part of the same defect: when `HOME` is **unset**, GLib pushes *no* home
directory at all (`xdgmime.c:245-262`); the tool substitutes `/` (`:573-577`) and probes
`/.local/share/mime/`. [INFERENCE] unobservable here only because `/.local/share/mime` does not
exist and I may not create it; with a home directory at `/` the tool would read databases GLib
never reads.

### F2 — HIGH — crash (exit 1) instead of an answer or a refusal, on a deep cache suffix

* tool `:332-363` `_cache_suffix_node`, recursion at `:351` (one Python frame per tree level);
  `_lookup` in text mode recurses the same way at `:177`.
* GLib `gio/xdgmime/xdgmimecache.c:492-572` `cache_glob_node_lookup_suffix`, recursion at
  `:544-550` (one C frame per level; thousands of levels are fine).

A cache built from a package XML with a simple glob longer than ~985 characters exceeds CPython's
default recursion limit. The tool dies with an uncaught `RecursionError` (exit **1**, traceback on
stderr) — neither the answer nor the documented exit 3.

Reproducing case `deep-03-cache-1000-char-suffix`: one glob `*.` + 1000 × `a` (built with
`update-mime-database`, `mime.cache` stored base64), name `x.` + 1000 × `a`.
oracle: `t/long\t0` (rc 0). tool DRAFT: rc 1,
`RecursionError: maximum recursion depth exceeded` at
`ch = c_char(name[length - 1])`. Threshold measured: L=990 answers, L=1000 crashes.
Text mode is not exposed (the `fgets(…,255)` chunking caps a text glob suffix at 254,
`xdgmimeglob.c:643`), so this is a cache-only path — but `update-mime-database` will write such a
tree from any long `<glob pattern=…>`.

### F3 — MEDIUM — cache mode parses text files GLib never reads, and refuses on them

* tool `:461-478` (`Resolver.__init__`) parses `globs2`/`globs` for every directory that has no
  usable cache, and `:236-249` can raise `Unsupported` from that parse; the raise is only caught
  at `:578-583`, i.e. it aborts the whole answer for every name.
* GLib `gio/xdgmime/xdgmime.c:129-153`: once a directory has a loadable `mime.cache` the function
  returns before touching `globs2`; and `:645-646` makes every name lookup use `_caches` only when
  at least one cache is loaded, so the text hash is dead weight.

Result: a stray/corrupt `globs2` in a directory that GLib ignores makes the tool answer nothing —
`MADO_MIMEGLOB: UNSUPPORTED …/s1/mime//globs2: …`, exit 3 — for names GLib answers from the cache.
Refusals are permitted by the declared contract, but this one is caused by a file outside the
computation and it silently degrades the tool's coverage on real hosts that mix a package-provided
cache with a hand-edited `globs2`.

Reproducing cases `mixed-01-cache-plus-star-globs2` and `mixed-02-cache-plus-invalid-globs2`
(valid cache in `dh`, `50:t/bad:*` resp. `50:t/bad:*.\xff` in `s1`):
oracle `t/cacheonly\t0`; tool DRAFT exit 3.

### F4 — MEDIUM — refuses `*` (empty suffix) where GLib has a defined answer

* tool `:246-249` — `raise Unsupported("simple glob with an empty suffix")`.
* GLib `gio/xdgmime/xdgmimeglob.c:563-580` (`_xdg_glob_hash_append_glob` passes `glob + 1`, i.e.
  `""`) → `:169-233` (`_xdg_glob_hash_insert_ucs4`, `character = text[0]` is 0, the node is stored
  at character 0) and `:305-340` (a root node with character 0 never matches any non-zero
  `file_name[len-1]`). GLib answers "no match"; the `*` line is inert.

Reachable: `update-mime-database` writes `50:t/any:*` for `<glob pattern="*"/>` (verified in
scratch; the host's `/usr/share/mime/globs2` has no such line today).

Reproducing cases `simple-02-empty-suffix-star` (globs2 = `50:t/x:*`) → oracle
`application/octet-stream 1` / `application/octet-stream 1`, tool exit 3; and
`simple-03-star-plus-glob` → oracle `text/plain 0` for `a.txt`, tool exit 3 (one inert line
poisons an unrelated, correct answer).

### F5 — LOW — refuses a globs2 line that is not valid UTF-8, where GLib has no validation at all

* tool `:236-240` — `glob_b.decode("utf-8")` … `raise Unsupported("… not valid UTF-8")`.
* GLib `gio/xdgmime/xdgmimeint.c:92-96` `_xdg_utf8_validate` is `return TRUE;` (the FIXME), and
  `:145-160` `_xdg_convert_to_ucs4` decodes byte by byte with `_xdg_utf8_get_char`
  (`_xdg_utf8_skip_data`), which happily consumes bare continuation bytes; `xdgmimeglob.c:628-704`
  never validates a line.

Reproducing case `bytes-01-invalid-utf8-glob` (`50:t/x:*.\xff` + `50:text/plain:*.txt`):
oracle `text/plain 0` for `a.txt`; tool exit 3. The refusal is contract-legal but it is a
*coverage* loss on any hand-written database with a legacy 8-bit glob, and it kills answers for
unrelated names.

### F6 — LOW — refuses cache string offsets past EOF where GLib answers (docstring understates it)

* tool `:287-292` `Cache.cstr` — `raise Unsupported("cache string past end")`, reached from
  `:308-330` (literal), `:360` (suffix terminal), `:382-403` (fnmatch).
* GLib `gio/xdgmime/xdgmimecache.c:369-425` (literal) uses `cache->buffer + offset` with no
  string-bounds check; the mmap'd page past EOF reads as zero-filled memory, so `strcmp` simply
  fails and the search moves on.

Reproducing case `cachefmt-06-oob-literal-string` (the literal entry's string offset rewritten to
`len+64`): oracle `application/octet-stream 1` for both names; tool exit 3. Refusal over UB is the
right engineering choice — the defect is documentary (see F7) — but the case cannot be frozen for
a counter that requires equality.

### F7 — LOW — docstring inaccuracies

* `:449-450` "`XDG_DATA_HOME` (if set, even empty) else `$HOME/.local/share`" — GLib adds **no**
  home entry when `HOME` is unset, and always inserts the `'/'`, so `HOME=""` gives
  `/.local/share/mime/` (F1). The docstring encodes the tool's bug as if it were the model.
* `:31-35` "The tool refuses (exit 3, UNSUPPORTED) … a cache whose structure fails the upstream
  bounds checks **in a way the C code would loop on**." It also refuses on a cache **string offset
  past end** (F6), and it crashes rather than refusing beyond the recursion limit (F2). The
  enumeration is incomplete in both directions.
* `:24-30` describes the per-directory mode selection but not that text files are still *parsed*
  (and can abort the run) in directories that the cache-mode decision discards (F3).
* Everything else in the upstream-model block checked out against 2.90.1, including the cited
  ranges (`:129-200`, `:643`, `:419-494`, `:536-559`, `:391-417`, `:668-724`, `:567-690`,
  `xdgmime.c:645-646`) — actual definitions are at `xdgmime.c:129/217/494/639`,
  `xdgmimeglob.c:100/169/305/377/392/420/537/563/628`, `xdgmimecache.c:108/369/433/492/574/641/669`,
  `gcontenttype-fdo.c:568`, which is consistent with the text.

### F8 — NOTE (a strength, worth recording) — the C-locale `fnmatch` is right

`:71-73` calls libc `fnmatch(pattern, name, 0)` after `setlocale(LC_ALL, "C")` at `:571`. The
oracle never calls `setlocale`, so it runs in the startup "C" locale whatever `LC_ALL`/
`LANG` say; the tool forces the same locale explicitly. If it had not, a UTF-8 locale would make
`fnmatch` multibyte-aware and diverge on `?`/`[a-z]`. Verified with `*.[1-9]`, `*.so.[0-9]*`,
`cachegrind.out*`, `*.t*t` and `x??y` against the host cache and 300+ fixtures: no divergence.

## Attacked and found faithful (no divergence)

Each item was exercised through the oracle; the case ids are in the case file.

| area | evidence |
|---|---|
| text trie insert order, extra types at a terminal node (C **prepends** at `xdgmimeglob.c:261-262`, keeps the first node's `cs`/weight when the mime repeats at `:235-241`; tool `:150-160`) | `order-02`, `weight-01`, `multi-01`, `multi-03` |
| `n_mime_types` caps (10, and `n_mime_types-n` on the second pass, `:463-467`) | `multi-01/02/03` — 12 types give `t/m11` in text mode and `t/m09` in cache mode, both matched |
| folded-then-unfolded passes, duplicates, first-hit literals (`:442-467`) | `fold-01/02`, `cs-01/02/03`, `dupe-01/02` |
| fnmatch flags 0 on the unfolded name in text mode, folded-then-unfolded in cache mode | `full-01` (cache: `XZY`→`t/full`) vs `full-02` (text: `XZY`→octet) |
| glibc `qsort` stability for n≤10 with tied weights (C `xdgmimecache.c:641-666`, tool `:428-446`) | 40-shape weight matrix + `weight-01`; ties keep insertion order in both |
| cache literal binary search with duplicate literals (2 and 3 entries, `xdgmimecache.c:369-425`) | `cachefmt-02/03/04`; mid-index selection reproduced exactly, incl. a hand-unsorted array |
| cache suffix sibling binary search, incl. unsorted/patched arrays | `cachefmt-05`, `deep-04` |
| cache weights: low 8 bits, `0x100` = cs (`xdgmimecache.c:414-415`) | `weight-04` (`-5` → `0xff`), `cachefmt-01`, `cs-01` |
| what `update-mime-database` actually stores (literals lowercased unless `cs`; a `cs` glob also gets a plain duplicate line in `globs2`, and that duplicate is dropped by the (data,mime) dedup in `_xdg_glob_list_append` for literals/full globs or by the same-mime check at `_xdg_glob_hash_insert_ucs4` for simple globs, which keeps the *first* line's `cs`/weight) | `literal-01`, `cs-01`, `cs-02`, `dupe-01` |
| `XDG_DATA_HOME` empty vs unset (`xdgmime.c:245-258`) | `dirs-01`, `dirs-05` |
| `XDG_DATA_DIRS` empty elements / trailing colon (`xdgmime.c:264-300`) | `dirs-02` |
| a directory listed twice | `dirs-03` |
| symlinked mime dir, dangling `mime.cache` symlink | measured, matched (`dh`/`dh3`) |
| unreadable `globs2` (no fallback to `globs`, both) | measured, matched (mode 000, restored) |
| `mime.cache` newer/older than `globs2` — the cache always wins (`xdgmime.c:129-153`, `:645-646`) | `mode-01` |
| cache version gate (major 1, minor 1-2, ≥40 bytes; `xdgmimecache.c:108-160`) | `mode-02`, `mode-03`, header-only-cache probe (matched) |
| `__NOGLOBS__` is an inert literal in GLib, not a delete (`xdgmimeglob.c:537-580`) | `noglobs-01` |
| `fgets(…,255)` chunking, CRLF, NUL truncation (`xdgmimeglob.c:643-660`) | `fgets-01/02`, 400-case text fuzz |
| v1 `globs` parsing incl. a colon inside the glob | `v1-01` |
| trailing `/`, `/`, `""`, basename rules (`gcontenttype-fdo.c:592-604`, `:613-620`) | `slash-01`, `nomatch-01`, host parity |
| non-ASCII: a suffix node whose char is a code point never matches the name's UTF-8 last byte (`xdgmimecache.c:492-520`) | `bytes-02`; `*.é` never matches in either mode |
| real database at scale | 4111 host names, 0 differing |

## Residual risk and verification gaps

* The build's `HAVE_MMAP`: `_xdg_mime_cache_new_from_file` returns a cache with `buffer == NULL`
  when mmap is unavailable (`xdgmimecache.c:160-175`), which would make every name
  `application/octet-stream`. The installed glib2 does use mmap (the 207 KB host cache answers
  correctly), but the tool hard-codes the mmap build; this cannot be exercised from the oracle.
* Cache minor version 1: the tool accepts 1-2 and uses the same offsets (correct for 1: the extra
  sections are at 24/28/32). No minor-1 producer exists here, so only the acceptance path was
  tested (patched minor byte), not a real minor-1 file.
* GLib's in-process re-read path (`xdg_check_dir`/`xdg_check_dirs`, `xdgmime.c:376-485`, a 5 s
  stat throttle) is invisible to a fresh-process oracle; a long-lived caller that rewrites
  `mime.cache` mid-process is out of scope for both sides.
* A `mime.cache` that is a FIFO would block `open()` in both; not exercised (would hang).
* Case-file schema gap: no `cwd` field, so F1 cannot be frozen as a case without one (see F1).
* The OOB suffix `child_offset` probe has **no oracle label**: the oracle spins
  (`_xdg_glob_node_lookup_suffix`'s `continue` at `xdgmimecache.c:537-540` leaves `min`/`max`
  unchanged → infinite loop). Measured: `subprocess.run(..., timeout=3)` raised
  `TimeoutExpired` for the matching name; the tool exits 3 with
  `cache suffix node out of bounds (the C lookup loops)`. Evidence only — it cannot enter the
  case file because the label side never returns.

## Case file (schema v1) — 51 cases

Labels are the oracle's, measured on exactly the stored bytes. `{root}` is substituted by the
case's materialised root. Files that are not stored are not read by either side (the fixtures were
stripped to `mime.cache`/`globs2`/`globs`/`aliases`/`magic`/`version` before labelling).

Coverage: all 20 classes of the schema's enum (`bytes cachefmt cs deep dirs dupe fgets fold full
literal mixed mode multi noglobs nomatch order simple slash v1 weight`), both modes
(35 text, 16 cache).

### DRAFT score

**43 / 51 exact** (84.3 %). The other 8: **1 wrong answer** (`dirs-04`), **6 refusals** (exit 3:
`simple-02`, `simple-03`, `bytes-01`, `cachefmt-06`, `mixed-01`, `mixed-02`), **1 crash** (exit 1:
`deep-03`). Of the 44 cases the tool answered, 43 are exact and 1 is wrong.

| case | class | mode | oracle label (first rows) | tool DRAFT | verdict |
|---|---|---|---|---|---|
| `simple-02-empty-suffix-star` | simple | text | octet 1 / octet 1 | exit 3 | F4 refusal |
| `simple-03-star-plus-glob` | simple | text | text/plain 0 / octet 1 | exit 3 | F4 refusal |
| `bytes-01-invalid-utf8-glob` | bytes | text | text/plain 0 | exit 3 | F5 refusal |
| `dirs-04-home-empty-relative` | dirs | text | octet 1 / t/abs 0 | `t/rel 0` / `t/abs 0` | **F1 wrong** (cwd-sensitive) |
| `cachefmt-06-oob-literal-string` | cachefmt | cache | octet 1 / octet 1 | exit 3 | F6 refusal |
| `mixed-01-cache-plus-star-globs2` | mixed | cache | t/cacheonly 0 | exit 3 | F3 refusal |
| `mixed-02-cache-plus-invalid-globs2` | mixed | cache | t/cacheonly 0 | exit 3 | F3 refusal |
| `deep-03-cache-1000-char-suffix` | deep | cache | t/long 0 | exit 1 (`RecursionError`) | **F2 crash** |

All 43 other cases (`simple-01`, `fold-01/02`, `cs-01/02/03`, `deep-01/02`, `weight-01/02/03/04`,
`dupe-01/02`, `order-01/02/03`, `multi-01/02/03`, `nomatch-01`, `slash-01`, `bytes-02`,
`fgets-01/02`, `v1-01`, `noglobs-01`, `dirs-01/02/03/05`, `mode-01/02/03`, `cachefmt-01..05`,
`full-01/02`, `literal-01`, `deep-04`) match the oracle on every name.

Implication for PRED-C1-r94-v1 conjunct (i) ("on every frozen case the tool's (type, uncertain)
equals the oracle's"): cases `simple-02`, `simple-03`, `bytes-01`, `cachefmt-06`, `mixed-01`,
`mixed-02`, `deep-03` must be excluded from the frozen set, or the tool must be fixed first (F2-F6),
because a refusal/crash has no (type, uncertain). `dirs-04` must not be frozen without a `cwd`
field (F1). The honest freeze is the 43 matching cases plus fixed-tool versions of the eight.

## Commands run (all DRAFT; exit codes as printed)

| command | rc |
|---|---|
| `curl -sS -o glib-<f> -w '%{http_code}' https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/…` × 5 | 200 each; sha256 equal to the receipt |
| `gcc -O1 -o oracle …/mimeglob-oracle-r94.c $(pkg-config --cflags --libs gio-2.0)` | 0 |
| `python3 -I …/mado-mimeglob.c1.py --selftest` → `MADO_MIMEGLOB_SELFTEST: checks=15 failed=0` | 0 |
| `python3 fuzz_text.py 60`, `400` | 0 differing (60, 400 cases) |
| `python3 fuzz_cache.py 120`, `250` | 0 differing (120, 250 cases) |
| host parity (4111 synthesised names, `/usr/share/mime/mime.cache`) | 0 differing |
| `python3 battery.py` (24 case battery) | 3 refusals, otherwise equal |
| `python3 mkcases.py` (51 cases, labels from the oracle) | 43 exact, 8 not |
| `update-mime-database <scratch dir>` (many) | 0; never on /usr, /usr/local or $HOME |

## Case file JSON

```json
{
 "cases": [
  {
   "class": "simple",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dGV4dC9wbGFpbjoqLnR4dAo="
   },
   "id": "simple-01-suffix-txt",
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
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS50eHQ=",
    "QS5UWFQ=",
    "eC56eg=="
   ]
  },
  {
   "class": "simple",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC94OioK"
   },
   "id": "simple-02-empty-suffix-star",
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
    "YQ==",
    "eC50eHQ="
   ]
  },
  {
   "class": "simple",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC94OioKNTA6dGV4dC9wbGFpbjoqLnR4dAo="
   },
   "id": "simple-03-star-plus-glob",
   "labels": [
    [
     "text/plain",
     0
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS50eHQ=",
    "eA=="
   ]
  },
  {
   "class": "fold",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC91cDpNYWtlZmlsZQo="
   },
   "id": "fold-01-literal-not-folded",
   "labels": [
    [
     "t/up",
     0
    ],
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
    "TWFrZWZpbGU=",
    "TUFLRUZJTEU=",
    "bWFrZWZpbGU="
   ]
  },
  {
   "class": "fold",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9sbzptYWtlZmlsZQo="
   },
   "id": "fold-02-literal-folded-pass",
   "labels": [
    [
     "t/lo",
     0
    ],
    [
     "t/lo",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "TUFLRUZJTEU=",
    "TWFrZWZpbGU="
   ]
  },
  {
   "class": "cs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9jOiouYzpjcwo1MDp0ZXh0L3gtYysrOiouQzpjcwo="
   },
   "id": "cs-01-cs-simple-glob",
   "labels": [
    [
     "t/c",
     0
    ],
    [
     "text/x-c++",
     0
    ],
    [
     "text/x-c++",
     0
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC5j",
    "eC5D",
    "WC5D",
    "eC5jLnR4dA=="
   ]
  },
  {
   "class": "cs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9hOk1ha2VmaWxlOmNzCg=="
   },
   "id": "cs-02-cs-literal",
   "labels": [
    [
     "t/a",
     0
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "TWFrZWZpbGU=",
    "TUFLRUZJTEU="
   ]
  },
  {
   "class": "cs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6YS8xOioueTpjcyx6CjUwOmEvMjoqLnk6eixjcwo1MDphLzM6Ki5xOiB4Y3MKNTA6YS80OioucTpjc3gK"
   },
   "id": "cs-03-flag-forms",
   "labels": [
    [
     "a/1",
     1
    ],
    [
     "application/octet-stream",
     1
    ],
    [
     "a/3",
     1
    ],
    [
     "a/3",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC55",
    "WC5Z",
    "eC5x",
    "WC5R"
   ]
  },
  {
   "class": "deep",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6YS9nejoqLmd6CjYwOmEvdGd6OioudGFyLmd6Cg=="
   },
   "id": "deep-01-tar-gz",
   "labels": [
    [
     "a/tgz",
     0
    ],
    [
     "a/gz",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC50YXIuZ3o=",
    "eC5neg=="
   ]
  },
  {
   "class": "deep",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NDA6YS9sb25nOioudGFyLmd6CjkwOmEvc2hvcnQ6Ki5nego="
   },
   "id": "deep-02-no-longest-across-weights",
   "labels": [
    [
     "a/long",
     0
    ],
    [
     "a/short",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC50YXIuZ3o=",
    "eC5neg=="
   ]
  },
  {
   "class": "weight",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9vbmU6Ki50d28KNTA6dC90d286Ki50d28K"
   },
   "id": "weight-01-equal-order",
   "labels": [
    [
     "t/one",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC50d28="
   ]
  },
  {
   "class": "weight",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "LTU6dC9uZWc6Ki5xCjA6dC96ZXJvOioucQo="
   },
   "id": "weight-02-negative",
   "labels": [
    [
     "t/zero",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC5x"
   ]
  },
  {
   "class": "weight",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "MzAwOnQvYmlnOioucQoyNTA6dC9zbWFsbDoqLnEK"
   },
   "id": "weight-03-over-255-text",
   "labels": [
    [
     "t/big",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC5x"
   ]
  },
  {
   "class": "dupe",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9hOk1ha2VmaWxlCjUwOnQvYjpNYWtlZmlsZQo="
   },
   "id": "dupe-01-literal-two-types",
   "labels": [
    [
     "t/a",
     0
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "TWFrZWZpbGU=",
    "TUFLRUZJTEU="
   ]
  },
  {
   "class": "dupe",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NjA6dC94Oiouego=",
    "s1/mime/globs2": "NDA6dC94Oiouego="
   },
   "id": "dupe-02-first-weight-wins",
   "labels": [
    [
     "t/x",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC56"
   ]
  },
  {
   "class": "order",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9kaDoqLnoK",
    "s1/mime/globs2": "NTA6dC9zMToqLnoK",
    "s2/mime/globs2": "NTA6dC9zMjoqLnoK"
   },
   "id": "order-01-three-dirs",
   "labels": [
    [
     "t/dh",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC56"
   ]
  },
  {
   "class": "order",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9hOioudHdvCjUwOnQvYjoqLnR3bwo1MDp0L2M6Ki50d28K"
   },
   "id": "order-02-three-types-terminal",
   "labels": [
    [
     "t/a",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC50d28="
   ]
  },
  {
   "class": "multi",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NDA6dC9tMDA6Ki5tCjQxOnQvbTAxOioubQo0Mjp0L20wMjoqLm0KNDM6dC9tMDM6Ki5tCjQ0OnQvbTA0OioubQo0NTp0L20wNToqLm0KNDY6dC9tMDY6Ki5tCjQ3OnQvbTA3OioubQo0ODp0L20wODoqLm0KNDk6dC9tMDk6Ki5tCjUwOnQvbTEwOioubQo1MTp0L20xMToqLm0K"
   },
   "id": "multi-01-cap12-text",
   "labels": [
    [
     "t/m11",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC5t"
   ]
  },
  {
   "class": "nomatch",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC94OiouenoK"
   },
   "id": "nomatch-01",
   "labels": [
    [
     "application/octet-stream",
     1
    ],
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
    "YS50eHQ=",
    "",
    "Li4="
   ]
  },
  {
   "class": "slash",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC94OioudHh0Cg=="
   },
   "id": "slash-01-directory",
   "labels": [
    [
     "inode/directory",
     1
    ],
    [
     "inode/directory",
     1
    ],
    [
     "inode/directory",
     1
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "ZC8=",
    "Lw==",
    "YS9iLw==",
    "YS9i"
   ]
  },
  {
   "class": "bytes",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC94Oiou/wo1MDp0ZXh0L3BsYWluOioudHh0Cg=="
   },
   "id": "bytes-01-invalid-utf8-glob",
   "labels": [
    [
     "text/plain",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS50eHQ="
   ]
  },
  {
   "class": "bytes",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9lOiouw6kK"
   },
   "id": "bytes-02-nonascii-suffix",
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
    "eC7DqQ==",
    "eC6p"
   ]
  },
  {
   "class": "fgets",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9sb25nOiouYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhCjUwOnRleHQvcGxhaW46Ki50eHQK"
   },
   "id": "fgets-01-long-line-split",
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
    "eC5hYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWE=",
    "YS50eHQ="
   ]
  },
  {
   "class": "fgets",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dGV4dC9wbGFpbjoqLnR4dA0K"
   },
   "id": "fgets-02-crlf",
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
    "YS50eHQ=",
    "YS50eHQN"
   ]
  },
  {
   "class": "v1",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs": "dC9vbmU6Ki55OmNzCnQvdHdvOioueQo="
   },
   "id": "v1-01-globs-file",
   "labels": [
    [
     "t/two",
     0
    ],
    [
     "t/one",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC55",
    "eC55OmNz"
   ]
  },
  {
   "class": "noglobs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "MDp0L2RpZmY6X19OT0dMT0JTX18KNTA6dC9kaWZmOiouZGlmZgo="
   },
   "id": "noglobs-01-literal",
   "labels": [
    [
     "t/diff",
     0
    ],
    [
     "application/octet-stream",
     1
    ],
    [
     "t/diff",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "X19OT0dMT0JTX18=",
    "YS5wYXRjaA==",
    "YS5kaWZm"
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
    "dh/mime/globs2": "NTA6dGV4dC9wbGFpbjoqLnR4dAo=",
    "s1/mime/globs2": "NTA6dC9zMToqLnoK"
   },
   "id": "dirs-01-datahome-empty",
   "labels": [
    [
     "application/octet-stream",
     1
    ],
    [
     "t/s1",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS50eHQ=",
    "eC56"
   ]
  },
  {
   "class": "dirs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": ":{root}/s1::",
    "XDG_DATA_HOME": null
   },
   "files": {
    "s1/mime/globs2": "NTA6dC9hOiouego=",
    "s2/mime/globs2": "NTA6dC9iOioueQo="
   },
   "id": "dirs-02-datadirs-empties",
   "labels": [
    [
     "t/a",
     0
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC56",
    "eC55"
   ]
  },
  {
   "class": "dirs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/dh:{root}/dh",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9hOiouego="
   },
   "id": "dirs-03-dir-twice",
   "labels": [
    [
     "t/a",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC56"
   ]
  },
  {
   "class": "dirs",
   "env": {
    "HOME": "",
    "XDG_DATA_DIRS": "{root}/s1",
    "XDG_DATA_HOME": null
   },
   "files": {
    ".local/share/mime/globs2": "NTA6dC9yZWw6Ki5ycgo=",
    "s1/mime/globs2": "NTA6dC9hYnM6Ki5hYQo="
   },
   "id": "dirs-04-home-empty-relative",
   "labels": [
    [
     "application/octet-stream",
     1
    ],
    [
     "t/abs",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC5ycg==",
    "eC5hYQ=="
   ]
  },
  {
   "class": "dirs",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1",
    "XDG_DATA_HOME": null
   },
   "files": {
    "h/.local/share/mime/globs2": "NTA6dC9ob21lOiouaGgK"
   },
   "id": "dirs-05-datahome-unset-home",
   "labels": [
    [
     "t/home",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC5oaA=="
   ]
  },
  {
   "class": "mode",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/aliases": "",
    "dh/mime/globs": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQp0ZXh0L3gtcGxhaW46Ki50eHQK",
    "dh/mime/globs2": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDp0ZXh0L3gtcGxhaW46Ki50eHQK",
    "dh/mime/magic": "TUlNRS1NYWdpYwAK",
    "dh/mime/mime.cache": "AAEAAgAAADwAAABAAAAARAAAAEgAAACMAAAAkAAAAJwAAACgAAAApAAAAKh0ZXh0L3gtcGxhaW4AAAAAAAAAAAAAAAAAAAAAAAAAAQAAAFAAAAB0AAAAAQAAAFwAAAB4AAAAAQAAAGgAAAB0AAAAAQAAAHQAAAAuAAAAAQAAAIAAAAAAAAAALAAAADIAAAAAAAAAAAAAAAAAAACcAAAAAAAAAAAAAAAAAAAAAQAAAAA=",
    "dh/mime/subclasses": "",
    "dh/mime/version": "Mi41LjEK"
   },
   "id": "mode-01-cache-beats-newer-globs2",
   "labels": [
    [
     "text/x-plain",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "YS50eHQ="
   ]
  },
  {
   "class": "mode",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dGV4dC9wbGFpbjoqLnR4dAo=",
    "dh/mime/mime.cache": "AAEAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="
   },
   "id": "mode-02-cache-minor3-falls-back",
   "labels": [
    [
     "text/plain",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS50eHQ="
   ]
  },
  {
   "class": "mode",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dGV4dC9wbGFpbjoqLnR4dAo=",
    "dh/mime/mime.cache": "AAEAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
   },
   "id": "mode-03-cache-39-bytes-falls-back",
   "labels": [
    [
     "text/plain",
     0
    ]
   ],
   "mode": "text",
   "names_b64": [
    "YS50eHQ="
   ]
  },
  {
   "class": "cachefmt",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/aliases": "",
    "dh/mime/globs": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQphcHBsaWNhdGlvbi94LXRnejoqLnRhci5negp0ZXh0L3gtbWFrZTptYWtlZmlsZQp0ZXh0L3gtYzoqLmMKdC9mdWxsOng/eQp0ZXh0L3gtcGxhaW46Ki50eHQKYXBwbGljYXRpb24veC1nejoqLmd6CnQvb25lOioudHdvCnQvdHdvOioudHdvCg==",
    "dh/mime/globs2": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo2MDphcHBsaWNhdGlvbi94LXRnejoqLnRhci5nego1MDp0ZXh0L3gtbWFrZTptYWtlZmlsZQo1MDp0ZXh0L3gtYzoqLmM6Y3MKNTA6dGV4dC94LWM6Ki5jCjUwOnQvZnVsbDp4P3kKNTA6dGV4dC94LXBsYWluOioudHh0CjUwOmFwcGxpY2F0aW9uL3gtZ3o6Ki5nego1MDp0L29uZToqLnR3bwo1MDp0L3R3bzoqLnR3bwo=",
    "dh/mime/magic": "TUlNRS1NYWdpYwAK",
    "dh/mime/mime.cache": "AAEAAgAAAKQAAACoAAAArAAAALwAAAHYAAAB6AAAAfQAAAH4AAAB/AAAAgB0L29uZQAAAHQvZnVsbAAAYXBwbGljYXRpb24veC10Z3oAAABtYWtlZmlsZQAAAAB0ZXh0L3gtbWFrZQB0ZXh0L3gtYwAAAAB4P3kAYXBwbGljYXRpb24veC1negAAAAB0ZXh0L3gtcGxhaW4AAAAAdC90d28AAAAAAAAAAAAAAAAAAAEAAABQAAAAXAAAADIAAAAEAAAAxAAAAGMAAAABAAAA9AAAAG8AAAABAAABAAAAAHQAAAABAAABDAAAAHoAAAABAAABGAAAAC4AAAABAAABJAAAAHcAAAABAAABMAAAAHgAAAABAAABPAAAAGcAAAABAAABSAAAAAAAAABoAAABMgAAAHQAAAABAAABVAAAAHQAAAABAAABYAAAAC4AAAACAAABbAAAAC4AAAACAAABhAAAAC4AAAABAAABnAAAAAAAAAB4AAAAMgAAAHIAAAABAAABqAAAAAAAAAAsAAAAMgAAAAAAAACcAAAAMgAAAAAAAACMAAAAMgAAAGEAAAABAAABtAAAAHQAAAABAAABwAAAAC4AAAABAAABzAAAAAAAAAA8AAAAPAAAAAEAAAB0AAAANAAAADIAAAAAAAAAAAAAAfQAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
    "dh/mime/subclasses": "",
    "dh/mime/version": "Mi41LjEK"
   },
   "id": "cachefmt-01-cache-rich",
   "labels": [
    [
     "text/x-plain",
     0
    ],
    [
     "text/x-plain",
     0
    ],
    [
     "text/x-c",
     0
    ],
    [
     "application/octet-stream",
     1
    ],
    [
     "application/x-tgz",
     0
    ],
    [
     "t/one",
     1
    ],
    [
     "text/x-make",
     0
    ],
    [
     "t/full",
     0
    ],
    [
     "t/full",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "YS50eHQ=",
    "QS5UWFQ=",
    "eC5j",
    "eC5D",
    "eC50YXIuZ3o=",
    "eC50d28=",
    "TWFrZWZpbGU=",
    "eHp5",
    "WFpZ"
   ]
  },
  {
   "class": "cachefmt",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/aliases": "",
    "dh/mime/globs": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQp0ZXh0L3gtbWFrZTptYWtlZmlsZQp0ZXh0L3gtbWFrZTI6bWFrZWZpbGUK",
    "dh/mime/globs2": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDp0ZXh0L3gtbWFrZTptYWtlZmlsZQo1MDp0ZXh0L3gtbWFrZTI6bWFrZWZpbGUK",
    "dh/mime/magic": "TUlNRS1NYWdpYwAK",
    "dh/mime/mime.cache": "AAEAAgAAAFQAAABYAAAAXAAAAHgAAACAAAAAhAAAAJAAAACUAAAAmAAAAJx0ZXh0L3gtbWFrZQBtYWtlZmlsZQAAAAB0ZXh0L3gtbWFrZTIAAAAAAAAAAAAAAAAAAAACAAAAOAAAACwAAAAyAAAAOAAAAEQAAAAyAAAAAAAAAIAAAAAAAAAAAAAAAAAAAACQAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAA",
    "dh/mime/subclasses": "",
    "dh/mime/version": "Mi41LjEK"
   },
   "id": "cachefmt-02-dup-literal2",
   "labels": [
    [
     "text/x-make",
     0
    ],
    [
     "text/x-make",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "TWFrZWZpbGU=",
    "TUFLRUZJTEU="
   ]
  },
  {
   "class": "cachefmt",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/aliases": "",
    "dh/mime/globs": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQp0L2E6Zm9vCnQvYjpmb28KdC9jOmZvbwo=",
    "dh/mime/globs2": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDp0L2E6Zm9vCjUwOnQvYjpmb28KNTA6dC9jOmZvbwo=",
    "dh/mime/magic": "TUlNRS1NYWdpYwAK",
    "dh/mime/mime.cache": "AAEAAgAAADwAAABAAAAARAAAAGwAAAB0AAAAeAAAAIQAAACIAAAAjAAAAJB0L2EAdC9jAHQvYgBmb28AAAAAAAAAAAAAAAADAAAAOAAAACwAAAAyAAAAOAAAADQAAAAyAAAAOAAAADAAAAAyAAAAAAAAAHQAAAAAAAAAAAAAAAAAAACEAAAAAAAAAAAAAAAAAAAAAwAAAAAAAAAAAAAAAA==",
    "dh/mime/subclasses": "",
    "dh/mime/version": "Mi41LjEK"
   },
   "id": "cachefmt-03-dup-literal3",
   "labels": [
    [
     "t/b",
     0
    ],
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
    "Rm9v",
    "Zm9v",
    "Rk9P"
   ]
  },
  {
   "class": "cachefmt",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/mime.cache": "AAEAAgAAAFQAAABYAAAAXAAAAHgAAACAAAAAhAAAAJAAAACUAAAAmAAAAJx0ZXh0L3gtbWFrZQBtYWtlZmlsZQAAAAB0ZXh0L3gtbWFrZTIAAAAAAAAAAAAAAAAAAAACAAAAOAAAACwAAAAyAAAAOAAAAEQAAAAyAAAAAAAAAIAAAAAAAAAAAAAAAAAAAACQAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAA"
   },
   "id": "cachefmt-04-unsorted-literal",
   "labels": [
    [
     "text/x-make",
     0
    ],
    [
     "text/x-make",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "TWFrZWZpbGU=",
    "bWFrZWZpbGU="
   ]
  },
  {
   "class": "cachefmt",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/mime.cache": "AAEAAgAAADwAAABAAAAARAAAAEgAAACwAAAAtAAAAMAAAADEAAAAyAAAAMx0L2FhAAAAAHQvYmIAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAFAAAABiAAAAAQAAAHQAAABhAAAAAQAAAGgAAABhAAAAAQAAAIAAAABiAAAAAQAAAIwAAAAuAAAAAQAAAJgAAAAuAAAAAQAAAKQAAAAAAAAALAAAADIAAAAAAAAANAAAADIAAAAAAAAAAAAAAAAAAADAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAA"
   },
   "id": "cachefmt-05-unsorted-suffix",
   "labels": [
    [
     "application/octet-stream",
     1
    ],
    [
     "t/bb",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "eC5hYQ==",
    "eC5iYg=="
   ]
  },
  {
   "class": "cachefmt",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/mime.cache": "AAEAAgAAADgAAAA8AAAAQAAAAFAAAABYAAAAXAAAAGgAAABsAAAAcAAAAHR6enoAdC9saXQAAAAAAAAAAAAAAAAAAAEAAAC8AAAAMAAAADIAAAAAAAAAWAAAAAAAAAAAAAAAAAAAAGgAAAAAAAAAAAAAAAAAAAABAAAAAA=="
   },
   "id": "cachefmt-06-oob-literal-string",
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
   "mode": "cache",
   "names_b64": [
    "enp6",
    "YWFh"
   ]
  },
  {
   "class": "weight",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/aliases": "",
    "dh/mime/globs": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQp0L3BvczoqLnAKdC9uZWc6Ki5uCg==",
    "dh/mime/globs2": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQoxMDp0L3BvczoqLnAKLTE6dC9uZWc6Ki5uCg==",
    "dh/mime/magic": "TUlNRS1NYWdpYwAK",
    "dh/mime/mime.cache": "AAEAAgAAADwAAABAAAAARAAAAEgAAACYAAAAnAAAAKgAAACsAAAAsAAAALR0L25lZwAAAHQvcG9zAAAAAAAAAAAAAAAAAAAAAAAAAgAAAFAAAABuAAAAAQAAAGgAAABwAAAAAQAAAHQAAAAuAAAAAQAAAIAAAAAuAAAAAQAAAIwAAAAAAAAALAAAAP8AAAAAAAAANAAAAAoAAAAAAAAAAAAAAAAAAACoAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAA",
    "dh/mime/subclasses": "",
    "dh/mime/version": "Mi41LjEK"
   },
   "id": "weight-04-cache-negweight",
   "labels": [
    [
     "t/neg",
     0
    ],
    [
     "t/pos",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "eC5u",
    "eC5w"
   ]
  },
  {
   "class": "multi",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/aliases": "",
    "dh/mime/globs": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQp0L20xMToqLm0KdC9tMTA6Ki5tCnQvbTA5OioubQp0L20wODoqLm0KdC9tMDc6Ki5tCnQvbTA2OioubQp0L20wNToqLm0KdC9tMDQ6Ki5tCnQvbTAzOioubQp0L20wMjoqLm0KdC9tMDE6Ki5tCnQvbTAwOioubQo=",
    "dh/mime/globs2": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MTp0L20xMToqLm0KNTA6dC9tMTA6Ki5tCjQ5OnQvbTA5OioubQo0ODp0L20wODoqLm0KNDc6dC9tMDc6Ki5tCjQ2OnQvbTA2OioubQo0NTp0L20wNToqLm0KNDQ6dC9tMDQ6Ki5tCjQzOnQvbTAzOioubQo0Mjp0L20wMjoqLm0KNDE6dC9tMDE6Ki5tCjQwOnQvbTAwOioubQo=",
    "dh/mime/magic": "TUlNRS1NYWdpYwAK",
    "dh/mime/mime.cache": "AAEAAgAAAIwAAACQAAAAlAAAAJgAAAFIAAABTAAAAVgAAAFcAAABYAAAAWR0L20wMAAAAHQvbTA2AAAAdC9tMDUAAAB0L20xMQAAAHQvbTA0AAAAdC9tMDMAAAB0L20wOQAAAHQvbTAyAAAAdC9tMDgAAAB0L20wMQAAAHQvbTA3AAAAdC9tMTAAAAAAAAAAAAAAAAAAAAAAAAABAAAAoAAAAG0AAAABAAAArAAAAC4AAAAMAAAAuAAAAAAAAAAsAAAAKAAAAAAAAAB0AAAAKQAAAAAAAABkAAAAKgAAAAAAAABUAAAAKwAAAAAAAABMAAAALAAAAAAAAAA8AAAALQAAAAAAAAA0AAAALgAAAAAAAAB8AAAALwAAAAAAAABsAAAAMAAAAAAAAABcAAAAMQAAAAAAAACEAAAAMgAAAAAAAABEAAAAMwAAAAAAAAAAAAAAAAAAAVgAAAAAAAAAAAAAAAAAAAAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "dh/mime/subclasses": "",
    "dh/mime/version": "Mi41LjEK"
   },
   "id": "multi-02-cap12-cache",
   "labels": [
    [
     "t/m09",
     1
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "eC5t"
   ]
  },
  {
   "class": "multi",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MTp0L20xMToqLm0KNTA6dC9tMTA6Ki5tCjQ5OnQvbTA5OioubQo0ODp0L20wODoqLm0KNDc6dC9tMDc6Ki5tCjQ2OnQvbTA2OioubQo0NTp0L20wNToqLm0KNDQ6dC9tMDQ6Ki5tCjQzOnQvbTAzOioubQo0Mjp0L20wMjoqLm0KNDE6dC9tMDE6Ki5tCjQwOnQvbTAwOioubQo="
   },
   "id": "multi-03-cap12-text-same-set",
   "labels": [
    [
     "t/m11",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eC5t"
   ]
  },
  {
   "class": "full",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/aliases": "",
    "dh/mime/globs": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQp0L2Z1bGw6eD95Cg==",
    "dh/mime/globs2": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDp0L2Z1bGw6eD95Cg==",
    "dh/mime/magic": "TUlNRS1NYWdpYwAK",
    "dh/mime/mime.cache": "AAEAAgAAADgAAAA8AAAAQAAAAEQAAABMAAAAXAAAAGgAAABsAAAAcAAAAHR4P3kAdC9mdWxsAAAAAAAAAAAAAAAAAAAAAAAAAAAATAAAAAEAAAAsAAAAMAAAADIAAAAAAAAAAAAAAGgAAAAAAAAAAAAAAAAAAAABAAAAAA==",
    "dh/mime/subclasses": "",
    "dh/mime/version": "Mi41LjEK"
   },
   "id": "full-01-cache-fnmatch-fold",
   "labels": [
    [
     "t/full",
     0
    ],
    [
     "t/full",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "eHp5",
    "WFpZ"
   ]
  },
  {
   "class": "full",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/globs2": "NTA6dC9mdWxsOng/eQo="
   },
   "id": "full-02-text-fnmatch-no-fold",
   "labels": [
    [
     "t/full",
     0
    ],
    [
     "application/octet-stream",
     1
    ]
   ],
   "mode": "text",
   "names_b64": [
    "eHp5",
    "WFpZ"
   ]
  },
  {
   "class": "mixed",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/aliases": "",
    "dh/mime/globs": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQp0L2NhY2hlb25seToqLmsK",
    "dh/mime/globs2": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDp0L2NhY2hlb25seToqLmsK",
    "dh/mime/magic": "TUlNRS1NYWdpYwAK",
    "dh/mime/mime.cache": "AAEAAgAAADgAAAA8AAAAQAAAAEQAAABwAAAAdAAAAIAAAACEAAAAiAAAAIx0L2NhY2hlb25seQAAAAAAAAAAAAAAAAAAAAABAAAATAAAAGsAAAABAAAAWAAAAC4AAAABAAAAZAAAAAAAAAAsAAAAMgAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAABAAAAAA==",
    "dh/mime/subclasses": "",
    "dh/mime/version": "Mi41LjEK",
    "s1/mime/globs2": "NTA6dC9iYWQ6Kgo="
   },
   "id": "mixed-01-cache-plus-star-globs2",
   "labels": [
    [
     "t/cacheonly",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "eC5r"
   ]
  },
  {
   "class": "mixed",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/aliases": "",
    "dh/mime/globs": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQp0L2NhY2hlb25seToqLmsK",
    "dh/mime/globs2": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDp0L2NhY2hlb25seToqLmsK",
    "dh/mime/magic": "TUlNRS1NYWdpYwAK",
    "dh/mime/mime.cache": "AAEAAgAAADgAAAA8AAAAQAAAAEQAAABwAAAAdAAAAIAAAACEAAAAiAAAAIx0L2NhY2hlb25seQAAAAAAAAAAAAAAAAAAAAABAAAATAAAAGsAAAABAAAAWAAAAC4AAAABAAAAZAAAAAAAAAAsAAAAMgAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAABAAAAAA==",
    "dh/mime/subclasses": "",
    "dh/mime/version": "Mi41LjEK",
    "s1/mime/globs2": "NTA6dC9iYWQ6Ki7/Cg=="
   },
   "id": "mixed-02-cache-plus-invalid-globs2",
   "labels": [
    [
     "t/cacheonly",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "eC5r"
   ]
  },
  {
   "class": "deep",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/aliases": "",
    "dh/mime/globs": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQp0L2xvbmc6Ki5hYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhCg==",
    "dh/mime/globs2": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDp0L2xvbmc6Ki5hYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhCg==",
    "dh/mime/magic": "TUlNRS1NYWdpYwAK",
    "dh/mime/mime.cache": "AAEAAgAAADQAAAA4AAAAPAAAAEAAAC9AAAAvRAAAL1AAAC9UAAAvWAAAL1x0L2xvbmcAAAAAAAAAAAAAAAAAAAAAAAEAAABIAAAAYQAAAAEAAABUAAAAYQAAAAEAAABgAAAAYQAAAAEAAABsAAAAYQAAAAEAAAB4AAAAYQAAAAEAAACEAAAAYQAAAAEAAACQAAAAYQAAAAEAAACcAAAAYQAAAAEAAACoAAAAYQAAAAEAAAC0AAAAYQAAAAEAAADAAAAAYQAAAAEAAADMAAAAYQAAAAEAAADYAAAAYQAAAAEAAADkAAAAYQAAAAEAAADwAAAAYQAAAAEAAAD8AAAAYQAAAAEAAAEIAAAAYQAAAAEAAAEUAAAAYQAAAAEAAAEgAAAAYQAAAAEAAAEsAAAAYQAAAAEAAAE4AAAAYQAAAAEAAAFEAAAAYQAAAAEAAAFQAAAAYQAAAAEAAAFcAAAAYQAAAAEAAAFoAAAAYQAAAAEAAAF0AAAAYQAAAAEAAAGAAAAAYQAAAAEAAAGMAAAAYQAAAAEAAAGYAAAAYQAAAAEAAAGkAAAAYQAAAAEAAAGwAAAAYQAAAAEAAAG8AAAAYQAAAAEAAAHIAAAAYQAAAAEAAAHUAAAAYQAAAAEAAAHgAAAAYQAAAAEAAAHsAAAAYQAAAAEAAAH4AAAAYQAAAAEAAAIEAAAAYQAAAAEAAAIQAAAAYQAAAAEAAAIcAAAAYQAAAAEAAAIoAAAAYQAAAAEAAAI0AAAAYQAAAAEAAAJAAAAAYQAAAAEAAAJMAAAAYQAAAAEAAAJYAAAAYQAAAAEAAAJkAAAAYQAAAAEAAAJwAAAAYQAAAAEAAAJ8AAAAYQAAAAEAAAKIAAAAYQAAAAEAAAKUAAAAYQAAAAEAAAKgAAAAYQAAAAEAAAKsAAAAYQAAAAEAAAK4AAAAYQAAAAEAAALEAAAAYQAAAAEAAALQAAAAYQAAAAEAAALcAAAAYQAAAAEAAALoAAAAYQAAAAEAAAL0AAAAYQAAAAEAAAMAAAAAYQAAAAEAAAMMAAAAYQAAAAEAAAMYAAAAYQAAAAEAAAMkAAAAYQAAAAEAAAMwAAAAYQAAAAEAAAM8AAAAYQAAAAEAAANIAAAAYQAAAAEAAANUAAAAYQAAAAEAAANgAAAAYQAAAAEAAANsAAAAYQAAAAEAAAN4AAAAYQAAAAEAAAOEAAAAYQAAAAEAAAOQAAAAYQAAAAEAAAOcAAAAYQAAAAEAAAOoAAAAYQAAAAEAAAO0AAAAYQAAAAEAAAPAAAAAYQAAAAEAAAPMAAAAYQAAAAEAAAPYAAAAYQAAAAEAAAPkAAAAYQAAAAEAAAPwAAAAYQAAAAEAAAP8AAAAYQAAAAEAAAQIAAAAYQAAAAEAAAQUAAAAYQAAAAEAAAQgAAAAYQAAAAEAAAQsAAAAYQAAAAEAAAQ4AAAAYQAAAAEAAAREAAAAYQAAAAEAAARQAAAAYQAAAAEAAARcAAAAYQAAAAEAAARoAAAAYQAAAAEAAAR0AAAAYQAAAAEAAASAAAAAYQAAAAEAAASMAAAAYQAAAAEAAASYAAAAYQAAAAEAAASkAAAAYQAAAAEAAASwAAAAYQAAAAEAAAS8AAAAYQAAAAEAAATIAAAAYQAAAAEAAATUAAAAYQAAAAEAAATgAAAAYQAAAAEAAATsAAAAYQAAAAEAAAT4AAAAYQAAAAEAAAUEAAAAYQAAAAEAAAUQAAAAYQAAAAEAAAUcAAAAYQAAAAEAAAUoAAAAYQAAAAEAAAU0AAAAYQAAAAEAAAVAAAAAYQAAAAEAAAVMAAAAYQAAAAEAAAVYAAAAYQAAAAEAAAVkAAAAYQAAAAEAAAVwAAAAYQAAAAEAAAV8AAAAYQAAAAEAAAWIAAAAYQAAAAEAAAWUAAAAYQAAAAEAAAWgAAAAYQAAAAEAAAWsAAAAYQAAAAEAAAW4AAAAYQAAAAEAAAXEAAAAYQAAAAEAAAXQAAAAYQAAAAEAAAXcAAAAYQAAAAEAAAXoAAAAYQAAAAEAAAX0AAAAYQAAAAEAAAYAAAAAYQAAAAEAAAYMAAAAYQAAAAEAAAYYAAAAYQAAAAEAAAYkAAAAYQAAAAEAAAYwAAAAYQAAAAEAAAY8AAAAYQAAAAEAAAZIAAAAYQAAAAEAAAZUAAAAYQAAAAEAAAZgAAAAYQAAAAEAAAZsAAAAYQAAAAEAAAZ4AAAAYQAAAAEAAAaEAAAAYQAAAAEAAAaQAAAAYQAAAAEAAAacAAAAYQAAAAEAAAaoAAAAYQAAAAEAAAa0AAAAYQAAAAEAAAbAAAAAYQAAAAEAAAbMAAAAYQAAAAEAAAbYAAAAYQAAAAEAAAbkAAAAYQAAAAEAAAbwAAAAYQAAAAEAAAb8AAAAYQAAAAEAAAcIAAAAYQAAAAEAAAcUAAAAYQAAAAEAAAcgAAAAYQAAAAEAAAcsAAAAYQAAAAEAAAc4AAAAYQAAAAEAAAdEAAAAYQAAAAEAAAdQAAAAYQAAAAEAAAdcAAAAYQAAAAEAAAdoAAAAYQAAAAEAAAd0AAAAYQAAAAEAAAeAAAAAYQAAAAEAAAeMAAAAYQAAAAEAAAeYAAAAYQAAAAEAAAekAAAAYQAAAAEAAAewAAAAYQAAAAEAAAe8AAAAYQAAAAEAAAfIAAAAYQAAAAEAAAfUAAAAYQAAAAEAAAfgAAAAYQAAAAEAAAfsAAAAYQAAAAEAAAf4AAAAYQAAAAEAAAgEAAAAYQAAAAEAAAgQAAAAYQAAAAEAAAgcAAAAYQAAAAEAAAgoAAAAYQAAAAEAAAg0AAAAYQAAAAEAAAhAAAAAYQAAAAEAAAhMAAAAYQAAAAEAAAhYAAAAYQAAAAEAAAhkAAAAYQAAAAEAAAhwAAAAYQAAAAEAAAh8AAAAYQAAAAEAAAiIAAAAYQAAAAEAAAiUAAAAYQAAAAEAAAigAAAAYQAAAAEAAAisAAAAYQAAAAEAAAi4AAAAYQAAAAEAAAjEAAAAYQAAAAEAAAjQAAAAYQAAAAEAAAjcAAAAYQAAAAEAAAjoAAAAYQAAAAEAAAj0AAAAYQAAAAEAAAkAAAAAYQAAAAEAAAkMAAAAYQAAAAEAAAkYAAAAYQAAAAEAAAkkAAAAYQAAAAEAAAkwAAAAYQAAAAEAAAk8AAAAYQAAAAEAAAlIAAAAYQAAAAEAAAlUAAAAYQAAAAEAAAlgAAAAYQAAAAEAAAlsAAAAYQAAAAEAAAl4AAAAYQAAAAEAAAmEAAAAYQAAAAEAAAmQAAAAYQAAAAEAAAmcAAAAYQAAAAEAAAmoAAAAYQAAAAEAAAm0AAAAYQAAAAEAAAnAAAAAYQAAAAEAAAnMAAAAYQAAAAEAAAnYAAAAYQAAAAEAAAnkAAAAYQAAAAEAAAnwAAAAYQAAAAEAAAn8AAAAYQAAAAEAAAoIAAAAYQAAAAEAAAoUAAAAYQAAAAEAAAogAAAAYQAAAAEAAAosAAAAYQAAAAEAAAo4AAAAYQAAAAEAAApEAAAAYQAAAAEAAApQAAAAYQAAAAEAAApcAAAAYQAAAAEAAApoAAAAYQAAAAEAAAp0AAAAYQAAAAEAAAqAAAAAYQAAAAEAAAqMAAAAYQAAAAEAAAqYAAAAYQAAAAEAAAqkAAAAYQAAAAEAAAqwAAAAYQAAAAEAAAq8AAAAYQAAAAEAAArIAAAAYQAAAAEAAArUAAAAYQAAAAEAAArgAAAAYQAAAAEAAArsAAAAYQAAAAEAAAr4AAAAYQAAAAEAAAsEAAAAYQAAAAEAAAsQAAAAYQAAAAEAAAscAAAAYQAAAAEAAAsoAAAAYQAAAAEAAAs0AAAAYQAAAAEAAAtAAAAAYQAAAAEAAAtMAAAAYQAAAAEAAAtYAAAAYQAAAAEAAAtkAAAAYQAAAAEAAAtwAAAAYQAAAAEAAAt8AAAAYQAAAAEAAAuIAAAAYQAAAAEAAAuUAAAAYQAAAAEAAAugAAAAYQAAAAEAAAusAAAAYQAAAAEAAAu4AAAAYQAAAAEAAAvEAAAAYQAAAAEAAAvQAAAAYQAAAAEAAAvcAAAAYQAAAAEAAAvoAAAAYQAAAAEAAAv0AAAAYQAAAAEAAAwAAAAAYQAAAAEAAAwMAAAAYQAAAAEAAAwYAAAAYQAAAAEAAAwkAAAAYQAAAAEAAAwwAAAAYQAAAAEAAAw8AAAAYQAAAAEAAAxIAAAAYQAAAAEAAAxUAAAAYQAAAAEAAAxgAAAAYQAAAAEAAAxsAAAAYQAAAAEAAAx4AAAAYQAAAAEAAAyEAAAAYQAAAAEAAAyQAAAAYQAAAAEAAAycAAAAYQAAAAEAAAyoAAAAYQAAAAEAAAy0AAAAYQAAAAEAAAzAAAAAYQAAAAEAAAzMAAAAYQAAAAEAAAzYAAAAYQAAAAEAAAzkAAAAYQAAAAEAAAzwAAAAYQAAAAEAAAz8AAAAYQAAAAEAAA0IAAAAYQAAAAEAAA0UAAAAYQAAAAEAAA0gAAAAYQAAAAEAAA0sAAAAYQAAAAEAAA04AAAAYQAAAAEAAA1EAAAAYQAAAAEAAA1QAAAAYQAAAAEAAA1cAAAAYQAAAAEAAA1oAAAAYQAAAAEAAA10AAAAYQAAAAEAAA2AAAAAYQAAAAEAAA2MAAAAYQAAAAEAAA2YAAAAYQAAAAEAAA2kAAAAYQAAAAEAAA2wAAAAYQAAAAEAAA28AAAAYQAAAAEAAA3IAAAAYQAAAAEAAA3UAAAAYQAAAAEAAA3gAAAAYQAAAAEAAA3sAAAAYQAAAAEAAA34AAAAYQAAAAEAAA4EAAAAYQAAAAEAAA4QAAAAYQAAAAEAAA4cAAAAYQAAAAEAAA4oAAAAYQAAAAEAAA40AAAAYQAAAAEAAA5AAAAAYQAAAAEAAA5MAAAAYQAAAAEAAA5YAAAAYQAAAAEAAA5kAAAAYQAAAAEAAA5wAAAAYQAAAAEAAA58AAAAYQAAAAEAAA6IAAAAYQAAAAEAAA6UAAAAYQAAAAEAAA6gAAAAYQAAAAEAAA6sAAAAYQAAAAEAAA64AAAAYQAAAAEAAA7EAAAAYQAAAAEAAA7QAAAAYQAAAAEAAA7cAAAAYQAAAAEAAA7oAAAAYQAAAAEAAA70AAAAYQAAAAEAAA8AAAAAYQAAAAEAAA8MAAAAYQAAAAEAAA8YAAAAYQAAAAEAAA8kAAAAYQAAAAEAAA8wAAAAYQAAAAEAAA88AAAAYQAAAAEAAA9IAAAAYQAAAAEAAA9UAAAAYQAAAAEAAA9gAAAAYQAAAAEAAA9sAAAAYQAAAAEAAA94AAAAYQAAAAEAAA+EAAAAYQAAAAEAAA+QAAAAYQAAAAEAAA+cAAAAYQAAAAEAAA+oAAAAYQAAAAEAAA+0AAAAYQAAAAEAAA/AAAAAYQAAAAEAAA/MAAAAYQAAAAEAAA/YAAAAYQAAAAEAAA/kAAAAYQAAAAEAAA/wAAAAYQAAAAEAAA/8AAAAYQAAAAEAABAIAAAAYQAAAAEAABAUAAAAYQAAAAEAABAgAAAAYQAAAAEAABAsAAAAYQAAAAEAABA4AAAAYQAAAAEAABBEAAAAYQAAAAEAABBQAAAAYQAAAAEAABBcAAAAYQAAAAEAABBoAAAAYQAAAAEAABB0AAAAYQAAAAEAABCAAAAAYQAAAAEAABCMAAAAYQAAAAEAABCYAAAAYQAAAAEAABCkAAAAYQAAAAEAABCwAAAAYQAAAAEAABC8AAAAYQAAAAEAABDIAAAAYQAAAAEAABDUAAAAYQAAAAEAABDgAAAAYQAAAAEAABDsAAAAYQAAAAEAABD4AAAAYQAAAAEAABEEAAAAYQAAAAEAABEQAAAAYQAAAAEAABEcAAAAYQAAAAEAABEoAAAAYQAAAAEAABE0AAAAYQAAAAEAABFAAAAAYQAAAAEAABFMAAAAYQAAAAEAABFYAAAAYQAAAAEAABFkAAAAYQAAAAEAABFwAAAAYQAAAAEAABF8AAAAYQAAAAEAABGIAAAAYQAAAAEAABGUAAAAYQAAAAEAABGgAAAAYQAAAAEAABGsAAAAYQAAAAEAABG4AAAAYQAAAAEAABHEAAAAYQAAAAEAABHQAAAAYQAAAAEAABHcAAAAYQAAAAEAABHoAAAAYQAAAAEAABH0AAAAYQAAAAEAABIAAAAAYQAAAAEAABIMAAAAYQAAAAEAABIYAAAAYQAAAAEAABIkAAAAYQAAAAEAABIwAAAAYQAAAAEAABI8AAAAYQAAAAEAABJIAAAAYQAAAAEAABJUAAAAYQAAAAEAABJgAAAAYQAAAAEAABJsAAAAYQAAAAEAABJ4AAAAYQAAAAEAABKEAAAAYQAAAAEAABKQAAAAYQAAAAEAABKcAAAAYQAAAAEAABKoAAAAYQAAAAEAABK0AAAAYQAAAAEAABLAAAAAYQAAAAEAABLMAAAAYQAAAAEAABLYAAAAYQAAAAEAABLkAAAAYQAAAAEAABLwAAAAYQAAAAEAABL8AAAAYQAAAAEAABMIAAAAYQAAAAEAABMUAAAAYQAAAAEAABMgAAAAYQAAAAEAABMsAAAAYQAAAAEAABM4AAAAYQAAAAEAABNEAAAAYQAAAAEAABNQAAAAYQAAAAEAABNcAAAAYQAAAAEAABNoAAAAYQAAAAEAABN0AAAAYQAAAAEAABOAAAAAYQAAAAEAABOMAAAAYQAAAAEAABOYAAAAYQAAAAEAABOkAAAAYQAAAAEAABOwAAAAYQAAAAEAABO8AAAAYQAAAAEAABPIAAAAYQAAAAEAABPUAAAAYQAAAAEAABPgAAAAYQAAAAEAABPsAAAAYQAAAAEAABP4AAAAYQAAAAEAABQEAAAAYQAAAAEAABQQAAAAYQAAAAEAABQcAAAAYQAAAAEAABQoAAAAYQAAAAEAABQ0AAAAYQAAAAEAABRAAAAAYQAAAAEAABRMAAAAYQAAAAEAABRYAAAAYQAAAAEAABRkAAAAYQAAAAEAABRwAAAAYQAAAAEAABR8AAAAYQAAAAEAABSIAAAAYQAAAAEAABSUAAAAYQAAAAEAABSgAAAAYQAAAAEAABSsAAAAYQAAAAEAABS4AAAAYQAAAAEAABTEAAAAYQAAAAEAABTQAAAAYQAAAAEAABTcAAAAYQAAAAEAABToAAAAYQAAAAEAABT0AAAAYQAAAAEAABUAAAAAYQAAAAEAABUMAAAAYQAAAAEAABUYAAAAYQAAAAEAABUkAAAAYQAAAAEAABUwAAAAYQAAAAEAABU8AAAAYQAAAAEAABVIAAAAYQAAAAEAABVUAAAAYQAAAAEAABVgAAAAYQAAAAEAABVsAAAAYQAAAAEAABV4AAAAYQAAAAEAABWEAAAAYQAAAAEAABWQAAAAYQAAAAEAABWcAAAAYQAAAAEAABWoAAAAYQAAAAEAABW0AAAAYQAAAAEAABXAAAAAYQAAAAEAABXMAAAAYQAAAAEAABXYAAAAYQAAAAEAABXkAAAAYQAAAAEAABXwAAAAYQAAAAEAABX8AAAAYQAAAAEAABYIAAAAYQAAAAEAABYUAAAAYQAAAAEAABYgAAAAYQAAAAEAABYsAAAAYQAAAAEAABY4AAAAYQAAAAEAABZEAAAAYQAAAAEAABZQAAAAYQAAAAEAABZcAAAAYQAAAAEAABZoAAAAYQAAAAEAABZ0AAAAYQAAAAEAABaAAAAAYQAAAAEAABaMAAAAYQAAAAEAABaYAAAAYQAAAAEAABakAAAAYQAAAAEAABawAAAAYQAAAAEAABa8AAAAYQAAAAEAABbIAAAAYQAAAAEAABbUAAAAYQAAAAEAABbgAAAAYQAAAAEAABbsAAAAYQAAAAEAABb4AAAAYQAAAAEAABcEAAAAYQAAAAEAABcQAAAAYQAAAAEAABccAAAAYQAAAAEAABcoAAAAYQAAAAEAABc0AAAAYQAAAAEAABdAAAAAYQAAAAEAABdMAAAAYQAAAAEAABdYAAAAYQAAAAEAABdkAAAAYQAAAAEAABdwAAAAYQAAAAEAABd8AAAAYQAAAAEAABeIAAAAYQAAAAEAABeUAAAAYQAAAAEAABegAAAAYQAAAAEAABesAAAAYQAAAAEAABe4AAAAYQAAAAEAABfEAAAAYQAAAAEAABfQAAAAYQAAAAEAABfcAAAAYQAAAAEAABfoAAAAYQAAAAEAABf0AAAAYQAAAAEAABgAAAAAYQAAAAEAABgMAAAAYQAAAAEAABgYAAAAYQAAAAEAABgkAAAAYQAAAAEAABgwAAAAYQAAAAEAABg8AAAAYQAAAAEAABhIAAAAYQAAAAEAABhUAAAAYQAAAAEAABhgAAAAYQAAAAEAABhsAAAAYQAAAAEAABh4AAAAYQAAAAEAABiEAAAAYQAAAAEAABiQAAAAYQAAAAEAABicAAAAYQAAAAEAABioAAAAYQAAAAEAABi0AAAAYQAAAAEAABjAAAAAYQAAAAEAABjMAAAAYQAAAAEAABjYAAAAYQAAAAEAABjkAAAAYQAAAAEAABjwAAAAYQAAAAEAABj8AAAAYQAAAAEAABkIAAAAYQAAAAEAABkUAAAAYQAAAAEAABkgAAAAYQAAAAEAABksAAAAYQAAAAEAABk4AAAAYQAAAAEAABlEAAAAYQAAAAEAABlQAAAAYQAAAAEAABlcAAAAYQAAAAEAABloAAAAYQAAAAEAABl0AAAAYQAAAAEAABmAAAAAYQAAAAEAABmMAAAAYQAAAAEAABmYAAAAYQAAAAEAABmkAAAAYQAAAAEAABmwAAAAYQAAAAEAABm8AAAAYQAAAAEAABnIAAAAYQAAAAEAABnUAAAAYQAAAAEAABngAAAAYQAAAAEAABnsAAAAYQAAAAEAABn4AAAAYQAAAAEAABoEAAAAYQAAAAEAABoQAAAAYQAAAAEAABocAAAAYQAAAAEAABooAAAAYQAAAAEAABo0AAAAYQAAAAEAABpAAAAAYQAAAAEAABpMAAAAYQAAAAEAABpYAAAAYQAAAAEAABpkAAAAYQAAAAEAABpwAAAAYQAAAAEAABp8AAAAYQAAAAEAABqIAAAAYQAAAAEAABqUAAAAYQAAAAEAABqgAAAAYQAAAAEAABqsAAAAYQAAAAEAABq4AAAAYQAAAAEAABrEAAAAYQAAAAEAABrQAAAAYQAAAAEAABrcAAAAYQAAAAEAABroAAAAYQAAAAEAABr0AAAAYQAAAAEAABsAAAAAYQAAAAEAABsMAAAAYQAAAAEAABsYAAAAYQAAAAEAABskAAAAYQAAAAEAABswAAAAYQAAAAEAABs8AAAAYQAAAAEAABtIAAAAYQAAAAEAABtUAAAAYQAAAAEAABtgAAAAYQAAAAEAABtsAAAAYQAAAAEAABt4AAAAYQAAAAEAABuEAAAAYQAAAAEAABuQAAAAYQAAAAEAABucAAAAYQAAAAEAABuoAAAAYQAAAAEAABu0AAAAYQAAAAEAABvAAAAAYQAAAAEAABvMAAAAYQAAAAEAABvYAAAAYQAAAAEAABvkAAAAYQAAAAEAABvwAAAAYQAAAAEAABv8AAAAYQAAAAEAABwIAAAAYQAAAAEAABwUAAAAYQAAAAEAABwgAAAAYQAAAAEAABwsAAAAYQAAAAEAABw4AAAAYQAAAAEAABxEAAAAYQAAAAEAABxQAAAAYQAAAAEAABxcAAAAYQAAAAEAABxoAAAAYQAAAAEAABx0AAAAYQAAAAEAAByAAAAAYQAAAAEAAByMAAAAYQAAAAEAAByYAAAAYQAAAAEAABykAAAAYQAAAAEAABywAAAAYQAAAAEAABy8AAAAYQAAAAEAABzIAAAAYQAAAAEAABzUAAAAYQAAAAEAABzgAAAAYQAAAAEAABzsAAAAYQAAAAEAABz4AAAAYQAAAAEAAB0EAAAAYQAAAAEAAB0QAAAAYQAAAAEAAB0cAAAAYQAAAAEAAB0oAAAAYQAAAAEAAB00AAAAYQAAAAEAAB1AAAAAYQAAAAEAAB1MAAAAYQAAAAEAAB1YAAAAYQAAAAEAAB1kAAAAYQAAAAEAAB1wAAAAYQAAAAEAAB18AAAAYQAAAAEAAB2IAAAAYQAAAAEAAB2UAAAAYQAAAAEAAB2gAAAAYQAAAAEAAB2sAAAAYQAAAAEAAB24AAAAYQAAAAEAAB3EAAAAYQAAAAEAAB3QAAAAYQAAAAEAAB3cAAAAYQAAAAEAAB3oAAAAYQAAAAEAAB30AAAAYQAAAAEAAB4AAAAAYQAAAAEAAB4MAAAAYQAAAAEAAB4YAAAAYQAAAAEAAB4kAAAAYQAAAAEAAB4wAAAAYQAAAAEAAB48AAAAYQAAAAEAAB5IAAAAYQAAAAEAAB5UAAAAYQAAAAEAAB5gAAAAYQAAAAEAAB5sAAAAYQAAAAEAAB54AAAAYQAAAAEAAB6EAAAAYQAAAAEAAB6QAAAAYQAAAAEAAB6cAAAAYQAAAAEAAB6oAAAAYQAAAAEAAB60AAAAYQAAAAEAAB7AAAAAYQAAAAEAAB7MAAAAYQAAAAEAAB7YAAAAYQAAAAEAAB7kAAAAYQAAAAEAAB7wAAAAYQAAAAEAAB78AAAAYQAAAAEAAB8IAAAAYQAAAAEAAB8UAAAAYQAAAAEAAB8gAAAAYQAAAAEAAB8sAAAAYQAAAAEAAB84AAAAYQAAAAEAAB9EAAAAYQAAAAEAAB9QAAAAYQAAAAEAAB9cAAAAYQAAAAEAAB9oAAAAYQAAAAEAAB90AAAAYQAAAAEAAB+AAAAAYQAAAAEAAB+MAAAAYQAAAAEAAB+YAAAAYQAAAAEAAB+kAAAAYQAAAAEAAB+wAAAAYQAAAAEAAB+8AAAAYQAAAAEAAB/IAAAAYQAAAAEAAB/UAAAAYQAAAAEAAB/gAAAAYQAAAAEAAB/sAAAAYQAAAAEAAB/4AAAAYQAAAAEAACAEAAAAYQAAAAEAACAQAAAAYQAAAAEAACAcAAAAYQAAAAEAACAoAAAAYQAAAAEAACA0AAAAYQAAAAEAACBAAAAAYQAAAAEAACBMAAAAYQAAAAEAACBYAAAAYQAAAAEAACBkAAAAYQAAAAEAACBwAAAAYQAAAAEAACB8AAAAYQAAAAEAACCIAAAAYQAAAAEAACCUAAAAYQAAAAEAACCgAAAAYQAAAAEAACCsAAAAYQAAAAEAACC4AAAAYQAAAAEAACDEAAAAYQAAAAEAACDQAAAAYQAAAAEAACDcAAAAYQAAAAEAACDoAAAAYQAAAAEAACD0AAAAYQAAAAEAACEAAAAAYQAAAAEAACEMAAAAYQAAAAEAACEYAAAAYQAAAAEAACEkAAAAYQAAAAEAACEwAAAAYQAAAAEAACE8AAAAYQAAAAEAACFIAAAAYQAAAAEAACFUAAAAYQAAAAEAACFgAAAAYQAAAAEAACFsAAAAYQAAAAEAACF4AAAAYQAAAAEAACGEAAAAYQAAAAEAACGQAAAAYQAAAAEAACGcAAAAYQAAAAEAACGoAAAAYQAAAAEAACG0AAAAYQAAAAEAACHAAAAAYQAAAAEAACHMAAAAYQAAAAEAACHYAAAAYQAAAAEAACHkAAAAYQAAAAEAACHwAAAAYQAAAAEAACH8AAAAYQAAAAEAACIIAAAAYQAAAAEAACIUAAAAYQAAAAEAACIgAAAAYQAAAAEAACIsAAAAYQAAAAEAACI4AAAAYQAAAAEAACJEAAAAYQAAAAEAACJQAAAAYQAAAAEAACJcAAAAYQAAAAEAACJoAAAAYQAAAAEAACJ0AAAAYQAAAAEAACKAAAAAYQAAAAEAACKMAAAAYQAAAAEAACKYAAAAYQAAAAEAACKkAAAAYQAAAAEAACKwAAAAYQAAAAEAACK8AAAAYQAAAAEAACLIAAAAYQAAAAEAACLUAAAAYQAAAAEAACLgAAAAYQAAAAEAACLsAAAAYQAAAAEAACL4AAAAYQAAAAEAACMEAAAAYQAAAAEAACMQAAAAYQAAAAEAACMcAAAAYQAAAAEAACMoAAAAYQAAAAEAACM0AAAAYQAAAAEAACNAAAAAYQAAAAEAACNMAAAAYQAAAAEAACNYAAAAYQAAAAEAACNkAAAAYQAAAAEAACNwAAAAYQAAAAEAACN8AAAAYQAAAAEAACOIAAAAYQAAAAEAACOUAAAAYQAAAAEAACOgAAAAYQAAAAEAACOsAAAAYQAAAAEAACO4AAAAYQAAAAEAACPEAAAAYQAAAAEAACPQAAAAYQAAAAEAACPcAAAAYQAAAAEAACPoAAAAYQAAAAEAACP0AAAAYQAAAAEAACQAAAAAYQAAAAEAACQMAAAAYQAAAAEAACQYAAAAYQAAAAEAACQkAAAAYQAAAAEAACQwAAAAYQAAAAEAACQ8AAAAYQAAAAEAACRIAAAAYQAAAAEAACRUAAAAYQAAAAEAACRgAAAAYQAAAAEAACRsAAAAYQAAAAEAACR4AAAAYQAAAAEAACSEAAAAYQAAAAEAACSQAAAAYQAAAAEAACScAAAAYQAAAAEAACSoAAAAYQAAAAEAACS0AAAAYQAAAAEAACTAAAAAYQAAAAEAACTMAAAAYQAAAAEAACTYAAAAYQAAAAEAACTkAAAAYQAAAAEAACTwAAAAYQAAAAEAACT8AAAAYQAAAAEAACUIAAAAYQAAAAEAACUUAAAAYQAAAAEAACUgAAAAYQAAAAEAACUsAAAAYQAAAAEAACU4AAAAYQAAAAEAACVEAAAAYQAAAAEAACVQAAAAYQAAAAEAACVcAAAAYQAAAAEAACVoAAAAYQAAAAEAACV0AAAAYQAAAAEAACWAAAAAYQAAAAEAACWMAAAAYQAAAAEAACWYAAAAYQAAAAEAACWkAAAAYQAAAAEAACWwAAAAYQAAAAEAACW8AAAAYQAAAAEAACXIAAAAYQAAAAEAACXUAAAAYQAAAAEAACXgAAAAYQAAAAEAACXsAAAAYQAAAAEAACX4AAAAYQAAAAEAACYEAAAAYQAAAAEAACYQAAAAYQAAAAEAACYcAAAAYQAAAAEAACYoAAAAYQAAAAEAACY0AAAAYQAAAAEAACZAAAAAYQAAAAEAACZMAAAAYQAAAAEAACZYAAAAYQAAAAEAACZkAAAAYQAAAAEAACZwAAAAYQAAAAEAACZ8AAAAYQAAAAEAACaIAAAAYQAAAAEAACaUAAAAYQAAAAEAACagAAAAYQAAAAEAACasAAAAYQAAAAEAACa4AAAAYQAAAAEAACbEAAAAYQAAAAEAACbQAAAAYQAAAAEAACbcAAAAYQAAAAEAACboAAAAYQAAAAEAACb0AAAAYQAAAAEAACcAAAAAYQAAAAEAACcMAAAAYQAAAAEAACcYAAAAYQAAAAEAACckAAAAYQAAAAEAACcwAAAAYQAAAAEAACc8AAAAYQAAAAEAACdIAAAAYQAAAAEAACdUAAAAYQAAAAEAACdgAAAAYQAAAAEAACdsAAAAYQAAAAEAACd4AAAAYQAAAAEAACeEAAAAYQAAAAEAACeQAAAAYQAAAAEAACecAAAAYQAAAAEAACeoAAAAYQAAAAEAACe0AAAAYQAAAAEAACfAAAAAYQAAAAEAACfMAAAAYQAAAAEAACfYAAAAYQAAAAEAACfkAAAAYQAAAAEAACfwAAAAYQAAAAEAACf8AAAAYQAAAAEAACgIAAAAYQAAAAEAACgUAAAAYQAAAAEAACggAAAAYQAAAAEAACgsAAAAYQAAAAEAACg4AAAAYQAAAAEAAChEAAAAYQAAAAEAAChQAAAAYQAAAAEAAChcAAAAYQAAAAEAAChoAAAAYQAAAAEAACh0AAAAYQAAAAEAACiAAAAAYQAAAAEAACiMAAAAYQAAAAEAACiYAAAAYQAAAAEAACikAAAAYQAAAAEAACiwAAAAYQAAAAEAACi8AAAAYQAAAAEAACjIAAAAYQAAAAEAACjUAAAAYQAAAAEAACjgAAAAYQAAAAEAACjsAAAAYQAAAAEAACj4AAAAYQAAAAEAACkEAAAAYQAAAAEAACkQAAAAYQAAAAEAACkcAAAAYQAAAAEAACkoAAAAYQAAAAEAACk0AAAAYQAAAAEAAClAAAAAYQAAAAEAAClMAAAAYQAAAAEAAClYAAAAYQAAAAEAAClkAAAAYQAAAAEAAClwAAAAYQAAAAEAACl8AAAAYQAAAAEAACmIAAAAYQAAAAEAACmUAAAAYQAAAAEAACmgAAAAYQAAAAEAACmsAAAAYQAAAAEAACm4AAAAYQAAAAEAACnEAAAAYQAAAAEAACnQAAAAYQAAAAEAACncAAAAYQAAAAEAACnoAAAAYQAAAAEAACn0AAAAYQAAAAEAACoAAAAAYQAAAAEAACoMAAAAYQAAAAEAACoYAAAAYQAAAAEAACokAAAAYQAAAAEAACowAAAAYQAAAAEAACo8AAAAYQAAAAEAACpIAAAAYQAAAAEAACpUAAAAYQAAAAEAACpgAAAAYQAAAAEAACpsAAAAYQAAAAEAACp4AAAAYQAAAAEAACqEAAAAYQAAAAEAACqQAAAAYQAAAAEAACqcAAAAYQAAAAEAACqoAAAAYQAAAAEAACq0AAAAYQAAAAEAACrAAAAAYQAAAAEAACrMAAAAYQAAAAEAACrYAAAAYQAAAAEAACrkAAAAYQAAAAEAACrwAAAAYQAAAAEAACr8AAAAYQAAAAEAACsIAAAAYQAAAAEAACsUAAAAYQAAAAEAACsgAAAAYQAAAAEAACssAAAAYQAAAAEAACs4AAAAYQAAAAEAACtEAAAAYQAAAAEAACtQAAAAYQAAAAEAACtcAAAAYQAAAAEAACtoAAAAYQAAAAEAACt0AAAAYQAAAAEAACuAAAAAYQAAAAEAACuMAAAAYQAAAAEAACuYAAAAYQAAAAEAACukAAAAYQAAAAEAACuwAAAAYQAAAAEAACu8AAAAYQAAAAEAACvIAAAAYQAAAAEAACvUAAAAYQAAAAEAACvgAAAAYQAAAAEAACvsAAAAYQAAAAEAACv4AAAAYQAAAAEAACwEAAAAYQAAAAEAACwQAAAAYQAAAAEAACwcAAAAYQAAAAEAACwoAAAAYQAAAAEAACw0AAAAYQAAAAEAACxAAAAAYQAAAAEAACxMAAAAYQAAAAEAACxYAAAAYQAAAAEAACxkAAAAYQAAAAEAACxwAAAAYQAAAAEAACx8AAAAYQAAAAEAACyIAAAAYQAAAAEAACyUAAAAYQAAAAEAACygAAAAYQAAAAEAACysAAAAYQAAAAEAACy4AAAAYQAAAAEAACzEAAAAYQAAAAEAACzQAAAAYQAAAAEAACzcAAAAYQAAAAEAACzoAAAAYQAAAAEAACz0AAAAYQAAAAEAAC0AAAAAYQAAAAEAAC0MAAAAYQAAAAEAAC0YAAAAYQAAAAEAAC0kAAAAYQAAAAEAAC0wAAAAYQAAAAEAAC08AAAAYQAAAAEAAC1IAAAAYQAAAAEAAC1UAAAAYQAAAAEAAC1gAAAAYQAAAAEAAC1sAAAAYQAAAAEAAC14AAAAYQAAAAEAAC2EAAAAYQAAAAEAAC2QAAAAYQAAAAEAAC2cAAAAYQAAAAEAAC2oAAAAYQAAAAEAAC20AAAAYQAAAAEAAC3AAAAAYQAAAAEAAC3MAAAAYQAAAAEAAC3YAAAAYQAAAAEAAC3kAAAAYQAAAAEAAC3wAAAAYQAAAAEAAC38AAAAYQAAAAEAAC4IAAAAYQAAAAEAAC4UAAAAYQAAAAEAAC4gAAAAYQAAAAEAAC4sAAAAYQAAAAEAAC44AAAAYQAAAAEAAC5EAAAAYQAAAAEAAC5QAAAAYQAAAAEAAC5cAAAAYQAAAAEAAC5oAAAAYQAAAAEAAC50AAAAYQAAAAEAAC6AAAAAYQAAAAEAAC6MAAAAYQAAAAEAAC6YAAAAYQAAAAEAAC6kAAAAYQAAAAEAAC6wAAAAYQAAAAEAAC68AAAAYQAAAAEAAC7IAAAAYQAAAAEAAC7UAAAAYQAAAAEAAC7gAAAAYQAAAAEAAC7sAAAAYQAAAAEAAC74AAAAYQAAAAEAAC8EAAAAYQAAAAEAAC8QAAAAYQAAAAEAAC8cAAAAYQAAAAEAAC8oAAAALgAAAAEAAC80AAAAAAAAACwAAAAyAAAAAAAAAAAAAAAAAAAvUAAAAAAAAAAAAAAAAAAAAAEAAAAA",
    "dh/mime/subclasses": "",
    "dh/mime/version": "Mi41LjEK"
   },
   "id": "deep-03-cache-1000-char-suffix",
   "labels": [
    [
     "t/long",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "eC5hYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFh"
   ]
  },
  {
   "class": "order",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/aliases": "",
    "dh/mime/globs": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQp0L2QxOiouawo=",
    "dh/mime/globs2": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDp0L2QxOiouawo=",
    "dh/mime/magic": "TUlNRS1NYWdpYwAK",
    "dh/mime/mime.cache": "AAEAAgAAADQAAAA4AAAAPAAAAEAAAABsAAAAcAAAAHwAAACAAAAAhAAAAIh0L2QxAAAAAAAAAAAAAAAAAAAAAAAAAAEAAABIAAAAawAAAAEAAABUAAAALgAAAAEAAABgAAAAAAAAACwAAAAyAAAAAAAAAAAAAAAAAAAAfAAAAAAAAAAAAAAAAAAAAAEAAAAA",
    "dh/mime/subclasses": "",
    "dh/mime/version": "Mi41LjEK",
    "s1/mime/aliases": "",
    "s1/mime/globs": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQp0L2QyOiouawo=",
    "s1/mime/globs2": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDp0L2QyOiouawo=",
    "s1/mime/magic": "TUlNRS1NYWdpYwAK",
    "s1/mime/mime.cache": "AAEAAgAAADQAAAA4AAAAPAAAAEAAAABsAAAAcAAAAHwAAACAAAAAhAAAAIh0L2QyAAAAAAAAAAAAAAAAAAAAAAAAAAEAAABIAAAAawAAAAEAAABUAAAALgAAAAEAAABgAAAAAAAAACwAAAAyAAAAAAAAAAAAAAAAAAAAfAAAAAAAAAAAAAAAAAAAAAEAAAAA",
    "s1/mime/subclasses": "",
    "s1/mime/version": "Mi41LjEK"
   },
   "id": "order-03-cache-two-caches",
   "labels": [
    [
     "t/d1",
     1
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "eC5r"
   ]
  },
  {
   "class": "literal",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/aliases": "",
    "dh/mime/globs": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQp0L3VwOm1ha2VmaWxlCg==",
    "dh/mime/globs2": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDp0L3VwOm1ha2VmaWxlCg==",
    "dh/mime/magic": "TUlNRS1NYWdpYwAK",
    "dh/mime/mime.cache": "AAEAAgAAAEAAAABEAAAASAAAAFgAAABgAAAAZAAAAHAAAAB0AAAAeAAAAHx0L3VwAAAAAG1ha2VmaWxlAAAAAAAAAAAAAAAAAAAAAQAAADQAAAAsAAAAMgAAAAAAAABgAAAAAAAAAAAAAAAAAAAAcAAAAAAAAAAAAAAAAAAAAAEAAAAA",
    "dh/mime/subclasses": "",
    "dh/mime/version": "Mi41LjEK"
   },
   "id": "literal-01-cache-lowercased",
   "labels": [
    [
     "t/up",
     0
    ],
    [
     "t/up",
     0
    ],
    [
     "t/up",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "TWFrZWZpbGU=",
    "TUFLRUZJTEU=",
    "bWFrZWZpbGU="
   ]
  },
  {
   "class": "deep",
   "env": {
    "HOME": "{root}/h",
    "XDG_DATA_DIRS": "{root}/s1:{root}/s2",
    "XDG_DATA_HOME": "{root}/dh"
   },
   "files": {
    "dh/mime/aliases": "",
    "dh/mime/globs": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQp0L2I6Ki5iCnQvY2FiOiouY2FiCg==",
    "dh/mime/globs2": "IyBUaGlzIGZpbGUgd2FzIGF1dG9tYXRpY2FsbHkgZ2VuZXJhdGVkIGJ5IHRoZQojIHVwZGF0ZS1taW1lLWRhdGFiYXNlIGNvbW1hbmQuIERPIE5PVCBFRElUIQo1MDp0L2I6Ki5iCjUwOnQvY2FiOiouY2FiCg==",
    "dh/mime/magic": "TUlNRS1NYWdpYwAK",
    "dh/mime/mime.cache": "AAEAAgAAADgAAAA8AAAAQAAAAEQAAACgAAAApAAAALAAAAC0AAAAuAAAALx0L2IAdC9jYWIAAAAAAAAAAAAAAAAAAAAAAAABAAAATAAAAGIAAAACAAAAWAAAAC4AAAABAAAAcAAAAGEAAAABAAAAfAAAAAAAAAAsAAAAMgAAAGMAAAABAAAAiAAAAC4AAAABAAAAlAAAAAAAAAAwAAAAMgAAAAAAAAAAAAAAAAAAALAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAA=",
    "dh/mime/subclasses": "",
    "dh/mime/version": "Mi41LjEK"
   },
   "id": "deep-04-cache-prefix-terminal",
   "labels": [
    [
     "t/b",
     0
    ],
    [
     "application/octet-stream",
     1
    ],
    [
     "t/cab",
     0
    ]
   ],
   "mode": "cache",
   "names_b64": [
    "eC5i",
    "eC5jYg==",
    "eC5jYWI="
   ]
  }
 ],
 "glib2": "2.90.1-1",
 "oracle_src_sha256": "9c4337b36f93fa71bce13938f93d2e9758bb752815a67c57eb934a70bbfa6b11",
 "version": 1
}
```

## Scratch

`S=$HYAKU_SCRATCH/mado-r94/R94MReviewC1` (default `/fast/scratch/hyaku`) — deleted on exit; the
only artefact is this report (the case JSON above is embedded, not referenced).
