# HyprInputDocs — Pinned and Current Hyprland Documentation: `hyprctl devices`, `getoption`, and the Input Plane (mado-r15-w1)

Scope: Authoritative documentation-era analysis of `hyprctl devices`, `getoption` input settings, and per-device configuration across current official documentation, archived v0.54.0 documentation, installed man pages, and pinned upstream source code (Hyprland v0.56.2 @ commit `efb50993780079460b0cbed1363e2166a2de1d9f`).
Authority & Status: Leaf scout seat (`MadoR15.HyprInputDocs`). Scoped evidence for Milestone U6 (input evidence ladder and R14 ancillary provenance correction).
Architectural Focus: Rigorous separation of **inventory / configuration** from **application delivery**.
Tooling Record: 0 tools installed or upgraded in this lane.

---

## 1. Primary Documentation Sources and Docs-Era Baselines

The documentation surface for Hyprland input configuration and observation spans two primary syntax eras: the **v0.54 hyprlang era** (colon-separated keys, `device { ... }` blocks) and the **v0.55+ / v0.56+ Lua era** (dot-separated keys, `hl.device({ ... })` function calls).

| Source Descriptor / Canonical URL | Revision / Date | Evidence Class | Documented Scope & Role |
| :--- | :--- | :--- | :--- |
| **Current Official Wiki: Using hyprctl**<br>`https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/` | Latest git<br>Modified `2026-08-26` | `[INF-docs]` | Official CLI documentation for `devices` (`#info`), `getoption` (`#info`), `switchxkblayout`, and JSON flag `-j`. Documents dot notation `section.option` for getoption. |
| **Current Official Wiki: Devices**<br>`https://wiki.hypr.land/Configuring/Advanced-and-Cool/Devices/` | Latest git<br>Modified `2026-08-26` | `[INF-docs]` | Official per-device configuration guide. Documents Lua `hl.device()`, names obtained via `hyprctl devices`, permitted/excluded input options, and device-specific flags (`enabled`, `keybinds`, `tags`, `output`). |
| **Current Official Wiki: Variables (Input)**<br>`https://wiki.hypr.land/Configuring/Basics/Variables/` | Latest git<br>Modified `2026-08-26` | `[INF-docs]` | Official global variable dictionary. Documents complete `input` table (`#input`) and subcategories (`input.touchpad.`, `input.touchdevice.`, `input.virtualkeyboard.`, `input.tablet.`, `input.tablettool.`, `input-capture.`). |
| **Archived Wiki v0.54.0: Using hyprctl**<br>`https://wiki.hypr.land/0.54.0/Configuring/Using-hyprctl/` | v0.54.0 archive<br>Modified `2026-02-21` | `[INF-docs]` | Archived pre-0.55 hyprlang baseline. Documents colon syntax `section:option` (e.g. `input:touchpad:disable_while_typing`) and `devices`. |
| **Archived Wiki v0.54.0: Keywords**<br>`https://wiki.hypr.land/0.54.0/Configuring/Keywords/` | v0.54.0 archive<br>Modified `2025-11-18` | `[INF-docs]` | Archived hyprlang per-device syntax `device { name = ... }` (`#per-device-input-configs`) and CLI mutation `hyprctl keyword device[dev]:opt val`. |
| **Archived Wiki v0.54.0: Variables**<br>`https://wiki.hypr.land/0.54.0/Configuring/Variables/` | v0.54.0 archive<br>Modified `2026-02-21` | `[INF-docs]` | Archived variable dictionary showing pre-0.55 options (`tap-to-click` hyphen notation, absence of `follow_mouse_shrink`, absence of `tablettool`). |
| **Installed Man Page: hyprctl(1)**<br>`/usr/share/man/man1/hyprctl.1.gz` | Package `hyprland 0.56.2-2`<br>Pandoc 3.1.3 format | `[OBS]` | Static host package man page. Documents `devices` ("Lists all connected input devices"), control commands (`dispatch`, `keyword`, `eval`, `reload`), flags (`-j`, `--batch`). Explicitly notes `keyword` fails under Lua provider. |
| **Authoritative Tagged Upstream Source**<br>`https://github.com/hyprwm/Hyprland/blob/v0.56.2/src/debug/HyprCtl.cpp` | Tag `v0.56.2`<br>Commit `efb50993` (2026-08-05) | `[OBS]` | Upstream implementation of `devicesRequest` (L748-936) and `dispatchGetOption` (L1647-1715). |
| **Authoritative Config Manager Implementation**<br>`src/config/legacy/ConfigManager.cpp`<br>`src/config/lua/ConfigManager.cpp` | Tag `v0.56.2`<br>Commit `efb50993` (2026-08-05) | `[OBS]` | Upstream config resolution: legacy hyprlang lookup vs Lua `luaConfigValueName` (L1136-1140), proving dual-delimiter compatibility in v0.56.2. |

