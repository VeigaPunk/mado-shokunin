source: S501 (xdg-desktop-portal tag 1.22.1 tarball https://codeload.github.com/flatpak/xdg-desktop-portal/tar.gz/refs/tags/1.22.1 sha256 5afeda953c3743efaa1160e73d62c5bfcac2ceca60e0e134e9b48ed651783625; src/xdp-portal-config.c sha256 2da4fd835032401b2ca0e1a503cb600abdb68e27bc9d23b8fbd28f8e2d4c4fe1, src/xdp-types.h sha256 6b38de155c1e5ddb95ec85a0244fa9a3120712d11e0c8c726b83deca352b75ed, src/xdp-context.c sha256 2c009356170b3ca0cde0f33011e9ec7ea8c1f045dd90a2927deb62fe80180a36; per-interface call sites named in §2), S502 (GLib 2.90.1 glib/gkeyfile.c, https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gkeyfile.c, sha256 e1d1270f6c9881daf8a9f49b41395cbdd8e99fa290212e8530e0bd3df23ff656; host package glib2 2.90.1-1), S503 (portals.conf(5) shipped by the installed xdg-desktop-portal 1.22.1-2: /usr/share/man/man5/portals.conf.5.gz sha256 01eba9b4c14ce2e649e8451f722fb3af7d9b43dd15cd106f8ea33e81bd5fad51; the text is generated from upstream docs, so §-level statements from it are [INF-docs] even though the container is a host file)
covers: which xdg-desktop-portal 1.22.1 backend serves each of the 21 org.freedesktop.impl.portal.* interfaces it queries at start-up — desktop-string parsing, backend descriptor loading and sort, per-directory configuration selection and the directory order, the none / star / interface-key / default rules, Settings' find-all accumulation, the deprecated UseIn fallback, the gtk last resort, the GKeyFile rules those files inherit, a decision table, an error-signature table, the host's 21 answers, and the limits of the production-binary oracle that labelled them
verified-at: 2026-11-06, DRAFT before the round-90 freeze — no measured receipt exists for the candidate counter yet. The candidate is .ufo/waves/round-90/build/mado-portals.c1.py; the host run in §6 is a read-only run of that candidate over the portal configuration chain. Case labels cited as (DRAFT <case-id>) come from .ufo/waves/round-90/controls/portal-cases-r90.json and were re-derived here by re-running the oracle control on the same 92 cases: 92/92 labelled, every oracle and oracle_reason value equal to the committed labels, host tail digest 4a4cf31921e25dc6e60b283cc1aa1b79f743096bfdfc9dbb77df887c16f0fbf9.
recheck: 90d

# xdg-desktop-portal 1.22.1 backend routing: the resolver behind the routers

This entry states how `xdg-desktop-portal` 1.22.1 decides which `<name>.portal` backend serves each
`org.freedesktop.impl.portal.*` interface, and what that decision is on this host. The resolver is
`tools/mado-portals.py` (round-90 candidate `.ufo/waves/round-90/build/mado-portals.c1.py`); the labels are the
production binary's own verbose decision lines (S501 `src/xdp-portal-config.c`, run through
`.ufo/waves/round-90/controls/portal-oracle-r90.py`, §7).

Scope: read-only resolution of the *configuration* decision. Not in scope: whether a backend is installed as a
service, whether it answers a D-Bus call, permission or consent state, screen-share sessions, and any
`org.freedesktop.portal.*` frontend method. The round-12 entry (`corpus/knowledge/xdg-portal-routing-r12.md`)
holds a hand-derived 16-row candidate table; §6 compares it with the 21 answers this entry records.

## 1. The 21 interfaces queried at start-up

The names are the 21 `*_DBUS_IMPL_IFACE` constants under `DESKTOP_DBUS_IMPL_IFACE`
(`org.freedesktop.impl.portal`, xdp-types.h:46) in xdp-types.h:49-146; each is looked up once while the
context initialises (the `init_*` calls at xdp-context.c:385-417, plus Lockdown and Access at
xdp-context.c:354 and :368).

