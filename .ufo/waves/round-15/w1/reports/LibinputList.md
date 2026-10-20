# LibinputList — Official libinput 1.32.0 list-devices documentation: default vs compositor configuration boundaries (mado-r15-w1)

Seat: `MadoR15.LibinputList` (scout, leaf)  
Judged on: coverage (C1)  
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`  
Milestone: U6 input evidence ladder and R14 ancillary provenance correction  
Report path: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/LibinputList.md`  
Tooling record: 0 tools installed or upgraded in this lane.

---

## 1. Primary Sources & Documentation Anchors

This investigation examines the official libinput 1.32.0 documentation and installed manual pages via static, read-only inspection:

1. **Upstream Tagged User Documentation (tools.rst):**
   - Canonical URL: `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst`
   - Revision: Git tag `1.32.0` (blob SHA-256: `53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f`)
   - Section: `.. _libinput-list-devices:` (lines 40–88)

2. **Published HTML Documentation:**
   - Canonical URL: `https://wayland.freedesktop.org/libinput/doc/latest/tools.html#libinput-list-devices`
   - Page Title: `Helper tools — libinput 1.32.0 documentation` (generated from git commit `4cf1775`)
   - Cross-reference: `https://wayland.freedesktop.org/libinput/doc/latest/what-is-libinput.html` and `https://wayland.freedesktop.org/libinput/doc/latest/configuration.html`

3. **Installed System Manual Pages:**
   - Path: `/usr/share/man/man1/libinput-list-devices.1.gz`
   - Package: `libinput-tools 1.32.0-1` (Arch official package, SHA-256: `bc1dc08c9c7d9504254a28e4257d72ec38f6af0154cb0e480ae501bd8af6c13a`)
   - Header: `.TH libinput-list-devices "1" "" "libinput 1.32.0" "libinput Manual"`
   - Suite Manual: `/usr/share/man/man1/libinput.1.gz` (`libinput 1.32.0`)

---

## 2. What `libinput list-devices` CAN Say

Based on official libinput 1.32.0 documentation and the manual page, the output of `libinput list-devices` provides direct evidence for the following properties:

1. **Kernel Input Node Recognition:**
   - Identifies which kernel event device nodes (`/dev/input/event*`) are recognized and supported as input devices by libinput when opened in a fresh `seat0` context.
   - Quoted from `tools.rst`: *"The `libinput list-devices` command shows information about devices recognized by libinput and can help identifying why a device behaves different than expected. For example, if a device does not show up in the output, it is not a supported input device."*

2. **Hardware Capabilities & Classes:**
   - Reports the device capability classes detected by libinput: `keyboard`, `pointer`, `touch`, `tablet-tool`, `tablet-pad`, `gesture`, and `switch`.

3. **Physical Hardware Parameters & Identification:**
   - Reports device hardware metadata: human-readable device name, kernel event path, vendor and product bus IDs, device grouping (`Group`), logical seat assignment (`Seat: seat0, default`), and physical dimensions in millimeters when reported by hardware/udev (`Size: <width>x<height>mm`).

4. **Exposed Driver Configuration Interface:**
   - Lists which configuration features the device exposes to callers (`Tap-to-click`, `Tap drag lock`, `Left-handed`, `Nat.scrolling`, `Middle emulation`, `Calibration`, `Scroll methods`, `Click methods`).
   - Explicitly denotes unsupported or non-applicable configuration features with `n/a` (*"If an option is `n/a` it does not exist on this device"* — `tools.rst`).

5. **Built-in Library Default Configuration:**
   - Shows libinput's hardcoded or udev-quirk default settings for each exposed feature when no caller overrides exist.
   - For multi-state options, lists all supported candidate states with the built-in default prefixed by an asterisk (`*`) (*"the tool will show the default configuration for this device, for options that have more than a binary state all available options are listed, with the default one prefixed with an asterisk (`*`)"* — `tools.rst`).

---

## 3. What `libinput list-devices` CANNOT Say About Compositor Configuration

The official documentation and man page explicitly prohibit inferring compositor or desktop environment configuration from `libinput list-devices`:

1. **CANNOT Say What the Compositor's Effective Configuration Is:**
   - The tool does **not** query or reflect the active desktop environment or Wayland compositor's applied configuration.
   - **Verbatim Warning 1 (`tools.rst:49-50` / `tools.html`):**  
     `.. note:: This tool does **not** show your desktop's configuration, just the libinput built-in defaults.`
   - **Verbatim Warning 2 (`libinput-list-devices(1)` .SH NOTES):**  
     `An xorg.conf(5) configuration entry or Wayland compositor setting may have changed configurations on a device. The libinput list-devices tool only shows the device's default configuration, not the current configuration.`
   - **Verbatim Warning 3 (`libinput(1)` .SH DESCRIPTION):**  
     `These tools create libinput contexts separate from that of the compositor/X server and cannot change settings in a running session.`
   - **Mechanism:** `libinput list-devices` instantiates its own isolated `libinput_udev_create_context` directly against evdev nodes; it has no IPC channel to mutter, KWin, sway, or Hyprland, and cannot read compositor settings.

