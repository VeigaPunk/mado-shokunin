# R93MScoutSources — sources C1 rests on, re-opened independently

Seat: scout (leaf member, no subagent dispatch). Round 93, hyaku run 15 attempt 1, wave 1.
Base revision `4c6f723f3dca3a26f9d14475d695fe797e2e972c` (master).
Scratch: `$HYAKU_SCRATCH/mado-r93/R93MScoutSources` (default `/fast/scratch/hyaku/…`), deleted on exit.
No installs were made (nothing needed; every tool used was already on the host).

## 0. Headline results

1. **All three GLib digests in the L1 receipt are confirmed** by two independent fetches each, byte-identical.
2. **`src/portal-impl.c` does not exist at tag 1.22.1** — the URL named in the seat item returns HTTP 404. The
   reader lives in `src/xdp-portal-config.c`, renamed twice upstream. This is a stale-source finding the L1
   needs before the claim is frozen.
3. **The `[preferred]`/`.portal` key-read claims in the seat item are confirmed by source and by host probe**,
   with one wording correction: the `.portal` `UseIn` read passes the error out-param but never checks it, so a
   failed `UseIn` read leaves the backend **kept** with `use_in = NULL` and prints nothing.
4. **No new registry row is warranted for `portal-impl.c`** (it is not there). A new row *is* warranted for the
   byte-class key-read surface, and the row shape must use the `file:N` anchor form or QUALITY 107 reads MISS —
   proved by replaying `quality/check-anchor-cover.py` on the real S501/S502 rows.
5. **Cross-domain evidence (routed defect 1 of round 92):** the two byte-class corrections C1 asks for are
   **already landed in the sibling tool `tools/mado-mime.py`** (correct whitespace set at :87, bytes +
   `surrogateescape` load at :230-240 with the same `gstrfuncs.c` citation). Sweep recorded in §7.

---

## 1. GLib 2.90.1 — two fetches each, digests

Command (run twice per file, both fetches byte-identical):

```sh
curl -fsSL https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/<f> -o "$S/src/<f>.fetch<n>"   # n = 1,2
```

| file | fetch 1 sha256 | fetch 2 sha256 | L1 receipt (`receipts/sources-open-r93.txt`) | verdict |
|---|---|---|---|---|
| `gkeyfile.c` | `e1d1270f6c9881daf8a9f49b41395cbdd8e99fa290212e8530e0bd3df23ff656` | identical | `e1d1270f…f656` | **confirmed** |
| `gstrfuncs.c` | `6ea1c4333161ec4e7c85c212cb46200ec331e45f12ccd20c8d018a3fdaa62fd4` | identical | `6ea1c433…2fd4` | **confirmed** |
| `gstrfuncs.h` | `298b0dc4c82805322df7534152b917f9acd54d44e81132988476bb59a6426e23` | identical | `298b0dc4…6e23` | **confirmed** |

Sizes: gkeyfile.c 142,052 B (5,111 lines); gstrfuncs.c 96,685 B (3,529 lines); gstrfuncs.h 25,254 B (692 lines).
Copies of all three are in `.ufo/waves/round-93/w1/R93MScoutSources-fetch/` (each < 300 KB).

## 2. The deciding GLib lines (≤25 words each, with line numbers)

### 2.1 `g_ascii_isspace` and the 0x0B table entry

- `gstrfuncs.h:85-86` — `#define g_ascii_isspace(c) \ ((g_ascii_table[(guchar) (c)] & G_ASCII_SPACE) != 0)`
- `gstrfuncs.h:54` — `G_ASCII_SPACE  = 1 << 8,`
- `gstrfuncs.c:262` — `static const guint16 ascii_table_data[256] = {`
- `gstrfuncs.c:264` (bytes 8..15) — `0x004, 0x104, 0x104, 0x004, 0x104, 0x104, 0x004, 0x004,`
  → byte 8 BS `0x004`, 9 TAB `0x104`, 10 LF `0x104`, **11 VT `0x004`**, 12 FF `0x104`, 13 CR `0x104`, 14 SO `0x004`, 15 SI `0x004`.
  The SPACE bit is `0x100`; VT's entry `0x004` (CNTRL only) does not carry it.

