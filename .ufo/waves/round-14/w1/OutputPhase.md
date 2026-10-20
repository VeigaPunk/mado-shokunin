# OutputPhase — round 14 / w1 (U5 boundaries, regular-source targets)

Seat: `MadoR14.OutputPhase` (scout, leaf; no subagent dispatch, no compositor mutations, no protocol execution).
Milestone: U5 boundaries and regular-source targets.
Axes: coverage, operability.

Labels: `[OBS]` observed fact; `[INF-docs]` upstream documented semantics; `[INF]` inference; `[UNK]` unexercised / unknown on host.

---

## 1. Bound official sources

Both protocol specifications were opened from official sources at pinned revisions and cross-checked against locally installed packages. No network-fetched script or untrusted mirror was accessed.

| Source | Upstream repository / canonical URL | Pinned revision / tag | Installed package & path | File SHA-256 |
|---|---|---|---|---|
| `wlr-output-management` | `https://gitlab.freedesktop.org/wlroots/wlr-protocols` | `a5028afbe4a1cf0daf020c4104c1565a09d6e58a` (most recent commit modifying file on `master` `bf4fc79abc359eea5a0edec0ac6d4a2b2955f82a`) | `extra/wlr-protocols r112.a741f0a-1`<br>`/usr/share/wlr-protocols/unstable/wlr-output-management-unstable-v1.xml` | `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7` |
| `color-management-v1` | `https://gitlab.freedesktop.org/wayland/wayland-protocols` | Tag `1.49` (`a8d65d7f121497ddd0d10f620f4284896ab80aff`; file commit `c364bf61ec0c8fed865aa6fcfd79c2078fb6d356`) | `extra/wayland-protocols 1.49-1`<br>`/usr/share/wayland-protocols/staging/color-management/color-management-v1.xml` | `18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9` |

Byte identity note: The installed file digests match the pinned upstream raw bodies byte-for-byte (`[OBS]`).

---

## 2. Primary phase, namespace, and version locations

### 2.1 `wlr-output-management`

- **Repository**: `wlroots / wlr-protocols` (`https://gitlab.freedesktop.org/wlroots/wlr-protocols`).
- **File path**: `unstable/wlr-output-management-unstable-v1.xml`.
- **Protocol name**: `wlr_output_management_unstable_v1` (line 2).
- **Primary phase**: `unstable` (experimental).
  - **Directory anchor**: `unstable/`.
  - **Text anchor**: lines 32–34.
  - **Located quote (14 words)**:
    > "The protocol described in this file is experimental and backward incompatible changes may be made."
  - **Phase policy**: Follows legacy Wayland unstable protocol conventions. Incompatible changes bump the version number in protocol/interface names (`_v2`) and reset interface versions; stabilization would remove the `z` prefix and reset the version.
- **Primary namespace**:
  - **Protocol namespace**: `wlr_` (project-local namespace for wlroots protocols).
  - **Wire interface prefix**: `zwlr_` (legacy unstable `z` prefix + `wlr` identifier).
  - **Interfaces declared**:
    - `zwlr_output_manager_v1` (manager, line 42)
    - `zwlr_output_head_v1` (head description, line 82)
    - `zwlr_output_mode_v1` (mode parameters, line 217)
    - `zwlr_output_configuration_v1` (transactional config, line 280)
    - `zwlr_output_configuration_head_v1` (per-head config, line 461)
- **Primary version location**:
  - **Protocol major version**: `1` (encoded in protocol name and `_v1` interface name suffixes).
  - **Interface version**: `4` (line 42).
  - **Exact anchor**: `<interface name="zwlr_output_manager_v1" version="4">` (line 42).
  - **Child interface versions**: `zwlr_output_head_v1` v4 (line 82), `zwlr_output_mode_v1` v3 (line 217), `zwlr_output_configuration_v1` v4 (line 280), `zwlr_output_configuration_head_v1` v4 (line 461).
- **Host advertisement**: `zwlr_output_manager_v1` version **4** (observed in `.ufo/waves/round-13/w1/globals.json:155-158`, `[OBS]`).

### 2.2 `color-management-v1`

- **Repository**: `wayland / wayland-protocols` (`https://gitlab.freedesktop.org/wayland/wayland-protocols`).
- **File path**: `staging/color-management/color-management-v1.xml`.
- **Protocol name**: `color_management_v1` (line 2).
- **Primary phase**: `staging` (testing).
  - **Directory anchor**: `staging/color-management/`.
  - **Text anchor**: lines 74–76.
  - **Located quote (24 words)**:
    > "The protocol described in this file is currently in the testing phase. Backward compatible changes may be added together with the corresponding interface version bump."
  - **Phase policy**: Governed by `wayland-protocols` README §Protocol phases and GOVERNANCE §2.3. Protocols in `staging` are intended for wider adoption; backward-compatible changes advance interface versions (`version` and `since` attributes); breaking changes strictly require a new protocol major version (`color-management-v2`).
