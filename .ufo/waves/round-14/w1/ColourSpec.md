# ColourSpec — Primary wayland-protocols color-management-v1 XML Specification Analysis & S048 Reservation (mado-r14-w1)

**Seat:** `MadoR14.ColourSpec` (scout, leaf; no subagent dispatch, no background jobs, no commits/push).  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`.  
**Milestone:** U5 boundaries and regular-source targets.  
**Judged on:** coverage (C1), operability (C2).  
**Parent Directive (MadoR14, 2026-10-20):**  
"Parent curl -fsSL official raw1.49 XML | sha256sum succeeded matching installed exact 18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9; saved round14/evidence/colour-source-binding.txt. Choose tag1.49 source. S04035d9638 bytes differ, not used. Need exact full tag commit if available, symbolic XML anchors acceptable."  
**Draft path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/ColourSpec.md`  
**Report path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/reports/ColourSpec.md`  
**Date:** 2026-10-20.  
**Status:** complete findings; parent priority integrated; no shared repo files edited; no tests/builds/selftests run; no protocol execution.

---

## 1. Executive Summary & Bottom Line

1. **Exact Pinned Tag 1.49 Source Anchor & Binding Equality:**
   - **Chosen Source:** Upstream annotated release tag `1.49`, peeled full commit SHA: `ee78491a237eaff9389a0ccf8680521d074407d3` (annotated tag object: `a8d65d7f121497ddd0d10f620f4284896ab80aff`, committed 2026-06-07T15:06:32+02:00).
   - **Installed Host Package File:** `/usr/share/wayland-protocols/staging/color-management/color-management-v1.xml` (owned by package `wayland-protocols 1.49-1`, build date 2026-06-07).
   - **Exact Hash Match:** Both the installed file and upstream raw tag `1.49` hash to `18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9` (1,756 lines, 68,094 bytes).
   - **Binding Evidence Record:** Saved to `.ufo/waves/round-14/evidence/colour-source-binding.txt`.
   - **Explicit Rejection of 35d9638c:** Upstream `main` commit `35d9638cf0c3f0bbf0c42996580a284f3d8ce564` (used by S040 for `GOVERNANCE.md`) differs in bytes (`afa46ce1…` vs `18a2678e…` due to three typo fixes); per parent directive, **`35d9638c` is NOT used** for S048. Tag `1.49` (`ee78491a…`) is the chosen authority.

2. **Protocol Lifecycle & Staging Status:**
   - Protocol name: `color_management_v1`. Path: `staging/color-management/color-management-v1.xml`.
   - Header warning (lines 74–75, 13 words): *"Warning! The protocol described in this file is currently in the testing phase."*
   - S040 (`GOVERNANCE.md`) requires a formal 30-day minimum review process to declare a protocol stable (§2.3). `color-management-v1` has not been declared stable; it remains in the testing/staging phase.

3. **Four Core Sections Read Per Parent Directive (Symbolic & Line Anchors):**
   - **Section 526–596 (`wp_color_manager_v1` v3 Capability Negotiation):**  
     Symbolic anchors: `<interface name="wp_color_manager_v1" version="3">` events `supported_intent`, `supported_feature`, `supported_tf_named`, `supported_primaries_named`, concluded by `done` (lines 526–585). Compositors **must** support `perceptual` rendering intent (`:113-114`); all other intents and all creator features (`icc_v2_v4`, `parametric`, `windows_scrgb`, `windows_bt2100`) are optional. Unadvertised creator requests raise `unsupported_feature` fatal errors (`:99-100`).
   - **Section 634–703 (`wp_color_management_output_v1` Display Expectation):**  
     Symbolic anchors: `<interface name="wp_color_management_output_v1" version="3">`, event `image_description_changed`, request `get_image_description`. Describes output color encoding (`:672-679`). Exactly one image description active per output. Output changes trigger `image_description_changed` followed by `wl_output.done` (`:653-662`). The client must re-fetch via `get_image_description` because descriptions are immutable.
   - **Section 730–790 (`wp_color_management_surface_v1` Surface Colorimetry):**  
     Symbolic anchors: `<interface name="wp_color_management_surface_v1" version="3">`, requests `set_image_description` and `unset_image_description`. Double-buffered with copy semantics. Establishes the link between surface pixels and intended colorimetry (*"All surface contents must be readily intended for some display, but not necessarily for the display at hand."*, `:34-37`). All ready descriptions must be accepted (`:747-748`).
   - **Section 1692–1710 (`wp_image_description_info_v1.target_luminance` Theoretical Limit):**  
     Symbolic anchors: `<interface name="wp_image_description_info_v1" version="3">`, event `target_luminance`. Delivers target minimum and maximum absolute luminance $L$. Crucial theoretical limit quote (`:1701-1703`, 20 words):  
     > *"This luminance range is only theoretical and may not correspond to the luminance of light emitted on an actual display."*

4. **Falsification Guard (Protocol Requests vs. Physical Display HDR):**  
   Target luminances and mastering metadata are theoretical protocol constructs. Compositors retain full conversion discretion (lines 740–741). Host advertisement in `globals.json:295` (`wp_color_manager_v1` v3) proves wire interface availability on Hyprland 0.56.2; it does **not** prove HDR hardware output, wide-gamut panel reproduction, DRM/KMS HDR modesetting, or hardware LUT calibration.

5. **Landed Registry Row:** S048 is formally admitted and mined at `corpus/SOURCES.md:60` (Tier A, kind `spec`, tag `1.49` anchor).

---

## 2. Official Source Verification & Revision Facts

### 2.1 Upstream Repository & Exact Full Tag Commit

- **Canonical Repository:** `https://gitlab.freedesktop.org/wayland/wayland-protocols`
- **File in Tree:** `staging/color-management/color-management-v1.xml`
- **Normative Appendix:** `staging/color-management/appendix.md` (normative transfer function equations, cited at lines 60–61 and 268).
- **Tag Name:** `1.49`
- **Annotated Tag Object:** `a8d65d7f121497ddd0d10f620f4284896ab80aff`
- **Exact Full Tag Commit SHA:** `ee78491a237eaff9389a0ccf8680521d074407d3` (committed 2026-06-07T15:06:32+02:00)
- **Canonical Blob URL (tag 1.49):**  
  `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/1.49/staging/color-management/color-management-v1.xml`