**Decisive point the C1 claim depends on and that is easy to get backwards:** `g_ascii_isspace` is **not** C
`isspace()`. C's `isspace()` counts VT (0x0B); GLib's table does not. Parsing all 128 literal entries of
`ascii_table_data` programmatically, the bytes carrying the SPACE bit are exactly
`0x09 0x0A 0x0C 0x0D 0x20` — VT, BS, SO and SI are excluded. (Space 0x20 is the first entry of the row at
`gstrfuncs.c:267`, value `0x140` = `0x100|0x040`.)

### 2.2 Every `g_ascii_isspace` use in `gkeyfile.c` line parsing

There are **five** uses in the file; exactly **three** are line parsing, and they are the only whitespace rule
on a line:

- `gkeyfile.c:1625` (leading skip, in `g_key_file_parse_line`) — `while (g_ascii_isspace (*line_start))`
- `gkeyfile.c:1738` (key-name trailing chomp, in `g_key_file_parse_key_value_pair`) — `while (g_ascii_isspace (*key_end))`
- `gkeyfile.c:1757` (value leading chug, same function) — `while (g_ascii_isspace (*value_start))`

The other two are **not** line parsing and do not bear on the byte classes:
- `gkeyfile.c:4908` — `if (*value == '\0' || (*eof_int != '\0' && !g_ascii_isspace(*eof_int)))` (integer parse)
- `gkeyfile.c:4988` — `if (!g_ascii_isspace (value[i]))` (boolean parse)

Adjacent rules that are **literal, not `g_ascii_isspace`** (so VT is whitespace in none of them):
`g_key_file_line_is_group` accepts only `' '` and `'\t'` after `]` (`gkeyfile.c:4668-4670`);
`g_key_file_is_key_name` rejects only a leading/trailing `' '` (`gkeyfile.c:4611-4613`);
a value's **trailing** bytes are never stripped — `value_len = line + length - value_start` (`gkeyfile.c:1760`).

### 2.3 Where UTF-8 is validated — load time vs value read

`g_utf8_validate` occurs **exactly twice** in `gkeyfile.c`, both inside getters:

- `gkeyfile.c:2310` — `if (!g_utf8_validate (value, -1, NULL))` in `g_key_file_get_string` (`:2288`)
- `gkeyfile.c:2427` — `if (!g_utf8_validate (value, -1, NULL))` in `g_key_file_get_string_list` (`:2401`)

The loader never validates: `g_key_file_load_from_file` (`:922`) → `g_key_file_load_from_data` (`:974`) →
`g_key_file_parse_data` (`:1834`, splits lines, erases one CR before an LF at `:1855-1860`) →
`g_key_file_flush_parse_buffer` (`:890`, EOF flush) → `g_key_file_parse_line` (`:1613`).
`g_key_file_get_value` (`:2179-2212`) returns the **raw bytes** with no UTF-8 check — the validation is in the
string getters only, so it is per *value*, not per file. `g_key_file_parse_value_as_string` (`:4692`) does escape
decoding, not UTF-8 validation.

**Host probe (glib2 2.90.1-1, `python3` + `gi.repository.GLib`, and a ctypes probe on libglib-2.0) confirms each:**

| fixture | load | read of the relevant key |
|---|---|---|
| `[portal]\n# \xff\xfe comment\nDBusName=org.foo\n` | OK | `DBusName` → `org.foo` |
| `[other]\nx=\xff\xfe\n[portal]\nDBusName=org.foo\n` | OK | `DBusName` → `org.foo` |
| `[portal]\nOther=\xff\xfe\nDBusName=org.foo\n` | OK | `DBusName` → `org.foo` |
| `[portal]\nDBusName=\xff\xfe\n` | OK | `G_KEY_FILE_ERROR_UNKNOWN_ENCODING`: `Key file contains key “DBusName” with value “…” which is not UTF-8` |

`g_key_file_get_value` on the last fixture returns the raw bytes `b'\xff\xfe'` (ctypes probe) while
`g_key_file_get_string` returns `NULL` + the error — i.e. the two getters differ exactly as the source says.

### 2.4 `key_get_locale` and `g_key_file_locale_is_interesting`

- `gkeyfile.c:1806-1830` `key_get_locale` — takes the text from the **last** `[` (`g_strrstr (key, "[")`) and
  treats it as a locale **only when its length is greater than 2** (`if (locale_len > 2)`), i.e. more than `[]`.
- `gkeyfile.c:1586-1610` `g_key_file_locale_is_interesting` — `TRUE` if `G_KEY_FILE_KEEP_TRANSLATIONS`, else
  compares case-insensitively against `g_get_language_names()`.
- `gkeyfile.c:1788-1790` — the parse-time decision: `if (locale == NULL || g_key_file_locale_is_interesting (key_file, locale, locale_len))`.
- `gkeyfile.c:1812` — `locale = g_strrstr (key, "[");` (last `[`, so `x[a[b]` splits at the last one).

Host probe (`LC_ALL` unset, `LANG=en_US.UTF-8`): stored keys for
`DBusName=base` / `DBusName[]=empty` / `DBusName[C]=clocale` / `DBusName[fr]=french` are
`['DBusName', 'DBusName[]', 'DBusName[C]']` — `x[]` and `x[C]` are stored as **plain keys with the suffix kept**,
and `x[fr]` is **dropped at parse time** (not an interesting locale). `get_value('portal','DBusName')` → `base`,
`get_value('portal','DBusName[C]')` → `clocale`, `get_value('portal','DBusName[fr]')` → `None`.
(Under `LC_ALL=C` the language list is `["C"]`, so `x[C]` is the interesting one and `x[fr]` still drops.)

### 2.5 `g_key_file_add_key_value_pair` — repeated keys

- `gkeyfile.c:4420-4427` — `g_hash_table_replace (group->lookup_map, pair->key, pair);` — the **newest pair
  replaces the older** in the lookup map, so a repeated key takes its **last** value.
- `gkeyfile.c:1798-1799` — the parse path inserts the pair into the ordered list before the current head
  (`g_list_insert_before`, `gkeyfile.c:4426`), so **both** pairs stay in the list.
- `gkeyfile.c:2005-2060` `g_key_file_get_keys` — returns **one entry per stored pair, duplicates included**
  (it walks the pair list, not the hash).

Host probe: `[preferred]\ndefault=gnome\norg.x=c\ndefault=kde\n` →
`get_keys('preferred')` = `['default', 'org.x', 'default']` (the key appears **twice**, at both file positions),
`get_value('preferred','default')` = `kde` (last wins), `get_value('preferred','org.x')` = `c`.

## 3. `xdg-desktop-portal` 1.22.1 — the file named in the item does not exist

**The item's URL is stale.** `curl https://raw.githubusercontent.com/flatpak/xdg-desktop-portal/1.22.1/src/portal-impl.c`
→ `curl: (22) The requested URL returned error: 404`. The 1.22.1 tree has no `src/portal-impl.c` and no
`src/xdp-portal-impl.c`; the config/`.portal` reader is **`src/xdp-portal-config.c`**.

Upstream rename chain (GitHub API, `flatpak/xdg-desktop-portal`):

| commit | date | change |
|---|---|---|
| `a6feb89bbd6b` | 2024-11-28 | `src/portal-impl.c` → `src/xdp-portal-impl.c` ("Rename files to follow the prefix-name rule") |
| `4bb70f209748` | 2025-09-18 | `src/xdp-portal-impl.c` → `src/xdp-portal-config.c` ("Rename files to portal-config to match object name") |

`src/xdp-portal-impl.c` exists at tags 1.10.0–1.18.0; from 1.20.0 on the file is `xdp-portal-impl.c`, and at
1.21.0/1.22.0/1.22.1 it is `xdp-portal-config.c`. The gitlab.freedesktop.org mirror is not usable anonymously
(HTTP 302 to a sign-in page), so the GitHub tag is the fetchable locator.

