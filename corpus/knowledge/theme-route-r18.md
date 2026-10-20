source: S092 (swaybg v1.2.2 tag: swaybg.1.scd:19-31, README.md:3-5, main.c:521-529,575-577,658-663, background-image.c:24-46; raw SHA-256 in § Upstream contract); S093 (omarchy v3.8.4 tag: bin/omarchy-theme-set:17,29-30,38,41-42,45,48-50,53-73; bin/omarchy-theme-bg-next:6-9,11,14-17,41,46,49-50; bin/omarchy-theme-bg-set:12,21,24-25; bin/omarchy-theme-set-templates:6,38,43; default/hypr/autostart.conf:5); S094 (omarchy v3.8.4 themes/matte-black payload tree and colors.toml); S095 (host P5 theme state and consumer declarations, file bytes: current/theme.name, current/background, current/theme/, hypr/hyprland.conf:4,13, hypr/hyprlock.conf:1,10, waybar/style.css:1, swayosd/style.css:1, alacritty/alacritty.toml:1, walker omarchy-default/style.css:1, mako/config, btop/themes/current.theme, nvim/lua/plugins/theme.lua)
verified-at: 2026-10-20; tag-pinned raw bytes fetched with curl (receipts in .ufo/waves/round-18/fetch/NoteTheme/receipts.jsonl), host files read as bytes only (sha256sum, cat, readlink, stat, grep); SHA-256 values in the sections below and in .ufo/waves/round-18/drafts/NoteTheme-rows.md
recheck: re-fetch the tag-pinned raw URLs listed in § Safe observation and compare SHA-256 with the receipts; re-hash the host files in § Host declaration and readlink the current/ links; no omarchy-*, omarchy theme, swaybg, pkill, pgrep, hyprctl, pacman, systemctl or live probe; the tag commit by git ls-remote --tags only
surface: P5

# P5 themes and wallpapers — documentary route (omarchy theme set, swaybg)

Documentary route only. The upstream contract and the host file bytes below are
read, not observed: no theme set was run, no background was changed, no swaybg
process was inspected, and no consumer was reloaded in this pass. Unobserved
behaviour is listed in § Unexercised behavior. Companion plane note:
`corpus/knowledge/theme-wallpaper-plane.md` (round-7 declared-file census; its
§3 live wallpaper observation of 2026-10-14 is not re-measured here). The
host bytes below re-measure that census and agree with it (pins listed in
§ Host declaration).

Anchor keys used below:

| key | source | version | anchor form |
|---|---|---|---|
| OT | https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-theme-set | omarchy v3.8.4 (tag commit 8fcc9d6048af4cb0e3af8512c78049857a3b53dd) | `[OT:n]` = file line |
| OB | …/v3.8.4/bin/omarchy-theme-bg-next | v3.8.4 | `[OB:n]` = file line |
| OS | …/v3.8.4/bin/omarchy-theme-bg-set | v3.8.4 | `[OS:n]` = file line |
| OP | …/v3.8.4/bin/omarchy-theme-set-templates | v3.8.4 | `[OP:n]` = file line |
| OA | …/v3.8.4/default/hypr/autostart.conf | v3.8.4 | `[OA:n]` = file line |
| OM | https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black (tree page, final URL under `omacom/omarchy`) | v3.8.4 | names only, `[OM]` |
| SW | https://raw.githubusercontent.com/swaywm/swaybg/v1.2.2/swaybg.1.scd | swaybg v1.2.2 (tag commit a59ea3dbe543b44177ad1b5bdb4afa1c5be9b9d2, peeled) | `[SW:n]` = file line |
| SR | …/swaybg/v1.2.2/README.md | v1.2.2 | `[SR:n]` = file line |
| SM | …/swaybg/v1.2.2/main.c | v1.2.2 | `[SM:n]` = file line |
| SB | …/swaybg/v1.2.2/background-image.c | v1.2.2 | `[SB:n]` = file line |