---

## 2. `hyprctl devices` Specification and Upstream Mechanics

### 2.1 Purpose and Output Scope
`hyprctl devices` is an **inventory command** that queries the compositor's internal input device manager (`g_pInputManager`). It enumerates active hardware and virtual input devices recognized by the backend and libinput.

- **Man page definition (`hyprctl.1`)**: `"Lists all connected input devices."`
- **Wiki definition (`Using-hyprctl#info`)**: `"devices - lists all connected keyboards and mice"`.
- **Wiki use in layout management (`Using-hyprctl#switchxkblayout`)**: `"You can find the DEVICE using hyprctl devices command. DEVICE can also be current or all, self-explanatory. Current is the main keyboard from devices."`

### 2.2 Device Categories and Data Fields (JSON vs Text)
In Hyprland v0.56.2 (`HyprCtl.cpp:748-936`), `devicesRequest` inspects six distinct internal containers in `g_pInputManager`:

1. **Mice / Pointers (`m_pointers`)**:
   - `address`: Pointer memory address (`0x{:x}`).
   - `name`: Compositor-assigned device name (`m_hlName`).
   - `defaultSpeed`: Initial acceleration speed queried from libinput via `libinput_device_config_accel_get_default_speed()`.
   - `scrollFactor`: Device-level scroll speed multiplier (`m_scrollFactor.value_or(-1)`).
2. **Keyboards (`m_keyboards`)**:
   - `address`: Keyboard memory address.
   - `name`: Device name (`m_hlName`).
   - `rules`: Active XKB rule names (`rules`, `model`, `layout`, `variant`, `options`).
   - `active_layout_index`: Zero-based layout index (`k->getActiveLayoutIndex()`, or `"none"`).
   - `active_keymap`: Human-readable active keymap string (e.g. `"Portuguese (Brazil)"`, `"English (US)"`).
   - `capsLock` & `numLock`: Booleans queried via `xkb_keymap_mod_get_index` and `m_modifiersState.locked`.
   - `main`: Boolean indicating whether this keyboard is currently the compositor's primary keyboard (`k->m_active`).
3. **Tablets (`m_tablets`, `m_tabletPads`, `m_tabletTools`)**:
   - `address`, `name`, physical dimensions in mm (`physicalSize.x`, `physicalSize.y`).
   - Tablet pads report parent linkage (`belongsTo: { address, name }`).
4. **Touch Devices (`m_touches`)**:
   - `address`, `name`.
5. **Switches (`m_switches`)**:
   - Hardware switches (e.g. lid switch, tablet-mode switch), reporting address and device name.

### 2.3 Limits of `hyprctl devices`
- `[OBS]` `devices` reflects **hardware/kernel recognition and static xkb state only**.
- `[INF]` It reports that a device exists, is bound to libinput, and has a specific keymap loaded.
- `[INF]` It does **not** indicate whether any application is receiving events, whether the cursor is hovered over a window, or whether keystrokes are being delivered or swallowed.

---

## 3. `hyprctl getoption` Specification and Upstream Mechanics

### 3.1 Purpose and Syntax Evolution
`hyprctl getoption` queries the compositor's config manager for the effective value and user-assignment status of a named option.

- **Archived v0.54 Wiki (`0.54.0/Configuring/Using-hyprctl/#info`)**:
  - Option selector syntax: `section:option` (hyprlang colon delimiter).
  - Explicit documented examples:
    - `hyprctl getoption general:border_size`
    - `hyprctl getoption input:touchpad:disable_while_typing`
- **Current Wiki (`Configuring/Advanced-and-Cool/Using-hyprctl/#info`)**:
  - Option selector syntax: `section.option` (Lua dot delimiter).
  - Explicit documented examples:
    - `hyprctl getoption general.border_size`
    - `hyprctl getoption input.touchpad.disable_while_typing`

### 3.2 Upstream Dual-Delimiter Resolution (v0.56.2 Implementation)
Analysis of pinned upstream source v0.56.2 reveals how the compositor handles the transition:

1. In `src/debug/HyprCtl.cpp:1659`, `dispatchGetOption` receives the raw string `curitem` and calls `Config::mgr()->getConfigValue(curitem)`.
2. In the Lua config provider (`src/config/lua/ConfigManager.cpp:1030-1049` and `1136-1140`):
   ```cpp
   std::string CConfigManager::luaConfigValueName(const std::string& s) {
       std::string cpy = s;
       std::ranges::replace(cpy, ':', '.');
       std::ranges::replace(cpy, '-', '_');
       return cpy;
   }
   ```
   If `curitem` contains colons (legacy syntax `input:touchpad:disable_while_typing`), `luaConfigValueName` transparently maps colons to dots (`input.touchpad.disable_while_typing`) and hyphens to underscores.
3. In the legacy hyprlang config provider (`src/config/legacy/ConfigManager.cpp:978`):
   `m_config->getConfigValuePtr(val.c_str())` is queried directly using the native hyprlang colon notation.

### 3.3 Output Structure and the `set` Flag
`getoption` returns both the effective value and the `set` flag (`HyprCtl.cpp:1666-1715`):

- **Normal text output format**:
  ```text
  <type>: <value>
  set: <true|false>
  ```
- **JSON format (`-j getoption <opt>`)**:
  ```json
  {"option": "<name>", "<type>": <value>, "set": <true|false> }
  ```
- **Falsifiable Semantics of `set`**:
  `VAR.setByUser` indicates whether the option was explicitly defined by a configuration file or runtime command (`set: true`) versus running at the compositor's built-in default (`set: false`). This allows distinguishing explicit user overrides from engine fallbacks.

---

## 4. Comprehensive Inventory of `input` Configuration Options

From `Configuring/Basics/Variables/#input` (Latest git, 2026-08-26) compared with `0.54.0/Configuring/Variables/#input` (2026-02-21):

### 4.1 Global `input` Category
| Option Name | Type | Current Default | 0.54 Baseline | Documented Semantics / Functional Role |
| :--- | :--- | :--- | :--- | :--- |
| `kb_model` | str | `[[Empty]]` | `[[Empty]]` | XKB keymap model parameter. |
| `kb_layout` | str | `"us"` | `us` | XKB keymap layout parameter (comma-separated for multi-layout). |
| `kb_variant` | str | `[[Empty]]` | `[[Empty]]` | XKB keymap variant parameter. |
| `kb_options` | str | `[[Empty]]` | `[[Empty]]` | XKB keymap options (e.g. `compose:caps`, `grp:alt_shift_toggle`). |
| `kb_rules` | str | `[[Empty]]` | `[[Empty]]` | XKB keymap rules file parameter. |
| `kb_file` | str | `[[Empty]]` | `[[Empty]]` | Path to custom `.xkb` keymap file. |
| `numlock_by_default` | bool | `false` | `false` | Engages NumLock on compositor startup. |
| `resolve_binds_by_sym` | bool | `false` | `false` | Determines whether keybinds resolve by raw keycode or active layout symbol. |
| `repeat_rate` | int | `25` | `25` | Typematic repeat rate in repeats per second. |
| `repeat_delay` | int | `600` | `600` | Typematic initial delay in milliseconds. |
| `sensitivity` | float | `0.0` | `0.0` | Pointer sensitivity clamped to `[-1.0, 1.0]`. |
| `accel_profile` | str | `[[Empty]]` | `[[Empty]]` | Pointer acceleration: `"adaptive"`, `"flat"`, or `"custom"`. |
| `force_no_accel` | bool | `false` | `false` | Bypasses pointer settings for raw input signal. |
| `rotation` | int | `0` | `0` | Device rotation in degrees clockwise (`0-359`). |
| `left_handed` | bool | `false` | `false` | Swaps left and right pointer buttons. |
| `scroll_points` | str | `[[Empty]]` | `[[Empty]]` | Custom scroll curve definition for `accel_profile = "custom"`. |
| `scroll_method` | str | `[[Empty]]` | `[[Empty]]` | `"2fg"`, `"edge"`, `"on_button_down"`, `"no_scroll"`. |
| `scroll_button` | int | `0` | `0` | Button ID used for on-button scroll (0 = default). |
| `scroll_button_lock` | bool | `false` | `false` | Toggles sticky scroll lock rather than requiring hold. |
| `scroll_factor` | float | `1.0` | `1.0` | Scroll speed multiplier for external mice. |
| `natural_scroll` | bool | `false` | `false` | Inverts scrolling direction (natural/touchpad style). |
| `follow_mouse` | int | `1` | `1` | Cursor window-focus policy: `0` (click to focus), `1` (focus follows mouse), `2` (focus follows mouse loose), `3` (separate cursor and keyboard focus). |
| `follow_mouse_shrink` | int | `0` | *[Absent]* | *Added post-0.54*: Shrinks inactive window hitboxes by N pixels (dead zone in gaps). |
| `follow_mouse_threshold` | float | `0.0` | `0.0` | Minimum cursor travel in pixels before focus switches (`follow_mouse = 1`). |
| `focus_on_close` | int | `0` | `0` | Post-window-close focus: `0` (next candidate), `1` (window under cursor), `2` (*added post-0.54*: MRU active window). |
| `mouse_refocus` | bool | `true` | `true` | If disabled, mouse focus won't change unless cursor crosses a window boundary. |
| `float_switch_override_focus` | int | `1` | `1` | Focus behavior on tiling/floating transitions (`1` or `2`). |
| `special_fallthrough` | bool | `false` | `false` | Allows focusing regular workspace windows through floating special-workspace windows. |
| `off_window_axis_events` | int | `1` | `1` | Behavior for scroll events over window borders/gaps (`0` to `3`). |
| `emulate_discrete_scroll` | int | `1` | `1` | Emulates discrete notches from high-resolution scroll events (`0`, `1`, `2`). |

### 4.2 Subcategories of `input`
1. **`input.touchpad.` (`#touchpad`)**:
   - `disable_while_typing` (bool, `true`): Disables touchpad clicks/motion while typing.
   - `natural_scroll` (bool, `false`): Inverts touchpad scroll direction.
   - `scroll_factor` (float, `1.0`): Multiplier for touchpad scroll motion.
   - `middle_button_emulation` (bool, `false`): Simultaneous LMB+RMB sends MMB.
   - `tap_button_map` (str, `[[Empty]]`): `"lrm"` (default) or `"lmr"`.
   - `clickfinger_behavior` (bool, `false`): 1/2/3 fingers map to LMB/RMB/MMB clicks.
   - `tap_to_click` (bool, `true`): Tapping sends click events (named `tap-to-click` in v0.54).
   - `drag_lock` (int, `0`): `0` disabled, `1` timeout, `2` sticky.
   - `tap_and_drag` (bool, `true`): Tap-and-drag gesture (named `tap-and-drag` in v0.54).
   - `flip_x`, `flip_y` (bool, `false`): Inverts horizontal/vertical touchpad motion.
   - `drag_3fg` (int, `0`): Three-finger dragging (`0` disabled, `1` 3 fingers, `2` 4 fingers).
2. **`input.touchdevice.` (`#touchdevice`)**:
   - `transform` (int, `0`): Touch orientation rotation (`0-7`). In v0.54 default was `-1` (unset).
   - `output` (str, `[[Auto]]`): Bound monitor name or auto-detect.
   - `enabled` (bool, `true`): Enables or disables touch input.
3. **`input.virtualkeyboard.` (`#virtualkeyboard`)**:
   - `share_states` (int, `2`): Modifier unification (`0` no, `1` yes, `2` yes unless IME client).
   - `release_pressed_on_close` (bool, `false`): Releases held keys when virtual keyboard closes.
4. **`input.tablet.` (`#tablet`)**:
   - `transform` (int, `0`), `output` (str, `[[Empty]]`), `region_position` (vec2, `{0, 0}`), `absolute_region_position` (bool, `false`), `region_size` (vec2, `{0, 0}`), `relative_input` (bool, `false`), `left_handed` (bool, `false`), `active_area_size` (vec2, `{0, 0}`), `active_area_position` (vec2, `{0, 0}`).
5. **`input.tablettool.` (`#tablettool`)** *[Added post-0.54]*:
   - `eraser_button_mode` (int, `0`): Hardware behavior vs button event override (`1`).
   - `eraser_button_override` (int, `0`): Button ID sent when override is enabled.
   - `pressure_range_min` (float, `-1.0`), `pressure_range_max` (float, `-1.0`): Custom pressure mapping.
6. **`input-capture.` (`#input-capture`)** *[Added post-0.54]*:
   - `capture_modifiers` (bool, `false`), `enforce_barriers` (bool, `true`): Controls `zwp_input_capture_v1` protocol behavior.

---

## 5. Per-Device Configuration Plane (`hl.device` vs `device {}`)

Per-device configuration allows an operator to override global `input` options for specific hardware identifiers discovered via `hyprctl devices`.

### 5.1 Syntax Evolution Across Docs Eras
- **v0.54 Hyprlang Baseline (`0.54.0/Configuring/Keywords/#per-device-input-configs`)**:
  ```ini
  device {
      name = royuan-akko-multi-modes-keyboard-b
      repeat_rate = 50
      repeat_delay = 500
  }
  ```
  Runtime dynamic modification via hyprctl:
  ```bash
  hyprctl -r -- keyword device[my-device]:sensitivity -1
  ```
- **Current Lua Documentation (`Configuring/Advanced-and-Cool/Devices/`)**:
  ```lua
  hl.device({
      name = "my-epic-keyboard",
      sensitivity = -0.5
  })
  ```
  *Note on Man Page (`hyprctl.1`)*: Explicitly cautions that `hyprctl keyword` does not work under Lua; operators must use `hyprctl eval` instead:
  ```bash
  hyprctl eval 'hl.config({ ... })'
  ```

### 5.2 Inheritance and Exclusions
According to official documentation (`Devices/` L485-488):
1. **Inheritance**: Any option explicitly specified in a per-device block overrides the global `input` or `input.<subcategory>` setting for that device. Unspecified options fall back to the global configuration.
2. **Strict Exclusions**: The following options **CANNOT** be set per-device:
   - `force_no_accel`
   - Window-management options: `follow_mouse`, `follow_mouse_shrink`, `follow_mouse_threshold`, `float_switch_override_focus`, `mouse_refocus`, `special_fallthrough`.
3. **Exclusive Per-Device Properties**:
   - `enabled` (bool, default `true`): Connects or disconnects the device from the cursor / event dispatch. Supported on mice, touchpads, touch devices, and keyboards.
   - `keybinds` (bool, default `true`): Enables or disables keybind processing for devices sending key events.
   - `tags` (str): Comma-separated tags providing grouping and alt-names for per-device binds.
   - `output` (str): Binds a tablet to a specific display output.

---

## 6. The Critical Architectural Separation: Inventory/Config vs Delivery

The central requirement of Milestone U6 is establishing why compositor device enumeration (`hyprctl devices`) and configuration query (`hyprctl getoption input:*`) **do not equal application input delivery**.

```
+-----------------------------------------------------------------------------------+
| LAYER 1: Hardware & Kernel Inventory                                             |
| - evdev nodes (/dev/input/event*) -> libinput -> Aquamarine / Hyprland backend     |
| - Probed by: hyprctl devices (lists mice, keyboards, active keymap, caps/num lock)|
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| LAYER 2: Compositor Configuration Plane                                           |
| - Evaluates hyprland.conf / hyprland.lua -> ConfigManager                         |
| - Probed by: hyprctl getoption input:* (effective settings, set: true/false)      |
| - Overrides: hl.device() / device {} blocks per hardware name                     |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| LAYER 3: Compositor Global Interception & Capability Plane                        |
| - Wayland wl_seat global advertised (WL_SEAT_CAPABILITY_KEYBOARD | POINTER | TOUCH)|
| - Compositor intercepts key chords (192 global binds registered on this host)     |
| - Intercepted binds trigger internal dispatchers -> SWALLOWED (Never delivered)   |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| LAYER 4: Surface Focus & Delivery Gate (The Application Boundary)                 |
| - Event dispatched ONLY if client surface has active focus                        |
| - Focus governed by: follow_mouse, focus_on_close, mouse_refocus, aspect ratio    |
| - Blocked by: Session lock (hyprlock), Submaps, zwp_input_capture, device.enabled |
| - Filtered by: virtualkeyboard.share_states, IME / text-input-v1/v3 protocol      |
| - Delivered via: wl_keyboard.key, wl_pointer.motion/button, wl_touch.down        |
+-----------------------------------------------------------------------------------+
```

### 6.1 The Eight Delivery Gates (Why Inventory != Delivered Input)

1. **Surface Focus Prerequisite**:
   Under the Wayland protocol architecture (S008 DeVault §High-level design, S009 Wayland Architecture §Wayland Architecture), client applications receive input events strictly through focused Wayland surfaces (`wl_surface`). A keyboard event is only delivered via `wl_keyboard.key` if the client's surface has received `wl_keyboard.enter`. Having 8 active keyboards in `hyprctl devices` does not send a single keypress to an application if no surface holds focus.
2. **Compositor Bind Interception (Event Swallowing)**:
   Hyprland processes input chords through its internal keybind dispatcher (`g_pKeybindManager`). On this host, 192 binds are registered (`bindings.conf`, MADO-1 §4). When a key combination matches a registered bind (e.g. `SUPER+Q`, `SUPER+SPACE`), the compositor executes the associated dispatcher action and **swallows the event**. It is never encoded into the client's `wl_keyboard` wire buffer.
3. **Cursor Focus Gating Policies**:
   Global input settings configure focus transition logic, not event delivery:
   - `follow_mouse = 0` requires explicit clicks to transfer focus.
   - `follow_mouse_threshold` requires the mouse to travel N pixels before focus transfers.
   - `follow_mouse_shrink` defines dead zones in window gaps.
   - `mouse_refocus = false` suppresses focus changes within window boundaries.
4. **Session Lock Masking**:
   When the session is locked via `ext-session-lock-v1` (e.g. `hyprlock`), all regular application surfaces lose keyboard and pointer focus. The compositor redirects all hardware input exclusively to the lock-screen client.
5. **Submap Traps**:
   If the compositor enters an active keybind submap (`hyprctl submap`), default bindings and pass-through key delivery can be completely disabled or masked.
6. **Per-Device Disabling**:
   An operator can configure `hl.device({ name = "...", enabled = false })` or `keybinds = false`. The hardware remains visible in `hyprctl devices`, but the compositor completely drops pointer motion or key events from that device before delivery.
7. **Virtual Keyboard & IME Mediation**:
   `input.virtualkeyboard.share_states = 2` dictates that key down and modifier states are shared across keyboards *unless* an IME client is active. Input Method Engines (via `zwp_text_input_v3`) intercept raw keystrokes and deliver pre-edit or committed strings, completely altering the delivery pipeline.
8. **Input Capture Protocols**:
   Under `zwp_input_capture_v1` (`input-capture.capture_modifiers = true`), remote desktop or capture utilities can intercept input before it reaches local window surfaces.

---

## 7. Located Quotations (≤ 25 Words Each)

1. **Current Using hyprctl (`Advanced-and-Cool/Using-hyprctl/#info`, L544)**:
   > `"devices - lists all connected keyboards and mice"`
2. **Current Using hyprctl (`Advanced-and-Cool/Using-hyprctl/#info`, L550)**:
   > `"getoption [option] - gets the config option status (values)"`
3. **Current Using hyprctl (`Advanced-and-Cool/Using-hyprctl/#info`, L559-560)**:
   > `"For the getoption command, the option name should be written as section.option, e.g.: hyprctl getoption general.border_size"`
4. **Current Devices Guide (`Advanced-and-Cool/Devices/`, L481)**:
   > `"Since Hyprland 0.55, hyprlang is deprecated in favor of lua."`
5. **Current Devices Guide (`Advanced-and-Cool/Devices/`, L485)**:
   > `"The name can be easily obtained by checking the output of hyprctl devices."`
6. **Current Devices Guide (`Advanced-and-Cool/Devices/`, L489)**:
   > `"enabled -> (only for mice / touchpads / touchdevices / keyboards) enables / disables the device (connects / disconnects from the on-screen cursor)"`
7. **Archived v0.54 Using hyprctl (`0.54.0/Configuring/Using-hyprctl/#info`, L1866-1867)**:
   > `"For the getoption command, the option name should be written as section:option, e.g.: hyprctl getoption general:border_size"`
8. **Archived v0.54 Keywords (`0.54.0/Configuring/Keywords/#per-device-input-configs`, L1461-1463)**:
   > `"Per-device config options will overwrite your options set in the input section. It’s worth noting that ONLY values explicitly changed will be overwritten."`
9. **Archived v0.54 Keywords (`0.54.0/Configuring/Keywords/#per-device-input-configs`, L1546)**:
   > `"hyprctl -r -- keyword device[my-device]:sensitivity -1"`
10. **Installed Man Page (`hyprctl.1`)**:
    > `"Set a config keyword dynamically. This will not work if your config provider is lua (refer to eval)."`
11. **Upstream Source (`src/config/lua/ConfigManager.cpp:1136-1140`)**:
    > `"std::string CConfigManager::luaConfigValueName(const std::string& s) { std::string cpy = s; std::ranges::replace(cpy, ':', '.'); std::ranges::replace(cpy, '-', '_'); return cpy; }"`
12. **Upstream Source (`src/debug/HyprCtl.cpp:1659-1662`)**:
    > `"const auto VAR = Config::mgr()->getConfigValue(curitem); if (!VAR.dataptr) return \"no such option\";"`

---

## 8. Unknowns, Boundary Limits, and Unexercised Verification

1. `[UNK]` **Real-time Surface Focus & Delivery**: This scout did not monitor live event streams (`WAYLAND_DEBUG=1`, `wev`, or `libinput debug-events`) or inspect private socket buffers. Whether a specific open client window is currently receiving keystrokes is unobserved.
2. `[UNK]` **Hardware-specific libinput Driver Quirks**: Driver-level button mapping or vendor-specific quirk tables (e.g. `/usr/share/libinput/*.quirks`) for connected hardware were not probed.
3. `[UNK]` **Live Event Replay or Injection**: In strict compliance with leaf boundaries and milestone contracts, zero live compositor actions, keystroke injections, or `hyprctl keyword` mutations were executed. All findings are derived from static documentation and authoritative source code.
4. **Boundary Distinction**:
   - `hyprctl devices` = **Hardware / libinput Inventory**
   - `hyprctl getoption input:*` = **Compositor Engine Configuration**
   - `wl_seat` / `wl_keyboard` = **Application Delivery Pipeline** (Subject to focus, bind interception, session lock, and IME gating).
