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
## §1 What the compositor reports
## §2 The configure
## §3 What the protocol lets the client do
## §4 What GTK 4.24.1 does with it
## §5 What gkeep declares



**OBS** S164 - report size (Hyprland-Window.cpp:1685-1699): `return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);` (Hyprland-Window.cpp:1687); sendWindowSize (Hyprland-Window.cpp:1732-1753); the X11 path (Hyprland-Window.cpp:1751); the ack handler (Hyprland-Window.cpp:1514-1526).
hyprland sendWindowSize xdg_setSize=1 x11_configure=1
**OBS** S298 - setSize (Hyprland-XDGShell.cpp:354-358) and the deferred sendConfigure (Hyprland-XDGShell.cpp:455): `m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);` (Hyprland-XDGShell.cpp:455).
**OBS** S299 - the zero width or height case (xdg-shell.xml:1154-1157) and the ack_configure request (xdg-shell.xml:560): `The width and height arguments specify a hint to the window about how its surface should be resized` (xdg-shell.xml:1150).
**OBS** S300 - the configured-size store (gdktoplevel-wayland.c:681): `wayland_surface->next_layout.configured_width = width;` (gdktoplevel-wayland.c:681), the minimum-size constraint (gdktoplevel-wayland.c:523-528), the 0x0 case (gdktoplevel-wayland.c:647).
**OBS** S301 - gkeep's application_id line (gkeep-ui.py:449) and its default size: `window.set_decorated(False) window.set_default_size(420, 500)` (gkeep-ui.py:475).
gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep
