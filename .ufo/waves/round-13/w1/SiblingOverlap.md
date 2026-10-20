# SiblingOverlap — Protocol Diagnostics Ownership vs Input/Kernel Lane and System Maintenance

**Seat:** `MadoR13.SiblingOverlap` (connector, leaf)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Milestone:** exact-set census and sourced U4 boundaries (Round 13, Wave 1)  
**Judged on:** `coverage`, `operability`  
**Status:** Complete findings and draft; read-only scans performed; no shared files modified.

---

## 1. Executive Summary & Proposed Move

### 1.1 The Proposed Move
**Establish an unambiguous 3-lane diagnostic boundary and handoff contract for protocol surfaces between desktop compositor craft (`mado-shokunin`), host OS/kernel/driver maintenance (`tsukuroi-shokunin`), and fleet observability (`mori-shokunin`).**

In Round 13, `mado-shokunin` advances its coverage axis ($3/7 \rightarrow 4/7$) by admitting U4 protocol-phase and advertised-globals knowledge (`wayland-info`, `wayland-protocols` phasing, `wl_registry`). However, protocol diagnostics border directly on kernel input subsystems (`/dev/input/event*`, `libinput`), driver/DRM subsystems (`nvidia`, `drm`), and host log streams (`journalctl`). 

Without strict province demarcation, agents face second-order risks:
1. Conflating protocol interface advertisement (`wl_registry.global`) with kernel driver or hardware input execution.
2. Attempting to absorb system maintenance, kernel module diagnostics, or journal triage into `mado`.
3. Creating unverified cross-domain dependencies in verification fixtures.

This report establishes that:
- **Compositor protocol advertisement (`wl_registry.global`, `wayland-info`) and client binding negotiation belong strictly to `mado`'s display behavior surface.**
- **Kernel input event tracing (`/dev/input/event*`, `libinput debug-events`, evdev/evtest) and kernel module/driver health (NVIDIA GSP, DRM nodes) belong strictly to `tsukuroi` (OS substrate / driver plane) and cannot be absorbed by `mado`.**
- **Compositor process crashes, kernel OOMs, and session death logs in `journalctl -b` belong to `tsukuroi` (OS/boot triage) and `mori` (fleet kill/liveness correlation). `mado` reads compositor log shape only (`hyprland.log` length/presence) and never absorbs journal triage.**

---

## 2. Read-Only Scan of Fleet Province Declarations

All citations are grounded in primary `PROVINCE.md` files in `/home/vgpnk/Projects/shokunin`:

### 2.1 `mado-shokunin/PROVINCE.md`
- **Domain:** Desktop & compositor craft — the Hyprland/waybar/walker configuration plane and display behavior on this host (`PROVINCE.md:3-4`).
- **Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules, animations), `~/.config/waybar/`, `~/.config/walker/`, terminal emulator configs (`~/.config/alacritty|foot|kitty|ghostty/`), themes/wallpapers as declared files, screen/idle behavior (`hypridle`/`hyprlock` where present) (`:6-9`).
- **Refuses:** Secrets in configs (shape-only, $\rightarrow$ `kagi`), model endpoints ($\rightarrow$ `kama`), model quality ($\rightarrow$ `kengaku`). Never mutates a running compositor state; every claim is file-byte- or screenshot-verified (`:14-16`).
- **Rule:** "Out of province $\rightarrow$ report, never absorb" (`:18`).

### 2.2 `tsukuroi-shokunin/PROVINCE.md` (System Maintenance / Kernel / Drivers)
- **Domain:** Host operability & system repair (繕, mending) — the OS substrate itself: package state, systemd, drivers/firmware, boot health (`PROVINCE.md:3-4`).
- **Owns (surfaces, all read-only probes):** Pacman state (`pacman -Qkk` verify loops, foreign/AUR census, `.pkg.tar.zst` receipt discipline), systemd user units & timers (`systemctl --user`, unit files, failed states), journal/boot triage (`journalctl -b`, dmesg error classes), driver/firmware plane (kernel modules, nvidia driver + GSP firmware presence, `nvidia-smi` shape). Update-safety questions: what an `-Syu` would touch, what pins/holds exist (`:8-14`).
- **Adjacent Handoffs (ADJ-03):** "Desktop rendering, bindings, menu or idle behavior needs configuration-level diagnosis" $\rightarrow$ Tsukuroi retains user-manager/unit, package and driver health; hands off observed UI symptom to `mado`. Mado verifies file/screenshot behavior itself (`:48`).
- **Adjacent Handoffs (ADJ-06):** "Driver/firmware/package mechanism requires shipped-artifact reverse engineering beyond health inventory" $\rightarrow$ protocol integrator (`:51`).
- **Refuses:** Endpoint/model serving health ($\rightarrow$ `kama`), secrets ($\rightarrow$ `kagi`), binary RE of drivers ($\rightarrow$ `kaidoku`/`revenger`). Never installs, upgrades, or removes packages; never restarts services (`:25-28`).

### 2.3 `mori-shokunin/PROVINCE.md` (Fleet & Host Observability)
- **Domain:** Fleet & host observability (森) — whether the fleet, its waves and its host are alive and progressing (`PROVINCE.md:3-4`).
- **Owns (read-only probes):** Shokunin watchdog liveness, `.ufo/waves/*` settlement state, kill/OOM event classes from `journalctl --user` and cgroup `memory.events`, resource runway, lane silence grading (`:6-10`).
- **Refuses:** Dispatch and orchestration mechanism ($\rightarrow$ `kumitate`); OS package, systemd unit, driver/firmware and boot state ($\rightarrow$ `tsukuroi`) — mori reads journal and cgroup events as fleet evidence and reports them, never owning OS state; endpoint health ($\rightarrow$ `kama`); credential material ($\rightarrow$ `kagi`) (`:12-16`).

### 2.4 Adjacent Specialty Lanes
- **`tabi-shokunin/PROVINCE.md`:** Drives real browsers against real sites; owns CDP session discipline and interaction evidence (`:3-13`). Refuses RE as forensics ($\rightarrow$ `kaidoku`/`revenger`), web publishing ($\rightarrow$ `kake`), secrets ($\rightarrow$ `kagi`) (`:15-19`).
- **`souji-shokunin/PROVINCE.md`:** Fleet repository & workspace hygiene (receipt-gated removal of stale/duplicate artifacts) (`:3-5`). Acts on artifacts, never on processes or OS (`:40-43`).
- **`kumitate-shokunin/PROVINCE.md`:** Scopes OMP task/hub dispatch, ufo-fsd scripts and runtime (`:3-4`).
- **`kagi-shokunin/PROVINCE.md`:** Owns secrets & vault ops, credential hygiene evidence (`:3-4`).

---

## 3. Protocol Diagnostics Ownership Crosswalk

| Diagnostic Surface / Observation | Boundary Classification | Primary Owner | Secondary / Handoff Recipient | Why it is NOT absorbed by Mado |
|---|---|---|---|---|
| **Compositor Advertised Globals (`wayland-info`, `wl_registry`)** | Desktop display protocol | `mado-shokunin` | N/A (Documented display behavior) | Owned by `mado` as part of "display behavior on this host" (`PROVINCE.md:3-4`). |
| **Wayland Protocol Phasing (`wayland-protocols` upstream)** | Desktop specification | `mado-shokunin` | N/A (Knowledge surface) | Grounding vocabulary for compositor protocol support and deprecation. |
| **XDG Portal Route Candidates (`portals.conf`, `.portal` files)** | Desktop configuration | `mado-shokunin` | `tsukuroi` (package state) | Configuration candidate analysis (`xdg-portal-routing-r12.md`). |
| **Kernel Input Events (`/dev/input/event*`, `evtest`, `evemu`)** | Kernel / Input Subsystem | `tsukuroi-shokunin` | `mado` (only for config effect) | Requires device node access/privilege; belongs to OS hardware substrate. |
| **`libinput` Hardware Defaults (`libinput list-devices`)** | Hardware driver plane | `tsukuroi-shokunin` | `mado` (reported, not absorbed) | Reflects kernel/libinput defaults, not Hyprland `input.conf` parsing (`lessons/round-12.md` M04). |
| **Compositor Crash Logs / Segfaults in Journal** | OS / Host Triage | `tsukuroi-shokunin` | `mori` (attribution) | Core OS journal diagnosis (`tsukuroi PROVINCE.md:10-12`). |
| **DRM / KMS / Kernel Video Driver (`nvidia`, `nouveau`, `amdgpu`)** | Driver / Firmware Plane | `tsukuroi-shokunin` | `mado` (receives ADJ-03) | Kernel module state and GSP firmware presence (`tsukuroi PROVINCE.md:12-14`). |
| **Package Upgrades of `wayland-utils` / `hyprland`** | Host Packaging | `tsukuroi-shokunin` | Operator | Package mutation is strictly forbidden to `mado` and operator-owned (`RULES.md`). |

---

## 4. Second-Order Effects Across Axes

### 4.1 Coverage Axis (C1)
- **Positive Effect:** Grounding U4 strictly in specification phase (`wayland-protocols` README) and sanitized compositor global advertisements (`wayland-info` headers) allows `mado` to cleanly achieve $4/7$ coverage without generating ungrounded claims about kernel execution.
- **Harm Avoidance:** Eliminates the trap of citing `libinput` tools or kernel `/dev/input/` events as "compositor input behavior" (preventing inference trap M04 from being repeated).

### 4.2 Operability Axis (C2)
- **Positive Effect:** Keeps `tools/mado-verify.sh` and its exact-set census focused entirely on hermetic filesystem verification (`EXPECT` sources vs `LOCAL` directory files) and read-only host queries (`hyprctl`, `wayland-info`).
- **Harm Avoidance:** Precludes adding gate checks that probe `/dev/input/` or system journal streams, which fail closed in unprivileged/container environments and break gate portability.

---

## 5. Handoff Contract for Protocol & Substrate Findings

When `mado-shokunin` discovers an issue during protocol or display diagnostic probing:
1. **If the compositor fails to advertise a protocol or parser reports error:**
   - *Action:* `mado` records this in its config health/drift note (`corpus/knowledge/`). It remains inside `mado`.
2. **If the failure is caused by a missing kernel module, DRM driver failure, or package corruption:**
   - *Action:* `mado` prepares an ADJ-03 packet for `tsukuroi-shokunin`, citing the observed display symptom and relevant command exit code. `mado` never attempts to rebuild initramfs, modprobe drivers, or reinstall packages.
3. **If the compositor process was killed by OOM or signal 9/11:**
   - *Action:* `mado` notes the missing socket or dead PID as `[UNK]`. It reports the timestamp to `mori-shokunin` for wave/host pressure correlation and to `tsukuroi-shokunin` for journal core triage.

---

## 6. Verification & Checks for the Main Agent

The main agent can verify this boundary alignment by running:
1. Confirm no note in `corpus/knowledge/` asserts ownership over `/dev/input/`, kernel modules, or journal repair:
   ```bash
   grep -rnE '(/dev/input|modprobe|journalctl -b.*remediation)' corpus/
   ```
2. Verify that U4 knowledge entries cite only Tier-A protocol specs and sanitized user-space global listings, preserving the `[OBS]`/`[INF-docs]`/`[UNK]` separation.
