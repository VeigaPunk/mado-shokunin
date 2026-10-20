# SrcOmarchyThemeLayout — omarchy v3.8.4 theme layout (documentary, P5/P3)

Seat: SrcOmarchyThemeLayout. Feeds C2: primary `theme-route-r18.md` (P5), secondary
`walker-route-r18.md` (P3, walker.css generation). Documentary only: no theme was applied,
no host binary was run, no behaviour is claimed. Reserved source id: `S0xx-pending` (L1 assigns).

## Method and receipts

Fetch protocol followed: `curl -sSL --max-time 60`, no auth/cookies; one JSON receipt per body in
`.ufo/waves/round-18/fetch/SrcOmarchyThemeLayout/receipts.jsonl`; bodies in the same directory.
9 receipts, all `http_status: 200`, all validated against `mado-fetch-receipt-v1` keys.

| body | bytes | sha256 (first 16) | url |
|---|---|---|---|
| tree-v3.8.4-8fcc9d6.json | 401538 | c5facb09086f11c1 | api.github.com/repos/basecamp/omarchy/git/trees/8fcc9d6…?recursive=1 |
| tokyo-night.contents.json | 9357 | 6b8a8ed20b191763 | api.github.com/repos/basecamp/omarchy/contents/themes/tokyo-night?ref=v3.8.4 |
| tokyo-night.colors.toml | 461 | 1551ea824b04fd77 | raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/tokyo-night/colors.toml |
| tokyo-night.btop.theme | 1765 | 313c2186d059f2b1 | …/v3.8.4/themes/tokyo-night/btop.theme |
| lumon.hyprland.conf | 553 | 4cd2a08225c3410e | …/v3.8.4/themes/lumon/hyprland.conf |
| omarchy-theme-set | 2147 | 79069c8018a7d6d2 | …/v3.8.4/bin/omarchy-theme-set |
| omarchy-theme-set-templates | 1728 | 01264122666b3d49 | …/v3.8.4/bin/omarchy-theme-set-templates |
| alacritty.toml.tpl | 988 | 8fb009d72101a203 | …/v3.8.4/default/themed/alacritty.toml.tpl |
| version-at-tag | 6 | 0a5c29521592a324 | …/v3.8.4/version |

Tooling: curl 8.23.0 only. No packages installed or upgraded. No pacman/yay/expac, no
systemctl/journalctl/hyprctl/omarchy-* command, and no git command inside the omarchy checkout.

## Tag → commit

`git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4 'refs/tags/v3.8.4^{}'` returned
exactly one line, no peeled (`^{}`) line:

    8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4

[OBSERVED] lightweight tag → commit `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`. The recursive tree
at that commit was fetched with `truncated: false`; every path below is a path *at that commit*.
A tag's source never proves the installed host binary; host binaries stay [UNK].

## themes/ listing at v3.8.4 — 19 dirs, 245 blobs

`api.github.com/repos/basecamp/omarchy/git/trees/8fcc9d6…?recursive=1`, `truncated:false`:

catppuccin, catppuccin-latte, ethereal, everforest, flexoki-light, gruvbox, hackerman, kanagawa,
lumon, matte-black, miasma, nord, osaka-jade, retro-82, ristretto, rose-pine, tokyo-night,
vantablack, white.

Per-theme blob counts and non-template extras (from the tree; `backgrounds/` contents counted in
the blob total, not listed as an extra):

| theme | blobs | backgrounds | extras beyond base set |
|---|---|---|---|
| catppuccin | 13 | 4 | waybar.css |
| catppuccin-latte | 11 | 2 | light.mode |
| ethereal | 11 | 3 | — |
| everforest | 10 | 2 | — |
| flexoki-light | 12 | 2 | chromium.theme, light.mode |
| gruvbox | 14 | 6 | — |
| hackerman | 11 | 3 | — |
| kanagawa | 11 | 2 | hyprland.conf |
| lumon | 15 | 3 | chromium.theme, hyprland.conf, swayosd.css, waybar.css |
| matte-black | 12 | 4 | — |
| miasma | 11 | 3 | — |
| nord | 12 | 4 | — |
| osaka-jade | 12 | 4 | — |
| retro-82 | 21 | 9 | chromium.theme, hyprland.conf, swayosd.css, waybar.css |
| ristretto | 13 | 5 | — |
| rose-pine | 14 | 4 | chromium.theme, light.mode |
| tokyo-night | 16 | 7 | keyboard.rgb |
| vantablack | 13 | 5 | — |
| white | 13 | 4 | light.mode |

