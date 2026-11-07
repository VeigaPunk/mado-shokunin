# R91MScoutSources — GLib 2.90.1 source reading and registry rows (round 91, w1)

Seat: scout. Scope: open the GLib 2.90.1 sources C1 rests on, pin their hashes, record
the located line ranges, record where GLib departs from the freedesktop MIME
Applications Associations spec, and draft the `corpus/SOURCES.md` registry rows.

All commands below were run by this seat; each states its exit code. No measurement was
claimed: every `gio` run here is a fixture probe of the *installed* oracle binary, not a
scored label run, and the C1 counter was never invoked by this seat.

## 0. Scratch and fetch provenance

Scratch root: `S=$HYAKU_SCRATCH/mado-r91/R91MScoutSources` (`/fast/scratch/hyaku/mado-r91/R91MScoutSources`).

Each upstream file was fetched **twice** into two separate directories (`fetch1/`,
`fetch2/`) with `curl -sSL`, then compared with `cmp -s`. All ten pairs were byte-identical
(exit 0 for every `cmp`):

```
IDENTICAL gio_gcontenttype-fdo.c        IDENTICAL gio_xdgmime_xdgmimecache.c
IDENTICAL gio_gdesktopappinfo.c         IDENTICAL gio_xdgmime_xdgmimealias.c
IDENTICAL gio_gio-tool-mime.c           IDENTICAL gio_xdgmime_xdgmimeparent.c
IDENTICAL gio_xdgmime_xdgmime.c          IDENTICAL glib_gkeyfile.c
                                        IDENTICAL glib_gshell.c
                                        IDENTICAL glib_gutils.c
```

sha256 of the fetched bytes (identical for both fetches):

| upstream path at tag 2.90.1 | sha256 |
|---|---|
| gio/gdesktopappinfo.c | `8e9ce1a8327a2daf6bc16e8dcfb653c482afde7bebc2ca2621747626b5495b0d` |
| gio/gio-tool-mime.c | `40a450ec0ce177e61aae66175c02b3ebdb50aff1ec5ae65732cb800a60b2bd60` |
| gio/gcontenttype-fdo.c | `8a5b4f475947a9de2e0ca34e60b0dc31f5c56a2d7e0a9fe8cf84002aca8a2d7c` |
| gio/xdgmime/xdgmime.c | `afb1c1c1ba726a9fb8d8732f4031f5aa85a67ec3b7a2f989b617e4f4f5282410` |
| gio/xdgmime/xdgmimecache.c | `ccda4366a1b3d6feb81c6213fde4885b547189e7cfe612f81799d8c1f298db69` |
| gio/xdgmime/xdgmimealias.c | `a1e67ae3604c437b8516d6bc4c67f31afea6fc58393b9afe1c42a8b424111394` |
| gio/xdgmime/xdgmimeparent.c | `9c85c35f143b4fbf274ba07f433ad9102270ededf1a95f6cf0cc320d941f35e3` |
| glib/gkeyfile.c | `e1d1270f6c9881daf8a9f49b41395cbdd8e99fa290212e8530e0bd3df23ff656` |
| glib/gshell.c | `640a0d0fbc9c50d0c70eb8f9ff2c4994392515c6174f76ade9292d7500e60442` |
| glib/gutils.c | `65086c293646bf83884f56f54bb5e2e872adb28ee77f1223d6d9f095a75e3771` |

These match, byte for byte, the hashes the L1 recorded in
`.ufo/waves/round-91/receipts/sources-open-r91.txt` (which opened the same ten URLs
separately). `gkeyfile.c` is the same file already registered as S502.

Spec pages, fetched independently and hashed (`curl -sSL .../latest/<page>.html`):

| page | sha256 |
|---|---|
| index.html | `12ddf2cc546992d5b9c2e0895bd53697e728178ced0269d3718229b531fe826b` |
| file.html | `65c6378e278d47d971cc235180ee727241b4771c4a37a59b262a590fa1c91a6b` |
| associations.html | `77a4843aea1e1c2e8f288aa2f1bc4c37dec3da12ba4fc67feec913999879013a` |
| default.html | `00b5c8f359538398f84c0869be318b48faf7580ff9a9e4ac541f947e55f77ec6` |

