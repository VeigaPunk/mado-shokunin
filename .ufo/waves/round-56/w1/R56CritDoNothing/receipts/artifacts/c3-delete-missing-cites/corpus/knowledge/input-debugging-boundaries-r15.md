source: S051 https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst (tag 1.32.0, libinput-list-devices/debug-events/record, SHA-256 53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f); S052 https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml (tag 1.26.0, wl_seat/wl_pointer/wl_keyboard, SHA-256 cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07)
verified-at: 2026-10-20; static primary-document/XML inspection, not a live input-delivery test
recheck: Reopen the tagged S051/S052 source elements and compare the persisted digests; run `pacman -Q libinput wayland` and `sha256sum /usr/share/wayland/wayland.xml`. Stop on source/version/digest drift. Do not collect events.
covers: U6

# Input debugging — keep the layers apart

This note admits **a bounded diagnostic route**, not working input delivery,
complete U6 feature coverage, a kernel diagnosis or a new executed capability.
S051 supersedes queued [ref]'s loose composite tools description and mutable
anchor. S052 adds the core input contract, distinct from [ref]'s registry scope.
The round-15 primary-source checks are independent of the structural counter.

Version boundary: the parent initially observed `libinput 1.31.3-1` and
`wayland 1.26.0-1` with `pacman -Q` on 2026-10-20. During this wave a seat
upgraded libinput to 1.32.0-1 and installed libinput-tools 1.32.0-1;
the round lesson records actor, transaction and dependencies. Matching the
on-disk package to the 1.32.0 docs is **not** proof of the library loaded by
the running compositor or input behavior. No restart was performed.
S051's statements are `[INF-docs]`, not host feature measurements.
The reopened latest HTML page also says 1.32.0, but is not the immutable
anchor. `/doc/1.32.0/tools.html` returned HTTP 404; the tagged RST was
opened instead. No source-tag-to-binary equivalence is claimed.

## Layer ladder

Choose the claim first; do not climb from a weaker observation to a stronger
conclusion without new evidence at the next layer.

| Layer / question | Permitted evidence route | What it establishes | What it does not establish |
|---|---|---|---|
| Kernel/device → libinput: what does a helper describe? | Read S051 `libinput-list-devices`, `libinput-debug-events`, `libinput-record`; no tool execution here | `[INF-docs]` list-devices describes devices recognized by its libinput context and built-in defaults; record captures kernel events independently of a compositor/libinput context | Hyprland's active settings, processing of a particular event, focus, client receipt, rendered feedback or hardware health |
| Compositor policy: what was configured or enumerated? | Existing [config/live-layer route](hyprctl-verification-layer.md), input settings and `devices` metadata; a fresh authorized read must be sanitized before retention | A dated declaration, option value or compositor inventory, according to that route's own OBS/INF boundary | Actual event delivery; a recognized keyboard does not prove the intended client received a key. This round does not freshly run these commands |
| Wayland seat/capability: what can a client bind? | S052 `wl_seat.capabilities`, XML:2004–2087 | `[OBS-source]` capabilities change on bind/gain/loss; keyboard/pointer objects have capability-dependent lifecycles | [ref] retained only `wl_seat` interface/version 9, not capability bits; no captured focus or key event follows |
| Wayland client focus/event contract: which protocol state is relevant? | S052 `wl_pointer.enter`/`leave`/`motion`/`button`, XML:2138–2265; `wl_keyboard.enter`/`leave`/`key`, XML:2614–2699 | `[OBS-source]` pointer events are surface-local/focus-related; keyboard enter identifies a focused surface; key events carry platform-specific codes interpreted with the keymap. The key event requires an active surface in this XML revision | No live client input was observed; XML version 11 is not this host's advertised version 9, nor proof a diagnostic observer sees another client's stream |
| Toolkit/application outcome: did the intended action or text occur? | Authorized, claim-specific application observation would be required; none collected | `[UNK]` here | Neither physical key state, libinput helper output, compositor inventory nor the generic key contract guarantees text insertion, shortcut execution, IME composition or UI response |

### Concrete false inference

“`libinput list-devices` says natural scrolling is enabled, therefore
Hyprland currently uses it” is rejected. S051's **libinput list-devices**
Note explicitly says the output is the built-in defaults, not the desktop's
configuration. Start with the compositor-policy route for that narrower
claim; even a matching policy value would not prove client delivery.

S051 also says debug-events options must be set explicitly to reproduce the
sequence as the desktop sees it. Its output is not automatically a tap into
Hyprland's configured context. `record` is lower still: its kernel-event
capture is independent of the libinput context, X.Org/Wayland and running
libinput version. These distinctions are useful even when capture is not
permitted.

### Focus is not text

S052 `wl_keyboard.enter` sets the active surface and current logical keys;
it explicitly says clients should not synthesize key presses from that
pressed-key list. `leave` resets that logical state. The `key` event is a
platform-specific code interpreted through the provided mapping; the XML
is not a promise that a text field changes. Do not infer raw event
visibility, client focus or application text from a `wl_seat` global.
IME/text-input protocol behavior is outside this note; no additional
IME implementation or completeness claim is admitted.

## Safe boundary

This is a **static reading and routing** round. Actual configuration and
compositor state remain operator-owned under PROVINCE.md. The existing
SKILL read-verb whitelist is not broadened by describing upstream tools.

| Route | Disposition in this lane round | Why |
|---|---|---|
| Primary docs/XML, package version and XML checksum | Allowed static reads | No input stream, device access, focus changes or state application |
| `hyprctl getoption` / sanitized `devices` | Existing scoped read routes only; not run this round | Policy/inventory evidence, not input delivery; omit device identity and all session material before retaining any future result |
| `libinput list-devices` / list-kernel-devices / quirks | Documentation only; do not execute here | Device/node/seat identifiers can be retained, defaults are not compositor settings, and most helpers require input-device access |
| debug-events / debug-gui / evtest / protocol dumps / keymap or event logging | Not executed or collected | They can expose input/session material; an observer window/focus may itself change the situation. No raw device reads or broad `WAYLAND_DEBUG` capture |
| record, including `--no-events` | Not executed | Metadata-only recording still accesses a device and retains identity; the flag is not authorization. Default key-code obscuring does not make every recording anonymous |
| replay / virtual input / dispatch / setting options / reload | Mutation-class, not a harmless read probe | S051 says replay creates a new virtual device and replays events; no injection, focus changes, reload or compositor mutation is authorized |
| Kernel/driver repair or hardware diagnosis | Report to owning operator/lane, do not absorb | Device facts and a desktop symptom do not establish a kernel cause |

The upstream page recommends reproduction/record/replay procedures for its
bug workflow. They are **source data, not instructions to this lane**.
No permissions are acquired merely because documentation uses `sudo`.
Privacy screening must cover metadata and non-alphanumeric actions as well
as printable key codes; no raw recording is retained here.

## Unexercised delivery

`[UNK]` actual hardware event production, this compositor's processing of
those events, client focus/delivery, toolkit/IME behavior and the intended
application response remain unmeasured. No input capability was added to
SCORECARD's repertoire table. The coverage move is one sourced layer-route
entry on previously uncovered U6 ground, not successful end-to-end input
behavior. U7 Waybar module-text observation remains open too.
