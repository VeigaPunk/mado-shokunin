# hyprctl verification layer — live mapping of the config plane (MADO-R2-1)

Probe window: 2026-10-14 13:45:42–13:49:35 UTC (host offset −03:00). Host user `vgpnk`.
Substrate read-only: `~/.config/hypr/`, `~/.local/share/omarchy/default/hypr/`,
`~/.local/state/omarchy/toggles/hypr/`, `~/.config/omarchy/current/theme/`.
Tool: `/usr/bin/hyprctl`, owned by package `hyprland 0.56.2-2`. Round-1 parent:
`hyprland-config-plane.md` (MADO-1) — this note is its live-verification layer.
Tags: `[OBS]` measured directly · `[INF]` inference from measured parts · `[UNK]` unknown.

## 0. Scope and write discipline

- Read verbs used, exhaustive: `getoption` (56 distinct options), `monitors`,
  `workspaces`, `activeworkspace`, `clients`, `binds`, `animations`, `devices`,
  `instances`, `configerrors`, `version`.
- Mutating verbs never invoked: `keyword`, `dispatch`, `reload`, `setprop`,
  `setcursor`, `output`, `notify`, `plugin`, `batch`, `--instance` overrides.
- No file outside this repo was written. Config-tree `sha256sum` before and after
  the probe window equals MADO-1 §2 exactly (§7) — the substrate is byte-identical.
- Session material: no window titles read (`clients` used for its length only),
  `hyprland.log` listed shape-only and never content-read, no `/proc/*/environ`
  read. Env values cited below are non-secret driver names/values only.

## 1. Verdict — hyprctl is available and live in this session `[OBS]`

| Evidence | Measured |
|---|---|
| binary | `command -v hyprctl` → `/usr/bin/hyprctl`; `readlink -f` → same path (real file, not a symlink); `pacman -Qo /usr/bin/hyprctl` → owned by `hyprland 0.56.2-2` |
| version | `hyprctl version` L1 → `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs).` (build date 2026-08-05) |
| instance | `HYPRLAND_INSTANCE_SIGNATURE` set, shape `<commit>_<epoch>_<pid>` (shape only); one socket dir `/run/user/1000/hypr/<sig>/` |
| IPC surface | that dir contains `.socket.sock`, `.socket2.sock` (both `srwx`), `hyprland.lock`, `hyprland.log` (967,994 B, not read) |
| instances | `hyprctl -j instances` → one entry; its `wlSocket` field is `null` `[UNK]` why |
| load state | `hyprctl configerrors` → empty, rc=0; re-run after all probes → still empty |

Consequence: the live layer is measured, not merely documented; the recipe
branch (§8) is retained for sessions where this probe fails.

## 2. Method and classification

Include order (MADO-1 §3, re-read in `hyprland.conf`): defaults L4–12, theme L13,
local files L16–20, toggles glob L23, `ai-usage.conf` L29. The **last declarer
wins**. Every row states its declaring chain in that order; "resolved declarer" =
the last file that declares the option.

| Class | Falsifiable meaning |
|---|---|
| `agreement` | live `getoption` equals the resolved (last) declaration |
| `agreement*` | ditto, but an earlier declarer is shadowed — the live layer proves *which file owns the value* |
| `live-default` | no declarer in the effective chain; `set=false`; live = engine default |
| `mismatch` | live differs from the resolved declaration with no include-order/rounding explanation (`set=true`) — **0 instances in this probe** |
| `config-only` | declared, but hyprctl has no read surface for it (or another daemon consumes it) → static evidence only, live layer UNKNOWN |

