# HostThemeConsumers — `~/.config/omarchy/current` consumer table

Round 18 W1 scout (leaf). Question: which host files import/read
`~/.config/omarchy/current`, at which line, with which imported path, and what is the
sha256 of each consumer file. Bytes-only evidence; no process, systemd, compositor,
package-manager or omarchy command was run. All reads on 2026-10-20.

## Method

1. Literal assigned command, over the assigned roots:

   ```
   grep -rn 'omarchy/current' ~/.config/hypr ~/.config/waybar ~/.config/alacritty \
     ~/.config/mako ~/.config/walker ~/.config/btop ~/.config/swayosd \
     ~/.local/share/omarchy/default
   ```

   Result: **20 matches in 17 files** (rc 0). `~/.config/mako`, `~/.config/walker`
   and `~/.config/btop` contributed **zero** matches — see §2.
2. Completeness sweep: same literal over all of `~/.config` (browser/cache dirs
   excluded) → 4 further live consumers outside the assigned roots (§3).
3. Symlink pass: `find ~/.config -type l` (41 links; 8 omarchy/theme related), because
   GNU `grep -r` does not follow symlinks met during recursion (§2.1).
4. Identity: `sha256sum` on the consumer path as written (a symlink hashes its target's
   bytes); `stat -c %F %i %h %s` to separate copies from links; `realpath -m` to check
   each import resolves.
5. Producer scripts in `~/.local/share/omarchy/bin/` read as bytes (read-only) to bound
   the consumer contract; no git command run inside that checkout (`.git` files read as
   bytes). Two raw upstream `version` fetches, receipts in §9.

`~` below = `/home/vgpnk`. Hashes truncated to 8 hex in prose, full values in tables.

## 1. Assigned-root grep hits — consumer table

