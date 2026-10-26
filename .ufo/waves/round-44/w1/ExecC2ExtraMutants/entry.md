# After Hyprland sets the gkeep box: sendWindowSize, the configure the client receives, what xdg-shell 1.49 lets it do with it, and what gkeep 133b867 declares

source: S164 - hyprwm/Hyprland src/desktop/view/Window.cpp @ efb5099 (v0.56.2, held row) - CWindow::sendWindowSize, the pending-size-ack list and onAck
source: S298 - hyprwm/Hyprland src/protocols/XDGShell.cpp @ efb5099 (v0.56.2) - CXDGToplevelResource::setSize and CXDGSurfaceResource::scheduleConfigure
source: S299 - wayland-protocols 1.49 stable/xdg-shell/xdg-shell.xml - what a configure size means and what the client may do with it
source: S300 - GTK 4.24.1 gdk/wayland/gdktoplevel-wayland.c - gdk_wayland_toplevel_handle_configure and the fixed-size decision
source: S301 - own-work: the full ~/Projects/gkeep/gkeep/ui.py at gkeep 133b867, pinned at .ufo/waves/round-44/fetch/gkeep-ui.py - what the app declares
verified-at: 2026-10-26
recheck: 90d - re-pull the four upstream files at their pinned revisions and gkeep ui.py at 133b867, re-run the C2 counter; a Hyprland tag after v0.56.2, a GTK 4.24.x bump or a gkeep commit touching ui.py is the earlier trigger
ground: what the compositor does with the box once the floating branch has written it, what the client is allowed to do with the configure it receives, and what gkeep itself asks for
Lane: mado-shokunin. Round: 44.
assimilated-from: merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md (its sendWindowSize -> xdg configure chain, re-derived at the pinned sources; the refused staged files and their flips are in corpus/lessons/round-44.md)

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| Does the compositor tell the client the size it computed? | sendWindowSize, which builds a size to report and hands it to the toplevel | OBS (source) |
| Does the client have to take that size? | the xdg-shell configure description: a hint, and the configured state is not applied immediately | OBS (source) |
| What does GTK 4.24.1 do with a non-zero configure size? | the toplevel configure handler, which stores it in the next layout | OBS (source) |
| What does gkeep itself declare? | the app's own default size and the absence of a size request | OBS (source) |
| Does a gkeep window on this host actually take the 420x500 it is asked for? | the client's own layout, which no read verb of this lane can see | UNK on the host |

## §1 The compositor sends a size after it sets the box

**OBS** S164 - `sendWindowSize` derives the size it reports from the animated size rather than from the layout box it just wrote: `const auto REPORTSIZE = realToReportSize();` (Hyprland-Window.cpp:1741); when `force` is false and the pending report already equals the current one it returns early, so a repeated call with an unchanged size sends nothing.

**OBS** The xdg arm stores the serial the toplevel hands back: `m_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());` (Hyprland-Window.cpp:1753), while the X11 arm calls `configure` on the xwayland surface instead (line 1751). The two are alternatives in one if/else, so a Wayland client is told with a configure and an X11 client with an xcb-style configure, never both.

**OBS** The serial is resolved on the client's ack, newest first: `const auto SERIAL = std::ranges::find_if(m_pendingSizeAcks | std::views::reverse, [serial](const auto& e) { return e.first <= serial; });` (Hyprland-Window.cpp:1515), and the list is pruned up to that serial at line 1521. That makes the ack list a report of what the compositor believes the client has taken, not a record of what it drew.

**INF** So the compositor's own model of the window ends at "a configure with this size was sent and, later, acked". Nothing in the pinned handler reads a size back from the client.

## §2 What the configure is, and what the client may do with it

**OBS** S299 - the protocol calls the event a suggestion with a defined apply point: `This configure event asks the client to resize its toplevel surface or to change its state.` (xdg-shell.xml:1146); the next sentence says the configured state should not be applied immediately, and the event is closed by an `ack_configure` the client sends before it commits.

**OBS** The same description says the width and height are a hint in window-geometry coordinates (line 1150), and that zero means the client decides its own dimension (line 1154). A client is therefore free, under the protocol text, to answer a 420x500 configure with another size.

**OBS** S298 - the compositor side is a deferred send: `m_stateUpdate = g_pEventLoopManager->doLaterLock([this] { configure(); });` (Hyprland-XDGShell.cpp:633) is armed by `setSize` at line 357, which first stores `m_pendingApply.size = size;` (line 355). A second request before the loop runs reuses the scheduled serial instead of queueing a second configure (line 630).

**INF** A size change the compositor makes is therefore applied to its own state immediately and reaches the client only on the next event-loop turn, coalesced with any other configure the surface had pending. The client's later resize is the only thing that can disagree with it.

## §3 What GTK 4.24.1 does with the configure

**OBS** S300 - the GTK toplevel configure handler treats a maximized, fullscreen or tiled state, or an active resize, as a fixed size: `if (saved_size && !fixed_size && was_fixed_size)` (gdktoplevel-wayland.c:656); a non-zero width and height with a non-fixed state is stored as `next_layout.configured_width` and `configured_height` (lines 681-682), which is the size the toolkit will arrange to.

**OBS** The zero case is the saved-size path: a 0x0 configure after a maximize or fullscreen restores the saved width and height (lines 661-665), the behaviour the protocol text at line 1154 licenses.

**INF** For a floating, non-maximized, non-tiled toplevel the configure size is taken at face value by GTK, so a gkeep window under the host's rules should reach the layout stage at 420x500 - which is a statement about the toolkit, not a measurement of the host session.

## §4 What gkeep declares

**OBS** S301 - the application sets one default size and asks for nothing else: `window.set_default_size(420, 500) self.board = Board(window)` (gkeep-ui.py:476-477), on a `Gtk.ApplicationWindow` whose application id is `org.omarchy.gkeep` (line 449); the full file holds no `set_size_request` call at all.

**INF** The app's own request and the compositor's configure therefore ask for the same number, and the client declares no constraint that would hold it there: a 420x500 reported or arranged size cannot, by itself, say which of the two produced it. Only a window whose own default size differed from the rule's would separate them.

Census (recomputed by the C2 counter from the pinned receipts):

gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep
hyprland sendWindowSize xdg_setSize=1 x11_configure=1

## What this entry does not establish

- The size a gkeep window is actually arranged at on this host: the client's layout is not readable from the request socket, and no gkeep window was opened for this round.
- Whether GTK's arrangement follows a configure the client itself overrode: the handler quoted above runs before the toolkit's own size negotiation.
- Behaviour on any Hyprland other than 0.56.2 at efb5099, any GTK other than 4.24.1, or any gkeep commit other than 133b867.
