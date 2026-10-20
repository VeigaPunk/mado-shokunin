# LibinputTools — round 15 / w1 — report

Seat: `MadoR15.LibinputTools` (scout, leaf; no delegation, no background jobs).  
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`.  
Axis: **coverage** (scouting official libinput 1.32.0 `tools.html` for `list-devices` vs `debug-events` vs `record`/`replay` safety classes). No axis verdict is issued.  
Milestone: U6 input evidence ladder and R14 ancillary provenance correction.

---

## Outcome

- Opened and verified the official upstream libinput 1.32.0 documentation for helper tools at `https://wayland.freedesktop.org/libinput/doc/latest/tools.html` (document title: `Helper tools — libinput 1.32.0 documentation`).
- Located all subcommands, exact anchors, and verbatim quotes across `list-devices`, `list-kernel-devices`, `debug-events`, `debug-gui`, `record`, and `replay`.
- Classified the helper tools into four distinct **Safety Classes**:
  1. **Class 1 — Static Metadata / Capability Enumeration** (`list-devices`, `list-kernel-devices`, `record --no-events`): Read-only capability and built-in driver default queries; explicit non-equivalence to runtime desktop/compositor configuration.
  2. **Class 2 — Live Event Stream Monitoring** (`debug-events`, `debug-gui`): Dynamic evdev event tapping and terminal/GTK stream visualization; requires root privileges; unmanaged event monitoring creates severe live privacy leaks.
  3. **Class 3 — Persistent Event Stream Capture** (`record`): Kernel event capture to serialized YAML; risk of keystroke, timing, and pointer coordinate persistence; masked alphanumeric keys (`'a'`) do not obscure timing or non-alphanumeric input.
  4. **Class 4 — Active Synthetic Event Injection** (`replay`): Kernel `/dev/uinput` virtual device creation and live event re-injection; mutates desktop state and drives active UI components.
- Established the boundary fences for the U6 input evidence ladder: leaf seats must reject execution of live event reading, recording, and replay tools, restricting evidence to static documentation, package metadata, and compositor-plane configuration queries.
- Tooling record: zero tools installed or upgraded by this seat (`MadoR15.LibinputTools`). Observed host package state shifted mid-wave (sibling `MadoR15.LibinputEvents` executed `sudo pacman -S --needed --noconfirm libinput libinput-tools` at 04:25:16 -0300, upgrading `libinput 1.31.3-1` -> `1.32.0-1` and installing `libinput-tools 1.32.0-1`; details in §6).
- No files written except this report. No commits, tests, linters, formatters, builds, smoke runs, or live probes. No credentials or `agent.db*` files accessed.

---

## 1. Upstream Source Identity & Anchors

- **Primary Source URL:** `https://wayland.freedesktop.org/libinput/doc/latest/tools.html`  
  *(Note: Upstream freedesktop maintains the current release documentation at `/doc/latest/tools.html`; the explicit versioned URL `/doc/1.32.0/tools.html` returns HTTP 404, while the document `<title>` explicitly identifies: `Helper tools — libinput 1.32.0 documentation`).*
- **Related Source URL:** `https://wayland.freedesktop.org/libinput/doc/latest/reporting-bugs.html` (`Reporting bugs — libinput 1.32.0 documentation`), referenced by `tools.html` for bug submission, evemu comparisons, and device descriptions.
- **Upstream Git Reference:** `https://gitlab.freedesktop.org/libinput/libinput` (release tag `1.32.0`).

### Top-Level Tool Architecture & Privilege Anchor
- **Heading:** `Helper tools`  
  **Anchor:** `#helper-tools`  
  **Verbatim Quote:**  
  > *"libinput provides a `libinput` tool to query state and events. This tool takes a subcommand as argument, similar to the **git** command. A full explanation of the various commands available in the libinput tool is available in the **libinput(1)** man page."*
- **Kernel Node Access & Root Requirement Quote:**  
  > *"Most of the tools must be run as root to have access to the kernel’s `/dev/input/event*` device files."*

---

## 2. Command Breakdown & Exact Verbatim Quotes