| # | consumer file (`~`) | line | imported path (verbatim) | sha256(consumer file) | state |
|---|---|---|---|---|---|
| 1 | `.config/hypr/hyprland.conf` | 13 | `~/.config/omarchy/current/theme/hyprland.conf` | `ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365` | LIVE — Hyprland main config |
| 2 | `.config/hypr/hyprland.conf.bak.1792267376` | 13 | `~/.config/omarchy/current/theme/hyprland.conf` | `4f52854a3c143dcf58430a679e339619223d2b5008115a322d06b2de637ea462` | DEAD — backup |
| 3 | `.config/hypr/hyprlock.conf` | 1 | `~/.config/omarchy/current/theme/hyprlock.conf` | `b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1` | CONDITIONAL — hyprlock only |
| 4 | `.config/hypr/hyprlock.conf` | 10 | `~/.config/omarchy/current/background` | `b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1` | CONDITIONAL — hyprlock background asset |
| 5 | `.config/waybar/style.css` | 1 | `../omarchy/current/theme/waybar.css` | `8f335ca01da53d32eb968c2f7752f3149f073e8e56411980913f4dd25d385fdf` | LIVE — waybar autostart |
| 6 | `.config/waybar/style.css.bak.20261003-190229` | 1 | `../omarchy/current/theme/waybar.css` | `04d4e5f68dafba8785a02a2b3c57b59f16604bc76b92f13d3cfe86810e47c952` | DEAD |
| 7 | `.config/waybar/style.css.bak.1791314470` | 1 | `../omarchy/current/theme/waybar.css` | `2f4e01b5108f6400be7cd8ef6f0aa102a5d8da8d4e21023111c079809d467e16` | DEAD |
| 8 | `.config/waybar/style.css.bak.1792203278` | 1 | `../omarchy/current/theme/waybar.css` | `8316c08ceaa7e3f0624e1b82b1e03523096820fbf775362a930d7f831b0c4e8f` | DEAD |
| 9 | `.config/waybar/style.css.bak.1792267376` | 1 | `../omarchy/current/theme/waybar.css` | `8316c08ceaa7e3f0624e1b82b1e03523096820fbf775362a930d7f831b0c4e8f` | DEAD — byte-dup of #8 |
| 10 | `.config/waybar/style.css.pre-ai-readability` | 1 | `../omarchy/current/theme/waybar.css` | `c9215e9ee3053e19a07fb5618150fa46f6b3af36cc75aba930db31bd022b4782` | DEAD |
| 11 | `.config/alacritty/alacritty.toml` | 1 | `~/.config/omarchy/current/theme/alacritty.toml` | `695301c86577c808a94a01a4227bfaab3dbbe9a394a9954032f6173adec824f8` | LIVE |
| 12 | `.config/alacritty/alacritty.toml.bak.20261003-190229` | 1 | `~/.config/omarchy/current/theme/alacritty.toml` | `ea3e0fa094ca2c763d284dbba39730ee3638ed20c97da6e69adb45f77ee1207a` | DEAD |
| 13 | `.config/swayosd/style.css` | 1 | `../omarchy/current/theme/swayosd.css` | `6e3ba08fd929ba345c405c151858a581e2c0ced724ef07e0e23f155731f76d8c` | LIVE — `swayosd-server.service` enabled (§7) |
| 14 | `.local/share/omarchy/default/elephant/omarchy_background_selector.lua` | 30 | `home .. "/.config/omarchy/current/theme.name"` | `292c7deb0ddc0d006728a3c9740cf196c818240af5d24b7c0cb9a2e2bab5f7eb` | CONDITIONAL — provider call |
| 15 | `.local/share/omarchy/default/elephant/omarchy_background_selector.lua` | 38 | `home .. "/.config/omarchy/current/theme/backgrounds"` | `292c7deb0ddc0d006728a3c9740cf196c818240af5d24b7c0cb9a2e2bab5f7eb` | CONDITIONAL — provider call |
| 16 | `.local/share/omarchy/default/hypr/autostart.conf` | 5 | `~/.config/omarchy/current/background` (`swaybg -i … -m fill`) | `acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441` | LIVE — sourced by `hyprland.conf:4` |
| 17 | `.local/share/omarchy/default/hypr/envs.conf` | 3 | `~/.config/omarchy/current/theme/gum.env.conf` | `80067da7b52fe1b45812f3d98cf44c025a693235e7380f4f405915ee4bf680fe` | LIVE — sourced by `hyprland.conf:9` |
| 18 | `.local/share/omarchy/default/pi/agent/extensions/omarchy-system-theme.ts` | 5 | `~/.config/omarchy/current/theme/light.mode` (doc comment) | `6dc29806fdef89914a70e24b02d9fb103614a978ffcef3ffbac7a9e22dc02f71` | UNEXERCISED — extension not deployed (§7) |
| 19 | `.local/share/omarchy/default/pi/agent/extensions/omarchy-system-theme.ts` | 13 | `home, ".config/omarchy/current/theme/light.mode"` | `6dc29806fdef89914a70e24b02d9fb103614a978ffcef3ffbac7a9e22dc02f71` | UNEXERCISED — same |
| 20 | `.local/share/omarchy/default/walker/themes/omarchy-default/style.css` | 1 | `../../../../../../../.config/omarchy/current/theme/walker.css` | `481267af0e89a475c851de82692176b4b496045e41081fa94eec0fbaf32500b0` | LIVE when walker launches (§2.3) |

Sum check: rows 1–20 = 20 matches over 17 files. Breakdown: hypr 4, waybar 6,
alacritty 2, swayosd 1, omarchy/default 7.

## 2. grep-invisible consumers

### 2.1 Why the assigned command cannot see them (control test)

GNU `grep -r` follows symlinks only on the command line, not those met during
recursion. Reproduced:

```
$ mkdir /tmp/gt2; printf 'omarchy/current\n' >/tmp/gt-target.txt; ln -s /tmp/gt-target.txt /tmp/gt2/link.txt
$ grep -rn 'omarchy/current' /tmp/gt2 ; echo rc=$?      -> rc=1 (no match)
$ grep -Rn 'omarchy/current' /tmp/gt2                   -> /tmp/gt2/link.txt:1:omarchy/current
```

Same on the host: `grep -rn 'omarchy/current' ~/.config/elephant` → rc 1, although
every menu there is a symlink to a default-tree Lua file whose lines 30/38 match
(rows 14–15). Consequences: `~/.config/mako` and `~/.config/btop` (both assigned roots)
report zero hits even though both are live theme consumers, and a whole consumer
(`~/.config/nvim/.../theme.lua`) is invisible to the assigned sweep.

