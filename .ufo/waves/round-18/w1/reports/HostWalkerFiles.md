# HostWalkerFiles — walker/elephant config bytes + hypr launch bindings (round 18, P3 anchor)

Seat: MadoR18.HostWalkerFiles (leaf, file-bytes only). Date: 2026-10-20.
Scope: `~/.config/walker/*`, `~/.config/elephant/*`, the walker/elephant trees under
`~/.local/share/omarchy`, the walker package's own `/etc/xdg/walker` defaults, and the hypr
binding lines that launch walker. Nothing was executed: no walker, elephant,
omarchy-launch/refresh/restart/menu, systemctl, hyprctl, pacman/yay/expac, notify-send,
screenshot or input probe. Commands used are read-only byte tools (`ls`, `find`, `sha256sum`,
`cat -n`, `grep`, `sed -n`, `wc`, `stat`, `od`, `hexdump`, `realpath -m`, `date -u`) plus
reads of `/var/log/pacman.log`, `/var/lib/pacman/local/<pkg>/desc`, the generator directory
under `/run/user/1000/systemd`, and `~/.local/share/omarchy/.git` as bytes (no `git`/`jj`
command was run, in or out of the checkout). No web source was opened, so no fetch receipts
exist for this seat; no tool was installed or upgraded.

Confidence tags: **Observed** = output of a byte read on this host; **[INFERENCE]** =
reasoning from observed bytes + script source; **[UNK]** = not exercised, not knowable from
these bytes.

## 1. Host declaration anchors (versions/commits)

| anchor | value | source | confidence |
|---|---|---|---|
| walker version | `2.17.2-1` (`2.17.0-1 -> 2.17.2-1`, 2026-10-20T09:16:46-0300) | `/var/log/pacman.log:2929` | Observed |
| walker pkg metadata | `%DESC% wayland application runner`; `%URL% https://github.com/abenz1267/walker`; `%BUILDDATE% 1791468872` (=2026-10-08T14:14:32Z); `%INSTALLDATE% 1792498606` (=2026-10-20T12:16:46Z); `%PACKAGER% Omarchy <pkgs@omarchy.org>` | `/var/lib/pacman/local/walker-2.17.2-1/desc:10-14,19-26` | Observed |
| elephant version | `2.22.1-1` (`2.21.0-1 -> 2.22.1-1`, 2026-10-20T09:31:03-0300) | `/var/log/pacman.log:3095` | Observed |
| elephant pkg metadata | `%DESC% general purpose datasource and executor`; `%URL% https://github.com/abenz1267/elephant`; `%BUILDDATE% 1792499381` (=2026-10-20T12:29:41Z); `%INSTALLDATE% 1792499463` (=2026-10-20T12:31:03Z); `%PACKAGER% Unknown Packager` | `/var/lib/pacman/local/elephant-2.22.1-1/desc:10-26` | Observed |
| elephant split packages | base + `bluetooth, calc, clipboard, desktopapplications, files, menus, providerlist, runner, symbols, todo, unicode, websearch` (all `2.22.1-1`); `*-debug` splits removed 2026-10-20T09:38:34-0300 | `/var/lib/pacman/local/elephant-*/`; `/var/log/pacman.log:3136-3147` | Observed |
| host binaries | `/usr/bin/walker` 7,039,912 B mtime `2026-10-08 11:14:32.000000000 -0300`; `/usr/bin/elephant` 23,460,760 B mtime `2026-10-20 09:29:41.000000000 -0300` | `stat` | Observed |
| mtime semantics | both binary mtimes equal `%BUILDDATE%` in local `-0300`, not install time — pacman preserved package mtimes | derived above | **[INFERENCE]** |
| omarchy checkout | `.git/HEAD` = `ref: refs/heads/master`; `packed-refs:2` `8fcc9d6048af4cb0e3af8512c78049857a3b53dd refs/heads/master`; `packed-refs:508` same hash `refs/tags/v3.8.4`; `ORIG_HEAD`/`FETCH_HEAD` same hash | byte read of `~/.local/share/omarchy/.git/{HEAD,packed-refs,ORIG_HEAD,FETCH_HEAD}` | Observed |
| omarchy origin | `https://github.com/basecamp/omarchy.git` | `~/.local/share/omarchy/.git/config` | Observed |
| `OMARCHY_PATH` | `$HOME/.local/share/omarchy`; prepended to `PATH` | `~/.config/uwsm/env:4-5` | Observed |

