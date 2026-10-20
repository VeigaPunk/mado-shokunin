# LibinputReplay — official libinput replay documentation and replay/injection vs read-only metadata distinction (round 15 w1)

Seat: `MadoR15.LibinputReplay` (scout, leaf)  
Date: 2026-10-20 (UTC)  
Milestone: U6 input evidence ladder and R14 ancillary provenance correction  
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`  
Output Report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/LibinputReplay.md`  
Scope: Open official libinput replay documentation and inspect tool implementation to distinguish replay/injection from read-only metadata. No replay or event generation executed.

Tags: `[OBS]` observed static fact · `[INF-docs]` upstream documented semantics · `[INF]` inference · `[UNK]` unexercised / unknown.

---

## 0. Actions and Tooling Record

- **Actions taken:**
  - Read-only static inspection of upstream documentation: `https://wayland.freedesktop.org/libinput/doc/latest/tools.html` (§libinput record and libinput replay, lines 205–285, §libinput record’s autorestart feature, §Recording multiple devices at once) and git tag `1.32.0` raw source `doc/user/tools.rst`.
  - Read-only static inspection of installed manual pages: `man 1 libinput-replay` (`/usr/share/man/man1/libinput-replay.1.gz`, 46 lines) and `man 1 libinput-record` (`/usr/share/man/man1/libinput-record.1.gz`, 229 lines).
  - Read-only static inspection of installed tool script source: `/usr/lib/libinput/libinput-replay` (Python 3 script, 411 lines).
  - Static package metadata and hash checks: `pacman -Q libinput libinput-tools`, `pacman -Qi libinput-tools`, `sha256sum /usr/lib/libinput/libinput-replay /usr/share/man/man1/libinput-replay.1.gz`.
- **Prohibitions observed:**
  - No `libinput replay`, `record`, `debug-events`, `debug-gui`, `measure`, or `analyze` command was executed.
  - No access to `/dev/input/event*` or `/dev/uinput`; no `sudo` or root commands run.
  - No input events recorded, read, replayed, or injected. No compositor state mutated.
  - No test, build, gate, regression, linter, or formatter executed.
  - No credentials, auth files, or `~/.omp/agent/agent.db*` accessed; `omp` CLI not launched.
  - No subagent delegation; leaf scout seat.
- **Tooling record:**
  - Tool installs or upgrades by this seat: **none**.
  - Host observation `[OBS]`: `extra/libinput 1.32.0-1` and `extra/libinput-tools 1.32.0-1` are installed on the host.

---

## 1. Pinned Source Documents and Identity

| Source Identifier | Scope & Path | Revision / Checksum | Nature & Authority |
|---|---|---|---|
| **Upstream Tools Doc (HTML)** | `https://wayland.freedesktop.org/libinput/doc/latest/tools.html` | Header "libinput 1.32.0 documentation" | Primary upstream web documentation (mutable URL path) |
| **Upstream Tools Doc (Source)** | `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst` | Git tag `1.32.0`, commit `c7e6fe66f509ba2eda680c28aa64795987b49e7c`; sha256 `53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f` | Primary upstream documentation source text |
| **Installed Man Page** | `/usr/share/man/man1/libinput-replay.1.gz` | sha256 `fc521d90594b3eee0c24b724f486394e22772ca32039323631adb7f77d0a5522` | Official command manual for `libinput replay` |
| **Installed Man Page** | `/usr/share/man/man1/libinput-record.1.gz` | sha256 `068bb947fc04da1b61cffc9fa1907cbffbc10dcf263092ea60c9ddba58b341f2` | Official command manual for `libinput record` |
| **Installed Replay Tool** | `/usr/lib/libinput/libinput-replay` | Python 3 script, sha256 `c8cd3fa9a6ddb697a8ae007bfd6f8fa4d86fce08f67269d6e4a86a3bf55a3f93` (411 lines) | Official Python implementation of `libinput replay` |

---

## 2. Primary Documentation Quotes (Quote Discipline)

Each quote is verbatim, whitespace-counted strictly $\le 25$ words, and anchored to an exact location and revision.