### 2.1 `libinput list-devices` & `libinput list-kernel-devices`
- **Heading:** `libinput list-devices`  
  **Anchor:** `#libinput-list-devices`  
  **Verbatim Purpose Quote:**  
  > *"The `libinput list-devices` command shows information about devices recognized by libinput and can help identifying why a device behaves different than expected. For example, if a device does not show up in the output, it is not a supported input device."*
- **Crucial Compositor Disconnect Warning (Verbatim Note):**  
  > *"Note: This tool does **not** show your desktop’s configuration, just the libinput built-in defaults."*
- **Device Attribute & Option Format Quote:**  
  > *"The `libinput list-devices` command lists general information about the device (the kernel event node) but also the configuration options. If an option is `n/a` it does not exist on this device. Otherwise, the tool will show the default configuration for this device, for options that have more than a binary state all available options are listed, with the default one prefixed with an asterisk (`*`)."*
- **Human Consumption Caveat:**  
  > *"Note: This tool is intended for human-consumption and may change its output at any time."*
- **Kernel Device Enumeration Heading & Anchor:** `libinput list-kernel-devices` (`#libinput-list-kernel-devices`)  
  **Verbatim Quote:**  
  > *"The `libinput list-kernel-devices` command shows the devices known by **the kernel**. This command can help identify issues when a device is not handled by libinput."*

### 2.2 `libinput debug-events` & `libinput debug-gui`
- **Heading:** `libinput debug-events`  
  **Anchor:** `#libinput-debug-events`  
  **Verbatim Purpose Quote:**  
  > *"The `libinput debug-events` command prints events from devices and can help to identify why a device behaves different than expected."*
- **Compositor Simulation Requirement Quote:**  
  > *"All configuration options (enable/disable tapping, etc.) are available as commandline arguments. To reproduce the event sequence as your desktop session sees it, ensure that all options are turned on or off as required. See the **libinput-debug-events(1)** man page or the `--help` output for information about the available options."*
- **Bug Reporting Verbose Flag Note:**  
  > *"Note: When submitting a bug report, always use the `--verbose` flag to get additional information: `libinput debug-events --verbose <other options>`"*
- **Event Stream Representation:**  
  Outputs device addition metadata (`DEVICE_ADDED`, `seat0`, `cap:k|p|t|S`) followed by timestamped event vectors:
  ```text
  -event20  POINTER_MOTION    +3.62s   2.72/ -0.93
   event20  POINTER_MOTION    +3.63s   1.80/ -1.42
  ```
- **GUI Visualization Heading & Anchor:** `libinput debug-gui` (`#libinput-debug-gui`)  
  **Verbatim Quote & Caveat:**  
  > *"A simple GTK-based graphical tool that shows the behavior and location of touch events, pointer motion, scroll axes and gestures. Since this tool gathers data directly from libinput, it is thus suitable for pointer-acceleration testing."*  
  > *"Note: This tool does **not** use your desktop’s configuration, just the libinput built-in defaults."*

### 2.3 `libinput record` and `libinput replay`
- **Heading:** `libinput record and libinput replay`  
  **Anchor:** `#libinput-record-and-libinput-replay` (and `#libinput-record`)  
  **Verbatim Purpose Quote:**  
  > *"The `libinput record` command records the **kernel** events from a specific device node. The recorded sequence can be replayed with the `libinput replay` command. This pair of tools is crucial to capturing bugs and reproducing them on a developer’s machine."*
- **Context Independence & Layer Boundary Quote:**  
  > *"The recorded events are **kernel events** and independent of the libinput context. libinput does not need to be running, it does not matter whether a user is running X.Org or Wayland or even what version of libinput is currently running."*
- **Privacy & Key Code Obfuscation Quote:**  
  > *"For data protection, `libinput record` obscures key codes by default, any alphanumeric key shows up as letter “a”."*
- **Duration Warning Quote:**  
  > *"Warning: The longer the recording, the harder it is to identify the event sequence triggering the bug. Please keep the event sequence as short as possible."*