- **Canonical Raw URL (tag 1.49 / commit ee78491a):**  
  `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/staging/color-management/color-management-v1.xml`
- **Installed Host Path:** `/usr/share/wayland-protocols/staging/color-management/color-management-v1.xml`
- **Installed Package:** `wayland-protocols 1.49-1` (Arch `extra`, package build date 2026-06-07).

### 2.2 Hash & Byte Identity Verification

```sh
# Verification recorded in .ufo/waves/round-14/evidence/colour-source-binding.txt:
$ sha256sum /usr/share/wayland-protocols/staging/color-management/color-management-v1.xml
18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9  /usr/share/wayland-protocols/staging/color-management/color-management-v1.xml

$ curl -fsSL https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/staging/color-management/color-management-v1.xml | sha256sum
18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9  -
```

The installed file and the upstream tag `1.49` release commit (`ee78491a…`) are **byte-for-byte identical** (1,756 lines, 68,094 bytes, sha256 `18a2678e…`).

---

## 3. Deep Analysis of the Four Parent-Directed Sections

### 3.1 Section 526–596: `wp_color_manager_v1` Capability Negotiation

Symbolic Anchor: `<interface name="wp_color_manager_v1" version="3">` (lines 80–632).
- **Event `supported_intent` (lines 526–537):**  
  Immediately sent once for each supported rendering intent. Line 531: *"A compositor must not advertise intents that are deprecated in the bound version of the interface."*
  (Mandatory vs. Optional: lines 113–114 state: *"Compositors must support the perceptual rendering intent. Other rendering intents are optional."*).
- **Event `supported_feature` (lines 539–550):**  
  Immediately sent once for each compositor supported feature in `enum feature` (0=icc_v2_v4, 1=parametric, 2=set_primaries, 3=set_tf_power, 4=set_luminances, 5=set_mastering_display_primaries, 6=extended_target_volume, 7=windows_scrgb, 8=windows_bt2100).
- **Event `supported_tf_named` (lines 552–563):**  
  Immediately sent once for each supported named transfer function.
- **Event `supported_primaries_named` (lines 565–577):**  
  Immediately sent once for each supported named primaries set.
- **Event `done` (lines 580–585):**  
  *"This event is sent when all supported rendering intents, features, transfer functions and named primaries have been sent."*