All four match the L1's `sources-open-r91.txt` hashes and the ones already in S507.

Host: `pacman -Q glib2 shared-mime-info` → `glib2 2.90.1-1`, `shared-mime-info 2.5.1-2`;
`sha256sum /usr/bin/gio` → `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`
(the hash the C1 counter pins). Host `mimeinfo.cache` files carry the cache header
`00 01 00 02` (major 1, minor 2) at `/usr/share/mime/mime.cache` and
`~/.local/share/mime/mime.cache`; `/usr/local/share/mime/mime.cache` is absent.

## 1. Located line ranges (2.90.1 as fetched)

Every range below was located by `grep -n` over the fetched bytes and read in context.

**gio/gdesktopappinfo.c**

| symbol | lines |
|---|---|
| `desktop_file_dir_app_name_is_masked` (mask rule) | 288–304 |
| `validate_xdg_desktop` (desktop-token validation) | 311–325 |
| `get_valid_current_desktops` | 328–353 |
| `get_lowercase_current_desktops` | 356–377 |
| `get_apps_from_dir` | 769–811 |
| `expand_strv` | 855–898 |
| `desktop_file_dir_unindexed_read_mimeapps_list` | 901–990 |
| `desktop_file_dir_unindexed_read_mimeapps_lists` (per-dir file order) | 993–1042 |
| `desktop_file_dir_unindexed_mime_lookup` | 1312–1348 |
| `desktop_file_dir_unindexed_default_lookup` | 1350–1370 |
| `desktop_file_dir_new_for_config` (config dir, no `/applications`) | 1414–1424 |
| `desktop_file_dir_get_app` | 1532–1540 |
| `desktop_file_dir_mime_lookup` | 1575–1581 |
| `desktop_file_dir_default_lookup` | 1591–1597 |
| `desktop_file_dirs_lock` (dir order) | 1624–1678 |
| `g_desktop_app_info_load_from_keyfile` | 1894–2096 |
| `g_desktop_app_info_new` (drops Hidden) | 2186–2216 |
| `get_list_of_mimetypes` | 4552–4587 |
| `g_desktop_app_info_get_desktop_ids_for_content_type` | 4589–4620 |
| `g_app_info_get_recommended_for_type_impl` | 4622–4646 |
| `g_app_info_get_fallback_for_type_impl` | 4648–4685 |
| `g_app_info_get_all_for_type_impl` | 4687–4711 |
| `g_app_info_get_default_for_type_impl` | 4721–4784 |

**gio/gio-tool-mime.c** — `handle_mime` 62–181; the "one type" branch that prints
`Default application for …` then `Registered applications:` / `Recommended applications:`
is 109–152.

**gio/gcontenttype-fdo.c** — `_g_unix_content_type_unalias` 68–80;
`_g_unix_content_type_get_parents` 82–111; `_g_content_type_set_mime_dirs_locked` 116–139.

**gio/xdgmime/xdgmime.c** — `xdg_mime_init_from_directory` 129–213 (cache first at
137–153, then `globs2`/`globs`/`magic`/`aliases`/`subclasses`/`icons`/`generic-icons`);
`xdg_init_dirs` 217–300; `xdg_mime_set_dirs` 331–346; `_xdg_mime_unalias_mime_type`
735–746; `xdg_mime_list_mime_parents` 902–925; `xdg_mime_get_mime_parents` 928+.

**gio/xdgmime/xdgmimecache.c** — `_xdg_mime_cache_new_from_file` 108–160 with the version
gate at 136–139 (`MAJOR_VERSION 1`, `MINOR_VERSION_MIN 1`, `MINOR_VERSION_MAX 2` at
63–65); `cache_alias_lookup` 314–361 (binary search per cache, `_caches` walked in
order); `_xdg_mime_cache_unalias_mime_type` 1051–1062;
`_xdg_mime_cache_list_mime_parents` 1064–1130.

