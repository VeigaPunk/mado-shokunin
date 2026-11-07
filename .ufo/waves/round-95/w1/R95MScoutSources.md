# R95MScoutSources — independent re-open of the round-95 C1 sources

Seat: R95MScoutSources (scout, leaf). Round mado 95, wave w1, attempt 1.
Base revision `4a2af6817024f6ed47084a5217c1825ae247f4fe` (master).
Scratch: `$HYAKU_SCRATCH/mado-r95/R95MScoutSources` (removed on exit).

**Headline: two real defects in the candidate `mado-mimesniff.c1.py`, both reproduced against the
compiled oracle, plus one spec-vs-GLib divergence class the candidate answers in the *wrong* mode.**

---

## 1. Digest re-open (every URL, two fetches each)

All fetches: `curl -sS -o <f> -w '%{http_code}' <url>`, sha256 of the body, twice per URL, 2026-11-07.

| URL | HTTP | fetch1 sha256 | fetch2 sha256 | vs `receipts/sources-open-r95.txt` |
|---|---|---|---|---|
| `…/glib/-/raw/2.90.1/gio/xdgmime/xdgmimecache.c` | 200 | `ccda4366…db69` | `ccda4366…db69` | **CONFIRMED** (identical) |
| `…/gio/xdgmime/xdgmime.c` | 200 | `afb1c1c1…2410` | `afb1c1c1…2410` | **CONFIRMED** |
| `…/gio/xdgmime/xdgmimeint.c` | 200 | `c2364aa8…2f29` | `c2364aa8…2f29` | **CONFIRMED** |
| `…/gio/xdgmime/xdgmime.h` | 200 | `8df6f212…dad9` | `8df6f212…dad9` | **CONFIRMED** |
| `…/gio/xdgmime/xdgmimemagic.c` | 200 | `fcb1eafe…e742` | `fcb1eafe…e742` | **CONFIRMED** |
| `…/gio/xdgmime/xdgmimeint.h` | 200 | `3e00ec92…ef702` → `3e00ec92…f702` | same | **CONFIRMED** |
| `…/gio/gcontenttype-fdo.c` | 200 | `8a5b4f47…a2d7c` | `8a5b4f47…a2d7c` | **CONFIRMED** |
| `…/gio/gcontenttype.c` | 200 | `fb9c6878…54664` | `fb9c6878…54664` | **CONFIRMED** |
| `…/shared-mime-info-spec/latest/ar01s02.html` | **301** | `1566c459…a3c66` | `1566c459…a3c66` | **REFUTED as a spec digest** (see below) |

Also fetched by me (not in the L1 list), HTTP status + sha256 recorded per lane QUALITY 158:

| URL | HTTP | sha256 (2/2 identical) |
|---|---|---|
| `https://gitlab.freedesktop.org/xdg/shared-mime-info/-/raw/2.5.1/src/update-mime-database.cpp` | 200 | `7be6d761253442203b042f2a6dd48b53a46877381eaa2134fbbb66c7d0d15a66` |
| `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gstrfuncs.c` | 200 | `6ea1c4333161ec4e7c85c212cb46200ec331e45f12ccd20c8d018a3fdaa62fd4` |
| `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gstrfuncs.h` | 200 | `298b0dc4c82805322df7534152b917f9acd54d44e81132988476bb59a6426e23` |

### 1.1 The spec-page digest: `1566c459…` is a redirect stub, not the spec

`specifications.freedesktop.org/shared-mime-info-spec/latest/ar01s02.html` answers **HTTP 301** with a
109-byte body:

```
<a href="http://specifications.freedesktop.org/shared-mime-info/latest/ar01s02.html">Moved Permanently</a>.
```

`sha256` of that body = `1566c4594b825fde8bda64c8136a856e46df6e645a13236f1356097fdc6a3c66` — **exactly the
digest the L1 recorded**. So the L1 did not fetch the spec; it hashed the 301 stub (it must have used
`curl` without `-L`). The spec itself is at `…/shared-mime-info/latest/ar01s02.html` (200):

```
e00fa00e69b1e95ad8642d05fc5023c26f859bdaf8bdda3e091a55feb016c61e   (2/2 fetches identical)
```