**The file I fetched, twice, byte-identical:**
`https://raw.githubusercontent.com/flatpak/xdg-desktop-portal/1.22.1/src/xdp-portal-config.c` →
sha256 `2da4fd835032401b2ca0e1a503cb600abdb68e27bc9d23b8fbd28f8e2d4c4fe1` (31,103 B, 1,004 lines).
This is **exactly the digest S501 already records** for `src/xdp-portal-config.c`, so the L1's existing pin is
correct and no new upstream pin is needed for that file. The 1.22.1 tag tarball
(`https://codeload.github.com/flatpak/xdg-desktop-portal/tar.gz/refs/tags/1.22.1`, two fetches identical,
sha256 `5afeda953c3743efaa1160e73d62c5bfcac2ceca60e0e134e9b48ed651783625`) also re-derives S501's pin.

### 3.1 Which keys are read, and when — the quoted lines

`.portal` descriptor, `register_portal()` (`src/xdp-portal-config.c:177`):

- `:189` — `if (!g_key_file_load_from_file (keyfile, path, G_KEY_FILE_NONE, error))` → `return FALSE;` (`:190`)
- `:201-203` — `impl_config->dbus_name = g_key_file_get_string (keyfile, "portal", "DBusName", error);`
- `:204` — `if (impl_config->dbus_name == NULL) return FALSE;` → caller `:335-338` prints
  `g_warning ("Error loading %s: %s", path, error->message);` and `continue;` → **backend skipped**
- `:214-216` — `impl_config->interfaces = g_key_file_get_string_list (keyfile, "portal", "Interfaces", NULL, error);`
- `:217` — `if (impl_config->interfaces == NULL) return FALSE;` → **backend skipped** (same `:337` warning)
- `:244-246` — `impl_config->use_in = g_key_file_get_string_list (keyfile, "portal", "UseIn", NULL, error);`
  — the **result is never checked**; the backend is inserted with `use_in = NULL` and nothing is printed.

`portals.conf`, `load_portal_configuration_for_dir()` (`:396`):

- `:408` — `if (!g_key_file_load_from_file (key_file, path, G_KEY_FILE_NONE, NULL))` → `return NULL;`
  (the error is **discarded**: `NULL`, so a load failure voids the file silently)
- `:411` — `ifaces = g_key_file_get_keys (key_file, "preferred", NULL, NULL);` → the **whole group** is enumerated
- `:427` — `interface->portals = g_key_file_get_string_list (key_file, "preferred", ifaces[i], NULL, NULL);`
  → **every** `[preferred]` key is read **eagerly**, whether or not the session would consult that interface
- `:428-432` — `if (interface->portals == NULL) { g_critical ("Invalid portals for interface '%s' in %s", ifaces[i], portal_file); return NULL; }`
  → **one failed read voids the whole config file**
- `:441-446` — a repeated `default` key is read twice; the second time
  `g_warning ("Duplicate default key will get ignored");` fires.

**Host probe of the exact call shape** (ctypes on libglib-2.0, `[preferred]` with
`default=kde` and `org.freedesktop.impl.portal.Print=gnome\xe9`):
`get_keys` → `['default', 'org.freedesktop.impl.portal.Print']`; the `Print` read
(`err=NULL`, as xdp calls it) → **NULL** ⇒ the `g_critical` path ⇒ the whole config file is void, even though
`Print` was never going to be consulted for `FileChooser`. The `default` read → `['kde']`.
For a `.portal` with `UseIn=;\xe9`, the `UseIn` read → **NULL with the error set** (xdp does not look at it):
backend kept, `use_in = NULL`, no message.

**One wording correction to the seat item.** The item says "a `.portal` with an invalid Interfaces/DBusName is
skipped" — confirmed (`Error loading …`, backend skipped, other backends and the config unaffected). It should
add: an invalid byte in **`UseIn`** does **not** skip the backend (the read's failure is unchecked). The
declaration's C1 §(a)/(b) does not currently rest on the `UseIn` case, but the byte-class entry's §8 placeholder
list names it, and the behaviour is "backend kept without a UseIn".

## 4. Registry: is a new row warranted for `portal-impl.c`?

`grep -n 'portal-impl' corpus/SOURCES.md` → **no matches**. The registry's last id is **S510** (445 rows), so the
next free id is **S511**.

**Recommendation: no row for `portal-impl.c`** — at tag 1.22.1 that file does not exist, so a row naming it would
cite a source that is not there (SOURCES contract rule 1: a row is a claim, written only after opening the source
in the round that writes the row). The reader's bytes are already rowed by **S501**, whose `src/xdp-portal-config.c`
digest `2da4fd83…` re-derives exactly from my two fetches.

**But S501's anchor does not cover the byte-class key-read lines.** S501's anchor cell names
`src/xdp-portal-config.c` lines 538-584, 668, 749, 827-846, 897-910, 928-1004 — the search roots, the `none`/`*`
checks and `find_all`. It does **not** name 189, 201, 214, 244, 408, 411, 427. Rule 2 forbids widening S501's
anchor in place (only `status`, `recheck`, `used-by` change). Two in-contract moves:

- **(a) prose citation only** — the round-90 entry cites S501 in prose (`S501 src/xdp-portal-config.c`) and never
  in an evidence row; the byte-class entry can do the same and needs no new row.
- **(b) a new row** for the key-read surface, e.g. **S513**, at the same URL but a different scope ⇒ the census
  prints a **W04** (duplicate url across scopes), which is a non-failing warning (verified below).

### 4.1 The anchor shape that QUALITY 107 accepts — a hard constraint

`quality/check-anchor-cover.py` (QUALITY criterion 107) does **not** read the prose form
`gkeyfile.c lines 1638-1649`. It requires the occurrence `NAME:` followed by a comma-separated locator list, where
`NAME` is the last path component of the **last** `http(s)://` token of the source cell. Replaying the committed
checker on the **real** S501/S502 rows with a synthetic evidence row:

```
ANCHOR_COVER: row=K01 sid=S502 line=2310 name=gkeyfile.c locators=none verdict=MISS reason=no-cover
ANCHOR_COVER: row=K02 sid=S501 line=189  name=1.22.1    locators=none verdict=MISS reason=no-cover
CHECK107: rows=2 covered=0 miss=2 verdict=FAIL
```

S502 fails because its anchor is prose (`gkeyfile.c lines …`, no `gkeyfile.c:`), and S501 fails because its
source cell's **last** URL is the codeload **tarball**, so `NAME` resolves to `1.22.1`, not to a file.
**Consequence for the L1:** any byte-class evidence row that pins `gkeyfile.c:2310` or `xdp-portal-config.c:189`
against S502/S501 reads MISS. New rows must (i) end their source cell with the **file's own** URL and (ii) use the
`file:N` anchor form. I verified that shape end-to-end (§4.2).

### 4.2 Draft rows (11-column shape, no `|` inside any cell) — for the L1 to land

Ids continue from S510; S511 is free (see §5 for the id-collision note with the round-92 scout's *report-only*
drafts, which were never committed).

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S511 | GLib 2.90.1 ASCII classification table — https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gstrfuncs.c (sha256 6ea1c4333161ec4e7c85c212cb46200ec331e45f12ccd20c8d018a3fdaa62fd4) | code | A | which byte values GLib 2.90.1 counts as ASCII whitespace | gstrfuncs.c:262-282 (the table; the byte 8..15 row is line 264) | the table row that shows byte 11 (VT) carries no G_ASCII_SPACE bit, so g_ascii_isspace is not C isspace | queued | 2026-11-07 | 180d | — |
| S512 | GLib 2.90.1 ASCII predicate macros — https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gstrfuncs.h (sha256 298b0dc4c82805322df7534152b917f9acd54d44e81132988476bb59a6426e23) | code | A | the g_ascii_isspace predicate and the G_ASCII_SPACE bit it tests | gstrfuncs.h:54,85-86 (G_ASCII_SPACE = 1 << 8; the g_ascii_isspace macro) | the predicate that decides which bytes GKeyFile treats as whitespace when parsing a line | queued | 2026-11-07 | 180d | — |
| S513 | xdg-desktop-portal 1.22.1 config and portal file readers — https://raw.githubusercontent.com/flatpak/xdg-desktop-portal/1.22.1/src/xdp-portal-config.c (sha256 2da4fd835032401b2ca0e1a503cb600abdb68e27bc9d23b8fbd28f8e2d4c4fe1) | code | A | which keys of the preferred group and of a portal file the reader reads, and when | xdp-portal-config.c:189,201,214,244,408,411,427 | the eager per-key read that voids a config file on one failed read, and skips a backend on a failed DBusName or Interfaces read | queued | 2026-11-07 | 180d | — |
| S514 | GLib 2.90.1 key-file byte classes — https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gkeyfile.c (sha256 e1d1270f6c9881daf8a9f49b41395cbdd8e99fa290212e8530e0bd3df23ff656) | code | A | the byte classes of a key-file line: whitespace positions, per-read UTF-8 validation, repeated keys and locale suffixes | gkeyfile.c:1625,1738,1757,2310,2427 | which bytes are whitespace in a line, that UTF-8 is checked per value read and not at load, and how a repeated key and a locale suffix are stored | queued | 2026-11-07 | 180d | — |

**Verification of the drafts (scratch fixture repos under my scratch, `git -C "$D" rev-parse --show-toplevel`
asserted equal to the fixture before the first commit):**

- `quality/check-anchor-cover.py` on a synthetic entry pinning `gstrfuncs.c:264` (S511), `gstrfuncs.h:85` and
  `gstrfuncs.h:54` (S512), `xdp-portal-config.c:189` and `:427` (S513):
  `CHECK107: rows=5 covered=5 miss=0 verdict=OK`. Same for S514 pinning `gkeyfile.c:2310` and `:1625`:
  `rows=2 covered=2 miss=0 verdict=OK`.
- `scripts/sources-census.sh validate` on the **real** registry plus the draft rows: **no finding names
  S511–S514**; the only new line versus the untouched-registry baseline is
  `file W04 S514 duplicate url gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gkeyfile.c across scopes`
  (W04 is a non-failing warning; `validate` still exits 0). Rows 449, malformed-row count 0, duplicate ids 0.
- **Placement matters:** appending the rows at the *end of the file* puts them outside the `## Registry` section
  and the census prints `E12 S511 row outside Registry section`. They must be inserted directly after the last
  registry row (S510), before the `## Paths`/`## Search log` prose.

### 4.3 Two id/registry coordination notes for the L1

1. **S511 is claimed twice.** The round-93 declaration and the round-93 build entry
   (`.ufo/waves/round-93/build/portal-keyfile-bytes-r93.md`, frontmatter) cite **S511** for
   *GLib gstrfuncs.c + gstrfuncs.h*. The round-92 scout report (`.ufo/waves/round-92/w1/R92MScoutSources.md` §4)
   recommended **S511 = GNU Bash 5.3 Reference Manual** and **S512 = GNU grep 3.12** — as **report-only
   recommendations that were never committed** (the registry's last id is S510; the round-92 lesson's Gate
   records only S508–S510). So there is no committed collision, but the round-92 draft ids are now spoken for.
   The L1 should either (i) land S511/S512 as the gstrfuncs rows (my §4.2) and re-id the round-92 drafts to
   S515/S516 when they are ever landed, or (ii) keep the round-92 ids and give the gstrfuncs rows S513/S514.
   My §4.2 table uses (i) but adds **S513/S514** because the round-93 build entry cites S511 for *both*
   gstrfuncs files in one row, and a single row cannot carry two `NAME`s: the checker resolves `NAME` from the
   **last** URL in the source cell, so a two-file row covers only the last file's pins (proved: a two-URL row
   with `gstrfuncs.c:262-266 and gstrfuncs.h:54` yields `name=gstrfuncs.h locators=54`, and a
   `gstrfuncs.c:264` pin then reads MISS). Splitting the two gstrfuncs files into S511/S512 is what makes the
   byte-class entry's pins checkable.
