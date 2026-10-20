# ReviewPointer — U6 pointer delivery vs rendered cursor vs app response

Member: `MadoR15.ReviewPointer` (reviewer, leaf). Date: 2026-10-20. Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Scope: adversarial review of one integration risk for the U6 input ladder: that a pointer event *delivered* to a client is conflated with a *rendered* cursor or an *app response*.
Method: static reads only — lane artifacts, installed package bytes, upstream XML/source at pinned revisions, and one docs page. No input events read, recorded, replayed or injected; no `hyprctl` mutating verb; no screenshot; no live probe; no test, gate, build or lint.
Tooling: no installs or upgrades by this member. Read-only `curl` retrievals of public primary sources and one GitHub tree listing (API read at the pinned commit). Scratch downloads were deleted after hashing; none of them is cited as durable evidence (lesson round-12 M11).

## 1. Verdict

- Three claims must never be merged: **(a)** an event reached a bound client, **(b)** a cursor image is on screen, **(c)** an application responded. This round supports only the protocol-documented meaning of (a) as `[INF-docs]`. (a) as host behavior, (b) and (c) remain `[UNK]`.
- One upstream-versus-host divergence is material: Hyprland at the pinned commit does **not** enforce the `wl_pointer.set_cursor` serial rule that the protocol states (F1). Any cursor claim that relies on serial gating is rejected.
- `hyprctl cursorpos`, the natural probe for "where is the pointer", is **not** on the SKILL read-verb whitelist (F2).
- `libinput debug-events` output reflects libinput built-in defaults, not the desktop configuration, so its deltas cannot be compared with what a client receives (F3).
- Residual risk: no delivery, rendering or app-response behavior was exercised; see §7.

## 2. Layer ladder (what each observation can and cannot prove)

| Layer | Observation route | Establishes | Does not establish | Status this round |
|---|---|---|---|---|
| L0 kernel evdev | `libinput record`, `/dev/input/event*` | raw device events (root, device access) | anything about the desktop | out of scope — UNK, never run |
| L1 libinput | `libinput debug-events` (S007) | libinput's event stream under built-in defaults | desktop accel/scroll config; compositor delivery | `[INF-docs]` only; not run |
| L2 compositor state | `hyprctl devices` (whitelisted); `hyprctl cursorpos` (**not whitelisted**, F2) | compositor-visible devices; logical global pointer position if read | delivery to a client; rendered image | UNK; no read issued |
| L3 protocol semantics | wayland.xml `wl_pointer`, `wl_seat`, `cursor-shape-v1` | what a conforming compositor must send/accept | host behavior | `[INF-docs]`, exact anchors §5 |
| L4 host implementation | Hyprland source at pinned commit `efb50993…` | what this build's code does (static) | runtime behavior; Arch package patch state (unverified) | `[INF-src]`, §4 |
| L5 rendered image | pixel/screenshot evidence | what is on screen | — | UNK; no screenshot admitted this round |
| L6 app response | client-specific observation | application reaction | anything about L3–L5 | UNK; no admitted route |

## 3. Acceptance conditions (a U6 pointer statement is accepted only if all hold)

- **A1 Protocol text.** Cites the installed/tagged XML by its anchor: sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`, `wayland` 1.26.0-1, `protocol/wayland.xml` at tag `1.26.0`, lines `wl_pointer` 2138; `set_cursor` 2154–2195; `enter` 2197–2210; `leave` 2212–2222; `motion` 2224–2233; `button` 2244–2265; `frame` 2313–2350; `wl_seat.capabilities` 2030–2059. Label `[INF-docs]`.
- **A2 Host code.** Cites Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f` file:line (§4), labels it `[INF-src]`, and states "static source at the commit reported by `hyprctl version`; not binary equivalence; Arch package patch state unverified."
- **A3 Serial claims.** Any sentence on `set_cursor` serial behavior states the protocol rule AND that Hyprland at that commit does not enforce it (F1). A host-level claim of "stale serial ignored" is rejected.
- **A4 Delivery.** Host delivery is stated only as "UNK; not exercised" with the protocol statement as the documented expectation, e.g. "the protocol defines enter/motion/button/frame to the focused client; host delivery to a client was not observed."
- **A5 libinput.** Names the tool version separately from the library: `libinput-tools 1.32.0-1` (binary `/usr/bin/libinput`, per `pacman -Ql libinput-tools`) and `libinput 1.31.3-1` (library, per `pacman -Q libinput`). States debug-events uses built-in defaults (doc quote §6, row S007).
- **A6 Rendered cursor.** Rendered-image statements are UNK unless backed by L5 evidence. Visibility *policy* may be cited only as a dated, labelled host point sample (§6, row R4) and must not be read as delivery or rendering proof.
- **A7 Coordinates.** Each coordinate space is named: libinput deltas (unaccelerated/accelerated per device), `wl_pointer` surface-local fixed-point, Hyprland global layout coordinates. No numeric equality across them.
- **A8 Revision.** Any citation of `wayland/wayland` names the tag or commit. Host-installed XML and upstream `main` are different revisions (§5) and must not be conflated.
- **A9 Source admission.** A claim cites only a row whose SOURCES status is `mined`. S007 is `queued` (`corpus/SOURCES.md:19`); S052 (reserved in the round-15 spec) has no row (0 hits for S051/S052 in `corpus/SOURCES.md`). Until L1 mines them, no U6 statement is admitted.

