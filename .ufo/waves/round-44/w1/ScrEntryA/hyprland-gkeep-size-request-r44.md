# What the compositor sends the gkeep client after it sets the box: the report size, the configure and its serial, the ack, xdg-shell 1.49's terms, GTK 4.24.1's handler, and gkeep's own declaration

source: S164 - hyprwm/Hyprland src/desktop/view/Window.cpp @ efb50993780079460b0cbed1363e2166a2de1d9f (v0.56.2), held row - CWindow::sendWindowSize, realToReportSize, onAck and getReportedSize
source: S298 - hyprwm/Hyprland src/protocols/XDGShell.cpp @ efb50993780079460b0cbed1363e2166a2de1d9f (v0.56.2) - CXDGToplevelResource::setSize and CXDGSurfaceResource::scheduleConfigure
source: S299 - wayland-protocols 1.49 stable/xdg-shell/xdg-shell.xml - the configure event and ack_configure: what the numbers mean and what the client owes
source: S300 - GTK 4.24.1 gdk/wayland/gdktoplevel-wayland.c - the toplevel configure handler
source: S301 - gkeep 133b867 gkeep/ui.py (full file) - the application id, the window type and the default size
verified-at: 2026-10-26
recheck: 30d - re-pull the five documents at their pinned revisions and re-run the quotation check; a Hyprland release after v0.56.2, a GTK 4.24.x change to gdktoplevel-wayland.c, wayland-protocols 1.50, or a gkeep commit touching ui.py is the earlier trigger
ground: what the compositor sends the gkeep client once the rule's box is set, what the client may do with it, what GTK and gkeep actually do, and which links remain unobserved
Lane: mado-shokunin. Round: 44.
amends: merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md - its client half is re-derived here from five pinned documents at the host's own revisions; its "settled" and "complete" wording is not adopted, and the live state stays UNK

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| Does the rule's box reach a value the compositor can send? | the round-43 entry's target, window and animated-size sections, at the same commit | OBS (source) in that entry; INF for the join to this one |
| Which number does the compositor send a wayland client? | the animation goal, clamped, taken before the send | OBS |
| When is a send issued, and when is it skipped? | the animated-size begin callback, and the unchanged-size early return | OBS |
| When does a sent size become an acknowledged size? | the pending-serial list and the ack handler | OBS |
| May a client keep a size other than the configure's? | the 1.49 configure text: hint wording, zero-means-client rule, ack duty | OBS (text); the conformance of ignoring a non-zero hint is UNK |
| What does GTK 4.24.1 do with a non-zero configure size? | the toplevel configure handler | OBS |
| What does gkeep ask for? | ui.py: an application window, a 420x500 default, no size request | OBS |
| What size is a live gkeep window drawn at on this host? | nothing in these five documents | UNK |

## §1 Where round 43 stopped: the goal box