Tag selection: `v3.8.4` is the omarchy checkout tag (`~/.local/share/omarchy/.git/ORIG_HEAD`
and `.git/packed-refs` both name `8fcc9d6048af4cb0e3af8512c78049857a3b53dd` for
`refs/heads/master` and `refs/tags/v3.8.4`). `v1.2.2` is the swaybg tag matching the
host package version (§ Host declaration). Tag commits were read with
`git ls-remote --tags` only.

## Upstream contract

### Theme-set writer (omarchy v3.8.4)

- `[OT:17]` derives `THEME_NAME` from the argument: lowercase, spaces to hyphens, HTML tags stripped. `[OT:19-22]` refuses a name with neither `themes/<name>` nor `~/.config/omarchy/themes/<name>`.
- `[OT:29-30]` copies the official theme payload first, then user overrides, into `current/next-theme`. `[OT:38]` runs `omarchy-theme-set-templates` before the swap. `[OT:41-42]` removes `current/theme` and moves `next-theme` into its place. `[OT:45]` writes `current/theme.name`.
- `[OT:48-50]` calls `omarchy-theme-bg-next` unless `OMARCHY_THEME_SKIP_BACKGROUND=1`. Swaybg is therefore relaunched from inside the background writer, not from the restart list.
- `[OT:53-62]` restarts waybar (only when running), swayosd, terminal, hyprctl, btop, opencode, mako, helix. swaybg is not in this list. `[OT:65-70]` runs the app setters (foot, gnome, browser, vscode, obsidian, keyboard). `[OT:73]` calls the `theme-set` hook.

### Background writers (omarchy v3.8.4)

- `omarchy-theme-bg-next` reads the theme name from `current/theme.name` `[OB:6]`, gathers backgrounds from `~/.config/omarchy/backgrounds/<name>/` and `current/theme/backgrounds/` `[OB:7-9]`, lists them with `find -L … -maxdepth 1 -type f` sorted NUL-safe `[OB:11]`, and picks the next entry with wrap-around `[OB:41]`. With zero backgrounds it runs `swaybg --color '#000000'` `[OB:14-17]`.
- With backgrounds, `[OB:46]` sets the link with `ln -nsf "$NEW_BACKGROUND" "$CURRENT_BACKGROUND_LINK"`, and `[OB:49-50]` runs `pkill -x swaybg` then `setsid uwsm-app -- swaybg -i "$CURRENT_BACKGROUND_LINK" -m fill`. The swaybg argument is the link, not the image.
- `omarchy-theme-bg-set` `[OS:12]` resolves the argument with `realpath`, `[OS:21]` sets the link with `ln -nsf`, and `[OS:24-25]` relaunches swaybg on the link with `-m fill`. It exists as a second writer of the same link; it also does not touch `theme.name`.

### Template renderer (omarchy v3.8.4)

- `[OP:6]` reads built-in templates from `$OMARCHY_PATH/default/themed`; `[OP:38]` globs user `*.tpl` first, then built-in `*.tpl`.
- `[OP:43]` renders a template only when no output of that name exists yet in `next-theme`, so a theme's own payload file wins over a template. This is the rule that makes `btop.theme` (payload) and `btop.theme.tpl` (template) resolve to the payload.

### Default autostart (omarchy v3.8.4)

- `[OA:5]` `exec-once = uwsm-app -- swaybg -i ~/.config/omarchy/current/background -m fill`. The declaration names the link; retargeting the link changes the wallpaper without editing config.

### Theme payload (omarchy v3.8.4, matte-black)

- `[OM]` the `themes/matte-black` tree lists eight files (`btop.theme`, `colors.toml`, `icons.theme`, `neovim.lua`, `preview.png`, `preview-unlock.png`, `unlock.png`, `vscode.json`) and a `backgrounds/` directory. The backgrounds tree lists `0-ship-at-sea.jpg`, `1-dark-waters.jpg`, `2-dot-hands.jpg`, `omarchy.png`. Tree page SHA-256: 50c1ac25… (theme) and 9e1160a0… (backgrounds).
- `[OM]` raw `themes/matte-black/colors.toml` at the tag is 461 bytes, SHA-256 `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`.

### Swaybg (upstream v1.2.2)