Version proof is exactly the pacman.log line plus the local package `desc`; no walker or
elephant `--version` was run. A tag's source never proves the host binary — the package
metadata above is the only host-binary provenance used here.

## 2. Byte inventory (sha256)

| file | sha256 | bytes | note |
|---|---|---|---|
| `~/.config/walker/config.toml` | `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787` | 1336 | 49 lines, ends `0a` |
| `~/.local/share/omarchy/config/walker/config.toml` | `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787` | 1336 | **byte-identical to the user copy** |
| `~/.config/elephant/calc.toml` | `2c0ef81b8edc9edfdc409570bf18ba9d44f488a30d6b223533cce66ee266bdb5` | 14 | identical to omarchy copy |
| `~/.config/elephant/desktopapplications.toml` | `999b191512b29b6822a18f48495169bf4b96573388da2b035452e530f31f434e` | 62 | identical to omarchy copy |
| `~/.config/elephant/symbols.toml` | `9c0d5edf1fce95f3c785af79535c3c95ab6aaa5c16048e7e42560182e33efd9b` | 81 | identical to omarchy copy |
| `~/.local/share/omarchy/default/walker/restart.conf` | `de0f70294000bc29f5876ea195db127f74060ac990aad5a129eeb72c98b15433` | 38 | copied to systemd drop-in |
| `~/.local/share/omarchy/default/walker/walker.desktop` | `5cb9874eedbcb32c7b121ea60f6433f881499247cac7e6473a9a93adeebc3aa7` | 138 | autostart copy identical (`~/.config/autostart/walker.desktop`) |
| `~/.local/share/omarchy/default/walker/themes/omarchy-default/layout.xml` | `dbb6bbbe74be894a0f545c91a08e5ee007b3bc8f72a3f07af3fe309bf49e0261` | 6488 | 156 lines |
| `~/.local/share/omarchy/default/walker/themes/omarchy-default/style.css` | `481267af0e89a475c851de82692176b4b496045e41081fa94eec0fbaf32500b0` | 1243 | 121 lines; imports theme CSS |
| `~/.local/share/omarchy/default/themed/walker.css.tpl` | `d7faea3d54688f6a9a4aa8f02496a809098d20751e72f2311eae87ed7efeec0e` | 241 | 6 lines |
| `~/.config/omarchy/current/theme/walker.css` | `f44cb45063494d2f4a8f489c47d8901b3bc98b27fbd1ca1c5a8801b40606bbc0` | 191 | rendered, mtime 17:49:02 |
| `~/.config/omarchy/current/theme/colors.toml` | `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786` | — | identical to `themes/matte-black/colors.toml` |
| `~/.local/share/omarchy/default/elephant/omarchy_background_selector.lua` | `292c7deb0ddc0d006728a3c9740cf196c818240af5d24b7c0cb9a2e2bab5f7eb` | 2076 | 73 lines |
| `~/.local/share/omarchy/default/elephant/omarchy_themes.lua` | `d997d5a4c27ffc109a4302075fd4f12445ddc1fc44eea3ec28a37dd9617f386a` | 2922 | 96 lines |
| `~/.local/share/omarchy/default/elephant/omarchy_unlocks.lua` | `b577869246d8050fd02401b37916c6251afaaaf8e9bdc9c2c9c7d48a82905c61` | 2746 | 92 lines |
| `~/.local/share/omarchy/default/hypr/bindings/utilities.conf` | `57ddb3045f81d6932d7e89482b295a28bc490550fa9dd1a1ff93db91573524fc` | 4119 | 76 lines |
| `~/.local/share/omarchy/default/hypr/bindings/clipboard.conf` | `19ca281aae91a7db511fb4f3a5aabbabff9c1f7b6b949ff62924b01082ffaaef` | 319 | 5 lines |
| `~/.local/share/omarchy/default/hypr/apps/walker.conf` | `8ebc83e3e1c3c8296648f3334cc3d981dc95a27070e6aa9f449e7e45c510d0e9` | 80 | 2 lines |
| `~/.config/hypr/bindings.conf` | `e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581` | 2879 | 40 lines |
| `~/.config/hypr/hyprland.conf` | `ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365` | — | 32 lines |
| `~/.local/share/omarchy/bin/omarchy-launch-walker` | `fd9e93f830bc228610df15d754136e066ee920fea5f20817aa93e65d5a1d81d8` | 412 | 14 lines |
| `~/.local/share/omarchy/bin/omarchy-refresh-walker` | `05cd9c672252fd17d2a2c6d699a7e59ed1cd81c0c873abb1a6c6bd45c093f9a2` | 893 | 26 lines |
| `~/.local/share/omarchy/bin/omarchy-restart-walker` | `9ac82d0c1370ec19f59c8347716036765d3335d348feaec4c9581e2ca3bf8174` | 709 | 24 lines |
| `/etc/xdg/walker/config.toml` (package default) | `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b` | 13743 | mtime 2026-10-08 11:14:32 |
| `/etc/xdg/walker/themes/default/style.css` | `5829f472a3a6fc664627cd16f7f867717bfd3d56c1612b75bf61eaf3d8a8961a` | 2841 | upstream default theme |
| `/etc/xdg/walker/themes/default/layout.xml` | `55106a1ce3b6a477fbaa04e50e7df367b0e242287f207f8fc7b6460f401dafd3` | — | 160 lines, differs from omarchy layout |
| `/etc/xdg/walker/themes/default/item*.xml` | `d6dac24c…` (item), `4fe8af04…` (dmenu), `2fae16af…` (symbols), `03e6cf15…` (symbols_grid), `b3597b72…` (clipboard), `8ded6a2c…` (files), `4de69a87…` (providerlist), `ece4a094…` (calc), `f644e39d…` (todo), `34ef99fc…` (unicode), `e9613245…` (archlinuxpkgs = dnfpackages) | — | item templates |
| `/etc/xdg/walker/themes/default/{keybind,preview}.xml` | `1233d0b1…`, `073a912e…` | — | — |