Base set present in **all 19** themes (top-level, verified programmatically, `missing=[]`):
`colors.toml`, `btop.theme`, `icons.theme`, `neovim.lua`, `vscode.json`, `preview.png`,
`preview-unlock.png`, `unlock.png`. `backgrounds/omarchy.png` is present in 18/19; flexoki-light
is the exception (its backgrounds are `1-orb.png`, `2-omarchy.png`).

## One theme in full: tokyo-night (16 blobs)

Cross-checked by two independent listings: the recursive tree at commit 8fcc9d6 and
`GET /contents/themes/tokyo-night?ref=v3.8.4` (10 entries = 9 files + `backgrounds/` dir).

    themes/tokyo-night/backgrounds/0-swirl-buck.jpg
    themes/tokyo-night/backgrounds/1-sunset-lake.png
    themes/tokyo-night/backgrounds/2-pawel-czerwinski.jpg
    themes/tokyo-night/backgrounds/3-milad-fakurian.jpg
    themes/tokyo-night/backgrounds/4-oma-cityscape.jpg
    themes/tokyo-night/backgrounds/5-oma.jpg
    themes/tokyo-night/backgrounds/omarchy.png
    themes/tokyo-night/btop.theme
    themes/tokyo-night/colors.toml
    themes/tokyo-night/icons.theme
    themes/tokyo-night/keyboard.rgb
    themes/tokyo-night/neovim.lua
    themes/tokyo-night/preview-unlock.png
    themes/tokyo-night/preview.png
    themes/tokyo-night/unlock.png
    themes/tokyo-night/vscode.json

## Two fetched theme files

`themes/tokyo-night/colors.toml` (23 lines, sha256 1551ea82…): six named colors plus
`color0`–`color15`. Anchors: line 1 `accent = "#7aa2f7"`; line 4 `background = "#1a1b26"`.
This is the only color source the template renderer reads.

`themes/tokyo-night/btop.theme` (82 lines, sha256 313c2186…): btop's `theme[key]` form.
Anchors: line 1 `# Theme: tokyo-night`; line 5 `theme[main_bg]="#1a1b26"`.

`themes/lumon/hyprland.conf` (26 lines, sha256 4cd2a082…, fetched as the override specimen):
line 1 `$activeBorderColor = rgb(f2fcff)`; line 9 `gaps_in = 8`. Note it carries layout keys
(`gaps_in`, `gaps_out`), not only colors.

## Premise check: tokyo-night has no hyprland.conf and no alacritty.toml

The assignment's example paths do not exist at v3.8.4. tokyo-night's 16 blobs (above) contain
neither. `hyprland.conf` exists only for kanagawa, lumon, retro-82; `alacritty.toml` exists for
**no** theme. Alacritty colors are rendered from `default/themed/alacritty.toml.tpl` into
`~/.config/omarchy/current/theme/alacritty.toml`.
[INFERENCE] Assuming a theme ships app configs named after the app is wrong for this tag; the
dispatch is template-first with theme-copy override (below).

## Which consumer files a theme provides

Renderer order (`bin/omarchy-theme-set`, sha256 79069c80…):
line 28 `# Copy official theme first, then overlay user customizations on top`; line 29 copies
`$OMARCHY_PATH/themes/<name>/*`, line 30 copies `~/.config/omarchy/themes/<name>/*` over it;
line 38 calls `omarchy-theme-set-templates`; line 45 writes `current/theme.name`; line 49 calls
`omarchy-theme-bg-next` unless `OMARCHY_THEME_SKIP_BACKGROUND=1`.