- `[SW:19-31]` documents `-c` (colour), `-i` (image), `-m` (mode: stretch, fill, fit, center, tile; default stretch; `solid_color` shows colour only). Per-output options exist via `-o`.
- `[SM:521-529]` parses `-i` into the image path and `-m` into the mode, logging an error on an invalid mode. `[SM:575-577]` defaults the mode to stretch when an image is given without `-m`.
- `[SM:658-663]` loads each distinct image path in the render loop, and `[SB:24-46]` opens it with `gdk_pixbuf_new_from_file` (or `cairo_image_surface_create_from_png` without gdk-pixbuf), logging failure. The path is opened as given; a symlink resolves at open time.
- `[SR:3-5]` describes swaybg as a wallpaper utility for compositors that implement wlr-layer-shell and `wl_output` version 4.

## Host declaration

Host bytes read with `cat`, `readlink`, `stat`, `sha256sum` and `grep -n` only. Paths under `/home/vgpnk`. The `.bak*` siblings of the consumer files carry the same import lines; they are not loaded and are excluded.

### Current state (`~/.config/omarchy/current/`)

| entry | shape | value / anchor | sha256 | mtime (−0300) |
|---|---|---|---|---|
| `theme.name` | regular file, 12 B | `matte-black` | `48749715228bfa375bd84bef15ea0ad85b2ef88445607e8e6277bed103955c3b` | 2026-10-03 17:49:02.617 |
| `background` | symlink, 71 B | `/home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg` | target `55fa691adfd3fb8a9102b826a28d8de679938f04879799da499b8ace2fe039ac` (1,681,677 B) | 17:49:02.620 |
| `theme/` | directory, 24 files | see the listing below | — | 17:49:02.613 |

- `current/theme/` holds 24 regular files (8 payload + 16 rendered; see the count below) and `backgrounds/` (4 images). Key pins: `waybar.css` `a1807a176659d7d6…`, `swayosd.css` `f88118e98b44cfa3…`, `walker.css` `f44cb45063494d2f…`, `hyprlock.conf` `3ef010e72b5f6911…`, `hyprland.conf` `79126bec8c28da30…`, `alacritty.toml` `8c3d1457c09d32e8…`, `mako.ini` `95bf0c86c955cc81…`, `btop.theme` `e9ee6fb643852b37…`, `colors.toml` `dbdd13a629aac86d…`.
- `current/next-theme` is absent (the swap completed). `~/.config/omarchy/backgrounds/` is absent (no user backgrounds). `~/.config/omarchy/themes/` is empty. `~/.config/omarchy/hooks/theme-set.d/` holds only `show-theme-notification.sample`, which the hook runner skips.

### Payload versus rendered (`[OM]`, `[OP:6,38,43]`)

- The eight host payload files have the same names as the tag's `themes/matte-black` listing. `colors.toml` is byte-identical to the tag (`dbdd13a6…`). The other seven payload files were compared host-to-host only (`current/theme/x` against `~/.local/share/omarchy/themes/matte-black/x`, identical for all seven); their tag bytes were not fetched.
- The count is consistent with the renderer: 8 payload + 17 built-in templates − 1 (`btop.theme`, which the payload supplies and `[OP:43]` skips) = 24. The 16 rendered names are `alacritty.toml`, `chromium.theme`, `foot.ini`, `ghostty.conf`, `gum.env.conf`, `helix.toml`, `hyprland-preview-share-picker.css`, `hyprland.conf`, `hyprlock.conf`, `keyboard.rgb`, `kitty.conf`, `mako.ini`, `obsidian.css`, `swayosd.css`, `walker.css`, `waybar.css`. `[INF]` from source plus count; the rendered bytes were not re-derived.

### Consumers of `current/theme` and `current/background`

