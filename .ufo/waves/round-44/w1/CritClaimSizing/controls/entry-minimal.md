# gkeep size request - control entry (quotes only)

source: S164 - hyprwm/Hyprland src/desktop/view/Window.cpp @ efb5099 (held row; receipt .ufo/waves/round-44/fetch/Hyprland-Window.cpp)
source: S298 - hyprwm/Hyprland src/protocols/XDGShell.cpp @ efb5099 - the toplevel setSize implementation
source: S299 - wayland-protocols 1.49 stable/xdg-shell/xdg-shell.xml - the toplevel configure event
source: S300 - GTK 4.24.1 gdk/wayland/gdktoplevel-wayland.c - the Wayland toplevel configure handler
source: S301 - gkeep 133b867 gkeep/ui.py (full file) - the app's window construction
verified-at: 2026-10-26
recheck: 90d - re-open the five receipts

S164 - "const auto REPORTSIZE = realToReportSize();" (Hyprland-Window.cpp:1741)
S298 - "uint32_t CXDGToplevelResource::setSize(const Vector2D& size) {" (Hyprland-XDGShell.cpp:354)
S299 - "This configure event asks the client to resize its toplevel surface or" (xdg-shell.xml:1146)
S300 - "gdk_wayland_toplevel_handle_configure (GdkWaylandSurface *wayland_surface)" (gdktoplevel-wayland.c:606)
S301 - "self.board = Board(window)" (gkeep-ui.py:477)

gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep
hyprland sendWindowSize xdg_setSize=1 x11_configure=1
