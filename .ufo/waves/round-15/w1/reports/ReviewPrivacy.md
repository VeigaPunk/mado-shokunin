# ReviewPrivacy — U6 diagnostic event capture privacy and device access (round 15, w1)

Scope: adversarial review of the proposed U6 input-debugging route as a documentation-only note.
Not in scope: any capture, replay, device read, grab, injection, kernel diagnosis, gate/config/registry edits.
No commits, tests, builds, linters, formatters, smoke runs or live probes were run. No credential/auth file, `~/.omp/agent/agent.db*`, or `omp` CLI was touched.

## Verdict

**Conditional ACCEPT for a documentation-only U6 note; REJECT any capture-adjacent step.**

The libinput tooling documents a path to keystroke-bearing event logs, device identity, and device grab or injection. Its privacy protection is partial and layer-dependent, not a guarantee. A U6 note is acceptable only if it cites upstream statements as `[INF-docs]`, pins the revision, and performs no device access. Everything below is conditional on that.

## Findings, by severity

### F1 (high): the libinput obfuscation is partial and differs between layers
- Evdev layer (`obfuscate_keycode`, `print_evdev_event`): `EV_KEY` codes 2–57 and 71–83 are rewritten to `KEY_A`. Codes 1 (ESC), 15 (TAB), 28 (ENTER), and 29 (LEFTCTRL) pass unchanged. `MSC_SCAN` is forced to 30. Codes 58 (CAPSLOCK), 59–68 (F1–F10), 87–88 (F11–F12), and 125 (LEFTMETA) are not obfuscated at this layer.
- libinput layer (`print_keyboard_event`, record.c:460–463): codes 1–84 are printed as `key: -1`, which hides them entirely. Codes 85 and above (F11, F12, arrows, Meta) are printed as-is. The two layers therefore use different ranges. The upstream claim "any alphanumeric key shows up as letter a" is accurate only for the evdev layer.
- Timing is not obfuscated. The EV_SYN line prints `%+dms` deltas, so inter-key timing survives every obfuscation setting.
- Overrides: `--show-keycodes` disables all keycode obfuscation (record.c:242, 463).
- HID path: `--with-hidraw` output is explicitly not obfuscated.
- Upstream statements (quote, ≤25 words):
  - tools.html: "For data protection, libinput record obscures key codes by default, any alphanumeric key shows up as letter “a”."
  - record.man:64–66: "Show keycodes as-is in the recording. By default, common keys are obfuscated..."
  - record.man:134–136: "HID reports are not obfuscated and a sufficiently motivated person could recover the key strokes from the logs."
  - debug-events.man:42–44: "Key events shown by this tool are partially obfuscated to avoid passwords and other sensitive information showing up in the output."
- Acceptance: the note may say "partially obfuscated by layer, with stated exclusions and retained timing." Rejection: any wording that says keys are hidden, or that a recording is "safe" to share.

### F2 (high): device identity is emitted whether or not keys are obfuscated
- `print_device_description` (record.c:1889–1898, called at record.c:2309) writes the device node, evdev name and bus/vendor/product/version (`print_description`, record.c:1498–1530), an HID report section, udev properties filtered to `ID_INPUT*`, `HID_BPF*`, `LIBINPUT*`, `EVDEV_ABS*` (record.c:1758–1759), and driver/virtual flags.
- The call-site gating for the HID section was not fully traced in this pass ([UNK]).
- Acceptance: no device name, vendor/product ID, node path, udev property, or HID ID appears in any lane artifact. Rejection: any such value copied from upstream examples or from a host run.

### F3 (high): device access requires root; this route must not reach `/dev/input`
- tools.html: "Most of the tools must be run as root to have access to the kernel’s `/dev/input/event*` device files."
- record.man:10 and replay.man:9: the tools "need to run as root" to read from the device.
- Every upstream example uses `sudo`.
- Host state: `which libinput` returned nothing, so libinput is not installed. Under the tooling directive it could be installed, but installing it is not needed for a documentation route and would enable live capture. Recommendation: do not install it this round.
- No `/dev/input` listing was performed by this seat.
- Acceptance: the note records device access as "not exercised, root-only per upstream." Rejection: any step that runs `sudo`, opens `/dev/input/event*` or `/dev/hidraw*`, or lists those nodes.

### F4 (high): grab and virtual-device creation are control hazards
- `libinput record --grab` exclusively grabs devices so events are not delivered to the host (record.man:64–66; record.c:2433–2434).
- `libinput replay` creates a uinput virtual device from the recording (`libinput-replay.py:148`, `d.create_uinput_device()`; tools.html "replay" section).
- Both are injection or interference routes. Neither is a read-only probe, contrary to any assumption that replay is harmless.
- Acceptance: the note bans `--grab`, `replay`, and uinput creation. Rejection: any sentence calling replay or record "read-only" or "harmless".

### F5 (medium): upstream bug-report guidance asks for recordings and hardware identity
- reporting-bugs.html asks the reporter to attach a recording, `udevadm info` output, vendor model, `/sys/class/dmi/id/modalias`, and `libinput debug-events --verbose` output.
- A lane note must not transpose this into a recommendation to collect those artifacts. The lane's province is read-only and shape-only for session material (SKILL.md:218–246; AGENTS.md).
- Rejection: any recommendation to attach or retain recordings, udev output, DMI identifiers, or verbose debug-events output.

### F6 (medium): upstream example outputs must not become host facts
- tools.html contains example device lists, `list-kernel-devices --hid` output with names and IDs, and sample `POINTER_MOTION` traces.
- Acceptance: examples are cited only as "the documentation shows the format," with no values copied into the lane. Rejection: any example value presented as a host observation.