| ID | Location & Revision | Verbatim Quote (Word Count) | What It Supports | What It Does NOT Support |
|---|---|---|---|---|
| **Q-REP1** | `tools.rst:206–207` (tag 1.32.0) | "The recorded sequence can be replayed with the libinput replay command." (11) | Replay is the playback counterpart to record. | That replay is read-only, safe, or non-mutating. |
| **Q-REP2** | `tools.rst:274–275` (tag 1.32.0) | "libinput replay creates a new virtual device based on the description in the log file." (15) | Replay synthesizes a new virtual input device. | That virtual devices are isolated from the active compositor. |
| **Q-REP3** | `tools.rst:275–277` (tag 1.32.0) | "Hitting enter replays the event sequence once and the tool stops once all events have been replayed." (17) | Replay execution is triggered interactively or via flags. | Automatic restoration of pre-replay host session state. |
| **Q-REP4** | `libinput-replay.1:9–11` | "This tool needs to run as root to create a device and/or replay events." (14) | Replay requires elevated root privilege. | Unprivileged or read-only diagnostic safety. |
| **Q-REP5** | `libinput-replay.1:22–23` | "This tool replays events from a recording through the kernel and is independent of libinput." (15) | Replayed events pass directly into kernel evdev subsystem. | Compositor-level safety filtering or event containment. |
| **Q-REP6** | `tools.rst:282–284` (tag 1.32.0) | "Use libinput record --no-events to print the device description and exit immediately without waiting for any events:" (17) | Device description can be printed without capturing events. | Dynamic event sequencing, timing, or compositor state. |
| **Q-REP7** | `libinput-record.1:69–71` | "Only print the device description(s) and exit immediately without waiting for events." (12) | `--no-events` terminates immediately after descriptor output. | Live device state, keystrokes, or active input delivery. |
| **Q-REP8** | `/usr/lib/libinput/libinput-replay:292` | "Note that the device may not be in a neutral state now." (12) | Interrupted event replay can leave keys/buttons stuck. | Reliable state hygiene during or after replay runs. |

---

## 3. Structural Distinction: Replay/Injection versus Read-Only Metadata

Static analysis of the documentation and `/usr/lib/libinput/libinput-replay` establishes an absolute boundary between active input injection and read-only metadata:

```
[ Replay / Input Injection ]                [ Read-Only Metadata ]
-----------------------------------------   -----------------------------------------
Vector:   /dev/uinput                       Vector:   sysfs / udev / YAML header
Action:   Creates virtual kernel device     Action:   Parses static descriptors
          (libevdev.Device.create_uinput)             (capabilities, IDs, quirks)
Payload:  Injects live EV_KEY, EV_REL,      Payload:  EMPTY events array (events: [])
          EV_ABS, EV_SYN packets                      No timing, no keystrokes
Scope:    Broadcast to Kernel & Compositor  Scope:    Contained within reading process
Safety:   MUTATING / DANGEROUS              Safety:   READ-ONLY / NON-MUTATING
          Violates safe-probe fence                   Conforms to safe-probe fence
```

### 3.1 What Replay / Input Injection Actually Does

1. **Kernel Virtual Device Creation:**
   - In `/usr/lib/libinput/libinput-replay:112–152`, `create(device)` reads the device's recorded evdev properties (`name`, `id`, `codes`, `absinfo`, `properties`).
   - It instantiates a `libevdev.Device()` and invokes `d.create_uinput_device()` (line 148).
   - This issues a `UI_DEV_CREATE` ioctl to the Linux kernel via `/dev/uinput`, instantiating a new virtual kernel device node (`/dev/input/eventX`).
2. **Substrate Mutation via Synthetic Event Stream:**
   - In `replay(device, verbose)` (lines 191–228), the tool iterates over the recorded `events` array and calls `uinput.send_events(evs)` (line 224).
   - The kernel processes these events identically to physical hardware interrupts and routes them to all open evdev readers—specifically the running display server/compositor (e.g. Hyprland).
   - The injected events trigger active compositor actions: window focus shifts, synthetic typing, clicks, workspace changes, or keybinding execution.
3. **Filesystem Side-Effects (Quirks Generation):**
   - In `setup_quirks(recording)` (lines 311–343), `libinput-replay` writes a generated quirk file to `$XDG_RUNTIME_DIR/libinput/libinput-replay*.quirks`. This mutates the runtime directory.
4. **State Corruption Risk upon Interruption:**
   - If replay is interrupted (e.g. `Ctrl+C`), events are halted mid-sequence. Line 292 warns: `"Note that the device may not be in a neutral state now."`
   - A modifier key (`KEY_LEFTCTRL`, `KEY_LEFTALT`), mouse button, or touch point may remain logically held down in the kernel input state, locking the desktop session into an unusable state.
5. **Direct Safety Fence Violation:**
   - `SKILL.md:225–226` explicitly mandates: *"No firing, no injection: `hyprctl dispatch` is a mutation... keystroke injection (`hyprctl dispatch sendshortcut` or synthetic input) is mutation."*
   - Replay is the kernel equivalent of synthetic injection: it directly mutates the running compositor and application plane.

### 3.2 What Read-Only Metadata Actually Consists Of

1. **Isolated Device Descriptors (`libinput record --no-events`):**
   - The official documentation (`tools.rst:282–284`) and man page (`libinput-record.1:69–71`) define `--no-events`:
     *"Only print the device description(s) and exit immediately without waiting for events. The output file will contain the full YAML structure with an empty events section."*
   - The resulting YAML payload contains only structural metadata:
     - `system`: OS distribution, kernel version string, DMI modalias.
     - `libinput`: library version string.
     - `evdev`: device name, bus/vendor/product/version tuple (`struct input_id`), supported event types and code bitmasks (`EV_KEY`, `EV_REL`, `EV_ABS`), axis limits (`input_absinfo`: min, max, fuzz, flat, resolution).
     - `udev`: assigned udev properties (`ID_INPUT_*`).
     - `quirks`: applied quirk attributes.
     - `events`: `[]` (empty list; no event structures, no timestamps).