| interface (prefix `org.freedesktop.impl.portal.`) | constant at xdp-types.h | lookup site | lookup function |
|---|---|---|---|
| Access | :49 | xdp-context.c:368 | `xdp_portal_config_find` |
| Lockdown | :51 | xdp-context.c:354 | `xdp_portal_config_find` |
| AppChooser | :53 | open-uri.c:1184 | `xdp_portal_config_find` |
| Account | :56 | account.c:292 | `xdp_portal_config_find` |
| Background | :59 | background.c:1458 | `xdp_portal_config_find` |
| Clipboard | :68 | clipboard.c:646 | `xdp_portal_config_find` |
| DynamicLauncher | :71 | dynamic-launcher.c:1159 | `xdp_portal_config_find` |
| Email | :74 | email.c:366 | `xdp_portal_config_find` |
| FileChooser | :77 | file-chooser.c:899 | `xdp_portal_config_find` |
| GlobalShortcuts | :84 | global-shortcuts.c:839 | `xdp_portal_config_find` |
| Inhibit | :87 | inhibit.c:584 | `xdp_portal_config_find` |
| InputCapture | :92 | input-capture.c:1692 | `xdp_portal_config_find` |
| Notification | :101 | notification.c:1338 | `xdp_portal_config_find` |
| Print | :111 | print.c:385 | `xdp_portal_config_find` |
| RemoteDesktop | :120 | remote-desktop.c:1696 | `xdp_portal_config_find` |
| ScreenCast | :124 | screen-cast.c:1164 | `xdp_portal_config_find` |
| Screenshot | :128 | screenshot.c:644 | `xdp_portal_config_find` |
| Secret | :133 | secret.c:262 | `xdp_portal_config_find` |
| Settings | :136 | settings.c:320 | `xdp_portal_config_find_all` |
| Usb | :141 | usb.c:1558 | `xdp_portal_config_find` |
| Wallpaper | :146 | wallpaper.c:427 | `xdp_portal_config_find` |

Settings is the only interface that asks for *every* matching backend (§4.5); the other twenty take the first
match. `init_usb` is compiled only under `HAVE_GUDEV` (xdp-context.c:414-416), so Usb is queried only in a build
that found gudev — a distinction the oracle cannot see (§7).

## 2. Desktops

- `XDG_CURRENT_DESKTOP` is read from the environment; unset or empty is treated as `""`
  (xdp-portal-config.c:140-142).
- The value is split on `:` (the search-path separator) into tokens; a token is kept only when it is
  non-empty and every byte is ASCII alphanumeric, `-` or `_` (validate_xdg_desktop, :114-131); invalid
  tokens are freed and dropped (:147-153).
- Every surviving token is ASCII-lowercased (:160-173); the lowercased list is what everything else uses
  (stored at :623).

Consequence: `Hyprland` and `hyprland` are the same desktop; `Gnome-Classic` survives; `foo.bar` and an empty
`::` token are dropped; a leading or trailing `:` contributes nothing. Validation runs on the raw token, so
uppercase is allowed and only lowercasing changes it. (DRAFT d02, d03, d06, d07, d08, d09, d11, d12, d13.)

## 3. Backends

- A backend is any file whose name ends in `.portal` in a `xdg-desktop-portal/portals` directory
  (xdp-portal-config.c:329). Its *source name* is the basename up to its **last** `.` (:192-193), so
  `foo.bar.portal` is source `foo.bar`.
- Search order: `XDG_DESKTOP_PORTAL_DIR` alone when set (:359-365); otherwise `XDG_DATA_HOME`, each
  `XDG_DATA_DIRS` entry, then the build-time `DATADIR` (:367-384).
- The first file of a source name wins; a later duplicate logs "Skipping duplicate source" and is ignored
  (:195-199).
