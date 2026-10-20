# Remaining planes — live-surface census (round 6, lane M6-3)

Watch arm 2 (coverage) of `plans/round-6.plan.md` (c): the PROVINCE surfaces
that had no plane note before this round — **themes/wallpapers as declared
files** and **display/session shape** — censused as shapes (paths, sizes,
modes, symlink targets, process identities, read-only queries). Census-style:
rows are measurements; **no verdict token is issued here** (CLEAN|DIVERGED is
the gate's vocabulary). The declared-vs-live arms that would ride
`tools/mado-verify.sh` are gated on the round-6 mutation proof (a) per the
plan's ordering; at probe time no mutation-proof artifact exists in
`corpus/knowledge/` (checked: `ls …/corpus/knowledge | grep -iE
'mutation|drift|watch'` → none), so this note adds no gate rows.

Probe window: 2026-10-14 17:39:02Z–17:41:45Z (host offset −03:00, local
14:39–14:41). Host user `vgpnk`. Read verbs only: `ls/stat/find/readlink/
sha256sum/wc/du/head/grep` on files, `pgrep/ps/loginctl/systemctl --user
list-*/busctl --user list`, `hyprctl` read verbs (`version`, `configerrors`,
`instances`, `layers`, `clients`, `monitors`), `makoctl mode`, `pacman -Q`.
No `hyprctl dispatch/keyword/notify`; hypridle/hyprlock/hyprsunset were never
started or stopped; no theme command (`omarchy theme …`) was executed; no
idle interval was waited out. Nothing written outside this file and scratch
`/tmp/w6-mado-m6-3/` (`theme-tree.log`, `consumers-session.log`,
`hyprctl.log`, `theme-pins.log`, `chain-decl.log`, `display-session.log`,
`walker-chain.log`, `provenance.log`, `details.log`, `final-details.log`,
`last.log`). Secrets shape-only: no secret-shaped file content read; window
titles not read (clients reduced to pid/class/tags/workspace). Scratch is
ephemeral — the measurements below are the durable record.

Tags: `[OBS]` measured · `[INF]` inference from measured parts · `[UNK]`
unknown. Times UTC unless marked local.

## §0 Coverage ledger — what was already plane-noted, what this adds

| PROVINCE surface (`PROVINCE.md:6-10`) | Existing plane note(s) | This census adds |
|---|---|---|
| `~/.config/hypr/` (conf/keybinds/rules) | `hyprland-config-plane.md`, `keybind-rule-semantics.md`, `hyprctl-verification-layer.md` | source-order re-measure only (§2) |
| `~/.config/waybar/` | `waybar-walker-plane.md`, `waybar-walker-semantics.md` | live layer + css import row (§2, §4) |
| `~/.config/walker/` | `walker-deep.md` | walker theme-css import chain (§2) |
| terminal configs (`alacritty|foot|kitty|ghostty`) | `terminals-and-omarchy.md` | runtime rows: live Alacritty processes (§3) |
| themes/wallpapers as declared files | partial only (`terminals-and-omarchy.md` §4 colors; `idle-lock-plane.md` §2 background shape) | full declared-file census + consumers (§1, §2) |
| screen/idle behavior | `idle-lock-plane.md` | display/session shape (§4); idle transitions stay UNKNOWN (MADO-R4-2) |
| omarchy skill (docs surface) | `terminals-and-omarchy.md` §7 | — |
| "display behavior on this host" (domain line, `PROVINCE.md:1-4`) | monitors in r2 notes (`hyprland-config-plane.md` §…); hyprsunset/portal rows in `hyprland-config-plane.md` §8 | session/portal/OSD/shape census (§4) |

Gate relation `[OBS]`: `tools/mado-verify.sh` v1 declares "hypr core, waybar,
walker, terminals" as its file planes (`tools/mado-verify.sh:5`, invariant
block `:32-54`); the theme appears only as a record-level NOTE
(`live.theme.current`, `:1014-1020`); idle/lock transitions are explicitly
not verified (`:56-58`). Nothing in this note changes the gate; wiring these
rows in is the (a)-gated extension per the plan.

## §1 Theme plane as declared files — census `[OBS]`

### 1.1 `~/.config/omarchy/` root (all real dirs, mode 755, mtime 2026-10-03)

| Entry | Shape | Notable contents |
|---|---|---|
| `current/` | dir | `background` symlink, `theme/` dir, `theme.name` (12 B) |
| `themes/` | dir | **empty** (0 entries) — no user themes |
| `themed/` | dir | `alacritty.toml.tpl.sample` 2,729 B (1 entry) |
| `branding/` | dir | `about.txt` 2,734 B; `screensaver.txt` 1,525 B |
| `extensions/` | dir | `menu.sh` 656 B |
| `hooks/` | dir | five `*.d` dirs + active hook (already censused, `terminals-and-omarchy.md` §7) |

### 1.2 `current/` wiring

- `theme.name` 12 B → content `matte-black`; sha256
  `48749715228bfa375bd84bef15ea0ad85b2ef88445607e8e6277bed103955c3b`.
- `theme/` is a **real directory** (not a symlink; `readlink -f` returns its
  own path) — same as `idle-lock-plane.md` §2 observed.
- `background` is a symlink (71 B link, absolute target):
  `…/current/theme/backgrounds/0-ship-at-sea.jpg` — the wallpaper is declared
  as a link into the theme tree, not as a copy.

### 1.3 `current/theme/` file census — 24 files (515,974 B) + `backgrounds/`

`du -sb` of the whole theme dir: 3,718,129 B (files + backgrounds, arithmetic
checks: 515,974 + 1,681,677 + 1,033,920 + 482,067 + 4,491 = 3,718,129).

| File | B | File | B |
|---|---|---|---|
| `alacritty.toml` | 772 | `mako.ini` | 119 |
| `btop.theme` | 2,648 | `neovim.lua` | 150 |
| `chromium.theme` | 9 | `obsidian.css` | 2,523 |
| `colors.toml` | 461 | `preview.png` | 470,315 |
| `foot.ini` | 378 | `preview-unlock.png` | 22,524 |
| `ghostty.conf` | 454 | `swayosd.css` | 166 |
| `gum.env.conf` | 5,413 | `unlock.png` | 2,512 |
| `helix.toml` | 4,582 | `vscode.json` | 65 |
| `hyprland.conf` | 143 | `walker.css` | 191 |
| `hyprland-preview-share-picker.css` | 1,844 | `waybar.css` | 68 |
| `hyprlock.conf` | 176 | `icons.theme` | 9 |
| `keyboard.rgb` | 8 | `kitty.conf` | 444 |

All mode 644, mtime 2026-10-03 17:49 (theme-set time; payload mtimes are
17:42 — see 1.5).

Pins taken this pass (full sha256): `alacritty.toml`
`8c3d1457c09d32e8…`; `hyprland.conf` `79126bec8c28da30…`; `mako.ini`
`95bf0c86c955cc81…`; `waybar.css` `a1807a176659d7d6…`; `walker.css`
`f44cb45063494d2f…`; `hyprlock.conf` `3ef010e72b5f6911…`; `swayosd.css`
`f88118e98b44cfa3…`; `colors.toml` `dbdd13a629aac86d…`. Two cross-checks
land: `hyprlock.conf` equals `idle-lock-plane.md` §2's pin, and `mako.ini`
equals the R3-1 pin recorded for `~/.config/mako/config` — the "50 B mako
config" cell R3-2 resolved is confirmed as the symlink's own size (the link
target's bytes are these).

### 1.4 `backgrounds/` (4 files)

| File | B | sha256 |
|---|---|---|
| `0-ship-at-sea.jpg` (the active one) | 1,681,677 | `55fa691adfd3fb8a…` |
| `1-dark-waters.jpg` | 1,033,920 | — |
| `2-dot-hands.jpg` | 482,067 | — |
| `omarchy.png` | 4,491 | — |

The active wallpaper is a JPEG declared by the `current/background` symlink
(1.2); size matches the r2-era figure (1,681,677 B) — the file itself is
unchanged, now also sha-pinned.

### 1.5 Provenance — payload vs generated `[OBS]` + `[INF]`

- Payload tree `~/.local/share/omarchy/themes/` holds **19** theme dirs
  (catppuccin, catppuccin-latte, ethereal, everforest, flexoki-light,
  gruvbox, hackerman, kanagawa, lumon, matte-black, miasma, nord,
  osaka-jade, retro-82, ristretto, rose-pine, tokyo-night, vantablack,
  white).