### 2.2 Symlink consumers (observed with `find -type l` + `readlink`)

| consumer file (`~`) | line | link target / imported path | sha256 (resolved consumer bytes) | state |
|---|---|---|---|---|
| `.config/mako/config` | n/a (whole file is a link) | `/home/vgpnk/.config/omarchy/current/theme/mako.ini` | `95bf0c86c955cc813d1b60d18e738567c7f135885c5f02a6acfbbb38946e3bec` | LIVE — mako `exec-once` (`autostart.conf:2`) |
| `.config/btop/themes/current.theme` | n/a (link) | `/home/vgpnk/.config/omarchy/current/theme/btop.theme` | `e9ee6fb643852b378429fc382badef31180aac4cfdccf7201c6749d1999acda9` | LIVE when btop starts (`btop.conf:5 color_theme = "current"`) |
| `.config/nvim/lua/plugins/theme.lua` | n/a (link) | `../../../../.config/omarchy/current/theme/neovim.lua` | `ec7df5fb1d3b7fc644fa0f69cd959ebc43fad8ebdb4aedfd01a5b1e387cd9778` | LIVE when nvim starts (lazy `{ import = "plugins" }`) |
| `.config/elephant/menus/omarchy_background_selector.lua` | n/a (link) | `/home/vgpnk/.local/share/omarchy/default/elephant/omarchy_background_selector.lua` | `292c7deb0ddc0d006728a3c9740cf196c818240af5d24b7c0cb9a2e2bab5f7eb` | CONDITIONAL — elephant menu provider |
| `.config/elephant/menus/omarchy_themes.lua` | — | `…/default/elephant/omarchy_themes.lua` | `d997d5a4c27ffc109a4302075fd4f12445ddc1fc44eea3ec28a37dd9617f386a` | not a `current/` consumer (reads `themes/` dirs only) |
| `.config/omarchy/current/background` | n/a (link, inside current) | `/home/vgpnk/.config/omarchy/current/theme/backgrounds/0-ship-at-sea.jpg` | `55fa691adfd3fb8a9102b826a28d8de679938f04879799da499b8ace2fe039ac` | LIVE — swaybg reads the link name |

Of the 8 theme-related links, 5 consume `current/` (the five rows above, counting the
background link as a `current/` asset) and 3 do not: `omarchy_themes.lua`,
`omarchy_unlocks.lua`, `omarchy-recover-internal-monitor.service`.

nvim load path (bytes): `.config/nvim/init.lua:2` → `require("config.lazy")`;
`.config/nvim/lua/config/lazy.lua:22` `{ import = "plugins" }` → `lua/plugins/*.lua`, so
`theme.lua` is loaded and returns the `matteblack.nvim` + `colorscheme = "matteblack"`
spec from the theme file. [INFERENCE from config bytes; nvim not launched.]

### 2.3 Walker: path-convention consumer with one grep-visible row

Walker has no literal `omarchy/current` in `~/.config/walker/config.toml`; it names the
theme and an additional location:

- `.config/walker/config.toml:3` `theme = "omarchy-default"`
- `.config/walker/config.toml:4` `additional_theme_location = "~/.local/share/omarchy/default/walker/themes/"`

The import itself is row 20 (`default/walker/themes/omarchy-default/style.css:1`, sha
`481267af…`), which resolves seven `../` levels to `$HOME` and then
`current/theme/walker.css` (`realpath -m` verified). Whether walker expands `~` in
`additional_theme_location` is [UNK] (no runtime; see §7).

`btop` is the same shape: `btop.conf:5` `color_theme = "current"` (sha `4e17dd28…`) plus
the `themes/current.theme` link in §2.2.

## 3. Additional live consumers outside the assigned roots

Found by the full-`~/.config` sweep; not covered by the assigned directory list.

