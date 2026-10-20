# InputSafety — U6 safe-command allowlist audit (sentinel, round 15 w1)

Axis: **coverage** (the U6 safe-boundary facet). No verdict on C1.
Labels: `[OBS-static]` = bytes read without running the subject tool. `[INF-docs]` = upstream or man-page text. `[INF]` = derived. `[UNK]` = not exercised.

**Executed, read-only:**
- `pacman -Q`, `-Qi`, `-Qlq`, `-Qo` (package database only).
- File reads of `SKILL.md`, `PROVINCE.md`, `corpus/`, `.ufo/waves/round-13/w1/globals.json`, `.ufo/waves/round-15/input-draft.txt` and sibling reports.
- The installed `libinput-*.1.gz` man pages, `/etc/group`, `/usr/lib/udev/rules.d/*`, `/var/log/pacman.log` (transaction lines only) and `~/.local/share/omarchy/**`.
- One HTTPS fetch of https://wayland.freedesktop.org/libinput/doc/latest/tools.html (banner "libinput 1.32.0").

**Not run:** any `libinput` subcommand, `hyprctl`, `stat`/`getfacl` on device nodes, `/dev/input` or `/dev/uinput` access, sudo, D-Bus, Wayland clients, tests, gates or builds.

**Tooling:** nothing installed or upgraded. RULES.md read first.

## Verdict

The durable fence (`SKILL.md:218-242`) does **not** ban the U6 routes. It has a hyprctl-only verb whitelist (`:220-224`). It also permits generic `wc`/`stat`/`sha256sum`/`grep` "on files" (`:200`) and unrestricted `busctl --user` (`:125`, `:140-141`).

The ban on debug-events, record, replay, evtest and injection exists only in this round's contract (`spec.json:3`). After round 15 the host keeps the capability and loses the fence, because `libinput-tools` is now installed and the user can read input devices. Severity: **HIGH**. The smallest remediation is one appended fence rule (proposed text in the last section). L1 owns `SKILL.md`; this seat did not edit it.

## Findings

**F1 — HIGH. The skill has no input-tool clause.**
- Evidence:
  - `SKILL.md:220-224` whitelists hyprctl verbs only.
  - `:225-230` bans "keystroke injection" and "dispatcher invocation" but names no tools.
  - `:200` allows `sha256sum`/`grep`/`stat` "on files" without saying *regular* files.
  - `:234-236` covers titles, `hyprland.log`, environ and the instance signature, but not keycodes, event logs or authentication input.
  - The gate (`tools/mado-verify.sh`) contains no libinput, `/dev/input` or uinput reference.
- Exploit path: a later-round seat that follows SKILL alone runs `libinput debug-events --show-keycodes`, or `sha256sum /dev/input/event*`, which blocks on and consumes the live event stream. No written rule forbids either.
- Impact: keystroke capture with no rule broken.

**F2 — HIGH. Root is not the barrier on this host.**
- Evidence:
  - `[OBS-static]` `/etc/group:23` `input:x:992:vgpnk` and `:17` `wheel:x:998:vgpnk`.
  - `/usr/lib/udev/rules.d/50-udev-default.rules:51` `SUBSYSTEM=="input", GROUP="input"` (systemd 261.2-1).
  - `[INF]` The event nodes are group-`input` readable. Node modes were not measured.
  - `[INF-docs]` The upstream text says tools "must be run as root" (tools.html §Helper tools) and "usually needs to be run as root" (libinput-debug-events(1)).
  - RULES.md grants passwordless sudo, though only for installs.
- Exploit path: the unprivileged agent user runs `libinput record --show-keycodes -o x.yml /dev/input/eventN`. No sudo prompt or root step is needed.
- Draft defect: `input-draft.txt:18,42` presents "requires root" as the access barrier. On this host that framing understates reach.
- Remediation: ban by **command class, regardless of privilege**, and state that group membership makes root irrelevant.

