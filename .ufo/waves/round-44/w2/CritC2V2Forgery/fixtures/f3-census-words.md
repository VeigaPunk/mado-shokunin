# After the box: how Hyprland hands the gkeep window its size, what the protocol lets the client do with it, and what GTK and gkeep do

source: S164 - hyprwm/Hyprland src/desktop/view/Window.cpp @ efb5099 (v0.56.2; held row) - the report size, sendWindowSize and the pending-ack list
source: S298 - hyprwm/Hyprland src/protocols/XDGShell.cpp @ efb5099 (v0.56.2) - the toplevel's setSize and the deferred configure it sends
source: S299 - wayland-protocols 1.49 stable/xdg-shell/xdg-shell.xml - what an xdg_toplevel.configure size means to a client
source: S300 - GNOME/gtk gdk/wayland/gdktoplevel-wayland.c @ 4.24.1 - how a GTK 4 toplevel stores and applies a configured size
source: S301 - VeigaPunk/gkeep gkeep/ui.py @ 133b867 (full file) - the window gkeep builds and the only size it declares
verified-at: 2026-10-26
recheck: 90d - re-pull the five pinned files (Hyprland efb5099, wayland-protocols 1.49, GTK 4.24.1, gkeep 133b867) and re-run the counter; a Hyprland, gtk4 or wayland-protocols package update on the host or a gkeep commit is the earlier trigger
ground: the step after corpus/knowledge/hyprland-gkeep-geometry-r43.md - once the compositor has set the window's goal box, how that size reaches the client and whether gkeep could answer with another
Lane: mado-shokunin. Round: 44.
assimilated-from: merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md (its sendWindowSize step and its client-side reading, re-derived at the host's own commit and package versions; its "the chain is now complete" and "the rendered geometry ... is 420x500" are not adopted; the refused residue files and their flip conditions are in corpus/lessons/round-44.md)

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| Which size does Hyprland report to a Wayland client? | the report-size function: the GOAL of the animated size, clamped at zero | OBS (source) |
| How does that size reach the client? | the toplevel's setSize, which defers one xdg_toplevel.configure carrying the size | OBS (source) |
| Does Hyprland remember which configure the client acknowledged? | the pending-ack list of (serial, size) pairs and the ack handler | OBS (source) |
| Must the client use the configured size? | the protocol text: the size is a hint; zero means the client decides | OBS (spec) |
| What does GTK 4.24.1 do with a non-zero configured size? | the toplevel's configure handler and its layout pass | OBS (source) + INF (gkeep's case) |
| Does gkeep declare a size that could compete with 420x500? | gkeep's window construction | OBS (source) |
| Has a gkeep window been seen acknowledging 420x500 on this host? | no gkeep window open in round 43 or round 44 | UNK |

## §1 What the compositor reports

**OBS** S164 - for a Wayland client the report size is the GOAL of the animated size, clamped below at zero: `return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);` (Hyprland-Window.cpp:1687). Round 43 traced the rule's size into that GOAL (corpus/knowledge/hyprland-gkeep-geometry-r43.md), so the size sent to a floating gkeep window is the box the floating algorithm set.

**OBS** The report size comes from realToReportSize (Hyprland-Window.cpp:1685-1699), which for an X11 client clamps at 1x1 and may scale by the monitor instead. The same file's sendWindowSize (Hyprland-Window.cpp:1732) returns early when the pending reported size is unchanged and the call is not forced (Hyprland-Window.cpp:1743-1744); otherwise it configures an X11 surface directly (Hyprland-Window.cpp:1751) or, for an xdg toplevel, appends the serial returned by setSize and the floored size to the pending-ack list (Hyprland-Window.cpp:1753).

hyprland sendWindowSize xdg_setSize=1 x11_configure=1

## §2 The configure

**OBS** S298 - setSize stores the size as pending state and returns the next configure serial (Hyprland-XDGShell.cpp:354-358); the deferred state application sends it to the client: `m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);` (Hyprland-XDGShell.cpp:455).

**OBS** When the client acknowledges, onAck (Hyprland-Window.cpp:1514) takes the newest pending pair whose serial is not after the acknowledged one, drops it and every older pair, and for a Wayland client writes that pair's size into the surface's pending state as the acked size (Hyprland-Window.cpp:1526).

**INF** The ack records which size the client says it is answering; it does not force the client's next buffer to be that size. What Hyprland does with a buffer of another size after the ack is outside this entry's pins (UNK).

