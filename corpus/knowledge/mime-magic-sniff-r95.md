source: S519 (GLib 2.90.1 gio/xdgmime/xdgmimecache.c sha256 ccda4366…db69 — the magic section, the data entry and the subclass walk), S520 (gio/xdgmime/xdgmimeint.c c2364aa8…2f29 — the binary/text fallback), S521 (gio/gcontenttype-fdo.c 8a5b4f47…2d7c — the guess given data, looks_like_text, the desktop rule; gio/gcontenttype.c fb9c6878…4664 for the public entry), S522 (gio/glocalfileinfo.c b006a93d…4497 — the GIO caller that sniffs), S523 (shared-mime-info spec 0.21 at its moved locator, ar01s02.html e00fa00e…c61e), S505 (xdgmime.c afb1c1c1…2410, re-opened: for_data and the per-directory text files), S511/S512 (glib/gstrfuncs.c and .h, the ASCII table); every file fetched twice by the L1 `MadoR95` with HTTP 200 and identical digests (`.ufo/waves/round-95/receipts/sources-open-r95.txt`, including its append-only correction: the spec's registered S517 locator now answers 301 and the 1566c459… body is the redirect stub, as R95MScribeEntry also found)
covers: what GLib 2.90.1 `g_content_type_guess (name-or-NULL, data, len, &uncertain)` answers when it is **given bytes** — the name-step short-circuits, empty data, the magic section of each `mime.cache` (entry order, cross-cache priority, matchlet range/mask/word/children, bounds checks), the binary/text fallback and `looks_like_text` including the VT byte, the desktop rule, and the 0/1/several name-type resolution through `_xdg_mime_cache_mime_type_subclass`; who on this host calls it with bytes (GIO's `standard::content-type`)
verified-at: 2026-11-07 — `tools/mado-mimesniff.py` (the frozen candidate `.ufo/waves/round-95/build/mado-mimesniff.c1c.py`) against the oracle `.ufo/waves/round-95/controls/mimesniff-oracle-r95.c` (sha256 99df35f8…124a, against glib2 2.90.1-1): the C1 measurement `.ufo/waves/round-95/receipts/c1-measured-r95.txt` (frozen cases, fresh cases from a measurement-time seed, the host file list data-only and with names). The DRAFT rows of §7 are the scribe seat's (R95MScribeEntry) and stay labelled DRAFT.
recheck: 90d — re-pull xdgmimeint.c, xdgmimecache.c, xdgmime.c and gcontenttype-fdo.c at the next GLib tag that changes any of them (the 2.90.1 tag is the pin); also when `glib2` leaves 2.90.1-1 or `shared-mime-info` leaves 2.5.1-2 (the host database's contents are part of every host answer), and when `update-mime-database` changes its cache writer.

# File bytes → MIME type: what GLib 2.90.1 guesses from data

This entry states the answer GLib 2.90.1 gives to `g_content_type_guess (filename-or-NULL, data,
len, &uncertain)` — the type and the uncertain flag — from the shared-mime-info databases, when
the call is given bytes. Its predecessor `corpus/knowledge/mime-glob-guess-r94.md` answers the same
call with `data = NULL`; that entry's §2 is the name step this one cites and does not restate.
Line numbers are those of the files named in the front matter (`gcontenttype-fdo.c`,
`gcontenttype.c`, `xdgmime.c`, `xdgmimecache.c`, `xdgmimeint.c`, `gstrfuncs.c`, `gstrfuncs.h`);
the spec is the shared-mime-info 0.21 page `ar01s02.html` (S523). Every behavioural statement
carries either a source line or a DRAFT row of §7; statements carrying neither are marked
**[UNVERIFIED]**.

## 1. Question and scope

- **The entry point.** `g_content_type_guess` (S521 `gcontenttype.c`:315-320) is a one-line call to
  `g_content_type_guess_impl` (`gcontenttype-fdo.c`:568).
- **Two guards come first.** `data_size == (gsize) -1` is refused and answers
  `application/octet-stream` with `uncertain` left FALSE (`gcontenttype-fdo.c`:589); both `data` and
  `data_size` are then only used under `if (data)` (`:622`).
- **Data is the second step, not the first.** The name lookup runs first (`:594-611`), and a single
  name type returns at `:613-620` without the bytes ever being read. §2.6 is the whole arbitration.
- **The bytes are read only through the database's magic section.** In cache mode the path is
  `xdg_mime_get_mime_type_for_data` (S505 `xdgmime.c`:516-541) → `_xdg_mime_cache_get_mime_type_for_data`
  → `cache_get_mime_type_for_data` (S519 `xdgmimecache.c`:751-807). The text `magic` files
  (`xdgmimemagic.c`) are the other mode and out of scope here (§6).
- **Data as passed.** GLib has no sniff-length policy of its own in this function: it is given
  `data_size` and reads exactly that. A caller that sniffs 4096 bytes gets an answer for those 4096
  bytes; the 128-byte window of §2.4 is inside GLib, not the caller's.
- **Who passes bytes on this host (QUALITY 154).** GIO's local file info (`g_file_query_info`,
  attribute `standard::content-type`) guesses from the basename first and sniffs only when that
  answer is uncertain: S522 `glocalfileinfo.c`:1337 `content_type = g_content_type_guess (basename,
  NULL, 0, &result_uncertain);`, `:1340` `if (!fast && result_uncertain && path != NULL)`, then reads
  up to `_g_unix_content_type_get_sniff_len ()` bytes (`:1351`; the caches' largest magic extent,
  clamped to the 16384-byte buffer at `:1345`, `:1352-1353`) and calls `g_content_type_guess
  (basename, sniff_buffer, res, NULL)` (`:1373`). `standard::fast-content-type` never sniffs. So
  `gio info`, GTK file choosers and other GIO users reach this entry's rules only for a name with zero
  or several types. `xdg-open` on Hyprland does **not**: xdg-utils 1.2.1 falls to `info_generic`,
  which runs `file --brief --dereference --mime-type` (libmagic, not `mime.cache`) — the r92 entry's
  §1 and R95MConnector §2.4 (`/usr/bin/xdg-mime` `info_generic`, `mimetype` absent on this host).
- **Out of scope.** The name step's own rules (r94 entry); text mode (refused when a text database
  file exists, §6); aliases/parents as data structures (they are consulted only inside the subclass
  test, §2.6); the application step (r91/r92); a caller's choice of bytes.
- **Evidence class.** §2-§4 carry source lines and rows; the claim's measurement is the frozen case
  set (`.ufo/waves/round-95/controls/mimesniff-cases-r95-frozen.json`); the rows of §7 are the scribe
  seat's DRAFT fixtures, kept because they read well, not as the measurement.

## 2. The rules

### 2.1 Databases and mode

The directory list and the cache/text switch are the ones the r94 entry's §2.1-2.2 describes
(S505 `xdgmime.c`:217-300, per-directory cache probe at `:129-211`); this tool reuses round 94's
resolver unchanged. One consequence specific to data: **any** loadable cache switches the whole
process to cache mode, so a `magic` text file in a directory whose own `mime.cache` is invalid is
never read while another directory holds a valid cache (S505:645-646). With **no** loadable cache, a
directory's `globs2`/`globs`/`magic`/`aliases`/`subclasses` are read as text (S505 `xdgmime.c`:157-204);
when none of those files exists anywhere, GLib's tables are empty and every answer is the fallback,
the empty-data rule or the trailing slash — which the tool answers (frozen `mode` cases with absent,
truncated, garbage or wrong-version caches). On this host the tool reports `mode=cache` with the
user's 288-byte `~/.local/share/mime/mime.cache` (no magic entries; one `*.uproject` glob,
R95MProbeC1 §a) and `/usr/share/mime/mime.cache`.

