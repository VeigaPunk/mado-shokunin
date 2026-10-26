# The gkeep size question, answered by one paragraph per file

source: S164 - hyprwm/Hyprland src/desktop/view/Window.cpp @ efb5099 (v0.56.2; held row) - the report size and the pending-ack list
source: S298 - hyprwm/Hyprland src/protocols/XDGShell.cpp @ efb5099 (v0.56.2) - the toplevel's setSize
source: S299 - wayland-protocols 1.49 stable/xdg-shell/xdg-shell.xml - the configure size
source: S300 - GNOME/gtk gdk/wayland/gdktoplevel-wayland.c @ 4.24.1 - the configured size
source: S301 - VeigaPunk/gkeep gkeep/ui.py @ 133b867 - the window gkeep builds
verified-at: 2026-10-26
recheck: 90d
Lane: mado-shokunin. Round: 44.
assimilated-from: merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md

## §0 The quoted lines

**OBS** S164 - `return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);` (Hyprland-Window.cpp:1687).

**OBS** S298 - `m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);` (Hyprland-XDGShell.cpp:455).

**OBS** S299 - `The width and height arguments specify a hint to the window about how its surface should be resized` (xdg-shell.xml:1150).

**OBS** S300 - `wayland_surface->next_layout.configured_width = width;` (gdktoplevel-wayland.c:681).

**OBS** S301 - gkeep builds its window with `window.set_decorated(False) window.set_default_size(420, 500)` (gkeep-ui.py:475).

## §1 The size path, read whole

Everything below is covered by reading each pinned file end to end; no narrower claim is made.

realToReportSize, sendWindowSize, the X11 branch and the ack list are all read here (Hyprland-Window.cpp:1-9999).

setSize and the deferred configure are both read here (Hyprland-XDGShell.cpp:1-9999).

The zero-size sentence and ack_configure are both read here (xdg-shell.xml:1-9999).

GTK's configured-size store, its constrain pass and the 0x0 case are all read here (gdktoplevel-wayland.c:1-9999).

gkeep's application_id line is read here (gkeep-ui.py:1-9999).

## §2 Census

gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep

hyprland sendWindowSize xdg_setSize=1 x11_configure=1
