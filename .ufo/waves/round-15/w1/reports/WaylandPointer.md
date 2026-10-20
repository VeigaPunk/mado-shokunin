# WaylandPointer — Primary Wayland Core XML Semantics and Surface Focus Boundaries

- **Seat:** `MadoR15.WaylandPointer` (scout)
- **Milestone:** U6 input evidence ladder and R14 ancillary provenance correction
- **Scope:** Primary Wayland core XML specification for `wl_pointer` (`enter`, `leave`, `motion`, `button`, `frame`) and surface focus boundaries.
- **Operating Mode:** Read-only static inspection of local installed XML and package metadata. No live client event reading/recording/replay/injection, compositor mutation, or socket tapping.

---

## 1. Primary Source Artifact & Provenance

- **Canonical File Path:** `/usr/share/wayland/wayland.xml`
- **Installed Package:** `wayland 1.26.0-1` (Arch Linux x86_64, official package, packager Lukas Fleischer)
- **File SHA-256:** `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07` (3,442 lines, 143,454 bytes)
- **Upstream Repository & Tag:** `https://gitlab.freedesktop.org/wayland/wayland` @ release tag `1.26.0` (2026-07-16)
- **Registry Relationship:** Extends `S043` (`corpus/SOURCES.md:55`, which previously catalogued `wl_registry` lines 117–177) to the `wl_pointer` interface (lines 2138–2571).
- **Interface Extents:** `<interface name="wl_pointer" version="11">` spanning lines 2138 to 2571.

---

## 2. Core Protocol Semantics of Assigned `wl_pointer` Events

In Wayland protocol architecture, `wl_pointer` requests flow client $\to$ compositor, while events flow compositor $\to$ client.

```
+---------------------------------------------------------------------------------------+
|  wl_pointer Event Contract (wayland.xml:2138-2571, Interface Version 11)              |
+---------------+---------+--------+----------------------------------------------------+
| Event         | Version | Lines  | Signature / Parameters                             |
+---------------+---------+--------+----------------------------------------------------+
| enter         | 1       | 2195   | serial: uint, surface: wl_surface,                 |
|               |         |        | surface_x: fixed, surface_y: fixed                 |
| leave         | 1       | 2213   | serial: uint, surface: wl_surface                  |
| motion        | 1       | 2227   | time: uint, surface_x: fixed, surface_y: fixed     |
| button        | 1       | 2246   | serial: uint, time: uint, button: uint,            |
|               |         |        | state: enum button_state                           |
| frame         | 5       | 2307   | (none)                                             |
+---------------+---------+--------+----------------------------------------------------+
```

### 2.1 `enter` Event (lines 2195–2211, Version 1)
- **XML Declaration:**
  ```xml
  <event name="enter">
    <description summary="enter event">
      Notification that this seat's pointer is focused on a certain surface.
      When a seat's focus enters a surface, the pointer image is undefined
      and a client should respond to this event by setting an appropriate
      pointer image with the set_cursor request.
    </description>
    <arg name="serial" type="uint" summary="serial number of the enter event"/>
    <arg name="surface" type="object" interface="wl_surface" summary="surface entered by the pointer"/>
    <arg name="surface_x" type="fixed" summary="surface-local x coordinate"/>
    <arg name="surface_y" type="fixed" summary="surface-local y coordinate"/>
  </event>
  ```
- **Semantic Invariants:**
  1. **Focus Grant:** Signals that pointer focus has transitioned to `surface`.
  2. **Coordinate Origin:** Provides entry coordinates `(surface_x, surface_y)` in surface-local 24.8 signed fixed-point format (`fixed`).
  3. **Cursor Undefined:** The cursor image is explicitly undefined upon entry; client is expected to issue `set_cursor` using the received `serial`.
  4. **Serial Anchor:** The `serial` uint is the authorization token required by `wl_pointer.set_cursor` (lines 2186–2188).

### 2.2 `leave` Event (lines 2213–2225, Version 1)
- **XML Declaration:**
  ```xml
  <event name="leave">
    <description summary="leave event">
      Notification that this seat's pointer is no longer focused on
      a certain surface.

      The leave notification is sent before the enter notification
      for the new focus.
    </description>
    <arg name="serial" type="uint" summary="serial number of the leave event"/>
    <arg name="surface" type="object" interface="wl_surface" summary="surface left by the pointer"/>
  </event>
  ```
- **Semantic Invariants:**
  1. **Focus Revocation:** Explicitly terminates the client surface's pointer focus.
  2. **Zero Coordinates:** Transmits no coordinates; the pointer is no longer located over the surface.
  3. **Ordering Guarantee:** Verbatim: *"The leave notification is sent before the enter notification for the new focus."* Compositor MUST notify the losing surface before notifying the gaining surface.

### 2.3 `motion` Event (lines 2227–2236, Version 1)
- **XML Declaration:**
  ```xml
  <event name="motion">
    <description summary="pointer motion event">
      Notification of pointer location change. The arguments
      surface_x and surface_y are the location relative to the
      focused surface.
    </description>
    <arg name="time" type="uint" summary="timestamp with millisecond granularity"/>
    <arg name="surface_x" type="fixed" summary="surface-local x coordinate"/>
    <arg name="surface_y" type="fixed" summary="surface-local y coordinate"/>
  </event>
  ```
- **Semantic Invariants:**
  1. **Surface-Local Coordinates:** `surface_x` and `surface_y` are relative to the top-left of the focused surface. No global compositor coordinates are exposed.
  2. **Time Base:** Timestamp `time` in milliseconds with undefined epoch base (monotonic relative to compositor clock).
  3. **Focus Gate:** Only dispatched to the surface that currently holds pointer focus.

### 2.4 `button` Event (lines 2246–2270, Version 1)
- **XML Declaration:**
  ```xml
  <enum name="button_state">
    <description summary="physical button state">
      Describes the physical state of a button that produced the button event.
    </description>
    <entry name="released" value="0" summary="the button is not pressed"/>
    <entry name="pressed" value="1" summary="the button is pressed"/>
  </enum>

  <event name="button">
    <description summary="pointer button event">
      Mouse button click and release notifications.

      The location of the click is given by the last motion, warp or enter event.
      The time argument is a timestamp with millisecond granularity, with an undefined base.

      The button is a button code as defined in the Linux kernel's
      linux/input-event-codes.h header file, e.g. BTN_LEFT.

      Any 16-bit button code value is reserved for future additions to the
      kernel's event code list. All other button codes above 0xFFFF are
      currently undefined but may be used in future versions of this protocol.
    </description>
    <arg name="serial" type="uint" summary="serial number of the button event"/>
    <arg name="time" type="uint" summary="timestamp with millisecond granularity"/>
    <arg name="button" type="uint" summary="button that produced the event"/>
    <arg name="state" type="uint" enum="button_state" summary="physical state of the button"/>
  </event>
  ```
- **Semantic Invariants:**
  1. **Decoupled Position:** Verbatim: *"The location of the click is given by the last motion, warp or enter event."* Button events carry NO coordinate parameters. The client must correlate clicks with previously latched coordinates.
  2. **Linux Kernel Evdev Code Space:** Button codes correspond directly to Linux kernel `linux/input-event-codes.h` values (e.g. `BTN_LEFT = 0x110 = 272`). Values within 16-bit space are reserved for kernel codes.
  3. **State Representation:** Binary physical state via enum `button_state` (`released = 0`, `pressed = 1`).
  4. **Transaction Serial:** Contains `serial` used by subsequent implicit grabs or surface interactions.

### 2.5 `frame` Event (lines 2307–2348, Version 5)
- **XML Declaration:**
  ```xml
  <event name="frame" since="5">
    <description summary="end of a pointer event sequence">
      Indicates the end of a set of events that logically belong together.
      A client is expected to accumulate the data in all events within the
      frame before proceeding.

      All wl_pointer events before a wl_pointer.frame event belong
      logically together...

      A wl_pointer.frame event is sent for every logical event group,
      even if the group only contains a single wl_pointer event.
      Specifically, a client may get a sequence: motion, frame, button,
      frame, axis, frame, axis_stop, frame.

      The wl_pointer.enter and wl_pointer.leave events are logical events
      generated by the compositor and not the hardware. These events are
      also grouped by a wl_pointer.frame. When a pointer moves from one
      surface to another, a compositor should group the
      wl_pointer.leave event within the same wl_pointer.frame.
      However, a client must not rely on wl_pointer.leave and
      wl_pointer.enter being in the same wl_pointer.frame.
      Compositor-specific policies may require the wl_pointer.leave and
      wl_pointer.enter event being split across multiple wl_pointer.frame
      groups.
    </description>
  </event>
  ```
- **Semantic Invariants:**
  1. **Atomic Grouping:** Demarcates logical event batching (e.g., motion + axis, diagonal scroll components, or enter/leave). Clients MUST accumulate event state until `frame` before updating application geometry or dispatching UI callbacks.
  2. **Universal Dispatch:** Dispatched after *every* logical event group, including single events.
  3. **Compositor Logical Events:** Verbatim: *"The wl_pointer.enter and wl_pointer.leave events are logical events generated by the compositor and not the hardware."*
  4. **Grouping Boundary Discretion:** Compositors *should* group `leave` in the frame of transition, but clients *must not* rely on `leave` and `enter` sharing the same frame across surfaces.

---

## 3. Surface Focus Boundaries and Containment Architecture

The Wayland protocol enforces strict surface focus encapsulation through compositor-owned state and double-buffered client requests:

```
+-----------------------------------------------------------------------------------+
|  Compositor Pointer Focus Boundary Lifecycle                                       |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  1. Surface Input Region Definition (wl_surface.set_input_region, xml:1697-1720)   |
|     - Pending input region modified by client in surface-local coordinates.       |
|     - Committed to active state via wl_surface.commit (double-buffered).          |
|     - Default input region is infinite (entire surface).                          |
|     - Hits outside region fall through to next surface in server surface stack.   |
|                                                                                   |
|  2. Focus Transition (Compositor Evaluation)                                      |
|     - Pointer moves across boundary: Compositor revokes focus from Surface A.     |
|     - Step A: wl_pointer.leave(serial, surface_A) sent to Surface A's client.     |
|     - Step B: wl_pointer.frame() sent to Surface A's client.                      |
|     - Step C: wl_pointer.enter(serial, surface_B, x, y) sent to Surface B's client|
|     - Step D: wl_pointer.frame() sent to Surface B's client.                      |
|     - Invariant: leave(surface_A) strictly precedes enter(surface_B).             |
|                                                                                   |
|  3. Cursor Role Security Fencing (wl_pointer.set_cursor, xml:2149-2193)           |
|     - set_cursor requires serial matching latest wl_pointer.enter event.           |
|     - Request ignored if requesting client does not hold pointer focus.           |
|     - Input region is ignored for surfaces given cursor role.                     |
|                                                                                   |
|  4. Coordinate Encapsulation & Leak Prevention                                    |
|     - Only surface-local coordinates exposed in enter/motion/warp.                |
|     - Button events carry NO coordinates.                                         |
|     - Non-focused clients receive zero motion, button, or axis events.            |
+-----------------------------------------------------------------------------------+
```

### 3.1 Input Region and Server Surface Stack (`wl_surface`, lines 1697–1720)
- `wl_surface.set_input_region` configures the geometric region of the surface that receives pointer and touch input.
- Verbatim: *"Input events happening outside of this region will try the next surface in the server surface stack."*
- State lifecycle: Double-buffered. Requests modify pending state; effective upon `wl_surface.commit`.
- Default: Setting `region = NULL` or leaving unset sets input region to infinite (entire surface extent accepts input).

### 3.2 Seat Capability and Pointer Acquisition (`wl_seat`, lines 2004–2070)
- `wl_seat.capability.pointer = 1` advertises pointer hardware presence.
- `wl_seat.get_pointer` (lines 2061–2070): Creates the `wl_pointer` object. If called on a seat without pointer capability, compositor raises protocol error `wl_seat.error.missing_capability (0)`.
- Removal: When capability is dropped, client must destroy object via destructor request `wl_pointer.release` (since version 3, lines 2297–2305).

### 3.3 Security Fencing via Serial Tokens (`wl_pointer.set_cursor`, lines 2149–2193)
- Pointer cursor surface assignment requires proof of focus:
  - Verbatim: *"The cursor actually changes only if the pointer focus for this device is one of the requesting client's surfaces or the surface parameter is the current pointer surface."*
  - Verbatim: *"The serial parameter must match the latest wl_pointer.enter serial number sent to the client. Otherwise the request will be ignored."*
- Prevents unfocused clients from altering cursor appearance, intercepting clicks, or spoofing UI outside their assigned surface.

### 3.4 Non-Hardware Warp Semantics (`wl_pointer.warp`, lines 2557–2571, Version 11)
- Added in version 11 for programmatic repositioning within a surface (e.g. surface movement under cursor or pointer confinement exit).
- Verbatim: *"This event must not occur in the same wl_pointer.frame as a wl_pointer.enter or wl_pointer.motion event."*

---

## 4. Boundary Fences & Unexercised Scope ("No Client Events")

In accordance with round 15 charter, U6 milestone requirements, and leaf safety boundaries:
1. **No Live Probes:** No Wayland compositor sockets (`$WAYLAND_DISPLAY`) were opened or connected to.
2. **No Client Events:** No client event loops (`wl_display_dispatch`, `libwayland-client`) were executed, tapped, or traced.
3. **No Input Injection or Kernel Probing:** No `uinput`, evdev, `/dev/input/*`, or hardware diagnostic ioctls were exercised (`[UNK]`).
4. **Scope Separation:** This investigation establishes the formal upstream XML contract and surface focus boundaries (Layer 3/4 of the U6 input ladder), separate from kernel evdev (Layer 1), libinput device dispatch (Layer 2), and client toolkit event consumption (Layer 5/6).

---

## 5. Tooling Record

- No tools installed or upgraded. Existing read-only filesystem inspection tools (`read`, `grep`, `bash` coreutils) satisfied all evidence collection.
