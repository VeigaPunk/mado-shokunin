# WaylandSeat — Primary Wayland Core `wl_seat` Capability Lifecycle & Delivery Boundary (mado-r15-w1)

**Seat Identity**: `WaylandSeat` (scout, leaf)  
**Wave**: `mado-r15-w1`  
**Target**: `/home/vgpnk/Projects/shokunin/mado-shokunin`  
**Milestone**: U6 input evidence ladder and R14 ancillary provenance correction  
**Assigned Scope**: Locate exact primary Wayland `wl_seat` capability lifecycle and why advertised keyboard/pointer != delivered app input. Pure read-only static analysis; no live event probes, no client event interception, no input injection, no tests or gate execution.

---

## 1. Source Open & Precedence

1. **Installed Protocol XML `[OBS]`**:
   - File path: `/usr/share/wayland/wayland.xml` (package `wayland 1.26.0-1`, Arch Linux `extra`).
   - Package verification: `pacman -Qo /usr/share/wayland/wayland.xml` → `wayland 1.26.0-1`.
   - File SHA-256: `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`.
   - Relevant interface line bounds:
     - `wl_seat` (interface version 11): lines 2004–2136.
     - `wl_pointer` (interface version 11): lines 2138–2571.
     - `wl_keyboard` (interface version 11): lines 2573–2751.

2. **Upstream Canonical Repository `[OBS]`**:
   - Git repository: `https://gitlab.freedesktop.org/wayland/wayland`
   - Release git tag: `1.26.0` (commit `5f430e41167dd359b70fb5e9f584ba2dc058e4cc`).
   - Canonical raw URL: `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml`
   - Byte equality: Identical SHA-256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07` across installed host XML and upstream 1.26.0 tag raw XML.

3. **Precedence and Registry Relationship `[INF-docs]`**:
   - Installed `/usr/share/wayland/wayland.xml` is already admitted in `corpus/SOURCES.md` as row `S043` (`SOURCES.md:55`) for registry events. Expanding `S043`'s anchor to include `wl_seat` (:2004–2136), `wl_pointer` (:2138–2571), and `wl_keyboard` (:2573–2751) avoids duplicating the source row under a new ID like S052 while preserving exact byte-level provenance.

---

## 2. Key Findings: `wl_seat` Capability Lifecycle

1. **Interface Identity and Global Binding `[INF-docs]`**:
   - Interface: `<interface name="wl_seat" version="11">` (line 2004).
   - Description: "A seat is a group of keyboards, pointer and touch devices." Published as a global during compositor startup or when an input device is hot-plugged (lines 2006–2008).
   - Binding: Clients discover the seat via `wl_registry.global` and bind to it via `wl_registry.bind`.
   - Seat Name: `event name="name" since="2"` (lines 2105–2125). Emitted once after binding and before announcing capabilities. Identifies the seat uniquely across clients for the compositor instance.

2. **Capabilities Bitmask & Event Emission `[INF-docs]`**:
   - Bitfield Enum `capability` (lines 2012–2020):
     - `pointer = 1`: The seat has pointer devices.
     - `keyboard = 2`: The seat has one or more keyboards.
     - `touch = 4`: The seat has touch devices.
   - Event `capabilities` (lines 2030–2059):
     - Emitted immediately upon client binding to the seat global.
     - Emitted dynamically whenever the seat gains or loses any capability (e.g. on device plug/unplug or re-routing).
     - Carries the complete bitmask of current capabilities.

3. **Device Object Creation & Protocol Invariants `[INF-docs]`**:
   - Requests:
     - `get_pointer(id: new_id<wl_pointer>)` (lines 2061–2073)
     - `get_keyboard(id: new_id<wl_keyboard>)` (lines 2075–2087)
     - `get_touch(id: new_id<wl_touch>)` (lines 2089–2101)
   - Mandatory Precondition: Requests only take effect if the seat currently has the capability or has had it in the past.
   - Protocol Violation: Invoking `get_pointer`, `get_keyboard`, or `get_touch` on a seat that has *never* had that capability is a fatal protocol error: `wl_seat.error.missing_capability = 0` (lines 2026–2027, 2068–2070, 2082–2084, 2097–2099).

4. **Capability Removal and Object Destruction `[INF-docs]`**:
   - When a capability bit is removed in `wl_seat.capabilities`, the client is obligated to destroy the associated device object using its respective destructor:
     - `wl_pointer.release` (since v3, line 2301)
     - `wl_keyboard.release` (since v3, line 2726)
     - `wl_touch.release` (since v3, line 2830)
   - Once removed, no further events are received on those objects (lines 2044–2045).

5. **Regained Capabilities and the Version 5+ Invariant `[INF-docs]`**:
   - Pre-v5 Behavior (Misinterpretation): In v4 or earlier, some compositors resumed sending events to old objects if capability returned; specification explicitly classifies this as a "misinterpretation of the intended behavior and must not be relied upon by the client" (lines 2047–2051).
   - Version 5+ Invariant: Objects created prior to the most recent added-capability event become permanently dead:
     *"wl_pointer objects of version 5 or later must not send events if created before the most recent event notifying the client of an added pointer capability."* (lines 2051–2053; applies equally to `wl_keyboard` and `wl_touch`, lines 2055–2056).
   - Clients must explicitly allocate a new object via `wl_seat.get_*` upon receiving an added capability event.

6. **Seat Object Destruction `[INF-docs]`**:
   - Request `release` (type="destructor", since="5", lines 2129–2134): Tells the compositor that the client will no longer use the seat object.

---

## 3. Why Advertised Keyboard/Pointer != Delivered App Input

The presence of `pointer = 1` or `keyboard = 2` in `wl_seat.capabilities` is a seat-level hardware/compositor capability indicator, not an assurance or stream of delivered application input. A multi-layer architecture separates capability advertisement from application receipt:

1. **Hardware Aggregation vs. Client Surface Isolation `[INF-docs]`**:
   - `wl_seat` aggregates multiple physical or virtual input devices under one logical seat (`wayland.xml:2006–2008`).
   - Wayland's security and isolation model strictly forbids global input snooping or broadcasting. There is no client-side raw input listener (unlike X11 `XRecord` or root window `XSelectInput`). Clients only receive events routed specifically to surfaces they own.

2. **The Surface Focus Prerequisite (The Mandatory Delivery Gate) `[INF-docs]`**:
   - **Keyboard Gate (`wl_keyboard`)**:
     - By specification, `wl_keyboard` default logical state has `active surface = null`, `keys down = empty`, and `active modifiers = 0` (lines 2585–2586).
     - Keystrokes (`wl_keyboard.key`) are delivered *only* to the client owning the surface with active keyboard focus.
     - Focus is granted exclusively via `wl_keyboard.enter(serial, surface, keys)` and revoked via `wl_keyboard.leave(serial, surface)`.
     - An unfocused, background, minimized, obscured, or non-active-workspace client receives zero key events regardless of seat capability.
   - **Pointer Gate (`wl_pointer`)**:
     - Motion (`wl_pointer.motion`), clicks (`wl_pointer.button`), and scroll (`wl_pointer.axis`) events are dispatched *strictly* while the pointer intersects the surface.
     - Focus is bounded by `wl_pointer.enter` and `wl_pointer.leave`. If the pointer is over another application, the wallpaper, or another monitor, the client receives zero pointer events.

3. **Surface Input Region Filtering `[INF-docs]`**:
   - A client surface's input acceptance area is defined by `wl_surface.set_input_region`.
   - Even when the pointer is visually inside a window's buffer bounds, if the pointer falls outside the declared input region (or if the input region is empty, e.g. for click-through overlays), the compositor routes pointer events through to surfaces below or discards them.

4. **Compositor Interception & Keybindings `[INF]`**:
   - The compositor sits directly in the event path between `libinput`/kernel and Wayland clients.
   - Compositor keybindings (e.g. Hyprland `bind = ...` for window management, workspace switching, application launchers, or media keys) are intercepted and consumed by the compositor before any Wayland protocol events are synthesized.
   - The focused application never receives `wl_keyboard.key` events for bound shortcuts.

5. **Exclusive Grabs and Session Lock Modes `[INF-docs]`**:
   - Session locks (`ext-session-lock-v1`): When the screen is locked, all seat input is redirected to the lock surface; all normal application surfaces lose focus and receive no input.
   - Popups & Layer Surfaces: Surfaces with exclusive grab modes (`xdg_popup.grab` or layer shell exclusive keyboard interactivity) intercept all input, starving regular toplevel surfaces.

6. **Input Method / IME Redirection `[INF-docs]`**:
   - When text input protocols (`zwp_text_input_v1/v3`, `zwp_input_method_v1/v2`) are active, physical keystrokes are intercepted by the input method engine (IME, e.g. fcitx5).
   - The client receives composed strings (`commit_string`) or pre-edit events instead of direct `wl_keyboard.key` events.

7. **Compositor Device Configuration & Policy `[INF]`**:
   - Compositors can disable specific devices or remap their behavior (e.g. Hyprland per-device config `device:name { enabled = false }`).
   - The seat may continue advertising `keyboard` or `pointer` (because other devices or virtual seats exist), but a disabled device generates no delivered input.

8. **Stale Device Objects on Capability Flap `[INF-docs]`**:
   - Under the version 5+ protocol contract, if a seat loses and regains a capability, pre-existing `wl_pointer` or `wl_keyboard` objects are rendered permanently inert (`wayland.xml:2051–2053`).
   - If a client fails to release the stale object and request a new one via `get_pointer`/`get_keyboard`, it will never receive further input despite the seat actively advertising the capability.

9. **Live Host Focus & Delivery State is Unexercised `[UNK]`**:
   - The actual routing of input events to specific host applications, current window focus in Hyprland, IME engine state, and physical device event generation are live operational dimensions that are completely unexercised by static protocol specification analysis.

---

## 4. Located Quotations (≤ 25 Words Each)

All quotations sourced directly from `/usr/share/wayland/wayland.xml` (sha256 `cc860987...`):

1. **`wl_seat` description** (lines 2006–2007):
   > *"A seat is a group of keyboards, pointer and touch devices. This object is published as a global during start up..."* (20 words)

2. **`wl_seat.error.missing_capability`** (lines 2026–2027):
   > *"get_pointer, get_keyboard or get_touch called on seat without the matching capability"* (11 words)

3. **`wl_seat.capabilities` event** (lines 2032–2033):
   > *"This is sent on binding to the seat global or whenever a seat gains or loses the pointer, keyboard or touch capabilities."* (21 words)

4. **`wl_seat.capabilities` removal** (lines 2042–2044):
   > *"When the pointer capability is removed, a client should destroy the wl_pointer objects associated with the seat... using the wl_pointer.release request."* (20 words)

5. **`wl_seat.capabilities` v5+ inert invariant** (lines 2051–2053):
   > *"wl_pointer objects of version 5 or later must not send events if created before the most recent event notifying the client of an added pointer capability."* (24 words)

6. **`wl_seat.get_pointer` protocol violation** (lines 2068–2070):
   > *"It is a protocol violation to issue this request on a seat that has never had the pointer capability."* (18 words)

7. **`wl_keyboard` default logical state** (lines 2585–2586):
   > *"By default, the active surface is null, the keys currently logically down are empty, the active modifiers and the active group are 0."* (22 words)

8. **`wl_keyboard.enter` focus requirement** (lines 2616–2617):
   > *"Notification that this seat's keyboard focus is on a certain surface."* (10 words)

---

## 5. Candidate Registry Anchors

To incorporate these findings into `corpus/SOURCES.md`, either:
- **Option A (In-place Expansion of S043)**: Expand `S043` anchor to include `wl_seat` (:2004–2136), `wl_pointer` (:2138–2571), and `wl_keyboard` (:2573–2751). Retains existing package pin `wayland 1.26.0-1` (`cc860987...`) and avoids URL/file duplicate collisions.
- **Option B (New Upstream Spec Row S052)**: Anchor to upstream repository git tag:
  `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml` (tag `1.26.0`, commit `5f430e41167dd359b70fb5e9f584ba2dc058e4cc`, SHA-256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`).

---

## 6. Tooling and Process Disclosure

- **Tooling Directive Compliance**: No tools were installed or updated by this seat.
- **Static Invocations Executed**:
  - `pacman -Qo /usr/share/wayland/wayland.xml` (package ownership verification)
  - `pacman -Qi wayland` (package version/metadata inspection)
  - `sha256sum /usr/share/wayland/wayland.xml` (hash verification)
  - `git ls-remote https://gitlab.freedesktop.org/wayland/wayland.git refs/tags/1.26.0` (remote tag SHA resolution)
  - `curl -s https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml | sha256sum` (upstream byte equality verification)
- **Prohibited Actions Avoided**: Zero input injection, no event replay/recording, no live compositor probes, no `/dev/input` access, no test/gate execution, no delegation, no credential or agent database access.
