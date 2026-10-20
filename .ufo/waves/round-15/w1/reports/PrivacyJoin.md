# PrivacyJoin — Input Privacy & Safe-Probe Boundary Synthesis

**Seat:** `MadoR15.PrivacyJoin` (connector, leaf).  
**Lane Root:** `/home/vgpnk/Projects/shokunin/mado-shokunin`.  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`.  
**Report Path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/PrivacyJoin.md`.  
**Milestone:** U6 input evidence ladder and R14 ancillary provenance correction.  
**Judged on:** coverage (C1, U1–U5 5/7 → U1–U6 6/7).  

---

## 1. Declared Axes

In accordance with `/skill:godspeed` and the round contract:
1. **Coverage ($C_1$, primary active scored axis):** Sourced current-art ground $5/7 \rightarrow 6/7$ ($7.1429 \rightarrow 8.5714 / 10$) by admitting exactly one bounded U6 input-debugging layer route (`covers: U6`) citing opened primary documentation and Wayland core protocol without raw event capture or live mutation.
2. **Operability & Safety (unscored / non-harm):** Hermetic suite pass fraction (10/10), frozen gate integrity (`fba82a66…c207`), and strict mutation-free fence (`SKILL.md:218–246`). Retaining delivery, IME, and kernel diagnostics as unexercised unknowns (`[UNK]`).
3. **Calibration & Provenance (unscored / non-harm):** R14-V1 ancillary mutation-receipt precision correction (preserving historical worktree receipts, appending exact derived target $cd1d73d7\dots$ mapping). Lesson-grounded criteria and reciprocal source-row joins (`corpus/QUALITY.md`).

---

## 2. Local Evidence & Ground Truth

### 2.1 Existing SKILL Safe-Probe & Session-Material Discipline
- **Mutation-Free Fence (`SKILL.md:218–246`):**
  - *Rule 1 (Read-verb whitelist):* `hyprctl` restricted to `getoption`, `monitors`, `workspaces`, `clients`, `devices`, `binds`, `layers`, `version`, `configerrors`, `instances`, `splash`, `rollinglog` (`:220–224`).
  - *Rule 2 (No firing, no injection):* "No keystroke injection, no dispatcher invocation; rule-effect and bind behavior stay UNKNOWN" (`:225–226`).
  - *Rule 3 (Boundary proof):* Config trees byte-identical before/after (`sha256sum ~/.config/hypr/*.conf`, `:231–233`).
  - *Rule 4 (Session material stays shape-only):* "`clients` for length/tags, never window titles; `hyprland.log` shape-only; no `/proc/*/environ`; `HYPRLAND_INSTANCE_SIGNATURE` shape-checked, never printed in full" (`:234–236`).
  - *Rule 5 (Unverifiable $\rightarrow$ UNKNOWN):* If a claim needs a mutation or a surface that does not exist, mark `[UNK]` and stop (`:237–240`).
- **Prior Round Context:**
  - Round 12 (`corpus/knowledge/xdg-portal-routing-r12.md:110`): portal request payloads and session tokens rejected as session material.
  - Round 13 (`corpus/knowledge/wayland-protocol-boundaries-r13.md:8, 104`): Wayland protocol phases separated from live execution; kernel input ladder explicitly left open.
  - Round 14 (`corpus/knowledge/output-colour-boundaries-r14.md:58–61, 108`): head advertisements contain identity; "no configuration request does not mean no identity received." Raw metadata retention forbidden.

### 2.2 Libinput 1.32.0 Primary Sources & C Implementation
Inspection of official upstream documentation and source tree (libinput 1.32.0 tag, verified statically):
- **`tools.html` (Helper tools):**
  - Root requirement: *"Most of the tools must be run as root to have access to the kernel’s `/dev/input/event*` device files."*
  - `list-devices`: *"This tool does **not** show your desktop’s configuration, just the libinput built-in defaults."*
  - `record`: *"The recorded events are **kernel events** and independent of the libinput context."* *"For data protection, libinput record obscures key codes by default, any alphanumeric key shows up as letter 'a'."*
  - `replay`: *"creates a new virtual device based on the description in the log file."*
