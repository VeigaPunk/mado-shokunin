# R94MScoutSources — C1 source re-verification (GLib 2.90.1 / shared-mime-info spec 0.21)

Seat: R94MScoutSources · Round 94 (hyaku run 15, w1) · 2026-11-07
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`
Base revision: `a3de997289014e7dbf1d73ae206be1d6f8cdadd0` (master)
Scratch (deleted on exit): `/fast/scratch/hyaku/mado-r94/R94MScoutSources`

Everything below is from sources I re-opened and re-fetched myself. No measurement was run
(no counter, no candidate-vs-oracle sweep as a *claim*): the oracle/candidate runs below are
**DRAFT exploratory runs**, used only to characterise a divergence I had already located in
source. They are not the C1 measurement.

---

## 1. Digest re-verification of `sources-open-r94.txt` — ALL 7 CONFIRMED

Two independent fetches each (`curl -sS -L`, no retry), sha256 of both bodies compared.
Digests are byte-identical across the two fetches in every case.

| # | File | HTTP | fetch1 sha256 | fetch2 sha256 | L1 receipt digest | Verdict |
|---|------|------|---------------|---------------|-------------------|---------|
| 1 | `xdgmimeglob.c` | 200 | `38ed862316a6e948b2b45b93a27c463e1b1e162a2200cf4eeb1e2af8e2980734` | identical | `38ed8623…80734` | **CONFIRMED** |
| 2 | `xdgmimecache.c` | 200 | `ccda4366a1b3d6feb81c6213fde4885b547189e7cfe612f81799d8c1f298db69` | identical | `ccda4366…8db69` | **CONFIRMED** |
| 3 | `xdgmime.c` | 200 | `afb1c1c1ba726a9fb8d8732f4031f5aa85a67ec3b7a2f989b617e4f4f5282410` | identical | `afb1c1c1…2410` | **CONFIRMED** |
| 4 | `xdgmimeint.c` | 200 | `c2364aa825a761255fd6c3390a78c94f06eeaf9babeb07b5ea489ba4cef92f29` | identical | `c2364aa8…f29` | **CONFIRMED** |
| 5 | `gcontenttype-fdo.c` | 200 | `8a5b4f475947a9de2e0ca34e60b0dc31f5c56a2d7e0a9fe8cf84002aca8a2d7c` | identical | `8a5b4f47…a2d7c` | **CONFIRMED** |
| 6 | `smi-index.html` | 200 | `d93c098ee0d4bb5fa479927135469034640e8f3a0e8c88013748fb510c913513` | identical | `d93c098e…3513` | **CONFIRMED** |
| 7 | `smi-s02.html` | 200 | `e00fa00e69b1e95ad8642d05fc5023c26f859bdaf8bdda3e091a55feb016c61e` | identical | `e00fa00e…c61e` | **CONFIRMED** |

Additional URLs I fetched myself (not in the L1 list), HTTP status + sha256 recorded per lane QUALITY 158:

| File | URL | HTTP | sha256 (both fetches identical) |
|------|-----|------|-------------------------------|
| `update-mime-database.cpp` (2.5.1) | `https://gitlab.freedesktop.org/xdg/shared-mime-info/-/raw/2.5.1/src/update-mime-database.cpp` | **200** | `7be6d761253442203b042f2a6dd48b53a46877381eaa2134fbbb66c7d0d15a66` |
| `xdgmimeint.h` | `…/glib/-/raw/2.90.1/gio/xdgmime/xdgmimeint.h` | 200 | `3e00ec92c99614a210e3bb11a91055f44bac02b174269d6def516c6efbef702f` |
| `xdgmime.h` | `…/glib/-/raw/2.90.1/gio/xdgmime/xdgmime.h` | 200 | `8df6f21259a2cfe578358b2b22a62d3ab8a067aaec9fdb6527531492599dad12` |
| `gfileutils.c` | `…/glib/-/raw/2.90.1/glib/gfileutils.c` | 200 | `edbfc1dbf286c1538779590e18f7fe03faa6e7230a2e72ff00b57274f296f546` |
| `xdgmimeglob.h`, `xdgmimemagic.h`, `xdgmimealias.h`, `xdgmimeicon.h`, `xdgmimeparent.h`, `xdgmimecache.h` | `…/gio/xdgmime/<h>` | 200 each | (headers only, no behavioural claim rests on them) |
| `xdgmimealias.c`, `xdgmimeparent.c`, `xdgmimeicon.c`, `xdgmimemagic.c` | `…/gio/xdgmime/<c>` | 200 each | (needed to build a standalone upstream for ordering checks) |

Spec version confirmed from the index page itself: `smi-index.html` says
"This is version 0.21 of the Shared MIME-info Database specification, last updated 2 October 2018."
Matches the L1 receipt's "version 0.21".

**Digest verdict: the L1's `sources-open-r94.txt` is accurate on all 7 entries.** No digest
refuted. Host package versions confirmed read-only via `pacman -Q`:
`glib2 2.90.1-1`, `shared-mime-info 2.5.1-2`, `xdg-utils 1.2.1-2`, `python 3.14.8-1`.

---

## 2. Candidate docstring rule-by-rule vs the upstream line that decides it

Target: `.ufo/waves/round-94/build/mado-mimeglob.c1.py` lines 9–35 (the "Upstream model"
docstring block). Each row: the docstring rule, the **single** upstream line that decides it
(≤25 words), and whether the docstring's cited range actually contains it.

### 2.1 `dirs` — docstring cites `xdgmime.c xdg_init_dirs (:220-300)`

| Rule | Deciding upstream line (file:line) | In cited range? |
|------|--------------------------------------|----------------|
| `XDG_DATA_HOME` used if set (even empty) | `xdgmime.c:226` `xdg_data_home = getenv ("XDG_DATA_HOME");` + `:245` `if (xdg_data_home != NULL)` | **YES** |
| else `$HOME/.local/share` | `xdgmime.c:255` `else if (home != NULL)` + `:261` `strcat (guessed_xdg_home, "/.local/share/mime/");` | **YES** |
| `XDG_DATA_DIRS` unset → `/usr/local/share/:/usr/share/` | `xdgmime.c:231` `xdg_data_dirs = "/usr/local/share/:/usr/share/";` | **YES** |
| only **non-empty** `XDG_DATA_DIRS` elements | `xdgmime.c:279–283` `if (end_ptr == ptr) { ptr++; continue; }` | **YES** |
| each dir gets `/mime/` appended | `xdgmime.c:292` `strcat (dir, "/mime/");` | **YES** |

**Verdict: rule is SOUND and correctly cited.** The function actually starts at `xdgmime.c:217`
(`xdg_init_dirs (void)`), so the docstring's `:220-300` window starts 3 lines into the
function body and ends just past its close — the *deciding* lines are all inside, but the
range is a little off the true span `:217–302`. Cosmetic only.

### 2.2 `mode` — docstring cites `xdgmime.c xdg_mime_init_from_directory (:129-200)` and `(:645-646)`

| Rule | Deciding upstream line | In cited range? |
|------|-----------------------|-----------------|
| a `mime.cache` that **opens** wins over the dir's globs | `xdgmime.c:141` `XdgMimeCache *cache = _xdg_mime_cache_new_from_file (file_name);` → `:143` `if (cache != NULL)` | **YES** |
| cache must be **≥ 40 bytes** | `xdgmimecache.c:127` `if (fstat (fd, &st) < 0 || st.st_size < 40)` | **NO — in a different file** |
| cache must be **version 1.1–1.2** | `xdgmimecache.c:137–139` `if (GET_UINT16 (buffer, 0) != MAJOR_VERSION \|\| (minor < MINOR_VERSION_MIN \|\| minor > MINOR_VERSION_MAX))` with `:63–65` `MAJOR_VERSION 1 / MINOR_VERSION_MIN 1 / MINOR_VERSION_MAX 2` | **NO — in a different file** |
| the dir's **globs are not read** when a cache is used | `xdgmime.c:152` `return FALSE;` (returns from the per-directory initialiser, skipping the globs2/globs read at `:157–172`) | **YES** |
| otherwise `globs2` (weight:type:glob[:flags]) | `xdgmime.c:157–161` `stat (file_name, &st) == 0` → `_xdg_mime_glob_read_from_file (global_hash, file_name, TRUE);` | **YES** |
| otherwise `globs` (type:glob, **weight 50**) | `xdgmime.c:169–171` `_xdg_mime_glob_read_from_file (global_hash, file_name, FALSE);` with `xdgmimeglob.c:668` `weight = 50;` | **YES** (the `weight = 50` is in `xdgmimeglob.c`, not `xdgmime.c`) |
| **any** cache loaded ⇒ name lookups use only the caches | `xdgmime.c:645–646` `if (_caches) return _xdg_mime_cache_get_mime_types_from_file_name (file_name, mime_types, n_mime_types);` | **YES — exact** |

