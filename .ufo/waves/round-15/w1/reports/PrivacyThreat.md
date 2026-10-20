# PrivacyThreat — U6 input-debug output retention (passwords / keymaps / device identifiers)

Seat `MadoR15.PrivacyThreat` (sentinel, leaf). Scope: the proposed static-docs U6 route as landed in
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/input-draft.txt` (96 lines, read
2026-10-20 ~04:30 -03), plus the documented commands it names. This is an advisory, not admission. No event read, capture,
replay, injection, libinput subcommand, `hyprctl` call or compositor action was run.
Tags: `[OBS]` read here · `[INF-docs]` upstream text · `[INF]` inference · `[UNK]` not established.

## Verdict

The draft itself retains **no keystroke, keymap content or new device identity**. Its `## Safe boundary`
(`input-draft.txt:82-86`) already classes record/replay as capture-class. On those grounds I would accept it on
privacy, with one condition: three sentences currently imply safety controls that do not hold on this host
(F1, F2, F4). Each needs a one-clause qualifier. The other findings (F3, F5–F7) constrain any future rung and
the round record. None needs a broad security change.

## Findings

**F1 — HIGH — The doc's "root" barrier is not this host's barrier.**
- Exploit path. Any seat running as `vgpnk` follows the route's own documented commands, for example
  `libinput debug-events --show-keycodes` or `libinput record --with-hidraw`. It needs no sudo. It reads
  every keyboard at the kernel layer, regardless of Wayland focus, including the hyprlock and sudo/pinentry
  prompts. The output then lands in tool stdout.
- Evidence `[OBS]`, all static metadata:
  - `id -nG` → `vgpnk docker input wheel`.
  - `stat -c '%U:%G %a' /dev/input/event* | sort | uniq -c` → `26 root:input 660` (aggregate count only; no
    names were read).
  - `/usr/lib/udev/rules.d/50-udev-default.rules:51` → `SUBSYSTEM=="input", GROUP="input"`.
  - The capture tools were installed **inside this round**. `/var/log/pacman.log` shows
    2026-10-20T04:25:16-0300, `pacman -S --needed --noconfirm libinput libinput-tools`: libinput
    1.31.3-1→1.32.0-1, plus `libinput-tools 1.32.0-1`, `python-libevdev 0.13.1-1`, `python-pyudev`
    and `python-yaml`. `pacman -Qo /usr/bin/libinput` → `libinput-tools 1.32.0-1`. ReviewDocsEra F1 also
    reports this install; it does not identify the installing seat.
  - Passwordless `sudo` is available to every seat anyway (`~/.omp/agent/RULES.md:4-5`).
- Impact. `input-draft.txt:18,42` cite "Most of the tools must be run as root". Read as a privacy control,
  that sentence is false here `[INF]` (from group and mode; not exercised). Peer reports that say
  "no libinput binary" (ReviewLibinput F3, ReviewQuotes:20,111, DocsVersion:4) were true before 04:25:17
  and are false now. Nobody should rely on tool absence as a control.
- Smallest remediation (draft owner/L1). In the Safe boundary, label the root sentence as upstream prose,
  not a host control. Make the round's prohibition the only boundary. `input-draft.txt:60,74` still says
  `1.31.3-1`; correct it to "1.31.3-1 until 04:25:17, 1.32.0-1 after". Record the install in the round
  report: tool, version, channel, reason, seat.

**F2 — HIGH — Default keycode obfuscation is partial; it is not a retention license.**
- `[INF-docs]` debug-events man page, 1.32.0 (`tools/libinput-debug-events.man`, OPTIONS `--show-keycodes`):
  "Key events shown by this tool are partially obfuscated to avoid passwords…"
- `[INF-docs]` debug-events source (`src/util-libinput.c:324` @1.32.0). It masks only
  `KEY_ESC ≤ key < KEY_ZENKAKUHANKAKU` as `***`. Press/release state and millisecond timestamps are still
  printed.
- `[INF-docs]` record source (`tools/libinput-record.c`, `obfuscate_keycode()` @1.32.0). It rewrites only
  codes strictly between ESC and CAPSLOCK, plus keypad 7…dot, to `KEY_A`. ESC, TAB, ENTER and LEFTCTRL stay
  in the clear, and µs timing is kept.