- `[portal] DBusName` is required and must be a D-Bus name (:201-212); `Interfaces` is required and every
  entry must be a D-Bus interface name under `org.freedesktop.impl.portal.` (:214-236); `UseIn` is
  optional (:244-246). A file failing any of these is skipped with a warning and the load continues
  (:335-339).
- Sort order (`sort_impl_by_use_in_and_name`, :267-296): walk the desktops in order; at the first desktop
  whose `UseIn` membership differs, the member sorts first (case-insensitive compare, :255-265); if both
  are members, stop and compare source names with `g_strcmp0`; if neither, continue to the next desktop.
  Falling out of the loop compares source names bytewise, so an uppercase source sorts before a lowercase
  one (DRAFT p08).

Consequence: `UseIn` affects *ordering*, and only while it still discriminates; it is not a filter. A desktop
that appears in no `UseIn` leaves the list in plain source-name order. (DRAFT p04, p05, p06, p09.)

## 4. Configurations

### 4.1 One config per directory, and the directory order

`load_config_directory` (:466-508) tries, in the desktop order of §2, `<desktop>-portals.conf`; the first file
that *loads and has a `[preferred]` group* is that directory's config (:476-488). If none does, it tries
`portals.conf` (:491-505). A file with no `[preferred]` group returns NULL (:411-413, :460) and is skipped.

The directories are walked in this order, and every directory contributes at most one config (:538-589):
`$XDG_CONFIG_HOME/xdg-desktop-portal`, each `$XDG_CONFIG_DIRS/xdg-desktop-portal`, the build-time
`SYSCONFDIR/xdg-desktop-portal`, `$XDG_DATA_HOME/xdg-desktop-portal`, each
`$XDG_DATA_DIRS/xdg-desktop-portal`, then `DATADIR/xdg-desktop-portal`. With `XDG_DESKTOP_PORTAL_DIR` set,
that one directory is the only configuration directory (:527-536) as well as the only backend directory
(:359-365).

Two details that bite:
- The same directory can appear twice. `$XDG_DATA_DIRS` normally ends with `/usr/share` and `DATADIR` is
  normally `/usr/share`, so the last two steps name the same directory and the same config path is loaded
  twice (measured on this host, §6). It is harmless for `find` (the first copy answers) and for `find_all`
  (dedup, §4.5).
- A `[preferred]` key whose value is not a valid string list voids **the file**, not the directory: the
  loader returns NULL (:427-432) and `load_config_directory` then tries `portals.conf` (:494). A `[preferred]`
  group that is *empty* does the opposite: `g_key_file_get_keys` returns a non-NULL empty array, so the file
  is a config with zero keys and it shadows `portals.conf` in the same directory (§5, row 3; DRAFT f03).

### 4.2 `find` — one backend per interface (:856-925)

For each config, in the §4.1 order:
1. `none` first: `portal_config_interface_prefers_none` (:645-675) looks up the interface key; if absent it
   falls back to the `default` key (:665-666), and if that list contains the literal `none` the search ends
   *for the whole run* with no backend (:869-870). It does not matter where in the list `none` sits: the test
   is `g_strv_contains` over the whole list (:668), so `hyprland;none` and `kde;none` both mean none
   (DRAFT n03, n06).
2. The interface key's list (:872-882), then the `default` list (:884-894). Inside a list
   (`xdp_portal_config_find_impl_config_by_iface`, :735-776), items are tried in order:
   - `*` returns the first backend of the sorted array that implements the interface and stops the list
     (:749-753 with :693-711); items after it are dead (DRAFT s03).
   - a name with no matching source is skipped at `g_info` level — no warning at the default verbosity
     (:755-762); an existing backend that does not implement the interface is skipped the same way
     (:764-770).
   - the first item that exists *and* implements the interface wins.
3. Nothing in that config: the next config is consulted with the same rules.