## 4. Adversarial findings (ordered by severity)

**F1 — MAJOR. Host does not enforce the set_cursor serial rule.**
- Protocol: `set_cursor` "The serial parameter must match the latest wl_pointer.enter serial number sent to the client. Otherwise the request will be ignored." (`/usr/share/wayland/wayland.xml:2186-2188`, identical to tag 1.26.0.)
- Host at `efb50993780079460b0cbed1363e2166a2de1d9f`: `src/managers/SeatManager.cpp:616-629` `CSeatManager::onSetCursor` checks only that the pointer focus client matches (`:617-620`); the serial validation is **commented out** with a `TODO: fix this` (`:622-626`); the event is then emitted (`:628`).
- Handler: `src/protocols/core/Seat.cpp:119-137` forwards `serial` into `onSetCursor` without a local check.
- Consequence: an acceptance or rejection that depends on stale-serial rejection is a false claim for this host. Focus gating is enforced (`:617-620`); serial gating is not.
- Note: `wl_pointer.enter` serials are generated at `Seat.cpp:182` (`nextSerial(..., true)`); the serial value exists, the check does not.

**F2 — MAJOR (fence). `hyprctl cursorpos` is outside the admitted read whitelist.**
- `hyprctl --help` lists `cursorpos → Gets the current cursor position in global layout coordinates`.
- `SKILL.md:221-222` read-verb whitelist: `getoption, monitors, workspaces, activeworkspace, clients, binds, animations, devices, instances, layers, configerrors, version`. `cursorpos` is absent. The round-12 unmentioned-verb sweep (`.ufo/evidence/round-12/l2-scout.md:14-15`) also listed `cursorpos` as unmentioned.
- Consequence: any U6 use of `cursorpos` is rejected until L1 amends the whitelist. Even if amended, it is L2 state only (see R2).

**F3 — MODERATE. libinput debug-events is not the desktop's view.**
- S007 (`https://wayland.freedesktop.org/libinput/doc/latest/tools.html`, libinput 1.32.0 docs, opened by the lane 2026-10-19): list-devices note: "This tool does **not** show your desktop's configuration, just the libinput built-in defaults." debug-events: "To reproduce the event sequence as your desktop session sees it, ensure that all options are turned on or off as required."
- The debug-events tool requires root for `/dev/input/event*` (doc: "Most of the tools must be run as root").
- Version split: installed `libinput-tools 1.32.0-1` vs `libinput 1.31.3-1`; the Hyprland link-time libinput version is unverified.
- Consequence: debug-events deltas are not comparable with `wl_pointer` coordinates or with rendered motion (A7).

**F4 — MODERATE. Frame grouping is a client obligation, and host ordering is only statically read.**
- Protocol `frame` (`wayland.xml:2313-2333`): "A client is expected to accumulate the data in all events within the frame before proceeding."
- Host: `src/protocols/core/Seat.cpp:260-267` `CWLPointerResource::sendFrame`; focus change sends enter, then `sendPointerFrame(...)` (`src/managers/SeatManager.cpp:325-349`). Motion/button frame emission not traced in this review.
- Consequence: a sequence-ordering claim (enter → motion → button → frame) must cite both, and remains `[INF-src]` for the host.

