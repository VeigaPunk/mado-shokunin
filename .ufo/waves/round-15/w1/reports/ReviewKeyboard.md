# ReviewKeyboard — U6 integration risk: Wayland key events/focus vs text-input/IME/application interpretation

Round 15 w1, reviewer seat `MadoR15.ReviewKeyboard`. Read-only review: local static XML, lane artifacts, `pacman -Q`, no input capture, no injection, no live probe, no build/test. Tools installed or upgraded by this seat: none.

Labels: `[OBS]` host or lane artifact fact; `[INF-docs]` upstream primary text read locally; `[INF]` inference; `[UNK]` not established by any retained evidence.

## Verdict

**Conditional accept, bounded to documentation.** A U6 note may describe the keyboard path as an upstream-documented layer ladder (keymap → keyboard focus → text-input focus → IME → application). It must not claim host delivery, text insertion, IME activity, or app-side interpretation. Any sentence that equates "key event reached the compositor/kernel" with "application received or interpreted the text" is rejected. Coverage credit for the keyboard piece depends on the `## Unexercised delivery` section keeping text-input, IME, application interpretation, and shortcut consumption as `[UNK]`.

## Layer ladder (what each layer can and cannot support)

| # | Layer | Authority in hand | Supports | Does not support |
|---|---|---|---|---|
| L1 | Compositor keymap and input config | `[OBS]` `hyprctl -j devices` keyboards report `active_keymap: Portuguese (Brazil)`, layout `br` (`corpus/knowledge/config-health-report-r3.md:157-158,732,932`; `corpus/knowledge/hyprctl-verification-layer.md:159`). `[OBS]` `input:kb_layout=br`, `kb_options=compose:caps`, `repeat_rate=40`, `repeat_delay=250` (`hyprctl-verification-layer.md:120-123,132-133`). | Compositor-side configuration and what Hyprland reports about its own keyboards | What the client's xkb state is; what a client receives on the wire |
| L2 | Seat and keyboard focus | `[INF-docs]` `/usr/share/wayland/wayland.xml` (sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`): `wl_keyboard` v11 at `:2573`; `keymap` `:2600`; `enter` `:2614`; `leave` `:2635`; `key` `:2669`; `modifiers` `:2701`; `repeat_info` `:2732` (since 4). `[OBS]` `wl_seat` advertised at **v9** (`.ufo/waves/round-13/w1/globals.json` `globals[]`). | Keyboard focus is a per-surface enter/leave pair. `key` carries a raw keycode; xkb keycode = keycode + 8 (`keymap_format` enum, xkb_v1). Key repeat is signalled via `repeat_info`. | That a seat has keyboard capability (see F5). That a keypress is "typed text." |
| L3 | Text-input focus and IME | `[INF-docs]` `text-input-unstable-v3.xml` (installed, sha256 `160815cd…`): `zwp_text_input_v3` `:50`, manager `:585`; `enter` `:333`, `leave` `:347`, `preedit_string` `:364`, `commit_string` `:390`, `done` `:425`. Version-gated (since 2): `action` `:477`, `language` `:490`, `set_available_actions` `:502`, `show_input_panel` `:518`, `hide_input_panel` `:528`, `preedit_hint` `:555`. `[OBS]` `zwp_text_input_manager_v3` advertised **v1** (globals.json); `zwp_text_input_manager_v1` v1; `zwp_input_method_manager_v2` v1 (globals.json); `[OBS]` GlobalCapture row 28 marks it "outside" wayland-protocols (`.ufo/waves/round-13/w1/GlobalCapture.md:146`). | Text-input focus is a separate event stream that "follows the keyboard focus" only when the seat has keyboard capability (`text-input-unstable-v3.xml:333-347`). The client must send `enable`/`disable` and `commit`. | Whether any client has enabled text input; whether an IME is running; any preedit/commit behaviour on this host. |
| L4 | Application interpretation | none | Nothing | Everything: toolkit xkb use, compose/dead keys, text insertion, shortcut handling, per-app behaviour. All `[UNK]`. |

Kernel/libinput (`/dev/input/event*`, `debug-events`, `record`, `replay`) is not part of this ladder. It is outside the input-debugging scope set in `spec.json`, and it cannot bridge L1–L4 on its own (see F9).

## Findings (severity order)

**F1 — HIGH. Raw key event is not text.** `wl_keyboard.key` carries a platform keycode with no keysym or character (`wayland.xml:2669`; `keymap_format` `xkb_v1` requires client-side xkb and a +8 offset). Text comes from client xkb state plus, for IME/composed input, text-input `commit_string`/`preedit_string`. A U6 note that maps a captured keycode or a `debug-events` line to a character is a rejected inference.
- Accept if: the note states the raw-keycode boundary with the `wayland.xml:2669` cite and says no character or keysym is established.
- Reject if: any sentence maps keycodes to typed characters or to a specific app's text.

**F2 — HIGH. Keyboard focus ≠ text-input focus.** Two separate enter/leave streams exist: `wl_keyboard.enter/leave` (`wayland.xml:2614,2635`) and `zwp_text_input_v3.enter/leave` (`text-input-unstable-v3.xml:333,347`). Text-input enable/disable is client-driven and the two requests "are not expected to be paired" (`text-input-unstable-v3.xml`, `zwp_text_input_v3` description, lines ~50-70). Hyprland focus policy moves the keyboard target without any text-input state: `misc:focus_on_activate`, `input:follow_mouse=1` (`hyprctl-verification-layer.md:107,125`), `no_focus on` (`keybind-rule-semantics.md:189`), `no_follow_mouse` on jetbrains (`keybind-rule-semantics.md:232`), walker `force_keyboard_focus=true` (`walker-deep.md:124`; `waybar-walker-semantics.md:242`).
- Accept if: the note treats keyboard focus and text-input focus as independent layers and cites the focus-policy rows only as compositor-side causes of keyboard target.
- Reject if: "focused window" is used as a proxy for "IME active" or "text accepted."

**F3 — HIGH. IME route is not established on the host.** Advertised: `zwp_input_method_manager_v2` (v1) and `zwp_text_input_manager_v3` (v1) (`globals.json`). The input-method-v2 authority is not in the local `wayland-protocols` tree; the only local input-method file is `unstable/input-method/input-method-unstable-v1.xml` (`zwp_input_method_v1` `:243`). GlobalCapture marks v2 "outside" (`GlobalCapture.md:146`). `fcitx5` 5.1.22-1 is installed (`pacman -Q`). An r3 snapshot recorded fcitx5 PID 1709 running (`config-health-report-r3.md:413-416`); this review did not re-check that state. Current fcitx5 status: `[UNK]`.
- Accept if: any IME statement is `[UNK]` unless the owning-repository row (wlroots or Hyprland source for input-method-v2) is admitted at a pinned revision and the current runtime state is read.
- Reject if: the note names fcitx5 or IME as "handling input" for any app on the current host.

**F4 — MEDIUM. Advertised versions cap the object versions the client can use.** `wl_seat` is advertised at v9 while the installed XML defines v11 (`wayland.xml:2004`). `wl_keyboard` v10 introduces the `repeated` key state (`key_state` enum, `repeated` since 10, just before the `key` event at `:2669`). Under this host's advertised seat version, the client should not be assumed to receive `repeated`. Text-input manager advertised v1, while `zwp_text_input_v3` defines v2 features (`action`, `language`, `preedit_hint`, `set_available_actions`, `show/hide_input_panel`; all since 2). These features should be treated as not available through the advertised v1 manager.
- `[INF]` the object version inherits the bound parent's version (libwayland/scanner convention). This is not stated in the XML text read here and needs a libwayland source row before being cited as fact.
- Accept if: any version-dependent statement cites the advertised version from `globals.json` and not the XML's latest version.
- Reject if: the note lists v2 text-input events or v10 `repeated` as available on this host.

**F5 — MEDIUM. Seat capability is unobserved.** `globals.json` `excluded[]` removes "`wl_seat` human-readable name and capability list". The retained capture therefore does not show whether a keyboard capability is advertised to clients. Hyprland's `hyprctl devices` (compositor view) is not a `wl_seat.capabilities` observation. The `get_keyboard` request is documented as valid only when the seat has, or has had, the keyboard capability (`wayland.xml`, `get_keyboard` in `wl_seat`, after `:2004`).
- Accept if: any "clients receive keys" statement is `[UNK]` on the wl_seat side and is backed by the compositor-side L1 observation only as context.
- Reject if: the note cites `hyprctl devices` as evidence of `wl_seat` keyboard capability.

**F6 — MEDIUM. Keymap authority and staleness.** The client's keymap comes from the `wl_keyboard.keymap` fd (`wayland.xml:2600`), not from `hyprctl`. `active_keymap` (`hyprctl`) is the compositor's view. Client-side xkb overrides are `[UNK]`. The lock path runs `hyprctl switchxkblayout all 0` (`corpus/knowledge/idle-lock-plane.md:188,205`), so the layout can change mid-session. A keymap read taken earlier is stale after a layout switch.
- Accept if: the note says "keymap as sent at the last `keymap` event" and records the reading time, and it does not generalise to later state.
- Reject if: the note says "the keymap apps use is br" from `hyprctl` alone.

**F7 — MEDIUM. Compositor-side consumption and inhibition can remove or redirect keys before the client.** Hyprland's 192 binds (`hyprctl-verification-layer.md:157`) and `sendshortcut` dispatchers (`keybind-rule-semantics.md:152`) act in the compositor. `zwp_keyboard_shortcuts_inhibit_manager_v1` (v1) and `hyprland_global_shortcuts_manager_v1` (v1) are advertised (`globals.json`). Whether a bound key reaches `wl_keyboard.key` depends on Hyprland source behaviour, not in the corpus: `[UNK]`.
- Accept if: any "key delivered" claim is limited to "not known to be consumed by a bind or inhibited" with `[UNK]` on the consumption side.
- Reject if: the note says a bound key does or does not reach the client without a Hyprland source row.

**F8 — MEDIUM. Injection-capable globals are advertised, so keys need not originate from hardware.** Advertised: `zwp_virtual_keyboard_manager_v1` (v1), `zwlr_virtual_pointer_manager_v1` (v2), `hyprland_input_capture_manager_v1` (v1), `wp_security_context_manager_v1` (v1) (`globals.json`). A keyboard node named `hl-virtual-keyboard-fcitx5` appeared in the r3 device census (`config-health-report-r3.md:413`), which suggests a virtual keyboard created on behalf of fcitx5. That naming is `[INF]`; the mechanism is not verified against source.
- Accept if: the note says the ladder can start at a compositor-created virtual keyboard as well as hardware, and does not assume `/dev/input` origin.
- Reject if: any sentence says "all key events originate in the kernel input layer." Reject any injection, capture or replay step: the spec forbids them and the advertisement is not a delivery observation.

**F9 — LOW. libinput version drift between docs and host.** S007 is pinned to the "libinput 1.32.0 documentation" (`corpus/SOURCES.md:19`). The installed package is `libinput 1.31.3-1` (`pacman -Q`, this review). Tool flags and output may differ. Also, the round-12 lesson M04 says `libinput list-devices` "proves the compositor-applied keyboard/touchpad settings" (`corpus/lessons/round-12.md:37`). The tool's own scope is libinput built-in defaults, so M04 is not a basis for a keyboard claim. The U6 note must not reuse M04.
- Accept if: S051 records the version gap and the note cites the tool's stated scope.
- Reject if: any U6 sentence reuses M04's "proves compositor-applied" wording.

**F10 — LOW. Source pinning.** `S052` is reserved for "Wayland core wl_keyboard/wl_pointer XML (exact revision needed)" (`.ufo/waves/round-15/spec.json`). The reserved scope does not cover text-input v3, which the keyboard/IME rows need. No `S053` is reserved. Installed file sha256 values for `text-input-unstable-v3.xml` (`160815cd…`) and `text-input-unstable-v1.xml` (`a3671b8e…`) are recorded here, but no upstream commit for either is pinned. The `wayland.xml` sha (`cc860987…`) differs from the upstream `93c04ad` digest (`4831fd1c…`) cited for S043 (`.ufo/waves/round-13/w1/GlobalDocs.md`), so the installed-file digest must be the anchor, with the revision stated separately.
- Accept if: S052 pins the installed `wayland.xml` sha256 `cc860987…` (package `wayland 1.26.0-1`) and the upstream commit, and a text-input row (S053, to be allocated by L1) pins the installed `text-input-unstable-v3.xml` sha `160815cd…` (package `wayland-protocols 1.49-1`) with the upstream revision.
- Reject if: text-input or IME claims cite S052 or an unpinned web page.

## Acceptance conditions (combined)

1. Every layer row carries exactly one label from `[OBS]`, `[INF-docs]`, `[UNK]`, with cite and sha.
2. The raw-keycode boundary (F1) and the keyboard/text-input focus separation (F2) appear in the note body.
3. IME (F3) and application interpretation (L4) are `[UNK]` in `## Unexercised delivery`.
4. Version claims cite the advertised values from `globals.json` (F4), not XML latest.
5. Seat capability (F5) and shortcut consumption (F7) are `[UNK]` unless a source row closes them.
6. S052 and S053 (text-input) are pinned to installed sha plus upstream revision before the note cites them as `mined` (F10).
7. No claim relies on fcitx5 running now (F3) or on libinput M04 wording (F9).

## Rejection conditions (any one rejects the U6 keyboard/text sub-claim)

- Keycode-to-character or keysym-to-app mapping (F1).
- "Focused" used to mean "text-input active" or "IME handles input" (F2, F3).
- IME or fcitx5 described as active on the current host without a current read (F3).
- Text-input v2 events or wl_keyboard v10 `repeated` described as available on this host (F4).
- `hyprctl` cited as a `wl_seat` capability observation (F5).
- Bound-key delivery asserted without a Hyprland source row (F7).
- "All keys originate in the kernel input layer" (F8).
- Any input capture, injection, replay, or `debug-events` step (spec exclusion; no evidence supports it).

## Exact evidence pointers

- `/usr/share/wayland/wayland.xml` — `wl_keyboard` `:2573`, `keymap` `:2600`, `enter` `:2614`, `leave` `:2635`, `key` `:2669`, `modifiers` `:2701`, `repeat_info` `:2732`; `wl_seat` `:2004` (v11); `wl_registry.bind` `:141`; `get_keyboard` in `wl_seat` (missing_capability rule) after `:2004`.
- `/usr/share/wayland-protocols/unstable/text-input/text-input-unstable-v3.xml` — `zwp_text_input_v3` `:50`, manager `:585`, `enter` `:333`, `leave` `:347`, `preedit_string` `:364`, `commit_string` `:390`, `done` `:425`, since-2 items `:477,490,502,518,528,555`.
- `/usr/share/wayland-protocols/unstable/text-input/text-input-unstable-v1.xml` — manager `:372`.
- `/usr/share/wayland-protocols/unstable/input-method/input-method-unstable-v1.xml` — `zwp_input_method_v1` `:243` (v1 only; no v2 locally).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/globals.json` — `globals[]` (`wl_seat` v9; `zwp_text_input_manager_v3` v1; `zwp_input_method_manager_v2` v1; `zwp_keyboard_shortcuts_inhibit_manager_v1` v1; `zwp_virtual_keyboard_manager_v1` v1; `zwlr_virtual_pointer_manager_v1` v2; `hyprland_input_capture_manager_v1` v1; `hyprland_global_shortcuts_manager_v1` v1); `excluded[]` (seat capability list).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/GlobalCapture.md` — `:138-139` (text-input), `:146` (input-method v2 "outside"), `:213` (text-input v3 1 vs 2).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/config-health-report-r3.md` — `:157-158,413-416,732,932` (keyboard census, `hl-virtual-keyboard-fcitx5`, fcitx5 PID 1709, r3 snapshot).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/hyprctl-verification-layer.md` — `:107,120-123,125,132-133,157,159`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/idle-lock-plane.md` — `:188,205` (`switchxkblayout all 0`).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/keybind-rule-semantics.md` — `:152` (`sendshortcut`), `:189` (`no_focus`), `:232` (`no_follow_mouse`).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/walker-deep.md:124`; `waybar-walker-semantics.md:242` (`force_keyboard_focus`).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` — `:19` (S007, libinput 1.32.0), `:62` (S050 last row; S051/S052 unallocated).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md:37` (M04 overreach).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-14-verifier-spotcheck.md:169` (R14-V1; out of this seat's scope, cited for the ancillary route only).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/spec.json` — U6 milestone; S051/S052 reservation.

## Residual risk and verification gaps

- No live state was read for fcitx5, the current seat capability list, active text-input objects, or bind consumption. All are `[UNK]`.
- Object-version inheritance (F4) and the Hyprland virtual-keyboard naming (F8) are `[INF]` until a libwayland or Hyprland source row is admitted.
- The local `wayland.xml` and text-input XML digests are recorded, but neither file has a pinned upstream commit in the registry yet (F10).
- Application-side xkb and text behaviour (L4) is unobserved; any app-specific claim is out of scope for this host.

## Tool and channel record

No installs or upgrades. Read-only commands used: `pacman -Q` (versions), `sha256sum` and `grep`/`sed` over local static XML and lane artifacts.
