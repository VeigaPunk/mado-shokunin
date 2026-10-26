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

Where to learn more: `corpus/SOURCES.md` (tiered registry, study paths, search log).

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
- **Host-wide package pause until an explicit operator recovery decision:**
  no package transactions or service/compositor mutations. This source-only
  round additionally forbids package queries, live reads (including process
  and compositor probes), input capture, screenshots and producer execution.
  Read already available tagged source instead of installing a help tool.
  All old live/RUN examples are suspended here, including pure-read producers.
  The round-15 rejected-harmed host debt is not cleared; see QUALITY21/M1/M2.

## Config-plane map — who owns this key

`~/.config/hypr/hyprland.conf` is a pure orchestrator: 17 `source` statements, zero
settings of its own (29 lines; MADO-1 §1/§3). Include order *is* precedence — the last
file to set a key wins:

> defaults (`~/.local/share/omarchy/default/hypr/*`, `hyprland.conf:4-12`) → theme include
> (`:13`) → user files (`:16-20`) → toggles glob
> (`~/.local/state/omarchy/toggles/hypr/*.conf`, `:23`) → `ai-usage.conf` (`:29`)
> Erratum (round 12, 2026-10-19): live is now 18 sources / 32 L, last include gkeep.conf — see § Errata (round 12).

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
| bar (waybar) | `~/.config/waybar/config.jsonc`, `style.css` (historical MADO-2 §1) | Historical v0.15.0 process/style/restart observations in MADO-R3-1 §1, not current state | Dated surface/tray ledger MADO-R3-1 §2.3; **no current module-text observation**. A producer invocation cannot reconstruct the current GTK label or rendered bar. For the custom-module source route use §Waybar observation boundary (round 16); no live or producer run this round. | `omarchy restart waybar` remains operator-only |
| launcher (walker) | `~/.config/walker/config.toml` (49 L; packaged table `/etc/xdg/walker/config.toml`, 298 L — MADO-R3-1 §6) | walker 2.17.0 via `app-walker@autostart.service` + `elephant.service`; restart `omarchy restart walker` | file bytes; `systemctl --user status app-walker@autostart`; `hyprctl -j layers` when open (absent when closed); D-Bus `dev.benz.walker` (`org.gtk.Actions.List` → `as 0`); sockets shape-only (MADO-R3-1 §6.7/§6.8) | same |
| notifications / OSD | `~/.config/mako/config`, `~/.config/swayosd/{config.toml,style.css}` (MADO-2 §4) | Mako owns `org.freedesktop.Notifications` (PID-measured); swayosd-server separate | `makoctl mode`; `busctl --user status org.freedesktop.Notifications` | restart/reload commands |
| idle / lock | `hypridle.conf` (19 L, `e7d3b8dd…`), `hyprlock.conf` (43 L, `b8d173dc…`), theme `hyprlock.conf` (5 L, `3ef010e7…`) — the two local configs byte-identical to the shipped Omarchy payload; not sourced by hyprland.conf; daemon declared by default autostart `exec-once` (`default/hypr/autostart.conf:1`); actuator set under `~/.local/share/omarchy/bin/` (MADO-R4-2 §1/§2b) | hypridle 0.1.8 = idle daemon; on/off is the stateless process-toggle `omarchy-toggle-idle` (`pgrep`/`pkill -x hypridle` ↔ `uwsm-app -- hypridle`; routes: bar glyph `config.jsonc:207`, `SUPER CTRL+I` `utilities.conf:30`, menu `omarchy-menu:212`); hyprlock spawned on demand only (`omarchy-system-lock:8-13`, `pidof hyprlock` guard); lock/wake side-effects script-defined — DPMS off ≈3 s after lock, wake restores (MADO-R4-2 §5/§8) | `pgrep -x hypridle` — absent at the 16:00–16:08Z probe (MADO-R4-2 §7); PID 1203349 present 16:11–16:22Z (restarted with the session), absent again by 16:24Z with no stop line (cause `[UNK]`; F1's disappearance pattern recurred) — re-measure before reuse; `systemctl --user is-active` → `inactive`, `is-enabled` → `disabled`; `journalctl --user` boot-start only (F1); file bytes; session sample via `loginctl show-session` (`IdleHint`/`LockedHint`) and `hyprctl -j layers` (no lock surface while unlocked); live idle transitions have no read surface — no lock test allowed | start/stop daemon; `omarchy-restart-hypridle`; firing the chain (`omarchy-system-lock`, DPMS); any lock or idle-interval test |
| sunset / xdph | `hyprsunset.conf` (14 L), `xdph.conf` (4 L) (MADO-1 §8) | separate consumers, outside the include graph; hyprsunset measured absent; xdph portal running (PID epoch-varying — 1920 at MADO-1 §8, 1203662 this pass) | `pgrep -x hyprsunset` (no match); `pgrep -af xdg-desktop-portal-hyprland`; file bytes | start/stop services |
| terminals | `~/.config/{alacritty,foot,kitty,ghostty}/` — only Alacritty installed (MADO-3 §1/§5) | per-terminal binary; `omarchy restart terminal` (omarchy skill:172) | file bytes + `command -v`; colors resolve through the theme include | restart; `omarchy install terminal` |
| theme & wallpaper | `~/.config/omarchy/current/theme/**`, `theme.name`, `current/background` (MADO-3 §4) | every app includes the theme files; rewritten by `omarchy theme set` | `omarchy theme current`; file reads | `omarchy theme set` |

### Which terminal tree is live on this host (round 23; `corpus/knowledge/terminal-trees-r23.md`)

| Situation | Action | Why (anchor) |
|---|---|---|
| A question names `~/.config/foot/`, `~/.config/kitty/` or `~/.config/ghostty/` | Answer "declared bytes, no consumer" first: `command -v <t>` and `pacman -Q <t>` (read-only) | none of the three is installed (terminal-trees-r23 §Host declaration) |
| Someone asks how that terminal would read or reload its config | Quote the pinned upstream route and label it contract, not observation | S140/S146 foot (no runtime reload), S124/S127/S128 kitty (search order, auto reload, ctrl+shift+f5, SIGUSR1), S136/S138/S139 ghostty (`config.ghostty` vs legacy `config`, ctrl+shift+, and SIGUSR2) |
| A change to one of these trees is proposed | Report it as inert until the operator installs the terminal and routes it in `xdg-terminals.list`; never install, start or signal it | install and selection are operator-owned (PROVINCE.md; terminal-route-r17) |

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
| Which Wayland globals the compositor advertises to its portal; is a named global among them | portal journal, not a socket — the portal's own registry view (`xdph-PortalManager.cpp:85` `CPortalManager::onGlobal`, log at `:88`) | `tools/mado-globals.py --live` — one program only, `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`, exact argv, stdin `/dev/null`, env limited to `PATH`/`XDG_RUNTIME_DIR`/`DBUS_SESSION_BUS_ADDRESS`/`LC_ALL`, 30 s timeout, 8 MiB cap — or `--journal-file P`; exit map 0/1/2/3/4/5 in § "Advertised Wayland globals" | `[OBS]` for the advertised set as the portal logged it; what a client got is outside this read |
| Does the size a window rule asks for match the size the compositor reports for that client? | two read-only inputs, no new verb: file bytes (the `size` rule line) + hyprctl live (`clients`, which prints the animation goal box) | `hyprctl clients -j \| python3 tools/mado-geometry.py --clients - --rules <file>`; per-verdict licence and exit map in § "Rule size versus reported size" | `[OBS]` for both printed sides (the rule text and the goal box); rendered size, the client's own request and rule attribution stay `[UNK]` |

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
| `python3 tools/mado-globals.py --journal-file <journal>` / `--live` | which Wayland globals the compositor advertised to its portal, as the portal's journal logged them: per-session `MADO_GLOBALS_SESSION:` lines, one sorted `MADO_GLOBAL: name= ver= count= class=` line per latest-session global, the `MADO_GLOBALS:` summary (interfaces, classes, `ignored=`, verdict); `--diff` drift between the last two sessions; `--expect NAME` presence | round-41, journal sha256 `bf8fa91a…`: 2 sessions (pid 1918 boot `-`, pid 1952 boot `7ab69ee4…`), 63 interfaces / 63 adverts in the latest; `MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab`; final `MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4 expected_missing=- ignored=0 verdict=OK` |
| `hyprctl clients -j \| python3 tools/mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf` | whether a `windowrule = size W H, match:class RX` line's size matches the size the compositor reports for the client that line matches: a read-only join of config bytes and one `clients` dump, per matched client AGREE / DIFFER / TILED / BADSIZE; `--selftest` | host run 2026-10-26 (no gkeep window open): `MADO_GEOMETRY: rules=1 float_rules=1 other=1 unsupported=0 clients=4 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT`, rc 3; the size line it parsed: `MADO_GEOM_RULE: n=2 file=1 effect=size arg=420x500 class=^(org.omarchy.gkeep)$`; per-verdict licence in § "Rule size versus reported size" |

### Advertised Wayland globals

`python3 tools/mado-globals.py --journal-file <journal>` parses the portal unit's `short-iso` journal (`xdph-PortalManager.cpp:85-88` logs one line per advertised global) into sessions; `--live` runs
exactly one program, `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso` (stdin `/dev/null`, env `PATH`/`XDG_RUNTIME_DIR`/`DBUS_SESSION_BUS_ADDRESS`/`LC_ALL`, 30 s timeout,
8 MiB stdout cap; capture the journal by redirecting that same command to a file). Output: `MADO_GLOBALS_SESSION:` per session; one `MADO_GLOBAL: name= ver= count= class=` per latest-session global
(sorted by name); `MADO_GLOBALS_DIFF:` under `--diff`; a `MADO_GLOBALS:` summary with `ignored=` and verdict.

Exit map: 0 `OK` · 1 `MISSING_EXPECTED` (`--expect NAME` absent) · 2 `SETUP` (usage/unreadable/too_large/bad_expect) · 3 `NO_SESSIONS` · 4 `UNRECOGNIZED_FORMAT` · 5 live-journal failure
(journalctl_unusable/journalctl_failed/journalctl_too_large). UNRECOGNIZED_FORMAT = every `Got interface:`-bearing line failed the grammar (`sessions=0`, `ignored>0`) — another `journalctl -o` format, level
or spacing — never a silent NO_SESSIONS; partially foreign journals pass with `ignored=N`.

Class is a fixed table over names: focus-grab, input-synthesis, input-capture, session-lock, idle, clipboard, capture, toplevel-control, output-control, sandbox, else `other`. Advertising a global is not
proving a capability: the census reports `class=` only — no socket, no client, nothing exercised. Real runs on the round-41 journal (second sample: same run with `--expect zwlr_screencopy_manager_v2`, rc 1):

    $ python3 tools/mado-globals.py --journal-file .ufo/waves/round-41/fetch/xdph-journal.txt
    MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab
    MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4 expected_missing=- ignored=0 verdict=OK
    MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4 expected_missing=zwlr_screencopy_manager_v2 ignored=0 verdict=MISSING_EXPECTED

### Rule size versus reported size

`python3 tools/mado-geometry.py --clients <dump|-> --rules <file>…` joins two caller-supplied read-only inputs: the
`windowrule = size W H, match:class RX` and `windowrule = float on|off, match:class RX` lines of Hyprland config files,
and one `hyprctl clients -j` dump. It starts no process, opens no socket and reads no config tree of its own — the caller
runs `hyprctl clients -j | python3 tools/mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf`. Output: one
`MADO_GEOM_RULE:` line per supported rule, one `MADO_GEOM_CLIENT:` line per matched client, then a `MADO_GEOMETRY:` summary.

Support ceiling (round-43 wave w2, `CritC1Capability` F3): only a `windowrule` line whose single criterion is `match:class` is
counted; `match:tag`, `match:title`, any extra `match:` field, `windowrulev2` and the block form are dropped (size and float lines
alike are counted in `unsupported=`), and `source` statements are not followed, so pass every rule file yourself. On 2026-10-26 the
tool reads 3 of the host's 7 size rules across the sourced files, and `--rules ~/.config/hypr/hyprland.conf` alone returns `rules=0`,
`NO_SIZE_RULES`, exit 4 (`.ufo/waves/round-43/w2/CritC1Capability/findings.md`).

What the reported size is. The `clients` reply prints `"size": [{}, {}]` (`Hyprland-HyprCtl.cpp:395`, command
registered at `:2007`) from `w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL)` (`:427-428` in the JSON format, `:448`
in the plain one), and `GEOMETRIC_GOAL` is `m_realSize->goal()` while `GEOMETRIC_CURRENT` is `m_realSize->value()`
(`Hyprland-GeometricMovableAnimated.cpp:19-20`): the dump is the animation's target box, not the value on screen. A rule's
`size` reaches that box only on the floating path: the default floating algorithm reads `m_ruleApplicator->static_.size`
for a window on its first map and takes the box from `calculateExpression` (`Hyprland-DefaultFloatingAlgorithm.cpp:49,55-56`);
the applicator stores the parsed `Math::SExpressionVec2` (`Hyprland-WindowRuleApplicator.cpp:422,426`). The class match is
anchored upstream — `re2::RE2::FullMatch` (`Hyprland-RegexMatchEngine.cpp:16`, `negative:` prefix at `:7-8`) — which is
why the tool uses `re.fullmatch`.

Per-verdict licence — a verdict reads two printed values, it never calls a fault:

| Verdict | Licenses | Does not license |
|---|---|---|
| AGREE | the reported goal box equals the rule's `size` for that client: the rule's size reached this client's goal | that the window renders at that size (the dump prints the goal, not the current value); that the rule is the only writer (a resize, a center or a later effect can set the same value); that the client asked for it |
| DIFFER | the goal box differs from the rule's `size` | a defect or a cause: a user resize, a compositor clamp or a later effect all produce it — a report, not a fault |
| TILED | the matched client is not floating, so the floating algorithm's map branch never ran for it: the tiler, not the floating rule path, set its box | that the rule is inert: at map a non-floating window stores the rule's size as its pseudo size (`Window.cpp:2402-2408`, round-43 pin), which decides the box when the window is pseudo-tiled, and `clients -j` has no pseudo field; nor that a later floating instance of the class ignores the rule |
| BADSIZE | only that there was no size to compare (no `size` value, or not two integers) | any agreement claim |
| NO_MATCHING_CLIENT (rc 3) | no mapped client matched any supported `size` rule — a null observation | that the rule works, or that the file declares none |
| NO_SIZE_RULES (rc 4) | the rules files carry no supported `size` line | anything about a `float`-only or unsupported-grammar file |
| FULLSCREEN (round 44) | the matched client's `fullscreen` field is 2: the state's box replaced the rule's box, so the rule's size is not compared — under the default handler the target box is the monitor's logical box (`.ufo/waves/round-43/fetch/Hyprland-WindowTarget.cpp:90-94`; `fetch-c1/Hyprland-FullscreenHandler.cpp:191-194`), under the scrolling layout's handler a fullscreen column (`ScrollingFullscreenHandler.cpp:197,301-304`, pinned in `.ufo/waves/round-44/w1/ExecFsSemantics/pins/`) | that the rule failed; that the box is the monitor box under a layout-managed handler; what the window will measure when it leaves fullscreen — a floating client's pre-fullscreen box is remembered (`Hyprland-FullscreenHandler.cpp:130-131`, floating only), a tiled client returns to its layout's box, and the dump shows neither |
| MAXIMIZED (round 44) | the field is 1: under the default handler the box is the workspace work area less the window's reserved area (`Hyprland-WindowTarget.cpp:96-105`; `Hyprland-FullscreenHandler.cpp:195-198`), under the scrolling handler a `1.F` column (`ScrollingFullscreenHandler.cpp:232`); not compared | the same as FULLSCREEN; `fullscreenClient` (the client's requested mode) is never read — the request only writes the internal mode the geometry guards read, and `fullscreen` in the dump is that internal value (`fetch-c1/Hyprland-HyprCtl.cpp:431`) |
| NOT_COMPARED (rc 5, round 44) | at least one matched client was skipped for its state and none agreed: no comparison was made | AGREE; and it is not DIFFER either — a dump with any differing client still exits 1 |

Exit map: 0 `OK` · 1 `DIFFER` (at least one matched client differs) · 2 `SETUP` (usage | unreadable | too_large |
bad_json) · 3 `NO_MATCHING_CLIENT` · 4 `NO_SIZE_RULES` · 5 `NOT_COMPARED` (round 44).
Round 44 adds exit 5 `NOT_COMPARED` (tested after `NO_MATCHING_CLIENT`, before `OK`); a dump with no maximized or
fullscreen matched client prints the round-43 summary line byte for byte, so the round-43 contract still holds
(`quality/counters/c1-r44-geometry-states-v2.py` clause r) — a one-way implication: a fullscreen client classed BADSIZE
also prints the round-43 line. Correction (round-43 closure D3, corrected by round-44 w2 `CritSkillLicence` F3): the
TILED row's Licenses cell can be read as ruling the rule out, and that reading is false for a pseudo-tiled client — the
rule's size is stored as the target's pseudo size at map (`.ufo/waves/round-44/fetch/Hyprland-Window.cpp:2402-2410`)
and the tiler sizes to it (`.ufo/waves/round-43/fetch/Hyprland-WindowTarget.cpp:197-215`, scaled down when it does
not fit), while `clients -j` has no pseudo field; read TILED as "not floating" only.

