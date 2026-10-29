# Terminals & omarchy skill — measured inventory (MADO-3)

Measured 2026-10-14 on this host, read-only. Every claim below carries an
anchor: `path:line` or an inline command with its output. No oral knowledge.
The omarchy skill is treated as documentation surface per `PROVINCE.md:10-11`;
nothing was written outside this file.

## 1. What exists

All four terminal config trees exist; each has a `.bak.20261003-190229`
sibling from the same second. Evidence: `ls -la` of each directory,
2026-10-14.

| App | Config | Bytes | Lines | mtime | Backup |
|---|---|---|---|---|---|
| alacritty | `~/.config/alacritty/alacritty.toml` | 876 | 28 | 2026-10-03 19:02 | `alacritty.toml.bak.20261003-190229` (873 B) |
| foot | `~/.config/foot/foot.ini` | 516 | 25 | 2026-10-03 19:02 | `foot.ini.bak.20261003-190229` (513 B) |
| kitty | `~/.config/kitty/kitty.conf` | 954 | 34 | 2026-10-03 19:02 | `kitty.conf.bak.20261003-190229` (953 B) |
| ghostty | `~/.config/ghostty/config` | 1325 | 41 | 2026-10-03 19:02 | `config.bak.20261003-190229` (1322 B) |

Note the naming split: ghostty's file is `config` (no extension), the other
three use `.toml` / `.ini` / `.conf` respectively — matching the paths the
omarchy skill lists at `SKILL.md:166-169`.

## 2. Key settings per terminal

Line numbers are from the Read view of each file.

### alacritty.toml (28 lines)

- Imports the omarchy theme: `general.import = [ "~/.config/omarchy/current/theme/alacritty.toml" ]` — `alacritty.toml:1`
- `TERM = "xterm-256color"` under `[env]` — `alacritty.toml:3-4`
- OSC 52 clipboard enabled in `[terminal]` — `alacritty.toml:6-7`
- Font: `JetBrainsMono Nerd Font` regular/bold/italic, `size = 12.5` — `alacritty.toml:9-13`
- Window: `padding.x = 14`, `padding.y = 14`, `decorations = "None"` — `alacritty.toml:15-18`
- Keybindings — `alacritty.toml:20-27`:
  - `Shift+Insert` → Paste, `Ctrl+Insert` → Copy — `alacritty.toml:22-23`
  - `Shift+Return` sends CSI-u `\u001B[13;2u` (comment: TUIs can distinguish it) — `alacritty.toml:24-25`
  - `Alt|Shift+Return` sends CSI-u `\u001B[13;4u` (comment: legacy encoding collides with Alt+Return; tmux matches `M-S-Enter`) — `alacritty.toml:26-27`

### foot.ini (25 lines)

- Imports the theme: `include=~/.config/omarchy/current/theme/foot.ini` — `foot.ini:2`
- `term=xterm-256color` — `foot.ini:3`; `initial-window-mode=windowed` — `foot.ini:6`
- Font `JetBrainsMono Nerd Font:size=12.5` — `foot.ini:4`; `pad=14x14` — `foot.ini:5`
- `workers=0` — `foot.ini:7`
- Scrollback `lines=10000` — `foot.ini:9-10`
- Cursor `block`, `blink=no` — `foot.ini:12-14`
- Key bindings: `clipboard-copy=Control+Insert`, `primary-paste=none`, `clipboard-paste=Shift+Insert` — `foot.ini:16-19`
- Text bindings map `\x1b[13;2u=Shift+Return` and `\x1b[13;4u=Mod1+Shift+Return` — `foot.ini:21-25`

### kitty.conf (34 lines)

- Imports the theme: `include ~/.config/omarchy/current/theme/kitty.conf` — `kitty.conf:1`
- Font `JetBrainsMono Nerd Font`, `bold_italic_font auto`, `font_size 12.5` — `kitty.conf:4-6`
- Window: `window_padding_width 14`, `hide_window_decorations yes`, `confirm_os_window_close 0` — `kitty.conf:9-11`
- Keybindings: `ctrl+insert copy_to_clipboard`, `shift+insert paste_from_clipboard` — `kitty.conf:14-15`; `shift+enter` → `send_text all \e[13;2u` — `kitty.conf:17`; `alt+shift+enter` → `send_text all \e[13;4u` — `kitty.conf:19`
- `allow_remote_control yes` — `kitty.conf:22`
- Aesthetics: `cursor_shape block`, `cursor_blink_interval 0`, `shell_integration no-cursor`, `enable_audio_bell no` — `kitty.conf:25-28`
- Tab bar: bottom edge, `powerline` style, `slanted`, title template appends window count — `kitty.conf:31-34`

