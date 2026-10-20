# InputVersions — Static Package Queries, XML Paths, and Help Availability

**Seat:** `MadoR15.InputVersions` (scout, leaf)  
**Judged on:** coverage (C1)  
**Milestone:** U6 input evidence ladder and R14 ancillary provenance correction  
**Report path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/InputVersions.md`  
**Execution posture:** Static inspection only; no sudo/raw device access, no event observation, no live probes, no compositor action. Installs performed by this seat: **none** (0 packages).

---

## 1. Package Versions & Environment Provenance

### 1.1 Static Package Query Findings

| Package | Package Version | Build Date | Install Date | Pkg-Config / Header Version | Upstream URL |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `wayland` | `1.26.0-1` | 2026-08-09 | 2026-10-11 | `1.26.0` (`/usr/include/wayland-version.h`: `WAYLAND_VERSION "1.26.0"`, `MAJOR 1`, `MINOR 26`, `MICRO 0`) | `https://wayland.freedesktop.org/` |
| `wayland-protocols` | `1.49-1` | 2026-06-07 | 2026-10-03 | `1.49` (`/usr/share/pkgconfig/wayland-protocols.pc`) | `https://wayland.freedesktop.org/` |
| `wlr-protocols` | `r112.a741f0a-1` | — | 2026-10-20 (02:41:32) | `1.0` (`/usr/share/pkgconfig/wlr-protocols.pc`, commit `a741f0ac5d655338a5100fc34bc8cec87d237346`) | `https://gitlab.freedesktop.org/wlroots/wlr-protocols` |
| `hyprland` | `0.56.2-2` | 2026-09-01 | 2026-10-11 | `0.56.2` (git commit `efb50993...`) | `https://github.com/hyprwm/Hyprland` |
| `aquamarine` | `0.15.0-2` | 2026-09-04 | 2026-10-11 | `0.15.0` (`Provides: libaquamarine.so=14-64`) | `https://github.com/hyprwm/aquamarine` |
| `xf86-input-libinput` | `1.5.0-1` | — | 2026-10-03 | `1.5.0` (`/usr/lib/pkgconfig/xorg-libinput.pc`) | `https://xorg.freedesktop.org/` |

### 1.2 `libinput` Package Baseline vs Mid-Round Package Mutation

A critical discrepancy between baseline host package state, mid-round on-disk package state, and running compositor memory state was observed:

1. **Host Baseline at Wave Launch:**
   - Package: `libinput 1.31.3-1` (installed 2026-10-03, build date 2026-06-03).
   - `libinput.pc`: `Version: 1.31.3` (SHA-256: `0772d9506570e0cc9bfcec8a2376c0cad38f000cd94399b7ae60f2df4707b241`).
   - Debug utilities package: `libinput-tools` was **not installed** at wave launch (`pacman -Q libinput-tools` returned code 1).
2. **Mid-Round Package Mutation:**
   - At `2026-10-20T04:25:16-0300` (logged in `/var/log/pacman.log`), sibling seat `MadoR15.LibinputEvents` executed `sudo pacman -S --needed --noconfirm libinput libinput-tools` via official Arch `extra` channel.
   - Result:
     - `libinput`: upgraded `1.31.3-1` -> `1.32.0-1` (build date 2026-09-17).
     - `libinput-tools`: installed `1.32.0-1` (`/usr/bin/libinput`).
     - Dependencies installed: `python-libevdev 0.13.1-1`, `python-pyudev 0.24.4-1`, `python-yaml 6.0.3-2`.
3. **Running Compositor Memory Isolation:**
   - Active Hyprland process (`pid 1706`) continues mapping `/usr/lib/libinput.so.10.13.0 (deleted)`.
   - **Invariance Rule:** The running compositor retains the pre-upgrade `1.31.3-1` library in memory. On-disk packages now report `1.32.0-1`. The running compositor version must **never** be inferred from on-disk package state after mid-wave mutation.

---

## 2. Installed XML Availability and Paths

### 2.1 Core Wayland Input Interfaces (`wayland 1.26.0-1`)