### 2.2 Empty data

`xdg_mime_get_mime_type_for_data` answers an **empty** buffer before anything else:

| state | answer | prio | source |
|---|---|---|---|
| `len == 0` (and `data != NULL`) | `application/x-zerosize` | 100 | S505:523-527 `if (len == 0) { … *result_prio = 100; return XDG_MIME_TYPE_EMPTY;` |
| `data == NULL` | nothing is sniffed (`:622` `if (data)`) | 0 | S521:622; DRAFT `nil` control |

Because the empty answer is inside the *data* function, it is reached only when the name step did
not already answer: one name type wins over empty data (row `n-one-empty` → `t/single` 0), while
zero or several name types get `application/x-zerosize` 0 (rows `f-empty`, `n-two-empty`). With
`data == NULL` and no name type the answer is `application/octet-stream` **1**, not zerosize (a
20-line control passing `NULL, 0` printed `application/octet-stream 1`, `application/octet-stream 1`,
`text/plain 0` for names NULL, `zz`, `x.txt`).

### 2.3 Magic, per cache

#### 2.3.1 The two structures

The cache's magic list is `N_MATCHES, MAX_EXTENT, FIRST_MATCH_OFFSET` (spec §2.9) and GLib reads
`n_entries` at `+0` and the entry offset at `+8` (S519:296-297) — **`MAX_EXTENT` is never read**.
An entry is 16 bytes: `PRIORITY`, `MIME_TYPE_OFFSET`, `N_MATCHLETS`, `FIRST_MATCHLET_OFFSET`
(S519:252-255). A matchlet is 32 bytes: `RANGE_START(+0)`, `RANGE_LENGTH(+4)`, **`WORD_SIZE(+8)`**,
`VALUE_LENGTH(+12)`, `VALUE_OFFSET(+16)`, `MASK_OFFSET(+20)`, `N_CHILDREN(+24)`,
`FIRST_CHILD_OFFSET(+28)` (S519:173-177, `:218-219`). GLib reads +0, +4, +12, +16, +20, +24, +28:
**`WORD_SIZE` is never read** (spec §2.9 defines it, §2.5 defines its byte-swapping) — the value is
compared byte for byte (D2).

#### 2.3.2 Which entry wins

1. Within one cache: the **first** entry, in list order, that has a holding matchlet wins; the loop
   returns on the first hit (S519:301-308 `match = cache_magic_compare_to_data (…); if (match) return match;`).
   Priorities of later entries in the same cache are never consulted (row `m-order`: priority 30
   listed before 95 → `app/lo`).
2. Within one entry: the first of its matchlets that holds; `prio` is set to the entry's priority
   (S519:262-270). An entry whose matchlet list fails `OUT_OF_BOUNDS` returns NULL and the cache
   moves on to the next entry (S519:257-258).
3. Across caches: the answer replaces the running one only on a **strictly greater** priority
   (S519:773-774 `match = cache_magic_lookup_data (cache, data, len, &prio); if (prio > priority)`),
   so the first of two equal priorities wins (rows `m-caches`: 90 then 95 → `app/b95`; 60 then 60 →
   `a60`).
4. `priority` starts at 0 (S519:290 `*prio = 0;`, `:761`) and the answer is used only under
   `if (priority > 0)` (S519:784): a matching entry whose priority is 0 is **discarded** and the
   fallback of §2.4 decides (row `m-prio0` → `text/plain` 0).
5. `priority` is an `int` holding the uint32 (`S519:252`, `759`): 2^31 and up become negative and can
   never beat 0 (row `m-negative` → `text/plain` 0).

#### 2.3.3 How a matchlet holds

- The value is tried at every offset `i` in `[range_start, range_start + range_length)`; all four
  fields are `xdg_uint32_t` (S519:173-174), so a range that wraps in 32-bit arithmetic stops early
  rather than running long (S519:181).
- If `i + data_length > len` the matchlet is **FALSE immediately** — a short buffer never matches
  a longer value and the later offsets of the range are not tried (S519:185-186; rows `m-short`:
  `ABC` against a 4-byte value → fallback `text/plain`, and `X` against a matchlet at offset 200 →
  `text/plain`).