Package file lists confirm `walker` ships only `/etc/xdg/walker/**` + LICENSE (no man page,
no systemd unit, no `/usr/share/walker`), and each elephant split ships only
`/usr/lib/elephant/<name>.so` + LICENSE (`/var/lib/pacman/local/walker-2.17.2-1/files:2-30`,
`elephant-menus-2.22.1-1/files`). There is no `/etc/xdg/elephant` and no `/usr/share/elephant`
on this host.

## 3. Host walker config, line by line (Observed)

`~/.config/walker/config.toml` (49 lines, sha `fecf71fa…`):

| lines | content | note |
|---|---|---|
| 1 | `force_keyboard_focus = true` | upstream default `false` |
| 2 | `selection_wrap = true` | upstream `false` |
| 3 | `theme = "omarchy-default"` | upstream `"default"` |
| 4 | `additional_theme_location = "~/.local/share/omarchy/default/walker/themes/"` | omarchy-only key; leading `~` |
| 5 | `hide_action_hints = true` | upstream `false` |
| 7-8 | `[placeholders]`, `"default" = { input = "… Search...", list = "No Results" }` | input begins `ef 80 82` = U+F002 (Nerd Font glyph), then space + `Search...` |
| 10-11 | `[keybinds]`, `quick_activate = []` | upstream `["F1".."F4"]` |
| 13-14 | `[columns]`, `symbols = 1` | upstream `"symbols" = 3` |
| 16-21 | `[providers]`, `max_results = 256`, `default = [ "desktopapplications", "websearch" ]` | upstream `50`; default list drops `calc` |
| 23-45 | six `[[providers.prefixes]]`: `/`→`providerlist`, `.`→`files`, `:`→`symbols`, `=`→`calc`, `@`→`websearch`, `$`→`clipboard` | see §4 remap table |
| 47-49 | `[[emergencies]]`, `text = "Restart Walker"`, `command = "omarchy-restart-walker"` | omarchy-only; invokes systemctl wrapper |

Everything else is absent. The file is byte-identical to omarchy's shipped
`config/walker/config.toml` and its mtime (2026-10-03 17:44:32.097…) is a minute after the
omarchy copy's (17:42:32.296…), so it is a pristine install-time copy, **not a user-tuned
config**. The copy path is `omarchy-refresh-walker:15`
(`omarchy-refresh-config walker/config.toml`), which per `omarchy-refresh-config:21-32`
copies `~/.local/share/omarchy/config/$config_file` over `~/.config/$config_file`, keeping a
timestamped `.bak.` only when the bytes differ.

## 4. Upstream contract vs host declaration (walker)

`/etc/xdg/walker/config.toml` (13743 B, sha `3c5c6867…`) is the only config walker itself
ships; its mtime equals the walker package build date. Anchored divergences:

| concern | upstream `/etc/xdg/walker/config.toml` | host `~/.config/walker/config.toml` |
|---|---|---|
| keyboard focus | `force_keyboard_focus = false` :1 | `true` :1 |
| wrap | `selection_wrap = false` :6 | `true` :2 |
| action hints | `hide_action_hints = false` :14 | `true` :5 |
| theme | `theme = "default"` :9 | `"omarchy-default"` :3 + `additional_theme_location` :4 |
| max results | `max_results = 50` :67 | `256` :17 |
| default providers | `desktopapplications, calc, # runner, websearch` :59-64 | `desktopapplications, websearch` :18-21 |
| columns | `"symbols" = 3` :37-38 | `symbols = 1` :13-14 |
| keybinds | full map incl. `quick_activate = ["F1".."F4"]` :43-56 | only `quick_activate = []` :10-11 |
| prefix `/` | `files` :83-85 | `providerlist` :23-25 |
| prefix `.` | `symbols` :87-89 | `files` :27-29 |
| prefix `:` | `clipboard` :107-109 | `symbols` :31-33 |
| prefix `$` | `windows` :111-113 | `clipboard` :43-45 |
| prefix `=` / `@` | `calc` :99-101 / `websearch` :103-105 | same :35-41 |
| omitted upstream prefixes | `;` providerlist :75-77, `>` runner :79-81, `!` todo :91-93, `%` bookmarks :95-97 | absent |
| omitted upstream sections | `[niri]` :24-27, `[shell]` (layer `overlay`, all anchors) :29-35, `providers.empty/ignore_preview/argument_delimiter/sets/max_results_provider` :65-73, `providers.actions` :118-304, `dmenu` :126 | absent |
| extra | — | `[[emergencies]]` :47-49 |

[UNK] whether the omitted keys fall back to `/etc/xdg/walker/config.toml` values or to
walker's compiled defaults. Nothing here proves merge semantics; the host file must not be
presented as walker's complete schema.

The shipped upstream theme `/etc/xdg/walker/themes/default/` (layout `55106a1c…`,
style `5829f472…`, item templates) is only selected when `theme = "default"`; it uses its own
palette (`@define-color window_bg_color #1f1f28` etc., style.css:1-5) and a fixed
`width-request 600`/`height-request 570` (layout.xml:19-20), unlike the omarchy layout
(`width-request 644`, no height-request, layout.xml:15).