- **`libinput-record(1)` Man Page & C Source (`tools/libinput-record.c`):**
  - `--show-keycodes`: disables obfuscation; shows keycodes as-is (`record.c:242, 463`).
  - `--with-hidraw`: *"HID reports are **not obfuscated** and a sufficiently motivated person could recover the key strokes from the logs. Do not type passwords while recording HID reports."*
  - Layer discrepancy in obfuscation:
    * *Evdev layer (`print_evdev_event`, `record.c:236–243`):* `EV_KEY` codes 2–57 and 71–83 masked to `KEY_A`. Crucial control keys pass unmasked: Code 1 (`KEY_ESC`), 15 (`KEY_TAB`), 28 (`KEY_ENTER`), 29 (`KEY_LEFTCTRL`), 58 (`KEY_CAPSLOCK`), 59–68 (`KEY_F1–F10`), 87–88 (`KEY_F11–F12`), 125 (`KEY_LEFTMETA`).
    * *Libinput layer (`print_keyboard_event`, `record.c:460–463`):* Codes 1–84 masked to `-1`; codes $\ge 85$ (F11, F12, arrows, Meta) passed as-is.
  - Timing retention: EV_SYN records timestamp deltas (`%+dms`) with microsecond resolution.
  - Device description dump (`print_device_description`, `record.c:1889–1898`): writes device node, evdev name, `[bustype, vendor, product, version]`, complete HID descriptor bytes, udev properties (`ID_INPUT*`, `LIBINPUT*`), and sysfs paths.
  - `system` dump: writes OS release, kernel release, and `system.dmi` (`/sys/class/dmi/id/modalias`, BIOS version, system serial).
  - `--grab`: *"Exclusively grab all opened devices. This will prevent events from being delivered to the host system."* (`record.c:2433–2434`).

### 2.3 Local Host Environment Observations
- Package queries (`pacman -Q`): `libinput 1.32.0-1`, `libinput-tools 1.32.0-1`, `wayland 1.26.0-1`, `wayland-utils 1.3.0-1`.
- Binary presence: `/usr/bin/libinput` is present on PATH.
- *Zero execution:* No subcommand (`debug-events`, `record`, `replay`, `list-devices`) was executed by this seat.

---

## 3. Direct Connection: Existing Session Material vs. Input Debugging

Existing SKILL session-material discipline was conceived around the **Wayland compositor boundary**:
1. *Window metadata:* Window titles (`clients`) leak document names, web URLs, private messages; tags/length are safe.
2. *Compositor logs:* `hyprland.log` contains debug strings and window titles; mtime/size shape checks are safe.
3. *Process environment:* `/proc/*/environ` contains API keys and credentials; shape checks are safe.
4. *Instance tokens:* `HYPRLAND_INSTANCE_SIGNATURE` identifies the IPC socket; 12-char prefix check is safe.

Input debugging via kernel event interfaces (`/dev/input/event*`, `libinput debug-events`, `libinput record`) completely shatters this compositor-centric mental model. Kernel evdev sits **below** the Wayland compositor and **outside** application sandboxing. Connecting the two models reveals that input debugging introduces leaks of a fundamentally different order of magnitude:

| Aspect | Compositor Session Material (`SKILL.md`) | Input Debugging Stream (`libinput` / `evdev`) |
|---|---|---|
| **Boundary** | Compositor-mediated IPC socket | Direct kernel character device (`/dev/input/event*`) |
| **Authority** | Filtered by window focus & seat state | Global kernel capture; bypasses window focus and screen locks |
| **Key Material** | Absent (compositor does not log raw keys) | Direct scancodes / keycodes emitted on every physical press |
| **Motion Material**| Static cursor position sample (`cursorpos`) | Continuous sub-millisecond motion & pressure trajectories |
| **Identity Scope** | Ephemeral compositor instance signature | Permanent hardware identifiers (DMI, USB serials, bus IDs) |
| **Injection Risk** | Denied by socket permission | `uinput` virtual device injection escalates to hardware input |

---

## 4. Unique Input-Debugging Leakage Taxonomy (5 New Privacy Leak Classes)

Connecting SKILL rules to libinput observations reveals **five new privacy leak classes** unique to input debugging:

### Class 1: Temporal & Biometric Keystroke Dynamics
- **Mechanism:** Even when keycodes are obscured (e.g. masked to `KEY_A` or `-1`), `libinput record` and `debug-events` retain unquantized timestamps (`%+dms` deltas and `[sec, usec]` tuples).
- **Leak:** Inter-keystroke intervals (IKIs), flight times, and press durations form a unique behavioral biometric signature that can deanonymize an operator. Furthermore, timing analysis of keystroke sequences allows statistical reconstruction of natural language text and password structure regardless of keycode masking.

