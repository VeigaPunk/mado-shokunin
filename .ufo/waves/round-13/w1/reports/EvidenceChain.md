# EvidenceChain — Connect protocol phase docs, global advertisement, host compositor and U4 coverage ground; falsify advertisement-to-behavior implication

**Seat:** `MadoR13.EvidenceChain` (connector, leaf)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Milestone:** exact-set census and sourced U4 boundaries  
**Axes judged on:** coverage, operability  
**Status:** Complete findings and synthesis draft; no mutating commands, no shared-file edits.

---

## 1. Executive Summary & Named Proposal

### Non-Obvious Move: The Four-Node Evidence Chain with Adversarial Falsification Gate
We synthesize the round's inputs into a verifiable 4-node directed evidence chain that advances the **coverage** axis (C1: grounded U4 protocol boundary, moving U-items from 3/7 to 4/7) while protecting the **operability** axis (preventing false-positive gate passes and eliminating invalid runtime behavioral assumptions).

```
[Node 1: Upstream Specification] 
  wayland-protocols (README.md, GOVERNANCE.md) & wayland.xml (wl_registry)
        │
        ▼ (Defines protocol phase, ABI stability rules, interface contract)
[Node 2: Compositor Capability Advertisement]
  wl_registry.global announcement (observable via sanitized wayland-info)
        │
   ════════════════════════════════════════════════════════════════════════
   FALSIFICATION GATE: Advertisement != Protocol Binding != Runtime Behavior
   ════════════════════════════════════════════════════════════════════════
        │
        ▼ (Requires explicit wl_registry.bind request to activate interface)
[Node 3: Client Interface Binding]
  Client specifies requested version (≤ advertised version) -> server instantiates proxy
        │
        ▼ (Operational execution subject to compositor implementation & policy)
[Node 4: Host Compositor Runtime Behavior]
  Compositor internal dispatch logic, event emission, error generation, policy enforcement
```

**Adversarial Truth:** A compositor advertising a global interface via `wl_registry.global` proves *only* that the compositor exposes that symbol name and numeric version in its registry table. It **falsifiably does NOT prove**:
1. That the underlying protocol extension is in `stable/` or `staging/` phase (it could be legacy `unstable/`, `experimental/` `xx_`, or out-of-tree vendor extension);
2. That a client can successfully invoke `wl_registry.bind` without error;
3. That requests sent over the bound interface produce functional display/state mutations (they may be stubs, no-ops, capability-gated, or emit protocol errors such as `wl_display.error.implementation`);
4. That the host is running a particular package version or distribution configuration.

---

## 2. Evidence Corpus & Exact Grounding Anchors

Every citation is grounded in primary, read-only sources opened during this round:

### Node 1: Upstream Specification & Core Architecture
* **S005 — `wayland-protocols` README:**
  * **Location:** `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md`
  * **Anchors & Quotes (≤25 words):**
    * *Phase definition:* "Protocols have three currently used phases: the experimental phase, the staging phase, and the stable phase." (`README.md:19-20`)
    * *Backward compatibility:* "Backward-incompatible changes can only be introduced in a new major version of a protocol." (`README.md:24-25`)
    * *Staging adoption:* "When a protocol has reached a stage where it is ready for wider adoption, it enters the 'staging' phase." (`README.md:39-40`)
    * *Legacy unstable prefix:* "During this phase, protocol interface names were, in addition to the major version postfix, also prefixed with `z` to distinguish them from stable protocols." (`README.md:61-63`)
  * **Revision:** Pin commit `3dac056d83ad8947` / tag `1.49` (`ee78491a237ea`).
  * **Role in U4:** Grounds the lifecycle contract and deprecation vocabulary. Directory placement (`stable/`, `staging/`, `experimental/`), *not* interface name prefix, determines official phase.

* **S040 (Candidate) — `wayland-protocols` GOVERNANCE:**
  * **Location:** `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/GOVERNANCE.md`
  * **Anchors & Quotes (≤25 words):**
    * *Inclusion bar:* "Protocols in the 'xdg' and 'wp' namespaces must have at least 3 open-source implementations (either 1 client + 2 servers, or 2 clients + 1 server)" (`GOVERNANCE.md:90-92`)
    * *Staging stability test:* "A member project has the option to invoke the 30 day discussion period for any staging protocol proposal which has been in use without substantive changes for a period of one year." (`GOVERNANCE.md:127-129`)
  * **Revision:** Commit `d90a7862` / tag `1.49`.
  * **Role in U4:** Establishes governance hurdles required before an interface can claim multi-vendor consensus.

* **S043 (Candidate) — Wayland Core Registry Specification (`wayland.xml`):**
  * **Location:** `/usr/share/wayland/wayland.xml` (installed package `wayland 1.26.0-1`) & `https://gitlab.freedesktop.org/wayland/wayland/-/raw/main/protocol/wayland.xml`
  * **Anchors & Quotes (≤25 words):**
    * *Global announcement:* "The event notifies the client that a global object with the given name is now available, and it implements the given version of the given interface." (`wayland.xml:154-156`)
    * *Binding request:* "Binds a new, client-created object to the server using the specified name as the identifier." (`wayland.xml:143-144`)
    * *Global removal & race handling:* "The object remains valid and requests to the object will be ignored until the client destroys it, to avoid races" (`wayland.xml:172-174`)
  * **Role in U4:** Mechanically splits announcement (`event global`) from binding (`request bind`).

---

### Node 2: Advertised Globals Ground (Host Compositor Exposure)
* **S041 (Candidate) — Host Advertised Globals Capture:**
  * **Location:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/globals.json`
  * **Tool:** `wayland-info` (installed via authorized channel `pacman -S --needed --noconfirm wayland-utils`, package `wayland-utils 1.3.0-1`, binary `/usr/bin/wayland-info`).
  * **Execution:** Read-only probe `wayland-info` on socket `wayland-1`, exit code `0`, `stderr_bytes: 0`.
  * **Compositor Identity:** `Hyprland 0.56.2` (commit `efb50993780079460b0cbed1363e2166a2de1d9f`).
  * **Sanitization:** Strict interface header capture (`interface: '...' version: N`). All indented output blocks (EDID make/model, modes, transform, coordinates, subpixel orientation, dmabuf formats/modifiers, DRM lease device paths, seat device names, colorimetry tables) are discarded.
  * **Observed Metrics:**
    * Total advertised global objects: `72` (`global_count: 72`).
    * Unique interfaces: `71` (`unique_interface_count: 71`).
    * Multiplicity / duplicate interface: `wp_drm_lease_device_v1` (count: 2, version: 1 per `multiplicity` array). `wl_output` (version 4) appears exactly once. No hardware topology, monitor count, or output geometry is inferred from the sanitized global listing.
    * Digest of sanitized interface set: `9569d02fe2b04bf62079258b1d74f5d2ad8510c26ef0710a1a64c95f1a9becaa` (`set_sha256`).

---

## 3. Dissecting the Advertisement Spectrum: Hyprland 0.56.2 Global Inventory

The 71 unique interfaces exposed by the host compositor span multiple distinct phases, origins, and lifecycles:

| Interface Class | Examples from `globals.json` | Upstream Phase / Origin | Implication of Advertisement |
|---|---|---|---|
| **Core Protocol** | `wl_compositor` (v6), `wl_subcompositor` (v1), `wl_shm` (v2), `wl_seat` (v9), `wl_data_device_manager` (v3), `wl_output` (v4) | Wayland Core (`wayland.xml`) | Standard core IPC. Required for baseline surface presentation and input handling. |
| **Stable Standard** | `wp_viewporter` (v1), `wp_presentation` (v1), `xdg_wm_base` (v6) | `stable/` in `wayland-protocols` | Formally frozen interfaces; backward-incompatible changes require new major version or new interface name. |
| **Staging Standard** | `wp_fractional_scale_manager_v1` (v1), `wp_cursor_shape_manager_v1` (v2), `wp_tearing_control_manager_v1` (v1), `wp_alpha_modifier_v1` (v1), `ext_foreign_toplevel_list_v1` (v1), `wp_color_manager_v1` (v1) | `staging/` in `wayland-protocols` | Ready for adoption, backward-compatible iterations allowed, active testing in wild. |
| **Legacy Unstable (`z`-prefix)** | `zxdg_output_manager_v1` (v3), `zwp_idle_inhibit_manager_v1` (v1), `zwp_relative_pointer_manager_v1` (v1), `zxdg_decoration_manager_v1` (v2), `zwp_linux_dmabuf_v1` (v5) | `unstable/` in `wayland-protocols` | Carries historical naming prefix; subject to replacement by un-prefixed stable/staging equivalents. |
| **Vendor / Compositor-Specific** | `hyprland_toplevel_export_manager_v1` (v2), `hyprland_focus_grab_v1` (v1), `hyprland_surface_v1` (v1), `zwlr_foreign_toplevel_manager_v1` (v3), `zwlr_layer_shell_v1` (v4) | `hyprland-protocols` / `wlr-protocols` | Outside freedesktop `wayland-protocols` governance; specific to wlroots/Hyprland ecosystems. |

---

## 4. Falsifying the Advertisement-to-Behavior Implication

### Fallacy 1: "The compositor advertises interface X, therefore functionality X works."
* **Falsification:**
  * In the Wayland architecture, `wl_registry.global` is a broadcast enumeration event. The compositor creates this event stream when `wl_display.get_registry` is called.
  * A compositor implementation may instantiate a global manager to satisfy toolkit requirements or protocol scanner dependencies, but provide a no-op or stub implementation for individual requests within that interface.
  * *Example:* `zxdg_decoration_manager_v1` (v2) is advertised in `globals.json`. However, in a tiling compositor like Hyprland, a client binding to `zxdg_toplevel_decoration_v1` and requesting `set_mode(server_side)` may have its request ignored, or the compositor may force `client_side` decorations based on configuration rules. The existence of the global manager does not guarantee server-side decoration rendering.

### Fallacy 2: "The compositor advertises version $V_{adv}$, therefore all requests up to version $V_{adv}$ succeed."
* **Falsification:**
  * Per `wayland.xml:135-138`, a client issues `wl_registry.bind(name, id, version)`. If the client passes $V_{req} > V_{adv}$, the compositor MUST terminate the client connection with a fatal protocol error (`wl_display.error.invalid_object` or version mismatch).
  * Even when $V_{req} \le V_{adv}$, the compositor's request dispatcher may fail to implement specific optional requests introduced in that version, or may fail under specific driver/hardware constraints (e.g., `zwp_linux_dmabuf_v1` advertised with modifier support, but allocation fails if the DRM node lacks modifier query support).

### Fallacy 3: "Global advertisement guarantees static lifecycle availability."
* **Falsification:**
  * As documented in `wayland.xml:127-130`, "Globals come and go as a result of device or monitor hotplugs, reconfiguration or other events, and the registry will send out global and global_remove events to keep the client up to date with the changes."
  * Protocol objects can dynamically vanish when removed by the compositor via `global_remove`. If a client assumes any global advertised at connection start is static, operations against it post-removal encounter the race avoidance rule (`wayland.xml:172-174`), where requests are silently ignored until destruction. Duplicate interface announcements (such as two `wp_drm_lease_device_v1` global entries in `globals.json`) represent multiple registered server objects exposing that interface, but do not provide hardware device paths or lease availability in the sanitized capture without client binding and DRM leasing requests.

### Fallacy 4: "Interface name prefix indicates protocol phase."
* **Falsification:**
  * A naive heuristic equates `z`-prefix with unstable, and no-prefix with stable.
  * Upstream `wayland-protocols` README explicitly refutes this: the `z`-prefix is a **legacy unstable convention**. New protocols entering `staging/` use their standard prefix (`wp_`, `xdg_`, `ext_`) without a `z`, even though they are *not* yet stable!
  * Conversely, experimental protocols use the `xx` namespace (`GOVERNANCE.md:78`). Therefore, interface naming cannot determine phase without inspecting the upstream specification tree or repository metadata.

---

## 5. Trace of Second-Order Effects

1. **Runtime Surface:**
   * Probes MUST remain passive and read-only. `wayland-info` issues `get_registry`, receives `global` events, sends `sync`, prints the table, and calls `wl_display_disconnect`. It creates zero surfaces, creates no buffers, and alters no compositor state.
   * Testing live behavior requires protocol injection or client automation (e.g. creating surfaces, binding buffers), which is strictly fenced out of mado's read-only inspection contract.

2. **Contract & Province Surface:**
   * `PROVINCE.md` covers Hyprland/waybar/walker configurations and display behavior on this host. Probing protocol boundaries establishes the exact substrate capabilities available to waybar (e.g. `zwlr_foreign_toplevel_manager_v1`, `ext_foreign_toplevel_list_v1`) and walker without mutating the session.

3. **Verification Surface (Gate & Selftest):**
   * The C2 census work in `tools/mado-verify.sh` must remain completely causally isolated from C1 protocol knowledge. A change in advertised globals or Wayland protocol documentation must not alter the hermetic evaluation of `hypr.root.include_graph` or `hypr.local.inventory`.
   * When integrating U4 into `corpus/knowledge/wayland-protocol-boundaries-r13.md`, the entry must clearly partition:
     * `[O]` Observed host globals (sanitized `globals.json`);
     * `[INF-docs]` Protocol phases from upstream `wayland-protocols` README / GOVERNANCE;
     * `[U]` Live behavior under client request dispatch (which requires client instrumentation outside leaf read-only scope).

---

## 6. Actionable Synthesis for Main Agent & Integrator

1. **Admit U4 into `corpus/knowledge/wayland-protocol-boundaries-r13.md`:**
   * Cites `mined` rows:
     * S005 (`wayland-protocols` README, status flip `queued` -> `mined`)
     * S040 (new: `wayland-protocols` GOVERNANCE.md)
     * S041 (new: sanitized `globals.json` capture)
     * S043 (new: `wayland.xml` core registry specification)
   * Carries header `covers: U4`.
   * Replaces the 0/7 -> 3/7 baseline with 4/7 (C1 achieved: 5.7143 / 10).

2. **Maintain Strict Falsification Boundaries:**
   * Ensure `wayland-protocol-boundaries-r13.md` explicitly includes the falsification arguments from Section 4, preventing any future agent from claiming that listing `wp_drm_lease_device_v1` or `wp_tearing_control_manager_v1` in `globals.json` proves lease capability or tearing rendering is functioning, and prohibiting any inference of output geometry or hardware topology from the sanitized global capture.

3. **Tooling Record:**
   * Tool: `wayland-utils` (providing `wayland-info`)
   * Version: `1.3.0-1`
   * Channel: `pacman -S --needed --noconfirm wayland-utils` (official Arch Linux package repository)
   * Reason: Required for read-only query of advertised Wayland compositor globals; executed without `-Sy` partial upgrade per RULES.md directive.