| consumer | declaration (host bytes) | resolves to | consumer sha256 |
|---|---|---|---|
| Hyprland core | `~/.config/hypr/hyprland.conf:13` `source = ~/.config/omarchy/current/theme/hyprland.conf` | `current/theme/hyprland.conf` | `ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365` |
| Hyprland default autostart | `~/.config/hypr/hyprland.conf:4` `source = ~/.local/share/omarchy/default/hypr/autostart.conf` | `[OA:5]` swaybg line | host `acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441` = tag |
| user autostart | `~/.config/hypr/autostart.conf` (line 5 is an unrelated `grok-bot` exec) | no swaybg line in the user file | `5ace17016fe2998aa6e7ad2221c1889b430aa4b94faf5ef1f907d6301dd5fc46` |
| hyprlock | `~/.config/hypr/hyprlock.conf:1` `source = ~/.config/omarchy/current/theme/hyprlock.conf`; `:7-12` `background { … path = ~/.config/omarchy/current/background … }` (path at `:10`) | `current/theme/hyprlock.conf`; the link | `b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1` |
| waybar | `~/.config/waybar/style.css:1` `@import "../omarchy/current/theme/waybar.css";` | `current/theme/waybar.css` | `8f335ca01da53d32eb968c2f7752f3149f073e8e56411980913f4dd25d385fdf` |
| swayosd | `~/.config/swayosd/style.css:1` `@import "../omarchy/current/theme/swayosd.css";` | `current/theme/swayosd.css` | `6e3ba08fd929ba345c405c151858a581e2c0ced724ef07e0e23f155731f76d8c` |
| alacritty | `~/.config/alacritty/alacritty.toml:1` `general.import = [ "~/.config/omarchy/current/theme/alacritty.toml" ]` | `current/theme/alacritty.toml` | `695301c86577c808a94a01a4227bfaab3dbbe9a394a9954032f6173adec824f8` |
| walker | `~/.config/walker/config.toml:3-4` `theme = "omarchy-default"`, `additional_theme_location = "~/.local/share/omarchy/default/walker/themes/"`; the theme `style.css:1` `@import "../../../../../../../.config/omarchy/current/theme/walker.css";` (seven `../` from `omarchy-default/` reach `/home/vgpnk`) | `current/theme/walker.css` | config `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787`; style `481267af0e89a475c851de82692176b4b496045e41081fa94eec0fbaf32500b0` |
| mako | `~/.config/mako/config` is a symlink (50 B) to `/home/vgpnk/.config/omarchy/current/theme/mako.ini` | `current/theme/mako.ini` | target `95bf0c86c955cc813d1b60d18e738567c7f135885c5f02a6acfbbb38946e3bec` |
| btop | `~/.config/btop/themes/current.theme` symlink to `current/theme/btop.theme`; `~/.config/btop/btop.conf:5` `color_theme = "current"` | `current/theme/btop.theme` | `e9ee6fb643852b378429fc382badef31180aac4cfdccf7201c6749d1999acda9` |
| neovim | `~/.config/nvim/lua/plugins/theme.lua` symlink (relative, `../../../../.config/omarchy/current/theme/neovim.lua`) | `current/theme/neovim.lua` | — |

Declared edges only. Whether each consumer loads these bytes on this host is `[UNK]`
(§ Unexercised behavior).

### Declared-only (no consumer read here)

`foot.ini`, `kitty.conf`, `ghostty.conf`, `helix.toml`, `keyboard.rgb`, `obsidian.css` and `chromium.theme` are template renders (`[OP:6,38]`) whose consumer (the app or setter script) was not opened in this pass. `vscode.json` and `icons.theme` are payload files that the setters at `[OT:65-70]` read according to the round-7 census (`theme-wallpaper-plane.md` §4); those setter scripts were not fetched here. The three elephant preview images are payload files read by elephant providers per the same census; their use is the P3 note's scope.

### Host binary and tree versions

- `swaybg 1.2.2-1`: `/var/log/pacman.log:1158` `installed swaybg (1.2.2-1)` (2026-10-03T17:44:27-0300). `grep -n swaybg` returns two lines: `:484` (the install command line) and `:1158`. No upgrade line.
- omarchy checkout `~/.local/share/omarchy` at tag `v3.8.4` (see Tag selection). The host copies of `bin/omarchy-theme-set` (`79069c80…`), `bin/omarchy-theme-bg-next` (`ee482812…`), `bin/omarchy-theme-bg-set` (`638f265f…`) and `default/hypr/autostart.conf` (`acb6a668…`) are byte-identical to the tag files named in § Upstream contract.
- Agreement with the round-7 census (`theme-wallpaper-plane.md` §1–§4): `theme.name` pin `48749715…`, background target, the 24-file count, the eight ★ pins and the mako/btop/neovim symlinks match. No contradiction; the round-7 live swaybg observation is not repeated.

