# LibinputEvents — libinput 1.32.0 debug-events documentation and boundary analysis

Seat: `MadoR15.LibinputEvents` (scout, leaf; no delegation, no background jobs).  
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`.  
Axis: **coverage** (scouting official libinput 1.32.0 `debug-events` documentation to ground U6 input boundary without live event collection).  
Milestone context: U6 input evidence ladder (moving coverage 5/7 -> 6/7) and R14 ancillary provenance correction.

---

## 1. Tooling & Package Transaction Record

Per operator tooling directive (RULES.md) and parent seat coordination (`MadoR15`):

- **Transaction**: `sudo pacman -S --needed --noconfirm libinput libinput-tools`
  - Timestamp: `2026-10-20T04:25:16-0300` (`07:25:16Z`)
  - Packages upgraded: `libinput` (`1.31.3-1` -> `1.32.0-1`)
  - Packages installed: `libinput-tools` (`1.32.0-1`), `python-libevdev` (`0.13.1-1`), `python-pyudev` (`0.24.4-1`), `python-yaml` (`6.0.3-2`)
  - Channel: official Arch Linux repository (`extra`)
  - Reason: static inspection of libinput 1.32.0 documentation, installed man pages (`libinput-debug-events.1.gz`), and CLI flags.
- **Commands run post-install**:
  1. `pacman -Ql libinput libinput-tools | grep man` (static package file verification)
  2. `man 1 libinput-debug-events | col -bx` (static man page inspection)
  3. `/usr/bin/libinput debug-events --help` (static CLI options print)
  4. `ls -l /usr/include/libinput.h` (installed header verification)
  5. `sha256sum /usr/share/man/man1/libinput-debug-events.1.gz`
- **Non-execution guarantee**:
  - ZERO device nodes (`/dev/input/event*`) opened or accessed.
  - ZERO input events read, monitored, recorded, replayed, or injected.
  - `libinput debug-events` was NEVER invoked beyond `--help`.
  - No system services or compositors restarted.

---

## 2. Upstream Anchors & Documented Identities (libinput 1.32.0)

- **Official Web Documentation**:
  - URL: `https://wayland.freedesktop.org/libinput/doc/latest/tools.html#libinput-debug-events`
  - Title: `Helper tools — libinput 1.32.0 documentation`
- **Installed Man Page**:
  - File: `/usr/share/man/man1/libinput-debug-events.1.gz`
  - Package: `libinput-tools 1.32.0-1`
  - Compressed SHA-256: `dc38aae29479ed54fa90318bddb3cb52d815565de276b3dec459f8afd09f8b9e`
  - Decompressed SHA-256: `8d024afc514b78e3e4a24c1983e4a666cb065571542c663120eda9fbc35e9156`
- **Upstream Git Repository & Revision**:
  - Repository: `https://gitlab.freedesktop.org/libinput/libinput.git`
  - Git Tag: `refs/tags/1.32.0` (tag object `c7e6fe66f509ba2eda680c28aa64795987b49e7c`, commit `5cf833b572f5a33663888da321dce0ba1abd82a2`)
  - `tools/libinput-debug-events.man` (SHA-256 `92c23aa4b286833cc3a89644327a7c7a2a24dbdcc5c1904c16b646f0167655f8`)
  - `tools/libinput-debug-events.c` (SHA-256 `c69f55673afcd5b326f600a6827c17fbb06ff2a06d0748f31bf99d268c5b216a`)
  - `src/util-libinput.c` (SHA-256 `efbe80d0bbe60276789756e558759733b8c13aa879a9f76825042dfe2bc0f303`)
  - `tools/shared.c` (SHA-256 `2306a7f845dc0bec45e67a1faff239337d218d372c62c5da845d991e514b7f6f`)

---

## 3. Analysis: Privileges, Event Content, and Context Scope

