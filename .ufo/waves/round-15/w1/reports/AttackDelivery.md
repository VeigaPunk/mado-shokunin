# AttackDelivery — round 15 W1 critic

**Target inference:** "The `wl_seat` keyboard/pointer capability, or a populated `hyprctl devices`, proves that input reaches the focused app."
**Verdict:** **falsified.** Both surfaces are compositor device-set facts. Each one is computed before at least eight independent drop or redirect points, and neither surface names a focus target. U6 has to keep them as *device-presence* rungs. Delivery to a focused client stays `[UNK]`.

Axes: coverage (C1, U6). The impacted facets are rung semantics for the ladder rows, the separation of delivery from presence, and how the historical host capture is worded.

## Sources (static bytes only, no protocol client and no live probe)

| id | source | pin |
|---|---|---|
| W | `/usr/share/wayland/wayland.xml` (pkg `wayland 1.26.0-1`) | sha256 `cc860987e54f8d85…` |
| H-hdr | `/usr/include/hyprland/src/devices/IKeyboard.hpp` (pkg `hyprland 0.56.2-2`) | sha256 `82e0bc9e1f31f634…` |
| H | Hyprland source at `efb50993780079460b0cbed1363e2166a2de1d9f`. This is the same commit as S050 and as the host's `hyprctl version` (`hyprctl-verification-layer.md:160`). URLs have the form `https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/src/<path>`. | `debug/HyprCtl.cpp` `798b7c6c4c168455…`; `managers/input/InputManager.cpp` `feedf32e2e3d23ae…`; `managers/SeatManager.cpp` `bd7485535c7e9f71…`; `protocols/core/Seat.cpp` `cc23bb8b4f1e44cd…`; `devices/IKeyboard.cpp` `8a800efe9baa7f37…`; `managers/KeybindManager.cpp` `8d8f35fc84c4a2f8…` |

The H-hdr field set (`m_active`/`m_enabled`/`m_allowed`, `IKeyboard.hpp:84-89`) matches what the H sources use. That match supports the claim that the pinned source and the installed build agree. `[INF]` I did not compare the binary itself to the source.

## Counterexamples

### 1. A keyboard capability can be set while every key is dropped

- **The capability is the OR of all device objects, with no enabled or permission filter.** `InputManager.cpp:1869-1881` sets `caps |= h->getCapabilities()` over all non-expired HIDs. `IKeyboard.cpp:25-27` returns `HID_INPUT_CAPABILITY_KEYBOARD` unconditionally. `Seat.cpp:527-536` maps that to `WL_SEAT_CAPABILITY_KEYBOARD`.
- **The first statement of the key path drops disabled or denied keyboards.** `InputManager.cpp:1620-1621` reads `if (!pKeyboard->m_enabled || !pKeyboard->m_allowed) return;`.
- **`m_enabled` comes from the per-device `enabled` config** (`InputManager.cpp:1233,1240`).
- **`m_allowed` comes from the dynamic `PERMISSION_TYPE_KEYBOARD` rule.** It is false while the permission prompt is pending and false on deny (`InputManager.cpp:1244-1268`).
- **Counterexample:** the only physical keyboard is set `enabled=false` or is permission-denied. The seat still advertises `keyboard`, and no key reaches any client.
- **The protocol does not promise anything stronger.** W:2014-2015 defines the capability bit as "if a member is set, then it is present on the seat". That is presence, not delivery.

### 2. `hyprctl devices` cannot show those drop gates

- **The emitted fields per keyboard** (`HyprCtl.cpp:784-801`) are only `address`, `name`, `rules`, `model`, `layout`, `variant`, `options`, `active_layout_index`, `active_keymap`, `capsLock`, `numLock` and `main`. There is no `enabled`, no `allowed`/permission field and no focus field.
- **`main` is `m_active`.** It is set by `CSeatManager::setKeyboard` (`SeatManager.cpp:161-173`), which the key path calls at `InputManager.cpp:1677`. It marks the keyboard that was last active on the seat. It does not identify a focused surface or a receiving client.
- **The list is every member of `m_keyboards`, including protocol-created virtual keyboards** (`InputManager.cpp:1127-1130`; added to the capability set at `:89-92`). A client's virtual keyboard can therefore keep `keyboard` in the capability set and appear in `devices` even if no physical keyboard exists.
- **Committed host history already shows these are snapshots.** The keyboard node count was 8 in round 2 and 9 in round 3 (`config-health-report-r3.md:157,932`), and the corpus labels it hotplug-sensitive. A node count is not a device health or delivery measurement.

### 3. Even an enabled and allowed key has seven more exits before the app

All of these sit in `InputManager.cpp:1619-1682` unless another file is named:

1. **Event-bus cancel** (`:1629-1632`), for example a plugin.
2. **`inputCapture` capture** sets `passEvent=false` (`:1634-1639`).
3. **A matching keybind consumes the key.** `KeybindManager.cpp:409` gives `suppressEvent = !…passEvent`, and `:841-842` passes the key on only when no bind was found or the dispatcher allows it.
4. **An IME grab diverts the key to the input method instead of the seat** (`:1661-1663`). This connects to the unexercised IME limit.
5. **Multi-keyboard merge or dedupe can swallow a press or release** (`:1648-1670`).
6. **No focus resource means a silent return.** `SeatManager.cpp:256-257` returns when `!m_state.keyboardFocusResource`.
7. **A key goes only to `wl_keyboard` objects of the focus client's bound seat resources** (`SeatManager.cpp:259-268`). It is also dropped when that resource has no `m_currentSurface` (`Seat.cpp:421-423`).

The protocol states the same rule. W:2684-2685 says the compositor "must not send this event if the wl_keyboard did not have an active surface immediately before this event". The active surface is set only by `wl_keyboard.enter` (W:2622-2624). Neither the capability event nor `devices` reports a per-client enter.

### 4. "Focused" is not observable from either surface, and not from `activewindow` either

- **The seat focus can be something other than the active window.** The keyboard-focus surface may be a layer surface: exclusive layer surfaces take priority (`InputManager.cpp:454-465`) and `refocusLastWindow` is refused while one exists (`:1758-1760`). It may also be a seat-grab surface (`SeatManager.cpp:582-614,687-790`).
- **`hyprctl activewindow`** reads `Desktop::focusState()->window()` (`HyprCtl.cpp:633-634`), not the seat's `m_state.keyboardFocus`.
- **No hyprctl command reads `keyboardFocus`.** Grepping `HyprCtl.cpp` for `keyboardFocus` returns 0 hits.
- **The protocol does not guarantee focus either.** W:2009 says a seat "typically" "maintains a keyboard focus". That is not a guarantee about which client holds it.

### 5. The host capture held no capability observation

- **Round 13 deliberately excluded the capability list.** `globals.json:339` lists "wl_seat human-readable name and capability list" as excluded, so only `{interface: wl_seat, version: 9}` is held.
- **A registry global is not the capability event.** W:2032 says the event is "sent on binding". An unbound advertisement therefore says nothing about capabilities.
- Any U6 text implying "seat has a keyboard" from the round-13 capture overreaches by one rung before delivery is even considered.

### 6. Delivered is not the same as the app outcome

The client may still ignore or reinterpret what it receives. W:2627-2628 tells clients not to treat the `enter` key list as key presses, and keymap interpretation is client-side (W:2675-2676). Delivery is necessary for an app outcome but not sufficient. This keeps "app outcome" a separate, later `[UNK]` rung.

## Impacted axes

- **Coverage (C1/U6), structural risk.** If the ladder merges "advertised/present" with "delivered/focused", the U6 note overclaims and would fail a semantic hand check. This is the same class of rejected inference as R14's advertisement-is-not-behavior rule.
- **No harm** to U1-U5 or to operability.

## Smallest safe correction (for L1 / LayerJoin; no edit made here)

1. Each U6 ladder row should state three things:
   - **Proves:** the compositor HID set includes a keyboard/pointer HID object (capability), or names, keymaps and the last-active `main` (devices).
   - **Does not prove:** enabled, permission-allowed, not bind-consumed, not captured or IME-diverted, focus target, per-client `enter`/`key`, or app outcome.
   - **Cite:** H `InputManager.cpp:1620-1621,1869-1881` and `HyprCtl.cpp:784-801`, plus W:2014-2015,2684-2685.
2. Gloss `main` as "last-active keyboard (`m_active`)", never as "focused" or "primary input path".
3. Describe the round-13 `wl_seat` row as "registry advertisement v9; capability list not captured (`globals.json:339`)".
4. Keep the following at `[UNK]` with operator-owned execution:
   - delivery: client `wl_keyboard.enter`/`key` on a named surface;
   - IME routing;
   - kernel/libinput event content;
   - app outcome.

   No new capture or probe is required for the bounded route.

This is a fixable defect, not a judge-reject tradeoff: the fix is wording and rung separation, and it costs no coverage.

## Process record

- **Installs or updates:** none.
- **Scratch:** the six upstream source files were fetched read-only with `curl` into `/tmp/ad15` and deleted after the report was written. The fetch can be repeated from the URLs and digests above.
- **Not done:** no input events read, recorded, replayed or injected; no compositor action; no protocol client; no tests or gates run.
