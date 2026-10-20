# GlobalCapture — host advertised Wayland globals (round 13, w1)

Draft evidence for L1 integration. No shared source file touched; no compositor-mutating command run.
The U4 admission and the C1 axis verdict remain L1's call; this seat supplies the host census, the
tool/compositor pins and a candidate own-work source (S041).

## Axes this move serves

- **coverage** — U4 needs (a) protocol-phase vocabulary and (b) what the host actually advertises.
  This seat supplies (b) as a sanitized census and a pinned upstream crosswalk; it does not admit U4.
- **operability** — an inventory is only comparable if it is exact, replayable and identity-free:
  names + versions, a set digest, a multiplicity rule, and replay commands that reproduce the digest.

## Move

`wayland-info` was absent on first probe (`command -v wayland-info` → not found, rc 1). Per the
operator tooling directive and after reading `/home/vgpnk/.omp/agent/RULES.md`, it was installed
through the first authorized channel:

| tool | version | channel | reason |
|---|---|---|---|
| wayland-utils (provides `wayland-info`) | 1.3.0-1 | `sudo pacman -S --needed --noconfirm wayland-utils` (pacman `extra`) | assigned host probe; no partial upgrade (`-Sy`) was run |

## Probe record

Exact command and return code:

```
$ wayland-info
rc=0
(stderr empty: 0 bytes)
```

A second invocation produced the identical set digest (see **Replay**). Raw stdout was used only as
ephemeral scratch to compute the projection and was then deleted; the raw dump contains output
identity and is not retained (lane boundary: no raw session material; QUALITY criterion 13). The
committed artifact is the sanitized projection, and the set digest replays from it alone.

Environment used for resolution: `WAYLAND_DISPLAY=wayland-1`, `XDG_RUNTIME_DIR=/run/user/1000`
(the socket exists at `/run/user/1000/wayland-1`). Only the socket name is recorded; no environment
dump, no process list, no logs.

## Pins

| item | value | source |
|---|---|---|
| binary | `/usr/bin/wayland-info` sha256 `d9d851d5d6b408976dcfccefbf149ef10a47aed463509a15d70606fc9ba8b400` | `sha256sum /usr/bin/wayland-info`, 2026-10-20 |
| package | `wayland-utils 1.3.0-1` | `pacman -Q wayland-utils`, 2026-10-20 |
| man page | `1.3.0`, dated 2020-07-08 | `man wayland-info` |
| installed Wayland package | `wayland 1.26.0-1` (provides `/usr/lib/libwayland-client.so.0`, the soname `wayland-info` resolves; link-time version not verified) | `pacman -Q wayland`, `pacman -Qo /usr/lib/libwayland-client.so.0`, `ldd /usr/bin/wayland-info`, 2026-10-20 |
| compositor | Hyprland `0.56.2`, tag `v0.56.2`, branch `v0.56.2`, dirty `false` | `hyprctl -j version`, rc 0, 2026-10-20 |
| compositor commit | `efb50993780079460b0cbed1363e2166a2de1d9f` | same probe; equals the tag commit S018 mined; session-bound as below |

The compositor commit equality is what lets a future lane bind global-advertisement facts to the
tagged Hyprland source already in the registry (S018) without a new source row.

## Session binding (compositor ↔ socket)

Read-only correlation computed in memory; the instance signature was neither printed nor persisted:

```
$ hyprctl -j instances
rc=0
(stderr empty)
```

| observation | value |
|---|---|
| instances returned | **1** |
| `HYPRLAND_INSTANCE_SIGNATURE` matches | **exactly 1** record (unique) |
| selected record's `wl_socket` | `wayland-1` |
| `WAYLAND_DISPLAY` | `wayland-1` |
| match | **true** |
| correlation captured_utc | `2026-10-20T04:18:27Z` |

Persisted in `globals.json.session_binding`: `correlated`, `unique_signature_match`,
`instance_count`, `wl_socket`, capture time, probe command and return code. No signature, pid or
instance start time was retained. Because the signature match is unique and the socket agrees, the
compositor association of this capture is `[OBS]`, not `[INF]`; if either condition had failed the
association would have stayed an inference.

