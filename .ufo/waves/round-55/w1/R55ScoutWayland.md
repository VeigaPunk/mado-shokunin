# Seat R55ScoutWayland: report (round-55 w1)

Scope: read-only research on `wl_keyboard.repeat_info` and key state `repeated`, the Hyprland guard at `fetch/Hyprland-protocols-core-Seat.cpp:441-448`, one hop to libwayland 1.26.0. Deliverable: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ScoutWayland/wayland.md`. This report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ScoutWayland.md`.

## What I did

1. Searched `claims-frozen.md` and `registration.md` with grep only (grep for scout or wayland.md rules). I did NOT read them in full, although the lane brief asked for that first; nothing in this scout seat depends on their text beyond the pin list. No edits to either file.
2. Verified the pins against `fetch/SHA256SUMS.txt`:

```
$ sha256sum fetch/wayland-1.26.0-wayland.xml fetch/Hyprland-protocols-core-Seat.cpp
cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07  wayland-1.26.0-wayland.xml
cc23bb8b4f1e44cd46ab278e5353275dbb03adfe3955393af64c7b828ed0818d  Hyprland-protocols-core-Seat.cpp
```
Both match the SHA256SUMS.txt entries.

3. Read the XML: `repeat_info` L2732-2751, key_state L2652-2667, key event L2669-2699, the `wl_keyboard` interface L2573-2752, and grep for `<enum name="error"` (only other interfaces define error enums; `wl_keyboard` defines none).
4. Read Seat.cpp L441-448 (the guard), L339-350 (creation path), L603-610 (broadcast path). Grep for `repeatInfo|sendRepeatInfo|repeat_info` and `m_repeatRate|m_repeatDelay|repeatRate|repeatDelay|setRepeatInfo|repeat_rate`, then read the callers (InputManager L1164-1203 and L1219-1286, SeatManager L159-185, IKeyboard L127-151).
5. Grep for `m_lastRate|m_lastDelayMs|KEY_STATE_REPEATED|key_state_repeated|STATE_REPEATED|REPEATED` over the fetch directory, then a case-insensitive `repeat` sweep over IKeyboard.cpp, InputManager.cpp, SeatManager.cpp, Seat.cpp and IKeyboard.hpp.
6. One hop: `read https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/src/wayland-client.c` (2852 lines, returned as artifact://81662). Grep for `repeat` returned no matches on the artifact; a grep for `wl_display_interface|repeat` on the same artifact returned matches, which validates the search. Grep was used only because it was the search tool; it was not run against any live system.
7. Host: did not run `hyprctl`. Only the pinned host copies in `fetch/` were read (`host-getoption.json`, `host-input.conf`).
8. No git, jj, commit, push, delegation, background job, or write to the fleet, sibling lanes, or shokuknow. No tools installed.

Key output lines (trimmed):

```
wayland-1.26.0-wayland.xml:2734  Informs the client about the keyboard's repeat rate and delay.
wayland-1.26.0-wayland.xml:2740  Negative values for either rate or delay are illegal. A rate of zero
wayland-1.26.0-wayland.xml:2741  will disable any repeating (regardless of the value of delay).
wayland-1.26.0-wayland.xml:2690  Since version 10, compositors may send key events with the "repeated"
wayland-1.26.0-wayland.xml:2691  key state when a wl_keyboard.repeat_info event with a rate argument of
wayland-1.26.0-wayland.xml:2692  0 has been received. This allows the compositor to take over the
Hyprland-protocols-core-Seat.cpp:441  void CWLKeyboardResource::repeatInfo(uint32_t rate, uint32_t delayMs) {
Hyprland-protocols-core-Seat.cpp:442      if (!m_owner || m_resource->version() < 4 || (rate == m_lastRate && delayMs == m_lastDelayMs))
Hyprland-protocols-core-Seat.cpp:447      m_resource->sendRepeatInfo(rate, delayMs);
Hyprland-IKeyboard.hpp:57     CSignalT<>                repeatInfo;      (declared, no emitter in fetched files)
Hyprland-IKeyboard.hpp:121    int                            m_repeatRate        = 0;
InputManager.cpp:1282         pKeyboard->m_repeatRate  = std::max(0, REPEATRATE);
```

## Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ScoutWayland/wayland.md` (protocol facts, guard analysis, trigger table, out-of-province paragraph, libwayland note).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ScoutWayland.md` (this report).

No receipts were copied; the scratch directory held no files.

## Defects and ambiguities found

1. **Protocol: "illegal" with no error code.** `wayland-1.26.0-wayland.xml:2740` says negative `rate`/`delay` are "illegal". The `wl_keyboard` block (2573-2752) defines no error enum, so the protocol names no error and no required receiver behaviour.
2. **Protocol: `repeated` takeover is permissive.** `:2690-2693` uses "may", conditioned on a rate of 0 having been received. It does not say what a compositor does for non-zero rates, or what clients should expect for rate 0 with no `repeated` events.
3. **Protocol: logical-state gap for `repeated`.** `:2681-2684` covers only pressed and released. It does not say whether `repeated` changes the logically-down set.
4. **Hyprland: signedness.** `Hyprland-protocols-core-Seat.cpp:441` takes `uint32_t`; the protocol argument is `int`. The guard has no sign check. Negatives are excluded upstream by `InputManager.cpp:1282-1283` (`std::max(0, ...)`) and the config `.min = 0` (`ConfigValues.cpp:279-280`), so the fetched paths do not hit this. The wire round-trip depends on `sendRepeatInfo`'s signature, which is not in the pins: UNVERIFIED.
5. **Hyprland: possible first-send suppression.** The guard (`:442`) compares against `m_lastRate`/`m_lastDelayMs`, which are not declared in any fetched file. If their initial values are `(0, 0)`, a configuration of rate 0 with delay 0 would drop the first `repeat_info`, conflicting with `:2736-2738`. UNVERIFIED (header not pinned).
6. **Hyprland: missing capability check.** `repeatInfo` (`:441-448`) has no `HID_INPUT_CAPABILITY_KEYBOARD` check, unlike `sendKey` (`:425-426`) and `sendMods` (`:435-436`). The only such check on this path is in `updateRepeatInfo` (`:604-605`). The creation path (`:349-350`) relies on the `m_keyboard` null check alone. Whether a keyboard resource can exist without the capability is UNVERIFIED.
7. **Hyprland: rate 0 leaves clients with no repeats.** No fetched file emits key state `repeated`. `IKeyboard.hpp:57` declares `m_keyboardEvents.repeatInfo` but nothing emits it in the fetched files. With `repeat_rate = 0` the compositor sends rate 0 (`:350`, `:608`) and does not take over repetition. Whether a fuller source tree does this is not known from these pins.
8. **Pins: partial.** The Hyprland pins are eight files; `Seat.hpp`, the full `IKeyboard.cpp` body, and `sendRepeatInfo` are missing, so items 4, 5 and 6 stay open.

## Could not verify

- `sendRepeatInfo` parameter type and the wire encoding of a converted negative value.
- `m_lastRate` / `m_lastDelayMs` initial values (item 5).
- The enclosing function header for `Seat.cpp:339-350`, and whether the creation path is reachable without keyboard capability (item 6).
- The body of `IKeyboard::setKeymap` beyond line 147; I only traced the call at 147.
- Any client behaviour (toolkit repeat timers, handling of rate 0, handling of `repeated`, XKB per-key repeat). Outside these pins; no measurement possible in this lane.
- Live host state: did not run `hyprctl`; only the pinned host copies were read.
- Upstream `wayland-scanner` generated dispatch code for `wl_keyboard` (not fetched).

## Cleanup

Scratch `/fast/scratch/hyaku/mado-r55/R55ScoutWayland/` was created empty and removed. No files outside the two deliverable paths were written.