- With a mask (`MASK_OFFSET != 0`) every byte compares as `(value & mask) == (data & mask)`; without
  one, `memcmp` (S519:188-202). Row `m-mask` (`\x10\x00` under mask `\xf0\x00` → `\x1f\x99` matches).
- `WORD_SIZE` is not read, so a word-size 2 or 4 rule is still a raw byte comparison against the
  value stored in the cache. On this host 8 of 1282 matchlets carry 2 or 4, and synthesised data
  holding their stored bytes at their stored offsets matched them through the oracle (rows
  `word2-application/x-cpio`, `word4-application/vnd.tcpdump.pcap`,
  `word4-application/x-java-jce-keystore`).
- Children: after the value holds, `N_CHILDREN == 0` is TRUE; otherwise **any** child that holds
  makes the matchlet TRUE (S519:225-235). A child list failing `OUT_OF_BOUNDS(child_offset,
  n_children, 32, cache->size)` makes the matchlet FALSE **before** its own value is tested
  (S519:220-221). Rows `m-nest`: `NE\x01\x01Y` → `app/nest`, `NE\x01\x01Z` → fallback.
- Children are evaluated by recursion, depth-first, in list order; the first holding child ends it
  (S519:230-235).

#### 2.3.4 The bounds macro

`OUT_OF_BOUNDS(offset, n, record_size, max)` is
`((offset) & 0x3) || (offset) > (max) || (n) > ((max) - (offset)) / (record_size)`
(S519:83-84): an unaligned offset, an offset past the mapping, or a count that cannot fit is
treated as a bad list. The magic list itself is checked as `OUT_OF_BOUNDS (list_offset, 1, 12, …)`
and its entry array as `OUT_OF_BOUNDS (offset, n_entries, 16, …)` (S519:293-299) — both return
NULL, i.e. "no magic answer from this cache". The **value** and **mask** reads inside a matchlet
take no bounds check at all (`cache->buffer[data_offset + j]`, `:192`): a hand-made cache can read
past the mapping, which is undefined and which the tool refuses (§5).

#### 2.3.5 A branch this path never takes

`cache_get_mime_type_for_data` can pick the glob result a sniffed type inherits from
(S519:787-791), but the guess path calls it with no glob results
(`_xdg_mime_cache_get_mime_type_for_data`, S519:810-814, passes `NULL, 0`), so `n == 0` and the
sniffed type is returned as is (S519:792-795 at `:794`). The glob/sniff tie-break of the spec
(§2.12) is therefore implemented in `gcontenttype-fdo.c` only (§2.6, D4).

### 2.4 The fallback and `looks_like_text`

When no magic answered, `xdg_mime_get_mime_type_for_data` returns
`_xdg_binary_or_text_fallback(data, len)` (S505:540), which scans **the first 128 bytes**:

> `if (chardata[i] < 32 && chardata[i] != 9 && chardata[i] != 10 && chardata[i] != 13)
> return XDG_MIME_TYPE_UNKNOWN; /* binary data */` — S520 `xdgmimeint.c`:185-186 (22 words)

and otherwise `return XDG_MIME_TYPE_TEXTPLAIN;` (`:189`). That value is the **address** of a
constant (S505:56 `const char xdg_mime_type_unknown[] = "application/octet-stream";`), and
`gcontenttype-fdo.c` compares it by pointer, so a magic entry that literally names
`application/octet-stream` is a real type, not the sentinel (row `m-unknown-literal`: certain 0,
where the fallback would have been uncertain 1).

If the fallback returned the sentinel, `looks_like_text` is consulted over **the whole buffer**:

> `if (g_ascii_iscntrl (c) && !g_ascii_isspace (c) && c != '\b')` — S521 `gcontenttype-fdo.c`:542-544 (10 words)

with `return TRUE` after the loop (`:547`), and a TRUE turns the sentinel into `text/plain`
(S521:625-628). `g_ascii_iscntrl` and `g_ascii_isspace` are bit tests on one 256-entry table
(S512 `gstrfuncs.h`:67-68, `:85-86`; `G_ASCII_CNTRL = 1 << 2`, `G_ASCII_SPACE = 1 << 8`, `:48`,
`:54`). The table's row for bytes 8-15 is `0x004, 0x104, 0x104, 0x004, 0x104, 0x104, 0x004, 0x004`
(S511 `gstrfuncs.c`:264), i.e. **BS, VT, 0x0e, 0x0f are control and not space; TAB, LF, FF, CR are
both**. So VT (0x0b) is *not* `g_ascii_isspace` — unlike C's `isspace`.

The two windows disagree, and the answer is binary exactly when both fire:

| byte in the buffer | fallback (`:128` window) | `looks_like_text` (whole buffer) | answer, no magic |
|---|---|---|---|
| `0x00`-`0x07` | UNKNOWN | FALSE | `application/octet-stream` 1 |
| `0x08` | UNKNOWN | TRUE (the `'\b'` exemption) | `text/plain` 0 |
| `0x09`, `0x0a`, `0x0d` | skipped | TRUE | `text/plain` 0 |
| **`0x0b` (VT)** | **UNKNOWN** | **FALSE** (control, not space) | **`application/octet-stream` 1** |
| `0x0c` (FF) | UNKNOWN | TRUE (is space) | `text/plain` 0 |
| `0x0e`-`0x1f` | UNKNOWN | FALSE | `application/octet-stream` 1 |
| `0x7f` alone | TEXTPLAIN (not < 32) | not reached | `text/plain` 0 |
| `0x7f` beside a `0x01` | UNKNOWN (the `0x01`, not the `0x7f`) | FALSE | `application/octet-stream` 1 |
| `>= 0x80` | skipped | TRUE | `text/plain` 0 |

Rows `f-nul`, `f-bs`, `f-tab`, `f-vt`, `f-ff`, `f-us`, `f-del`, `f-soh`, `f-high`, `f-vt-early`.
The 128-byte window also hides a control byte beyond it: `a*130 + "\x0b"` and `a*130 + "\x00"`
are `text/plain` 0 (rows `f-vt130`, `f-nul130`) while `a*127 + "\x01"` is
`application/octet-stream` 1 (row `f-127`) — the spec's own "first 128 bytes" note (§2.12) is thus
implemented as a window, not as a whole-file property (D3).