2. **The byte-class entry's own evidence rows must use the `file:N` pin form.** The round-93 build entry's tables
   carry prose citations (`:2310`, `:427`) rather than `file:N` pin cells, so QUALITY 107 does not reach them
   today; if the L1 promotes them to evidence rows (third cell an `S###`), they must pin against S511–S514,
   not S501/S502, or the check reads MISS (§4.1).

## 5. Cross-domain sweep (routed defect 1 of round 92: "name cross-domain evidence encountered")

Sweep: every `SOURCES.md` row, every `corpus/knowledge/*.md` entry and every `tools/*.py` in the lane was grepped
for `g_ascii_isspace`, the ASCII whitespace set, `G_ASCII_SPACE`, `\v`, `isspace`, `KeyFile`, `gkeyfile`,
`portals.conf` and `G_KEY_FILE_ERROR`.

**Found (cross-domain, in-lane):** the *same two* byte-class corrections C1 asks for are already landed in a
sibling tool, `tools/mado-mime.py`:
- `:87` — `ASCII_SPACE = " \t\n\f\r"  # g_ascii_isspace (glib/gstrfuncs.c ascii_table_data): \v is not a space`
  (the same exclusion of VT the C1 port makes), used at `:138`, `:157`, `:160`;
- `:57-59` — the docstring: *"GKeyFile reading follows GLib 2.90.1 glib/gkeyfile.c as tools/mado-portals.py models
  it (C locale: locale-suffixed keys dropped), with g_ascii_isspace (space, \t, \n, \f, \r; not \v) as the
  whitespace set."*;