After all configs: the deprecated `UseIn` walk (:897-921) — desktops outer, sorted backends inner, first
backend that implements the interface and names the desktop wins, with a warning and a
"prefer portals.conf" warning-once (:910-913). Then the gtk last resort
(`xdp_portal_config_find_gtk_fallback_impl_config`, :823-853): the backend whose **DBusName** is exactly
`org.freedesktop.impl.portal.desktop.gtk` (:839-841) and that implements the interface (:843-844); its
*filename* is irrelevant (DRAFT u01 vs u02), and if it is absent or does not implement the interface there is
no backend at all (:852-853).

### 4.3 `find_all` — Settings only (:927-1004)

Per config, in the same order: a `none` returns what earlier configs collected (:945-946). Otherwise the
interface key's list is walked with `xdp_portal_config_find_impl_configs_by_iface` (:779-821), which adds
**every** matching backend of that list (a `*` matches all of them, :801) and deduplicates against the output
already collected (:804-808). If that config added at least one backend, its `default` list is *not*
consulted (:954-955); if it added none, the default list is walked next (:957-962). After all configs, a
non-empty result is returned as is (:964-965); else the `UseIn` walk collects matches for **all** desktops
instead of stopping at the first (:969-996); else the gtk last resort is appended if it implements Settings
(:998-1001). Result reason lines: `Using <src>.portal for <iface> (config)` (:817).

### 4.4 What GKeyFile guarantees (S502)

- Load: a regular file only (gkeyfile.c:843-848); the line buffer is flushed at EOF, so a file without a final
  newline is parsed completely (:890). A line is only a line at `\n` (or at EOF) (:1851-1895).
- Per line: leading whitespace is skipped (:1625-1626); `#` at the first non-blank byte, or an empty line, is
  a comment (:4561-4564); `[name]` is a group when the bytes after `]` are only spaces or tabs
  (:4647-4672); `key=value` needs a non-empty key and the first `=` (:4674-4690); anything else is
  `G_KEY_FILE_ERROR_PARSE` and the whole load fails (:1638-1649).
- Key names may not be empty and may not carry an initial or final space in the validator (:4604-4614), but
  the line parser has already skipped the line's leading whitespace (:1625-1626) and chomped the key's
  trailing whitespace (:1736-1741), so `default = kde` and an indented `   default=kde` both parse
  (DRAFT g01, g14). Interior spaces in a key are a deliberate compatibility allowance (:4608-4611). A
  locale suffix `[xx]` is accepted (:4616-4635) and the pair is kept only for an "interesting" locale
  (:1786-1800).
- The value chugs only **leading** whitespace (:1755-1758); trailing whitespace survives into the stored
  value (:1760, :1796).
- `g_key_file_get_string_list` (:2400-2470) parses with pieces (`g_key_file_parse_value_as_string`,
  :4692-4801): escapes `\s \n \t \r \\` and, in list context, `\;` (:4711-4767); any other escape is
  `G_KEY_FILE_ERROR_INVALID_VALUE` (:4743-4765); `;` splits (:4772-4776); pieces are raw substrings, so a
  space next to a separator belongs to a piece; a trailing empty piece is dropped because an empty final
  buffer is not appended (:4787-4791), while interior empty pieces are kept (DRAFT g18).
- Duplicate keys: later pairs win for value lookups (`g_key_file_get_value` returns the last pair), but
  `g_key_file_get_keys` returns one entry per pair. xdp walks that list (:422), so a duplicated `default`
  is seen twice: the first becomes the default, the second logs "Duplicate default key will get ignored"
  (:440-446). Routing is unchanged because both entries read the same (last) value.

## 5. Decision table

Every row is an oracle-labelled decision on the installed 1.22.1 binary (DRAFT case ids; §7 for the method).