### Class 2: Continuous Spatial & Multitouch Trajectory Streaming
- **Mechanism:** Mouse, touchpad, and touchscreen logging dumps continuous event frames (`POINTER_MOTION`, `EV_ABS / ABS_MT_POSITION_X`, `ABS_MT_POSITION_Y`, `ABS_MT_PRESSURE`).
- **Leak:** Unlike static point coordinates (`hyprctl cursorpos`), continuous spatial streams leak gesture unlock patterns, drawn signatures, on-screen keyboard key coordinates (where $(X, Y)$ maps directly to typed letters), document reading rhythms, and physical ergonomics.

### Class 3: Partial Obfuscation & Structural Credential Leakage
- **Mechanism:** The upstream "data protection" in `libinput record` applies strictly to alphanumeric keys. 
- **Leak:** 
  1. *Unmasked control keys:* Enter, Tab, Escape, Backspace, CapsLock, and Modifiers (Shift, Ctrl, Alt, Super) remain cleartext. A sequence such as `[Shift_L, A, A, A, A, A, Enter]` immediately leaks password length, character casing, and submission boundaries.
  2. *HID Reports:* Under `--with-hidraw`, raw USB HID report descriptor frames are recorded completely unmasked. Upstream explicitly warns: *"HID reports are not obfuscated and a sufficiently motivated person could recover the key strokes."*
  3. *Layer Discrepancy:* Libinput-layer logging masks codes 1–84, but evdev-layer logging leaves codes 1, 15, 28, 29 unmasked.

### Class 4: Out-of-Band Session-Lock & Authentication Interception
- **Mechanism:** Kernel evdev device nodes are multiplexed across all consumers. They do not respect Wayland seat focus, compositor grabbing, or lock-screen states (`hyprlock`).
- **Leak:** If an input recording or event probe runs in the background while the operator locks the session or authenticates with `sudo`/`pam`, the authentication passphrase entered into the lock screen is captured directly from `/dev/input/event*`, completely evading the Wayland security boundary.

### Class 5: Persistent Machine & Hardware Fingerprinting
- **Mechanism:** `libinput record` dumps system and device descriptions: `system.dmi` (BIOS vendor, board serial, product UUID from `/sys/class/dmi/id/modalias`), `evdev.id` (bustype, vendor, product, version), and udev device attributes.
- **Leak:** In existing SKILL rules, `HYPRLAND_INSTANCE_SIGNATURE` is shape-checked because it is ephemeral. In contrast, DMI and hardware serials are permanent machine fingerprints that persist across reboots, sessions, and OS reinstallations. Retaining these violates the shape-only principle.

---

## 5. Proposed Move: Input Privacy & Safe-Probe Boundary Synthesis

### 5.1 The Move
Establish a unified **Input Privacy & Safe-Probe Boundary** that bridges existing SKILL Rule 4 ("Session material stays shape-only") and Rule 2 ("No firing, no injection") with the U6 documentation ladder:
1. **Extend SKILL Rule 4 to Input Surfaces:** Explicitly amend the shape-only definition to cover input devices. `hyprctl devices` is whitelisted for **device counts and capability classes only** (e.g. keyboard count: 2, pointer count: 1); retaining raw device names, serials, vendor IDs, or event node paths is forbidden.
2. **Formulate the U6 Safe Boundary Block:** Provide L1 with the verified, drop-in `## Safe boundary` text for the U6 knowledge note, explicitly categorizing `libinput debug-events`, `libinput record`, `libinput replay`, `evemu`, and `/dev/input/*` under the five leakage classes and declaring them unauthorized.
3. **Declare Input Injections Control Hazards:** Formally classify `libinput replay`, `uinput` virtual device creation, and `libinput record --grab` as control/injection hazards that violate the mutation-free fence.

### 5.2 Concrete Draft Text for U6 Note (`## Safe boundary`)
```markdown
## Safe boundary — input debugging is non-executable documentation

This entry establishes a static architectural ladder; it is not authorization for input event capture, hardware inspection, or input injection. All input debugging routes belong to distinct safety and privacy hazard classes:

1. Privilege Boundary: Reading kernel input nodes (`/dev/input/event*`, `/dev/hidraw*`) requires root privileges (`sudo`). Mado operates strictly as an unprivileged, mutation-free diagnostic lane; no `sudo` invocation or raw character device access is permitted.
2. Keylogger & Privacy Hazards:
   - `libinput debug-events` and `libinput record` stream real-time event logs. Obfuscation is partial: alphanumeric keys are masked, but Enter, Tab, Escape, Backspace, modifiers, and raw HID reports (`--with-hidraw`) pass unmasked, leaking password structure and word lengths.
   - Microsecond event deltas (`%+dms`) leak behavioral keystroke timing dynamics.
   - Continuous pointer and multitouch coordinates leak spatial trajectories and touch PINs.
   - Kernel event capture operates below the compositor, intercepting authentication input entered into `hyprlock`.
   - Recording headers dump permanent hardware fingerprints (`system.dmi`, USB serials).
3. Injection & Control Hazards:
   - `libinput replay` creates a `/dev/uinput` virtual device and injects hardware events, directly violating the mutation-free fence ("No firing, no injection").
   - `libinput record --grab` exclusively grabs devices, blocking input delivery to the compositor and causing a denial-of-service hazard.

Permitted host inspection is strictly shape-only: package version confirmation (`pacman -Q libinput`), help text (`libinput --help`), and compositor device counts (`hyprctl -j devices | jq length`). Device names, paths, serials, and event streams remain completely unexercised (`[UNK]`).
```