and that is **byte-identical to round 94's stored copy**
(`.ufo/waves/round-94/w1/R94MScoutSources-sources/smi-s02.html`, `cmp` = identical).
**Conclusion: the page did not change between round 94 and round 95.** The round-94 digest `e00fa00e…`
is the correct spec digest; the round-95 receipt digest `1566c459…` is the redirect body. Round 94's
note ("served bytes vary over time") is an artefact of following-vs-not-following the redirect, not
of server-side variation. **Action for the L1: re-record the spec digest as `e00fa00e…c61e` (200, with
`-L`), and note the redirect.**

---

## 2. Docstring rule → deciding GLib 2.90.1 line

Candidate docstring = `.ufo/waves/round-95/build/mado-mimesniff.c1.py` lines 9–41. Each rule below is
quoted from the docstring; the deciding source line is quoted from the tag-2.90.1 file (≤25 words).

| # | Docstring rule (candidate line) | Deciding GLib 2.90.1 line | Verdict |
|---|---|---|---|
| 1 | "a trailing '/' -> inode/directory, uncertain" (l. 11–12) | `gcontenttype-fdo.c:597-603` — `if (i > 0 && filename[i - 1] == '/') { name_mimetypes[0] = "inode/directory"; … *result_uncertain = TRUE; }` | ok |
| 2 | "exactly one name type -> it, certain, the bytes are not read (:613-620)" (l. 12) | `gcontenttype-fdo.c:614` — `if (n_name_mimetypes == 1)` → `return s;` before the `if (data)` block | ok |
| 3 | "the bytes are sniffed (:622-639): xdg_mime_get_mime_type_for_data" (l. 12–13) | `gcontenttype-fdo.c:624` — `sniffed_mimetype = xdg_mime_get_mime_type_for_data (data, data_size, &sniffed_prio);` | ok |
| 4 | "if that returned the UNKNOWN constant (pointer comparison, not strcmp)" (l. 13) | `gcontenttype-fdo.c:625` — `sniffed_mimetype == XDG_MIME_TYPE_UNKNOWN &&` | ok |
| 5 | "and looks_like_text (:533-548: no byte that g_ascii_iscntrl and not g_ascii_isspace and not '\\b' -- i.e. none of 0x00-0x07, 0x0e-0x1f, 0x7f)" (l. 14–15) | `gcontenttype-fdo.c:542-544` — `if (g_ascii_iscntrl (c) && !g_ascii_isspace (c) && c != '\b')` | **rule right, the "i.e." gloss is WRONG** → see §4 defect A |
| 6 | "with a name given (even one with no type), a sniffed application/x-desktop becomes text/plain" (l. 16) | `gcontenttype-fdo.c:636-638` — `if (filename != NULL && strcmp (sniffed_mimetype, "application/x-desktop") == 0) sniffed_mimetype = "text/plain";` | ok |
| 7 | "No name type (:641-648): the sniffed type, uncertain only when it is still the UNKNOWN constant." (l. 16–17) | `gcontenttype-fdo.c:643-645` — `if (sniffed_mimetype == XDG_MIME_TYPE_UNKNOWN && result_uncertain) *result_uncertain = TRUE;` | ok |
| 8 | "a sniffed type other than the UNKNOWN constant wins outright when its priority is >= 80" (l. 18–19) | `gcontenttype-fdo.c:654` — `if (sniffed_prio >= 80) /* High priority sniffing match, use that */` | ok |
| 9 | "else the first name type that is a subclass of it" (l. 19) | `gcontenttype-fdo.c:663` — `if ( xdg_mime_mime_type_subclass (name_mimetypes[i], sniffed_mimetype))` | ok |
| 10 | "none -> the first name type, uncertain." (l. 19–20) | `gcontenttype-fdo.c:680-682` — `mimetype = g_strdup (name_mimetypes[0]); … *result_uncertain = TRUE;` | ok |
| 11 | "empty data -> application/x-zerosize with priority 100" (l. 21–22) | `xdgmime.c:523-527` — `if (len == 0) { … *result_prio = 100; return XDG_MIME_TYPE_EMPTY; }` | ok |
| 12 | "with caches, the cache answer; none -> _xdg_binary_or_text_fallback (xdgmimeint.c:176-190)" (l. 22–23) | `xdgmime.c:532-540` — `if (_caches) mime_type = _xdg_mime_cache_get_mime_type_for_data (…); … return _xdg_binary_or_text_fallback (data, len);` | ok |
| 13 | "a byte < 32 other than 9, 10, 13 in the first 128 bytes -> the UNKNOWN constant, else the TEXTPLAIN constant (priority stays 0)." (l. 23–24) | `xdgmimeint.c:183-189` — `for (i = 0; i < 128 && i < len; ++i) if (chardata[i] < 32 && chardata[i] != 9 && … != 10 && … != 13) return XDG_MIME_TYPE_UNKNOWN;` | ok |
| 14 | "per cache in directory order" (l. 25) | `xdgmimecache.c:763` — `for (i = 0; _caches[i]; i++)`; `_caches` is filled in `xdgmime.c:141-151` in dir order | ok |
| 15 | "cache_magic_lookup_data (:276-312) returns the first match entry (cache order) any of whose top-level matchlets holds" (l. 25–27) | `xdgmimecache.c:301-309` — `for (j = 0; j < n_entries; j++) { match = cache_magic_compare_to_data (…); if (match) return match; }` | ok |
| 16 | "a cache's answer replaces the running one only when its priority is strictly greater (an int: priorities >= 2^31 are negative and never win; priority 0 never wins)." (l. 27–28) | `xdgmimecache.c:774` — `if (prio > priority)` (both `int`); `prio` set at `:267` `*prio = priority;` from a `CARD32` | ok |
| 17 | "cache_magic_matchlet_compare (:212-239): a child list that fails the bounds check makes the matchlet false before its own test" (l. 29–30) | `xdgmimecache.c:220-221` — `if (OUT_OF_BOUNDS (child_offset, n_children, 32, cache->size)) return FALSE;` | ok |
| 18 | "a matchlet holds when its value matches and it has no children or any child holds." (l. 30–31) | `xdgmimecache.c:225-236` — `if (cache_magic_matchlet_compare_to_data (…)) { if (n_children == 0) return TRUE; …` | ok |
| 19 | "for i from range_start while i < range_start + range_length (32-bit wrap)" (l. 31–32) | `xdgmimecache.c:181` — `for (i = range_start; i < range_start + range_length; i++)` (all `xdg_uint32_t`) | ok |
| 20 | "stop false as soon as i + value_length (32-bit wrap) exceeds len" (l. 32) | `xdgmimecache.c:185-186` — `if (i + data_length > len) return FALSE;` — **both operands `xdg_uint32_t`: the sum wraps** | **the candidate refuses instead of wrapping** → §4 defect B |
| 21 | "with a mask, every byte compared under the mask" (l. 32–33) | `xdgmimecache.c:192-193` — `if (((unsigned char *)cache->buffer)[data_offset + j] & …mask_offset + j]) != …)` | ok |
| 22 | "word_size is not read." (l. 33) | `xdgmimecache.c:173-177` reads only `range_start`, `range_length`, `data_length`, `data_offset`, `mask_offset` — offset +8 (`WORD_SIZE`) is never read | ok (and see §3 D1) |
| 23 | "subclass … both unaliased (first cache whose alias list holds the name, :314-361)" (l. 34–35) | `xdgmimecache.c:948-949` — `umime = _xdg_mime_cache_unalias_mime_type (mime); ubase = …(base);` | ok |
| 24 | "equal; base 'x/*' with the same media type; base text/plain and mime text/*; base application/octet-stream and mime not inode/*" (l. 35–36) | `xdgmimecache.c:951`, `:959-961`, `:965-967`, `:969-971` | ok |
| 25 | "else each cache's parent list (every cache, not only the first holding the type), recursively, skipping parents already seen." (l. 36–37) | `xdgmimecache.c:979` `for (i = 0; _caches[i]; i++)` + `:1020-1022` `if (parent == (*seen)[k]) goto next_parent;` | ok |

