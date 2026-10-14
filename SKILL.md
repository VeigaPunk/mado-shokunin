---
name: mado-shokunin
description: Domain specialist — desktop & compositor craft. Rank: shonen (probation).
---

# mado-shokunin

desktop & compositor craft playbook — the Hyprland/waybar/walker/terminal config plane
and display behavior on this host. This document is the lane's operating manual: a fresh
agent holding only this file can run a **scoped config verification** end-to-end — pick a
claim or a plane, route it to its evidence class, stay inside the safety fence, classify
any divergence, and report with measured anchors. Every rule below carries a cited source;
nothing here is oral knowledge.

Tag legend: `[OBS]` measured directly (file bytes, command output) · `[INF]` composite
inference from measured parts · `[INF-docs]` inference from documentation (wiki / omarchy
skill text), not host-verified · `[UNK]` unknown. Observation / inference / unknown stay
separate at all times.

Version pins for all claims below: Hyprland 0.56.2 (commit `efb5099…`), waybar v0.15.0,
walker 2.17.0 (MADO-1 §9; MADO-2 §1; re-verified `hyprctl version`). Omarchy carries two
pins — name which one you mean: `omarchy version` → 3.8.3, while the checkout's
`git describe --tags` → v3.8.4 (branch `master`, clean; MADO-R3-1 §1/§8.4). Re-verify pins
before reusing a claim under a newer version — window-rule syntax in particular changes
between releases (omarchy skill:300-305).

## Standing rules

- Read-only substrates unless PROVINCE.md declares a write surface;
  detection-and-report for operator-owned remediation.
- Secrets shape-only, never content-read. Session material (window titles,
  `hyprland.log`, instance signatures) is shape-only too (MADO-R2-1 §0).
- Every claim: measured anchor (path:line, command output, evidence id).
  Observation / inference / unknown stay separate; a claim with only one anchored
  side is an UNK item, not a finding.
- Errata append-only; rejections kept.

## Config-plane map — who owns this key

`~/.config/hypr/hyprland.conf` is a pure orchestrator: 17 `source` statements, zero
settings of its own (29 lines; MADO-1 §1/§3). Include order *is* precedence — the last
file to set a key wins:

> defaults (`~/.local/share/omarchy/default/hypr/*`, `hyprland.conf:4-12`) → theme include
> (`:13`) → user files (`:16-20`) → toggles glob
> (`~/.local/state/omarchy/toggles/hypr/*.conf`, `:23`) → `ai-usage.conf` (`:29`)

Measured, not recited: `hyprctl getoption general:gaps_out` → `custom type: 0 0 0 0` —
owned by the *toggle* `window-no-gaps.conf`, not by user `looknfeel.conf` (wholly
comment-only) and not by the default (`gaps_out = 10`, default looknfeel:10). Same for
`hyprctl getoption input:kb_layout` → `str: br` (user `input.conf:10` over default `us`).
Both re-verified 2026-10-14; full chain in MADO-1 §7.

Layer write rules: the defaults tree is READ-ONLY forever (edits break `omarchy update`,
omarchy skill:41-47); user files under `~/.config/` are the operator's edit surface;
the toggles dir is tool-written (`omarchy toggle`); the theme dir is rewritten by
`omarchy theme set`. **mado writes none of them** (see Safe-probe).

### Who-owns-it table