- **Request `get_image_description` (lines 587–599, since v2):**  
  Retrieves an image description backing a frozen reference (`wp_image_description_reference_v1`).
- **Architectural Boundary:** Global manager advertisement in `wl_registry` establishes only that the global object exists; capabilities and creators are dynamically discovered through this event stream. Unadvertised requests trigger `error.unsupported_feature` (lines 99–100).

### 3.2 Section 634–703: `wp_color_management_output_v1` Display Expectation

Symbolic Anchor: `<interface name="wp_color_management_output_v1" version="3">` (lines 634–702).
- **Association (lines 639–643):**  
  Associated with the `wl_output` global underlying the `wl_output` object. Client destroying `wl_output` has no impact, but compositor removing the output global makes this object inert.
- **Destructor `destroy` (lines 646–651):**  
  Destroys the object without affecting remaining protocol objects.
- **Event `image_description_changed` (lines 653–662):**  
  *"This event is sent whenever the image description of the output changed, followed by one wl_output.done event common to output events across all extensions. If the client wants to use the updated image description, it needs to do get_image_description again, because image description objects are immutable."*
- **Request `get_image_description` (lines 664–702):**  
  Creates a new `wp_image_description_v1` object for the current image description of the output.
  - Exactly one active description per output (lines 667–668).
  - Purpose quote (lines 672–679): *"The image description of an output represents the color encoding the output expects. There might be performance and power advantages, as well as improved color reproduction, if a content update matches the image description of the output it is being shown on. If a content update is shown on any other output than the one it matches the image description of, then the color reproduction on those outputs might be considerably worse."*
  - Object preserves state from creation time; delivers `ready`/`ready2`, or `failed` with `no_output` if inert, or `low_version` if client interface version is inadequate.

### 3.3 Section 730–790: `wp_color_management_surface_v1` Surface Colorimetry

Symbolic Anchor: `<interface name="wp_color_management_surface_v1" version="3">` (lines 704–790).
- **Request `set_image_description` (lines 730–778):**  
  - Sets the image description and rendering intent on the surface.
  - Double-buffered state; applied on `wl_surface.commit` (lines 735–736).
  - Client responsibility: *"It is the client's responsibility to understand the image description it sets on a surface, and to provide content that matches that image description. Compositors might convert images to match their own or any other image descriptions."* (lines 738–741).
  - Non-ready image descriptions raise protocol error `image_description` (lines 743–745).
  - All ready image descriptions **must always be accepted** by the compositor (lines 747–748, 18 words: *"All image descriptions which are ready (see wp_image_description_v1) are allowed and must always be accepted by the compositor."*).
  - Render intent must be one advertised via `supported_intent`, else protocol error `render_intent` (lines 757–760).
  - Copy semantics: destroying the image description object after this request does not affect the pending or committed surface state (lines 768–770).
- **Request `unset_image_description` (lines 780–789):**  
  Removes any image description from the surface. Double-buffered (`wl_surface.commit`). Default behavior for unadorned surfaces is compositor-defined (should treat as sRGB, lines 763–765).

### 3.4 Section 1692–1710: `wp_image_description_info_v1.target_luminance` Theoretical Limit

Symbolic Anchor: `<interface name="wp_image_description_info_v1" version="3">`, `<event name="target_luminance">` (lines 1692–1710).
- **Event `target_luminance` (lines 1692–1710):**  
  Provides the luminance range (minimum and maximum absolute luminance $L$) that the image description targets. Compatible with SMPTE ST 2086 HDR static metadata for mastering displays.
- **The Exact Theoretical Limit Quote (lines 1701–1703, 20 words):**  
  > *"This luminance range is only theoretical and may not correspond to the luminance of light emitted on an actual display."*
- **Additional Theoretical Limits in Same Section:**  
  - `target_max_cll` (lines 1717–1719, 20 words): *"This luminance is only theoretical and may not correspond to the luminance of light emitted on an actual display."*
  - `target_max_fall` (lines 1729–1731, 20 words): *"This luminance is only theoretical and may not correspond to the luminance of light emitted on an actual display."*
- **Significance for U5 Falsification Boundary:**  
  Protocol metadata (even when explicitly targeting HDR mastering luminances up to 10,000 cd/m² via ST 2084 PQ or Windows scRGB/BT.2100) describes mathematical image encoding, **not** physical light emitted by hardware displays.

---

## 4. Contract-Required Source Open Records (S048 Landed Row)

