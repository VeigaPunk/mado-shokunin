# ColourSpec — rendered report (mado-r14-w1)

Full findings: `.ufo/waves/round-14/w1/ColourSpec.md`. Read-only upstream repository discovery and package observation; parent priority integrated; no tests executed; no client connections to compositor; no protocol execution.

## Findings

1. **Exact Pinned Tag 1.49 Source Anchor & Binding Equality:**
   - **Pinned Upstream Revision:** Upstream annotated release tag `1.49`, peeled full commit SHA: `ee78491a237eaff9389a0ccf8680521d074407d3` (annotated tag object: `a8d65d7f121497ddd0d10f620f4284896ab80aff`, committed 2026-06-07).
   - **Installed System Package File:** `/usr/share/wayland-protocols/staging/color-management/color-management-v1.xml` (owned by `wayland-protocols 1.49-1`, build date 2026-06-07).
   - **Exact Hash Match:** Both installed file and upstream raw tag `1.49` hash to `18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9` (1,756 lines, 68,094 bytes).
   - **Binding Evidence Record:** Saved to `.ufo/waves/round-14/evidence/colour-source-binding.txt`.
   - **Explicit Rejection of 35d9638c:** Upstream `main` commit `35d9638cf0c3f0bbf0c42996580a284f3d8ce564` (used by S040 for `GOVERNANCE.md`) differs in bytes (`afa46ce1…` vs `18a2678e…` due to three typo fixes); per parent directive, **`35d9638c` is NOT used** for S048. Tag `1.49` (`ee78491a…`) is the chosen authority.

2. **Protocol Lifecycle & Staging Status:**
   - Lives under `staging/color-management/color-management-v1.xml`.
   - Header warning (lines 74–75, 13 words): *"Warning! The protocol described in this file is currently in the testing phase."*
   - S040 (`GOVERNANCE.md` @ tag `1.49`) sets the procedure for declaring protocols stable (§2.3, 30-day minimum discussion), but `color-management-v1` has not been promoted to `stable/`. It is in the testing/staging phase.

3. **Four Core Sections Read Per Parent Directive (Symbolic & Line Anchors):**
   - **Section 526–596 (`wp_color_manager_v1` v3 Capability Negotiation):**  
     Symbolic anchors: `<interface name="wp_color_manager_v1" version="3">` events `supported_intent`, `supported_feature`, `supported_tf_named`, `supported_primaries_named`, concluded by `done` (lines 526–585). Global singleton interface (version 3). Persistence requirement: *"Compositors should never remove this global."* (line 88, 6 words).  
     **Mandatory vs. Optional:** Compositors **must** support `perceptual` rendering intent (value 0). Other intents (`relative`, `saturation`, `absolute`, `relative_bpc`, `absolute_no_adaptation`) are optional (lines 113–114, 12 words: *"Compositors must support the perceptual rendering intent. Other rendering intents are optional."*).  
     All creator features (`icc_v2_v4`, `parametric`, `windows_scrgb`, `windows_bt2100`) require explicit advertisement; unadvertised requests raise fatal protocol error `unsupported_feature` (lines 99–100, 449, 466, 516, 622).
   - **Section 634–703 (`wp_color_management_output_v1` Display Expectation):**  
     Symbolic anchors: `<interface name="wp_color_management_output_v1" version="3">`, event `image_description_changed`, request `get_image_description`. Describes what color encoding the physical output expects (lines 32–34, 18 words: *"The aim of the color management extension is to allow clients to know the color properties of outputs"*). Exactly one image description active per output. Output changes trigger `image_description_changed` followed by `wl_output.done` (lines 653–661). Clients must fetch a new description via `get_image_description` because descriptions are immutable.
   - **Section 730–790 (`wp_color_management_surface_v1` Surface Colorimetry):**  
     Symbolic anchors: `<interface name="wp_color_management_surface_v1" version="3">`, requests `set_image_description` and `unset_image_description`. Allows clients to set surface colorimetry via double-buffered `set_image_description` (copy semantics). Surface intent principle: *"All surface contents must be readily intended for some display, but not necessarily for the display at hand."* (lines 34–37, 18 words). All ready descriptions **must always be accepted** by the compositor (lines 747–748, 18 words). Copy semantics: destroying description object does not affect surface state (lines 768–770). Default when unset: compositor implementation-defined (should treat as sRGB).
   - **Section 1692–1710 (`wp_image_description_info_v1.target_luminance` Theoretical Limit):**  
     Symbolic anchors: `<interface name="wp_image_description_info_v1" version="3">`, event `target_luminance`. Provides target luminance range (minimum and maximum absolute luminance $L$).  
     **Theoretical Limit Quote (lines 1701–1703, 20 words):**  
     > *"This luminance range is only theoretical and may not correspond to the luminance of light emitted on an actual display."*  
     Repeated for `target_max_cll` (lines 1717–1719) and `target_max_fall` (lines 1729–1731).

