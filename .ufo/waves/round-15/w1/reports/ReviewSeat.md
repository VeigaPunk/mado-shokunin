# ReviewSeat — U6 integration risk: capability advertisement vs bound client delivery

Scope: static review of the U6 input-debugging route for the single risk "wl_seat capability advertisement versus bound client delivery". Read-only: lane artifacts, installed `/usr/share/wayland/wayland.xml`, upstream static bytes (curl to `/tmp`, nothing written into the repo), pinned Hyprland source at `efb50993780079460b0cbed1363e2166a2de1d9f`. No live probe, no input reads, no tests, no commits. Tools: none installed or upgraded (`curl`, `sha256sum`, `jq`, `cmp` pre-existing).

Labels: `[INF-docs]` upstream protocol text; `[INF-code]` pinned upstream source, not observed behaviour; `[OBS]` lane host observation; `[UNK]` not exercised.

## Findings (severity order)

**F1 — high. The host's seat capability bits are not observed anywhere in the lane.**
`.ufo/waves/round-13/w1/globals.json` records `wl_seat` as `{"interface":"wl_seat","version":9}` only (`.globals`). Its `excluded` array names "wl_seat human-readable name and capability list" as deliberately not retained. Therefore "this host advertises keyboard/pointer" is `[UNK]` for the host. The only capability statements available are source-level `[INF-code]`. Any U6 sentence asserting host capability presence without a new authorized capture is a defect.

**F2 — high. Advertisement is seat-wide device-class presence, not a per-client grant.**
- `[INF-docs]` `wayland.xml` `wl_seat` (installed, `<interface name="wl_seat" version="11">`, capabilities event `:2030-2057`): the event carries "the complete set of capabilities this seat has"; `get_pointer`/`get_keyboard`/`get_touch` (`:2075` onward) are separate requests that create objects.
- `[INF-code]` Hyprland `src/managers/input/InputManager.cpp:1869-1880` `CInputManager::updateCapabilities` ORs `getCapabilities()` over every live HID, then calls `g_pSeatManager->updateCapabilities`. Callers: `:91`, `:96` (virtual keyboard/pointer), `:1533` (`removeFromHIDs`).
- `[INF-code]` `src/managers/SeatManager.cpp:150-152` forwards to `PROTO::seat->updateCapabilities`; `src/protocols/core/Seat.cpp:583-592` sends the new mask to every seat resource when it changes. Nothing in this path is keyed to a client that holds a focused surface.

**F3 — high. Delivery requires a bound object owned by the focused client; absent that it is a silent drop.**
- `[INF-docs]` `wl_keyboard` description: each keyboard starts with a null active surface; nothing is delivered until `enter`.
- `[INF-code]` `Seat.cpp:467-476` `get_keyboard` creates a `CWLKeyboardResource` and appends it to the seat resource's `m_keyboards`.
- `[INF-code]` `SeatManager.cpp:230-231` sets `m_state.keyboardFocusResource` for the focused surface's client **before** iterating that client's `m_keyboards` (`:231`). `:235` sends `enter` per keyboard.
- `[INF-code]` `SeatManager.cpp:255-270` `sendKeyboardKey` (and `sendKeyboardMods` `:272`) passes the `keyboardFocusResource` guard whenever it is non-null, then iterates `m_keyboards`. A client with focus and zero bound `wl_keyboard` objects gets no error and no event. This is a silent no-op, `[UNK]` until exercised.

**F4 — high. `enter` is gated on the capability at send time, so focus can exist without any enter.**
- `[INF-code]` `Seat.cpp:370` (`sendKeymap`), `:393` (`sendEnter`), and `:413/:425/:435` (other keyboard sends) each return early when `m_currentCaps` lacks `KEYBOARD`.
- Combined with F3: a focus change while the seat lacks keyboard capability leaves `keyboardFocusResource` set, sends no `enter`, and drops keys silently.
- `[INF-code]` `SeatManager.cpp:186-189`: `setKeyboardFocus` with no `m_keyboard` logs "BUG THIS" and returns. This is a second, separate gate (keyboard presence in the input manager, not the seat mask).

