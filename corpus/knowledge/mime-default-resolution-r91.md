source: S504 (GLib 2.90.1 gio/gdesktopappinfo.c sha256 8e9ce1a8…5b0d, gio/gio-tool-mime.c 40a450ec…bd60), S505 (gio/gcontenttype-fdo.c and gio/xdgmime/{xdgmime,xdgmimecache,xdgmimealias,xdgmimeparent}.c), S506 (glib/gshell.c, glib/gutils.c), S502 (glib/gkeyfile.c e1d1270f…f656), S507 (freedesktop mime-apps spec 1.0.1); full digests in corpus/SOURCES.md and `.ufo/waves/round-91/receipts/sources-open-r91.txt`
covers: which `.desktop` application GLib 2.90.1 opens a MIME type or URI scheme with — the directory order, the per-directory mimeapps files and groups, the blocklist, masking, the default and list algorithms, desktop-file loading, the MIME database reader, the GKeyFile byte rules — and this host's answers
verified-at: 2026-11-06 — tools/mado-mime.py = the frozen candidate `.ufo/waves/round-91/build/mado-mime.c1.py` (sha256 2532ccb5…1a5e, frozen at fa71279fc927f86df2d14a62f1f60230a7cf4ada); pre-freeze draft on the frozen 268 cases `.ufo/waves/round-91/receipts/c1-controls-prefreeze-r91.txt`; host replay 1211/1211 `.ufo/waves/round-91/receipts/host-run-r91.txt`; the measured receipt is named in SCORECARD round 91
recheck: 90d — re-pull the ten files at the next GLib tag that changes gdesktopappinfo.c, gkeyfile.c or xdgmime; also when `glib2` leaves 2.90.1-1 or `shared-mime-info` leaves 2.5.1-2.

# GLib 2.90.1 default-application resolution: which `.desktop` opens a MIME type

This entry states how GLib 2.90.1 answers "which application opens this MIME type" — the question
`gio mime TYPE`, `xdg-open`, file managers and portals' OpenURI all reduce to
`g_app_info_get_default_for_type()`. It names the directories searched, the per-directory file and group
order, the default algorithm, the two list algorithms, the desktop-file load rules, the MIME-database alias
and parent rules, and what this host answers. Line numbers are those of GLib tag 2.90.1 (`gio/gdesktopappinfo.c`
is shortened to `gdesktopappinfo.c`; `gio/gcontenttype-fdo.c` to `gcontenttype-fdo.c`; `gio/xdgmime/*` to
`xdgmime*.c`).

Scope: the *resolution* decision, read-only. Not in scope: launching the application, whether it starts,
D-Bus activation, portals, `xdg-open`'s own fallbacks beyond this call, and MIME sniffing.

## 1. The plane

- Three public answers exist (`gio/gio-tool-mime.c:109-152`): the default (`g_app_info_get_default_for_type`,
  :115), the registered list (`g_app_info_get_all_for_type`, :127) and the recommended list
  (`g_app_info_get_recommended_for_type`, :140).
- `gio mime TYPE` prints the default, then the two lists; with no default it prints only
  `No default applications for “TYPE”` and no lists (:115-152). The lists are therefore *unobservable*
  through gio when there is no default.
- A URI scheme is the same question on the synthetic type `x-scheme-handler/<lowercased-scheme>`
  (gdesktopappinfo.c:4787-4809).
- Default resolution reads no trait of the file being opened beyond its MIME type: no glob, magic or icon
  lookup takes part (the type is given).

## 2. The search order

`desktop_file_dirs_lock` builds the directory list once (gdesktopappinfo.c:1624-1679):

| # | directory | contents | upstream |
|---|---|---|---|
| 1 | `$XDG_CONFIG_HOME` (default `~/.config`) | config only: `*-mimeapps.list` and `mimeapps.list`; **no desktop files** | :1653, :1415-1431 |
| 2 | each `$XDG_CONFIG_DIRS` entry (default `/etc/xdg`) | config only, same files | :1657-1659 |
| 3 | `$XDG_DATA_HOME` (default `~/.local/share`) + `/applications` | `*.desktop`, `*-mimeapps.list`, `mimeapps.list`, `defaults.list`, `mimeinfo.cache` | :1662, :1395-1413 |
| 4 | each `$XDG_DATA_DIRS` entry (default `/usr/local/share:/usr/share`) + `/applications` | same as 3 | :1666-1668 |

Earlier entries win: masking (§6) and the id lookup (§4) both walk this order. An empty `XDG_DATA_DIRS` or
`XDG_CONFIG_DIRS` falls back to the compiled default (glib/gutils.c:2605-2607, :2703-2706). The config
directories take part in *list* processing only — `desktop_file_dir_unindexed_init` skips
`get_apps_from_dir` for them (:1045-1052), and `read_mimeapps_lists` stops after `mimeapps.list` (:1023-1026).

Desktops come from `XDG_CURRENT_DESKTOP`, split on `:`; a token is dropped when empty or when it carries a
byte other than `[A-Za-z0-9_-]`, and survivors are ASCII-lowercased (gdesktopappinfo.c:312-377). The
lowercased list is used for `<desktop>-mimeapps.list` (:1011) — so `Hyprland` looks for
`hyprland-mimeapps.list` (case d05: a `Hyprland-mimeapps.list` is not read).

## 3. Per-directory file order and groups

`desktop_file_dir_unindexed_read_mimeapps_lists` (:993-1043) reads, in this order, every existing file:

| file | groups read | groups ignored (warning) | upstream |
|---|---|---|---|
| `<desktop>-mimeapps.list`, one per desktop in order | `[Default Applications]` | `[Added Associations]`, `[Removed Associations]` | :1011-1014, :921-930, :947-956 |
| `mimeapps.list` | `[Added Associations]`, `[Removed Associations]`, `[Default Applications]` | — | :1017-1019 |
| `defaults.list` (data dirs only) | `[Default Applications]` | `[Added Associations]`, `[Removed Associations]` | :1032-1034 |
| `mimeinfo.cache` (data dirs only) | `[MIME Cache]` **as additions**, `[Removed Associations]`, `[Default Applications]` | — | :1039-1041 |

Inside one file the group order is fixed — additions, then removals, then defaults — whatever the textual
order (case l06: `[Removed Associations]` before `[Added Associations]`; the addition still counts and the
removal of the same id is skipped).

Per-key processing (`read_mimeapps_list`, :901-990):
- The key is **unaliased** before it is stored (`get_tweaks`, :833-853; `_g_unix_content_type_unalias` at
  :839), so a `text/x-old=…` key lands on `text/plain` (case x02).
- `g_key_file_get_string_list` splits on `;`; a value that is not a valid string list skips that key only
  (case k02, §5).
- Additions are appended unless the id is already in this directory's removals or already present
  (`expand_strv`, :855-898). Removals are appended unless the id is already in this directory's additions.
  Defaults have no blocklist (:982).

## 4. The default algorithm, step by step

`g_app_info_get_default_for_type_impl` (:4722-4784):

1. Build the type list: the request unaliased once, then breadth-first ancestors
   (`get_list_of_mimetypes`, :4552-4588; see §7 for how the BFS also advances an alias chain).
2. For each type in that order, collect into one ordered, duplicate-free list:
   a. every directory's `[Default Applications]` ids for the type, directories in §2 order
      (`desktop_file_dir_default_lookup`, :1351-1368);
   b. then every directory's additions for the type, skipping an id that is masked by a higher-precedence
      directory, blocklisted, or already collected (`desktop_file_dir_unindexed_mime_lookup`, :1312-1349);
      each directory's removals join a blocklist that **survives into later ancestors** (:4770-4773).
3. Walk that list in order; for each id, walk the directories in order and take the first directory that has
   a file of that name **and** whose file loads (`desktop_file_dir_get_app`, :1533-1540; called at :4758).
   That app is the answer. `Hidden=true` is not consulted here (§8.1).
4. If no id of this type resolves, clear the collected ids, keep the blocklist, and repeat for the next
   ancestor (:4770-4773). Nothing left → NULL.

Consequences worth naming:
- *All* directories' defaults outrank *all* directories' additions: a system `defaults.list` default beats a
  user `[Added Associations]` entry (case l15: default `c.desktop`, registered `a.desktop`).
- A default id need not be installed in the directory that named it; step 3 re-resolves it from the top
  (case m02: a user `Type=Link` copy masks the id from the lists, yet the default still loads the system copy).
- `[Default Applications]` in a config directory needs no desktop file there; it is a pure pointer.

## 5. The two lists

Both are built by `g_desktop_app_info_get_desktop_ids_for_content_type` (:4590-4626): for each type of the
list, for each directory in §2 order, the same additions collector as §4.2b is run into one ordered list.