2. **Built-in Defaults (`libinput list-devices`):**
   - Reports device hardware properties and library built-in defaults (e.g. whether tap-to-click is supported and its default state).
   - Critical boundary: As established by `ReviewLibinput` and `ReviewQuotes` (citing `tools.rst:45–46`), `list-devices` reports libinput defaults, **not** the running desktop session's active configuration.
3. **Compositor Read-Verbs (`hyprctl devices`):**
   - Reads the compositor's own internal view of connected keyboards, mice, and touch devices (counts, device names, active keymap) without injecting events or creating virtual nodes.

---

## 4. Evidence Comparison: Replay vs Read-Only Metadata

| Dimension | `libinput replay` (Synthetic Injection) | `libinput record --no-events` / Metadata |
|---|---|---|
| **Operation Type** | Active write / synthetic injection | Read-only static extraction |
| **Privilege Required** | Root (`sudo` / access to `/dev/uinput`) | Root if reading `/dev/input/event*`; none for static descriptors |
| **Kernel Subsystem** | Writes to `/dev/uinput` via `UI_DEV_CREATE` and `input_event` ioctls | Reads sysfs / udev database / evdev ioctl query |
| **Compositor Impact** | Injected events are consumed by Hyprland; mutates live state | Zero event delivery; compositor is untouched |
| **Session Material** | Injects synthetic keystrokes and pointer coordinates | Shape and capability bitmasks only; no keystrokes captured |
| **Risk of Session Hang** | High (keys/buttons may remain pressed on interrupt) | None (process terminates cleanly) |
| **Mado Policy Status** | **STRICTLY BANNED** (`SKILL.md:225–226`, PROVINCE.md) | **Metadata only** (ladder ground; prefer static XML/config) |

---

## 5. Input Evidence Ladder: Scope of Proof and Non-Proof

For the U6 input-debugging layer route, the distinction between replay and read-only metadata defines what evidence can and cannot prove:

1. **What Read-Only Device Metadata PROVES:**
   - Proves whether a kernel event node exposes specific hardware capabilities (e.g. whether an input device declares `EV_KEY`, `EV_REL`, or `EV_ABS`).
   - Proves the library's built-in default settings for that device model.
2. **What Read-Only Device Metadata DOES NOT PROVE:**
   - Does NOT prove that Hyprland has enabled or configured those capabilities (Hyprland effective settings are governed by `input:*` in `hyprland.conf` and read via `hyprctl getoption`).
   - Does NOT prove that the device is mapped to a Wayland seat or surface.
   - Does NOT prove event delivery or receipt by any client application (`[UNK]`).
3. **What Replay / Injection CANNOT PROVE for Mado:**
   - Replay injects events at the kernel evdev layer (L0). Even if a virtual device accepts injected packets, this does not prove that Hyprland forwarded them across Wayland protocol boundaries (`wl_seat`, `wl_keyboard`, `wl_pointer`) to the focused client surface (`[UNK]`).
   - Because replay actively mutates desktop state and risks hung input states, it is barred from all mado verification and measurement.

---

## 6. Recommendations for U6 Milestone

1. **Formalize Replay Ban in Safe-Probe Allowlist:**
   - The U6 `## Safe boundary` section must explicitly enumerate: `libinput replay`, `/dev/uinput`, and synthetic input injection as strictly forbidden routes.
2. **Exclude Replay Artifacts from Corpus:**
   - No YAML recording with an active `events` section and no replayed trace may be admitted as evidence.
   - If hardware capability descriptors are cited, they must be derived from static documentation (`tools.rst`), package-level specifications (`wayland.xml`), or sanitized compositor reads (`hyprctl devices` shape/counts).
3. **Preserve Unexercised Boundary (`[UNK]`):**
   - The U6 note must conclude with `## Unexercised delivery` containing explicit `[UNK]` for application event delivery, IME composition, and kernel-level event handling.

---

## 7. Remaining Gaps & Unknowns (`[UNK]`)

- `[UNK]` Host kernel configuration for `/dev/uinput` permissions and virtual device naming.
- `[UNK]` Hyprland's internal seat assignment for dynamically added uinput devices (unexercised; no devices created).
- `[UNK]` Real-time event propagation latency between kernel evdev and Wayland client surfaces on this host.

---

## 8. Tooling and Verification

- **Tool installs or updates:** None.
- **Verification to be run by main agent:**
  - Verify report existence and absolute path: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/LibinputReplay.md`.
  - Validate quote discipline: all quotes $\le 25$ words and attributed to pinned revisions.
  - Verify that no replay or mutation command was executed in the workspace.
