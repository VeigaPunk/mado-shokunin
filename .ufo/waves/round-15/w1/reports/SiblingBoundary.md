# SiblingBoundary — Hardware/Kernel Diagnostics vs Desktop Policy (Round 15, w1)

**Seat:** `MadoR15.SiblingBoundary` (connector, leaf; no subagent dispatch, no background jobs, no commits/push).  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`.  
**Milestone:** U6 input evidence ladder and R14 ancillary provenance correction.  
**Declared Axis Judged On:** `coverage` (C1).  
**Companion Axes Evaluated:** `adjacency`, `calibration`, `operability`, `freshness`, `depth`.  
**Report Path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/SiblingBoundary.md`.  
**Status:** Complete findings and single bounded synthesis proposal. Read-only static inspection throughout; no tool installations or upgrades, no gate runs, no compositor mutations, no live input probes.

---

## 1. Naming the Axes

Per Godspeed posture and round-15 contract:

1. **Primary Judged Axis:**
   - **`coverage` (C1):** Advancing sourced U-item reachability from 5/7 ($7.1429/10$) to 6/7 ($8.5714/10$) under the lowest non-retired rubric by admitting Milestone U6 (`input-evidence-ladder-r15.md`), establishing a bounded input-debugging layer route with reciprocal mined source joins S051/S052 and the three required sections (`## Layer ladder`, `## Safe boundary`, `## Unexercised delivery`), without absorbing raw kernel event capture or unobserved application outcome delivery.

2. **Companion Unscored / Harm-Watched Axes:**
   - **`adjacency`:** Enforcing strict separation between `mado-shokunin` (desktop & compositor configuration plane, display/input policy), `tsukuroi-shokunin` (OS substrate, kernel modules, driver/firmware plane, device nodes, journal/boot triage), `mori-shokunin` (fleet & host observability, process life/death, resource runway), `kagi-shokunin` (credential hygiene, secret-bearing event stream fences), and `tameshi-shokunin` (reusable verification-fixture craft).
   - **`calibration`:** Eliminating false equivalences across the input stack. Specifically, distinguishing:
     1. libinput built-in driver defaults from compositor-applied desktop configuration (`round-12.md` M04);
     2. userspace Wayland protocol capability advertisement (`wl_seat.capabilities`) from bound client delivery;
     3. compositor key event dispatch from client/IME text commitment;
     4. static documentation route from live host input capture.
   - **`operability`:** Keeping `tools/mado-verify.sh` hermetic and unprivileged. The gate must never execute root-requiring, evdev-sniffing, or input-injecting commands (`libinput debug-events`, `evtest`, `evemu`, `ydotool`), preserving exact gate digests and selftest passes ($268/268$).
   - **`freshness` / `depth`:** Retaining explicit `[UNK]` for unexercised delivery/IME/kernel limits, and correcting R14-V1 ancillary receipt provenance without rewriting historical records.

---

## 2. Evidence from Round Cache and Local Repositories

All evidence was gathered through read-only inspection of lane and sibling province declarations, knowledge corpora, and round-15 wave artifacts:

### 2.1 Lane PROVINCE (`/home/vgpnk/Projects/shokunin/mado-shokunin/PROVINCE.md`)
- **Domain:** Desktop & compositor craft — the Hyprland/waybar/walker configuration plane and display behavior on this host.
- **Owns (Surfaces):** `~/.config/hypr/` (`hyprland.conf`, `input` sections, keybinds, rules, animations, monitors), `~/.config/waybar/`, `~/.config/walker/`, terminal emulator configs (`alacritty`, `foot`, `kitty`, `ghostty`), themes/wallpapers as declared files, screen/idle behavior (`hypridle`, `hyprlock`). Omarchy skill (`~/.agents/skills/omarchy/`) is read-only documentation.
- **Operating Fences:** All config trees are **READ-ONLY**: probe, measure, recommend — the operator applies changes.
- **Refusals:** Secrets in configs (shape-only, $\to$ `kagi`), model endpoints ($\to$ `kama`), model quality ($\to$ `kengaku`). **Never mutates a running compositor state**; every claim is file-byte- or screenshot-verified.
- **Rule:** *Out of province $\to$ report, never absorb.*
- **Round-15 Contract Invariance:** *"no input event reading/recording/replay/injection, compositor action or hardware/kernel diagnosis."*

### 2.2 Sibling Tsukuroi (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md`)
- **Domain:** Host operability & system repair (繕, mending) — OS substrate: package state, systemd user units & timers, journal/boot triage, driver/firmware plane (kernel modules, nvidia driver + GSP firmware presence, `nvidia-smi` shape), update-safety questions.
- **Owns (Hardware & Kernel Diagnostics):** Kernel modules, kernel input drivers (`evdev`, `usbhid`, `i2c_hid`, `psmouse`), `/dev/input/event*` character devices, udev rules (`/etc/udev/rules.d/`, `/usr/lib/udev/rules.d/`), boot/kernel logs (`dmesg`, `journalctl -k -b`).
- **Finding-to-Owner Handoff Row ADJ-03 (`PROVINCE.md:48`):**
  - *Trigger:* "Desktop rendering, bindings, menu or idle behavior needs configuration-level diagnosis"
  - *Tsukuroi Retains:* "User-manager/unit, package and driver health; an active unit does not prove the UI works"
  - *Next Analysis Recipient:* `mado` (`../mado-shokunin/PROVINCE.md:3-16`)
  - *Minimum Handoff Evidence:* "Observed UI symptom and time plus relevant OS probe/exit; identify configuration surface without copying its contents. Mado verifies file/screenshot behavior itself"

### 2.3 Sibling Mori (`/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md`)
- **Domain:** Fleet & host observability (森) — whether the fleet, its waves, and host are alive and progressing.
- **Owns:** Watchdog liveness, `.ufo/waves/*` settlement, kill/OOM catalog-ID records, signal-11 coredumps (`coredumpctl`).
- **Refuses:** OS package, systemd unit, driver/firmware and boot state ($\to$ `tsukuroi`); dispatch ($\to$ `kumitate`); UI/compositor state ($\to$ `mado`).
- **Adjacency Boundary:** Mori passively observes process crashes (such as Waybar or Hyprland crashing with signal 11 on input dispatch), but does not diagnose input configurations ($\to$ `mado`) or kernel input drivers ($\to$ `tsukuroi`).

### 2.4 Sibling Kagi (`/home/vgpnk/Projects/shokunin/kagi-shokunin/PROVINCE.md`)
- **Domain:** Secrets & vault operations — credential hygiene evidence.
- **Owns:** Secret detection, credential handling, token custody.
- **Refusal / Threat Boundary:** Input debugging tools (`libinput debug-events`, `libinput record`, `evtest`) capture raw scancodes and keycodes from `/dev/input/event*`. When a user or automated agent types credentials, sudo passwords, or API keys, capturing raw input event streams constitutes a severe **keystroke-logging credential leak**. Mado's explicit refusal to read raw input events is an essential privacy fence protecting Kagi's domain.

### 2.5 Sibling Tameshi (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md`)
- **Domain:** Verification-fixture craft — hermetic suites, mutation testing, fail-closed arms.
- **Refuses:** Product domain code; each lane owns its own gate.
- **Round-15 Interaction:** R14-V1 ancillary receipt precision (R14-V1 lesson correction) refines mutation receipt provenance headers in Mado without altering the frozen gate code or delegating gate ownership.

### 2.6 Lane Sourced Evidence and Historical Mistakes
- **/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:19-21:**
  - `S007` (queued): `libinput helper tools` — `https://wayland.freedesktop.org/libinput/doc/latest/tools.html`. Documented anchor: *"Most of the tools must be run as root to have access to the kernel’s `/dev/input/event*` device files."*
  - `S008` (queued): `The Wayland Protocol (DeVault)` — `https://wayland-book.com/introduction/high-level-design.html`. Documented anchor: *"the role of the Wayland compositor is to dispatch input events to the appropriate Wayland client"*.
  - `S009` (queued): `Wayland Architecture` — `https://wayland.freedesktop.org/architecture.html`. Step-by-step event path from kernel evdev to compositor display server to client buffer.
- **/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md:37:**
  - `M04`: *"libinput list-devices proves the compositor-applied keyboard/touchpad settings."* Corrected as a mistake: `[INF-docs]` libinput helper tools report built-in defaults, not desktop configuration.

---

## 3. Distinguishing Hardware/Kernel Input Diagnostics from Desktop Policy

Input events traverse a deep multi-layer stack from physical transducers to application text commits. The primary source of architectural confusion and domain bleed in input debugging is the conflation of **Kernel/Driver Hardware Health** with **Desktop Compositor Policy**.