### ghostty/config (41 lines)

- Optional theme include: `config-file = ?"~/.config/omarchy/current/theme/ghostty.conf"` — `ghostty/config:2`
- Font family/style/size — `ghostty/config:5-7`
- Window: `window-theme = ghostty`, padding x/y = 14, `confirm-close-surface=false`, `resize-overlay = never`, `gtk-toolbar-style = flat` — `ghostty/config:10-15`
- Cursor `block`, `cursor-style-blink = false` — `ghostty/config:18-19`
- `shell-integration-features = no-cursor,ssh-env` with comment "all shell integration options must be passed together" — `ghostty/config:21-23`
- Keybinds: insert pair — `ghostty/config:26-27`; `shift+enter=csi:13;2u` — `ghostty/config:29`; `alt+shift+enter=csi:13;4u` — `ghostty/config:31`; four `resize_split` binds on `super+control+shift+alt+arrow_*` — `ghostty/config:32-35`
- `mouse-scroll-multiplier = 0.95` — `ghostty/config:38`
- `async-backend = epoll` with a cited Hyprland discussion link (general slowness fix) — `ghostty/config:40-41`

## 3. Cross-terminal invariants (measured)

- Same font family in all four: `alacritty.toml:10-12`, `foot.ini:4`, `kitty.conf:4`, `ghostty/config:5-6`.
- Same size `12.5` in all four: `alacritty.toml:13`, `foot.ini:4`, `kitty.conf:6`, `ghostty/config:7`.
- Padding 14 on both axes: `alacritty.toml:16-17`, `foot.ini:5`, `kitty.conf:9`, `ghostty/config:11-12`.
- Insert-key clipboard pair identically bound: `alacritty.toml:22-23`, `foot.ini:17/19`, `kitty.conf:14-15`, `ghostty/config:26-27`.
- Shift+Return and Alt+Shift+Return forced to CSI-u in all four, with near-verbatim comments: `alacritty.toml:24-27`, `foot.ini:22-25`, `kitty.conf:16-19`, `ghostty/config:28-31`.
- Block cursor with blink disabled (foot/kitty/ghostty): `foot.ini:13-14`, `kitty.conf:25-26`, `ghostty/config:18-19`. Alacritty sets no cursor style here — default not measured.
- Every file delegates colors to the omarchy theme include; none carries a hex color itself (verified by reading all four in full).

## 4. Theme plane — colors live outside the user configs

- Active theme name `matte-black`: `~/.config/omarchy/current/theme.name:1` (file 12 B).
- Theme directory `~/.config/omarchy/current/theme/` holds per-app color files: `alacritty.toml`, `foot.ini`, `kitty.conf`, `ghostty.conf` alongside `colors.toml`, `hyprland.conf`, `waybar.css`, `walker.css`, `mako.ini`, etc. (dir listing, 2026-10-14).
- Measured palette (same across all four theme files): background `#121212`, foreground `#bebebe`, cursor `#eaeaea`, selection `#515151`; normal colors e.g. color0 `#333333`, color1 `#D35F5F`, color4 `#e68e0d` — `theme/alacritty.toml:2-3`, `theme/foot.ini:2-3`, `theme/kitty.conf:1-2,9-10`, `theme/ghostty.conf:1-5,7-10`.
- Templating mechanism: `~/.config/omarchy/themed/alacritty.toml.tpl.sample` (86 lines) documents placeholder variables (`{{ background }}`, `{{ color0 }}`…`{{ color15 }}`, `_strip`/`_rgb` modifiers) and states user templates take priority over built-ins — `alacritty.toml.tpl.sample:1-37`.
- Inference: editing colors inside the four user configs would be theme-overwritten on the next `omarchy theme set`, since the color layer is the included theme file. The user configs are the non-color layer (font, padding, keybinds, cursor).

## 5. Install / serving state (who actually runs)