### 2.5 The desktop rule

After the sniff (and after the text/plain promotion), a **sniffed** `application/x-desktop` becomes
`text/plain` whenever a name was given, whatever its extension:

> `if (filename != NULL && strcmp (sniffed_mimetype, "application/x-desktop") == 0)
> sniffed_mimetype = "text/plain";` — S521:636-638 (13 words)

The comparison is `strcmp`, not the pointer test, so a magic entry naming the type is caught; the
rule is skipped when `filename == NULL`. It is reached only when the sniff runs at all — zero name
types or several (§2.6). Rows `m-desktop`, a cache with the desktop magic and no globs: NULL name →
`application/x-desktop` 0; names `zz.nomatch` and `zz.desktop` → `text/plain` 0. On this host the
same content answers `application/x-desktop` **0** for the names `x.desktop` and `whatever.desktop`
(one name type, `*.desktop` → `application/x-desktop`, short-circuited at S521:613-620) and
`text/plain` 0 for `zz.nomatch` — so the shield does **not** apply to a `.desktop`-named file: the
name step has already typed it. The rule is GLib's, not the spec's (D5).

### 2.6 The guess: 0, 1 or several name types

`name_mimetypes[10]` is filled by the name step (S521:607-608, r94 entry; at most 10 types). Then:

| name types | bytes | answer | uncertain | source / row |
|---|---|---|---|---|
| name ends `/` | any | `inode/directory` | 1 | S521:597-603; `n-dir` |
| exactly 1 | **not read** | that type | 0 | S521:613-620; `n-one`, `n-one-empty`, `n-one-beats-hi` |
| 0 | magic hit, priority > 0 | the sniffed type | 0 | S519:784-795; `m-prio90`, `n-two-zero-name` |
| 0 | fallback | §2.4 table | 1 iff the sentinel | S521:641-647; `f-*` |
| ≥2 | sniffed, `prio >= 80` | the sniffed type | 0 | S521:652-655; `n-two-hi` |
| ≥2 | sniffed, `prio < 80`, some name type is a subclass | that name type | 0 | S521:661-671; `m-prio79-sub`, `n-textplain-sub` |
| ≥2 | sniffed, `prio < 80`, no subclass | the **first** name type | 1 | S521:675-682; `m-prio79-name`, `n-two-bin` |

`prio >= 80` is GLib's own threshold, not the spec's (`:654` `if (sniffed_prio >= 80) /* High
priority sniffing match, use that */`); it is tested before any subclass question, so an unrelated
high-priority sniff replaces a two-type name answer (D4).

The subclass test is `_xdg_mime_cache_mime_type_subclass` (S519:937-1046), unaliasing both sides
first through the cache alias list (S519:948-949, `cache_alias_lookup` at `:315-361`):

1. equal after unaliasing → true (S519:951-952);
2. `base` is `x/*` and the media types are equal → true (S519:957-961, `xdg_mime_media_type_equal`
   is a prefix compare, S505:781-792);
3. `base == text/plain` and `mime` starts `text/` → true (S519:965-967) — row `n-textplain-sub`:
   two `text/x-*` name types against a 60-priority `text/plain` sniff → `text/x-a` 0;
4. `base == application/octet-stream` and `mime` does not start `inode/` → true (S519:969-971);
5. else every cache's parent list, over **every** cache (not only the one holding the type), depth
   first, with a cycle guard on the parent pointer (`for (k = 0; (*seen)[k] != NULL; k++) if
   (parent == (*seen)[k]) goto next_parent;`, S519:1019-1022). Rows `m-prio79-sub`
   (`app/child → app/mid → app/base`) and `m-prio79-sub-alias` (the alias `text/x-old` of
   `text/x-new`, resolved then made a subclass of `text/plain` by rule 3).

`result_uncertain` is FALSE unless one of the three explicit sets (`:602-603` directory, `:643-645`
sentinel with no name type, `:681-682` first of several) fired; a magic or fallback answer under no
name type is certain, including the `application/octet-stream` sentinel promoted by nothing (row
`f-soh` is uncertain 1 because the sentinel survived).

## 3. Where GLib departs from the spec (S523)

The spec's §2.12 fixes the order and the vocabulary: glob first, magic only on conflict or failure;
"use the default type of application/octet-stream for binary data, or text/plain for textual data";
"If any of the mimetypes resulting from a glob match is equal to or a subclass of the result from
the magic sniffing" (23 words) that name type is the result; "Otherwise use the result of the glob
match that has the highest weight." §2.5 says "Higher priority entries come first" and "The word
size is used for byte-swapping"; §2.9 gives the cache layout including `WORD_SIZE`.