- **File Path:** `/usr/share/wayland/wayland.xml`
- **File SHA-256:** `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07` (3,442 lines, 137,847 bytes)
- **Input Interfaces Defined:**
  - `wl_seat` (interface version 11, lines 2004–2136):
    - Summary: `"group of input devices"`
    - Capabilities: bitmask entries `pointer = 1` (`"the seat has pointer devices"`), `keyboard = 2` (`"the seat has one or more keyboards"`), `touch = 4` (`"the seat has touch devices"`).
    - Error: `missing_capability = 0` (`"get_pointer, get_keyboard or get_touch called on seat without the matching capability"`).
    - Requests: `get_pointer`, `get_keyboard`, `get_touch`, `release` (v5).
    - Events: `capabilities`, `name` (v2).
  - `wl_pointer` (interface version 11, lines 2138–2571):
    - Summary: `"pointer input device"`
    - Error: `role = 0` (`"given wl_surface has another role"`).
    - Requests: `set_cursor`, `release` (v3).
    - Events: `enter`, `leave`, `motion`, `button`, `axis`, `frame` (v5), `axis_source` (v5), `axis_stop` (v5), `axis_discrete` (v5), `axis_value120` (v8), `axis_relative_direction` (v9).
  - `wl_keyboard` (interface version 11, lines 2573–2752):
    - Summary: `"keyboard input device"`
    - Keymap Format: `no_keymap = 0`, `xkb_v1 = 1` (`"libxkbcommon compatible, null-terminated string; to determine the xkb keycode, clients must add 8 to the key event keycode"`).
    - Requests: `release` (v3).
    - Events: `keymap`, `enter`, `leave`, `key`, `modifiers`, `repeat_info` (v4).
  - `wl_touch` (interface version 11, lines 2754–2898):
    - Summary: `"touchscreen input device"`
    - Requests: `release` (v3).
    - Events: `down`, `up`, `motion`, `frame`, `cancel`, `shape` (v6), `orientation` (v6).

### 2.2 Extended Input Protocols (`wayland-protocols 1.49-1`)

All installed under `/usr/share/wayland-protocols/`:

| Subsystem / Protocol | Classification | Absolute Path | SHA-256 | Interfaces Defined |
| :--- | :--- | :--- | :--- | :--- |
| **Tablet** | Stable | `/usr/share/wayland-protocols/stable/tablet/tablet-v2.xml` | `ac1128b26c779cf90b9ed71182ba5e34a7262826789adae206d825a4d45908b4` | `zwp_tablet_manager_v2`, `zwp_tablet_seat_v2`, `zwp_tablet_tool_v2`, `zwp_tablet_v2`, `zwp_tablet_pad_ring_v2`, `zwp_tablet_pad_strip_v2`, `zwp_tablet_pad_group_v2`, `zwp_tablet_pad_v2` |
| **Cursor Shape** | Staging | `/usr/share/wayland-protocols/staging/cursor-shape/cursor-shape-v1.xml` | `bb57d91e53a79dadab7c612dab87c233393cee73673feefa7442cfbfdd9aed2f` | `wp_cursor_shape_manager_v1`, `wp_cursor_shape_device_v1` |
| **Pointer Warp** | Staging | `/usr/share/wayland-protocols/staging/pointer-warp/pointer-warp-v1.xml` | `1389e89c68c6f6d231fd2dcda57fa9c75c5230d0ac1deffa8d80a7648e197e66` | `wp_pointer_warp_v1` |
| **Transient Seat** | Staging | `/usr/share/wayland-protocols/staging/ext-transient-seat/ext-transient-seat-v1.xml` | `d7d836047218030558bbd4e706e6a9b7e91338c4b2b637215be6a5d26da58d81` | `ext_transient_seat_manager_v1`, `ext_transient_seat_v1` |
| **Pointer Gestures** | Unstable | `/usr/share/wayland-protocols/unstable/pointer-gestures/pointer-gestures-unstable-v1.xml` | `9f7b6ad542f444001312113395b8de6f24e59d6f0c57c9b44f6c3c498ef004d7` | `zwp_pointer_gestures_v1`, `zwp_pointer_gesture_swipe_v1`, `zwp_pointer_gesture_pinch_v1`, `zwp_pointer_gesture_hold_v1` |
| **Relative Pointer** | Unstable | `/usr/share/wayland-protocols/unstable/relative-pointer/relative-pointer-unstable-v1.xml` | `ab4930dd3084f732b6fdd12ee6dbd0a112a758ed8a57b170366391dbeb1a22ff` | `zwp_relative_pointer_manager_v1`, `zwp_relative_pointer_v1` |
| **Pointer Constraints** | Unstable | `/usr/share/wayland-protocols/unstable/pointer-constraints/pointer-constraints-unstable-v1.xml` | `f980fac900ba1dcfbbe97f588fc17b893926bd2b57624563653a1bfe4d035948` | `zwp_pointer_constraints_v1`, `zwp_locked_pointer_v1`, `zwp_confined_pointer_v1` |
| **Text Input** | Unstable | `/usr/share/wayland-protocols/unstable/text-input/text-input-unstable-v3.xml` | `160815cda13c285a30df1971d8f0a5b3aac07071537df59916d2f748b18e4f59` | `zwp_text_input_manager_v3`, `zwp_text_input_v3` |
| **Input Method** | Unstable | `/usr/share/wayland-protocols/unstable/input-method/input-method-unstable-v1.xml` | `e04464e22eee9ac67e21c3316c8bb47293656902c2f26b91ebdd8b40eeba03a0` | `zwp_input_method_context_v1`, `zwp_input_method_v1`, `zwp_input_panel_v1`, `zwp_input_panel_surface_v1` |
| **Input Timestamps** | Unstable | `/usr/share/wayland-protocols/unstable/input-timestamps/input-timestamps-unstable-v1.xml` | `375d336bbff6331a31c55c276ceb253b3ae9d6b2cba7261ea2a014a60c05df17` | `zwp_input_timestamps_manager_v1`, `zwp_input_timestamps_v1` |
| **Keyboard Inhibit** | Unstable | `/usr/share/wayland-protocols/unstable/keyboard-shortcuts-inhibit/keyboard-shortcuts-inhibit-unstable-v1.xml` | `9fa733d9a3b6883e3519d5c3d23eb8122c4dcf2e4d034293f7739fc03f9c6fb4` | `zwp_keyboard_shortcuts_inhibit_manager_v1`, `zwp_keyboard_shortcuts_inhibitor_v1` |
| **XWayland Grab** | Unstable | `/usr/share/wayland-protocols/unstable/xwayland-keyboard-grab/xwayland-keyboard-grab-unstable-v1.xml` | `be39999dae2a3cae890c0032dfa7fbfae037f070cb72be0a597a1f592658a5c3` | `zwp_xwayland_keyboard_grab_manager_v1` |

### 2.3 `wlr-protocols` Input Protocols (`r112.a741f0a-1`)

- Virtual Pointer: `/usr/share/wlr-protocols/unstable/wlr-virtual-pointer-unstable-v1.xml` (SHA-256: `3ff6d540be0bc5228195bf072bde42117ea17945a5c2061add5d3cf97d6bb524`)
  - Interfaces: `zwlr_virtual_pointer_manager_v1` (v2), `zwlr_virtual_pointer_v1` (v2)
- Input Inhibitor: `/usr/share/wlr-protocols/unstable/wlr-input-inhibitor-unstable-v1.xml` (SHA-256: `18fbb52c208479e0a293526017feec271297eefb2d9d1bc94ae3b6c5961d71ff`)
  - Interfaces: `zwlr_input_inhibit_manager_v1` (v1), `zwlr_input_inhibitor_v1` (v1)

### 2.4 `libinput` Protocol XML Status

`libinput` provides **NO** Wayland XML protocol files (`pacman -Ql libinput | grep -i xml` returns empty).
- `libinput` is a low-level device management and event handling library written in C. It interfaces with the Linux kernel via `evdev` and `udev`, and provides C APIs declared in `/usr/include/libinput.h` (7,453 lines, SHA-256: `cf36c7eb7dcd784318e0519624d5342c0c828ef32b9478f4f06990822cdbfcd4`).
- Static hardware quirks database: installed at `/usr/share/libinput/*.quirks` (52 `.quirks` files, e.g. `10-generic-keyboard.quirks`, `30-vendor-logitech.quirks`, `50-system-apple.quirks`).

---

## 3. Relevant Static Help & Tooling Availability

All help texts were obtained via standard non-interactive `--help` query flags without executing device nodes or live event probes.

### 3.1 `wayland-scanner` Help (`wayland 1.26.0-1`)

