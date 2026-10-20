# OutputHost report — round 14, w1

## Files changed

| path | role |
|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/OutputHost.md` | detailed findings: historical host advertisement mapping for U5 boundaries |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/reports/OutputHost.md` | this rendered scoped report |

No shared source, gate, fixture, corpus, or config file was modified. No commits or push.

## Behavior / result

- Primary target analyzed: committed `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/globals.json` (`captured_utc: 2026-10-20T04:10:03Z`, session correlation `04:18:27Z`). No fresh host client executed.
- R13-V1 retained-data clarification strictly applied: **global records contain interface/version only; sanitized probe/session metadata is also retained.** The 72 items under `globals` contain only `interface` and `version`; all indented detail lines (EDID, display geometry, colorimetry blocks, DRM device paths, seat names, numeric registry IDs) were dropped by the allowlist projection filter.
- R13-V2 evidence precision maintained: the observation is an immutable historical point sample; within-run boundary checks prove configuration file stability during execution, not cross-revision or cross-session output equality.
- R13-V3 standalone digest provenance maintained: all artifacts cited carry explicit SHA-256 digests and Git commit pins.
- Output-management interfaces identified in historical registry:
  - `zwlr_output_manager_v1` advertised at version **4** (wlr-protocols unstable).
  - `zxdg_output_manager_v1` advertised at version **3** (wayland-protocols unstable).
  - `wl_output` advertised at version **4** (Wayland core stable).
  - `zwlr_output_power_manager_v1` advertised at version **1** (wlr-protocols unstable).
- Color & calibration interfaces identified in historical registry:
  - `wp_color_manager_v1` advertised at version **3** (wayland-protocols staging; v1 has `create_parametric_creator`, v2 adds manager `get_image_description`, v3 adds `create_windows_bt2100`). In Hyprland 0.56.2 (`ProtocolManager.cpp:235`), v3 advertisement is configuration-dependent (`experimental:wp_cm_1_2`, default `true`).
  - `zwlr_gamma_control_manager_v1` advertised at version **1** (wlr-protocols unstable).
  - `hyprland_ctm_control_manager_v1` advertised at version **2** (Hyprland compositor-private).
- Adjacent display & capture interfaces identified:
  - `wp_drm_lease_device_v1` advertised at version **1** with multiplicity **2**.
  - `wp_presentation` advertised at version **2** (wayland-protocols stable).
  - `wp_tearing_control_manager_v1` (v1), `wp_fractional_scale_manager_v1` (v1), `wp_viewporter` (v1), `wp_single_pixel_buffer_manager_v1` (v1).
  - `zwlr_screencopy_manager_v1` (v3), `ext_output_image_capture_source_manager_v1` (v1), `ext_image_copy_capture_manager_v1` (v1).
- What advertisement supports for U5:
  - Proves server-side announcement dispatch for `zwlr_output_manager_v1@4` (where v4 specifically adds `adaptive_sync`; `set_custom_mode` is v1) and `wp_color_manager_v1@3` under Hyprland 0.56.2 (`efb50993780079460b0cbed1363e2166a2de1d9f`) on socket `wayland-1`.
  - Establishes co-existence of standard staging color management alongside wlr gamma control and compositor-private CTM control.
- What advertisement cannot support for U5:
  - Does NOT license claims of working display reconfiguration (`zwlr_output_configuration_v1.apply` / `test` unexercised; KMS transactions unknown).
  - Does NOT license claims of HDR display reproduction, wide-gamut output, or physical LUT manipulation (`wp_color_manager_v1` colorimetry blocks omitted; hardware capabilities unexercised).
  - Diagnostic reads by `wayland-info` (binding `wp_color_manager_v1` at v1 per `wayland-info.c:2919` and querying output `get_image_description` at v1 per `:2750`) do not exercise v2/v3 manager features or configuration changes.
  - Does NOT license monitor topology or count claims (dropped during sanitization).
  - Does NOT license upstream protocol stability or cross-session permanence.

## Evidence retained

- Historical Artifact: `.ufo/waves/round-13/w1/globals.json`.
- Committed File SHA-256: `ced47240c2a1941bbbf1f125d9a1e41624cfeeb8218ab2a3a425eb335a08a949`.
- Canonical Set SHA-256: `9569d02fe2b04bf62079258b1d74f5d2ad8510c26ef0710a1a64c95f1a9becaa`.
- Tool & Package Pins: `wayland-info` 1.3.0-1 (`wayland-utils 1.3.0-1`, pacman extra), binary SHA-256 `d9d851d5d6b408976dcfccefbf149ef10a47aed463509a15d70606fc9ba8b400`.
- Compositor Pin: Hyprland `0.56.2`, tag `v0.56.2`, commit `efb50993780079460b0cbed1363e2166a2de1d9f`, dirty `false`.
- Session Binding: socket `wayland-1`, unique instance signature match `true`, 1 instance.

## Risks & limitations

- Point observation: bound to historical instant `2026-10-20T04:10:03Z` and PID instance 1; globals can change dynamically via `global_remove` or compositor reload.
- Advertisement only: wire discovery does not execute feature logic.
- Sanitized identity: monitor names, EDID, and colorimetry tables were dropped; hardware topology is intentionally unavailable.

## Blockers

None.

## Checks L1 should run once

```sh
jq -e '
  (.globals[] | select(.interface == "zwlr_output_manager_v1") | .version == 4) and
  (.globals[] | select(.interface == "zxdg_output_manager_v1") | .version == 3) and
  (.globals[] | select(.interface == "wp_color_manager_v1") | .version == 3) and
  (.globals[] | select(.interface == "zwlr_gamma_control_manager_v1") | .version == 1) and
  (.globals[] | select(.interface == "hyprland_ctm_control_manager_v1") | .version == 2) and
  (.globals[] | select(.interface == "wl_output") | .version == 4) and
  .global_count == 72 and
  .unique_interface_count == 71 and
  .session_binding.correlated == true
' .ufo/waves/round-13/w1/globals.json
```
Expected: `true` (exit code 0).
