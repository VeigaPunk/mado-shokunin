# OutputHost — Historical Host Advertisement Mapping for U5 Boundaries (Round 14, w1)

Seat: `MadoR14.OutputHost` (scout, leaf; no subagent dispatch, no background jobs, no commits/push).
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Milestone: U5 boundaries and regular-source targets.
Axes served: **coverage (C1)**, **operability (C2)**.

## 1. Scope and Pinned Substrate

This investigation maps what host protocol advertisement **supports** and **cannot support** for the U5 output-management and colour boundary.

Per contract and seat assignment:
- Primary input: committed `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/globals.json` only.
- Fresh host client execution: **none**; no Wayland client executed, no compositor mutations, no protocol requests issued.
- Date of observation: explicitly historical (`captured_utc: 2026-10-20T04:10:03Z`; session binding `2026-10-20T04:18:27Z`).

### Outside Corrections Addressed

1. **R13-V1 (Retained-data wording):**
   Clarification strictly maintained: **global records contain interface/version only; sanitized probe/session metadata is also retained.**
   The 72 items under `globals` contain exclusively `interface` and `version`. Top-level metadata retains sanitized probe, tool, compositor, and session-binding records. All raw device identities, EDID blocks, physical display identifiers, colorimetry blocks, DRM device paths, and process/instance signatures were excluded by the projection filter.
2. **R13-V2 (Evidence precision):**
   Distinguishes within-run boundary receipts (substrate files unchanged during a verification run) from cross-revision output equality. `globals.json` is an immutable historical point observation bound to a specific instant, socket, and commit; it does not assert cross-session or cross-revision immutability.
3. **R13-V3 (Receipt measured digest):**
   All evidence citations carry explicit SHA-256 digests and source pins to ensure verifiable provenance.

---

## 2. Committed Artifact & Metadata Census