| # | GLib | spec | row |
|---|---|---|---|
| D1 | an **empty** buffer is `application/x-zerosize`, certain, priority 100 — a type neither §2.12 nor the cache layout mentions | binary/text only; an empty file has no control byte, so it is textual → `text/plain` | `f-empty` |
| D2 | `WORD_SIZE` is **never read**: cache magic compares stored bytes raw; 8 of 1282 host matchlets carry 2 or 4 | word-size byte-swaps the value on little-endian hosts (§2.5, §2.9) | `word2-*`, `word4-*` |
| D3 | the text/binary decision is a **128-byte window** feeding a whole-buffer second test, and the two disagree about VT: `0x0b` anywhere in the first 128 bytes is binary, `0x0b` at 130 is text | "Checking the first 128 bytes … for ASCII control characters is a good way to guess" (§2.12) — no second window, and C `isspace` counts VT | `f-vt`, `f-vt130`, `f-vt-early` |
| D4 | a sniffed type with priority **≥ 80** wins outright, with no subclass test; below 80 the first subclass name type wins; otherwise the first name type, uncertain | any glob result that is a subclass of the sniffed type wins, else the highest-weight glob — no priority threshold | `n-two-hi` vs `m-prio79-name` |
| D5 | a sniffed `application/x-desktop` is rewritten to `text/plain` whenever a name is given | no such rule; the sniffed type stands | `m-desktop` |
| D6 | within one cache the **first matching entry in list order** wins and priority is only compared **between** caches | "Higher priority entries come first" is a file-order convention the reader is expected to honour; the cache carries no sorting requirement | `m-order` |
| D7 | a priority-0 match is discarded (`if (priority > 0)`), and priorities ≥ 2^31 read as negative so they can never win | priority default 50, maximum 100 (§2.2); 0 is not discussed | `m-prio0`, `m-negative` |
| D8 | the sentinel comparisons are **pointer** comparisons, so a magic entry naming `application/octet-stream` yields that type with `uncertain = 0` | a type name is a type name; the spec has no sentinel | `m-unknown-literal` |
| D9 | `looks_like_text` exempts `'\b'` — a buffer with only `0x08` is text | control characters make data binary | `f-bs` |
| D10 | with `data == NULL` and `len == 0` the answer is `application/octet-stream` 1, not zerosize (the zerosize branch lives inside the data function) | silent; the API's `data`/`data_size` pairing is GLib's own | `nil` control |

`MAGIC_DELETEALL`/`__NOMAGIC__` (spec §2.5) is not implemented by the cache reader at all; it is
applied by `update-mime-database` when it regenerates a database, so a hand-made cache can only
obey it by omission.

## 4. Operator consequences

1. **A renamed file does not sniff.** One name type short-circuits before the bytes are read
   (S521:613-620): `notes.txt` holding a PDF header answers `text/plain` **0**, `x.pdf` holding a
   PNG header answers `application/pdf` **0** (rows `notes.txt`/`x.pdf` in §7). Only a name with
   0 or ≥2 types reaches the magic section.
2. **A two-type extension hands the answer to the threshold.** `x.png` is two types on this host
   (`image/png`, `image/apng`, r94 §4.4), so data decides: PDF bytes → `image/png` **1** (no
   subclass, priority below 80), PNG bytes → `image/png` **0** (rows `x.png` twice).
3. **VT is the one byte where "control" and "space" part company.** `0x0b` in the first 128 bytes
   makes a file binary, while `0x0c` and `0x08` do not; 1152 of the L1's 3620 sampled `/usr` files
   contain `0x0b` somewhere in the first 4096 bytes, but none of them inside the first 128 without
   another binary byte, which is why a host sample of that size cannot show the rule (§7).
4. **Empty files are a GLib type.** `application/x-zerosize` 0 comes from the data function, so it
   also beats a two-type name (row `n-two-empty`) — but not a one-type name (row `n-one-empty`).
5. **The magic answer is only as good as the cache.** On this host the magic section has 689 entries
   / 1282 matchlets, priorities 5…90 with 43 entries at ≥ 80; a rebuilt database (`update-mime-database`)
   can reorder entries, and D6 makes list order part of the answer.
6. **Desktop files are shielded only when the name does not already type them.**
   `application/x-desktop` is rewritten to `text/plain` for any filename that reaches the sniff
   (row `m-desktop`, `zz.nomatch`), but a name that is one name type never reaches it: on this host
   `x.desktop` and `whatever.desktop` answer `application/x-desktop` **0**. The shield is a security
   choice for the *untyped-name* case (S521:630-635), not a detection rule.

## 5. The tool and how to run it

`tools/mado-mimesniff.py` (= the frozen candidate `.ufo/waves/round-95/build/mado-mimesniff.c1c.py`; its
sha256 is the C1 pin in `.ufo/waves/round-95/claims-declaration-r95.md`) is read-only: it opens
only `mime.cache` under the searched roots, writes nothing, and loads round 94's
`tools/mado-mimeglob.py` (`65f80a6c…2453`) **from its own directory** for the name step, so the two
files must sit side by side. It runs under the C1 counter's audit-hook launcher (no open outside
the case and Python, no spawn but ctypes' `ldconfig` libc lookup, no dlopen but libc).

```sh
python3 -I tools/mado-mimesniff.py --json notes.txt                       # name NULL, bytes sniffed
python3 -I tools/mado-mimesniff.py --json --name x.png notes.txt          # one name for every FILE
python3 -I tools/mado-mimesniff.py --json --names-from-files a.txt b.pdf  # each path as its own name
python3 -I tools/mado-mimesniff.py --json --data-home <root>/dh --data-dirs '<root>/s1:<root>/s2' \
        --home <root>/h a.bin                                             # synthetic database
python3 -I tools/mado-mimesniff.py --json --data-home-unset --data-dirs-unset --home-unset a.bin
python3 -I tools/mado-mimesniff.py --selftest                             # checks=26 failed=0, rc 0
```

Output (exit 0): `--json` prints `{"mode","dirs","results":[{"file","name","type","uncertain",
"sniffed","prio","types"}]}`; without `--json`, a header `MADO_MIMESNIFF_DIRS: mode=… dirs=…` and
one `MADO_MIMESNIFF: <type> uncertain=<0|1> name=<escaped|-> file=<escaped>` per file. `types` is
the name step's list (empty when the name is NULL), `sniffed` the data function's type, `prio` its
priority (0 when nothing matched).

**Verdict map.** The answer is the pair `(type, uncertain)`, nothing else:

| GLib outcome | tool exit | tool line |
|---|---|---|
| answered | 0 | `type` + `uncertain` equal to the oracle's `<type>\t<0|1>` |
| no FILE, `--name` with `--names-from-files`, unreadable FILE | 2 | `mado-mimesniff: setup error: …` on stderr |
| a cache-less directory holds `globs2`/`globs`/`magic`/`aliases`/`subclasses` (text mode); a cache read past the mapping; a compare that reads at a data index >= len (the 32-bit sum wrapped to <= len); a matchlet child chain or a parent chain deeper than 4096 (declared limit) | 3 | `MADO_MIMESNIFF: UNSUPPORTED <reason>` |