**Rules whose cited line range does not support the claim:** rule **5** only. The prose
("no byte that g_ascii_iscntrl and not g_ascii_isspace and not '\b'") is exactly
`gcontenttype-fdo.c:542-544`; the parenthetical gloss enumerating the bytes is *not* in GLib at all and
is **wrong** (see defect A). The enumeration is decided by `glib/gstrfuncs.h:67-68,85-86` +
`glib/gstrfuncs.c:262-280` (the `g_ascii_table`), which the docstring never cites — the file it names
(`gcontenttype-fdo.c`) does not contain the byte set.

---

## 3. Spec ↔ GLib divergences (ar01s02 §2.5 "The magic files" / §2.9 MAGIC section vs GLib 2.90.1)

| id | Divergence | spec says | GLib 2.90.1 does | file:line |
|---|---|---|---|---|
| **D1** | `word_size` byte-swap | §2.5: "The word size is used for byte-swapping. Little-endian systems should reverse the order of groups of bytes in the value and mask if this is greater than one." | the **cache** reader never reads the `WORD_SIZE` field (matchlet offset +8) and never swaps; only the **text** reader swaps, at parse time | spec `ar01s02` §2.5 (fetched text lines 403-407) vs `xdgmimecache.c:167-210` (reads +0,+4,+12,+16,+20 only) vs `xdgmimemagic.c:470-494` (`if (matchlet->word_size > 1) … SWAP_BE16_TO_LE16 …`) |
| **D2** | `WORD_SIZE` in the cache | §2.9 `Matchlet:` lists `4 CARD32 WORD_SIZE` as field 3 | the cache writer **writes** it (`update-mime-database.cpp:2990`) but the cache reader **ignores** it — the field is inert | `update-mime-database.cpp:2988-2992` vs `xdgmimecache.c:173-177` |
| **D3** | consequence of D1/D2: **the same rule answers differently in the two modes** | one database, one answer | text mode byte-swaps the value, cache mode does not → `host16 0x4142` matches `BA` in text mode but `AB` in cache mode. Verified with the real producer (`update-mime-database` 2.5.1 on a scratch dir): text mode `BA`→`application/x-r95demo`, cache mode `AB`→`application/x-r95demo` | empirical + `xdgmimemagic.c:483-494` vs `xdgmimecache.c:202` `memcmp(cache->buffer + data_offset, …)` |
| **D4** | `priority` is an int | §2.9 `Match: 4 CARD32 PRIORITY` (unsigned) | `cache_get_mime_type_for_data` keeps `int priority` (`:761`), `cache_magic_compare_to_data` writes `*prio = priority` from the CARD32 (`:267`) → a priority ≥ 2^31 is negative and can never win; priority 0 never wins either (`prio > priority` is false) | `xdgmimecache.c:761,774,267` |
| **D5** | first match per cache | §2.5 "Higher priority entries come first" (a *text-file* ordering rule) | the cache reader returns the **first matching entry in file order** and ignores priority within a cache — priority only breaks ties *between* caches | `xdgmimecache.c:301-309` (first match wins), `:774` (strictly greater across caches) |
| **D6** | cross-cache tie | (spec silent) | `if (prio > priority)` — strictly greater, so the **earlier** directory wins a tie | `xdgmimecache.c:774` |
| **D7** | `__NOMAGIC__` (magic-deleteall) | §2.5: "`>0=__NOMAGIC__\n`" | GLib has **no** `__NOMAGIC__` handling in either reader (`grep -c NOMAGIC` = 0 in `xdgmimemagic.c` and in `xdgmimecache.c`); the producer does define and emit it | `update-mime-database.cpp:47,489-490` vs `xdgmimemagic.c`/`xdgmimecache.c` (absent) |
| **D8** | the 128-byte fallback vs `looks_like_text` | (spec silent) | two *different* text tests: the fallback reads only the first 128 bytes (`i < 128 && i < len`) with `!= 9/10/13`, while `looks_like_text` reads **all** bytes with the `iscntrl && !isspace && != '\b'` rule | `xdgmimeint.c:183-186` vs `gcontenttype-fdo.c:538-546` |
| **D9** | text-mode magic section ordering | §2.5 sections are `[prio:type]` blocks, priority-descending | the text reader keeps a priority-sorted list and picks the **highest** priority match (`match->priority > mime_magic->match_list->priority`), so text and cache differ in D5 as well | `xdgmimemagic.c:608,618,670` vs `xdgmimecache.c:301-309` |

