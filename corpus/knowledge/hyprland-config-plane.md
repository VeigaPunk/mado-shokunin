# Hyprland config plane — measured inventory (MADO-1)

Probe window: 2026-10-14 12:52–13:05 UTC (host offset −03:00). Host user: `vgpnk`.
Substrate `~/.config/hypr/` read-only; nothing outside this repo was written.
Method: `wc`, `stat`, `sha256sum`, `grep` on files; runtime cross-checks via
`hyprctl` (v0.56.2), `ps`, `systemctl --user`.

Tags: `[OBS]` measured directly · `[INF]` inference from measured parts · `[UNK]` unknown.

## 1. Summary

`[OBS]` `~/.config/hypr/` = 13 files: 12 active `*.conf` (10,386 B) + 1 dead backup
(65 B); combined `wc -c` total 10,451 B. The root `hyprland.conf` (29 lines, 1,273 B)
is a pure orchestrator: 17 `source` statements (9 Omarchy defaults, 1 theme include,
5 local overrides, 1 toggle glob, 1 ai-usage) and no direct settings of its own.

## 2. Local file table `[OBS]`

| File | Bytes | Lines | mtime (host) | sha256 (first 12) |
|---|---|---|---|---|
| hyprland.conf | 1273 | 29 | 2026-10-06 16:21 | `4f52854a3c14` |
| bindings.conf | 2879 | 40 | 2026-10-03 17:44 | `e574a1ed0853` |
| input.conf | 1584 | 54 | 2026-10-03 17:44 | `3769c92ab766` |
| monitors.conf | 1012 | 29 | 2026-10-03 19:02 | `69c9d8996dfd` |
| looknfeel.conf | 1000 | 40 | 2026-10-03 17:44 | `777a4fdc8b61` |
| hypridle.conf | 765 | 19 | 2026-10-03 17:44 | `e7d3b8dd9835` |
| hyprlock.conf | 742 | 43 | 2026-10-03 17:44 | `b8d173dcff55` |
| hyprsunset.conf | 363 | 14 | 2026-10-03 17:44 | `3042e4a92303` |
| ai-usage.conf | 319 | 5 | 2026-10-06 16:21 | `21e76af98ce7` |
| autostart.conf | 210 | 5 | 2026-10-13 22:48 | `5ace17016fe2` |
| envs.conf | 133 | 5 | 2026-10-03 17:45 | `04af5cdf028b` |
| xdph.conf | 106 | 4 | 2026-10-03 17:44 | `2fded88a27b8` |
| autostart.conf.bak.1791942509 | 65 | 2 | 2026-10-13 22:48:29.476 | `8b472371e78b` |

Full hashes: `sha256sum ~/.config/hypr/*.conf ~/.config/hypr/*.bak.*`
(e.g. hyprland.conf = `4f52854a3c143dcf58430a679e339619223d2b5008115a322d06b2de637ea462`).

## 3. Root include graph — `hyprland.conf` line anchors `[OBS]`

```
L1   comment: wiki link
L4   source default autostart.conf
L5   source default bindings/media.conf
L6   source default bindings/clipboard.conf
L7   source default bindings/tiling-v2.conf
L8   source default bindings/utilities.conf
L9   source default envs.conf
L10  source default looknfeel.conf
L11  source default input.conf
L12  source default windows.conf
L13  source ~/.config/omarchy/current/theme/hyprland.conf
L16-20  local monitors / input / bindings / looknfeel / autostart
L23  source glob ~/.local/state/omarchy/toggles/hypr/*.conf
L26  commented windowrule example
L29  source local ai-usage.conf
```

`[OBS]` Precedence is by include order: local files (L16–20) come after defaults
(L4–12) and after the theme (L13); the toggle glob (L23) and ai-usage (L29) come last.
Measured proof in §7: the enabled toggle `window-no-gaps.conf` overrides the default
looknfeel values despite being read later.

`[OBS]` The whole default tree is 33,830 B across 35 files under
`~/.local/share/omarchy/default/hypr/` (every file has a mirrored consumer except
the orphans noted in §6/§9).

## 4. Keybinds `[OBS]`

Counts per sourced file (`grep -c '^bind'`; `bindd`/`bindeld` are described binds):

| Source | bind lines |
|---|---|
| default bindings/media.conf | 23 (of which 14 `bindeld`) |
| default bindings/clipboard.conf | 4 |
| default bindings/tiling-v2.conf | 90 |
| default bindings/utilities.conf | 50 |
| local bindings.conf | 25 |
| **sum** | **192** |

`[OBS]` `hyprctl binds -j | len()` = **192** — the arithmetic closes exactly; every
effective bind is accounted for by these five files.