- Payload `themes/matte-black/` contains only: `backgrounds/`,
  `btop.theme`, `colors.toml`, `icons.theme`, `neovim.lua`, `preview.png`,
  `preview-unlock.png`, `unlock.png`, `vscode.json` — **none of the per-app
  runtime files** (`alacritty.toml`, `hyprland.conf`, `mako.ini`,
  `waybar.css`, `walker.css`, `hyprlock.conf`, …) exist in the payload.
- `[OBS]` Two payload files were verified byte-equal to the live theme:
  `colors.toml` (`dbdd13a6…` both sides) and the active wallpaper
  (`55fa691a…` both sides); payload mtimes 17:42 precede the current/theme
  mtimes 17:49.
- `[OBS]` `~/.local/share/omarchy/default/themed/` holds **17 `*.tpl`
  templates** (alacritty.toml, btop.theme, chromium.theme, foot.ini,
  ghostty.conf, gum.env.conf, helix.toml, hyprland-preview-share-picker.css,
  hyprland.conf, hyprlock.conf, keyboard.rgb, kitty.conf, mako.ini,
  obsidian.css, swayosd.css, walker.css, waybar.css — `.tpl` each).
  `[INF]` The per-app files in `current/theme/` are rendered from these
  templates against the theme's `colors.toml` at theme-set time; the
  template/payload split explains why `current/theme/` has 24 files while
  the `matte-black` payload has 9 (+ backgrounds). Not proven by running
  `omarchy theme set` (would mutate operator-owned theme state).

### 1.6 State and toggles (supporting shape) `[OBS]`

- `~/.local/state/omarchy/` → `migrations/` (**330** zero-byte marker files)
  and `toggles/`; `toggles/hypr/` still exactly `flags.conf` (141 B) and
  `window-no-gaps.conf` (135 B) — same two files as the round-4 audit
  (`province-accuracy-selfaudit.md` §2), no new toggles, no
  `screensaver-off` flag (`idle-lock-plane.md` §8 read-back stands).

## §2 Consumption chains — declared file → live consumer `[OBS]`

| Surface | Declared chain (file anchors) | Live evidence (probe window) |
|---|---|---|
| wallpaper | `default/hypr/autostart.conf:5` `exec-once = uwsm-app -- swaybg -i ~/.config/omarchy/current/background -m fill`; symlink → theme JPEG (§1.2) | `swaybg` PID **1203358**, cmdline exactly the declared form, ppid Hyprland 1203316; layer ns `wallpaper` |
| notifications | `default/hypr/autostart.conf:2` `exec-once = uwsm-app -- mako`; `~/.config/mako/config` symlink (50 B, mode 777) → `~/.config/omarchy/current/theme/mako.ini` | `mako` PID **1203350**, layer ns `notifications`; `makoctl mode` → `default` |
| hypr core | `~/.config/hypr/hyprland.conf:13` `source = ~/.config/omarchy/current/theme/hyprland.conf` (before local overrides `:16-20`, toggles `:23`, plugin `:29`) | 17 source lines re-measured `:4-29`; `configerrors` empty rc=0; version 0.56.2 `efb5099…` |
| waybar | `~/.config/waybar/style.css:1` `@import "../omarchy/current/theme/waybar.css";` (style.css 1,887 B) | `waybar` PID **1203352**, layer ns `waybar` |
| walker (css) | `config.toml:3` `theme = "omarchy-default"` + `:4` `additional_theme_location = ~/.local/share/omarchy/default/walker/themes/`; `…/omarchy-default/style.css:1` `@import "../../../../../../../.config/omarchy/current/theme/walker.css";` (1,243 B css; `layout.xml` 6,488 B) | `walker --gapplication-service` PID 1203471 (parents/versions per `walker-deep.md`) |
| swayosd | `~/.config/swayosd/style.css:1` `@import "../omarchy/current/theme/swayosd.css";` (style.css 372 B; config.toml 87 B) | `swayosd-server` PID **1203475**; user unit `swayosd-server.service` loaded **active running** |
| alacritty | `~/.config/alacritty/alacritty.toml:1` `general.import = [ "~/.config/omarchy/current/theme/alacritty.toml" ]` (`terminals-and-omarchy.md` §1) | 3 live windows (§3) |
| hyprsunset | `~/.config/hypr/hyprsunset.conf` 363 B, sha `3042e4a9…` (= MADO-1/MADO-R2 pin); "identity profile at 07:00" (`hyprland-config-plane.md:163`) | binary `/usr/bin/hyprsunset` (0.4.0-3); unit `hyprsunset.service` **disabled**; no process; config pin equal |

