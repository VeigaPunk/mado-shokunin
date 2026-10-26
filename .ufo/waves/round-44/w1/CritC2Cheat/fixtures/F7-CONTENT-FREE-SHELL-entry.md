# After the box: the gkeep size request (fixture shell)
source: S164 - Hyprland-Window.cpp
source: S298 - Hyprland-XDGShell.cpp
source: S299 - xdg-shell.xml
source: S300 - gdktoplevel-wayland.c
source: S301 - gkeep-ui.py
verified-at: 2026-10-26
recheck: 90d

**OBS** S164 - `return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);` (Hyprland-Window.cpp:1687).
**OBS** S298 - `m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);` (Hyprland-XDGShell.cpp:455).
**OBS** S299 - `The width and height arguments specify a hint to the window about how its surface should be resized` (xdg-shell.xml:1150).
**OBS** S300 - `wayland_surface->next_layout.configured_width = width;` (gdktoplevel-wayland.c:681).
**OBS** S301 - `window.set_decorated(False) window.set_default_size(420, 500)` (gkeep-ui.py:475).

gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep
hyprland sendWindowSize xdg_setSize=1 x11_configure=1
