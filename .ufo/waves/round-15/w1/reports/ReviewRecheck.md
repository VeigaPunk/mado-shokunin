# ReviewRecheck — U6 safe metadata/doc recheck vs event capture (round 15, w1)

Seat: MadoR15.ReviewRecheck (reviewer, leaf). Scope: adversarial review of the U6 integration risk "safe metadata/doc recheck avoiding event capture". Read-only: static fetches of pinned primary docs/source, `git ls-remote` tag reads, installed-file hashes. No device, compositor or input probe; no event tool run; no sudo; no tool installed or upgraded. Lane tooling rules read at `/home/vgpnk/.omp/agent/RULES.md`. Scratch bytes: `/tmp/mado-r15-reviewrecheck/` (provenance only, QUALITY 13).

## Verdict

**Conditional.** The U6 documentation route may be accepted only as a documented, unexercised boundary. Accept the recheck only if it uses the allowed routes below and carries the corrections in F1–F2. Reject any "metadata-only" recheck that runs a device-level libinput tool, a protocol dumper, `WAYLAND_DEBUG`, or `wayland-info` without disclosing the keyboard object it creates.

## Findings (severity order)

**F1 — HIGH. The U4 request inventory omits a keyboard object; U6 cannot call the wayland-info recheck input-free.**
- `wayland-info-1.3.0.c` (sha256 `fcdc6c09d8111c8bcec407299be9ef582105c8ff954ebf9b57fa25b5e86c46a6`, tag 1.3.0 peel `d01edd68961ca01779dcb96afe56c2d99ff79067` via `git ls-remote`, matching S046):
  - `:822-826` returns early if `seat->global.version < 4`.
  - `:828-833` on `WL_SEAT_CAPABILITY_KEYBOARD` calls `wl_seat_get_keyboard` (`:829`) and `wl_keyboard_add_listener` (`:830`).
  - `:1822-1824` binds `wl_seat` at `min(version,4)`.
- S046's detail-call anchors (`:1775, :2031, :2626, :2744, :2750`) match the raw file exactly. The seat keyboard request at `:829` is absent from S046 and from `corpus/knowledge/wayland-protocol-boundaries-r13.md:43` and `output-colour-boundaries-r14.md:87`.
- Required: an append-only erratum to the U4 note, listing `:822-833` and the `wl_keyboard` listener. Until then, the U6 note must not describe wayland-info as advertisement-only or as making zero input-object requests. The seat version on this host is `[UNK]` (not measured here).