- Path: `/usr/bin/wayland-scanner`
- Synopsis: `wayland-scanner [OPTION] [client-header|server-header|enum-header|private-code|public-code] [input_file output_file]`
- Options:
  - `-h, --help`: display this help and exit.
  - `-v, --version`: print the wayland library version that the scanner was built against.
  - `-c, --include-core-only`: include the core version of the headers (e.g. `wayland-client-core.h` instead of `wayland-client.h`).
  - `-s, --strict`: exit immediately with an error if DTD verification fails.

### 3.2 `wayland-info` Help (`wayland-utils 1.3.0-1`)

- Path: `/usr/bin/wayland-info`
- Synopsis: `wayland-info [options...]`
- Options:
  - `-h|--help`: Print this help and exit.
  - `-i|--interface <interface>`: Only print information about the Wayland globals containing `<interface>` in their name (e.g. `wl_seat`, `wp_cursor_shape_manager_v1`).

### 3.3 `hyprctl` Input-Relevant Subcommands (`hyprland 0.56.2-2`)

- Path: `/usr/bin/hyprctl`
- Input-Relevant Commands (from `hyprctl --help`):
  - `devices`: `"Lists all connected keyboards and mice"`
  - `cursorpos`: `"Gets the current cursor position in global layout coordinates"`
  - `getoption <option>`: `"Gets the config option status (values)"` (e.g. input options `input:sensitivity`, `input:kb_layout`)
  - `switchxkblayout ...`: `"Sets the xkb layout index for a keyboard"`
  - Flags: `-j` (JSON output), `-r` (refresh state), `--instance (-i)` (specific instance).

### 3.4 `libinput` Helper Tools & Safety Classification (`libinput-tools 1.32.0-1`)

From `/usr/bin/libinput --help` and associated man pages (`libinput(1)`, `libinput-list-devices(1)`, `libinput-record(1)`, `libinput-debug-events(1)`):

1. **`libinput list-devices` (Static / Configuration Query Class):**
   - Synopsis: `libinput list-devices [--help|--version]`
   - Scope: Enumerates local evdev nodes on default seat `seat0` and lists libinput built-in default configuration options.
   - **Boundary Fence:** Does **not** show the Wayland compositor's runtime configuration (`libinput-list-devices(1)` notes: *"creates a libinput context on the default seat 'seat0' ... A device may be recognized by libinput but not handled by the X.Org libinput driver or the Wayland compositor"*).
2. **`libinput debug-events` (Active Event Stream Debugging Class):**
   - Synopsis: `libinput debug-events [options] [--udev <seat>|--device /dev/input/event0 ...]`
   - Scope: Prints live input events to stdout.
   - Options: `--grab` (exclusively grabs device, starving compositor), `--compress-motion-events`, `--show-keycodes`.
   - **Safety Fence:** Unexercised in this audit; prohibited under no-live-probes / no-event-observation rule.
3. **`libinput record` / `libinput replay` (Kernel Raw Event Capture & Injection Class):**
   - Synopsis: `libinput record [options] [/dev/input/event0 ...]`
   - Scope: Records raw kernel evdev streams directly into YAML.
   - **Safety Fence:** Requires direct `/dev/input/eventX` access (`sudo libinput-record`). Replay injects events via `/dev/uinput`. Both strictly unexercised and out of bounds for non-invasive debugging.

---

## 4. Confidence & Remaining Gaps

- **Confidence:** Absolute (100%) for installed package versions, pkg-config metadata, SHA-256 sums of XML files and headers, and static help synopsis text.
- **Identified Gap / Anomaly:** Mid-round package upgrade executed by sibling seat `MadoR15.LibinputEvents` at 04:25:16 created a dichotomy between on-disk package state (`1.32.0-1`) and running compositor process memory (`1.31.3-1` DSO mapping). Integrators must cite the appropriate baseline vs disk layer explicitly.
- **Unexercised Boundaries:** No event observation, no `/dev/input/event*` reading, no live IPC calls to `hyprctl devices` or `wayland-info`, and no compositor mutation were performed.

---

## 5. Tooling Statement

No tools or packages were installed, updated, or removed by seat `MadoR15.InputVersions`.
All queries were executed strictly via read-only inspection tools (`pacman -Q`, `pkg-config`, `sha256sum`, and static binary `--help`).