| Dimension | Desktop Input Policy (`mado-shokunin` Owns) | Hardware & Kernel Input Diagnostics (`tsukuroi-shokunin` Owns) |
|---|---|---|
| **Architectural Layer** | Userspace Wayland Compositor (Hyprland 0.56.2), compositor seat manager, client protocol dispatch. | Linux Kernel (7.2.3-arch1-3), evdev input subsystem, kernel drivers, hardware buses (USB/I2C/Bluetooth). |
| **Concrete Substrates** | `~/.config/hypr/hyprland.conf` (`input` block: `kb_layout`, `kb_variant`, `kb_options`, `follow_mouse`, `sensitivity`), per-device overrides (`device:name { ... }`), keybind definitions (`bind = ...`). | `/dev/input/event*`, `/dev/input/by-id/*`, `/dev/input/mice`, `/sys/class/input/`, `/sys/module/hid_*/`, kernel dmesg, udev rules (`/usr/lib/udev/rules.d/90-libinput-model-quirks.hwdb`). |
| **Protocol & API Scope** | Wayland wire protocols: `wl_seat` (pointer, keyboard, touch capabilities), `wl_keyboard` (keymap via `xkbcommon`, enter/leave, key, modifiers), `wl_pointer` (motion, button, axis), `zwp_text_input_v3`. | Linux evdev ioctls: `EVIOCGNAME`, `EVIOCGBIT`, `EVIOCGABS`, `EVIOCGKEY`, HID report descriptors, kernel scancode-to-keycode translation tables. |
| **Read-Only Probes** | `hyprctl -j devices` (compositor's internal device registry and active configuration), `hyprctl getoption input:...`, `wayland-info` (sanitized `wl_seat` interface advertisement). | `evtest`, `evemu-record`, `libinput debug-events`, `libinput list-devices`, `udevadm info /dev/input/event*`, `journalctl -k -b` for input driver errors. |
| **Mutating Actions (Refused)** | Injecting synthetic events (`hyprctl dispatch sendshortcut`), modifying running config via `hyprctl keyword`, mutating device properties. | Replaying events (`evemu-play`, `libinput replay`), resetting USB buses, reloading kernel modules (`modprobe -r psmouse && modprobe psmouse`), altering udev attributes. |
| **Failure Modes Governed** | Syntax errors in `input` block, invalid keybind syntax, shadowed keybinds, unmapped modifier keys, invalid xkb options, focus-follows-mouse policy misconfigurations. | Unrecognized USB HID devices, missing kernel modules, broken touch digitizer calibration, USB bus EMI drops, hardware switch bounce, `/dev/input/event*` permission denials (`EACCES`). |
| **Security & Privacy Fence** | Operates unprivileged; reads static configuration and sanitized compositor metadata; zero credential exposure. | Privileged (requires `root` or `input` group); reads raw event streams; strictly fences raw keystroke data from leaving the host triage boundary ($\to$ `kagi`). |
| **Adjacency Trigger** | Receives ADJ-03 handoff from `tsukuroi` when input behavior issues trace to compositor configuration or keybind routing. | Receives handoff from `mado` (`MADO-TO-TSUKUROI-INPUT-01`) when input failures trace to missing device nodes, driver unbinds, or kernel evdev errors. |

### The Anti-Pattern: Implementation Absorption

**Implementation absorption** occurs when a lane crosses this inviolable fence:
1. **Mado absorbs Tsukuroi:** Mado attempts to verify whether a keyboard or mouse is working by running `libinput debug-events`, `evtest`, or scanning `/dev/input/event*`. This violates Mado's PROVINCE (Mado governs *desktop & compositor craft*, not OS driver/kernel health), violates leaf read-only safety, and introduces a root/privilege dependency.
2. **Mado absorbs Kagi's Threat Surface:** By attempting to record or inspect raw input events, Mado becomes a keystroke logger, capturing authentication credentials, passwords, and tokens.
3. **Mado equates Libinput Defaults with Compositor State:** Conflating `libinput list-devices` with Hyprland's active configuration (the M04 mistake). Libinput reports driver baseline defaults; Hyprland applies user overrides via its own seat abstraction.
4. **Mado equates Protocol Advertisement with Application Delivery:** Claiming that because `wl_seat` advertises keyboard capability, an application receives or commits text. Protocol advertisement is Layer 4; application/IME outcome is Layer 5 (`[UNK]`).
5. **Tsukuroi absorbs Mado:** Tsukuroi attempts to diagnose hotkey or window focus issues by analyzing kernel module options, when the issue is an unmapped dispatcher or shadowed bind in `hyprland.conf`.

---

## 4. Proposed Move: The Five-Tier Input Evidence Ladder & Reciprocal Handoff Protocol

As the UFO-FSD Connector, we propose a single, bounded synthesis move across the round's scout, reviewer, and connector proposals:

### 4.1 The Five-Tier Input Evidence Ladder

We partition all input evidence into five strictly bounded architectural tiers:

```
[ Tier 0: Physical Hardware & Firmware ]  <--- PHYSICAL / HOST SUBSTRATE
   - Key switches, optical sensors, capacitive touch digitizers, device firmware.
   - External to software analysis; unobservable except via hardware diagnostics.

[ Tier 1: Linux Kernel Substrate & evdev ]  <--- TSUKUROI OWNS (Mado Refuses)
   - Kernel drivers (usbhid, i2c_hid), /dev/input/event* character devices, udev rules.
   - Verified by tsukuroi via dmesg, lsmod, udevadm. Requires root/input privilege.
   - INVIOLABLE FENCE: Mado NEVER reads /dev/input/event* or runs evtest/evemu.

[ Tier 2: Low-Level Input Processing (libinput) ]  <--- DOCUMENTATION BOUNDARY (S007)
   - Userspace library converting evdev events to normalized pointer/touch/key events.
   - Debug tools (libinput debug-events, record) require root and act as keyloggers.
   - S007 serves as static documentation for input abstraction; Mado NEVER executes tools.
   - Libinput default properties != Compositor desktop configuration (M04 correction).

------------------------- THE INVIOLABLE PROVINCE FENCE -------------------------

[ Tier 3: Compositor Seat Management & Policy ]  <--- MADO OWNS (File-byte & hyprctl verified)
   - ~/.config/hypr/hyprland.conf (input block, kb_layout, sensitivity, follow_mouse).
   - Keybinding routing table (bind, bindm, submaps), device overrides (device:name).
   - Read-only unprivileged verification: hyprctl -j devices, hyprctl getoption input:*.
   - Proves compositor-internal model only; does NOT prove physical delivery to client.

[ Tier 4: Wayland Client Protocol Delivery ]  <--- MADO OWNS (Documentation / Protocol Specification)
   - wl_seat capabilities, wl_keyboard (keymap, enter, key), wl_pointer, zwp_text_input_v3.
   - Pinned protocol specifications (S005, S008, DeVault Wayland Book).
   - Sanitized global advertisement (wayland-info, globals.json).
   - FENCE: Interface advertisement != Bound client delivery != Rendered UI outcome.

[ Tier 5: Application / IME / Client Outcome ]  <--- UNEXERCISED DELIVERY [UNK]
   - Toolkit event dispatch (GTK/Qt/Electron event loops), Fcitx5/IBus text commit.
   - Retained as explicit [UNK] in Mado; requires application-specific observation.
```

### 4.2 The Reciprocal Handoff Contract: `MADO-TO-TSUKUROI-INPUT-01`

To establish a complete bidirectional handoff discipline with `tsukuroi-shokunin` (mirroring Tsukuroi's `ADJ-03`):

* **ID:** `MADO-TO-TSUKUROI-INPUT-01`
* **Finding / Boundary Trigger:** An input device (keyboard, mouse, touchpad) is declared in `~/.config/hypr/hyprland.conf` or requested by the operator, but does not appear in `hyprctl devices`, or fails to produce any compositor-level response despite valid configuration syntax and verified include graph precedence.
* **Mado Retains:** The verified configuration bytes (`hyprland.conf`, `device` blocks), `hyprctl devices` JSON output (showing device absence or disconnected state), and verification that compositor syntax is clean (`tools/mado-verify.sh` PASS).
* **Next Analysis Recipient:** `tsukuroi` (`../tsukuroi-shokunin/PROVINCE.md:8-15`).
* **Minimum Handoff Evidence Packet:**
  1. UTC capture timestamp.
  2. Missing or failing input device name/identifier (e.g. `AT Translated Set 2 keyboard` or `SynPS/2 Synaptics TouchPad`).
  3. Compositor version and display socket (`Hyprland 0.56.2`, `wayland-1`).
  4. Mado's verification proof: `tools/mado-verify.sh --no-live` PASS on configuration syntax and source resolution.
  5. Specific requested OS diagnosis: check kernel input module presence (`lsmod | grep -E 'hid|input'`), `/dev/input/event*` existence and permissions, udev device enumeration (`udevadm trigger --dry-run`), and kernel ring buffer (`journalctl -k -b`) for USB disconnect or HID protocol faults.
* **Forbidden Inference:** Mado never infers a hardware failure or kernel bug from a missing hotkey response; Tsukuroi never infers a configuration syntax defect from a healthy evdev node.

---

## 5. Trace of Second-Order Effects Across Surfaces

1. **Coverage Axis (C1):**
   - Enables clean admission of Milestone U6 (`input-evidence-ladder-r15.md`) by anchoring it firmly in **Tier 3** (Compositor Seat Policy) and **Tier 4** (Protocol Specification & Sanitized Advertisement), while explicitly referencing Tier 2 via static documentation (S007).
   - Satisfies the required U6 structure:
     * `## Layer ladder`: The five-tier breakdown above;
     * `## Safe boundary`: The strict refusal of root-requiring `/dev/input/` tools and the `MADO-TO-TSUKUROI-INPUT-01` handoff;
     * `## Unexercised delivery`: Explicit `[UNK]` for application/IME outcomes (Tier 5).
   - Advances sourced U-items from $5/7 \approx 7.1429/10$ to $6/7 \approx 8.5714/10$.

2. **Operability Axis:**
   - Protects `tools/mado-verify.sh` from acquiring dangerous, unprivileged-host-breaking checks. The gate remains strictly confined to configuration file-byte parsing, include graph resolution, and optional read-only `hyprctl` queries.
   - Prevents the introduction of fragile dependencies on `/dev/input/` character device permissions or evdev availability.

3. **Adjacency Axis:**
   - Formalizes the input boundary between Mado and Tsukuroi, closing the loop with Tsukuroi's `ADJ-03`.
   - Protects `kagi-shokunin`'s credential domain by establishing an inviolable architectural ban on raw event logging.

4. **Calibration Axis & R14-V1 Provenance Correction:**
   - Eliminates false equivalences (M04) by explicitly noting that libinput defaults do not equal compositor configuration.
   - Pairs seamlessly with `MistakeRecord`'s R14-V1 receipt correction: mutation testing receipts remain strictly ancillary provenance corrections without modifying the gate or adding generic execution wrappers.

---

## 6. Risks, Contradictions, and Verification

### 6.1 Risks and Contradiction Guards

1. **Risk of Apparent Under-Coverage:** A reviewer might ask: *"If Mado does not capture input events, how can it claim an input evidence ladder?"*
   - *Resolution:* Grounded in Mado's PROVINCE and Protocol standards: Mado governs *desktop configuration and compositor seat policy*. Mado provides the evidence ladder that maps where compositor authority begins (Tier 3) and where it ends (Tier 4 $\to$ Tier 5), documenting what is proved versus what remains `[UNK]`. Claiming to verify input by running a privileged keystroke logger violates the lane contract, security hygiene, and the PROVINCE refusal rules.
2. **Contradiction Guard (`hyprctl devices` vs `libinput list-devices`):**
   - Both list devices, but their semantics and authorities are completely distinct:
     * `libinput list-devices` reads directly from `/dev/input/event*` (requires root) and reports libinput driver defaults;
     * `hyprctl devices` queries Hyprland's IPC socket (unprivileged user) and reports the compositor's active internal device table and applied configuration.
   - Mado permits `hyprctl devices` (read-only unprivileged inspection) and rejects `libinput list-devices` as a live probe.

### 6.2 Verification Recipe for L1 Integration

1. Inspect `corpus/knowledge/input-evidence-ladder-r15.md` (U6 note) to ensure it incorporates the Five-Tier Input Ladder and explicitly marks Tier 0–2 as host/kernel diagnosis (`tsukuroi`) and Tier 5 as `[UNK]`.
2. Verify that `grep -nE '(libinput debug-events|libinput record|evtest|evemu|/dev/input)' tools/mado-verify.sh` returns zero occurrences in executable gate code.
3. Confirm that S051/S052 citations in `corpus/SOURCES.md` cite primary documentation (e.g. libinput tools documentation and Wayland protocol architecture) as static interface references without claiming live host event capture.

---

## 7. Tooling Record

Per Tooling Directive (operator, 2026-10-19):
- **Tools Installed / Updated:** None.
- All observations and analyses were conducted read-only on committed repository artifacts, sibling PROVINCE declarations, and existing system state.