An exit-3 run is a **refusal**, never an answer: an input whose oracle run crashes or hangs is
labelled `["UNSUPPORTED", null]` and only exit 3 satisfies it; a frozen case marked
`expect_refusal` (text mode, the two depth limits) requires exit 3 although GLib answers it — that is
the declared limit, scored as such. `prio`/`sniffed`/`types` are diagnostics; a frozen case compares
`(type, uncertain)` only. `--selftest` prints `MADO_MIMESNIFF_SELFTEST: checks=26 failed=0` (rc 0).

## 6. Limits and unknowns

1. **Cache mode, or no database at all.** With no loadable `mime.cache` and a text database file in
   some directory, GLib reads the text files (`xdgmimemagic.c` for `magic`, not modelled); the tool
   refuses (exit 3). With no database file anywhere it answers. The host is cache mode.
2. **Data as passed.** GLib reads exactly `data_size` bytes; a caller's sniff length (4096 in the
   counter, `g_content_type_guess` callers in general) is the caller's choice and is not modelled.
   The tool reads the whole file it is given.
3. **`fnmatch`-free but locale-bearing at the name step only.** The data path uses no locale; the
   name step's full-glob matching does (r94 entry §6.2), and the tool sets `LC_ALL=C`.
4. **Undefined C is refused, not reproduced** (exit 3): a cache read past the zero-filled last page
   of the mapping, and a compare that reaches a data index >= len — possible only when
   `i + value_length` wraps (S519:185); a wrapped compare that meets a differing byte first answers
   as GLib does (`memcmp` stops there; frozen case `wrap-l1-firstdiff`). **Declared limits:** a
   matchlet chain or a parent chain deeper than 4096 levels is refused; GLib's recursion overflows an
   8 MiB stack near 74849 matchlet levels and between 60000 and 100000 parent levels (L1 and
   R95MCritic bisections), a depth that moves with the stack size, so no cap can equal it.
5. **Priorities and word sizes are format-level.** `update-mime-database` never writes a priority
   above 100 or a word size other than 1/2/4, so D2/D6/D7 need a hand-made cache (or the shipped
   `word_size` 2/4 matchlets of §2.3.3, which do appear on this host).
6. **The subclass test is byte-based** and uses the caches' alias/parent lists only; a parent
   relationship present only in a text `subclasses` file of a cache-mode database is invisible, as
   GLib's own cache reader is.