**The candidate is cache-mode only** (it refuses text mode with exit 3), so D1–D9 are *not* candidate
bugs — but D1/D3 mean **the cache reader's answer is the byte-swapped-away one**, and the candidate
faithfully reproduces the cache reader (it does not swap). That is *correct for the mode the candidate
claims*, and the docstring says so ("word_size is not read"). The one place the candidate is wrong
about the *cache* mode is defect A below.

---

## 4. Defects in the candidate (each reproduced against the compiled oracle)

Candidate: `.ufo/waves/round-95/build/mado-mimesniff.c1.py`, sha256 `a13b6e0e3b0c399892ff027309f942daa96e92713851e8d8cfb736b277cde99d`
(= the bytes I ran; the L1's frozen candidate). Oracle: `.ufo/waves/round-95/controls/mimesniff-oracle-r95.c`,
sha256 `99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a`, compiled
`cc -O0 -o "$S/oracle" … $(pkg-config --cflags --libs gio-2.0)` (rc 0), gio-2.0 **2.90.1**.

### Defect A — `looks_like_text` byte set: byte **0x0b (VT)** is treated as text by the candidate, as binary by GLib

* **Root cause.** `gcontenttype-fdo.c:542-544` rejects a byte when
  `g_ascii_iscntrl(c) && !g_ascii_isspace(c) && c != '\b'`. GLib's `g_ascii_table`
  (`glib/gstrfuncs.h:67-68,85-86` + `glib/gstrfuncs.c:262-280`) gives
  `CNTRL = {0..31}` and `SPACE = {9,10,12,13,32}` — **0x0b (VT) is CNTRL but NOT SPACE**
  (verified: `g_ascii_isspace(0x0b)==0`, `g_ascii_iscntrl(0x0b)==1`, while C `isspace(0x0b)==8192`).
  So GLib's reject-set is `{0x00-0x07, 0x0b, 0x0e-0x1f, 0x7f}`.
  The candidate implements `looks_like_text` (c.1.py:207-208) as
  `not any(b < 8 or 14 <= b < 32 or b == 127 …)` → reject-set `{0x00-0x07, 0x0e-0x1f, 0x7f}` —
  **0x0b is missing**. It is also missing from the docstring gloss (l. 15).
* **Reproducing input** — case `lltext-01-vt-0b-is-binary` in my case file
  (`w1/R95MScoutSources-cases.json`): a mime.cache whose only magic entry is `app/nomatch` (never
  matches), data = one byte `0x0b`, name NULL.
  * oracle → `application/octet-stream` / uncertain **1**
  * candidate → `text/plain` / uncertain **0**
* **Why the oracle says binary:** the fallback `xdgmimeint.c:183-186` sees `0x0b < 32 && 0x0b != 9/10/13`
  → `XDG_MIME_TYPE_UNKNOWN`; then `gcontenttype-fdo.c:625-628` asks `looks_like_text`, which rejects
  `0x0b` → the answer stays `application/octet-stream`, uncertain.
  The candidate's `looks_like_text` accepts `0x0b` → it upgrades to `text/plain`.
* **Reach:** every data whose first 128 bytes contain `0x0b` and no other rejected byte. A VT in a
  text file (a vertical tab is legal in text) is exactly the realistic case, and the divergence flips
  the answer from *binary* to *text*, i.e. the wrong branch of the fallback, not a marginal label.
  Second case `lltext-02-vt-0b-after-ascii` = `b"ab\x0bcd"` → same flip.
* **The candidate's own selftest encodes the bug**: `s10 VT passes looks_like_text` asserts
  `b"ab\x0bcd"` → `("text/plain", 0)`. The oracle says `application/octet-stream`/1. **The selftest
  is wrong, and it is the only check that pins this behaviour** — so a mutant that fixes the byte set
  would fail the selftest. Fixing defect A requires editing `s10` too.

### Defect B — the 32-bit wrap in the matchlet length test is refused instead of computed

* **Root cause.** `xdgmimecache.c:181-186`:
  ```c
  for (i = range_start; i < range_start + range_length; i++)   /* all xdg_uint32_t */
    {
      if (i + data_length > len)                              /* i, data_length are xdg_uint32_t: the sum WRAPS */
        return FALSE;
  ```
  `i` and `data_length` are 32-bit unsigned, so `i + data_length` wraps mod 2^32 and is then compared
  against `len`. The candidate instead refuses whenever the *mathematical* sum passes 2^32
  (c.1.py `matchlet_value`: `if i + value_length > M32: raise Unsupported(...)`, plus the docstring
  l. 40-41 "a matchlet whose i + value_length passes 2^32 (memcmp past the data)").
* **Reproducing input** — case `wrap-01-i-plus-valuelen-32bit-wrap`: one magic entry
  `range_start=0xFFFFFF00, range_length=0x50, value_length=0x200`, data = 8 bytes `b"12345678"`.
  * oracle → `text/plain` / uncertain **0** (the wrapped sum is `0x100` = 256 > 8 → the matchlet is
    false → no magic match → the text fallback answers)
  * candidate → **exit 3 UNSUPPORTED**
* **Verdict:** the candidate is *over-refusing*. GLib's own behaviour here is well-defined (the sum
  wraps, the comparison is `256 > 8`, the matchlet is simply false); there is no UB to refuse. The
  candidate's refusal is triggered by the *un-wrapped* sum, so it refuses a case GLib answers
  deterministically. The case schema says a case whose oracle "crashes or does not finish within 10 s"
  is labelled `["UNSUPPORTED",null]`; here the oracle answers, so the label must be `["text/plain",0]`
  and the tool must produce it — the candidate cannot.

