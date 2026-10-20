# TextInputBoundary — Wayland text-input-v3 vs. wl_keyboard Boundary Evidence Report

**Seat:** `MadoR15.TextInputBoundary` (scout, leaf)  
**Target:** `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Milestone:** U6 input evidence ladder and R14 ancillary provenance correction  
**Judged on:** `coverage` (C1)  
**Status:** Complete scoped findings on text/IME protocol boundary vs. `wl_keyboard` key delivery. Read-only static XML and package inspection; no live probes, no device access, no event injection, no registry mutation.

---

## 1. Axes & Non-Regressive Posture (Godspeed)

| Axis | Role & Impact | Non-Regressive Boundary |
|---|---|---|
| **coverage (C1)** | Expands the evidentiary ladder for milestone U6 by establishing the exact structural, semantic, and transactional boundary separating input-method text composition (`zwp_text_input_v3`) from low-level keyboard delivery (`wl_keyboard`). | Reports exact source anchors as **unadmitted context** only. Does not add unauthorized rows to `corpus/SOURCES.md` (reserved for canonical planner L1). Does not assert broad runtime IME capabilities. |
| **operability (C2)** | Preserves strict separation between protocol documentation (`[INF-docs]`), historical compositor advertisements (`[OBS-history]`), and unexercised runtime features (`[UNK]`). | Adheres to safe read-only inspection. Executes zero tests, zero live probes, zero `/dev/input/event*` or virtual device operations, and no compositor mutations. |

---

## 2. Primary Source Artifacts Inspected

1. **Wayland Protocols text-input-v3 XML (Primary Focus):**
   - **Local Path:** `/usr/share/wayland-protocols/unstable/text-input/text-input-unstable-v3.xml`
   - **Owning Package:** `wayland-protocols 1.49-1`
   - **File SHA-256:** `160815cda13c285a30df1971d8f0a5b3aac07071537df59916d2f748b18e4f59`
   - **Line Count:** 604 lines
   - **Upstream Source:** `https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/unstable/text-input/text-input-unstable-v3.xml`
   - **Protocol Identity:** `<protocol name="text_input_unstable_v3">`
   - **Interfaces Declared:**
     - `<interface name="zwp_text_input_v3" version="2">` (lines 50–583)
     - `<interface name="zwp_text_input_manager_v3" version="2">` (lines 585–603)

2. **Core Wayland Specification XML (Baseline Comparator):**
   - **Local Path:** `/usr/share/wayland/wayland.xml`
   - **Owning Package:** `wayland 1.26.0-1`
   - **File SHA-256:** `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`
   - **Line Count:** 3,442 lines
   - **Upstream Source:** `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml`
   - **Interface Declared:** `<interface name="wl_keyboard" version="11">` (lines 2573–2752)

---

## 3. Systematic Differentiation: text-input-v3 vs. wl_keyboard

The protocol specifications expose six primary structural and semantic distinctions between text/IME input and core keyboard event delivery:

### 3.1 Data Abstraction & Delivery Primitive: UTF-8 Text vs. Hardware Keycodes

- **`wl_keyboard` (Hardware Keycodes & State Machine):**
  - Delivers raw platform keycodes (Linux evdev scancodes) via `wl_keyboard.key` (`<arg name="key" type="uint"/>`, `<arg name="state" type="uint" enum="key_state"/>`, lines 2669–2700).
  - Delivers keyboard layout translations via `wl_keyboard.keymap` (lines 2600–2612) sending a read-only file descriptor containing an XKB keymap (`xkb_v1 = 1`).
  - Delivers modifier bitmasks via `wl_keyboard.modifiers` (`mods_depressed`, `mods_latched`, `mods_locked`, `group`, lines 2701–2722).
  - **Limitation:** The client is entirely responsible for transforming raw scancodes into characters via its local XKB state machine (`"to determine the xkb keycode, clients must add 8 to the key event keycode"`, line 2597). No text strings or complex composition states exist in this interface.
- **`zwp_text_input_v3` (Composed UTF-8 Strings & Pre-edit):**
  - Delivers fully composed strings via `commit_string` (`<arg name="text" type="string" allow-null="true"/>`, lines 390–402):
    > *"Notify when text should be inserted into the editor widget. The text to commit could be either just a single character after a key press or the result of some composing (pre-edit)."* (lines 392–394).
  - Delivers active composing text via `preedit_string` (`<arg name="text" type="string"/>`, `<arg name="cursor_begin" type="int"/>`, `<arg name="cursor_end" type="int"/>`, lines 364–388):
    > *"Notify when a new composing text (pre-edit) should be set at the current cursor position. Any previously set composing text must be removed. Any previously existing selected text must be removed."* (lines 366–368).
  - Delivers contextual deletion via `delete_surrounding_text` (`<arg name="before_length" type="uint"/>`, `<arg name="after_length" type="uint"/>`, lines 404–423), allowing the IME to modify or delete existing editor text buffer bytes around the cursor.

### 3.2 State Synchronization & Double-Buffering: Transaction Pipeline vs. Immediate Stream

- **`wl_keyboard` (Unbuffered Discrete Stream):**
  - Keystrokes (`key`) and modifier changes (`modifiers`) are emitted immediately as discrete asynchronous events. There is no batching, no double-buffering, and no transaction boundary.
- **`zwp_text_input_v3` (Bidirectional Double-Buffered Transaction with Serial Tracking):**
  - **Client-to-Compositor:** Requests that set state (`enable`, `disable`, `set_surrounding_text`, `set_text_change_cause`, `set_content_type`, `set_cursor_rectangle`, `set_available_actions`) modify pending state only. They are applied atomically to current state upon an explicit `commit` request (lines 305–331):
    > *"Text input state (enabled status, content purpose, content hint, surrounding text and change cause, cursor rectangle) is conceptually double-buffered within the context of a text input... The compositor must count the number of commit requests coming from each zwp_text_input_v3 object and use the count as the serial in done events."* (lines 312–329).
  - **Compositor-to-Client:** Events updating editor state (`preedit_string`, `commit_string`, `delete_surrounding_text`, `action`, `preedit_hint`) are double-buffered and do NOT take immediate effect. They are staged in pending state and applied together when the compositor emits `done(serial)` (lines 425–459).
  - **Evaluation Ordering:** The `done` event mandates an explicit 7-step evaluation order (lines 435–445):
    1. Replace existing preedit string with the cursor.
    2. Delete requested surrounding text.
    3. Insert commit string with the cursor at its end.
    4. Calculate surrounding text to send.
    5. Insert new preedit text in cursor position.
    6. Place cursor inside preedit text.
    7. Perform the requested action.

### 3.3 Contextual Awareness & Bidirectional Feedback: Rich Semantics vs. Context-Blind

- **`wl_keyboard` (Context-Blind):**
  - The compositor transmits hardware scancodes with zero visibility into what kind of input field is focused (e.g., password, terminal, URL bar), what text currently surrounds the cursor, or where the cursor is rendered on the screen.
- **`zwp_text_input_v3` (Rich Bidirectional Feedback):**
  - **Surrounding Text:** `set_surrounding_text` (lines 130–167) transmits up to 4,000 bytes of UTF-8 plain text with byte offsets for `cursor` and `anchor` (selection bounds), enabling contextual autocompletion and complex script transliteration.
  - **Text Change Cause:** `set_text_change_cause` (lines 177–195) informs the IME whether a text buffer modification was caused by `input_method` (`0`) or `other` (`1`, e.g., direct keyboard navigation or mouse paste), allowing the IME to reset or adjust active pre-edit text.
  - **Content Purpose and Hints:** `set_content_type` (lines 248–264) transmits:
    - `content_purpose` (lines 224–246): `normal`, `alpha`, `digits`, `number`, `phone`, `url`, `email`, `name`, `password`, `pin`, `date`, `time`, `datetime`, `terminal`.
    - `content_hint` bitfield (lines 197–222): `none`, `completion`, `spellcheck`, `auto_capitalization`, `lowercase`, `uppercase`, `titlecase`, `hidden_text`, `sensitive_data`, `latin`, `multiline`, `on_screen_input_provided` (v2), `no_emoji` (v2), `preedit_shown` (v2).
  - **Cursor Positioning:** `set_cursor_rectangle` (lines 266–303) sends surface-local rectangle coordinates `(x, y, width, height)` allowing the compositor/IME candidate popup window to follow the cursor without occluding text. In version 2, these values synchronize with `wl_surface.commit` (lines 286–297).

### 3.4 Focus Domain & Activation Lifecycle: Widget-Level vs. Surface-Level

- **`wl_keyboard` (Surface-Level Hardware Focus):**
  - Keyboard focus is tied strictly to surface boundaries via `wl_keyboard.enter` (`surface`, `keys`, lines 2614–2633) and `wl_keyboard.leave` (`surface`, lines 2635–2650).
- **`zwp_text_input_v3` (Widget-Level Logical Input Focus):**
  - While text-input focus follows surface keyboard focus (`enter` lines 333–345, `leave` lines 347–362), inside a focused surface the client must explicitly enable or disable text input as UI focus shifts between editable and non-editable widgets:
    - `enable` (lines 87–118): *"This request must be issued every time the focused text input changes to a new one, including within the current surface."* (lines 92–93).
    - `disable` (lines 120–128): *"Explicitly disable text input on the current surface (typically when there is no focus on any text entry inside the surface)."* (lines 122–123).
    - Single-focus invariant: *"Clients must not enable more than one text input on the single seat and should disable the current text input before enabling the new one."* (lines 97–98).

### 3.5 Panel & Language Controls (Version 2 Additions)

- **`wl_keyboard`:** No protocol representation of virtual input panels or language metadata.
- **`zwp_text_input_v3`:**
  - `show_input_panel` (lines 518–526) / `hide_input_panel` (lines 528–536): Client hints requesting the compositor to show or hide an on-screen keyboard (OSK) or handwriting panel.
  - `language` event (lines 490–500): Compositor/IME notifies the client of the active input method language formatted as an IETF BCP 47 tag.
  - `preedit_hint` event (lines 555–582): Provides contextual styling hints (`whole`, `selection`, `prediction`, `prefix`, `suffix`, `spelling_error`, `compose_error`) for rendering complex composing text.
  - `action` / `set_available_actions` (lines 466–488, 502–516): Handles semantic widget actions (e.g. `submit` for search/URL bars).

### 3.6 Protocol Governance & Development Phase

- **`wl_keyboard`:**
  - Defined in Wayland core (`wayland.xml`), stable since Wayland 1.0, current interface version 11.
- **`zwp_text_input_v3`:**
  - Placed under `unstable/text-input/` in `wayland-protocols`.
  - Retains the legacy `z` prefix indicating unstable staging.
  - Governed by explicit experimental caveat in preamble (lines 40–47):
    > *"Warning! The protocol described in this file is experimental and backward incompatible changes may be made."*

---

## 4. Source Anchors (Unadmitted Context)

Below are the exact source anchors from `/usr/share/wayland-protocols/unstable/text-input/text-input-unstable-v3.xml` and `/usr/share/wayland/wayland.xml`. These anchors are reported as **unadmitted context** for the U6 ladder; no extra row is added to `corpus/SOURCES.md` by this leaf seat.

| Anchor Tag / Line Range | Protocol / Interface | Element Name | Verbatim Anchor Text / Specification Fact |
|---|---|---|---|
| `text-input-unstable-v3.xml:40-47` | `text_input_unstable_v3` | `<description>` | `"Warning! The protocol described in this file is experimental and backward incompatible changes may be made."` |
| `text-input-unstable-v3.xml:50-78` | `zwp_text_input_v3` v2 | `<description>` | `"The zwp_text_input_v3 interface represents text input and input methods associated with a seat... The information about the entered text is sent to the text-input object via the preedit_string and commit_string events."` |
| `text-input-unstable-v3.xml:87-118` | `zwp_text_input_v3` v2 | `<request name="enable">` | `"Requests text input on the surface previously obtained from the enter event. This request must be issued every time the focused text input changes to a new one, including within the current surface."` |
| `text-input-unstable-v3.xml:130-167` | `zwp_text_input_v3` v2 | `<request name="set_surrounding_text">` | Plain text buffer up to 4000 UTF-8 bytes with byte offsets for `cursor` and selection `anchor`. |
| `text-input-unstable-v3.xml:177-195` | `zwp_text_input_v3` v2 | `<request name="set_text_change_cause">` | Enum `change_cause`: `input_method = 0`, `other = 1`. Informs IME of external edits (e.g. keyboard typing). |
| `text-input-unstable-v3.xml:197-264` | `zwp_text_input_v3` v2 | `<request name="set_content_type">` | Bitfield `content_hint` (14 flags) and enum `content_purpose` (14 purposes including `password`, `terminal`, `url`). |
| `text-input-unstable-v3.xml:266-303` | `zwp_text_input_v3` v2 | `<request name="set_cursor_rectangle">` | Coordinates `(x, y, width, height)` in surface-local space; applies on `wl_surface.commit` since version 2. |
| `text-input-unstable-v3.xml:305-331` | `zwp_text_input_v3` v2 | `<request name="commit">` | Double-buffered pending state applied atomically; compositor counts commit requests as serial for `done`. |
| `text-input-unstable-v3.xml:364-388` | `zwp_text_input_v3` v2 | `<event name="preedit_string">` | Ephemeral composing text `<arg name="text" type="string"/>` with byte offsets `cursor_begin` and `cursor_end`. |
| `text-input-unstable-v3.xml:390-402` | `zwp_text_input_v3` v2 | `<event name="commit_string">` | Committed UTF-8 text string inserted into editor widget at cursor. |
| `text-input-unstable-v3.xml:404-423` | `zwp_text_input_v3` v2 | `<event name="delete_surrounding_text">` | Byte lengths `before_length` and `after_length` around cursor to delete. |
| `text-input-unstable-v3.xml:425-459` | `zwp_text_input_v3` v2 | `<event name="done">` | Evaluates double-buffered events in strict 7-step order using commit serial handshake. |
| `text-input-unstable-v3.xml:518-536` | `zwp_text_input_v3` v2 | `<request name="show_input_panel">` / `hide_input_panel` | Client hints requesting on-screen keyboard visibility. |
| `text-input-unstable-v3.xml:585-603` | `zwp_text_input_manager_v3` v2 | `<interface>` | Global singleton factory: `<request name="get_text_input">` binds text input to a `wl_seat`. |
| `wayland.xml:2573-2587` | `wl_keyboard` v11 | `<description>` | Core keyboard interface representing physical seat keyboards: active surface, logically down keys, active modifiers, active layout group. |
| `wayland.xml:2589-2612` | `wl_keyboard` v11 | `<event name="keymap">` | Keymap fd (`xkb_v1 = 1`). Client adds 8 to evdev keycode to obtain XKB keycode. |
| `wayland.xml:2669-2700` | `wl_keyboard` v11 | `<event name="key">` | Discrete physical key events: `<arg name="key" type="uint"/>` and `<arg name="state" type="uint" enum="key_state"/>` (`released = 0`, `pressed = 1`, `repeated = 2`). |
| `wayland.xml:2701-2722` | `wl_keyboard` v11 | `<event name="modifiers">` | State bitmasks: `mods_depressed`, `mods_latched`, `mods_locked`, layout `group`. |

---

## 5. Host Context Correlation & Evidentiary Boundaries

1. **Compositor Advertisement in S041 Capture (`globals.json`):**
   - Historical capture `.ufo/waves/round-13/w1/globals.json:114–117` confirms that Hyprland 0.56.2 advertises:
     ```json
     {
       "interface": "zwp_text_input_manager_v3",
       "version": 1
     }
     ```
   - **Version Discrepancy Note:** The installed XML in `wayland-protocols 1.49-1` defines interface version **2** (adding `preedit_hint`, `show_input_panel`, `hide_input_panel`, `language`, `action`, `error`). However, the host compositor advertised version **1**. In accordance with Wayland protocol binding semantics (`wl_registry.bind`), a client cannot bind version 2 features if the compositor advertises version 1.
2. **fcitx5 Virtual Device vs. Wire Protocol:**
   - In `corpus/knowledge/config-health-report-r3.md:411–416` (F9), a virtual keyboard node `hl-virtual-keyboard-fcitx5` was observed under `hyprctl devices`.
   - **Falsification / Safety Fence:** The presence of a virtual keyboard node in compositor device tables reflects a virtual hardware emulation path (e.g. `zwp_virtual_keyboard_v1` or uinput), NOT wire-level `zwp_text_input_v3` delivery. Protocol XML text cannot establish whether any running client or compositor actually negotiates or uses `zwp_text_input_v3`.
3. **Classification Table:**
   - `[INF-docs]`: Upstream protocol definitions, request/event structures, and transaction ordering in `text-input-unstable-v3.xml` and `wayland.xml`.
   - `[OBS-history]`: Compositor advertisement of `zwp_text_input_manager_v3` version 1 in S041 (`globals.json`).
   - `[UNK]`: Actual runtime invocation of `zwp_text_input_v3` by client toolkits (GTK, Qt), actual IME engine message passing, and whether version 1 vs. version 2 differences impact running applications.

---

## 6. Judgement

- **Coverage (C1):** Successfully resolves the specific text/IME input boundary vs. `wl_keyboard` key delivery using primary Wayland XML sources, establishing exact source anchors for the U6 evidence ladder.
- **Operability (C2):** Preserves all non-regressive boundaries: no unauthorized edits to `corpus/SOURCES.md`, no over-claiming of runtime IME capabilities, and zero mutating probes.

---

## 7. Tooling Record

No tools were installed or upgraded during this task (`pacman`, `uv`, `cargo`, and official binaries unchanged).