### 4.1 Primary Source Open Entry

- **Source ID:** S048
- **Source Identity:** wayland-protocols color-management-v1 XML specification
- **Canonical URL:** `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/staging/color-management/color-management-v1.xml`
- **Pinned Revision:** Annotated tag `1.49` (full commit `ee78491a237eaff9389a0ccf8680521d074407d3`, 2026-06-07; byte-identical to installed package `wayland-protocols 1.49-1`).
- **Date Opened:** 2026-10-20.
- **Blob SHA-256:** `18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9` (1,756 lines, 68,094 bytes).
- **Kind / Tier:** `spec` / Tier A.
- **Scope:** `Documented colour-manager support events and image descriptions, not measured HDR or physical colour accuracy`
- **Status:** `mined` (cites `corpus/knowledge/output-colour-boundaries-r14.md`).
- **Recheck Policy:** `on-release`

### 4.2 Mined Located Quotes (≤ 25 words each, verified against tag 1.49 bytes)

| Ref | Section / Lines | Exact Text | Word Count | Architectural Topic |
|---|---|---|---|---|
| Q1 | §Intro :32–34 | "The aim of the color management extension is to allow clients to know the color properties of outputs" | 18 words | Output color discovery purpose |
| Q2 | §Intro :34–37 | "All surface contents must be readily intended for some display, but not necessarily for the display at hand." | 18 words | Surface intention vs display reality |
| Q3 | §Intro :42–44 | "The color properties are represented as an image description object which is immutable after it has been created." | 18 words | Immutable image description abstraction |
| Q4 | §Intro :74–75 | "Warning! The protocol described in this file is currently in the testing phase." | 13 words | Staging testing lifecycle status |
| Q5 | §Manager :88 | "Compositors should never remove this global." | 6 words | Singleton persistence requirement |
| Q6 | §Manager :113–114 | "Compositors must support the perceptual rendering intent. Other rendering intents are optional." | 12 words | Mandatory vs optional rendering intents |
| Q7 | §526–596 :580–583 | "This event is sent when all supported rendering intents, features, transfer functions and named primaries have been sent." | 18 words | Manager capability negotiation completion |
| Q8 | §634–703 :653–656 | "This event is sent whenever the image description of the output changed, followed by one wl_output.done event" | 17 words | Output image description dynamic update |
| Q9 | §730–790 :747–748 | "All image descriptions which are ready (see wp_image_description_v1) are allowed and must always be accepted by the compositor." | 18 words | Surface ready image description acceptance rule |
| Q10 | §730–790 :768–770 | "Setting the image description has copy semantics; after this request, the image description can be immediately destroyed" | 18 words | Surface attachment copy semantics |
| Q11 | §Feedback :894–895 | "The preferred image description is not automatically used for anything. It is only a hint" | 15 words | Surface feedback non-binding hint |
| Q12 | §1692–1710 :1701–1703 | "This luminance range is only theoretical and may not correspond to the luminance of light emitted on an actual display." | 20 words | Theoretical luminance limit quote |

### 4.3 Landed SOURCES.md Registry Row (11 Columns, Tag 1.49 Primary Anchor)

From `corpus/SOURCES.md:60`:
```markdown
| S048 | Colour-management XML — https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/staging/color-management/color-management-v1.xml | spec | A | Documented colour-manager support events and image descriptions, not measured HDR or physical colour accuracy | tag 1.49; wp_color_manager_v1 supported_* and done; output get_image_description; surface set_image_description; wp_image_description_info_v1 target_luminance; raw sha256 18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9 | Separates manager capability events, output/surface image descriptions and theoretical luminance from actual light emitted by a display | mined | 2026-10-20 | on-release | corpus/knowledge/output-colour-boundaries-r14.md |
```

### 4.4 Rejection and Flip Register