Artifact: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/globals.json`
Committed File SHA-256: `ced47240c2a1941bbbf1f125d9a1e41624cfeeb8218ab2a3a425eb335a08a949`
Canonical Set SHA-256 (`interface@version`, sorted): `9569d02fe2b04bf62079258b1d74f5d2ad8510c26ef0710a1a64c95f1a9becaa`

### Metadata Fields Retained

| Field Path | Retained Value | Meaning / Boundary Scope |
|---|---|---|
| `schema` | `"mado-globals-capture-v1"` | Explicit schema tag for sanitized globals capture. |
| `captured_utc` | `"2026-10-20T04:10:03Z"` | Historical timestamp of probe execution. |
| `probe.command` | `"wayland-info"` | Command executed for the discovery probe. |
| `probe.return_code` | `0` | Clean process exit. |
| `probe.stderr_bytes` | `0` | Zero stderr output. |
| `probe.display_socket` | `"wayland-1"` | Targeted Wayland display socket. |
| `probe.sanitization` | `"only interface header lines; every indented detail line dropped"` | Allowlist projection rule discarding device identity. |
| `tool.name` | `"wayland-info"` | Diagnostic tool binary name. |
| `tool.path` | `"/usr/bin/wayland-info"` | Diagnostic tool binary path. |
| `tool.binary_sha256` | `d9d851d5d6b408976dcfccefbf149ef10a47aed463509a15d70606fc9ba8b400` | Tool binary SHA-256 digest on host. |
| `tool.package` | `"wayland-utils"` | Installed package providing the tool. |
| `tool.package_version` | `"1.3.0-1"` | Installed package version. |
| `tool.man_version` | `"1.3.0 (2020-07-08)"` | Manpage version anchor. |
| `tool.install_channel` | `"pacman extra"` | Installation channel. |
| `tool.wayland_package_version` | `"1.26.0-1"` | Core Wayland library package version. |
| `tool.linked_soname` | `"libwayland-client.so.0"` | Dynamic linker soname resolution. |
| `tool.linkage_note` | `"soname observed via ldd and owned by wayland 1.26.0-1; link-time version not verified"` | Linkage qualification. |
| `compositor.name` | `"Hyprland"` | Target compositor. |
| `compositor.version` | `"0.56.2"` | Reported semantic version. |
| `compositor.tag` | `"v0.56.2"` | Git tag matching S018 mining. |
| `compositor.commit` | `"efb50993780079460b0cbed1363e2166a2de1d9f"` | Git commit hash. |
| `compositor.branch` | `"v0.56.2"` | Git branch. |
| `compositor.dirty` | `false` | Clean build status. |
| `compositor.probe_command` | `"hyprctl -j version"` | Probe command for compositor identity. |
| `compositor.probe_return_code` | `0` | Clean exit of compositor probe. |
| `global_count` | `72` | Total registry advertisement entries. |
| `unique_interface_count` | `71` | Distinct interface names advertised. |
| `multiplicity` | `[{"interface": "wp_drm_lease_device_v1", "count": 2, "version": 1}]` | Explicit record of duplicated advertisements. |
| `excluded` | 9 explicit exclusion rules | Detailed list of dropped identity blocks (geometry, EDID, paths, colorimetry). |
| `session_binding.correlated` | `true` | Correlation evaluated in process memory. |
| `session_binding.unique_signature_match`| `true` | Single instance signature match confirmed. |
| `session_binding.instance_count` | `1` | Exactly one active compositor instance on host. |
| `session_binding.wl_socket` | `"wayland-1"` | Matches `WAYLAND_DISPLAY`. |
| `session_binding.captured_utc` | `"2026-10-20T04:18:27Z"` | Correlation timestamp. |
| `session_binding.probe_command` | `"hyprctl -j instances"` | Correlation probe command. |
| `session_binding.probe_return_code` | `0` | Correlation probe return code. |

---

## 3. Inventory of Output-Management and Colour Interfaces

Out of the 72 advertised globals in `globals.json`, the following 17 interfaces govern or directly touch output configuration, display colorimetry/calibration, presentation, and output capture:

### Tier 1: Output Configuration & Power Management (Direct U5 Output Boundary)

| Registry Index | Interface Name | Advertised Version | Upstream Authority / Project | Upstream Development Phase | Core Function / Protocol Scope |
|---|---|---|---|---|---|
| **#31** | `zwlr_output_manager_v1` | **4** | `wlr-protocols` (`unstable/wlr-output-management-unstable-v1.xml`) | `unstable` (wlr-protocols ecosystem) | Privileged compositor output configuration manager. Distributes heads, modes, positions, scales, and enables atomic configuration transactions. |
| **#9** | `zxdg_output_manager_v1` | **3** | `wayland-protocols` (`unstable/xdg-output/xdg-output-unstable-v1.xml`) | `unstable` | Companion shell output manager. Exposes logical screen geometry, fractional coordinates, output names, and descriptions. |
| **#72** | `wl_output` | **4** | `wayland` core (`wayland.xml`) | `stable` (Core) | Baseline output announcement. Provides physical dimensions, subpixel layout, make, model, transform, refresh modes, and scale. |
| **#23** | `zwlr_output_power_manager_v1` | **1** | `wlr-protocols` (`unstable/wlr-output-power-management-unstable-v1.xml`) | `unstable` (wlr-protocols ecosystem) | Output display power management (DPMS modes: on, standby, suspend, off). |

### Tier 2: Color Management, Gamma Calibration & CTM (Direct U5 Colour Boundary)

| Registry Index | Interface Name | Advertised Version | Upstream Authority / Project | Upstream Development Phase | Core Function / Protocol Scope |
|---|---|---|---|---|---|
| **#66** | `wp_color_manager_v1` | **3** | `wayland-protocols` (`staging/color-management/color-management-v1.xml`) | `staging` | Upstream color management. Provides ICC profile attachment, parametric color spaces, image descriptions, rendering intents, and output colorimetry queries. |
| **#15** | `zwlr_gamma_control_manager_v1` | **1** | `wlr-protocols` (`unstable/wlr-gamma-control-unstable-v1.xml`) | `unstable` (wlr-protocols ecosystem) | Direct gamma ramp / color calibration curve setting for displays. |
| **#46** | `hyprland_ctm_control_manager_v1`| **2** | `hyprland-protocols` | `outside` (Hyprland compositor-private) | Compositor-internal Color Transform Matrix control (night light, color temperature, matrix adjustment). |

### Tier 3: Display Buffering, Geometry, Scaling & Presentation (Adjacent Display Boundaries)

| Registry Index | Interface Name | Advertised Version | Upstream Authority / Project | Upstream Development Phase | Core Function / Protocol Scope |
|---|---|---|---|---|---|
| **#67, #69** | `wp_drm_lease_device_v1` | **1** (multiplicity 2) | `wayland-protocols` (`staging/drm-lease/drm-lease-v1.xml`) | `staging` | Direct DRM KMS connector lease mechanism for VR HMDs / direct display hardware access. |
| **#36** | `wp_presentation` | **2** | `wayland-protocols` (`stable/presentation-time/presentation-time.xml`) | `stable` | Presentation time feedback and hardware display refresh synchronization. |
| **#7** | `wp_tearing_control_manager_v1` | **1** | `wayland-protocols` (`staging/tearing-control/tearing-control-v1.xml`) | `staging` | Asynchronous page flip / tearing permission per surface on supporting outputs. |
| **#8** | `wp_fractional_scale_manager_v1`| **1** | `wayland-protocols` (`staging/fractional-scale/fractional-scale-v1.xml`)| `staging` | Fractional surface scaling reporting for high-DPI displays. |
| **#6** | `wp_viewporter` | **1** | `wayland-protocols` (`stable/viewporter/viewporter.xml`) | `stable` | Surface buffer cropping and scaling to viewport output dimensions. |
| **#44** | `wp_single_pixel_buffer_manager_v1`| **1** | `wayland-protocols` (`staging/single-pixel-buffer/single-pixel-buffer-v1.xml`)| `staging` | Single-pixel 32-bit RGBA buffer creation for solid color surfaces without buffer memory waste. |
| **#49** | `wp_content_type_manager_v1` | **1** | `wayland-protocols` (`staging/content-type/content-type-v1.xml`) | `staging` | Surface content-type hints for output display processing (e.g. game mode, cinema). |

### Tier 4: Output Frame Capture (Adjacent Output Observation Boundaries)

| Registry Index | Interface Name | Advertised Version | Upstream Authority / Project | Upstream Development Phase | Core Function / Protocol Scope |
|---|---|---|---|---|---|
| **#61** | `zwlr_screencopy_manager_v1` | **3** | `wlr-protocols` (`unstable/wlr-screencopy-unstable-v1.xml`) | `unstable` (wlr-protocols ecosystem) | Direct output pixel/frame copy to client buffers. |
| **#63** | `ext_output_image_capture_source_manager_v1`| **1** | `wayland-protocols` (`staging/ext-image-capture-source/`)| `staging` | Output capture source abstraction for modern ext image copy protocols. |
| **#65** | `ext_image_copy_capture_manager_v1`| **1** | `wayland-protocols` (`staging/ext-image-copy-capture/`)| `staging` | Standardized screen and toplevel image capture protocol. |

---

## 4. Grounded Support Map: What Advertisement SUPPORTS for U5

Based strictly on committed `globals.json` `[OBS]`, the following claims are verified:

1. **Server-Side Registry Dispatch Presence:**
   Hyprland 0.56.2 (commit `efb50993780079460b0cbed1363e2166a2de1d9f`) actively announces `zwlr_output_manager_v1@4` and `wp_color_manager_v1@3` to clients connecting on socket `wayland-1`.
   The compositor implements the Wayland wire serialization necessary to emit `wl_registry.global` events for these interfaces.
2. **Coexistence of Heterogeneous Protocol Authorities:**
   The host demonstrates simultaneous advertisement across three distinct governance sources:
   - Upstream `wayland-protocols` staging (`wp_color_manager_v1@3`, `wp_drm_lease_device_v1@1`, `wp_tearing_control_manager_v1@1`).
   - Upstream `wlr-protocols` unstable (`zwlr_output_manager_v1@4`, `zwlr_gamma_control_manager_v1@1`, `zwlr_output_power_manager_v1@1`).
   - Compositor-private extensions (`hyprland_ctm_control_manager_v1@2`).
3. **Advertised Interface Version Alignment & Config Dependency:**
   - `zwlr_output_manager_v1` is advertised at **version 4**: in pinned `wlr-output-management-unstable-v1.xml`, `set_custom_mode` has no `since` attribute (present from version 1); version 4 specifically adds `adaptive_sync` (`adaptive_sync` event on `zwlr_output_head_v1`, `set_adaptive_sync` request on `zwlr_output_configuration_head_v1`, enum `adaptive_sync_state`, and error `invalid_adaptive_sync_state`).
   - `wp_color_manager_v1` is advertised at **version 3**: in pinned `color-management-v1.xml`, `create_parametric_creator` has no `since` attribute (present from version 1); version 2 adds manager `get_image_description`, output `preferred_changed2`, image description `ready2`, and `compound_power_2_4` transfer function; version 3 specifically adds `create_windows_bt2100`. Furthermore, in Hyprland 0.56.2 (`ProtocolManager.cpp:235`), `wp_color_manager_v1` version 3 advertisement is configuration-dependent: enabled via `experimental:wp_cm_1_2` (default `true`).
   - `wl_output` is advertised at **version 4** (supporting human-readable name and description events, since 4).
4. **Multiplicity Truth:**
   `wp_drm_lease_device_v1` is advertised twice (multiplicity = 2, distinct registry names 67 and 69 dropped to maintain determinism). No other output or color interface exhibits multiplicity.

---

## 5. Grounded Limit Map: What Advertisement CANNOT Support for U5

The following inferences are strictly **unsupported, rejected, or classified as UNKNOWN (`[UNK]`)**:

| Rejected Claim / Overreach | Truthful Grounding / Reason for Rejection | Boundary Verdict |
|---|---|---|
| **"Advertisement proves working monitor reconfiguration."** | `wl_registry.global` announces object availability. It does not execute `zwlr_output_configuration_v1.apply` or `test`. Compositor configuration policies, head locking, security tokens, mode validation, and DRM/KMS driver responses are unexercised. | `[REJECTED]` — Reconfiguration execution is `[UNK]`. |
| **"Advertisement proves HDR or wide color gamut works on the display."** | `wp_color_manager_v1@3` announcement proves only that the protocol interface is registered. It does not prove that connected monitors support HDR, that the GPU supports wide-gamut framebuffers, that tone-mapping shaders function, or that HDR metadata (ST 2086 / CTA-861-G) is transmitted. | `[REJECTED]` — Display color reproduction is `[UNK]`. |
| **"wayland-info's queries prove feature execution."** | S046 confirms `wayland-info` (`wayland-info.c:2919-2920`) binds `wp_color_manager_v1` at interface version 1; the diagnostic `get_image_description` call (`:2750`) is issued on the output object (`wp_color_management_output_v1`, a v1 request), distinct from the manager's v2 `get_image_description` request. Diagnostic reads verify discovery responses only; they do not exercise output configuration changes, display mode switching, rendering transformations, or v2/v3 manager features. | `[REJECTED]` — Diagnostic v1 binding is not feature execution. |
| **"Advertisement proves protocol maturity or stability."** | Upstream development phase is governed by owning repositories (S005, S040). `wp_color_manager_v1` is in `staging/`; `zwlr_output_manager_v1` is in `unstable/`. Wire advertisement does not grant stable ABI guarantees. | `[REJECTED]` — Registry name/version does not imply frozen ABI. |
| **"Monitor hardware counts, models, and geometry can be derived from globals.json."** | All indented detail blocks (`wl_output` geometry/modes, `zxdg_output_manager_v1` logical IDs, `wp_color_manager_v1` colorimetry blocks) were dropped under the sanitization filter. Zero hardware or display identities are retained. | `[REJECTED]` — Hardware topology is explicitly omitted. |
| **"The historical capture guarantees identical state across sessions."** | Globals can appear or disappear via `global_remove` events, hotplug, or configuration reload. The capture is dated `2026-10-20T04:10:03Z` and session-bound to PID instance 1. It is not an eternal desktop contract. | `[REJECTED]` — Point observation is strictly historical. |

---

## 6. Synthesis Table for Peer Consumers

This table directly provides the three-facet fact/evidence/does-not-license foundation for `EvidenceChain`, `OutputSpec`, `ColourSpec`, `HyprSupport`, and `AttackCoverage`:

| Domain | Observed Fact `[OBS]` | Retained Evidence Source | What It Does NOT License `[UNK]` |
|---|---|---|---|
| **Output Management** | Hyprland 0.56.2 advertises `zwlr_output_manager_v1@4` and `zxdg_output_manager_v1@3` on socket `wayland-1`. | `globals.json` entries #31 and #9; set SHA-256 `9569d02f…`. | Does NOT license claims of working display mode changes, multi-monitor configuration, head disabling, or KMS atomic commits. |
| **Color Management** | Hyprland 0.56.2 advertises `wp_color_manager_v1@3`, `zwlr_gamma_control_manager_v1@1`, and `hyprland_ctm_control_manager_v1@2`. | `globals.json` entries #66, #15, #46; metadata sanitization record. | Does NOT license claims of working HDR rendering, ICC profile application, display colorimetry calibration, or physical LUT manipulation. |
| **Hardware & Session** | Sanitized capture retains 72 advertisements (71 unique) from a single confirmed Hyprland instance. | `globals.json` `session_binding` and `excluded` rules. | Does NOT license monitor count inferences, EDID/make/model claims, cross-session invariance, or desktop health certification. |

---

## 7. Tooling Record & Checks

- **Tooling Directive (Operator 2026-10-19):** No tool was installed or updated by this seat. Plain read-only inspection of committed artifacts was performed.
- **Verification Command for L1:**
```sh
# Verify exact output-management and color interface versions in the committed capture
jq -e '
  (.globals[] | select(.interface == "zwlr_output_manager_v1") | .version == 4) and
  (.globals[] | select(.interface == "zxdg_output_manager_v1") | .version == 3) and
  (.globals[] | select(.interface == "wp_color_manager_v1") | .version == 3) and
  (.globals[] | select(.interface == "zwlr_gamma_control_manager_v1") | .version == 1) and
  (.globals[] | select(.interface == "hyprland_ctm_control_manager_v1") | .version == 2) and
  (.globals[] | select(.interface == "wl_output") | .version == 4) and
  .global_count == 72 and
  .unique_interface_count == 71
' .ufo/waves/round-13/w1/globals.json
```
Expected output: `true` (exit code 0).