**Verdict: rule is SOUND but two of its sub-facts are attributed to the wrong file.**
The docstring's sentence *"a mime.cache that opens, is >= 40 bytes and has version 1.1-1.2 is a
cache"* is decided in **`xdgmimecache.c:126–139`**, not in the cited `xdgmime.c:129-200` window.
The `xdgmime.c:129-200` window only shows the *call* into the validator. The docstring's own
mode sentence elsewhere says "any valid mime.cache", so the conclusion is right; only the
citation is imprecise. The candidate's implementation is nevertheless correct here — it
re-implements the size/version check itself (candidate `load_cache`: `if len(buf) < 40: return
None`, `if major != 1 or not (1 <= minor <= 2): return None`), matching upstream.

### 2.3 `text` — docstring cites `xdgmimeglob.c` `:643`, `:536-559`, `:419-494`, `:463-467`, `:469-480`, `:391-417`

| Rule | Deciding upstream line | In cited range? |
|------|-----------------------|-----------------|
| lines are `fgets(…, 255)` chunks | `xdgmimeglob.c:643` `while (fgets (line, 255, glob_file) != NULL)` | **YES** |
| literal / simple / full classification | `xdgmimeglob.c:547–550` `if (*ptr == '*' && first_char) maybe_in_simple_glob = TRUE; else if (*ptr == '\\' \|\| *ptr == '[' \|\| *ptr == '?' \|\| *ptr == '*') return XDG_GLOB_FULL;` | **YES** (`:536-559` covers `_xdg_glob_determine_type`, `:537–559`) |
| literals: exact first | `xdgmimeglob.c:442` `if (strcmp ((const char *)list->data, file_name) == 0)` | **YES** |
| literals: then case-folded, **cs excluded** | `xdgmimeglob.c:452–453` `if (!list->case_sensitive && strcmp ((const char *)list->data, lower_case) == 0)` | **YES** |
| literal hit ⇒ single answer, first list hit | `xdgmimeglob.c:444` `mime_types[0] = list->mime_type;` / `return 1;` | **YES** |
| simple globs: reversed-suffix trie, **deepest match only** | `xdgmimeglob.c:328–335` recurse into `node->child` first; `n` from the deeper level wins | **YES** |
| simple: pass 1 on ASCII-lowercased name, cs excluded | `xdgmimeglob.c:463–464` `_xdg_glob_hash_node_lookup_file_name (glob_hash->simple_node, lower_case, len, FALSE, mimes, n_mimes);` | **YES** |
| simple: pass 2 on the original name, cs included, only if <2 | `xdgmimeglob.c:465–467` `if (n < 2) n += _xdg_glob_hash_node_lookup_file_name (glob_hash->simple_node, file_name, len, TRUE, mimes + n, n_mimes - n);` | **YES** |
| full globs: `fnmatch(3)` **flags 0** on the **unfolded** name, only if <2 | `xdgmimeglob.c:473` `if (fnmatch ((const char *)list->data, file_name, 0) == 0)` | **YES** |
| duplicates merged, larger weight wins, swap-from-end | `xdgmimeglob.c:392–417` `filter_out_dupes`; `:404–406` `mimes[i].weight = MAX (mimes[i].weight, mimes[j].weight);` then `mimes[j].mime = mimes[last].mime;` | **YES** |
| sorted by weight, descending | `xdgmimeglob.c:485` `qsort (mimes, n, sizeof (MimeWeight), compare_mime_weight);` with `:367–373` `return bb->weight - aa->weight;` | **YES** |

**Verdict: SOUND and correctly cited.** Note one wording caveat: the docstring says the *full*
glob pass runs "only if fewer than 2" — upstream's guard is `if (n < 2)` at `xdgmimeglob.c:469`,
so the full-glob pass is **skipped entirely** once two simple-glob hits exist, and a full glob
never competes with a simple glob on weight. The docstring's phrasing "only if fewer than 2"
conveys this correctly.

### 2.4 `cache` — docstring cites `xdgmimecache.c cache_glob_lookup_file_name (:668-724)`

| Rule | Deciding upstream line | In cited range? |
|------|-----------------------|-----------------|
| literal binary search, per cache | `xdgmimecache.c:379–429` `for (i = 0; _caches[i]; i++)` + binary search `:387–423` | **YES** |
| a cs hit on the folded pass **ends the literal search** | `xdgmimecache.c:414–424` `int case_sensitive = weight & 0x100;` … `if (case_sensitive_check \|\| !case_sensitive) {…return 1;} return 0;` | **YES** |
| reverse suffix tree **per cache**, each cache adds its own deepest match | `xdgmimecache.c:583` `for (i = 0; _caches[i]; i++)` + `:534–542` recursion; `:594` `list_offset = GET_UINT32 (cache->buffer, 16);` | **YES** |
| fnmatch list per cache | `xdgmimecache.c:455` `list_offset = GET_UINT32 (cache->buffer, 20);` | **YES** |
| weight in the **low 8 bits**, `0x100` = cs | `xdgmimecache.c:414–415` `case_sensitive = weight & 0x100; weight = weight & 0xff;` (also `:468–469`, `:555–556`) | **YES** |
| same merge and sort | `xdgmimecache.c:711` `n = filter_out_dupes (mimes, n);` `:715` `qsort (mimes, n, sizeof (MimeWeight), compare_mime_weight);` | **YES** |

**Verdict: SOUND and correctly cited.**

### 2.5 `guess` — docstring cites `gcontenttype-fdo.c g_content_type_guess_impl (:567-690)`

| Rule | Deciding upstream line | In cited range? |
|------|-----------------------|-----------------|
| trailing `/` ⇒ `inode/directory`, uncertain | `gcontenttype-fdo.c:597–604` `name_mimetypes[0] = "inode/directory"; … *result_uncertain = TRUE;` | **YES** |
| else the **basename**'s types | `gcontenttype-fdo.c:607–608` `basename = g_path_get_basename (filename); n_name_mimetypes = xdg_mime_get_mime_types_from_file_name (basename, name_mimetypes, 10);` | **YES** |
| one type ⇒ it, certain | `gcontenttype-fdo.c:613–620` `if (n_name_mimetypes == 1) { gchar *s = g_strdup (name_mimetypes[0]); … return s; }` | **YES** |
| none ⇒ `application/octet-stream`, uncertain | `gcontenttype-fdo.c:641–650` `if (sniffed_mimetype == XDG_MIME_TYPE_UNKNOWN && result_uncertain) *result_uncertain = TRUE; mimetype = g_strdup (sniffed_mimetype);` | **YES** (the string is `xdgmime.c:56` `const char xdg_mime_type_unknown[] = "application/octet-stream";`) |
| several ⇒ the first, uncertain | `gcontenttype-fdo.c:675–683` `mimetype = g_strdup (name_mimetypes[0]); if (result_uncertain) *result_uncertain = TRUE;` | **YES** |