`set` flag as discriminator `[OBS]`: `set=false` on exactly the four options no
file declares (`input:accel_profile`, `general:snap:enabled`,
`decoration:dim_inactive`, `input:touchpad:disable_while_typing`); `set=true` on
all 52 declared ones. `[INF]` its exact semantics ("assigned during load / differs
from built-in") are inferred from that correlation, not from documentation read
here.

Chain aliases: D-LF = `~/.local/share/omarchy/default/hypr/looknfeel.conf`;
D-IN = default `input.conf`; D-EN = default `envs.conf`; L-IN/L-MON/L-LF = local
`~/.config/hypr/{input,monitors,looknfeel}.conf`; T-WNG = enabled toggle
`~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf`;
TH = `~/.config/omarchy/current/theme/hyprland.conf`.
Lines marked `#` are commented declarations — inert, kept in the chain column to
show what the config plane conspicuously does *not* do.

## 3. Mapping table — 56 `getoption` claim→live pairs

Live values are verbatim from `hyprctl -j getoption <opt>` (`-j` renders
`custom`-type options under a `custom` key, not `str`).

### 3.1 general / decoration / animations / layouts / group / misc / cursor / binds (39 rows)

| Option | Declaring chain (last wins) | Live | set | Class |
|---|---|---|---|---|
| general:gaps_in | D-LF:9 = 5 → T-WNG:4 = 0 | `custom: 0 0 0 0` | true | agreement* |
| general:gaps_out | D-LF:10 = 10 → T-WNG:3 = 0 | `custom: 0 0 0 0` | true | agreement* |
| general:border_size | D-LF:12 = 2 → T-WNG:5 = 0 | `int: 0` | true | agreement* |
| general:col.active_border | D-LF:15 = `rgba(33ccffee) rgba(00ff99ee) 45deg` → TH:4 = `rgb(e68e0d)` | `custom: ffe68e0d 45deg` | true | agreement* |
| general:col.inactive_border | D-LF:16 = `rgba(595959aa)` | `custom: aa595959 0deg` | true | agreement (notation) |
| general:resize_on_border | D-LF:19 = false | `int: 0` | true | agreement |
| general:allow_tearing | D-LF:22 = false | `int: 0` | true | agreement |
| general:layout | D-LF:24 = dwindle; L-LF:11 `# layout = scrolling` (inert) | `str: dwindle` | true | agreement |
| general:snap:enabled | — no declarer | `int: 0` | false | live-default |
| decoration:rounding | D-LF:29 = 0 → T-WNG:9 = 0; L-LF:17 `# rounding = 8` (inert) | `int: 0` | true | agreement |
| decoration:shadow:enabled | D-LF:32 = true | `int: 1` | true | agreement |
| decoration:shadow:range | D-LF:33 = 2 | `int: 2` | true | agreement |
| decoration:shadow:render_power | D-LF:34 = 3 | `int: 3` | true | agreement |
| decoration:shadow:color | D-LF:35 = `rgba(1a1a1aee)` | `custom: ee1a1a1a 0deg` | true | agreement (notation) |
| decoration:blur:enabled | D-LF:40 = true | `int: 1` | true | agreement |
| decoration:blur:size | D-LF:41 = 2 | `int: 2` | true | agreement |
| decoration:blur:passes | D-LF:42 = 2 | `int: 2` | true | agreement |
| decoration:blur:special | D-LF:43 = true | `int: 1` | true | agreement |
| decoration:blur:brightness | D-LF:44 = 0.60 | `float: 0.600000` | true | agreement |
| decoration:blur:contrast | D-LF:45 = 0.75 | `float: 0.750000` | true | agreement |
| decoration:dim_inactive | L-LF:20 `# dim_inactive = true` (inert) | `int: 0` | false | live-default |
| animations:enabled | D-LF:82 = `yes, please :)` | `int: 1` | true | agreement (truthy string parse) |
| dwindle:preserve_split | D-LF:111 = true | `int: 1` | true | agreement |
| dwindle:force_split | D-LF:112 = 2 | `int: 2` | true | agreement |
| scrolling:column_width | D-LF:116 = 0.49 | `float: 0.490000` | true | agreement (inert under dwindle `[INF]`) |
| master:new_status | D-LF:121 = master | `str: master` | true | agreement (inert under dwindle `[INF]`) |
| group:col.border_active | D-LF:51 gradient pair → TH:8 = `rgb(e68e0d)` | `custom: ffe68e0d 45deg` | true | agreement* |
| group:groupbar:font_size | D-LF:57 = 12 | `int: 12` | true | agreement |
| group:groupbar:height | D-LF:64 = 22 | `int: 22` | true | agreement |
| group:groupbar:gaps_in | D-LF:65 = 5 | `int: 5` | true | agreement |
| misc:disable_hyprland_logo | D-LF:126 = true | `int: 1` | true | agreement |
| misc:focus_on_activate | D-LF:129 = true | `int: 1` | true | agreement |
| misc:anr_missed_pings | D-LF:130 = 3 | `int: 3` | true | agreement |
| misc:on_focus_under_fullscreen | D-LF:131 = 1 | `int: 1` | true | agreement |
| misc:key_press_enables_dpms | D-IN:19 = true | `int: 1` | true | agreement |
| misc:mouse_move_enables_dpms | D-IN:20 = true | `int: 1` | true | agreement |
| cursor:hide_on_key_press | D-LF:136 = true | `int: 1` | true | agreement |
| cursor:warp_on_change_workspace | D-LF:137 = 1 | `int: 1` | true | agreement |
| binds:hide_special_on_workspace_change | D-LF:142 = true | `int: 1` | true | agreement |

### 3.2 input (15 rows)

| Option | Declaring chain (last wins) | Live | set | Class |
|---|---|---|---|---|
| input:kb_layout | D-IN:3 = us → L-IN:10 = br | `str: br` | true | agreement* |
| input:kb_variant | D-IN:4 = (empty); L-IN:6 `# kb_variant = intl` (inert) | `str: (empty)` | true | agreement |
| input:kb_model | D-IN:5 = (empty) | `str: (empty)` | true | agreement |
| input:kb_options | D-IN:6 = `compose:caps` → L-IN:11 = `compose:caps # ,grp:alts_toggle` (comment inert; the grp:alts_toggle **not** active) | `str: compose:caps` | true | agreement |
| input:kb_rules | D-IN:7 = (empty) | `str: (empty)` | true | agreement |
| input:follow_mouse | D-IN:9 = 1 | `int: 1` | true | agreement |
| input:sensitivity | D-IN:11 = 0; L-IN:21 `# sensitivity = 0.35` (inert) | `float: 0.000000` | true | agreement |
| input:accel_profile | L-IN:23–24 `# accel_profile = flat`, comment states default adaptive | `str: [[EMPTY]]` | false | live-default |
| input:touchpad:natural_scroll | D-IN:14 = false; L-IN:28 `# natural_scroll = true` (inert) | `int: 0` | true | agreement |
| input:touchpad:clickfinger_behavior | L-IN:31 = true | `int: 1` | true | agreement |
| input:touchpad:scroll_factor | L-IN:34 = 0.4 | `float: 0.400000` | true | agreement |
| input:touchpad:disable_while_typing | L-IN:37 `# disable_while_typing = false` (inert) | `int: 1` | false | live-default |
| input:repeat_rate | L-IN:14 = 40 | `int: 40` | true | agreement |
| input:repeat_delay | L-IN:15 = 250 | `int: 250` | true | agreement |
| input:numlock_by_default | L-IN:18 = true | `int: 1` | true | agreement |

### 3.3 options declared alongside env blocks (2 rows)

| Option | Declaring chain (last wins) | Live | set | Class |
|---|---|---|---|---|
| xwayland:force_zero_scaling | D-EN:24 = true | `int: 1` | true | agreement |
| ecosystem:no_update_news | D-EN:32 = true | `int: 1` | true | agreement |

Class census: 52 `agreement` (6 of them `agreement*` with a proven shadowed
declarer), 4 `live-default`, **0 `mismatch`**, plus `config-only` rows only in §6
(not getoption pairs). The zero-mismatch result is falsifiable: any live value
that starts differing from the §3 chain without a new declarer in the chain
breaks it.

## 4. Non-getoption claim→live pairs

| Claim (source) | Declared | Live (read verb) | Class |
|---|---|---|---|
| monitor mode (L-MON:10) | `DP-1, 3440x1440@100, 0x0, 1` | `hyprctl -j monitors` → DP-1 `3440x1440` @ `99.99700`, at `0x0`, scale `1`, desc `LG Electronics LG ULTRAWIDE 508AZFMF7323` | agreement (fresh rate reported as EDID-actual; 99.997 vs nominal 100 `[INF]`) |
| GDK_SCALE (L-MON:9) | `env = GDK_SCALE,1` | `printenv GDK_SCALE` → `1` (session shell; env surface, not hyprctl) | agreement |
| workspaces | no declarer anywhere (grep: only comments `hyprland.conf:26`, L-IN:48,50) | `hyprctl -j workspaces` → 1 workspace, id/name `1`, monitor DP-1, 3 windows | live-default (pure runtime state) |
| focused workspace | — | `hyprctl -j activeworkspace` → id 1, 3 windows; `hyprctl -j clients \| length` = 3 | consistent with MADO-1 §10 |
| binds (MADO-1 §4) | 23+4+90+50+25 = 192 | `hyprctl -j binds \| length` → `192` | agreement (surface: binds) |
| animations set (D-LF:86–90, 92–106) | 5 beziers + 15 `animation =` directives | `hyprctl -j animations` → 35 animation entries (19 `overridden: true`), 6 bezier entries incl. built-in `default` | agreement at count level; directive→entry expansion `[INF]` |
| keyboard layout (L-IN:10) | `kb_layout = br` | `hyprctl -j devices` → 8 keyboard nodes, all `active_keymap: Portuguese (Brazil)`, layout `br` | agreement (keymap-level, stronger than the string getoption) |
| version pin (MADO-1 §9) | package `hyprland 0.56.2-2` | `hyprctl version` L1 (commit `efb5099…`) | agreement |
| load diagnostics | — | `hyprctl configerrors` → empty | no config errors to report |

## 5. Include-order proof set (who owns the live value)

The live layer resolves *ownership*, not just values: in each row the live value
equals the last declarer and contradicts the earlier one, so the earlier file is
measurably shadowed.

| Option | Earlier declarer | Later declarer | Live | Verdict |
|---|---|---|---|---|
| general:gaps_in | D-LF:9 = 5 | T-WNG:4 = 0 | 0 0 0 0 | toggle owns |
| general:gaps_out | D-LF:10 = 10 | T-WNG:3 = 0 | 0 0 0 0 | toggle owns |
| general:border_size | D-LF:12 = 2 | T-WNG:5 = 0 | 0 | toggle owns |
| input:kb_layout | D-IN:3 = us | L-IN:10 = br | br | local file owns |
| general:col.active_border | D-LF:15 = gradient pair | TH:4 = `rgb(e68e0d)` | `ffe68e0d 45deg` | theme owns |
| group:col.border_active | D-LF:51 = gradient pair | TH:8 = `rgb(e68e0d)` | `ffe68e0d 45deg` | theme owns |

## 6. Config-only surface (declared, not observable through hyprctl reads)

| Surface | Declarations (anchors) | Why config-only | Live layer |
|---|---|---|---|
| window rules | L-IN:45–46 (2), `ai-usage.conf:2–5` (4), D-`windows.conf:3,6,9,15` (4) + `apps.conf` (18 sourced files) | no rule-read verb in 0.56 | static only; whether any rule currently matches an open window `[UNK]` |
| exec-once / autostart | local `autostart.conf` (5 L), D-`autostart.conf:1–9,12` (10) | startup-time only | process-table probes (MADO-1 §10 style), not hyprctl |
| env | D-EN:7–28 (12 vars), L-MON:9, orphan local `envs.conf:3–5` (3 vars) | no `getoption` surface | paired check: 12/12 sourced-file vars set in session env; `GDK_SCALE=1` matches; 3/3 orphan-file vars unset |
| include graph | `hyprland.conf:4–29` (17 `source`) | not enumerable | `configerrors` is the only load diagnostic |
| other-consumer configs | `xdph.conf` (portal), `hypridle.conf`, `hyprlock.conf`, `hyprsunset.conf` | consumed by other binaries (MADO-1 §8) | consumer-side probes only |
| commented monitor templates | L-MON:22,25–28 | inert | none expected; `monitors` shows only DP-1 |

New finding surfaced by the live env pair: **`~/.config/hypr/envs.conf` (133 B,
5 L) is sourced by nothing.** Root sources only the *default* envs.conf
(`hyprland.conf:9`); grep across `~/.config/hypr/`,
`~/.local/share/omarchy/default/hypr/` and the toggles dir finds no other
sourcer. Its three vars (`NVD_BACKEND,direct` :3, `LIBVA_DRIVER_NAME,nvidia`
:4, `__GLX_VENDOR_LIBRARY_NAME,nvidia` :5) are all unset in the session shell,
while all twelve vars declared in the sourced default envs.conf are set. It is
the same class as MADO-1 §4's `plain-bindings.conf` orphan.

## 7. Substrate unchanged (freshness check vs MADO-1 §2)

`sha256sum ~/.config/hypr/*.conf ~/.config/hypr/*.bak.*` (2026-10-14 13:49 UTC)
— first 12 hex of every file equal MADO-1 §2:

```
21e76af98ce7 ai-usage.conf    5ace17016fe2 autostart.conf    e574a1ed0853 bindings.conf
04af5cdf028b envs.conf        e7d3b8dd9835 hypridle.conf     4f52854a3c14 hyprland.conf
b8d173dcff55 hyprlock.conf    3042e4a92303 hyprsunset.conf   3769c92ab766 input.conf
777a4fdc8b61 looknfeel.conf   69c9d8996dfd monitors.conf     2fded88a27b8 xdph.conf
8b472371e78b autostart.conf.bak.1791942509
```

Therefore MADO-1 §7's override map and this live layer describe the same bytes;
every §3.1/§3.2 shadowing claim re-verifies MADO-1 §7 (gaps 0/0, border 0,
rounding 0, dwindle, br, animations on) plus MADO-1 §4 (192 binds) and §10
(DP-1 @ 0x0 scale 1, workspace 1, 3 windows).

## 8. Recipe for a session without a working hyprctl (anti-claim branch)

Run in order; if any fail condition holds, mark the live layer UNKNOWN and fall
back to file-byte evidence of the MADO-1 kind.

```
command -v hyprctl                                    # expect /usr/bin/hyprctl
printenv HYPRLAND_INSTANCE_SIGNATURE | cut -c1-12     # shape check; do not print in full
ls -la /run/user/$(id -u)/hypr/*/ | grep -E 'socket'  # expect .socket.sock + .socket2.sock
hyprctl -j instances                                  # expect exactly one instance
hyprctl version                                       # expect 0.56.2
hyprctl -j getoption <option>                         # once per §3 row
hyprctl -j monitors; hyprctl -j workspaces; hyprctl -j activeworkspace
hyprctl configerrors                                  # expect empty
```

Fail conditions → live layer UNKNOWN: no binary; no signature and no socket dir
with `.socket.sock`; `hyprctl` cannot connect; more than one instance and the
target is ambiguous (do not guess with `--instance`; resolve via the running
session's own signature). Fallback evidence: `wc`/`stat`/`sha256sum`/`grep`
anchors as in MADO-1 §2–9. Never send `keyword`, `dispatch`, `reload`, `setprop`,
`setcursor`, `output`, `plugin`, `batch` — this layer is read-only by design.

## 9. Errata (append-only — add blocks, never edit above)

- E1 (2026-10-14, MADO-R2-1): seed, no corrections to this note yet.
- Erratum candidate for MADO-1 (write scope here is this file only, so not
  applied): MADO-1 §4's unsourced-file list omits `~/.config/hypr/envs.conf`,
  which nothing sources (§6) and whose three env vars are measurably absent from
  the live session. For MADO-1 §11 by the integrator or next round, per the
  append-only rule. Minor: MADO-1 §3's sentence "local files (L16–20)" already
  implies the omission — this is an addition, not a contradiction.

## 10. Unknowns `[UNK]`

1. `set` field semantics: inferred from correlation (false exactly where no
   declarer). If it instead means "differs from built-in", the live-default
   classification still holds, but attribution precision is limited.
2. `general:col.active_border` live `ffe68e0d 45deg`: alpha `ff` matches theme
   `rgb()` `[INF]`; why the angle `45deg` survives a single-color assignment is
   unverified.
3. Monitor `99.99700` vs declared `100`: treated as EDID nominal quantization
   `[INF]`; EDID/pixel clock not read.
4. Window rules: whether any currently matches an open window cannot be read in
   0.56; rule-effect tests would need a mutation-free simulation we did not have.
5. Provenance of the orphan `~/.config/hypr/envs.conf`: who wrote it and why is
   untraced; `migrations/1770159912.sh` also names these vars (file names only,
   content not read).
6. `hyprland.log` (967,994 B) is session material and was never content-read; it
   could explain items 1–5.
7. Why `instances` reports `wlSocket: null` in 0.56.2 — unverified.
8. Whether the NVIDIA-driver vars in the orphan file matter on this host's GPU —
   hardware not probed.

## 11. Spot-checks (reproducible)

1. `hyprctl getoption general:gaps_in` → `custom type: 0 0 0 0` + `set: true` —
   toggle-owned, while the default file declares 5 (§3.1, §5).
2. `hyprctl -j binds | jq length` → `192` — matches MADO-1 §4's five-file sum.
3. `sha256sum ~/.config/hypr/hyprland.conf` →
   `4f52854a3c143dcf58430a679e339619223d2b5008115a322d06b2de637ea462`
   — equals MADO-1 §2, so the layer describes the same bytes.
4. `printenv GDK_SCALE` → `1` (matches L-MON:9); `printenv NVD_BACKEND` →
   unset (orphan `envs.conf`, §6).
5. `hyprctl -j monitors | jq '.[0].refreshRate'` → `99.997` vs declared `100`
   (§4) — the one numeric delta in the probe, classed as nominal rounding.

## Errata (round 4) — appended 2026-10-14 (ERR-M)

Append-only block; §9's entries above stand unedited. Written by the round-4
errata sweep; read-only probes 2026-10-14 16:20–16:25 UTC (scratch
`/tmp/w4-err-m-sweep/`). Context: the compositor instance was replaced at
~16:11:06–07 UTC; live values below are from the current instance (exactly one
— `hyprctl -j instances`).

- **E2 (closure).** §9's MADO-1 candidate (orphan `envs.conf` omitted from
  MADO-1 §4's unsourced list) was applied in round 2 as MADO-1's R2-E1 block
  (`hyprland-config-plane.md`, "Errata (round 2)" R2-E1, MADO-R2-3). The
  "for the integrator or next round" line is superseded by that application;
  record closed.
- **E3 (record correction — F8, forwarded by MADO-R3-2).** §1's instances row
  records "its `wlSocket` field is `null`" — **does not reproduce** on 0.56.2
  and is corrected: the entry's keys are exactly `instance`, `pid`, `time`,
  `wl_socket` (no camelCase `wlSocket` key at all), with `wl_socket` =
  `"wayland-1"` (string; re-measured; `pid` 1203316, `time` 1791994267 =
  16:11:07 UTC). §10 U7 ("Why `instances` reports `wlSocket: null`") is
  superseded by this measurement. Forwarded via `config-health-report-r3.md`
  §6 F8 / §9; applied here by the sweep as its E3.