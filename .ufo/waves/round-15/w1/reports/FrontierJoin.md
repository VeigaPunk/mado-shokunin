# FrontierJoin — Connecting U6 Bounded Documentation Route to Still-Open Actual Delivery and U7 Waybar Gaps

**Seat:** `MadoR15.FrontierJoin` (connector, leaf)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Milestone:** U6 input evidence ladder and R14 ancillary provenance correction  
**Judged Axis:** `coverage` (C1, lowest non-retired rubric: sourced U1–U5 5/7 → U1–U6 6/7)  
**Harm-Watch Axes:** `operability`, `calibration`, `adjacency`, `freshness`, `depth`  
**Report Path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/FrontierJoin.md`  

---

## 1. Naming the Axes (Godspeed)

1. **coverage (Primary / Scored — C1):**
   Advances the finite current-art ground rubric ($10 \times \text{covered U-items} / 7$) from $5/7$ ($7.1429/10$) to $6/7$ ($8.5714/10$) by admitting Milestone U6 (`input-evidence-ladder-r15.md`) as a bounded input-debugging layer route. It explicitly refuses any complete-input-coverage claim, leaving U7 (Waybar module text) as the unadmitted, open $1/7$ gap ($14.2857\%$).
2. **operability (Harm-Watch):**
   Preserves hermetic test suites and zero live probes (`tools/mado-verify.sh --selftest` 268/268, `--no-live` file plane CLEAN). Rejects root-requiring evdev sniffing (`libinput debug-events`), keyloggers, and synthetic injection (`libinput replay`, `ydotool`).
3. **calibration (Harm-Watch):**
   Prevents inference conflation:
   - Libinput built-in driver defaults do not equal compositor configuration (`lessons/round-12.md:37` M04);
   - Compositor device presence (`hyprctl devices`) does not equal surface focus;
   - Seat capabilities (`wl_seat.capabilities`) do not equal client delivery;
   - Client socket delivery does not equal application execution outcome or layer-surface rendering.
   Preserves R14-V1 ancillary mutation receipt precision as an explanatory sidecar mapping without mutating historical bytes.
4. **adjacency (Harm-Watch):**
   Strictly enforces the boundary between `mado-shokunin` (compositor policy, desktop configs), `tsukuroi-shokunin` (kernel modules, evdev `/dev/input/event*`, hardware health), `mori-shokunin` (process life/death observability), and `kagi-shokunin` (credential privacy; input-event sniffing barred to prevent keystroke credential theft).
5. **freshness & depth (Harm-Watch):**
   Labels upstream documentation as `[INF-docs]`, historical captures as `[OBS-history]`, and unexercised delivery/IME/kernel rungs as explicit `[UNK]`.

---

## 2. Evidence Grounding

This analysis synthesizes primary evidence from repository files, static protocol definitions, and peer wave reports without running any live probes:

### 2.1 The Finite Rubric and Gap Inventory
- **SCORECARD.md:600–612:** C1 coverage baseline is $5/7$ (`ea0446fcb4840089f0e541d96350144506fb5d1d`), targeting $6/7$ via U6. Requires provenance trio, reciprocal mined joins (S051/S052), and sections `## Layer ladder`, `## Safe boundary`, and `## Unexercised delivery` containing `[UNK]`.
- **`corpus/knowledge/arc-synthesis.md:301` (§6 Gap Ledger):**
  `| waybar module text | no IPC/query verb in waybar 0.15.0 (r3 anti-claim branch) |`
- **`corpus/knowledge/wayland-protocol-boundaries-r13.md:8`:**
  `"It does not close protocol request behavior, output management/colour (U5), the kernel-input ladder (U6), or Waybar module text (U7)."`
- **`corpus/knowledge/output-colour-boundaries-r14.md:108`:**
  `"U6 input debugging and U7 Waybar module text remain outside this entry."`
- **`corpus/README.md:94–95` (§## Frontier):**
  `"Still open: rule attribution, output-management behavior, the input debugging ladder and Waybar module text — study paths and queued sources in SOURCES."`
- **`GapCensus.md:111–124`:** Confirms 0/28 knowledge notes currently cover U6 or U7. U1–U5 are covered; U6 is the single active target; U7 is the retained remaining gap.

### 2.2 The Input Delivery Decoupling Chain
- **`AttackDelivery.md:20–66`:**
  - `wl_seat.capabilities` is an unconditional bitwise OR of all attached HID objects (`InputManager.cpp:1869–1881`), with zero permission or enabled filtering.
  - Disabled (`enabled=false`) or permission-denied (`PERMISSION_TYPE_KEYBOARD`) devices drop events at the entry of the key path (`InputManager.cpp:1620–1621`).
  - Active keys have 7 further exit/drop points before client delivery: event-bus cancel, `inputCapture`, keybind consumption (192 binds, `KeybindManager.cpp:409`), IME divert, multi-keyboard dedupe, missing keyboard focus resource, and null active surface.
  - `hyprctl devices` `main` field only indicates the last-active keyboard (`m_active`), not focus or delivery.
- **`TextInputBoundary.md:47–118`:**
  - `wl_keyboard` delivers context-blind evdev scancodes with no double-buffering.
  - `zwp_text_input_v3` delivers double-buffered UTF-8 composed text (`commit_string`, `preedit_string`) via a serialized 7-step transactional pipeline (`done(serial)`), requiring explicit widget-level `enable`/`disable` calls. IME intercept suppresses or alters direct keyboard delivery.
- **`ReviewLibinput.md:14–29` & `LibinputTools.md:45–58`:**
  - `tools.html#libinput-list-devices` note explicitly states: `"This tool does not show your desktop's configuration, just the libinput built-in defaults."`
  - Conflating libinput driver defaults with compositor configuration is the lane's recorded mistake M04 (`lessons/round-12.md:37`).

### 2.3 The U7 Waybar Introspection Horizon
- **`corpus/knowledge/waybar-walker-semantics.md` (MADO-R3-1) §2.3, §6.8:**
  - Waybar 0.15.0-3 has **no IPC query verb** or query socket to extract live rendered widget contents.
  - Signals (`RTMIN+7..11`) are blind controls, not readouts.
  - Waybar is a Wayland layer surface (`zwlr_layer_surface_v1`), sitting on the receiving end of compositor event dispatch.
  - Extracting rendered module text requires visual pixel capture + OCR (explicitly barred as a non-reproducible, non-verdict probe in R1/R2) or process memory inspection (violates read-only safety).
  - The lane's standing position is an **anti-claim**: rendered module text is classified as `[UNK]`.

---

## 3. Contradictions Across Round Proposals

Tracing second-order effects across runtime, contract, substrate, and verification surfaces reveals three distinct contradictions:

1. **The "Complete Input Coverage" Fallacy:**
   - *Tension:* An ungrounded proposal might equate admitting U6 with achieving "complete input coverage" or closing the input domain.
   - *Contradiction:* This violates the contract on two independent surfaces:
     - *Mathematical / Rubric:* The active finite rubric has 7 discrete items. Admitting U6 reaches $6/7$ ($8.5714/10$). Claiming completion would falsely claim $7/7$ while U7 remains un-admitted and unexercised.
     - *Substrate / Behavioral:* U6 is explicitly an *evidence ladder of diagnostic tools and layers*. The ladder proves that lower tiers (kernel, libinput defaults, compositor options, protocol seat capabilities) decouple from higher tiers (actual client delivery and application outcome). Asserting "complete coverage" would commit the very category errors exposed by M04, `AttackDelivery`, and `TextInputBoundary`.
2. **The Layer-Surface Focus Decoupling vs. Toplevel Focus:**
   - *Tension:* The assumption that input always routes to the focused application window (`activewindow`).
   - *Contradiction:* `InputManager.cpp:454–465` establishes that exclusive Wayland layer surfaces (`zwlr_layer_surface_v1`, such as Waybar, lockscreens, or app launchers) take precedence over toplevel application windows (`xdg_toplevel`). When an exclusive layer surface is active, toplevel window refocusing is refused. Therefore, compositor-level focus is split between toplevel application surfaces and layer surfaces.
3. **The Introspection Horizon Parallels:**
   - *Tension:* Treating U6 Actual Delivery and U7 Waybar Module Text as disconnected, isolated gaps.
   - *Contradiction:* Both gaps stem from the exact same structural cause: the **Client-Compositor Introspection Horizon**. Once an event traverses the Wayland wire socket (`wl_keyboard.key` or `wl_pointer.button`), or once Waybar computes its widget text from system sensors, the resulting state exists solely within client process memory. Wayland provides no standard back-channel for an external observer or compositor to query whether the client processed the event or what text it rendered.

---

## 4. Proposed Move: The Dual-Terminal Observability Cliff Synthesis

We propose a single, bounded synthesis move across the round's proposals: **The Dual-Terminal Observability Cliff**.

### 4.1 Structural Formulation in Milestone U6
In the admitted U6 knowledge note (`corpus/knowledge/input-evidence-ladder-r15.md`), Tier 5 of the evidence ladder must be formally structured into two reciprocal client-side consumer archetypes:

```
[ Tier 1: Kernel evdev Nodes (/dev/input/event*) ]
         │  (tsukuroi domain; mado refuses root evdev access)
         ▼
[ Tier 2: Driver Defaults & Quirks (libinput 1.32.0) ]
         │  (tools.html: built-in defaults ≠ desktop config; lesson M04)
         ▼
[ Tier 3: Compositor Seat Inventory & Policy (Hyprland 0.56.2) ]
         │  (hyprctl devices, getoption input:*; binds intercept 192 keys)
         ▼
[ Tier 4: Wayland Protocol Focus & Wire Events (wl_seat, wl_keyboard) ]
         │  (surface enter serial; context-blind evdev scancodes)
         ├─────────────────────────────────────────┐
         ▼                                         ▼
[ Tier 5A: Toplevel App Delivery ]       [ Tier 5B: Layer Surface Consumer (U7) ]
  • Client widget event loop              • Waybar 0.15.0 layer surface
  • XKB scancode translation              • Module status calculation
  • zwp_text_input_v3 IME commit          • Click/scroll handler actions
  • Application UI state outcome          • Rendered module text on bar
  ──► STATUS: UNKNOWN [UNK]               ──► STATUS: UNKNOWN [UNK] (U7 GAP)
```

1. **Tier 5A — Toplevel Application Delivery:**
   - Encompasses client application widgets (e.g. Alacritty, Kitty, Foot).
   - Key and pointer events are translated via client-side XKB state machines or intercepted by `zwp_text_input_v3` IME composition.
   - *Status:* Unexercised and classified as `[UNK]`.
2. **Tier 5B — Layer Surface State & Interactive Outcome (The U7 Waybar Anchor):**
   - Encompasses Wayland layer surfaces (`zwlr_layer_surface_v1`), concretely represented on this host by Waybar 0.15.0.
   - Waybar consumes system state and receives interactive click/scroll events to update module display text.
   - Because Waybar 0.15.0 lacks an IPC query verb, the internal widget state and rendered text cannot be introspected.
   - *Status:* Unexercised and classified as `[UNK]`, anchoring the retained **U7 Waybar Gap**.

### 4.2 Explicit Rejection of Complete-Input-Coverage
The U6 note, `corpus/README.md`, and `SCORECARD.md` must explicitly state:
- Milestone U6 covers *only* the verifiable diagnostic route across Tiers 1–4 (kernel documentation, libinput defaults, compositor configuration, and protocol wire focus boundaries).
- Actual application delivery (Tier 5A) and layer-surface status rendering (Tier 5B / U7) remain unexercised and opaque (`[UNK]`).
- Coverage reaches exactly $6/7$ ($8.5714/10$); it does **not** saturate input domain operability, and U7 remains the sole active gap in the current-art rubric.

---

## 5. Risks and Mitigations

| Risk | Consequence | Mitigation |
|---|---|---|
| **Conflating U6 with 7/7 Saturation** | Claiming full input verification would falsify SCORECARD counting and break the 7-item finite denominator. | Counter strictly counts `covers: U6`; report explicitly checks that U7 remains listed as an open gap in `SCORECARD.md` and `corpus/README.md`. |
| **Simulating Waybar Verification via OCR** | Attempting screenshot OCR to claim U7 closure would violate non-intrusive safety and introduce non-reproducible pixel flakiness. | Maintain the Round 3 anti-claim branch: rendered module text without IPC query verbs is permanently classified as `[UNK]`. |
| **Inverting M04 via Libinput Probes** | Running `libinput list-devices` and presenting it as active Hyprland configuration reopens lesson M04. | Ground Tier 2 strictly in `tools.html:43–44` documentation quotes; use `hyprctl getoption input:*` with `set: true` for compositor-applied policy. |
| **Privacy Breach via Event Sniffing** | Running `libinput debug-events` or `record` acts as a keylogger, leaking user credentials (breaching Kagi's domain). | Strictly fence the milestone to static documentation and XML parsing; zero event capture or device node execution. |
| **R14-V1 Receipt Mutation** | Overwriting provisional headers in R14 receipts violates append-only auditability (QUALITY 4/13). | Implement R14-V1 strictly as an append-only sidecar mapping in `.ufo/waves/round-15/receipt-correction.json` binding provisional headers to derived target `cd1d73d7...`. |

---

## 6. Verification and Acceptance

The integrator (L1) and main agent must verify the following observable facts before closing Round 15:

1. **Structural Measurement (C1):**
   `python3 .ufo/waves/round-15/measure.py REV`
   - Must output covered items: `['U1', 'U2', 'U3', 'U4', 'U5', 'U6']`.
   - Covered count: `6/7`, score: `8.5714/10`.
   - `covers: U7` must be absent across all knowledge notes.
2. **Corpus README Frontier Alignment:**
   `corpus/README.md` lines 91–102 must be updated:
   - Remove "the input debugging ladder" from the open frontier list.
   - Retain: "Still open: rule attribution, output-management behavior, actual client input delivery and Waybar module text (U7)."
3. **U6 Note Facet Verification:**
   `corpus/knowledge/input-evidence-ladder-r15.md` (or candidate draft) must contain:
   - Header with `covers: U6`, provenance trio, and reciprocal mined joins to S051/S052.
   - Required headings: `## Layer ladder`, `## Safe boundary`, and `## Unexercised delivery`.
   - In `## Layer ladder`, Tier 5 explicitly distinguishes Toplevel Application Delivery (5A) and Layer Surface / Waybar Module Text (5B).
   - In `## Unexercised delivery`, both Tier 5A and Tier 5B (U7) are marked `[UNK]`.
4. **Hermetic Non-Regression:**
   - `bash tools/mado-verify.sh --selftest` passes 268/268 (or round-14 372/372).
   - Zero live input events, recordings, or synthetic replays exist in repository evidence.
5. **R14-V1 Provenance Preservation:**
   - Raw sha256 digests of the three round-14 mutation receipts remain byte-identical.
   - `.ufo/waves/round-15/receipt-correction.json` maps provisional headers `ef50e262...` and `d6d5eb27...` to derived target `cd1d73d7...` at commit `32118fc1...`.

---

## 7. Tooling Record

- **Tooling Directive Compliance (RULES.md):**
  - Zero packages, Python tools, or external binaries were installed or upgraded by this seat.
  - All investigations were conducted using read-only static file inspection, git metadata, and local documentation.
  - No live compositor, device, or input-event commands were executed.