**F5 — MINOR. Cursor-shape path ignores its serial argument in the traced code.**
- Installed `/usr/share/wayland-protocols/staging/cursor-shape/cursor-shape-v1.xml` (sha256 `bb57d91e53a79dadab7c612dab87c233393cee73673feefa7442cfbfdd9aed2f`, `wayland-protocols` 1.49-1) `set_shape` at line 137: "The cursor actually changes only if the input device focus is one of the requesting client's surfaces."
- Host `src/protocols/CursorShape.cpp:43-54` `onSetShape(pMgr, serial, shape)`: the shown body validates the enum and emits `setShape`; `serial` is not referenced in lines 43–54.
- Consequence: any app-set shape claim is UNK for serial semantics; the full cursor-shape `set_shape` serial text was read only through line 151 and needs its own row before admission.

**F6 — MINOR. Undefined image on enter; default cursor path untraced.**
- Protocol `enter`: "the pointer image is undefined and a client should respond to this event by setting an appropriate pointer image with the set_cursor request" (`wayland.xml:2202-2204`).
- Host: `setCursorSurface` routing `src/pointer/cursor/CursorManager.cpp:140-146` (null surface → `resetCursorImage`); `src/pointer/PointerManager.cpp:156` `setCursorSurface`; the compositor-default cursor selection path was not traced.
- Consequence: "no client cursor → Hyprland shows X" is rejected (R4).

**F7 — MINOR. Config-option semantics only from a search snippet.**
- Hyprland wiki config-options page (`https://wiki.hypr.land/configuring/core/config-options/`, page metadata `modified_time 2026-10-19T15:34:09+00:00`) was retrieved as raw HTML and the cursor section was not reached; the option descriptions (`no_hardware_cursors`, `inactive_timeout`, `hide_on_key_press`) come from a search-result snippet of that page. Treat as `[INF-docs-snippet]` until re-opened.
- Source key present in fetched host code: `cursor:use_cpu_buffer` (`src/pointer/PointerManager.cpp:443-445`). `no_hardware_cursors` was not located in the fetched files.

**F8 — INFO. Upstream `main` and installed bytes differ.**
- Round-13 record (`.ufo/waves/round-13/w1/GlobalDocs.md`): upstream `main` `protocol/wayland.xml` sha256 `4831fd1c…` at `93c04ad`. Installed and tag-1.26.0 bytes are `cc860987…` (verified this round by download; identical). Do not cite `4831fd1c…` as the host's protocol text.

## 5. Revision anchors (exact)

| Object | Revision | sha256 / identity | Verified this round |
|---|---|---|---|
| `/usr/share/wayland/wayland.xml` (`wayland` 1.26.0-1) | tag `1.26.0` | `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`, 3442 lines | yes: curl of `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml` hashed identical to installed file |
| upstream `protocol/wayland.xml` `main` | `93c04ad` (round-13 record) | `4831fd1c…` | not re-fetched; prior record only |
| `cursor-shape-v1.xml` (`wayland-protocols` 1.49-1) | installed file | `bb57d91e…` | hash and `set_shape` lines read; upstream tag not compared |
| Hyprland | `efb50993780079460b0cbed1363e2166a2de1d9f` (= `hyprctl version` commit; tag v0.56.2) | GitHub tree `recursive=1`, 1181 entries, not truncated | yes (source files below) |
| libinput docs | `libinput 1.32.0` latest page | S007 (queued) | read this round, not mined |

Host source file hashes at the pinned commit (curl, this round): `src/protocols/core/Seat.cpp` `cc23bb8b…`; `src/managers/SeatManager.cpp` `bd748553…`; `src/protocols/CursorShape.cpp` `d3a1bcb6…`; `src/pointer/cursor/CursorManager.cpp` `255ef12e…`; `src/pointer/PointerManager.cpp` `83c69d93…`.

## 6. Other exact pointers

- Host point samples (dated 2026-10-14, not re-measured): `corpus/knowledge/hyprctl-verification-layer.md:112-113` (`cursor:hide_on_key_press` = 1; `cursor:warp_on_change_workspace` = 1); `corpus/knowledge/idle-lock-plane.md:226-228` (`cursor:inactive_timeout` = 0.0; `cursor:hide_on_key_press` = 1; `cursor:invisible` = 0), with `:236-239` the cursor-never-hides-by-inactivity note. These describe visibility policy, not delivery or rendering.
- Lane rules: `SKILL.md:222` (read whitelist; `setcursor`, `dispatch`, `keyword`, `reload`, `setprop`, `output`, `notify`, `plugin`, `batch` forbidden); `SKILL.md` read-only boundary forbids `hyprctl setcursor`, which changes cursor theme and reloads the cursor manager (`hyprctl --help`).
- Protocol mismatch on set_cursor enforcement: `/usr/share/wayland/wayland.xml:2161-2188` vs `SeatManager.cpp:622-626`.
- Privacy: `libinput record` obscures key codes only (doc: "any alphanumeric key shows up as letter 'a'"); the doc names no pointer-trajectory obscuring. Pointer trajectories from any recording are personal-activity data; no recording is admitted.