### F7 (medium): source anchoring and mutability
- S007 (SOURCES.md:19) points to `doc/latest/tools.html`, which is mutable and carries no revision. SOURCES rules require a revision anchor.
- The `libinput-record.html` URL returns HTTP 404 (`read` attempt, 2026-10-20). Do not cite it.
- Pinned upstream authority used here: libinput tag 1.32.0, tools/ at the tag (see Evidence). Any admitted row must use these pins, or a superseding row with a pinned revision.
- Acceptance: the note cites the 1.32.0 tag pins and records that the `latest` page was read on 2026-10-20. Rejection: a bare `latest` citation as sole support.

## Acceptance conditions (all required)
1. Documentation-only: no libinput binary run, no `/dev/input`, `/dev/hidraw`, or `/dev/uinput` access, no `sudo`, no event log written anywhere, including /tmp.
2. Layer-specific obfuscation stated with the exclusions in F1, timing retention, `--show-keycodes`, and HID non-obfuscation, each tagged `[INF-docs]` with a pin.
3. Device identity and grab/replay explicitly marked not authorized and not exercised.
4. Delivery, IME, and kernel behaviour stay `[UNK]`.
5. No upstream example values copied as host data.
6. Gate, config, registry, and SKILL unchanged by this route (the wayland-protocol note already fences kernel/libinput diagnosis at wayland-protocol-boundaries-r13.md:8 and :104).

## Rejection conditions (any one rejects)
- R1: any claim that libinput record or debug-events output is privacy-safe, or that keys are "hidden" without the layer qualification in F1.
- R2: any event dump, timing trace, keycode list, device name/ID, udev property, node path, or DMI value in a note, SOURCES cell, LOG, or report.
- R3: any instruction or step using `sudo`, `libinput record|replay|debug-events|debug-gui|measure|analyze|list-devices|list-kernel-devices`, `--grab`, `--show-keycodes`, `--with-hidraw`, `--autorestart`, or uinput.
- R4: any recommendation to attach recordings or hardware identifiers, or to run the reporting-bugs.html steps.
- R5: a `latest` or 404 URL cited as sole support, or an unpinned S007 cell.
- R6: presenting `[INF-docs]` statements as host-observed behavior.

## Unknowns (kept, not closed)
- Exact obfuscation range in `libinput debug-events` (the printing code path was not in the fetched files) [UNK].
- Whether the HID section of the device description is gated by `--with-hidraw` (call-site not traced) [UNK].
- Whether any libinput subcommand works without root on this host [UNK]; nothing was run.

## Evidence (all read-only)
- Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:19` (S007 row, queued, `latest` anchor); `corpus/knowledge/wayland-protocol-boundaries-r13.md:8,104`; `SKILL.md:218–246` (safety rules 1–6); `AGENTS.md`; `PROVINCE.md`; `SCORECARD.md:334–336, 483–485, 591–593` (U6 bounded: no raw input capture, injection, or kernel diagnosis); `.ufo/waves/round-15/w1/spec.json:149` (this seat's prompt).
- Upstream, libinput 1.32.0, fetched 2026-10-20 to `/tmp/mado-r15-privacy` (scratch, removed after this report):
  - `https://wayland.freedesktop.org/libinput/doc/latest/tools.html` (run-as-root, obfuscation, record, replay sections)
  - `https://wayland.freedesktop.org/libinput/doc/latest/reporting-bugs.html`
  - `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/tools/libinput-record.c` sha256 `06721130765f489be1e75e20b96e6bf21b01380f43ce1fc87dc9c5d4fa403e46` (obfuscate_keycode 159–185; print_evdev_event 236–243; print_keyboard_event 460–463; print_device_description 1889–1898; print_description 1498–1530; udev filter 1758–1759; grab 2433–2434)
  - `.../tools/libinput-record.man` sha256 `89a08189f82308253f71f97c188fb3e85151044089dd5e2c56d6d2bbbf7a6445` (lines 10, 64–66, 79, 130–136)
  - `.../tools/libinput-debug-events.man` sha256 `92c23aa4b286833cc3a89644327a7c7a2a24dbdcc5c1904c16b646f0167655f8` (lines 42–46)
  - `.../tools/libinput-debug-events.c` sha256 `c69f55673afcd5b326f600a6827c17fbb06ff2a06d0748f31bf99d268c5b216a`
  - `.../tools/libinput-replay.py` sha256 `c8cd3fa9a6ddb697a8ae007bfd6f8fa4d86fce08f67269d6e4a86a3bf55a3f93` (line 148)
  - `.../tools/libinput-replay.man` (line 9); `.../tools/libinput-list-kernel-devices.man` (line 17)
  - `https://raw.githubusercontent.com/torvalds/linux/v6.12/include/uapi/linux/input-event-codes.h` sha256 `f9889a73d7d4f7e303d2d346a3622657169c5e8d7d354cb7a030ff47a7fdfdee` (KEY_ESC 1, TAB 15, ENTER 28, LEFTCTRL 29, CAPSLOCK 58, KP7 71, KPDOT 83, ZENKAKUHANKAKU 85, F11 87, F12 88, LEFTMETA 125)
  - Attempt: `https://wayland.freedesktop.org/libinput/doc/latest/libinput-record.html` returned HTTP 404; not cited.

## Tools
- No installs or upgrades. `libinput` is absent on this host (`which libinput` empty); `/usr/bin/wayland-info` exists but was not run.
- `curl` and `bash` used for read-only fetches of upstream static sources. Scratch copies were removed after this report was written.

## Checks for the main agent
- Confirm the U6 note's sentences against F1–F7 and R1–R6, without running any libinput command.
- Confirm S007 is either pinned by a superseding row or left queued (not cited as sole support).