### Defect C (borderline, reported not claimed) — the deep-nesting refusal threshold is stack-dependent, not 100000

The candidate refuses a matchlet chain "nested deeper than 100000" (c.1.py `MAX_NEST = 100000`; docstring
l. 41-42). GLib's `cache_magic_matchlet_compare` (`xdgmimecache.c:212-239`) is **recursive** and
overflows the C stack at a depth that depends on the stack rlimit, not on 100000:

| stack rlimit | deepest depth the oracle answers | candidate at 100 000 | candidate at 200 000 |
|---|---|---|---|
| 8 MiB (default) | ≈ 74 825 (fuzzy: 74 824 crashed 1 run in 4; 74 825–74 826 in the bisection) | answers (oracle **crashes**) | refuses (oracle crashes) |
| 64 MiB | > 400 000 (answers at 400 000) | answers (oracle answers) | refuses (oracle answers) |

At the default 8 MiB the oracle crashes from depth ≈ 74 825 (the exact edge is fuzzy — stack layout
randomisation moves it by a frame or two between runs), so for depths in (74 826, 100 000] the
oracle is `UNSUPPORTED` while the candidate answers. At 64 MiB the oracle answers at 400 000 while the
candidate refuses — the opposite error. The candidate's fixed 100000 is therefore **wrong in both
directions depending on the environment**, and the round-94 → round-95 measurement environment's
rlimit decides which way. I did **not** file this as a case: the label is environment-dependent, so
it cannot be frozen. **Recommendation for the L1: state the nest limit as "the depth at which the C
recursion overflows *the measurement host's* stack" and pin the rlimit in the counter, or drop the
`nest` class from the frozen set.** (Note the candidate's own selftest asserts nothing about this
threshold, so it is unverified by construction.)