- So a default recording still leaks password length, keystroke timing (typing biometrics) and the Enter
  that ends the password.
- `--show-keycodes` removes all masking. `--with-hidraw` reports are "**not obfuscated**… Do not type
  passwords while recording HID reports" (`libinput-record.man:140-142`; option text `:87`
  "DO NOT TYPE SENSITIVE DATA").
- Impact. `input-draft.txt:20,46` quote "record obscures key codes by default" with no qualifier. A reader
  can take that as "safe to keep".
- Smallest remediation. Add one clause: "obfuscation is partial (length/timing/Enter remain) and is
  disabled by `--show-keycodes`/`--with-hidraw`; no event output is retained in any form."

**F3 — HIGH (forward) — The keymap is the decoder, and the corpus already holds it.**
- `[INF-docs]` `wayland.xml` (sha256 `cc860987…5f07`):
  - `wl_keyboard.key` carries a raw `key` uint plus a millisecond `time` (`:2669-2698`).
  - Meaning comes from the keymap fd (`:2600-2611`) with keycode+8 (`:2597`).
- `[OBS]` committed corpus already has the layout and options:
  - `active_keymap: Portuguese (Brazil)`, layout `br` (`corpus/knowledge/config-health-report-r3.md:157-158,412-413`;
    `hyprctl-verification-layer.md:159`);
  - `kb_options=compose:caps` (ReviewKeyboard L1).
- Exploit. Any *retained* keycode sequence decodes to plaintext using public lane data: an unmasked
  `debug-events` line, a `--show-keycodes`/hidraw recording, or client protocol logging (F4). A "sanitized
  keycodes" excerpt is still a password.
- Draft status: compliant. `:85-86` retains no keycode, and keymap/layout stay in `[UNK]` (`:93`).
- Constraint for the record. Keymap and layout facts may stay at configuration level. No artifact may ever
  co-locate them with event codes or timings.

**F4 — MEDIUM — The unnamed "delivery" rung is also a keystroke and plaintext logger.**
- `[INF-docs]` libwayland 1.26.0 `src/connection.c:1609-1661` (`wl_closure_print`, used by `WAYLAND_DEBUG`):
  - uint args are printed verbatim (`%u`), so every `wl_keyboard.key` code is logged;
  - strings are printed verbatim (`"%s"`), so `zwp_text_input_v3.commit_string`/`preedit_string`
    (`/usr/share/wayland-protocols/unstable/text-input/text-input-unstable-v3.xml:364,390`) are logged, which
    is IME-committed text in clear (fcitx5 installed per ReviewKeyboard F3), along with window titles;
  - arrays print only `array[N]` and fds only `fd N`, so the keymap *content* is not dumped.
- Exploit. The lane's prior escalation order (`round-13/w1/GlobalDocs.md:302-304`, "L1 list →
  `WAYLAND_DEBUG=client` traffic") is the natural next step for `## Unexercised delivery`. Run on a terminal
  or browser while the operator types, it logs the password.
- Smallest remediation. Optionally add one sentence to `## Unexercised delivery`: client protocol logging
  (`WAYLAND_DEBUG`) prints key codes and text-input strings verbatim. It is capture-class, not a read-only
  check.

**F5 — MEDIUM — Documented "metadata-only" steps still emit host and device identity.**
- `[INF-docs]` `record --no-events` (tools.html §record, "only the device description is needed") still
  writes:
  - `system.dmi` = DMI modalias, which includes BIOS vendor/version/date and system vendor/product
    (`libinput-record.man:161,270-271`);
  - `os` and `kernel`;
  - `evdev id [bus, vendor, product, version]`;
  - a subset of udev properties, "may include properties set on a parent device" (`:315-318`).
- `[INF-docs]` `list-kernel-devices --hid` prints USB `vendor:product` ids plus hidraw/evdev nodes, and
  `list-devices` prints node, group and seat (tools.html).