`[OBS]` Consumer start scopes line up with the uwsm envelopes:
`app-Hyprland-swaybg-…scope`, `app-Hyprland-mako-…scope`,
`app-Hyprland-waybar-…scope`, `app-Hyprland-chromium-…scope`,
`app-Hyprland-fcitx5-…scope`, three
`app-Hyprland-xdg-terminal-exec-…scope`, one
`app-Hyprland-omarchy-hyprland-monitor-watch-…scope`; `hypridle.service` and
`hyprsunset.service` are `disabled`. `[OBS]` The user
`~/.config/hypr/autostart.conf` (210 B, mtime 2026-10-13 22:48, plus
`autostart.conf.bak.1791942509` 65 B) contributes exactly one local exec —
the Grok Bot appimage (out-of-province app; recorded before in
`province-accuracy-selfaudit.md` §2) — and a commented template line; it
does **not** re-declare wallpaper/notifications/idle: those come from
`default/hypr/autostart.conf` via `hyprland.conf:4`.

## §3 Terminals runtime census `[OBS]`

`[OBS]` Three live Alacritty windows, all `class = Alacritty`, all on
workspace 1, all tagged `default-opacity*` + `terminal*`
(`hyprctl -j clients`, reduced to pid/class/tags/ws; titles not read):

| PID | ppid | started (local) | cmdline |
|---|---|---|---|
| 1204373 | 1203316 (Hyprland) | 2026-10-14 13:11:23 | `alacritty --working-directory=/home/vgpnk` |
| 1205237 | 1203316 | 13:11:54 | `alacritty --working-directory=…/Projects/shokunin` |
| 2603289 | 1203316 | 14:32:33 | `alacritty --working-directory=/home/vgpnk` |

`[OBS]` Package `alacritty 0.17.0-1`; the other three terminal packages are
absent (`terminals-and-omarchy.md` §5 stands — configs inert). The theme
import chain is file-level (§2 table) and unchanged since
`terminals-and-omarchy.md`; `[UNK]` whether the three live processes render
today's theme bytes (would require process introspection or a restart — not
executed; the r2-era opacity-tag anomaly F2 is not re-adjudicated here).

## §4 Display & session shape `[OBS]`

- **Session.** `loginctl show-session 4` → `User=vgpnk`, `seat0`, `tty2`,
  `Service=sddm`, `Type=wayland`, `Class=user`, `Active=yes`,
  `State=active`; session 5 = `systemd-user` manager. Start chain:
  `sddm-helper` PID 1203167 (`--start uwsm start -g -1 -e -D Hyprland
  hyprland.desktop`) → `Hyprland --watchdog-fd 4` PID 1203316, both started
  13:11:06 local; `uwsm aux app-daemon` PID 1203477. Boot 2026-10-13 11:02
  (`who -b`) — session start, not reboot.
- **Wayland surface.** `hyprctl -j instances` → one entry,
  `wl_socket "wayland-1"`, `time` 1791994267 (= 16:11:07Z).
- **uwsm targets.** Active user targets include `graphical-session.target`,
  `graphical-session-pre.target`,
  `wayland-session@hyprland.desktop.target`,
  `wayland-session-envelope@hyprland.desktop.target`,
  `wayland-session-pre@…`, `wayland-session-xdg-autostart@…`.
- **Monitor.** DP-1 3,440×1,440, scale 1, refresh 99.997 Hz, `dpmsStatus`
  true, `disabled=false`, `focused=true` — r2's monitor coverage
  (`hyprland-config-plane.md`) re-measured at probe time.
- **Layer surfaces.** `wallpaper` (1203358) · `waybar` (1203352) ·
  `notifications` (1203350).
- **Clients.** 4 total — the 3 Alacritty (§3) + chromium 2552209
  (`chromium-based-browser*` + `default-opacity*`, ws 1; ppid = walker's
  elephant provider 1203474 per `province-accuracy-selfaudit.md` §6-era
  numbering).