---

## 5. Verified-correct behaviour (no defect found)

Recorded so the L1 does not re-open these.

* **Digest of every source file** confirmed (§1).
* **`word_size` is not read** in cache mode — the candidate matches the cache reader
  (`xdgmimecache.c:173-177`), and `update-mime-database` writes the field but it is inert (D2).
* **priority as int** (D4): a cache priority of 0 → the magic match never wins (oracle `text/plain`,
  candidate `text/plain`); priority `0x80000000` → negative, never wins (both `text/plain`); a
  priority-0 match does not shadow the fallback.
* **first match per cache wins** (D5): a cache with `(10,"app/low")` before `(90,"app/high")`, both
  matching → oracle `app/low`, candidate `app/low`.
* **strictly-greater across caches** (D6): two caches with equal priority → the earlier directory
  wins (oracle and candidate agree); unequal → the higher priority wins.
* **mask comparison** (rule 21): masked bytes compare under the mask (oracle and candidate agree).
* **the `>= 80` sniffed-priority branch** (rule 8): priority 80 wins outright, 79 falls through to the
  subclass tie-break — oracle and candidate agree at the boundary.
* **the subclass rules** (rules 23–25): `x/*` supertype, `text/plain` ← `text/*`,
  `application/octet-stream` ← not `inode/*`, alias unaliasing, and the parent-list walk with the
  `seen` set (cycles terminate) — all agree.
* **`__NOMAGIC__`** (D7): GLib ignores it in both modes; the candidate ignores it too.
* **the 128-byte fallback** (rule 13) matches `xdgmimeint.c:183-186` exactly, including that it
  reads only 128 bytes while `looks_like_text` reads all of them (D8) — the *scope* difference is
  reproduced correctly; only the byte set is wrong (defect A).
* **fuzzing:** 336-case hand-built sweep, a 256-single-byte sweep, a 380-case two-cache sweep, and a
  720-case randomised structured-magic sweep (nested children, masks, ranges, priorities 0/1/30/50/
  79/80/81/100/200, random names) — **every diff found was the same 0x0b root cause**; no other
  divergence surfaced.