**F5 — medium. Late binding receives enter on the source path.**
- `[INF-code]` `Seat.cpp:352-358` (`CWLKeyboardResource` constructor): if the new resource's client matches `m_state.keyboardFocus`'s client, it calls `sendEnter`. So a `wl_keyboard` bound after focus was granted does get `enter` (subject to F4's capability gate). Any claim that late binding never delivers input is contradicted by source; any claim that it always does is unexercised.

**F6 — medium. Divergence candidate: `get_keyboard`/`get_pointer` without capability.**
- `[INF-docs]` `wayland.xml` `wl_seat` error `missing_capability` (`:2026`): "It is a protocol violation to issue this request on a seat that has never had the … capability."
- `[INF-code]` `Seat.cpp:467-476` (`setGetKeyboard`) and `:479-488` (`setGetPointer`) emplace resources with no capability check and no `missing_capability` path in the visible lambda bodies. Hyprland also does not track "had the capability in the past". This is a static divergence candidate, not an observed behaviour. U6 may mention it only as `[INF-code]`/`[UNK]`, never as host behaviour.

**F7 — medium. Capability removal does not release client objects on the source path.**
- `[INF-docs]` `wayland.xml` `capabilities` event (`:2030-2057`): clients "should" release objects when a capability is removed; no further events arrive.
- `[INF-code]` `Seat.cpp:583-592` only sends the new mask. Objects persist, and sends are gated by `m_currentCaps` (F4). The U6 note should state "no events while capability absent" as `[INF-code]`, not "objects are destroyed".

**F8 — low (source hygiene). Pinning and scope collision.**
- Installed `wayland.xml` sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07` is byte-identical to upstream `wayland/wayland` tag `1.26.0` `protocol/wayland.xml` (fetched by curl, `cmp` equal, 2026-10-20). S052 can therefore cite the upstream raw URL without a local path.
- `corpus/SOURCES.md` has no `…/-/raw/1.26.0/…` URL. S043 cites the local path and a docs anchor, scoped to `wl_registry` (`:117-177`). S052 must be scoped to `wl_seat`/`wl_keyboard`/`wl_pointer` and must not reuse S043's scope.
- Hyprland source hashes at `efb50993…` (first 20 hex chars of `sha256sum`): `src/managers/input/InputManager.cpp` `feedf32e2e3d23aeaed7`; `src/managers/SeatManager.cpp` `bd7485535c7e9f71382e`; `src/protocols/core/Seat.cpp` `cc23bb8b4f1e44cd46ab`. Re-derive with `curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/<path> | sha256sum`.
- Hyprland rows are `[INF-code]` tier evidence (cf. S050 pattern: "not observed host behavior"). They cannot carry a host verdict.

## Acceptance conditions (the U6 capability-delivery sentence passes only if all hold)

A1. Capability presence is stated as seat-wide, source-level, and unobserved on this host (F1, F2). Host wording is `[UNK]` unless a separately authorized sanitized capability capture exists.
A2. Delivery is stated as requiring, as separate evidence classes: (i) a bound `wl_keyboard`/`wl_pointer` owned by the focused surface's client; (ii) a focus event from `SeatManager.cpp:182-252`; (iii) the capability gate at send (`Seat.cpp:370/393`); (iv) compositor routing before the client (F3, F4).
A3. The silent-drop case (focus with zero bound keyboards, or focus without capability) is recorded as `[INF-code]`, `[UNK]` on the host, with no error to the client claimed (F3, F4).
A4. Late bind is recorded with the `Seat.cpp:352-358` path and the capability caveat (F5).
A5. `missing_capability` divergence and capability-removal object lifetime are either omitted or recorded as `[INF-code]`/`[UNK]` (F6, F7).
A6. Every upstream citation carries a revision and a hash: wayland.xml `cc860987…` at tag 1.26.0; Hyprland at `efb50993…` with the three hashes above. Shortened hashes are labelled as prefixes with a re-derive command (QUALITY rule 6).
A7. Keyboard capability/focus is kept distinct from text-input/IME and pointer rendering; this seat's note does not claim keystroke or cursor delivery (sibling reviewers own those).
A8. Scope stays documentary: no claim that any key or pointer event was produced, read, or injected.

## Rejection conditions (any one blocks the U6 sentence)

R1. Any sentence equating `wl_seat` v9 in `globals.json` with keyboard or pointer capability presence or delivery.
R2. Citing `globals.json` or S041 for capability bits; they are excluded by design.
R3. Claiming focus or any keystroke/pointer receipt follows from advertisement or binding alone.
R4. Presenting Hyprland `[INF-code]` as observed host behaviour, or as binary-source equivalence.
R5. Using S043 (`wl_registry` scope) as support for the capability lifecycle.
R6. Admitting S052 with a local `/usr/share/…` path, or with a scope identical to S043.
R7. Requiring a live seat, focus, or input probe to pass. Out of scope for this round; passing condition is documentary.
R8. Claiming missing-capability enforcement or capability-removal destruction as host facts (F6/F7).

## Evidence pointers

- `.ufo/waves/round-13/w1/globals.json` — `.globals` (wl_seat v9 only), `.excluded` (capability list excluded).
- `corpus/knowledge/wayland-protocol-boundaries-r13.md` §Advertisement, binding and behavior (advertisement ≠ binding ≠ behaviour); §Rejected.
- `corpus/SOURCES.md:55` (S043 row); `:59` (S047); `:60` (S048); `:62` (S050 "not observed host behavior").
- `/usr/share/wayland/wayland.xml` — `wl_seat` `:2004-2137`; capabilities event `:2030-2057`; `missing_capability` `:2026`; `get_keyboard` `:2075`; `wl_keyboard` `:2573`; keymap `:2600`; enter `:2614`; key `:2669`. sha256 `cc860987…5f07`.
- Upstream `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml` — byte-identical to installed (fetched 2026-10-20).
- Hyprland @`efb50993780079460b0cbed1363e2166a2de1d9f` (static, `[INF-code]`):
  - `src/managers/input/InputManager.cpp:91, 96, 1533, 1869-1880`
  - `src/managers/SeatManager.cpp:150-152, 182-189, 230-235, 255-270, 272-282`
  - `src/protocols/core/Seat.cpp:337-358, 366-384, 387-398, 467-488, 505-508, 527-537, 583-592`
- `corpus/lessons/round-14.md` M1 (retained-data scope; S049 correction) — establishes the same field-specific retention discipline this note must follow.

## Residual risk and verification gaps

- No host capability was observed; host seat capability and delivery remain `[UNK]`. A future authorized read-only capture could record seat capabilities without retaining device identity, but it is not part of this round.
- Hyprland behaviour is inferred from source at one pinned commit. Compositor runtime state (e.g. input inhibitors, keybind/shortcut interception, layer-surface exclusivity) is not reviewed here and is outside this seat's assignment.
- The F6 divergence is a read of three lambda bodies; a helper or macro outside the fetched file could add a check. Keep it `[INF-code]` until confirmed.
- Checks for the main agent to run (not run by this seat): read-only confirmation of the SHA-256 values above against the fetched upstream bytes, and a grep confirming no `…/raw/1.26.0/…` URL exists in `corpus/SOURCES.md` before S052 is appended.