| consumer file (`~`) | line | imported path (verbatim) | sha256(consumer file) | state |
|---|---|---|---|---|
| `.config/foot/foot.ini` | 2 | `include=~/.config/omarchy/current/theme/foot.ini` | `3e88354476f2682e7a1a0bc840d04e221e5c6a7312b3ee9dcf76ec16d0842e60` | LIVE if foot is the terminal |
| `.config/ghostty/config` | 2 | `config-file = ?"~/.config/omarchy/current/theme/ghostty.conf"` | `cb828c044b07d4fd924fe1d6b55c956035feb16f8d5c67899c8a598994596667` | LIVE if ghostty is the terminal |
| `.config/kitty/kitty.conf` | 1 | `include ~/.config/omarchy/current/theme/kitty.conf` | `f875291ecfe64ebc4ddc588282bcdb20fb883769e9938148411efa378d7f1e70` | LIVE if kitty is the terminal |
| `.config/hyprland-preview-share-picker/config.yaml` | 4 | `stylesheets: ["../omarchy/current/theme/hyprland-preview-share-picker.css"]` | `cf88364e497e4af2adaff9a0b7ca12227d29f831bc7e18846dd8f03bf4c618a8` | LIVE on picker launch |

Dead duplicates of these also exist (all import the same theme paths, none is read by
its tool): `foot.ini.bak.20261003-190229` `8afc9646…`, `ghostty/config.bak.20261003-190229`
`e4763012…`, `kitty/kitty.conf.bak.20261003-190229` `95eed20a…`.

No other `omarchy/current` literal exists under `~/.config` after the symlink pass.
`~/.config/waybar/config.jsonc` does **not** import the theme (it only calls
`omarchy-*` helpers); its colors come through `style.css` row 5.

## 4. What is being imported (target identity today)

`current/theme.name` = `matte-black\n` (sha `48749715…`). `current/theme/` holds 25
entries — 24 regular files plus the `backgrounds/` directory; there are no per-file
links inside it.

| imported target | sha256 |
|---|---|
| `theme/hyprland.conf` | `79126bec8c28da306712148734a3ee58335a8bd48bf863e4e2e2db6d6d8344b6` |
| `theme/hyprlock.conf` | `3ef010e72b5f69113e1500bb083fb053f9f121212ad5ed4fe74ad8d12507ad0b` |
| `theme/alacritty.toml` | `8c3d1457c09d32e83367ac946ff6e85f6bda334c302587a043bef7dc7ac09139` |
| `theme/waybar.css` | `a1807a176659d7d6beaaf2a5c96cb7a03d131ee2740b8961d4c9aee393839c18` |
| `theme/swayosd.css` | `f88118e98b44cfa32ebc2d8f2394bd0448b2d1e0c01f01dd48677fe66ec7522b` |
| `theme/walker.css` | `f44cb45063494d2f4a8f489c47d8901b3bc98b27fbd1ca1c5a8801b40606bbc0` |
| `theme/mako.ini` | `95bf0c86c955cc813d1b60d18e738567c7f135885c5f02a6acfbbb38946e3bec` |
| `theme/btop.theme` | `e9ee6fb643852b378429fc382badef31180aac4cfdccf7201c6749d1999acda9` |
| `theme/gum.env.conf` | `ecab9ec497c555155536913c09e03e612f1e91296953ead8e9052da310f3435f` |
| `theme/neovim.lua` | `ec7df5fb1d3b7fc644fa0f69cd959ebc43fad8ebdb4aedfd01a5b1e387cd9778` |
| `theme/foot.ini` | `d9c2e20e079a9314ec4cfd87370436ee0f34759a76bcdb0d5e1128ce672dcbeb` |
| `theme/ghostty.conf` | `418636f99922f1ea64de37354fbb2708dd27c9d5f577ea63dd04d8d39b81203e` |
| `theme/kitty.conf` | `e8795b49ff5b6135f15243e73a45a9e970acfd09b2a30ae459fa6a163c0d4187` |
| `theme/hyprland-preview-share-picker.css` | `24474e34a4ed902250858eec8562838de33ce4a2782c5026ab764eb4cf6566c9` |
| `theme/colors.toml` | `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786` |
| `current/background` → `theme/backgrounds/0-ship-at-sea.jpg` | `55fa691adfd3fb8a9102b826a28d8de679938f04879799da499b8ace2fe039ac` |