Host run 2026-10-26, no gkeep window open: the gkeep rule file declares `size 420 500` and the dump holds four tiled
clients, so nothing matches.

    $ hyprctl clients -j | python3 tools/mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf
    MADO_GEOM_RULE: n=1 file=1 effect=float arg=on class=^(org.omarchy.gkeep)$
    MADO_GEOM_RULE: n=2 file=1 effect=size arg=420x500 class=^(org.omarchy.gkeep)$
    MADO_GEOMETRY: rules=1 float_rules=1 other=1 unsupported=0 clients=4 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT

NO_MATCHING_CLIENT is not "the rule works": it says only that no mapped window carried the class. What a live gkeep
window would report needs that window open — an operator act, not a mado probe, and the rendered size after the
animation stays `[UNK]` either way.

Known limit (round-43 wave w1, `RevRefTool` V1): the match is Python `re.fullmatch`, which backtracks. A rule regex
inside the accepted alphabet with an alternation under a repeat, such as `(a|aa)+$`, makes the tool hang on a long
class string (`"a"*38+"b"` takes about 4.6 s; about 1 KB never finishes) with no output at all. The gkeep rule
regex is a plain anchored literal, but a client chooses its own class: run the join as
`hyprctl clients -j | timeout 5 python3 tools/mado-geometry.py --clients - --rules <file>` and treat exit 124 as
"no verdict", never as a verdict. RE2, which Hyprland uses, does not backtrack, so this is the tool's limit, not the compositor's.

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
   **Round-16 override:** no producer execution, even pure-read/contained.
   Producer text, tooltip and provider metadata are session material; the
   source-only scope supersedes the historical conditional license above.
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
| "What is the bar showing right now?" | `[UNK]`; a producer sample is not the current bar label or pixels | Source-only route: `corpus/knowledge/waybar-observation-boundaries-r16.md` (S053/S054). No producer, signal or live probe is authorized this round; a later rendered observation needs separate authorization. |
| Weather chip vanished | `.unavailable` class collapses the module by design when offline | check the network path in `weather.sh`; `style.css:75-79` (MADO-R3-1 §7) |
| "Did my window rule apply?" | 0.56.2 has an *effect* read, not a *match* read: `getprop` returns the applied value with no rule attribution | `hyprctl getprop address:<addr> <prop>` (pick the window by class/address from `clients -j`, never titles); several rules can yield the same value (MADO-R12-1) |
| "Which portal backend serves this?" | `XDG_CURRENT_DESKTOP` selects `<desktop>-portals.conf`; its ordered list meets each backend's `.portal` `Interfaces=` — a running service proves neither the route nor consent | read `/usr/share/xdg-desktop-portal/hyprland-portals.conf` + `portals/*.portal`; D-Bus property reads only, never a request (MADO-R12-3) |
| "Is hyprlang still supported?" | Lua is the forward config since 0.55; hyprlang kept "for 1 - 2 releases starting from 0.55" | `hyprctl version`; `hyprctl systeminfo` `configProvider`; re-check on every release (MADO-R12-2) |
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

## Current diagnostic boundaries (round 13)

For protocol phase and advertised globals, use
[`wayland-protocol-boundaries-r13.md`](corpus/knowledge/wayland-protocol-boundaries-r13.md)
(S005, S040–S043; observer implementation S046). Read the owning protocol repository for phase; read the
sanitized `wayland-info` inventory for interface/version advertisement.
Neither route proves feature behavior. Do not infer HDR, monitor
reconfiguration or input delivery from a global's presence.
The earlier round-12 `wayland-info` absence was a dated observation:
round 13 installs `wayland-utils 1.3.0-1` through pacman for this read route.
Host configurations and compositor actions remain operator-owned.

### Output/colour and source-target boundaries (round 14)

Use [`output-colour-boundaries-r14.md`](corpus/knowledge/output-colour-boundaries-r14.md)
for S047's exact output test/apply/outcome contract and S048's manager
support events versus immutable output/surface image descriptions.
Successful validation is not successful apply; even apply success need
not exactly match requested properties. Colour metadata is not measured
panel luminance or HDR rendering. S041 is historical advertisement only.
The U4 appended R13-V1 erratum and S049 clarify that **global records**
are interface/version pairs while sanitized probe/session metadata also
remains in the enclosing artifact.

**Never assume dry-run safety from the XML.** S050's tagged Hyprland
`efb5099` source returns true through a test stub, and `disable_head`
saves disabled state/schedules reload before any later test/apply.
These are static source facts, not a measured host failure or binary
equivalence claim. Treat the whole configuration-building transaction
as mutation-class and operator-owned. Binding can also deliver head
identity before explicit configuration requests; no requests is not
no received identity. The U5 note carries exact source anchors.

For the gate's supported declared-source policy, every direct target
and every matched glob member must be a regular file; file symlinks
are followed. `hypr.root.sources_resolve` names `non-regular:` versus
`unresolved:`; it does not claim Hyprland itself raises a config error
for targets that its parser may skip. Exact set membership and positional
order remain separate checks. Named directory fixtures are the measured
new subset; the order-swap fixture preserves existing behavior, not a
new feature. Generic hyprlang grammar and expanded-glob membership policy
remain unclaimed.

Standalone round-14 selftest evidence records its resolved measured
commit, raw whole-gate SHA-256, exact command and actual exit in the
receipt itself (R13-V3). `boundary.readonly` means unchanged configuration
bytes within that run, not identical outputs across code revisions
(R13-V2). Historical outputs are not retroactively rewritten.

### Input debugging and tooling safety (round 15)

Use [`input-debugging-boundaries-r15.md`](corpus/knowledge/input-debugging-boundaries-r15.md)
(S051/S052) for the documented helper-context → compositor-policy →
client-focus → application-outcome ladder. `list-devices` reports library
defaults, not desktop settings; `getoption` is a config read, not applied
per-device state or delivery. Registry advertisement is not capability
bits or focused-client receipt, and a keycode is not inserted text.
Actual input delivery, toolkit/IME behavior and kernel causes stay `[UNK]`.
XML v11 does not establish host support above the historical advertised v9.

The standing no-injection/session-material fence expressly excludes raw
input-device access, debug-events/debug-gui/evtest, record (including
`--no-events`), replay/uinput/virtual-keyboard clients and protocol dumps.
No raw keycodes, keymap contents, timings, device identity or input
recordings are retained. Device inventory rechecks keep only counts/shape.
This prohibition is policy regardless of root, group membership or binary
availability. Upstream bug-report commands are source data, not permission.

**Tool installs are not exempt from host safety.** Round-15 LibinputEvents
upgraded the already-installed input library while the host was not fully
updated; the orchestrator ruled this a forbidden partial upgrade.
Before any future install, `pacman -Sp --print-format '%n %v' <pkgs>` must
list only not-already-installed packages. Compare every planned package
name with installed names, including dependencies; any overlap goes to L0,
not an install. No further pacman operations, downgrade/revert or compositor
restart in round 15. The operator owns remediation. See
[`round-15.md`](corpus/lessons/round-15.md) M2 and QUALITY 20.

**Round-16 superseding instruction:** all pacman transactions are currently
paused host-wide. Do not even obtain a fresh package plan for this task;
never downgrade, reinstall, remove packages or restart host services.
Criterion 20's real full-plan/installed-name comparison is conditional on a
future explicit operator lift and installation authorization, not a way
around the pause. The prior in-memory overlap fixtures are not production
validation. R15-V1 remains operator-owned; R15-V2 and the disclosed no-live
probe breach become QUALITY 21 and round-16 lesson M1/M2. Old live command
tables describe dated routes, not authorization for this round.
This version of the static classifier always requires paused=true. It cannot
authorize a post-lift installation; that would require separately reviewed
instructions/policy, not editing its input to manufacture permission.

R14-V1's three provisional mutation receipts remain historical derived-target
evidence, not standalone final-full-gate receipts. The appended standing-use
erratum maps each header to the exact committed-derived executable without
restamping pre-commit runs as `measured_commit`.

### Waybar observation boundary (round 16)

Use [`waybar-observation-boundaries-r16.md`](corpus/knowledge/waybar-observation-boundaries-r16.md)
(S053/S054) to separate producer stdout, parser fields, format/visibility,
GTK markup and rendered appearance. A fresh producer result is not the
current bar label. The historical `RUN` route elsewhere in this file is
superseded for the question “what is showing now?”: actual module text,
tooltips, alt/provider payloads and pixels are unmeasured session material,
not permission to execute a producer or collect private output. This
round is source-only; no screenshot, refresh signal or service launch.
Tagged source is not proof of the installed binary or current behavior.
The seven-item documentary rubric can complete while these remain unknown.
The sourced route covers custom modules only; built-in module contracts
remain unsourced. Old screenshot/RUN recipes are not standing authorization:
an operator must name the exact producer/capture, allowed data and retained
destination before any later execution. Producer fields and screenshot
pixels may contain private session data; without that authorization, keep
them shape-only. Launching/restarting Waybar also runs configured producers
and hooks, so a rendering request alone does not authorize a launch.

### Post-hoc transcript tripwire (round 17)

After every wave and before writing anything about seat conduct, run
`python3 -I tools/mado-tripwire.py --scan <session-dir>/<Lane>R<N>` over the
round's seat transcripts (no `--permit` while the host pause holds) and
quote its first line, `counts` and `unparsed_spawns`. A finding is an
issued command to disclose in the lesson, not a host-state fact: confirm
package transactions against `/var/log/pacman.log` by timestamp (UTC in
transcripts, -0300 in the log) using the call's `custom/tool_execution_start`
time — a record's own timestamp can be minutes late for provider-history
records holding many calls. Round 17 found, in rounds 13-16, every disclosed
package transaction plus undisclosed elevated/query calls (lesson
`round-17.md` M2); breaches outside its classes (jj, /proc reads, file
misroots) are not findings. Its `--scan` entry stays a probe: it reads mutable
transcripts. Round 18 adds the gate entry `--frozen` (registry row
`mado-tripwire-frozen`): a digest-pinned replay of committed incident lines.

### Reading tripwire rows — observed vs lead; fail-closed harnesses (round 20)

Every finding row carries `evidence` (tool `a57d4fe9…`, commit `a8960de`; knowledge
`corpus/knowledge/tripwire-precision-r20.md`). `observed`: the transcript states the
command and the path that runs it (bash text, `!`/`%%bash`, a literal spawn or spawn alias,
or a helper whose body is visible in the same file and is called with bindable arguments —
earlier py cells count until a `reset`). `lead` has two sources: a literal host argv
handed to a callee whose body is not visible (an unbound name, a non-stdlib import, a
parameter, a spawn-named method of an unresolved object), and a visible body the executed
text reaches without a followed call (a thread target, callback, decorator, returned
closure, inline lambda, dunder of a constructed class, a coroutine created without
`await`, a recursive or over-depth helper) — "may run", not "ran". A lead stays in
`findings` and exits 1 unless its class is permitted; the verdict adds
`observed_findings`/`lead_findings`. Report them apart — "6/6 incident lines flagged = 5
observed + 1 lead", never a bare 6/6 — and never write a lead as a command that ran. Pure
data gives no row: builtins (S105) and callables of stdlib modules that cannot start a
process, run code text or call back (`deque`, `shlex.join`, `json.dumps`, `heapq`,
`copy`, `os.path`, …; S106, S107, S113–S115) unless the text rebinds the name; `del` of
a shadowing name at module level restores the builtin (S111); a body nothing references
gives no row. VCS help and dry runs are not writes: git `-h`/`--help` as a flag, `git
help`, `commit --dry-run|--short|--porcelain|--long|-z`, `add`/`push -n|--dry-run`, also
inside a short cluster (`-nv`) (S099–S102), `jj … -h|--help` and `jj help` (S103), and
`jj --ignore-working-copy git push --dry-run`; still writes: `git commit -n`
(`--no-verify`), `git commit -m --help` (a message), `pull -n`, plain `jj git push
--dry-run` (it snapshots first; S104), `jj -R git … git push` (the subcommand is found by
position), a `jj <alias> --help` whose verb is unknown or variable (a user alias runs
its command), and any form in an unparsed (`/unparsed`) segment, whose tokens may belong
to the next command. Measure, do not assert: `python3 -I .ufo/waves/round-20/tw-precision.py REV`
(175 cases, families P/S/W/H/L; QUALITY 30) for what a change adds, and `python3
.ufo/waves/round-20/a2/a2-guards.py REV --fixtures-rev 6a7d9ca` for what it drops (recall
losses, crash flips, pure-data rows, VCS truth) — a detector change read only for
precision hid 52 recall losses in round 20 (lesson M9). Still unanalysed: scripts
written then run, shell aliases, dynamic dispatch, JavaScript cells, other sessions — a
`clean` verdict bounds only the covered forms.

Any harness that stubs a host binary for a hermetic run fails closed (QUALITY 29): test
each setup step on its own (`mount … || exit 125`, then `cmp` the target against the stub
`|| exit 125`), never rely on `set -e` across a `&&` list (S110), and check the harness
with `bash .ufo/waves/round-20/isolation-check.sh HARNESS` before it runs anything real.
`.ufo/waves/round-20/isolate.sh` passes that check; it is not a sandbox (the environment
and the compositor/session sockets stay reachable) and gives no licence to run a host
probe while the host pause binds.

## Gate registry

This `SKILL.md` is the registry home, per `PROTOCOL.md` §Gate standard,
Registry. Commands run from this lane's root. Record the measured commit alongside ordinary output;
`--snapshot FILE` also records the gate digest. Historical usage sections
below retain their original revisions, not current instrument pins.

