# R95MReviewC1 — review of the C1 candidate (`mado-mimesniff` c1)

Seat: `R95MReviewC1` (reviewer, leaf). Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base revision: `4a2af6817024f6ed47084a5217c1825ae247f4fe` (master).

Under review (frozen draft named by my item):

| artefact | sha256 |
|---|---|
| `.ufo/waves/round-95/build/mado-mimesniff.c1.py` (candidate) | `a13b6e0e3b0c399892ff027309f942daa96e92713851e8d8cfb736b277cde99d` |
| `tools/mado-mimeglob.py` (name step, round 94, unchanged) | `65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453` |
| `.ufo/waves/round-95/controls/mimesniff-oracle-r95.c` (oracle) | `99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a` |
| `.ufo/waves/round-95/controls/mimesniff-host-files-r95.txt` (frozen host list, 3528 paths) | `ab409a1bf948432ff4aec59b13eb9d5e550a6898deb4b1020e6a9234c47cf1e1` |

Oracle built in my scratch: `cc -O0 -o oracle controls/mimesniff-oracle-r95.c $(pkg-config --cflags --libs gio-2.0)`
against glib2 2.90.1-1 / shared-mime-info 2.5.1-2. **Every run below is DRAFT** (no counter was run; nothing was
written under `receipts/`). `--selftest` and the candidate/oracle runs are not measurements.

The L1's in-flight successor `build/mado-mimesniff.c1b.py` was still changing while I wrote (`abef0014…` at 05:10,
`37997bdb2c2f2e4ca815afb18b869e50e85989a470e55b8bd363c7820656d3d2` at 05:22). Where it matters I say which c1b
sha I observed; the findings are scoped to **c1 = a13b6e0e…**, the sha my item names.

## Method

Line-by-line comparison of the whole candidate against the fetched GLib 2.90.1 sources, then differential testing
against the compiled oracle:

* GLib read: `xdgmime.c:129-206` (init callback), `:217-300` (`xdg_init_dirs`), `:516-541` (`for_data`), `:781-792`, `:821-831`
  (`media_type_equal`, subclass wrapper), `:880-940`; `xdgmimeint.c:176-190` (fallback); `xdgmime.h`; `xdgmimecache.c:83-84`
  (`OUT_OF_BOUNDS`), `:167-210` (`cache_magic_matchlet_compare_to_data`), `:212-239` (`_compare`), `:241-274`
  (`cache_magic_compare_to_data`), `:276-312` (`cache_magic_lookup_data`), `:314-361` (`cache_alias_lookup`),
  `:380-710` (literal/suffix/fnmatch lookup, `filter_out_dupes`, `compare_mime_weight`, `cache_glob_lookup_file_name`),
  `:751-807` (`cache_get_mime_type_for_data`), `:937-1046` (`_xdg_mime_cache_mime_type_subclass`);
  `gcontenttype-fdo.c:532-548` (`looks_like_text`), `:567-690` (`g_content_type_guess_impl`); `gcontenttype.c:315-321`.
* Instrument: a scratch harness (`mado-mimesniff` imported through `importlib` — the documented Python API — and the
  oracle as a subprocess with `env -i LC_ALL=C HOME=<root>/h XDG_DATA_HOME=<root>/dh XDG_DATA_DIRS=<root>/s1:<root>/s2`).
  Synthetic caches were built with the candidate's own `build_cache`; realistic caches with
  `update-mime-database <scratch>/dh/mime` on a hand-written `packages/*.xml` (suffix tree, literals, weights,
  case-sensitive globs, nested magic) — the `real` class, run only inside scratch.
* Differential runs: the frozen host list (3528 files × {data-only, own path} = 7056 pairs); 370 random synthetic
  caches × 1–4 inputs; 700 byte-mutated caches (seeds 11/12/13: 300/200/200); a 256-byte single-byte matrix;
  24 targeted magic/priority/name cases; 11 subclass cases; 12 basename shapes; padding/OOB-string cases; unaligned
  child-offset cases; duplicate-dir cases.
* Deep structures: child chains 10 000/20 000/40 000/50 000/60 000/70 000/71 000/72 000/73 000/74 000/75 000/78 000/
  80 000/85 000/90 000/95 000/100 000/100 001/120 000/150 000/200 000; parent chains 100/500/900/950..1000/1100/1500/
  5000/20 000.