Local `bindings.conf` (40 lines): 25 active `bindd` at L2–16 ("Application bindings",
e.g. L2 `SUPER, RETURN → xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"`) and
L19–28 (webapp launchers, e.g. L19 ChatGPT, L20 Grok, L28 X compose). Nothing is
unbound: the only `unbind` occurrence is the commented L34. L30–39 are commented
extras (Logitech MX Keys notes at L37–39).

`[OBS]` Deprecated/unsourced binding files:
- `default/hypr/bindings.conf` L1 self-labels "Deprecated bindings file"; root does
  not source it and it still points to the old `tiling.conf` (L14–16).
- `default/hypr/bindings/tiling.conf` (3,845 B, 50 binds) is referenced only by that
  deprecated file.
- `default/hypr/plain-bindings.conf` (923 B) — no `source` anywhere in
  `~/.config/hypr`, `default/hypr/`, or `~/.local/state/omarchy/toggles` references it.

## 5. Window rules `[OBS]`

Local rules (5 active total, all `match:` v2 syntax):
- `input.conf:45` `windowrule = match:class (Alacritty|kitty|foot), scroll_touchpad 1.5`
- `input.conf:46` `windowrule = match:class com.mitchellh.ghostty, scroll_touchpad 0.2`
- `ai-usage.conf:2–5` four rules for `^(org.omarchy.ai-usage)$`: `tag +floating-window`,
  `float on`, `center on`, `size 875 600`.
- `hyprland.conf:26` is a commented example only.