- Only Alacritty is on PATH: `command -v alacritty` → `/usr/bin/alacritty`; `command -v foot`, `kitty`, `ghostty` → no output (not found), 2026-10-14.
- Default terminal preference: `~/.config/xdg-terminals.list` (127 B, 2026-10-03) lists `Alacritty.desktop` as first choice; `/etc/xdg/xdg-terminals.list` does not exist (stat).
- Launcher path: `~/.config/hypr/bindings.conf:2` binds `SUPER, RETURN` to `uwsm-app -- xdg-terminal-exec`; `bindings.conf:3` binds `SUPER ALT, RETURN` to a tmux-attach variant.
- foot launcher entries are hidden stubs: `~/.local/share/applications/footclient.desktop` and `foot-server.desktop` are 28-byte files containing `[Desktop Entry]` + `Hidden=true` (cat, 2026-10-14).
- omarchy terminal management commands exist and were read (not executed): `omarchy commands --json` shows route `omarchy install terminal` ("Install one of the approved terminals and set it as the default") and `omarchy default terminal` ("Set the default terminal used by xdg-terminal-exec"); `omarchy restart --help` lists `omarchy restart terminal` — "Reload supported terminal emulators after config changes" (2026-10-14).
- Observation: config trees exist for all four terminals, but only Alacritty is installed and referenced. kitty/foot/ghostty configs are inert on this host until their packages are installed (`omarchy install terminal`).

## 6. Backup delta — what changed on 2026-10-03

`diff` of each `.bak.20261003-190229` against the live file reports exactly
one changed line per file: font size 9 → 12.5.

- `alacritty.toml:13` — `size = 9` → `size = 12.5`
- `foot.ini:4` — `size=9` → `size=12.5`
- `kitty.conf:6` — `font_size 9.0` → `font_size 12.5`
- `ghostty/config:7` — `font-size = 9` → `font-size = 12.5`

Inference: a single coordinated font-size bump across all four terminals on
2026-10-03 19:02; the backup suffix `20261003-190229` predates that change by
the seconds before it. No other difference exists between backup and live
file in any of the four.

## 7. omarchy skill anatomy

- Location: `~/.agents/skills/omarchy/` — a single file `SKILL.md`
  (14908 B, 392 lines, mtime 2026-10-03 17:42). No subdirectories, no
  assets (`find` + `ls -laR`, 2026-10-14).
- Frontmatter declares name `omarchy` and its domain — `SKILL.md:1-12`:
  - "REQUIRED for end-user customization of Linux desktop, window manager, or system config" — `SKILL.md:3-4`
  - Explicit config paths: hypr, waybar, walker, **alacritty, foot, kitty, ghostty**, mako, omarchy — `SKILL.md:5-7`
  - Triggers include "terminal config" — `SKILL.md:8`
  - Excludes "Omarchy source development in `~/.local/share/omarchy/` and `omarchy dev` workflows" — `SKILL.md:9-11`
- Body section map (line ranges from Read view):
  - "When This Skill MUST Be Used" — `SKILL.md:21-37`; terminals listed at `:27`; stop-rule at `:35`; dev exclusion restated at `:37`
  - "Critical Safety Rules" — `SKILL.md:39-69`; `~/.local/share/omarchy/` is READ-ONLY, "READING is safe and encouraged" — `:41-42`; read-safe uses incl. reading command source — `:58-62`; safe locations: `~/.config/`, custom themes, hooks — `:64-67`
  - "System Architecture" table (Arch/Hyprland/Waybar/Walker/terminals/Mako/SwayOSD) — `SKILL.md:71-83`; terminals row `:81`
  - "Command Discovery" — `SKILL.md:85-106`; prefer `omarchy <group> <action>`; `omarchy commands --json` — `:101-102`
  - Command groups table — `SKILL.md:108-124`
  - Hyprland config layout + behaviors — `SKILL.md:126-149`; auto-reload on save `:145`; validate with `hyprctl reload` + `hyprctl configerrors` `:147-148`
  - Waybar: does NOT auto-reload, must `omarchy restart waybar` — `SKILL.md:151-161` (`:159`)
  - Terminals block: the four config paths `:166-169`; command `omarchy restart terminal` `:172`
  - Other configs table (btop, fastfetch, lazygit, starship, git, walker) — `SKILL.md:174-183`
  - Patterns: edit user config + backup `:185-205`; new theme `:207-212`; hooks `:214-232`; refresh-to-defaults with confirmation `:234-247`
  - Common tasks: themes `:249-259`; keybindings incl. mandatory `unbind` before rebinding `:261-286`; monitors `:288-297`; window rules must re-fetch the Hyprland wiki, "syntax changes frequently" `:300-307`; fonts `:309-315`; system `:317-328` incl. always `omarchy debug --no-sudo --print` `:328`
  - Troubleshooting `:330-349`; decision framework `:351-360`; reminders `:362-371`; out of scope `:373-378`; example requests `:380-392`