| # | configuration state | result | upstream | case |
|---|---|---|---|---|
| 1 | interface key names a backend that exists and implements it | that backend, reason `interface specific config` | :872-882 | k01 |
| 2 | interface key names a backend that does not exist | that item is skipped, the rest of the list is tried | :755-762 | k02 |
| 3 | interface key names an existing backend that does not implement it | that item is skipped | :764-770 | k03 |
| 4 | interface key yields nothing | the same config's `default` list is consulted | :884-894 | k04 |
| 5 | a list's first item exists and implements it | that backend (`default config`, or `interface specific config` when reached through the interface key) | :742-773 | d01 |
| 6 | `*` inside a list | the first sorted backend that implements the interface; the list stops there | :749-753, :693-711 | s01, s02, s03 |
| 7 | `*` finds no implementing backend | that list contributes nothing; the next list or config is tried | :751-752 returns NULL | s04 |
| 8 | `none` anywhere in the effective list (interface key when present, else `default`) | no backend; later configs, `UseIn` and the gtk fallback are all skipped | :668-672, :869-870 | n01, n02, n03, n06 |
| 9 | `None` (capitalised) in a list | treated as a backend name; it does not exist, so it is skipped | :668 literal compare | n05 |
| 10 | a directory has no desktop file and no `portals.conf` | the next directory's config decides | :471-505 | f04 |
| 11 | a desktop file has an empty `[preferred]` group | it is chosen and shadows `portals.conf` in that directory | :411-413, :476-488 | f03 |
| 12 | a desktop file's key value is not a valid list | that file is voided and `portals.conf` in the same directory is used | :427-432, :494 | g09 |
| 13 | a desktop file has no `[preferred]` group | it is skipped, `portals.conf` is used | :411-413, :460 | f01 |
| 14 | no config yields a pick | `UseIn` walk: desktops in XDG order, sorted backends within a desktop | :897-921 | u03, u04 |
| 15 | `UseIn` yields nothing | the backend whose DBusName is `org.freedesktop.impl.portal.desktop.gtk` | :823-853 | u01 |
| 16 | gtk absent, or it does not implement the interface | no backend | :852-853 | u02, u07 |
| 17 | Settings (`find_all`) | every matching backend of every config in order; the interface list suppresses that config's default; `none` returns what was collected; `UseIn` collects across desktops; gtk appended last | :927-1004 | a01, a03, a04, a06, a07 |

Two negative results worth naming because they are *not* errors: an interface with no backend is a normal
outcome (xdp builds a skeleton impl and every call fails later), and a short interface key such as
`FileChooser=kde` is an inert key — the comparison is on the full `org.freedesktop.impl.portal.*` name, and
nothing validates `[preferred]` key names beyond GKeyFile's key rules (:422-426; DRAFT k05, k06).

## 6. Error signatures

