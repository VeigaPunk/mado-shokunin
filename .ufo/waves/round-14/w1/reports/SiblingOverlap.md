# SiblingOverlap — Compositor Display Policy vs DRM/KMS/Kernel Diagnosis (Round 14, w1)

**Seat:** `MadoR14.SiblingOverlap` (connector, leaf; no subagent dispatch, no background jobs, no commits/push).  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`.  
**Milestone:** U5 boundaries and regular-source targets.  
**Declared Axes Judged On:** `coverage` (C1), `operability` (C2).  
**Companion Axes Evaluated:** `adjacency`, `calibration`, `freshness`, `depth`.  
**Status:** Complete findings and synthesis proposal. Read-only observation throughout; no tool installations, no gate runs, no compositor mutations.

---

## 1. Naming the Axes

Per Godspeed posture and round-14 contract:
1. **Primary Judged Axes:**
   - **coverage (C1):** Advancing sourced U-item joins from 4/7 ($5.7143/10$) to 5/7 ($7.1429/10$) by admitting Milestone U5 (`output-colour-boundaries-r14.md`) covering `wlr-output-management` (S047) and `color-management-v1` (S048) with reciprocal `mined` joins, without unobserved feature exercise or cross-domain bleed.
   - **operability (C2):** Hardening `tools/mado-verify.sh`'s source resolver to reject direct directory-shaped targets and globs with directory matches via regular-file checks following file symlinks, with stable owning-row diagnostics (`nonregular:` / `non-regular:`), achieving $0/3 \to 3/3$ across isolated directory fixtures while preserving exact set and source-order behaviors.
2. **Companion Unscored / Harm-Watched Axes:**
   - **adjacency:** Preserving the strict separation between `mado-shokunin` (desktop & compositor craft), `tsukuroi-shokunin` (OS substrate, drivers, kernel/boot health), `mori-shokunin` (fleet observability), `tameshi-shokunin` (verification fixtures), and `kagi-shokunin` (secrets). No implementation absorption.
   - **calibration:** Eliminating overbroad claims; enforcing that Wayland protocol advertisement is never equated with hardware display capability or verified colorimetric rendering; applying verifier corrections R13-V1, R13-V2, and R13-V3.
   - **freshness:** Respecting single-run configuration boundary hashes (`gate-file-plane.txt`) without conflating them with cross-revision output equality.
   - **depth:** Retaining explicit unknown boundaries (`[UNK]`) for runtime display reconfiguration, HDR pipeline tone-mapping, and hardware LUT states.

---

## 2. Evidence from Round Cache and Local Repositories

All evidence was gathered through read-only inspection of lane and sibling province declarations, knowledge corpora, and round-14 wave artifacts:

### 2.1 Lane PROVINCE (`mado-shokunin/PROVINCE.md`)
- **Domain:** Desktop & compositor craft — the Hyprland/waybar/walker configuration plane and display behavior on this host.
- **Owned Surfaces:** `~/.config/hypr/` (`hyprland.conf`, `monitors.conf`, `bindings.conf`, `rules`, animations), `~/.config/waybar/`, `~/.config/walker/`, terminal emulator configs (`alacritty`, `foot`, `kitty`, `ghostty`), themes/wallpapers as declared files, screen/idle behavior (`hypridle`, `hyprlock`). Omarchy skill is read-only documentation.
- **Operating Fences:** All config trees are **READ-ONLY**: probe, measure, recommend — the operator applies changes.
- **Refusals:** Secrets in configs (shape-only, $\to$ `kagi`), model endpoints ($\to$ `kama`), model quality ($\to$ `kengaku`). **Never mutates a running compositor state**; every claim is file-byte- or screenshot-verified.
- **Rule:** *Out of province $\to$ report, never absorb.*

### 2.2 Sibling Tsukuroi (`tsukuroi-shokunin/PROVINCE.md`)
- **Domain:** Host operability & system repair (繕, mending) — OS substrate: package state, systemd user units & timers, journal/boot triage, driver/firmware plane (kernel modules, nvidia driver + GSP firmware presence, `nvidia-smi` shape), update-safety questions.
- **Finding-to-Owner Handoff Row ADJ-03:**
  - *Trigger:* "Desktop rendering, bindings, menu or idle behavior needs configuration-level diagnosis"
  - *Tsukuroi Retains:* "User-manager/unit, package and driver health; an active unit does not prove the UI works"
  - *Next Recipient:* `mado` (`../mado-shokunin/PROVINCE.md:3-16`)
  - *Minimum Evidence:* "Observed UI symptom and time plus relevant OS probe/exit; identify configuration surface without copying its contents. Mado verifies file/screenshot behavior itself"
  - *Counterexample:* "A failed user unit without a configuration or UI question remains OS diagnosis."
  - *Forbidden Inference:* "An active user unit proves that the visible UI works."
- **Host Driver/Firmware Evidence (`tsukuroi-shokunin/corpus/knowledge/driver-firmware-plane.md`):**
  - Kernel `7.2.3-arch1-3`, `nvidia-open-dkms 610.57.04-1`, `nvidia-utils 610.57.04-1`, `libva-nvidia-driver 0.0.18-1`.
  - Loaded modules: `nvidia` (18 MB), `nvidia_uvm`, `nvidia_modeset`, `nvidia_drm` (167 KB, minor 1), `drm_ttm_helper`.
  - Hardware: NVIDIA GeForce RTX 5070, GSP firmware active (`EnableGpuFirmware: 18`). SecureBoot off (unsigned DKMS module).
  - Tsukuroi owns diagnosing whether `nvidia_drm` is loaded, whether DKMS built modules match the running kernel, and whether `journalctl -k` logs DRM modeset or GPU Xid faults.

### 2.3 Adjacent Sibling Provinces
- **`mori-shokunin`:** Fleet & host observability (watchdog liveness, cgroup `memory.events`, journal coredump/SIGKILL notices, resource runway). Refuses OS state ($\to$ `tsukuroi`) and UI/compositor state ($\to$ `mado`).
- **`tameshi-shokunin`:** Verification-fixture craft (mutation testing, hermetic suites). Refuses product domain ownership or editing sibling gates.
- **`kaidoku-shokunin`:** Reverse engineering shipped artifacts (Ghidra, REA). Refuses live host state ($\to$ `tsukuroi`).
- **`kama-shokunin`:** Local model serving endpoints. Refuses config writes and driver state.
- **`kagi-shokunin`:** Secrets & vault operations. Refuses non-secret configuration parsing.

### 2.4 Pre-Existing Boundaries and Tension in Mado
- In `hyprland-config-plane.md:237-238` and `hyprctl-verification-layer.md:193-195`, Mado observed that `~/.config/hypr/envs.conf` declared three NVIDIA variables (`NVD_BACKEND,direct`, `LIBVA_DRIVER_NAME,nvidia`, `__GLX_VENDOR_LIBRARY_NAME,nvidia`), but the file was unsourced and the variables unset in the live session. Mado documented: *"Whether the NVIDIA-driver vars in the orphan file matter on this host's GPU stays UNKNOWN."*
- In `globals.json` (S041, `ced47240…`), Hyprland 0.56.2 advertises `zwlr_output_manager_v1@4` and `wp_color_manager_v1@3`. The sanitization filter explicitly excluded `wl_output` geometry/modes, EDID, colorimetry blocks, and DRM lease device paths (`lines 332-343`).

---

## 3. Distinguishing Compositor Display Policy from DRM/KMS/Kernel Diagnosis

Milestone U5 introduces output management and color boundaries to Mado. Because outputs physically connect to GPU display engines, there is an acute danger of **domain bleed and implementation absorption**:
- Either Mado attempts to verify whether display reconfiguration or HDR "actually works" by probing DRM sysfs nodes, checking DKMS status, running `nvidia-smi`, or reading kernel ring buffers;
- Or Mado mistakes userspace Wayland protocol advertisements for proven hardware display pipeline activation.

To eliminate this ambiguity, we establish an explicit architectural distinction:

| Dimension | Compositor Display Policy (`mado-shokunin` Owns) | DRM/KMS/Kernel Diagnosis (`tsukuroi-shokunin` Owns) |
|---|---|---|
| **Architectural Layer** | Userspace Wayland Compositor (Hyprland 0.56.2), Wayland client protocols, user configuration files. | Linux Kernel (7.2.3-arch1-3), Direct Rendering Manager (DRM), Kernel Mode Setting (KMS), kernel modules, GPU firmware. |
| **Concrete Substrates** | `~/.config/hypr/monitors.conf`, `hyprland.conf` include graph, workspace rules (`workspace = 1, monitor:DP-1`), layer-surface rules (`waybar`, `swaybg`), `hypridle.conf` DPMS timeout declarations. | `/dev/dri/card*`, `/dev/dri/renderD*`, `/sys/class/drm/card*-*`, `/sys/module/nvidia_drm/parameters/modeset`, `/lib/modules/$(uname -r)/updates/dkms/nvidia.ko.zst`, `/lib/firmware/nvidia/`. |
| **Protocol & API Scope** | Wayland wire protocols: `zwlr_output_manager_v1` (v4), `zxdg_output_manager_v1` (v3), `wp_color_manager_v1` (v3), `zwlr_gamma_control_manager_v1` (v1), `zwlr_output_power_manager_v1` (v1), `hyprland_ctm_control_manager_v1` (v2). | Kernel ioctls: `DRM_IOCTL_MODE_GETCONNECTOR`, `DRM_IOCTL_MODE_GETCRTC`, `DRM_IOCTL_MODE_ATOMIC_COMMIT`, DRM plane color LUT properties (DEGAMMA_LUT, CTM, GAMMA_LUT), EDID I2C DDC transfers. |
| **Read-Only Probes** | `hyprctl -j monitors` (compositor's internal model of active outputs, positions, modes, scales, transforms); `wayland-info` (sanitized advertisement of global interfaces). | `lsmod \| grep nvidia`, `modinfo nvidia_drm`, `dkms status`, `nvidia-smi --query-gpu=...`, `journalctl -k -b` for DRM modesetting logs or GPU Xid errors. |
| **Mutating Actions (Refused)** | Mutating running compositor state: `hyprctl dispatch dpms`, `hyprctl keyword monitor ...`, sending `zwlr_output_configuration_v1.apply`. | Modifying kernel parameters, restarting display managers (`sddm`), recompiling DKMS modules, resetting GPU (`nvidia-smi -r`). |
| **Failure Modes Governed** | Syntax errors in `monitors.conf`, missing includes in `hyprland.conf`, out-of-order source lines, non-regular source targets, unmapped workspaces, layer surface margin overlap. | Kernel DRM atomic commit failures (`EINVAL`/`EBUSY`), link training failure on DisplayPort, EDID checksum corruption, DKMS module mismatch on kernel update, GSP firmware crash. |
| **Adjacency Trigger** | Receives ADJ-03 handoff from tsukuroi when UI/display configuration diagnosis is required. | Receives handoff from mado when a display symptom traces to kernel driver or hardware modesetting failures. |

### The Anti-Pattern: Implementation Absorption
**Implementation absorption** would occur if:
1. **Mado absorbs Tsukuroi:** Mado adds checks to `tools/mado-verify.sh` for kernel driver presence (`nvidia-drm`), KMS modesetting parameters, DKMS module existence, GPU temperature/power via `nvidia-smi`, or parses kernel ring buffer lines for DRM errors. This violates Mado's PROVINCE: Mado governs *desktop & compositor craft*, not OS driver/kernel health.
2. **Tsukuroi absorbs Mado:** Tsukuroi parses `~/.config/hypr/monitors.conf` or evaluates Wayland protocol XMLs to decide whether the GPU is healthy, ignoring ADJ-03.
3. **Mado absorbs Runtime Execution:** Mado sends `zwlr_output_configuration_v1.test` or `apply` requests via Wayland clients to verify output reconfiguration, violating the prohibition against mutating running compositor state.
4. **False Equivalence:** Mado claims that because `wp_color_manager_v1@3` is advertised, the display is operating in HDR mode or wide color gamut. Advertisement proves only interface presence in userspace dispatch tables; it does not prove DRM connector capabilities, display EDID HDR metadata support, or hardware pipeline tone-mapping.

---

## 4. Proposed Move: The Four-Tier Display Substrate Partition & Reciprocal Handoff Contract

As the UFO-FSD Connector, we propose a single, non-obvious move that synthesizes round-14's findings across `OutputHost`, `EvidenceChain`, `ReviewSourceBar`, `ScribeFrontier`, and `ReviewResolver`:

### The Four-Tier Display Partition Matrix

We partition all display and color evidence into four strictly bounded tiers:

```
[ Tier 1: Declared Compositor Configuration ]  <--- MADO OWNS (File-byte verified)
   - ~/.config/hypr/monitors.conf, hyprland.conf include graph, workspace rules.
   - Verified by tools/mado-verify.sh (regular-file check, include order).

