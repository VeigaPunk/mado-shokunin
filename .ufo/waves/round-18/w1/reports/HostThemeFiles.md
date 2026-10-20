# HostThemeFiles — host theme file bytes (round 18, P5 anchor)

Seat: MadoR18.HostThemeFiles (leaf, file-bytes only). Date: 2026-10-20.
Scope: `~/.config/omarchy/current/*`, `~/.config/omarchy/themes/`, and the
`~/.local/share/omarchy` checkout read strictly as file bytes. No pacman/yay/expac, no
loginctl/systemctl/journalctl, no walker/swaybg/waybar/omarchy command, no git command run
inside the checkout. Confidence tags: **Observed** = command output on this host;
**[INFERENCE]** = reasoning from observed bytes + script source.

## 1. Anchors

| anchor | value | confidence |
|---|---|---|
| `~/.config/omarchy/current/theme.name` | regular file, 12 bytes, mode 644, `matte-black\n` (hex `6d 61 74 74 65 2d 62 6c 61 63 6b 0a`) | Observed (`od -An -tx1 -c`) |
| sha256 `theme.name` | `48749715228bfa375bd84bef15ea0ad85b2ef88445607e8e6277bed103955c3b` | Observed |
| `~/.config/omarchy/current` | real directory (not a symlink), 3 entries: `background`, `theme/`, `theme.name` | Observed |
| `~/.config/omarchy/current/theme` | **real directory (copied dir), NOT a symlink**; `readlink -f` returns the path itself; `stat -c %F` = `directory`; inode 27311, nlink 1 | Observed |
| `current/theme` contents | 28 regular files, 0 symlinks, 1 subdir (`backgrounds/`); top level 24 files | Observed (`find . -type f | wc -l` = 28, `-type l` = 0) |
| `~/.config/omarchy/current/background` | **symlink** (71-char absolute link string) → `/home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg`; target is a regular 1681677-byte file, sha256 `55fa691a…e039ac`; link mtime `2026-10-03T17:49:02.620233763-03:00` | Observed |
| `~/.config/omarchy/themes/` | real directory, **0 entries** (empty; no user theme overlays) | Observed (`find -mindepth 1 | wc -l` = 0) |
| `current/theme` modes | dirs 755, files 644, owner/group `vgpnk:vgpnk` | Observed |
| `current/theme` mtime | `2026-10-03T17:49:02.613233762-03:00`; `background` link and `theme.name` in the same second | Observed |

`theme.name` semantics: omarchy stores the raw name, not a display label
(`omarchy-theme-current` reads the same file and only re-formats for display). Value
`matte-black` names the checkout theme `~/.local/share/omarchy/themes/matte-black/`.

## 2. Symlink vs copied dir — verdict

- `current/theme` is a **copied directory** materialized by `omarchy-theme-set`: the script
  builds `current/next-theme`, copies theme files in, renders templates, then
  `rm -rf` + `mv` swaps it into place (`~/.local/share/omarchy/bin/omarchy-theme-set:25,29,41,42`).
  It is **not** a symlink to the checkout and not a symlink into `~/.config/omarchy/themes/`.
- `current/background` is the **only symlink** in the inspected tree, and it is **absolute**,
  pointing into the copied theme's own `backgrounds/` dir.
  `omarchy-theme-bg-next:46` creates it with `ln -nsf "$NEW_BACKGROUND"`; `$NEW_BACKGROUND`
  comes from `find -L "$THEME_BACKGROUNDS_PATH" …` (line 11) where
  `THEME_BACKGROUNDS_PATH="$HOME/.config/omarchy/current/theme/backgrounds/"` is absolute, so
  `find` emits absolute paths and the next cycle's `readlink` comparison (line 21) matches.
  [INFERENCE — the absolute link target is exactly what that code path produces; the link may
  also have been inherited from an earlier `theme set`.]
- `~/.config/omarchy/themes/` being empty plus `omarchy-theme-set:30` copying
  `$USER_THEMES_PATH/$THEME_NAME/*` with errors suppressed means there is **no user overlay**
  for `matte-black`; `cp` of a missing dir silently no-ops (`2>/dev/null`).

## 3. Origin of the 28 files (copy vs template render)

Checkout `~/.local/share/omarchy/themes/matte-black/` holds 12 files (8 top-level +
4 backgrounds). All 12 are byte-identical to their `current/theme` counterparts (explicit
`MATCH` loop for each: `btop.theme`, `colors.toml`, `icons.theme`, `neovim.lua`,
`preview.png`, `preview-unlock.png`, `unlock.png`, `vscode.json`, and the 4 backgrounds).

The 16 remaining files are rendered from `~/.local/share/omarchy/default/themed/*.tpl` by
`omarchy-theme-set-templates` at set time (template list = 17; `btop.theme.tpl` exists but the
renderer skips any output that already exists, `omarchy-theme-set-templates:43`, so the
copied `btop.theme` wins — its sha256 matches the checkout copy `e9ee6fb6…`, not the template
`fadc4fdc…`). Rendered set:

`alacritty.toml`, `chromium.theme`, `foot.ini`, `ghostty.conf`, `gum.env.conf`, `helix.toml`,
`hyprland-preview-share-picker.css`, `hyprland.conf`, `hyprlock.conf`, `keyboard.rgb`,
`kitty.conf`, `mako.ini`, `obsidian.css`, `swayosd.css`, `walker.css`, `waybar.css`.

mtime split corroborates the two sources: copied entries and backgrounds share
`17:49:02.541927358`, template outputs run `17:49:02.585…` through `.614` (sequential sed
writes), while the checkout source files are `17:42:33.8–.9`. So the theme was set/copied at
`17:49:02` from a checkout unpacked at `17:42`.

User template overlay dir `~/.config/omarchy/themed/` contains only
`alacritty.toml.tpl.sample` (1 file, not a `.tpl`), so no user template overrides are active.

## 4. sha256 + size of every file in `current/theme` (Observed)

```
8c3d1457c09d32e83367ac946ff6e85f6bda334c302587a043bef7dc7ac09139	772	alacritty.toml
55fa691adfd3fb8a9102b826a28d8de679938f04879799da499b8ace2fe039ac	1681677	backgrounds/0-ship-at-sea.jpg
98f0c2b65a2587d114949e8125c22f891c993e0305ca36537bd9b7a9869e8a93	1033920	backgrounds/1-dark-waters.jpg
e8d73aa65be29bf9d0bec62f64add450485ca52367701ff683e0f2bd66f0791a	482067	backgrounds/2-dot-hands.jpg
63d002b2320cef0184d79bb44fbf4062780d2c083428acf16191344084b75a8f	4491	backgrounds/omarchy.png
e9ee6fb643852b378429fc382badef31180aac4cfdccf7201c6749d1999acda9	2648	btop.theme
e02da2b72d23d24c9f70ce52e737485c2163e143a21331d2f23ee76aa900e572	9	chromium.theme
dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786	461	colors.toml
d9c2e20e079a9314ec4cfd87370436ee0f34759a76bcdb0d5e1128ce672dcbeb	378	foot.ini
418636f99922f1ea64de37354fbb2708dd27c9d5f577ea63dd04d8d39b81203e	454	ghostty.conf
ecab9ec497c555155536913c09e03e612f1e91296953ead8e9052da310f3435f	5413	gum.env.conf
c7f85d447f480b00710c075f8d1cbf25e56b4c8b757ff1f06b33b7a7bd50544c	4582	helix.toml
79126bec8c28da306712148734a3ee58335a8bd48bf863e4e2e2db6d6d8344b6	143	hyprland.conf
24474e34a4ed902250858eec8562838de33ce4a2782c5026ab764eb4cf6566c9	1844	hyprland-preview-share-picker.css
3ef010e72b5f69113e1500bb083fb053f9f121212ad5ed4fe74ad8d12507ad0b	176	hyprlock.conf
1c2342215182a8e2880028e03e679fad194dbdfa5155b55daf8386390526cfbc	9	icons.theme
8f32a6ecf0de6c50032550d719422b9aca409126c6b75cdc5189b099ef9e6f5e	8	keyboard.rgb
e8795b49ff5b6135f15243e73a45a9e970acfd09b2a30ae459fa6a163c0d4187	444	kitty.conf
95bf0c86c955cc813d1b60d18e738567c7f135885c5f02a6acfbbb38946e3bec	119	mako.ini
ec7df5fb1d3b7fc644fa0f69cd959ebc43fad8ebdb4aedfd01a5b1e387cd9778	150	neovim.lua
d195eeaf760f9d8781bad760445dde36e77fb975c10768a00f9b5389d08657c1	2523	obsidian.css
02bf70793f2617710885cc8e389d3d00186b46e1a5a3fe5ffebe776b4ae5ae18	470315	preview.png
00ae994f78564d06c08b17eff733073217400b2bfa2f18405ae10e4b34afe212	22524	preview-unlock.png
f88118e98b44cfa32ebc2d8f2394bd0448b2d1e0c01f01dd48677fe66ec7522b	166	swayosd.css
ac806f14a214140f33e6c222879633ea24b194f59a86c59847e67bb379680c2d	2512	unlock.png
18171ea89a57d4639b935d80a6b271c19a23e4ebe682cc0703144bb77474b83c	65	vscode.json
f44cb45063494d2f4a8f489c47d8901b3bc98b27fbd1ca1c5a8801b40606bbc0	191	walker.css
a1807a176659d7d6beaaf2a5c96cb7a03d131ee2740b8961d4c9aee393839c18	68	waybar.css
```