| # | shape | what you observe | mechanism | evidence |
|---|---|---|---|---|
| 1 | a list item carries trailing whitespace: `default=hyprland;gtk␠␠` | the item never matches; Screenshot falls to `UseIn`, FileChooser to the gtk last resort, so the loss is easy to miss | values are not right-trimmed (gkeyfile.c:1760, :1796); unknown sources are skipped at `g_info` (xdp:755-762) | `g_key_file_get_string_list` → `['hyprland', 'gtk  ']` (ctypes, GLib 2.90.1); DRAFT g03 |
| 2 | a space after a separator: `default=kde; gtk` | the second item is dead; nothing warns | only the value's *leading* whitespace is chugged (gkeyfile.c:1755-1758); a piece keeps its own leading space | ctypes → `['kde', ' gtk']`; DRAFT g02 |
| 3 | `[preferred]` with no keys in `hyprland-portals.conf`, a usable `portals.conf` beside it | `portals.conf` is ignored; FileChooser resolves by gtk last resort instead of by `default config` | `g_key_file_get_keys` returns a non-NULL empty array for an empty group (gkeyfile.c:411-413 has no length check) | ctypes → `ok=1 keys=[]`; DRAFT f03 (FileChooser `gtk`, reason `gtk-last-resort`) |
| 4 | a malformed line, e.g. `default=kde` before `[preferred]`, or `[preferred] x` | the desktop file is voided and the generic `portals.conf` is used | parse error (gkeyfile.c:1638-1649) fails the load (xdp:408-409) | DRAFT g10, g15 |
| 5 | an invalid escape: `default=kde\q` | the desktop file is voided; the generic `portals.conf` decides | INVALID_VALUE (gkeyfile.c:4743-4765) makes `get_string_list` return NULL, which returns NULL from the loader (xdp:427-432) | DRAFT g09 (FileChooser `gnome`, reason `default config`) |
| 6 | a config file without a final newline | no effect: the last key is parsed | the parse buffer is flushed at EOF (gkeyfile.c:890) | `/usr/share/xdg-desktop-portal/hyprland-portals.conf` ends with `default=hyprland;gtk` and no newline, and the §7 host run resolves FileChooser to gtk and Screenshot to hyprland; DRAFT d01-d05 carry newline-less configs |
| 7 | two config fragments concatenated with no newline between them | the second fragment's `[group]` header is swallowed into the first key's value and the following key lands in the same group | a line ends only at `\n` or EOF (gkeyfile.c:1851-1895) | ctypes: `"[preferred]\ndefault=gtk[preferred]\ndefault=kde"` → one group, `get_string_list` → `['kde']`; xdp itself never concatenates — each path is its own GKeyFile (xdp:404-409), so this is a fixture-construction hazard |
| 8 | a `.portal` with an invalid DBusName, a foreign interface, or no `[portal]` | the backend silently disappears from the sorted list (a warning only) | xdp:201-236, :335-339 | DRAFT p01, p02, p03, p10 |

## 7. This host, 2026-11-06

Command (read-only; the resolver opens only `*.portal` and `*portals.conf` under the searched roots):

```sh
python3 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-90/build/mado-portals.c1.py
```

Exit 0. Full output:

```text
MADO_PORTALS: desktops=hyprland backends=hyprland,gnome-keyring,gtk,kwallet configs=/usr/share/xdg-desktop-portal/hyprland-portals.conf,/usr/share/xdg-desktop-portal/hyprland-portals.conf
MADO_PORTAL: org.freedesktop.impl.portal.Lockdown -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Access -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Settings -> gtk (config)
MADO_PORTAL: org.freedesktop.impl.portal.FileChooser -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.AppChooser -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Print -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Notification -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Inhibit -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Screenshot -> hyprland (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Background -> none (no-backend)
MADO_PORTAL: org.freedesktop.impl.portal.Wallpaper -> none (no-backend)
MADO_PORTAL: org.freedesktop.impl.portal.Account -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Email -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Secret -> none (no-backend)
MADO_PORTAL: org.freedesktop.impl.portal.GlobalShortcuts -> hyprland (default config)
MADO_PORTAL: org.freedesktop.impl.portal.DynamicLauncher -> gtk (default config)
MADO_PORTAL: org.freedesktop.impl.portal.ScreenCast -> hyprland (default config)
MADO_PORTAL: org.freedesktop.impl.portal.RemoteDesktop -> none (no-backend)
MADO_PORTAL: org.freedesktop.impl.portal.Clipboard -> none (no-backend)
MADO_PORTAL: org.freedesktop.impl.portal.InputCapture -> hyprland (default config)
MADO_PORTAL: org.freedesktop.impl.portal.Usb -> none (no-backend)
```

