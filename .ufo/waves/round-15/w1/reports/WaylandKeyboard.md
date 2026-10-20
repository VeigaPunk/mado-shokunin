# WaylandKeyboard — round 15 / w1 — report

Seat: `MadoR15.WaylandKeyboard` (scout, leaf; no delegation, no background jobs).  
Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`.  
Axis: **coverage** (primary Wayland core XML `wl_keyboard` enter/leave/key/keymap semantics and client focus boundaries).  
Milestone context: U6 input evidence ladder and R14 ancillary provenance correction.

---

## 1. Primary Source Identification & Provenance

- **Specification Title:** Wayland Core Protocol XML (`wayland.xml`)
- **Upstream Repository:** `https://gitlab.freedesktop.org/wayland/wayland`
- **Release Tag:** `1.26.0` (commit `87cc8a8728a923fc57938faa81ba0e74f34ecdc7`; annotated tag object `5f430e41167dd359b70fb5e9f584ba2dc058e4cc`)
- **Canonical Upstream Blob URL:**  
  `https://gitlab.freedesktop.org/wayland/wayland/-/blob/1.26.0/protocol/wayland.xml`
- **Canonical Upstream Raw URL:**  
  `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml`
- **Official Documentation HTML Spec:**  
  `https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_keyboard`
- **Local Installed File:** `/usr/share/wayland/wayland.xml` (via Arch Linux official package `wayland 1.26.0-1`)
- **File SHA-256:** `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07` (3,442 lines; byte-identical between local `/usr/share/wayland/wayland.xml` and upstream `1.26.0/protocol/wayland.xml`)
- **Target Interface Range:** `wayland.xml:2573-2752` (`<interface name="wl_keyboard" version="11">`)
- **Authority Tier:** Tier A primary core specification.

---

## 2. Interface Scope & Logical State Specification

The `wl_keyboard` interface represents keyboard input associated with a seat (`wl_seat`).

- **Interface declaration (`wayland.xml:2573`):**
  ```xml
  <interface name="wl_keyboard" version="11">
  ```
- **Interface description (`wayland.xml:2574–2587`):**
  > "The wl_keyboard interface represents one or more keyboards associated with a seat." (lines 2575–2576)

- **Logical State Machine (`wayland.xml:2578–2586`):**
  > "Each wl_keyboard has the following logical state:  
  > - an active surface (possibly null),  
  > - the keys currently logically down,  
  > - the active modifiers,  
  > - the active group.  
  > By default, the active surface is null, the keys currently logically down are empty, the active modifiers and the active group are 0." (lines 2578–2586)

---

## 3. Keymap Semantics (`keymap` Event & `keymap_format` Enum)

- **Enum `keymap_format` (`wayland.xml:2589–2598`):**
  - `no_keymap` (`value="0"`): `"no keymap; client must understand how to interpret the raw keycode"` (line 2595).
  - `xkb_v1` (`value="1"`): `"libxkbcommon compatible, null-terminated string; to determine the xkb keycode, clients must add 8 to the key event keycode"` (line 2597).
  - *Key derivation rule:* Wayland keycodes correspond to Linux evdev scancodes. Clients utilizing `xkb_v1` MUST add `8` to translate the protocol keycode into an XKB-compatible keycode (`xkb_keycode = wl_keycode + 8`).

- **Event `keymap` (`wayland.xml:2600–2612`):**
  - **Signature:** `keymap(format: uint, fd: fd, size: uint)`
  - **Memory mapping semantics (`wayland.xml:2602–2604`):**
    > "This event provides a file descriptor to the client which can be memory-mapped in read-only mode to provide a keyboard mapping description."
  - **Version 7 MAP_PRIVATE mandate (`wayland.xml:2606–2607`):**
    > "From version 7 onwards, the fd must be mapped with MAP_PRIVATE by the recipient, as MAP_SHARED may fail."

---

## 4. Client Focus Boundaries: `enter` and `leave` Semantics

Keyboard focus in Wayland is bounded to exactly one client surface (`wl_surface`) at any given moment.

### A. Focus Acquisition: `enter` Event (`wayland.xml:2614–2633`)

- **Signature:** `enter(serial: uint, surface: object<wl_surface>, keys: array)`
- **Core notification (`wayland.xml:2616–2617`):**
  > "Notification that this seat's keyboard focus is on a certain surface."
- **Modifier follow-up ordering rule (`wayland.xml:2619–2620`):**
  > "The compositor must send the wl_keyboard.modifiers event after this event."
- **Logical state transition & non-reentrancy constraint (`wayland.xml:2622–2625`):**
  > "In the wl_keyboard logical state, this event sets the active surface to the surface argument and the keys currently logically down to the keys in the keys argument. The compositor must not send this event if the wl_keyboard already had an active surface immediately before this event."
- **Client emulation prohibition / fence (`wayland.xml:2627–2628`):**
  > "Clients should not use the list of pressed keys to emulate key-press events. The order of keys in the list is unspecified."

### B. Focus Loss: `leave` Event (`wayland.xml:2635–2650`)

- **Signature:** `leave(serial: uint, surface: object<wl_surface>)`
- **Core notification (`wayland.xml:2637–2638`):**
  > "Notification that this seat's keyboard focus is no longer on a certain surface."
- **Strict sequencing invariant (`wayland.xml:2640–2641`):**
  > "The leave notification is sent before the enter notification for the new focus."
- **Logical state reset & validation constraint (`wayland.xml:2643–2646`):**
  > "In the wl_keyboard logical state, this event resets all values to their defaults. The compositor must not send this event if the active surface of the wl_keyboard was not equal to the surface argument immediately before this event."

---

## 5. Key Event Semantics (`key` Event & `key_state` Enum)

- **Enum `key_state` (`wayland.xml:2652–2667`):**
  - `released` (`value="0"`): `"key is not pressed"` (line 2664)
  - `pressed` (`value="1"`): `"key is pressed"` (line 2665)
  - `repeated` (`value="2"`, `since="10"`): `"key was repeated"` (line 2666)
  - **Repetition transition semantics (`wayland.xml:2656–2662`):**
    > "Since version 10, the key can be in a \"repeated\" pseudo-state which means the same as \"pressed\", but is used to signal repetition in the key event. The key may only enter the repeated state after entering the pressed state and before entering the released state. This event may be generated multiple times while the key is down."

- **Event `key` (`wayland.xml:2669–2699`):**
  - **Signature:** `key(serial: uint, time: uint, key: uint, state: uint<key_state>)`
  - **Timing & keycode interpretation (`wayland.xml:2671–2676`):**
    > "A key was pressed or released. The time argument is a timestamp with millisecond granularity, with an undefined base. The key is a platform-specific key code that can be interpreted by feeding it to the keyboard mapping (see the keymap event)."
  - **Modifier synchronization requirement (`wayland.xml:2678–2679`):**
    > "If this event produces a change in modifiers, then the resulting wl_keyboard.modifiers event must be sent after this event."
  - **Focus boundary enforcement on key delivery (`wayland.xml:2681–2688`):**
    > "In the wl_keyboard logical state, this event adds the key to the keys currently logically down (if the state argument is pressed) or removes the key from the keys currently logically down (if the state argument is released). The compositor must not send this event if the wl_keyboard did not have an active surface immediately before this event. The compositor must not send this event if state is pressed (resp. released) and the key was already logically down (resp. was not logically down) immediately before this event."
  - **Version 10 compositor-driven repeat takeover (`wayland.xml:2690–2693`):**
    > "Since version 10, compositors may send key events with the \"repeated\" key state when a wl_keyboard.repeat_info event with a rate argument of 0 has been received. This allows the compositor to take over the responsibility of key repetition."

---

## 6. Associated Lifecycle & Focus-Decoupled Events

### A. Modifier State Decoupling: `modifiers` Event (`wayland.xml:2701–2722`)
- **Signature:** `modifiers(serial: uint, mods_depressed: uint, mods_latched: uint, mods_locked: uint, group: uint)`
- **Decoupling from active keyboard surface focus (`wayland.xml:2706–2712`):**
  > "The compositor may send this event without a surface of the client having keyboard focus, for example to tie modifier information to pointer focus instead. If a modifier event with pressed modifiers is sent without a prior enter event, the client can assume the modifier state is valid until it receives the next wl_keyboard.modifiers event. In order to reset the modifier state again, the compositor can send a wl_keyboard.modifiers event with no pressed modifiers."

### B. Keyboard Object Destruction: `release` Request (`wayland.xml:2726–2728`)
- Added in version 3 (`type="destructor"`). Releases client-side keyboard resource upon seat capability loss.

### C. Client Repeat Configuration: `repeat_info` Event (`wayland.xml:2732–2751`)
- Added in version 4: `repeat_info(rate: int, delay: int)`.
- **Ordering invariant (`wayland.xml:2736–2738`):**
  > "This event is sent as soon as the wl_keyboard object has been created, and is guaranteed to be received by the client before any key press event."
- **Repeat suppression (`wayland.xml:2740–2741`):**
  > "Negative values for either rate or delay are illegal. A rate of zero will disable any repeating (regardless of the value of delay)."

### D. Seat Capability Precondition (`wayland.xml:2075–2085`)
- In `wl_seat` (`version="11"`), `get_keyboard` request (`wayland.xml:2075-2087`):
  > "This request only takes effect if the seat has the keyboard capability, or has had the keyboard capability in the past. It is a protocol violation to issue this request on a seat that has never had the keyboard capability. The missing_capability error will be sent in this case." (lines 2080–2084).

---

## 7. Summary of Focus Boundary Invariants for U6 Evidence Ladder

1. **Surface Encapsulation:** Keyboard events (`key`) are strictly gated by surface focus. A compositor MUST NOT emit `key` events to a client without an active surface (`wayland.xml:2684–2685`).
2. **Atomic Transition Ordering:** When shifting focus across surfaces, `leave` strictly precedes `enter` (`wayland.xml:2640–2641`).
3. **Non-Reentrancy:** An `enter` event cannot be emitted if the keyboard already has an active surface (`wayland.xml:2624–2625`).
4. **State Erasure on Leave:** A `leave` event unconditionally resets active surface to `null`, logically down keys to empty, and modifiers/group to `0` (`wayland.xml:2585–2586, 2643–2644`).
5. **No Event Emulation on Enter:** Clients are explicitly prohibited from synthesizing keypress events from the `enter` keys array (`wayland.xml:2627–2628`).
6. **Keymap Scancode Offset:** Wayland core keycodes must be shifted by `+8` to interface with `libxkbcommon` (`wayland.xml:2597`).

---

## 8. Judgement & Verification

- **Coverage (C1):** Fully locates and cites the primary specification for Wayland core `wl_keyboard` enter/leave/key/keymap semantics, version history (v1 through v11), line numbers, and exact verbatim quotes.
- **Operability & Safety:** Strictly read-only static analysis of official installed XML and upstream Git repository metadata. No Wayland client was connected; no socket communication or protocol manipulation was attempted.

---

## 9. Gaps & Unknowns (`[UNK]`)

- No Wayland protocol client was created or connected to `/run/user/1000/wayland-0` (`[UNK]`).
- Live compositor key routing, active surface assignment, and input method extension (`text-input-v3`) focus interactions were not observed or measured (`[UNK]`).

---

## 10. Tooling Record

None installed or upgraded. All observations derived from static inspection via standard repository and system tools (`pacman`, `git ls-remote`, `curl`, `sha256sum`, and built-in text inspection).