Default global rules — `default/hypr/windows.conf` (15 lines):
- L3 `suppress_event maximize, match:class .*` (the file's L2 notes "Hyprland 0.53+ syntax")
- L6 `tag +default-opacity, match:class .*`
- L9 XWayland no-focus fix (multi-matcher: class/title/xwayland/float/fullscreen/pin)
- L12 `source apps.conf`; L15 `opacity 0.97 0.9, match:tag default-opacity`

`default/hypr/apps.conf` (19 lines) sources 18 per-app files (L2–19:
1password, bitwarden, browser, hyprshot, jetbrains, localsend, pip, qemu, retroarch,
steam, geforce, moonlight, system, telegram, typora, terminals, walker,
webcam-overlay). `[OBS]` `apps/davinci-resolve.conf` (120 B) exists but is not
sourced by it — orphan.

## 6. Animations `[OBS]`

- Local `looknfeel.conf:25–28` has an `animations {}` block whose only content is
  commented (`# enabled = no`); so local settings contribute nothing.
- Effective set = `default/hypr/looknfeel.conf:81–106`: 5 beziers (L86–90:
  easeOutQuint, easeInOutCubic, linear, almostLinear, quick) and 15 `animation =`
  directives (L92–106, e.g. `windows … easeOutQuint`, `windowsIn … popin 87%`,
  `workspaces, 0, 0, ease`).
- `hyprctl getoption animations:enabled` → `int: 1` — animations are on.

## 7. Override chain and effective values `[OBS]`

Measured with `hyprctl getoption` in the live session:

| Option | Default source | Local/toggle | Effective (`getoption`) |
|---|---|---|---|
| general:gaps_in | default looknfeel:9 = 5 | toggle window-no-gaps = 0 | `custom type: 0 0 0 0` |
| general:gaps_out | default looknfeel:10 = 10 | toggle window-no-gaps = 0 | `custom type: 0 0 0 0` |
| general:border_size | default looknfeel:12 = 2 | toggle = 0 | `int: 0` |
| decoration:rounding | default looknfeel:29 = 0 | local comment only | `int: 0` |
| general:layout | default looknfeel:24 = dwindle | local comment (scrolling) inert | `str: dwindle` |
| input:kb_layout | default input:3 = us | local input:10 = br | `str: br` |

`[OBS]` Enabled toggle file `~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf`
(135 B, mtime 2026-10-03 17:53) contains `gaps_out=0 / gaps_in=0 / border_size=0` and
`rounding=0`; the session matches it. `[OBS]` `flags.conf` (141 B) in the same dir is
comment-only, and `default/hypr/toggles/single-window-aspect-ratio.conf` is not
mirrored into the enabled dir — aspect-ratio stays default.

`[INF]` Therefore the visible frame (no gaps, no rounding, dwindle, br keyboard,
animations on) is the composition of Omarchy defaults + one enabled toggle + local
`input.conf`, not of local `looknfeel.conf` (which is entirely comments).

## 8. Adjacent configs — separate consumers `[OBS]`

These four local files are **not** sourced by `hyprland.conf`; each has its own binary:

- `hypridle.conf` (19 lines): L1–6 general (lock_cmd `omarchy-system-lock` L2,
  inhibit_sleep=3 L5); L9–12 listener timeout 150 → screensaver; L15–19 listener
  timeout 152 → lock + wake. Binary hypridle 0.1.8-2; started by default
  autostart.conf:1.
- `hyprlock.conf` (43 lines): L1 sources the theme color file
  `~/.config/omarchy/current/theme/hyprlock.conf`; L14–16 `animations { enabled = false }`;
  L18–39 input-field (size 650×100, JetBrainsMono Nerd Font); L41–43 fingerprint auth
  disabled. Binary hyprlock 0.9.6-3, invoked via `omarchy-system-lock`.
- `hyprsunset.conf` (14 lines): L3–6 identity profile at 07:00 (tint neutralized);
  L8–14 comments document how to enable nightlight. Binary hyprsunset 0.4.0-3.
- `xdph.conf` (4 lines): `screencopy { allow_token_by_default = true;
  custom_picker_binary = hyprland-preview-share-picker }`; consumed by
  xdg-desktop-portal-hyprland 1.4.1-2 (`/usr/lib/xdg-desktop-portal-hyprland`, PID 1920
  running).

## 9. Version markers `[OBS]`

- `hyprctl version` → `Hyprland 0.56.2 built from branch v0.56.2 at commit
  efb50993780079460b0cbed1363e2166a2de1d9f`, ABI string
  `efb50993780079460b0cbed1363e2166a2de1d9f_aq_0.15_hu_0.14_hg_0.5_hc_0.1_hlg_0.6`;
  package `hyprland 0.56.2-2`.
- Omarchy: `/home/vgpnk/.local/share/omarchy/version` → `3.8.3`; git HEAD
  `8fcc9d60` "Merge branch 'master' into rc".
- `hyprctl configerrors` → empty (clean load).
- `default/hypr/windows.conf:2` pins the rule syntax era: "Hyprland 0.53+ syntax".

## 10. Runtime snapshot `[OBS]`

- `hyprctl monitors`: DP-1 (ID 0), `3440x1440@99.99700 at 0x0`, LG ULTRAWIDE
  508AZFMF7323, scale 1. Config declares `3440x1440@100` (`monitors.conf:10`).
  `env = GDK_SCALE,1` active (`monitors.conf:9`); all other monitor templates commented.
- `hyprctl activeworkspace`: id 1, 3 windows.
- `ps -eo pid,comm,args | grep hypridle|hyprlock|hyprsunset` → no match; and
  `systemctl --user is-active hypridle` → `inactive` (unit `/usr/lib/systemd/user/hypridle.service`
  exists). `[OBS]` hypridle is not running in this session although default
  `autostart.conf:1` `exec-once`s it. `[UNK]` cause (failed start, restart without
  exec-once replay, or manual stop) — unverified; do not conclude.
- Local autostart adds one process: `autostart.conf:5` grok-bot appimage; the path is a
  symlink to `/home/vgpnk/Applications/Grok_Bot_0.70.2.AppImage` (shape only, not read).

## 11. Errata (append-only — add blocks, never edit above)

- E1 (2026-10-14, MADO-1 seed): no corrections yet.

## 12. Open items `[UNK]`

1. Who/what writes `~/.local/state/omarchy/toggles/hypr/` (omarchy toggle tooling
   assumed, not traced).
2. Why hypridle is absent from the process tree (see §10).
3. Backup rotation policy for `autostart.conf.bak.1791942509`; `[INF]` suffix is epoch
   seconds (1791942509 = 2026-10-14T01:48:29Z = local 2026-10-13 22:48:29, matching its
   mtime and the rewrite of `autostart.conf`). Only one backup exists.
4. Whether `~/.config/omarchy/current/theme` is a symlink farm updated by a theme
   switcher or a copied tree — `ls -ld` shows a real directory; update mechanism untraced.
5. `default/hypr/bindings/tiling.conf` and `plain-bindings.conf` and
   `apps/davinci-resolve.conf` are unsourced; removal impact untested.

## 13. Spot-checks (reproducible)

1. `hyprctl getoption decoration:rounding` → `int: 0`; explains toggle override (§7).
2. Bind sum: `grep -c '^bind'` on media(23)+clipboard(4)+tiling-v2(90)+utilities(50)+local(25)
   = 192 = `hyprctl binds -j | length` (§4).
3. `sha256sum ~/.config/hypr/hyprland.conf` →
   `4f52854a3c143dcf58430a679e339619223d2b5008115a322d06b2de637ea462` (§2).