## Safe observation

What an operator may read without mutating state:

- `readlink`, `stat`, `cat` and `sha256sum` on the entries in § Host declaration; re-run to detect drift.
- `grep -n -E 'current/(theme|background)'` on `~/.config/hypr`, `~/.config/waybar`, `~/.config/alacritty`, `~/.config/swayosd`, `~/.config/walker` and `~/.local/share/omarchy/default/walker`, excluding `*.bak*` copies.
- `grep -n swaybg /var/log/pacman.log` (a file read; no pacman query).
- Upstream: `curl -sSL` of the raw URLs above at the tags; `git ls-remote --tags https://github.com/swaywm/swaybg` and `… basecamp/omarchy` for tag commits. Fetch receipts are in `.ufo/waves/round-18/fetch/NoteTheme/receipts.jsonl`. Non-credited receipts: `swaybg` `doc/` paths (HTTP 404; the man page is `swaybg.1.scd` at the repo root) and a `themes/matte-black/theme.name` probe (HTTP 404).

Not run under the host pause and not used: `omarchy theme set|current|list|bg …`, `omarchy-theme-bg-next|bg-set`, any `omarchy-restart-*`, `omarchy-hook`, `pkill`, `pgrep`, `hyprctl`, `swaybg`, `pacman`, `systemctl`, `loginctl` and any live probe of a running consumer. The `theme-set` hook directory was listed, not executed.

## Unexercised behavior

- `[UNK]` Whether a swaybg process is running now, its argv, and its layer surface. Round-7 `theme-wallpaper-plane.md` §3.3 recorded PID 1203358 on 2026-10-14; this pass did not re-measure it.
- `[UNK]` Whether the running swaybg re-reads the retargeted link. Swaybg opens the image by path when it loads (`[SM:658-663]`, `[SB:24-46]`) and bg-next/bg-set relaunch swaybg on the link after `ln -nsf` (`[OB:46,49-50]`, `[OS:21,24-25]`); the file read does not show a file watch, and the full `main.c` was not traced for re-load on output change.
- `[UNK]` Whether the current swaybg was started by the last theme set (inferred from the mtimes at 2026-10-03 17:49:02 `[INF]`) or by a later autostart; no process or session state read.
- `[UNK]` Whether any consumer (waybar, swayosd, mako, btop, alacritty, walker, hyprlock, hyprland, neovim) has loaded the current bytes. `[OT:53-62]` restarts several of them at theme-set time; whether those restarts took effect is not observed.
- `[UNK]` Rendering on this host: swaybg `-m fill` scaling of `0-ship-at-sea.jpg` on the 3440×1440 output, colours and layer order, and any hyprlock background draw.
- `[UNK]` The 16 rendered files: their bytes were not re-derived from the templates with the current `colors.toml`; the renderer's output was inferred from the count and source (`[OP:38,43]`).
- `[UNK]` Byte equality of the seven non-`colors.toml` payload files to the tag: names agree, bytes were compared host-to-host only. The 1.68 MB `0-ship-at-sea.jpg` exceeds the 1 MiB fetch cap and was not fetched upstream.
- `[UNK]` Arch packaging of `swaybg 1.2.2-1`: whether the installed binary was built from the v1.2.2 tag without patches. The log records the install only; the binary was not run or queried.
- `[UNK]` Behaviour when `OMARCHY_THEME_SKIP_BACKGROUND=1` is set in the environment; the host environment was not read.
- `[UNK]` Walker and elephant's use of the preview images and the theme's `icons.theme`, `vscode.json`, `neovim.lua` and `chromium.theme` consumers: declared-only here (§ Declared-only).