`bin/omarchy-theme-set-templates` (sha256 01264122…) renders every `default/themed/*.tpl` (17
templates) by substituting `colors.toml` keys, but:
line 37 `# Process user templates first, then built-in templates (user overrides built-in)` and
line 42 `# Don't overwrite configs already exists in the output directory (copied from theme specific folder)`.
So a file carried by the theme with the same basename suppresses the template. A theme
"provides" a consumer config in exactly two ways: as a copied asset, or as a copied override.

### A. Always theme-provided (all 19), consumed directly

| theme file | consumer | wiring evidence |
|---|---|---|
| colors.toml | renderer input; plymouth colors | `bin/omarchy-theme-set-templates:9`; `bin/omarchy-plymouth-set-by-theme:23-24` |
| btop.theme | btop theme file | `install/config/theme.sh:18` symlinks to `~/.config/btop/themes/current.theme` |
| icons.theme | GNOME icon theme | `bin/omarchy-theme-set-gnome:15-18` reads it into `gsettings icon-theme` |
| neovim.lua | Neovim colorscheme plugin | linked outside this repo at `~/.config/nvim/lua/plugins/theme.lua`; `migrations/1784518937.sh:9` retargets that link [INFERENCE: created by omarchy-nvim] |
| vscode.json | VS Code/Codium/Cursor theme name+extension | `bin/omarchy-theme-set-vscode:6,20-25` |
| preview.png | theme picker preview | `default/elephant/omarchy_themes.lua:33` |
| preview-unlock.png | plymouth unlock preview | `default/elephant/omarchy_unlocks.lua:49` |
| unlock.png | plymouth boot logo | `bin/omarchy-plymouth-set-by-theme:26` |
| backgrounds/ | desktop background cycle | `bin/omarchy-theme-bg-next:7`; relaunch `swaybg -i "$CURRENT_BACKGROUND_LINK" -m fill` at `:50` |
| light.mode (4 themes) | presence-only light flag | `bin/omarchy-theme-set-gnome:6`; `default/pi/agent/extensions/omarchy-system-theme.ts:13` |

### B. Theme-carried overrides of template outputs (copy wins over render)

| override | themes carrying it | consumer wiring |
|---|---|---|
| hyprland.conf | kanagawa, lumon, retro-82 | `config/hypr/hyprland.conf:13` `source = ~/.config/omarchy/current/theme/hyprland.conf` |
| waybar.css | catppuccin, lumon, retro-82 | `config/waybar/style.css:1` `@import` |
| swayosd.css | lumon, retro-82 | `config/swayosd/style.css:1` `@import` |
| chromium.theme | flexoki-light, lumon, retro-82, rose-pine | `bin/omarchy-theme-set-browser:6` |
| keyboard.rgb | tokyo-night | `bin/omarchy-theme-set-keyboard-asus-rog:6`, `…-f16:6` |
| btop.theme | all 19 (template exists but is shadowed) | `install/config/theme.sh:18` |

### C. Template-rendered only at v3.8.4 (theme provides no file for these)

17 templates in `default/themed/`: `alacritty.toml`, `btop.theme`, `chromium.theme`, `foot.ini`,
`ghostty.conf`, `gum.env.conf`, `helix.toml`, `hyprland-preview-share-picker.css`,
`hyprland.conf`, `hyprlock.conf`, `keyboard.rgb`, `kitty.conf`, `mako.ini`, `obsidian.css`,
`swayosd.css`, `walker.css`, `waybar.css`. Consumers: `config/alacritty/alacritty.toml:1`,
`config/foot/foot.ini:2`, `config/ghostty/config:2`, `config/kitty/kitty.conf:1`,
`config/hypr/hyprlock.conf:1`, `default/hypr/envs.conf:3`, `config/hyprland-preview-share-picker/config.yaml:4`,
`config/walker/config.toml:3` + `default/walker/themes/omarchy-default/style.css:1`
(`@import …current/theme/walker.css`). `mako.ini` is symlinked at install
(`install/config/theme.sh:21`); `helix.toml` via `bin/omarchy-install-helix:11`; `obsidian.css`
copied by `bin/omarchy-theme-set-obsidian:6`.

## Host declaration (file reads only)

