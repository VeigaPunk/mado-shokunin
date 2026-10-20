# EvidenceChain — Connect U4 announcement/bind limits to U5 output management and colour semantics; supply the three-row falsification boundary table

**Seat:** `MadoR14.EvidenceChain` (connector, leaf)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Milestone:** U5 boundaries and regular-source targets  
**Axes judged on:** `coverage`, `operability`  
**Status:** Complete findings and synthesis draft; no mutating commands, no shared-file edits.

---

## 1. Executive Summary & Named Proposal

### Non-Obvious Move: The Three-Tier Transactional & Capability-Negotiation Disconnect
We synthesize round-14's inputs into a verifiable evidence bridge that connects the established **U4 announcement and bind limits** directly to **U5 output-management (`zwlr_output_manager_v1`) and colour-management (`wp_color_manager_v1`) semantics**.

In Round 13 (U4), the lane established the core architectural truth:
$$\text{Advertisement} \neq \text{Protocol Binding} \neq \text{Runtime Behavior}$$

In Round 14 (U5), we show why advertising an interface in `wl_registry.global` fails even more drastically for complex configuration and colour subsystems:
1. **Output Management is Transactional and Falsifiably Decoupled from State Application:**
   * Advertising `zwlr_output_manager_v1` (v4) does not expose display heads or modes.
   * Binding `zwlr_output_manager_v1` does not grant configuration authority; the client must observe `head` and `mode` events and await `done(serial)`.
   * Configuration is an explicit two-phase commit via `create_configuration(serial)`. Crucially, upstream protocol specification (`wlr-output-management-unstable-v1.xml:486-487`) explicitly states: *"Even if the compositor succeeds to test a configuration, applying it may fail."* Moreover, a successful `apply` request carries no guarantee of exact match (`:470-473`), and hotplug invalidations emit `cancelled` (`:518-522`).
   * Therefore, advertising `zwlr_output_manager_v1` does not license asserting that output reconfiguration, resolution switching, custom modes, or adaptive sync are functional or applied.
2. **Colour Management Requires Dynamic Multi-Event Negotiation Before Creators Can Function:**
   * Advertising `wp_color_manager_v1` (v3) does not prove support for HDR, wide gamuts, or specific colorimetry formats.
   * Binding `wp_color_manager_v1` does not license invoking profile creators (`create_parametric_creator`, `create_icc_creator`, `create_windows_scrgb`); the compositor must first emit `supported_feature`, `supported_intent`, `supported_tf_named`, and `supported_primaries_named` events. Invoking an unsupported request triggers fatal protocol error `unsupported_feature` (`color-management-v1.xml:99-100`).
   * Even when image descriptions are attached to surfaces (`set_image_description`), this denotes content intention, not physical display pipeline capability. The protocol description explicitly acknowledges: *"All surface contents must be readily intended for some display, but not necessarily for the display at hand."* (`:34-37`).
   * Therefore, advertising `wp_color_manager_v1` does not license claiming working HDR display presentation, wide-gamut hardware reproduction, or colorimetric precision.
3. **Substrate & Domain Separation Protects the Hermetic Boundary:**
   * Read-only gate observation cannot and must not issue mutating `apply` requests or attach colorimetric surfaces.
   * Hardware modesetting, CRTC allocation, and DRM leasing belong strictly to the kernel/KMS plane (sibling `tsukuroi` province, not `mado`).
   * Addressing outside reviews **R13-V1**, **R13-V2**, and **R13-V3** hardens the boundary between observed headers, single-run config hashes, and cross-revision outputs.

This move directly improves **coverage** (C1: grounded U5 protocol boundary, moving U-items from 4/7 [5.7143/10] to 5/7 [7.1429/10] without feature exercise) while preserving **operability** (C2: prevents false-positive feature claims, maintains hermetic gate boundaries, and isolates diagnostic observation from hardware execution).

---

## 2. Grounded Evidence Corpus & Exact Citations

All citations are grounded in primary, read-only sources opened in this round:

### S047 (Reserved) — `wlr-output-management-unstable-v1.xml` (wlr-protocols)
* **Location:** `/usr/share/wlr-protocols/unstable/wlr-output-management-unstable-v1.xml` (installed package `wlr-protocols r112.a741f0a-1`, pacman extra) & upstream `https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/master/unstable/wlr-output-management-unstable-v1.xml` (commit `a741f0a`).
* **Anchors & Quotes (≤25 words):**
  * *Purpose:* `"This protocol exposes interfaces to obtain and modify output device configuration."` (`wlr-output-management-unstable-v1.xml:29-30`)
  * *Experimental warning:* `"Warning! The protocol described in this file is experimental and backward incompatible changes may be made."` (`:32-34`)
  * *Test vs apply limitation:* `"Even if the compositor succeeds to test a configuration, applying it may fail."` (`:486-487`)
  * *No exact state match guarantee:* `"In case the configuration is successfully applied, there is no guarantee that the new output state matches completely the requested configuration."` (`:470-473`)
  * *Hotplug race cancellation:* `"Sent if the compositor cancels the configuration because the state of an output changed and the client has outdated information"` (`:518-522`)
* **Role in U5:** Establishes the transactional, multi-phase lifecycle of output management; provides primary authority proving that configuration testing and application can fail independently of manager existence.

### S048 (Reserved) — `color-management-v1.xml` (wayland-protocols)
* **Location:** `/usr/share/wayland-protocols/staging/color-management/color-management-v1.xml` (installed package `wayland-protocols 1.49-1`, pacman extra) & upstream `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/main/staging/color-management/color-management-v1.xml` (tag `1.49`).
* **Anchors & Quotes (≤25 words):**
  * *Scope:* `"The aim of the color management extension is to allow clients to know the color properties of outputs"` (`color-management-v1.xml:32-34`)
  * *Staging status:* `"Warning! The protocol described in this file is currently in the testing phase."` (`:74-75`)
  * *Surface intention vs display reality:* `"All surface contents must be readily intended for some display, but not necessarily for the display at hand."` (`:34-37`)
  * *Mandatory vs optional intents:* `"Compositors must support the perceptual rendering intent. Other rendering intents are optional."` (`:113-114`)
  * *Feature negotiation requirement:* `enum feature` (`:139-169`) and `event supported_feature` (`:539-551`); unsupported requests trigger `error.unsupported_feature` (`:99-100`).
* **Role in U5:** Establishes that colour manager global advertisement does not certify display HDR or wide gamut capabilities; proves dynamic per-connection capability negotiation is required before creators or render intents can be used.

### S041 — Sanitized Host Registry Capture
* **Location:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/globals.json`
* **Observed Entries:**
  * Line 155: `{"interface": "zwlr_output_manager_v1", "version": 4}`
  * Line 295: `{"interface": "wp_color_manager_v1", "version": 3}`
  * Lines 332-343: `excluded` array explicitly records dropped hardware details:
    * `"wl_output name/description/x/physical_width/make/subpixel_orientation/mode"`
    * `"zxdg_output_manager_v1 logical output identifiers"`
    * `"wp_color_manager_v1 display colorimetry blocks"`
    * `"wp_drm_lease_device_v1 device paths"`
* **Role in U5:** Provides ground truth that the host compositor (Hyprland 0.56.2 `efb50993...`) advertises these exact interface headers without retaining sensitive or unverified hardware configurations.

### S046 — Upstream Diagnostic Implementation (`wayland-info.c`)
* **Location:** `https://gitlab.freedesktop.org/wayland/wayland-utils/-/raw/1.3.0/wayland-info/wayland-info.c` (tag `1.3.0` @ `d01edd68...`)
* **Anchors & Functionality:**
  * `global_handler` (:3125-3163) binds advertised interfaces to query read-only parameters.
  * Colour manager detail queries (:2744, :2750) bind and issue `get_information` / `get_output`.
* **Role in U5:** Grounds the distinction between diagnostic read-only binding/queries and functional client feature requests.

---

## 3. The Three-Row Falsification Boundary Table

The following table connects U4 announcement/bind limits to U5 output-management and colour semantics, establishing the strict boundary preventing advertised-feature claims:

| Domain / Observed Fact | Grounded Evidence Source | What It Does NOT License (Adversarial Falsification Boundary) |
|---|---|---|
| **1. Output Management Transactional Boundary**<br><br>The compositor advertises `zwlr_output_manager_v1` (version 4) in the Wayland registry. The upstream protocol defines head/mode enumeration, transactional configuration (`create_configuration`), validation testing (`test`), and state application (`apply`). | • `.ufo/waves/round-13/w1/globals.json:155` (`zwlr_output_manager_v1` @ 4)<br>• Installed `wlr-output-management-unstable-v1.xml` (r112.a741f0a-1, **S047**)<br>• `/usr/include/hyprland/protocols/wlr-output-management-unstable-v1.hpp`<br>• Pinned Hyprland 0.56.2 | **Does NOT license:**<br>1. Claiming that display resolution changes, custom modes, head disabling/enabling, scale adjustments, or adaptive sync are functional or applied on this desktop.<br>2. Inferring connected monitor count, physical geometry, EDID identities, or DRM connector mappings from manager advertisement.<br>3. Equating successful configuration validation (`test`) with application success (refuted by S047: *"Even if the compositor succeeds to test a configuration, applying it may fail"*).<br>4. Assuming configuration requests are race-free or immutable across hotplug events (invalidated by S047 `cancelled` event). |
| **2. Colour Management Capability-Negotiation Boundary**<br><br>The compositor advertises `wp_color_manager_v1` (version 3) in the Wayland registry. The upstream staging protocol defines extension interfaces for surfaces/outputs and dynamic negotiation of supported features, intents, primaries, and transfer functions. | • `.ufo/waves/round-13/w1/globals.json:295` (`wp_color_manager_v1` @ 3)<br>• Installed `color-management-v1.xml` in `wayland-protocols 1.49-1` (staging phase, **S048**)<br>• `wayland-info.c:2744-2750` (S046 diagnostic detail queries)<br>• Pinned Hyprland 0.56.2 | **Does NOT license:**<br>1. Claiming that High Dynamic Range (HDR) display output, wide color gamut (WCG), or hardware color calibration is active or supported by the display pipeline.<br>2. Claiming client support for specific profile creators (parametric, ICC, Windows scRGB/BT.2100) without observing per-connection server `supported_feature` events (unsupported requests trigger protocol error `unsupported_feature`).<br>3. Inferring compositor shader rendering precision or colorimetric transfer accuracy from surface image description attachment.<br>4. Treating staging protocol version 3 as a frozen stable ABI (refuted by S048: *"currently in the testing phase"*). |
| **3. Diagnostic Observation vs Substrate Execution Boundary**<br><br>Diagnostic tools (`wayland-info`) bind advertised globals and issue read-only detail queries. The sanitized capture retains interface/version headers and session metadata, explicitly excluding physical display properties and DRM paths. | • `.ufo/waves/round-13/w1/globals.json:332-343` (`excluded` array)<br>• `PROVINCE.md` (read-only compositor config & display behavior fence)<br>• `round-13-verifier-spotcheck.md` (R13-V1, R13-V2, R13-V3 rulings)<br>• Sibling `tsukuroi` province boundary | **Does NOT license:**<br>1. Asserting physical display topology or DRM/KMS hardware state (strictly tsukuroi-owned kernel/DRM province, not mado).<br>2. Executing mutating protocol requests (`apply`, modesetting, surface commits) during gate verification.<br>3. Equating a single-run unchanged config boundary hash (`gate-file-plane.txt`) with byte-identical outputs across Git revisions (R13-V2).<br>4. Treating registry advertisement headers as an end-to-end verified desktop feature verdict. |

---

## 4. Addressing Outside Review Rulings (R13-V1, R13-V2, R13-V3)

To ensure six-month maintainability and precision across rounds, this evidence chain incorporates the exact corrections required by the round-13 verifier spot-check (`corpus/lessons/round-13-verifier-spotcheck.md:200-210`):

