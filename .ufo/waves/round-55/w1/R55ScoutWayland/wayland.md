# R55ScoutWayland: wl_keyboard repeat semantics (protocol level, read-only)

Lane: mado round-55 w1, seat R55ScoutWayland. Scope: protocol facts with located quotes, the Hyprland guard at `fetch/Hyprland-protocols-core-Seat.cpp:441-448`, and what is outside mado's province. No edits to tracked files.

## Sources and provenance

- S1 `fetch/wayland-1.26.0-wayland.xml`, sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`, matches `fetch/SHA256SUMS.txt`. `<interface name="wl_keyboard" version="11">` at line 2573, ends line 2752.
- S2 `fetch/Hyprland-protocols-core-Seat.cpp`, sha256 `cc23bb8b4f1e44cd46ab278e5353275dbb03adfe3955393af64c7b828ed0818d`, matches `SHA256SUMS.txt`.
- S3 libwayland tag 1.26.0, `src/wayland-client.c`, one hop: `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/src/wayland-client.c`. Not in the fetch pins.

## 1. `wl_keyboard.repeat_info` (since 4), S1:2732-2751

- L2732: `<event name="repeat_info" since="4">`
- L2734: "Informs the client about the keyboard's repeat rate and delay."
- L2736-2738: "This event is sent as soon as the wl_keyboard object has been created, and is guaranteed to be received by the client before any key press event."
- L2740-2741: "Negative values for either rate or delay are illegal. A rate of zero will disable any repeating (regardless of the value of delay)."
- L2743-2745: "This event can be sent later on as well with a new value if necessary, so clients should continue listening for the event past the creation of wl_keyboard."
- L2747-2750: `rate` is `type="int"`, "the rate of repeating keys in characters per second"; `delay` is `type="int"`, "delay in milliseconds since key down until repeating starts".

**Rate 0.** Per L2740-2741 it disables repeating in the client, and the delay is irrelevant. The text does not say who repeats instead. That is answered only by the `repeated` text in section 2.

**Negative values.** L2740 calls them "illegal". The `wl_keyboard` block (L2573-2752) defines no `<enum name="error">`; the only error enums in the file are on other interfaces (for example L2022 `wl_seat`, L2150 `wl_pointer`). So the protocol names no error code, no required reaction, and no defined receiver behaviour for a negative value. The text says the sender must not send one, and the schema does not say what a receiver must do if one arrives.

**When sent.** Once at `wl_keyboard` creation, before any key press (L2736-2738). Later updates are allowed "if necessary" (L2743-2745). The text gives no rate-limit or minimum-change rule, and does not say whether an identical re-send is forbidden.

## 2. `key_state` `repeated` (since 10), S1:2652-2699

- L2656-2658: "Since version 10, the key can be in a "repeated" pseudo-state which means the same as "pressed", but is used to signal repetition in the key event."
- L2660-2662: "The key may only enter the repeated state after entering the pressed state and before entering the released state. This event may be generated multiple times while the key is down."
- L2666: `<entry name="repeated" value="2" summary="key was repeated" since="10"/>`
- L2690-2693: "Since version 10, compositors may send key events with the "repeated" key state when a wl_keyboard.repeat_info event with a rate argument of 0 has been received. This allows the compositor to take over the responsibility of key repetition."
- L2681-2684 (logical-state text of `key`): "In the wl_keyboard logical state, this event adds the key to the keys currently logically down (if the state argument is pressed) or removes the key from the keys currently logically down (if the state argument is released)."

**Ambiguity 1.** L2690-2693 says compositors "may" send `repeated`, and only after a rate of 0 has been received. It does not require the compositor to repeat when the rate is non-zero, and it does not say what happens when the rate is 0 and the compositor sends nothing. Combined with L2740-2741, a rate of 0 means the client stops self-repeating, and the protocol leaves the rest to the compositor.

**Ambiguity 2.** The logical-state text at L2681-2684 covers only `pressed` and `released`. It does not say whether a `repeated` event changes the set of logically-down keys. Section 2 of the protocol implies it does not, but the text does not state it.

**Version gate.** `repeated` exists only from version 10 (L2666, L2656). Nothing in the quoted text says what a compositor must do when a client is bound below version 10.

## 3. Hyprland guard, S2:441-448

Verbatim:

```
441  void CWLKeyboardResource::repeatInfo(uint32_t rate, uint32_t delayMs) {
442      if (!m_owner || m_resource->version() < 4 || (rate == m_lastRate && delayMs == m_lastDelayMs))
443          return;
444      m_lastRate    = rate;
445      m_lastDelayMs = delayMs;
446  
447      m_resource->sendRepeatInfo(rate, delayMs);
448  }
```

What the guard does with the values:

- **Rate 0 is passed through unchanged.** There is no `rate == 0` branch. The value goes to `sendRepeatInfo(0, delayMs)` with the delay unchanged. This matches L2740-2741.
- **Negative values are not checked.** The parameter is `uint32_t` (L441), but the protocol argument is `int` (S1 L2747, L2749). A negative `int` passed in is converted to a large `uint32_t`, and the guard does not catch it. What reaches `sendRepeatInfo` is the converted value; whether that re-encodes as a negative wire `int` depends on the `sendRepeatInfo` signature, which is not in the fetch pins. **UNVERIFIED.**
- **Negatives never reach this function from the fetched paths.** Upstream, `Hyprland-InputManager.cpp:1282-1283` stores `std::max(0, REPEATRATE)` and `std::max(0, REPEATDELAY)`. The config also declares `.min = 0` (`Hyprland-ConfigValues.cpp:279-280`). `m_repeatRate` and `m_repeatDelay` are `int` with default 0 (`Hyprland-IKeyboard.hpp:121-122`). So the clamp is upstream, not in the guard.
- **Dedupe.** A repeat identical to the last sent `(rate, delay)` pair on the same resource is dropped. `m_lastRate` and `m_lastDelayMs` are not declared in any fetched file (the header `Seat.hpp` is not in the pins). Their initial values are **UNVERIFIED**. If they start at `(0, 0)`, the first `repeat_info` for a `(0, 0)` configuration would be silently dropped, which conflicts with L2736-2738 (the event must be received before any key press).
- **Version gate.** Clients bound below version 4 get a silent return (`version() < 4`). This matches L2732 (`since="4"`). Nothing is logged.
- **`!m_owner`** is also a silent return.
- **No keyboard-capability check in `repeatInfo` itself.** `sendKey` (S2:425-426) and `sendMods` (S2:435-436) both check `HID_INPUT_CAPABILITY_KEYBOARD`. `repeatInfo` (441-448) does not. The only capability check on this path is in the broadcast `CWLSeatProtocol::updateRepeatInfo` (S2:603-605). The creation path (S2:349-350) reaches `repeatInfo` without one, guarded only by the `m_keyboard` null check at S2:344. Whether a `wl_keyboard` can exist without that capability is **UNVERIFIED**.
- **No `repeated` emission in fetched code.** A grep for `KEY_STATE_REPEATED|key_state_repeated|STATE_REPEATED|REPEATED` over the fetch directory found only the `m_lastRate`/`m_lastDelayMs` lines in the guard. The signal `m_keyboardEvents.repeatInfo` is declared at `Hyprland-IKeyboard.hpp:57` but never emitted in the fetched files (`IKeyboard.cpp`, `InputManager.cpp`, `SeatManager.cpp`, `Seat.cpp`, `IKeyboard.hpp`, case-insensitive sweep). So in the fetched sources, the compositor-side takeover of L2690-2693 is not implemented: with rate 0 the client receives rate 0 and no `repeated` events.

## 4. When the guard is reached (fetched code)

| Trigger | Location | Path |
|---|---|---|
| `wl_keyboard` created | S2:339-350 | `repeatInfo(m_repeatRate, m_repeatDelay)` at S2:350 |
| Active keyboard changes | `SeatManager.cpp:161-173` (call at 172) | `updateActiveKeyboardData` (175-180) → `updateRepeatInfo` (S2:603-610) → per-resource `repeatInfo` |
| Keymap reload on any keyboard | `IKeyboard.cpp:143-147` (call at 147, unconditional) | `updateActiveKeyboardData` uses the *active* keyboard's values |
| Keymap event on the active keyboard | `InputManager.cpp:1180-1185` | same |
| Key or modifier from a different keyboard | `InputManager.cpp:1677-1678`, `1718-1719` | `setKeyboard` runs before `sendKeyboardKey`/`sendKeyboardMods`, so a changed rate goes out before the key event |
| Config applied to a device | `InputManager.cpp:1282-1286` | sets the values, then calls `setKeymap` at 1286, which reaches `IKeyboard.cpp:147` |

The enclosing function header of S2:339-350 was not read. The line 1286 → `IKeyboard.cpp:147` link follows from the call order shown; I did not trace `setKeymap`'s body beyond line 147.

Read against the protocol: the `setKeyboard` call at `InputManager.cpp:1677` precedes the key event, which matches L2736-2738. The guard's dedupe means most of these triggers are no-ops when the values did not change.

## 5. Out of mado's province, or unmeasured

Mado can read the protocol text and what this compositor passes into it. It cannot measure how a real client uses the values. Whether a toolkit or application (GTK, Qt, wlroots clients, terminals, browsers) honours rate 0 by turning off its own timer, how it times repeats from `delay`, and whether it reacts to `repeated` at all, are all client behaviour that the fetched files do not contain. The XKB per-key repeat setting (`xkb_keymap_key_repeats`) is also outside these files, and so is any `repeated`-state handling by a client library. Measured repeat latency and jitter need live input and a real client, which this lane does not have. The libwayland client source (S3) does not implement repeat either, so the protocol text and the client's own code are the only places that define the behaviour. Host values (`fetch/host-getoption.json`: rate 40, delay 250; `fetch/host-input.conf` lines 14-15) are pinned copies; this seat did not run `hyprctl`.

## 6. libwayland 1.26.0 (S3): one hop

`src/wayland-client.c` at tag 1.26.0 contains no occurrence of "repeat" (a grep over the full fetched text returned no matches; the same grep returned matches for `wl_display_interface` from the same artifact, so the search covered the content). The file is the generic dispatcher. Adds nothing on repeat semantics. It confirms that libwayland does not synthesize repeat events or interpret `rate`/`delay`. The generated `wl_keyboard` dispatch (`wayland-client-protocol.c`) is not fetched and is not covered.

## Verified vs not

- Verified by reading the pinned files and the one-hop source: all quotes above, the guard body, the trigger chain, the absence of `repeated` emission in fetched Hyprland files, and the absence of repeat logic in `wayland-client.c`.
- UNVERIFIED: `sendRepeatInfo` parameter type; `m_lastRate`/`m_lastDelayMs` initial values; caps invariant for the creation path; the body of `setKeymap` beyond line 147; the enclosing function of S2:339-350.
