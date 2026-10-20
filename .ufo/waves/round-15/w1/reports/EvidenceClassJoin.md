# EvidenceClassJoin — Tri-Class Evidence Mapping (OBS static-source, INF-docs, UNK) and Unsupported Host Implication Analysis for Milestone U6 (Round 15, w1)

**Seat:** `MadoR15.EvidenceClassJoin` (connector, leaf; no delegation, no background jobs, no commits)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Judged on:** `coverage` (C1, lowest active finite rubric U1–U5 5/7 → U1–U6 6/7)  
**Milestone:** U6 input evidence ladder and R14 ancillary provenance correction  
**Report path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/EvidenceClassJoin.md`  

---

## 1. Naming the Axes

Per Godspeed discipline and the round-15 contract:
1. **Primary Judged Axis — coverage (C1):**
   - Advances sourced current-art ground from U1–U5 (5/7 = 7.1429/10) to U1–U6 (6/7 = 8.5714/10) by establishing a bounded, documentary input-debugging layer route without raw event capture, keystroke recording, uinput injection, or kernel diagnosis.
2. **Harm-Watched Companion Axes:**
   - **operability (C2):** Preserves hermetic gate boundaries and test suites; executes zero live event probes, zero `/dev/input/event*` access, zero `sudo`, zero compositor actions, and zero gate runs during leaf analysis.
   - **calibration:** Eliminates overbroad or speculative claims; strictly partitions primary source text (`OBS static-source`), interface specifications (`INF-docs`), and unexercised host behaviors (`UNK`); permanently enforces Lesson M04 (`corpus/lessons/round-12.md:37`, criterion 15).
   - **freshness:** Accurately distinguishes documentation era from runtime library state, accounting for host package drift without conflating static manual pages with live execution.
   - **depth / adjacency:** Preserves strict province boundaries: kernel, evdev, and driver diagnosis remain owned by `tsukuroi-shokunin` (handoff ADJ-03); credentials, privacy, and sensitive session material remain owned by `kagi-shokunin`; desktop and compositor craft remain owned by `mado-shokunin`.

---

## 2. Evidence Grounding & Round Cache Findings

All evidence was gathered through read-only inspection of pinned static files, package manifests, and wave w1 reports across the round cache:

### 2.1 Primary Static Sources (`OBS static-source`)
- **Installed Wayland Core XML:** `/usr/share/wayland/wayland.xml` (package `wayland 1.26.0-1`, SHA-256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`, 168,656 bytes, 3,442 lines). Declares interfaces `<interface name="wl_seat" version="11">` (lines 2004–2137), `<interface name="wl_pointer" version="11">` (lines 2138–2572), and `<interface name="wl_keyboard" version="11">` (lines 2573–2753).
- **Installed Text-Input XML:** `/usr/share/wayland-protocols/unstable/text-input/text-input-unstable-v3.xml` (package `wayland-protocols 1.49-1`, SHA-256 `160815cda13c285a30df1971d8f0a5b3aac07071537df59916d2f748b18e4f59`, 604 lines). Declares `<interface name="zwp_text_input_v3" version="2">` (lines 50–583) and `<interface name="zwp_text_input_manager_v3" version="2">` (lines 585–603).
- **Official libinput 1.32.0 Documentation:** `https://wayland.freedesktop.org/libinput/doc/latest/tools.html` (page banner verbatim reads `"libinput 1.32.0 documentation"`, generated from git commit `4cf1775`). GitLab upstream raw source `doc/user/tools.rst` at tag `1.32.0` has SHA-256 `53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f`.
- **Upstream Hyprland Source at Commit `efb50993`:** `src/devices/IKeyboard.hpp` (SHA-256 `82e0bc9e…`), `src/managers/input/InputManager.cpp` (`feedf32e…`), `src/managers/SeatManager.cpp` (`bd748553…`), `src/protocols/core/Seat.cpp` (`cc23bb8b…`), `src/managers/KeybindManager.cpp` (`8d8f35fc…`), `src/debug/HyprCtl.cpp` (`798b7c6c…`).
- **Committed Historical Host Capture:** `.ufo/waves/round-13/w1/globals.json` (round 13, S041) advertises global `wl_seat` at version 9, `zwp_text_input_manager_v3` at version 1, `zwp_text_input_manager_v1` at version 1, and `zwp_input_method_manager_v2` at version 1. It explicitly lists `"wl_seat human-readable name and capability list"` in its `excluded` field (lines 339–340).
- **Draft Note Under Review:** `.ufo/waves/round-15/input-draft.txt` (round 15, w1) lines 1–96.

### 2.2 Peer Findings & Tensions in the Round Cache
- `ReviewLibinput.md`: Names Lesson M04 (`corpus/lessons/round-12.md:37`) where `libinput list-devices` was erroneously taken as proof of compositor settings. Emphasizes that libinput tools report driver built-in defaults only.
- `AttackDelivery.md`: Identifies at least eight independent exit/drop gates in Hyprland's input and seat pipeline (`InputManager.cpp`, `SeatManager.cpp`) between `wl_seat` capability advertisement and client application receipt (disabled device, permission deny, event-bus cancel, inputCapture, global keybind interception, IME grab, multi-keyboard dedupe, absent client focus resource).
- `TextInputBoundary.md` & `ReviewKeyboard.md`: Prove that `wl_keyboard.key` carries only raw hardware evdev scancodes with no character strings, while `zwp_text_input_v3` carries composed UTF-8 strings (`commit_string`, `preedit_string`) via a double-buffered transaction.
- `ReviewDocsEra.md`: Documents that `pacman -S --needed --noconfirm libinput libinput-tools` was executed mid-round by another seat, upgrading disk packages from `1.31.3-1` to `1.32.0-1`, while the running Hyprland compositor process (PID 1706) still maps deleted in-memory library `/usr/lib/libinput.so.10.13.0 (deleted)` (1.31.3 code).
- `ReviewSafety.md` & `ReviewPrivacy.md`: Prove that `libinput record` preserves timing, modifiers, and hardware IDs while `libinput replay` creates virtual uinput devices (injection/mutation class), mandating that U6 remain strictly documentary.

---

## 3. Tri-Class Evidence Mapping

The following matrix systematically maps each proposed U6 statement to its verified evidence class:
- **`[OBS static-source]`**: Byte-level, hash-verified, or package-queried facts observable in static primary artifacts without running execution or live queries.
- **`[INF-docs]`**: Formal protocol contracts, documented state machines, and interface rules logically inferred from authoritative documentation/XML specifications.
- **`[UNK]`**: Host runtime facts, event delivery paths, and client processing behaviors that remain unexercised and unproved.

| # | Proposed U6 Statement / Rung | OBS static-source (Direct Static Observation) | INF-docs (Documented Interface Semantics) | UNK (Host Runtime & Unexercised Boundary) |
|---|---|---|---|---|
| **1** | **Kernel evdev node access & privilege requirement** | `tools.html` text: *"Most of the tools must be run as root to have access to the kernel’s `/dev/input/event*` device files."* | Input debugging tools interface directly with Linux evdev character devices; root privilege is required for device-level observation. | `[UNK]` Which `/dev/input/event*` nodes exist on this host, what their access permissions are, or whether any device node is attached. |
| **2** | **libinput device enumeration vs. compositor configuration** | `tools.html` text: *"This tool does **not** show your desktop's configuration, just the libinput built-in defaults."* | `list-devices` reports libinput driver defaults and quirks matched against its device database; it runs a standalone libinput context. | `[UNK]` Effective compositor input configuration (unless read via `hyprctl getoption input:*` with `set: true`), per-device sensitivity, or active keymap. |
| **3** | **Event observation and record/replay mechanics** | `tools.html` text: *"The recorded events are **kernel events** and independent of the libinput context."* Tag 1.32.0 `tools.rst` SHA-256 `53264328…`. | `libinput record` logs raw kernel evdev sequences; `libinput replay` instantiates a new virtual device via uinput (injection class). | `[UNK]` Whether any event occurred on the host, whether events reached the compositor, or whether replay was ever executed (strictly prohibited). |
| **4** | **Data protection & keycode obfuscation scope** | `tools.html` text: *"For data protection, libinput record obscures key codes by default, any alphanumeric key shows up as letter 'a'."* | Obfuscation applies to evdev keycodes 2–57 and 71–83 only. Modifiers (CTRL, ALT, META), navigation (ESC, TAB, ENTER), function keys (F1–F10), and inter-event timing survive in plain YAML. | `[UNK]` Host keystroke content; no recording was created, collected, or persisted on this host. |
| **5** | **Compositor seat inventory & keymap compiling** | Host package `hyprland 0.56.2-2` (commit `efb50993…`). Round-3 host capture: `hyprctl devices` reported keyboards with `active_keymap: Portuguese (Brazil)`. | `hyprctl devices` and `getoption input:*` report the compositor's internal evaluation of configured devices and XKB compilation. | `[UNK]` Whether hardware keyboard state matches compositor keymap; whether compositor device nodes currently receive kernel events. |
| **6** | **`wl_seat` capability advertisement lifecycle** | `/usr/share/wayland/wayland.xml:2030-2057` (`wl_seat.capabilities`, version 11). `globals.json:339-340` advertises `wl_seat` at version 9. | `capabilities` event advertises seat-wide device classes (`POINTER`, `KEYBOARD`, `TOUCH`) on binding or device hotplug. It is a presence bitmask, not a per-client grant. | `[UNK]` Whether `wl_seat` on this host advertises keyboard or pointer capability (capability list was deliberately excluded in `globals.json`). |
| **7** | **`wl_keyboard` surface focus & active surface rule** | `/usr/share/wayland/wayland.xml:2614-2636` (`enter`/`leave`), `:2684-2686` (`key`). | `enter` assigns keyboard focus to a `wl_surface`. The compositor *must not* send `key` events if the client object did not have an active surface immediately before the event. | `[UNK]` Which surface currently holds compositor keyboard focus, or whether any `enter` or `leave` event was dispatched to a client. |
| **8** | **`wl_keyboard` raw scancodes vs. text abstraction** | `/usr/share/wayland/wayland.xml:2669-2700` (`key`), `:2596-2612` (`keymap_format.xkb_v1`). | `key` delivers platform evdev scancodes (`uint key`, `key_state state`). Clients must add 8 to obtain the XKB keycode. It carries NO character strings, keysyms, or UTF-8 text. | `[UNK]` What keysym the client's local XKB state machine produced, whether dead keys composed, or how the application translated scancodes. |
| **9** | **`wl_pointer` focus, relative coordinates & frame** | `/usr/share/wayland/wayland.xml:2197-2325` (`enter`, `motion`, `button`, `frame`). | Pointer focus is surface-scoped; motion coordinates `(surface_x, surface_y)` are relative to the focused surface; `frame` demarcates atomic event packets. | `[UNK]` Pointer focus state, surface coordinates, button presses, motion events, or rendered cursor position on this host. |
| **10** | **Text input & IME double-buffered transaction** | `/usr/share/wayland-protocols/unstable/text-input/text-input-unstable-v3.xml:50-583` (`zwp_text_input_v3`, SHA-256 `160815cd…`). | `commit_string` and `preedit_string` deliver composed UTF-8 text. State changes are double-buffered and evaluated atomically in a 7-step sequence upon `done(serial)`. | `[UNK]` Whether text-input-v3 or an IME daemon (e.g. `fcitx5`) was bound or active, or whether any preedit/commit text was delivered. |
| **11** | **Client application outcome & UI response** | None (no application inspection in scope). | Application event loops consume Wayland socket events, update widget state, insert buffer characters, or trigger shortcut actions. | `[UNK]` End-to-end application receipt, widget focus handling, text insertion, shortcut consumption, or visual rendering. |

---

## 4. Unsupported Host Behavior Implications

A rigorous analysis of the round cache reveals six distinct unsupported host behavior implications (contradictions and false inferences). Each represents an invalid inferential leap across layer boundaries that the U6 entry must explicitly reject:

### Implication 1: Inferring Compositor Settings from libinput Tool Defaults
- **False Inference:** "Running `libinput list-devices` or reading its documentation reveals the active input configuration (e.g. tapping, natural scrolling, acceleration profile) applied by Hyprland."
- **Contradiction:** Primary documentation explicitly denies this: *"This tool does **not** show your desktop's configuration, just the libinput built-in defaults."* Compositors instantiate their own libinput context and configure devices according to their own configuration plane (`~/.config/hypr/input.conf`).
- **Precedent & Risk:** Re-opens Lesson M04 (`corpus/lessons/round-12.md:37`).
- **Required Boundary:** Host configuration must be established strictly via `hyprctl getoption input:<key>` with its `set: true` flag or evaluated config bytes. `libinput list-devices` defaults must be labelled `[INF-docs]` defaults only.

### Implication 2: Equating `wl_seat` Capability Advertisement with Application Delivery
- **False Inference:** "Because `wl_seat` advertises keyboard and pointer capabilities (or because `hyprctl devices` lists connected devices), user keystrokes and pointer events successfully reach focused applications."
- **Contradiction:** Grounded source analysis in `AttackDelivery.md` demonstrates that at least **eight independent drop gates** sit in Hyprland's input pipeline (`src/managers/input/InputManager.cpp`, `src/managers/SeatManager.cpp`) before a wire event can be emitted:
  1. *Per-device disable check:* `if (!pKeyboard->m_enabled) return;` (`InputManager.cpp:1620`).
  2. *Permission rule:* `if (!pKeyboard->m_allowed) return;` (dynamic permission deny, `InputManager.cpp:1621`).
  3. *Event-bus cancellation:* Plugins or internal listeners cancel event propagation (`InputManager.cpp:1629`).
  4. *Input capture:* `inputCapture` manager diverts events (`passEvent = false`, `InputManager.cpp:1634`).
  5. *Compositor keybind consumption:* 192 global keybinds intercept chords inside the compositor (`KeybindManager.cpp:841`), swallowing them before client dispatch.
  6. *IME interception:* Active input methods divert key events away from `wl_seat` (`InputManager.cpp:1661`).
  7. *Multi-keyboard deduplication:* Merging duplicate scancodes drops redundant events (`InputManager.cpp:1648`).
  8. *Absent focus resource:* `if (!m_state.keyboardFocusResource) return;` (`SeatManager.cpp:256`).
- **Required Boundary:** `wl_seat.capabilities` proves only device-class presence at the seat level `[INF-docs]`. Delivery to a specific application surface remains unexercised and must be marked `[UNK]`.

### Implication 3: Conflating Raw Keycodes with Typed Characters and IME Composition
- **False Inference:** "Capturing or observing a `wl_keyboard.key` event demonstrates that an application received text or typed input."
- **Contradiction:** `wl_keyboard.key` transmits an integer scancode (evdev scancode) with state (pressed/released). The Wayland core specification explicitly requires the client to translate scancodes using a client-side XKB state machine (`wayland.xml:2596`). Composed Unicode text, dead keys, and CJK ideographs bypass `wl_keyboard.key` entirely and travel over `zwp_text_input_v3` (`commit_string`, `preedit_string`).
- **Required Boundary:** A raw keycode is not text. The boundary between keyboard focus and text-input focus must remain explicit, with text insertion marked `[UNK]`.

### Implication 4: Conflating Documentation Era (1.32.0) with Host Runtime Binary State
- **False Inference:** "The host's running compositor executes libinput 1.32.0 behavior as described on `https://wayland.freedesktop.org/libinput/doc/latest/tools.html`."
- **Contradiction:** As documented by `ReviewDocsEra.md`, the host booted with `libinput 1.31.3-1`. A mid-round package installation updated on-disk packages to `1.32.0-1` (`pacman.log` at 04:25:17), but the running Hyprland compositor process (PID 1706) continues to map `/usr/lib/libinput.so.10.13.0 (deleted)` (1.31.3 code). Furthermore, documentation on `doc/latest/` is an unpinned rolling web page generated from git commit `4cf1775`.
- **Required Boundary:** The U6 entry must explicitly document the version divergence: documentation era (1.32.0) vs. on-disk package (`pacman -Q libinput`) vs. running in-memory process. Upstream documentation prose must not be cited as proof of installed binary execution.

### Implication 5: Inferring Seat Capability Presence from Historical `globals.json`
- **False Inference:** "The committed host capture in `.ufo/waves/round-13/w1/globals.json` (S041) proves that Hyprland advertises keyboard and pointer capabilities on `seat0`."
- **Contradiction:** As proven by `ReviewSeat.md` and `AttackDelivery.md`, the capture script that produced `globals.json` explicitly excluded `"wl_seat human-readable name and capability list"` (lines 339–340). S041 records only `{"interface":"wl_seat","version":9}`. The capability bitmask itself was never captured or retained.
- **Required Boundary:** Host capability advertisement is unobserved on this host and must be labelled `[UNK]`.

### Implication 6: Treating Diagnostic Recording and Replay as Benign Read-Only Probes
- **False Inference:** "`libinput record` and `libinput replay` are safe, passive diagnostic reads suitable for verifying the U6 input ladder."
- **Contradiction:** `ReviewSafety.md` and `ReviewPrivacy.md` prove that:
  1. `libinput record` records keystrokes and timing to persistent disk files; its default obfuscation leaves passwords vulnerable via modifier tracking, control code preservation (ENTER, TAB, ESC), and inter-key timing deltas.
  2. `libinput record --grab` exclusively seizes device nodes, breaking compositor event dispatch.
  3. `libinput replay` creates virtual devices via the kernel uinput interface, injecting synthetic hardware events into the session.
- **Required Boundary:** Recording and replay are state-changing, privacy-violating mutation tools. They are strictly prohibited by the round charter and must be catalogued under `## Safe boundary` as rejected routes.

---

## 5. Proposed Non-Obvious Move: The Tri-Class Drop-Gate Boundary Partition

### 5.1 Move Statement
Synthesizing the findings of `input-draft.txt`, `LayerJoin.md`, `AttackDelivery.md`, `ReviewSeat.md`, `TextInputBoundary.md`, and `ReviewDocsEra.md`, we propose:

> **The Tri-Class Drop-Gate Partition:** Structure the U6 knowledge note (`corpus/knowledge/input-debugging-boundaries-r15.md`) around a formal **Tri-Class Drop-Gate Matrix** that explicitly inserts Hyprland's eight compositor drop gates between Tier 3 (Compositor Inventory) and Tier 4 (Protocol Wire Delivery), locking every gate to `[INF-code]` (source logic) and `[UNK]` (host runtime execution), while restricting Tier 1–2 to `[INF-docs]` (documented tool boundaries) and grounding the header in dual reciprocal `mined` sources (S007 superseding row / S043 scope-clarified).

### 5.2 Second-Order Effects Across Surfaces
1. **Runtime & Substrate Surfaces:**
   - Enforces 100% passive, read-only inspection. Absolutely zero live device reads (`/dev/input/event*`), zero keystroke recordings, zero virtual uinput injections, and zero compositor IPC mutations.
   - Decouples static documentation from the mid-round package upgrade drift (PID 1706 in-memory 1.31.3 vs. on-disk 1.32.0).
2. **Contract & Province Surfaces:**
   - Adheres strictly to `PROVINCE.md`: kernel-level diagnosis and driver faults remain fenced to `tsukuroi-shokunin` (handoff ADJ-03).
   - Complies with `SCORECARD.md:598-621`: provides the exact provenance trio, `covers: U6`, required headings (`## Layer ladder`, `## Safe boundary`, `## Unexercised delivery`), and explicit `[UNK]` in the final section.
   - Satisfies `QUALITY.md` criteria: prevents duplicate registry URLs (criterion 17), enforces scoped data retention (criterion 19), and preserves lesson grounding (criterion 15).
3. **Verification Surface:**
   - Eliminates ambiguity for structural measurement tools (`measure.py` exits 0 with coverage 6/7) while providing a transparent, falsifiable boundary for non-author verifiers.

---

## 6. Risks & Trade-Offs

1. **Source Registry Collision Risk:**
   - *Risk:* `spec.json` reserved `S051` for libinput tools and `S052` for Wayland core XML. However, `SOURCES.md:19` already holds queued `S007` pointing to `tools.html`, and `SOURCES.md:55` holds mined `S043` pointing to `/usr/share/wayland/wayland.xml`. Creating unlinked duplicates would violate QUALITY criterion 17.
   - *Mitigation:* L1 planner must either promote `S007` in place with a pinned revision anchor or append a superseding row (`supersedes S007 —`), and clarify `S043`'s scope (which was historically pinned to `wl_registry`) to explicitly cover `wl_seat`, `wl_pointer`, and `wl_keyboard`.
2. **Docs-Era Drift Risk:**
   - *Risk:* Quoting libinput 1.32.0 documentation while the running session executes 1.31.3 code risks verifier challenge.
   - *Mitigation:* Explicitly cite tag `1.32.0` raw source SHA-256 (`53264328…`) as a documentation-era authority, state the installed package version from `pacman -Q`, and record runtime execution as `[UNK]`.

---

## 7. Verification Steps for Main Agent

Upon integration by canonical planner L1, the main agent should verify:
1. **Structural Measurement Probe:**
   `python3 .ufo/waves/round-15/measure.py <COMMIT>` executes cleanly and reports coverage **6/7 (8.5714/10)**, with navigation 29/29 and zero missing/extra/duplicate records.
2. **Registry Integrity:**
   `bash tools/mado-verify.sh --selftest` and sources census commands exit 0 with zero unlinked duplicate URLs.
3. **Boundary Verification:**
   Inspect `corpus/knowledge/input-debugging-boundaries-r15.md` to confirm:
   - Header contains provenance trio (`source:`, `verified-at:`, `recheck:`) and `covers: U6`.
   - Headings `## Layer ladder`, `## Safe boundary`, and `## Unexercised delivery` are present.
   - `## Unexercised delivery` contains explicit `[UNK]` tags for event delivery, IME, and application outcome.
   - Zero live device outputs, device serials, or keystroke logs are present in repo artifacts.

---

*Report written to `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/EvidenceClassJoin.md`.*