**Verdict: SOUND and correctly cited.** One nuance the docstring omits: at `gcontenttype-fdo.c:652`
the sniffed type wins over the glob match *when data is supplied*; with `data == NULL` (the
oracle's call shape, `g_content_type_guess(name, NULL, 0, &unc)`) the sniffed branch is skipped
entirely, so "several ⇒ the first, uncertain" holds unconditionally. The docstring's model is
correct **for the oracle's data-less call**, which is what C1 measures.

### 2.6 The remaining docstring paragraphs

| Claim | Verdict |
|-------|---------|
| "A byte >= 0x80 at a compared position never matches a suffix node (the C code widens a signed char)." | **SOUND.** `xdgmimeglob.c:319` `character = file_name[len - 1];` where `xdg_unichar_t` is `unsigned int` (`xdgmimeint.h:27`) and `file_name` is `const char *` — a byte ≥0x80 becomes a huge unsigned value that never equals a stored UCS-4 code point. Same in the cache path (`xdgmimecache.c:497`). |
| "fnmatch runs through the C library in the 'C' locale (the oracle does not call setlocale)." | **SOUND** for the oracle (a C program with no `setlocale` call ⇒ "C" locale by default). The candidate additionally forces `_libc.setlocale(_LC_ALL, b"C")` (candidate line 567), which is what makes the candidate match the oracle. |
| "The tool refuses (exit 3, UNSUPPORTED) a glob file line that is not valid UTF-8, a simple glob with an empty suffix, a weight outside +/-2^30, and a cache whose structure fails the upstream bounds checks in a way the C code would loop on." | **SOUND and load-bearing.** Each refusal corresponds to real upstream non-determinism or a hang — see §6. |

**Overall docstring audit: no refuted rule.** Two citation imprecisions (the 40-byte and
version checks live in `xdgmimecache.c`, not `xdgmime.c`; `xdg_init_dirs` starts at `:217`), and
one cosmetic range offset. No rule in lines 9–35 asserts something the sources do not support.

---

## 3. Every place in `xdgmime.c` that decides cache vs text mode

`xdgmime.c` decides mode in **two independent places**, and they are *not* the same decision:

**(a) Per-directory: does this directory contribute a cache or text globs?**
`xdgmime.c:129–215` `xdg_mime_init_from_directory`. Order inside one directory:
1. `xdgmime.c:137–139` — `stat` `<dir>/mime.cache`.
2. `xdgmime.c:141` — `_xdg_mime_cache_new_from_file (file_name)`.
3. `xdgmime.c:143` — `if (cache != NULL)` ⇒ register in `_caches` (`xdgmime.c:147–150`).
4. `xdgmime.c:152` — **`return FALSE;`** — the per-directory initialiser returns here, so this
   directory's `globs2` / `globs` / `magic` / `aliases` / `subclasses` / `icons` are **never read**.
5. `xdgmime.c:157–163` — else `<dir>/globs2` exists ⇒ `_xdg_mime_glob_read_from_file (global_hash, file_name, TRUE)` (version-two format).
6. `xdgmime.c:165–173` — else `<dir>/globs` ⇒ `_xdg_mime_glob_read_from_file (global_hash, file_name, FALSE)` (version-one format, weight 50).

The `return FALSE` at `:152` is the *only* thing that makes "a dir with a valid mime.cache also
has its globs2 ignored" true. **DRAFT empirical confirmation** (oracle, `env -i`):
a directory holding both a valid `mime.cache` and a `globs2` with an extra pattern
`50:text/x-r94extra:*.r94extra` answers `x.r94extra → application/octet-stream 1`
(the extra `globs2` pattern is invisible), while the same `globs2` **without** the cache answers
`x.r94extra → text/x-r94extra 0`.

**(b) Global: at lookup time, which database answers?**
`xdgmime.c:641–648` `xdg_mime_get_mime_types_from_file_name`:
```
  if (_caches)
    return _xdg_mime_cache_get_mime_types_from_file_name (file_name, mime_types, n_mime_types);
  return _xdg_glob_hash_lookup_file_name (global_hash, file_name, mime_types, n_mime_types);
```
This is the decisive line. It is a **global** switch on `_caches` being non-NULL, i.e. **one
valid cache anywhere in the directory list switches the whole process to cache mode** and the
`global_hash` (all text globs collected in step (a)) is never consulted for names.

**DRAFT empirical confirmation.** Two directories, `s1` holding a valid `mime.cache` and `s2`
holding a `globs2` with `50:text/x-r94froms2:*.r94s2`:
`x.r94s2 → application/octet-stream 1` (s2's globs2 is ignored), `x.r94only → text/x-r94only 0`
(served from s1's cache).

**Consequence for the C1 "mixed" class**: "cache mode" is not per-directory. A case labelled
`mode:"mixed"` must be modelled as *one global switch*, exactly as the candidate does
(candidate `Resolver.__init__`: `self.mode = "cache" if caches else "text"`, and `self.db`
picks the cache DB whenever **any** cache loaded). Also note `xdgmime.c:510`
`xdg_run_command_on_dirs (xdg_mime_init_from_directory, NULL);` visits **every** directory, and
each one that has a valid cache registers it; `xdgmime.c:645` then consults *all* of them
(`xdgmimecache.c:583` `for (i = 0; _caches[i]; i++)`) and merges their results.

**Related but distinct:** `xdgmime.c:404–427` `xdg_check_dir` decides *staleness* (re-read) and
checks `mime.cache` and `globs` — **not** `globs2`. That is an upstream quirk (a `globs2`-only
change is not seen by the 5-second staleness check at `xdgmime.c:482–490`), unrelated to the
C1 mode switch but worth recording: it does not affect a single-shot oracle run.

---

## 4. Spec text (v0.21) on the five requested topics, with the GLib counterpart

Spec = `smi-s02.html` (sha256 `e00fa00e…c61e`), section numbers as printed in the fetched page.

### 4.1 Case-insensitive matching and `cs`

> §2.4: "Applications MUST match globs case-insensitively, except when the case-sensitive attribute
> is set to true. This is so that e.g. main.C will be seen as a C++ file, but IMAGE.GIF will still
> use the *.gif pattern."

> §2.4 (flags): "The fourth field ("cs" in the first globs2 example) contains a list of
> comma-separated flags. The flags currently defined are: cs (for case-sensitive).
> Implementations should ignore unknown flags." … "Implementations should also ignore further
> fields, so that the syntax of the globs2 file can be extended in the future."

GLib counterpart: `xdgmimeglob.c:694–702` recognises `cs` only as a whole comma-delimited
token (`flag == p || flag[-1] == ','` and `flag[2] == 0 || flag[2] == ','`), and truncates at the
next colon (`xdgmimeglob.c:688–691`), which is the spec's "ignore further fields". The
cs bit is then honoured in the literal path (`xdgmimeglob.c:452`) and the simple-glob path
(`xdgmimeglob.c:339`, `:355`) and, in the cache, as the `0x100` bit of the weight word
(`xdgmimecache.c:414`, `:468`, `:555`).

**Divergences:**
- **D1 (text mode, full globs are case-SENSITIVE).** The spec's MUST covers *all* globs.
  GLib's text-mode full-glob pass matches with `fnmatch (pattern, file_name, 0)` on the
  **unfolded** name (`xdgmimeglob.c:473`) and never folds it. A non-cs full glob such as
  `*.[ch]` therefore does **not** match `x.C` in text mode. **DRAFT paired confirmation**
  (same DB content, text vs cache): `x.c` matches in both; `x.C` → `application/octet-stream 1`
  in **text** mode but → `text/x-r94full 0` in **cache** mode (the cache's fnmatch pass at
  `xdgmimecache.c:707` tries `lower_case` first, `xdgmimecache.c:709` then the raw name).
  **This is the single most important divergence for C1: text mode and cache mode disagree
  about the same database content.** The host's own `/usr/share/mime` proves it is not
  theoretical: `main.C → text/x-c++src` and `IMAGE.GIF → image/gif` in cache mode.
- **D2 (text mode, cs globs are only honoured on the *exact* case).** Because the text path
  folds only the *name* (`ascii_tolower`, `xdgmimeglob.c:377–387`) and compares the folded name
  against a *stored* pattern, a `cs` glob whose pattern is already lowercase (`*.c:cs`) is
  unreachable in text mode: `xdgmimeglob.c:463` (folded, cs excluded) and `:466` (unfolded,
  cs included) mean the cs entry is only consulted with the **original** name. **DRAFT
  confirmation**: `50:text/x-cslc:*.c:cs` + `50:text/x-cslc:*.c` in a `globs2` ⇒ `main.c →
  text/x-cslc`, `main.C → (no match)`. This is exactly the spec's intent, but note it is
  reached via name-folding, not via a `cs` check on the full-glob path.
- **D3 (update-mime-database writes each cs glob TWICE).** `update-mime-database.cpp:896–907`
  writes the `:cs` line **and then always writes the same pattern again without flags**
  ("Always write the line without the flags, for older parsers"). Confirmed in the host's
  `/usr/share/mime/globs2`: `50:text/x-c++src:*.C:cs` on line 1255 followed by
  `50:text/x-c++src:*.C` on line 1256. The spec's §2.4 example shows only the `:cs` form
  (`50:text/x-c++src:*.C:cs`). The duplicate non-cs line is what makes `*.C` still match
  case-insensitively in text mode.

### 4.2 Longest pattern

> §2.4: "If several patterns of the same weight match then the longest pattern SHOULD be used.
> In particular, files with multiple extensions (such as Data.tar.gz) MUST match the longest
> sequence of extensions (eg '*.tar.gz' in preference to '*.gz'). Literal patterns (eg, 'Makefile')
> must be matched before all others."

> §2.12 (recommended order): "start by doing a glob match of the filename. Keep only globs with
> the biggest weight. If the patterns are different, keep only globs with the longest pattern, as
> previously discussed."

GLib counterpart: the simple-glob trie is a **reversed suffix tree** and the lookup descends to
the deepest node, returning only that node's mimes (`xdgmimeglob.c:328–335`: the recursive call
into `node->child` must return 0 for the shallower `node->mime_type` to be used). The cache
equivalent is `xdgmimecache.c:534–542` with the same shape.

**Divergences:**
- **D4 (spec's "biggest weight, then longest" vs GLib's "longest, then weight").** §2.12 puts
  *weight* first and *length* second. GLib's trie puts **length first**: the deepest suffix wins
  and the shallower, higher-weight glob never enters the result set. **DRAFT paired
  confirmation** (one directory, `50:text/x-deep:*.tar.gz` and `60:text/x-shallow:*.gz`):
  `x.tar.gz → text/x-r94deep 0` — the weight-60 `*.gz` loses to the weight-50 `*.tar.gz`.
  The same holds in cache mode (`x.tar.gz → text/x-r94deep 0`).
- **D5 (spec's "literal patterns must be matched before all others" is only half-implemented).**
  GLib checks literals first (`xdgmimeglob.c:440–460`) and returns a **single** answer on a hit
  (`:445 mime_types[0] = list->mime_type; return 1;`), so a literal match **suppresses** all
  simple and full globs — consistent with the spec. But the literal list is in *insertion order*,
  not weight order: `xdgmimeglob.c:440` walks `glob_hash->literal_list` in insertion order.
  **DRAFT confirmation**: `10:text/x-low:Makefile` before `90:text/x-high:Makefile` ⇒
  `Makefile → text/x-low` (weight ignored). Same in cache mode (the cache literal list is
  sorted by literal, and equal literals are resolved by the binary search's mid choice).
- **D6 (spec §2.12 "keep only globs with the biggest weight" — GLib keeps up to 10 and keeps
  all of them).** `xdgmime.c:608` passes `10` as the array size; `xdgmimeglob.c:471`
  `list && n < n_mime_types` stops at 10, and the final list is *all* hits sorted by weight, not
  just the top one. The spec's §2.12 phrasing ("keep only globs with the biggest weight") would
  suggest a single winner; GLib returns the whole ordered list and `g_content_type_guess_impl`
  picks `name_mimetypes[0]` (`gcontenttype-fdo.c:680`).

### 4.3 `__NOGLOBS__` / glob-deleteall

> §2.2: "A glob-deleteall element, which indicates that patterns from previously parsed
> directories must be discarded. The patterns defined in this file (if any) are used instead."

> §2.4: "The glob-deleteall element, which means that implementations SHOULD discard information
> from previous directories, is written out into the globs2 file using __NOGLOBS__ as the
> pattern. For instance: 0:text/x-diff:__NOGLOBS__ / 50:text/x-diff:*.diff … In the above
> example, the mimetype text/x-diff is redefined (for instance in a user's ~/.local/share/mime)
> to only be associated with the pattern *.diff, so the other patterns like *.patch were
> removed. The weight in front of the __NOGLOBS__ line is ignored. In a given globs2 file, the
> __NOGLOBS__ line for a given mimetype is always written out before any other globs for this
> mimetype."

GLib counterpart: **there is none.** `grep -n "NOGLOBS\|deleteall" xdgmimeglob.c xdgmimecache.c
xdgmime.c xdgmimeint.c gcontenttype-fdo.c` ⇒ **no match** in any GLib 2.90.1 xdgmime source.

**Divergences:**
- **D7 (`__NOGLOBS__` is not implemented by GLib at all — the spec's SHOULD is unmet).**
  `__NOGLOBS__` is treated as an ordinary literal pattern. **DRAFT confirmation**: a `globs2`
  containing `0:text/x-r94demo:__NOGLOBS__` answers the *file named* `__NOGLOBS__` with
  `text/x-r94demo 0` — i.e. GLib thinks `__NOGLOBS__` is a literal filename pattern, and the
  "discard previous directories' patterns" semantics **never happens**. Cross-directory
  `glob-deleteall` is therefore a **no-op**: a `__NOGLOBS__` line in a later directory does not
  remove an earlier directory's `*.keep` for the same mimetype. **DRAFT confirmation**:
  dir1 `50:text/x-keepme:*.keep`, dir2 `0:text/x-keepme:__NOGLOBS__` + `50:text/x-keepme:*.keep2`
  ⇒ `x.keep → text/x-keepme 0` (dir1's pattern still live).
- **D8 (the `__NOGLOBS__` marker is written into the CACHE too, as a literal).**
  `update-mime-database.cpp:453–462` stores `__NOGLOBS__` as a `Glob` with `noglob = TRUE`, and
  `glob_type()` classifies it as a **LITERAL** (no `*`), so `write_literal_cache`
  (`update-mime-database.cpp:2639–2644`, filter `is_literal_glob`) emits it into the
  **LiteralList** of `mime.cache`. **DRAFT confirmation**: dumping the cache built from a
  package with `<glob-deleteall/>` shows a literal entry `'__NOGLOBS__' -> text/x-r94demo w 0`
  in the LiteralList. Consequently a file literally named `__NOGLOBS__` is typed as that mimetype
  in **cache** mode too (DRAFT: `__NOGLOBS__ → text/x-r94demo 0` against a cache-mode dir).
  So the D7 divergence is present in **both** modes, but it surfaces through different tables.
- **D9 (the spec's "the weight in front of the __NOGLOBS__ line is ignored" is honoured only by
  convention).** `update-mime-database.cpp:458` hard-codes `glob->weight = 0;` for the
  `__NOGLOBS__` marker, and `write_out_glob2` (`:899–907`) writes that 0. GLib never interprets
  it at all, so the weight is simply an unused literal weight of 0.

### 4.4 Weight range

> §2.2: "There is also an optional weight attribute which is used when resolving conflicts with
> other glob matches. **The default weight value is 50, and the maximum is 100.**"

> §2.9 (cache layout): "4 CARD32 WEIGHT in lower 8 bits / FLAGS in rest: 0x100 = case-sensitive"
> (LiteralEntry `:536`, GlobEntry `:545`, ReverseSuffixTreeLeafNode `:558`).

GLib counterpart: the text path parses the weight with `atoi` (`xdgmimeglob.c:664`) — **no range
check at all**; the cache path masks it to 8 bits and steals bit `0x100` for `cs`
(`xdgmimecache.c:414–415`, `:468–469`, `:555–556`).

**Divergences:**
- **D10 (spec says max weight 100; GLib imposes no limit).** `xdgmimeglob.c:664` `weight = atoi (p);`
  accepts any `int`. **DRAFT confirmation**: a hand-written `globs2` with
  `300:text/x-r94w300:*.r94w` beats `100:text/x-r94w100:*.r94w` ⇒ `x.r94w → text/x-r94w300 1`.
  The *producer* enforces the range, not the consumer: `update-mime-database.cpp:313–314`
  `if (p < 0 || p > 100) return -1;` in `get_int_attribute`.
- **D11 (the producer rejects an out-of-range weight by writing `-1`, which the consumer then
  reads as -1 or as 255 depending on mode).** **DRAFT confirmation**: `update-mime-database` with
  `weight="300"` prints `Error in type 'text/x-r94demo' … Bad weight (-1) in <glob> element.`
  yet still writes the glob into `globs2` and `globs` — the `types` file still lists the
  mimetype. The emitted `globs2` line is `-1:text/x-r94demo:*.r94a`, and the emitted cache
  suffix-leaf weight is `0xff` (255 = `-1 & 0xff`). **DRAFT paired confirmation** of the
  divergence this creates: a `globs2` with `50:text/x-normal:*.ae` and `-1:text/x-badw:*.ae`
  answers `z.ae → text/x-normal 1` in **text** mode (atoi gives −1, so −1 sorts last) but
  `z.ae → text/x-badw 1` in **cache** mode (255 sorts first). **Same database, different answer
  per mode.**
- **D12 (the `0x100` cs flag and the 8-bit weight field collide).** A cache leaf with weight
  256 is indistinguishable from weight 0 + cs. **DRAFT confirmation**: hand-patching a cache
  suffix leaf's weight to 256 makes the glob **case-sensitive**: `z.w256 → text/x-w256 0` but
  `Z.W256 → application/octet-stream 1`. The spec's layout (§2.9) has the same collision
  ("WEIGHT in lower 8 bits / FLAGS in rest: 0x100 = case-sensitive"), so this is a *spec-inherited*
  hazard, not a GLib invention — but it is reachable only from a hand-built cache, since the
  producer caps weight at 100.

### 4.5 `mime.cache` header and the literal/suffix/glob list layouts (§2.9 — **not** §2.11)

> **Correction to the seat brief:** the seat brief asks for "the literal/suffix/glob list layouts
> (section 2.11)". In the fetched spec (v0.21) the `mime.cache` format is **§2.9 "The mime.cache
> files"**; **§2.11 is "Subclassing"**, and §2.12 is "Recommended checking order". The layout
> quotes below are therefore from **§2.9** (`smi-s02.html` lines 498–560 of the text rendering).

Spec §2.9, verbatim:
> "Header: 2 CARD16 MAJOR_VERSION 1 / 2 CARD16 MINOR_VERSION 2 / 4 CARD32 ALIAS_LIST_OFFSET /
> 4 CARD32 PARENT_LIST_OFFSET / 4 CARD32 LITERAL_LIST_OFFSET / 4 CARD32 REVERSE_SUFFIX_TREE_OFFSET /
> 4 CARD32 GLOB_LIST_OFFSET / 4 CARD32 MAGIC_LIST_OFFSET / 4 CARD32 NAMESPACE_LIST_OFFSET /
> 4 CARD32 ICONS_LIST_OFFSET / 4 CARD32 GENERIC_ICONS_LIST_OFFSET"
> "LiteralList: 4 CARD32 N_LITERALS / 12*N_LITERALS LiteralEntry / LiteralEntry: 4 CARD32
> LITERAL_OFFSET / 4 CARD32 MIME_TYPE_OFFSET / 4 CARD32 WEIGHT in lower 8 bits / FLAGS in rest:
> 0x100 = case-sensitive"
> "GlobList: 4 CARD32 N_GLOBS / 12*N_GLOBS GlobEntry / GlobEntry: 4 CARD32 GLOB_OFFSET / 4 CARD32
> MIME_TYPE_OFFSET / 4 CARD32 WEIGHT in lower 8 bits / FLAGS in rest: 0x100 = case-sensitive"
> "ReverseSuffixTree: 4 CARD32 N_ROOTS / 4 CARD32 FIRST_ROOT_OFFSET / ReverseSuffixTreeNode:
> 4 CARD32 CHARACTER / 4 CARD32 N_CHILDREN / 4 CARD32 FIRST_CHILD_OFFSET /
> ReverseSuffixTreeLeafNode: 4 CARD32 0 / 4 CARD32 MIME_TYPE_OFFSET / 4 CARD32 WEIGHT in lower
> 8 bits / FLAGS in rest: 0x100 = case-sensitive"
> "Lists in the file are sorted, to enable binary searching. The list of aliases is sorted by
> alias, the list of literal globs is sorted by the literal. The SuffixTreeNode siblings are
> sorted by character."
> "Mimetypes are stored in the suffix tree by appending suffix tree leaf nodes with '\0' as
> character. These nodes appear at the beginning of the list of children."
> "All offsets are in bytes from the beginning of the file. Strings are zero-terminated. All
> numbers are in network (big-endian) order."

GLib counterpart, offset by offset (all confirmed by reading `xdgmimecache.c` and by dumping a
real cache built by `update-mime-database` 2.5.1):

| Spec §2.9 | GLib 2.90.1 | Agrees? |
|-----------|-------------|---------|
| header MAJOR=1, MINOR=2 | `xdgmimecache.c:63–65` `MAJOR_VERSION 1 / MINOR_VERSION_MIN 1 / MINOR_VERSION_MAX 2` | **YES, but GLib accepts MINOR 1 too** — D13 |
| ALIAS_LIST_OFFSET @4 | `xdgmimecache.c:330` `GET_UINT32 (cache->buffer, 4)` | YES |
| PARENT_LIST_OFFSET @8 | `xdgmimecache.c:989` `GET_UINT32 (cache->buffer, 8)` | YES |
| LITERAL_LIST_OFFSET @12 | `xdgmimecache.c:389` `GET_UINT32 (cache->buffer, 12)` | YES |
| REVERSE_SUFFIX_TREE_OFFSET @16 | `xdgmimecache.c:594` `GET_UINT32 (cache->buffer, 16)` | YES |
| GLOB_LIST_OFFSET @20 | `xdgmimecache.c:455` `GET_UINT32 (cache->buffer, 20)` | YES |
| MAGIC_LIST_OFFSET @24 | `xdgmimecache.c:292` `GET_UINT32 (cache->buffer, 24)` | YES |
| NAMESPACE/ICONS/GENERIC_ICONS @28/32/36 | not read by xdgmimecache.c | **D14** |
| LiteralEntry 12 B: LITERAL, MIME_TYPE, WEIGHT\|FLAGS | `xdgmimecache.c:404–405` `offset = GET_UINT32 (... + 12*mid);` then mime offset `+4`, weight `+8` | YES |
| GlobEntry 12 B, same shape | `xdgmimecache.c:455–470` | YES |
| ReverseSuffixTreeNode 12 B: CHARACTER, N_CHILDREN, FIRST_CHILD_OFFSET | `xdgmimecache.c:530–531` `n_children = GET_UINT32 (... + 12*mid + 4); child_offset = GET_UINT32 (... + 12*mid + 8);` with `:521` character at `+ 12*mid` | YES |
| leaf = CHARACTER 0, MIME_TYPE, WEIGHT\|FLAGS | `xdgmimecache.c:545–556` (`match_char != 0` break, then mime at `+4`, weight at `+8`) | YES |
| WEIGHT low 8 bits, 0x100 = cs | `xdgmimecache.c:414–415` `case_sensitive = weight & 0x100; weight = weight & 0xff;` | YES |
| lists sorted; literal list binary-searchable | `xdgmimecache.c:389–423` binary search over the literal list | YES |
| suffix-tree siblings sorted by character | `xdgmimecache.c:520–525` `match_char = GET_UINT32 (... + 12*mid);` with a binary search | YES |
| leaf nodes use '\0' and come first | `xdgmimecache.c:545` `if (match_char != 0) break;` | YES |
| big-endian | `xdgmimecache.c:76–77` `GET_UINT16/GET_UINT32` via `ntohs`/`ntohl` | YES |
| "Cache files have to be written atomically" | producer side: `update-mime-database.cpp` writes `mime.cache.new` then `atomic_update` | YES |

**Divergences:**
- **D13 (GLib accepts cache minor version 1; the spec only defines minor 2).**
  `xdgmimecache.c:64–65` `MINOR_VERSION_MIN 1 / MINOR_VERSION_MAX 2` vs spec §2.9
  "2 CARD16 MINOR_VERSION 2". A version-1.1 cache is accepted by GLib and is undefined by the
  spec. The candidate mirrors GLib (`if major != 1 or not (1 <= minor <= 2): return None`) — it
  is spec-divergent but GLib-faithful, which is the right choice for C1 (the oracle is GLib).
- **D14 (GLib never reads the NAMESPACE_LIST / ICONS_LIST / GENERIC_ICONS_LIST offsets).**
  Spec §2.9 defines offsets 28/32/36; `xdgmimecache.c` has no read of them. **DRAFT
  confirmation**: dumping the cache built from a real package shows the header slots 28/32/36
  hold 484/488/492 — valid, populated offsets that GLib ignores. Harmless for name→type, but it
  means the cache carries data GLib will not use.
- **D15 (the spec's 40-byte minimum is implicit; GLib states it explicitly and enforces it).**
  Spec §2.9's header is 4 + 9*4 = **40 bytes**. GLib `xdgmimecache.c:126–127`
  "A valid cache must be at least 40 bytes for the header." — consistent, and the candidate
  reproduces it.

### 4.6 Summary of every spec/GLib divergence found (C1-relevant)

| # | Area | Spec says | GLib 2.90.1 does | Severity for C1 |
|---|------|-----------|------------------|------------------|
| D1 | case, full globs | MUST match case-insensitively | text mode matches the **unfolded** name (`xdgmimeglob.c:473`); cache mode folds first (`xdgmimecache.c:707`) | **HIGH — text and cache disagree on the same DB** |
| D2 | case, `cs` | cs ⇒ case-sensitive | in text mode the cs entry is only consulted with the original name (`xdgmimeglob.c:463`, `:466`) | MEDIUM |
| D3 | producer | one `:cs` line | `update-mime-database.cpp:896–907` writes the `:cs` line **and** a duplicate flagless line | MEDIUM (DB shape) |
| D4 | longest | §2.12: biggest weight, then longest | trie returns the **deepest suffix**; weight never breaks the tie across depths | **HIGH** |
| D5 | literals | "must be matched before all others" | literals win, but the list is in **insertion order**, not weight order (`xdgmimeglob.c:440`) | MEDIUM |
| D6 | result set | "keep only globs with the biggest weight" | keeps up to **10** and returns them all, sorted (`xdgmimeglob.c:471`, `:485`) | LOW |
| D7 | `__NOGLOBS__` | SHOULD discard previous directories' patterns | **not implemented at all** — `__NOGLOBS__` is an ordinary literal | **HIGH** |
| D8 | `__NOGLOBS__` in cache | (not specified) | the marker is written into the cache **LiteralList** as a literal (`update-mime-database.cpp:453–462`, `:2639`) | MEDIUM |
| D9 | `__NOGLOBS__` weight | "the weight … is ignored" | producer hard-codes 0 (`update-mime-database.cpp:458`); consumer ignores the marker entirely | LOW |
| D10 | weight range | max 100 | consumer imposes none (`atoi`, `xdgmimeglob.c:664`) | MEDIUM |
| D11 | invalid weight | (not specified) | producer emits `-1`; consumer reads −1 (text) vs 255 (cache) → **different answers per mode** | **HIGH** |
| D12 | weight/cs collision | 8-bit weight + `0x100` cs | as specified; reachable only via hand-built cache | LOW |
| D13 | cache version | MINOR_VERSION 2 | GLib accepts MINOR 1–2 (`xdgmimecache.c:64–65`) | LOW |
| D14 | cache lists | 9 list offsets | GLib ignores offsets 28/32/36 | LOW |

---

## 5. `update-mime-database` (shared-mime-info 2.5.1) — the five requested write behaviours

Source: `update-mime-database.cpp`, fetched twice, both sha256
`7be6d761253442203b042f2a6dd48b53a46877381eaa2134fbbb66c7d0d15a66`, HTTP 200.
Host binary is `shared-mime-info 2.5.1-2` (`pacman -Q`).

### 5.1 Does it write `__NOGLOBS__` lines? **YES — into `globs2`, into `globs` (v1), and into `mime.cache`**

- `update-mime-database.cpp:46` `#define NOGLOBS "__NOGLOBS__"`
- `update-mime-database.cpp:450–462` — on a `<glob-deleteall/>` element:
  ```c
  else if (strcmp((char *)field->name, "glob-deleteall") == 0)
    {
      Glob *glob;
      auto list = static_cast<GList *>(g_hash_table_lookup (globs_hash, NOGLOBS));
      glob = g_new0 (Glob, 1);
      glob->pattern = g_strdup (NOGLOBS);
      glob->type = type;
      glob->weight = 0;
      glob->noglob = TRUE;
      glob->case_sensitive = FALSE;
  ```
- `update-mime-database.cpp:919–927` `compare_glob_by_weight` puts `noglob` entries **first**
  (`if (ag->noglob || bg->noglob) return bg->noglob - ag->noglob;`), which is how the spec's
  "the `__NOGLOBS__` line for a given mimetype is always written out before any other globs for
  this mimetype" is realised.
- `update-mime-database.cpp:896–907` `write_out_glob2` emits `0:<type>:__NOGLOBS__` into
  `globs2`; `write_out_glob` (`:865–876`) emits `text/x-r94demo:__NOGLOBS__` into `globs` (v1).
- Into the **cache**: `glob_type("__NOGLOBS__")` is **LITERAL** (no `*`), so
  `is_literal_glob` (`update-mime-database.cpp:2620–2623`) selects it and
  `write_literal_cache` (`:2639–2644`) writes it into the **LiteralList**. **DRAFT confirmation**
  — cache dump of a package with `<glob-deleteall/>`:
  `literal entries 2: '__NOGLOBS__' -> text/x-r94demo w 0x0` and `'makefile' -> text/x-r94demo w 0x32`.

### 5.2 Does it write weights > 255? **NO — it refuses > 100 and writes `-1` instead**

- `update-mime-database.cpp:299–319` `get_int_attribute`:
  ```c
  p = strtol (prio_string, &end, 10);
  if (*prio_string == '\0' || *end != '\0') p = -1;
  ...
  if (p < 0 || p > 100) return -1;
  ```
  ⇒ weights are constrained to **[0, 100]**, matching spec §2.2's "maximum is 100".
- `update-mime-database.cpp:415–421` — the out-of-range case raises
  `Bad weight (-1) in <glob> element.` and **still records the glob** with `weight = -1`.
- `update-mime-database.cpp:896–907` writes the raw `glob->weight` into `globs2` ⇒ a `-1:` line.
- `update-mime-database.cpp:2449–2458` `get_glob_weight_and_flags` masks to 8 bits for the
  cache: `res = glob->weight & 0xff; if (glob->case_sensitive) res |= 0x100;` ⇒ `-1` becomes
  **255** in the cache. Also `update-mime-database.cpp:2860` `(entry->weight & 0xff) | entry->flags`
  for the suffix tree.
  **DRAFT confirmation** — cache dump of the `weight="300"` package: suffix-tree leaf
  `LEAF text/x-r94demo w 0xff`; and the same package's `globs2` carries `-1:text/x-r94demo:*.r94a`.
- ⇒ **No producer-side path writes a weight > 255.** The >255 / 0x100-collision surface is only
  reachable from a hand-built cache (D12).

### 5.3 Does it write `cs` literals and cs globs? **YES — into both `globs2` and `mime.cache`**

- `update-mime-database.cpp:415–437` — `<glob>`: `weight = get_weight (field);
  case_sensitive = get_boolean_attribute (field, "case-sensitive");` and
  `char *pat = case_sensitive ? g_strdup (pattern) : g_ascii_strdown (pattern, -1);`
  ⇒ **a cs pattern keeps its case; a non-cs pattern is lower-cased.**
- `update-mime-database.cpp:896–907` `write_out_glob2` — for a cs glob it writes the `:cs` line
  **and then always writes the same pattern again without the flag**
  ("Always write the line without the flags, for older parsers"). The `cs` token is emitted as
  the 4th colon-field.
- Cache side: `update-mime-database.cpp:2449–2458` `get_glob_weight_and_flags` sets `0x100` for cs;
  `:2482` writes it as the `%ud` weight word; `:2860` writes `(entry->weight & 0xff) | entry->flags`
  for the suffix tree.
- **DRAFT confirmation** — a package with `<glob pattern="Makefile.R94" case-sensitive="true"/>`:
  `globs2` shows `50:text/x-cslit:Makefile.R94:cs` **followed by** `50:text/x-cslit:Makefile.R94`;
  the cache's LiteralList shows `'Makefile.R94' -> text/x-cslit w 0x132` (= 50 | 0x100).
  The host's real `/usr/share/mime/globs2` shows the same doubling for all five of its cs globs
  (lines 272, 527, 1052, 1255, 1507).

### 5.4 Does it write full globs? **YES — into both `globs2` and `mime.cache`**

- `update-mime-database.cpp:2596–2617` `glob_type` classifies a pattern as `GLOB_FULL` when it
  contains `\`, `[`, `?`, or a non-leading `*` — the same predicate as GLib's
  `_xdg_glob_determine_type` (`xdgmimeglob.c:547–550`).
- `update-mime-database.cpp:2650–2655` `write_glob_cache` selects `is_full_glob` and writes the
  **GlobList**; `:2772` `build_suffixes` handles only simple globs for the suffix tree.
- **DRAFT confirmation** — cache dump of a package with `*.[ch]`, `*r94x*`, `data?.bin`:
  `glob entries 3: '*.[ch]' -> text/x-r94demo w 0x28, '*r94x*' -> application/x-r94full w 0x46,
  'data?.bin' -> text/x-r94demo w 0x14`, while the simple globs land in the suffix tree.

### 5.5 Requested table — rule | spec quote | GLib quote | update-mime-database quote | divergence?

| rule | spec quote | GLib 2.90.1 quote | update-mime-database 2.5.1 quote | divergence? |
|------|------------|------------------|------------------------------|------------|
| case-insensitive matching & `cs` | §2.4 "Applications MUST match globs case-insensitively, except when the case-sensitive attribute is set to true." | `xdgmimeglob.c:473` `fnmatch ((const char *)list->data, file_name, 0)` (unfolded, text mode); `xdgmimecache.c:707` folds first | `:428` `char *pat = case_sensitive ? g_strdup (pattern) : g_ascii_strdown (pattern, -1);` `:896–907` writes `:cs` **and** a flagless duplicate | **YES — D1/D2/D3** |
| longest pattern | §2.4 "If several patterns of the same weight match then the longest pattern SHOULD be used." / §2.12 "Keep only globs with the biggest weight." | `xdgmimeglob.c:328–335` deepest trie node wins; `:485` qsort by weight | `:919–927` `compare_glob_by_weight` sorts by weight only | **YES — D4** (GLib: length before weight) |
| `__NOGLOBS__` / glob-deleteall | §2.4 "implementations SHOULD discard information from previous directories … written out … using __NOGLOBS__ as the pattern" | *no match for `NOGLOBS` in any xdgmime source* | `:46` `#define NOGLOBS "__NOGLOBS__"` `:453–462` `:896–907`; into the cache via `:2639–2644` | **YES — D7/D8/D9** (GLib does not implement it) |
| weight range | §2.2 "The default weight value is 50, and the maximum is 100." | `xdgmimeglob.c:664` `weight = atoi (p);` (no limit) | `:313–314` `if (p < 0 \|\| p > 100) return -1;` `:458` `glob->weight = 0;` `:2454` `res = glob->weight & 0xff;` | **YES — D10/D11** (producer caps at 100, consumer does not) |
| cache header & list layouts | §2.9 "2 CARD16 MAJOR_VERSION 1 / 2 CARD16 MINOR_VERSION 2 / 9× CARD32 offsets"; "WEIGHT in lower 8 bits / FLAGS in rest: 0x100 = case-sensitive" | `xdgmimecache.c:63–65` (accepts MINOR 1–2) `:127` ≥40 bytes `:137–139` version `:414–415` `case_sensitive = weight & 0x100; weight = weight & 0xff;` `:330/:389/:455/:594` list offsets | `:2454–2456` `res = glob->weight & 0xff; if (glob->case_sensitive) res |= 0x100;` `:2860` `(entry->weight & 0xff) \| entry->flags` | **YES — D13/D14** (minor-version range; three unused offsets). Layout otherwise matches byte-for-byte. |

---

## 6. Findings that bear directly on the C1 candidate's refusal policy

The candidate's docstring says it refuses (exit 3) four inputs. Each refusal is grounded in
upstream behaviour I confirmed from source — and one of them protects against an upstream
**hang**.

**(a) Malformed cache — upstream INFINITE LOOP, candidate refuses.**
`xdgmimecache.c:532–533`, inside `cache_glob_node_lookup_suffix`'s binary search:
```c
          if (OUT_OF_BOUNDS (child_offset, n_children, 12, cache->size))
            continue;
```
This `continue` is inside the `while (max >= min)` binary-search loop, and it does **not**
advance `min`/`max` — with a node whose `FIRST_CHILD_OFFSET` is out of bounds but whose
`CHARACTER` matches the probed character, the loop re-examines the same `mid` forever.
**DRAFT confirmation**: I hand-built a 104-byte `mime.cache` whose suffix-tree root node has
`CHARACTER='z'` and `FIRST_CHILD_OFFSET=0xFFFFFF00`. Against that DB:
* the **installed glib 2.90.1 oracle** hangs — `timeout 5 … oracle zzz` ⇒ **exit 124**;
* the **standalone upstream 2.90.1 build** (compiled from the fetched sources in my scratch) hangs
  identically — **exit 124**;
* the **candidate** returns `MADO_MIMEGLOB: UNSUPPORTED cache suffix node out of bounds (the C
  lookup loops)` — **exit 3**.
This is the strongest justification for the candidate's refusal rule and it is a genuinely
important fact for the C1 case generator: **a `cachefmt` case must never be built from a
structurally-invalid cache, or the oracle hangs and the counter stalls.** The candidate's
message even names the upstream loop.

**(b) `__NOGLOBS__` in cache mode is a literal.** A case whose `mime.cache` contains a literal
`__NOGLOBS__` will answer the file name `__NOGLOBS__` with that mimetype (D8). The candidate
reproduces it (DRAFT: `__NOGLOBS__ → text/x-r94demo 0` in both text and cache mode).

**(c) Weight `-1` in `globs2` vs 255 in the cache.** A `globs2` written by `update-mime-database`
from an out-of-range weight carries `-1`; the cache carries 255. The two modes then disagree
(D11). The candidate reproduces both (DRAFT paired: `z.ae → text/x-normal 1` text vs
`z.ae → text/x-badw 1` cache).

**(d) Non-UTF-8 `globs2` line.** GLib's comment at `xdgmimeglob.c:641–642` says "FIXME: Not
UTF-8 safe." — GLib's own reader is byte-oriented and does not validate; the candidate refuses
instead. **DRAFT**: with `50:text/x-bad:*.b\xffad` in a `globs2`, the oracle answers
`application/octet-stream 1` while the candidate exits 3 with
`…globs2: line is not valid UTF-8`. The candidate's refusal is a *divergence from the oracle*:
GLib answers, the tool refuses. This is legitimate under the C1 contract ("exit 3 = UNSUPPORTED
(a refusal, never a wrong answer)"), but it means such a case must be classified as a refusal,
not as a mismatch — and it means the C1 counter must not treat a refusal as a wrong answer.

**(e) Weight > 2^30.** GLib's `atoi` is undefined/overflowing there; the candidate refuses
(exit 3). The oracle answers (`text/x-huge 0`). Same contract note as (d).

**(f) A simple glob with an empty suffix (`*` alone).** GLib's `_xdg_glob_determine_type`
(`xdgmimeglob.c:547`) makes `*` SIMPLE with an empty suffix; the trie insert then walks an
empty string. The candidate refuses. DRAFT: oracle answers `application/octet-stream 1`; the
candidate exits 3.

**(g) 255-byte `fgets` chunking.** GLib reads `globs2` in 255-byte chunks
(`xdgmimeglob.c:643`) and a >254-byte line is split into two "lines", the second of which is
garbage. DRAFT: a 300-char pattern line ⇒ the oracle answers `application/octet-stream 1` and
the candidate agrees. Both are consistent with upstream's chunking.

---

## 7. DRAFT differential spot-check of the candidate against upstream (exploratory only)

To make the divergences actionable rather than merely asserted, I compiled a **standalone
upstream** xdgmime 2.90.1 from the fetched sources in my scratch (`xdgmime.c`, `xdgmimeglob.c`,
`xdgmimecache.c`, `xdgmimeint.c`, `xdgmimealias.c`, `xdgmimeparent.c`, `xdgmimeicon.c`,
`xdgmimemagic.c` + a 10-line probe printing the **full ordered** type list) and compared it
with the candidate on 14 fixture pairs covering every divergence above. These are **DRAFT
exploratory runs, not the C1 measurement** (no counter was run, no case file, no mutants).

Comparison method: for each fixture, run the standalone upstream probe and the candidate
(`--json`) under the same `env -i` environment and compare the **complete ordered `types`
array**, not just the winning type.

| # | fixture | upstream winning type(s) | candidate winning type(s) | full ordered list identical? |
|---|---------|--------------------------|----------------------------|------------------------------|
| 1 | 2 dirs, deep(50) vs shallow(60), TEXT — `x.tar.gz` | `text/x-r94deep` | `text/x-r94deep` | **yes** |
| 2 | 2 dirs, deep(50) vs shallow(60), CACHE — `x.tar.gz` | `text/x-r94shallow` (uncertain) | `text/x-r94shallow` (uncertain) | **yes** |
| 3 | 1 dir deep vs shallow, TEXT — `x.tar.gz`, `x.gz` | `text/x-r94deep`, `text/x-r94shallow` | same | **yes** |
| 4 | 1 dir deep vs shallow, CACHE — `x.tar.gz`, `x.gz` | `text/x-r94deep`, `text/x-r94shallow` | same | **yes** |
| 5 | cs literal `Makefile.R94`, TEXT | `text/x-cslit`, `text/x-plain` | same | **yes** |
| 6 | cs literal `Makefile.R94`, CACHE | `text/x-plain`, `text/x-plain` | same | **yes** |
| 7 | literal order (w10 then w90), TEXT — `Makefile` | `text/x-low` | `text/x-low` | **yes** |
| 8 | literal order, CACHE — `Makefile` | `text/x-low` | `text/x-low` | **yes** |
| 9 | `__NOGLOBS__` literal, TEXT | `text/x-r94demo` | `text/x-r94demo` | **yes** |
| 10 | `__NOGLOBS__` literal, CACHE | `text/x-r94demo` | `text/x-r94demo` | **yes** |
| 11 | full glob `*.[ch]`, TEXT — `x.c`, `x.C` | `text/x-fg`, *(none)* | same | **yes** |
| 12 | full glob `*.[ch]`, CACHE — `x.c`, `x.C` | `text/x-fg`, `text/x-fg` | same | **yes** |
| 13 | weight `-1`, TEXT — `z.af` | `text/x-normal` (uncertain) | `text/x-normal` (uncertain) | **yes** |
| 14 | weight `-1`, CACHE — `z.af` | `text/x-badw` (uncertain) | `text/x-badw` (uncertain) | **yes** |

Rows 2 vs 1, 5 vs 6, 11 vs 12 and 13 vs 14 are the four **text-vs-cache** pairs: in every pair
the two modes genuinely disagree about the same database content (D1, D2/D5, D11), and in
every pair the candidate reproduces *both* modes faithfully.

Two further order checks at larger scale, comparing the standalone upstream's **full** list to
the candidate's `types` array:
* 200 equal-weight **simple** globs: upstream `text/x-r001 text/x-r200 text/x-r199 …`; candidate
  `text/x-r001 text/x-r200 text/x-r199 …` — **identical**, including the reversal. This is the
  upstream `_xdg_glob_hash_insert_ucs4` child-list ordering (`xdgmimeglob.c:262–266`,
  `child->next = node->child`) combined with `filter_out_dupes`' swap-from-the-end
  (`xdgmimeglob.c:409–411`), reproduced exactly.
* The candidate's `finish()` comment says "glibc's stable merge sort". **glibc 2.44's `qsort` is
  not stable** (it is a merge sort only when it can allocate; upstream `xdgmimeglob.c:485`
  calls `qsort` with only `n <= 10` elements, so in practice the insertion-sort path is used
  and order is preserved — which is what the 200-entry test confirms). The comment is
  *technically* inaccurate about glibc's `qsort` in general but describes the observed
  behaviour correctly for `n <= 10`. Worth noting so nobody generalises it to larger `n`.

---

## 8. Reproducing inputs for every finding above

All fixtures were built under `$S/fast/scratch/hyaku/mado-r94/R94MScoutSources` (deleted on
exit). Recipe for each class:

* **`__NOGLOBS__` literal (D7/D8)** — a package with `<glob-deleteall/>` plus one `<glob>`;
  `update-mime-database <dir>`; then query the name `__NOGLOBS__`.
* **weight `-1` (D11)** — a package with `<glob pattern="*.af" weight="300"/>`; observe
  `Bad weight (-1) in <glob> element.` and the `-1:` line in `globs2`; then compare the same
  DB read as text vs as cache.
* **full-glob case (D1)** — `globs2` with `50:text/x-fg:*.[ch]`; query `x.c` and `x.C` in text
  mode and in cache mode; the two modes disagree on `x.C`.
* **deep vs shallow (D4)** — one directory with `50:text/x-deep:*.tar.gz` and
  `60:text/x-shallow:*.gz`; query `x.tar.gz`; the weight-50 deeper pattern wins.
* **literal insertion order (D5)** — `globs2` with `10:text/x-low:Makefile` then
  `90:text/x-high:Makefile`; query `Makefile`; the weight-10 (first-listed) wins.
* **cs literal (D2)** — package with `<glob pattern="Makefile.R94" case-sensitive="true"/>`; query
  `Makefile.R94` (cs type) and `makefile.r94` (non-cs type); the two modes order them
  differently.
* **cache cs-bit collision (D12)** — hand-patch a cache suffix-leaf weight to 256; query
  `z.w256` and `Z.W256`.
* **upstream infinite loop** — a 104-byte `mime.cache` with header minor=2, suffix-tree offset
  at byte 16, one root node `CHARACTER='z'`, `N_CHILDREN=1`, `FIRST_CHILD_OFFSET=0xFFFFFF00`;
  query `zzz`; **both the oracle and standalone upstream hang (timeout 5 ⇒ exit 124)**.

---

## 9. Gaps / not established

* I did **not** verify the C1 case file, the counter, the mutants, or the frozen candidate
  hashes — those are other seats' artefacts and outside my item.
* I did **not** audit `xdgmimealias.c` / `xdgmimeparent.c` / `xdgmimeicon.c` / `xdgmimemagic.c`
  for spec divergences (they are outside the name→type path); they were fetched only so that a
  standalone upstream could be built.
* The spec's §2.9 vs §2.11 section-number mismatch in the seat brief (§4.5) is my reading of
  the fetched page; if the L1's `S517` row cites a different section, that row should be
  reconciled.
* Whether `update-mime-database` upstream at 2.5.1 is byte-identical to the host's
  `shared-mime-info 2.5.1-2` build was not checked (no source package on the host); the
  upstream source I quote is the 2.5.1 tarball file, and the host binary's observed output
  (`/usr/share/mime/globs2`, `types`, `globs2`) matches the source's behaviour on every case
  I exercised.
* The `qsort`-stability claim in the candidate's `finish()` comment is about glibc 2.44 on this
  host; a different libc could order equal-weight ties differently.

## 10. Installs

**None.** No package was installed, upgraded or removed; `pacman` was used read-only
(`pacman -Q glib2 shared-mime-info xdg-utils python`) per the PACMAN GUARD. All tooling used
(`curl`, `gcc`, `pkg-config`, `python3`, `sha256sum`, `od`, `timeout`) was already present on
the host. No service was restarted or stopped; no host MIME database was written —
`update-mime-database` was run **only** on directories inside my scratch tree.

## 11. Scratch cleanup

`/fast/scratch/hyaku/mado-r94/R94MScoutSources` was removed after copying the fetched sources
of record (the 7 L1-listed files plus `update-mime-database.cpp`, `xdgmimeint.h`, `xdgmime.h`,
`gfileutils.c` and the xdgmime headers/sources needed for the standalone build) into
`.ufo/waves/round-94/w1/R94MScoutSources-sources/` (21 files + `SHA256SUMS.txt`, which
`sha256sum -c` verifies clean). Scratch on disk at exit: **none**.

Files written by this seat (both under `.ufo/waves/round-94/w1/`, the seat's own subtree):
* `R94MScoutSources.md` — this report.
* `R94MScoutSources-sources/` — the re-fetched sources of record, with `SHA256SUMS.txt`.

No other file in the lane, the repo, or any host location was written by this seat.
`update-mime-database` was run **only** on directories inside the seat's scratch tree; no host
MIME database (`~/.local/share/mime`, `/usr/share/mime`, `/usr/local/share/mime`) was touched.
