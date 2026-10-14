---
name: mado-shokunin
description: Domain specialist — desktop & compositor craft. Rank: shonen (probation).
---

# mado-shokunin

desktop & compositor craft playbook — the Hyprland/waybar/walker/terminal config plane
and display behavior on this host. Probation seed — rounds 1-3 build the corpus from
measured surfaces; every rule below earns a cited source before it counts. Nothing here
is oral knowledge.

**Probation round 1 sources** (measured 2026-10-14, read-only, in `corpus/knowledge/`):
- `hyprland-config-plane.md` (MADO-1) — hypr tree, include graph, override chain, keybinds, window rules, animations, runtime.
- `waybar-walker-plane.md` (MADO-2) — bar/launcher/notification/idle-lock plane, drift vs stock, decision table, rejections.
- `terminals-and-omarchy.md` (MADO-3) — terminal configs, theme plane, install state, omarchy skill anatomy.

Version pins for all claims below: Hyprland 0.56.2, Omarchy 3.8.3, waybar v0.15.0,
walker 2.17.0 (MADO-1 §9; MADO-2 §1; re-verified `hyprctl version`, `omarchy version`).
Re-verify pins before reusing a claim under a newer version — window-rule syntax in
particular changes between releases (omarchy skill `~/.agents/skills/omarchy/SKILL.md:300-305`).

## Standing rules

- Read-only substrates unless PROVINCE.md declares a write surface;
  detection-and-report for operator-owned remediation.
- Secrets shape-only, never content-read.
- Every claim: measured anchor (path:line, command output, evidence id).
  Observation / inference / unknown stay separate.
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
| Env vars (NVIDIA + GDK_SCALE) | `~/.config/hypr/envs.conf:3-5`; `monitors.conf:9` | file read | MADO-1 §2 |
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

Persist nothing into config trees; screenshot artifacts, if kept, live under the lane repo.
OBS/INF/UNK stay separate and errata are append-only (corpus/QUALITY.md:1-5); a rejected
claim is kept, never silently dropped (MADO-2 §9 model).

## Omarchy boundary — skill instructs, mado measures

`~/.agents/skills/omarchy/SKILL.md` (392 lines, single file, no assets — MADO-3 §7) is the
domain's instruction authority for end-user customization; PROVINCE.md:10-11 declares it a
read-only documentation surface for this lane. Two actors, one substrate:

- **The skill instructs the editing actor** — it carries the rituals mado cites but does
  not execute: hypr auto-reload + validation pair (`:145-148`), waybar restart (`:159`),
  terminal restart (`:172`), walker restart (`:203`), mandatory `unbind` before rebind
  (`:272-286`), window-rules wiki re-fetch (`:300-305`), never-edit-source rules
  (`:41-47`, `:373-378`).
- **mado measures the substrate** — with the probe table above; a finding is a measured
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
   (MADO-2 §9; `omarchy menu keybindings --print` this pass).
3. **The skill writes for an editing assistant; mado is stricter.** Edits it authorizes in
   `~/.config/` remain operator-only for this lane (PROVINCE.md:10-12). When the two rules
   disagree, the stricter one wins for mado.
4. **Skill drift is a finding, not a licence.** Report the pair (skill line vs measured
   state); corrections go to the append-only errata of the source note, never into the
   skill file.

## Round 1 sources and evidence trail

- `corpus/knowledge/hyprland-config-plane.md` (MADO-1, 218 lines): inventory §2, include
  graph §3, keybinds §4, window rules §5, animations §6, override chain §7, separate
  consumers §8, version pins §9, runtime §10, open items §12.
- `corpus/knowledge/waybar-walker-plane.md` (MADO-2, 365 lines): inventory §1, waybar §2,
  walker §3, notifications/OSD §4, idle/lock §5, drift vs stock §6, decision table §7,
  unknowns §8, rejections §9.
- `corpus/knowledge/terminals-and-omarchy.md` (MADO-3, 180 lines): terminals §1-2,
  invariants §3, theme plane §4, install state §5, backup delta §6, skill anatomy §7.
- Re-verified anchors this pass: binds=192; `gaps_out`=0 via toggle; `input:kb_layout`=br;
  hypridle inactive + no PID; `makoctl mode`=default; `omarchy theme current`=Matte Black;
  `hyprctl configerrors` empty; `grim -t ppm -` 14,860,817 B, nothing persisted.
- Later rounds append: error patterns, executable checklists, verifier wiring — each with
  its measured anchor.
