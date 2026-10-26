# The gkeep size question, settled

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

## §1 Decision table

The answers below name no id; each cites a keyword line and a locator range. Every "settled" answer is false.

| question | settled answer | where |
|---|---|---|
| Which size does Hyprland report? | exactly the size the client asked for, never the compositor's goal | realToReportSize (Hyprland-Window.cpp:1685-1699) |
| How does that size reach the client? | through a file descriptor handoff, not a protocol event | sendWindowSize (Hyprland-Window.cpp:1732) |
| Does the X11 path exist? | no, it was removed before 0.56.2 | X11 (Hyprland-Window.cpp:1751) |
| Are acks remembered? | no, acks are dropped on receipt | ack (Hyprland-Window.cpp:1514) |
| Does setSize queue anything? | no, it writes to the socket immediately | setSize (Hyprland-XDGShell.cpp:354-358) |
| Is the deferred configure used? | never, the deferred path is unreachable | configure (Hyprland-XDGShell.cpp:455) |
| What does a zero dimension mean? | an error the client must report to the compositor | zero (xdg-shell.xml:1154-1157) |
| Does the client answer a configure? | no, the protocol has no client answer | ack_configure (xdg-shell.xml:560) |
| What does GTK do with a configured size? | ignores it and keeps the size it computed | configured (gdktoplevel-wayland.c:681) |
| Does GTK constrain by hints? | never, hints are consulted only at map time | constrain (gdktoplevel-wayland.c:525) |
| What does GTK do with a 0x0 configure? | treats it as a request for the smallest size | 0x0 (gdktoplevel-wayland.c:647) |
| What application id does gkeep use? | none; the window is anonymous | application_id (gkeep-ui.py:449) |

## §2 Census

gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep

hyprland sendWindowSize xdg_setSize=1 x11_configure=1