- **Portals.** `busctl --user list` + `pgrep -af xdg-desktop-portal`:
  frontend `/usr/lib/xdg-desktop-portal` PID **1203504**; impls
  `-gtk` PID 1203545 and `-hyprland` PID **1203662** (the display-behavior
  consumer named in the plan); `PermissionStore` 1203521, `Documents`
  1203526, fcitx5 1203353 (Fcitx/IBus portals); `Secret`/`kwallet`
  activatable. Packages: `xdg-desktop-portal 1.22.1-2`,
  `xdg-desktop-portal-hyprland 1.4.1-2`, `-gtk 1.15.3-1`.
- **OSD / display daemons.** `swayosd-server` user unit active (§2);
  `omarchy-hyprland-monitor-watch` PID 1203378 plus its pipeline subshell
  1203555 (`socat -U - "UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$…/.socket2.sock"
  | while read …` — watches `monitorremoved*` events; the two PIDs are one
  script + its `while` subshell `[INF]`).
- **Night-light.** hyprsunset: no process, unit disabled, config byte-pin
  equal (§2) — "absent / identity profile" as the plan expected.
- **Idle.** hypridle absent as a process again (F1-class; `idle-lock-plane.md`
  E2 and this probe agree); no lock/screensaver surfaces; live idle
  transitions remain out of scope (MADO-R4-2) and are **not** widened here.
- **Packages (shape).** hyprland 0.56.2-2 · hypridle 0.1.8-2 · hyprlock
  0.9.6-3 · hyprsunset 0.4.0-3 · swaybg 1.2.2-1 · mako 1.11.0-1 · waybar
  0.15.0-3 · walker 2.17.0-1 · alacritty 0.17.0-1 · uwsm 0.26.7-1 · sddm
  0.21.0-7.

## §5 Observation / inference / unknown

**Observations** — all anchored above: theme tree = 24 generated files +
4-file background set under `current/theme/`; `theme.name` = `matte-black`;
the wallpaper is a symlink consumed by a live `swaybg`; mako's config is a
symlink into the theme and its process carries the `notifications` layer;
waybar/walker/swayosd stylesheets all `@import` the current theme; the
session is SDDM→uwsm→Hyprland on `wayland-1` with portal backends
(hyprland+gtk) live; 3 Alacritty windows; hyprsunset/hypridle/hyprlock
absent as processes with their file pins stable.

**Inferences** — per-app theme files are rendered from the 17 `default/
themed/*.tpl` templates at theme-set time (payload lacks them; `colors.toml`
and the active wallpaper are the byte-equal payload parts); the two
monitor-watch PIDs are one socat pipeline; consumer scopes come from the
uwsm app-daemon (`uwsm-app` in `default/hypr/autostart.conf`).

**Unknowns** `[UNK]`

1. Whether `omarchy theme set` regenerates the 24 `current/theme/` files
   from the 17 templates — read from structure only; executing it would
   mutate operator-owned theme state.
2. How `swaybg` is asked to reload on theme change (no wallpaper unit/scope
   beyond the transient one; no `theme-set` hook observed) — reload path
   unmeasured.
3. Whether the live Alacritty/waybar/walker/swayosd processes render
   today's theme bytes (no introspection/restart performed; screenshots not
   taken).
4. Start route of `swayosd-server.service` (unit active; which enablement or
   trigger started it — no autostart `.desktop` found in
   `~/.config/autostart` / `/etc/xdg/autostart`).
5. Whether the monitor-watch `recover` handlers have executed in this
   session (no monitor events observed; only the listener shape is
   measured).
6. Whether hyprsunset was ever started this session (no trace; unit
   disabled; identity-profile config unchanged).
7. Cause of Alacritty PID 2603289 appearing mid-session (14:32:33 local) —
   operator action presumed, not recorded.
8. Gate wiring: no declared-vs-live rows for these surfaces exist in gate v1
   (`tools/mado-verify.sh:5, :56-58, :1014-1020`); the round-6 arm that would
   ride them is gated on the mutation proof (a), not yet evidenced in
   `corpus/knowledge/` at probe time.
9. Live idle transitions (MADO-R4-2 constraint) — unchanged, still UNKNOWN.

Era caveat: all PIDs/timers are point samples of the probe window; sibling
round-6 lanes may write repo files concurrently (not inspected).

## §6 Spot-checks (reproducible, read-only)

