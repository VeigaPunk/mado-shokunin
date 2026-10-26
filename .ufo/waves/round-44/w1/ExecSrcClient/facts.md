# ExecSrcClient - located-quote fact table: the CLIENT side of C2

Round 44, wave w1, seat ExecSrcClient. Scope: what xdg-shell 1.49, GTK 4.24.1 and gkeep 133b867
establish about the client's handling of the size a compositor configures, plus the compositor
seam that hands the size over (context rows, section D - another seat owns that side).

Pins (`.ufo/waves/round-44/fetch/`, sha256 from `receipts/fetch-sha256.txt`, all verified by
`verify_facts.py` below before any row is emitted):

| receipt | sha256 | bytes |
|---|---|---|
| `xdg-shell.xml` | `7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df` | 63846 |
| `gdktoplevel-wayland.c` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` | 97548 |
| `gkeep-ui.py` | `07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a` | 14639 |
| `Hyprland-Window.cpp` | `d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded` | 124226 |
| `Hyprland-XDGShell.cpp` | `d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0` | 35458 |

## A. xdg-shell 1.49 (`xdg-shell.xml`)

Protocol text only: it constrains the compositor's *offer* and the client's *obligation*, never
GTK's behaviour. Locators are the 1-based line on which the quote starts, computed by
`verify_facts.py` from the pinned bytes.

| claim | quote (<=25 words) | file:line | sha256 |
|---|---|---|---|
| A1 | configure width/height is a HINT, in window-geometry coordinates, not an order | `The width and height arguments specify a hint to the window` | `xdg-shell.xml:1150` | `7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df` |
| A2 | configure 0x0 means the client picks its own dimension | `If the width or height arguments are zero, it means the client should decide its own window dimension.` | `xdg-shell.xml:1154` | `7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df` |
| A3 | the configured size is interpreted THROUGH the states array, not on its own | `The states listed in the event specify how the width/height arguments should be interpreted` | `xdg-shell.xml:1159` | `7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df` |
| A4 | state maximized=1 makes the configure geometry EXACT (must be obeyed) | `The window geometry specified in the configure event must be obeyed by the client` | `xdg-shell.xml:841` | `7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df` |
| A5 | state fullscreen=2 makes the configure geometry a MAXIMUM, not an exact size | `The surface is fullscreen. The window geometry specified in the configure event is a maximum; the client cannot resize beyond it.` | `xdg-shell.xml:851` | `7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df` |
| A6 | state resizing=3 also makes the configure geometry a maximum | `The surface is being resized. The window geometry specified in the configure event is a maximum; the client cannot resize beyond it.` | `xdg-shell.xml:860` | `7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df` |
| A7 | tiled_* states carry NO size semantics in the protocol, only decoration advice | `The window is currently in a tiled layout and the left edge is considered to be adjacent to another part of the tiling grid.` | `xdg-shell.xml:875` | `7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df` |
| A8 | every configure must be acked before the commit that responds to it | `must make an ack_configure request sometime before the commit request, passing along the serial of the configure event.` | `xdg-shell.xml:564` | `7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df` |
| A9 | intermediate configures may be dropped: only the last needs acking | `If the client receives multiple configure events before it can respond to one, it only has to ack the last configure event.` | `xdg-shell.xml:571` | `7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df` |
| A10 | configure_bounds (since v4) may precede a configure and bounds the recommended size | `The configure_bounds event may be sent prior to a xdg_toplevel.configure event to communicate the bounds` | `xdg-shell.xml:1191` | `7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df` |
| A11 | client min size is advisory: the compositor may ignore it | `The client should not rely on the compositor to obey the minimum size` | `xdg-shell.xml:1009` | `7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df` |

## B. GTK 4.24.1 (`gdktoplevel-wayland.c`)

The whole client path, in order: `xdg_toplevel_configure` stores -> `xdg_surface.configure`
(`handle_configure`) consumes -> `compute_size` applies -> `ack_configure` is sent. `pending` is
`{int width; int height; GdkToplevelState state; gboolean is_resizing; ...}` (gdktoplevel-wayland.c,
struct GdkWaylandToplevel). The extension is `.c`, which the frozen counter's comment stripper does
not cover (it lists `.cpp/.hpp/.h/.cc`), so a GTK quote *may* come from a comment; every row below is
code anyway, so the rows hold under either reading.

| claim | quote (<=25 words) | file:line | sha256 |
|---|---|---|---|
| B1 | the xdg_toplevel.configure handler only STORES width/height into pending | `pending_state |= resize_constraint_state; toplevel->pending.state |= pending_state; toplevel->pending.width = width;` | `gdktoplevel-wayland.c:785` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B2 | the xdg_surface.configure handler is where pending width/height is consumed | `width = wayland_toplevel->pending.width;` | `gdktoplevel-wayland.c:644` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B3 | GTK reads a 0 width AND 0 height as 'no size given' (saved_size) | `saved_size = (width == 0 && height == 0);` | `gdktoplevel-wayland.c:647` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B4 | on 0x0 while leaving a fixed state GTK restores its own saved size | `if (saved_size && !fixed_size && was_fixed_size) { width = wayland_toplevel->saved_width; height = wayland_toplevel->saved_height;` | `gdktoplevel-wayland.c:656` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B5 | a floating configure (no maximized/fullscreen/tiled, not resizing) is NOT fixed_size | `fixed_size = new_state & (GDK_TOPLEVEL_STATE_MAXIMIZED | GDK_TOPLEVEL_STATE_FULLSCREEN | GDK_TOPLEVEL_STATE_TILED) || is_resizing;` | `gdktoplevel-wayland.c:633` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B6 | a non-zero configure size is latched as configured_width/configured_height | `wayland_surface->next_layout.configured_width = width;` | `gdktoplevel-wayland.c:681` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B7 | and is marked fixed only when the state says so (floating -> not fixed) | `wayland_toplevel->next_layout.size_is_fixed = fixed_size;` | `gdktoplevel-wayland.c:680` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B8 | a fresh non-zero configure asks for constraint against GTK's own min size | `if (!saved_size) { wayland_toplevel->next_layout.should_constrain = TRUE;` | `gdktoplevel-wayland.c:664` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B9 | compute_size takes the compositor size when one was latched | `if (wayland_surface->next_layout.configured_width > 0 && wayland_surface->next_layout.configured_height > 0)` | `gdktoplevel-wayland.c:513` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B10 | the latched size is clamped by GTK's geometry hints before use | `if (wayland_toplevel->next_layout.should_constrain) { gdk_surface_constrain_size (&wayland_toplevel->geometry_hints,` | `gdktoplevel-wayland.c:523` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B11 | a non-fixed latched size is cleared after one application (one-shot) | `if (!wayland_toplevel->next_layout.size_is_fixed) { wayland_toplevel->next_layout.should_constrain = FALSE;` | `gdktoplevel-wayland.c:532` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B12 | GTK's min size is the compute_size callback's min_width, sent to the compositor | `geometry.min_width = size.min_width;` | `gdktoplevel-wayland.c:492` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B13 | the constraint mask is MIN-only for a resizable window: no ceiling from GTK | `if (gdk_toplevel_layout_get_resizable (layout))` | `gdktoplevel-wayland.c:490` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B14 | so the clamp applied to a latched size is a floor, not a ceiling | `mask = GDK_HINT_MIN_SIZE;` | `gdktoplevel-wayland.c:494` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B15 | a non-resizable window pins min=max=natural size | `geometry.max_width = geometry.min_width = size.width; geometry.max_height = geometry.min_height = size.height;` | `gdktoplevel-wayland.c:498` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B16 | those hints leave as xdg_toplevel.set_min_size/set_max_size | `XDG_SHELL_CALL (xdg_toplevel, set_min_size, toplevel, min_width, min_height);` | `gdktoplevel-wayland.c:1333` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B17 | the ack is sent at the END of handle_configure, with the pending serial | `XDG_SHELL_CALL (xdg_surface, ack_configure, wayland_surface, wayland_surface->pending.serial);` | `gdktoplevel-wayland.c:706` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B18 | the saved size strips GTK's shadow margins | `toplevel->saved_width = surface->width - impl->shadow_left - impl->shadow_right;` | `gdktoplevel-wayland.c:210` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B19 | with no configure_bounds GTK falls back to the union of all monitors | `gdk_rectangle_union (&display_geometry, &monitor_geometry, &display_geometry);` | `gdktoplevel-wayland.c:476` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |
| B20 | and passes that fallback in as the size-request bound | `bounds_width = display_geometry.width; bounds_height = display_geometry.height;` | `gdktoplevel-wayland.c:480` | `0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe` |

## C. gkeep 133b867 (`gkeep-ui.py`)

| claim | quote (<=25 words) | file:line | sha256 |
|---|---|---|---|
| C1 | gkeep sets a default size of 420x500, immediately after turning CSD off | `window.set_decorated(False) window.set_default_size(420, 500)` | `gkeep-ui.py:475` | `07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a` |
| C2 | gkeep's application_id, the token the windowrule class matches | `super().__init__( application_id="org.omarchy.gkeep", flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE, )` | `gkeep-ui.py:448` | `07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a` |
| C3 | the only CSS min-* properties in the file: 30px tall, 72px wide, in one block | `padding: 6px 12px; min-height: 30px; min-width: 72px;` | `gkeep-ui.py:86` | `07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a` |

## D. Seam: what Hyprland 0.56.2 actually sends (context, not client behaviour)

Rows here exist only to fix the input to the client rows in A-C: which size leaves
`CWindow::sendWindowSize`, over which request, and how the ack comes back. Verified against the
same pinned bytes with the same parsers; the compositor-side argument belongs to its own seat
(`Hyprland-Window.cpp` is held row S164's receipt).

| claim | quote (<=25 words) | file:line | sha256 |
|---|---|---|---|
| D1 | Wayland targets are reported with a 0 lower clamp (X11 uses 1) | `if (!m_isX11) return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);` | `Hyprland-Window.cpp:1686` | `d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded` |
| D2 | sendWindowSize calls realToReportSize, then setSize on the xdg toplevel | `const auto REPORTSIZE = realToReportSize();` | `Hyprland-Window.cpp:1741` | `d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded` |
| D3 | the serial from setSize is queued with the size, for onAck | `else if (m_xdgSurface && m_xdgSurface->m_toplevel) m_pendingSizeAcks.emplace_back(` | `Hyprland-Window.cpp:1752` | `d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded` |
| D4 | the X11 branch instead pushes an xcb configure | `if (m_isX11 && m_xwaylandSurface) m_xwaylandSurface->configure({REPORTPOS, REPORTSIZE});` | `Hyprland-Window.cpp:1750` | `d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded` |
| D5 | onAck applies the acked size to the surface's pending state | `m_pendingSizeAck = *SERIAL;` | `Hyprland-Window.cpp:1520` | `d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded` |
| D6 | setSize latches the size and schedules a configure for the whole surface | `m_pendingApply.size = size;` | `Hyprland-XDGShell.cpp:355` | `d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0` |
| D7 | the configure carries exactly the latched size and the latched states | `if (const auto PSTATES = sc<int*>(wl_array_add(&arr, m_pendingApply.states.size() * sizeof(int)))) std::ranges::copy(m_pendingApply.states, PSTATES); m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);` | `Hyprland-XDGShell.cpp:452` | `d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0` |
| D8 | Hyprland tracks a client min size for the layout | `Vector2D CXDGToplevelResource::layoutMinSize() { Vector2D minSize;` | `Hyprland-XDGShell.cpp:467` | `d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0` |

## E. Structure facts (parser-read, not quoted)

| fact | value | where |
|---|---|---|
| gkeep calls set_default_size exactly once, with 420, 500 | `calls=1 args=420x500` | `gkeep-ui.py:476` |
| gkeep calls set_size_request zero times | `calls=0` | `gkeep-ui.py (whole file)` |
| gkeep declares one application_id | `calls=1 value=org.omarchy.gkeep` | `gkeep-ui.py:449` |
| gkeep turns CSD off | `window.set_decorated(False)` | `gkeep-ui.py:475` |
| min-height at line 87 sits under the selector declared at line 80 | `button.ink {{ / min-height: 30px` | `gkeep-ui.py:87` |
| min-width at line 88 sits under the selector declared at line 80 | `button.ink {{ / min-width: 72px` | `gkeep-ui.py:88` |
| the file declares this many min-* CSS properties in total | `count=2` | `gkeep-ui.py (whole file)` |
| number of `window...{` CSS blocks that themselves declare min-* | `count=0` | `gkeep-ui.py (whole file)` |
| GTK acks the configure exactly once per handle_configure | `ack_configure calls=1` | `gdktoplevel-wayland.c (whole file)` |
| GTK never sends set_min_size/max_size anywhere else | `set_min_size=1 set_max_size=1` | `gdktoplevel-wayland.c (whole file)` |
| Hyprland never sends xdg_toplevel.configure_bounds | `configure_bounds occurrences=0` | `Hyprland-XDGShell.cpp (whole file)` |

## F. Exact / maximum / hint, per configure state (composed from section A)

| configure state | protocol force on width/height | row |
|---|---|---|
| none (plain floating configure) | a *hint*; the client may pick another size | A1 |
| `maximized` (1) | *exact*: "must be obeyed by the client, or ... invalid_surface_state" | A4 |
| `fullscreen` (2) | *maximum*: "cannot resize beyond it"; must be obeyed to cover the whole area | A5 |
| `resizing` (3) | *maximum*: "cannot resize beyond it" | A6 |
| `tiled_left/right/top/bottom` (5-8) | **no size semantics stated at all**; decoration advice only | A7 |
| `0x0` in either dimension | the client decides (A2), which GTK reads as "restore my own size" (B4) | A2, B4 |

So the protocol never makes a floating configure binding, and never makes a fullscreen configure
exact - it makes it a ceiling. A client that lands *below* the ceiling, or above a bare hint, is
conforming. GTK's own reading of a latched size is a one-shot application (B9 -> B11), clamped
against a MIN-only mask when the configure carried a fresh non-zero size (B8, B10, B13, B14): GTK
cannot come out *smaller* than its own minimum, and nothing in the pinned file stops it from
adopting a size bigger than its natural request. That is the whole room in which the
gkeep/Hyprland size disagreement lives.

## G. What the pinned sources do NOT establish

Each item names the rows it would have needed and the file that was never pinned.

1. **That GTK honours a compositor size LARGER than its natural size.** B9-B11 show the latched size
   is taken and applied; B13/B14 show the only clamp is a MIN floor for a resizable window. But the
   `update_size` -> buffer-commit path that turns this into a `wl_surface` size lives in
   `gdk/wayland/gdksurface.c` and GTK's widget allocation in `gtk/gtkwindow.c`, **neither pinned**.
   Reading these five files does not say what a 900x1200 configure does to a 420x500 gkeep.
   [INFERENCE] from B9-B11: the configured size is the one GDK *adopts*, raised to GTK's minimum.
2. **What gkeep's actual minimum/natural size IS.** `set_size_request(` occurs zero times in the
   pinned full file (E), and the only CSS `min-*` declarations are two lines under `button.ink`
   (C3, E) - i.e. 30px/72px on *buttons*. The window's minimum is whatever `GtkWindow` computes
   from its children in `gtk/gtkwindow.c`, not pinned.
3. **That `set_default_size(420, 500)` reaches the screen as 420x500.** C1 pins the call; how GTK
   turns it into the size it commits on a 0x0 configure is `gtk/gtkwindow.c` plus
   `gdk/wayland/gdksurface.c`, not pinned. B20 only shows the *fallback* size comes from
   `gdk_toplevel_notify_compute_size`, not from a field holding 420x500.
4. **Which states Hyprland attaches to the configure for a rule-sized floating window.** D6/D7 show
   the states array is whatever `m_pendingApply.states` holds at schedule time; they do not show
   the set for gkeep. If `maximized`/`fullscreen`/`tiled`/`resizing` were ever in it, GTK's
   `fixed_size` flips (B5), the one-shot clearing at B11 stops applying and the size becomes sticky.
   This needs a runtime capture, not a source read.
5. **That Hyprland honours GTK's `set_min_size` when it sizes the box from a windowrule.** D8 proves
   Hyprland *tracks* a client min size for the layout; no pinned line shows the rule-size path
   consulting it.
6. **That GTK's shadow margins are zero for gkeep.** `set_decorated(False)` is pinned (E) and B18
   subtracts `shadow_*` from the saved size, but where those fields are assigned is not in this
   file. "The surface commits exactly 420x500" is therefore not visible in the pins.
7. **That `configure_bounds` reaches GTK on Hyprland.** `grep -c configure_bounds` on the pinned
   `Hyprland-XDGShell.cpp` is 0 (E), so GTK's `has_bounds` stays false and the monitor-union
   fallback (B19, B20) is the live path - but that is a statement about this commit, not about
   0.56.2 under every state.
8. **Anything about a client other than GTK.** Section F's permissiveness means one configure can be
   honoured exactly, clamped, or ignored by three toolkits. No row here generalises to
   Qt/Electron/Chromium, so no row supports a claim about "clients" as a class.
9. **That the ack is observable as a resize.** B17 acks at the end of `handle_configure`, i.e. before
   `compute_size` applies the size in the same layout pass, and the pins do not order that ack
   against the buffer commit. "The compositor saw the ack, so the window resized" is unsupported.
10. **Which of the two boxes C1 compares.** Nothing in these five files says whether
    `hyprctl clients -j` reports the box Hyprland assigned or the size the client committed; that is
    the compositor-side question, and it is why A1+A2 (hint, client decides) matter: the two may
    legitimately differ without either side misbehaving.

## H. What the C2 entry can lift from here

Clause h of PRED-C2-r44 recomputes two lines from the pinned bytes. `verify_facts.py` runs the
frozen counter's own `host_census()` against these same pins and both lines come back verbatim:

    gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep
    hyprland sendWindowSize xdg_setSize=1 x11_configure=1

`xdg_setSize=1` / `x11_configure=1` are D3/D4 counted inside `CWindow::sendWindowSize`; the gkeep
line's three fields are C1 (default size), E (zero `set_size_request` calls) and C2
(application_id). Every row in A-D is gate-usable as written: 3-25 words, word-bounded, occurring
exactly once in its receipt, surviving the counter's comment stripping for that extension, and
occurring in none of the other four pins - so five Gate rows quoting five different receipts stay
pairwise distinguishable.

Tooling: no package was installed for this seat; `python3` (host) plus the lane's frozen counter,
imported read-only, were sufficient. No scratch tree was left behind.

## I. Verification

`verify_facts.py` (this seat dir) imports the FROZEN counter's own parsers (`quote_at`,
`occurrences`, `quote_in_code`, `norm_receipt`, `host_census`) from
`quality/counters/c2-r44-gkeep-size-request.py` and, for every row above, asserts:

* `3 <= len(quote.split()) <= 25`;
* the whitespace-collapsed quote occurs word-bounded **exactly once** in its receipt;
* it survives the frozen counter's comment stripping for that extension (`.cpp` stripped, `.c` and
  `.xml` untouched, `.py` `#`-stripped);
* it occurs in **no other** pinned receipt (`norm_receipt`);
* the printed locator is the line the parser computed, and each receipt's sha256 still equals the
  frozen `receipts/fetch-sha256.txt` value (5/5 `PIN-OK`);
* **grep agrees with every locator**: taking the source line at the computed number and running
  `grep -nF` on a 32-character prefix of it returns that same line number (42/42).

It also runs the frozen counter's `host_census()` on the same pinned bytes and requires it to
reproduce both clause-h lines verbatim (section H).

Raw output: `verify.log` in this seat dir. Re-run:
`cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I .ufo/waves/round-44/w1/ExecSrcClient/verify_facts.py`
-> `grep_locator_ok=42/42`, `census_clause_h ok=True`,
`rows=42 fails=0 pin_mismatch=0 census_ok=True grep_fails=0`.