`theme/btop.theme` is a **copy**, not a hardlink, of
`~/.local/share/omarchy/themes/matte-black/btop.theme` (same sha, different inode
`27317` vs `1542`, link count 1 both). The matte-black source dir itself contains only
`btop.theme`, `colors.toml`, `icons.theme`, `neovim.lua`, `vscode.json`, the preview PNGs
and `backgrounds/`; everything else in `current/theme` is generated (see §5.2).

`theme/light.mode` does **not** exist for matte-black, so the pi extension in rows 18–19
would resolve `"dark"` — moot until it is deployed.

## 5. Resolution and contract facts

### 5.1 Imports resolve

`realpath -m` on every relative import target:

- `.config/waybar/style.css` `../omarchy/current/theme/waybar.css` →
  `~/.config/omarchy/current/theme/waybar.css` (EXISTS)
- `.config/swayosd/style.css` same shape → `…/swayosd.css` (EXISTS)
- `.config/hyprland-preview-share-picker/config.yaml` `../omarchy/…` (EXISTS)
- default walker theme `../../../../../../../.config/…/walker.css` (7 levels) →
  `~/.config/omarchy/current/theme/walker.css` (EXISTS)

`current` is a **real directory**, not a link to `themes/<name>`:
`stat` → `directory`, inode `21283`, link count 1; `theme/` inode `27311`.
`~/.config/omarchy/themes/` (user themes) is empty; `~/.local/share/omarchy/themes/`
holds the 19 shipped themes.

### 5.2 Every import is rewritten by a theme switch (producer boundary)

`~/.local/share/omarchy/bin/omarchy-theme-set` (bytes read; not executed):

- `:12` `CURRENT_THEME_PATH="$HOME/.config/omarchy/current/theme"`, `:13` `next-theme`
- `:25–30` build `next-theme` as a copy: official theme dir first, user theme overlay on top
- `:38` `omarchy-theme-set-templates` renders `$OMARCHY_PATH/default/themed/*.tpl` with
  `colors.toml` into `next-theme`; an existing file from the theme dir is **not**
  overwritten, and `~/.config/omarchy/themed/*.tpl` overrides built-ins
  (`omarchy-theme-set-templates:38–44`)
- `:41–42` `rm -rf "$CURRENT_THEME_PATH"` then `mv "$NEXT_THEME_PATH" "$CURRENT_THEME_PATH"`
  — a non-atomic window in which `current/theme` is absent; every LIVE consumer above
  that starts or reloads inside that window fails to resolve its import
- `:45` writes `current/theme.name`; `:48–50` `omarchy-theme-bg-next` (which does
  `ln -nsf` at `omarchy-theme-bg-next:46`) repoints `current/background`
- `:53–63` restarts `waybar`, `swayosd`, `terminal`, `hyprctl`, `btop`, `opencode`,
  `mako`, `helix`. Of these, waybar/swayosd/terminal/hyprctl/btop/mako are consumers
  found above; walker, nvim, elephant, the picker and terminals that are not running are
  not restarted and pick the new theme up only at next launch.

So `current/theme` = (theme-dir copy ∪ rendered templates): a theme switch changes the
bytes behind **all 20** import rows at once.

### 5.3 Variable-name contract per consumer (observed)

| consumer | expects from imported file | imported file defines |
|---|---|---|
| hyprland | `$activeBorderColor` (used in `col.active_border`) | `$activeBorderColor` |
| hyprlock | `$color,$inner_color,$outer_color,$font_color,$check_color` + background image | all five + path via `current/background` |
| waybar | `@background,@foreground` | both |
| swayosd | `@background-color,@border-color,@label,@image,@progress` | all five |
| walker | `@selected-text,@text,@base,@border,@background` (plus `@foreground`) | all six |
| mako | `text-color,border-color,background-color` + `include …/default/mako/core.ini` | all three (core.ini has no `omarchy/current` refs; chain terminates) |
| alacritty / foot / ghostty / kitty | full `[colors.*]` / palette | present |
| btop | whole `.theme` file | 2648 B palette |
| gum | `env = …` variables | present |

Shadowing check: `~/.config/hypr/looknfeel.conf` is sourced **after** the theme
(`hyprland.conf:19`) but does not set an active `col.active_border` (only commented
lines 5/8), so the theme's border stays effective. `waybar/style.css` uses the theme for
base colors but keeps a hardcoded `#a55555` accent in 3 rules (screenrecord/idle/
notification indicators), which does not track a theme switch.

