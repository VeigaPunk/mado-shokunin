# ReviewLibinput — U6 integration risk: tools docs default configuration vs compositor runtime state

Lane: mado-shokunin · round 15 · wave w1 · member `ReviewLibinput` (reviewer, leaf)
Scope: adversarial review of one integration risk for the U6 input-debugging rung. No event observation, recording, replay, raw device reads, injection, kernel diagnosis, or compositor mutation. No tests, gates, builds, or formatters.

## Verdict

The risk is real and already has a lane precedent. Libinput's helper-tool docs say `libinput list-devices` (and the GUI variant) reports **libinput built-in defaults, not the desktop's configuration**. The compositor's effective settings come from its own config and are read through Hyprland's own surfaces (`hyprctl getoption`, `hyprctl devices`). A U6 note MUST keep these two planes separate. Lesson M04 in `corpus/lessons/round-12.md:37` already names the inverse inference as a trap. I found no round-15 draft that repeats it yet (no `corpus/knowledge/` U6 entry or round-15 draft text exists on disk at review time), so this is a gate for the InputDraft / ReceiptSafety / SourceChain landings, not a finding against landed text.

Recommendation: **accept** a U6 layer rung that cites the libinput docs only as docs-era defaults and cites Hyprland `getoption`/`devices` only as compositor-side reads, with the conditions below. **Reject** any sentence that equates the two planes.

## Findings (by severity)

**F1 — HIGH — The inverse inference is the lane's own recorded trap.**
- `corpus/lessons/round-12.md:37` (M04): "`libinput list-devices` proves the compositor-applied keyboard/touchpad settings." Recorded as an inference trap, `[INF-docs]`, discernment criterion 15.
- `.ufo/waves/round-13/w1/SiblingOverlap.md:68` routes `libinput list-devices` as "Reflects kernel/libinput defaults, not Hyprland `input.conf` parsing (`lessons/round-12.md` M04)." Any U6 layer row that uses list-devices as host state reopens M04.
- Primary text (libinput 1.32.0 docs, `https://wayland.freedesktop.org/libinput/doc/latest/tools.html`, section "libinput list-devices"): "This tool does **not** show your desktop's configuration, just the libinput built-in defaults." The same note appears under "libinput debug-gui": "This tool does **not** use your desktop's configuration, just the libinput built-in defaults."
- FAQ "Can I write a program to make libinput do $FOO" (`https://wayland.freedesktop.org/libinput/doc/latest/faqs.html#can-i-write-a-program-to-make-libinput-do-foo`): "The only way to modify libinput's behavior is to use the configuration options exposed by the respective compositor." This is the doc-level reason a debug tool cannot show compositor state. `debug-events` runs its own libinput context (same FAQ, diagram "libinput context 2").

**F2 — HIGH — Docs-era mismatch on the Hyprland side.**
- Host evidence: `.ufo/evidence/round-12/configera-host.txt:87` `configProvider: hyprlang`; `:102` `[OBS]` Hyprland 0.56.2 with `configProvider: hyprlang`; `:103` `[UNK]` which file the running instance opened.
- The Hyprland wiki pages I opened are Lua-era: `https://wiki.hypr.land/Configuring/Advanced-and-Cool/Devices/` documents `hl.device({ name = ..., sensitivity = ... })` and says "Since Hyprland 0.55, hyprlang is deprecated in favor of lua." Its page header says "Looking for the old hyprlang syntax? Check the 0.54 wiki pages." Page `https://wiki.hypr.land/Configuring/Basics/Variables/` carries the same deprecation note. Both pages are "Latest git" (modified 2026-08-26).
- Consequence: the per-device syntax on the page is not the host's syntax. Per-device claims cannot be sourced from these pages. Hyprland's "Using hyprctl" page (`https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/`) says hyprctl calls are "dispatched by the compositor synchronously," which is a cost note, not an era anchor.

**F3 — MEDIUM — Version mismatch and no host list-devices output.**
- libinput docs are 1.32.0 (tools.html header). Installed `libinput` is `1.31.3-1` (`pacman -Q libinput`). `libinput-tools 1.32.0-1` exists in the `extra` sync DB (`pacman -Si libinput-tools`) but is not installed.
- Static check of the installed `libinput` file list (`pacman -Ql libinput`) shows no `bin/` or `man1` entries, and `command -v libinput` is empty. So the host has no libinput CLI, and there is no host list-devices output to compare with the doc's sample. The doc sample (`SynPS/2 Synaptics TouchPad ... Tap-to-click: disabled`) is docs-era, not host evidence.
- The doc also says the output "is intended for human-consumption and may change its output at any time." Any U6 row must not treat a field name or sample line as a stable contract.