### A. Device Access Privileges (Kernel evdev Access Boundary)
1. **Root Requirement**:
   - `libinput-debug-events(1)`: *"This tool usually needs to be run as root to have access to the /dev/input/eventX nodes."*
   - `tools.html`: *"Most of the tools must be run as root to have access to the kernel’s /dev/input/event\* device files."*
   - Implementation (`tools/shared.c:open_restricted()`): Uses standard POSIX `open(path, flags)` directly. Because character devices under `/dev/input/event*` default to permissions `0660 root:input`, unprivileged users cannot open these nodes directly.
   - Unlike Wayland compositors (which integrate with `systemd-logind` or `seatd` via D-Bus `TakeDevice` to obtain pre-authenticated file descriptors for active graphical sessions without root privileges), `libinput debug-events` lacks unprivileged session brokering.
2. **Disruptive Exclusive Grab (`--grab`)**:
   - `libinput-debug-events(1)`: *"--grab: Exclusively grab all opened devices. This will prevent events from being delivered to the host system."*
   - Implementation (`tools/shared.c:open_restricted()`): Executes `ioctl(fd, EVIOCGRAB, (void *)1)`.
   - Impact: In kernel evdev, `EVIOCGRAB` grants exclusive consumption of event nodes to the grabber. Invoking `--grab` starves the active Wayland compositor (Hyprland), immediately causing host input freeze.

### B. Event Content & Privacy Boundary
1. **Event Types & Scope**:
   - Device Lifecycle: `DEVICE_ADDED` (prints seat, group, capabilities `cap:k` (keyboard), `cap:p` (pointer), `cap:t` (touch), `cap:g` (gesture), `cap:S` (switch), resolution, tapping/scroll configuration).
   - Motion & Interaction Streams: `POINTER_MOTION` (timestamps, `dx`/`dy`, unaccelerated deltas), `POINTER_BUTTON`, `POINTER_AXIS`, `TOUCH_DOWN`, `TOUCH_MOTION`, `GESTURE_SWIPE_*`, `GESTURE_PINCH_*`.
2. **Keyboard Key Events & Obfuscation**:
   - Implementation (`src/util-libinput.c:print_key_event()`):
     ```c
     key = libinput_event_keyboard_get_key(k);
     if (!opts->show_keycodes && (key >= KEY_ESC && key < KEY_ZENKAKUHANKAKU)) {
         keyname = "***";
         key = -1;
     } else {
         keyname = libevdev_event_code_get_name(EV_KEY, key);
     }
     ```
   - Partial Obfuscation:
     - By default, alphanumeric keys in the range `[KEY_ESC, KEY_ZENKAKUHANKAKU)` are masked as `*** (-1)`.
     - `libinput-debug-events(1)`: *"--show-keycodes: Key events shown by this tool are partially obfuscated to avoid passwords and other sensitive information showing up in the output. Use the --show-keycodes argument to make all keycodes visible."*
   - Privacy Hazard:
     - Even with default obfuscation, functional keys, modifier states, inter-keystroke timings, pointer coordinates, and touch interactions are fully exposed.
     - Live execution across a user session captures arbitrary user activity.
3. **Upstream Warning on Output Stability**:
   - `libinput-debug-events(1)`: *"This is a debugging tool only, its output may change at any time. Do not rely on the output."*

### C. Context Scope & Architectural Disconnect
1. **Isolated Context vs. Compositor Context**:
   - `libinput-debug-events(1)` (NOTES): *"Events shown by this tool may not correspond to the events seen by a different user of libinput. This tool initializes a separate context."*
   - `tools.html`: *"Note: This tool does not show your desktop’s configuration, just the libinput built-in defaults."*
   - Implementation (`tools/libinput-debug-events.c:main()`): Calls `tools_open_backend()` which allocates a fresh `struct libinput *li` via `libinput_udev_create_context()` or `libinput_path_create_context()`.
   - The tool does **not** attach to, inspect, or reflect the running Wayland compositor's libinput instance. Compositor-configured acceleration profiles, custom tap mappings, disabled devices, or calibration overrides are invisible to `debug-events` unless manually recreated as CLI options.