1. **R13-V1 (Retained-Data Wording Precision):**
   * *Previous Ambiguity:* Stating that `globals.json` retained "only registry interface/version headers" was overly broad.
   * *Clarified Standard:* Global records retain interface name and version only; sanitized probe execution metadata (tool version, package pin, return code) and session correlation metadata (matching display socket `wayland-1`, boolean match flags) are also legitimately retained. Physical output geometry, EDID, modes, device paths, and colorimetry tables remain strictly discarded in the `excluded` array.
2. **R13-V2 (Single-Run Boundary vs Cross-Revision Output Equality):**
   * *Previous Ambiguity:* Conflating a config boundary unchanged within a single run with byte-identical outputs across Git revisions.
   * *Clarified Standard:* The gate's file-plane verification (`gate-file-plane.txt:47`) proves that the configuration boundary remained unchanged *within that single execution run*. It must not be cited as proof of byte-identical outputs across distinct Git revisions unless an explicit cross-revision diff receipt is generated.
3. **R13-V3 (Standalone Receipt Measured Digest & Provenance):**
   * *Previous Ambiguity:* Standalone selftest outputs (`gate-selftest.txt`) lacked self-contained revision and gate digest headers.
   * *Clarified Standard:* Any future receipt generated by standalone verification must explicitly record the measured git revision, worktree gate SHA-256, and execution timestamp in its header to ensure unforgeable provenance.

---

## 5. Trace of Second-Order Effects Across Surfaces

1. **Runtime Surface (Compositor & Session):**
   * Zero compositor mutations. No test surfaces are created, no `create_configuration` or `apply` requests are transmitted, and no display modes are altered.
   * The host session remains clean and unaffected; observation remains strictly passive and grounded in historical captured bytes (`globals.json`) and installed protocol XML files.

2. **Contract & Province Surface (mado vs tsukuroi):**
   * `PROVINCE.md` explicitly confines `mado` to desktop configuration files and display behavior, forbidding running compositor mutations.
   * Hardware-level DRM/KMS configuration, CRTC state, kernel modesetting, and connector detection remain fenced in sibling `tsukuroi`'s province. S047 and S048 establish protocol semantics without intruding into kernel/driver diagnosis.

3. **Verification Surface (Gate & Selftest Isolation):**
   * The C1 protocol boundaries in U5 remain strictly causally isolated from C2 source resolver verification in `tools/mado-verify.sh`.
   * Expanding U-item coverage from 4/7 to 5/7 does not alter the evaluation of regular-file target checks, symlink handling, or source-order fixtures.

---

## 6. Actionable Synthesis & Verification Plan

### For the L1 Planner & Integrator
1. **Admit U5 into Knowledge Corpus:**
   * Integrate U5 output-management and colour boundaries into `corpus/knowledge/` citing reciprocal mined rows:
     * `S047` (`wlr-output-management-unstable-v1.xml`, status flip `queued` -> `mined`)
     * `S048` (`color-management-v1.xml`, status flip `queued` -> `mined`)
   * Ensure the knowledge entry carries the header `covers: U5` and includes the three-row falsification table from Section 3.
   * Advances C1 coverage score from $4/7 \approx 5.7143/10$ to $5/7 \approx 7.1429/10$.

2. **Maintain Strict Falsification Fences:**
   * Enforce that no future agent or document claims working HDR, color calibration, display reconfiguration, or monitor topology based on `globals.json` or protocol XML.
   * Keep runtime behavior explicitly marked `[UNK]` until a separately authorized, feature-specific behavioral observation is designed.

3. **Tooling Record:**
   * Tool: `wlr-protocols` (providing `/usr/share/wlr-protocols/unstable/wlr-output-management-unstable-v1.xml`)
     * Version: `r112.a741f0a-1` (pacman extra)
     * Reason: Primary authority for `zwlr_output_manager_v1` interface semantics and transaction lifecycle.
   * Tool: `wayland-protocols` (providing `/usr/share/wayland-protocols/staging/color-management/color-management-v1.xml`)
     * Version: `1.49-1` (pacman extra)
     * Reason: Primary authority for `wp_color_manager_v1` staging interface and capability negotiation enums.
   * Status: Pre-installed official packages inspected read-only; no new installations or package upgrades executed.