**Totals:** 7056 host pairs — 0 differences. 370 random-cache inputs — 0 differences (3 in the first seed were the
VT finding below). 700 mutated caches — 15 differences, all of them the two declared "read past the mapping"
refusals (UB; see residual risk R1), 0 other. 24 + 11 + 12 + 4 + 3 + 1 targeted cases — 0 differences. The
single-byte matrix — exactly 1 difference (0x0b, F1).

## Findings (by severity)

| # | severity | kind | case | GLib answers | c1 answers |
|---|---|---|---|---|---|
| F1 | **high** | wrong answer on a frozen-class input (`lltext`) | `lltext-71-vt` | `application/octet-stream 1` | `text/plain 0` |
| F5 | **high** | refusal where GLib answers (`wrap`) | `wrap-71-sum-gt-len` | `text/plain 0` | UNSUPPORTED (exit 3) |
| F2 | **high** (measurement-conditional) | answers where the oracle crashes (`nest`) | `nest-71-chain75000` | `["UNSUPPORTED",null]` (SIGSEGV) | `app/deep 0` |
| F4 | **high** (deep chain only) | uncaught `RecursionError`, rc 1 (`subclass`) | `subclass-71-parents1500` | `app/p0 0` | traceback, exit 1 |
| F3 | medium | refusal where GLib answers (whole environment, `mode`) | `mode-71-no-database` | `text/plain 0` / `x-zerosize 0` / `inode/directory 1` | exit 3 |
| F6 | high (case file, not the candidate) | poisoned case-level label (`nameN`, `alias`) | `nameN-06-literal-and-glob`, `alias-01-sniff-alias-string` | `app/readme 0` / `text/plain 0` for input 0 | c1 answers input 0 correctly; label is `UNSUPPORTED` |

The five candidate-defect cases (F1, F5, F2, F4, F3) are in `w1/R95MReviewC1-cases.json`, each label re-verified
against the live oracle at write time; F6's two cases are the frozen cases themselves (`nameN-06`, `alias-01`).

### F1 — `looks_like_text` treats 0x0b (VT) as whitespace; GLib does not

* **candidate**: `build/mado-mimesniff.c1.py:207-208`
  `return not any(b < 8 or 14 <= b < 32 or b == 127 for b in data)`
* **GLib**: `gio/gcontenttype-fdo.c:533-548` rejects a byte when `g_ascii_iscntrl(c) && !g_ascii_isspace(c) &&
  c != '\b'`. The installed glib's `g_ascii_table` marks `0x0b` control with **no** space flag (measured with a
  6-line C probe linked to the installed glib: bytes 08..13 = cntrl/space `(1,0)(1,1)(1,1)(1,0)(1,1)(1,1)`):
  ```c
  #include <glib.h>
  #include <stdio.h>
  int main(void) { for (int b = 0; b < 256; b++) { char c = (char)b; int cn = g_ascii_iscntrl(c), sp = g_ascii_isspace(c);
    if (cn) printf("%02x cntrl=%d space=%d reject=%d\n", b, cn, sp, (cn && !sp && c != '\b')); } return 0; }
  ```
  The candidate's own docstring repeats the wrong set ("0x00-0x07, 0x0e-0x1f, 0x7f").
* **effect**: for data that the binary/text fallback (`xdgmimeint.c:176-190`) turns into `UNKNOWN` because of a VT,
  GLib keeps `UNKNOWN` (⇒ `application/octet-stream`, `uncertain=1` for a typeless name) while c1 upgrades to
  `text/plain`, `uncertain=0`. This is a **wrong answer**, not a refusal: it changes both the type and the flag.
* **reproducing case**: `lltext-71-vt` — empty loadable cache in `dh`; inputs `b"ab\x0bcd"`, `b"ab\x0ccd"`,
  `b"ab\x09cd"`; oracle `["application/octet-stream",1]`, `["text/plain",0]`, `["text/plain",0]`; c1
  `("text/plain",0)` for all three.
* **the candidate's own selftest encodes the defect**: check `s10 VT passes looks_like_text`
  (`c1.py:467`) asserts `("text/plain",0)` for `b"ab\x0bcd"`, so `--selftest` is 23/23 green *because* the check is
  wrong. A repair must change s10, and the C2 kill-sets are unaffected (they guard `mado-mimeglob.py`/`mado-portals.py`).
* **frozen cases**: `lltext-02-vt-binary` (3 inputs) and `fallback-02-ctrl-matrix` input 5 fail on c1; both are
  fixed in c1b (04 inputs recovered in my DRAFT comparison).
* **status in c1b**: fixed (`c1b:211` adds `b == 11`, s10 rewritten). I verified c1b answers
  `application/octet-stream 1` for `b"ab\x0bcd"`.

### F5 — the 32-bit wrap check runs before the wrapped comparison: a refusal where the C stops and answers

* **candidate**: `build/mado-mimesniff.c1.py:112-115`
  ```python
  if i + value_length > M32:
      raise Unsupported("matchlet i + value_length passes 2^32 (memcmp past the data)")
  if i + value_length > len(data):
      return False
  ```
* **GLib**: `gio/xdgmime/xdgmimecache.c:167-210`
  `if (i + data_length > len) return FALSE;` — `i` and `data_length` are `xdg_uint32_t`, so the sum wraps mod 2^32
  *before* the comparison with `len` (size_t). When the wrapped value is `> len`, the C returns FALSE without
  reading and the guess falls through to the fallback; the candidate refuses instead.
* **reproducing case**: `wrap-71-sum-gt-len` — one magic entry at priority 60 whose matchlet is
  `range_start=0xFFFFFFF0, range_length=1, value=b"\x40"*32`; data `b"AAAA"` (len 4). C: `0xFFFFFFF0+32` wraps to
  `16 > 4` ⇒ FALSE ⇒ fallback ⇒ `text/plain 0`; c1 raises `Unsupported` (exit 3). With data len 16 or 20 the wrapped
  sum is `<= len`, the C reads `data + 0xFFFFFFF0` and dies (SIGSEGV) — both sides refuse there, which is correct.
* **frozen case**: `wrap-07-vl-m32-at-i1-ub` (label `text/plain 0`) fails on c1 **and on c1b** — see the frozen-run
  section; the required fix is a byte-wise `memcmp` model, not the wrapped-sum arithmetic.
* **status**: this is the L1's own `L1-F1` (`build/l1-findings-r95.md`) and the Critic's C1-F2; I reproduced it
  independently. c1b fixes my case (`wrap-71-sum-gt-len`) but not the frozen one.

### F2 — the nesting cap (100000) is above the C stack limit; c1 answers cases whose oracle label is UNSUPPORTED

* **candidate**: `build/mado-mimesniff.c1.py:88` (`MAX_NEST = 100000`) and `:152-153`
  (`if len(stack) > MAX_NEST: raise Unsupported("… the C recursion overflows")`).
* **GLib**: `gio/xdgmime/xdgmimecache.c:212-239` recurses once per matched child; the C stack (8 MiB, `ulimit -s`)
  overflows far below 100 000. Measured with one magic entry whose matchlets form a chain of `D` levels (each level
  `range_start=0, range_length=1, value=b"\x00"`, the next level as its only child; data `b"\x00"` matches every
  level): **D = 74 000 answers `app/deep 0`, D = 75 000…200 000 SIGSEGV (rc −11)**. (The Critic measured the first
  crash at D = 74 849; my brackets are consistent.)
* **effect**: for `74 849 <= D <= 100 000` the oracle's label is `["UNSUPPORTED",null]` (the schema's crash rule)
  while c1 answers `app/deep 0` — a case the `nest` class can hit.
* **reproducing case**: `nest-71-chain75000` — the 75 000-deep chain (2.4 MiB cache), data `b"\x00"`; oracle
  SIGSEGV ⇒ `["UNSUPPORTED",null]`; c1 `("app/deep",0)`.
* **frozen cases**: the nine frozen `nest` cases use 168-268-byte caches (a few levels), so F2 is not hit by the
  frozen set; it is a latent defect of the stated cap and a risk only for generated cases.
* **caveat**: the crash depth depends on the stack limit, so a frozen deep-chain case has a label that can flip
  between hosts. c1b (`MAX_NEST = 512`, docstring reworded to a declared limit) changes the failure mode to a
  refusal band `[513, 74 848]` where GLib answers; that band needs the declaration's named limit and must not be
  frozen. The robust design is: frozen `nest` cases only at depths the C certainly answers (or the declared band),
  and no frozen case whose label is a stack-dependent crash.

### F4 — the parent-chain walk is Python recursion with no guard: `RecursionError` (exit 1) where GLib answers

* **candidate**: `build/mado-mimesniff.c1.py:232`/`:268` — `subclass()` calls itself once per parent level.
* **GLib**: `gio/xdgmime/xdgmimecache.c:937-1046` recurses too, but with ~64-byte frames; it answers chains far
  beyond Python's limit (verified with the oracle: D = 1000, 1500, 5000, 20 000 all answer `app/p0 0`).
* **effect**: with a legal cache whose parent list is a chain of `D >= ~1000` entries and a sniffed type at
  `g_content_type_guess` returns the name type; c1 raises `RecursionError`, which `main()` does not
  catch (`c1.py:533` catches only `Unsupported`) ⇒ traceback on stderr, **exit 1** — neither the answer nor the
  contract's exit 3.