**F3 — HIGH. Injection paths that need no root.**
- Evidence:
  - `/usr/lib/udev/rules.d/60-steam-input.rules:5` gives `/dev/uinput` `TAG+="uaccess"` (package `steam-devices 1.0.0.87-3`). `[INF]` The active-seat user gets a uinput ACL; not measured.
  - `python-libevdev 0.13.1-1` arrived at 04:25:17 as a dependency (`pacman.log:2433`). It is a uinput-capable library.
  - `libinput-replay(1)`: replays "through the kernel"; tools.html: "creates a new virtual device".
  - Wayland injection globals are advertised (`round-13/w1/globals.json:147,151,143`): `zwp_virtual_keyboard_manager_v1`, `zwlr_virtual_pointer_manager_v1`, `zwp_input_method_manager_v2`. These need no device access at all.
  - Omarchy binds use `sendshortcut` (`default/hypr/bindings/clipboard.conf:2-4`; `config/elephant/symbols.toml:1`).
  - `omarchy-voxtype-install:11` installs `wtype`. The voxtype default `mode = "type"` "requires ydotool" (`default/voxtype/config.toml:62-64`).
- Exploit path: replay a recording, or drive a virtual keyboard, containing a SUPER chord. A compositor bind fires, e.g. an `omarchy toggle` that writes the toggles dir (`SKILL.md:214`). That is dispatcher mutation by proxy and bypasses rule 2.
- Remediation: name injection by mechanism (uinput, virtual-keyboard/pointer, input-method, `sendshortcut`/`pass`, portals) as well as by tool.

**F4 — HIGH. Device grab can lock out input.**
- Evidence: `--grab` on `debug-events`, `debug-gui` and `record` "will prevent events from being delivered to the host system" (each man page). `debug-gui` "exclusively grabs pointing devices" by default (libinput-debug-gui(1), DESCRIPTION).
- Impact: the compositor loses keyboard or pointer until the process dies, and recovery belongs to the operator. Neither the draft nor the skill names this.

**F5 — HIGH. Authentication material travels the same path.**
- Evidence:
  - `[OBS-static]` autostart runs `polkit-gnome-authentication-agent-1` (`default/hypr/autostart.conf:6`) and `fcitx5` (`:4`).
  - Hyprlock is in province (`PROVINCE.md:9`).
  - Obfuscation is partial and can be overridden:
    - debug-events: "partially obfuscated … Use the --show-keycodes argument to make all keycodes visible" (libinput-debug-events(1)).
    - record: "common keys are obfuscated" (libinput-record(1) `--show-keycodes`).
    - `--with-hidraw`: "HID reports are **not obfuscated** … recover the key strokes". "Do not type passwords while recording HID reports" (libinput-record(1), RECORDING HID REPORTS).
- Exploit path: any capture window that overlaps a lock, polkit, sudo or pinentry prompt records timing and keystrokes of a password. An `input_method_v2` or fcitx5 observer sees committed text.
- Remediation: treat keycodes, key timing, IME text, clipboard contents and prompt input as authentication material. They are never read, not even shape-only.

**F6 — MEDIUM. Event logs and side channels missing from session-material rule 4.**
- Event logs on disk: `record --autorestart` writes rotating files (libinput-record(1)), and `libinput analyze` reads recordings ("analyze a recording", libinput-analyze(1)).
- Protocol and bus dumps: `WAYLAND_DEBUG` dumpers (S006 §Protocol dumpers) print `wl_keyboard.key`. `busctl monitor`/`capture` and `dbus-monitor` see IME and portal traffic. `SKILL.md:125,140-141` allows `busctl --user` with no verb limit.
- Kernel channels: `journalctl -k`/`dmesg`, debugfs HID event files, `usbmon`, `udevadm monitor`.
- Remediation: restrict `busctl` to `status`, `get-property` and `introspect`. Ban `call`, `set-property`, `monitor`, `capture` and `emit`.

**F7 — MEDIUM. Mid-round reach change has no recorded installer.**
- Evidence:
  - `pacman.log:2429-2436`: `pacman -S --needed --noconfirm libinput libinput-tools` at 2026-10-20T04:25:16-0300 upgraded libinput 1.31.3-1 → 1.32.0-1 and installed libinput-tools, python-libevdev, python-pyudev and python-yaml.
  - No mado file attributes it (grep over `.ufo` and `LOG.md`).
  - ReviewDocsEra F1 independently flags it as a partial upgrade.
  - The same install also changed the live device layer. `pacman.log:2438` runs `35-systemd-udev-reload.hook` (Target `usr/lib/udev/rules.d/*`). `/usr/share/libalpm/scripts/systemd-hook:64-69` runs `udevadm control --reload`, then `udevadm trigger -c change` and `udevadm settle`, unless `/etc/systemd/do-not-udevadm-trigger-on-update` exists. That file is absent. `[INF]` A change uevent was replayed for every device, input devices included, during a no-input-action round. Its effect on the compositor is `[UNK]`. MadoR15.AttackNoHarm reported this first; I re-derived it from static bytes.
