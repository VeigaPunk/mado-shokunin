# LayerJoin — U6 Input Evidence Ladder and R14 Ancillary Provenance Correction

**Seat:** `MadoR15.LayerJoin` (connector, leaf)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Judged on:** `coverage` (lowest active finite rubric 5/7 → 6/7)  
**Milestone:** U6 input evidence ladder and R14 ancillary provenance correction  
**Report path:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/reports/LayerJoin.md`  

---

## 1. Named Axes

1. **coverage (Primary / Scored):** Advances U-item current-art ground from U1–U5 (5/7 = 7.1429/10) to U1–U6 (6/7 = 8.5714/10) by establishing the verifiable input-debugging ladder connecting libinput documentation, compositor device/option reads, Wayland core protocol focus, and client application outcome without feature exercise or live event probes.
2. **operability (Harm Watch):** Prevents false-positive capability claims by proving why lower-layer device presence or tool defaults do not imply compositor configuration, protocol focus, or application delivery; preserves hermetic gate boundaries.
3. **calibration (Harm Watch):** Retains lane lesson M04 (`corpus/lessons/round-12.md:37` / discernment criterion 15) prohibiting the inverse inference that `libinput list-devices` reflects compositor configuration; formalizes R14-V1 ancillary receipt precision as an explanatory sidecar mapping without rewriting historical bytes.
4. **freshness / adjacency (Harm Watch):** Avoids absorbing kernel evdev diagnosis or hardware fault isolation (strictly sibling `tsukuroi` province); enforces read-only documentation inspection and static XML parsing, refusing live event capture, keystroke recording, and uinput replay.

---

## 2. Evidence Grounding

All references are grounded strictly in primary primary documentation, static XML protocol definitions, and committed lane evidence:

### E1. libinput 1.32.0 Official Helper Tools Documentation
* **Source:** `https://wayland.freedesktop.org/libinput/doc/latest/tools.html` (generated from git commit `4cf1775`) & tag `1.32.0` (`doc/user/tools.rst` sha256 `53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f`).
* **Anchors & Quotes (≤25 words):**
  * *list-devices limitation:* `"This tool does not show your desktop's configuration, just the libinput built-in defaults."` (`tools.html#libinput-list-devices`)
  * *Human consumption warning:* `"This tool is intended for human-consumption and may change its output at any time."` (`tools.html#libinput-list-devices`)
  * *Privileged access:* `"Most of the tools must be run as root to have access to the kernel's /dev/input/event* device files."` (`tools.html`)
  * *Kernel event independence:* `"The recorded events are kernel events and independent of the libinput context."` (`tools.html#libinput-record-and-libinput-replay`)
  * *Data protection default:* `"For data protection, libinput record obscures key codes by default, any alphanumeric key shows up as letter 'a'."` (`tools.html#libinput-record-and-libinput-replay`)
  * *Virtual device creation:* `"libinput replay creates a new virtual device based on the description in the log file."` (`tools.html#libinput-record-and-libinput-replay`)

### E2. Wayland Core Protocol XML Specification
* **Source:** `/usr/share/wayland/wayland.xml` (installed package `wayland 1.26.0-1`, sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`, S043 pin).
* **Anchors & Quotes (≤25 words):**
  * *wl_seat:* `"A seat is a group of keyboards, pointer and touch devices... A seat typically has a pointer and maintains a keyboard focus and a pointer focus."` (`wayland.xml:2006-2009`)
  * *wl_seat.capabilities:* `"This is sent on binding to the seat global or whenever a seat gains or loses the pointer, keyboard or touch capabilities."` (`wayland.xml:2032-2035`)
  * *wl_keyboard logical state:* `"Each wl_keyboard has the following logical state: - an active surface (possibly null), - the keys currently logically down, - the active modifiers, - the active group."` (`wayland.xml:2578-2583`)
  * *wl_keyboard.enter:* `"Notification that this seat's keyboard focus is on a certain surface."` (`wayland.xml:2616-2617`)
  * *wl_keyboard.key active surface restriction:* `"The compositor must not send this event if the wl_keyboard did not have an active surface immediately before this event."` (`wayland.xml:2684-2686`)
  * *wl_pointer.enter:* `"Notification that this seat's pointer is focused on a certain surface."` (`wayland.xml:2199-2200`)

### E3. Compositor Configuration & Runtime Read Verbs
* **Source:** Hyprland 0.56.2 (commit `efb50993...`), `SKILL.md:40-75`, `corpus/knowledge/hyprctl-verification-layer.md:123-160`, and `config-health-report-r3.md:157-161, 731-732`.
* **Anchors:**
  * `hyprctl getoption input:kb_layout` → `str: br`, `set: true` (evaluates entire 17/18-file include chain; user `input.conf:10` overrides default `us`).
  * `hyprctl -j devices` enumerates compositor-bound device nodes (e.g. 9 keyboard nodes, 4 mice, 0 touch devices), all with `active_keymap: Portuguese (Brazil)`.
  * `hyprctl binds -j` enumerates 192 live global keybindings intercepting key events inside the compositor before any client surface sees them.

### E4. R14-V1 Ancillary Receipt Provenance & Target Excision
* **Source:** `corpus/lessons/round-14-verifier-spotcheck.md:169`, `.ufo/waves/round-14/evidence/committed-bindings.json:2-13`, and `tools/mado-verify.sh:1723-1733`.
* **Anchors:**
  * Committed revision `32118fc1014837b3a385c7a66abbdc59b1560835` holds raw whole-gate digest `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`.
  * `mado_r7_target_build` derives target SHA-256 `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96` (117,602 bytes) by excising R7 selftest, R7 regression, and R8 blocks.
  * The three mutation receipts (`regression-recut.txt`, `regular-target-mutants.txt`, `retained-census-mutants.txt`) carry provisional headers (`ef50e262...`, `d6d5eb27...`) but faithfully bind to derived target `cd1d73d7...`.

---

## 3. Proposed Move: The Five-Tier Input Evidence Ladder

We establish a synthesis across the round's proposals by connecting all input observation rungs into a strict, unidirectional **Input Evidence Ladder**. Each row explicitly defines what the observation proves, what it does **not** prove, and the architectural mechanism that separates them.

### The Input Evidence Ladder

| Tier / Subsystem | Primary Grounded Evidence Class | What It Strictly PROVES (Observable Proof Scope) | What It Does NOT Prove (Falsification / Non-Sequitur Boundary) | Decoupling Mechanism (Why the Inference Fails) |
|---|---|---|---|---|
| **Tier 1: Kernel evdev & Hardware Detection** | `/dev/input/event*`<br>`libinput list-kernel-devices`<br>`tools.html#libinput-list-kernel-devices` | • Kernel device node existence and driver attachment.<br>• Low-level evdev capabilities reported by kernel (`KEY`, `REL`, `ABS`).<br>• Underlying USB/HID bus identifiers (`--hid`). | • Does NOT prove libinput initialization or quirk application.<br>• Does NOT prove compositor recognition or event ingestion.<br>• Does NOT prove Wayland surface delivery or application responsiveness. | Kernel device nodes can be ignored, unassigned by udev, grabbed exclusively by another daemon, or missing seat tags (`seat0`). |
| **Tier 2: Libinput Driver Defaults & Calibration** | `libinput list-devices`<br>`tools.html#libinput-list-devices`<br>`reporting-bugs.html` | • Hardware properties recognized by libinput library.<br>• Built-in driver defaults for tapping, natural scroll, and clickfinger.<br>• Libinput quirks matched against vendor/model database. | • **Does NOT prove desktop/compositor configuration.**<br>• Does NOT prove compositor active keymap, layout, or sensitivity.<br>• Does NOT prove event delivery to Wayland clients. | Primary doc explicitly warns: *"This tool does NOT show your desktop's configuration, just the libinput built-in defaults."* Compositors override defaults via internal configuration. |
| **Tier 3: Compositor Seat Inventory & Config** | `hyprctl devices`<br>`hyprctl getoption input:*`<br>`hyprctl-verification-layer.md` | • Compositor-instantiated device nodes (e.g. 9 keyboards, 4 mice).<br>• Evaluated configuration after full include hierarchy (`kb_layout = br`).<br>• Active XKB keymap compiled by the compositor. | • Does NOT prove physical evdev health or hardware fault absence.<br>• Does NOT prove key/motion events reach Wayland client surfaces.<br>• Does NOT prove event bypass around global keybindings. | **Compositor Bind Interception:** 192 global bindings consume key combinations in the compositor (e.g. `SUPER+Q`, `SUPER+Return`), stripping them from the event stream before client dispatch. |
| **Tier 4: Wayland Protocol Focus & Wire Events** | `wl_seat.capabilities`<br>`wl_keyboard.enter/key`<br>`wl_pointer.enter/motion`<br>`wayland.xml:2004-2720` | • Client surface holds active keyboard or pointer focus (`enter` event with serial).<br>• Serialized keycodes, modifier state, and xkb keymap fd delivered over Wayland socket.<br>• Surface-local coordinates `(sx, sy)` on pointer motion. | • Does NOT prove that physical keypresses were delivered (unbound keys only).<br>• Does NOT prove input method / IME bypass.<br>• Does NOT prove unfocused, background, or occluded windows receive input.<br>• Does NOT prove client processed the event. | **Surface Focus & IME Isolation:** Wayland sends `wl_keyboard.key` *only* to the currently focused surface (`wayland.xml:2684`). Text-input protocols (`zwp_text_input_v1/v3`) intercept raw keys, converting them to IME preedit/commit strings. |
| **Tier 5: Client Application Outcome** | Toolkit event loop<br>Widget focus state<br>Application UI update | • Application logic executed (character inserted, menu opened, button triggered).<br>• Successful end-to-end traversal across all 5 tiers. | • Does NOT prove health of any single upstream tier in isolation.<br>• App failure does not identify whether root cause was hardware, driver, compositor bind, focus loss, IME, or hung UI thread. | An application event loop starvation, unhandled keycode, or modal dialog drop produces the identical symptom as a disconnected cable or stolen bind. |

---

## 4. Second-Order Effects & Traps Across Surfaces

1. **Lesson M04 Anti-Trap (Discernment Criterion 15):**  
   `corpus/lessons/round-12.md:37` records the critical mistake: asserting that `libinput list-devices` proves compositor-applied settings. The evidence ladder permanently closes this trap by grounding Tier 2 in `tools.html:43-44`'s explicit denial and establishing Tier 3 (`hyprctl getoption input:*` with `set: true`) as the only valid proof of compositor-applied input configuration.

2. **Privacy and Safety Boundary (No Keystroke Leaks):**  
   - Libinput debugging tools (`debug-events`, `record`, `debug-gui`) require root access to `/dev/input/event*`.  
   - `debug-events` streams live events in plaintext, acting as a direct keylogger. Even though `libinput record` obscures alphanumeric keys as `'a'` by default, modifier keys, control codes, function keys, and event timing are preserved in plain YAML, exposing sensitive password lengths and interaction habits.  
   - The U6 route is strictly bounded to **read-only documentation inspection and static protocol XML parsing**. No live device reads, event captures, keystroke logging, or uinput replays are authorized or required.

3. **Runtime vs Installed Library Split:**  
   ReviewDocsEra observed that `libinput 1.32.0-1` was installed during round 15, but running Hyprland (PID 1706) holds memory maps to `/usr/lib/libinput.so.10.13.0 (deleted)` from version `1.31.3-1`. The ladder prevents invalid inferences by anchoring driver defaults to the documentation era (`1.32.0`) and compositor behavior to the pinned compositor release (0.56.2 `efb50993...`), explicitly acknowledging that running processes decouple from on-disk packages until operator restart.

4. **R14-V1 Ancillary Receipt Precision Integration:**  
   The R14-V1 verifier ruling (`round-14-verifier-spotcheck.md:169`) noted that three mutation receipts carried provisional whole-gate hashes (`ef50e262...`, `d6d5eb27...`) while accurately testing derived target `cd1d73d7...`. In exact parallel to Tier 2 vs Tier 3 input separation, conflating a provisional whole-gate header with derived-target execution is an object-identity category error. The resolution is an append-only sidecar mapping in `.ufo/waves/round-15/receipt-correction.json` connecting provisional headers to committed target `cd1d73d7...` without altering historical receipt bytes.

---

## 5. Risks and Mitigations

| Risk | Consequence | Mitigation |
|---|---|---|
| **Sources Collision (QUALITY 17)** | Adding a new S051 row pointing to `tools.html` collides with existing `queued` S007. | L1 should promote S007 in-place (`queued` → `mined`, anchor pinned to git commit `4cf1775` / tag `1.32.0`), or create a formal superseding row explicitly declaring `supersedes S007`. |
| **Core XML Duplicate (S052 vs S043)** | Citing `/usr/share/wayland/wayland.xml` for `wl_keyboard` duplicates S043 (`wayland.xml:117-177`). | Reuse S043 in-place by expanding its `anchor` to include lines `2004-2720` and appending `corpus/knowledge/input-evidence-ladder-r15.md` to `used-by`, or cite upstream release tag commit directly. |
| **Compositor Bind Confusion** | Mistaking an unhandled keystroke in an app for a broken input stack. | Explicitly check Tier 3 keybind surface (`hyprctl binds -j`): if `SUPER` or active modifiers match a compositor dispatcher, the event is intentionally stripped at Tier 3. |
| **IME / Text-Input Shadowing** | IME protocols suppress `wl_keyboard.key` in favor of preedit/commit strings. | The ladder bounds `wl_keyboard` to direct physical key delivery and marks IME-handled text streams as a distinct protocol phase (`[UNK]`). |

---

## 6. Verification and Acceptance Criteria

The integrator / L1 planner should verify the landed U6 artifacts against the following criteria:

1. **Structural Coverage (C1):** `python3 .ufo/waves/round-15/measure.py REV` reports `U1 U2 U3 U4 U5 U6`, `6/7`, score `8.5714/10` with zero registry collision warnings.
2. **Ladder Completeness:** The U6 note contains the five distinct tiers with explicit "PROVES" and "DOES NOT PROVE" columns and labels all unexercised delivery/IME paths as `[UNK]`.
3. **No M04 Inversion:** Zero sentences claim that `libinput list-devices` reflects desktop/compositor configuration.
4. **Hermetic Safety:** Zero event captures, raw `/dev/input` reads, or uinput injection scripts exist in repository evidence.
5. **R14-V1 Sidecar:** `.ufo/waves/round-15/receipt-correction.json` maps `ef50e262...` and `d6d5eb27...` to `cd1d73d7...` and committed commit `32118fc1...` while leaving original receipt digests unchanged.

---

## 7. Tooling Record

* **Installed / Updated Tools:** None. All inspections performed using existing packages (`wayland 1.26.0-1`, `hyprland 0.56.2-2`, `libinput 1.32.0-1`), static file reads (`/usr/share/wayland/wayland.xml`), and official online documentation (`tools.html`).
* **Environment Integrity:** No mutating compositor commands, live input event reading, or privileged operations were executed.