[ Tier 2: Wayland Protocol Specification & Registry Advertisement ]  <--- MADO OWNS (Documentation boundary)
   - Pinned XMLs: S047 wlr-output-management v4 @ a741f0a / cdd2c7e; S048 color-management-v1 v3 @ tag 1.49.
   - Sanitized capture: globals.json (S041).
   - Documented two-phase commit: test validates, apply commits; dynamic capability negotiation enums.
   - INVIOLABLE FENCE: Advertisement != Client feature execution != Hardware capability.

[ Tier 3: Compositor Runtime Point-Observation ]  <--- MADO OWNS (Passive query only)
   - hyprctl -j monitors (compositor's current viewport model, scales, active workspaces).
   - Read-only; zero mutations. Does NOT prove hardware DRM pipe or physical pixel output.

------------------------- THE INVIOLABLE PROVINCE FENCE -------------------------

[ Tier 4: DRM / KMS / Kernel Substrate & Hardware Diagnostics ]  <--- TSUKUROI OWNS (Mado refuses & hands off)
   - Kernel modules (nvidia_drm, nvidia_modeset), DKMS builds, /sys/module/nvidia_drm/parameters/modeset.
   - DRM character devices (/dev/dri/card*), connectors, CRTCs, planes, hardware EDID, link training.
   - GPU firmware (GSP blobs), PCIe link state, nvidia-smi telemetry, kernel journal modeset errors.
```

### The Reciprocal Handoff Contract: MADO-TO-TSUKUROI-DISP-01

To ensure six-month maintainability and reciprocal adherence to Tsukuroi's `ADJ-03`, we formalize the reciprocal handoff:

* **ID:** `MADO-TO-TSUKUROI-DISP-01`
* **Trigger:** A reported display anomaly (black screen, mode setting failure, DPMS wake failure, GPU hang, or color corruption) is determined to have valid, loadable configuration files in `~/.config/hypr/` and valid compositor include precedence.
* **Mado Retains:** The verified configuration bytes (`monitors.conf`, `hyprland.conf`), include graph order, source resolver regular-file status, and read-only `hyprctl monitors` observation (if available).
* **Next Analysis Recipient:** `tsukuroi` (`../tsukuroi-shokunin/PROVINCE.md:6-14`).
* **Minimum Handoff Packet:**
  1. UTC observation time.
  2. Observed display symptom (e.g., monitor DP-1 dark, resolution fallback, or session coredump).
  3. Compositor version and display socket (`Hyprland 0.56.2`, `wayland-1`).
  4. Mado's verification proof: `tools/mado-verify.sh --no-live` PASS on `hypr.root.include_graph` and `hypr.root.sources_resolve`.
  5. Specific requested OS diagnosis: check `nvidia_drm` loading, DKMS build alignment (`dkms status`), `journalctl -k` for DRM modeset errors or GPU Xid faults, and `/sys/class/drm/` connector status.
* **Forbidden Inference:** Mado never infers a driver defect from a missing monitor in `monitors.conf`; Tsukuroi never infers a configuration defect from an active DKMS module.

---

## 5. Trace of Second-Order Effects Across Surfaces

1. **Coverage Axis (C1):**
   - Enables clean admission of Milestone U5 (`output-colour-boundaries-r14.md`) by anchoring it firmly in **Tier 2** (protocol specification and sanitized advertisement) with links to **Tier 1** (configuration).
   - Reciprocal mined rows S047 and S048 advance U-items from $4/7 \approx 5.7143/10$ to $5/7 \approx 7.1429/10$.
   - Explicitly reserves Tier 4 as out-of-province, preventing rejection by outside spot-checks for unsubstantiated hardware claims.

2. **Operability Axis (C2):**
   - Keeps `tools/mado-verify.sh` hermetic and robust. By strictly confining the gate to Tier 1 regular-file targets and include graph walks, the gate never depends on host GPU state, kernel version, or `/dev/dri/card*` nodes.
   - C2 improvements (resolving direct directories, all-directory globs, and mixed globs) remain purely filesystem-predicated, avoiding flaky hardware dependencies.

3. **Adjacency Axis:**
   - Strengthens the fleet contract. Eliminates the ambiguity noted in rounds 1–3 regarding NVIDIA environment variables (`envs.conf`), cementing driver diagnosis in Tsukuroi while leaving configuration syntax in Mado.

4. **Calibration Axis & Verifier Corrections:**
   - Directly honors **R13-V1:** Affirms that `globals.json` retains only interface headers in its global table, while sanitized probe/session metadata is retained, and all hardware/EDID/colorimetry details are dropped.
   - Directly honors **R13-V2:** Emphasizes that single-run configuration boundary hashes (`gate-file-plane.txt`) verify within-run immutability, not cross-revision output equivalence.
   - Directly honors **R13-V3:** Integrates with `ReceiptBuild`'s `receipt.py` to ensure that standalone receipts carry unforgeable revision and gate SHA-256 headers.

---

## 6. Risks and Verification

### Risks and Contradictions
1. **Risk of Perceived Under-Coverage:** A critic might argue: *"If Mado does not check DRM connectors or /sys/class/drm, how does it know the display works?"*
   - *Resolution:* Grounded in Mado's PROVINCE: Mado governs *configuration and compositor craft*, verified by file bytes and screenshot/read verbs. Physical hardware link training belongs to kernel diagnosis. Claiming hardware truth without kernel access is an overreach; honoring the boundary is honest craft.
2. **Contradiction Guard:** `globals.json` lists `wp_drm_lease_device_v1` (multiplicity 2). A reader might confuse DRM lease with DRM kernel diagnosis.
   - *Resolution:* `wp_drm_lease_device_v1` is an IPC protocol global allowing clients (e.g. VR compositors) to request connector leases from the Wayland compositor. Advertising the protocol global is a Tier 2 Wayland event; the underlying kernel DRM lease ioctl (`DRM_IOCTL_MODE_CREATE_LEASE`) is Tier 4 (tsukuroi-owned).

### Verification Recipe for L1 Integration
1. Verify that `corpus/knowledge/output-colour-boundaries-r14.md` (U5 note) incorporates the Four-Tier Partition Table and explicitly declares Tier 4 out-of-province.
2. Run `grep -nE '(/dev/dri|/sys/class/drm|nvidia-smi|dkms)' tools/mado-verify.sh` to ensure zero Tier 4 commands exist in Mado's gate.
3. Confirm that S047 and S048 in `corpus/SOURCES.md` cite primary spec XML anchors without claiming DRM/KMS hardware verification.

---

## 7. Tooling Record

Per Tooling Directive (operator, 2026-10-19):
- **Tools Installed / Updated:** None.
- All observations were conducted read-only on committed repository artifacts and existing system state.