## 7. Rejection conditions (reject the statement if any holds)

- **R1** "libinput debug-events showed motion, therefore the application moved/received it." Flip: client-side wl_pointer capture on this host under separate authorization (outside this round).
- **R2** "`hyprctl cursorpos` changed, therefore the rendered cursor is at X." Flip: L5 pixel evidence.
- **R3** "Hyprland ignored a stale `set_cursor`." Flip: client-side observation of the request and its effect; source shows no serial check (F1).
- **R4** "With no client cursor set, Hyprland displays theme cursor X." Flip: traced default-cursor path plus L5 evidence.
- **R5** Any `hyprctl cursorpos` evidence before L1 amends SKILL.md:222.
- **R6** Citing upstream `main` sha `4831fd1c…` as the host protocol text. Flip: host bytes equal that hash.
- **R7** Using libinput "latest" (1.32.0) docs to describe the installed 1.31.3 library's behavior, or the Hyprland-linked library.
- **R8** Citing S007 or any unmined row as admission support. Flip: L1 mines the row with an opened, cited anchor.
- **R9** Any statement that a cursor, shape, or pointer change is "working" from configuration, package presence, or a registry advertisement alone (the round-13/14 advertisement-is-not-behavior rule).
- **R10** Persisting pointer trajectories, `libinput record` output, or `hyprctl devices` device names unprojected. Flip: shape-only projection per SKILL safety rule 4.

## 8. Residual risk and verification gaps

- Not exercised: delivery to any client, rendered cursor image, cursor-theme state, app response, IME/keyboard interaction (covered by the keyboard review).
- Not located: `no_hardware_cursors` and `inactive_timeout` source keys in fetched Hyprland files; the wiki cursor section was not opened (F7).
- Not traced: Hyprland's default cursor selection, motion/button frame emission, and whether Arch's `hyprland` 0.56.2-2 package carries patches beyond `efb5099` (only the `hyprctl version` commit tie was observed).
- Not compared: upstream `wayland.xml` `main` at `93c04ad` against the tag, and the full cursor-shape `set_shape` serial text beyond line 151.
- Not reconciled: libinput 1.31.3 library vs 1.32.0 tool and docs.
- Next checks for L1 (not run here): mine S052 at tag `1.26.0` with the anchors in §3-A1; add a row for Hyprland efb5099 `Seat.cpp`/`SeatManager.cpp`/`CursorShape.cpp` as `[INF-src]` with the F1 divergence stated; decide whether `cursorpos` joins the whitelist (SKILL.md:222); re-open the wiki cursor section before admitting option semantics.

## 9. Sources used (absolute paths or URLs)

- `/usr/share/wayland/wayland.xml` (sha `cc860987…`), lines 2004–2059, 2138–2350.
- `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml` (same sha).
- `/usr/share/wayland-protocols/staging/cursor-shape/cursor-shape-v1.xml` (sha `bb57d91e…`), lines 43–54, 137–150.
- `https://wayland.freedesktop.org/libinput/doc/latest/tools.html` (S007).
- `https://github.com/hyprwm/Hyprland` tree at `efb50993780079460b0cbed1363e2166a2de1d9f`: `src/protocols/core/Seat.cpp`, `src/managers/SeatManager.cpp`, `src/protocols/CursorShape.cpp`, `src/pointer/cursor/CursorManager.cpp`, `src/pointer/PointerManager.cpp` (raw.githubusercontent.com, read-only).
- `https://wiki.hypr.land/configuring/core/config-options/` (search snippet only; F7).
- Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin/SKILL.md:221-222`; `corpus/SOURCES.md:19`; `corpus/knowledge/hyprctl-verification-layer.md:112-113`; `corpus/knowledge/idle-lock-plane.md:226-239`; `.ufo/waves/round-15/w1/spec.json` (S051/S052 reservation, ReviewPointer item); `.ufo/waves/round-15/w1/dispatch.json` (ReviewPointer entry).
- Local commands (read-only): `pacman -Q`/`pacman -Ql`, `hyprctl --help`, `hyprctl version`, `sha256sum`, `grep`/`sed` on the files above.