- `~/.local/share/omarchy/.git/HEAD` = `ref: refs/heads/master`; `.git/packed-refs:2` has
  `8fcc9d6048af4cb0e3af8512c78049857a3b53dd refs/heads/master`; `.git/packed-refs:508` has
  `8fcc9d6048af4cb0e3af8512c78049857a3b53dd refs/tags/v3.8.4`. So the checkout is at the tagged
  commit, on branch master.
- All **245** `themes/` blobs in the checkout were re-hashed as git blobs and compared with the
  tree at 8fcc9d6: `missing=[] mismatch=[] extra_local_files=[]`. The checkout's theme tree is
  byte-identical to v3.8.4.
- `version` file content is `3.8.3\n` (sha256 0a5c2952…), identical to raw `/v3.8.4/version`.
  The v3.8.4 tag tree therefore self-reports 3.8.3. [OBSERVED] [UNK: release-procedure reason;
  do not use the `version` file as tag proof.]
- Current host state bytes: `~/.config/omarchy/current/theme.name` = `matte-black`;
  `current/theme/` holds 25 entries (17 rendered consumer files + base assets + `backgrounds/`);
  `~/.config/omarchy/themes/` is empty (no user overlays);
  `current/background` → `…/theme/backgrounds/0-ship-at-sea.jpg`;
  `~/.config/btop/themes/current.theme` → `…/current/theme/btop.theme`;
  `~/.config/mako/config` → `…/current/theme/mako.ini`;
  `~/.config/nvim/lua/plugins/theme.lua` → `…/current/theme/neovim.lua`.
  This is declared file state, not exercised behaviour.

## Candidate SOURCES row (draft; L1 assigns id, tier, mined flag)

`S0xx-pending` — basecamp/omarchy, tag v3.8.4 = 8fcc9d6048af4cb0e3af8512c78049857a3b53dd.
Upstream https, docs/spec/code: `themes/` tree (19 themes, 245 blobs), `bin/omarchy-theme-set`,
`bin/omarchy-theme-set-templates`, `default/themed/*.tpl`, `config/walker/config.toml`,
`default/walker/themes/omarchy-default/style.css`. Scope names theme, wallpaper/swaybg, walker.
Receipts: `.ufo/waves/round-18/fetch/SrcOmarchyThemeLayout/` (9 receipts, bodies + sha256).
Proposed used-by: `theme-route-r18.md` (P5), optionally `walker-route-r18.md` (P3).

## What the route notes may cite (documentary, no observed behaviour)

- P5 `## Upstream contract`: theme directory schema (base set above); copy precedence official →
  user overlay (`omarchy-theme-set:28-30`); colors.toml key schema; template-first rendering with
  theme-copy suppression (`omarchy-theme-set-templates:37,42`); background cycle uses
  `swaybg … -m fill` (`omarchy-theme-bg-next:50`) and no theme background falls back to
  `swaybg --color '#000000'` (`:17`).
- P3 `## Upstream contract`: walker.css is generated from `default/themed/walker.css.tpl`
  (`@define-color selected-text {{ accent }}` at :1), never supplied by these 19 themes; walker
  selects theme `omarchy-default` (`config/walker/config.toml:3`) from
  `additional_theme_location` (`:4`), whose `style.css:1` imports the generated
  `~/.config/omarchy/current/theme/walker.css`.
- P5/P3 `## Host declaration`: checkout at 8fcc9d6 (tag v3.8.4) with 245/245 theme blobs verified;
  current theme `matte-black`; version file says 3.8.3.
- `## Unexercised behavior`: theme application, walker UI rendering, swaybg transitions, and all
  host binaries remain unexecuted; record `[UNK]` there.

## Unknowns / gaps

- [UNK] Why tag v3.8.4's tree contains `version` = 3.8.3.
- [UNK] Installed `omarchy` package version and whether host binaries match this checkout
  (pacman queries are paused host-wide).
- [UNK] Runtime behaviour of `omarchy-theme-set` (never executed), including whether all consumer
  apps are present on this host.
- [UNK] Content of `~/.config/omarchy/themed` user templates on host (not read; not needed for
  this item).
- [INFERENCE] `neovim.lua`'s consumer link is created outside this repo; only a migration that
  repairs it is in-tree.