- `:230-240` — `load_keyfile` reads **bytes** and decodes `data.decode("utf-8", "surrogateescape")`, with the
  comment *"GKeyFile parses bytes: invalid UTF-8 voids nothing at load time (comments, unread keys); it fails
  only the key whose value is read (_check_utf8)"* — the per-read UTF-8 rule C1 port claims.

So the base tool `tools/mado-portals.py` at `4c6f723f` is the **only** GKeyFile reader in the lane with the old
behaviour, and it is the one C1 moves:
- `:127` `while i < len(raw) and raw[i] in " \t\n\v\f\r":` — leading skip **includes VT**;
- `:146` `key = s[:eq].rstrip(" \t\n\v\f\r")` — key chomp **includes VT**;
- `:149` `value = s[eq + 1:].lstrip(" \t\n\v\f\r")` — value chug **includes VT**;
- `:268` and `:342` `open(path, "r", encoding="utf-8", newline="")` — **strict** UTF-8 decode ⇒ a file with any
  invalid byte is rejected whole, instead of failing only the key whose value is read.

The C1 candidate `.ufo/waves/round-93/build/mado-portals.c1.py` fixes exactly these: `:68`
`ASCII_SPACE = " \t\n\f\r"  # g_ascii_isspace (glib/gstrfuncs.c ascii_table_data): \v is not a space`, and
`:298-301` / `:374-377` read bytes and `decode("utf-8", "surrogateescape")`. **Note:** the candidate's sha256 is
now `e46a861e6a8ab62e26671169e201b953ca629a3861c6dddc74fd89b73b2ac021`, **not** the declaration's
`89039e30…` (that is still the sha256 of the round-92 `build/mado-portals.d1.py`); the candidate has been edited
during this wave (70 diff lines vs `d1.py`: NUL handling, `_next_char` for `g_utf8_find_next_char`, surrogateescape
writes, and a new round-93 byte-class selftest block at `:634-654`). The declaration's digest is stale — the L1
must re-pin the candidate's bytes at the freeze.

**Not found:** no other lane tool, entry or registry row asserts a whitespace set that includes VT for a
GKeyFile-parsed file. `corpus/knowledge/mime-default-resolution-r91.md:146` states the same rule correctly for
GLib's boolean parse (*"`Hidden=` is true only for `true` or `1` followed by nothing but `g_ascii_isspace` bytes
(S502 gkeyfile.c:4979-5004; `\v` is not one, `\f` is — cases sh-38, sh-65)"*) — corroborating the table read in §2.1.

