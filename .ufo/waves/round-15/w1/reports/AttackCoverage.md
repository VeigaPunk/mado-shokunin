# AttackCoverage — MadoR15.AttackCoverage (critic, 2026-10-20)

**Target.** C1 coverage moves from U1–U5 (5/7, 7.1429) to U1–U6 (6/7, **8.5714**) through a documentation-only U6 input-debugging layer route.

**Axis.** Coverage only.

**State at review.** `input-draft.txt` and the round-15 `measure.py` had not landed yet. This review therefore attacks the route and the rubric, not the landed text.

## Verdict input

**A documentation-only U6 can legitimately count, but only as a ladder of what each layer and probe can observe. It must never count as delivery.**

- **Definition.** U6 is pre-registered as "kernel-input → Wayland debugging **ladder**" (`SCORECARD.md:248`). Its origin row (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w1/mado-art.md:24`) states the purpose: "Triage must identify which layer a probe can actually observe."
  - A documented route therefore fits the item. U4 and U5 were admitted the same way, as documentation boundaries with `[UNK]` behaviour (`SCORECARD.md:389,513`).
  - The counter is structural. It measures a sourced, reciprocal, faceted entry, not input working on this host.

**The judge should reject the claim if the landed note does any of the following:**

- **R1 — Reports a probe run.** It presents any `libinput debug-events`, `debug-gui`, `record`, `replay`, `list-devices` or `list-kernel-devices` output, or any `WAYLAND_DEBUG` output, as a host observation. Any of these means the round's no-collection contract was broken.
- **R2 — Treats an earlier rung as proof of delivery.** It infers that the app received input from:
  - a kernel or libinput event;
  - `wl_seat` capabilities;
  - `getoption` or `hyprctl devices` output.
- **R3 — Applies newer XML semantics to this host.** It describes `wl_keyboard` key state `repeated` (since v10) or `wl_pointer.warp` (since v11) as host behaviour. See counterexample C2.
- **R4 — Uses a floating source URL.** It uses `libinput/doc/latest/tools.html` as S051's pin.
- **R5 — Duplicates S007.** It adds S051 as a fresh row for the same URL and scope as S007 without `supersedes S007 —`. This repeats the S030/S045 duplicate-admission precedent (`corpus/SOURCES.md:57,114`).

## Strongest counterexamples

### C1 — `debug-events` does not observe the compositor's input context

- **Upstream text.** libinput 1.32.0 `doc/user/tools.rst` at tag `5cf833b572f5a33663888da321dce0ba1abd82a2`, sha256 `53264328…`:
  - `:142`: "To reproduce the event sequence as your desktop session sees it, ensure that all options are turned on or off as required."
  - `:45`: `list-devices` "does **not** show your desktop's configuration, just the libinput built-in defaults."
  - `:220`: `record` captures "**kernel events** and independent of the libinput context."
  - `:276`: `replay` "creates a new virtual device." That is injection into the live seat.
- **Consequence.** Every libinput rung is a separate context, with defaults or options supplied by the operator. None of them observes what the compositor did with the event. Lesson M04 (`corpus/lessons/round-12.md:37`) already covers `list-devices`; `debug-events` belongs to the same class.

### C2 — The pinned XML is newer than what the host advertises

- **Pinned text.**
  - The S052 candidate (wayland tag 1.26.0, commit `87cc8a8728a923fc57938faa81ba0e74f34ecdc7`) is byte-identical to the installed `/usr/share/wayland/wayland.xml` (sha256 `cc860987e54f8d85…`, `wayland 1.26.0-1`).
  - It declares `wl_seat`, `wl_pointer` and `wl_keyboard` at version 11 (`:2004,:2138,:2573`).
- **Sampled host.**
  - The round-13 host sample advertised **`wl_seat` v9** (`.ufo/waves/round-13/w1/GlobalCapture.md:119`).
  - So `repeated` (`:2666`, since 10) and `warp` (`:2552`, since 11) are absent at the sampled version. At v9, key repeat is client-side via `repeat_info`.
- **Consequence.** This is the U4 lesson again: the XML version is not the advertised version. The note must label XML text `[INF-docs]` with its version, and record seat conformance as `[UNK]`.

### C3 — Compositor `getoption` is not the per-window effective input setting

- **Global value.** `input:touchpad:scroll_factor` reads 0.4 globally.
- **Per-window override.** A window rule overrides it to 1.5 for Alacritty, kitty and foot (`corpus/knowledge/keybind-rule-semantics.md:243-244`).
- **Consumed binds.** Binds consume keys by default. Only `non_consuming` passes the event to the active window (wiki.hypr.land Binds, flags list; this is the Lua-era current wiki, so U2 era labelling applies).
- **Consequence.** The compositor rung must contain an explicit "consumed by bind or rule" branch between libinput and `wl_keyboard.key`.

## Must fix

- **K1 — Supersede S007 instead of duplicating it.** S007 is already the libinput `tools.html` row: `queued`, using the floating `latest` URL, opened 2026-10-19 (`corpus/SOURCES.md:19`).
  - S051 must open `teaches` with `supersedes S007 —`.
  - Pin it to libinput tag 1.32.0 commit `5cf833b5…`, `doc/user/tools.rst`, sha256 `53264328…`. Installed `libinput 1.32.0-1` matches.
  - S007 stays queued as historical metadata; S042→S006 is the precedent (`corpus/lessons/round-13.md:36,50`).
- **K2 — Pin S052 and separate it from S043.** S043 already cites `/usr/share/wayland/wayland.xml` for `wl_registry` (`corpus/SOURCES.md:55`).
  - Pin S052 to `raw/1.26.0/protocol/wayland.xml` (commit `87cc8a87…`, sha256 `cc860987…`).
  - Use distinct anchors: `wl_seat.capabilities` `:2004-2058`; `wl_keyboard` keymap, enter and key `:2600-2680`; `wl_pointer` enter, motion, button and frame `:2197-2313`.
  - Record the scope difference from S043 explicitly so the E04/W04 duplicate census does not read it as a duplicate.
- **K3 — Ladder rows must say what each rung does not prove.** The required rows are:
  - kernel node / libinput separate context;
  - compositor policy (getoption is global; per-window rules; bind consumption);
  - `wl_seat` capability, which says only that the seat has one or more keyboards (`:2016`), not delivery;
  - `wl_keyboard.enter`/`key` sent to the focused surface;
  - toolkit, IME and app outcome as `[UNK]`.
- **K4 — Route the compositor rung to existing host evidence.** Point to the existing host notes, `[OBS]` dated 2026-10-14:
  - `hyprctl-verification-layer.md:120-134,159` (`input:*` getoption pairs; `hyprctl -j devices` 8 keyboards with `br` keymap);
  - `keybind-rule-semantics.md:243`.
  - Do not re-run or re-measure them; this round permits no live probes.
- **K5 — Separate replay from read-only inspection in `## Safe boundary`.**
  - `replay` and `record` are injection and capture. They are not authorized, and `record` obscures only alphanumeric keys (`:262`).
  - `list-devices` and `list-kernel-devices` need `/dev/input` access and root ("Most of the tools must be run as root", tools.html §Helper tools). They are not run this round.

## Counter gap (M1, carried from R14)

- **What the counter cannot see.** The required facets are the headings `## Layer ladder`, `## Safe boundary` and `## Unexercised delivery`, `[UNK]` in the last section, and reciprocal mined S051/S052. A note that says "debug-events confirmed keystrokes reach Firefox" still scores 6/7.
- **Hand check to record next to the count:**
  - no R1–R5 condition;
  - S051 supersedes S007 at the pinned tag;
  - S052 version 11 is labelled as text, and host `wl_seat` is v9 or `[UNK]`;
  - the bind-consumption and per-window rungs are present;
  - delivery, IME and kernel stay `[UNK]`.
- **What 8.5714 means.** It is structural current-art ground. It is not input-behaviour coverage, and the U7 Waybar module text stays open.

## Record

- **Static reads:**
  - `pacman -Q`: libinput 1.32.0-1, wayland 1.26.0-1, wayland-protocols 1.49-1, hyprland 0.56.2-2, aquamarine 0.15.0-2, libxkbcommon 1.13.2-1;
  - `sha256sum` on the installed `wayland.xml`;
  - `ls /usr/lib/libinput` (names only).
- **Upstream reads.** Raw files were fetched read-only:
  - libinput `tools.rst` and wayland `wayland.xml`, plus the GitLab tags API for both;
  - wiki.hypr.land Binds;
  - `tools.html` through the reader.
- **Failed lookup.** The Hyprland `ProtocolManager.cpp` path returned 404 at v0.56.2, so no compositor-side seat version is claimed. The host v9 comes from the round-13 capture only.
- **Not done.** No input tool, `hyprctl`, compositor, client or device read. No jj or git commands, no tests.
- **Cleanup.** The `/tmp/ac15` scratch was removed (`absent`).
- **Installs.** None.