- Claimed hook layout (`SKILL.md:219-223`) shows flat files `theme-set`,
  `font-set`, `post-update` directly under `~/.config/omarchy/hooks/`.
  Observed reality (`ls -la ~/.config/omarchy/hooks/`, 2026-10-14): no flat
  files; five `*.d` directories `battery-low.d`, `font-set.d`, `post-boot.d`,
  `post-update.d`, `theme-set.d`, each holding `.sample` scripts (enable by
  removing the suffix), plus one active `post-update.d/install-voxtype.hook`.
  Observation; inference: the skill's hook listing is illustrative/older than
  the shipped layout. The `.sample` activation convention is stated inside
  each sample's header comment, not in the skill body.
- Relationship to this lane: `PROVINCE.md:10-11` declares the omarchy skill a
  read-only documentation surface. Several skill rules bind mado work
  directly: restart discipline for terminals `SKILL.md:172,204`, keybinding
  `unbind` requirement `:272-284`, and the window-rules wiki re-fetch
  `:300-305`.

## 8. Observation / inference / unknown

**Observations** (all anchored above): four config trees exist; all delegate
colors to the `matte-black` theme include; identical font/size/padding/CSI-u
invariants; only Alacritty installed; `xdg-terminals.list` prefers Alacritty;
backup delta is font size 9 → 12.5; skill is a single 392-line SKILL.md whose
frontmatter explicitly covers these terminal paths.

**Inferences** (not independently proven): the 2026-10-03 edits were one
operator action bumping font size everywhere; the color layer would be
regenerated by theme changes, so color edits belong in a custom theme
(`~/.config/omarchy/themes/`, currently empty) or a user template under
`~/.config/omarchy/themed/`; kitty/foot/ghostty configs are inert here
because their packages are absent.

**Unknowns**: (1) whether `foot`/`kitty`/`ghostty` binaries exist outside
PATH (only PATH was probed); (2) whether `omarchy restart terminal` actually
restarts kitty/foot/ghostty when installed — its route/summary was read but
the command was not executed; (3) which terminal the operator actually uses
day-to-day (persistent evidence only shows Alacritty as the configured
default); (4) whether the `.bak.20261003-190229` backups were produced by
hand or by an omarchy tool; (5) alacritty cursor default (not set in its
config, default not measured); (6) exact behavior of `omarchy theme set`
regeneration for terminal color files (read from sample docs, not executed).

## Errata (append-only)

- (none yet)

## Errata (round 2) — appended 2026-10-14 (MADO-R2-3)

Append-only block; nothing above this line is edited. Number re-measure pass
by MADO-R2-3 (read-only probes staged at `/tmp/mado-r2-3-probe/`, ephemeral).
No corrections are due this pass; the re-measure record is kept so the block
exists and re-runs stay reproducible per the round-2 protocol.

- **R2-E1 (number-touching — round-1 note-length pin, re-measured).** The
  round-1 body (commit `65a2254`) is **179 lines by `wc -l`** (180 in editor
  view; no trailing newline — `tail -c 1` → `)`); this block extends it.
  Quotes must name the command (SKILL.md "Round 1 sources" quotes the editor
  count of the round-1 body).
- **R2-E2 (re-measure held — no correction).** §1 table: 876/28, 516/25,
  954/34, 1,325/41 B/L; backups 873/513/953/1,322 B. §4: `theme.name`
  12 B = `matte-black`; palette spot-checks — `#121212`/`#bebebe` in the
  four theme files, cursor `#eaeaea`, selection `#515151`, palette
  `0=#333333`, `1=#D35F5F`, `4`-family `#e68e0d` (theme `ghostty.conf:1-8`,
  `kitty.conf:1-10`, `alacritty.toml:2-3`). §5: `command -v` → only
  `/usr/bin/alacritty`; `xdg-terminals.list` 127 B, first entry
  `Alacritty.desktop`; `/etc/xdg/xdg-terminals.list` absent; both foot
  stubs 28 B. §6: backup-vs-live `diff` = one `NcN` hunk per file
  (`size = 9` → `size = 12.5`; e.g. `alacritty.toml` `13c13`). §7: omarchy
  skill 392 L / 14,908 B; hooks dir = five `*.d` directories plus active
  `post-update.d/install-voxtype.hook`.