7. **Uncovered:** text mode; `magic-deleteall`; more than 10 name types (the C array holds 10);
   `data_size == (gsize) -1` (refused at S521:589 — the tool always passes the file's size);
   non-`C` locales; a caller that passes `data = NULL` with a nonzero `data_size` (the C would read
   it; the tool cannot express it).
8. **The rows of §7 are not the frozen set.** They are the scribe seat's scratch fixtures; the frozen
   cases and their measurement are `mimesniff-cases-r95-frozen.json` and `c1-measured-r95.txt`.

## 7. Reproducing the labels

Three DRAFT drivers, kept with their outputs in `.ufo/waves/round-95/w1/` as
`R95MScribeEntry-drv.py` / `-drv.out.txt`, `R95MScribeEntry-host.py` / `-host.out.txt`,
`R95MScribeEntry-name.py` / `-name.out.txt`; in the scratch they were named `drv.py`, `host.py`,
`name.py`. The copies are evidence: run them from a **copy in a scratch directory**, because
`drv.py` materialises `fx/` and the two host drivers `hostdata*/` beside themselves.

```sh
S=$HYAKU_SCRATCH/mado-r95/R95MScribeEntry
cc -O0 -o "$S/oracle" .ufo/waves/round-95/controls/mimesniff-oracle-r95.c $(pkg-config --cflags --libs gio-2.0)
mkdir -p "$S/tools"; cp .ufo/waves/round-95/build/mado-mimesniff.c1.py "$S/tools/mado-mimesniff.py"
cp tools/mado-mimeglob.py "$S/tools/"
python3 "$S/drv.py"    # 51 fixture rows: hand-made caches, name/data interplay
python3 "$S/host.py"   # 42 host-DB inputs + the word_size 2/4 matchlets
python3 "$S/name.py"   # 7 name/data rows on the host database
```

`drv.py` builds each fixture root as `{root}/{h,dh,s1,s2}` with the cache at `dh/mime/mime.cache`
and runs `env -i LC_ALL=C HOME=… XDG_DATA_HOME=… XDG_DATA_DIRS=<s1>:<s2> "$S/oracle" 0|=NAME file`
against the candidate with flags. 51 rows, **49 agree, 2 disagree**: `f-vt` and `f-vt-early`, both
`0x0b`, where the oracle answers `application/octet-stream 1` and the draft candidate answers
`text/plain 0` (candidate `looks_like_text` at `.ufo/waves/round-95/build/mado-mimesniff.c1.py`:208
and its selftest row `s10` at `:467` encode 8…13 as text). `host.py` (42 inputs) and `name.py`
(10 inputs) show **0 disagreements** on the host database, including the four `word_size` 4 and four
`word_size` 2 matchlets.

Selected DRAFT rows (state → oracle `type` `uncertain` / tool):

| row | state | name | data | oracle | tool |
|---|---|---|---|---|---|
| `f-empty` | empty buffer | NULL | `""` | `application/x-zerosize` 0 | same |
| `n-one-empty` | one name type beats empty | `x.one` | `""` | `t/single` 0 | same |
| `n-two-empty` | two name types | `x.two` | `""` | `application/x-zerosize` 0 | same |
| `nil` (control) | `data == NULL` | NULL / `zz` / `x.txt` | — | octet-stream 1 / 1 / `text/plain` 0 | n/a (API only) |
| `f-vt` | VT in the first 128 | NULL | `ab\x0bcd` | `application/octet-stream` 1 | `text/plain` 0 |
| `f-ff` | FF | NULL | `ab\x0ccd` | `text/plain` 0 | same |
| `f-bs` | BS | NULL | `ab\x08cd` | `text/plain` 0 | same |
| `f-del` | DEL alone | NULL | `ab\x7fcd` | `text/plain` 0 | same |
| `f-127` | 0x01 at index 127 | NULL | `a*127+\x01` | `application/octet-stream` 1 | same |
| `f-128` | 0x01 at index 128 | NULL | `a*128+\x01` | `text/plain` 0 | same |
| `f-nul130` | NUL at index 130 | NULL | `a*130+\x00` | `text/plain` 0 | same |
| `n-one` | one name type, binary bytes | `x.one` | `\x01\x02HI` | `t/single` 0 | same |
| `n-one-beats-hi` | one name type vs priority 90 magic | `x.one` | `HI` | `t/single` 0 | same |
| `n-dir` | trailing slash | `d/` | `HI` | `inode/directory` 1 | same |
| `m-prio90` | magic 90, no name | NULL | `HI there` | `app/hi` 0 | same |
| `n-two-hi` | two name types, magic 90 | `x.two` | `HI` | `app/hi` 0 | same |
| `m-prio79-name` | magic 79, no subclass | `x.two` | `MI x` | `app/x-a` 1 | same |
| `m-prio79-sub` | magic 79, name type a subclass | `x.dup` | `BA x` | `app/child` 0 | same |
| `m-prio79-sub-alias` | alias then `text/*` rule | `x.dup` | `plain\n` | `text/x-old` 0 | same |
| `n-textplain-sub` | two `text/*` name types, sniffed text/plain | `x.tt` | `TP x` | `text/x-a` 0 | same |
| `n-two-bin` | two name types, binary data | `x.two` | `\x01\x02` | `app/x-a` 1 | same |
| `m-prio0` | priority 0 | NULL | `Z0 x` | `text/plain` 0 | same |
| `m-negative` | priority 2^31 | NULL | `NG x` | `text/plain` 0 | same |
| `m-order` | 30 before 95 in one cache | NULL | `LO x` | `app/lo` 0 | same |
| `m-caches` | 90/95 and 60/60 across caches | NULL | `AA` / `EQ` | `app/b95` 0 / `app/a60` 0 | same |
| `m-range` | start 2, length 3 | NULL | `..RG` | `app/range` 0 | same |
| `m-mask` | masked first byte | NULL | `\x1f\x99` | `app/masked` 0 | same |
| `m-nest` | child must hold | NULL | `NE..Y` / `NE..Z` | `app/nest` 0 / octet-stream 1 | same |
| `m-word` | cache word_size 4 | NULL | `WDxx` | `app/word` 0 | same |
| `m-short` | value longer than data | NULL | `ABC` | `text/plain` 0 | same |
| `m-desktop` | desktop sniff, three names | NULL / `zz.nomatch` / `zz.desktop` | `[Desktop Entry]` | x-desktop 0 / text/plain 0 / text/plain 0 | same |
| `m-unknown-literal` | magic names octet-stream | NULL | `OB\x01` | `application/octet-stream` **0** | same |
| host `png`/`pdf`/`gzip`/`elf` | real signatures | NULL, `zz` | — | `image/png`, `application/pdf`, `application/gzip`, `application/x-executable`, all 0 | same |
| host `notes.txt`+PDF | one name type | `notes.txt` | `%PDF-1.7` | `text/plain` 0 | same |
| host `x.png`+PDF | two name types, priority < 80 | `x.png` | `%PDF-1.7` | `image/png` 1 | same |
| host `x.txt`+PNG | one name type | `x.txt` | `\x89PNG…` | `text/plain` 0 | same |
| host `x.png`+PNG | two name types, subclass | `x.png` | `\x89PNG…` | `image/png` 0 | same |
| host `x.pdf`+PNG | one name type | `x.pdf` | `\x89PNG…` | `application/pdf` 0 | same |
| host `x.desktop`, `whatever.desktop` | one name type, desktop body | — | `[Desktop Entry]` | `application/x-desktop` 0 | same |
| host `zz.nomatch`, desktop body | zero name types, sniffed desktop | `zz.nomatch` | `[Desktop Entry]` | `text/plain` 0 | same |

Host database facts used above (read-only): `/usr/share/mime/mime.cache` sha256
`b988d3d27bda7500ba4eb8e88d78e61049796d94ef79745dd366bacf5460bb47`, version 1.2, 689 magic
entries / 1282 matchlets, priority histogram 5:3, 10:34, 20:1, 30:3, 40:19, 45:3, 50:452, 51:1,
55:1, 60:78, 62:1, 65:3, 70:38, 75:9, 80:35, 90:8; `word_size` 1:1274, 2:4, 4:4.

## 8. Located quotes for the registry rows

The rows are in `corpus/SOURCES.md` (S519–S523 added this round, S505 re-opened); the lesson's `## Gate` carries one
quote per new row. S520 as registered (no held row named `xdgmimeint.c` before this round):

**S520** | GLib 2.90.1 xdgmime binary/text fallback — https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/xdgmime/xdgmimeint.c (sha256 `c2364aa825a761255fd6c3390a78c94f06eeaf9babeb07b5ea489ba4cef92f29`, fetched 2026-11-07 two fetches byte-identical per `receipts/sources-open-r95.txt`); host package glib2 2.90.1-1 | code | A | how GLib decides binary vs text when no magic answered: the 128-byte window, the byte classes, and the two constant pointers | `xdgmimeint.c:176-190`; quote `:185-186` "if (chardata[i] < 32 && chardata[i] != 9 && chardata[i] != 10 && chardata[i] != 13) return XDG_MIME_TYPE_UNKNOWN; /* binary data */" (22 words), `:189` "return XDG_MIME_TYPE_TEXTPLAIN;" | the fallback allows VT (0x0b) as a control byte while `looks_like_text` does not call it a space, so a VT in the first 128 bytes is binary | mined | 2026-11-07 | 90d | corpus/knowledge/mime-magic-sniff-r95.md

Located lines for the rows sharing a held file (S519 shares `xdgmimecache.c` with S505/S516, S521 shares
`gcontenttype-fdo.c` with S505/S518 — same digests, new scopes):

| row | new located lines | quote (≤25 words) |
|---|---|---|
| S505 `xdgmime.c` | 516-541 (for_data) | `:523-527` "if (len == 0) { if (result_prio != NULL) *result_prio = 100; return XDG_MIME_TYPE_EMPTY;" (14); `:533` "mime_type = _xdg_mime_cache_get_mime_type_for_data (data, len, result_prio);" (6); `:540` "return _xdg_binary_or_text_fallback(data, len);" (3); `:56` "const char xdg_mime_type_unknown[] = "application/octet-stream";" (5) |
| S519 `xdgmimecache.c` | 167-312 (magic), 751-807 (data entry), 937-1046 (subclass) | `:185-186` "if (i + data_length > len) return FALSE;" (8); `:202` "valid_matchlet = memcmp(cache->buffer + data_offset, (unsigned char *)data + i, data_length) == 0;" (13); `:220-221` "if (OUT_OF_BOUNDS (child_offset, n_children, 32, cache->size)) return FALSE;" (8); `:230-235` "for (i = 0; i < n_children; i++) { if (cache_magic_matchlet_compare (cache, child_offset + 32 * i, data, len)) return TRUE; }" (22); `:257-258` "if (OUT_OF_BOUNDS (matchlet_offset, n_matchlets, 32, cache->size)) return NULL;" (8); `:290` "*prio = 0;" (3); `:305-308` "match = cache_magic_compare_to_data (cache, offset + 16 * j, data, len, prio); if (match) return match;" (16); `:773-774` "match = cache_magic_lookup_data (cache, data, len, &prio); if (prio > priority)" (11); `:784` "if (priority > 0)" (4); `:83-84` "#define OUT_OF_BOUNDS(offset,n,record_size,max) \ (((offset) & 0x3) || (offset) > (max) || (n) > ((max) - (offset)) / (record_size))" (18); `:948-952` "umime = _xdg_mime_cache_unalias_mime_type (mime); ubase = _xdg_mime_cache_unalias_mime_type (base); if (strcmp (umime, ubase) == 0) return 1;" (16); `:957-961` "#if 1 /* Handle supertypes */ if (is_super_type (ubase) && xdg_mime_media_type_equal (umime, ubase)) return 1;" (15); `:965-967` "if (strcmp (ubase, "text/plain") == 0 && strncmp (umime, "text/", 5) == 0) return 1;" (15); `:969-971` "if (strcmp (ubase, "application/octet-stream") == 0 && strncmp (umime, "inode/", 6) != 0) return 1;" (15); `:1019-1022` "/* Detect and avoid buggy circular relationships */ for (k = 0; (*seen)[k] != NULL; k++) if (parent == (*seen)[k]) goto next_parent;" (22) |
| S521 `gcontenttype-fdo.c` | 533-548 (`looks_like_text`), 567-690 (guess with data), and `gcontenttype.c` 315-321 (the public entry) | `:542-544` "if (g_ascii_iscntrl (c) && !g_ascii_isspace (c) && c != '\b')" (10); `:589` "g_return_val_if_fail (data_size != (gsize) -1, g_strdup (XDG_MIME_TYPE_UNKNOWN));" (7); `:613-614` "/* Got an extension match, and no conflicts. This is it. */ if (n_name_mimetypes == 1)" (16); `:625-628` "if (sniffed_mimetype == XDG_MIME_TYPE_UNKNOWN && data && looks_like_text (data, data_size)) sniffed_mimetype = "text/plain";" (13); `:636-638` "if (filename != NULL && strcmp (sniffed_mimetype, "application/x-desktop") == 0) sniffed_mimetype = "text/plain";" (13); `:641-647` "if (n_name_mimetypes == 0) { if (sniffed_mimetype == XDG_MIME_TYPE_UNKNOWN && result_uncertain) *result_uncertain = TRUE; mimetype = g_strdup (sniffed_mimetype);" (18); `:654` "if (sniffed_prio >= 80) /* High priority sniffing match, use that */" (12); `:663` "if ( xdg_mime_mime_type_subclass (name_mimetypes[i], sniffed_mimetype))" (5); `:680-682` "mimetype = g_strdup (name_mimetypes[0]); if (result_uncertain) *result_uncertain = TRUE;" (9); `gcontenttype.c:315-320` "g_content_type_guess (const gchar *filename, const guchar *data, gsize data_size, gboolean *result_uncertain) { return g_content_type_guess_impl (filename, data, data_size, result_uncertain);" (18) |

Spec quotes used in §3 (S523, body sha256 `e00fa00e69b1e95ad8642d05fc5023c26f859bdaf8bdda3e091a55feb016c61e`,
59208 B, HTTP 301 → 200 with redirects followed): §2.12 "use the default type of
application/octet-stream for binary data, or text/plain for textual data" (18); §2.12 "Checking the
first 128 bytes of the file for ASCII control characters is a good way to guess whether a file is
binary or text" (24); §2.12 "Otherwise use the result of the glob match that has the highest
weight." (14); §2.5 "Higher priority entries come first." (5); §2.5 "The word size is used for
byte-swapping." (8).

All 36 C quotes above were extracted mechanically from the fetched bytes by
`.ufo/waves/round-95/w1/R95MScribeEntry-quotes.py` (line ranges → whitespace-collapsed text); every
one is ≤ 25 words and every file digest is printed with it. The `gstrfuncs.c`/`gstrfuncs.h` rows are
S511/S512, fetched this round with HTTP 200 and digests `6ea1c4333161ec4e7c85c212cb46200ec331e45f12ccd20c8d018a3fdaa62fd4`
and `298b0dc4c82805322df7534152b917f9acd54d44e81132988476bb59a6426e23`, matching the SOURCES rows;
their quoted lines are `gstrfuncs.c`:262-264 (the table and its bytes 8-15) and `gstrfuncs.h`:45-57,
85-86 (the bits and the two macros).