## 6. Commands run (each with its exit status)

| command | rc | note |
|---|---|---|
| `curl -fsSL …/glib/{gkeyfile.c,gstrfuncs.c,gstrfuncs.h}` ×2 each | 0 | digests in §1 |
| `curl -fsSL …/1.22.1/src/portal-impl.c` | **22** | **404 — file does not exist at that tag** (§3) |
| `curl -fsSL …/1.22.1/src/xdp-portal-config.c` ×2 | 0 | `2da4fd83…`, identical; matches S501 |
| `curl -fsSL https://codeload.github.com/…/tar.gz/refs/tags/1.22.1` ×2 | 0 | `5afeda95…`, identical; matches S501 |
| `curl -sSL https://gitlab.freedesktop.org/xdg/xdg-desktop-portal/-/raw/1.22.1/src/portal-impl.c` | 0 (HTTP 302) | mirror needs sign-in; body is a login redirect |
| GitHub API tree/commits for the rename history | 0 | §3 table |
| `python3` (pygobject + ctypes) probes on host glib2 2.90.1-1 | 0 | §2.3, §2.4, §2.5, §3.1 |
| `python3 quality/check-anchor-cover.py` on the real S501/S502 rows | 1 | expected MISS; §4.1 |
| `python3 quality/check-anchor-cover.py` on the draft rows | 0 | `miss=0 verdict=OK`; §4.2 |
| `bash scripts/sources-census.sh validate` on real registry ± drafts | 1 / 0 | baseline E11s are fixture artifacts (§4.2 note); no finding names S511–S514 |
| `grep -n 'portal-impl' corpus/SOURCES.md` | 1 | no matches |

**Census caveat, stated honestly:** the E11 "missing used-by" lines the census prints in my fixture are
artifacts of the scratch fixture (only `corpus/knowledge`, `corpus/lessons`, `tools`, `quality`, `scripts` were
symlinked into it, so `corpus/README.md` and `.ufo/waves/round-*/…` paths could not resolve). The untouched
registry in the same fixture prints the **same** E11 set, and the diff between "with drafts" and "without drafts"
is exactly one added line (the S514 W04). The lane's own census is unaffected by my fixture.

## 7. Unresolved / for the L1

1. **`src/portal-impl.c` does not exist at 1.22.1.** If the frozen claim, the knowledge entry or the registry
   cites it, the citation is unopenable. The correct locator is `src/xdp-portal-config.c`
   (sha256 `2da4fd83…`, already S501's pin) — the seat item's URL and the "portal-impl.c" name need replacing
   everywhere they appear.
2. **Id collision S511** between the round-93 declaration/build entry (GLib gstrfuncs) and the round-92 scout's
   report-only recommendation (GNU Bash manual) — decide once, and renumber the round-92 drafts accordingly (§4.3).
3. **The candidate's digest is stale** in the declaration (`89039e30…` → current `e46a861e…`); re-pin at the
   freeze (§5).
4. **`.portal` `UseIn` read failure keeps the backend** (`use_in = NULL`, no message) — the byte-class entry's
   §8 placeholder list names this case; the behaviour is now pinned to `:244-246` (§3.1).
5. Not verified here (out of this seat's scope): the oracle labels for the 16 frozen byte-class cases, and the
   tool's answers on them — those are the counter's and the executor's to produce.

## 8. Files written

- `.ufo/waves/round-93/w1/R93MScoutSources.md` — this report.
- `.ufo/waves/round-93/w1/R93MScoutSources-fetch/gkeyfile.c` (142,052 B),
  `…/gstrfuncs.c` (96,685 B), `…/gstrfuncs.h` (25,254 B), `…/xdp-portal-config.c` (31,103 B) — the four fetched
  sources, each < 300 KB, digests in §1 and §3.

Scratch (`$HYAKU_SCRATCH/mado-r93/R93MScoutSources/`: `src/`, `probe/`, `chk/`) was deleted on exit.

Report: .ufo/waves/round-93/w1/R93MScoutSources.md