What the run used (read-only reads): the run's own `desktops=hyprland` line reports
`XDG_CURRENT_DESKTOP=Hyprland`; the only configuration and descriptor directory present is
`/usr/share/xdg-desktop-portal` — `/etc/xdg-desktop-portal`,
`~/.config/xdg-desktop-portal`, `~/.local/share/xdg-desktop-portal` and
`/usr/local/share/xdg-desktop-portal` do not exist on this host. `XDG_DATA_DIRS` ends with `/usr/share`, so
that directory is also the build-time `DATADIR` and the run lists its `hyprland-portals.conf` twice (§4.1).
`hyprland-portals.conf` is `[preferred]` plus `default=hyprland;gtk` with no final newline; `gtk-portals.conf`
is `default=gtk`. The descriptors are `gtk.portal` (11 interfaces, `UseIn=gnome`), `hyprland.portal`
(Screenshot, ScreenCast, GlobalShortcuts, InputCapture; `UseIn=wlroots;Hyprland;sway;Wayfire;river;`),
`gnome-keyring.portal` (Secret; `UseIn=gnome`) and `kwallet.portal` (Secret; `UseIn=kde`). The sorted backend
order is hyprland, gnome-keyring, gtk, kwallet: hyprland wins the first desktop (Hyprland is in its `UseIn`),
the rest fall back to source-name order.

Summary: gtk serves 11 interfaces, hyprland 4 (Screenshot, ScreenCast, GlobalShortcuts, InputCapture), and
**6 interfaces have no backend at all**: Background, Wallpaper, Secret, RemoteDesktop, Clipboard, Usb. Secret
is the informative one: `gnome-keyring.portal` implements it, but its `UseIn=gnome` is never reached because
the desktop list is `['hyprland']`, and gtk does not implement Secret, so the last resort does not fire
(xdp:897-921, :843-844).

Relation to the round-12 table (`corpus/knowledge/xdg-portal-routing-r12.md:47-62`): its 16 rows are
reproduced exactly by the 21 answers above for those 16 interfaces — its XDPH rows are this host's hyprland
rows, and its GTK rows are this host's gtk rows. It omits **five** interfaces (Background, Wallpaper,
RemoteDesktop, Clipboard, Usb); it does *not* omit Secret or Settings, which it lists at :61 and :62. Its
Secret row ("No matching preferred candidate evidenced") is now resolved: there is no backend, with the
mechanism above; its `[UNK]` about runtime behaviour stays unknown (§9).

`--selftest` on the same candidate: `MADO_PORTALS_SELFTEST: checks=19 failed=0`, exit 0 (DRAFT run, not a
measurement).

## 8. The oracle: method and limits