1. **Wallpaper chain** — `readlink ~/.config/omarchy/current/background` →
   `…/current/theme/backgrounds/0-ship-at-sea.jpg`;
   `sha256sum` that file →
   `55fa691adfd3fb8a9102b826a28d8de679938f04879799da499b8ace2fe039ac`
   (= payload copy); `pgrep -ax swaybg` → PID 1203358 with
   `-i /home/vgpnk/.config/omarchy/current/background -m fill`;
   `hyprctl -j layers` → `wallpaper` ns with that pid.
2. **mako symlink + pin** — `stat -c '%N' ~/.config/mako/config` → symlink →
   `~/.config/omarchy/current/theme/mako.ini`; `sha256sum` target →
   `95bf0c86c955cc81…` (= R3-1 mako pin); `pgrep -ax mako` → 1203350;
   `makoctl mode` → `default`.
3. **Session + portals** — `loginctl show-session 4 -p Type -p Service
   -p Active -p State` → `wayland/sddm/yes/active`;
   `pgrep -af 'xdg-desktop-portal'` → 1203504 (frontend), 1203545 (gtk),
   1203662 (hyprland); `hyprctl -j instances | jq -c '.[0].wl_socket'` →
   `"wayland-1"`.
4. **Theme pins** — `sha256sum ~/.config/omarchy/current/theme/{theme.name…}`
   as §1.3; `hyprlock.conf` equals `idle-lock-plane.md` §2 pin; `hyprsunset`
   still `3042e4a9…` with no process.

## §7 Errata (append-only — add blocks, never edit above)

- E1 (2026-10-14, M6-3 seed): new note; no corrections recorded yet.
  Cross-plane checks applied: `idle-lock-plane.md` §2 pins (hyprlock/
  hyprsunset/theme background) reproduced; `terminals-and-omarchy.md` §1-§5
  config pins and only-Alacritty state reproduced; R3-1's mako pin resolved
  through the symlink as that note's R3-2 follow-up expected. No
  contradiction found to correct.
- E2 (2026-10-14, M6-3, post-write spot-check re-run ~17:43Z): **mako's
  `notifications` layer surface is not permanently mapped** — at 17:39:32Z
  `hyprctl -j layers` listed `notifications` (pid 1203350); in the re-run
  the same query returns only `wallpaper` (1203358) and `waybar` (1203352)
  while the mako process (1203350, `pgrep -ax`) is unchanged. `[OBS]` two
  point samples; §2/§4's layer rows are probe-window statements, not a
  steady-state claim. Cause (surface unmapped while no notification is
  visible vs. a transient first sample) `[UNK]` — no notification was sent
  to test either way (would mutate the session).

## Freshness pointer (round 19, 2026-10-20)

- The walker version pin in this note (line 246, `walker 2.17.0-1`) is dated 2026-10-14 (probe window 17:39-17:41Z) and describes walker 2.17.0; on 2026-10-20 the host package moved to 2.17.2 per `/var/log/pacman.log:2929` (S090); the binary-bytes row S096 is reserved and not yet recorded. Current routing: corpus/knowledge/walker-route-r18.md.
- Version-bound, dated: line 246 only (walker 2.17.0-1 in the package-shape list). The other package versions on that line (hyprland, hypridle, hyprlock, hyprsunset, swaybg, mako, waybar, alacritty, uwsm, sddm) are 2026-10-14 pins and were not re-measured this round.
- Walker process and CSS import rows (§2 walker row, §4 clients): PID 1203471 and the `walker --gapplication-service` sample are 2026-10-14 point samples; the 2026-10-20 upgrade logged walker-restart.hook entries (S090 lines 3062, 3123), so no live walker process fact is re-asserted. The config.toml and style.css lines cited there are file-level bytes read on 2026-10-14, not checked against 2.17.2 behaviour.
- Version-independent (file bytes and host state, not the walker binary): theme-tree census and sha256 pins (§1), symlink targets (§1.2, §2 wallpaper and mako rows), hyprsunset and hyprlock pins (§2, §4), session/portal/monitor shape (§4), spot-checks (§6). These remain 2026-10-14 point samples dated by the probe window; none depends on the walker version.
- Not in this note: walker help text, walker binary sha, config line counts, `walker --version` output. No value of these is asserted here, so none needs re-pinning.
- Not re-measured live this round (host pause): behaviour of the 2.17.2 binary stays [UNK].