Render-governance anchors for downstream note authors (Observed):

```
colors.toml  sha256 dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786
  accent="#e68e0d" cursor="#eaeaea" foreground/background="#bebebe"/"#121212"
walker.css   sha256 f44cb45063494d2f4a8f489c47d8901b3bc98b27fbd1ca1c5a8801b40606bbc0  (191 B)
waybar.css   sha256 a1807a176659d7d6beaaf2a5c96cb7a03d131ee2740b8961d4c9aee393839c18  (68 B)
hyprland.conf sha256 79126bec8c28da306712148734a3ee58335a8bd48bf863e4e2e2db6d6d8344b6 (143 B, sets col.active_border=rgb(e68e0d))
```

Template sources (Observed): `~/.local/share/omarchy/default/themed/walker.css.tpl`
sha256 `d7faea3d…efeec0e`, `waybar.css.tpl` sha256 `71290219…62a3d6`. Walker/Waybar configs are
**generated** into the copied theme dir — there is no symlink from a live config dir in this tree.

## 5. Reproduce

```sh
cat ~/.config/omarchy/current/theme.name; od -An -tx1 -c ~/.config/omarchy/current/theme.name
readlink -f ~/.config/omarchy/current/theme
readlink  ~/.config/omarchy/current/background
readlink -f ~/.config/omarchy/current/background
ls -la --time-style=full-iso ~/.config/omarchy/current/ ~/.config/omarchy/current/theme/ \
  ~/.config/omarchy/current/theme/backgrounds/ ~/.config/omarchy/themes/
find ~/.config/omarchy/current/theme -type f -print0 | sort -z | xargs -0 sha256sum
find ~/.config/omarchy/current/theme -type l
```

## 6. Not established here

- No live behaviour was observed: no walker/swaybg/waybar process state, no theme consumers,
  no parsing of these files by any binary (host binaries stay `[UNK]`).
- The `~/.local/share/omarchy` checkout's tag/commit (contract says v3.8.4) was not verified by
  this seat; only the files above, read as bytes, are evidenced. No git command was run there.
- Whether `current/background` was written by the `17:49:02` set run or inherited earlier is
  not provable from bytes alone; only that the link is absolute and resolves into
  `current/theme/backgrounds/`.
- `~/.config/omarchy/themes/` emptiness is observed at one instant; no claim about future
  user-theme installs.