| name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| mado-verify | gate | `bash tools/mado-verify.sh` (default live; `--no-live` explicitly skips live; `--root DIR` for isolated roots; `--snapshot FILE` for digest-bearing receipt) | 0 clean; 1 failed (FAIL or required UNKNOWN; read counts); 2 could-not-evaluate (usage or snapshot refusal); other could-not-evaluate; snapshot preserves child 0/1 | `bash tools/mado-verify.sh --selftest`; `--selftest`: 0 clean, 2 failed (assertion failure), other could-not-evaluate | `tools/mado-verify.sh`: `EXPECT`, `LOCAL`, omarchy/theme and live-version pins; fixture expectations in `selftest()` | no configuration writes; selftest uses `/tmp/w5-mado-m52-selftest.*`; snapshot writes caller-selected non-config destination only and refuses an existing file | mado |
| mado-regression | gate | `MADO_VERIFY_HARNESS=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh bash tools/mado-verify.sh --regression` | 0 clean (PASS); 1 failed (FAIL); 2 could-not-evaluate (SETUP or usage); other could-not-evaluate | `bash tools/mado-verify.sh --selftest`; hermetic regression scenarios assert codes and ids | `tools/mado-verify.sh`: `PIN_MADO`, `SPEC_SHA`, `TABLE_MADO`, embedded spec body; target excludes documented R7/R8 blocks | `/tmp/mado-verify-regression.*`, retained on FAIL/SETUP or `--keep`; sibling harness read-only | mado |
| mado-snapshot-diff | gate | `bash tools/mado-verify.sh --snapshot-diff OLD NEW` | 0 clean (SAME or detail-only change); 1 failed comparison (class or scope changed, not a desktop-health verdict); 2 could-not-evaluate (SETUP or usage); other could-not-evaluate | `bash tools/mado-verify.sh --selftest`; snapshot scenarios assert codes and row ids | v1 format and comparison expectations in `tools/mado-verify.sh`; caller supplies both receipts | read-only inputs | mado |
| mado-frozen-regression | gate | `python3 .ufo/waves/round-13/frozen/verify.py` | 0 clean (`frozen_match`); 1 failed (`frozen_verdict_mismatch`); 2 could-not-evaluate (`snapshot_tampered` or `frozen_error`); other could-not-evaluate | same command with `--selftest`; 0 clean, 2 failed; isolated fixtures assert exit and stable id | `.ufo/waves/round-13/frozen/expected.json` pins both `gate.sh` and `harness.sh` before execution plus expected exit/marker | reads committed snapshots; child regression uses isolated temporary trees; selftest temporary fixtures | mado |
| mado-source-merge | gate | `python3 .ufo/waves/round-13/w1/reports/MistakeFix.py --registry corpus/SOURCES.md` | 0 clean; 1 failed merge-review screen (active URL collision); 2 could-not-evaluate (usage/read/parse/policy); other could-not-evaluate | same script with `--selftest`; 0 clean, 1 failed; in-memory fixtures assert exit and named findings | same script: `run_selftest()` expected fixture decisions and `supersedes` policy | read-only; no scope-overlap oracle or network lookup | mado |
| mado-round13-measure | probe | `python3 .ufo/waves/round-13/measure.py REV` | 0 observations printed, not admission; nonzero could-not-evaluate | — (measurement probe, not a verdict gate) | same script: revision-bound source join, U4 facets and four named-case expectations; SCORECARD defines rubric | temporary isolated config fixtures; no live config writes | mado |
| mado-round14-measure | probe | `python3 .ufo/waves/round-14/measure.py REV` | 0 observations printed, not admission; nonzero could-not-evaluate | — (revision-bound observation probe) | same script: U-item reciprocal joins/U5 facets, three regular-target cases and separate preservation controls; SCORECARD rubric | isolated temporary fixtures, never live configuration writes | mado |
| mado-round15-measure | probe | `python3 .ufo/waves/round-15/measure.py REV` | 0 observations printed, not admission; 2 usage could-not-evaluate; other nonzero could-not-evaluate | — (static observation probe, not verdict gate) | same script: revision-bound source/header/navigation joins; U4/U5 preserved, U6 three sections plus unknown and reciprocal S051/S052; SCORECARD rubric | reads committed repo bytes only; no gate execution, fixtures, input-device or config access | mado |
| mado-frozen-regression-r14 | gate | `python3 .ufo/waves/round-14/frozen/verify.py` | 0 clean (`frozen_match`); 1 failed (`frozen_verdict_mismatch`); 2 could-not-evaluate (`snapshot_tampered` or `frozen_error`); other could-not-evaluate | same command with `--selftest`; 0 clean, 2 failed; isolated fixtures assert exit and stable id | `.ufo/waves/round-14/frozen/expected.json` pins gate/harness inputs plus expected exit/marker | reads round-14 committed snapshots; child regression/selftest isolated temporary trees | mado |
| mado-action-plan | gate | `python3 -I tools/mado-action-plan.py --plan PLAN --policy .ufo/waves/round-16/safety-policy.json` | 0 clean within finite declared-kind/name policy (`plan_safe`); 1 failed (blocked kind/name, unknown kind or empty argv); 2 could-not-evaluate (malformed plan/policy or usage); other could-not-evaluate | same script `--selftest`; 0 clean, 1 failed; self-invocation asserts code and finding | script `PINNED_*` and literal selftest expectations; `.ufo/waves/round-16/safety-policy.json`; independent cases `safety-cases.json` | reads supplied regular JSON inputs; selftest isolated temp fixtures; never executes supplied argv | mado |
| mado-action-plan-frozen | gate | `python3 -I tools/mado-action-plan.py --frozen .ufo/waves/round-16/frozen` | 0 clean comparison (`frozen_match`, including expected refused plan); 1 failed comparison; 2 could-not-evaluate (`snapshot_tampered` or `frozen_error`); other could-not-evaluate | same script `--selftest`, includes frozen CLI fixtures | `.ufo/waves/round-16/frozen/expected.json` pins plan/policy input bytes and exact expected code/finding; receipt separately binds executable and expectation digests to measured commit | fixed-name snapshot reads; isolated selftest fixtures only | mado |
| mado-round16-measure | probe | `python3 .ufo/waves/round-16/measure.py REV` | 0 observations only, never admission; nonzero could-not-evaluate | — (static revision-bound probe) | script U1–U6 preserved checks, U7 S053/S054/facets, original literal calibration rule; SCORECARD declares scope | git-show committed repo bytes only; no gate, host or device execution | mado |
| mado-tripwire | probe | `python3 -I tools/mado-tripwire.py --scan PATH [PATH ...] [--permit CLASS ...]` (post-hoc scan of OMP session JSONL; assistant `toolCall` bash commands and python eval `!`/`%%bash`/literal spawns only) | 0 no unpermitted finding (`clean` when there are no findings, `permitted_only` when every finding is waived); 1 at least one unpermitted host_mutation/package_query/live_probe finding (`findings`); 2 could-not-evaluate (usage, refused symlink/`agent.db`/credential name, unreadable, no `.jsonl`, invalid line, internal error); 2 wins over 1 | `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/core` (9), `…/compound` (16), `…/hardening` (33), `…/w2-regressions` (30); known misses pinned in `.ufo/waves/round-17/w2/adversarial` (4/26 by design); 0 all pass, 1 any fail, 2 malformed expected.json; each case self-invokes `--scan` and compares exit plus the exact (class, rule, line[, file]) multiset | rules in `tools/mado-tripwire.py` (class tables at the top); real-transcript receipts `.ufo/waves/round-17/evidence/tripwire-*.txt` bound to `session-index.json` digests | reads only the given JSONL files; writes nothing | mado |
| mado-label-check | probe | `python3 -I .ufo/waves/round-17/label-check.py [CLAIMS]` | 0 every claim ok; 1 any MISMATCH (expected for declared red claims); 2 could-not-evaluate; `EXPECT_SUMMARY` must equal the claim count | — (declared red/green/mutant claims in `.ufo/waves/round-17/label-claims.json` are its controls) | outcome tokens only: `MADO_<NAME>:` verdict word, `finding` values (not under want/expected keys), got-side of selftest rows; optional `measured_commit`; exit = expectation verdict when every claim declares `expect` | claims file read from the worktree; doc and receipt bytes via `git show` | mado |
| mado-round17-measure | probe | `python3 .ufo/waves/round-17/measure.py REV` | 0 observations only, never admission; 2 usage/bad rev | — (static revision-bound probe) | rubric V (P1-P6, exact `surface:` line, pinned legacy U1/U2/U7 paths, upstream relevance, facet floor) and the literal calibration counter; SCORECARD round-17 corrections declare scope | `git show`/`ls-tree` only | mado |
| mado-tripwire-frozen | gate | `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen` (digest-pinned replay of byte-exact incident transcript lines; the `--scan` entry above stays a probe) | 0 clean (`frozen_match`); 1 failed (`frozen_verdict_mismatch`: exit, label, (file, line, class, rule) multiset or a `known_misses` line differs); 2 could-not-evaluate (`snapshot_tampered`: digest mismatch, missing/symlink/escaping/unlisted input; `unpinned_legacy`: entry without sha256; `frozen_error`: malformed expected.json); other could-not-evaluate | `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-18/tripwire/frozen` (17 mode-frozen cases; exit and first-line outcome) plus the four scan suites above | `.ufo/waves/round-18/frozen/expected.json` pins every input sha256, permit, expected exit/label, 8 findings and 3 known misses; `provenance.json` maps snapshot lines to source lines and source digests (`session-index.json`); a receipt binds `tool_sha256` and `measured_commit` | reads committed snapshot bytes only; never reads live transcripts | mado |
| mado-frozen-provenance | probe | `python3 -I .ufo/waves/round-18/frozen-provenance-check.py` | 0 `match` (every mapped snapshot line byte-equal to its source line, source digests equal the round-17 index); 1 `mismatch`; 2 could-not-evaluate (source transcript gone — the snapshot is then the only copy) | — (falsified by one-byte and vanished-source controls in its w1 report) | `provenance.json` and `.ufo/waves/round-17/evidence/session-index.json` | read-only over mutable host transcripts | mado |
| mado-receipt-check | probe | `python3 -I .ufo/waves/round-18/receipt-check.py [CLAIMS]` | 0 every claim meets its declared expectation; 1 any unmet; 2 could-not-evaluate (unreadable receipt/tool, malformed claim, pending rev); `EXPECT_SUMMARY: k/n` | — (declared red/green/mutant claims in `.ufo/waves/round-18/receipt-claims.json` are its controls) | claim file; receipt and tool bytes via `git show` at the named revisions | read-only | mado |
| mado-fetch-verify | probe | `python3 -I .ufo/waves/round-18/fetch-verify.py [--sources corpus/SOURCES.md --rows S072,...] [--quote 'S0NN=<text>']` | 0 every receipt body re-hashes and every listed row is receipted; 1 any bad/unreceipted/missing quote; 2 usage | — (fixture controls in its w1 report) | `.ufo/waves/round-18/fetch/*/receipts.jsonl` (`mado-fetch-receipt-v1`) | read-only | mado |
| mado-pipe-rc-census | probe | `python3 -I .ufo/waves/round-18/pipe-rc-census.py REV` | 0 no unchecked producer site; 1 at least one; 2 usage/bad rev — a screen, never proof (QUALITY 26: the behavioural bite is selftest OM9/OM10) | — | `tools/*.sh` at REV | `git show` only | mado |
| mado-measure-mutants | probe | `python3 -I .ufo/waves/round-18/measure-mutants.py` | 0 every declared mutant met its expectation (`bites`, `no_bite` listed); nonzero could-not-evaluate | — (each mutant is a committed-in-clone red case for one tightening) | instrument digests `a280b3ab…` (`f52f43f`) and `de4c422b…` (`d9a5a18`); mutant diffs in `evidence/measure-mutants.json` | `/tmp` git clones only; never the lane | mado |
| mado-anchor-durability | probe | `python3 -I .ufo/waves/round-19/anchor-durability.py REV [--rows S###,...]` (reads `git show REV:corpus/SOURCES.md`; screens `mined` rows only; prints one `ROW <id>` line per screened row with its verdict tag and reason) | 0 no flagged row; 1 at least one row tagged PER_FETCH_DIGEST or UNPINNED_ALIAS (summary line printed; the probe does not decide defect versus false positive, a reviewer does); 2 usage or could-not-evaluate (unreadable REV or SOURCES.md) | — (contract control, unobserved until landed: REV `17661e0fa83f978fb659f5bb8fef47f0969f6945` must flag S094 PER_FETCH_DIGEST and S084 UNPINNED_ALIAS) | `corpus/SOURCES.md` at REV; receipts at REV under `.ufo/waves/round-1[0-9]/fetch/*/receipts.jsonl` (digest-collision arm only); rule constants in the script header | reads committed bytes via `git show` only; writes nothing | mado |
| mado-supersede-sweep | probe | `python3 -I .ufo/waves/round-19/supersede-sweep.py REV [--ledger PATH]` (for each owned file in ledger scope that contains the `old` value: prints `STALE <path>` unless the file holds a line with the `new` value and a ledger row id; prints `POINTED <path>` otherwise) | 0 no STALE line; 1 at least one `STALE <path>`; 2 usage, bad REV or unreadable ledger | — (contract control, unobserved until landed: REV `17661e0fa83f978fb659f5bb8fef47f0969f6945` must print 11 STALE of 13, the set `fresh-pins.py` also reports at that REV) | `.ufo/waves/round-19/supersessions.json` (ledger id `walker-2.17.2`: old `2.17.0`, new `2.17.2`, rows S090 and S096, scope `corpus/knowledge/*.md`, `corpus/README.md`, `SKILL.md`, `PROVINCE.md`, `tools/*`); default `--ledger` path [UNK] until landed | reads committed bytes via `git show` only; writes nothing | mado |
| mado-landed-check | probe | `bash .ufo/waves/round-19/landed-check.sh LANE_DIR HASH...` (resolves the remote tip live with `git -C LANE_DIR ls-remote origin refs/heads/master`; prints one `LANDED`, `LOCAL_ONLY` (with reason) or `MISSING` line per HASH) | 0 every HASH LANDED (object present and ancestor of the live remote tip); 1 any LOCAL_ONLY or MISSING; 2 usage or could-not-evaluate (not a directory or repo, no origin, no refs/heads/master on origin, ls-remote failure, ancestry error) | — (no committed selftest; the author's controls are a `/tmp` clone with a bare `/tmp` remote: commit ahead, behind, unknown hash) | none; the remote tip is read live from `origin`, never from a cached remote-tracking ref | network read (`git ls-remote origin`); no fetch, no git write, never invokes jj | mado |
| mado-frozen-repin | probe (writes a caller-selected DIR; see note D1) | `python3 -I .ufo/waves/round-19/frozen-repin.py --from .ufo/waves/round-18/frozen --to DIR --tool PATH [--allow-new-findings]` (copies pinned inputs byte-exact after a sha256 check, runs `--scan` in DIR, writes DIR/expected.json schema `mado-tripwire-frozen-v1` and DIR/README.md with a RECEIPT first line) | 0 DIR written; 1 refused, no write (a source expected finding disappears, or a finding lands on a line that is neither expected nor a known miss, unless `--allow-new-findings`); 2 usage or could-not-evaluate (pinned input digest mismatch, unreadable source, malformed expected.json) | — (contract controls, unobserved until landed: the current tool gives an identical expected.json with known misses kept; a `/tmp` tool copy with a toy rule flagging `pacman -Q` inside strings turns known misses into findings; a mutant dropping a finding exits 1) | `.ufo/waves/round-18/frozen/expected.json` and its input digests (source pins); DIR is caller-selected and outside the lane | writes only the caller-selected DIR (DIR-exists rule [UNK] until landed); reads round-18 frozen inputs; writes no lane file | mado |
| mado-tw-recall | probe | `python3 -I .ufo/waves/round-19/tw-recall.py REV` (fixed denominator: the 6 incident (file, line) pairs of `.ufo/waves/round-18/frozen/expected.json` at 9c54c56; runs REV's `tools/mado-tripwire.py --scan` on the pinned inputs; score = 10 x detected / 6) | 0 JSON printed (any score, 0 included; no pass/fail verdict); 2 could-not-evaluate (usage, unknown REV, pinned input digest mismatch, `git show` failure, scan rc outside 0/1 or no verdict line) | — (the fixed denominator and digest pins are its only controls; precision on control lines is not measured) | `.ufo/waves/round-18/frozen/expected.json` and its input digests at `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`; REV's tool sha256 printed as provenance | reads committed bytes via `git show`; writes only a temp dir it removes | mado |
| mado-fresh-pins | probe | `python3 -I .ufo/waves/round-19/fresh-pins.py REV` (fixed denominator: the 13 owned files at 9c54c56 that contain `2.17.0`; a file is current at REV when a line holds `2.17.2` and an `S###` token; score = 10 x current / 13) | 0 JSON printed (any score, 0 included; no pass/fail verdict); 2 could-not-evaluate (usage, unknown REV, `ls-tree` or `git show` failure) | — (the fixed denominator and the pointer regex are its only controls; row-id validity is not checked) | `PIN_REV` `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`, `OLD` `2.17.0` and `POINTER` regex in the script | reads committed bytes via `git ls-tree` and `git show` only; writes nothing | mado |
| mado-assessment | gate | `python3 -I tools/mado-assessment.py --check BUNDLE --root ROOT` | 0 clean; 1 failed integrity assertion; 2 could-not-evaluate malformed/incomplete/unreadable input; other could-not-evaluate | `python3 -I tools/mado-assessment.py --selftest .ufo/waves/round-21/assessment-fixtures`; `--selftest` verifies codes, result labels and stable finding ids | `.ufo/waves/round-21/assessment-fixtures/{seal.json,expected.json,cases,snapshots}`; seal SHA pinned in gate | read-only actual assessment/input bytes; selftest spawns only this gate; no classifier, Git, network or host probes | mado |
| mado-r26-counter-selftest | gate | `python3 -I .ufo/waves/round-26/quality/counter-selftest.py [--c1 PATH] [--c2 PATH] [--rev REV] [--scratch DIR] [--keep]` | 0 clean only when every check passes (`SELFTEST pass=N total=M`); 1 failed assertion; usage or uncaught setup errors are not a pass. | The entry command is the self-test itself; there is no `--selftest` flag. `counter-selftest-green.txt` records 9/9 and exit 0; mutated-counter negative runs are in `counter-selftest-red.txt`. | `counter-selftest.py` pins `c1/count.py` at `f98e264b…d352cd` and `c2/count.py` at `b92c32da…a716a8`; evidence: `.ufo/waves/round-26/quality/counter-selftest-green.txt` and `counter-selftest-red.txt`. M26-8: the active C1-v2 compatibility baseline fails 7/9, and 6/10 self-test mutants survive (`.ufo/waves/round-26/w2/reports/MutSelftest.md`). | Imports the two counters and substitutes offline synthetic harness surfaces; uses temporary scratch under `/fast/scratch/hyaku/mado-r26` by default, removed unless `--keep`; no home-config, oracle, or compositor writes. | mado |
| mado-r26-population | gate | `python3 -I .ufo/waves/round-26/quality/check-population.py --registration PATH RECEIPT [RECEIPT ...]` | 0 PASS when each parsed denominator, CASE-line count, and registered total agree; 1 FAIL on a population mismatch or unregistered predicate; 2 UNREADABLE when inputs cannot be read or parsed for comparison. | No built-in self-test flag or runner. The recorded red/green matrix invokes the entry command over the synthetic fixtures and committed before-receipts; see `.ufo/waves/round-26/quality/q37-population-red-green.txt`. | Registered totals are read from `.ufo/waves/round-26/registration.md`; implementation `.ufo/waves/round-26/quality/check-population.py` sha256 `803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64`. Evidence: `q37-population-red-green.txt`. M26-8: the five committed population fixtures missed 3/6 mutants; survivors were CASE-anywhere, first-PRED-only, and parse-error exit 0 (`.ufo/waves/round-26/w2/reports/MutQ37.md`). | Reads registration and receipt text only; writes nothing and runs no counter. | mado |
| mado-r26-control-receipts | gate | `python3 -I .ufo/waves/round-26/quality/check-control-receipts.py --round N --data-registry PATH [--repo PATH] [--tip REV] [--shapes S1,S2,...] [--any-md] [--counter-sha SHA]` | 0 PASS when the oldest qualifying receipt commit is strictly before registry `createdAt` and all requested shapes are covered; 1 FAIL otherwise; 2 UNEVALUABLE when tip/history/registry cannot be evaluated. | `python3 -I .ufo/waves/round-26/quality/q36-fixtures/run_fixtures.py --out .ufo/waves/round-26/quality/q36-mutants.txt`; recorded result: 8/8 mutants killed across 10 fixtures, exit 0 (`q36-mutants.txt`). | The checker reads the requested tip's Git history/blobs and registry `createdAt`; optional `--counter-sha` values are caller-supplied. Evidence: `.ufo/waves/round-26/quality/q36-mutants.txt`. M26-8: this checker only enumerates `.md` receipts, so round-26 `.txt` controls are excluded and its round-26 gate fails; see `corpus/lessons/round-26.md` M26-8 and the round-27 successor assignment. | Read-only Git history/blob queries; no repository, config, or receipt writes. Fixture repositories are synthetic and isolated under `/fast/scratch/hyaku/mado-r26/q36`. | mado |
| mado-r27-counter-selftest | gate | `python3 -I quality/counter-selftest.py --c1 PATH --c2 PATH --rev REV` (from the lane root; R27 counter runs the suite on fresh clones) | 0 every fixed check passes; 1 any check fails or a counter cannot be loaded. | No separate self-test flag; the command runs the fixed synthetic checks and inventory. Exercised as suite A by `.ufo/waves/round-27/c2/count.py`; aggregate measurement: `.ufo/waves/round-27/evidence/c2-after-0b53bd86.txt:5,64-65`. | LANDED; source `quality/counter-selftest.py`; added by `5c1d4957eb63ff57afb3f048b81eec8b7eba0d8e`; current blob SHA-256 `aa0e14d160b8429b945f12329e5673a1d484986d1b617a05920a92e77a1d4898`. | Reads supplied counter files; synthetic/offline cases use temporary scratch (removed unless `--keep`); no Hyprland execution. | mado |
| mado-r27-population-suite | gate | `python3 -I quality/population-suite.py --checker PATH` (from the lane root; R27 counter runs the suite on fresh clones) | 0 every built-in fixture meets its expected exit/verdict/report; 1 any fixture fails or times out; missing checker reports exit 2. | No separate self-test flag; the command itself runs the built-in fixtures. Exercised as suite B by `.ufo/waves/round-27/c2/count.py`; aggregate measurement: `.ufo/waves/round-27/evidence/c2-after-0b53bd86.txt:5,64-65`. | LANDED; source `quality/population-suite.py`; added by `5c1d4957eb63ff57afb3f048b81eec8b7eba0d8e`; current blob SHA-256 `99e7d876c1fcf2585354a22eff9d1c674c902ad1108e19ea50c9caa49eb3046c`. | Runs checker against built-in synthetic fixtures in a temporary directory, removed on exit; no lane or host-config writes. | mado |
| mado-r27-control-receipts | gate | `python3 -I quality/check-control-receipts.py --round N --data-registry PATH [--repo PATH] [--tip REV] [--shapes S1,S2,...] [--seeds N] [--receipt-glob PATTERN ...] [--any-md] [--counter-sha SHA]` | 0 PASS only when the oldest qualifying receipt commit precedes registry `createdAt` and every named shape has at least `--seeds` distinct receipts; 1 FAIL otherwise; 2 UNEVALUABLE when tip/history/registry cannot be evaluated. | Fixture runner: `.ufo/waves/round-27/quality/q36-successor-receipts.txt`; the receipt records red/green fixture results and the checker's behavior. | LANDED; source `quality/check-control-receipts.py`; added by `b6650d583924d670c9e98594ffb1c6f25e8e7682`; current blob SHA-256 `2233db1d489fa325c3b4bd9b5b1dccc68eb9311864a0d975303907463fa65af2`. | Read-only Git history/blobs and receipt text; fixtures use isolated synthetic repositories under `/fast/scratch/hyaku/mado-r27/q36`. | mado |

Round-16 classifier limit: `plan_safe` means only no blocked declared kind
and no listed argv[0] basename. It is **not** credential/privacy safety,
no-live-probe clearance, destination confinement or permission to execute.
Unlisted wrappers/interpreters (including `omarchy-pkg-add` and `python3`)
pass the finite screen; operand paths are not analyzed. Residual controls
record this explicitly. It does not intercept actual tool calls; the
round-15 incident was undeclared/ungated and is not prevented or repaired.
Frozen match means recorded comparison matched, never that a red plan is
safe. The existing verifier defaults live and is not run in that mode this
round; only isolated selftest and committed digest are harm-watch evidence.

Round-17 tripwire limit: detection after the fact over the files given,
never interception, prevention or host repair. It records commands
*issued* (tool results are ignored), so a refused call still counts and a
successful harmful call cannot hide behind `isError`. `clean` means no
finding in the covered forms, not that no host command ran: non-literal
spawn arguments (`unparsed_spawns`), JavaScript eval cells (`eval_unparsed`),
scripts written then run, shell functions/aliases, other tools and other
sessions are outside it. Pair every verdict with a `/var/log/pacman.log`
window count, cite `counts`/`permitted`, and never cite a `--permit` run as
clean. Its classes are not `mado-action-plan`'s declared-kind policy:
`clean` is not `plan_safe`.

Regression's mutable sibling harness digest is printed as provenance, not
an enforced harness pin. A passing run binds the observed target, spec and
harness together; it is not equivalence to an older harness revision.
For the committed two-evidences replay, use `mado-frozen-regression`:
its input digests are verified before executing the copied gate/harness.
These are explicitly frozen round-13 inputs, not aliases for mutable
sibling code. Registration alone is not verification; the round report
cites the actual self-invocations and frozen-run outcome.

For round-14 evidence use `mado-frozen-regression-r14`; the round-13
row and snapshots remain immutable historical evidence, not aliases for
the current gate. Round-14's expected file pins both executable inputs
before the replay compares the recorded historical kill table.

### Round 33 — published-axis gate and claim-verdict gate

| name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| mado-axis-scores | gate | `python3 -I quality/check-axis-scores.py --rev REV --repo .` | 0 clean (`mismatched=0`); 1 failed (`mismatched>0`); 2 could-not-evaluate (usage, bad rev, no SCORECARD) | `python3 -I quality/check-axis-scores.py --selftest`; prints `MADO_AXIS_SELFTEST: N/N assertions passed`; 0 clean, 1 failed | publication marker `Axis table re-derived at`, unquoted, 2000-character window; instruments `quality/check-index.py` and `.ufo/waves/round-31/c2/count.py` | reads committed bytes via `git show`; selftest writes nothing | mado |
| mado-r33-claim-verdict | gate | `python3 -I .ufo/waves/round-33/c2/count.py --repo . --scorecard SCORECARD.md` | 0 `TARGET_MET`; 1 `TARGET_MISSED`; 2 usage | the pre-data receipts under `.ufo/waves/round-33/controls/c2-*.txt` | predicate sentence in the script and in `.ufo/waves/round-33/registration.md`; frozen rev `d9ed38166cc3be8ef4c52b41d66ad94010feb047` | reads a scorecard path and `git archive` of the named rev; writes nothing | mado |

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

Round-16 current-status correction: this dated 2026-10-14 table is
historical, not current promotion authority. Current `SHONEN.md` has four
`[~]` assertions and zero approved boxes; lane-dispatched MADO-R3-4 does
not satisfy the present independent non-author rule. The historical arc
and completion-plan statements retain their dates and are superseded for
current status by SHONEN.md and SCORECARD's fleet-round-1 correction.

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

## Round-7 — the gate's regression mode, and the two new planes (append, M7-4)

Appended 2026-10-14 18:48Z. Round-7 plan (`plans/round-7.plan.md`, 135 L by
`wc -l` / 8,689 B / sha `d4e23e8159ff4441…`) orders ONE move in three ordered
stages: (a) the gate's own proof becomes re-runnable (`--regression`), then
(b) the theme/wallpaper plane and (c) the walker live surface widen the gate's
declared census — **(b)/(c) gated on (a) green**. Measured outcome at this
append: **(a) landed as a gate mode; (b)/(c) landed as measured notes, not as
gate rows** — the ordering clause was honoured and this section says so plainly
rather than smoothing it. Independent audit: `reports/r7-aud-m7.md` (AUD-M7,
239 L / 18,927 B, sha `4011b2c44c9abb35…`; five claims re-measured, zero config
mutation, its own combined config-plane hash identical before/after and after
every regression run). Its verdicts: stage (a) + the no-regression contracts
PASS; stages (b)/(c) NOT-LANDED as gate rows, with both notes' anchors
independently reproduced. This lane wrote only this file; scratch
`/tmp/w7-mado-m7-4/`. Substrate stayed read-only (my probes were read verbs plus
the gate's own runs; the regression mode reads no substrate).

### Stage (a) — `--regression`: usage and contract

    bash tools/mado-verify.sh --regression         # replay the recorded mutation case
    bash tools/mado-verify.sh --regression --keep  # also retain the scratch root on PASS
    env: MADO_VERIFY_HARNESS=/path/to/mutate-and-run.sh    # default: sibling tameshi checkout

`--regression --help` appends the mode paragraph (rc 0, measured); the base
`--help` still lists only the five original flags — same discoverability class
as the "still self-labels v1" note above, not a verdict input. Refused with
usage error, exit 2: `--target` / `--defects` / `--suite` / `--label` /
`--workdir` / `--timeout` / `--tail` ("--regression takes no …") and `--no-live`
/ `--live` / `--selftest` / `--root` ("not valid with --regression (the case
reads no substrate)"). Token `MADO_REGRESSION: PASS|FAIL|SETUP` — **never**
`MADO_VERIFY:`; exit map 0 PASS · 1 FAIL (measured table differs) · 2 SETUP
(unverifiable) / usage. Scratch only under `/tmp/mado-verify-regression.*`
(removed on PASS unless `--keep`; kept on FAIL/SETUP). The harness is consumed
read-only — a needed change is a recommendation to tameshi, never a patch.

The case is **recorded, not re-derived** (the tameshi idiom: re-run recorded
cases at pinned revisions with a stated contract): tameshi's T6-1 ten-defect
spec (`c7ee75b9…1dd8`, written from an in-gate heredoc and re-checked against
the pin on the written bytes) applied to this gate's own round-6 revision. That
revision is reconstructed by **excising the two marked `MADO-R7` blocks**
(`# >>> MADO-R7-SELFTEST-BLOCK >>>` `:379-558`; `# >>> MADO-R7-REGRESSION-BLOCK
>>>` `:699-1087` — refs at the round-7 revision) and asserting byte-identity to
`PIN_MADO` `c4c1afb7…a5171` (1,186 L) before any sweep; a mismatch refuses with
SETUP and prints the `REGRESSION_RECUT` command. Suite: `bash "$MUTANT"
--selftest` (fresh fixtures per run; no substrate read). PASS requires the
measured table to **equal** the recorded one: all ten ids present, every
verdict KILLED, flips 0, inconclusive 0, control GREEN, `MUTATE_RESTORE: OK`,
target bytes unchanged.

**Deviation, recorded:** the plan §(a) sketched a `|killed − recorded| ≤ 1` /
≤1-flip tolerance (tameshi's report shape); the implementation deliberately
applies none — the target is byte-frozen by excision, so slack would only hide
a lost kill (gate `:719-722`, band line `:1003`; the LOG entry repeats
it). Fail-closed direction (only costs PASSes) and disclosed in the artifact
and the record.

Measured this append, read-only (my run 18:34:36Z, rc 0, 12.2 s; audit re-runs
corroborate):

    REGRESSION_TABLE mado-verify-hardened: match=10/10 recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0
    REGRESSION_CASE mado-verify-hardened: PASS (recorded table reproduced: killed=10/10 flips=0 inconclusive=0 control=green restore=ok)
    MADO_REGRESSION: PASS (case=mado-verify-hardened; target=c4c1afb7…a5171)

Harness revision moved mid-round (`b56c6e57…22bcb` → `cf41efaa…242c75`, tameshi
lane concurrent); the mode prints the harness sha as **provenance, not gated** —
both revisions re-measured the same 10/10 table (audit §5.2), and a
behavior-changing harness surfaces as FAIL, not silently.

Reading rules that follow:

1. **From round 7, every gate-widening claim carries `MADO_REGRESSION: PASS`.**
   A plane widening adds rows *outside* the two marked blocks, so the derived
   target stops equalling `PIN_MADO` and the mode reads SETUP, never
   stale-PASS; the fix is the printed re-cut (sweep, then update
   `PIN_MADO`/`TABLE_MADO`). Edits *inside* the blocks (more selftest
   scenarios) leave the pin valid — that is the designed split.
2. `MADO_REGRESSION:` and `MADO_VERIFY:` never mix — a regression run prints
   zero `MADO_VERIFY:` tokens (measured in every log, including this lane's).
3. A SETUP is not a gate failure — it says the case could not be verified (pin
   moved, harness missing, spec mismatch); only FAIL names a non-reproducing
   table.

### Stage (b) — theme/wallpaper plane: measured surface, not yet gate rows

Note: `corpus/knowledge/theme-wallpaper-plane.md` (M7-2; 394 L / 27,594 B, sha
`8c578cc70e36506d…` at this read). It issues **no verdict token** — landing
`theme.*` gate rows is stage (b) and remains owed (census below). Its §6 is the
paste-ready row spec:

- File rows: `theme.name` read + format pin; include/import chain rows for
  `hyprland.conf:13`, `hyprlock.conf:1`, waybar `style.css:1`,
  `alacritty.toml:1`, and the mako config symlink; `walker_css`/`swayosd_css`
  (installed-consumer-gated); `theme.wallpaper.link` — the `current/background`
  symlink resolves inside `current/theme/backgrounds/` to a non-empty file.
- Live rows: `swaybg` argv names the background **symlink** with `-m fill` and
  the level-0 `wallpaper` layer pid == the swaybg pid; `omarchy theme current`
  agrees with `theme.name` under the measured reader rule. The theme *choice*
  stays NOTE (operator-owned — today's `live.theme.current` row, unchanged);
  chain *integrity* is what would become verdict input.

Key anchors (re-measured this lane and by the audit): `theme.name` =
`matte-black` (12 B); `current/background` → `…/theme/backgrounds/0-ship-at-sea.jpg`
(1,681,677 B, sha `55fa691a…`); `pgrep -ax swaybg` → `1203358 /usr/bin/swaybg
-i /home/vgpnk/.config/omarchy/current/background -m fill`; `hyprctl -j layers`
→ DP-1 level 0 `wallpaper` pid 1203358, level 2 `waybar` 1203352. The
name-normalization rule is measured from the two scripts that produce both
sides (`omarchy-theme-current:9` reader, `omarchy-theme-set:17` writer):
`printf 'matte-black' | sed -E 's/(^|-)([a-z])/\1\u\2/g; s/-/ /g'` →
`Matte Black` (my re-run ✓). A pair the rule does not join is recorded, never
forced; the rule is measured on this host's one theme, not assumed general.

Fence unchanged: the theme dir is rewritten by `omarchy theme set`; every
mutating verb (`theme set`, `bg *`, `restart *`, `refresh *`, `install *`)
stays out of the gate — it observes the plane and never sets it. Parts whose
live chain stays unresolved (`walker.css`, `swayosd.css`, `btop.theme`,
`themed/*.tpl.sample` rendering) get their exact probe recorded, never an
inferred consumer (note §7; inertness of `*.tpl.sample` proven from
`omarchy-theme-set-templates`/`omarchy-hook` source).

### Stage (c) — walker live surface: measured surface, not yet gate rows

Note: `corpus/knowledge/walker-live-surface.md` (M7-3; 300 L / 19,203 B, sha
`2bbb9609283f2d81…`). The gate's walker live rows today are version + services
only (`:1648-1667` at the round-7 revision); the note is the surface the wiring
would cite and does not carry gate rows itself. Measured invariants
(re-measured here):

- sockets `$XDG_RUNTIME_DIR/walker/walker.sock` and
  `$XDG_RUNTIME_DIR/elephant/elephant.sock` — `srwxr-xr-x`, 0 B, stat'd never
  connected;
- `busctl --user status dev.benz.walker` → owner pid == the walker pid
  (1203471, `/usr/bin/walker --gapplication-service`); elephant 1203474; both
  units `active`;
- layer invariant: if a walker namespace appears in `hyprctl -j layers` its pid
  == the walker pid; **absence is a NOTE** (the launcher is closed — the gate
  never opens it).

Rendered UI and the socket protocol stay UNKNOWN by constraint (never opened,
never connected). `walker --version` = `2.17.0`; binary sha `64826a8531eac525…`.
The plan's `walker-deep.md` §10/§11 errata append is **owed** — `walker-deep.md`
unchanged (`0982ba06…` at this read); the note's §5 ledger is the text to carry
there.

### Identity, census, verdicts at this append

| | Before (round 6) | After (stage (a) landed) |
|---|---|---|
| gate lines / bytes | 1,186 / 50,126 | **1,755 / 75,771** (`git diff --numstat` = +569/−0, all inside the two MADO-R7 blocks) |
| gate sha256 | `c4c1afb75dd1c8aa…a5171` | `90d50cdd4d18410b…` (stable 18:31:59Z → this append) |
| selftest | 53/53 | **89/89** (rc 0; +36 executed assertions — 37 call sites in the R7 block, R10's defected-gate branch not taken on a pristine run) |
| live verdict (read-only) | CLEAN (35 pass, 4 notes) | CLEAN (35 pass, 4 notes), rc 0 — identical |
| file-plane verdict | CLEAN (17 pass, 2 notes) | CLEAN (17 pass, 2 notes), rc 0 — identical |
| `row` + `row_from_rc` call sites | 106 + 6 | 106 + 6 (a 7th `row_from_rc` occurrence is the helper's definition) |
| plane ids / coverage | 6 ids; walker live = version + services; theme = 1 NOTE | unchanged — no `theme.*` rows, no walker socket/owner/layer rows |
| boundary proof | combined sha `bb2639d9a980…` | `bb2639d9a980…` in both verdict runs (gate's own row PASS) |

Excision proof, re-run here: the two-block excision from `90d50cdd…` → sha256
`c4c1afb7…a5171`, 1,186 L, byte-equal to `git show
HEAD:tools/mado-verify.sh` — i.e. the verify path is untouched, which is what
the two identical verdicts also show from the other side.

Corrections this append carries: the plan's design-time numbers are pre-round-6
— "selftest count before → after (28 → 28+N)" reads **53 → 89**, and the plan's
theme/walker line refs (`:1014-1021`, `:989-998`/`:1000-1011`) sit at the
round-5 revision; round-6's refs (`:1102-1108`, `:1077-1101`) sit at the
1,186-L revision and shift to `:1673-1677` / `:1648-1667` once the MADO-R7
blocks are added. The scribe draft's "SKILL `:103`/`:138` spell
`fr.arrouillard.waybar`" erratum candidate does **not** reproduce: both sites
carry the measured live name `fr.arouillard.waybar` (double-r grep count 0 at
this revision, `busctl --user list` → `fr.arouillard.waybar`).

### Open items

- Stages (b)/(c) gate rows: **not landed**. Landing conditions, both stated in
  their notes: widen the selftest plane-prefix regexes (`:352`, `:356`,
  `:371-375`) to include any new plane id, and ship a covering mutant per new
  clause (round-6 reading rule 2) — then carry `MADO_REGRESSION: PASS` under
  rule 1 above (the rows land outside the marked blocks, so the case needs a
  re-cut; no widening ships without one).
- `walker-deep.md` §10/§11 errata: substance ready (M7-3 §5 ledger), append
  owed by the lane owning that note.
- The omarchy freshness watch arm (round-6 spec, `omarchy-drift-watch.md`) is
  still unlanded — same mutant + re-cut conditions apply.
- Record-keeping at this append: `LOG.md` carries the M7-1 round-7 entry
  (`:297`, 297 L, sha `1ee327882c3f810b…`); `SCORECARD.md` (18 L,
  `e23b75fe…`) and `corpus/README.md` (19 L, `2dd274f5…`) are still at round-6
  state; the scribe draft (`plans/round-7-record-draft.md`, 568 L,
  `045d380ab52ce317…`) and AUD-M7's report carry the provisional pins the
  finalizer must freeze from the committed revision.
- Cosmetic, by design: the gate still self-labels "v1 (round 5 / M5-2)" and
  the base `--help` omits `--regression` — the two MADO-R7 blocks being the
  only difference from the recorded revision is exactly what makes the
  excision pin work.
- `corpus/lessons/` still 0 entries (seventh round of the round-1 promise).

## Round-8 — the post-hardening sweep, plane 7, and the receipt modes (append, M8-4)

Appended 2026-10-14 19:37Z. Round-8 plan (`plans/round-8.plan.md`, 206 L by
`wc -l` / 13,854 B / sha `ffcc058aa17755d9…`) orders ONE move in three ordered
stages: (a) the hypr live rows reached through PATH stubs, then (b) the
`omarchy` freshness plane and (c) an assertion floor — **(b)/(c) gated on (a)
green**. Measured outcome at this append, at the landed revision
`tools/mado-verify.sh` sha256 `7da4ec5013583c91…` (2,887 L / 131,612 B, mtime
16:29:03 −03:00; stable 16:29:03 → 19:37Z through every run quoted here):
**the declared census gains plane 7 with its live body exercised hermetically
(b — landed), the recorded mutation case is re-cut and re-passes (landed), and
two new receipt modes ship (`--snapshot` / `--snapshot-diff`)**; **stage (a)'s
hypr-live stub scenarios (J/K/L) and stage (c)'s assertion floor did NOT land**
— the wave's lanes were the sweep (M8-1), the plane (M8-2) and the modes
(M8-3), and neither (a) nor (c) had an owning lane. This section says so
plainly rather than smoothing it. Independent verification:
`reports/r8-aud-m8.md` (AUD-M8; 127 L / 11,881 B / `4d8cd1cb163d810e…`) and
`reports/r8-ver-m8.md` (VER-M8; 156 L / 9,997 B / `a96795039520e86a…`). This
lane wrote only this file; scratch `/tmp/w8-mado-m8-4/`; the substrate stayed
read-only — every run quoted below is the gate's own read-only mode, and the
snapshot spot-checks wrote only under this lane's scratch.

### The post-hardening sweep — result

Note `corpus/knowledge/gate-mutation-sweep-r8.md` (M8-1; 178 L / 10,946 B / sha
`9d6435f5cdd52561…`). Headline, measured: the recorded T6-1 ten-defect spec
re-run against the round-7-hardened revision `90d50cdd…` → **killed 10 /
survived 0 / inconclusive 0 — 100 % (10/10)**, control GREEN (89/89),
`MUTATE_RESTORE: OK`, target sha before = after. The recorded spec is refused
verbatim on the live bytes (nine non-unique anchors — round 7 embedded the spec
in the gate's own heredoc, so nine anchors occur twice); the re-cut spec sha256
`85d946d7905d8c92…6b01` (3,166 B) keeps the ten clauses and widens each anchor
by adjacent live lines; harness pin `cf41efaa8be5f52d…242c75` (1,341 L),
consumed read-only. Rate path for the same ten defects: round-5 revision
`d7edaab4` 4/10 (40 %) → `c4c1afb7` 10/10 → live `90d50cdd` 10/10.

Independently reproduced, twice: AUD-M8 re-ran the re-cut spec against its own
frozen copy of `90d50cdd…` (`killed=10 … rc 0`), re-derived the excision
itself, and re-ran the recorded spec against `c4c1afb7…` — all PASS; VER-M8
swept the whole file at three revisions (`90d50cdd…`, `f58632b9…`, `38ed880f…`)
with its own re-cut specs — 10/10 at each, and `MADO_REGRESSION: PASS` at each.
Both reports print the in-flight pin machinery as the only red at their closes
(AUD-M8 C4/C5: `--regression` SETUP and the R10 selftest case failing while the
pin was mid-re-cut) — that is the alarm doing its job, and it is resolved at
the landed revision below.

**The re-cut.** `PIN_MADO` moved `c4c1afb7…a5171` → `d2bcdb31daea5d68…db62`;
the derived target is now this file with **three** marker families excised
(`MADO-R7-SELFTEST-BLOCK`, `MADO-R7-REGRESSION-BLOCK`, `MADO-R8-BLOCK` — the R8
pair wraps round-8's own additions so a widening *inside* it needs no re-cut;
anything new outside every pair still does). This lane reproduced the pin
independently: the three-family `sed` excision of the landed bytes yields
`d2bcdb31…`, 1,617 L, byte-for-byte. My own run at the landed revision:

    MADO_REGRESSION: PASS (case=mado-verify-hardened; target=d2bcdb31…db62)   rc 0
    REGRESSION_CASE … PASS (recorded table reproduced: killed=10/10 flips=0
      inconclusive=0 control=green restore=ok)

### The new modes — `--snapshot` / `--snapshot-diff`

    bash tools/mado-verify.sh --snapshot FILE [--no-live|--live] [--root DIR]
        # runs the gate, writes a v1 receipt to FILE (FILE must not exist;
        # receipts are never overwritten). Exit = the run's verdict; the write
        # adds MADO_SNAPSHOT: WRITTEN|REFUSED (a refusal exits 2).
    bash tools/mado-verify.sh --snapshot-diff OLD NEW
        # diffs two receipts class by class. MADO_DIFF: SAME|DETAIL-CHANGED|
        # CHANGED|SETUP (exit 0/0/1/2). Reads only the two files; never prints
        # MADO_VERIFY:.

Discoverability, measured: the base `--help` still lists only the five original
flags (same class as the round-7 note); the mode paragraph is appended by
`--snapshot --help` and `--snapshot-diff --help` (both rc 0), and scenario S9
asserts the help documents both modes. The receipt header carries
`# mado-verify snapshot v1`, the creation time, `tool=` (the self-label) and
`gate-sha256=` — a receipt names the revision that produced it.

Spot-checks of the modes, executed at the landed revision (scratch
`/tmp/w8-mado-m8-4/`):

1. `--no-live --snapshot a.snap` → `MADO_SNAPSHOT: WRITTEN … (rows=31 pass=20
   fail=0 unknown=0 skip=8 note=3; scope=file-plane)`, rc 0; the file is 40 L /
   2,860 B and starts `# mado-verify snapshot v1`.
2. A second write to the same path → `MADO_SNAPSHOT: REFUSED (destination
   exists: … — receipts are never overwritten)`, **rc 2**.
3. `--snapshot-diff a.snap b.snap`, where `b.snap` receipts a divergent run
   (empty root, my scratch) → `MADO_DIFF: CHANGED (rows 31→30; regressed=14
   recovered=0 flipped=0 relaxed=0 relabeled=5 appeared=0 vanished=1;
   detail-changed=22; scope=1)`, **rc 1**; `--snapshot-diff a.snap a.snap` →
   `MADO_DIFF: SAME …`, **rc 0**.
4. No run touched the substrate: the gate's own `boundary.readonly` row prints
   the same combined config-plane prefix `bb2639d9a980…` in every run, and the
   gate's sha256 was identical before and after all of them.

### Plane 7 — `omarchy` freshness, and how its live body is reached

`omarchy_plane()` (`:2610`) emits 11 rows — 8 verdict-bearing and 3 NOTE-level,
the plan §(b)'s split, from `omarchy-drift-watch.md` §6 (named at `:2574`).
D-1 resolves as the plan predicted: `omarchy.theme` is a NOTE with HELD|MOVED
printed in the detail (a routine theme change must not turn the freshness gate
permanently red). Measured live verdicts at the landed revision, every pin
HELD:

| row | verdict | detail (quoted from the live run) |
|---|---|---|
| `omarchy.version.cmd` | PASS | HELD: 'omarchy version' → 3.8.3 (P1 pin) |
| `omarchy.version.file` | PASS | HELD: version file '3.8.3' (P2 pin; == HEAD:version blob at the pinned HEAD) |
| `omarchy.git.tag` | PASS | HELD: v3.8.4 exactly at HEAD (P3 pin) |
| `omarchy.git.head` | PASS | HELD: 8fcc9d60 (P3 pin) |
| `omarchy.skill.link` | PASS | HELD: symlink into the checkout (one file; nothing to drift) |
| `omarchy.skill.sha` | PASS | HELD: leaf sha256 becd149e4d1c… (P4 pin) |
| `omarchy.skill.vs_head` | PASS | worktree == HEAD blob (index-free; no local edit) |
| `omarchy.cmd.groups` | PASS | HELD: all 11 skill groups present (56 live groups in --json --all) |
| `omarchy.cmd.surface` | NOTE | HELD: 282 commands in --json --all (counter only, not a verdict input) |
| `omarchy.theme` | NOTE | HELD: 'Matte Black' (operator-owned; D-1: never a verdict input) |
| `omarchy.doc.drifts` | NOTE | R2 carried: 5 *.d hook dirs live vs flat files in the skill text (MADO-3 §7); R1 route-table drift declared in the note, not re-derived here |

The live rows are reached **hermetically**: scenarios OM1–OM8 install stub
`omarchy` / `git` verbs first on PATH (the `git` stub answers `describe`,
`rev-parse`, `show` from fixture blobs; the omarchy stub refuses unknown verbs
with rc 64) and drive the real row code through `--root` fixtures — a moved
pin FAILs naming the pin (OM3/OM7), a missing stub reads UNKNOWN and never
CLEAN (OM4), an equal-bytes copy in place of the symlink reads MOVED as a copy
while `.skill.sha` still measures the same bytes (OM5), a worktree edit is
detected without `git status` (OM6), and a missing group is named (OM8). That
is this round's stub-based live-body exercise — it is the `omarchy` plane's,
not the hypr live plane's (see below). Fence unchanged: the plane reads only
the §6 guard list — no `git status`, no `git fetch`, no mutating `omarchy` verb.

### Identity, census, verdicts at this append

| | Before (round-7 landed `90d50cdd…`) | After (landed `7da4ec50…`) |
|---|---|---|
| gate lines / bytes | 1,755 / 75,771 | **2,887 / 131,612** (`git diff --numstat` vs HEAD = +1,141/−9) |
| gate sha256 | `90d50cdd4d18410b…` | `7da4ec5013583c91…` |
| selftest | `89/89`, rc 0 | **`217/217`**, rc 0 (twice) |
| file-plane verdict | CLEAN (17 pass, 2 notes; skip=1) | CLEAN (**20 pass, 3 notes**; `counts: pass=20 fail=0 unknown=0 skip=8 note=3`), rc 0 |
| live verdict | CLEAN (35 pass, 4 notes) | CLEAN (**43 pass, 7 notes**; `counts: pass=43 fail=0 unknown=0 skip=0 note=7`), rc 0 |
| `row` + `row_from_rc` sites | 106 + 6 | **162 + 6** (omarchy 56 / hypr 23 / hypr-live 51 / waybar 17 / terms 10 / gate 3 / walker 2) |
| distinct row ids / planes | 40 / 6 ids | **51 / 7 ids** (omarchy 11 / hypr-live 21 / hypr 9 / waybar 4 / terms 4 / walker 1 / gate 1) |
| selftest helper plane regex | 6 ids | **7 ids** (`hypr|hypr-live|waybar|walker|terms|omarchy|gate`, five sites `:357`, `:361`, `:376-380`) |
| row ids asserted by the suite | 11 of 40 | **22 of 51** (all 11 new ones are `omarchy.*`; no hypr-live id added) |
| regression case | PASS @ `c4c1afb7…` | **PASS @ `d2bcdb31…`** (three-family excision; my own run, rc 0) |
| boundary proof | `bb2639d9a980…` | `bb2639d9a980…` (unchanged in every run) |
| scenario labels in the suite | A–I, R1–R13 | + **OM1–OM8**, **S1–S10** |

Corrections this append carries: the plan's design-time counters are pre-round-7
— its "selftest count before → after (53 → 53+M)" reads **89 → 217**, its
"distinct asserted row ids (11 of 40)" is right for the before state and reads
**22 of 51** after; its line refs (`:379-558`, `:699-1087`,
`:352`/`:356`/`:371-375`, `:676-1108`) sit at the round-7 revision and shift
(the helper regexes are `:357`/`:361`/`:376-380`; the live readers
`live_plane()` `:2300`; `omarchy_plane()` `:2610`).

### What did not land (plan stages (a) and (c))

- **(a) hypr-live stub scenarios J/K/L — not in the suite.** No `hyprctl`
  PATH-stub fixture exists (`grep -n hyprctl` shows only the reader sites, the
  `have hyprctl` guard and scenario C's no-hyprctl sandbox); scenarios A–I are
  unchanged by round 8, and no hypr-live row id entered the asserted set. The
  live plane's *body* is still exercised only by the real read verbs on this
  host (35 → 43 live rows pass at the landed revision, but from the substrate,
  not from a stub) — the round-6 open item stands.
- **(c) assertion floor — not landed.** The two exit-2 arms the round-6 record
  named (`--root` with no value; a bad `MADO_VERIFY_LIVE`) still have behavior
  but no assertion (`grep` for both refusal strings inside the suite: 0), and
  both existed already at HEAD (`git show HEAD:tools/mado-verify.sh`, 1,755 L)
  — round 8 neither added nor pinned them; `VERSION_STR` still self-labels
  "v1 (round 5 / M5-2)" (now also copied into every snapshot receipt's `tool=`
  line); the boundary combined-hash prefix is still not asserted in a `sha_pin`
  detail; the `row_from_rc` rc-6 arm is byte-identical (still maps 6 → UNKNOWN
  — no white-box pin and no branch removal), so the round-6 owner decision is
  still open.
- The exit-flatten family stays a harness boundary: recorded as a
  recommendation to tameshi (a kill criterion that also reads suite stdout),
  never a patch from this repo.
- A widening *outside* the three marked families makes `--regression` read
  SETUP with its printed `REGRESSION_RECUT` — by design, never a stale PASS.

### Unknowns at this append

- The gate was written by three lanes inside this round; every number above is
  tied to `7da4ec50…` (stable 16:29:03 −03:00 → this append). Later revisions
  are not covered — re-run `sha256sum tools/mado-verify.sh` before quoting.
- Whether the `omarchy` guard list stays sufficient when the checkout moves:
  `omarchy.skill.vs_head` needs a read verb inside the checkout (`git show`);
  tree-wide cleanliness stays unmeasured by constraint (no `git status`).
- Whether the `v1` receipt schema carries a different host's live-scope rows
  without a split — untested beyond two local scopes.
- `corpus/lessons/` still 0 entries (eighth round); `corpus/README.md` rows and
  the round-7 `walker-deep.md` §10/§11 errata remain owed by their owners.

## Round-9 — the theme plane lands, the walker surface deepens (append, M9-4)

Appended 2026-10-14 20:17Z. Round-9 plan (`plans/round-9.plan.md`, 231 L by
`wc -l` / 15,136 B / sha `8630c91a75a2eb43…`, committed with the round-8
landing) orders ONE move in three ordered stages: (a) the `theme` plane lands
as gate rows from `corpus/knowledge/theme-wallpaper-plane.md` §6; (b) the
walker live-surface rows land from `corpus/knowledge/walker-live-surface.md`
§4/§5 plus the `walker-deep.md` §10/§11 errata; (c) census closure + receipts.
Measured outcome at the round-9 gate revision `tools/mado-verify.sh` sha256
`93e43f8fe8b9bdd4…` (3,231 L / 150,103 B, mtime 17:05:32 −03:00; stable ≥10
min through this lane's battery; **uncommitted in the worktree at this
append**): **(a) landed as the file-plane arm** — 10 theme rows, scenarios
T1–T9, helper regex seven → eight ids, the pin re-cut and re-passing;
**(b) did not land as gate rows** — the walker live surface stays
measured-only, and the round's walker work is the M9-2 note
`walker-deep-r9.md`; **(c) landed as the re-cut receipt** quoted below. The
theme note's two live rows are **exempted by name** (anchors below), the
plan's own fallback where the round-8 stub discipline does not reach. This
lane wrote only this file; scratch `/tmp/w9-mado-m94/`; the substrate stayed
read-only (read verbs + the gate's own modes; no launcher, no socket
connect, no `omarchy theme set`).

### Theme plane arm — what the gate now checks (landed `93e43f8f…`)

Plane id `theme`; `theme_plane()` at `:3113` (called `:2465`); the plane
comment `:3002-3012` states the landed scope. The note's §6 spec is the
input, never edited; its 12 table rows resolve as **10 landed ids + 2 live
rows exempted by name + `theme.choice` relocated to the existing NOTE**:

| Row id | Layer | PASS | FAIL | Other |
|---|---|---|---|---|
| `theme.name.read` | file | `theme.name` one line matching `^[a-z0-9-]+$` (live `matte-black`) | unreadable / malformed | UNKNOWN if tree absent under root |
| `theme.chain.hypr_include` | file | `hyprland.conf:13` sources the theme file, target exists | line moved / target missing | — |
| `theme.chain.hyprlock` | file | `hyprlock.conf:1` sources the theme file, target exists | same | — |
| `theme.chain.waybar_css` | file | `waybar/style.css:1` imports the theme css, target exists | same | — |
| `theme.chain.alacritty` | file | `alacritty.toml:1` imports the theme toml, target exists | same | — |
| `theme.chain.mako_link` | file | `~/.config/mako/config` symlink resolving inside `current/theme/`, target exists | regular file / dangling / target outside | UNKNOWN if `readlink` absent |
| `theme.chain.walker_css` | file | walker theme package's `style.css` imports `current/theme/walker.css`, target exists | import present but target missing / broken | NOTE when walker/package absent (never a silent skip) |
| `theme.chain.swayosd_css` | file | swayosd `style.css:1` imports `current/theme/swayosd.css`, target exists | same | NOTE when swayosd absent |
| `theme.wallpaper.link` | file | `current/background` symlink inside `backgrounds/` to a non-empty file | dangling / outside / empty | — |
| `theme.parts.declared_only` | file | — | — | NOTE always: the §4.1 parts whose consumer is absent (live: 6 — foot.ini, kitty.conf, ghostty.conf, helix.toml, vscode.json, keyboard.rgb) |

Live reading at the landed revision (my run, read-only): **9 PASS + 1 NOTE**
— `theme.name.read` `matte-black`; the four chain rows hold their declared
lines; `mako_link` and `wallpaper.link` resolve into `current/theme/`;
`wallpaper.link` → `…/backgrounds/0-ship-at-sea.jpg`; the declared-only NOTE
names the six absent consumers. `theme.choice` is **unchanged** — the
`live.theme.current` NOTE (`:2753`/`:2757`), operator-owned, never a verdict
input, so a routine theme change cannot turn the gate red; chain *integrity*
is what the new rows judge.

Scenario register (hermetic, `--root` fixtures; `:788-912`): **T1** clean →
10 rows, zero FAIL/UNKNOWN, counts agree; **T2** a chain target removed → the
named row FAILs alone (DIVERGED, and no fake CLEAN); **T3** the include line
moved → FAIL naming both line numbers; **T4** a copy in place of the mako
link + a dangling background; **T5** the background link must resolve inside
`backgrounds/`; **T6** an empty background target FAILs; **T7** a malformed
`theme.name` FAILs (shape, not value); **T8** an absent consumer reads NOTE —
never a FAIL, never a skip; **T9** a missing tree reads UNKNOWN, never CLEAN.
`build_fixture` grew the pieces the chain rows read (theme `alacritty.toml` /
`hyprlock.conf` / `mako.ini` / `walker.css` / `swayosd.css`, a
`backgrounds/0-fixture.jpg`, the `current/background` and `.config/mako/config`
symlinks, `.config/swayosd/style.css`, the walker theme package) and mirrors
the theme include at **fixture line 13** = the live anchor. The builder sits
outside every marked family, so the widening re-cut the pin: `PIN_MADO`
`d2bcdb31…` → **`dc7c4141…`** (derived target 1,945 L, re-derived
independently and cmp-identical per the gate's re-cut record `:1254-1268`).

Receipts, my own runs at `93e43f8f…` (logs `/tmp/w9-mado-m94/`):

    MADO_SELFTEST: 268/268 assertions passed                        rc 0
    --no-live: CLEAN (29 pass, 4 notes)   counts: pass=29 fail=0 unknown=0 skip=8 note=4
    live:      CLEAN (52 pass, 8 notes)   counts: pass=52 fail=0 unknown=0 skip=0 note=8
               boundary.readonly PASS, combined sha bb2639d9a980…
    MADO_REGRESSION: PASS (case=mado-verify-hardened; target=dc7c4141…)
    REGRESSION_TABLE mado-verify-hardened: match=10/10 recorded-killed=10
      measured-killed=10 survived=0 inconclusive=0 flips=0
    REGRESSION_DATE: 2026-10-14T20:13:58Z · spec c7ee75b9…1dd8 (pin matches)
      · harness cf41efaa…242c75 (recorded b56c6e57… — provenance, not gated)

Census, before → after (gate identity + counting commands; site counts count
`row`/`row_from_rc` call sites, ids count distinct first-args):

| | round-8 landed `7da4ec50…` | round-9 landed `93e43f8f…` |
|---|---|---|
| gate lines / bytes | 2,887 / 131,612 | **3,231 / 150,103** (`git diff --numstat` +352/−8) |
| `row` sites (+`row_from_rc`) | 162 (+6) | **189 (+6)** — theme 27 sites |
| plane ids / distinct row ids | 7 / 51 | **8** / **55** by literal `row`-site count (AUD-M9's counting command) — **61** as emitted at run time (the plane emits 10 ids; 6 are helper-driven, not literal sites) |
| row ids asserted by the suite | 22 of 51 | **32** (the 10 theme ids all asserted via T1–T9; the same union AUD-M9 counts as 22 → 32) |
| helper regex ids / sites | 7 / 7 | **8 / 7** (`:387`, `:391`, `:406-410`) |
| selftest | 217/217 | **268/268** (+51, the T family) |
| `--no-live` / live verdicts | CLEAN (20 pass, 3 notes) / CLEAN (43 pass, 7 notes) | CLEAN (29 pass, 4 notes) / CLEAN (52 pass, 8 notes) |
| `PIN_MADO` / regression | `d2bcdb31…` / PASS | **`dc7c4141…` / PASS** (my run) |

### The owe, stated — the theme clauses' covering mutant

The gate's own re-cut record says it plainly: *"the newly landed theme rows
carry no defect of their own yet: a covering mutant for the theme clauses is
owed by the sweep lane (round-6 reading rule 2) — recorded, not smoothed"*
(`:1266-1268`). So the recorded ten-defect case still dies 10/10 at the
re-cut revision, but **no mutant yet targets a theme clause itself**: under
reading rule 2 (round-6 append) an untested clause stands until a mutant
proves otherwise, and a survivor is a FINDING. This is the round's largest
named remainder.

### Exempted by name — the rows that did not ship

Under the plan's ordering clause (if the round-8 stub discipline (a8) did not
fully land, the live rows are exempted **by name** and the exemption counted —
never faked), these did not land, each with its clause anchor:

1. **`theme.wallpaper.live`** (`theme-wallpaper-plane.md` §6; plan §(a)) —
   needs `pgrep -ax swaybg` (argv naming the background *symlink* with
   `-m fill`) and `hyprctl -j layers` (level-0 `wallpaper` pid == swaybg
   pid). No `swaybg`/argv reader exists and no `hyprctl` PATH stub exists
   ((a8) resolved **partial**: the `omarchy` stub idiom landed, the
   hypr-live variant did not); the substrate is never read by a stub
   scenario. Measured anchors held for when it lands: `pgrep -ax swaybg` →
   `1203358 /usr/bin/swaybg -i …/current/background -m fill`; layers DP-1
   level 0 `wallpaper` pid 1203358.
2. **`theme.name.display_agree`** (§6/§5; plan §(a)) — `omarchy theme current`
   vs the measured reader rule; the pair today is `Matte Black` /
   `matte-black` (rule: `sed -E 's/(^|-)([a-z])/\1\u\2/g; s/-/ /g'`), but the
   gate read of the live verb would be substrate and the fixture carries no
   display pair.
3. **Walker live-surface rows** (`walker-live-surface.md` §4/§5; plan §(b)):
   the two socket rows (`$XDG_RUNTIME_DIR/walker/walker.sock`,
   `…/elephant/elephant.sock` — path/type/mode/size, **stat'd never
   connected**), the D-Bus owner row (`dev.benz.walker` owner pid == the
   walker pid; a mismatch FAILs), the layer-invariant row (a walker
   namespace must carry the walker pid; **absence is a NOTE**, never a
   pass/fail signal). `grep -c 'walker.sock' tools/mado-verify.sh` → **0** at
   `93e43f8f…`; the gate's walker live surface stays version + services
   (`:2728-2747`). The hermetic barrier is structural: `--root` roots a
   `$HOME`-shaped tree, while `$XDG_RUNTIME_DIR` and the session bus sit
   outside it, and no `busctl` stub exists.

Measured live values these rows would read, all re-verified this append
(read-only, point samples): walker 1203471 `/usr/bin/walker
--gapplication-service`, elephant 1203474; sockets `srwxr-xr-x` 0 B (mtime
13:11:09, the session start second); `busctl --user list` → `dev.benz.walker`
owner **1203471**, unique name `:1.23` (elephant holds no session-bus name);
`hyprctl -j layers` → DP-1 level 0 `wallpaper` 1203358, level 2 `waybar`
1203352, **no walker namespace** (launcher closed).

### Walker findings — M9-2's `walker-deep-r9.md`

Note: `corpus/knowledge/walker-deep-r9.md` (M9-2, round 9; 398 L / 24,391 B /
sha `a5acfe0162c9e5cd…`; the note is the authority). Headlines:

- **Version/shape pinned to build identity** — binary sha256 `64826a85…`,
  BuildID `a22452d1…`, `.comment` rustc 1.97.1 (Arch) / LLD 22.1.8, package
  `walker 2.17.0-1` with `pacman -Qkk` 29 files / 0 altered; the printed
  `2.17.0\n` proven to be the compiled-in rodata literal (offset 847,791) —
  a replaced or rebuilt binary moves the sha256, the BuildID or the toolchain
  line. Help pins (`ca4820a8…`, `b513c43f…`, `0945536c…`) byte-identical to
  round 7.
- **Config reload semantics** — settled OBS across five independent classes:
  no reload verb in the CLI (0 hits for config/reload/watch across the three
  `--help` forms); **no filesystem-watch machinery** in the binary
  (`inotify` = 0, `(?i)watch` = 0); the `Reload`-family tokens (1 `reload`,
  52 `Reload`) are **result-list refresh semantics** (`after = "AsyncReload"`),
  never configuration — the named trap; no D-Bus reload method; `systemctl
  --user show` → `CanReload=no`, no `ExecReload`. INF-high: config is read
  **once at process start**; edit → restart is the apply path
  (`omarchy-restart-walker` restarts `elephant.service` +
  `app-walker@autostart.service`). UNK kept with its class named: whether an
  edit applies without a restart — every exercise path opens the launcher
  (fenced), and ptrace was unattempted.
- **A bound and its limit** — `--help` under a scratch XDG planting a broken
  `config.toml`: rc 0, stdout byte-identical, nothing created; the
  short-circuit-vs-silent-tolerance reading stays UNK.
- **MOVED check** — every round-7 pin re-measured ~1 h 37 m later (across the
  round-8 commit): identical; none MOVED.

The `walker-deep.md` §10/§11 errata ledger routed from round 7 is **still
owed** (file 617 L / 38,403 B / sha `0982ba066c72575a…`, unchanged); M9-2's
note §8 carries the candidate text (parse-error templates pinned by offset;
the artifact-identity chain added to the §10 row; the third companion
negative for the §9 reload rule).

### Re-run recipes (read-only)

    bash tools/mado-verify.sh --selftest     # 268/268 at 93e43f8f…
    bash tools/mado-verify.sh --no-live      # file plane: CLEAN (29 pass, 4 notes)
    bash tools/mado-verify.sh                # live: CLEAN (52 pass, 8 notes)
    bash tools/mado-verify.sh --regression   # PASS, target dc7c4141…, 10/10 flips=0

The theme arm alone: `--no-live --root <fixture>` against `build_fixture`'s
tree — T1–T9 are the shape; a broken row FAILs naming row + part, a missing
tree reads UNKNOWN, never CLEAN. The walker surface by hand (no gate rows
yet): `pgrep -ax walker`; `busctl --user list | grep dev.benz.walker`
(owner pid == the walker pid); `stat -c '%F %a %s %y'
"$XDG_RUNTIME_DIR/walker/walker.sock" "$XDG_RUNTIME_DIR/elephant/elephant.sock"`
(stat, never connect); `hyprctl -j layers` (walker namespace absent when
closed; if present its pid must equal the walker pid). Reload: there is
none — restart is the apply path.

### Corrections this append carries

- The plan's design-time numbers are round-7 values (`89/89` selftest, 106
  `row` sites, 40 ids, gate `90d50cdd…`): the landed round-8 base reads
  217/217, 162, 51, `7da4ec50…`, and the round-9 landed revision 268/268,
  189, 61, `93e43f8f…` — the same stale-base class rounds 7 and 8 recorded.
- The plan's line refs sit at older revisions: helper regexes
  `:352`/`:356`/`:371-375` → `:387`/`:391`/`:406-410`; `live.theme.current`
  `:1673`/`:1677` → `:2753`/`:2757`; the walker rows → `:2728-2747`; the
  theme plane is `theme_plane()` `:3113`.
- Independent verification of the landed arm: VER-M9 (`reports/r9-ver-m9.md`,
  139 L / `98ec0c3b57a0d348…`) reproduced the theme file arm at the same
  revision (clean fixture → 10 theme rows; broken → exactly 1 named FAIL;
  empty root → UNKNOWN, no fake CLEAN; live CLEAN 52/8) — with the same
  caveat this append carries: the gate moved six times before it held, so
  every number binds to `93e43f8f…` only.
- Independent audit: AUD-M9 (`reports/r9-aud-m9.md`, 166 L /
  `7ad8eccdd8d213a5…`) — C1 PASS (file half; every anchor re-read), C1b
  NOT LANDED (the two live rows), C2 PASS (268/268; asserted 22 → 32), C3
  PASS (census + regex widening), C4 PASS for the recorded case with the
  same finding this append carries (the spec is byte-identical to round 8
  — no new recorded mutant covers the theme clauses), C5/C5b PASS
  (snapshot receipts green at the landed revision; the landing receipt
  itself reads `MADO_DIFF: CHANGED (rows 31→41; appeared=10;
  detail-changed=0)`, every appeared row one of the ten theme ids), C6
  PASS (zero config mutation, boundary `bb2639d9a980…` unchanged).

### Unknowns / open items at this append

1. Whether the committed revision equals `93e43f8f…`; a later revision
   re-opens the selftest count, the pin, and every receipt above.
2. The theme clauses' covering mutant — owed; whether the round's sweep lane
   lands it, and any survivor, are findings to record, never to smooth.
3. When the exempted rows get a hermetic route: an accepted
   `XDG_RUNTIME_DIR` seam, a `busctl` stub under the omarchy idiom, or a
   `hyprctl`/`swaybg` stub — else they stay exempted by name and counted.
4. `walker-deep.md` §10/§11 errata; `corpus/README.md` rows; the round-8
   draft's 19 `⟨PENDING⟩`s — all ride the round record, not this file (this
   lane's write scope was this file only).
5. `corpus/lessons/` still 0 entries (ninth round) — the round charters
   `round-9.md` or records why no independent seat exists.

## Round-10 — arc closeout: the synthesis and the gate's standing-use note (append, M10-4)

Appended 2026-10-14 21:03Z. Round 10 (`plans/round-10.plan.md`, 295 L by
`wc -l` / 19,322 B / sha `eca573b271e926e3…`, committed with the round-9
landing) is the arc's final round: fold nine landed rounds into the ten-round
synthesis and hand the gate over with its standing-use contract. This lane's
write was this append only; scratch `/tmp/w10-mado-m10-4/`; the 30-minute
poll (opened 20:50Z) watched both artifacts — the note first appeared
20:55:43Z (last write 20:58:01Z, M10-3's tick appended), the synthesis's last
write 20:57:22Z; both sha-stable across four samples through 21:00:55Z before
this append, in-window. Read-only throughout: the gate was read and its helps
quoted; no substrate touched. The revision every number below binds to:
`tools/mado-verify.sh` sha256 `93e43f8fe8b9bdd4…` (3,231 L / 150,103 B,
committed `de22dfd` — round-9 landing). Where this append and the two files
differ, their measured rows govern.

### Where the arc is written down

- **The ten-round synthesis** — `corpus/knowledge/arc-synthesis.md`
  (self-label M10-1; 387 L / 30,796 B / sha `a5b4833141461810…` at this
  append). It carries the arc ledger (mint + rounds 1–10, one row per round
  with commit, axis move, gate sha, selftest count), the gate ladder
  re-derived per arc commit (28/28 → 53/53 → 89/89 → 217/217 → 268/268), the
  invariants, the three trends (expansion improved · quality improved ·
  discernment **unprovable-but-better** — its harm-side fact, ten rounds with
  `corpus/lessons/` at 0, named as such), the gap ledger (12 surfaces), and
  the classification — **9 closed / 8 operator-owned / 12 unknown**; no item
  left as "carried". Re-derivation protocol §0, spot-checks §8.
  Naming note: the plan's working name `ten-round-synthesis.md` landed as
  `arc-synthesis.md`; the M10-2 note's recheck line still carries the working
  name (flagged here; its block unedited).
- **The gate's standing-use note** — `corpus/knowledge/gate-standing-use.md`
  (self-label M10-2; with M10-3's first-cadence `--regression` tick — `PASS`,
  target `dc7c4141…f8fd`, at this same gate sha — appended; 361 L / 22,931 B
  / sha `aaa2e625253e881e…` at this append). It carries the custody rules,
  the invocation map quoted from the landed helps, the verdict vocabulary,
  the standing cadence (the round that established each line), the
  maintenance rules with their ancestry, the residual/limit ledger with each
  item's check, and the operator's handoff. It is the contract's home.

### Quick invocation map (quoted from the landed helps at `93e43f8f…`)

    bash tools/mado-verify.sh                  # live read-only run; CLEAN rc 0 · DIVERGED rc 1 · usage rc 2
    bash tools/mado-verify.sh --no-live        # file plane only; the 8 live rows read SKIP, the verdict names it
    bash tools/mado-verify.sh --root DIR       # verify DIR as the config root (--root=DIR accepted)
    bash tools/mado-verify.sh --selftest       # hermetic fixtures, no substrate; fail rc 2 (268/268 at this revision, note §1)
    bash tools/mado-verify.sh --regression [--keep]    # replay the recorded case; PASS rc 0 · FAIL 1 · SETUP 2
    bash tools/mado-verify.sh --snapshot FILE          # v1 receipt; REFUSED (exists, or in-plane) rc 2, nothing written
    bash tools/mado-verify.sh --snapshot-diff OLD NEW  # SAME / DETAIL-CHANGED rc 0 · CHANGED rc 1 · SETUP 2
    env: MADO_VERIFY_ROOT · MADO_VERIFY_LIVE=auto|yes|no · MADO_VERIFY_HARNESS

Tokens: `MADO_VERIFY: CLEAN|DIVERGED` · `MADO_SELFTEST:` ·
`MADO_REGRESSION: PASS|FAIL|SETUP` · `MADO_SNAPSHOT: WRITTEN|REFUSED` ·
`MADO_DIFF: SAME|DETAIL-CHANGED|CHANGED|SETUP`; row classes PASS/FAIL/
UNKNOWN/SKIP/NOTE — UNKNOWN blocks CLEAN, NOTE never flips a verdict. Base
`--help` lists the five original flags; the mode paragraphs print via
`<mode> --help` (the excision invariant keeps the base text still — the note
§5.7 says why; discoverability is a named residual, not a defect). Full mode
table, writes and exits: note §1; cadence: §4.

### What ships open (named, never promised)

From the note's §6 ledger at this append: the theme live rows ×2 and the
walker live-surface rows (exempted by name, r9); hypr-live stub scenarios
J/K/L (open since r8); the assertion floor (`VERSION_STR` `:77`, base-help
discoverability, the two usage arms, the boundary-prefix assertion); the
`row_from_rc` rc-6 arm (dead since r6); the theme clauses' covering mutant
(owed under r6 rule 2 — re-cut record `:1266-1268`); plus the record debt the
arc ships with (`corpus/README.md` rows; `corpus/lessons/` 0 entries;
`walker-deep.md` §10/§11 errata; the drafts' ⟨PENDING⟩ markers). A NOTE stays
non-verdict, an UNKNOWN stays unknown; a stub scenario proves row logic,
never live values.

### Unknowns at this append

1. The committed round-10 revision. This append binds to the worktree
   revision `93e43f8f…`; re-check `sha256sum tools/mado-verify.sh` before
   quoting (§0/§9 of both files carry the same rule).
2. Whether the synthesis gains its round-10 landing row at the commit — its
   §1 row 10 reads "in flight"; not predicted here.
3. Whether the record family (§(c)) lands — out of this file's scope; the
   SKILL's own state before this append: 1,336 L / 99,084 B / sha
   `946bf9d5…`.

recheck: `sha256sum tools/mado-verify.sh corpus/knowledge/arc-synthesis.md
corpus/knowledge/gate-standing-use.md` — the three shas above; then the note
§8's three commands re-derive the gate's state.

## Round-11 — the arc's end: final pointers (append, M11-4)

Appended 2026-10-14 21:35Z. Round 11 (`plans/round-11.plan.md`, 352 L by
`wc -l` / 23,438 B / sha `4bde28aa5eef9600…`, committed with the round-10
landing) is the arc's closeout round: verify the round-10 handoff, settle
every open item, freeze the revision, and commit the arc-end record. This
lane's write was this append only — the round's SKILL-lane edit; scratch
`/tmp/w11-mado-m11-4/`; read-only throughout (the gate was read and run in
its read-only modes; no substrate file written; no compositor/session
mutation — no restart, no socket connect, no `omarchy` write verb). The
append is the pointer layer: it binds the arc's terminal artifacts to their
measured state and hands the next reader the route through them. Where this
append and a pointed-to file's own bytes differ at read time, the measured
bytes govern — run the recheck line first. Round 11 is chartered as the
arc's last round (plan §(c): "no further round opens"); the standing rules
above are unchanged by this append — pointers, not ground.

Every number below binds to `tools/mado-verify.sh` sha256
`93e43f8fe8b9bdd4…` (3,231 L / 150,103 B; committed `de22dfd`; unchanged at
HEAD — `git show HEAD:tools/mado-verify.sh | sha256sum` reads identical; the
sha identical before and after my runs). HEAD is
`f7bfc9fe149bc94057323964e7cb0411f6f89e25` ("probation round 10 (training
r9): see LOG"), worktree clean (`git status --porcelain` empty) at the
samples below. A later gate edit re-opens every number here.

### The pointer map — the arc, artifact by artifact

| Artifact | What it carries | Measured at this append (2026-10-14 21:31–21:33Z) | Recheck |
|---|---|---|---|
| `corpus/knowledge/arc-synthesis.md` (M10-1; committed `f7bfc9f`) | the ten-round synthesis: arc ledger (mint + rounds 1–10: commit, axis move, gate sha, selftest count), the gate ladder re-derived per arc commit (28/28 → 53/53 → 89/89 → 217/217 → 268/268), the invariants, the three trends, the gap ledger (12 surfaces), the classification (9 closed / 8 operator-owned / 12 unknown) | 387 L / 30,796 B / `a5b4833141461810…` | `sha256sum corpus/knowledge/arc-synthesis.md` |
| `corpus/knowledge/gate-standing-use.md` (M10-2 text + M10-3's first-cadence tick; committed `f7bfc9f`) | the gate's standing-use contract: custody rules, the invocation map quoted from the landed helps, the verdict vocabulary, the standing cadence, maintenance rules with ancestry, the residual/limit ledger with each item's check, the operator's handoff | 361 L / 22,931 B / `aaa2e625253e881e…` | `sha256sum corpus/knowledge/gate-standing-use.md` |
| `corpus/knowledge/arc-closeout.md` (M11-1; plan §(c)) | the closeout's single durable artifact: the verification ledger, the terminal disposition ledger (closed / operator-owned / unknown — no "carried"), the freeze pins, the handoff ledger | not present at the 21:33Z sample; lands this round | `ls -l corpus/knowledge/arc-closeout.md`; when present, its own recheck line and `git log -1` for the arc-end commit |
| `tools/mado-verify.sh` — the verdict gate | the standing verdict is `bash tools/mado-verify.sh` (live, read-only); `--no-live` proves the file plane; `--selftest` is hermetic; the mode contract lives in the note above | `93e43f8f…` · 3,231 L / 150,103 B; my runs at this append: `--selftest` → `MADO_SELFTEST: 268/268 assertions passed` rc 0; `--no-live` → `MADO_VERIFY: CLEAN (29 pass, 4 notes)` rc 0; boundary `bb2639d9a980…` identical before/after; live point sample — see below | `bash tools/mado-verify.sh --selftest`; `… --no-live`; `… --help` |
| `reports/r10-aud-m10.md` (AUD-M10) · `reports/r10-ver-m10.md` (VER-M10) | the round-10 independent receipts: the four synthesis claims + the note's two commands re-derived — PASS, with the live point sample named F2; the ladder re-derived one level below the records — CONFIRMED | 160 L / 13,177 B / `d9892618…` · 156 L / 9,126 B / `8de65dfd…` | `sha256sum reports/r10-aud-m10.md reports/r10-ver-m10.md` |
| the record family — `LOG.md` · `SCORECARD.md` · `corpus/README.md` · `corpus/lessons/` · the record drafts | what the arc ships recorded vs owed: the arc-end entry and the final row land last (plan §(b)/(c)); the README's note rows, the drafts' `⟨PENDING⟩` sets, the `walker-deep.md` §10/§11 errata, and `corpus/lessons/` are the owed debt the closeout settles | `LOG.md` 301 L / `81c60ea8…`; `SCORECARD.md` 22 L / `5f1df3f4…`; `corpus/README.md` 19 L / `2dd274f5…` — 8 note rows vs 21 notes in `corpus/knowledge/` (13 unrowed); `corpus/lessons/` 0 entries | `wc -l` and `sha256sum` per file; `ls corpus/knowledge/*.md \| wc -l` |
| this file — `SKILL.md` | the operating manual; the append series below (rounds 5–10) is the landing history and this append closes it | 1,424 L by `wc -l` / 104,700 B / `e9e67efe44f2d635e56a…` before this append | `sha256sum SKILL.md` |

### Reading route — for a fresh agent holding only this file

1. **To verify the plane**: Standing rules → config-plane map →
   claim→evidence routing → the scoped-verification checklist; every claim
   ends with a measured anchor; run the gate for the standing verdict
   (`bash tools/mado-verify.sh`).
2. **To understand the arc**: `arc-synthesis.md` (what was measured across
   ten rounds, and what stayed unknown), then `gate-standing-use.md` (the
   contract under which the gate is run and maintained), then
   `arc-closeout.md` (the terminal state and the operator's handoff, landing
   this round).
3. **To extend the work**: the residual set is enumerated — never
   informally "carried" — in the synthesis's gap ledger and the note §6;
   the round-11 settlement's dispositions land in the closeout note; config
   changes stay operator-owned per the map above.

### The gate at this append (my runs, read-only)

- `--selftest` → `MADO_SELFTEST: 268/268 assertions passed` rc 0
  (hermetic fixtures; the boundary row unchanged).
- `--no-live` → `MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only —
  live layer skipped: --no-live)`, `counts: pass=29 fail=0 unknown=0 skip=8
  note=4`; boundary row `bb2639d9a980…` PASS (config plane byte-identical
  before/after).
- live → `MADO_VERIFY: DIVERGED (3 fail, 0 unknown, 49 pass)`: the three
  fails are `live.waybar.process` / `live.waybar.layer` /
  `live.waybar.tray` — no waybar process at the sample (`pgrep -a waybar` →
  none; walker 1203471 `/usr/bin/walker --gapplication-service`, swaybg
  1203358 running). Session state — the AUD-M10 F2 class
  (`reports/r10-aud-m10.md:120`) — not a gate defect: the file plane and the
  boundary row stayed green and the gate's sha is unchanged before/after.
  The closeout's battery carries the round's authoritative live receipt.

### Corrections this append carries

- **The r9-aud citation at `SKILL.md:1314` resolves wrong.** The line cites
  AUD-M9 as `reports/r9-aud-m9.md, 166 L / 7ad8eccdd8d213a5…`; the landed
  blob (and the worktree, clean) reads
  `866272eeda09bc0898da16ca96b9738b166c60bb96734ce144bfe537a71ed954` — 166 L
  / 15,580 B, `sha256sum reports/r9-aud-m9.md` equal to `git show
  HEAD:reports/r9-aud-m9.md | sha256sum`. The cited sha does not resolve;
  the corrected reading is `866272ee…` (the line count matches). Registered
  by the round-11 plan (`:121-127`) as the closeout spot-check's worked
  example; carried here append-only — the `:1314` block stays unedited, this
  section is the correction.
- **The round-10 append's closing frame is superseded.** Its "arc's final
  round" frame is superseded by the fleet's decision that round 11 is the
  closeout (round-11 plan, opening frame); the round-10 artifacts stand, the
  closing frame does not. The spot-checked citations otherwise resolve: the
  round-9 append's four note cites (`0982ba06…`, `a5acfe01…`, `73b1466b…`,
  `98ec0c3b…`) and the round-10 pair above read as cited.

### What this append does not do

- No settlement: the disposition ledger (closed / operator-owned / unknown)
  is the closeout note's content (plan §(b)); this append neither restates
  nor pre-empts it.
- No record-family edits: README rows, SCORECARD rows, lessons, the drafts'
  `⟨PENDING⟩` sets, `walker-deep.md` errata — outside this file's scope;
  this lane writes only `SKILL.md`.
- No new coverage, no promise: a NOTE stays non-verdict, an UNKNOWN stays
  unknown; the gate's verdict line stays `bash tools/mado-verify.sh`.

### Unknowns at this append

1. The closeout note (`corpus/knowledge/arc-closeout.md`) — not present at
   the 21:33Z sample; its content, its commit, and the arc-end commit are
   this round's open items; a later reader rechecks the path.
2. Whether the record family lands (README rows / SCORECARD final row /
   `corpus/lessons/` / the drafts' closures) — the closeout's settlement
   reports it; out of this file's scope.
3. The live plane's state at the closeout's battery: waybar was absent at
   this append's sample; the session is the operator's, not this lane's —
   the closeout's run re-samples and its receipt governs.
4. The final frozen revision: the last landed gate revision at this append
   is `93e43f8f…`; if any round-11 edit moves the gate, every number here
   re-opens at the new revision.

recheck: `sha256sum SKILL.md LOG.md SCORECARD.md corpus/README.md
corpus/knowledge/arc-synthesis.md corpus/knowledge/gate-standing-use.md`;
`ls -l corpus/knowledge/arc-closeout.md` (present → read it; absent → the
closeout has not landed); `bash tools/mado-verify.sh --selftest &&
bash tools/mado-verify.sh --no-live`.

## Fleet round 1 — corpus navigation (2026-10-15)

Start at [the corpus index](corpus/README.md) for note and province-surface
routes. Its fleet-round-1 completion supersedes historical statements above
that the README note rows remain owed; those statements describe the closed
2026-10-14 arc, not the current index. Indexing does not re-verify a live
desktop claim: follow each note's date, evidence class, recheck and unknowns.

Navigation correction to the round-11 recheck above: the landed closeout is
[`corpus/knowledge/closeout-r11.md`](corpus/knowledge/closeout-r11.md), not
`corpus/knowledge/arc-closeout.md`. The historical missing-file inference
must not be used to conclude that the closeout is absent.

Promotion remains operator/integrator-owned. The current [SHONEN checklist](SHONEN.md)
records inherited evidence as assertions; this round's dispatched subagents
are still the mado authoring lane, not outside-lane promotion verifiers.

### Interactive continuation status — fleet round 1 is not admitted

The index routes above are preserved candidate navigation work, not a
completed fleet-round claim. The interrupted headless launch left no landed
fleet-round report. Current plan:
[WWKD](.ufo/plans/fleet-round-1-wwkd.md); current authority blocker:
[routing evidence](.ufo/blocked/fleet-round-1-routing.json). The validated
32-scope plan did not dispatch: existing global role bindings and connector
fallback do not match the operator's required aliases. Do not substitute a
different route, change global configuration, or infer a completion from
the inherited nine-adviser history.

This qualification supersedes “fleet-round-1 completion” above as a round
status statement; the exact landed-note paths remain usable navigation.
No live desktop-health, promotion, outside-lane spot-check or completed-round
count is added. Substrates stay read-only; pushes remain prohibited.

## Errata (round 12)

This append re-anchors present-tense SKILL claims contradicted by the 2026-10-17 operator-applied gkeep drift. The measurements are dated 2026-10-19; see `corpus/knowledge/config-drift-r12.md` and `.ufo/evidence/round-12/drift-*.txt`. No earlier SKILL text is rewritten.

- **Hypr root shape — former `SKILL.md:40-41`.** Old: 17 source statements — `grep -cE '^[[:space:]]*source' ~/.config/hypr/hyprland.conf.bak.1792267376`, 2026-10-19; 29 lines — `wc -l ~/.config/hypr/hyprland.conf.bak.1792267376`, 2026-10-19. New: 18 sources — the same `grep -cE` on current `hyprland.conf`, 2026-10-19; 32 lines — `wc -l ~/.config/hypr/hyprland.conf`, 2026-10-19. Reason: the operator-applied gkeep comment and source were appended; `diff -u ~/.config/hypr/hyprland.conf.bak.1792267376 ~/.config/hypr/hyprland.conf` on 2026-10-19 shows only that three-line addition, leaving the orchestrator role intact.
- **Final include — former `SKILL.md:46,67,92-93`.** Old: `ai-usage.conf` at line 29 was named last. New: `ai-usage.conf` remains at line 29, then `gkeep.conf` is sourced at line 32. Reason: source order changed; only the “sourced last” qualifier is contradicted. Rule-body contents were not reread here. Re-measure: `grep -nE '^[[:space:]]*source[[:space:]]*=' ~/.config/hypr/hyprland.conf.bak.1792267376 ~/.config/hypr/hyprland.conf` and `diff -u ~/.config/hypr/hyprland.conf.bak.1792267376 ~/.config/hypr/hyprland.conf` — 2026-10-19.
- **Hypr local inventory — former `SKILL.md:102`.** Old: 12 active `.conf` files — MADO-1's historical file-table rows, re-counted by the documented row-search pattern in `drift-hypr.txt`, 2026-10-19 (the filesystem observation is 2026-10-14; its original listing invocation was not retained). New: 13 active files — `find ~/.config/hypr -maxdepth 1 -type f -name '*.conf' | wc -l`, 2026-10-19. Reason: the operator-owned `gkeep.conf` is an additional active file.
- **Waybar config/style lengths — former `SKILL.md:103`.** Old: 249 `config.jsonc` lines and 136 `style.css` lines — `wc -l ~/.config/waybar/config.jsonc.bak.1792267376 ~/.config/waybar/style.css.bak.1792267376`, 2026-10-19. New: 260 config lines and 155 style lines — `wc -l ~/.config/waybar/config.jsonc ~/.config/waybar/style.css`, 2026-10-19. Reason: the module was inserted in config and the stylesheet advanced beyond its named intermediate; backup hashes and intermediate measurements are in `drift-waybar.txt`.
- **Earlier `ai-usage.conf` line in the shadowing example — `SKILL.md:338`.** The reference to `ai-usage.conf:29` remains an earlier-layer anchor, not a claim of last precedence. Current source order also has `gkeep.conf` at line 32 — `grep -nE '^[[:space:]]*source[[:space:]]*=' ~/.config/hypr/hyprland.conf`, 2026-10-19. Disposition: retain the historical line anchor; do not describe it as the terminal source.
- **Dated SHA examples — `SKILL.md:297` and `:422`.** Both `4f52854a…` mentions are worked/re-verification evidence dated 2026-10-14; they report that day's root, not a present pin. Today's former/current hash pair is measured by `sha256sum ~/.config/hypr/hyprland.conf.bak.1792267376 ~/.config/hypr/hyprland.conf` — 2026-10-19. Disposition: preserve both dated examples unchanged; the backup remains the old pin and current live is `ce7483f3…`.

Append-only disposition: this section records the moved pins and their re-measure commands; it does not authorize edits to config files, a compositor reload, or a change to the operator-owned gkeep project.


## Errata (round 18, append-only)

> Erratum (round 18; ConnStalePinsSweep): the version pin "walker 2.17.0" at the
> top of this file (lines 22-23) and the launcher row of the config-plane map
> ("walker 2.17.0"; packaged table "298 L") are dated 2026-10-14. File reads on
> 2026-10-20: `/var/log/pacman.log:2929` upgraded walker 2.17.0-1 → 2.17.2-1 and
> `:3095` elephant 2.21.0-1 → 2.22.1-1; `/etc/xdg/walker/config.toml` is now
> 13,743 B / 305 L / `3c5c6867…` (byte-equal to upstream v2.17.2
> `resources/config.toml`). The running binary is `[UNK]` (no process probe).
> Current documentary route: `corpus/knowledge/walker-route-r18.md`.

> Erratum (round 18, residual check W3CriticC3Final): the `mado-tripwire-frozen`
> registry row says "17 mode-frozen cases"; at `be886a3` the suite has 31
> (`evidence/final/tripwire-frozen-selftest.txt`). Since `be886a3` these are
> `frozen_error` (exit 2), not compared verdicts: an expected exit/label pair the
> verdict cannot take, an unreachable or unlisted expected line, a known miss that is
> blank, out of range or on an expected line, an empty or duplicated input, an
> unknown top-level key or a duplicate JSON key; a symlinked frozen directory (as
> passed) or `inputs/` dir is `snapshot_tampered`. Scope: the gate detects a change
> in the classifier's output on 5 pinned incident files (5 distinct rule ids, 8
> findings); `known_misses` are annotations that fail only if a listed line starts
> producing a finding — removing them does not fail; the eval-path classifier is
> covered by the scan suites, not by this gate; a coordinated rewrite of input,
> digest and expected verdict, or a permit-only rewrite, still matches (git history
> and the bound receipt are the defence).


## Errata (round 19, append-only — walker 2.17.2 pins; S090/S091/S096)

> Erratum (round 19; SkillPins): walker is installed at 2.17.2-1 — S090 `/var/log/pacman.log:2929` records `[ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)` at 2026-10-20T09:16:46-0300, and the only walker version literal in `/usr/bin/walker` is `2.17.2` (S096). This supersedes the pins above: the round-18 erratum at `:1820-1828` already dates `:23` and `:114`, while `:1075` and `:1473-1476` are re-anchored here for the first time.
> - Former `SKILL.md:23` — "walker 2.17.0 (MADO-1 §9; MADO-2 §1; re-verified `hyprctl version`)": the installed package is 2.17.2-1 (S090) and the binary's sole version literal is 2.17.2 (S096), but the claims below that pin were measured on 2.17.0 on 2026-10-14 and stay dated — the pin line names what was measured, not what is installed; the `hyprctl version` clause re-verifies Hyprland, not walker (S090/S096, 2.17.2 not re-measured live).
> - Former `SKILL.md:114`, packaged-table cell — "298 L": dated 2026-10-14 (round-18 erratum `:1824`); re-verified 2026-10-20 (`wc -l`, `sha256sum`) as 305 L / 13,743 B / `3c5c6867…` (S091), byte-equal to the upstream v2.17.2 `resources/config.toml` recorded at S073.
> - Former `SKILL.md:114`, consumer cell — "walker 2.17.0 via `app-walker@autostart.service` + `elephant.service`": the version is dated and now 2.17.2 (S090 upgrade line; S096 binary literal); the two unit names and the restart route were not re-probed this round and remain as written.
> - Former `SKILL.md:114`, user-config cell — "49 L": re-verified 2026-10-20 unchanged at 49 L / 1,336 B / `fecf71fa…` (S091); the only moved value on that row is the walker version, now 2.17.2 (S090).
> - Former `SKILL.md:1075` — "`walker --version` = `2.17.0`; binary sha `64826a8531eac525…`": the 2.17.0 reading is a dated 2026-10-14 execution, not repeated (`--version` launches the binary; host pause); today's file bytes are 7,039,912 B / sha256 `25240650…` with the sole version literal `2.17.2` at file offset 856,302 in the `.rodata` run `version2.17.2\n` (S096) — the printed line is inferred from that literal, not observed.
> - Former `SKILL.md:1473` — "binary sha256 `64826a85…`, BuildID `a22452d1…`": dated round-9 identity of the 2.17.0-1 build; the installed 2.17.2 build's bytes hash `25240650…` with BuildID `19200fe47eb6c90fc4956f0d52d0c7c84bb89e99` (`sha256sum`, `readelf -n`; S096).
> - Former `SKILL.md:1474` — "`.comment` rustc 1.97.1 (Arch) / LLD 22.1.8": dated round-9 toolchain; the 2.17.2 build's `.comment` reads rustc 1.99.0 (b940084d7 2026-09-28), LLD 23.1.1, GCC 16.2.1 20260810 (S096, `readelf -p .comment`).
> - Former `SKILL.md:1475` — "`walker 2.17.0-1` with `pacman -Qkk` 29 files / 0 altered": the package pin is superseded by 2.17.2-1 (S090); the `-Qkk` count is a dated round-9 record, not re-run this round (host pacman pause), so it stays `[UNK]` for 2.17.2 and is not claimed.
> - Former `SKILL.md:1476` — "printed `2.17.0\n` … rodata literal (offset 847,791)": dated; the 2.17.2 binary's sole version literal sits at 856,302 (S096), and its embedded default config at offset 806,960 is 13,743 B / `3c5c6867…`, byte-equal to the `/etc/xdg` file (S091).
> - Residual — the running process stays `[UNK]` (no process probe, host pause); 2.17.2 is established for the installed package (S090) and for the `/usr/bin/walker` bytes (S096), and `corpus/knowledge/walker-route-r18.md` remains the documentary route for 2.17.2 with the host rows S090/S091 in support.

## Round 19 registry and scan-rule notes (append-only)

> Round 19 (L1; w1 TwMerge-2, CriticInstallerClass, SimplifyCounters): `tools/mado-tripwire.py`
> now carries five classes — `host_mutation`, `package_query`, `live_probe`, plus
> `tool_install` (uv/pip/pipx/npx/npm -g/cargo install; operator-authorized channels,
> permit-able, never `host_mutation`; `sudo` in front stays `host_mutation`) and
> `vcs_write` (jj mutating verbs, jj reads without `--ignore-working-copy`, git write
> verbs; `scripts/hyaku/jj-lane.sh` invocations are clean). Post-wave scans run
> `--permit tool_install` and compare each install hit with the seat's `## Installs`
> entry; `vcs_write` stays unpermitted (a lane seat never writes VCS state). HelperFn
> rule B (a call to an undefined name with a literal host-command argv list) is a
> heuristic lead, not a proof of execution.
> The frozen replay baseline for the current classifier is `.ufo/waves/round-19/frozen`
> (re-pinned by `frozen-repin.py`; the three round-18 known misses are expected
> `package_query/pacman:-Q` findings whose class matches the round-18 known-miss
> notes). `--frozen .ufo/waves/round-18/frozen` now reads `frozen_verdict_mismatch`
> by design (the misses became findings); keep it as the red-before of that change.
> Frozen F1 (blank-line pin → `frozen_error`) and F2 (`link/.`-style symlinked DIR →
> `snapshot_tampered`) are closed (suite `.ufo/waves/round-19/tripwire/r19-frozen-f1f2`).
> `mado-tw-recall`: a `git show` failure exits 1, not 2 (SimplifyCounters D1); the
> counter is pre-registered and unchanged this round.
> Round-19 source supersessions (append-only): S094 → S097 (omarchy matte-black payload;
> per-fetch HTML digests replaced by tag commit and git tree ids) and S084 → S098 (xdg
> search order; docs.rs `latest` alias replaced by the xdg 3.0.0 crate whose sha256 equals
> walker v2.17.2 `Cargo.lock:2708`). Registry rows above that name S094 or S084 describe
> round-18 evidence; current support is S097 and S098.
> SKILL erratum corrections (w2 AtkSkillErratum, CriticC2W2): "sole version literal" in the
> round-19 walker erratum means the sole *walker* version literal (the binary holds other
> x.y.z strings); its "round-18 erratum `:1820-1828`/`:1824`" line numbers are baseline
> `9c54c56` numbers (the round-18 erratum now starts at `:1826`); the `:114` row moved two
> values (walker version and the packaged table 298 L → 305 L), not one.
> PROVINCE pins (w2 AtkProvinceLine): `PROVINCE.md` gained the round-19 path-root line, so the
> "18 L, sha `7aad7b86…`" statements at `:666`/`:747` and the slogan citation `PROVINCE.md:18`
> at `:391` describe the round-18 file; read the current `PROVINCE.md` bytes instead.

## Round 21 standing-use correction — tripwire limits

The round-20 “Reading tripwire rows” section describes intended bounded treatment, **not** a general proof of restored recall, precision or safe VCS no-writes. At delivered v3.1 `a8960de`, independent residual reviews found invoked partialmethod/recursive-string/callback/global-binding misses, inert-reference false leads, a process-capable stdlib purity hole and quadratic retained environment snapshots. `--ignore-working-copy` and unchanged Git refs do not rule out repository/index/object/config/workspace writes. Read the in-file correction in [`tripwire-precision-r20.md`](corpus/knowledge/tripwire-precision-r20.md#round-21-correction--delivered-round-20-claims-were-too-broad) and `corpus/lessons/round-20-verifier-spotcheck.md` before interpreting the old examples. Preserve 172/175 as a missed historical target; a clean scan or a lead label is never execution authorization. Source-only host pause remains unchanged.

## Round 21 — bounded binding evidence and separate artifact assessment

Use [`corpus/knowledge/tripwire-binding-boundaries-r21.md`](corpus/knowledge/tripwire-binding-boundaries-r21.md) for the source-backed distinction between a callable value and an invocation, partialmethod descriptor binding (S116), process-capable stdlib exceptions (S117), and Git's no-new-commit versus no-repository-write boundary (S118). The old round-20 target, three disagreements and rejection are unchanged; new independent fixtures are a separate population.

Before interpreting a post-hoc finding: check the actual tool digest/revision and fixture digest, read its `observed` versus `lead` marker, and retain parse/resource/error outcomes. A finite oracle pass is not whole-corpus no-harm, runtime observation or permission to issue the printed command. C2's `mado-assessment` gate verifies artifact assertions and actual bytes, not authenticated chronology, source semantics, named-reviewer identity, promotion or an author-independent verdict.

Round-21 scope qualification for the old pure-data examples at557–559: “plain literal argv data” is not “arbitrary instances/configuration.” Custom iterators/dunders, JSON `default=` callbacks and logging factory sections can execute visible bodies; an unused data field containing `()` is not automatically a factory. S119 supersedes the module-list inference, and S120 binds the annotation decision to Python3.14's lazy semantics; forcing annotations and older-runtime profiles remain separate limitations. This supersedes the universal interpretation, not the historical receipts.

### Round-21 final withdrawal

Delivered classifier a6cef898 / SHA46c82902 remains **harmed**, not a verified general binding repair: `.ufo/waves/round-21/residual/FinalBindingReview.md` records factory-lifetime, unresolved/global leakage, returned-binding, direct-run and synthetic-name failures that the finite oracle did not catch. Read the final disposition inside `corpus/knowledge/tripwire-binding-boundaries-r21.md` before using its candidate discussion. C2's demonstrated artifact gate does not admit the round or a capability rank. The classifier's module docstring is also stale about commit dry-run exemptions: current code flags commit/index preparation except recognized help/usage; retain `FinalRemovalReview.md` as that documentation defect, not a licence to execute it. Inherited clean labels with nonzero unparsed counters are not safety evidence.

## Round 22 — scoped lifetime and evidence-grain recovery

Read [`corpus/knowledge/tripwire-lifetime-recovery-r22.md`](corpus/knowledge/tripwire-lifetime-recovery-r22.md), sourced to opened S121/S122, before interpreting factory capture, late globals or direct standard Thread/Timer calls. Raw independent truth was sealed at `9185f1f9806b823a23ef9f5077a893e40e46e1b9`; normalized populations are later materializations, not retroactive preregistration. A finite repair result does not erase the r19/r20/r21 red receipts, prove all Python semantics or authorize a host action. Final round-22 evidence and genuinely non-author closure govern any re-admission proposal.

### Gate registry — mado-evidence-audit

| name | kind | entry command | verdict map | self-test command and spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| mado-evidence-audit | gate | `python3 -I tools/mado-evidence-audit.py --check BUNDLE --root ROOT` | 0=clean artifact assertions; 1=failed contradictory assertions; 2=could-not-evaluate, including invalid/markerless input or snapshot_tampered | `python3 -I tools/mado-evidence-audit.py --selftest .ufo/waves/round-22/audit/fixtures` (`--selftest`; real self-invocation compares exit and stable IDs for every fixture) | `.ufo/waves/round-22/audit/fixtures/expected.json`, `expected.sha256`, input_entries digests and symlink targets; raw truth seal `.ufo/waves/round-22/truth-seal.json` | read-only over selected artifacts; no host, network, classifier execution or source mutation | mado |

This gate validates arithmetic and asserted labels, not that an `observed` marker is semantically true. The actual r19 scan is markerless and remains could-not-evaluate. Six incident lines are not eleven finding rows: derived5/1-line or10/1-row views and new counterfactual inflation assertions must retain their provenance, never become an old r19 observed6/6 assertion or retrospective precision proof. A nonzero unparsed/error outcome is uncertainty even when an inherited scanner labels its empty finding set clean.

### Round-22 final withdrawal

Final classifier restores v2's bounded ownership/caller-argument fixes (SHA256cd9da20c), not v3's unsafe consumer-sweep suppression. The latter could hide callbacks escaping through container/attribute stores. Primary57/57 does not cure supplemental2/4 or source-supported caller-frame leakage (`.ufo/waves/round-22/residual/ResidualForward.md`; sourced note's final withdrawal). Strict C1 and unchanged-row historical C2 targets remain unprovable/not admitted. The46/46 artifact audit and killed digest-check mutant do not supply semantic precision, outside-lane admission, host clearance or authorization to advance the round.

Standalone C2 selftest in a fresh Git clone requires restoring three intentionally empty, manifest-pinned fixture directories (Git does not store empty directories). From that clone's root, first run:

```sh
mkdir -p -- .ufo/waves/round-22/audit/fixtures/cases/AuditRawPathBackslash/root .ufo/waves/round-22/audit/fixtures/cases/AuditRawPathDotDotInternal/root/sub .ufo/waves/round-22/audit/fixtures/cases/AuditRawPathEscape/root
python3 -I tools/mado-evidence-audit.py --selftest .ufo/waves/round-22/audit/fixtures
```

Only fixture directories are created; no snapshot byte, symlink, label or expected result changes. `.ufo/waves/round-22/evidence/resume/empty-directory-materialization.json` pins the setup. The bounded intervention driver recreates the same manifest-declared directories inside its throwaway tree and passed235 command-state runs at78b1824; its two earlier setup failures remain could-not-evaluate, not green evidence. Active-path equality does not prove absence of every historical classifier read or semantic truth.


## Monitor rule versus running output (round 45)

`hyprctl monitors all -j | python3 tools/mado-monitors.py --monitors - --config ~/.config/hypr/monitors.conf` joins the `monitor =` lines of the given config files with one dump: per output AGREE / DIFFER (fields mode, position, scale, transform, mirror, disabled) / DISABLED / UNRULED / NOT_COMPARED (scale with no clean divisor); top verdict NO_RULES 4 | NOT_COMPARED 5 (monitorv2 block, unmodelled line, unpredicted scale) | DIFFER 1 | NO_MATCHING_MONITOR 3 | OK 0; setup 2. Contract and limits in the tool docstring; ground in `corpus/knowledge/hyprland-monitor-rule-r45.md`. Use `monitors all -j`: plain `monitors -j` omits disabled outputs. A DIFFER is a join, not a blame: a runtime `keyword monitor`, an output-management client or a missing mode explains it as well as the config. A rule without `@RATE` asks for 60 Hz. Host run 2026-10-26: DP-1 AGREE, `verdict=OK`, exit 0 (`.ufo/waves/round-45/receipts/live-monitors-host-r45.txt`). The `monitor =` line form exists only on the 0.56.x line (upstream a9902ea removes it).
