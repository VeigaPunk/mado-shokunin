# OutputPhase — rendered report (mado-r14-w1)

Date: 2026-10-20. Seat: `MadoR14.OutputPhase` (scout, leaf). Milestone: U5 boundaries and regular-source targets. Axes: coverage, operability.

## Behavior

Investigated the primary phase, namespace, and version locations for `wlr-output-management` and `color-management-v1` from official sources and contrasted project/phase ownership without constructing a per-interface crosswalk. Read-only package and official upstream sources only; no protocol client or compositor mutations executed.

Full findings: `.ufo/waves/round-14/w1/OutputPhase.md`.

## Official sources bound

| Specification | Project / Canonical URL | Pinned revision / tag | Installed package & path | File SHA-256 |
|---|---|---|---|---|
| `wlr-output-management` | `wlroots / wlr-protocols`<br>`https://gitlab.freedesktop.org/wlroots/wlr-protocols` | Commit `a5028afbe4a1cf0daf020c4104c1565a09d6e58a` (on `master` `bf4fc79a`) | `wlr-protocols r112.a741f0a-1`<br>`/usr/share/wlr-protocols/unstable/wlr-output-management-unstable-v1.xml` | `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7` |
| `color-management-v1` | `wayland / wayland-protocols`<br>`https://gitlab.freedesktop.org/wayland/wayland-protocols` | Release tag `1.49` (`a8d65d7f`; file commit `c364bf61`) | `wayland-protocols 1.49-1`<br>`/usr/share/wayland-protocols/staging/color-management/color-management-v1.xml` | `18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9` |

Byte identity: Installed package files match upstream raw contents byte-for-byte (`[OBS]`).

## Findings

### 1. Primary phase, namespace, and version locations

- **`wlr-output-management`**:
  - **Phase**: `unstable` (experimental). Directory: `unstable/`. Text anchor: lines 32–34.
    - Located quote (14 words): *"The protocol described in this file is experimental and backward incompatible changes may be made."*
  - **Namespace**: `wlr_` protocol namespace; `zwlr_` wire interface prefix (legacy unstable `z` prefix).
    - Interfaces: `zwlr_output_manager_v1`, `zwlr_output_head_v1`, `zwlr_output_mode_v1`, `zwlr_output_configuration_v1`, `zwlr_output_configuration_head_v1`.
  - **Version**: Protocol major version `1` (`_v1`); interface version **4** (`<interface name="zwlr_output_manager_v1" version="4">`, line 42).
  - **Host advertisement**: Hyprland 0.56.2 advertises `zwlr_output_manager_v1` version **4** (`globals.json:155-158`, `[OBS]`).

- **`color-management-v1`**:
  - **Phase**: `staging` (testing). Directory: `staging/color-management/`. Text anchor: lines 74–76.
    - Located quote (24 words): *"The protocol described in this file is currently in the testing phase. Backward compatible changes may be added together with the corresponding interface version bump."*
  - **Namespace**: `color_management_v1` protocol namespace; `wp_` wire interface prefix (standard Wayland Protocols prefix).
    - Interfaces: `wp_color_manager_v1`, `wp_color_management_output_v1`, `wp_color_management_surface_feedback_v1`, `wp_image_description_creator_icc_v1`, `wp_image_description_creator_params_v1`, `wp_image_description_v1`, `wp_color_management_surface_v1`.
  - **Version**: Protocol major version `1` (`_v1`); interface version **3** (`<interface name="wp_color_manager_v1" version="3">`, line 80).
  - **Revision mismatch check**: Commit `3dac056d` (the S005 README pin) declared version **2**; release tag `1.49` declares version **3**, matching installed `wayland-protocols 1.49-1` and host advertisement.
  - **Host advertisement**: Hyprland 0.56.2 advertises `wp_color_manager_v1` version **3** (`globals.json:295-298`, `[OBS]`).

### 2. Contrast of project and phase ownership

1. **Governance & project ownership**:
   - `wlr-output-management` belongs to `wlroots / wlr-protocols`. It is maintained project-locally for wlroots-compatible compositors and is closed to new protocols (README: *"New protocols should not be submitted to wlr-protocols. Instead, submit them to [wayland-protocols]."*).
   - `color-management-v1` belongs to `wayland / wayland-protocols` under freedesktop.org. It is governed by multi-compositor consensus (`GOVERNANCE.md` §2.2/§2.3) across GNOME, KDE, wlroots, Red Hat, Collabora, and AMD.
2. **Phase paradigm & stability contracts**:
   - `wlr-output-management` remains in `unstable/` with `z` prefix (`zwlr_`). Incompatible changes can be made at any time; stabilization requires dropping `z` and resetting version.
   - `color-management-v1` is in `staging/` with `wp_` prefix. Under `wayland-protocols` rules, breaking changes within staging strictly require a new protocol major version (`_v2`); minor additions bump interface versions.
3. **Semantic domains**:
   - Output management governs **display hardware topology and layout**: heads, display modes, positions, transforms, scale, and atomic configuration transactions (`test` / `apply`).
   - Color management governs **colorimetry, transfer curves, and HDR metadata**: attaching image descriptions to surfaces and querying output color capabilities without modifying layout or timing modes.
4. **Advertisement vs feature execution**:
   - Host `globals.json` demonstrates interface discovery matching official upstream definitions (v4 and v3).
   - Registry presence does **not** prove working configuration transactions or HDR presentation pipelines on the host (`[UNK]`).

## Lesson Gate candidates

- **Admit:**
  - `zwlr_output_manager_v1` is an experimental unstable protocol in `unstable/` (wlr-protocols commit `a5028afb`, line 42, interface v4).
  - `wp_color_manager_v1` is a staging protocol in `staging/color-management/` under wayland-protocols governance (tag `1.49`, line 80, interface v3).
  - Tag `1.49` is required for version 3; older commit `3dac056d` defined version 2.
- **Reject:**
  - Staging phase equals a frozen stable ABI.
  - Interface prefixes universally identify ownership without repository verification.
  - Registry advertisement proves output reconfiguration or HDR feature behavior.
  - Pinning `3dac056d` for version 3 claims.
- **Not admitted:**
  - Host execution behavior of `test`/`apply` or color-management rendering (`[UNK]`).
  - Per-interface method crosswalk.

## Routing

- `SourceInventory` / `ColourSpec`: S048 must pin `wayland-protocols` tag `1.49` (`a8d65d7f` / file commit `c364bf61`), not `3dac056d`, to match interface version 3.
- `OutputSpec` / `WlrVersion`: S047 binds to `wlr-protocols` `unstable/wlr-output-management-unstable-v1.xml` commit `a5028afb` (sha256 `65b0f82a…`), declaring interface version 4.