## 5. walker theme wiring (P3↔P5 coupling, Observed)

- `~/.local/share/omarchy/default/walker/themes/omarchy-default/style.css:1`
  `@import "../../../../../../../.config/omarchy/current/theme/walker.css";`. The import has
  exactly 7 `../`; `realpath -m` from the style.css directory resolves to
  `/home/vgpnk/.config/omarchy/current/theme/walker.css` — observed, with 191 bytes and
  `@define-color selected-text #e68e0d; text #bebebe; base #121212; border #bebebe;
  foreground #bebebe; background #121212;` (lines 1-6).
- Those values are the render of `default/themed/walker.css.tpl` (6 lines,
  `{{ accent }}`, `{{ foreground }}`, `{{ background }}` twice, sha `d7faea3d…`) by
  `omarchy-theme-set-templates`: it reads `current/next-theme/colors.toml` (:9), builds a
  `sed` map (:18-33), writes every non-existing `*.tpl` output into `next-theme` (:38-45);
  `omarchy-theme-set:38` calls it before the `rm -rf`/`mv` swap into `current/theme`
  (:41-45). `current/theme/colors.toml` sha `dbdd13a6…` has `accent = "#e68e0d"`,
  `foreground = "#bebebe"`, `background = "#121212"` (:1-4), matching the rendered CSS.
- The active theme is `matte-black` (`~/.config/omarchy/current/theme.name`, 12 bytes with
  trailing `0a`); the checkout theme `themes/matte-black/` supplies `colors.toml` with the
  same digest and **no** `walker.css`, so `walker.css` is template-rendered, not copied.
- `omarchy-theme-set` restarts waybar, swayosd, terminals, hyprctl, btop, opencode, mako and
  helix (:52-70) but **not walker**. Whether a theme switch reaches a running walker, or only
  the next spawn, is **[UNK]** — no runtime observation was made. The only scripted walker
  restart is `omarchy-restart-walker` (and the pacman hook / `[[emergencies]]`).

## 6. Layout anchors (`layout.xml`, 156 lines, sha `dbb6bbbe…`)

`GtkWindow id="Window"` (:4-9, title `Walker`), `GtkBox BoxWrapper` width-request 644 (:11-15),
`GtkEntry id="Input"` (:40-47), `GtkLabel id="ElephantHint"` label `Waiting for elephant...`
(:61-67), `GtkLabel id="Placeholder"` label `No Results` (:71-75), `GtkScrolledWindow` +
`GtkGridView id="List"` with `max_columns 1` (:81-104, max_columns at :100), `GtkBox id="Preview"`
(:107-111), keybind boxes (:116-140), error label hidden (:143-149). The "Waiting for elephant..."
label is the only in-template statement of the walker↔elephant dependency.

## 7. Launcher / service / hook contract (Observed)

`~/.local/share/omarchy/bin/omarchy-launch-walker` (14 lines, sha `fd9e93f8…`):

- :5-7 `if ! pgrep -x elephant; then setsid uwsm-app -- elephant & fi`
- :9-12 if no process matches `walker --gapplication-service`, spawn
  `setsid uwsm-app -- env GSK_RENDERER=cairo walker --gapplication-service &`
- :14 `exec walker --width 644 --maxheight 300 --minheight 300 "$@"`

So **every** call — including `--help` — can start both daemons. This is why the launcher is
not a safe observation tool even for argument probing. `GSK_RENDERER=cairo` is set only for
the background service spawn, not the foreground CLI.

Service chain:
- `default/walker/walker.desktop:4` `Exec=walker --gapplication-service`; copied byte-identically
  to `~/.config/autostart/walker.desktop` by `omarchy-launch`/`refresh`/install (`refresh-walker:5-6`,
  `install/config/walker-elephant.sh:3-5`).