| Intent | Owner file (operator's edit target) | Verify with (read-only) | Anchors |
|---|---|---|---|
| App/webapp keybinds | `~/.config/hypr/bindings.conf` (25 local `bindd`, overrides stock) | `omarchy menu keybindings --print`; `hyprctl binds -j` | MADO-1 §4 — 192 live = 23+4+90+50+25 (re-verified 192) |
| Re-binding an already-bound key | same file — `unbind = …` BEFORE the new `bind` | `omarchy menu keybindings --print` first, so the old binding is named | omarchy skill:272-286; MADO-1 §4 (no active unbind in the file today) |
| Monitor layout / scale / position | `~/.config/hypr/monitors.conf:10` (+ `GDK_SCALE` at `:9`) | `hyprctl monitors` — live DP-1 3440x1440@99.997; config declares @100 | MADO-1 §10 |
| Keyboard layout / repeat / touchpad | `~/.config/hypr/input.conf` (user overrides default input.conf) | `hyprctl getoption input:kb_layout` → `str: br` | MADO-1 §7; input.conf:10-18 |
| Local window rules (terminal scroll, usage-tray float) | `input.conf:45-46`; `ai-usage.conf:2-5` (sourced last, `hyprland.conf:29`) | file read + `hyprctl configerrors` (empty = clean) | MADO-1 §5, §9 |
| Global window rules | stock `default/hypr/windows.conf` + `apps.conf` (18 per-app files, `apps.conf:2-19`) | file reads; syntax era pinned at `windows.conf:2` ("Hyprland 0.53+") | MADO-1 §5 |
| Gaps / borders / rounding / animations / layout | default looknfeel + user looknfeel (comment-only here) + toggles | `hyprctl getoption general:gaps_out`, `decoration:rounding` | MADO-1 §6-7 |
| Autostart processes | `~/.config/hypr/autostart.conf:5` (grok-bot); default `autostart.conf:1` (hypridle) | `pgrep` | MADO-1 §8, §10 |
| Env vars (NVIDIA + GDK_SCALE) | `~/.config/hypr/monitors.conf:9` (effective); local `envs.conf:3-5` is an orphan — no `source` reaches it (`hyprland.conf:9` sources only the default envs.conf), its 3 vars unset | `printenv GDK_SCALE` → `1`; `printenv NVD_BACKEND` → unset | MADO-1 §2; MADO-R2-1 §4/§6 |
| Idle timings (150 s screensaver / 152 s lock; ≈302 s effective per the file's own reset rationale) | `~/.config/hypr/hypridle.conf:10,16` — separate consumer, NOT sourced by hyprland.conf | `systemctl --user is-active hypridle`; `pgrep -x hypridle` — no match at the round-3/4 probes; volatile: restarted with the 16:11Z session, absent again by 16:24Z, no stop line (F1, cause `[UNK]`) | MADO-1 §8/§10; MADO-2 §5; MADO-R3-2 §6 F1; MADO-R4-2 §3/§7 |
| Lock screen UI | `~/.config/hypr/hyprlock.conf` + theme `hyprlock.conf` | file read (fingerprint disabled at `:41-43`) | MADO-1 §8; MADO-2 §5 |
| Night light | `~/.config/hypr/hyprsunset.conf` (identity profile `:3-6`) | file read | omarchy skill:386 |
| Screen-share picker | `~/.config/hypr/xdph.conf:1-4` | file read | MADO-1 §8 |
| Bar layout / modules | `~/.config/waybar/config.jsonc`; needs `omarchy restart waybar` | read `config.jsonc:2` — style-only auto-reload | MADO-2 §2.1, §7 |
| Bar colors | theme `~/.config/omarchy/current/theme/waybar.css` (fg/bg only) | read it; hardcoded `#a55555` stays local in `style.css:96,101,110,135` | MADO-2 §2.5 |
| Launcher (theme, prefixes, providers) | `~/.config/walker/config.toml`; `omarchy restart walker` | file read | MADO-2 §3 |
| Notification silencing (DND) | Mako mode (`makoctl mode`); config `~/.config/mako/config:1-5` | `makoctl mode` → `default` | MADO-2 §2.4/§4 |
| Terminal font / padding / keybinds | per-terminal file (alacritty/foot/kitty/ghostty); colors via theme include; only Alacritty installed | `command -v <term>`; file read | MADO-3 §1-3, §5 |
| Theme & wallpaper (all apps) | `~/.config/omarchy/current/theme/` + `theme.name` + `current/background` symlink; switch via `omarchy theme set` | `omarchy theme current` → `Matte Black`; `cat theme.name` → `matte-black` | MADO-3 §4 |

Four traps the table encodes, each measured:

1. **Separate consumers.** hypridle/hyprlock/hyprsunset/xdph are not in the include graph —
   each has its own binary; no `hyprland.conf` edit reaches them (MADO-1 §8).
2. **Toggle beats user file.** The live no-gap/no-rounding frame is owned by
   `toggles/hypr/window-no-gaps.conf`, not by `looknfeel.conf` (MADO-1 §7).
3. **Bar: config needs restart, style does not.** `reload_style_on_change: true`
   (`config.jsonc:2`) reloads style only; module changes wait for `omarchy restart waybar`
   (MADO-2 §7).
4. **`ai-usage.conf` is sourced last** (`hyprland.conf:29`) — the usage-tray float rules
   are owned there, ahead of every other layer (MADO-1 §3/§5).

### Plane map — verification scope entry points

A scoped verification starts by picking a scope; this table says where each plane lives,
what reads it, how it takes effect, and which live route can verify it.

| Scope | Files to read | Consumer & reload semantics | Live route (read-only) | Operator-only |
|---|---|---|---|---|
| hypr core | `~/.config/hypr/*.conf` — 12 active files (MADO-1 §2) | Hyprland 0.56.2; auto-reloads on save (omarchy skill:145) | hyprctl read verbs: `getoption`, `binds`, `clients`, `monitors`, `workspaces`, `devices`, `animations`, `layers`, `configerrors`, `version`; env/consumers via `printenv`/`pgrep`/`systemctl` | `hyprctl reload`; any file write |
| bar (waybar) | `~/.config/waybar/config.jsonc` (249 L), `style.css` (136 L) (MADO-2 §1) | waybar v0.15.0 running (PID 1707, parent = Hyprland; MADO-R3-1 §1); style auto-reloads (`config.jsonc:2`); modules need `omarchy restart waybar` | measured ledger (MADO-R3-1 §2.3, re-verified): bar surface via `hyprctl -j layers` (levels `2` → namespace `waybar`, pid 1707, `3440 26`); tray via `busctl --user get-property fr.arouillard.waybar /StatusNotifierWatcher …`; **no IPC/query verb in 0.15.0** (`waybar --help` = config/style/log/bar only) → module text config-only, reconstruct via pure-read producers (`RUN`) | `omarchy restart waybar` |
| launcher (walker) | `~/.config/walker/config.toml` (49 L; packaged table `/etc/xdg/walker/config.toml`, 298 L — MADO-R3-1 §6) | walker 2.17.0 via `app-walker@autostart.service` + `elephant.service`; restart `omarchy restart walker` | file bytes; `systemctl --user status app-walker@autostart`; `hyprctl -j layers` when open (absent when closed); D-Bus `dev.benz.walker` (`org.gtk.Actions.List` → `as 0`); sockets shape-only (MADO-R3-1 §6.7/§6.8) | same |
| notifications / OSD | `~/.config/mako/config`, `~/.config/swayosd/{config.toml,style.css}` (MADO-2 §4) | Mako owns `org.freedesktop.Notifications` (PID-measured); swayosd-server separate | `makoctl mode`; `busctl --user status org.freedesktop.Notifications` | restart/reload commands |
| idle / lock | `hypridle.conf` (19 L, `e7d3b8dd…`), `hyprlock.conf` (43 L, `b8d173dc…`), theme `hyprlock.conf` (5 L, `3ef010e7…`) — the two local configs byte-identical to the shipped Omarchy payload; not sourced by hyprland.conf; daemon declared by default autostart `exec-once` (`default/hypr/autostart.conf:1`); actuator set under `~/.local/share/omarchy/bin/` (MADO-R4-2 §1/§2b) | hypridle 0.1.8 = idle daemon; on/off is the stateless process-toggle `omarchy-toggle-idle` (`pgrep`/`pkill -x hypridle` ↔ `uwsm-app -- hypridle`; routes: bar glyph `config.jsonc:207`, `SUPER CTRL+I` `utilities.conf:30`, menu `omarchy-menu:212`); hyprlock spawned on demand only (`omarchy-system-lock:8-13`, `pidof hyprlock` guard); lock/wake side-effects script-defined — DPMS off ≈3 s after lock, wake restores (MADO-R4-2 §5/§8) | `pgrep -x hypridle` — absent at the 16:00–16:08Z probe (MADO-R4-2 §7); PID 1203349 present 16:11–16:22Z (restarted with the session), absent again by 16:24Z with no stop line (cause `[UNK]`; F1's disappearance pattern recurred) — re-measure before reuse; `systemctl --user is-active` → `inactive`, `is-enabled` → `disabled`; `journalctl --user` boot-start only (F1); file bytes; session sample via `loginctl show-session` (`IdleHint`/`LockedHint`) and `hyprctl -j layers` (no lock surface while unlocked); live idle transitions have no read surface — no lock test allowed | start/stop daemon; `omarchy-restart-hypridle`; firing the chain (`omarchy-system-lock`, DPMS); any lock or idle-interval test |
| sunset / xdph | `hyprsunset.conf` (14 L), `xdph.conf` (4 L) (MADO-1 §8) | separate consumers, outside the include graph; hyprsunset measured absent; xdph portal running (PID epoch-varying — 1920 at MADO-1 §8, 1203662 this pass) | `pgrep -x hyprsunset` (no match); `pgrep -af xdg-desktop-portal-hyprland`; file bytes | start/stop services |
| terminals | `~/.config/{alacritty,foot,kitty,ghostty}/` — only Alacritty installed (MADO-3 §1/§5) | per-terminal binary; `omarchy restart terminal` (omarchy skill:172) | file bytes + `command -v`; colors resolve through the theme include | restart; `omarchy install terminal` |
| theme & wallpaper | `~/.config/omarchy/current/theme/**`, `theme.name`, `current/background` (MADO-3 §4) | every app includes the theme files; rewritten by `omarchy theme set` | `omarchy theme current`; file reads | `omarchy theme set` |

## Claim → evidence-class routing

The routing decides which evidence class may carry which claim — and which claims an
evidence class is barred from. A claim is only as strong as its tag; pick the class
deliberately and name it in the report.

| Evidence class | Licenses (claim allowed) | Does not license (claim barred) | Anchor |
|---|---|---|---|
| File bytes (`read`, `path:line`, `wc`, `sha256sum`, `grep`, `diff`) | what a file declares and where; include order; who declares a key; orphans / unsourced files; substrate identity | the effective value — declarations can be shadowed (toggle beats user file) or inert (commented lines); nothing about the running session | MADO-1 §2/§3/§7; MADO-R2-1 §2/§7 |
| hyprctl live read (`getoption`, `binds`, `clients`, `monitors`, `workspaces`, `devices`, `animations`, `instances`, `layers`, `configerrors`, `version`) | effective value after the whole include chain, and which declarer owns it (`agreement*` shadowing proof); parsed bind surface (counts/flags/modmask, 192/192 reconciled); runtime state (workspaces, clients, dynamic tags, the bar's layer surface via `layers`); load health | intent; who wrote the file; dispatcher *behaviour* (no keystroke injection run — `[INF-docs]` only); per-window rule effects (no rule-read verb in 0.56); env vars (no query surface) | MADO-R2-1 §3-§5; MADO-R2-2 §1/§2.2/§5; `layers` extension MADO-R3-2 §2.5 |
| Docs-inference (`[INF-docs]` / `MAN` — wiki / omarchy skill / locally installed man pages) | procedure and documented semantics: change rituals, grammar (mod-list bits, flags), documented evaluation order; waybar module/format semantics from the installed package's man pages (`MAN` tag, MADO-R3-1 §2.1/§3) — label it, never assert as host state | the host's current value or state; that the host matches the doc's era — wiki drift (lua-era vs host hyprlang) and skill drift (hooks flat vs `*.d`) stand; man pages track the installed package but document defaults, not the live config | MADO-R2-2 §2.1/§4.3/§6.2; MADO-R3-1 tag legend/§2.1; omarchy skill:300-305 |
| Consumer-side probe (no hyprctl surface exists) | runtime facts owned by other consumers: `printenv` for env, `pgrep`/`systemctl`/`journalctl --user` for process & service history, `makoctl` for DND, `busctl` for D-Bus properties/tray; payloads from pure-read producers run contained (`RUN` — no network, no mutation; MADO-R3-1 §10) | config-load semantics; the consumer's own config values (config-only surfaces stay static) | MADO-R2-1 §4/§6; MADO-1 §8/§10; MADO-R3-1 §10; MADO-R3-2 F1 |

### Claim-first routing (what am I trying to settle?)

| The claim you must settle | Route to | Run (read-only) | Tag |
|---|---|---|---|
| What a file declares / where a key is declared | file bytes | `grep -n`, `wc`, `sha256sum`, read | `[OBS]` |
| The effective value after the whole chain | hyprctl live | `hyprctl -j getoption <key>` (value + `set` flag) | `[OBS]` |
| Who owns the live value (shadowing proof) | hyprctl live | live value vs the last declarer chain — `agreement*` | `[OBS]` (MADO-R2-1 §5) |
| Which binds exist / counts / flags / modmask | hyprctl live | `hyprctl -j binds` + reconcile per MADO-R2-2 §5 | `[OBS]` |
| Live display / workspace / window state | hyprctl live | `monitors`, `workspaces`, `activeworkspace`, `clients` (length/tags only) | `[OBS]` |
| Load health | hyprctl live | `hyprctl configerrors` (empty = clean) | `[OBS]` |
| Window-rule effects; exec-once results; env vars | no hyprctl surface | declarations: file bytes; state: consumer probes (`pgrep`, `printenv`, `systemctl`) | declarations `[OBS]`, live `[UNK]` unless a consumer probe covers it |
| What a dispatch/bind does when fired; rule toggles | docs-inference only (mutation banned) | do not fire; quote docs | `[INF-docs]`; behaviour stays `[UNK]` |
| Change ritual / grammar / evaluation order | docs-inference | omarchy skill / wiki text, era cross-checked | `[INF-docs]`; never host state |
| Who owns notifications / DND state | consumer-side probe | `busctl --user status org.freedesktop.Notifications`; `makoctl mode` | `[OBS]` |
| Bar runtime facts (running? mapped? tray? module text) | hyprctl live + consumer-side probe | `hyprctl -j layers` (namespace `waybar`, pid, geometry); `pgrep -x waybar`; tray via `busctl --user get-property fr.arouillard.waybar /StatusNotifierWatcher …`; indicator scripts probe process/mako mode (`RUN`, e.g. `idle.sh:3`) | `[OBS]` (MADO-R3-1 §1/§2.3); module text without an IPC verb → `[UNK]` |

### Divergence vocabulary and severity taxonomy

Divergence vocabulary when reading a live row (falsifiable classes, MADO-R2-1 §2):
`agreement` / `agreement*` — live equals the last declarer; starred = an earlier declarer is
provably shadowed. `live-default` — `set=false`, no declarer: engine default or pure runtime
state, never attributed to a file. `mismatch` — live ≠ resolved declaration; report as a drift
finding (0 instances in the 56-option pass; any new mismatch falsifies that result). `config-only`
— declared but no read surface (window rules, exec-once, include graph, other-consumer configs):
the live layer stays UNKNOWN. A semantics claim is only as strong as its tag — declared bind
parsing is `[OBS]` (192/192), dispatcher behaviour is `[INF-docs]` (nothing fired, MADO-R2-2 §1/§6.1).

Severity is the consequence label for a finding. The scale below is the lane's canonical
one — the scale of the round-3 end-to-end report (MADO-R3-2 §6, register F1–F10); the
round-2 vocabulary classes above are its inputs. It adds no factual claim of its own.

| Sev | Name | Trigger (falsifiable) | Measured register | Handling |
|---|---|---|---|---|
| S1 | functional | a declared behavior cannot happen live — missing consumer/state; safety- or user-visible | F1: hypridle absent → the 150 s/152 s idle-lock chain has no consumer (journal proves it started at boot; stop cause `[UNK]`) — MADO-R3-2 §6 F1 | operator decision; remedies named in the report |
| S2 | discrepancy | declared vs live (or doc vs host) mismatch with a plausible user-visible effect; no breakage proven — includes orphan files whose declared effect is provably absent and live anomalies with cause `[UNK]` | F2: Alacritty `default-opacity*` on 2/3 windows → opacity product ≈0.9409/0.81 (MADO-R3-2 §6 F2; MADO-R2-2 §4.6); F3: orphan `envs.conf` NVIDIA trio unset on an NVIDIA-GPU host; a `mismatch` row lands here and falsifies the 0-mismatch census | report pair + recommendation; operator decides |
| S3 | informational | record-level, hygiene, nominal rounding; no action required — also `agreement*` ownership proofs, `live-default`, intentional drift vs stock | F4–F10 (grok-bot absent; monitor 99.997 vs 100; uninstalled-terminal configs; backup litter; `wl_socket` record correction; keyboard node count 8→9; mako `--version` misuse) — MADO-R3-2 §6; 6 ownership proofs + 4 `live-default` (MADO-R2-1 §5); drift inventory MADO-2 §6 | record only |

Rules that keep the taxonomy falsifiable:

1. A finding needs both anchored sides (declared anchor × measured probe). One side → UNK item.
2. `config-only` is not a severity — it is the absence of a read surface; the live layer stays UNKNOWN.
3. Severity ranks consequence; the tag ranks confidence. Keep them orthogonal (`[INF-docs]` drift can be S2; an `[OBS]`-vs-`[OBS]` contradiction is S2 too).
4. Cause `[UNK]` caps at S2 (no breakage proven); S1 requires a measurable non-occurrence of the declared behavior, not an expectation.

Round-3 R3-1 adds severity-eligible observations not yet in R3-2's register — the inert
`custom/voxtype` module plus its producer's `trap 'kill 0'` process-group hazard
(MADO-R3-1 §8.1), and `battery` with no device on this host (§8.2). Classify them with the
same triggers before they enter any register.

## Safe-probe discipline — measure, don't mutate

Boundary (PROVINCE.md:10-12, :16): all config trees are READ-ONLY for this lane — probe,
measure, recommend; the operator applies. Never mutate a running compositor state; every
claim is file-byte- or screenshot-verified. Why the strictness: Hyprland auto-reloads on
config save (omarchy skill:145) — a write into `~/.config/hypr/` becomes live state in the
same moment, so there is no "stage now, apply later" for files. Waybar does not auto-reload
(skill:159), so its edits merely wait for a restart — still not mado's to make. The skill's
validation pair `hyprctl reload` + `hyprctl configerrors` (skill:147-148) splits by lane:
mado runs only the read leg (`configerrors`).

### Read-only probes (all executed 2026-10-14 unless cited)

| Probe | Answers | Sample |
|---|---|---|
| `hyprctl version` | version pins | `Hyprland 0.56.2` |
| `hyprctl configerrors` | config load health | empty = clean |
| `hyprctl monitors` / `workspaces` / `activeworkspace` | live display & workspace state | DP-1 3440x1440@99.997, workspace 1 |
| `hyprctl getoption <key>` | effective value after the whole override chain | `gaps_out` → `custom type: 0 0 0 0`; `input:kb_layout` → `str: br` |
| `hyprctl binds -j` | effective bind count | 192 (matches file arithmetic, MADO-1 §4) |
| `hyprctl layers -j` | compositor-side view of bar/launcher layer surfaces | DP-1 levels `2` → `waybar` pid 1707 `3440x26`; level `0` → `wallpaper` (MADO-R3-1 §1; read-only whitelist extension, MADO-R3-2 method) |
| `omarchy commands --json` | command inventory: route/binary/summary/args | read-only discovery |
| `omarchy theme current` / `omarchy version` | active theme / Omarchy pin | `Matte Black` / `3.8.3` |
| `omarchy menu keybindings --print` | effective human bind list | exit 0; SUPER+RETURN → Terminal |
| `wc` / `stat` / `sha256sum` / `grep` / `diff` on files | byte-level truth behind any claim | MADO-1 §2/§13 methodology |
| `pgrep -a` / `ps` | what actually runs | waybar 1707, mako 1706, walker 1808, swayosd 1815, 3x alacritty; hypridle/hyprlock absent |
| `systemctl --user is-active <unit>` | service state | hypridle → `inactive` |
| `makoctl mode` | DND state | `default` |
| `busctl --user status org.freedesktop.Notifications` | who owns notifications | Mako PID 1706 (MADO-2 §4) |
| reading `~/.local/share/omarchy/**` | defaults + command sources | reading is safe and encouraged (omarchy skill:41, :58-62) |
| `grim -t ppm -` (screenshot read to stdout) | visual state without a file | read OK, 14,860,817 B this pass (stdout, nothing persisted); grim/slurp/hyprpicker all on PATH |

### Mutating commands — operator only, mado never runs

- `hyprctl reload` — applies config to the live session (skill:147).
- `omarchy restart waybar|walker|terminal` — kills and respawns the component (MADO-2 §3.1/§7).
- `omarchy refresh …` — copies stock over the user file, destroying local drift; the skill
  requires user confirmation (skill:234-247); drift inventory in MADO-2 §6.
- `omarchy toggle …` — writes the toggles dir that overrides every other layer (`hyprland.conf:23`).
- `omarchy theme set …` — rewrites the theme plane consumed by every app (MADO-3 §4).
- any file write under `~/.config/`, `~/.local/state/omarchy/`, or `~/.local/share/omarchy/`.

### Safety rules — the mutation-free fence

1. **Read-verb whitelist.** hyprctl: only `getoption`, `monitors`, `workspaces`,
   `activeworkspace`, `clients`, `binds`, `animations`, `devices`, `instances`, `layers`,
   `configerrors`, `version`. Never: `keyword`, `dispatch`, `reload`, `setprop`, `setcursor`,
   `output`, `notify`, `plugin`, `batch`, `--instance` overrides (MADO-R2-1 §0, §8; `layers`
   added read-only in MADO-R3-2 method/§2.5).
2. **No firing, no injection.** No keystroke injection, no dispatcher invocation; rule-effect and
   rebind tests are operator-only — `hyprctl keyword 'windowrule[name]:enable false'` is mutating
   (MADO-R2-2 claim boundary / §5). Running a producer script is allowed only when its source
   proves it pure-read and side-effect-free (no network, no writes) and it runs contained — the
   `omarchy-voxtype-status:5` `trap 'kill 0' EXIT` is the measured counter-example: it SIGTERMs
   its own process group (MADO-R3-1 §8.1).
3. **Prove the boundary.** A probe pass ends only when the config trees are byte-identical:
   `sha256sum` before/after equals MADO-1 §2 (MADO-R2-1 §7). Trees stay read-only
   (PROVINCE.md:10-12); findings are report-and-recommend.
4. **Session material stays shape-only.** `clients` for length/tags, never window titles;
   `hyprland.log` shape-only; no `/proc/*/environ`; `HYPRLAND_INSTANCE_SIGNATURE` shape-checked,
   never printed in full (MADO-R2-1 §0).
5. **Unverifiable → UNKNOWN, not inference.** If a claim needs a mutation or a surface that does
   not exist, mark `[UNK]` and stop. If hyprctl is unavailable or unreachable, the live layer is
   UNKNOWN: fall back to file-byte evidence (recipe in the checklist, step 3); never disambiguate
   instances by guess (MADO-R2-1 §6/§8).
6. **Scratch outside the substrate.** Probe artifacts under `/tmp/<lane>-*` only; nothing
   persisted into config trees (MADO-R2-1 §0; MADO-R2-2 header).

Persist nothing into config trees; screenshot artifacts, if kept, live under the lane repo.
OBS/INF/UNK stay separate and errata are append-only (corpus/QUALITY.md:1-5); a rejected
claim is kept, never silently dropped (MADO-2 §9 model).

## Scoped verification — executable checklist

Definition of done: every claim in scope is a classed row with two anchored sides; every
finding carries a severity; the substrate is proven byte-identical; remaining unknowns are
listed explicitly; every command used is named so the pass re-runs.

0. **Declare the scope** — write the claim list first (one question, one plane, or the
   full four-plane report). Everything below serves that list.
1. **Scratch outside the substrate:**
   `mkdir -p /tmp/mado-verify-$(date +%s) && cd "$_"` — artifacts never touch config trees.
2. **Baseline the bytes** (match the scope; hypr example):
   `sha256sum ~/.config/hypr/*.conf ~/.config/hypr/*.bak.* > before-hypr.sha256`
   plus the scope's other files (waybar/walker/mako/terminal/theme) into their own list.
3. **Environment gate** — all must pass; any fail → live layer UNKNOWN → file-byte branch:
   - `command -v hyprctl` → `/usr/bin/hyprctl`
   - `hyprctl version | head -1` → `Hyprland 0.56.2 … efb5099…`
   - `hyprctl configerrors` → empty, rc=0
   - `hyprctl -j instances | jq length` → `1`
   - `printenv HYPRLAND_INSTANCE_SIGNATURE | cut -c1-12` — shape check only, never full
   - Fail conditions (MADO-R2-1 §8): no binary; no signature and no
     `/run/user/$(id -u)/hypr/*/.socket.sock`; hyprctl cannot connect; >1 instance and the
     target is ambiguous — do NOT guess via `--instance`; resolve via the running session's
     own signature, else mark live UNKNOWN and fall back to file-byte anchors.
4. **Map owners (file bytes)** — grep each claim's key through the include chain
   (Config-plane map), note every declarer in order, flag files no `source` reaches.
5. **Live pass (hyprctl reads only)** — one row per claim: value + `set` flag. Expected
   samples: `gaps_out` → `custom: 0 0 0 0` (set true); `input:kb_layout` → `str: br`;
   `input:touchpad:scroll_factor` → `float: 0.400000`; `hyprctl -j binds | jq length` →
   `192`; `configerrors` → empty.
6. **Consumer probes** where no hyprctl surface: `printenv GDK_SCALE` → `1`;
   `printenv NVD_BACKEND` → unset; `makoctl mode` → `default`;
   `systemctl --user is-active hypridle` → `inactive`; `pgrep -x hypridle` → empty.
7. **Classify** — divergence vocabulary; severity for findings; keep the UNK list.
8. **Boundary proof** — re-run step 2 and `diff` before/after; must be empty (measured:
   all 13 `~/.config/hypr` files byte-identical to MADO-1 §2). Any delta → abort, report,
   do not continue.
9. **Report** — one table plus UNK list plus boundary statement:

   | # | Claim | Route (class) | Declared side (anchor) | Live side (probe → value) | Class | Sev | Tag |
   |---|---|---|---|---|---|---|---|

   and the sentence: "Substrate byte-identical before/after (sha256), pass <date>."

### Worked example — 3-claim scoped pass (executed 2026-10-14 14:40 UTC, read-only)

| # | Claim | Route | Declared (anchor) | Live (probe → value) | Class | Sev |
|---|---|---|---|---|---|---|
| 1 | Effective `general:gaps_out` | hyprctl live | default `looknfeel.conf:10` = 10; toggle `window-no-gaps.conf:3` = 0 | `hyprctl -j getoption general:gaps_out` → `{"custom":"0 0 0 0","set":true}` | `agreement*` — toggle owns | S3 |
| 2 | Effective keyboard layout | hyprctl live | default `input.conf:3` = us; local `input.conf:10` = br | `hyprctl -j getoption input:kb_layout` → `{"str":"br","set":true}` | `agreement*` — local owns | S3 |
| 3 | NVIDIA env vars set? | consumer probe | orphan `envs.conf:3-5` declares 3 vars; no sourcer | `printenv NVD_BACKEND` → unset (rc=1) | orphan — declared effect provably absent (= round-3 register F3) | S2 |

Boundary statement for the pass: `sha256sum ~/.config/hypr/*.conf` → all first-12 prefixes
equal MADO-1 §2 (`hyprland.conf` = `4f52854a3c143dcf58430a679e339619223d2b5008115a322d06b2de637ea462`);
no file written; no compositor state mutated. Companion pins from the same pass:
`hyprctl -j binds | jq length` → 192; `makoctl mode` → `default`; `omarchy theme current` →
`Matte Black`.

### Reproduction package — re-run the round-3 end-to-end pass

The round-3 report is not narrated-only; it re-runs. Two packages, both read-only
(hyprctl read verbs + file reads + consumer probes; nothing touches a substrate):

1. **Round-3 set** — the pass behind MADO-R3-2 (`/tmp/mado-r3-2-probe/`, scratch,
   ephemeral; MADO-R3-2 §11 item 4): `01-filebytes.sh` (sha/bytes chains),
   `02-hyprctl.sh` (live reads → 57 raw `getoption` JSONs + binds/monitors/layers),
   `03-consumers.sh` (process/service/D-Bus/env probes), `expected.tsv` (57 round-2
   expected rows), `check-getoptions.py`. Recipe: copy the set to fresh scratch,
   redirect its `D=` to the copy (scripts write into `D`), then
   `bash 01-filebytes.sh && bash 02-hyprctl.sh && bash 03-consumers.sh && python3 check-getoptions.py`
   → `checked 57; mismatches/missing: 0` (re-run from a copy 2026-10-14 16:07 UTC,
   `/tmp/mado-r4-4-repro/`; full chain rc 0; census 46 `agreement` + 6 `agreement*`
   + 4 `live-default` + 1 extra).
2. **Round-4 reviewer pack** — `/tmp/mado-r4-1-probe/repro-r3.sh` (MADO-R4-1, scratch,
   ephemeral): self-contained one-pass driver of the same sweep (embeds `expected.tsv`,
   emits `summary.txt`); usage `D=/tmp/<your-scratch> bash repro-r3.sh` — the `D=`
   redirect keeps each package's own scratch frozen.

Durable half: the notes themselves (`corpus/knowledge/`: `config-health-report-r3.md`
§0–§11 + Appendix A; `executor-test-sufficiency.md`; `corpus/README.md` coverage map).
Scratch under `/tmp` is ephemeral by declaration — copy a package out before it is
reaped. Epoch-varying values (PIDs, window set, device counts) are expected to differ
between runs; pins and the 57-option check are the stable assertions. One such change
was measured inside round 4 itself: the compositor session restarted 2026-10-14
16:11:06Z (new Hyprland PID 1203316 replacing 1671; hypridle restarted with it, cause
`[UNK]`), so pre-restart packs carry the old session's PIDs and fresh re-runs see new
ones.

## Error patterns & traps

Symptom → cause → the check that settles it (each measured):

| Symptom | Cause | Correct check |
|---|---|---|
| "The file says X, so X is live" | shadowing — later layers win (toggle L23, theme L13, `ai-usage.conf:29`) | `hyprctl getoption <key>` (value + `set`) |
| "Run `hyprctl reload` to validate" | mutation — reload applies to the live session (skill:147) | mado runs `hyprctl configerrors` only; `reload` is operator-only |
| "Edited waybar modules; nothing changed" | style auto-reloads (`config.jsonc:2`); modules need restart (skill:159) | re-read `config.jsonc:2`; restart is operator-only (MADO-2 §7) |
| "SUPER+SPACE opens the Omarchy menu" | stock binding launches Walker; the menu is SUPER ALT+SPACE | `omarchy menu keybindings --print`; `hyprctl binds -j` (MADO-2 §9; R2-E2) |
| "NVIDIA vars are configured" | orphan `envs.conf` sourced by nothing | `printenv NVD_BACKEND` (unset) + `grep -rn 'envs.conf'` across the chain (MADO-R2-1 §6) |
| Bind math doesn't close (≠192) | unsourced/deprecated binding files, commented `unbind:34` | per-file `grep -c '^bind'` sums 23+4+90+50+25; `hyprctl binds -j` counts live (MADO-R2-2 §1) |
| "The docs say X, the host does Y" | docs drift — wiki lua-era vs host hyprlang; skill hooks flat vs `*.d` | pin `hyprctl version`; `configerrors`; label `[INF-docs]` (MADO-R2-2 §6.2; MADO-3 §7) |
| "What do the open windows show?" | `clients` titles are session material | use `clients` length/tags only; dynamic tags render `*` (MADO-R2-2 §4.6) |
| "Check the compositor log" | `hyprland.log` is session material | shape-only (size/mtime); never content-read (MADO-R2-1 §0) |
| Bar shows an idle/notification icon | bar state is a process/mode probe, not a bar flag | `pgrep -x hypridle`; `makoctl mode` (MADO-2 §2.4) |
| "Will the session lock after idle?" | the declared 150 s/152 s chain has no consumer while hypridle is absent (S1, F1) — it cannot fire; lock state has no read surface while unlocked | `pgrep -x hypridle` + `journalctl --user` boot/stop lines; never trigger the chain (mutation, operator-only) (MADO-R3-2 §6 F1; MADO-R4-2 §7) |
| "What is the bar showing right now?" | waybar has no query verb — config-only + producer probes | compositor view `hyprctl -j layers`; pure-read producer payloads (`RUN`), e.g. the indicator scripts (MADO-R3-1 §2.3/§3) |
| Weather chip vanished | `.unavailable` class collapses the module by design when offline | check the network path in `weather.sh`; `style.css:75-79` (MADO-R3-1 §7) |
| A version claim won't reproduce | Omarchy dual pin — `omarchy version` 3.8.3 vs checkout tag v3.8.4 | name the source: `omarchy version` vs `git -C ~/.local/share/omarchy describe --tags` (MADO-R3-1 §8.4) |
| Count-sensitive claim drifts (8 → 9 keyboards) | device lists are hotplug-sensitive | state device context; re-count `hyprctl -j devices` (MADO-R3-2 F9) |
| Two hypr instances: "which is mine?" | ambiguous target | resolve via the session's own signature; never guess with `--instance` (MADO-R2-1 §8) |

## Omarchy boundary — skill instructs, mado measures

`~/.agents/skills/omarchy/SKILL.md` (392 lines, single file, no assets — MADO-3 §7) is the
domain's instruction authority for end-user customization; PROVINCE.md:10-11 declares it a
read-only documentation surface for this lane. Two actors, one substrate:

- **The skill instructs the editing actor** — it carries the rituals mado cites but does
  not execute: hypr auto-reload + validation pair (`:145-148`), waybar restart (`:159`),
  terminal restart (`:172`), walker restart (`:203`), mandatory `unbind` before rebind
  (`:272-286`), window-rules wiki re-fetch (`:300-305`), never-edit-source rules
  (`:41-47`, `:373-378`).
- **mado measures the substrate** — with the probe tables above; a finding is a measured
  pair: skill text vs host bytes.

| Situation | Route |
|---|---|
| "What is the correct way to change X?" | omarchy skill — quote its ritual, then verify the host state it assumes |
| "What is set / running / drifted now?" | mado probes; file-byte or command-output evidence |
| Skill text vs host disagreement | record drift [OBS], keep the skill untouched, report both sides |
| Editing the skill, or `~/.local/share/omarchy/**` | never — skill is read-only documentation; source is read-safe but edit-forbidden (skill:41, :49) |
| Omarchy source development / `omarchy dev …` | out of scope for the skill itself (skill:37, :373-378); out of province → report, never absorb (PROVINCE.md:18) |

Rules:

1. **Never recite the skill from memory.** Its window-rules block demands a wiki re-fetch
   before ANY window-rule work (skill:300-305), and its listings can be older than the
   host: the hooks block shows flat files (`:219-223`) while the host has five `*.d`
   directories (MADO-3 §7). Verify against the live bytes before citing either.
2. **Host-verify even "obvious" claims.** "SUPER+SPACE opens the Omarchy menu" is false
   here — the live list shows SUPER+SPACE → Launch apps, SUPER ALT+SPACE → Omarchy menu
   (MADO-2 §9; `omarchy menu keybindings --print`).
3. **The skill writes for an editing assistant; mado is stricter.** Edits it authorizes in
   `~/.config/` remain operator-only for this lane (PROVINCE.md:10-12). When the two rules
   disagree, the stricter one wins for mado.
4. **Skill drift is a finding, not a licence.** Report the pair (skill line vs measured
   state); corrections go to the append-only errata of the source note, never into the
   skill file.

## Evidence trail & sources

- Round 1: `corpus/knowledge/hyprland-config-plane.md` (MADO-1, 217 L by `wc -l`; editor
  view 218): inventory §2, include graph §3, keybinds §4, window rules §5, animations §6,
  override chain §7, separate consumers §8, version pins §9, runtime §10, open items §12.
  `corpus/knowledge/waybar-walker-plane.md` (MADO-2, 364 L by `wc -l`; editor 365):
  inventory §1, waybar §2, walker §3, notifications/OSD §4, idle/lock §5, drift vs stock
  §6, decision table §7, unknowns §8, rejections §9. `corpus/knowledge/terminals-and-omarchy.md`
  (MADO-3, 179 L by `wc -l`; editor 180): terminals §1-2, invariants §3, theme plane §4,
  install state §5, backup delta §6, skill anatomy §7.
- Round 2: `corpus/knowledge/hyprctl-verification-layer.md` (MADO-R2-1, 280 L by `wc -l`;
  editor 281; 56 `getoption` claim→live pairs + 9 non-getoption pairs; classes and
  ownership proofs). `corpus/knowledge/keybind-rule-semantics.md` (MADO-R2-2; the note
  self-labels MADO-4; 315 L by `wc -l`; editor 316; 192/192 bind reconciliation; 24
  dispatchers; rule semantics; §4.6 live divergence). Both measured 2026-10-14 against the
  same bytes as MADO-1 (sha256 equality, MADO-R2-1 §7).
- Round 3 (this pass, MADO-R3-3): sufficiency upgrade of this document — the plane map,
  claim-first routing, the S1/S2/S3 severity taxonomy (adopting MADO-R3-2 §6's register
  scale), the scoped-verification checklist and the error patterns above; the worked example
  and the re-verified pins were executed read-only 2026-10-14 14:40–14:45 UTC
  (`/tmp/mado-r3-3-*`). Sibling round-3 notes integrated, both landed during this pass's
  15-minute poll (14:51/14:53 UTC): `corpus/knowledge/waybar-walker-semantics.md` (MADO-R3-1,
  455 L by `wc -l`; editor 456 — bar/launcher module semantics, introspection ledgers,
  boundary proof) and `corpus/knowledge/config-health-report-r3.md` (MADO-R3-2, 546 L by
  `wc -l`; editor 547 — 4-plane coverage table; 57/57 getoption re-measure, 0 mismatch;
  F1–F10 register = 1×S1 + 2×S2 + 6×S3; its §9 stale-quote item is fixed here).
- Re-verified anchors in this pass: binds=192; `gaps_out`=0 via toggle; `input:kb_layout`=br;
  `input:touchpad:scroll_factor`=0.400000; hypridle inactive + no PID; `makoctl mode`=default;
  `omarchy theme current`=Matte Black; `hyprctl configerrors` empty; `hyprctl version` 0.56.2
  `efb5099…`; `hyprland.conf` sha256 `4f52854a…`; `printenv` → `GDK_SCALE=1`, `NVD_BACKEND` unset;
  `hyprctl -j layers` → level 2 `waybar` pid 1707 `3440x26`; `busctl` tray items `as 0`;
  `waybar --help` exposes no query verb; Omarchy dual pin re-measured (`omarchy version` 3.8.3 /
  tag v3.8.4, clean).
- Later rounds append: an executable verdict gate (`corpus/scripts/`), verifier wiring, and
  severities for MADO-R3-1's unregistered candidates — each with its measured anchor. Known
  stale quote fixed this pass: the round-2 distillation quoted the keybind note as "313 by
  `wc -l`"; it is 315 (LOG round-2 observation (a); flagged in MADO-R3-2 §9).

## Promotion-box status — what remains

The lane's gate is `SHONEN.md` — the canonical four boxes (`[~]` = lane-asserted
with pointer; `[x]` = named non-author verifier; seed PROTOCOL.md:419-431).
State measured 2026-10-14 16:28Z — SHONEN.md unchanged since the round-3 commit
(mtime 12:51 −03):

| Box (SHONEN.md) | Mark | Verifier attribution — or what remains |
|---|---|---|
| decision tables / checklists / cited sources | `[x]` | MADO-R3-4 (non-author executor lane) — `corpus/knowledge/executor-test-sufficiency.md`; SKILL sha `ef4c29e3…` frozen at the round-3 commit |
| e2e domain task executed and logged (`:7`) | `[~]` | what remains: the named non-author reviewer attribution. A reviewer seat re-ran the R3 pass from the notes — scratch `/tmp/w4-m4-1-repro/` (runs 16:21/16:24Z; corrected pass: 57-option check, 0 mismatches). Pack: the Reproduction package above — `config-health-report-r3.md` §11 item 4, `/tmp/mado-r3-2-probe/`, `/tmp/mado-r4-1-probe/repro-r3.sh`; re-run copy `/tmp/mado-r4-4-repro/` (16:07Z, 57/0) |
| executable without oral context | `[x]` | MADO-R3-4 (same note; per-step sufficiency over steps 0–9) |
| PROVINCE accuracy (`:11`) | `[~]` | what remains: the named non-author verifier's verdict. Audit note landed — `corpus/knowledge/province-accuracy-selfaudit.md` (17,190 B, sha `f81f19db…`; self-audit explicitly labeled, claim census 15/15 `[~]`, its §7 is the closure handoff). Pack: `PROVINCE.md` (18 L, sha `7aad7b86…`) + audit scratch `/tmp/w4-m4-3/*.log`; the round-4 verifier seat's poll found the note at 16:26Z (`/tmp/w4-ver-m4-scratch/poll.log`) |

Rules (`plans/round-4.plan.md`): self-attestation does not count — only an
integrator-dispatched, independent seat closes a box; the round-4 measure is
2 named verifier attributions in `SHONEN.md` with evidence pointers. Anti-claim:
a non-reproduction or a province violation keeps the box open and says why.
This SKILL pins the verifier inputs; the marks themselves land in `SHONEN.md`.

## Round-5 — verdict gate & box-4 closure status (append, M5-4)

Appended 2026-10-14 17:27Z (25-min poll closed 17:27:08Z; M5-1/M5-2 both
landed in-window). Round-5 plan (`plans/round-5.plan.md`, 9 L, sha
`1061fe40b7c2da4e…`) owns two moves: (a) close box 4 via the §8 re-run with a
named verifier, (b) ship the lane's first executable gate. This section records
both as measured; the only file this lane wrote is this one (scratch
`/tmp/w5-mado-m5-4/`; logs named below). Substrate stayed read-only.

### Gate usage — `tools/mado-verify.sh` (v1, round 5 / M5-2)

One command verifies the declared planes (hypr core, waybar, walker, terminals)
against live bytes and hyprctl read verbs, then prints one verdict line.

    bash tools/mado-verify.sh                 # live, read-only, root=$HOME
    bash tools/mado-verify.sh --no-live       # file plane only; verdict names the skipped live layer
    bash tools/mado-verify.sh --root DIR      # file plane against DIR (used by the selftest)
    bash tools/mado-verify.sh --selftest      # hermetic fixture assertions (no substrate reads)
    env: MADO_VERIFY_ROOT, MADO_VERIFY_LIVE=auto|yes|no

Exit map (script `--help`/header): `0` = CLEAN · `1` = DIVERGED — a check
FAILed, or a required check was UNVERIFIABLE, i.e. any UNKNOWN blocks CLEAN ·
`2` = tool/usage error (bad args; a failing `--selftest`). Row classes PASS /
FAIL / UNKNOWN / SKIP / NOTE; NOTE rows are record-level (S3-class or open
findings) and never flip the verdict.

Measured this pass, read-only (logs `/tmp/w5-mado-m5-4/gate-selftest.log`,
`gate-live.log`):

- `--selftest` (17:12:34Z) → `MADO_SELFTEST: 28/28 assertions passed`, rc 0.
  Hermetic: fixtures under `/tmp/w5-mado-m52-selftest.*`, removed on success;
  scenario C proves the anti-claim (live requested, no `hyprctl` on PATH →
  `live.plane` UNKNOWN row, exit 1, no fake CLEAN).
- live run (17:12:39Z) → `MADO_VERIFY: CLEAN (35 pass, 0 fail, 0 unknown,
  4 notes)`, rc 0; independent before/after combined sha256 over the declared
  config trees byte-identical (`489eaf5d…` both sides).
- Script identity at this pass: 1098 L, sha `d7edaab4bf108625…` — re-measure
  before citing (live wave).

Scope honesty (script header): window-rule effects, dispatcher behaviour,
module text, idle/lock transitions have no read surface → stay UNKNOWN, never
guessed. The manual equivalent stays this SKILL's Scoped verification checklist
(steps 0–9); the gate encodes those rows and adds `boundary.readonly` as a gate
row. Path note: the `:426` placeholder (`corpus/scripts/`) is superseded —
round 5 ships `tools/mado-verify.sh`.

### Box-4 status — PROVINCE accuracy

Close evidence landed 17:07–17:09Z, two parts:

1. §8 re-run receipt (in-repo, durable) — `corpus/knowledge/province-accuracy-
   selfaudit.md` round-5 addendum (M5-1): 25/25 §8 rows re-derive, 4 cross-class
   spot-checks, "no falsification found"; file now 345 L by `wc -l`, 24,670 B,
   sha `7c0a58208dea60e8…` (v4 = byte-prefix append over v3 `3014a840…`).
2. Named verifier verdict (scratch, ephemeral) — `/tmp/w5-ver-m4b-work/
   VERDICT.md` (8,625 B, sha `f70fc3c70a11e91e…`): "**[x] VER-M4B — box 4
   CLOSES**"; all province claims hold on the verified revision.

`SHONEN.md` measured at this append's cap (17:27Z, 12 L, sha
`f6495fe68f4265e3…`): box 4 still `[~]` at `:11` — the closure edit
(`[x] VER-M4B` + pointer, per the self-audit §7 procedure) is the
scribe/finalizer's write, outside this lane's scope. When it lands, SHONEN
reads 4/4 `[x]`.

Refreshed pointers (supersede the `:443` row's v1 numbers, 17,190 B / sha
`f81f19db…`): self-audit 24,670 B / `7c0a58208dea60e8…` (v4); `PROVINCE.md`
unchanged (18 L, `7aad7b86…`); box-4 evidence pack = verdict sha + self-audit
v4 sha + M5-1 scratch `/tmp/w5-mado-m5-1/` (ephemeral — hashes fold into the
record).

## Round-6 — the gate proven to fail, and watch-arm usage (append, M6-4)

Appended 2026-10-14 18:05Z, at the close of a 30-min poll for M6-1 (its note
landed 17:59:18Z). Round-6 plan (`plans/round-6.plan.md`, 53 L, sha
`00d4072821cbb15e…`) orders one operability move in three stages: (a) prove the
round-5 gate can fail, then let the proven gate carry (b) the omarchy freshness
arm and (c) the remaining planes' live surface. Measured outcome: (a) landed as
a **selftest hardening** — no declared plane added, no verify-path edit; (b)
and (c) landed as **notes** (one paste-ready arm spec, one census), not as gate
rows. This lane's only write is this file; scratch `/tmp/w6-mado-m6-4/` (logs
named inline); the substrate stayed read-only.

### The gate was made to fail — mutation record (stage a)

Source: `corpus/knowledge/gate-mutation-proof.md` (167 L, 10,693 B, sha
`716836ca1bf3484a…`; M6-1). Harness: `tameshi-shokunin/tools/mutate-and-run.sh`,
consumed read-only; its case note is `tameshi-shokunin/corpus/knowledge/
mutation-case-mado-verify.md` (323 L, 24,534 B, sha `f2d53d49…`). Run shape
(both lanes, and this lane's four re-runs):

    tameshi-shokunin/tools/mutate-and-run.sh --target mado-shokunin/tools/mado-verify.sh \
      --defects <spec> --suite 'bash "$MUTANT" --selftest' --workdir <scratch>

Per defect: KILLED = suite exit ≠ 0 · SURVIVED = suite exit 0 · INCONCLUSIVE =
timeout / suite not runnable. The control run comes first — a red control
refuses the sweep (exit 2) — and `MUTATE_RESTORE: OK` re-hashes the target, so
a sweep never leaves the gate written.

Why the suite really exercises the mutant (measured; it retires the gap the
plan anticipated): the harness copies the target and runs
`bash "$MUTANT" --selftest`; every sub-run inside the selftest re-invokes `$0`,
which *is* the mutant copy — a killed mutant's failure line
(`A: CLEAN verdict (missing: MADO_VERIFY: CLEAN)`) can only have come from the
mutant. No `--target PATH` option on the selftest is needed.

Identity re-pin (supersedes `:487-488` and `:480`):

| | round-5 gate (before) | round-6 gate (landed) |
|---|---|---|
| lines / bytes | 1,098 / 45,334 | 1,186 / 50,126 |
| sha256 | `d7edaab4bf108625…` | `c4c1afb75dd1c8aa…` |
| selftest | `28/28` | `53/53` (rc 0, ≈1.1 s) |
| diff vs previous | — | +88/−0, all inside `selftest()` (M6-1 §Pins) |

Kill grids — every run below was reproduced independently by this lane,
defect-for-defect (control GREEN, `MUTATE_RESTORE: OK`, zero INCONCLUSIVE):

| Spec (scratch, ephemeral) | Defects | Before | After |
|---|---|---|---|
| tameshi clause spec `c7ee75b9…` | 10 | 4 KILLED / 6 SURVIVED (40%) | **10 KILLED / 0 (100%)** |
| M6-1 clause sweep `122df4ad…` (v1) | 15 | 8 / 7 (53%) | 11 / 4 (73%) |
| M6-1 extra-probe sweep `700dece9…` (v2: live-branch verdict token, skip-reason strings, `--root=DIR` form, env renames, version string, counts line) | 9 | — | 3 / 6 (33%) |

The hardening (all additions inside `selftest()`; new helpers `st_row_detail`,
`st_counts_agree`) adds scenarios **E** (no `python3` on PATH → the reader
degradation arms must read UNKNOWN), **F** (a failing selftest must exit 2; the
child runs with `MADO_SELFTEST_NESTED=1` so the probe cannot recurse), **H**
(an undeclared 18th `source =` line must flip the include census to FAIL),
**I** (a PATH-stub `sha256sum` makes the boundary hashes differ mid-run → the
boundary proof must FAIL), plus the skipped-live row (`live.plane SKIP`), a
`sha_pin` detail check, and counts-line agreement in A/B/C/E/H/I.

Residual survivors at the landed revision — findings, recorded, not smoothed:

| Survivor | Clause | Why it survives |
|---|---|---|
| `row_from_rc` rc-6 arm | UNKNOWN-never-CLEAN | dead code — nothing in the gate exits 6, so `6) … UNKNOWN → PASS` is an equivalent edit under any black-box suite |
| `--root` with no value | usage exit map (2) | no assertion on that usage path |
| bad `MADO_VERIFY_LIVE` | usage exit map (2) | no assertion on that usage path (the swept exit channel D5 *is* covered) |
| failing `--selftest` → 0 | failing-selftest exit map | exit-flatten family: the suite runs it **red** (`MADO_SELFTEST: FAILED — 52 passed, 1 failed` · `F: failing selftest exits 2 (got '0' want '2')`) but the mutant's own exit is 0, and KILLED is judged by exit only — a harness boundary (M6-1 §3), not a suite gap |

Three reading rules that follow:

1. An exit-code-only kill criterion is blind to the exit-flatten family — read
   the assertion tail whenever the mutation can touch the suite's own failure
   path.
2. A surviving mutant says "no test notices this clause", never "the clause is
   broken"; the clause stands until a mutant proves otherwise, and nothing
   ships wider without a covering mutant.
3. Mutation-test the copy, never the committed path:
   `--suite 'bash "$MUTANT" --selftest'`. The gate's own verdicts stay
   `bash tools/mado-verify.sh` (or `--no-live` / `--selftest`).

Still unexercised (open): the live-plane body — the live plane declares 51
`row hypr-live` sites (`:673-1111`) and the suite asserts only its guard row
(`live.plane`, 4 sites). A PATH-stub `hyprctl` scenario is the highest-yield
remainder (M6-1 §3; tameshi §8 rec #1) — which is why the v2 probe grid above
stays at 33%.

### Watch arm 1 — omarchy freshness (stage b): usage

Status **spec, not landed**: `corpus/knowledge/omarchy-drift-watch.md` (287 L,
18,714 B, sha `49f5a9a14776d83d…`; M6-2) carries the measurement plus a
paste-ready plane (`omarchy`, row namespace `omarchy.*`; gate census 6 → 7
plane ids). It did not land because M6-2's write scope was the note and landing
rows moves the mutation-proof target sha (note §5) — so the gate still declares
its six planes. Until the rows land, run the watch by hand from the pin table.

Baseline pins (re-measured at dispatch 17:40-17:42Z, read-only; re-anchoring is
an append-only erratum event, never a silent edit):

| Pin | Probe (read-only) | Value 2026-10-14 |
|---|---|---|
| P1 release marker | `omarchy version` | `3.8.3` |
| P2 version file | `cat ~/.local/share/omarchy/version` | `3.8.3\n`, 6 B, == `HEAD:version` blob |
| P3 checkout | `git -C ~/.local/share/omarchy describe --tags --exact-match` · `rev-parse HEAD` | tag `v3.8.4` exactly at HEAD `8fcc9d60…` (branch `master`; 4,363 commits / 1,237 tracked / 63 tags) |
| P4 skill leaf | `sha256sum` of the resolved link (`~/.agents/skills/omarchy/SKILL.md`) | 392 L / 14,908 B / `becd149e…`; == `HEAD:default/omarchy-skill/SKILL.md` |
| P5 link topology | `ls -la ~/.agents/skills/` | `omarchy -> ~/.local/share/omarchy/default/omarchy-skill` (+3 sibling links, same target) |
| P6 theme | `omarchy theme current` | `Matte Black` (NOTE-level — D-1 below) |

Two corrections this arm lands on standing text:

- **Dual pin resolved** (`:20-24`): the 3.8.3-vs-v3.8.4 disagreement is
  upstream-internal — the release tag sits exactly at HEAD, while the `version`
  file at that commit says `3.8.3` (worktree vs `HEAD:version` → IDENTICAL).
  Not local dirt, not an install fault: keep naming the source, and read the
  pair as a baseline relation rather than a contradiction.
- **The installed skill is a symlink into the read-only checkout** (`:357`):
  "installed vs upstream" content drift is structurally impossible while the
  link holds, so the freshness surface is *link topology* + *checkout motion*.
  Editing anything under `~/.agents/skills/omarchy/` edits the checkout — the
  edit the omarchy skill itself forbids (skill:41, :49); the arm's
  `omarchy.skill.vs_head` row detects it without ever running `git status`.

Drift classes and verdict mapping: C1 release markers · C2 checkout motion ·
C3 link topology · C4 skill content → verdict-bearing (**any MOVED → DIVERGED
naming the pin**); C5 docs register · C6 surface counters · C8 install-time
ordering → record-level NOTEs; C7 probe unavailable → **UNKNOWN, never CLEAN**.
Verbs stay read-only (`version`, `theme current`, `commands --json --all`,
`git describe/rev-parse/show/log/ls-tree`, `stat`, `sha256sum`, `readlink`).
Never `git status` on the checkout (it refreshes the index stat cache —
`province-accuracy-selfaudit.md` §3.5), never `git fetch`, never a mutating
verb (`theme set`, `bg next`, `restart *`, `refresh *`, `install *`, `setup *`,
`update`). Register trap measured: `omarchy commands --json` under-reports (267
default vs 282 with `--all`; `upload log` is `hidden=true`) — use `--all` or
resolve by binary.

Hand-forward: **D-1** — the plan lists `omarchy theme current` among the pins,
but the theme is operator-owned mutable state that the gate already treats as a
NOTE (`:1104`, `:1108` at the landed revision); the spec keeps it NOTE-level
while printing HELD|MOVED, so a routine theme change cannot turn the freshness
gate permanently red (literal plan reading = a one-line `NOTE → FAIL`). Landing
conditions for the rows: the four spec scenarios (clean / version MOVED / live
verb unavailable → UNKNOWN / link replaced by a real dir with equal sha) plus
widening the selftest helper plane regexes (`:352`, `:356`, and the round-6
`st_counts_agree` twins at `:371-375`), which today match only the six current
plane ids — new `omarchy.*` rows would otherwise go uncounted.

### Watch arm 2 — remaining planes' live surface (stage c)

`corpus/knowledge/remaining-planes-census.md` (333 L by `wc -l`, 20,512 B, sha
`710e3e289643f2ff…`; M6-3) — census rows, no verdict token (that vocabulary
belongs to the gate). Headlines: the theme plane is 24 generated files + 4
backgrounds under `~/.config/omarchy/current/theme/`; consumers measured — the
wallpaper symlink feeds a live `swaybg` (`-m fill`, layer ns `wallpaper`),
mako's config is a symlink into the theme, waybar/walker/swayosd stylesheets
all `@import` the current theme, alacritty's `general.import` chain covers 3
live windows (alacritty 0.17.0-1; foot/kitty/ghostty absent); session SDDM →
uwsm → Hyprland on `wayland-1` with portals `-hyprland` 1.4.1-2 + `-gtk` live;
hyprsunset absent with its file pin stable; hypridle absent again (F1-class).
Idle transitions stay **UNKNOWN by constraint** (MADO-R4-2) — not widened. The
note adds no gate rows; wiring them in is the (a)-gated extension. Its erratum
E2 measured a transient worth keeping: mako's `notifications` layer surface is
not permanently mapped (two point samples disagree) — read those rows as
probe-window statements, not steady state.

### Census and verdicts at this append

| | Before (round 5) | After (round 6) |
|---|---|---|
| declared planes / row sites | 6 · 106 `row` + 6 `row_from_rc` | unchanged (hardening is selftest-only) |
| selftest | `28/28` | `53/53` |
| live verdict (read-only) | CLEAN (35 pass, 4 notes) | CLEAN (35 pass, 0 fail, 0 unknown, 4 notes), rc 0 |
| file-plane verdict | CLEAN (17 pass, 2 notes; live skipped) | same, rc 0; `boundary.readonly` PASS, combined sha `bb2639d9a980…` |

Both verdicts were re-run by this lane against the landed revision at append
time (`/tmp/w6-mado-m6-4/gate-after-liverun.log`, `gate-after-nolive.log`), and
the gate's sha256 was identical before and after every sweep.

### Open items

- The residual survivors above and the unexercised live-plane body — the next
  hardening pass (the round-7 plan already names the gate's regression mode as
  its candidate).
- Watch arm 1 unlanded (spec + pins ready, D-1 open); watch arm 2 census-only.
  Neither may ship as gate rows without a mutant that kills the clause.
- `LOG.md` entry for round 6 is owed by the scribe/finalizer lane
  (AGENTS.md:3); this lane's write scope was this file only.
- Cosmetic, unchanged by design: the hardened gate still self-labels
  "v1 (round 5 / M5-2)" in `VERSION_STR` and its header (M6-1 §3).