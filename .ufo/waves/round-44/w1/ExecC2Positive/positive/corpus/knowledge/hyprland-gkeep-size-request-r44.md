# What happens to the gkeep window's box after Hyprland sets it: the size the compositor reports, the xdg configure that carries it, what the protocol permits, what GTK 4 does with it, and what gkeep itself declares

source: S164 - hyprwm/Hyprland src/desktop/view/Window.cpp @ efb5099 (v0.56.2, held row) - sendWindowSize, realToReportSize, the pending-ack list, onAck, and the X11 configure branch
source: S298 - hyprwm/Hyprland src/protocols/XDGShell.cpp @ efb5099 (v0.56.2) - CXDGToplevelResource::setSize, the state application, the deferred configure and its serial
source: S299 - wayland-protocols 1.49 stable/xdg-shell/xdg-shell.xml - what the width and height of a toplevel configure mean to the client
source: S300 - GTK 4.24.1 gdk/wayland/gdktoplevel-wayland.c - the xdg_toplevel configure handler and the layout that applies the configured size
source: S301 - own-work: gkeep gkeep/ui.py at 133b867 (full file), pinned at .ufo/waves/round-44/fetch/gkeep-ui.py - the app's application id and default size
verified-at: 2026-10-26
recheck: 30d - re-pull the four upstream files at their tags and the gkeep file at 133b867 and re-run the counter; a Hyprland tag after v0.56.2, a GTK 4.24.x bump or a wayland-protocols bump is the earlier trigger
ground: what the compositor does with the gkeep window's box after the rule sets it, what the client is permitted to do with the size it is sent, and what gkeep itself asks for
Lane: mado-shokunin. Round: 44.
assimilated-from: merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md (its post-rule size-request chain, re-derived at the pinned commits; the refused residue and its flip conditions are in corpus/lessons/round-44.md)

## What this adds to round 43

Round 43 ended at the box: the rule's size expression is evaluated in the floating algorithm's first-map branch, written to the target and the window, and `hyprctl clients -j` prints the animation goal (entry `hyprland-gkeep-geometry-r43.md`). This entry starts one step later and follows the box out of the compositor: the size the compositor hands to the client, the protocol event that carries it, the one thing the client may do with it, what the host's toolchain (GTK 4.24.1) does, and what gkeep itself declares about its size. Nothing here is measured on a live gkeep window; the host census of round 43 still has no gkeep client.

## §1 The compositor reports the goal box to the client

**OBS** S164 - the report branch sends the size and keeps the serial: in `CWindow::sendWindowSize(bool force)` the X11 arm configures the xwayland surface and the Wayland arm pushes the returned serial together with the size onto the pending list, so the size that was sent is not yet the size the client acknowledged: `if (m_isX11 && m_xwaylandSurface) m_xwaylandSurface->configure({REPORTPOS, REPORTSIZE}); else if (m_xdgSurface && m_xdgSurface->m_toplevel) m_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());` (Hyprland-Window.cpp:1750).

**OBS** - the size sent is `REPORTSIZE = realToReportSize()` (Window.cpp:1741): for a Wayland window that function returns the goal of the animated size, clamped to non-negative (Window.cpp:1685-1689), never the current animated value. The entry point is a callback on the animated size (Window.cpp:800-810) and the function returns early unless it is forced or the pending reported size or the reported position changed (Window.cpp:1743-1747).

**OBS** - the acknowledgement half is `CWindow::onAck(uint32_t serial)` (Window.cpp:1514-1529): it finds the last pending entry whose serial is not newer than the acked one, drops every pending entry up to it, and for Wayland copies that entry's size, the size the compositor itself pushed at Window.cpp:1753, into the surface's `m_pending.ackedSize`, with the comment that the window has ponged; X11 returns before that. The ack carries a serial and no size, so the size the client actually applied never reaches this code, and `getReportedSize()` returns the recorded value on Wayland (Window.cpp:1861-1867), a reader with no caller in this file.

## §2 The size becomes an xdg configure with a serial