- **Replay / Virtual Device Creation Quote:**  
  > *"The recording can be replayed with the `libinput replay` command:  
  > `$ sudo libinput replay touchpad.yml`  
  > `libinput replay` creates a new virtual device based on the description in the log file. Hitting enter replays the event sequence once and the tool stops once all events have been replayed. Hitting enter again replays the sequence again, Ctrl+C stops it and removes the virtual device."*
- **Static Device Description Flag Quote:**  
  > *"Sometimes only the device description is needed, e.g. for checking the device’s capabilities, udev properties, or quirks. Use `libinput record --no-events` to print the device description and exit immediately without waiting for any events:  
  > `$ sudo libinput record --no-events /dev/input/event17`"*
- **Autorestart & Multi-Device Anchors:**  
  - `#libinput-record-s-autorestart-feature`: `"libinput record often collects thousands of events per minute... It is thus imperative that the event log is kept as short as possible."`
  - `#recording-multiple-devices-at-once`: `"Recording multiple devices requires the --output-file argument..."`

---

## 3. Safety Class Taxonomy & Boundary Analysis

| Safety Class | Representative Tools | Substrate / Device Node | Behavioral Nature | Privacy & State Impact | Mado Seat Boundary Policy |
|---|---|---|---|---|---|
| **Class 1: Static Metadata Inspection** | `libinput list-devices`, `libinput list-kernel-devices`, `record --no-events` | `/dev/input/event*` (kernel evdev nodes) | Read-only static query of hardware capabilities, group IDs, and built-in defaults. | No session event interception. However, output reflects **only driver built-in defaults**, NOT compositor runtime config. | **Execution rejected in leaf seats** (no live probes/privilege elevation). Permitted as static reference documentation only. |
| **Class 2: Live Event Monitoring** | `libinput debug-events`, `libinput debug-gui` | `/dev/input/event*` (live evdev stream) | Dynamic observation and formatting of unmanaged kernel input events. | **Active privacy leak.** Snoops raw keystrokes, pointer motion, and touch points across all desktop windows, bypassing Wayland client isolation. | **Strictly prohibited** ("no input event reading/recording/replay/injection"). |
| **Class 3: Event Stream Capture & Serialization** | `libinput record` | `/dev/input/event*` -> YAML file | Persistent serialization of raw timestamped kernel event sequences. | **Severe privacy & storage risk.** Captures high-frequency timing and input. Masking alphanumeric keys to `'a'` does NOT protect non-alphanumeric keys, modifiers, or motion traces. | **Strictly prohibited** ("no input event reading/recording/replay/injection"). |
| **Class 4: Synthetic Event Injection** | `libinput replay` | `/dev/uinput` (virtual kernel input device) | Active hardware emulation and synthetic event injection into the kernel input stack. | **Direct system mutation.** Triggers real compositor event processing, focus shifts, window activations, and potential unintended UI actions. | **Strictly prohibited** ("never mutates a running compositor state"; "no replay/injection"). |

---

## 4. Why Recording and Replay Are Prohibited in Mado-Shokunin

1. **PROVINCE.md Boundary Violation:**  
   `PROVINCE.md` states: *"Never mutates a running compositor state... Refuses: secrets in configs (shape-only, -> kagi)... Out of province -> report, never absorb."*  
   `libinput replay` injects events via kernel virtual devices, mutating the live compositor state and dispatching synthetic events to Wayland clients. This is an active state mutation, explicitly forbidden for non-operator seats.
2. **Session Material & Privacy Leaks (SKILL.md § Standing Rules):**  
   `SKILL.md` establishes: *"Session material (window titles, hyprland.log, instance signatures) is shape-only too (MADO-R2-1 §0)."*  
   Raw event streams captured by `libinput debug-events` and `libinput record` capture real user session material. Even though `record` replaces alphanumeric keycodes with `'a'`, it retains:
   - Key press/release timing (vulnerable to keystroke timing analysis and password length inference).
   - Non-alphanumeric keycodes (Return, Backspace, Escape, Tab, Super, Alt, Control), exposing desktop hotkeys and command navigation.
   - Exact pointer motion deltas and touch coordinates across private windows.