- The xdg-autostart generator materializes `/run/user/1000/systemd/generator.late/app-walker@autostart.service`
  (generated 2026-10-20 09:57): `SourcePath=/home/vgpnk/.config/autostart/walker.desktop` (:5),
  `Type=exec`, `ExecStart=:/usr/bin/walker --gapplication-service` (:14), `Restart=no` (:15),
  wanted by `xdg-desktop-autostart.target` (symlink observed).
- `~/.config/systemd/user/app-walker@autostart.service.d/restart.conf` (38 B, sha `de0f7029…`,
  copy of `default/walker/restart.conf`) overrides with `Restart=always`, `RestartSec=2`
  (:1-3). The drop-in applies because the generated unit carries the same instance name.
- `elephant.service` (173 B, hand/user file): `After=graphical-session.target` (:4),
  `ExecStart=elephant` (:8), `Restart=on-failure` (:9), `WantedBy=graphical-session.target`
  (:12).
- `/etc/pacman.d/hooks/walker-restart.hook` (from `install/config/walker-elephant.sh:13-25`):
  `Type = Package`, `Operation = Upgrade`, `Target = walker`, `walker-debug`, `elephant*`,
  `When = PostTransaction`, `Exec = /home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker`
  (hook file :1-11). Whether this hook fired during the 09:16/09:31 upgrades is **[UNK]**
  (no hook log line read).
- `omarchy-restart-walker:5-14`: restarts `elephant.service` if enabled, then
  `app-walker@autostart.service` if enabled, else prints a red "RESTART MANUALLY". This is the
  script the `[[emergencies]]` entry and the pacman hook invoke.

## 8. Hypr binding lines that launch walker (exact, Observed)

- `~/.config/hypr/hyprland.conf:6` sources `default/hypr/bindings/clipboard.conf`;
  `:8` sources `default/hypr/bindings/utilities.conf`; `:12` sources
  `default/hypr/windows.conf`.
- `default/hypr/windows.conf:12` sources `default/hypr/apps.conf`; `apps.conf:18` sources
  `apps/walker.conf`; `apps/walker.conf:2` `layerrule = no_anim on, match:namespace walker`.
- `default/hypr/bindings/utilities.conf:2`
  `bindd = SUPER, SPACE, Launch apps, exec, omarchy-launch-walker`
  and `:3` `bindd = SUPER CTRL, E, Emoji picker, exec, omarchy-launch-walker -m symbols`.
- `default/hypr/bindings/clipboard.conf:5`
  `bindd = SUPER CTRL, V, Clipboard manager, exec, omarchy-launch-walker -m clipboard`.
- `~/.config/hypr/bindings.conf` has **no active walker bind**; line 40 is a commented
  example (`# bind = SUPER, PERIOD, exec, omarchy-launch-walker -m symbols # Emoji Button`).
  No `unbind` of the default binds exists in the user file (grep found none).
- `omarchy-menu` walker call sites (not hypr binds, but same launch path): `:21-22`
  `pgrep -f "walker.*--dmenu"` → `walker --close`; `:43` pipes the menu through
  `omarchy-launch-walker --dmenu --width 295 --minheight 1 --maxheight 630 -p "$prompt…"`;
  `:269` `-m menus:omarchyunlocks`; `:298` `-m menus:omarchythemes`; `:302`
  `-m menus:omarchyBackgroundSelector`; `:468` edits `~/.config/walker/config.toml` then
  `omarchy-restart-walker`; `:857` `walker -p "Launch…"` (bare binary, no launcher).

Active walker launchers therefore: Super+Space, Super+Ctrl+E, Super+Ctrl+V, plus every
`omarchy-menu` path and the config `[[emergencies]]` entry. All ultimately hit
`omarchy-launch-walker` except the dmenu `walker --close` and `walker -p` calls.

## 9. Elephant provider/menu bytes (Observed)

User config (`~/.config/elephant/`): only three provider TOMLs, byte-identical to omarchy's
`config/elephant/` copies:

- `calc.toml:1` `async = false`
- `desktopapplications.toml:1-3` `show_actions = false`, `only_search_title = true`,
  `history = false`
- `symbols.toml:1` `command = 'wl-copy && hyprctl dispatch sendshortcut "SHIFT,Insert,activewindow"'`
  — a runtime action string only; never executed this round.

`~/.config/elephant/menus/` holds three symlinks (no regular files) to
`~/.local/share/omarchy/default/elephant/*.lua`; the targets' digests are in §2. They are
linked by `omarchy-refresh-walker:19-23` and by `install/config/walker-elephant.sh:27-31`.

Menu Lua anchors:
- `omarchy_themes.lua`: `Name = "omarchythemes"` (:4), `HideFromProviderlist = true` (:6),
  `GetEntries()` (:41), reads `~/.config/omarchy/themes` + `$OMARCHY_PATH/themes` (:43-45),
  `io.popen("find -L '"..theme_dir.."' …")` (:52), preview fallback (:65-66), entries with
  `Preview`/`PreviewType = "file"` and action `omarchy-theme-set <theme>` (:75-81).
- `omarchy_background_selector.lua`: `Name = "omarchyBackgroundSelector"` (:1),
  `Cache = false` (:3), reads `theme.name` (:30-34), searches
  `current/theme/backgrounds` + `backgrounds/<theme>` (:37-42), `io.popen("find -L …")`
  (:48-51), action `omarchy-theme-bg-set <path>` (:61), `PreviewType = "file"` (:63-64).
- `omarchy_unlocks.lua`: `Name = "omarchyunlocks"` (:9), `FixedOrder = true` (:12), scans
  theme dirs for `preview-unlock.png` (:49-51), action wraps
  `omarchy-launch-floating-terminal-with-presentation` + `omarchy-plymouth-set-by-theme`
  (:63-65), default entry runs `omarchy-plymouth-reset` (:81-83).

`/usr/lib/elephant/` contains exactly these provider modules: `bluetooth, calc, clipboard,
desktopapplications, files, menus, providerlist, runner, symbols, todo, unicode, websearch`
(all `.so`). [INFERENCE] this set is the provider inventory the running daemon can expose;
nothing here proves which providers a given query actually loads.

## 10. Safe observation recipe (no daemon launch)

Runnable, read-only checks backed by the observations above:

```
sha256sum ~/.config/walker/config.toml
  # expect fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787
cmp -s ~/.config/walker/config.toml ~/.local/share/omarchy/config/walker/config.toml
  # expect 0 (pristine copy)
sha256sum /etc/xdg/walker/config.toml
  # expect 3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b
sha256sum ~/.config/elephant/*.toml
  # expect 2c0ef81b…, 999b1915…, 9c0d5edf…
grep -n 'walker\|elephant' ~/.config/hypr/bindings.conf
  # expect only the commented line 40
grep -n 'omarchy-launch-walker' ~/.local/share/omarchy/default/hypr/bindings/*.conf
  # expect utilities.conf:2-3, clipboard.conf:5
sed -n '2929p;3095p' /var/log/pacman.log
  # expect the walker/elephant upgrade lines quoted in §1
cat ~/.local/share/omarchy/.git/packed-refs | grep -n 'v3.8.4'
  # expect 8fcc9d6048af4cb0e3af8512c78049857a3b53dd
```

Do **not** run `walker`, `elephant`, `omarchy-launch-walker` (any args), `omarchy-menu`,
`omarchy-refresh-walker`, `omarchy-restart-walker`, `systemctl`, `hyprctl`, `pacman`/`yay`/
`expac` or `pgrep`-driven probes (`pgrep` itself is read-only but was not used). The launcher
spawns `elephant` and `walker --gapplication-service` at lines 5-12 before exec'ing the CLI, so
it is not a read-only interface; `omarchy-restart-walker` calls systemctl; `omarchy-menu:21-22`
can close a running walker.