**INF** `corpus/knowledge/hyprland-gkeep-geometry-r43.md` stops at the box, not at the client: the host's three rules declare a floating, centred 420x500 box for the class, the floating algorithm's first-map branch evaluates the stored size expression into the layout target, the target hands the box to the window, and the animated size keeps that value as its GOAL - which is the number `hyprctl clients -j` prints as `size` (that entry's §2 and §3). No request-socket read exposes the animated CURRENT value, so "the rule applied" and "the window is drawn at 420x500" were already different statements there.

**INF** This entry takes the next link only: with the GOAL box in hand, what the compositor sends the wayland client, what the client may do with it, what GTK and gkeep do, and what remains unobserved. The rule text, the anchored match and the floating branch are not re-derived here.

## §2 Report size

**OBS** The number sent is derived from the animation goal, not from the drawn frame: for a wayland window the goal is clamped to non-negative and returned as is; for an X11 window it is clamped to at least 1x1 and, when `xwayland:force_zero_scaling` is on, multiplied by the monitor scale and rounded (Hyprland-Window.cpp:1685-1702).

**OBS** A send is queued when the animated size begins a transition - a begin-callback posts it to the event loop - and is skipped when the pending reported size and the reported position are unchanged, unless the call is forced (Hyprland-Window.cpp:800-812, 1743-1744).

**INF** During an open or resize animation the client is told the destination, not the frame currently on screen; the GOAL-versus-CURRENT split round 43 found in the read path sits here in the write path too.

## §3 The configure and its serial

**OBS** The send branches once: an X11 window gets one xwayland configure carrying the reported position and size (Hyprland-Window.cpp:1750-1751), while a wayland window gets the toplevel's `setSize` and the returned serial is stored beside the integer-floored size in a pending list (lines 1752-1753).

**OBS** S164 - the wayland arm keeps the configure serial beside the size it asked for, in the pending list the acknowledgement later trims: `else if (m_xdgSurface && m_xdgSurface->m_toplevel) m_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());` (Hyprland-Window.cpp:1752); the pair is the only record in the pinned function that ties the sent size to the serial that came back with it.

**OBS** The toplevel resource latches the size into its pending apply state and asks its surface for a configure (Hyprland-XDGShell.cpp:354-357).

**OBS** S298 - the toplevel's `setSize` records the size, schedules the state application and returns the configure serial: `uint32_t CXDGToplevelResource::setSize(const Vector2D& size) { m_pendingApply.size = size; scheduleStateApplication(); return m_owner->scheduleConfigure(); }` (Hyprland-XDGShell.cpp:354); the surface hands back the serial already pending when a state update is queued, and otherwise arms a later send and takes a fresh display serial (lines 629-637), which the send then uses (lines 640-642).

**INF** One serial covers a batch of latched surface state, so an acknowledgement names the batch, not the individual size call; a second size change while a configure is pending rides the serial already issued.

## §4 The ack

**OBS** The surface's ack event is wired straight into the window's ack handler (Hyprland-Window.cpp:184).

**OBS** The handler picks the newest pending entry whose serial is not greater than the acked one, drops that entry and every older one, and for a non-X11 window stores its size as the surface's pending `ackedSize` and sets the acked bit; an ack older than every pending entry is ignored, and an X11 window stops after the trim (Hyprland-Window.cpp:1514-1528).

**OBS** The acknowledged size is what `getReportedSize()` returns for a wayland window; the X11 branch returns the last configured size (Hyprland-Window.cpp:1861-1866).

**UNK** No caller of `getReportedSize()` appears in the five pinned documents, so which compositor decision consumes the acknowledged size is outside this evidence.

**INF** The ack moves the compositor's record of the client's size from "what I sent" to "what the client reported back", one batch at a time; it does not by itself change the animation goal, and it is not a read of the drawn size.

## §5 What the protocol lets the client do

**OBS** The configure event asks the client to resize its toplevel surface or to change its state, and says the configured state must not be applied immediately (xdg-shell.xml:1144-1148).

**OBS** S299 - the size in a configure is a hint in window geometry coordinates: `The width and height arguments specify a hint to the window about how its surface should be resized in window geometry coordinates.` (xdg-shell.xml:1150); a zero width or height means the client decides its own dimension (lines 1154-1157).

**OBS** The only hard duty is the acknowledgement: a client that commits in response must ack before the commit with that configure's serial (xdg-shell.xml:562-566), may answer several received events with the last one (line 572), and may discard all but the last (line 615).

**OBS** Window geometry is the client's own declaration, clamped to the bounding rectangle of the surface and its subsurfaces (xdg-shell.xml:541-552).

**INF** The pinned 1.49 text obliges the client to answer, not to adopt the hinted size: it states no requirement that the surface or the window geometry equal the configure's numbers, and the zero rule hands the dimension back to the client. Whether a conformant client may ignore a non-zero hint is UNK - the text neither permits nor forbids it.

## §6 What GTK does

**OBS** GTK's handler reads the pending width and height and marks the size fixed when the new state is maximized, fullscreen or tiled, or when the configure carries the compositor's `resizing` state (gdktoplevel-wayland.c:633-645, 743-745).

**OBS** A configure of 0x0 means the client sets the size; when it arrives while leaving maximize or fullscreen, GTK restores the size it saved beforehand (gdktoplevel-wayland.c:647-660). The saved size is the current surface size minus shadows, kept only outside a fixed state and above the 1x1 guard (lines 197-212).

**OBS** A non-zero configure is adopted: GTK saves the current size for a later 0x0, asks the layout to constrain, records the configure's numbers as the next layout's configured size and requests a layout (gdktoplevel-wayland.c:662-693).

**OBS** S300 - the handler writes the configure's numbers into the next layout and always acks last: `wayland_surface->next_layout.configured_width = width; wayland_surface->next_layout.configured_height = height;` (gdktoplevel-wayland.c:681); the else arm clears the configured size to zero (lines 686-689), and the handler ends by acking the pending serial (line 706).

**INF** A GTK toplevel does not keep a size of its own against a non-zero configure: the numbers become its next layout's configured size, which is toolkit policy - §5 shows the protocol leaves that choice to the client.

## §7 What gkeep asks for

**OBS** The app declares its identity and builds a plain application window with decorations off, a 420x500 default and the board as its child (gkeep-ui.py:449, 474-479).

**OBS** S301 - the window's only size statement is a default, stated once at startup: `window = Gtk.ApplicationWindow(application=self, title="gkeep") window.set_decorated(False) window.set_default_size(420, 500) self.board = Board(window)` (gkeep-ui.py:474); the application id is declared at line 449 of the same file.

**OBS** The pinned full file contains no `set_size_request` call (the census below counts 0), so gkeep states a default size and never a hard size.

**INF** Nothing in gkeep's own bytes resists a configure: its only window-size statement is a default, and the size request that GTK would treat as a floor is absent; what the toolkit then does is §6.

## §8 What is and is not observed

**UNK** No gkeep window was open while this entry was written, and nothing here observes one: whether a gkeep window is mapped, what size it reports to the compositor, and whether it acks are all unobserved. Every statement above is a source read at a pinned revision (Hyprland efb5099, wayland-protocols 1.49, GTK 4.24.1, gkeep 133b867), not a client run.

**OBS** The last host census on record held four mapped clients, none floating and none gkeep, and the geometry tool answered `NO_MATCHING_CLIENT` when it ran (`.ufo/waves/round-43/receipts/live-geometry-host.txt`); the five pins do not change that.

**INF** What a live window would show is a prediction, not a result: the chain says a 420x500 goal box is sent, GTK would adopt it as its next configured size, and gkeep's 420x500 default would not be what decides it. The prediction is untested here.

## Census (computed from the two client-side receipts by the round-44 counter)

gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep
hyprland sendWindowSize xdg_setSize=1 x11_configure=1

## What this entry does not establish

- The drawn size of a gkeep window at any moment, on this host or elsewhere; §8 keeps that UNK.
- Whether GTK's adopted configure size survives gkeep's own layout: the pins hold the toolkit handler and the app's startup, not a run of either.
- Which compositor decision consumes the acknowledged size: no caller of `getReportedSize()` is in the pins.
- Behaviour on any Hyprland other than 0.56.2 at efb5099, any GTK other than 4.24.1, any wayland-protocols other than 1.49, or any gkeep commit other than 133b867.
- The staged `gkeep-client-size-request-r12.md` framing: this entry amends it and does not adopt its "settled"/"complete" wording; which staged files are admitted or refused is recorded in the round-44 lesson's Gate, not here.
