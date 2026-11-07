source: S515 (GLib 2.90.1 gio/xdgmime/xdgmimeglob.c sha256 38ed8623…0734), S516 (gio/xdgmime/xdgmimecache.c ccda4366…db69), S517 (shared-mime-info spec 0.21, ar01s02.html, raw HTML sha256 e00fa00e…c61e in four L1 fetches, two at round start and two re-fetched after the scribe seat reported a different digest), S518 (gio/gcontenttype-fdo.c 8a5b4f47…2d7c) and the held S505 (gio/xdgmime/xdgmime.c afb1c1c1…2410 for the directory list and the cache/text mode switch); digests and located lines in `.ufo/waves/round-94/receipts/sources-open-r94.txt`. S505 is the round-91 row, re-opened (same digest) this round.
covers: what GLib 2.90.1 `g_content_type_guess (name, NULL, 0, &uncertain)` answers for a file **name** — the xdgmime data-directory list, cache vs text mode, the literal / simple-suffix / full-glob lookup in both modes, ASCII folding and the `cs` flag, deepest-suffix selection and its per-cache scope, weight merge and sort, the cache weight encoding, and how the guess turns 0/1/many matches into (type, uncertain)
verified-at: 2026-11-07 — `tools/mado-mimeglob.py` (sha256 65f80a6c…2453) against the oracle `.ufo/waves/round-94/controls/mimeglob-oracle-r94.c` (sha256 9c4337b3…6b11, gcc -O1 against glib2 2.90.1-1): the C1 measurement `.ufo/waves/round-94/receipts/c1-measured-r94.txt` (370 frozen cases, fresh and host legs); the `e…` rows of §7 were drafted by the scribe seat on the wave candidate (98/101, 3 refusals) and re-run by the L1 on the landed bytes, 101/101 (`.ufo/waves/round-94/receipts/entry-rows-c1b-r94.txt`)
recheck: 90d — re-pull xdgmimeglob.c, xdgmimecache.c, xdgmime.c and gcontenttype-fdo.c at the next GLib tag that changes any of them (the 2.90.1 tag is the pin); also when `glib2` leaves 2.90.1-1 or `shared-mime-info` leaves 2.5.1-2, and when `update-mime-database` changes its cache writer.

# File name → MIME type: what GLib 2.90.1 guesses from the name alone

This entry states the answer GLib 2.90.1 gives to `g_content_type_guess (filename, NULL, 0,
&uncertain)` — the type and the uncertain flag — from the shared-mime-info databases. It is the step
that precedes `corpus/knowledge/mime-default-resolution-r91.md`: rounds 91–92 resolve *type →
application*; this one resolves *name → type*. Line numbers are those of the files named in the
front matter (`xdgmimeglob.c`, `xdgmimecache.c`, `xdgmime.c`, `gcontenttype-fdo.c`); the spec is the
shared-mime-info 0.21 page `ar01s02.html` (S517). Every behavioural statement carries either a source
line or a DRAFT oracle row (`e…` ids, table in §7); statements carrying neither are marked
**[UNVERIFIED]**.

## 1. Question and scope

- **The call.** `g_content_type_guess_impl` (S518:568) takes `filename`, `data`, `data_size` and
  `result_uncertain`. With `data = NULL` the sniffing block (:620-638) is skipped and the answer is
  the name lookup alone. Its result is one type string plus a boolean.
- **C locale.** GLib never calls `setlocale` in this path; the oracle does not either, so `fnmatch(3)`
  runs byte-wise in the `"C"` locale. The tool sets `LC_ALL=C` explicitly (candidate, `main`). A
  program that has called `setlocale` itself gets *its* locale's `fnmatch` (§3 D6, §6).
- **Databases.** The directory list is xdgmime's own `getenv`-based list (S505:217-300), the same one
  the r91 entry §7 describes for aliases and parents — not GLib's desktop-file directory list.
- **Out of scope.** Content sniffing (`data != NULL`, which can override or break a tie,
  S518:620-690); aliases and parent types (the guess returns the glob's type verbatim, never
  unaliased); the application step (r91) and `xdg-mime`/`xdg-open` (r92 — whose `open_generic` file
  path asks `xdg-mime query filetype FILE`, xdg-open.in:486, a different type source: that path runs
  `file`-style detection, not this glob lookup).
- **One name, one component.** Only the last path component is looked up (`g_path_get_basename`,
  S518:607; row `e16`: `dir.txt/f.c` → `text/x-c`), and a filename ending in `/` never reaches the
  lookup at all (§2.5).
- **Evidence class.** The 101 names in §7 were run on 40 fixture databases built in this seat's
  scratch (`$HYAKU_SCRATCH/mado-r94/R94MScribeEntry`, removed on exit; the driver and its output are
  copied into `.ufo/waves/round-94/w1/`). They are DRAFT: nothing here is frozen and nothing here is
  a measurement.

## 2. The rules

### 2.1 The directory list (dirs)

`xdg_init_dirs` (S505:217-300) builds one list, in this order, and nothing else is searched:

1. `$XDG_DATA_HOME + "/mime/"` when `XDG_DATA_HOME` is set — **even when it is empty**, which yields
   the literal `"/mime/"` (:244-254). **[UNVERIFIED]** by run: creating `/mime` needs root; the row
   `e8c` only shows that an empty `XDG_DATA_HOME` contributes no *existing* directory.
2. otherwise, when `$HOME` is set, `$HOME + "/.local/share/mime/"` (:256-263); when neither variable is
   set, no first directory is added at all.
3. every non-empty element of `$XDG_DATA_DIRS` + `"/mime/"` (:266-298); an unset variable means
   `"/usr/local/share/:/usr/share/"` (:228-229), a set-but-empty one contributes **no** system
   directory (the empty piece is skipped at :279-284). Row `e8b`: `XDG_DATA_DIRS=""` with a globs2
   in `s1` answers `application/octet-stream, uncertain 1`.
4. Config directories take no part, and `XDG_DATA_HOME` set means `$HOME` is not consulted either.

Rows: `e8`, `e8b`, `e8c`, `e8d`, `e8e` (an empty element `:s1:` is skipped).

### 2.2 Mode: cache or text, decided per directory but switched globally

`xdg_mime_init_from_directory` (S505:129-211), per directory, in this order (located lines 137,160):

1. `stat ("<dir>/mime.cache")`; if it exists and `_xdg_mime_cache_new_from_file` returns a cache, the
   directory is a **cache directory**, its `globs2`/`globs` are not read, and the function returns
   (`:136-152`, `return FALSE`).
2. otherwise `stat ("<dir>/globs2")` → read it as *version two* (`weight:type:glob[:flags]`); if absent
   `stat ("<dir>/globs")` → read it as version one (`type:glob`, weight fixed at 50) (`:155-176`).
3. `magic`, `aliases`, `subclasses`, `icons`, `generic-icons` are read too (`:180-211`) — `packages/`
   is **never** read (that is `update-mime-database`'s input, not the lookup's).

A cache loads only when the file is at least 40 bytes and its version is 1.1–1.2 (S516:127,
`_xdg_mime_cache_new_from_file`; macros `MAJOR_VERSION 1`, `MINOR_VERSION_MIN 1`, `MAX 2`, :60-62).
Rows `e14` (39-byte cache → the same directory's globs2 is used) and `e15` (major 2 → globs2).

The **switch is global and all-or-nothing**: `xdg_mime_get_mime_types_from_file_name` returns the
cache answer whenever *any* directory produced a cache (S505:639-651, `if (_caches) return
_xdg_mime_cache_get_mime_types_from_file_name (…)`, located lines 645-646). Text globs already read
from other directories are then dead data.

Rows: `e5` (a user `globs2` beside a system cache is invisible), `e19` (a directory's own `globs2` is
shadowed by its own cache).

### 2.3 Text lookup

`_xdg_glob_hash_lookup_file_name` (S515:420-500) runs four phases in this order.

1. **Literals** (:440-460): `strcmp (list->data, file_name)` over every literal in read order; the
   first equality returns **one** type (`:442`). Then, for literals not flagged `cs`,
   `strcmp (list->data, lower_case)` — note the *stored* bytes on the left and the **lowered name**
   on the right (:452-459). So an all-lowercase literal matches any case, a mixed-case literal
   matches only itself. Rows `e1` (`Makefile` → `text/x-make`, `MAKEFILE` → octet-stream) and `e32`
   (`makefile` → `text/x-make`, `Makefile` → the other type); the host's `/usr/share/mime/globs2:432`
   stores `50:text/x-makefile:makefile`, i.e. the generated form is lowercase.
2. **Simple suffixes** (:463-467, located lines 463, 465-467): a reversed-suffix trie over the glob
   minus its leading `*` (:582). One descent, so **only the deepest match** of the name is returned: a
   shorter (shallower) suffix that also matches never appears. First pass on the ASCII-lowercased name
   with `cs` globs excluded, then — only if fewer than two types — a second pass on the original name
   with `cs` globs included. The second pass re-finds a non-`cs` entry the first pass already found,
   which is how a single type reaches the count 2 and stops the next phase (row `e11`: `x.y` with
   `*.y` and `x?y` → `a/suffix`, **certain**).
3. **Full globs** (:469-480, located line 473): `fnmatch (list->data, file_name, 0)` — the *unfolded*
   name only, no `FNM_CASEFOLD` — over every full glob, only when fewer than two types so far.
4. **Merge and sort** (`filter_out_dupes` :392-417): two entries of the same type keep the larger
   weight, with the swap-from-the-end order of the C loop; then `qsort` by weight descending
   (:485) and truncation to 10 (:428). Equal weights keep the order the C library's sort leaves —
   on this glibc the merge sort is stable (row `e18`: two directories' `*.q` → first directory's type,
   uncertain; row `e21`: the same type twice → one answer, certain).

Glob classification (`_xdg_glob_determine_type`, :537-560): `literal` unless the pattern contains
`\`, `[`, `?` or `*`; `simple` when the only special byte is a single `*` **at position 0** (:547-550,
`:555`); everything else `full`. A `*` anywhere else, e.g. `*.tar.*`, is full.

Reading the file (`_xdg_mime_glob_read_from_file`, :628-720): `fgets (line, 255, glob_file)` (:643),
so a line longer than 254 bytes is split into two lines and neither keeps the intended pattern (row
`e31`: a 300-byte suffix never matches); a first byte `#` or NUL skips the line; the weight is
`atoi`; in version two the flags field starts after the second colon and ends at the next colon, and
`cs` counts only at the field start or after a comma and only when followed by a comma or the end
(:690-706). Pairs are appended in read order; a repeated `(suffix, type)` pair adds nothing to the
trie (the insert scans the character-0 children for the same type, :236-271), and a repeated literal
only duplicates a list entry that the first-hit rule already answers identically.

### 2.4 Cache lookup

`cache_glob_lookup_file_name` (S516:669-730, located lines 701, 709) has the same four phases with
two structural differences.

1. **Literals** (:701-703): a **folded pass** (`lower_case`, `case_sensitive_check = FALSE`) and then
   an exact pass (`case_sensitive_check = TRUE`). A hit on a `cs` entry during the folded pass ends
   the whole literal search with 0 (:414-424), skipping later caches too — row `e23`: a first cache
   with a `cs` literal `makefile` and a second with a non-`cs` literal `Makefile` answers
   `MAKEFILE` → `application/octet-stream, uncertain 1`. Because `update-mime-database` lowercases
   literal patterns (it wrote `makefile` for `<glob pattern="Makefile">`; row `e6`), literal matches
   are case-insensitive in cache mode in practice.
2. **Suffixes** (:701-704, `cache_glob_lookup_suffix` :574-616): each cache walks its own tree and
   contributes **its own deepest match**; the loop runs over every cache in directory order. So one
   name can carry several types in cache mode where text mode carries one (row `e6`: `*.gz` in one
   cache and `*.tar.gz` in another → `c/two`, **uncertain 1**; the same two globs as text → row
   `e6b`, `c/two`, certain).
3. **Full globs** (:706-712): the folded pass runs **only when the suffix count is 0**, the
   exact-name pass when it is below 2 — so a name whose only suffix match is a `cs` glob gets the
   exact-name `fnmatch` pass but never the folded one.
4. Weight in a cache is `weight & 0xff` and bit `0x100` is the `cs` flag (:414-415, :468-469,
   :555-556): a hand-made cache weight 300 sorts as 44 (row `e12`: `low/two` before `high/one`,
   uncertain). Merge, sort and the 10-type cap are the same code shape as text (:675, :715).

Structural bounds checks (`OUT_OF_BOUNDS`) skip a list or continue rather than crash; the candidate
reproduces them and refuses (exit 3) only where the C loop would not terminate.

### 2.5 The guess

`g_content_type_guess_impl` (S518:568-690, located lines 597, 603, 613, 620, 675, 683):

| name state | answer | uncertain | source |
|---|---|---|---|
| filename ends `/` | `inode/directory`, no lookup at all | 1 | :594-604 |
| 1 matching type | that type | 0 | :614-620 |
| 0 matching types | `application/octet-stream` | 1 | :641-650 |
| ≥2 matching types | the first in weight order | 1 | :675-683 |

At most 10 types are collected (`name_mimetypes[10]`, :574; the call passes 10, :608). The table is
verified by rows `e16` (`Makefile/`, `a.txt/`, `/` → directory; `""` → octet-stream), `e1`/`e6`
(single type certain), `e1` `zz`/`e17` (no match → octet-stream), `e1` `x.dup` and `e18` `x.q`
(several → first, uncertain).

## 3. Where GLib departs from the spec (S517)

The spec's §2 says: "Applications MUST match globs case-insensitively, except when the case-sensitive
attribute is set to true"; "If several patterns of the same weight match then the longest pattern
SHOULD be used. In particular, files with multiple extensions (such as `Data.tar.gz`) MUST match the
longest sequence of extensions"; "The glob-deleteall element … SHOULD discard information from
previous directories, is written out into the globs2 file using `__NOGLOBS__` as the pattern"; and its
RECOMMENDED order is "start by doing a glob match of the filename. Keep only globs with the biggest
weight. If the patterns are different, keep only globs with the longest pattern".

| # | GLib | spec | row |
|---|---|---|---|
| D1 | the suffix phase returns **only the deepest match** of the name and never sees a shallower one, so weight cannot reorder suffixes: a weight-10 `*.a.b.c` beats a weight-90 `*.c` | filter by weight first, then by pattern length | `e2` (`app/deep`, certain) |
| D2 | in cache mode **each cache** contributes its own deepest suffix, so the union of caches can hold two types | one match over the merged database | `e6` (`c/two`, uncertain) vs `e6b` (`c/two`, certain) |
| D3 | lower-weight matches are **not discarded**: up to 10 are collected and sorted, so a lower-weight type survives as *uncertainty* | keep only the biggest weight | `e1` `x.dup` (60 vs 40 → `app/hi`, uncertain) |
| D4 | `__NOGLOBS__` is **not implemented**: none of the four files contains the string; the text reader appends it as an ordinary literal glob named `__NOGLOBS__`, so nothing is deleted | deleteall discards earlier directories' globs | `e4` (an earlier dir's `*.patch` still matches; a file literally named `__NOGLOBS__` matches `text/x-diff`) |
| D5 | folding is **ASCII only** (`ascii_tolower`, S515:377-390; xdgmimeint.c:107-114 `_xdg_ucs4_to_lower` is not on this path), and the lookup compares **bytes**: a multi-byte suffix can never match | case-insensitive matching | `e17` (`x.é` with `*.é` → octet-stream) |
| D6 | full globs are **case-sensitive in text mode** (`fnmatch` on the unfolded name, :473) and **case-insensitive in cache mode** (folded pass first, :706-709) | case-insensitive unless `cs` | `e3` (`XZY` no match) vs `e6` (`zzXq` matches), `e26` (`X.C` no match) vs `e26b` (matches) |
| D7 | weights are not preserved into a cache: 8 bits, with `0x100` taken for `cs` | a numeric weight | `e12` (300 reads as 44) |
| D8 | a literal is compared as *stored* against the lowered name, so a mixed-case literal is case-sensitive in text mode; the cache builder's lowercasing hides this in cache mode | case-insensitive literals | `e1`/`e32` vs `e6` |
| D9 | a trailing `/` short-circuits to `inode/directory` **before** any glob, even when a literal matches the component | not a globbing rule | `e16` (`Makefile/` → directory, not `text/x-make`) |

`glob-deleteall` still takes effect when `update-mime-database` regenerates the database: it drops
the glob from the generated `globs2`/`mime.cache` (row `e25`: a package with `<glob-deleteall/>` and
`*.diff` answers `a.patch` → octet-stream), but it does **not** remove another directory's globs in
either mode (row `e24`, cache mode: `a.patch` → `dl/x` from the other cache).

### 3.1 Cache mode and text mode disagree

The same packages give different answers with and without `mime.cache` (R94MProbeC1: 117 of 9521
answers over 56 layouts built with `update-mime-database` 2.5.1, nine mechanisms; each has a frozen
cache/text pair, the `pb-` cases of `.ufo/waves/round-94/controls/mimeglob-cases-r94-frozen.json`):

| # | mechanism | text mode | cache mode |
|---|---|---|---|
| M1 | full globs and case | `fnmatch` on the name as given (S515:473) | folded pass first (S516:706-707), so `FOO.C` meets the builder-lowercased `*.[ch]` |
| M2 | literal order | exact literals first, then folded non-`cs` (S515:440-459) | folded first, then exact (S516:686-694) |
| M3 | a `:` inside a pattern | cut at the flags separator by the globs2 reader (S515:680-692) | kept whole in the binary cache |
| M4 | lines over 254 bytes | split by `fgets (…, 255)` (S515:643) | written whole by the builder |
| M5 | weights over 255 or below 0 | `atoi` value kept | `weight & 0xff` (S516:415) |
| M6 | two directories | one merged trie, one deepest match | one deepest match per cache, then merged by weight |
| M7 | deepest suffix | across all directories | per cache (S516:583-611) |
| M8 | a missing or invalid cache | the directory falls back to its globs2 | any other valid cache switches every lookup to caches (S505:645-646) |
| M9 | a `cs` literal hit on the folded pass | not special | ends the literal search, later caches included (S516:424) |

A database edited by hand and never rebuilt therefore answers differently from the same database
after `update-mime-database`; the tool reads whichever form GLib reads.

### 3.2 Bytes the decoder does not validate

`_xdg_utf8_validate` returns TRUE without looking (xdgmimeint.c:92-96), and `_xdg_utf8_to_ucs4`
reads a lone continuation byte or 0xFE/0xFF as a signed `char` widened to 32 bits — the same value
the suffix lookup gives the name's byte (S515:319). So `*.\x80` and `*.\xff` match a name ending in
that one byte, while a well-formed multi-byte character (`*.é`) never matches; and a lead byte
swallows the next one when the pattern is classified (`*.\xc3[` is a simple glob, not a full one).
Frozen cases `bytes-04`, `l1-bytes-01`…`03`.

## 4. Operator consequences

1. **A hand-written package is not a database.** The lookup reads only
   `mime/{mime.cache,globs2,globs,magic,aliases,subclasses,icons,generic-icons}` (S505:129-211).
   `~/.local/share/mime/packages/*.xml` without a following `update-mime-database
   ~/.local/share/mime` changes nothing.
2. **A cache kills the text files beside it, and the mode is global.** A `globs2` in a directory that
   holds a loadable `mime.cache` is never read (row `e19`), and so is a `globs2` in *any* directory once
   some other directory has a cache (row `e5`). On this host both `~/.local/share/mime/mime.cache` and
   `~/.local/share/mime/globs2` exist and the tool reports `mode=cache` with 3 directories (DRAFT,
   §7), so **the user's `globs2` is dead**: a stale `mime.cache` *is* the user database.
3. **A capitalised extension works only as far as the glob's flags and class say.** `*.txt`, `*.pdf`
   (no `cs`) match `NOTES.TXT`, `REPORT.PDF` (rows `e1`, `e28`); a `cs` glob such as the C/C++ pair
   `*.c:cs` / `*.C:cs` makes the extension case-*sensitive* (`FILE.ZIP` with `*.zip:cs` → no match,
   row `e28`); and a full glob (`*.[ch]`, `x?y`) is case-sensitive in text mode but not in cache mode
   (D6).
4. **On this host `.png` is already ambiguous.** Both `image/png` and `image/apng` carry `*.png`, so
   GLib answers `image/png` with `uncertain = 1` for `image.png` and `IMAGE.PNG` alike (DRAFT tool
   `types` array, §7). A caller that respects the flag treats every PNG as a guess. A two-type glob
   is visible in both modes (row `e1` `x.dup`, text; row `e6`, cache) — the ambiguity is in the
   database, not in the reader.
5. **`__NOGLOBS__` deletes nothing** (D4): a `glob-deleteall` copied between databases, or a
   hand-edited `globs2` line, leaves the other directories' globs in force. If a fix is meant to
   *remove* a pattern for GLib, the database must be regenerated with `update-mime-database` and the
   removal must be inside one database's build, not across directories (row `e24`).
6. **A broken cache file silently downgrades one directory to text mode** (rows `e14`, `e15`) — and if
   no other directory has a cache, the whole answer changes mode.

## 5. The tool and how to run it

`tools/mado-mimeglob.py` (the frozen candidate `.ufo/waves/round-94/build/mado-mimeglob.c1b.py`,
sha256 `65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453`; the wave candidate `…c1.py`
`0700915a…d63e` was revised by the L1 after R94MReviewC1 F1–F7) is read-only: it opens
only `mime.cache`, `globs2` and `globs` under the searched roots, writes nothing, and `--selftest`
uses a temporary directory.

```sh
python3 -I tools/mado-mimeglob.py notes.txt IMAGE.PNG archive.tar.gz
python3 -I tools/mado-mimeglob.py --json --data-home <root>/dh --data-dirs '<root>/s1:<root>/s2' --home <root>/h a.txt
python3 -I tools/mado-mimeglob.py --json --data-home-unset --data-dirs-unset README
python3 -I tools/mado-mimeglob.py --selftest
```

Output (exit 0): a header `MADO_MIMEGLOB_DIRS: mode=text|cache dirs=…`, then one line per name,
`MADO_MIMEGLOB: <type> uncertain=<0|1> name=<escaped>`; `--json` prints
`{"mode", "dirs", "results": [{"name", "type", "uncertain", "types"}]}`, where `types` is the
pre-guess list (the same list the guess picked from). Exit 2 is a setup error (no name);
exit 3 is `UNSUPPORTED` with one reason line — a refusal, never an answer. `--selftest` printed
`MADO_MIMEGLOB_SELFTEST: checks=19 failed=0` (rc 0) on this host.

## 6. Limits and unknowns

1. **Sniffing is out of scope.** Real callers pass `data`; a sniffed type at priority ≥ 80 replaces the
   name answer, and a lower-priority sniff only breaks a tie (S518:620-690). This entry and the tool
   model the `data = NULL` answer only.
2. **`fnmatch` is the C library's.** Full globs go through `fnmatch(3)`; GLib does not set the locale,
   so an application that called `setlocale` itself sees different full-glob matching than the `"C"`
   rows here. Nothing outside `"C"` was verified.
3. **`HOME` unset with `XDG_DATA_HOME` unset.** The C code adds no first directory (S505:244-263) and
   the tool adds none (`--home-unset`; frozen cases `l1-dirs-01`, `l1-dirs-02`). An empty `HOME` is
   concatenated, giving the absolute `/.local/share/mime/` (R94MReviewC1 F1: the wave candidate
   path-joined it and read a directory relative to the caller's working directory).
4. **A bare `*` glob is inert.** GLib inserts a root node whose character is 0 and reads past the
   array (S515:582, undefined); observed: it never matches (row `e27`, `rv-simple-02/03`). The tool
   skips the line. The wave candidate refused it (exit 3).
5. **Refusals** (exit 3) are kept only where the C code has no defined answer: a glob that ends inside
   a multi-byte sequence (the decoder reads past the string), a weight outside ±2^30, a cache suffix
   node that fails the bounds check (the C lookup never returns), and a cache string that runs past
   the zero-filled last page of the mapping. A globs2 line that is not UTF-8 is read as bytes, as GLib
   does (§3.2; row `e30`).
6. **Hand-made cache invariants are reproduced, not checked.** The literal list must be sorted by
   `strcmp`; if it is not, the binary search misses and the tool misses with it (row `e29`: `aaa`
   unfound, `bbb` found). Agreement with GLib is not agreement with intent.
7. **Weights above 255 and the `cs` bit are format-level** (D7); `update-mime-database` never writes
   them, so only a hand-made cache shows the truncation.
8. **The `e…` rows are not the frozen set.** They are the scribe seat's scratch databases; the frozen
   set and its measurement are `.ufo/waves/round-94/controls/mimeglob-cases-r94-frozen.json` and
   `.ufo/waves/round-94/receipts/c1-measured-r94.txt`.
9. **Uncovered:** `magic` and sniffing; aliases and parent types (not consulted by a guess); more than
   10 matching types; non-`C` locales; names containing NUL (a CLI cannot carry one); databases
   written by anything other than `update-mime-database`; and a `data_size` of
   `(gsize) -1` (rejected by `g_return_val_if_fail`, S518:589).

## 7. Reproducing the labels

The oracle is `.ufo/waves/round-94/controls/mimeglob-oracle-r94.c` (sha256 `9c4337b3…6b11`),
compiled and run in this seat's scratch:

```sh
S=$HYAKU_SCRATCH/mado-r94/R94MScribeEntry
gcc -O1 -o "$S/oracle" .ufo/waves/round-94/controls/mimeglob-oracle-r94.c $(pkg-config --cflags --libs gio-2.0)
env -i LC_ALL=C HOME=<root>/h XDG_DATA_HOME=<root>/dh XDG_DATA_DIRS=<root>/s1:<root>/s2 "$S/oracle" a.txt X.TAR.GZ
```

The driver `.ufo/waves/round-94/w1/R94MScribeEntry-probe.py` (kept with its output
`…/w1/R94MScribeEntry-rows.txt`) builds each root from files written by the case (`globs2`, `globs`,
hand-made `mime.cache`) or by `update-mime-database` on a package XML, then runs the oracle and the
candidate on the same names with the same environment. 101 rows over 40 databases: on the wave
candidate 98 agree and 3 are refusals (`e27`, `e30` twice); on the landed tool 101 agree
(`.ufo/waves/round-94/receipts/entry-rows-c1b-r94.txt`, `ROWS=101 DIFFS=0`).

Selected rows (mode, name → oracle type, oracle uncertain / tool type, tool uncertain):

| case | mode | state | name | oracle | tool |
|---|---|---|---|---|---|
| `e1` | text | `*.txt` non-cs | `a.txt` / `A.TXT` | `text/plain` 0 / `text/plain` 0 | same |
| `e1` | text | `*.c:cs` + `*.C:cs` | `x.c` / `x.C` | `text/x-c` 0 / `text/x-c++` 0 | same |
| `e1` | text | literal `Makefile` | `Makefile` / `MAKEFILE` | `text/x-make` 0 / octet-stream 1 | same |
| `e1` | text | `*.tar.gz` + `*.gz` | `x.tar.gz` | `app/x-tgz` 0 | same |
| `e1` | text | two types, weights 60/40 | `x.dup` | `app/hi` 1 | same |
| `e1` | text | full glob `x?y` | `xzy` / `XZY` | `app/full` 0 / octet-stream 1 | same |
| `e1` | text | equal weights, two types | `f.two` | `t/one` 1 | same |
| `e1` | text | trailing slash | `d/` | `inode/directory` 1 | same |
| `e2` | text | `10:*.a.b.c` vs `90:*.c` | `x.a.b.c` | `app/deep` 0 | same |
| `e4` | text | `__NOGLOBS__` in a later dir | `a.patch` | `text/x-diff` 0 | same |
| `e5` | cache | user globs2, system cache | `a.sys` | `sys/one` 0 | same |
| `e6` | cache | two caches, `*.gz` and `*.tar.gz` | `x.tar.gz` | `c/two` 1 | same |
| `e6b` | text | same two globs, one trie | `x.tar.gz` | `c/two` 0 | same |
| `e6` | cache | literal lowercased by the builder | `MAKEFILE` | `c/three` 0 | same |
| `e11` | text | `*.y` + `x?y` | `x.y` | `a/suffix` 0 | same |
| `e12` | cache | fabricated weights 300 vs 50 | `x.big` | `low/two` 1 | same |
| `e16` | text | basename / empty name | `dir.txt/f.c` / `""` | `text/x-c` 0 / octet-stream 1 | same |
| `e17` | text | `*.é` | `x.é` | octet-stream 1 | same |
| `e19` | cache | own globs2 beside own cache | `a.gg` | octet-stream 1 | same |
| `e23` | cache | cs literal stops the folded search | `MAKEFILE` | octet-stream 1 | same |
| `e24` | cache | deleteall in one dir, glob in another | `a.patch` | `dl/x` 0 | same |
| `e25` | cache | deleteall inside one build | `a.patch` | octet-stream 1 | same |
| `e26` | text | `*.[ch]` | `X.C` | octet-stream 1 | same |
| `e26b` | cache | `*.[ch]` | `X.C` | `src/c` 0 | same |
| `e28` | text | `*.zip:cs` / `*.pdf` | `FILE.ZIP` / `REPORT.PDF` | octet-stream 1 / `app/pdf` 0 | same |
| `e29` | cache | unsorted literal list | `aaa` / `bbb` | octet-stream 1 / `t/b` 0 | same |
| `e31` | text | 300-byte glob line, `fgets` split | `a.zzz…` | octet-stream 1 | same |
| `e27` | text | bare `*` glob | `x` | octet-stream 1 | same (the wave candidate: `UNSUPPORTED`) |
| `e30` | text | invalid UTF-8 glob line | `a.ok` | `text/ok` 0 | same (the wave candidate: `UNSUPPORTED`) |

Host check (DRAFT; synthetic names only, no name of any real file was read): with the session's
`HOME`/`XDG_DATA_HOME`/`XDG_DATA_DIRS`, the tool reports `mode=cache`, 3 directories, and the oracle
and the tool agree on `notes.txt` → `text/plain` 0, `IMAGE.PNG` → `image/png` **1**,
`archive.tar.gz` → `application/x-compressed-tar` 0, `README` → `text/x-readme` 0,
`x.mado-r94-probe` → `application/octet-stream` 1.