## Sanitized artifact

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/globals.json`

| field | value |
|---|---|
| schema | `mado-globals-capture-v1` |
| captured_utc | `2026-10-20T04:10:03Z` |
| file sha256 (provisional, work window) | `ced47240c2a1941bbbf1f125d9a1e41624cfeeb8218ab2a3a425eb335a08a949` |
| global advertisements | 72 |
| distinct interfaces | 71 |
| canonical set sha256 (`interface@version`, sorted) | `9569d02fe2b04bf62079258b1d74f5d2ad8510c26ef0710a1a64c95f1a9becaa` |
| multiplicity | `wp_drm_lease_device_v1@1` advertised **twice** (two lease devices) |

Sanitization rule: only the registry header lines matching
`^interface: '<name>', version: <n>, name: <registry-id>$` were projected. Every indented detail
block was dropped, which removes output name/description/make/model/modes, logical output
identifiers, colorimetry blocks, DRM device paths, dmabuf device/modifier tables, seat name and
capabilities, shm formats and presentation clocks. Registry numeric ids were also dropped because
they are connection-local and would make replays differ.

Identity scan over the artifact:

```
$ grep -Ei 'eDP|HDMI|DP-|/dev/|serial|vendor|model|title' .ufo/waves/round-13/w1/globals.json
(no matches)
```

## Exact census — 72 advertisements, registry order

`dir/ver` is the **upstream** wayland-protocols placement and interface version at commit
`35d9638c…` (see **Crosswalk source**), not a host-implementation claim. `outside` means the
interface name does not occur anywhere in the pinned tree (`stable/`, `staging/`, `experimental/`,
`unstable/`).

| # | interface | advertised | upstream dir | upstream ver | anchor in pinned tree |
|---|---|---|---|---|---|
| 1 | `wl_seat` | 9 | outside | — | — |
| 2 | `wl_data_device_manager` | 3 | outside | — | — |
| 3 | `wl_compositor` | 6 | outside | — | — |
| 4 | `wl_subcompositor` | 1 | outside | — | — |
| 5 | `wl_shm` | 2 | outside | — | — |
| 6 | `wp_viewporter` | 1 | stable | 1 | `stable/viewporter/viewporter.xml:27` |
| 7 | `wp_tearing_control_manager_v1` | 1 | staging | 1 | `staging/tearing-control/tearing-control-v1.xml:26` |
| 8 | `wp_fractional_scale_manager_v1` | 1 | staging | 1 | `staging/fractional-scale/fractional-scale-v1.xml:47` |
| 9 | `zxdg_output_manager_v1` | 3 | unstable | 3 | `unstable/xdg-output/xdg-output-unstable-v1.xml:57` |
| 10 | `wp_cursor_shape_manager_v1` | 2 | staging | 2 | `staging/cursor-shape/cursor-shape-v1.xml:25` |
| 11 | `zwp_idle_inhibit_manager_v1` | 1 | unstable | 1 | `unstable/idle-inhibit/idle-inhibit-unstable-v1.xml:27` |
| 12 | `zwp_relative_pointer_manager_v1` | 1 | unstable | 1 | `unstable/relative-pointer/relative-pointer-unstable-v1.xml:53` |
| 13 | `zxdg_decoration_manager_v1` | 2 | unstable | 2 | `unstable/xdg-decoration/xdg-decoration-unstable-v1.xml:26` |
| 14 | `wp_alpha_modifier_v1` | 1 | staging | 1 | `staging/alpha-modifier/alpha-modifier-v1.xml:26` |
| 15 | `zwlr_gamma_control_manager_v1` | 1 | outside | — | — |
| 16 | `ext_foreign_toplevel_list_v1` | 1 | staging | 1 | `staging/ext-foreign-toplevel-list/ext-foreign-toplevel-list-v1.xml:54` |
| 17 | `zwp_pointer_gestures_v1` | 3 | unstable | 3 | `unstable/pointer-gestures/pointer-gestures-unstable-v1.xml:28` |
| 18 | `zwlr_foreign_toplevel_manager_v1` | 3 | outside | — | — |
| 19 | `zwp_keyboard_shortcuts_inhibit_manager_v1` | 1 | unstable | 1 | `unstable/keyboard-shortcuts-inhibit/keyboard-shortcuts-inhibit-unstable-v1.xml:44` |
| 20 | `zwp_text_input_manager_v1` | 1 | unstable | 1 | `unstable/text-input/text-input-unstable-v1.xml:372` |
| 21 | `zwp_text_input_manager_v3` | 1 | unstable | 2 | `unstable/text-input/text-input-unstable-v3.xml:585` |
| 22 | `zwp_pointer_constraints_v1` | 1 | unstable | 1 | `unstable/pointer-constraints/pointer-constraints-unstable-v1.xml:49` |
| 23 | `zwlr_output_power_manager_v1` | 1 | outside | — | — |
| 24 | `xdg_activation_v1` | 1 | staging | 1 | `staging/xdg-activation/xdg-activation-v1.xml:69` |
| 25 | `ext_idle_notifier_v1` | 2 | staging | 2 | `staging/ext-idle-notify/ext-idle-notify-v1.xml:27` |
| 26 | `hyprland_lock_notifier_v1` | 1 | outside | — | — |
| 27 | `ext_session_lock_manager_v1` | 1 | staging | 1 | `staging/ext-session-lock/ext-session-lock-v1.xml:48` |
| 28 | `zwp_input_method_manager_v2` | 1 | outside | — | — |
| 29 | `zwp_virtual_keyboard_manager_v1` | 1 | outside | — | — |
| 30 | `zwlr_virtual_pointer_manager_v1` | 2 | outside | — | — |
| 31 | `zwlr_output_manager_v1` | 4 | outside | — | — |
| 32 | `org_kde_kwin_server_decoration_manager` | 1 | outside | — | — |
| 33 | `hyprland_focus_grab_manager_v1` | 1 | outside | — | — |
| 34 | `zwp_tablet_manager_v2` | 1 | stable | 2 | `stable/tablet/tablet-v2.xml:109` |
| 35 | `zwlr_layer_shell_v1` | 5 | outside | — | — |
| 36 | `wp_presentation` | 2 | stable | 2 | `stable/presentation-time/presentation-time.xml:28` |
| 37 | `xdg_wm_base` | 7 | stable | 7 | `stable/xdg-shell/xdg-shell.xml:32` |
| 38 | `zwlr_data_control_manager_v1` | 2 | outside | — | — |
| 39 | `zwp_primary_selection_device_manager_v1` | 1 | unstable | 1 | `unstable/primary-selection/primary-selection-unstable-v1.xml:70` |
| 40 | `xwayland_shell_v1` | 1 | staging | 1 | `staging/xwayland-shell/xwayland-shell-v1.xml:59` |
| 41 | `hyprland_toplevel_mapping_manager_v1` | 1 | outside | — | — |
| 42 | `hyprland_global_shortcuts_manager_v1` | 1 | outside | — | — |
| 43 | `xdg_wm_dialog_v1` | 1 | staging | 1 | `staging/xdg-dialog/xdg-dialog-v1.xml:26` |
| 44 | `wp_single_pixel_buffer_manager_v1` | 1 | staging | 1 | `staging/single-pixel-buffer/single-pixel-buffer-v1.xml:39` |
| 45 | `wp_security_context_manager_v1` | 1 | staging | 1 | `staging/security-context/security-context-v1.xml:26` |
| 46 | `hyprland_ctm_control_manager_v1` | 2 | outside | — | — |
| 47 | `hyprland_input_capture_manager_v1` | 1 | outside | — | — |
| 48 | `hyprland_surface_manager_v1` | 2 | outside | — | — |
| 49 | `wp_content_type_manager_v1` | 1 | staging | 1 | `staging/content-type/content-type-v1.xml:27` |
| 50 | `xdg_toplevel_tag_manager_v1` | 1 | staging | 1 | `staging/xdg-toplevel-tag/xdg-toplevel-tag-v1.xml:26` |
| 51 | `xdg_system_bell_v1` | 1 | staging | 1 | `staging/xdg-system-bell/xdg-system-bell-v1.xml:26` |
| 52 | `vicinae_hotkey_manager_v1` | 1 | outside | — | — |
| 53 | `ext_workspace_manager_v1` | 1 | staging | 1 | `staging/ext-workspace/ext-workspace-v1.xml:30` |
| 54 | `ext_data_control_manager_v1` | 1 | staging | 1 | `staging/ext-data-control/ext-data-control-v1.xml:41` |
| 55 | `wp_pointer_warp_v1` | 1 | staging | 1 | `staging/pointer-warp/pointer-warp-v1.xml:27` |
| 56 | `wp_fifo_manager_v1` | 1 | staging | 1 | `staging/fifo/fifo-v1.xml:26` |
| 57 | `zxdg_exporter_v2` | 1 | unstable | 1 | `unstable/xdg-foreign/xdg-foreign-unstable-v2.xml:59` |
| 58 | `zxdg_importer_v2` | 1 | unstable | 1 | `unstable/xdg-foreign/xdg-foreign-unstable-v2.xml:99` |
| 59 | `ext_background_effect_manager_v1` | 1 | staging | 1 | `staging/ext-background-effect/ext-background-effect-v1.xml:29` |
| 60 | `wp_commit_timing_manager_v1` | 1 | staging | 1 | `staging/commit-timing/commit-timing-v1.xml:27` |
| 61 | `zwlr_screencopy_manager_v1` | 3 | outside | — | — |
| 62 | `hyprland_toplevel_export_manager_v1` | 2 | outside | — | — |
| 63 | `ext_output_image_capture_source_manager_v1` | 1 | staging | 1 | `staging/ext-image-capture-source/ext-image-capture-source-v1.xml:61` |
| 64 | `ext_foreign_toplevel_image_capture_source_manager_v1` | 1 | staging | 1 | `staging/ext-image-capture-source/ext-image-capture-source-v1.xml:86` |
| 65 | `ext_image_copy_capture_manager_v1` | 1 | staging | 1 | `staging/ext-image-copy-capture/ext-image-copy-capture-v1.xml:37` |
| 66 | `wp_color_manager_v1` | 3 | staging | 3 | `staging/color-management/color-management-v1.xml:80` |
| 67 | `wp_drm_lease_device_v1` | 1 | staging | 1 | `staging/drm-lease/drm-lease-v1.xml:28` |
| 68 | `wp_linux_drm_syncobj_manager_v1` | 1 | staging | 1 | `staging/linux-drm-syncobj/linux-drm-syncobj-v1.xml:58` |
| 69 | `wp_drm_lease_device_v1` | 1 | staging | 1 | `staging/drm-lease/drm-lease-v1.xml:28` |
| 70 | `wl_drm` | 2 | outside | — | — |
| 71 | `zwp_linux_dmabuf_v1` | 5 | stable | 6 | `stable/linux-dmabuf/linux-dmabuf-v1.xml:27` |
| 72 | `wl_output` | 4 | outside | — | — |

## Derived structure (each count re-derivable from the artifact)

- Phase split of advertisements: **stable 5, staging 28, unstable 12, outside 27** — sum 72.
  Distinct names: **stable 5, staging 27, unstable 12, outside 27** — sum 71; the staging
  advertisement count exceeds the distinct count by the duplicated `wp_drm_lease_device_v1@1`.
  `jq -r '.globals[].interface' globals.json | sort -u | wc -l` → 71; rows per phase follow from
  the table.
- Outside-tree namespace grouping (string prefix only, no ownership claim): `wl_` 7, `zwlr_` 8,
  `hyprland_` 8, `zwp_` 2, `org_kde_` 1, `vicinae_` 1 — sum 27.
- Multiplicity is real: two distinct registry advertisements of `wp_drm_lease_device_v1` at version
  1. A set comparison that deduplicates silently loses one; the artifact records it explicitly.
- Prefix does **not** determine phase, measured on this census:
  - 24 z-prefixed advertisements split 12 unstable, 2 stable (`zwp_linux_dmabuf_v1`,
    `zwp_tablet_manager_v2`), 10 outside (`zwlr_*` 8 plus two `zwp_*` names absent from the tree).
  - `ext_` 9 → staging 9.
  - `xdg_` 5 → staging 4, stable 1 (`xdg_wm_base`).
  - `wp_` 16 advertisements → staging 14, stable 2 (`wp_viewporter`, `wp_presentation`).
- Advertised version versus pinned upstream interface version: exactly **three** differences, all
  **below** upstream, none above:
  - `zwp_linux_dmabuf_v1` 5 vs 6 (`stable/linux-dmabuf/linux-dmabuf-v1.xml:27`)
  - `zwp_tablet_manager_v2` 1 vs 2 (`stable/tablet/tablet-v2.xml:109`)
  - `zwp_text_input_manager_v3` 1 vs 2 (`unstable/text-input/text-input-unstable-v3.xml:585`)

  This is a host fact about advertised versions, not a statement that the compositor lacks the
  newer methods: a compositor may implement less than the latest interface version, and that
  mapping is not observable from `wayland-info`.

## Crosswalk source, revision and limits

The crosswalk was computed against a pinned upstream tree, not against page prose:

- Source: `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/archive/35d9638cf0c3f0bbf0c42996580a284f3d8ce564/wayland-protocols-35d9638cf0c3f0bbf0c42996580a284f3d8ce564.tar.gz`, fetched 2026-10-20.
- Revision: commit `35d9638cf0c3f0bbf0c42996580a284f3d8ce564`, committed 2026-10-12
  ("treewide: fix typos"), obtained from the GitLab commits API for `wayland/wayland-protocols`.
  README last touched at `3dac056d83ad8947eed6eb621f346e91da736efd` (2026-01-16, API
  `?path=README.md&per_page=1`).
- Tier: A (official upstream project).
- Interface versions were read from `<interface name="…" version="…">` tags under
  `stable/`, `staging/`, `experimental/`, `unstable/`; where a name exists in more than one
  directory, the phase-priority order stable > staging > experimental > unstable was used, matching
  the promotion rule (stable copies are canonical; staging copies are retained only for backwards
  compatibility). Names absent from all four directories are `outside`.
- Admission: used as an **upstream layout/version observation** and as the only basis for phase
  labels; phase labels are `[INF-docs]`, never host behavior.
- Rejection: not admitted as evidence of what the compositor implements. An advertised global
  proves advertisement on this socket, nothing about method support, permissions or stability.
- Flip: a per-interface host implementation claim would need either the tagged Hyprland source at
  `efb5099…` or a protocol-level probe; neither is in this seat's scope.

## Fenced claims

- `[OBS]` On 2026-10-20T04:10:03Z, `wayland-info` (rc 0, empty stderr) on socket `wayland-1`,
  session-bound to the single running Hyprland instance (see **Session binding**), against
  Hyprland 0.56.2 (`efb50993780079460b0cbed1363e2166a2de1d9f`, dirty false) listed 72 global
  advertisements covering 71 distinct interfaces; two runs agreed on set digest `9569d02f…`.
- `[OBS]` `hyprctl -j instances` (rc 0) listed 1 instance; the current
  `HYPRLAND_INSTANCE_SIGNATURE` selected exactly one record and its `wl_socket` equals
  `WAYLAND_DISPLAY=wayland-1` (2026-10-20T04:18:27Z).
- `[OBS]` `wp_drm_lease_device_v1@1` is advertised twice; all other interfaces once.
- `[OBS]` In the pinned upstream tree, 44 of the 71 distinct interfaces occur (45 advertisements)
  and 27 do not; 3 advertised versions are below the pinned upstream interface version and 0 above.
- `[INF-docs]` Phase labels (stable/staging/unstable) follow directory placement at `35d9638c`,
  per README §Protocol directory tree structure; they are not readable from name prefixes.
- `[UNK]` Whether the three version lags reflect unimplemented methods, compile-time options, or
  another cause; whether other sockets/compositor sessions advertise a different set; whether any
  advertised global is usable by a given client under its security context.

## Candidate own-work source S041

Proposed row (11 columns, contract v1 shape; L1 decides admission):

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S041 | Host Wayland globals capture — `.ufo/waves/round-13/w1/globals.json` (mado-shokunin) | own-work | A | host Hyprland 0.56.2 advertised Wayland global interface names and versions, sanitized to interface-only and session-bound to the compositor by `wl_socket` | `globals.json` @ pending round-13 w1 commit (provisional file sha256 `ced47240…`, set sha256 `9569d02f…`) | 72 advertisements / 71 interfaces reproduced by `wayland-info` rc 0; prefix does not determine phase; multiplicity must be preserved when comparing sets | queued | 2026-10-20 | 90d | — |

Flip to `mined` when both hold: (1) L1 commits the file and rebinds the sha from
`git show <wave-commit>:.ufo/waves/round-13/w1/globals.json`; (2) a U4 knowledge note cites it for
the host advertisement census. Per QUALITY criterion 7 the hash above is a work-window hash and is
labeled provisional.

## Source opens (round 13)

1. **wayland-protocols README (re-open)** — `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/main/README.md`,
   accessed 2026-10-20; revision: archive at `35d9638c…` (2026-10-12), README last-touch `3dac056d…`
   (2026-01-16); tier A.
   - Quote (§Protocol directory tree structure, `README.md:69-71`): "Stable protocols are placed in
     the `stable/` directory, staging protocols are placed in the `staging/` directory,
     experimental protocols are placed in the `experimental/` directory" (24 words).
   - Quote (§Legacy protocol phases, `README.md:61-62`): "During this phase, protocol interface
     names were, in addition to the major version postfix, also prefixed with `z` to distinguish
     them from stable protocols." (24 words).
   - Admission: fences phase attribution to directory placement and marks the `z` prefix as a
     legacy marker, which is what the crosswalk uses.
   - Rejection: not used as a host fact and not admitted as sole support for a phase list; the
     per-interface observation is the XML location in the pinned tree.
   - Flip: if S005 (same URL) is promoted to `mined` with the pinned archive anchor, the crosswalk
     can cite S005 directly and this re-open becomes redundant. S005's row was not edited.

2. **wayland-protocols pinned tree** — tarball URL above, accessed 2026-10-20; revision
   `35d9638c…`; tier A.
   - Quote (`stable/linux-dmabuf/linux-dmabuf-v1.xml:27`): `<interface name="zwp_linux_dmabuf_v1" version="6">`.
   - Admission: upstream interface names, directory placement and interface versions for the
     crosswalk only.
   - Rejection: no claim about the host beyond the advertised version numbers.
   - Flip: re-fetch on the next wayland-protocols release or before any phase re-admission.

## Replay / verification for L1 (not run by this seat)

```sh
# 1. Reproduce the host set digest (socket must exist)
wayland-info | sed -n "s/^interface: '\([^']*\)', *version: *\([0-9]*\),.*/\1@\2/p" | sort | sha256sum
# expected: 9569d02fe2b04bf62079258b1d74f5d2ad8510c26ef0710a1a64c95f1a9becaa  -

# 2. Reproduce it from the committed artifact
jq -r '.globals[] | "\(.interface)@\(.version)"' .ufo/waves/round-13/w1/globals.json | sort | sha256sum
# same digest

# 3. Counts
jq '.global_count, .unique_interface_count, .multiplicity' .ufo/waves/round-13/w1/globals.json

# 4. Bind the committed hash (after L1 commits)
git show <wave-commit>:.ufo/waves/round-13/w1/globals.json | sha256sum
```

Both replay paths were exercised at authoring time and returned the expected digest. The
`git show` binding is deliberately left to L1.

## Handoff

- Files written: this draft, `.ufo/waves/round-13/w1/globals.json`, and the scoped report at
  `.ufo/waves/round-13/w1/reports/GlobalCapture.md`.
- No shared source file, gate script, fixture or corpus file was modified; no commit, push or
  compositor mutation.
- Risks: single host, single socket, single capture time; `wayland-info` 1.3.0 is a 2020 man page
  (listing is registry-driven, so unknown extra protocols still appear); the duplicate DRM-lease
  global makes naive set comparison lossy; phase labels are upstream-layout inference.
- Blockers: none. The only unavailable input was absent `wayland-info`, resolved by the authorized
  install recorded above.