---

## 6. Commands run (exit codes)

| # | command | rc |
|---|---|---|
| 1 | `mkdir -p "$HYAKU_SCRATCH/mado-r95/R95MScoutSources"` | 0 |
| 2 | `curl -sS -o <f> -w '%{http_code}' <each of 9 L1 URLs>`, twice each | 0 (HTTP 200 ×8, 301 ×1) |
| 3 | `curl -sSL -o specL-N.html <spec URL>`, twice | 0 (HTTP 200, `e00fa00e…c61e`) |
| 4 | `curl -sS -o umd-N.cpp <update-mime-database 2.5.1>`, twice | 0 (HTTP 200) |
| 5 | `curl -sS -o gs-gstrfuncs.[ch].N <glib gstrfuncs.[ch]>`, twice | 0 (HTTP 200) |
| 6 | `cmp specL-1.html <round-94 smi-s02.html>` | 0 (identical) |
| 7 | `cc -O0 -o "$S/oracle" …/mimesniff-oracle-r95.c $(pkg-config --cflags --libs gio-2.0)` | 0 |
| 8 | `python3 -I tools/mado-mimesniff.py --selftest` | 0 (`checks=23 failed=0`) |
| 9 | `python3 t1.py` (336-case sweep) | 0 (5 diffs, all 0x0b) |
| 10 | `python3 t2.py` (256 single-byte sweep) | 0 (1 diff: 0x0b) |
| 11 | `python3 t3.py` (priority/mask/order/word_size edges) | 0 (1 diff: 0x0b) |
| 12 | `python3 t4.py` (380-case two-cache sweep) | 0 (7 diffs, all 0x0b) |
| 13 | `python3 t5.py` (32-bit wrap) | 0 (found defect B) |
| 14 | `python3 t6.py` (720-case structured magic fuzz) | 0 (12 diffs, all 0x0b) |
| 15 | `python3 t7.py` + `update-mime-database` on a scratch dir | 0 (found D1/D3) |
| 16 | `python3 t9.py`/`t10.py`/`t11.py` (nesting depth vs rlimit) | 0 (found defect C) |
| 17 | `python3 mkcases.py` (build + oracle-label the three cases) | 0 |
| 18 | `python3 t8.py` (re-verify: recorded label == oracle re-run) | 0 (3/3 labels match the oracle) |

No tool was installed or upgraded (none needed); `pacman -Q glib2 shared-mime-info` was read-only.

---

## 7. Deliverables

* **Report:** `.ufo/waves/round-95/w1/R95MScoutSources.md` (this file).
* **Attack cases:** `.ufo/waves/round-95/w1/R95MScoutSources-cases.json`,
  sha256 `660c5bb012b6205e939c0c749d354525b8e0bf96df8863a8daa6f81bf1662aae`, 2574 bytes, 3 cases in the
  shared schema (`version`/`oracle_src_sha256`/`glib2`/`cases`), classes `lltext` and `wrap`, each label
  re-verified against the compiled oracle (`t8.py`: recorded == oracle re-run for 3/3).
  * `lltext-01-vt-0b-is-binary` — defect A, `application/octet-stream`/1
  * `lltext-02-vt-0b-after-ascii` — defect A, `application/octet-stream`/1
  * `wrap-01-i-plus-valuelen-32bit-wrap` — defect B, `text/plain`/0
* **Scratch:** `$HYAKU_SCRATCH/mado-r95/R95MScoutSources` deleted on exit (verified).

**Recommended L1 actions**
1. Re-record the spec digest as `e00fa00e…c61e` (HTTP 200, follow redirects); `1566c459…` is the
   301 stub. The spec page is unchanged since round 94.
2. Add the two `lltext` and one `wrap` cases above to the frozen set (they are in the 20-class
   vocabulary) — each is a guaranteed failure of the current candidate.
3. Fix defect A in the candidate **and** in its selftest check `s10` (which currently asserts the
   wrong answer for `0x0b`).
4. Fix defect B: the length test must wrap mod 2^32 exactly as `xdgmimecache.c:185` does, and the
   refusal should be limited to the genuinely undefined case (`i + value_length` exceeding the *buffer*,
   not 2^32).
5. Pin the stack rlimit for the `nest` class or drop it (defect C).