| Proposed Claim | Disposition | Grounding Evidence | Flip Condition |
|---|---|---|---|
| Advertised `wp_color_manager_v1` v3 proves HDR display or wide gamut is operating | **REJECT** | S048 lines 1701–1703 (*"luminance range is only theoretical"*); `globals.json:336` (colorimetry excluded) | Separately authorized hardware/DRM KMS display test |
| `color-management-v1` is a stable protocol | **REJECT** | S048 lines 74–75 (*"currently in the testing phase"*); S040 §2.3 (requires formal declaration) | Promotion to `stable/` namespace in wayland-protocols release |
| `set_image_description` guarantees identical physical color reproduction | **REJECT** | S048 lines 740–741 (*"Compositors might convert images"*); lines 34–37 (intended for some display, not hand) | Colorimeter-verified physical display calibration run |
| All creator features (ICC, parametric, Windows scRGB/BT.2100) are universally supported | **REJECT** | S048 lines 139–169, 539–550; unsupported requests raise protocol error `unsupported_feature` | Per-connection server `supported_feature` event observation |
| Preferred image description is automatically applied by compositor | **REJECT** | S048 lines 894–895 (*"not automatically used for anything. It is only a hint"*); lines 896–898 | Specification change altering feedback semantics |
| Output image description is permanently immutable | **REJECT** | S048 lines 653–662 (`image_description_changed` event signals output color property updates) | Specification freezing output descriptions |

---

## 5. Outside Spot-Check Rulings Addressed (R13-V1, R13-V2, R13-V3)

1. **R13-V1 (Retained-Data Wording Precision):**
   - *Clarified Standard:* Global records contain `interface` and `version` only; sanitized probe execution metadata (tool binary, package, exit code) and session correlation metadata (socket `wayland-1`, instance match flags) are also legitimately retained.
   - *Colour Exclusion Record:* Line 336 of `globals.json` explicitly lists `"wp_color_manager_v1 display colorimetry blocks"` under `excluded`. Physical display colorimetry was intentionally excluded from the captured record.
2. **R13-V2 (Within-Run Boundary vs. Cross-Revision Output Equality):**
   - Citing tag `1.49` aligns directly with the installed package file `wayland-protocols 1.49-1` (`18a2678e…`).
   - Within-run file-plane verification proves package file stability during execution; tag `1.49` provides byte-identical upstream equality, completely superseding the need to reference the unreleased `35d9638c` commit.
3. **R13-V3 (Standalone Receipt Measured Digest):**
   - Full 64-character hexadecimal SHA-256 digests (`18a2678e…`), exact tag commit `ee78491a237eaff9389a0ccf8680521d074407d3`, and literal verification commands recorded in `.ufo/waves/round-14/evidence/colour-source-binding.txt`.

---

## 6. Synthesis for U5 Knowledge Note & Verification Checks

### 6.1 U5 Knowledge Facets Verification Table (Target: `measure.py`)

From `corpus/knowledge/output-colour-boundaries-r14.md` (lines 12–18), which satisfies `table_facets` in `measure.py`:

| Question | Evidence that answers it | What remains unproved |
|---|---|---|
| **Output management:** what does a configuration test or apply reply mean? | `[INF-docs]` S047 distinguishes the current-state serial, a proposed full head configuration, validation-only `test`, state-changing `apply`, and `succeeded`/`failed`/`cancelled`. | `[UNK]` This host's acceptance, requested-versus-actual state, hotplug race handling, rendering and persistence. |
| **Colour management:** which colour properties does the protocol describe? | `[INF-docs]` S048 separates manager support events, an output's immutable image-description snapshot, a surface's preferred description and a client-set surface description. | `[UNK]` Actual supported feature events, ICC processing, tone mapping, HDR signal path, panel luminance and colour accuracy. |
| Does the intended **feature** actually work? | `[UNK]` Requires an authorized feature-specific observation, including the exact request, reply and resulting state or physical measurement as appropriate. | Upstream XML, matching interface versions and retained registry records alone cannot answer this. |

### 6.2 Literal Re-Derivation Commands (Criterion 6)

```sh
# 1. Verify byte-equality of installed package XML and upstream tag 1.49
sha256sum /usr/share/wayland-protocols/staging/color-management/color-management-v1.xml
# Expected: 18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9

curl -fsSL https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/staging/color-management/color-management-v1.xml | sha256sum
# Expected: 18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9

# 2. Verify theoretical luminance limit quote at lines 1701-1703
sed -n '1701,1703p' /usr/share/wayland-protocols/staging/color-management/color-management-v1.xml
# Expected:
#         This luminance range is only theoretical and may not correspond to the
#         luminance of light emitted on an actual display.

# 3. Verify historical host advertisement of color manager v3 in globals.json
jq -e '.globals[] | select(.interface == "wp_color_manager_v1") | .version == 3' .ufo/waves/round-13/w1/globals.json
# Expected: true (exit code 0)
```