**F4 — MEDIUM — Coincidence risk on defaults that agree.**
- `input:accel_profile` reads `str: [[EMPTY]]`, `set: false` (`corpus/knowledge/hyprctl-verification-layer.md:127`; `corpus/knowledge/config-health-report-r3.md:541`, `:824`). The lane classed it `live-default`.
- libinput configuration doc (`https://wayland.freedesktop.org/libinput/doc/latest/configuration.html`, "Pointer acceleration"): "Most devices have their default profile (usually called "adaptive") and a "flat" profile." An unset Hyprland option *may* leave libinput's default in place, but that is `[INF]`. A per-device override (F2 syntax) or a compositor-internal default could differ, and the lane's global `getoption` cannot see per-device values.
- `input:touchpad:natural_scroll` reads `int: 0`, `set: true` (`hyprctl-verification-layer.md:128`). The docs say natural scrolling is "usually off by default" (configuration.html, "Scrolling"). The numeric match is a coincidence unless the compositor's value is read directly. The valid claim is the Hyprland effective value with its `set` flag, not "libinput default therefore host."

**F5 — MEDIUM — Source status blocks coverage credit.**
- `corpus/SOURCES.md:19` S007 (libinput helper tools) is `queued`. S006, S008, S009, S010 are also `queued` (`:18`, `:20`-`:22`).
- SCORECARD's coverage rubric (coverage / sourced current-art ground) counts an item only when an admitted `corpus/knowledge/` entry opens with `source:` citing a **`mined`** SOURCES row and names the item. A U6 entry that cites S007 while S007 is `queued` does not add coverage, and the reserved S051/S052 (from the round-15 spec) do not exist in SOURCES yet.

**F6 — LOW — Stale tool-presence claim for the adjacent U4 tool.**
- `.ufo/evidence/round-12/l2-scout.md:10` and `:12` say `wayland-info` is absent. Static check now finds `/usr/bin/wayland-info` owned by `wayland-utils 1.3.0-1` (`pacman -Qo`). The U6 row's "`wayland-info` absent" and the U4 row's claim are stale. Re-measure before any round-15 sentence repeats either claim. I did not run it.

**F7 — LOW — `hyprctl devices` scope is narrower than a touchpad claim.**
- `hyprctl --help` (static): "devices → Lists all connected keyboards and mice." The round-12 gate and config-health tables read `keyboards`, `touch`, `mice` keys (`config-health-report-r3.md:731`-`:732`, `:932` F9: "keyboards 9 ... touch 0; mice 4").
- Nothing in the lane's artifacts shows which libinput settings `devices` exposes per touchpad. Touchpad libinput settings from `devices` are `[UNK]`.
- The keymap claim is different: `hyprctl-verification-layer.md:159` shows `active_keymap: Portuguese (Brazil)` agreeing with `kb_layout = br`. That is a compositor-side keymap read. It is not a libinput setting. `[INF]` from the xkb role: keymap handling sits on the compositor side, not libinput.

**F8 — PROCESS DISCLOSURE — one live read.**
- I ran `hyprctl version` once (read-only; output: Hyprland 0.56.2, commit `efb5099…`). Brief said no live probes. I did not use it beyond version identity, and I did not run `hyprctl devices`, `getoption`, `libinput`, `wayland-info`, or any input tool.

## Acceptance conditions (U6 layer rung may pass only if all hold)

- **A1** Every libinput statement is labelled "built-in defaults / docs-era (1.32.0)" and quotes or anchors to `tools.html` (list-devices or debug-gui note) or `configuration.html`. It never says "host" or "effective."
- **A2** Every statement about host effective input settings cites `hyprctl getoption input:<key>` **with its `set` flag** (or config file bytes with the declaring line). Examples: `hyprctl-verification-layer.md:126`-`:130`, `SKILL.md:123`.
- **A3** Keymap statements cite `hyprctl devices` `active_keymap` as compositor-visible, not libinput (`hyprctl-verification-layer.md:159`).
- **A4** Hyprland per-device syntax claims are either (a) sourced to a hyprlang-era page (the 0.54 wiki the Devices page points to) with host `configProvider: hyprlang` stated, or (b) `[UNK]`. The Lua `hl.device` example is never presented as host syntax.
- **A5** Any `accel_profile`, `natural_scroll` or similar "agrees with default" line is `[INF]` and names the per-device and compositor-default gap (F4).
- **A6** Any knowledge entry cites only `mined` SOURCES rows (F5). S007 becomes citable only after its row is mined.
- **A7** The U6 layer rung explicitly states "no event observation; no `debug-events`, `record`, `replay`, `measure`, or `analyze` run" and names unexercised delivery/IME/kernel limits as `[UNK]`.

## Rejection conditions (any one fails the rung)