**gio/xdgmime/xdgmimealias.c** — `_xdg_mime_alias_list_lookup` 83–101 (`bsearch` over the
qsort'ed array); `read_from_file` 104–149 with `qsort` at 147.

**gio/xdgmime/xdgmimeparent.c** — `_xdg_mime_parent_list_lookup` 88–107 (`bsearch`);
`read_from_file` 110–185.

**glib/gshell.c** — `unquote_string_inplace` 65–; `g_shell_unquote` 272–;
`tokenize_command_line` 434–657; `g_shell_parse_argv` 658–730.

**glib/gutils.c** — `g_find_program_for_path` 300–519 (the
`if (g_path_is_absolute (original_program)) return NULL;` early-out at 363–364);
`g_build_system_data_dirs` 2597–2618; `g_build_user_data_dir` 1876–1888.

**glib/gkeyfile.c** — `g_key_file_get_value` 2179–; `g_key_file_get_string` 2288–2325;
`g_key_file_parse_value_as_boolean` 4979–5004 (accepts `true`/`1`/`false`/`0`, comparing
only the non-whitespace prefix).

## 2. Where GLib 2.90.1 departs from the mime-apps spec

The spec is version 1.0.1 (`specifications.freedesktop.org/mime-apps-spec/latest/`).
Five departures, each with the spec text and the GLib line that contradicts it. All four
were exercised against the installed `/usr/bin/gio` on fixtures under `$S` (read-only
`gio mime TYPE`, one type argument, `env -i` with every XDG root inside the scratch).

**(a) The spec's default must be *associated with* the type; GLib does not check.**
Spec `default.html`: "Note as well that the default application for a given type must be
an application that is associated with the type." GLib's default path
(`g_app_info_get_default_for_type_impl`, 4721–4784) collects `[Default Applications]`
entries and takes the first that *loads*; it never asks whether that desktop file claims
the type. Fixture (`$S/fxC`): `[Default Applications] text/x-child=foo.desktop` with
`foo.desktop` declaring no `MimeType` → `gio mime text/x-child` prints
`Default application for “text/x-child”: foo.desktop`. Same for `Hidden=true`
(`$S/fxB`): the hidden app *is* accepted as the default, while it is dropped from the
registered/recommended lists (2186–2216 vs 4687–4711/4622–4646). So a `Hidden=true`
desktop file can be the default but never a listed application.

**(b) The spec's listing algorithm adds ".desktop file … which lists the given type in its
MimeType= line"; GLib ignores `MimeType=` lines entirely and reads `mimeinfo.cache`.**
Spec `associations.html` step 3 of the algorithm: "add to the results list any .desktop
file found in the same directory as the mimeapps.list which lists the given type in its
MimeType= line". GLib's equivalent source is `mimeinfo.cache`'s `[MIME Cache]` group
(`read_mimeapps_list` with `MIME_CACHE_GROUP`, 993–1042). Fixture (`$S/fxE`): a desktop
file with `MimeType=text/x-child;` and **no** `mimeinfo.cache` → `gio mime text/x-child`
prints `No default applications for “text/x-child”`; adding a `mimeinfo.cache` with
`[MIME Cache] text/x-child=mimeapp.desktop;` for the same tree → the app appears as
default, registered and recommended. The candidate reproduces both halves exactly
(`default=none registered=- recommended=-` then `default=mimeapp.desktop registered=mimeapp.desktop
recommended=mimeapp.desktop`). This is the single most consequential departure for the
C1 model: `MimeType=` in a `.desktop` file contributes **nothing** to what `gio mime`
prints.

**(c) The spec's removal blacklist is per-mimetype; GLib's blocklist spans ancestors.**
Spec `associations.html`: "The above process is repeated for each mimetype from the most
specific to the least specific", and the note that an application "Added" with a more
specific mime type keeps that association even if "Removed" … using a less specific type.
GLib keeps **one** `blocklist` for the whole lookup: it is allocated at 4735, outside the
per-type loop, and the comment at 4770–4772 says so explicitly ("Reset the list, ready to
try again with the next (parent) mimetype, but keep the blocklist in place"). The
same single blocklist is used by `g_desktop_app_info_get_desktop_ids_for_content_type`
(4597–4606). Fixture (`$S/fxB`): `[Removed Associations] text/x-child=foo.desktop` plus
`[Added Associations] text/x-parent=foo.desktop`, queried with `text/x-child` → `gio mime`
prints `No default applications for “text/x-child”` — the *child's* removal suppressed the
*parent's* addition, which the spec's per-mimetype blacklist would not do. Control: the
addition alone at `text/x-parent` does list `foo.desktop` for `text/x-child` (the parent
fallback works), and adding at the child while removing at the parent keeps the child
addition, matching the spec's note. The candidate agrees with GLib here
(`default=none registered=- recommended=-`).

**(d) The spec's `[Added Associations]`/`[Removed Associations]` may only appear in the
non-desktop-specific file; GLib reads `[Default Applications]` from *every* file it
opens, including `mimeinfo.cache` and `defaults.list`.** Spec `associations.html`: "[Added
Associations] and [Removed Associations] groups may only appear in the non-desktop-specific
files"; `file.html`: desktop-specific files "can only be used for specifying the default
application". GLib enforces the first half with a `g_warning` (921–927, 947–953) and
honours the second — but it reads `DEFAULT_APPLICATIONS_GROUP` from every file it parses
(971–987), so a `[Default Applications]` group inside `mimeinfo.cache` or `defaults.list`
takes effect, which the spec does not describe. Note also that GLib's
`defaults.list` and `mimeinfo.cache` are read at all only for data dirs (1024–1025), and
that `mimeinfo.cache`'s `[Removed Associations]` group *is* honoured (945–969).

**(e) The spec's masking rule is "same directory or later"; GLib masks by directory
precedence of the *desktop file*, not of the list file.** Spec `associations.html`: "The
adding and removal of associations only applies to desktop files in the current directory,
or a later one (in precedence order)". GLib implements the same intent but by a different
mechanism: `desktop_file_dir_app_name_is_masked` (288–304) walks the directory array and
returns TRUE if *any earlier* directory's `app_names` contains the id. So an addition in a
low-precedence `mimeapps.list` is dropped when a same-named desktop file exists in a
higher-precedence directory, and the mask check is applied to additions and removals
alike (1331, 1343) but never to `[Default Applications]` (1350–1370).

## 3. Registry rows — draft for the L1 to integrate

Rows S504–S507 already exist in `corpus/SOURCES.md` (landed in commit `54a0683c`, the C1
commit) and their locators, hashes and quotes match what this seat independently opened
and re-hashed. The L1's own `sources-open-r91.txt` recorded the same ten hashes. Because
the item asks this seat to *draft* the rows and the write scope forbids editing
`corpus/SOURCES.md`, the rows are reproduced below as the located-quote draft the L1 can
use for the lesson Gate block, and each is annotated with what this seat verified.

Shape (11 columns, from the SOURCES.md header and rows S501–S503):
`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.

### S504 — GLib 2.90.1 desktop-application resolver (draft; already landed)

- **kind/tier**: `code` / `A`
- **source**: `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gdesktopappinfo.c`
  (sha256 `8e9ce1a8327a2daf6bc16e8dcfb653c482afde7bebc2ca2621747626b5495b0d`) and
  `…/gio/gio-tool-mime.c` (sha256 `40a450ec0ce177e61aae66175c02b3ebdb50aff1ec5ae65732cb800a60b2bd60`);
  host package `glib2 2.90.1-1`, `/usr/bin/gio` sha256 `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`
- **scope**: how GLib answers which application opens a MIME type — directory order,
  per-directory list files and groups, the blocklist, masking, the default and list
  algorithms, desktop-file loading, and what `gio mime` prints
- **anchor**: `gdesktopappinfo.c` 1624–1678 (dir order), 901–1042 (list files and groups),
  1312–1370 (lookups), 1894–2096 (load_from_keyfile), 2186–2216 (Hidden dropped),
  4552–4711 (type list and the three list impls), 4721–4784 (default lookup);
  `gio-tool-mime.c` 109–152
- **located quote (≤25 words, with lines)**: `gdesktopappinfo.c:1624-1678` — "First, the
  configs. Highest priority: the user's ~/.config … the user's ~/.local/share/applications"
  (1652, 1661); `gdesktopappinfo.c:4751` — "(If any), see if one of those apps is installed…";
  `gio-tool-mime.c:127` — "list = g_app_info_get_all_for_type (mimetype);"
- **teaches**: the default and list rules the C1 candidate copies, and the four places it
  departs from the spec (this report §2)
- **status/opened/recheck/used-by**: `mined` / `2026-11-06` / `180d` /
  `corpus/knowledge/mime-default-resolution-r91.md`

### S505 — GLib 2.90.1 shared-mime-info reader (draft; already landed)

- **kind/tier**: `code` / `A`
- **source**: `…/gio/gcontenttype-fdo.c` (sha256 `8a5b4f47…2d7c`),
  `…/gio/xdgmime/xdgmime.c` (sha256 `afb1c1c1…2410`), `…/xdgmimecache.c`
  (sha256 `ccda4366…db69`), `…/xdgmimealias.c` (sha256 `a1e67ae3…1394`), `…/xdgmimeparent.c`
  (sha256 `9c85c35f…5e3`); host `shared-mime-info 2.5.1-2`
- **scope**: how a MIME type is unaliased and its parents found — xdgmime's own directory
  list, cache vs text mode, alias/parent bsearch, `fgets` chunking, cache header and
  version gate
- **anchor**: `gcontenttype-fdo.c` 68–111, 116–139; `xdgmime.c` 129–213, 217–300, 331–346,
  735–746, 902–925; `xdgmimecache.c` 63–65, 108–160, 314–361, 1051–1130;
  `xdgmimealias.c` 83–101, 104–149; `xdgmimeparent.c` 88–107, 110–185
- **located quote (≤25 words, with lines)**: `xdgmime.c:737-738` — "if (_caches) return
  _xdg_mime_cache_unalias_mime_type (mime_type);"; `xdgmimecache.c:137` — "if (GET_UINT16
  (buffer, 0) != MAJOR_VERSION ||"; `xdgmimealias.c:94` — "entry = bsearch (&key,
  list->aliases, list->n_aliases,"
- **teaches**: the alias/parent model; in particular that a *cache* dir suppresses the
  text `aliases`/`subclasses` files, and that the host's cache header `00 01 00 02` puts
  this host in cache mode for `/usr/share/mime` and `~/.local/share/mime`
- **status/opened/recheck/used-by**: `mined` / `2026-11-06` / `180d` /
  `corpus/knowledge/mime-default-resolution-r91.md`

### S506 — GLib 2.90.1 shell parser and program lookup (draft; already landed)

- **kind/tier**: `code` / `A`
- **source**: `…/glib/gshell.c` (sha256 `640a0d0f…0442`), `…/glib/gutils.c`
  (sha256 `65086c29…3771`)
- **scope**: how a desktop file's `Exec`/`TryExec` are judged loadable
- **anchor**: `gshell.c` 65–, 272–, 434–657, 658–730; `gutils.c` 300–519, 2597–2618, 1876–1888
- **located quote (≤25 words, with lines)**: `gutils.c:363-364` — "if (g_path_is_absolute
  (original_program)) return NULL;"; `gshell.c:534-536` — "case '#': if (p == command_line)"
- **teaches**: `g_find_program_for_path` and `g_shell_parse_argv` semantics the C1
  candidate ports
- **status/opened/recheck/used-by**: `mined` / `2026-11-06` / `180d` /
  `corpus/knowledge/mime-default-resolution-r91.md`

### S507 — freedesktop MIME Applications Associations spec 1.0.1 (draft; already landed)

- **kind/tier**: `spec` / `A`
- **source**: `https://specifications.freedesktop.org/mime-apps-spec/latest/` — index.html
  sha256 `12ddf2cc…826b`, file.html `65c6378e…1a6b`, associations.html `77a4843a…013a`,
  default.html `00b5c8f3…77ec6`
- **scope**: the documented contract for `mimeapps.list` — lookup order, desktop-specific
  files, added/removed associations, the default-application algorithm
- **anchor**: `file.html` (file list, 34–55); `associations.html` (groups, 38–54);
  `default.html` (§4)
- **located quote (≤25 words, with lines)**: `default.html` — "Note as well that the
  default application for a given type must be an application that is associated with the
  type."; `associations.html:45` — "The adding and removal of associations only applies to
  desktop files in the current directory, or a later one"
- **teaches**: the contract GLib departs from — this report §2 lists all five departures
- **status/opened/recheck/used-by**: `mined` / `2026-11-06` / `180d` /
  `corpus/knowledge/mime-default-resolution-r91.md`

No literal or escaped `|` appears inside any cell above. No row is added for
`glib/gkeyfile.c`: it is already registered as **S502** with the identical sha256
`e1d1270f…656`, and re-registering it would duplicate a row.

## 4. Statements in the declaration draft and the candidate docstring that the opened
source contradicts

**(i) The frozen declaration's C2 premise is too strong — and this very seat proves it.**
`claims-declaration-r91.md:92-93` says: "No lane check reads a dispatch's `Report:`
trailers: at `cc0381db` `quality/check-receipt-presence.py` and `quality/check-deliverables.py`
say nothing about seat reports." The second half is false. At `cc0381db`,
`quality/check-deliverables.py` already parses the `Report:` trailer —
line 34 `TRAILER = re.compile(r'^Report:\s*`?([A-Za-z0-9_.][A-Za-z0-9_./+-]*\.md)`?\s*$', re.M)`,
line 39 `for m in TRAILER.finditer(text):` — and proves the named file exists at the
revision with `git cat-file -e` (line 114), failing with `status=ABSENT` and
`verdict=FAIL` (124, 146, 150). Reproduced: running the base `cc0381db` copy of
`check-deliverables.py` against a report whose trailer names a nonexistent path prints
`REPORT_UNRESOLVED rev=cc0381db report=…` and
`CHECK101: reports=0 declared=0 exists=0 absent=1 undeclared=0 verdict=FAIL` (exit 1).

What `check-deliverables.py` does *not* do is discover seats from a dispatch that produced
no report at all — it only checks the reports handed to it on the command line. That is
the real gap C2 closes, and it is narrower than "no lane check reads `Report:` trailers".
The correction for the L1: restate C2's premise as "no lane check enumerates a wave's
dispatched seats and flags a seat whose report file is absent", which is exactly what
`quality/check-seat-reports.py` now does.

**(ii) The same gap, observed on the live lane, is why this seat's report was missing.**
The landed C2 gate run against the worktree
(`python3 -I quality/check-seat-reports.py --worktree --round 91`) prints:

```
SR01 missing round-91/r1 R91MResidC1 .ufo/waves/round-91/r1/R91MResidC1.md
SR01 missing round-91/r1 R91MResidC2 .ufo/waves/round-91/r1/R91MResidC2.md
SR01 missing round-91/w1 R91MScoutSources .ufo/waves/round-91/w1/R91MScoutSources.md
SEAT_REPORTS: mode=worktree rev=worktree rounds=1 waves=2 seats=16 trailered=16 present=13 missing=3 empty=0 unsafe=0 untrailed=0 verdict=MISSING
```

(exit 1). `R91MScoutSources` is this seat: the w1 round ran 16 seats, 13 reported, and
three did not — **including this scout**. Round 90's M90-4 ("a seat without a report file
is a dead seat in the evidence") has now repeated inside round 91 itself, one wave after
the round that set out to close it. This report file is the seat's own remedy; the two
`r1` residual seats (`R91MResidC1`, `R91MResidC2`) are the L1's to chase. Note the
counter's `all` expectation at the base revision already expects `rc=1` with
`sr01=133`, so the "missing" verdict is the *expected* steady state at `cc0381db`, not a
new regression — but it is a live, unreported dead seat now.

**(iii) The candidate docstring's file-order model is right; its `MimeType=` model is
missing.** `.ufo/waves/round-91/build/mado-mime.c1.py:20-27` describes the per-dir list
files and says "Each key is unaliased; additions skip ids already removed in this dir and
removals skip ids already added (expand_strv :855-898, read_mimeapps_list :901-990)". The
line numbers are right and the unaliasing is right (`read_mimeapps_list` stores under the
*unaliased* key via `desktop_file_dir_unindexed_get_tweaks` → `_g_unix_content_type_unalias`,
837–848). But the docstring never mentions that `MimeType=` lines in `.desktop` files are
not consulted at all — only `mimeinfo.cache`'s `[MIME Cache]` group is (source 1036–1041).
Since `gio mime`'s "Registered applications" list is exactly the `MimeType=`-derived set
in the spec's algorithm, a reader of the docstring would predict a `MimeType=`-only
desktop file to be registered; `gio` says it is not (§2(b) above). The docstring's
`lists out` line does say "registered = additions over the type and its ancestors", which
is consistent with the source but does not say *where* additions come from.

**(iv) The candidate docstring's `expand_strv` summary is incomplete in a way that
matters.** Line 25–26 says "additions skip ids already removed in this dir and removals
skip ids already added". The source's `expand_strv` (855–898) does exactly that — but only
for the *second and later* expansion of a given key: the first expansion short-circuits at
863–867 (`if (!*strv_ptr) { *strv_ptr = to_add; return; }`) and takes the list as is,
**without** consulting the blocklist. The candidate reproduces this faithfully in code
(`_expand`, 611–624: `if cur is None: return list(add)`), so this is a docstring
imprecision, not a code defect.

**(v) A claim in the declaration draft that the opened sources support.** "Labels: the
default id, and when gio prints one, the registered and recommended lists in order
(gio-tool-mime.c prints the lists only after a default)." Verified at
`gio-tool-mime.c:115-152`: when `g_app_info_get_default_for_type` returns NULL the tool
prints `No default applications for …` and stops; the two lists are printed only in the
`else` branch. The C1 candidate's docstring states the same asymmetry ("gio mime prints
the two lists only after a default; this tool always computes them") and it is correct.

**(vi) The declaration's host-evidence figure checks out.** The draft says "every MIME
type named in the host's mimeinfo.cache/mimeapps.list files … draft 538/538 agree". Counting
the distinct type names in `/usr/share/applications/mimeinfo.cache` (522),
`~/.local/share/applications/mimeinfo.cache` (149) and `~/.config/mimeapps.list` (56) with
a strict `[A-Za-z0-9.+-]+/[A-Za-z0-9.+_-]+` key pattern gives a **union of 538** distinct
types — the draft's number, reproduced.

## 5. Residual gaps

- The spec's own §2 file list (`file.html` 34–55) is eight `mimeapps.list` paths; GLib's
  `defaults.list` and `mimeinfo.cache` are not in it and are marked deprecated by the
  source itself (1027–1031: "it has never been part of any spec"). The landed S507 row
  already notes `defaults.list` and `mimeinfo.cache`; this report adds the source line.
- `xdg_mime_init_from_directory` reads `globs`, `globs2`, `magic`, `icons` and
  `generic-icons` as well (157–210). None of these affect default-application
  resolution, so the candidate's silence on them is correct for C1's scope; flagged so
  the L1 does not read the candidate's file list as exhaustive of the MIME database.
- The host's `~/.local/share/mime/` has `aliases` and `subclasses` files, but the host is
  in **cache mode** there (a `mime.cache` with header `00 01 00 02` exists), so those
  text files are not read on this host (xdgmime.c 137–153 returns early on a cache dir).
  The candidate's `MimeDB` implements this rule (`if os.path.exists(cpath): … continue`),
  matching the source.

## Commands run (all exit 0 unless noted)

```
curl -sSL <10 GLib 2.90.1 raw paths>      x2 into $S/fetch1, $S/fetch2
cmp -s $S/fetch1/f <f> $S/fetch2/f        x10   → all identical
sha256sum $S/fetch1/*.c                   → table in §0
curl -sSL <4 spec pages>                  → sha256 table in §0
grep -n -E '<symbols>' <each fetched .c>  → line ranges in §1
awk 'NR>=a&&NR<=b' <each fetched .c>      → context reads for §1/§2
env -i … gio mime <one type>              → fixture probes §2 (read form only, one type arg)
env -i … python3 .ufo/waves/round-91/build/mado-mime.c1.py <one type> → candidate cross-checks
python3 -I quality/check-seat-reports.py --worktree --round 91   → exit 1, SR01 x3
python3 -I $S/chk/check-deliverables-base.py --repo . --rev cc0381db --report … → exit 1, verdict=FAIL
pacman -Q glib2 shared-mime-info          → glib2 2.90.1-1, shared-mime-info 2.5.1-2
```

No tool was installed. No mutating git or jj command was run. No `gio mime` was run with
a second argument; no `xdg-mime`, `xdg-settings`, `update-desktop-database`, `xdg-open`,
`gio open` or `gtk-launch` was run; no service, sysctl or sudo action was taken. The
fixture trees live entirely under `$S` and are deleted on exit by this seat.

Report: .ufo/waves/round-91/w1/R91MScoutSources.md