- Draft defect: `input-draft.txt:59-60,74` says the host "has libinput 1.31.3-1", which has been stale since 04:25:17.
- Remediation:
  - L1 records the install with installer `[UNK]` and stops citing 1.31.3.
  - Note that presence of `/usr/bin/libinput` is a capability and not authorization.
  - State that RULES.md install authority does not grant execution.
  - Route through the operator any install that ships `usr/lib/udev/rules.d/*` (libinput, ydotool, steam-devices and similar), because it re-triggers every device.

**F8 — LOW. Whitelisted reads leak identity or argv.**
- `hyprctl devices` (`SKILL.md:221`) emits device names and hardware identity. `pgrep -a` (`:201`) prints argv.
- Keep both counts and shape only in U6 artifacts.
- Name `switchxkblayout`, `dispatch sendshortcut` and `dispatch pass` in the Never list. The closed whitelist already excludes them, but U6 readers need them named.

**F9 — LOW. Screenshots can show credentials.** `grim` (`:206`) can capture on-screen credentials or clipboard previews. Recommend keeping screenshots in memory and never during a prompt. This is not U6-specific.

Out of my surface: `resume_continuity_v1`. No such logic exists in this audit target, so it was not applicable.

## Proposed allowlist (for L1 to append; smallest fix)

**Rule 7 — Input-layer fence (U6).** Input evidence is static only.

**Allowed:**
- Upstream docs over HTTPS.
- Reading installed man pages, XML and quirks **files** as files.
- `pacman -Q/-Qi/-Ql/-Qo`.
- `<tool> --version`.
- Already-whitelisted `hyprctl getoption input:*` and `hyprctl -j devices` as counts only, when the round permits hyprctl. Round 15 forbids every hyprctl call.

**Never, with or without sudo, whatever the group membership:**
- **libinput:** every subcommand that opens a device node or recording: `list-devices`, `list-kernel-devices` (`--hid`), `debug-events`, `debug-gui`, `debug-tablet*`, `record` (including `--no-events`, `--autorestart`, `--with-hidraw`, `--show-keycodes`), `replay`, `measure *`, `analyze *`, `quirks list`, `test`. Also any `--grab`.
- **Other device tools:** `evtest`, `evemu-*`, `wev`, `xev`, `showkey`, `keyd monitor`, `wshowkeys`.
- **Injection tools:** `wtype`, `ydotool`, `dotool`.
- **Raw device access:** any read or write of `/dev/input/*`, `/dev/uinput`, `/dev/hidraw*`, `/sys/kernel/debug/hid/*`. Generic file tools only on **regular** files.
- **Wayland clients:** any client that binds virtual-keyboard, virtual-pointer, input-method, text-input, `hyprland_input_capture` or global-shortcuts. Also `WAYLAND_DEBUG` and protocol dumpers.
- **Portals and D-Bus:** RemoteDesktop/InputCapture portal sessions, `busctl call|set-property|monitor|capture`, `dbus-monitor`.
- **Compositor actions:** `hyprctl dispatch sendshortcut|pass`, `switchxkblayout`.
- **Kernel and udev:** `udevadm info|monitor`, `dmesg`, `journalctl -k`.
- **Existing artifacts:** reading any existing recording or event log.

Keycodes, key timing, IME or committed text, clipboard contents, and lock, polkit or sudo prompt input are authentication material and are never read. Device names, node paths, udev properties and DMI values are shape-only. Presence of an installed tool, and RULES.md install authority, grant no execution right.

**Acceptance checks for L1 (not run by this seat):**
- `grep -n 'Input-layer fence' SKILL.md` returns one hit.
- The U6 note's `## Safe boundary` names F2 (group access), F3 (no-root injection), F4 (grab) and F5 (authentication material).
- The note no longer says "libinput 1.31.3-1".
