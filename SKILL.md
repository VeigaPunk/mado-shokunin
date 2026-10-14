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
| Idle timings (150 s screensaver / 152 s lock) | `~/.config/hypr/hypridle.conf:10,16` — separate consumer, NOT sourced by hyprland.conf | `systemctl --user is-active hypridle`; `pgrep -x hypridle` — inactive/absent, cause unknown | MADO-1 §8/§10; MADO-2 §5 |
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
| bar (waybar) | `~/.config/waybar/config.jsonc` (249 L), `style.css` (136 L) (MADO-2 §1) | waybar v0.15.0 running (PID 1707, parent = Hyprland; MADO-R3-1 §1); style auto-reloads (`config.jsonc:2`); modules need `omarchy restart waybar` | measured ledger (MADO-R3-1 §2.3, re-verified): bar surface via `hyprctl -j layers` (levels `2` → namespace `waybar`, pid 1707, `3440 26`); tray via `busctl --user get-property fr.arrouillard.waybar /StatusNotifierWatcher …`; **no IPC/query verb in 0.15.0** (`waybar --help` = config/style/log/bar only) → module text config-only, reconstruct via pure-read producers (`RUN`) | `omarchy restart waybar` |
| launcher (walker) | `~/.config/walker/config.toml` (49 L; packaged table `/etc/xdg/walker/config.toml`, 298 L — MADO-R3-1 §6) | walker 2.17.0 via `app-walker@autostart.service` + `elephant.service`; restart `omarchy restart walker` | file bytes; `systemctl --user status app-walker@autostart`; `hyprctl -j layers` when open (absent when closed); D-Bus `dev.benz.walker` (`org.gtk.Actions.List` → `as 0`); sockets shape-only (MADO-R3-1 §6.7/§6.8) | same |
| notifications / OSD | `~/.config/mako/config`, `~/.config/swayosd/{config.toml,style.css}` (MADO-2 §4) | Mako owns `org.freedesktop.Notifications` (PID-measured); swayosd-server separate | `makoctl mode`; `busctl --user status org.freedesktop.Notifications` | restart/reload commands |
| idle / lock / sunset / xdph | `hypridle.conf`, `hyprlock.conf`, `hyprsunset.conf`, `xdph.conf` (MADO-1 §8) | separate consumers, outside the include graph; hypridle declared by default autostart `exec-once` yet measured inactive | `pgrep`/`systemctl --user is-active`; config values = file bytes only | start/stop services |
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
| Bar runtime facts (running? mapped? tray? module text) | hyprctl live + consumer-side probe | `hyprctl -j layers` (namespace `waybar`, pid, geometry); `pgrep -x waybar`; tray via `busctl --user get-property fr.arrouillard.waybar /StatusNotifierWatcher …`; indicator scripts probe process/mako mode (`RUN`, e.g. `idle.sh:3`) | `[OBS]` (MADO-R3-1 §1/§2.3); module text without an IPC verb → `[UNK]` |

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