## 6. Checkout/version fact (file bytes + pinned raw receipts)

- `.git/HEAD` = `ref: refs/heads/master`; `.git/packed-refs:2` =
  `8fcc9d6048af4cb0e3af8512c78049857a3b53dd refs/heads/master`;
  `packed-refs:507` v3.8.3 = `6aa2aec1c035d50cfb6871d490cdf9a1169f5ac3`,
  `:508` v3.8.4 = `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`.
- `git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4 'refs/tags/v3.8.4^{}'`
  → `8fcc9d6048af4cb0e3af8512c78049857a3b53dd` only (lightweight tag, no peeled line).
  Remote URL from `.git/config:7` = `https://github.com/basecamp/omarchy.git`.
- Host `version` file = `3.8.3\n` (6 B, sha `0a5c29521592a324aa0381ac743c15dc552747cd89c5f5c9715e547df40258c6`,
  mtime `2026-10-03 17:42:36`).
- Upstream `version` at **both** v3.8.3 and v3.8.4 = the same 6 bytes / same sha
  (§9). So `version` = 3.8.3 at tag v3.8.4 is an **upstream unbumped file**, not a local
  edit. Host checkout is tag v3.8.4 (`8fcc9d60…`) with `version` reading 3.8.3.
  `.git/index` mtime `2026-10-14 11:42:09` is recorded only as an observation.

## 7. Unexercised behaviour / [UNK]

- **hyprlock** rows 3–4: `hypridle.conf:11` runs
  `pidof hyprlock || omarchy-launch-screensaver`, and `omarchy-launch-screensaver` is the
  TTE terminal screensaver (Alacritty/Ghostty/Foot/Kitty), not hyprlock. No config-byte
  launcher for hyprlock exists (no bind, no unit), so whether hyprlock ever runs — and
  therefore whether rows 3–4 are exercised — is [UNK].
- **pi extension** rows 18–19: `~/.config/pi` and `~/.local/share/pi` do not exist; the
  extension lives only in the omarchy default tree. Loaded-by-pi is [UNK]; target
  `light.mode` is absent for matte-black.
- **elephant background selector** rows 14–15: `elephant.service` is enabled
  (`graphical-session.target.wants/elephant.service` symlink), but
  `~/.config/walker/config.toml` lists only `desktopapplications`/`websearch` providers,
  so provider registration/visibility inside walker is [UNK].
- **`~` expansion**: walker `additional_theme_location` carries a literal `~`; swayosd
  `config.toml` `style = "~/.config/swayosd/style.css"` likewise. Whether either binary
  expands it is [UNK] — no runtime allowed this round.
- Process-level state (running waybar/mako/swaybg/swayosd, enabled-vs-active units) is
  [INFERENCE] from autostart exec lines and `.wants` symlinks; `systemctl` was not run
  (host pause).
- All consumers above are observed only as file bytes; no theme switch, no app restart,
  no screenshot.

## 8. Confidence

- **Observed**: every grep line, line number, sha256, link target, `stat` type/inode,
  `realpath` result, script line cited, packed-refs line, raw fetch bytes.
- **Inference**: LIVE/DEAD/CONDITIONAL column (from `hyprland.conf` source order,
  `default/hypr/autostart.conf` exec-once list, `.wants` symlinks), nvim lazy import,
  §5.2 reload set.
- **Unresolved**: the four items in §7.

## 9. Receipts (raw fetches)

Written to `.ufo/waves/round-18/fetch/HostThemeConsumers/` (bodies + `receipts.jsonl`):

| url | status | bytes | sha256 |
|---|---|---|---|
| `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/version` | 200 | 6 | `0a5c29521592a324aa0381ac743c15dc552747cd89c5f5c9715e547df40258c6` |
| `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.3/version` | 200 | 6 | `0a5c29521592a324aa0381ac743c15dc552747cd89c5f5c9715e547df40258c6` |

Both bodies are `3.8.3\n` (anchor: byte 0). Tool: `curl 8.23.0`. No other web source
opened. No tool installs or upgrades were performed.