- **Primary namespace**:
  - **Protocol namespace**: `color_management_v1` (domain-specific name without project prefix).
  - **Wire interface prefix**: `wp_` (standard Wayland Protocols prefix for cross-desktop extensions).
  - **Interfaces declared**:
    - `wp_color_manager_v1` (manager, line 80)
    - `wp_color_management_output_v1` (output color properties, line 680)
    - `wp_color_management_surface_feedback_v1` (surface color feedback, line 785)
    - `wp_image_description_creator_icc_v1` (ICC creator, line 851)
    - `wp_image_description_creator_params_v1` (parametric creator, line 906)
    - `wp_image_description_v1` (immutable image description, line 1259)
    - `wp_color_management_surface_v1` (surface color attachment, line 1673)
- **Primary version location**:
  - **Protocol major version**: `1` (encoded in protocol name and `_v1` interface name suffixes).
  - **Interface version**: `3` (line 80).
  - **Exact anchor**: `<interface name="wp_color_manager_v1" version="3">` (line 80).
  - **Child interface versions**: all child interfaces in the pinned XML declare version `3`.
  - **Revision pinning note**: Older revision `3dac056d` (the S005 README pin) declared `wp_color_manager_v1` version **2**; release tag `1.49` declares version **3** (`[OBS]`).
- **Host advertisement**: `wp_color_manager_v1` version **3** (observed in `.ufo/waves/round-13/w1/globals.json:295-298`, `[OBS]`).

---

## 3. Contrast of project and phase ownership

This section contrasts project governance, phase stability contracts, and semantic domain boundaries between the two protocols, without constructing a per-interface crosswalk.

### 3.1 Governance and repository ownership

| Dimension | `wlr-output-management` | `color-management-v1` |
|---|---|---|
| **Owning project** | `wlroots` community (`wlr-protocols`). | `wayland-protocols` multi-desktop consortium (freedesktop.org). |
| **Governance model** | Project-specific maintainership. Merge requests approved by wlroots maintainers. | Formal multi-compositor governance (`GOVERNANCE.md` §2.2, §2.3) with voting/acknowledgments from multiple independent desktop environments (GNOME, KDE Plasma, wlroots, etc.). |
| **Submission status** | Explicitly frozen for new protocols. `wlr-protocols` README states: *"New protocols should not be submitted to wlr-protocols. Instead, submit them to [wayland-protocols]."* | Active upstream venue for modern Wayland protocol extensions. |
| **Intended audience** | wlroots-based compositors and compatible clients (e.g. `wlr-randr`, kanshi). | All Wayland compositors and standard desktop clients across environments. |

### 3.2 Phase paradigm and stability guarantees

| Dimension | `wlr-output-management` | `color-management-v1` |
|---|---|---|
| **Phase designation** | `unstable` (legacy categorization). | `staging` (modern categorization). |
| **Directory location** | `unstable/` | `staging/color-management/` |
| **Naming prefix** | `zwlr_` (retains legacy `z` unstable marker). | `wp_` (standard protocol prefix; no `z`). |
| **Breaking-change policy** | Upstream warning explicitly reserves the right to make experimental breaking changes within the protocol prior to stabilization. | Breaking changes are strictly forbidden in staging without creating a new protocol major version (`_v2`). |
| **Evolution path** | Stabilization would require dropping the `z` prefix and resetting the version (a transition wlroots has not executed). | Staging protocols transition to `stable/` by consensus once proven in production, preserving interface versions and names. |

### 3.3 Semantic domain and composition boundary

| Dimension | `wlr-output-management` | `color-management-v1` |
|---|---|---|
| **Core domain** | Display hardware topology, modes, and spatial layout. | Colorimetry, transfer characteristics, and HDR metadata. |
| **Managed objects** | Heads (connectors), display modes (resolution, refresh rate), scale, transform, layout coordinates, enabled state. | Image descriptions (ICC profiles, parametric color spaces, primaries, mastering display luminance, SDR/HDR transfer functions). |
| **Operational pattern** | Transactional atomic configuration: clients stage changes across heads on a configuration object, then issue a `test` or `apply` request. | Associative and feedback model: clients query output capabilities, construct immutable image descriptions, and attach them to `wl_surface`s. |
| **Relationship to outputs** | Mutates physical/logical output topology. | Reads output color properties; does not reconfigure output layout or timing modes. |

### 3.4 Version alignment vs host capability reality

1. **Protocol major version**: Both protocols are at major version `1` (`_v1`).
2. **Interface versions**:
   - `zwlr_output_manager_v1` is at interface version **4**.
   - `wp_color_manager_v1` is at interface version **3**.