**F2 — HIGH. "No focus, no input" is wrong for the protocol; the observer's handlers are the only reason it records nothing.**
- `wayland-info-1.3.0.c:759-765` closes the keymap fd unread. `:767-803`: `enter`, `leave`, `key` and `modifiers` handlers have empty bodies. `repeat_info` stores two integers.
- `/usr/share/wayland/wayland.xml` (sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`, matches S043 pin) at `:2706-2712` says the compositor "may send this event without a surface of the client having keyboard focus" (modifier state).
- Accept: "the diagnostic creates a `wl_keyboard` object and its handlers discard keymap, enter/leave, key and modifier events; the protocol permits modifier events without focus." Reject: "receives no input events."
- Whether `wl_keyboard.key` can reach a surface-less client is `[UNK]`; the `:2669-2699` text was not read in full here. Do not assert it either way.

**F3 — HIGH. The libinput tools that capture or inject events are banned routes.**
Primary doc: `https://wayland.freedesktop.org/libinput/doc/latest/tools.html`, libinput 1.32.0, rendered-page sha256 `524c177681d1eb0be28424e54d1c346c6de993e1b9c4e98c8ec409a849d6872f` (fetched 2026-10-20). Quoted sections:
- "Most of the tools must be run as root to have access to the kernel's `/dev/input/event*` device files."
- `debug-events` "prints events from devices"; `debug-gui` shows "touch events, pointer motion, scroll axes and gestures" live.
- `record` "records the **kernel** events from a specific device node"; it obscures alphanumeric key codes to "a" but still captures timing and pointer data.
- `replay` "creates a new virtual device" (input injection).
- `measure`, `analyze` and `record --no-events` also need device nodes; `list-kernel-devices` is kernel inventory, which the round-13/14 lessons assign to the sibling kernel/DRM owner.
- Reject: every device-node subcommand, `sudo` for `/dev/input`, and `replay` in any form.

**F4 — MEDIUM. `libinput list-devices` describes defaults, not the desktop.**
- Doc quote: "This tool does **not** show your desktop's configuration, just the libinput built-in defaults." Also "intended for human-consumption and may change its output at any time."
- Round-12 lesson M04 (`corpus/lessons/round-12.md`, inference-trap table) recorded the error of inferring compositor-applied settings from it.
- Accept only the applied-state route: `hyprctl -j devices` (whitelisted read verb, `SKILL.md` safety rule 1), projected to keyboard count, `active_keymap` and `layout`, as measured in `config-health-report-r3.md:157,412-416,731-732` (F9) and `hyprctl-verification-layer.md:159`. Those are earlier measurements; this seat did not re-run them.

**F5 — MEDIUM. Device identity is not covered by the privacy rules.**
- `SKILL.md` shape-only rules cover window titles, `hyprland.log`, instance signatures and `/proc/*/environ`. They do not cover device names, `address` fields, `/dev/input/eventN` paths or seat names.
- Accept: persist only counts and keymap/layout strings. Reject raw `hyprctl -j devices` or libinput output in any persisted artifact. The R3 pass wrote raw `devices.json` to scratch (`config-health-report-r3.md:731`); that is acceptable only as scratch, not as evidence.
- Recommend the lane (L1) add a device-identity rule to `SKILL.md`. This seat does not edit it.

**F6 — MEDIUM. S007 has no immutable revision anchor.**
- S007 (`corpus/SOURCES.md:19`, status `queued`) cites a `latest` URL with no revision. The anchor rule requires section plus revision (`SOURCES.md` owed-anchor paragraph).
- Pins obtained here: docs page `524c1776…` (above); libinput tag `1.32.0` → `c7e6fe66f509ba2eda680c28aa64795987b49e7c` (`git ls-remote https://gitlab.freedesktop.org/libinput/libinput.git refs/tags/1.32.0`, lightweight).
- Required before U6 cites S007: a superseding row with that tag commit, plus the `doc/` source at that commit read directly. The rst path at the tag was not verified here `[UNK]`. The U6 note must not cite the `latest` page as the sole pin.

**F7 — VERIFIED (no defect). Pinned anchors checked.**
- S043: installed `wayland.xml` hash equals the S043 pin.
- S046: tag `1.3.0` peel and all five detail-call lines match.
- `extras.html` (S042): the page says "`export WAYLAND_DEBUG=1` … is not enough, the following tools may help", and lists dumpers (`wayland-tracker`, `wayland-tracer`, `wlanalyzer`) and middle-man proxies (`wl-proxy`, `wlhax`). Dumpers and proxies capture message traffic, including key events; they are banned.

## Allowed recheck route (acceptance conditions)

1. Static docs and source only: `curl` to a scratch path, `sha256sum`, `git ls-remote` for tags, reading `/usr/share/**` files and installed package metadata (`pacman -Qi`, read-only).
2. Compositor pin: `hyprctl -j version` (whitelisted). Device state: `hyprctl -j devices`, projected to counts, keymap and layout only (F4, F5).
3. Advertisement: reuse the U4 sanitized capture; do not run `wayland-info` again inside U6. A new run requires the F1 caveat and an operator-authorized reason.
4. Every U6 row is classed `[OBS]` (applied-state via hyprctl projection), `[INF-docs]` (libinput/Wayland docs quoted with sha) or `[UNK]` (delivery, IME, focus, kernel). No row claims delivery.
5. `covers: U6` only after S007 is superseded and mined with a reciprocal `used-by` (F6); coverage 6/7 is counted only with that join.

## Rejection conditions

- Any run of `libinput debug-events|debug-gui|record|replay|measure|analyze|list-kernel-devices|quirks` on a device node, with or without `sudo`.
- `WAYLAND_DEBUG`, any dumper or middle-man proxy listed in `extras.html`, or `wlhax`.
- Any compositor-applied claim sourced from `libinput list-devices` (F4).
- Any persisted raw device JSON or device name (F5).
- Any "zero input objects" or "advertisement-only" wording for wayland-info without the F1 erratum.
- Any claim of delivery, IME behaviour, HDR, or kernel causation (unexercised; U6 remains partial on those).

## Residual risk and verification gaps

- No live `hyprctl -j devices` run in this seat; the keymap claim relies on prior measurements (`config-health-report-r3.md:157,731-732`).
- `libinput` is absent per the scout's sweep; this seat did not install it (no help sweep needed, since primary docs were pinned).
- `wl_seat` version on the host is `[UNK]`; whether `:829` runs on this host is unmeasured.
- `wl_keyboard.key` delivery to a surface-less client: `[UNK]`; `wayland.xml:2669-2699` full text unread.
- S007 `doc/` rst at tag `1.32.0`: unread; the rendered page is the only pinned text.

## Installs and tools

None. Used preinstalled `curl` and `git`; no package installed, upgraded or removed.

## Checks the main agent should run (once, after integration)

- `sha256sum /tmp/mado-r15-reviewrecheck/wayland-info-1.3.0.c` → `fcdc6c09…6a6`; `sha256sum /usr/share/wayland/wayland.xml` → `cc860987…5e07`.
- `git ls-remote https://gitlab.freedesktop.org/wayland/wayland-utils.git refs/tags/1.3.0` → peel `d01edd68…067`.
- `git ls-remote https://gitlab.freedesktop.org/libinput/libinput.git refs/tags/1.32.0` → `c7e6fe66…7b49e7c`.
- Re-derive counts from the committed `corpus/SOURCES.md` once S007 is superseded (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`).