2. **Sub-Compositor Layer Limitations**:
   - `debug-events` sits at the Linux kernel `evdev -> libinput` boundary.
   - It cannot observe:
     - Wayland compositor dispatch and event loop scheduling.
     - Wayland seat protocol delivery (`wl_seat`, `wl_keyboard`, `wl_pointer`, `wl_touch`).
     - Keymap and layout resolution (libinput handles raw kernel `KEY_*` codes; XKB state, modifiers, and keysym mapping are handled in the compositor and client via `libxkbcommon`).
     - Input Method Editor (IME) text input commits (`zwp_text_input_v3`).
     - Window focus, surface targeting, layer-shell grabs, and compositor keybindings.

---

## 4. Recommendation: Rejection Boundary, Not Execution

Executing `libinput debug-events` as an evidence collection probe for U6 MUST be **REJECTED**:

1. **Privilege Boundary**: Requires superuser (`root`) access to `/dev/input/event*`, which is outside unprivileged leaf boundaries.
2. **Privacy Boundary**: Ingesting live input streams captures sensitive host interaction (keystroke timings, navigation, pointer trajectories).
3. **Disruption Hazard**: Potential contention or accidental `--grab` (`EVIOCGRAB`) starves the active Wayland session of input.
4. **Epistemic Disconnect**: Running a separate libinput context measures neither compositor configuration nor Wayland client delivery.

### Recommended Architectural Role in U6 Evidence Ladder

Instead of running live debugging probes, U6 coverage should ground the **input debugging layer route** as a set of strictly partitioned architectural boundaries:

| Layer Boundary | Subsystem | Evidence Ground | Verification / Execution Status |
|---|---|---|---|
| **Layer 0: Kernel evdev** | `/dev/input/event*` character nodes | Linux kernel evdev subsystem | `[REJECTED]` Live access requires root; unexercised. |
| **Layer 1: Input Library** | `libinput` event processing & device quirks | Upstream `libinput` 1.32.0 docs (S007, `libinput-debug-events(1)`) | `[INF-docs]` Static documentation of debugging tools, separate context isolation, and built-in defaults. Live execution rejected. |
| **Layer 2: Compositor Input Engine** | Compositor libinput instance, device config, XKB map | Read-only compositor query (e.g. `hyprctl devices`) | `[OBS]` Host metadata showing compositor-recognized keyboards/mice without reading event streams. |
| **Layer 3: Wayland Protocols** | `wl_seat`, `wl_keyboard`, `wl_pointer` | Core `wayland.xml` & advertised globals (S043, S041) | `[INF-docs]` Protocol specification of input capabilities and seat lifecycle. |
| **Layer 4: Delivery & IME** | Client surface focus, `text-input`, active bindings | Compositor routing & window management | `[UNK]` Explicit unexercised limit; no client input sniffing or synthetic injection. |

---

## 5. Candidate SOURCES Registry Information (for L1)

If L1 promotes or supersedes row S007 for U6:

- **Source ID**: `S007` (or superseding row `S051+`)
- **Title**: `libinput helper tools & debug-events specification — libinput 1.32.0`
- **Location**: `https://wayland.freedesktop.org/libinput/doc/latest/tools.html#libinput-debug-events` & `man:libinput-debug-events(1)`
- **Revision / Tag**: Git tag `1.32.0` (commit `5cf833b572f5a33663888da321dce0ba1abd82a2`)
- **Key Anchors**:
  - `tools.html#libinput-debug-events`: *"Most of the tools must be run as root to have access to the kernel's /dev/input/event\* device files."*
  - `libinput-debug-events(1)` NOTES: *"Events shown by this tool may not correspond to the events seen by a different user of libinput. This tool initializes a separate context."*
  - `libinput-debug-events(1)` OPTIONS: *"--show-keycodes: Key events shown by this tool are partially obfuscated to avoid passwords and other sensitive information showing up in the output."*
- **Tier**: `docs` (Tier A)
- **Status Lifecycle**: `mined` when integrated into the U6 knowledge note; establishes the input debugging layer route as an architectural rejection boundary.

---

## 6. Files Written

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/LibinputEvents.md` (this report only)