3. **Host observation**: The sanitized host capture (`globals.json`) observes Hyprland 0.56.2 advertising `zwlr_output_manager_v1` version 4 and `wp_color_manager_v1` version 3.
4. **Boundary fence**: As established in U4 (`wayland-protocol-boundaries-r13.md`), registry advertisement indicates protocol interface discovery matching the official source definitions. It does **not** prove that transactional output reconfiguration (`test`/`apply`), HDR tone mapping, or color-managed buffer rendering function correctly on this host (`[UNK]`).

---

## 4. Gate candidate decisions (for round-14 lesson)

### 4.1 Admit

- **A-OutputPhase-1 (`wlr-output-management` phase and purpose).** `zwlr_output_manager_v1` is an experimental, unstable wlroots-governed protocol in `unstable/`, designed specifically for output device configuration.
  - Quote: *"The protocol described in this file is experimental and backward incompatible changes may be made."* (14 words, XML:32–34).
  - Scope: `wlr-protocols` commit `a5028afb` / package `wlr-protocols r112.a741f0a-1`.
  - Flip: Upstream wlroots promotes the protocol to stable or merges an incompatible replacement.
- **A-OutputPhase-2 (`wlr-output-management` interface version).** The primary manager interface version in official source is 4 (`<interface name="zwlr_output_manager_v1" version="4">`, XML:42).
  - Scope: `wlr-protocols` commit `a5028afb`.
  - Flip: Upstream wlroots bumps the interface version or resets it in a major version bump.
- **A-OutputPhase-3 (`color-management-v1` phase and versioning rule).** `wp_color_manager_v1` is a staging protocol in `staging/color-management/` under `wayland-protocols` governance, where breaking changes require a new major version.
  - Quote: *"The protocol described in this file is currently in the testing phase. Backward compatible changes may be added together with the corresponding interface version bump."* (24 words, XML:74–76).
  - Scope: `wayland-protocols` tag `1.49` (commit `a8d65d7f` / file commit `c364bf61`) / package `wayland-protocols 1.49-1`.
  - Flip: Upstream `wayland-protocols` promotes the protocol to `stable/` or creates `color-management-v2`.
- **A-OutputPhase-4 (`color-management-v1` interface version 3 pin).** The primary manager interface version in official `wayland-protocols 1.49` is 3 (`<interface name="wp_color_manager_v1" version="3">`, XML:80). Prior pin `3dac056d` declared version 2; citing `3dac056d` for version 3 is invalid.
  - Scope: `wayland-protocols` tag `1.49`.
  - Flip: Upstream `wayland-protocols` releases a newer version bumping the interface version.

### 4.2 Reject

- **R-OutputPhase-1 (Staging equals stable frozen ABI).** Rejected: `color-management-v1` XML explicitly warns that the protocol is in the testing phase; under `wayland-protocols` README §Protocol phases, staging protocols are subject to evolution and are not frozen stable ABIs.
  - Flip: Upstream `wayland-protocols` formally promotes `color-management-v1` to `stable/`.
- **R-OutputPhase-2 (Interface prefix encodes protocol ownership universally).** Rejected: An interface prefix alone (`zwlr_` vs `wp_`) cannot substitute for verifying the owning repository and governing body.
  - Flip: An explicit governance authority documenting a global prefix reservation scheme across all repositories.
- **R-OutputPhase-3 (Advertised interface version proves feature execution).** Rejected: Hyprland 0.56.2 advertising `zwlr_output_manager_v1` v4 and `wp_color_manager_v1` v3 does not demonstrate that output reconfiguration transactions or HDR color pipelines execute successfully.
  - Flip: Separately authorized behavioral execution traces on the target host.
- **R-OutputPhase-4 (Reusing S005 commit `3dac056d` for `wp_color_manager_v1` v3).** Rejected: Commit `3dac056d` in `wayland-protocols` defines `wp_color_manager_v1` version 2, not version 3.
  - Flip: Verifying that `3dac056d` contains version 3 (refuted by source inspection).

### 4.3 Not admitted

- Behavioral results of `zwlr_output_configuration_v1.test` or `apply` on this host (`[UNK]`).
- Behavioral results of `wp_color_manager_v1` image description creation or HDR presentation (`[UNK]`).
- Internal implementation details of Hyprland's output or color managers (`[UNK]`).
- Complete per-interface method crosswalk (excluded by assignment boundary).

---

## 5. Verification gaps

- Read-only source and package observations were performed (`[OBS]`).
- No compositor mutations, client executions, or behavioral tests were run (`[UNK]`).
- Semantic conclusions regarding phase and governance are drawn directly from official upstream README and XML sources (`[INF-docs]`).