## 11. Unexercised behavior ([UNK] — host binaries stay unobserved)

1. Which keys of the host `config.toml` walker 2.17.2 actually honors, and whether omitted
   keys inherit `/etc/xdg/walker/config.toml` or compiled defaults.
2. Whether `~` is expanded in `additional_theme_location`; whether the trailing slash matters.
3. Theme discovery order (user dir vs `additional_theme_location` vs `/etc/xdg`).
4. Whether CSS changes reach a running walker after `omarchy-theme-set` (no walker restart in
   its restart list).
5. GApplication service activation: when `walker --width …` attaches to an existing service
   instance vs starting a new process; behavior when the service is not yet registered.
6. `pgrep -x elephant` / `pgrep -f "walker --gapplication-service"` race and false-negative
   paths in the launcher.
7. dmenu-mode selection/exit-code semantics used by `omarchy-menu:43`; what `walker --close`
   does when no dmenu instance exists.
8. Elephant IPC wire protocol and provider discovery; whether the `.so` set equals the
   advertised provider list; per-provider config load order.
9. Menus provider's Lua API (`GetEntries`, `Actions`, `Preview`, `FixedOrder`, `Cache`,
   `HideFromProviderlist`, `SearchName`) semantics beyond the observed field names.
10. Execution environment of `symbols.toml`'s shell command (`wl-copy`, `hyprctl` presence;
    quoting/injection behavior).
11. Hypr layer namespace `"walker"` actually being the layer surface namespace at runtime,
    and the effect of `no_anim`.
12. The pacman hook's execution during the 09:16/09:31 upgrades.
13. Any log evidence (walker/elephant logs were not read; journalctl is banned this round).

## 12. Route-note implications (P3)

- **Upstream identity is observable but not fetched.** The only upstream pointers on hand are
  package metadata: `walker` → `https://github.com/abenz1267/walker` and `elephant` →
  `https://github.com/abenz1267/elephant` (`desc:14` each). These are local metadata, not
  fetch receipts, so they cannot carry an upstream S-row under R17-V3. Whoever writes
  `walker-route-r18.md` must fetch tag-pinned raw docs/spec/code with curl, save the body +
  one JSON receipt line, and record tag→commit via `git ls-remote`; until then the row stays
  `S0xx-pending`.
- **Host declaration material that is already evidence-backed** (file-byte rows, no runtime
  claim): the sha256 table (§2), the host-vs-upstream divergence table (§4), the config line
  map (§3), the theme import chain (§5), the launcher/service/hook contract (§7) and the hypr
  binding lines (§8). These are documentary; they must not be phrased as "walker does X".
- **`## Safe observation`** can use exactly the §10 commands; it must explicitly exclude the
  launcher, `omarchy-menu`, `systemctl` and the `[[emergencies]]` path.
- **`## Unexercised behavior`** should carry the §11 items, at minimum 1, 2, 4, 5, 6, 7, 8, 9
  and 10; host binaries remain `[UNK]`.
- Do not claim `~/.config/walker/config.toml` is a full schema or a user customization: it is
  a byte-identical install copy of omarchy's config and omits roughly two dozen upstream keys
  (§4).
- The upstream default config at `/etc/xdg/walker/config.toml` is a walker-shipped file and a
  legitimate *local* upstream-contract witness, but it still is not a fetched receipt and its
  version is tied to the host package build (2026-10-08), not to a tag commit.

## 13. Gaps / notes on method

- No fetch receipts: no web source opened by this seat.
- No tools installed or upgraded.
- `git ls-remote` was **not** run (it would touch the network and the contract reserves tag→
  commit recording to the fetching seat); omarchy's tag is proven only by `.git` bytes.
- The walker binary's mtime equals its package build date; this report never treats mtime as
  install time.
- The one non-read-only-adjacent path taken was reading `/run/user/1000/systemd/generator.late/`
  (plain file read); no systemd client was invoked.