## §3 What the protocol lets the client do

**OBS** S299 - the configure size binds nobody: `The width and height arguments specify a hint to the window about how its surface should be resized` (xdg-shell.xml:1150); a zero width or height leaves the dimension to the client (xdg-shell.xml:1154-1157), and the states sent with it say how to interpret the size (xdg-shell.xml:1159-1161). The client answers a configure with the xdg_surface ack_configure request (xdg-shell.xml:560) before it commits the matching state; that ack is what Hyprland's onAck receives.

## §4 What GTK 4.24.1 does with it

**OBS** S300 - a non-zero configured size is kept for the next layout: `wayland_surface->next_layout.configured_width = width;` (gdktoplevel-wayland.c:681), with the size marked fixed only when the configure's states are maximized, fullscreen or tiled, or a resize is in progress (gdktoplevel-wayland.c:633-637).

**OBS** In the layout pass the configured size plus the shadow margins becomes the surface size (gdktoplevel-wayland.c:518-521), constrained by the window's geometry hints when the configure was not a 0x0 one (gdktoplevel-wayland.c:523-528); the hints carry the widget tree's minimum size for a resizable window (gdktoplevel-wayland.c:490-494). A 0x0 configure is recognised as one (gdktoplevel-wayland.c:647) and instead keeps the size GTK computes itself (gdktoplevel-wayland.c:539-544).

**INF** So a GTK 4.24.1 window adopts a non-zero configured size unless that size is below its minimum, in which case it is raised to the minimum. Whether Hyprland 0.56.2 sends a tiled state with a floating window's configure is not read here (UNK; it would only mark the size fixed, not change it).

## §5 What gkeep declares

**OBS** S301 - gkeep builds one undecorated application window and declares a default size only: `window.set_decorated(False) window.set_default_size(420, 500)` (gkeep-ui.py:475); its application id is set in the application constructor (gkeep-ui.py:449).

gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep

**OBS** The file has no `set_size_request` call (the census line above, recomputed by the counter); its only `min-width`/`min-height` (gkeep-ui.py:87-88) sit in the `button.ink` rule, a child widget's style, not the window's.

**INF** gkeep's default size equals the host rule's size (420x500, corpus/knowledge/hyprland-gkeep-geometry-r43.md), and its minimum is set by its widget tree, not by a declared request; the configure of §2 and gkeep's default therefore do not compete. Whether the widget tree's minimum is below 420x500 is not measured (UNK; it needs a live window or a GTK measurement).

## What the staged predecessor said, and what the pins correct

The staged `gkeep-client-size-request-r12.md` (package `merge/mado/`, read-only) is the predecessor; three of its sentences are not adopted
(w1/ScoutStagedResidue, w1/CritAssimilation):

- It names the request `xdg_toplevel.set_size`. The protocol has no such toplevel request; the size travels in the `xdg_toplevel.configure`
  event (xdg-shell.xml:1144) that Hyprland sends from its deferred state application (Hyprland-XDGShell.cpp:455).
- It reads the ack list as "the mechanism by which a client could report a different size". The client's ack_configure carries a serial only
  (xdg-shell.xml:560); onAck writes the compositor's own stored size for that serial (Hyprland-Window.cpp:1526), not a size the client chose.
- It says a GTK 4 window "will adopt the size the compositor configures". GTK 4.24.1 adopts it after constraining it by the window's
  geometry hints (gdktoplevel-wayland.c:523-528), and gkeep's widget-tree minimum is not measured here (UNK).

## What this entry does not establish

- That a gkeep window on this host rendered at 420x500: no gkeep window was open in rounds 43-44 (UNK).
- What Hyprland does when a client commits a buffer whose size differs from the acked one (not among the pins).
- The X11 path beyond its existence: gkeep is a GTK 4 Wayland client.
- Any Hyprland other than 0.56.2 at `efb5099`, any GTK other than 4.24.1, any gkeep other than 133b867.

**INF** gkeep also asks the toolkit for a minimum window size, and the compositor honors that minimum over its own goal.

**INF** On X11 the compositor never configures a surface directly; X11 windows keep whatever size the client picks.

**INF** The toplevel's setSize never puts a size on the wire, so no configure is ever delivered.

**INF** A gkeep window opens at whatever size the widget tree wants; gkeep declares no size of its own.