**OBS** S298 - setSize stores the wanted size, schedules the state application and returns a configure serial: `uint32_t CXDGToplevelResource::setSize(const Vector2D& size) { m_pendingApply.size = size; scheduleStateApplication(); return m_owner->scheduleConfigure(); }` (Hyprland-XDGShell.cpp:354). The stored size reaches the wire in `scheduleStateApplication()`'s deferred body as `m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr)` (XDGShell.cpp:455), and `scheduleConfigure()` (XDGShell.cpp:629-636) registers the deferred configure, allocates a fresh serial from the display and reuses an in-flight one instead of queueing a second, while `configure()` (XDGShell.cpp:640-643) sends the configure for that serial. So the serial in `m_pendingSizeAcks` is the serial the client is expected to ack.

## §3 What the protocol permits the client to do

**OBS** S299 - the protocol calls the width and height a hint and tells the client not to apply the state at once: `The width and height arguments specify a hint to the window about how its surface should be resized in window geometry coordinates.` (xdg-shell.xml:1150). The same description says the configured state should not be applied immediately (lines 1146-1148) and that a width or height of zero means the client should decide its own window dimension (lines 1154-1157). The client must ack the configure before committing the surface it arranged for it (lines 610-612, 560-566).

**INF** A client may therefore take the compositor's size, adjust it (subject to any constraints it was given) or ignore it, and the protocol is satisfied as long as it acks. The compositor's pending list cannot tell those cases apart: it stores the size it sent, not the size the client applied.

## §4 What GTK 4.24.1 does with the configure

**OBS** S300 - GTK adds its shadow margins to the configured size before it updates the surface: `width = wayland_surface->next_layout.configured_width + wayland_surface->shadow_left + wayland_surface->shadow_right;` (gdktoplevel-wayland.c:518). The condition is that both configured dimensions are greater than zero (lines 513-514); GTK then constrains the result to the geometry hints when the surface is resizing, updates the surface size, and clears the configured dimensions unless the size was fixed (lines 523-537). With a zero configure it uses the geometry's own width and height instead (lines 539-549). The handler that fills `pending.width`/`pending.height` is `xdg_toplevel_configure` (line 710 onward), the layout is requested at line 693, and the configure is acked at line 706.

**INF** For a normal toplevel the configured size is adopted plus shadow margins, so a maximized or fullscreen compositor box becomes a GTK surface at that size; a 0x0 configure leaves GTK's own default size in charge. The shadow margins mean the surface size GTK reports back is not byte-equal to the configure the compositor sent.

## §5 What gkeep declares

**OBS** S301 - the app sets only a default size and hands the window to its board: `window.set_default_size(420, 500) self.board = Board(window)` (gkeep-ui.py:476). Its application id is `org.omarchy.gkeep` (gkeep-ui.py:449) and `set_size_request` is never called in the file.

**INF** `set_default_size` is GTK's initial size for an unconfigured toplevel, so it is the size GTK uses when the compositor sends a zero configure and the fallback the compositor's configure replaces. It cannot by itself pin the window, which is why the round-43 rule and the app's declared size can agree without either deciding the outcome.

## §6 Client-side census of the pinned bytes

Both lines are recomputed by the counter from the pinned receipts, not copied from a run:

gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep
hyprland sendWindowSize xdg_setSize=1 x11_configure=1

The first line is gkeep's own declaration: one `set_default_size(420, 500)`, zero `set_size_request` calls, one application id. The second is the body of `CWindow::sendWindowSize(bool force)`: one `->setSize(` for the Wayland arm and one `->configure(` for the X11 arm, both inside the single report branch quoted in §1.

## §7 What this does not establish

- No live gkeep window: the round-43 census has four mapped clients, none floating, none of them gkeep, so no `sendWindowSize` round trip for this window has been observed on the host.
- The size the client actually applied is never reported back: the ack carries only a serial, and `getReportedSize()` hands out the compositor's own sent value (Window.cpp:1861-1867); whether GTK's surface ends at the configure size is unobserved here.
- The X11 branch is read, not exercised: gkeep is a Wayland GTK application on this host.

## Receipts

The five pins are committed at `.ufo/waves/round-44/fetch/` (mode 100644) with the sha256 values in `corpus/lessons/round-44.md` `## Gate`. Locators above are the counter's computed first-occurrence lines of the quotes (`Hyprland-Window.cpp:1750`, `Hyprland-XDGShell.cpp:354`, `xdg-shell.xml:1150`, `gdktoplevel-wayland.c:518`, `gkeep-ui.py:476`); the line ranges are read from the pinned files.
