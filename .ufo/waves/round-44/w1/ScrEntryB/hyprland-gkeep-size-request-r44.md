# What can and cannot establish the size a gkeep window renders once the rule's box is replaced: the compositor's ask, the protocol's licence, and the app's own declarations

Lane: mado-shokunin. Round: 44.

source: S164 - hyprwm/Hyprland src/desktop/view/Window.cpp @ efb5099 (v0.56.2; held row) - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp
source: S298 - hyprwm/Hyprland src/protocols/XDGShell.cpp @ efb5099 (v0.56.2) - https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/XDGShell.cpp
source: S299 - wayland-protocols 1.49 stable/xdg-shell/xdg-shell.xml - https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/stable/xdg-shell/xdg-shell.xml
source: S300 - GTK 4.24.1 gdk/wayland/gdktoplevel-wayland.c - https://gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gdk/wayland/gdktoplevel-wayland.c
source: S301 - gkeep 133b867 gkeep/ui.py (full file; the held excerpt is its lines 446-488) - https://raw.githubusercontent.com/VeigaPunk/gkeep/133b86717a02548aeaff3f1411bf301d936c5308/gkeep/ui.py
verified-at: 2026-10-26
recheck: 30d - re-pull the five pinned receipts at their URLs, re-derive the two census lines, and re-read the hosts (hyprland 0.56.2-4, gtk4 1:4.24.1-1, wayland-protocols 1.49-1); a Hyprland tag after v0.56.2 or a newer GTK is the earlier trigger
ground: what the compositor's ask, the protocol's licence and the app's own declarations can and cannot say about the size a gkeep window renders
assimilated-from: merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md (amended and superseded on its conclusion: it ends by declaring the chain complete and the rendered geometry 420x500, which this entry does not adopt, nor its settled wording; what it adds is the pending-ack mechanics, the protocol hint wording and the GTK configure handler)

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| What size does Hyprland ask a mapped gkeep toplevel for, and does it remember asking? | the send path in the pinned Window.cpp: the report size, the pending list, the serial returned by the toplevel ask | OBS source; the report size is the animated goal, not the drawn size |
| Does the ask reach the wire at once? | the pinned XDGShell.cpp: the size is recorded and a configure is scheduled for a later event-loop turn | OBS source; it licenses no delivery time |
| What may the client do with the size in a configure? | the pinned xdg-shell 1.49 toplevel configure description: a hint, zero meaning the client decides, and an error defined for the maximized state only (line 842) | OBS source; INF that a floating client staying off the hinted size is not thereby in error |
| What does GTK 4.24.1 keep of it? | the pinned configure handler: configured width and height into the next layout, flagged fixed under maximize, fullscreen or tile | OBS source; it licenses neither gkeep's allocation nor the rendered result |
| What does gkeep itself declare? | the pinned ui.py: one default size, zero size requests, one application id | OBS source; the default size equals the rule's size, so neither can be singled out |
| Is the ack a reading of the drawn size? | the ack handler in the pinned Window.cpp: a serial is matched and the remembered size stored as pending | OBS source; no read verb exposes the drawn geometry (corpus/knowledge/hyprland-gkeep-geometry-r43.md, its compositor-dump section) |
| Has this host session given a gkeep window 420x500? | a live `hyprctl clients -j` taken while gkeep is open | UNK - no gkeep window was observed for this round |

## §1 The compositor's half

**OBS** S164 - the send path splits on surface kind and only the Wayland branch files a pending entry: `if (m_isX11 && m_xwaylandSurface) m_xwaylandSurface->configure({REPORTPOS, REPORTSIZE}); else if (m_xdgSurface && m_xdgSurface->m_toplevel) m_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());` (Hyprland-Window.cpp:1750) - the X11 surface is configured, the Wayland toplevel is asked for the size.

**OBS** Both branches send the report size, which for a Wayland window is the clamped goal of the animated size (Hyprland-Window.cpp:1685-1689), and the pending entry pairs the serial obtained with the floored size (line 1753).

**OBS** The ack handler consumes that list: it takes the newest entry whose serial is not greater than the acked serial, stores its size as the surface's pending acked size and erases that entry with every older one, and an X11 window returns before the store (Hyprland-Window.cpp:1514-1529).

## §2 What the protocol lets the client do

**OBS** S298 - the toplevel ask records and schedules rather than writes: `m_pendingApply.size = size; scheduleStateApplication(); return m_owner->scheduleConfigure();` (Hyprland-XDGShell.cpp:355) - the caller gets a serial and the configure is emitted from the event loop.

**OBS** The schedule keeps one deferred callback and reuses its serial while pending, and the emission only resets that callback and sends (Hyprland-XDGShell.cpp:629-643).

**OBS** S299 - the size the client receives is advice: `The width and height arguments specify a hint to the window about how its surface should be resized in window geometry coordinates.` (xdg-shell.xml:1150) - zero width or height means the client decides its own dimension (lines 1154-1156), the maximized state is where the geometry must be obeyed (line 842), and every configure must be acked (line 1166).

## §3 What GTK 4.24.1 makes of it

**OBS** S300 - the configure handler adopts the compositor's numbers as the next layout and marks them fixed: `wayland_toplevel->next_layout.size_is_fixed = fixed_size; wayland_surface->next_layout.configured_width = width; wayland_surface->next_layout.configured_height = height;` (gdktoplevel-wayland.c:680) - fixed means maximized, fullscreen, tiled or resizing (lines 635-638).

**OBS** A zero by zero configure is read as a size the client sets, and GTK restores the size it saved before a maximize or fullscreen transition (gdktoplevel-wayland.c:647-660); the same handler acks with the pending serial (line 706).

## §4 What gkeep declares

**OBS** S301 - the app builds one window and gives it a default size only: `window = Gtk.ApplicationWindow(application=self, title="gkeep") window.set_decorated(False) window.set_default_size(420, 500)` (gkeep-ui.py:474) - the file holds no call to set_size_request at all, and the application id is org.omarchy.gkeep (line 449).

**INF** The default size equals the rule's size, so a 420x500 report cannot say which of the two produced it; what the app does not declare is any minimum that could override a configure.

## §5 What this entry does not establish

- The size a gkeep window is drawn at, on this host or another: every compositor read verb reports the animated goal (corpus/knowledge/hyprland-gkeep-geometry-r43.md, its compositor-dump section), and no gkeep window was observed for this round (UNK).
- That the client took the configure at the size asked: an ack reports a serial, not a committed geometry.
- What a maximized or fullscreen gkeep window would report: the pinned handler replaces the box, and the operability reading of that is a separate claim.
- Behaviour on a Hyprland other than 0.56.2 at efb5099, a GTK other than 4.24.1, or a gkeep other than 133b867.

Census (recomputed by the C2 counter from the pinned receipts):

gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep
hyprland sendWindowSize xdg_setSize=1 x11_configure=1