* **reproducing case**: `subclass-71-parents1500` — parents `app/p0→app/p1→…→app/p1500→app/base`, globs
  `*.x → app/p0` and `*.x → app/zz` (two name types), magic priority 40 `app/base` matching `b"B"`; name `f.x`,
  data `b"B"`; oracle `["app/p0",0]`; c1 `RecursionError: maximum recursion depth exceeded` (CLI rc 1).
  Threshold measured: D ≤ 990 answers, D ≥ 1000 raises (the exact number shifts with the caller's frame depth).
* **repair**: make the walk iterative (an explicit stack with the same seen list), or raise `Unsupported` at a depth
  the declaration names — but note the second option is a refusal where GLib answers for every depth in the band.
* **frozen case**: in a 05:30 read of the frozen file, `subclass-09-deep-chain-1200` was a legal 31 340-byte
  1200-level chain labelled `app/d0000 0` and c1 raised `RecursionError` there (c1b too); the 05:31 revision moved
  that id to a corrupted cache labelled UNSUPPORTED, which both refuse correctly, so the current frozen set no
  longer exercises F4. The defect is unchanged on legal caches — the repair must be iterative before a deep-chain
  case can be frozen.
* **status in c1b** (`37997bdb…`): unchanged — the same `RecursionError` reproduces.

### F3 — an environment with no database at all is refused, although GLib answers it from the pure fallback

* **candidate**: `build/mado-mimesniff.c1.py:278-280`
  ```python
  self.mode = self.resolver.mode
  if self.mode != "cache":
      raise Unsupported("text mode (no loadable mime.cache; GLib reads the magic files)")
  ```
  with `tools/mado-mimeglob.py:545` `self.mode = "cache" if caches else "text"`.
* **GLib**: `gio/xdgmime/xdgmime.c:129-206` reads the text `globs2`/`globs`/`magic`/`aliases`/`subclasses` of a
  directory only when that directory has no loadable `mime.cache`; `xdg_mime_get_mime_type_for_data`
  (`xdgmime.c:516-541`) uses `_xdg_mime_magic_lookup_data` only when `_caches` is NULL and otherwise falls through
  to `_xdg_binary_or_text_fallback` (`xdgmimeint.c:176-190`). When **no** such text file exists either, there is
  nothing for the tool to be unable to read: the answer is exactly the modelled fallback, the empty-data rule
  (`xdgmime.c:523-527`), the name rule and the trailing-slash rule (`gcontenttype-fdo.c:613-620`).
* **effect**: the refusal is broader than its own stated reason. c1 exits 3 for every input of such an environment
  (including `inode/directory` for a name ending in `/`, which needs no database at all), while the oracle answers.
  The counter scores a tool refusal against a real label as `wrong` (`quality/counters/c1-r95-mimesniff.py:283`),
  so a frozen `mode` case with a no-database env is unwinnable.
* **reproducing case**: `mode-71-no-database` — `dh/mime`, `s1/mime`, `s2/mime` contain only a README (no
  `mime.cache`, no `globs2`/`globs`/`magic`); inputs `(NULL, b"hello\n")`, `(NULL, b"")`, `(b"d/", b"x")`,
  `(b"f.txt", b"hello\n")`; oracle `text/plain 0`, `application/x-zerosize 0`, `inode/directory 1`, `text/plain 0`;
  c1 exits 3 on all four.
* **repair direction**: refuse only when a text database file actually exists in a cache-less directory (the tool
  already tracks `texts` in `Resolver.__init__`), and answer otherwise (an empty cache list plus the exact fallback
  gives GLib's answers). If the L1 prefers to keep the broad refusal, it must be a named limit **and** the frozen
  `mode`/`fallback` cases must always contain a loadable `mime.cache`.
* **frozen cases**: six `mode` cases / 7 inputs fail on c1 and on c1b — `mode-01-all-absent` (2 inputs),
  `mode-02-bad-major`, `mode-03-minor-zero`, `mode-05-truncated-39`, `mode-07-garbage-bytes`,
  `mode-08-bad-cache-and-none`; none of them carries a text database file, so the oracle's answers
  (fallback / zerosize / directory) are exactly what the tool models — only the premature exit 3 loses them.
* **status in c1b** (`37997bdb…`): unchanged — the same exit 3 reproduces.

## Verified equal (no finding)

* **Data step** — empty data ⇒ `application/x-zerosize`, priority 100 (`xdgmime.c:523-527`); with caches, the cache
  answer only (`xdgmime.c:529-533`); otherwise `_xdg_binary_or_text_fallback` with `i < 128` and the `{9,10,13}`
  exceptions (`xdgmimeint.c:176-190`); the fallback is reached exactly when `priority <= 0` (strictly-greater
  comparison, `xdgmimecache.c:751-807`), including a first matching entry at priority 0 (cache answers NULL) and
  uint32 priorities with the high bit set (`_s32`: negative never beats 0) — all tested, agree.
* **Magic section** — `OUT_OF_BOUNDS` (alignment + `n > (size-offset)/record`, `xdgmimecache.c:83-84`) applied at
  the same three levels (list/entry/matchlet), with the same `continue`/FALSE semantics (an OOB child list makes
  the matchlet false *before* its value test — verified with `n_children=0, child_offset=1` and `child_offset=size+8`);
  first matching entry in cache order wins, later higher priorities in the same cache are ignored; a cache's answer
  replaces the running one only on strictly greater priority; the zero-filled last page is modelled exactly
  (`Cache.buf` page padding): value/mask bytes in `[size, page_end)` read as 0 on both sides, a string that runs past
  EOF terminates at the padding, a `mimetype_offset` into the padding yields the empty type `"" 0` on both sides;
  `range_start + range_length` wraps mod 2^32 with no loop when it wraps below `range_start`; a mask of all zeros
  matches any data; `word_size` is not read; nested children are OR'd depth-first in index order (order-independent
  result); an OOB child list inside the suffix lookup is refused (the C `continue`s inside an unchanged binary
  search — an infinite loop); unaligned child offsets are rejected as GLib does.
* **Guess** — `g_path_get_basename` on every reachable shape (`""` → `.`, `a/.` → `.`, `a//b` → `b`,
  `a/../f.txt` → `f.txt`, trailing `/` intercepted before the basename), the `n == 1` early return that skips
  sniffing, the trailing-slash `inode/directory` with `uncertain=1` (data ignored), the `n == 0` branch, the
  `n >= 2` branch with `prio >= 80`, the subclass tie-break and the `types[0], uncertain=1` fallback
  (`gcontenttype-fdo.c:613-684`); the desktop override uses `strcmp` (a cache string equal to
  `application/x-desktop` is overridden for any non-NULL name — including the empty name `""` — and only there);
  the `UNKNOWN` **pointer identity** is modelled by `_Const`: a cache magic entry whose type string is
  `application/octet-stream` is *not* `UNKNOWN` (priority 90 ⇒ returned with `uncertain=0`; priority 40 with two
  name types ⇒ the `application/octet-stream` special case in `subclass` fires and the first name type is returned
  with `uncertain=0`) — both tested, agree.
* **Subclass** — unalias of both sides (single-step, first cache wins), equality, `x/*` supertype via
  `xdg_mime_media_type_equal` (`xdgmime.c:781-792`, including `/*` and a mime without `/`), `text/plain`/`text/*`,
  `application/octet-stream`/non-`inode/`, every cache's parent list searched (not only the first holding the type),
  the seen list as pointer identity modelled by `(cache index, parent offset)`, alias cycles and parent cycles
  terminate identically (`xdgmimecache.c:937-1046`, `xdgmime.c:821-831`).
* **Name step as used here** (round 94's `mado-mimeglob.py`, imported from the candidate's own directory) — the
  basename is taken exactly once, the cache glob lookup (lower-case literal pass, original-case literal pass with
  the `0x100` case-sensitive bit, suffix passes, fnmatch passes, `filter_out_dupes` with max-weight merge, the
  stable weight-descending sort, the 10-type cap) matches on every tested name, including the 12-glob cap case,
  equal-weight orders, non-UTF-8 names (`\xff.txt`, `a\x80.TXT`), and literal/suffix/fnmatch type strings that point
  into the zero padding (empty type).
* **Mode selection** — a loadable `mime.cache` in one directory and text files in another: the text files are
  ignored (both), the caches are used in directory order, a cache-less directory with `globs2` is parsed only when
  no cache loads; duplicate directories and the same cache in two directories agree.

## Frozen cases under c1 (DRAFT comparison, case file `cf7cb632…`, 184 cases / 322 inputs)

The frozen `controls/mimesniff-cases-r95.json`
(sha `cf7cb632f05a3aa89e03aabeb49d9879ce688c1775d4c292dc489f6a1c44fc4e`, 05:31) was still being revised while I
reviewed: an earlier read at 05:30 had 320 inputs, and `subclass-09-deep-chain-1200` was then a 31 340-byte legal
deep chain labelled `app/d0000 0` against which c1 raised `RecursionError`; the current read is a corrupted cache
labelled UNSUPPORTED that both c1 and c1b refuse correctly. Against the current file, the live oracle reproduced
every label (322/322, drift 0).

**c1 fails 14 inputs in 11 cases:**

| case (class) | wrong inputs | label | c1 | finding |
|---|---|---|---|---|
| `lltext-02-vt-binary` (`lltext`) | 3 | `application/octet-stream 1` | `text/plain 0` | F1 |
| `fallback-02-ctrl-matrix` (`fallback`) | 1 (input 5) | `application/octet-stream 1` | `text/plain 0` | F1 |
| `wrap-07-vl-m32-at-i1-ub` (`wrap`) | 1 | `text/plain 0` | UNSUPPORTED | F5 |
| `nameN-06-literal-and-glob` (`nameN`) | 1 (input 0) | `["UNSUPPORTED",null]` | `app/readme 0` | F6 |
| `alias-01-sniff-alias-string` (`alias`) | 1 (input 0) | `["UNSUPPORTED",null]` | `text/plain 0` | F6 |
| `mode-01-all-absent` (`mode`) | 2 | `text/plain 0`, `application/octet-stream 1` | exit 3 | F3 |
| `mode-02-bad-major` (`mode`) | 1 | `text/plain 0` | exit 3 | F3 |
| `mode-03-minor-zero` (`mode`) | 1 | `text/plain 0` | exit 3 | F3 |
| `mode-05-truncated-39` (`mode`) | 1 | `text/plain 0` | exit 3 | F3 |
| `mode-07-garbage-bytes` (`mode`) | 1 | `text/plain 0` | exit 3 | F3 |
| `mode-08-bad-cache-and-none` (`mode`) | 1 | `text/plain 0` | exit 3 | F3 |

The six `mode` cases that fail carry **no text database file at all** (`mode-01` has no files; the others only a
bad/truncated/garbage `mime.cache`), so this is F3 — a refusal where GLib answers from the pure fallback — not the
declared "text mode reads magic files" case. The frozen `nest` cases are shallow (168-268-byte caches); F2 is not hit
by them. F4 is not hit by the current file (its deep-chain case was replaced; see F4).

The same comparison with c1b (`37997bdb…`, 05:22) leaves **10 inputs in 9 cases** wrong: the six `mode` cases (7
inputs), `nameN-06`, `alias-01`, and — despite its wrap rewrite — `wrap-07-vl-m32-at-i1-ub`. That last frozen case
shows why the wrapped-sum arithmetic alone is not the right test: `start=1, range_length=1, value_length=0xFFFFFFFF`,
value `b"Z"`, data `b"AY"` ⇒ at `i=1` the C's `memcmp(cache+46, data+1, 0xFFFFFFFF)` stops at the **first differing
byte** (`Z` vs `Y`) and returns FALSE — nothing is read past the caller's buffer, the guess falls through to
`text/plain 0`. A faithful model compares byte by byte, stops at the first difference (`memcmp` semantics), and
refuses only when it actually reaches a read past the cache mapping or past the caller's buffer
(`g_file_get_contents` guarantees one NUL byte at `data[len]`, so `i+j == len` reads 0 and `i+j > len` is the UB
point).

### F6 — two frozen cases are unwinnable for a faithful per-input tool (case-file defect, not the candidate)

`nameN-06-literal-and-glob` and `alias-01-sniff-alias-string` each carry two inputs; the case's oracle run is one
process over both, and the **second** input makes it SIGSEGV (`nameN-06`: name `READMEX`; `alias-01`: name `x.new`).
`quality/counters/c1-r95-mimesniff.py` `oracle_label_case` (`:194-200`) runs every input of the case in one oracle
invocation and, on a crash, returns `None` for all of them, so the **answerable first input also gets the
`["UNSUPPORTED",null]` label** — although, run alone, the oracle answers it: `nameN-06` input 0 (name `README`,
data `text\n`) → `app/readme 0`; `alias-01` input 0 (name NULL, data `T`) → `text/plain 0` (both re-run per input by
me). A tool that answers the first input exactly as GLib does is then scored wrong ("the tool answered an
UNSUPPORTED input", `c1-r95-mimesniff.py:283`). The case schema's crash rule (*a case whose oracle run crashes is
labelled UNSUPPORTED and the tool must exit 3 on it*) is what produces this, and the executor applied it as written.
Fix before freezing: split each case so a crashing input sits alone in its own case (or drop the crashing input),
otherwise at most 320 of 322 inputs are winnable and C1's (i) cannot reach the full case count. This is not a
candidate defect; it caps the achievable score regardless of the tool.

## Residual risk and verification gaps

* **R1 — UB reads past the mapping.** c1 refuses with "cache read past the mapping"/"cache string runs past the
  mapping"; GLib reads adjacent mapped memory. Example: a cache padded to exactly 4096 bytes with a matchlet
  `value_offset=4096` and data `b"\x00"` — the oracle answers `application/octet-stream 1` (the byte after the
  mapping happened to be readable), c1 refuses. The declaration refuses C UB, so this is out of contract, but the
  frozen `bounds` cases must keep every value/mask/string read inside the last page; the L1's own probe
  (`build/l1-findings-r95.md`) reached the same conclusion. 700 byte-mutated caches produced 15 such disagreements
  and nothing else.
* **R2 — the `nest` boundary is stack-dependent.** The oracle's crash depth moves with `ulimit -s`; a frozen case
  above ~74 800 is a label that can flip between the recording host and the measurement host. c1b's `MAX_NEST = 512`
  avoids answering a crashing case but creates a refusal band `[513, 74 848]` where GLib answers — that band needs
  the named limit, not a frozen case.
* **R3 — F3 vs the counter's scoring.** `score_case` marks a tool refusal against a real label `wrong`
  (`c1-r95-mimesniff.py:283`), so a frozen `mode` case without a loadable cache loses regardless of the declaration.
* **R4 — F4 needs no frozen case to be real**: any cache with a parent chain of ≥ ~1000 entries (legal, ~130 KB at
  5000) makes the tool exit 1. The counter will see a crash, not a refusal; `main()` catching only `Unsupported`
  means the traceback is the whole output.
* **R5 — frozen-case state.** `controls/mimesniff-cases-r95.json` appeared at 05:28 and was still being revised at
  05:31 (`cf7cb632f05a3aa89e03aabeb49d9879ce688c1775d4c292dc489f6a1c44fc4e`, 184 cases / 322 inputs); it may change
  again. My DRAFT comparison is against that revision; every frozen label was reproduced by the live oracle. The
  file is not a measurement and the counter was not run.
* **R6 — out of contract by declaration, not reviewed further**: text mode with real `magic` files (the tool cannot
  parse `xdgmimemagic.c`); arbitrary-name NUL bytes are unmeasurable through the oracle's argv, so no case uses them.

## Overlap with other seats (corroboration, not a claim on their work)

* The Critic (`w1/R95MCritic.md`, C1-F3) independently measured the nesting-cap defect (first crash D = 74 849) and
  recommends a 512 cap + named limit; the L1's `build/l1-findings-r95.md` records the wrap-order defect as L1-F1;
  `w1/R95MScribeEntry-case-vt.json` and the Probe's `g-vt-minimal` carry the VT input. I reproduced all three
  independently before reading those files; F3 and F4 are not in them.
* c1b state I observed (`37997bdb…`, 05:22): F1, F2 and F5 repaired; **F3 and F4 still present** (verified by
  running c1b against `mode-71-no-database` and `subclass-71-parents1500`).

## Commands run (all DRAFT)

| command | result / exit |
|---|---|
| `python3 -I harness.py` (candidate `--selftest`, via module) | `MADO_MIMESNIFF_SELFTEST: checks=23 failed=0`, rc 0 |
| `python3 -I cases1.py` (24 targeted magic/priority/name cases) | `diffs: 0`, rc 0 |
| `python3 -I fuzz.py 1 120` (random synthetic caches) | 3 diffs, all VT (F1), rc 0 |
| `python3 -I fuzz.py 2 250` (random synthetic caches, VT byte withdrawn from the data alphabet) | `bad 0`, rc 0 |
| single-byte matrix, 256 inputs, empty cache | 1 diff: `0x0b` oracle `[application/octet-stream,1]` vs tool `[text/plain,0]` |
| `cc -O0 -o asciiprobe … $(pkg-config --cflags --libs glib-2.0)`; `./asciiprobe` | `0b cntrl=1 space=0`; 09/0a/0c/0d/20 space=1 |
| `python3 -I hostcheck.py 3528` (frozen host list, data-only + own path) | `checked pairs 7056 diffs 0`, rc 0 |
| `python3 -I nest.py 74000 75000 …` | 74 000 `app/deep 0`; 75 000+ `CRASH rc=-11`; tool answers to 100 000, refuses 120 000+ |
| parent chains 100…20 000 | oracle answers `app/p0 0` at 1000/1500/5000/20 000; tool answers ≤990, `RecursionError` ≥1000 |
| `python3 -I mutfuzz.py 11 300` / `12 200` / `13 200` | 6/5/4 disagreements, every one `cache read/string runs past the mapping` (R1) |
| CLI checks (`--json`, plain, `--selftest`, text mode, missing file) | rc 0/0/0/3/2 as documented; traceback path rc 1 for F4 |
| `python3 -I make_cases.py` | 5 cases written, every label `labels-match` against the live oracle |
| `python3 -I frozen_run.py` (DRAFT, frozen case file `cf7cb632…`) | 322 inputs, live oracle = all 322 labels; c1 wrong on 14 inputs / 11 cases; c1b (`37997bdb…`) wrong on 10 inputs / 9 cases |

## Artefacts

* `w1/R95MReviewC1.md` — this report.
* `w1/R95MReviewC1-cases.json` — the five reproducing cases in the shared CASE FILE SCHEMA
  (`version 1`, `oracle_src_sha256 = 99df35f8…`, `glib2 = 2.90.1-1`; classes `lltext`, `wrap`, `nest`, `subclass`,
  `mode`; ids `lltext-71-vt`, `wrap-71-sum-gt-len`, `nest-71-chain75000`, `subclass-71-parents1500`,
  `mode-71-no-database`). 3.25 MB (the 75 000-deep chain is 2.4 MB of cache), every label oracle-verified.
* Scratch `$HYAKU_SCRATCH/mado-r95/R95MReviewC1` (oracle, harness, probes) was deleted after the runs; anything
  cited above is either in the case file, in the lane's frozen controls, or reproducible from the commands listed.
* No installs, no upgrades, no service or host-database changes; `update-mime-database` ran only on
  `<scratch>/real/dh/mime`.