2. **CANNOT Say Whether the Compositor Handles the Device:**
   - Recognition by libinput does not imply the compositor actively listens to, handles, or maps the device to a seat or window.
   - **Verbatim Note (`libinput-list-devices(1)` .SH NOTES):**  
     `A device may be recognized by libinput but not handled by the X.Org libinput driver or the Wayland compositor.`

3. **CANNOT Say Whether the Compositor Even Uses libinput:**
   - Libinput is not mandatory for Wayland compositors.
   - Quoted from `what-is-libinput.html`: *"libinput is not a requirement for Wayland or even a Wayland compositor. There are some specialized compositors that do not need or want libinput."*

4. **CANNOT Say Whether Events Reach Wayland Clients (Application Delivery):**
   - Libinput operates strictly below the compositor. Clients never talk to libinput directly.
   - Quoted from `what-is-libinput.html`: *"libinput is not used directly by Wayland applications, it is an input stack used by the compositor... The Wayland client does not know whether libinput is in use."*
   - `list-devices` reports zero information about `wl_seat`, client surface focus, keyboard enter/leave semantics, or event dispatch.

5. **CANNOT Assert Absence of a Feature from Absence of a Configuration Knob:**
   - The lack of a configuration option does not imply the underlying feature does not work in hardware or software.
   - **Verbatim Note (`libinput-list-devices(1)` .SH NOTES):**  
     `In some cases a device may support a specific feature but does not expose configuration for it, e.g. when using the device without that particular feature does not make sense. A lack of a configuration option thus does not necessarily mean that this feature does not work.`

6. **CANNOT Be Used as a Stable Machine-Readable API:**
   - The output format is explicitly unversioned and human-facing only.
   - **Verbatim Warning (`tools.rst:86-87` / `tools.html`):**  
     `.. note:: This tool is intended for human-consumption and may change its output at any time.`

---

## 4. Synthesis with Lane Precedents & U6 Boundary Fences

1. **Re-affirming Discernment Lesson M04 (`corpus/lessons/round-12.md:37`):**
   - Lesson M04 recorded the claim *"libinput list-devices proves the compositor-applied keyboard/touchpad settings"* as an explicit inference trap (`[INF-docs]`).
   - Sibling boundary analysis (`.ufo/waves/round-13/w1/SiblingOverlap.md:68`) confirmed: *"Reflects kernel/libinput defaults, not Hyprland input.conf parsing."*
   - The official 1.32.0 documentation directly corroborates M04: any assumption that `list-devices` defaults represent the running desktop configuration is a category error.

2. **Decoupled Verification Planes for U6:**
   - **Library / Default Plane (libinput docs-era 1.32.0):** Documents hardware recognition, interface capability flags, and built-in defaults (`*two-finger`, `tap: disabled`).
   - **Compositor Effective Plane (Hyprland):** Must be queried via Hyprland's own IPC surfaces (`hyprctl getoption input:<key>` with its `set` flag, `hyprctl devices` for `active_keymap`), never inferred from `list-devices`.
   - **Client Delivery Plane (Wayland):** Governed by `wl_keyboard` / `wl_pointer` focus; completely decoupled from libinput's context.

---

## 5. Safe Boundary & Verification Gaps

- **Safe Boundary Enforced:**
  * No live probe or event tool was executed (`libinput list-devices`, `debug-events`, `record`, `replay`, `measure`, and `analyze` were NOT executed).
  * No raw `/dev/input/event*` nodes were opened or monitored.
  * No compositor state or configuration was mutated.
  * All findings are derived strictly from static read-only analysis of version-pinned documentation (`tools.rst` @ 1.32.0) and installed system manual pages (`libinput-tools 1.32.0-1`).

- **Verification Gaps / Remaining Unknowns:**
  * `[UNK]` Application event delivery: Whether input events successfully reach running client applications remains unmeasured.
  * `[UNK]` Host runtime library vs package version: On-disk package is `libinput 1.32.0-1` (installed mid-round at 04:25:17 AM -03), while running compositor process `/proc/1706/exe` still maps `/usr/lib/libinput.so.10.13.0 (deleted)` (1.31.3) until compositor restart.
  * `[UNK]` IME / Text-Input state: Virtual keyboard and input-method extensions (`text-input-v3`, `input-method-v2`) remain unexercised.