Method (`.ufo/waves/round-90/controls/portal-oracle-r90.py`, S501's own binary):

- Binary `/usr/lib/xdg-desktop-portal` (package `xdg-desktop-portal 1.22.1-2`,
  sha256 `e1429fbe1bf6c2203ba07f478b9e92e9221437b13a92eebafb0982748583a4f8`), run as `-v -r`.
- It runs inside `dbus-run-session --config-file=<generated bus.conf>`: session-type bus on a unix socket in
  the case's scratch directory, `EXTERNAL` auth, a permissive policy, and **no `<servicedir>`**, so nothing
  can be activated. `DBUS_SYSTEM_BUS_ADDRESS` points at a socket that does not exist, so the system bus is
  unreachable. `HOME` and `XDG_RUNTIME_DIR` are fixtures; `LC_ALL=C`.
- Mode `dir`: `XDG_DESKTOP_PORTAL_DIR` holds both the `.portal` files and the `(desktop-)portals.conf` files
  (xdp:359-365, :527-536), and the other XDG roots point at empty directories. Mode `xdg`: the real search
  path is rebuilt under the fixture, and the host's `/usr/share/xdg-desktop-portal` tail is part of the
  input, with its digest recorded (`4a4cf319…` on this host).
- The stdout log is read until `org.freedesktop.portal.Desktop acquired`, then the process group is killed.
  The five decision messages are parsed from xdp-portal-config.c:817, :846, :879, :891, :915/:987; an
  interface with no decision line is labelled `[]` with no reason. A run that never reaches the completion
  line is an error, never a label.
- Re-labelling the frozen 92-case set here produced equal `oracle` and `oracle_reason` values for every
  case (0 differing interface rows), with the same host tail digest.

Limits:
- It labels *configuration decisions*, not D-Bus behaviour: no `org.freedesktop.portal.*` call is made, no
  backend is started, no consent exists, no stream is created.
- `none` and "no backend at all" are indistinguishable in the label: both are an empty list with no reason.
  The counter maps the tool's `none-key` and `no-backend` onto that one label.
- Settings sources are deduplicated by the parser (`if src not in picks[iface]`), which hides the fact that
  upstream's `UseIn` branch in `find_all` (:969-993) has no dedup of its own: a backend whose `UseIn` names
  two of the listed desktops can be added twice there. No case exercises that shape, and the oracle could
  not see it if one did.
- Usb is queried only under `HAVE_GUDEV` (xdp-context.c:414-416); the label cannot distinguish "build did
  not query Usb" from "queried and found none".
- The three "Using ... (config)" strings are 1.22.1's; a version that rewords them invalidates the parser
  (the counter therefore refuses a host-tail digest change, but it cannot detect a reworded binary with the
  same digest).
- The host tail is pinned by digest, so a host change is a setup error (rc 2) rather than a silent relabel.
- The label file records the oracle binary's sha256 (on this host `e1429fbe…`), but the counter's setup gate
  (`quality/counters/c1-r90-portal-routing.py:226-230`) checks only
  the host tail digest and the absence of `/etc/xdg-desktop-portal`. A host whose installed binary changed while
  its `/usr/share/xdg-desktop-portal` tail did not would pass setup with labels produced by a different binary.

## 9. Named limits of the resolver

- Locale-suffixed keys (`key[xx]`) are dropped, as GLib drops uninteresting locales in the C locale; other
  locales are not modelled.
- Invalid UTF-8 in a config or descriptor makes the file unreadable (matching `g_key_file_load_from_file`
  failing and the loader skipping it).
- Directory enumeration order is not modelled; it only matters for same-named descriptors within one
  directory, which cannot happen (a later duplicate source is skipped at xdp:195-199).
- Settings' `UseIn` duplicates are deduplicated by the resolver; see §8 for the upstream difference.
- The resolver answers what the configuration selects. It does not prove a backend is installed as a
  service, is running, or answers calls.

## 10. Unknowns

- Whether a Secret request fails in the frontend or is answered by something outside this configuration
  chain: the resolver says "no backend", no request was made.
- Whether the running portal service inherited the `XDG_CURRENT_DESKTOP` observed in this shell: the round-12
  `[UNK]` stands; this entry reads the configuration plane only.
- Whether this host's `xdg-desktop-portal` was built with gudev, and therefore whether Usb was queried at all
  (§8).
- Whether a future 1.22.x changes the gtk last resort or the `none` scope; the entry is pinned to 1.22.1
  (`5afeda95…`).

## 11. Rejected

- **"The round-12 table omits Secret and Settings."** Rejected: it lists both
  (`corpus/knowledge/xdg-portal-routing-r12.md:61`, `:62`); it omits five other interfaces (§7).
- **"Trailing whitespace on a `portals.conf` list item is trimmed like a value's leading whitespace."**
  Rejected by measurement: only leading whitespace at the start of the value is chugged (gkeyfile.c:1755-1758)
  and pieces keep their own bytes (ctypes, DRAFT g02/g03).
- **"A config file without a final newline loses its last key."** Rejected for a single file: the parse buffer
  is flushed at EOF (gkeyfile.c:890), measured with ctypes and on this host's own `hyprland-portals.conf`; the
  merge in §6 row 7 needs something to concatenate two fragments.
- **"`none` only stops that directory's search."** Rejected: `portal_config_interface_prefers_none` is checked
  per config and returns NULL from `find` (:869-870), so `none` in a later config still ends the whole search
  (DRAFT n02, n03, x04).
- **"`*` means every backend."** Rejected for the twenty non-Settings interfaces: `*` returns one backend and
  stops the list (:749-753). Only Settings' `find_all` collects every match (:801, :927-1004).