- **registered** = types with ancestry (`include_fallback` TRUE, :4600; `g_app_info_get_all_for_type_impl`,
  :4688-4710).
- **recommended** = the unaliased request only (`include_fallback` FALSE; `g_app_info_get_recommended_for_type_impl`,
  :4623-4645). Hence recommending is a strict first-type subset of registering: a parent's association is
  registered but never recommended (case x04).
- Each id is then loaded with `g_desktop_app_info_new` (:2186-2216): first directory holding the name, and
  the id is **dropped when that copy is `Hidden=true` or fails to load** (:2209-2213).

Order: type-major, then directory, then position inside the value; duplicates suppressed by `array_contains`.
`mimeinfo.cache` values with a trailing `;` therefore end cleanly (the trailing empty piece is dropped,
`g_key_file_get_string_list`, glib/gkeyfile.c:4780-4790), while `a.desktop; a.desktop` yields the pieces
`a.desktop` and ` a.desktop`: only the value's leading whitespace is chugged (glib/gkeyfile.c:1755-1758), so a
space after a separator belongs to the next piece.

## 6. Loading a desktop file

`g_desktop_app_info_load_from_keyfile` (:1894-2096) rejects a file unless, in order:
1. the **first group** is exactly `[Desktop Entry]` (:1904-1909; case m06 — `[Other]` first voids it);
2. `Type=Application` (:1911-1917; case m05 — `Type=Link` is not an application);
3. `Path=`, `TryExec=`, `Exec=` are readable as strings (an invalid escape in one of them voids the file,
   :1919-1983);
4. a non-empty `TryExec=` resolves as a program (:1929-1951);
5. a non-empty `Exec=` is shell-parsable and its `argv[0]` resolves as a program (:1953-1983). `Exec=` empty
   or all-blank loads (leading whitespace is chugged, glib/gkeyfile.c:1755-1758; case p09).
6. `Hidden=` is recorded (:2022), not acted on here.

Program resolution is `g_find_program_for_path(program, NULL, working_dir=Path)` (S506 glib/gutils.c:300-520):
a relative name is first joined to `Path=`; a name that is then absolute, or that contains `/`, is tested
directly — `access(X_OK)` and not a directory, any file type (a FIFO with mode 755 counts) — and on a miss an
**absolute** name fails (:363-366) while any other name falls through to the `$PATH` search with the original
name (:368; `Exec=tools/prog` finds `$PATH-entry/tools/prog`, case sh-23). `PATH` unset means
`/bin:/usr/bin:.` (:388); an empty element is the bare name, relative results join `Path=`. The command line
is split by `g_shell_parse_argv` (S506 glib/gshell.c `tokenize_command_line` :434-640, `g_shell_unquote`
:272-333, `unquote_string_inplace` :65-185): `#` starts a comment only at the start or after a space or
newline (:534-552; `Exec=sh#x` names the program `sh#x`, case sh-01), only space, tab and newline delimit
(:499-512; a CR stays in the word, case sh-15), backslash-newline outside quotes is dropped, and inside double
quotes only `"` `\` `` ` `` `$` and newline are escapable (:108-121). Because GKeyFile decodes escapes *before*
the shell parser runs, `Exec=my\sprog %f` becomes `my prog %f` and then splits into two words, so the program is
not found (case p10). `Hidden=` is true only for `true` or `1` followed by nothing but `g_ascii_isspace` bytes
(S502 gkeyfile.c:4979-5004; `\v` is not one, `\f` is — cases sh-38, sh-65).

Masking (`desktop_file_dir_app_name_is_masked`, :283-306) is name-only: a *higher-precedence directory whose
`applications` listing contains the same name* masks the id, whether or not that higher file loads. It is
consulted by the additions collector (:1312-1349) and `get_all` (:1081-1111), never by `get_app` (:1533-1540).

## 7. The MIME database: aliases and parents

- The mime directories come from **xdgmime's own `getenv`**, not from GLib's defaults (S505 xdgmime.c
  `xdg_init_dirs` :217-300): `$XDG_DATA_HOME/mime/` if the variable is set (even empty), else
  `$HOME/.local/share/mime/`; then each **non-empty** `$XDG_DATA_DIRS` element + `/mime/` — an unset
  `XDG_DATA_DIRS` means `/usr/local/share/:/usr/share/` (:231), a set-but-empty one means none (:279), while the
  desktop-file side (§2) falls back to the default for an empty value. Case rv-04: with `XDG_DATA_DIRS=""` gio
  reads only the user `aliases` file. Config directories take no part.
- Per directory, `xdg_mime_init_from_directory` (xdgmime.c:129-230) tries `mime.cache` first: if it loads, the
  directory is a **cache dir** and its text files are not read (:136-152, `return FALSE`). A cache loads only
  when the file is at least 40 bytes, `major == 1` and `minor` in 1..2 (xdgmimecache.c:59-65, :108-160).
- The cache switch is **global**: when any directory has a loadable cache, aliases and parents come from the
  caches only — `_xdg_mime_unalias_mime_type` returns `_xdg_mime_cache_unalias_mime_type` (xdgmime.c:735-747)
  and `xdg_mime_list_mime_parents` returns the cache list (xdgmime.c:902-926). Text `aliases`/`subclasses` in
  other directories are then ignored (case x08).
- Text mode: every directory's `aliases` and `subclasses` are read in directory order (xdgmime.c:190-201) with
  `fgets(line, 255, …)` — `#` is a comment, the first space splits, and the target's **last byte is chopped
  unconditionally** (xdgmimealias.c:104-149, xdgmimeparent.c:110-185). A file whose last line has no final
  newline therefore loses the last character of that target (case x13: `app/x app/zz` yields parent `app/z`).
  Parent rows for the same type are appended across directories (:139-170). Alias rows from every `aliases`
  file are appended to one array that is `qsort`ed after **each** file (xdgmimealias.c:104-149, qsort at :147)
  and searched with `bsearch` (:94): for an alias defined more than once, the C library's sort and search decide
  which target wins. `tools/mado-mime.py` calls the same `qsort`/`bsearch` through ctypes, file by file, so it
  picks the entry GLib picks on the same host (cases w07-w09: `app/q` listed in two files resolves to the second
  file's target on this glibc 2.44).
- **Unalias is one lookup, not a loop** (xdgmime.c:735-747; cache path xdgmimecache.c:1051-1062). But
  `get_list_of_mimetypes` grows its list with `_g_unix_content_type_get_parents(element)`
  (gcontenttype-fdo.c:83-110), whose first entry is `unalias(element)`; for an element that is itself an alias
  target this is a second hop, so a chain `app/x → app/y → app/z` yields the type list `[app/y, app/z]`
  (case x11: default `a.desktop`, registered `a.desktop,b.desktop` — `b` comes from the `app/y` key having
  been unaliased into `app/z` when the cache file was read, §3).
- Parent order: text file order per directory, directory order across directories; cache mode unions the
  caches in directory order and stops at 127 parents (xdgmimecache.c:1064-1130).

## 8. Quirks

1. **A `Hidden=true` default is accepted.** The default path never asks about `Hidden` (:1533-1540, :4758);
   only the two lists drop it (:2209-2213). Case l20: default `a.desktop`, registered/recommended `b.desktop`
   only.
2. **An unloadable higher-precedence file masks a lower id.** Masking is name-only (:283-306), so a user
   `a.desktop` that is not even a key file hides the system `a.desktop` from the lists and from a cache
   addition, and with no default the answer is nothing (case m14; also m01, o02).
3. **`<desktop>-mimeapps.list` reads only `[Default Applications]`.** `[Added Associations]` there is dropped
   with a warning (:921-930), so it cannot add an association at all (case l08: no default, no lists); its
   `[Default Applications]` does work (case l09). Same for `[Removed Associations]` (:947-956).
4. **The alias chain is not followed by unalias, but the type BFS still walks it one hop per element** (§7;
   case x11). Do not describe the resolver as "follows aliases transitively", and do not describe it as
   "ignores chains" either.
5. **`defaults.list` only contributes `[Default Applications]`** (:1032-1034; case l10 reads it, case l11's
   `[Added Associations]` there is ignored).
6. **Within one file, additions outrank removals** (:938 before :964; case l06).
7. **A lower-precedence removal cannot remove a higher-precedence addition** (the removal is skipped when the
   id is already in the collected hits, :1312-1349; case l17).
8. **Cache mode is all-or-nothing** (§7; case x08).
9. **`Encoding=` in the first group voids the whole file.** GKeyFile rejects any first-group `Encoding=` other
   than `UTF-8` (glib/gkeyfile.c:1768-1782), and the loader then skips the file (case k06).
10. **`Exec=` escapes are decoded twice** (GKeyFile, then `g_shell_parse_argv`), so `\s` never survives as an
    escaped space (case p10).
11. **A subdirectory prefixes the id with its name and `-`** (`get_apps_from_dir`, :769-818): `vendor/a.desktop`
    is `vendor-a.desktop`, `v/w/a.desktop` is `v-w-a.desktop` (cases m07, m08).

## 9. Decision table

Every row is an L1 case of `.ufo/waves/round-91/controls/mime-cases-r91-l1.json` (schema `mime-cases-r91-v1`)
with gio's own label copied from that file: `default; registered; recommended`, where `null` is what gio
prints when it prints no default and therefore no lists.

| # | state | result (gio label) | upstream | case |
|---|---|---|---|---|
| 1 | user `[Default Applications]` vs cache addition | `b.desktop; [a.desktop,b.desktop]; [a.desktop,b.desktop]` | :1653, :4743-4753 | l02 |
| 2 | only `mimeinfo.cache` adds | `a.desktop; [a,b]; [a,b]` | :1039-1041, :1312-1349 | l01 |
| 3 | `[Removed Associations]` blocks a cache addition | `b.desktop; [b]; [b]` | :964, :1312-1349 | l05 |
| 4 | added and removed in one file, removed first textually | `b.desktop; [b,a]; [b,a]` | :938, :964 | l06 |
| 5 | removal in a lower dir, addition in a higher dir | `a.desktop; [a,c]; [a,c]` | :1312-1349 | l17 |
| 6 | user config default vs system config default | `a.desktop; []; []` | :1653 vs :1657 | l14 |
| 7 | system config default vs user addition | `c.desktop; [a]; [a]` | :4743-4753 | l15 |
| 8 | config dirs in `XDG_CONFIG_DIRS` order | `a.desktop; []; []` | :1657-1659 | o01 |
| 9 | data dirs in order, additions append | `b.desktop; [b,a]; [b,a]` | :1666-1668 | o03 |
| 10 | earlier data dir holds an unloadable copy | `b.desktop; [b]; [b]` | :283-306 | o02 |
| 11 | default id not installed, another default follows | `c.desktop; []; []` | :4756-4770 | l03 |
| 12 | default id not installed, additions follow | `a.desktop; [a]; [a]` | :4756-4770 | l04 |
| 13 | `defaults.list` `[Default Applications]` | `b.desktop; []; []` | :1032-1034 | l10 |
| 14 | `defaults.list` `[Added Associations]` | `null` | :1032-1034 | l11 |
| 15 | `<desktop>-mimeapps.list` `[Added Associations]` | `null` | :921-930 | l08 |
| 16 | `<desktop>-mimeapps.list` `[Default Applications]` | `c.desktop; []; []` | :1011-1014 | l09 |
| 17 | desktop order `hyprland` before `gnome` | `b.desktop; []; []` | :1011, :356-377 | d01 |
| 18 | `Hyprland-mimeapps.list` (mixed case) | `null` | :356-377 | d05 |
| 19 | default names a `Hidden=true` app | `a.desktop; [b]; [b]` | :1533-1540, :2209-2213 | l20 |
| 20 | user file is not a key file, masks the system copy | `null` | :283-306 | m14 |
| 21 | default id also masked, but a lower copy loads | `a.desktop; []; []` | :1533-1540 | m02 |
| 22 | `Type=Link` | `b.desktop; [b]; [b]` | :1911-1917 | m05 |
| 23 | first group is `[Other]` | `b.desktop; [b]; [b]` | :1904-1909 | m06 |
| 24 | subdirectory desktop file | `vendor-a.desktop; [vendor-a]; [vendor-a]` | :769-818 | m07 |
| 25 | `TryExec=` names a missing program | `b.desktop; [b]; [b]` | :1929-1951 | p01 |
| 26 | `Exec=` names a missing program | `b.desktop; [b]; [b]` | :1953-1983 | p03 |
| 27 | `Exec='sh' %f` (quoted program) | `a.desktop; [a]; [a]` | glib/gshell.c:293-320 | p06 |
| 28 | `Exec=sh "%f` (unbalanced quote) | `b.desktop; [b]; [b]` | glib/gshell.c:82-83 | p05 |
| 29 | key before any group in `mimeapps.list` | `a.desktop; [a]; [a]` | glib/gkeyfile.c:1711-1725, :1638-1649 | k01 |
| 30 | invalid escape in one value | `text/plain → a.desktop; [a]; [a]`, `image/png → c.desktop; []; []` | glib/gkeyfile.c:4740-4760 | k02 |
| 31 | first-group `Encoding=ISO-8859-1` | `a.desktop; [a]; [a]` | glib/gkeyfile.c:1768-1782 | k06 |
| 32 | trailing space in an id | `a.desktop; [a]; [a]` | glib/gkeyfile.c:1755-1760 | k10 |
| 33 | CRLF line endings | `c.desktop; []; []` | glib/gkeyfile.c:1851-1867 | k11 |
| 34 | alias `text/x-old → text/plain` | `b.desktop; [b]; [b]` | xdgmime.c:735-747 | x01 |
| 35 | alias key in `[Default Applications]` | `c.desktop; []; []` (both `text/plain` and `text/x-old`) | :839 | x02 |
| 36 | parent type carries the association | `a.desktop; [a]; []` | :4600, :4623-4645 | x03 |
| 37 | parent has its own association | `b.desktop; [b,a]; [b]` | :4552-4588 | x04 |
| 38 | two parents, file order | `a.desktop; [a,b]; []` | xdgmimeparent.c:110-185 | x05 |
| 39 | grandparent reached breadth-first | `c.desktop; [c,a]; []` | :4552-4588 | x06 |
| 40 | removed id stays blocked in the ancestor | `b.desktop; [b]; []` | :4771-4774 | x07 |
| 41 | cache dir present, text `subclasses` beside it | `text/x-c a.desktop; []; []`, `text/x-d null` | xdgmime.c:136-152, :739-746 | x08 |
| 42 | alias chain `app/x → app/y → app/z` | `a.desktop; [a,b]; []` | xdgmime.c:735-747, gcontenttype-fdo.c:83-110 | x11 |
| 43 | `subclasses` last line without final newline | `a.desktop; [a]; []` (parent chopped to `app/z`) | xdgmimeparent.c:127-138 | x13 |

## 10. How to run the resolver on the host

`tools/mado-mime.py` (lanes: landed from `.ufo/waves/round-91/build/mado-mime.c1.py` after the freeze) is
read-only: it opens only `mimeapps.list`, `<desktop>-mimeapps.list`, `defaults.list`, `mimeinfo.cache`,
`*.desktop` and `mime/{mime.cache,aliases,subclasses}` under the searched roots, and stats `$PATH` entries.
It writes no configuration file, launches nothing, and `--selftest` writes only to a temporary directory.

```sh
python3 -I tools/mado-mime.py text/plain
python3 -I tools/mado-mime.py --json image/png application/pdf x-scheme-handler/https
python3 -I tools/mado-mime.py --desktop GNOME text/html      # override XDG_CURRENT_DESKTOP
python3 -I tools/mado-mime.py --desktop-unset text/html      # as if XDG_CURRENT_DESKTOP were unset
python3 -I tools/mado-mime.py --config-dirs /etc/xdg --data-dirs /usr/share --path /usr/bin:/bin text/plain
python3 -I tools/mado-mime.py --selftest
```

Output (exit 0): one header `MADO_MIME_DIRS: desktops=… config=… data=…` then one line per type,
`MADO_MIME: <type> default=<id>|none registered=<id,…>|- recommended=<id,…>|-`; `--json` prints
`{"desktops":…, "dirs":…, "results":[{"type","default","registered","recommended"}…]}`. Exit 2 is a setup
error (no type named). The tool always computes both lists; `gio mime` prints them only when a default exists
(§1), so compare defaults always and lists only where gio prints them.

## 11. This host, 2026-11-06

Environment as the session sees it: `XDG_CURRENT_DESKTOP=Hyprland`, `XDG_CONFIG_HOME=~/.config`,
`XDG_CONFIG_DIRS=/etc/xdg`, `XDG_DATA_HOME=~/.local/share`, `XDG_DATA_DIRS=/usr/local/share:/usr/share`.

Inputs present (read-only reads; hashes re-taken by the L1): `~/.config/mimeapps.list` (sha256 `d6c81c26…`),
`~/.config/hyprland-mimeapps.list` (111 B), `~/.local/share/applications/mimeinfo.cache` (`222054e7…`),
`/usr/share/applications/mimeinfo.cache` (`122aa7cc…`); `/etc/xdg/mimeapps.list` and `/usr/local/share/applications`
do not exist; `/usr/share/mime/mime.cache` exists (`b988d3d2…`, version 1.2), so this host is in **cache mode** — its
`aliases`/`subclasses` text files are not consulted (§7).

Host replay (QUALITY 146), the landed tool's bytes (sha256 `2532ccb5…`) against one `gio mime TYPE` call per type,
live environment, every type the host's lists and `/usr/share/mime/{aliases,subclasses}` name
(`.ufo/waves/round-91/receipts/host-run-r91.txt`): `types=1211 agree=1211 semantic_diff=0 default_none=122` — for
the 122 types with no default gio prints no lists and the tool answers `none` (§1). The tool printed no refusal: it
has no refusal path; a construct outside the model resolves as the model reads it (§12).

| type | default | registered | recommended |
|---|---|---|---|
| `text/plain` | `nvim.desktop` | `libreoffice-writer.desktop, nvim.desktop` | `libreoffice-writer.desktop, nvim.desktop` |
| `text/x-c` | `nvim.desktop` | `nvim.desktop, libreoffice-writer.desktop` | `nvim.desktop` |
| `text/x-python` | `nvim.desktop` | `libreoffice-writer.desktop, nvim.desktop` | — |
| `image/png` | `imv.desktop` | `imv.desktop, chromium.desktop, com.github.PintaProject.Pinta.desktop, imv-dir.desktop, krita_png.desktop, org.kde.kdenlive.desktop, satty.desktop` | same as registered |
| `application/pdf` | `org.gnome.Evince.desktop` | `chromium.desktop, com.github.xournalpp.xournalpp.desktop, krita_pdf.desktop, libreoffice-draw.desktop, obsidian.desktop, org.gnome.Evince.desktop, org.gnome.Papers.desktop, org.inkscape.Inkscape.desktop` | same as registered |
| `text/html` | `chromium.desktop` | `chromium.desktop, libreoffice-writer.desktop, nvim.desktop` | `chromium.desktop` |
| `video/mp4` | `mpv.desktop` | `mpv.desktop, org.kde.kdenlive.desktop` | `mpv.desktop, org.kde.kdenlive.desktop` |
| `inode/directory` | `org.gnome.Nautilus.desktop` | `org.gnome.Nautilus.desktop` | `org.gnome.Nautilus.desktop` |
| `application/zip` | `org.gnome.Nautilus.desktop` | `org.gnome.Nautilus.desktop` | `org.gnome.Nautilus.desktop` |
| `x-scheme-handler/https` | `chromium.desktop` | `chatgpt.desktop, chromium.desktop` | `chatgpt.desktop, chromium.desktop` |

(Ten of the 538 types; `same as registered` marks rows where the two lists are identical, and `—` a row
where `gio mime` prints `No recommended applications`.)
Two readings of the table: `text/plain` shows a default that is not first in its own lists (the default comes
from `~/.config/mimeapps.list`, the list order from `mimeinfo.cache`), and `text/x-c` shows the parent
contribution — `libreoffice-writer` is registered through `text/plain` and is correctly absent from
`recommended` (§5).

## 12. Named limits

- **Resolution only.** Nothing here says an application starts, is D-Bus activatable, or that a portal answers;
  `g_app_info_launch` is never called. The host run does not launch anything.
- **Version-pinned to GLib 2.90.1** (tag bytes above, host `glib2 2.90.1-1`). A later 2.90.x that changes the
  directory list, the per-file group order or the `defaults.list` deprecation invalidates §2-§3.
- **MIME database limited to aliases and parents.** Globs, magic, icons and any sniffing are outside the
  question; `mime.cache` is read only for the alias and parent tables it needs.
- **Locale: C only.** GKeyFile treats the text from a key's last `[` as a locale only when it is longer than `[]`
  (S502 gkeyfile.c `key_get_locale` :1806-1830) and keeps such a key only for an interesting locale (:1586-1610);
  under `LC_ALL=C` that is exactly `C` (case-insensitive), so `text/plain[C]=` is kept as its own key,
  `text/plain[de]=` is dropped and `x[]=` is a plain key (cases rv-03, k07). A host run under another locale may
  keep more keys; that is not modelled.
- **GKeyFile parses bytes.** Invalid UTF-8 voids nothing at load; only the key whose value is read fails (S502
  gkeyfile.c:2309-2322; cases rv-01, rv-02, mc-12). A repeated key keeps its first position with its last value
  (`g_key_file_add_key_value_pair` :4419-4427; case mc-10). Whitespace is `g_ascii_isspace` (space, tab, LF, FF,
  CR — not VT).
- **`gio` cannot label the lists without a default** (§1); a type whose default is `none` has no observable
  list label, so the entry states the tool's `[]` as the same answer, not as a labelled one.
- **Directory order is read, not assumed.** Within one `applications` directory the desktop ids are collected in
  `readdir` order and a later entry of the same id replaces an earlier one (`get_apps_from_dir` :769-818,
  `g_hash_table_insert`), so `vendor-e.desktop` beside `vendor/e.desktop` is decided by the filesystem's order
  (case w10, fz-01); the tool reads the same order (`os.listdir`), so its answer can differ from another host's
  only where that host's filesystem orders the two names differently.
- **Duplicate aliases follow this host's C library** (§7): the tool replays `qsort`/`bsearch` from the running
  libc; another libc may pick another entry.
- **No write path.** `gio mime TYPE HANDLER` and `xdg-mime default` mutate `mimeapps.list`; nothing here
  exercises or models them, and the lane never runs them.

## 13. Unknowns

- Whether another distribution's GLib (2.80/2.82/2.84) orders these directories and reads these groups the
  same way; only 2.90.1 was opened.
- Whether this host's `libgio` carries a downstream patch: the sha256 above pins the installed bytes, not
  their upstream lineage.
- Whether the applications a user actually runs call this API or a portal on top of it; that is the launch
  plane, not the resolution plane.

## 14. Rejected

- **"`gio mime` prints the registered and recommended lists even with no default."** Rejected: the lists are
  printed only inside the `else` of a found default (gio/gio-tool-mime.c:115-152).
- **"A `[Removed Associations]` entry in a lower-precedence directory removes a higher-precedence addition."**
  Rejected: the removal is skipped when the id is already in the collected hits (gdesktopappinfo.c:1312-1349;
  case l17).
- **"An aliased key in `mimeapps.list` is ignored."** Rejected: keys are unaliased when stored
  (gdesktopappinfo.c:839; case x02).
- **"A `Hidden=true` default is not used."** Rejected: the default path never consults `Hidden`
  (gdesktopappinfo.c:1533-1540, :4758; case l20).
- **"The alias chain is followed transitively."** Rejected: `_xdg_mime_unalias_mime_type` is one lookup
  (xdgmime.c:735-747); the second hop in case x11 comes from the type-list BFS, not from unalias.
- **"The default application must be associated with the type" (S507 default.html).** Rejected as a description of
  GLib 2.90.1: `g_app_info_get_default_for_type_impl` takes the first loadable id of the collected list and never
  checks an association (S504 gdesktopappinfo.c:4740-4775); case l03 — `[Default Applications] text/plain=zz.desktop;c.desktop`
  with no association anywhere — gio answers `c.desktop` with registered `[]`. The specification is the contract the
  implementation claims; the installed implementation decides what `xdg-open` does.
- **"A shlex split is a good enough stand-in for `g_shell_parse_argv`."** Rejected after R91MExecShell: 15 of 65 cases
  disagreed with gio in 7 classes (`#` mid-word, tab before `#`, backslash-newline, `\$`/`` \` `` inside double
  quotes, CR inside a word, the PATH fallback for a `/`-bearing name, the `Hidden` whitespace set); the landed tool
  ports S506 instead (sh cases 65/65).

## 15. Correction (round 92, append-only) — `xdg-open` does not reduce to this call on Hyprland

The opening paragraph's "`xdg-open` … reduce[s] to `g_app_info_get_default_for_type()`" is wrong on this host.
xdg-utils 1.2.1 `xdg-open` maps an `XDG_CURRENT_DESKTOP` it does not know (Hyprland) to `DE=generic`
(xdg-open.in:595-596) and runs `open_generic` (:664-665), which asks `xdg-mime query default TYPE`
(`open_generic_xdg_mime`, :392-412; file paths at :486-489, URL schemes at :506-507). xdg-mime answers with its own
shell resolver `defapp_generic` (xdg-mime.in), not GLib (S508). On this host, 2026-11-06, the two answers differ for
378 of 1133 types (`.ufo/waves/round-92/w1/R92MExecHost-host-run.txt`: `glib_agree=755 glib_disagree=378`). What
`xdg-open` launches is modelled in `corpus/knowledge/xdg-mime-default-resolution-r92.md` (`tools/mado-xdgmime.py`);
this entry stays the model for `gio mime`, `gio open` and GLib/GTK callers.