- **R1** Any sentence that infers host or compositor settings from `libinput list-devices`, `debug-gui`, or the docs' sample output (repeats M04 / F1).
- **R2** Any row that calls a libinput default the "Hyprland active" or "applied" value, or the reverse.
- **R3** Any use of `hyprctl devices` as proof of touchpad or libinput per-device settings (F7).
- **R4** Any Lua `hl.device` syntax presented as the host config (F2), or any hyprlang claim sourced only to Lua-era pages.
- **R5** Any claim that a device list or `wl_seat` capability proves focused-application input delivery (delivery is out of scope here; see AttackDelivery seat).
- **R6** Any stale "`wayland-info` absent" or "`libinput` absent" statement without a fresh static re-check (F3, F6).
- **R7** Any instruction, script, or row that runs `sudo libinput …`, `debug-events`, `record`, `replay`, `evtest`, or raw `/dev/input` reads, or cites record output as a host artifact.
- **R8** Any cited source at `queued` status, or a reserved S051/S052 ID cited before it lands as a mined row (F5).

## Exact evidence pointers

| Claim | Pointer |
|---|---|
| list-devices = built-in defaults, not desktop config | https://wayland.freedesktop.org/libinput/doc/latest/tools.html (section "libinput list-devices"; note block) |
| debug-gui same boundary | same URL, section "libinput debug-gui" |
| debug-events needs root / event access; record obscures keys | same URL, "libinput debug-events", "libinput record and libinput replay" |
| compositor is the only config path; separate contexts | https://wayland.freedesktop.org/libinput/doc/latest/faqs.html#can-i-write-a-program-to-make-libinput-do-foo |
| default accel profile "adaptive"; natural scroll "usually off" | https://wayland.freedesktop.org/libinput/doc/latest/configuration.html (sections "Pointer acceleration", "Scrolling") |
| Hyprland per-device Lua syntax, hyprlang deprecated since 0.55 | https://wiki.hypr.land/Configuring/Advanced-and-Cool/Devices/ ; https://wiki.hypr.land/Configuring/Basics/Variables/ |
| hyprctl calls synchronous | https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/ |
| host config provider hyprlang | `.ufo/evidence/round-12/configera-host.txt:87`, `:102`, `:103` |
| M04 inference trap | `corpus/lessons/round-12.md:37` |
| sibling boundary routes list-devices to "not Hyprland input.conf" | `.ufo/waves/round-13/w1/SiblingOverlap.md:68` |
| live read verb surface, agreement boundary | `SKILL.md:123`; whitelist `SKILL.md:221`; device count drift `SKILL.md:358` |
| kb_layout ↔ devices keymap agreement | `corpus/knowledge/hyprctl-verification-layer.md:159`; getoption `:296` in SKILL |
| accel_profile unset / live-default | `corpus/knowledge/hyprctl-verification-layer.md:127`; `corpus/knowledge/config-health-report-r3.md:541`, `:824` |
| natural_scroll int 0 set true | `corpus/knowledge/hyprctl-verification-layer.md:128` |
| devices keyboards/touch/mice keys | `corpus/knowledge/config-health-report-r3.md:731`-`:732`, `:932` |
| source queued status | `corpus/SOURCES.md:18`-`:22` (S006-S010), `:19` (S007) |
| coverage rubric requires `mined` | SCORECARD.md, "Six-axis baseline" table, row "coverage / sourced current-art ground" |
| U6 / U4 tool presence (stale) | `.ufo/evidence/round-12/l2-scout.md:10`, `:12` |

## Tool and version record

- Installs: none. `libinput-tools 1.32.0-1` (extra) is available but not installed: its only use here would be running list-devices or debug-events, which is out of bounds.
- Versions observed (static `pacman -Q` / `-Qo` / `-Si`, plus one `hyprctl version`): hyprland `0.56.2-2`; libinput `1.31.3-1`; libinput-tools `1.32.0-1` (repo only); wayland-utils `1.3.0-1` (owns `/usr/bin/wayland-info`).
- Live probes: one `hyprctl version` (F8). No other compositor or device call.

## Verification gaps

- Not measured: `hyprctl devices` full field set for touchpads (F7); per-device overrides in the host config (F2, F4); host loaded config file and its era beyond `configProvider: hyprlang` (`configera-host.txt:103`).
- Not measured: whether `wayland-info` output matches the round-12 "absent" record (F6). Only presence was checked.
- Hyprland docs-era: only the Latest-git wiki pages were read. The hyprlang-era page for 0.54 that the Devices page points to was not opened.
- Doc-vs-host libinput mismatch (1.32.0 vs 1.31.3-1) is not resolved; the sample output is not host evidence.
- No round-15 U6 draft exists on disk at review time, so acceptance A1-A7 are conditions for the landings, not verdicts on them.