3. **Privilege Boundary:**  
   As documented in `tools.html` (`#helper-tools`), `libinput` tools require root access to open `/dev/input/event*`. Leaf seats must not invoke privileged probes or raw device snooping.

---

## 5. Epistemic Boundary in the U6 Input Evidence Ladder

In building the U6 input-debugging ladder (kernel -> libinput -> compositor -> Wayland protocol -> client application):

1. **What `libinput list-devices` Proves vs Does NOT Prove:**  
   - **Proves:** Whether a physical kernel input device is recognized by the libinput library, its detected hardware capabilities (`pointer`, `keyboard`, `touch`, `tablet`), physical dimensions, and driver-level built-in defaults.
   - **Does NOT Prove:** Active compositor policy. As emphasized by the official doc note (*"This tool does not show your desktop’s configuration, just the libinput built-in defaults"*), it cannot prove Hyprland's active keymap (`input:kb_layout`), sensitivity, natural scrolling toggle, or window focus rules.
2. **What `debug-events` Proves vs Does NOT Prove:**  
   - **Proves:** That the kernel evdev subsystem is generating events for device interactions and that libinput can parse those events.
   - **Does NOT Prove:** That the compositor delivered those events to any client application. The compositor can filter, suppress, re-bind, or discard events (e.g. global keybindings, lock screen suppression, inactive surfaces).
3. **The Clean Ladder Boundary:**  
   - Level 1 (Kernel Hardware): Kernel event nodes (`/dev/input/event*`).
   - Level 2 (Libinput Library): Driver capabilities & defaults (`tools.html`).
   - Level 3 (Compositor Plane): Configuration via `hyprctl getoption input:*` and device registry via `hyprctl devices` (`[OBS]`).
   - Level 4 (Wayland Core Protocol): Surface focus and event protocol specification (`wl_seat`, `wl_keyboard`, `wl_pointer`) (`[INF-docs]`).
   - Level 5 (Client Application): Actual application event receipt and UI reaction (`[UNK]`, unexercised delivery boundary).

---

## 6. Tooling Directive & Host Package Mutation Record

1. **Seat Action:**  
   - `MadoR15.LibinputTools` installed or upgraded **zero tools** (no pacman, uv, cargo, or npm executions).
   - Queries executed strictly via read-only static documentation fetch (`read` of upstream freedesktop HTML) and non-mutating package queries (`pacman -Q`, `pacman -Ss`).

2. **Host Package Baseline Mutation Observed During Wave:**  
   - **Baseline at Wave Start:** `libinput 1.31.3-1` (installed), `libinput-tools` (not installed).
   - **Mid-Wave Upgrade Event:** At `2026-10-20T04:25:16-0300` (`2026-10-20T07:25:16.905Z`), sibling seat `MadoR15.LibinputEvents` executed:
     ```bash
     sudo pacman -S --needed --noconfirm libinput libinput-tools
     ```
   - **Package Delta (/var/log/pacman.log lines 2429–2437):**  
     - `libinput`: upgraded `1.31.3-1` -> `1.32.0-1`
     - `libinput-tools`: installed `1.32.0-1` (new)
     - Implicit dependencies installed: `python-libevdev 0.13.1-1`, `python-pyudev 0.24.4-1`, `python-yaml 6.0.3-2`
   - **Channel / Reason:** Official Arch Linux `extra` repository; sibling sought local man pages and helper CLI under intent *"Install libinput and libinput-tools 1.32.0"*.
   - **Update Safety Assessment:**  
     - Represents an unsynced partial package upgrade (no `-Syu` full system sync), triggering `10-limine-snapper-lock.hook` and `35-systemd-udev-reload.hook`.
     - **Runtime State Disconnect:** The active Hyprland compositor process continues running with the pre-upgrade `libinput.so.10` mapped in memory; disk package binaries now reflect `1.32.0-1`.
     - This seat did not execute or rely on the installed host binaries, anchoring findings strictly on upstream documentation.
---

Report written to: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/LibinputTools.md`