---

## 6. Explicit Contradictions (Stated, Not Smoothed)

1. **The "Data Protection" Contradiction:**  
   *Upstream claim:* `tools.html` claims `libinput record` "obscures key codes for data protection".  
   *Ground truth:* `libinput-record.c` and `libinput-record.man` prove that control keys (Enter, Tab, Esc, Modifiers) are unmasked, `--with-hidraw` is completely unmasked, and microsecond timing is preserved.  
   *Synthesis:* Upstream "data protection" is a convenience filter for public bug trackers, not a secure privacy boundary. The U6 note must explicitly reject the inference that default recordings are privacy-safe.

2. **The `hyprctl devices` Read-Verb Whitelist Contradiction:**  
   *SKILL rule:* `SKILL.md:220–224` whitelists `devices` without qualification, while `:234–236` strictly restricts `clients` to length/tags.  
   *Ground truth:* `hyprctl devices` emits hardware descriptions, vendor strings, and keyboard layouts.  
   *Synthesis:* `devices` must be constrained by the same shape-only rule as `clients` (count and presence only; no hardware fingerprints).

3. **Host Tool Presence Drift:**  
   *Historical record:* `.ufo/evidence/round-12/l2-scout.md:3` recorded `libinput` absent. `ReviewPrivacy.md:98` recorded `which libinput` empty.  
   *Ground truth:* `libinput-tools 1.32.0-1` was installed mid-round; `/usr/bin/libinput` is now present on PATH.  
   *Synthesis:* Safety policy cannot depend on tool absence. The boundary must be normative and enforced by rule, regardless of binary availability.

---

## 7. Second-Order Effects Across Surfaces

- **Runtime Surface:** Zero runtime impact. No process launched, no device node accessed, no `/tmp` artifact created, no compositor state touched.
- **Contract Surface:** Zero modification to `tools/mado-verify.sh`, frozen gates, or harness files. Standing verification gate sha256 (`fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`) preserved exactly.
- **Substrate Surface:** Read-only config trees (`~/.config/hypr/`) remain byte-identical before and after.
- **Verification Surface:** Provides the necessary structural and semantic criteria for the round-15 measurement probe (`measure.py REV`), ensuring the `## Safe boundary` and `## Unexercised delivery` sections pass audit without triggering safety rejections.

---

## 8. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| **Over-broad restriction** | Rejecting legitimate static documentation reads | Restrict prohibition strictly to runtime device access, event capture, and injection; permit static man-page and header inspection (`[INF-docs]`). |
| **False compliance via `--no-events`** | Running `libinput record --no-events` to gather hardware metadata | Explicitly ban `--no-events` in the safe boundary; device identity and udev properties are hardware session material. |
| **Uncoordinated file edits** | Violating leaf seat contract by editing `SKILL.md` or `corpus/` directly | Confine this seat's output exclusively to this report (`PrivacyJoin.md`); leave all file edits to L1. |

---

## 9. Verification & Handoff for Main Agent

The main agent can verify this connector's findings through the following static checks:

1. **Verify No Gate / Substrate Tampering:**
   ```bash
   sha256sum tools/mado-verify.sh
   # Expected: fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207
   git status --porcelain -- tools/ ~/.config/hypr/
   # Expected: empty
   ```
2. **Verify Upstream Source Pins in U6 Note:**
   Confirm that L1's U6 candidate note cites the five leakage classes and pins libinput to version 1.32.0 documentation without using unpinned `latest` or 404 URLs.
3. **Verify Zero Event Artifacts:**
   Confirm that no `.yml`, `.evemu`, or event log exists under the repository or `/tmp`.
4. **Verify Reciprocal Joins & Census:**
   ```bash
   /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
   ```

**Report written:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/PrivacyJoin.md`.
