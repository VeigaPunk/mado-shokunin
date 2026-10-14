# Config-health report — end-to-end verification pass, all four planes (MADO-R3-2)

Probe window: 2026-10-14 14:40–14:48 UTC (host offset −03:00; local 11:40–11:48),
user `vgpnk`. Assignment: round-3 end-to-end task, per `plans/round-3.plan.md`
("a full config-health report across all four planes with divergences and
recommendations").

Scope — the four planes: **hypr** (compositor config) · **waybar** (+ mako,
swayosd, idle/lock) · **walker** (launcher) · **terminals** (+ theme plane,
omarchy skill).

Method — read-only throughout. File bytes: `sha256sum`, `wc -lc`, `grep`, `diff`.
Live: `hyprctl` read verbs (`getoption`, `binds`, `clients`, `devices`,
`monitors`, `workspaces`, `activeworkspace`, `animations`, `instances`,
`layers`, `configerrors`, `version`); `layers` is added to the round-2 read-verb
whitelist this pass — it is read-only and is the only live window onto the
bar's layer surface (§3.1). Consumer probes: `ps`, `systemctl --user`,
`journalctl --user`, `busctl`, `makoctl`, `pgrep`, `printenv`, `omarchy`,
`lspci` (shape-only), `command -v`. Scratch: `/tmp/mado-r3-2-probe/` (scripts,
raw JSON, expected-value table; ephemeral). Nothing under `~/.config/` or
`~/.local/` was written; no session material content-read (no window titles,
no `/proc/*/environ`, `hyprland.log` untouched, instance signature
shape-checked only).

Safety — no mutating verb (`keyword`/`dispatch`/`reload`/`setprop`/`output`/…)
ran; no keystroke injection; no compositor state changed. Substrate
byte-identity vs MADO-1 §2 proven: 13/13 `sha256` equal (§2.1).

Tags: `[OBS]` measured · `[INF]` inference · `[UNK]` unknown.
Severity scale for divergences (§6):

- **S1 functional** — a declared behavior cannot happen live (missing
  consumer/state); safety- or user-visible.
- **S2 discrepancy** — declared vs live (or doc vs host) mismatch with a
  plausible user-visible effect; no breakage proven.
- **S3 informational** — record-level, hygiene, nominal rounding; no action required.

## 0. Verdict

- `[OBS]` Config load is clean: `hyprctl configerrors` empty (rc=0) at probe
  start and re-run at probe end; Hyprland 0.56.2 (`efb5099…`), Omarchy 3.8.3.
- `[OBS]` **No config drift since rounds 1–2.** 37 `sha256` checks this pass;
  every file that carries a recorded pin re-matches: 13/13 hypr files
  (incl. the backup), both waybar files, walker config, mako config, swayosd
  config, the two pinned theme color files (`waybar.css`, `walker.css`), and
  the six stock binding/rule files where
  R2-2 pinned hashes (§2.1, §3, §4, §5).
- `[OBS]` **The round-2 live layer holds.** 57/57 `getoption` rows re-measured
  byte-identical to R2-1 §3 (46 `agreement` + 6 `agreement*` + 4
  `live-default` over the 56, plus 1 extra pair from R2-2 §5); **0 `mismatch`**
  — the note's "any new mismatch falsifies" condition did not trigger
  (Appendix A).
- `[OBS]` Bind and rule surfaces identical: 192 binds, flag counters
  d190/e14/l26/m2/r1, 13-entry modmask histogram, 24 dispatchers; 79 window-rule
  statements = 4 + 69 + 2 + 4 — all equal to R2-2 §1/§3/§4.2.
- Divergences found: **1× S1** (F1 — idle-lock consumer absent), **2× S2
  watch items** (F2 — Alacritty tag/opacity anomaly reproduces; F3 — orphan
  NVIDIA env file on an NVIDIA-GPU host), **6× S3** (F4–F10, two of them
  record-level corrections). Nothing blocks the running session; the config
  plane is stable, the open items are runtime-state and record hygiene.

## 1. Coverage — every round-1/2 claim family re-checked

| Source | Claim family | Result this pass |
|---|---|---|
| MADO-1 §2 | 13 hypr files: sha/bytes/lines | 13/13 equal; totals 10,386 B active + 65 B bak = 10,451 B, 289 L (`wc -lc`) |
| MADO-1 §3 | 17 `source`s; include order | 17 equal; anchors `hyprland.conf:9/:13/:16-20/:23/:29` re-read |
| MADO-1 §4 | binds 192 = 25+23+4+90+50; unsourced files | equal; 192 live; orphan files still present & unsourced |
| MADO-1 §5 | rules: 5 local + stock 18-app set | 79 statements re-counted = 4+69+2+4; `apps.conf` sources 18 files |
| MADO-1 §6 | animations | 35 entries / 19 `overridden` / 6 beziers incl. built-in `default` |
| MADO-1 §7 | override-chain effective values | 57/57 getoptions (Appendix A) |
| MADO-1 §8 | separate consumers | hypridle absent (F1); hyprlock/hyprsunset absent; xdph portal PID 1920 |
| MADO-1 §9/§10 | version pins; runtime snapshot | 0.56.2; Omarchy 3.8.3; DP-1 3440x1440@99.997; ws 1 / 3 windows; grok-bot absent (F4) |
| MADO-2 §1 | plane inventory + backups | 6 files equal; backup listings equal; mako byte-cell provenance resolved (§3.1) |
| MADO-2 §2 | waybar modules/signals/style/indicators | bytes equal; signals & producers equal; `#a55555` ×4; live layer pair added (§3.1) |
| MADO-2 §3 | walker config/service/theme | equal; service active; autostart desktop byte-identical; theme width 644 |
| MADO-2 §4 | mako / swayosd plane | `makoctl mode` `default`; D-Bus owner mako; swayosd producers identified (§3.2) |
| MADO-2 §5 | idle/lock | F1; hyprlock still config-only (lock screen not observed, read-only) |
| MADO-2 §6 | drift vs stock | raw diff counts 85 / 31 changed lines re-measured; backups unchanged |
| MADO-2 §7/§9 | decision table; rejections | anchors re-read; SUPER+SPACE direction re-verified (menu print) |
| MADO-3 §1–§6 | terminals/theme/install state | 4 files equal; bak→live diff = one font-size hunk each; only Alacritty on PATH; palette equal |
| MADO-3 §7 | skill anatomy + hooks | 392 L / 14,908 B; five `*.d` hook dirs; flat-file listing drift stands |
| R2-1 §3/§4/§7 | 56 getoption + 9 non-getoption rows; byte identity | 57 rows 0 mismatch; 9 pairs re-measured; 13/13 sha identity |
| R2-2 §1–§4 | binds/flags/histogram/dispatchers/rules; §4.6 tags | all equal; client tags reproduce (F2) |
| R2-E blocks (all three notes) | errata items | re-measured, all stand (mako 119 B, SUPER+SPACE, grok-bot, note-length pins) |

## 2. Plane A — hypr

### 2.1 File bytes — 13/13 identical to MADO-1 §2 `[OBS]`

| File | sha256[:16] | Bytes | Lines |
|---|---|---|---|
| ai-usage.conf | `21e76af98ce791fa` | 319 | 5 |
| autostart.conf | `5ace17016fe2998a` | 210 | 5 |
| bindings.conf | `e574a1ed08535e31` | 2879 | 40 |
| envs.conf | `04af5cdf028bf488` | 133 | 5 |
| hypridle.conf | `e7d3b8dd983523e4` | 765 | 19 |
| hyprland.conf | `4f52854a3c143dcf` | 1273 | 29 |
| hyprlock.conf | `b8d173dcff558287` | 742 | 43 |
| hyprsunset.conf | `3042e4a923030239` | 363 | 14 |
| input.conf | `3769c92ab7660f17` | 1584 | 54 |
| looknfeel.conf | `777a4fdc8b61db44` | 1000 | 40 |
| monitors.conf | `69c9d8996dfdcd67` | 1012 | 29 |
| xdph.conf | `2fded88a27b89f33` | 106 | 4 |
| autostart.conf.bak.1791942509 | `8b472371e78b7f8b` | 65 | 2 |

Every first-16 equals MADO-1 §2 / R2-1 §7. `wc -lc` totals: 12 active files
10,386 B; + 65 B backup = 10,451 B across 289 lines.

### 2.2 Include graph, gates, toggles `[OBS]`

- `grep -c '^source' hyprland.conf` → **17** (equal). Span checks re-read:
  `:9` default envs, `:13` theme, `:16-20` five local files, `:23` toggle glob,
  `:29` `ai-usage.conf` last.
- Toggles dir: `flags.conf` 141 B (comment-only), `window-no-gaps.conf` 135 B,
  still the enabled one; contents re-read — `gaps_out=0`, `gaps_in=0`,
  `border_size=0`, `rounding=0`. So the live no-gaps/no-border frame is still
  toggle-owned (MADO-1 §7).
- Default tree: 35 files / 33,830 B (equal to MADO-1 §1); unsourced files still
  present (`bindings.conf` deprecated, `bindings/tiling.conf`,
  `plain-bindings.conf`, `apps/davinci-resolve.conf`,
  `toggles/single-window-aspect-ratio.conf`).

### 2.3 Binds `[OBS]`

- `hyprctl -j binds` → **192**; flags `has_description 190 / repeat 14 /
  locked 26 / mouse 2 / release 1`; modmask histogram
  `{0:23, 1:2, 8:7, 9:2, 12:2, 13:1, 64:42, 65:37, 68:26, 69:3, 72:19, 73:22, 76:6}`;
  `submap ""` ×192, `catch_all 0` — all equal to R2-2 §1/§2.2.
- Dispatcher histogram (24 dispatchers): `exec 104`, `workspace 15`,
  `changegroupactive 11`, `movetoworkspacesilent 11`, `movetoworkspace 10`,
  four ×4, `sendshortcut 3`, seven ×2, eight ×1 — equal to R2-2 §3.
- The full 192/192 reconciliation was not re-run; the five source files'
  sha256 equal R2-2 §1 (`e574a1ed…` local; `8d21d57e…`, `19ca281a…`,
  `0cca5669…`, `57ddb304…` stock) — the round-2 result stands by byte identity.

### 2.4 Effective values — the 57-row `getoption` pass `[OBS]`

All 57 rows (56 from R2-1 §3 + `decoration:rounding_power` from R2-2 §5)
re-measured equal, `set` flags included; **0 mismatches**. Census over the 56:
46 `agreement` + 6 `agreement*` (shadowing proofs: toggle owns gaps/border,
local owns `kb_layout`, theme owns the two borders) + 4 `live-default`. Full
measured table in Appendix A. The `gaps_in`/`kb_layout`/`binds` spot-checks
also re-ran standalone (§11).

### 2.5 Runtime `[OBS]`

- monitors: DP-1 `3440x1440` refresh `99.997` at `0x0` scale `1`, desc
  `LG Electronics LG ULTRAWIDE 508AZFMF7323` — declared `@100`
  (`monitors.conf:10`); nominal-quantization class carried (F5).
- workspaces: 1 workspace (id/name `1`, DP-1, 3 windows); activeworkspace same
  — pure runtime state, no declarer.
- clients: 3 windows, all class `Alacritty`, all workspace 1; tags
  `default-opacity*,terminal*` (PID 3982970), `terminal*` (PID 275049),
  `default-opacity*,terminal*` (PID 1784450) — reproduces R2-2 §4.6 (F2).
  Titles not read.
- devices: **9** keyboard nodes, all `active_keymap: Portuguese (Brazil)`,
  layout `br` (R2-1 §4 recorded 8 — F9); 0 touch devices, 4 mice. The
  touchpad options (`input.conf:31-37`) are declared and hit live values
  (§2.4) but no touchpad device is currently attached — forward-looking
  config, not a fault.
- animations: 35 entries, 19 `overridden: true`, 6 beziers
  (`quick, almostLinear, easeInOutCubic, easeOutQuint, linear, default`) —
  equal to R2-1 §4.
- instances: 1; `wl_socket` present as `wayland-1` in `-j` (F8); socket dir
  `/run/user/1000/hypr/<sig>/` holds `.socket.sock`, `.socket2.sock` (both
  `srwx`) and `hyprland.lock` — R2-1 §1 surface claim re-verified; signature
  shape `<commit>_<epoch>_<pid>` only.
- `configerrors` empty, rc=0; `version` 0.56.2, commit `efb5099…` (equal).
- layers (whitelist extension, read-only): `wallpaper` level 0;
  `waybar` level 2 (= top), geometry `3440x26`, PID 1707 — see §3.1.

### 2.6 Adjacent consumers `[OBS]`

- hypridle: absent (F1) — `pgrep -x` no match, `systemctl --user is-active`
  `inactive`, but session journal proves it started at boot (§F1).
- hyprlock: absent (`pgrep -x` no match); config-only surface unchanged.
- hyprsunset: absent; identity-profile config unchanged.
- xdg-desktop-portal-hyprland: PID **1920** running (same PID as MADO-1 §8).
- Grok Bot: no process; symlink + 134,596,858 B target present (F4).
- env: `GDK_SCALE=1` (`monitors.conf:9` ✓); all 12 vars of the sourced default
  `envs.conf` SET; the 3 vars of the orphan local `envs.conf` UNSET
  (`NVD_BACKEND`, `LIBVA_DRIVER_NAME`, `__GLX_VENDOR_LIBRARY_NAME`) — F3.

## 3. Plane B — waybar (+ mako, swayosd, idle/lock)

### 3.1 waybar `[OBS]`

- Files: `config.jsonc` 249 L / 6,068 B `07f7d663106b72e4`; `style.css`
  136 L / 1,887 B `8316c08ceaa7e3f0`; backup listing equals MADO-2 §6
  (`.bak` 5,892 B; `.bak.1791314470` 5,114 B; style baks 1,458 B ×2). Drift vs
  stock still present: raw diff counts 85 / 31 changed lines (includes the
  reformatting class; consistent with MADO-2 §6 items 1–6).
- Live: PID 1707 started `Tue Oct 13 11:02:07` local, still the same process;
  bar surface visible to the compositor at layer level 2 = **top** with
  geometry `3440x26` — matches declared `layer: "top"` (`config.jsonc:3`) and
  `height: 26` (`:6`). This is a compositor-side live pair; **waybar itself
  exposes no introspection verb** (`waybar --help` lists only `-c/-s/-l/-b`
  launch options), so the round-3 anti-claim branch applies: the bar's evidence
  class here is file-bytes + compositor view, labeled.
- Signal bus: consumers `config.jsonc:66/203/209/215/239` (7/8/9/10/11);
  producers `omarchy-capture-screenrecording:253`,
  `omarchy-toggle-idle:13`, `omarchy-toggle-notification-silencing:13`,
  `omarchy-update-available-reset:5`, and the external
  `waybar-on-click.sh:6` (signal 11) — all equal to MADO-2 §2.3.
- Style: 4× hardcoded `#a55555` (`style.css:96/101/110/135`); theme
  `waybar.css` still only fg/bg (2 L, `a1807a176659d7d6`) — the red and the
  ai-usage chip remain theme-independent (carried).
- Indicators: `idle.sh` (pgrep hypridle → disabled glyph), 
  `notification-silencing.sh` (mako mode), `screen-recording.sh`
  (gpu-screen-recorder) — semantics unchanged; `makoctl mode` → `default`.
- Notification ownership: D-Bus `org.freedesktop.Notifications` → PID 1706
  (`/usr/bin/mako`), `:1.44` — equal to MADO-2 §4.

### 3.2 mako / swayosd `[OBS]`

- mako config byte-cell provenance resolved: `~/.config/mako/config` is a
  **symlink** to `~/.config/omarchy/current/theme/mako.ini`; `ls -la` shows the
  50-character target string (the original "50 B" figure was the symlink's own
  size), `wc -lc` through the link → 5 L / 119 B, sha `95bf0c86c955cc81…` (the
  value R2-E1 recorded). Both historical numbers measure different objects;
  content equals R2-E1's corrected cell. Theme switches rewire the mako colors
  through this link.
- mako CLI: `mako --version` → rc=1, prints `unrecognized option '--version'`
  **and** `Failed to parse config` (F10; no version flag exists; `--help` is
  clean). The running daemon is healthy (boot-start journal line, D-Bus owner,
  `makoctl mode` works).
- swayosd: `config.toml` 4 L / 87 B `a8a09212a32f38df`; `style.css` 28 L /
  372 B; server PID 1815. OSD producers identified (closes part of MADO-2 §8
  U2): volume keys → `omarchy-swayosd-client` (`media.conf:2-4, 18-19, 24-27`),
  brightness keys → `omarchy-brightness-display` (`media.conf:6-9, 20-21`) →
  `omarchy-swayosd-brightness`. So the OSD keys are the `XF86Audio*` /
  `XF86MonBrightness*` media keys, routed through omarchy wrappers `[OBS]`.

### 3.3 idle / lock

See F1. hyprlock remains config-only in this pass (no lock triggered —
read-only discipline); its files are unchanged.

## 4. Plane C — walker `[OBS]`

- `~/.config/walker/config.toml` 49 L / 1,336 B `fecf71fa4253803e` (equal);
  `~/.config/autostart/walker.desktop` sha `5cb9874eedbcb32c`, 138 B —
  **byte-identical** to stock `~/.local/share/omarchy/default/walker/walker.desktop`.
- Service `app-walker@autostart.service` active/generated, Main PID 1808 from
  boot; `elephant.service` active + enabled (equal to R2, plus now active).
- Theme: exactly one theme (`omarchy-default`); `style.css` 121 L;
  `layout.xml` `width-request 644` (line 15) — equal to MADO-2 §3.
- No own introspection (`walker --help` = launch flags only) — file-byte +
  process/service evidence class.
- Launch path re-verified via `omarchy menu keybindings --print`:
  `SUPER + SPACE → Launch apps` (stock `utilities.conf:2` → walker),
  `SUPER ALT + SPACE → Omarchy menu`, `COPILOT KEY → Omarchy menu`,
  `SUPER SHIFT CTRL + SPACE → Theme menu`; local `bindings.conf:40` still the
  commented walker line — R2-E2 holds.

## 5. Plane D — terminals (+ theme, omarchy skill) `[OBS]`

- Four config files equal (876/28, 516/25, 954/34, 1,325/41 B/L); sha256
  recorded this pass for future rounds (`695301c8…`, `3e883544…`,
  `f875291e…`, `cb828c04…`).
- Backups 873/513/953/1322 B; bak→live `diff` = exactly one hunk per file,
  font size `9 → 12.5` — the MADO-3 §6 delta stands.
- Only Alacritty on PATH (`/usr/bin/alacritty`); `foot`/`kitty`/`ghostty` NOT
  FOUND (F6). `xdg-terminals.list` 127 B, first entry `Alacritty.desktop`;
  foot desktop stubs 28 B both.
- Theme: `theme.name` 12 B `matte-black`; `omarchy theme current` →
  `Matte Black`; palette spot values present in theme files (`#121212`,
  `#bebebe`, `#eaeaea`, `#515151`, `#333333`, `#D35F5F`, `#e68e0d`);
  theme `waybar.css` 2 L / 68 B `a1807a17…` and `walker.css` 6 L / 191 B
  `f44cb450…` re-match their MADO-2 pins; `hyprlock.conf` 5 L / 176 B and
  `mako.ini` 5 L / 119 B measured this pass (no prior pin for those two;
  `mako.ini` is the symlink target of the pinned mako config, §3.2).
  `~/.config/omarchy/current`
  is still a real directory, not a symlink (MADO-1 §12 item 4 partial).
- omarchy skill: 392 L / 14,908 B, single file — equal. Hooks dir: five
  `*.d` directories (`battery-low.d`, `font-set.d`, `post-boot.d`,
  `post-update.d`, `theme-set.d`) — the skill's flat-file listing drift stands
  (MADO-3 §7).

## 6. Divergence register

### F1 — idle-lock consumer absent (S1 functional)

**Evidence `[OBS]`.** `pgrep -x hypridle` no match; `systemctl --user
is-active hypridle` → `inactive`, `is-enabled` → `disabled`,
`journalctl --user -u hypridle` → `No entries` (the unit never ran). But the
**session** journal shows it *did* start at boot: `uwsm_app-daemon` received
`app -- hypridle` → `systemd-run … --unit=app-Hyprland-hypridle-3ab80ab5.scope
… -- hypridle` → `Started hypridle.` (Oct 13 11:02:09 local); that scope is
now collected (`status` → could not be found) and no stop line was logged.
So "never started" is ruled out; the daemon stopped between Oct 13 11:02 and
the round-1 absence observation (~Oct 14 09:52 local) — **stop time and cause
`[UNK]`**. The only in-repo stopper found is `omarchy-toggle-idle` (`pkill -x
hypridle` / `uwsm-app -- hypridle`; stateless — no marker file), reachable
three ways: bar glyph click (`config.jsonc:207`), `SUPER CTRL+I`
(`utilities.conf:30`), omarchy menu (`bin/omarchy-menu:212`). The bar's
`idle.sh` currently renders the disabled glyph + tooltip "Idle lock disabled".

**Consequence.** The declared chain — 150 s screensaver / 152 s lock
(`hypridle.conf:9-12, 15-18`) — has no consumer, so it cannot fire; with no
one at the desk the session is not screen-locked. May be deliberate (the
toggle exists precisely for this), but the report cannot distinguish
operator-toggled-off from a later exit `[UNK]`.

**Recommendation (operator).** If idle locking is wanted: activate any toggle
route — click the bar glyph, press `SUPER CTRL+I`, or omarchy menu → *Idle* —
or run `uwsm-app -- hypridle`; each starts the daemon (absent → toggle's start
branch) and notifies "Now locking computer when idle". Verify: `pgrep -x
hypridle` non-empty and the bar glyph clears (it probes `pgrep`). Why: this
re-arms the declared 150 s/152 s chain so the screensaver and lock screen
protect the session again. If off is intended: no change needed — but note it
is **session-only**: the default autostart (`default/hypr/autostart.conf:1`,
`exec-once = uwsm-app -- hypridle`) will start it again at next login, so the
off state must be toggled again (or the exec-once dealt with) after each boot.

### F2 — Alacritty opacity/tag anomaly reproduces (S2 discrepancy)

**Evidence `[OBS]`.** 3 clients, tags: `3982970 default-opacity*,terminal*`;
`275049 terminal*`; `1784450 default-opacity*,terminal*` — identical to
R2-2 §4.6, unchanged since. New this pass: window ages (local start times) —
the *correct* window is the **oldest** (Oct 13 16:17:59); the two flagged
windows are **newer** (Oct 14 01:07:35 and Oct 14 09:26:56). Consequence per
R2-2 `[INF-docs]`: `windows.conf:15` also matches those two windows, so their
opacity is the product ≈0.9409 active / 0.81 inactive — darker than the
declared intent (`terminals.conf:3` unsets the tag; `:4` sets 0.97/0.9).
Cause `[UNK]`; the config bytes involved are provably unchanged (§2.1,
R2-2 hashes). The age ordering (newer windows carry the tag) does not fit a
simple "stale window" story `[OBS]`.

**Recommendation (operator).** Close the two flagged windows
(PIDs 3982970, 1784450), open a fresh Alacritty, then re-run `hyprctl -j
clients` and read the tags — a fresh window is expected to show `terminal*`
**without** `default-opacity*`. If it does, the anomaly was window-state and
is cleared; if a fresh window *also* carries `default-opacity*`, keep the
evidence and treat it as a rule-sequencing finding (repeatable operator test,
still read-only for mado). Why: restores the declared opacity (0.97/0.9) on
those windows and settles an `[UNK]` carried since round 2.

### F3 — orphan `envs.conf` (NVIDIA trio) on an NVIDIA-GPU host (S2 potential)

**Evidence `[OBS]`.** File 133 B, sha `04af5cdf028bf488` (unchanged);
`sourcer grep` across `~/.config/hypr/`, `default/hypr/`, `toggles/` finds
exactly one `envs.conf` `source` — `hyprland.conf:9` → the *default* file;
the local file is sourced by nothing. Live: all three of its vars UNSET
(`NVD_BACKEND`, `LIBVA_DRIVER_NAME`, `__GLX_VENDOR_LIBRARY_NAME`), while all
12 default-envs vars are SET. New this pass: `lspci -nn` (shape-only) shows
**NVIDIA GB205 [GeForce RTX 5070]** + AMD Granite Ridge iGPU — the vendor the
orphan file targets is present (closes the hardware half of R2-1 §10 U8).

**Recommendation (operator).** Decide intent: (a) if the NVIDIA overrides are
wanted, add `source = ~/.config/hypr/envs.conf` to `~/.config/hypr/hyprland.conf`
(auto-reload applies it on save; verify by checking `printenv NVD_BACKEND` in a
freshly launched app) — the three vars are the documented Hyprland-on-NVIDIA
trio `[INF-docs]`, and today they are provably inert; (b) if unwanted, archive
the file (rename to `.bak`) so it stops reading as half-finished setup. Why:
either the trio is intentional and should take effect, or it is dead weight in
the edit surface; leaving it both un-sourced and NVIDIA-shaped is the one state
that keeps confusing future readers. Effect of the unset trio on this host
remains **`[UNK]`** (no read-only surface measures it).

### F4 — Grok Bot exec-once, no process (S3 informational)

**Evidence `[OBS]`.** `autostart.conf:5` declares
`exec-once = /home/vgpnk/.local/share/grok-bot/appimage --ozone-platform=x11`;
no matching process; symlink → `/home/vgpnk/Applications/Grok_Bot_0.70.2.AppImage`
(134,596,858 B, mtime 2026-10-13 22:29:16 local). Equal to R2-E3; the target's
mtime still postdates session start + the autostart rewrite, so exec-once
cannot have launched this build at login; whether it ran later and exited is
`[UNK]`.

**Recommendation.** None required. If the app is expected at login, launch the
symlink once by hand to observe the real error; if it is no longer wanted,
comment `autostart.conf:5`. Why: keeps the login declaration honest with what
actually runs.

### F5 — monitor refresh 99.997 vs declared 100 (S3 nominal)

**Evidence `[OBS]`.** `monitors.conf:10` declares `3440x1440@100`; live
`refreshRate` `99.997`. Class carried: EDID nominal quantization `[INF]`.
**Recommendation.** None — no functional effect; only revisit if a mode
negotiation issue ever appears.

### F6 — terminal configs for uninstalled binaries (S3 informational)

**Evidence `[OBS]`.** foot/kitty/ghostty configs exist (bytes equal), binaries
NOT on PATH; only Alacritty installed and referenced.
**Recommendation.** Optional: `omarchy install terminal` if those terminals
are wanted (omarchy skill route); otherwise leave — the configs are inert.

### F7 — backup litter (S3 hygiene)

**Evidence `[OBS]`.** `autostart.conf.bak.1791942509` (65 B) in hypr; 4 backups
in waybar; 4 in terminal dirs. Refresh tools create these by design
(`<config>.bak.$(date +%s)`); no consumer reads them.
**Recommendation.** Optional archiving; nothing to fix.

### F8 — R2-1 §1 `wlSocket` observation does not reproduce (S3 record-level)

**Evidence `[OBS]`.** R2-1 §1 recorded: "its `wlSocket` field is `null` `[UNK]`
why" (its §10 U7). Live re-measure: `hyprctl -j instances` — one entry with
key `wl_socket` = `"wayland-1"` (a string; no `wlSocket` camelCase key at all);
plain `hyprctl instances` renders `wl socket: wayland-1`.
**Recommendation.** None for the operator. Lane-side: erratum candidate for
MADO-R2-1 §9 (write scope is this file, so not applied there): "§1's
`wlSocket: null` does not reproduce on 0.56.2; the live key is `wl_socket` and
its value is the socket name; UNK item 7 is moot as phrased."

### F9 — keyboard node count 8 → 9 (S3 informational)

**Evidence `[OBS]`.** R2-1 §4 recorded 8 keyboard nodes; live `devices` shows
**9** (razer-deathadder ×2, hyperx-alloy-origins ×3, video-bus,
power-button ×2, `hl-virtual-keyboard-fcitx5`), all keymap
`Portuguese (Brazil)` / layout `br` — the claim's substance (br everywhere)
holds over all 9. Cause `[UNK]`; candidate `[INF]`: the fcitx5 virtual
keyboard node (fcitx5 PID 1709 running; device list is hotplug-sensitive).
**Recommendation.** None; count-sensitive claims should state device context.

### F10 — `mako --version` misuse emits `Failed to parse config` (S3 note)

**Evidence `[OBS]`.** `mako --version` → rc=1, stderr:
`unrecognized option '--version'` + `Failed to parse config`. No version flag
exists; `mako --help` is clean. The daemon is healthy (boot-start journal
line, D-Bus name owner PID 1706, `makoctl mode` works), so this is CLI misuse
output, not a daemon-config symptom; whether the second line has any
config-parse meaning is `[UNK]`.
**Recommendation.** None; use `mako --help` for version-adjacent checks.

## 7. Operator recommendation summary (priority order)

1. **Decide idle-lock state** (F1). If wanted: bar-glyph click / `SUPER CTRL+I`
   / omarchy menu → *Idle*; verify with `pgrep -x hypridle` + bar glyph. If
   not: accept session-only, re-check after next login.
2. **Clear the Alacritty tag anomaly** (F2): close PIDs 3982970 and 1784450,
   open a fresh terminal, re-check `hyprctl -j clients` tags.
3. **Settle `envs.conf`** (F3): source it (if the NVIDIA trio is intended) or
   archive it.
4. **Grok Bot** (F4) only if it should be running; F5–F10 need no action.
   All commands above are operator-side; mado stays read-only per PROVINCE.md.

## 8. Unknowns

1. hypridle stop time/cause (F1) — bounded (start Oct 13 11:02:09; absent by
   ~Oct 14 09:52 local) but not resolvable read-only.
2. F2 root cause (tag evaluation vs window lifecycle); operator test named.
3. F3 effect of the unset NVIDIA trio on this host.
4. `set`-flag semantics (R2-1 §10 U1, carried).
5. `col.active_border` `45deg` survival after single-color assignment (U2, carried).
6. Whether any window rule currently matches an open window (no rule-read verb; U4, carried).
7. `$OMARCHY_PATH` resolution in the waybar process (no env reads; U4 of MADO-2).
8. Which tool wrote `config.jsonc.bak` (un-suffixed) and the epoch-name/metadata mismatch (MADO-2 §6, carried).
9. F9's exact cause; F10's second line; lock screen never end-to-end observed
   (read-only — no lock triggered); `custom/weather` live render unread.
10. Whether `omarchy restart terminal` restarts the uninstalled terminals
    (not executed; carried from MADO-3 §8).

## 9. Lane-internal carry

- `SKILL.md` "Round 2 sources" quotes `keybind-rule-semantics.md` as "313 by
  `wc -l`"; measured 315 (LOG round-2 observation (a)). Still unfixed as of
  this pass; belongs to the SKILL-authoring lane, not this file.
- Note-length convention: round-1 bodies are 217/364/179 by `wc -l`
  (editor 218/365/180); counts must name their command.
- Erratum candidate forwarded via F8 to MADO-R2-1 §9 (not applied here —
  write scope is this file only).

## 10. Errata (append-only — add blocks, never edit above)

- E1 (2026-10-14, MADO-R3-2 seed): no corrections to this note yet. Erratum
  candidates forwarded to other notes are tracked in §6 (F8 → MADO-R2-1 §9).

## 11. Spot-checks (reproducible, re-run at 14:48 UTC)

1. `sha256sum ~/.config/hypr/hyprland.conf` →
   `4f52854a3c143dcf58430a679e339619223d2b5008115a322d06b2de637ea462`
   (= MADO-1 §2 = R2-1 §7).
2. `hyprctl getoption general:gaps_in` → `custom type: 0 0 0 0` `set: true`;
   `hyprctl -j binds | jq length` → `192`.
3. `hyprctl -j clients` tags → `default-opacity*,terminal*` (3982970) /
   `terminal*` (275049) / `default-opacity*,terminal*` (1784450);
   `pgrep -x hypridle` → no match.
4. Full-pass reproducer (scratch, ephemeral):
   `bash /tmp/mado-r3-2-probe/01-filebytes.sh`,
   `…/02-hyprctl.sh` (writes the 57 raw getoption JSONs),
   `…/03-consumers.sh`, then `python3 /tmp/mado-r3-2-probe/check-getoptions.py`
   → `checked 57; mismatches/missing: 0`.

## Appendix A — 57-option live re-measure (0 mismatches vs R2-1 §3/R2-2 §5)

`hyprctl -j getoption <opt>`, 2026-10-14 14:43 UTC. `set` flag from the JSON;
class column = round-2 claim, re-confirmed by value equality.

| Option | Live | set | class |
|---|---|---|---|
| `general:gaps_in` | 0 0 0 0 | set | agreement* |
| `general:gaps_out` | 0 0 0 0 | set | agreement* |
| `general:border_size` | 0 | set | agreement* |
| `general:col.active_border` | ffe68e0d 45deg | set | agreement* |
| `general:col.inactive_border` | aa595959 0deg | set | agreement |
| `general:resize_on_border` | 0 | set | agreement |
| `general:allow_tearing` | 0 | set | agreement |
| `general:layout` | dwindle | set | agreement |
| `general:snap:enabled` | 0 | unset | live-default |
| `decoration:rounding` | 0 | set | agreement |
| `decoration:shadow:enabled` | 1 | set | agreement |
| `decoration:shadow:range` | 2 | set | agreement |
| `decoration:shadow:render_power` | 3 | set | agreement |
| `decoration:shadow:color` | ee1a1a1a 0deg | set | agreement |
| `decoration:blur:enabled` | 1 | set | agreement |
| `decoration:blur:size` | 2 | set | agreement |
| `decoration:blur:passes` | 2 | set | agreement |
| `decoration:blur:special` | 1 | set | agreement |
| `decoration:blur:brightness` | 0.6 | set | agreement |
| `decoration:blur:contrast` | 0.75 | set | agreement |
| `decoration:dim_inactive` | 0 | unset | live-default |
| `animations:enabled` | 1 | set | agreement |
| `dwindle:preserve_split` | 1 | set | agreement |
| `dwindle:force_split` | 2 | set | agreement |
| `scrolling:column_width` | 0.49 | set | agreement |
| `master:new_status` | master | set | agreement |
| `group:col.border_active` | ffe68e0d 45deg | set | agreement* |
| `group:groupbar:font_size` | 12 | set | agreement |
| `group:groupbar:height` | 22 | set | agreement |
| `group:groupbar:gaps_in` | 5 | set | agreement |
| `misc:disable_hyprland_logo` | 1 | set | agreement |
| `misc:focus_on_activate` | 1 | set | agreement |
| `misc:anr_missed_pings` | 3 | set | agreement |
| `misc:on_focus_under_fullscreen` | 1 | set | agreement |
| `misc:key_press_enables_dpms` | 1 | set | agreement |
| `misc:mouse_move_enables_dpms` | 1 | set | agreement |
| `cursor:hide_on_key_press` | 1 | set | agreement |
| `cursor:warp_on_change_workspace` | 1 | set | agreement |
| `binds:hide_special_on_workspace_change` | 1 | set | agreement |
| `input:kb_layout` | br | set | agreement* |
| `input:kb_variant` | (empty) | set | agreement |
| `input:kb_model` | (empty) | set | agreement |
| `input:kb_options` | compose:caps | set | agreement |
| `input:kb_rules` | (empty) | set | agreement |
| `input:follow_mouse` | 1 | set | agreement |
| `input:sensitivity` | 0.0 | set | agreement |
| `input:accel_profile` | [[EMPTY]] | unset | live-default |
| `input:touchpad:natural_scroll` | 0 | set | agreement |
| `input:touchpad:clickfinger_behavior` | 1 | set | agreement |
| `input:touchpad:scroll_factor` | 0.4 | set | agreement |
| `input:touchpad:disable_while_typing` | 1 | unset | live-default |
| `input:repeat_rate` | 40 | set | agreement |
| `input:repeat_delay` | 250 | set | agreement |
| `input:numlock_by_default` | 1 | set | agreement |
| `xwayland:force_zero_scaling` | 1 | set | agreement |
| `ecosystem:no_update_news` | 1 | set | agreement |
| `decoration:rounding_power` | 2.0 | unset | extra (R2-2 §5) |

## Errata (round 4) — appended 2026-10-14 (ERR-M)

Append-only block; nothing above is edited. Written by the round-4 errata
sweep; read-only probes 2026-10-14 16:20–16:25 UTC (scratch
`/tmp/w4-err-m-sweep/`). Runtime rows in this report are point samples of its
own probe window (14:40–14:48 UTC); the environment changed after it (E3).

- **E2 (tally corrigendum — §0).** §0 renders the register as "**6× S3**
  (F4–F10)"; the register holds **7** S3 findings — F4, F5, F6, F7, F8, F9,
  F10 = 7 (F4–F10 inclusive = 7). Correct totals: **1× S1 + 2× S2 + 7× S3 =
  F1–F10 (10 findings)**. Counted 16:2x UTC: `grep -c '^### F'` → 10, S3
  headers → 7. Per-finding severities are unaffected (LOG round-3 observation
  (a), applied).
- **E3 (superseding observation — F1 and the runtime layer; session
  turnover).** The session was replaced at ~16:11:06–07 UTC: the old
  compositor (PID 1671 — its PIDs populate §2–§3: waybar 1707, mako 1706,
  xdph 1920, …) is gone; the current instance is Hyprland **1203316**
  (`instances` `time` 1791994267 = 16:11:07 UTC; waybar 1203352, mako
  1203350; logind sessions 4–5). In the new instance hypridle ran as an
  autostart child — **PID 1203349**, started 16:11:07 UTC, ppid = Hyprland —
  measured present 16:21:49 UTC by this sweep and **absent again by 16:23:19
  UTC** (repeated `pgrep -a hypridle` → no match; `systemctl --user
  is-active` stayed `inactive` / `disabled` throughout — the daemon is a
  session child, never the unit). F1's evidence and consequence remain
  accurate for its probe window; post-turnover the daemon state is unstable
  (present 16:11:07–~16:22, absent from ~16:23:19) and the old instance's
  stop cause stays `[UNK]` — F1's S1 classification is a point-sample
  verdict; re-classification belongs to the next health pass. The autostart
  route itself is demonstrably functional in a fresh session
  (`default/hypr/autostart.conf:1` re-read; which launcher fired it `[UNK]`);
  the round-4 audit of `idle-lock-plane.md` (AUD-M1) reached the same
  turnover observation, same PIDs.
- **E4 (closure — F8 applied).** §6 F8's forwarded record correction was
  applied to MADO-R2-1 as `hyprctl-verification-layer.md` "Errata (round 4)"
  entry E3 (plus closure E2 for the older candidate); §9/§10's "tracked in §6
  (F8 → MADO-R2-1 §9)" carry is satisfied by this sweep.
- **E5 (closure — §9's stale-quote carry resolved).** §9's "Still unfixed as
  of this pass" note on the SKILL "313 by `wc -l`" quote was resolved in the
  same round by MADO-R3-3: the current `SKILL.md` reads "315 L by `wc -l`" in
  its round-2 sources and carries the fix note referencing LOG round-2
  observation (a) (re-read this pass; the SKILL file is under active edit by
  the round-4 lane, so its line counts are not pinned here). Carry closed.

## Reproduction package (round 4)

Appended 2026-10-14 by MADO-R4-1 (validation probes 16:21–16:24 UTC;
scratch `/tmp/w4-m4-1-repro/`). Purpose: the round-4 **box-3** re-run — a
non-author reviewer executes one pass of the commands below and judges §6's
findings against the recorded shapes and divergence classes. Read the ERR-M
block above first (E3 = session turnover at 16:11:07 UTC; E2 = tally).
Nothing above is edited. This kit supersedes §11.4's dependence on the
ephemeral `/tmp/mado-r3-2-probe/` scratch.

**Law.** Read verbs only — the `hyprctl` read verbs of §2.5 (incl. `layers`);
never `keyword`/`dispatch`/`reload`/`setprop`/`output`. No window titles, no
`/proc/*/environ`, no `hyprland.log` content; writes only under `$D`. Needs:
bash, coreutils, python3, `jq`, `hyprctl`, `pgrep`/`ps`,
`systemctl`/`journalctl --user`, `busctl`, `makoctl`, `omarchy`, `lspci`,
`printenv`. One pass ≈ 1 s on this host (§R.6 receipts).

**Legend.** `[PIN]` byte-stable — any mismatch is drift: stop, record, do not
repair. `[CFG]` config-derived live value — must equal the recorded shape.
`[EPOCH]` session-scoped — differs run to run; record, never fail.

### R.1 Setup

```bash
export D=/tmp/w4-repro; G="$D/getoption"; mkdir -p "$G"
```

### R.2 Pass 1 — file bytes and pins `[PIN]`

R.2.1 — 29 recorded pins: `file sha256 bytes lines`, one per line (full
sha256, re-measured 16:24 UTC; every prefix equals §2.1/§3/§4/§5). Save the
block below as `$D/pins.list`, then run the loop.

```
.config/hypr/ai-usage.conf 21e76af98ce791fa829b99d41a51014ec910a9db602e5a9806da233350ad423e 319 5
.config/hypr/autostart.conf 5ace17016fe2998aa6e7ad2221c1889b430aa4b94faf5ef1f907d6301dd5fc46 210 5
.config/hypr/bindings.conf e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581 2879 40
.config/hypr/envs.conf 04af5cdf028bf48897a5cebe77c720d4352925e159f7c2f8c7484396f1be9c49 133 5
.config/hypr/hypridle.conf e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41 765 19
.config/hypr/hyprland.conf 4f52854a3c143dcf58430a679e339619223d2b5008115a322d06b2de637ea462 1273 29
.config/hypr/hyprlock.conf b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1 742 43
.config/hypr/hyprsunset.conf 3042e4a923030239f4edf7b1943f41f4ed57107550177130c96f3b215b226e22 363 14
.config/hypr/input.conf 3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4 1584 54
.config/hypr/looknfeel.conf 777a4fdc8b61db4419c3392d43fbb549ceb868bf8eaa84d9bf278d6e40a8c1ea 1000 40
.config/hypr/monitors.conf 69c9d8996dfdcd6747775e984a479c53a520bd2ef193d337e171927fdf6795ee 1012 29
.config/hypr/xdph.conf 2fded88a27b89f33cbc2b64a1258117df74b591f39a84c78ec3504a7d3b09136 106 4
.config/hypr/autostart.conf.bak.1791942509 8b472371e78b7f8b9656b53bfe2290ff1f96b14e90bb063ebe1e3316437057ed 65 2
.config/waybar/config.jsonc 07f7d663106b72e4c2a7da90883ef2ade044d7e6cb791e81ead777f7d8a08e71 6068 249
.config/waybar/style.css 8316c08ceaa7e3f0624e1b82b1e03523096820fbf775362a930d7f831b0c4e8f 1887 136
.config/walker/config.toml fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787 1336 49
.config/mako/config 95bf0c86c955cc813d1b60d18e738567c7f135885c5f02a6acfbbb38946e3bec 119 5
.config/swayosd/config.toml a8a09212a32f38dfa570a2e21a7181b5164cb1ddd2e9ec223b5e7af14a9bd187 87 4
.config/swayosd/style.css 6e3ba08fd929ba345c405c151858a581e2c0ced724ef07e0e23f155731f76d8c 372 28
.config/omarchy/current/theme/waybar.css a1807a176659d7d6beaaf2a5c96cb7a03d131ee2740b8961d4c9aee393839c18 68 2
.config/omarchy/current/theme/walker.css f44cb45063494d2f4a8f489c47d8901b3bc98b27fbd1ca1c5a8801b40606bbc0 191 6
.config/omarchy/current/theme/hyprlock.conf 3ef010e72b5f69113e1500bb083fb053f9f121212ad5ed4fe74ad8d12507ad0b 176 5
.config/omarchy/current/theme/mako.ini 95bf0c86c955cc813d1b60d18e738567c7f135885c5f02a6acfbbb38946e3bec 119 5
.config/alacritty/alacritty.toml 695301c86577c808a94a01a4227bfaab3dbbe9a394a9954032f6173adec824f8 876 28
.config/foot/foot.ini 3e88354476f2682e7a1a0bc840d04e221e5c6a7312b3ee9dcf76ec16d0842e60 516 25
.config/kitty/kitty.conf f875291ecfe64ebc4ddc588282bcdb20fb883769e9938148411efa378d7f1e70 954 34
.config/ghostty/config cb828c044b07d4fd924fe1d6b55c956035feb16f8d5c67899c8a598994596667 1325 41
.config/autostart/walker.desktop 5cb9874eedbcb32c7b121ea60f6433f881499247cac7e6473a9a93adeebc3aa7 138 7
.agents/skills/omarchy/SKILL.md becd149e4d1c0767a80bcc1eb84e86e509149dc1e4b3d680cf24ab54bea5256d 14908 392
```

```bash
while read -r rel sha by ln; do
  f="$HOME/$rel"; got=$(sha256sum "$f" 2>/dev/null | cut -d' ' -f1)
  gb=$(wc -c < "$f" 2>/dev/null); gl=$(wc -l < "$f" 2>/dev/null); st=OK
  [ "$got" != "$sha" ] && st=PIN-DIFF
  [ "$gb" != "$by" ] && st="$st BYTES($gb!=$by)"
  [ "$gl" != "$ln" ] && st="$st LINES($gl!=$ln)"
  echo "$st | $rel | ${got:0:16} | $gb | $gl | $by/$ln"
done < "$D/pins.list" | tee "$D/pins-check.txt"   # expect: 29 lines, all "OK"
```

R.2.2 — include graph, toggles, anchors, mako symlink:

```bash
grep -c '^source' ~/.config/hypr/hyprland.conf                 # 17
sed -n '16,20p;23p;29p' ~/.config/hypr/hyprland.conf           # five locals; toggles glob :23; ai-usage :29 last
cat ~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf    # gaps_out=0 gaps_in=0 border_size=0 rounding=0
find ~/.local/share/omarchy/default/hypr -type f | wc -l                     # 35
find ~/.local/share/omarchy/default/hypr -type f -exec wc -c {} + | tail -1  # 33830 total
sed -n '9,18p' ~/.config/hypr/hypridle.conf                    # 150 s / 152 s chain
sed -n '9,10p' ~/.config/hypr/monitors.conf                    # GDK_SCALE=1; DP-1 3440x1440@100
ls -la ~/.config/mako/config; readlink -f ~/.config/mako/config; wc -lc ~/.config/mako/config  # symlink→theme/mako.ini; 5 L 119 B
```

R.2.3 — bind sources, rule census, walker.desktop:

```bash
for f in ~/.config/hypr/bindings.conf \
         ~/.local/share/omarchy/default/hypr/bindings/{media,clipboard,tiling-v2,utilities}.conf; do
  printf '%3s  %s  %s\n' "$(grep -c '^bind' "$f")" "$(sha256sum "$f" | cut -c1-16)" "$f"; done
# expect 25/e574a1ed08535e31 · 23/8d21d57e9d982b01 · 4/19ca281aae91a7db · 90/0cca56696969a0f3 · 50/57ddb3045f81d693
sha256sum ~/.local/share/omarchy/default/hypr/windows.conf ~/.local/share/omarchy/default/hypr/apps.conf
# 45b1e465… / 1a5482bb… (prefixes = R2-2 pins)
echo "windows.conf: $(grep -cE '^(window|layer)rule' ~/.local/share/omarchy/default/hypr/windows.conf)"   # 4
tot=0; for f in ~/.local/share/omarchy/default/hypr/apps/*.conf; do case "$f" in *davinci*) continue;; esac
  n=$(grep -cE '^(window|layer)rule' "$f"); tot=$((tot+n)); done
echo "18 sourced app files: $tot"                              # 69 (incl. 2 layerrules)
grep -c '^windowrule' ~/.config/hypr/input.conf                # 2
grep -c '^windowrule' ~/.config/hypr/ai-usage.conf             # 4
sha256sum ~/.config/autostart/walker.desktop ~/.local/share/omarchy/default/walker/walker.desktop   # both 5cb9874e…

# backups (F7) and terminal-plane residue (§5):
ls -la ~/.config/waybar/ | grep -c '\.bak'           # waybar backups: 4
wc -c ~/.config/hypr/*.bak.* ~/.config/waybar/*.bak* ~/.config/alacritty/*.bak.* ~/.config/foot/*.bak.* ~/.config/kitty/*.bak.* ~/.config/ghostty/*.bak.*
# expect 65 | 5892 5114 1458 1458 | 873 513 953 1322 (+ totals)
for t in alacritty/alacritty.toml foot/foot.ini kitty/kitty.conf ghostty/config; do
  d=$HOME/.config/$t; b=$(ls $HOME/.config/${t%/*}/*.bak.* 2>/dev/null | head -1)
  echo "--- $t vs $(basename "$b")"; diff "$b" "$d" || true; done   # one hunk per file: font size 9 → 12.5
head -5 ~/.config/xdg-terminals.list                 # first entry Alacritty.desktop
wc -c ~/.local/share/applications/footclient.desktop ~/.local/share/applications/foot-server.desktop   # 28 / 28
ls ~/.config/omarchy/hooks/                          # 5 dirs: battery-low.d font-set.d post-boot.d post-update.d theme-set.d
wc -c ~/.config/omarchy/current/theme.name; cat ~/.config/omarchy/current/theme.name   # 12; matte-black
grep -cE '#(121212|bebebe|eaeaea|515151|333333|D35F5F|e68e0d)' ~/.config/omarchy/current/theme/alacritty.toml   # 20
```

### R.3 Pass 2 — hyprctl live + the 57-row getoption check `[CFG]`

R.3.1 — read verbs and their parses (commands as validated 16:24 UTC):

```bash
hyprctl version | head -2                      # 0.56.2, commit efb5099…, clean
hyprctl configerrors; echo "rc=$?"             # empty output; rc=0
hyprctl -j instances > "$D/instances.json"
python3 -c "import json;d=json.load(open('$D/instances.json'));print('instances:',len(d));print(d[0]['wl_socket'])"   # 1; "wayland-1" (F8)
hyprctl -j monitors | python3 -c "import json,sys;[print(m['name'],f\"{m['width']}x{m['height']}\",'refresh',m['refreshRate'],'at',f\"{m['x']}x{m['y']}\",'scale',m['scale'],'|',m['description']) for m in json.load(sys.stdin)]"   # DP-1 3440x1440 refresh 99.997 (F5)
hyprctl -j workspaces > "$D/workspaces.json"
python3 -c "import json;d=json.load(open('$D/workspaces.json'));print('n=',len(d));[print('id',w['id'],'name',w['name'],'monitor',w['monitor'],'windows',w['windows']) for w in d]"   # [EPOCH]
hyprctl -j activeworkspace | python3 -c "import json,sys;w=json.load(sys.stdin);print('id',w['id'],'name',w['name'],'windows',w['windows'])"
hyprctl -j clients > "$D/clients.json"
python3 -c "import json;d=json.load(open('$D/clients.json'));print('n=',len(d));[print('class',c.get('class'),'pid',c.get('pid'),'tags',c.get('tags')) for c in d]"   # F2: tags only, no titles
hyprctl -j devices > "$D/devices.json"
python3 -c "import json,collections;d=json.load(open('$D/devices.json'));k=d.get('keyboards',[]) or [];print('keyboards:',len(k));print('keymaps:',dict(collections.Counter(x.get('active_keymap') for x in k)));print('layouts:',dict(collections.Counter(x.get('layout') for x in k)));print('touch:',len(d.get('touch',[]) or []),'mice:',len(d.get('mice',[]) or []))"   # F9
hyprctl -j binds > "$D/binds.json"
python3 - <<PY
import json, collections
d=json.load(open("$D/binds.json"))
print('n=',len(d))
print('has_description',sum(1 for b in d if b['has_description']),'repeat',sum(1 for b in d if b['repeat']),'locked',sum(1 for b in d if b['locked']),'mouse',sum(1 for b in d if b['mouse']),'release',sum(1 for b in d if b['release']))
print('modmask',dict(sorted(collections.Counter(b['modmask'] for b in d).items())))
print('submap',set(b['submap'] for b in d),'catch_all',sum(1 for b in d if b['catch_all']))
c=collections.Counter(b['dispatcher'] for b in d)
print('dispatchers n=%d'%len(c)); print(dict(sorted(c.items(), key=lambda kv:(-kv[1],kv[0]))))
PY
# expect: n=192; flags 190/14/26/2/1; modmask {0:23,1:2,8:7,9:2,12:2,13:1,64:42,65:37,68:26,69:3,72:19,73:22,76:6}; submap {''}; catch_all 0
# expect dispatchers n=24: {exec:104, workspace:15, changegroupactive:11, movetoworkspacesilent:11, movetoworkspace:10,
#   movecurrentworkspacetomonitor:4, movefocus:4, moveintogroup:4, resizeactive:4, swapwindow:4, sendshortcut:3,
#   bringactivetotop:2, cyclenext:2, focusmonitor:2, fullscreen:2, mouse:2, fullscreenstate:1, killactive:1, layoutmsg:1,
#   moveoutofgroup:1, pseudo:1, togglefloating:1, togglegroup:1, togglespecialworkspace:1}
#   (§2.3 prose says "four ×4 … seven ×2"; live and R2-2 §3 are five ×4 / five ×2 — see §R.6 D4)
hyprctl -j animations > "$D/animations.json"
python3 - <<PY
import json
d=json.load(open("$D/animations.json"))
print('entries',len(d[0]),'overridden',sum(1 for a in d[0] if a.get('overridden')))
print('beziers',sorted(c['name'] for c in d[1]))
PY
# expect: entries 35 overridden 19; beziers ['almostLinear','default','easeInOutCubic','easeOutQuint','linear','quick']
# shape note: the JSON is a 2-element list — [entries[], beziers[]] (D2)
hyprctl -j layers > "$D/layers.json"
python3 - <<PY
import json
d=json.load(open("$D/layers.json"))
for mon,info in d.items():
    for lvl,arr in sorted(info.get('levels',{}).items()):
        for e in arr: print(mon,'level',lvl,'ns',e.get('namespace'),'pid',e.get('pid'),'geom',f"{e.get('w')}x{e.get('h')}")
PY
# expect: DP-1 level 0 ns wallpaper; DP-1 level 2 ns waybar geom 3440x26
sig=$(python3 -c "import json;print(json.load(open('$D/instances.json'))[0]['instance'])")
ls -la "/run/user/$(id -u)/hypr/$sig/"   # .socket.sock .socket2.sock (srwx) + hyprland.lock  [EPOCH dir]
```

R.3.2 — the 57-row expectation table. Save as `$D/expected.tsv` (format
`option|kind|value|set|class`; class = round-2 claim, `extra` = R2-2 §5):

```
# expected live values — R2-1 §3 (56 getoption pairs) + R2-2 §5 extra (rounding_power)
# cols: option|kind|value|set(optional)|class(round-2 claim; 'extra'=R2-2 §5)
general:gaps_in|custom|0 0 0 0|true|agreement*
general:gaps_out|custom|0 0 0 0|true|agreement*
general:border_size|int|0|true|agreement*
general:col.active_border|custom|ffe68e0d 45deg|true|agreement*
general:col.inactive_border|custom|aa595959 0deg|true|agreement
general:resize_on_border|int|0|true|agreement
general:allow_tearing|int|0|true|agreement
general:layout|str|dwindle|true|agreement
general:snap:enabled|int|0|false|live-default
decoration:rounding|int|0|true|agreement
decoration:shadow:enabled|int|1|true|agreement
decoration:shadow:range|int|2|true|agreement
decoration:shadow:render_power|int|3|true|agreement
decoration:shadow:color|custom|ee1a1a1a 0deg|true|agreement
decoration:blur:enabled|int|1|true|agreement
decoration:blur:size|int|2|true|agreement
decoration:blur:passes|int|2|true|agreement
decoration:blur:special|int|1|true|agreement
decoration:blur:brightness|float|0.6|true|agreement
decoration:blur:contrast|float|0.75|true|agreement
decoration:dim_inactive|int|0|false|live-default
animations:enabled|int|1|true|agreement
dwindle:preserve_split|int|1|true|agreement
dwindle:force_split|int|2|true|agreement
scrolling:column_width|float|0.49|true|agreement
master:new_status|str|master|true|agreement
group:col.border_active|custom|ffe68e0d 45deg|true|agreement*
group:groupbar:font_size|int|12|true|agreement
group:groupbar:height|int|22|true|agreement
group:groupbar:gaps_in|int|5|true|agreement
misc:disable_hyprland_logo|int|1|true|agreement
misc:focus_on_activate|int|1|true|agreement
misc:anr_missed_pings|int|3|true|agreement
misc:on_focus_under_fullscreen|int|1|true|agreement
misc:key_press_enables_dpms|int|1|true|agreement
misc:mouse_move_enables_dpms|int|1|true|agreement
cursor:hide_on_key_press|int|1|true|agreement
cursor:warp_on_change_workspace|int|1|true|agreement
binds:hide_special_on_workspace_change|int|1|true|agreement
input:kb_layout|str|br|true|agreement*
input:kb_variant|str||true|agreement
input:kb_model|str||true|agreement
input:kb_options|str|compose:caps|true|agreement
input:kb_rules|str||true|agreement
input:follow_mouse|int|1|true|agreement
input:sensitivity|float|0.0|true|agreement
input:accel_profile|str|[[EMPTY]]|false|live-default
input:touchpad:natural_scroll|int|0|true|agreement
input:touchpad:clickfinger_behavior|int|1|true|agreement
input:touchpad:scroll_factor|float|0.4|true|agreement
input:touchpad:disable_while_typing|int|1|false|live-default
input:repeat_rate|int|40|true|agreement
input:repeat_delay|int|250|true|agreement
input:numlock_by_default|int|1|true|agreement
xwayland:force_zero_scaling|int|1|true|agreement
ecosystem:no_update_news|int|1|true|agreement
decoration:rounding_power|float|2.0|false|extra
```

R.3.3 — loop + checker:

```bash
awk -F'|' '!/^#/ && NF>=3 {print $1}' "$D/expected.tsv" > "$D/options.list"   # must print $1 unescaped (D1)
while IFS= read -r opt; do
  safe=$(printf '%s' "$opt" | tr ':' '_')
  out=$(hyprctl -j getoption "$opt" 2>&1) || { echo "GETOPTION FAILED: $opt :: $out" >> "$D/getoption-failures.txt"; continue; }
  printf '%s' "$out" > "$G/$safe.json"
done < "$D/options.list"
echo "getoption files: $(ls "$G" | wc -l) / expected: $(wc -l < "$D/options.list")"   # expect 57 / 57
```

```bash
python3 - <<'PY'
import json, os
D = os.environ.get('D', '/tmp/w4-repro')
G = os.path.join(D, 'getoption')
rows = []
for line in open(os.path.join(D, 'expected.tsv')):
    line = line.rstrip('\n')
    if not line or line.startswith('#'): continue
    parts = line.split('|')
    rows.append((parts[0], parts[1], parts[2],
                 parts[3] if len(parts) > 3 else '-',
                 parts[4] if len(parts) > 4 else '-'))
print(f"options in expected.tsv: {len(rows)}")
fail = 0; census = {}
with open(os.path.join(D, 'getoptions-measured.tsv'), 'w') as fh:
    for opt, kind, val, setexp, cls in rows:
        fn = os.path.join(G, opt.replace(':', '_') + '.json')
        if not os.path.exists(fn): print('MISSING', opt); fail += 1; continue
        d = json.load(open(fn)); got = d.get(kind)
        if kind == 'int':   ok = got is not None and int(got) == int(val)
        elif kind == 'float': ok = got is not None and abs(float(got) - float(val)) < 1e-9
        else: ok = str(got) == val
        s = 'set' if d.get('set') else 'unset'
        want = {'true': 'set', 'false': 'unset', '-': '-'}.get(setexp, setexp)
        sok = want == '-' or want == s
        if not (ok and sok): fail += 1; print('MISMATCH', opt, '| exp', repr(val), setexp, '| got', repr(got), s)
        census[cls] = census.get(cls, 0) + 1
        fh.write(f"{opt}\t{kind}\t{got}\t{s}\t{cls}\n")
print('class census of the re-checked set:', dict(census))
print(f"checked {len(rows)}; mismatches/missing: {fail}")
PY
# expect: options in expected.tsv: 57
#         class census of the re-checked set: {'agreement*': 6, 'agreement': 46, 'live-default': 4, 'extra': 1}
#         checked 57; mismatches/missing: 0
```

### R.4 Pass 3 — consumers `[CFG]`/`[EPOCH]`

```bash
ps -eo pid,lstart,etimes,comm,args | grep -E '/waybar|/mako|walker|swayosd|hypridle|hyprlock' | grep -v grep   # [EPOCH]
pgrep -x hypridle || echo 'pgrep hypridle: no match'       # F1 (E3: state unstable post-turnover)
pgrep -x hyprlock || echo 'no match'; pgrep -x hyprsunset || echo 'no match'
systemctl --user is-active hypridle; systemctl --user is-enabled hypridle   # inactive; disabled
journalctl --user -u hypridle --no-pager -n 15 2>&1 | tail -3               # -- No entries --
journalctl --user -b --no-pager 2>/dev/null | grep -i hypridle | tail -20  # start line(s); NO stop line
pgrep -af 'xdg-desktop-portal-hyprland' | head -3          # [EPOCH]
for u in app-walker@autostart.service elephant.service; do echo "$u : active=$(systemctl --user is-active $u) enabled=$(systemctl --user is-enabled $u)"; done   # active/generated; active/enabled
makoctl mode                                                # default
busctl --user status org.freedesktop.Notifications 2>&1 | grep -E 'Name=|PID=|UniqueName='   # [EPOCH]
mako --version; echo "rc=$?"                                # F10: rc=1; stderr 'unrecognized option' + 'Failed to parse config'
waybar --version; walker --version; swayosd-server --version; hyprlock --version   # v0.15.0 / 2.17.0 / 0.3.2 / v0.9.6
omarchy version; omarchy theme current                      # 3.8.3 / Matte Black
for c in hyprctl alacritty foot kitty ghostty waybar walker mako makoctl swayosd-client elephant jq; do printf '%-15s ' "$c"; command -v "$c" || echo 'NOT FOUND'; done   # F6: only alacritty; jq = ~/.local/bin/jq
printf 'GDK_SCALE=%s\n' "$(printenv GDK_SCALE || echo UNSET)"   # 1
for v in NVD_BACKEND LIBVA_DRIVER_NAME __GLX_VENDOR_LIBRARY_NAME; do printf '%s=%s\n' "$v" "$(printenv "$v" || echo UNSET)"; done   # F3: UNSET ×3
grep -rn 'envs.conf' ~/.config/hypr/ ~/.local/share/omarchy/default/hypr/ ~/.local/state/omarchy/toggles/ 2>/dev/null   # only hyprland.conf:9 → default
grep -E '^env = ' ~/.local/share/omarchy/default/hypr/envs.conf | while IFS= read -r line; do name=$(printf '%s' "$line" | sed 's/^env = //' | cut -d, -f1); if printenv "$name" >/dev/null 2>&1; then echo "$name=SET"; else echo "$name=UNSET"; fi; done   # 12× SET
grep -n '"signal"' ~/.config/waybar/config.jsonc            # :66/:203/:209/:215/:239
grep -rn 'RTMIN' ~/.local/share/omarchy/bin/ | head -20     # RTMIN+7…+11 producers
grep -n 'a55555' ~/.config/waybar/style.css                 # :96/:101/:110/:135
lspci -nn 2>/dev/null | grep -iE 'vga|3d|display'           # F3 hardware: RTX 5070 GB205 + AMD Granite Ridge
ls -la ~/.local/share/grok-bot/ 2>/dev/null; readlink -f ~/.local/share/grok-bot/appimage
stat -c '%s %y' /home/vgpnk/Applications/Grok_Bot_0.70.2.AppImage 2>/dev/null || echo 'target stat failed'   # F4: 134596858 B, 2026-10-13 22:29:16
ps -eo pid,comm,args | grep -iE 'grok|Grok_Bot|appimage' | grep -v grep || echo 'no grok-bot process'   # F4
omarchy menu keybindings --print 2>/dev/null | grep -iE 'space|launch apps' | head -6   # SUPER+SPACE → Launch apps; SUPER ALT+SPACE → Omarchy menu (R2-E2)
grep -n 'width-request' ~/.local/share/omarchy/default/walker/themes/omarchy-default/layout.xml   # :15 → 644
wc -lc ~/.local/share/omarchy/default/walker/themes/omarchy-default/style.css ~/.local/share/omarchy/default/walker/themes/omarchy-default/layout.xml   # 121/1243; 156/6488
waybar --help 2>&1 | head -12                               # anti-claim: launch flags only, no query verb
```

### R.5 Finding-by-finding verdict table + gates

| F | class | check (pass) | expected shape (R3 / kit) | re-run verdict rule |
|---|---|---|---|---|
| F1 | S1 | `pgrep -x hypridle`; unit status; journal (R.4) | no match; `inactive`/`disabled`; `-u hypridle` "No entries"; session journal: start line(s), **no stop line** | absent → REPRODUCED. Present → STATE-MOVED: require a current-session start line; E3 documents the present 16:11–~16:22 / absent from ~16:23:19 cycle — expect either; do not fail |
| F2 | S2 | `hyprctl -j clients` tags (R.3) | Alacritty windows carrying `default-opacity*`: R3 2/3; kit 2/2 | any current window flagged → REPRODUCED; all clean → record window set; NOT-REPRODUCED-as-of-now (window-state caveat, §6 F2) |
| F3 | S2 | env trio + sourcer grep + `lspci` (R.4) | 3× UNSET; grep hits only `hyprland.conf:9`; RTX 5070 present | all three → REPRODUCED |
| F4 | S3 | grok-bot scan + `ls`/`stat` (R.4) | no process; symlink present; target 134,596,858 B mtime 2026-10-13 22:29:16 | no process + target present → REPRODUCED |
| F5 | S3 | `hyprctl -j monitors` refreshRate (R.3) | `99.997` (declared `@100`; nominal class) | equal → REPRODUCED |
| F6 | S3 | `command -v` sweep (R.4) | only `alacritty`; foot/kitty/ghostty NOT FOUND | same → REPRODUCED |
| F7 | S3 | backup listings + `wc -c` (R.2.3/R.4) | hypr 1 (65 B); waybar 4; terminals 4 = 873/513/953/1322 B | same set → REPRODUCED |
| F8 | S3 | `hyprctl -j instances` (R.3) | key `wl_socket` = `"wayland-1"`; no `wlSocket` key | equal → REPRODUCED (closure applied, E4) |
| F9 | S3 | `hyprctl -j devices` (R.3) | keyboards 9, all `Portuguese (Brazil)` / `br`; touch 0; mice 4 | keymaps all `br`; record count (hotplug-sensitive; R2-1 saw 8) → REPRODUCED |
| F10 | S3 | `mako --version` + owner + `makoctl mode` (R.4) | rc=1; stderr 2 lines; `mako --help` clean; owner PID live; mode `default` | rc=1 + 2 lines + daemon healthy → REPRODUCED |

**Gates.** `P1` 29/29 pins OK and the stock-6 shas match (any miss ⇒ DRIFT:
stop, record, do not repair). `P2` `configerrors` empty rc=0; getoptions
`checked 57; mismatches/missing: 0`; binds 192 with flags 190/14/26/2/1,
modmask histogram equal, 24 dispatchers; animations 35/19/6; sources 17;
rules 4+69+2+4; bind sources 25+23+4+90+50. `P3` every F1–F10 judged per
the table. **Box-3 criterion:** "R3 pass reproduces" iff P1+P2 clean and
every finding is REPRODUCED or STATE-MOVED with a documented move (E3
class).

### R.6 Kit-validation receipts and faults (round 4)

- **K1 — pre-turnover dry run, 16:07 UTC.** The three author probe scripts
  (copies; scratch `/tmp/mado-r4-4-repro/`, ephemeral) ran rc=0: filebytes
  317 L, hyprctl 68 L, consumers 259 L; getoption checker `checked 57;
  mismatches/missing: 0`; hypridle absent; portal PID 1920 — the old-session
  state matching R3 (§11.1–§11.3).
- **K2 — this kit's runs, 16:21/16:24 UTC** (post-turnover, E3). Sequential
  consolidated runner (as found sha256 `70dff755…`; corrected `389a1bb7…`;
  scratch `/tmp/w4-m4-1-repro/`): pins **29/29 OK**; getoption files **57/57**
  and `checked 57; mismatches/missing: 0`; census `{agreement*: 6,
  agreement: 46, live-default: 4, extra: 1}`; binds 192, flags and modmask
  equal to §2.3/Appendix A; animations 35/19/6; devices 9 br; clients 2/2
  F2-flagged; `configerrors` rc=0.
- **K3 — faults found while validating (all corrected in the commands
  above).** D1: the consolidated runner as found over-escaped the awk field
  (`{print \$1}`) — screenshot symptom: `awk: … backslash not last character
  on line`, `getoption files: 0 / expected: 0`, checker `checked 57;
  mismatches/missing: 57` (all MISSING). D2: it assumed `hyprctl -j
  animations` was a flat row list; the JSON is `[35 entries, 6 beziers]`
  and the naive parse raises `AttributeError: 'list' object has no
  attribute 'get'`. D3: its pin comparator held the 16-char prefix
  `5cb9874eedbcb32c` as a full-sha target → false `PIN-DIFF` on
  `walker.desktop` though both files hash
  `5cb9874eedbcb32c7b121ea60f6433f881499247cac7e6473a9a93adeebc3aa7`. D4
  (note text, unfiled): §2.3 renders the dispatcher tail as "four ×4 …
  seven ×2"; live (16:21Z and 16:24Z) and R2-2 §3 both give **five ×4**
  (`movecurrentworkspacetomonitor`, `movefocus`, `moveintogroup`,
  `resizeactive`, `swapwindow`) and **five ×2** (`bringactivetotop`,
  `cyclenext`, `focusmonitor`, `fullscreen`, `mouse`); the printed split
  also implies 25 groups vs the measured 24. Erratum candidate; not applied
  (write scope = this block).
- **K4 — turnover cross-reference.** Session replacement and hypridle #2
  are recorded in E3; this kit's independent witnesses: hypridle running in
  the consumer pass at 16:21:02 UTC (`etimes` 593) and gone at 16:24:08 UTC
  (repeated `pgrep -x hypridle` rc=1), between E3's 16:21:49 present /
  16:23:19 absent bounds; scope `…-87ed9048.scope` collected. Stop cause
  and restart cause `[UNK]` read-only (no `hyprland.log` reads).

### R.7 `[EPOCH]` values — expect these to differ; record, never fail

- All PIDs (waybar/mako/walker/swayosd/hypridle present-or-absent/portal/
  clients): §2–§4 hold the pre-turnover set; E3 holds the current one.
- Instance signature + `time` + `/run/user/1000/hypr/<sig>/` (old and new
  dirs both exist) + `.socket*` mtimes.
- Window set and per-workspace window counts (R3: 3 windows; kit: 2) — F2
  tags are judged on whatever windows exist.
- Keyboard/device counts (F9; hotplug) and monitor refresh quantization
  (F5; mode negotiation). Journal timestamps; service states; D-Bus
  owner/`UniqueName`; `ps` `lstart`.

### R.8 Limits (what a read-only pass cannot settle)

- No rule-read verb: whether any window rule currently *matches* a window
  stays unproven (§8 U6); dispatcher semantics are static, none fired.
- Waybar exposes no query verb (anti-claim): its live internals stay
  file-byte + compositor-view class. Lock cycle not triggered (read-only);
  grok-bot's real error would need a launch.
- F2 root cause, hypridle stop cause, and the turnover cause are outside
  read-only reach; E3/K4 keep them `[UNK]`. Reviewer must not run mutating
  verbs or the idle toggle; F1 re-arming stays operator-side (§7).
- Pins drift ⇒ "not reproduced" for byte-identity; escalate to the lane —
  never silently adopt new values.