4. **Protocol Requests vs. Physical HDR on Display (Falsification Boundary):**  
   - Parametric requests (`set_luminances`, `set_mastering_display_primaries`, `set_mastering_luminance`, `set_max_cll`, `set_max_fall`) and Windows helpers (`create_windows_scrgb`, `create_windows_bt2100`) define software colorimetry metadata.
   - Compositors retain conversion discretion: *"Compositors might convert images to match their own or any other image descriptions."* (lines 740–741). Attaching an image description does not guarantee that pixel values pass through without gamut remapping, tone compression, or clipping.
   - **Falsification Guard:** Historical advertisement of `wp_color_manager_v1` v3 (`globals.json:295`) proves wire interface presence on Hyprland 0.56.2; it does **not** prove that the attached monitor is HDR-capable, that DRM/KMS HDR modesetting is active, that 10-bit/12-bit/FP16 scanout is occurring, or that hardware color calibration LUTs are configured.

5. **Landed SOURCES.md Registry Row (11 Columns, Tag 1.49 Primary Anchor):**
From `corpus/SOURCES.md:60`:
```markdown
| S048 | Colour-management XML — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/staging/color-management/color-management-v1.xml | spec | A | Documented colour-manager support events and image descriptions, not measured HDR or physical colour accuracy | tag 1.49; wp_color_manager_v1 supported_* and done; output get_image_description; surface set_image_description; wp_image_description_info_v1 target_luminance; raw sha256 18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9 | Separates manager capability events, output/surface image descriptions and theoretical luminance from actual light emitted by a display | mined | 2026-10-20 | on-release | corpus/knowledge/output-colour-boundaries-r14.md |
```

6. **Rejection and Flip Register:**
   - *Claim:* Advertised `wp_color_manager_v1` v3 proves HDR display or wide gamut is operating.  
     *Disposition:* **REJECT** (S048 lines 1701–1703; `globals.json:336` colorimetry excluded). *Flip:* Separately authorized hardware/DRM display test.
   - *Claim:* `color-management-v1` is a stable protocol.  
     *Disposition:* **REJECT** (S048 lines 74–75 testing phase; S040 §2.3). *Flip:* Formal promotion to `stable/` in wayland-protocols release.
   - *Claim:* `set_image_description` guarantees identical physical color reproduction.  
     *Disposition:* **REJECT** (S048 lines 740–741; lines 34–37). *Flip:* Colorimeter-verified hardware calibration run.
   - *Claim:* All creator features (ICC, parametric, Windows scRGB/BT.2100) are universally supported.  
     *Disposition:* **REJECT** (S048 lines 139–169, 539–550; unsupported requests raise error). *Flip:* Per-connection `supported_feature` event observation.
   - *Claim:* Preferred image description is automatically applied by compositor.  
     *Disposition:* **REJECT** (S048 lines 894–895 hint). *Flip:* Specification change altering feedback semantics.

7. **Outside Spot-Check Corrections (R13-V1, R13-V2, R13-V3):**
   - **R13-V1:** Global records contain interface and version only; sanitized probe and session metadata is also retained. Line 336 of `globals.json` explicitly excluded `"wp_color_manager_v1 display colorimetry blocks"`.
   - **R13-V2:** File-plane verification proves within-run package file stability (`18a2678e…`), while tag `1.49` provides byte-identical upstream equality, completely superseding the need to reference the unreleased `35d9638c` commit.
   - **R13-V3:** All sources carry full 64-character SHA-256 digests and Git commit SHAs, preserved in `.ufo/waves/round-14/evidence/colour-source-binding.txt`.

## Judgement

- **Coverage (C1):** Establishes official tag `1.49` upstream equality, confirms S048 landed with complete 11-column registry fields, and grounds the 3 required U5 facets (output management, colour, feature unknown) to advance U-item coverage from 4/7 (5.7143/10) to 5/7 (7.1429/10).
- **Operability (C2):** Provides byte-verified URLs, commit SHAs, line numbers, and located quotes (≤25 words) without running tests or mutating compositor state.

## Gaps & Unknowns

- No live color management protocol requests were transmitted to the compositor (`[UNK]`).
- Compositor color transform pipeline, shader precision, and display driver HDR metadata pass-through remain unexercised.

## Tooling

None installed or upgraded.

## Checks L1 Should Run Once

```sh
# 1. Verify byte-equality of installed package XML and upstream tag 1.49
sha256sum /usr/share/wayland-protocols/staging/color-management/color-management-v1.xml
# Expected: 18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9

curl -fsSL https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/staging/color-management/color-management-v1.xml | sha256sum
# Expected: 18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9

# 2. Verify theoretical luminance limit quote at lines 1701-1703
sed -n '1701,1703p' /usr/share/wayland-protocols/staging/color-management/color-management-v1.xml

# 3. Verify historical host advertisement in globals.json
jq -e '.globals[] | select(.interface == "wp_color_manager_v1") | .version == 3' .ufo/waves/round-13/w1/globals.json
# Expected: true (exit code 0)
```