- `[OBS]` strings from `/usr/bin/Hyprland` 0.56.2 for the draft's named `hyprctl devices` route
  (`input-draft.txt:30-34`) give these fields:
  - keyboards: `address "0x{:x}"` (heap pointer), `name`, xkb `rules/model/layout/variant/options`,
    `active_keymap`, live `capsLock`/`numLock`, `main`;
  - mice: `name`, `defaultSpeed`, `scrollFactor`.
  "Read-only" does not mean identity-free (same lesson as R14 `SourceSafety.md:112-113`).
- Constraint. No future capture of these fields without in-pipe projection to counts. Never list
  `record --no-events` as a safe metadata step. The draft retains none of them (`:85-86`), and it marks
  `hyprctl devices` as unexecuted (`:33`).

**F6 — MEDIUM — Retention sinks sit outside the report.**
- `[OBS]` Tool stdout is persisted verbatim in harness transcripts. Example:
  `.ufo/interactive-sessions/20261015T050057Z/*.jsonl` holds 95 `toolResult` records. That directory is
  only gitignored, so it stays on disk.
- `[OBS]` Lane `.gitignore` = `.ufo/interactive-sessions/` only. `git check-ignore` on a lane-root
  `recording.yml` and on a wave report gives rc=1, so neither is ignored. The repo is colocated `.git` + `.jj`,
  so the next snapshot/commit makes a stray capture durable.
- `[INF-docs]` `record --autorestart` keeps creating timestamped files (`libinput-record.man`, `--autorestart`).
- Impact. Redacting the report after a capture does not erase it. The only zero-retention state is zero
  capture, and that is the draft's stance.
- Any future authorized run: project in-pipe, never write raw output to tool stdout or the lane tree (R14
  `Safety.md:219-221` precedent).

**F7 — LOW — `--grab` turns a capture into lockout.** `[INF-docs]` debug-events and record `--grab`
"prevent events from being delivered to the host system" (`libinput-record.man:71-72`). A grabbing capture
also stops the operator typing to stop it. This is covered by the existing prohibition; noted for the
InputSafety allowlist.

## Accept / reject conditions (privacy only)

- **Accept** if the admitted note:
  - keeps `input-draft.txt:82-86` and `## Unexercised delivery` `[UNK]`;
  - adds the F1 qualifier (root is upstream prose, not a host control) and the F2 qualifier (partial
    obfuscation; no retention);
  - corrects the stale `1.31.3-1` host version;
  - retains no keycode, timing, DMI string, vendor:product id, node path, heap address or new device name.
- **Reject** if any U6 artifact (note, report, evidence, transcript-backed claim) contains output of a
  libinput subcommand other than `--version`/`--help`, `hyprctl devices`, `WAYLAND_DEBUG`, or
  evtest/evemu/wev. Also reject if it presents default obfuscation, root requirement or tool absence as the
  privacy control.

## Tooling record

- Installs or updates by this seat: **none**.
- Observed, not by this seat: `libinput 1.31.3-1→1.32.0-1`, `libinput-tools 1.32.0-1`,
  `python-libevdev 0.13.1-1`, `python-pyudev 0.24.4-1`, `python-yaml 6.0.3-2`, all via
  `pacman -S --needed --noconfirm`, 2026-10-20T04:25:17-0300. The installing seat is `[UNK]`. This is a
  targeted `-S` with no update-safety-gate record. Hyprland PID 1706 maps a deleted `libinput.so` per
  ReviewDocsEra.

## Reads (static only)

- Upstream pages at tag 1.32.0: tools.html; `tools/libinput-{debug-events,record}.man`;
  `tools/libinput-{debug-events,record}.c`; `src/util-libinput.c`.
- wayland 1.26.0 `src/connection.c`.
- Local XML: `/usr/share/wayland/wayland.xml:2573-2700`; text-input-v3 XML.
- Static metadata: `pacman -Q/-Qo/-Ss`, `/var/log/pacman.log`, `id`, `stat`, udev rule; `strings /usr/bin/Hyprland`.
- Lane files: `SKILL.md:29-37,234-236`, `corpus/QUALITY.md:19,50-53`, corpus device rows and the
  round-13/14/15 reports cited above.
- Not opened: `~/.omp/agent/agent.db*` and credential/auth files. The `omp` CLI was not run.
- Files written by this seat: this report only.
