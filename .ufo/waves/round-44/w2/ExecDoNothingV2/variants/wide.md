# After the box: how Hyprland hands the gkeep window its size, what the protocol lets the client do with it, and what GTK and gkeep do

source: S164 - hyprwm/Hyprland src/desktop/view/Window.cpp @ efb5099 (v0.56.2; held row) - the report size, sendWindowSize and the pending-ack list
source: S298 - hyprwm/Hyprland src/protocols/XDGShell.cpp @ efb5099 (v0.56.2) - the toplevel's setSize and the deferred configure it sends
source: S299 - wayland-protocols 1.49 stable/xdg-shell/xdg-shell.xml - what an xdg_toplevel.configure size means to a client
source: S300 - GNOME/gtk gdk/wayland/gdktoplevel-wayland.c @ 4.24.1 - how a GTK 4 toplevel stores and applies a configured size
source: S301 - VeigaPunk/gkeep gkeep/ui.py @ 133b867 (full file) - the window gkeep builds and the only size it declares
verified-at: 2026-10-26
recheck: 90d - re-pull the five pinned files (Hyprland efb5099, wayland-protocols 1.49, GTK 4.24.1, gkeep 133b867) and re-run the counter; a Hyprland, gtk4 or wayland-protocols package update on the host or a gkeep commit is the earlier trigger











Locators (whole files): report size sendWindowSize X11 ack (Hyprland-Window.cpp:1-3000); setSize configure (Hyprland-XDGShell.cpp:1-2000); zero ack_configure (xdg-shell.xml:1-3000); configured minimum 0x0 (gdktoplevel-wayland.c:1-2000); application_id (gkeep-ui.py:1-500).
S164 `return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);` (Hyprland-Window.cpp:1687).
S298 `m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);` (Hyprland-XDGShell.cpp:455).
S299 `The width and height arguments specify a hint to the window about how its surface should be resized` (xdg-shell.xml:1150).
S300 `wayland_surface->next_layout.configured_width = width;` (gdktoplevel-wayland.c:681).
S301 `window.set_decorated(False) window.set_default_size(420, 500)` (gkeep-ui.py:475).
hyprland sendWindowSize xdg_setSize=1 x11_configure=1
gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep
