# C2 compositor-side fact table — Window.cpp + XDGShell.cpp

Pins (re-hashed this seat, 2026-10-26):
- `W` = `.ufo/waves/round-44/fetch/Hyprland-Window.cpp`, 2966 lines,
  sha256 `d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded`
  (= `receipts/fetch-sha256.txt`; URL raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp)
- `X` = `.ufo/waves/round-44/fetch/Hyprland-XDGShell.cpp`, 980 lines,
  sha256 `d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0`
  (same commit, src/protocols/XDGShell.cpp)

Every `file:line` below is `grep -n`-computed, not typed. Every quote is verified by
`verify-quotes.sh` (output: `quotes-verified.txt`, PASS on all rows).

---

## A. Size the compositor reports (Window.cpp)

| # | claim | quote (<=25 words) | file:line | sha256 (prefix) |
|---|---|---|---|---|
| F1 | Wayland branch of `realToReportSize`: the report size is the layout's goal size clamped to floor **0,0** — the client's own size is never consulted | `return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);` | W:1687 (fn `Vector2D CWindow::realToReportSize()` at W:1685) | d735d454… |
| F2 | X11 branch uses floor **1,1** instead; the two backends do not share a floor | `const auto  REPORTSIZE = m_realSize->goal().clamp(Vector2D{1, 1}, Math::VECTOR2D_MAX);` | W:1691 | d735d454… |
| F3 | `sendWindowSize` takes a `force` flag; a non-forced call is the common path | `void CWindow::sendWindowSize(bool force) {` | W:1732 | d735d454… |
| F4 | Early return when the pending reported size is unchanged **and** (position unchanged **or** not X11) — i.e. a Wayland window whose goal size did not move re-sends nothing | `if (!force && m_pendingReportedSize == REPORTSIZE && (m_reportedPosition == REPORTPOS \|\| !m_isX11))` | W:1743 | d735d454… |
| F5 | X11 branch: configure sent immediately on the XWayland surface | `m_xwaylandSurface->configure({REPORTPOS, REPORTSIZE});` | W:1751 | d735d454… |
| F6 | xdg branch: `setSize(REPORTSIZE)` returns a serial, and `(serial, REPORTSIZE.floor())` is appended to `m_pendingSizeAcks` | `m_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());` | W:1753 | d735d454… |

## B. Ack bookkeeping (Window.cpp)

| # | claim | quote | file:line | sha256 |
|---|---|---|---|---|
| F7 | `onAck` scans `m_pendingSizeAcks` **in reverse** and takes the newest entry whose serial is `<=` the acked serial | `const auto SERIAL = std::ranges::find_if(m_pendingSizeAcks \| std::views::reverse, [serial](const auto& e) { return e.first <= serial; });` | W:1515 (fn at W:1514) | d735d454… |
| F8 | Ack for a serial older than every pending entry is dropped (no state write) | `if (SERIAL == m_pendingSizeAcks.rend())` | W:1517 | d735d454… |
| F9 | All entries up to and including the matched serial are erased (coalesced/older configures retired) | `std::erase_if(m_pendingSizeAcks, [&](const auto& el) { return el.first <= SERIAL->first; });` | W:1521 | d735d454… |
| F10 | X11 returns before any surface write, so X11 never stores an acked size this way | `if (m_isX11)` | W:1523 | d735d454… |
| F11 | The acked size is written into the **pending** state of the wl_surface, with an `acked` dirty bit | `m_wlSurface->resource()->m_pending.ackedSize` | W:1526 | d735d454… |
| F12 | The local `m_pendingSizeAck` is consumed after the write | `m_pendingSizeAck.reset();` | W:1528 | d735d454… |
| F13 | `getReportedSize()` for Wayland returns `m_current.ackedSize`; X11 returns `m_reportedSize` | `return m_wlSurface->resource()->m_current.ackedSize;` | W:1865 (fn at W:1861) | d735d454… |
| F14 | Window subscribes `onAck` to the xdg_surface ack event in the constructor | `m_listeners.ack              = m_xdgSurface->m_events.ack.listen([this](uint32_t d) { onAck(d); });` | W:184 | d735d454… |

## C. Where sendWindowSize is called (every call site)

| # | call site | enclosing function | quote at site | file:line | sha256 |
|---|---|---|---|---|---|
| F15 | W:809 | `void CWindow::onMap()` (W:759) — inside `m_realSize->setCallbackOnBegin(...)`, deferred by `doLater`, guarded by `!m_isMapped \|\| isX11OverrideRedirect()`. **This is the Wayland layout-resize entry point** (non-forced). | `sendWindowSize();` | W:809 | d735d454… |
| F16 | W:1559 | `void CWindow::onX11ConfigureRequest(CBox box)` (W:1544) — forced, on the "not floating / fullscreen / dragging / suppressed" branch | `sendWindowSize(true);` | W:1559 | d735d454… |
| F17 | W:2852 | `void CWindow::unmanagedSetGeometry()` (W:2839) — forced, X11 override-redirect path | `sendWindowSize(true);` | W:2852 | d735d454… |

No other `sendWindowSize` occurrence exists in W (grep count 5: def at 1732, one log line at 1735, calls 809/1559/2852)
and the symbol does not occur in X at all.

## D. setSize -> scheduleStateApplication -> scheduleConfigure -> sendConfigure

| # | claim | quote | file:line | sha256 |
|---|---|---|---|---|
| F18 | `setSize` stores the size in `m_pendingApply.size`, schedules the toplevel configure, then returns the xdg_surface serial | `m_pendingApply.size = size;` | X:355 (fn at X:354) | d90b534c… |
| F19 | `setSize` tail returns `m_owner->scheduleConfigure()` (same shape as the state setters) | `return m_owner->scheduleConfigure();` | X:357 | d90b534c… |
| F20 | `scheduleStateApplication` latches: a second call while `m_stateUpdate` is live is a no-op | `if (m_stateUpdate)` | X:445 (fn at X:443) | d90b534c… |
| F21 | The toplevel configure carrying the size is sent later, from the event loop, with `m_pendingApply.size` **as it is at that moment** and the accumulated state array | `m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);` | X:455 | d90b534c… |
| F22 | `scheduleConfigure` latches the same way and otherwise mints a fresh display serial | `m_scheduledSerial = wl_display_next_serial(g_pCompositor->m_wlDisplay);` | X:635 (fn at X:629) | d90b534c… |
| F23 | The xdg_surface configure (serial only) is what the client acks; it is sent in `configure()` | `m_resource->sendConfigure(m_scheduledSerial);` | X:642 (fn at X:640) | d90b534c… |

Ordering consequence: `setSize` schedules the **toplevel** configure first and the **surface**
configure second (X:356-357), both as `doLaterLock` callbacks; the serial handed back to
`Window.cpp` is minted at schedule time (X:635), not at send time.

## E. Client side of the handshake inside the pins

| # | claim | quote | file:line | sha256 |
|---|---|---|---|---|
| F24 | Ack configure is filtered: serial older than the last seen is ignored, then re-emitted | `if (serial < m_lastConfigureSerial)` | X:602 | d90b534c… |
| F25 | The accepted serial is re-emitted on `m_events.ack` (the signal Window.cpp F14 consumes) | `m_events.ack.emit(serial);` | X:605 | d90b534c… |
| F26 | On surface commit the **xdg surface's** pending state (window geometry) becomes current. This is *not* the acked-size promotion: `m_current`/`m_pending` here are `CXDGSurfaceResource`'s own state | `m_current = m_pending;` | X:519 | d90b534c… |
| F26b | The acked size is written to the **wl_surface** resource's pending state and flagged dirty on `updated.bits.acked`; nothing in these two files clears or reads that bit | `m_wlSurface->resource()->m_pending.updated.bits.acked = true;` | W:1527 | d735d454… |
| F27 | The client's `set_window_geometry` is stored but only feeds popup positioning / min-max offsets, never the toplevel size | `m_pending.geometry = {x, y, w, h};` | X:610 | d90b534c… |
| F28 | On the **initial** commit of a Wayland toplevel, Hyprland calls `setSize` directly with the layout-predicted size, bypassing `sendWindowSize`/`m_pendingSizeAcks` | `m_xdgSurface->m_toplevel->setSize(predSize);` | W:2732 | d735d454… |
| F29 | On later commits, a floating non-fullscreen Wayland window is only re-clamped to the client's declared min/max — the clamp reads `m_realSize`, not the client's buffer | `const Vector2D NEWSIZE  = REALSIZE.clamp(minSize.value_or(Vector2D{MIN_WINDOW_SIZE, MIN_WINDOW_SIZE}), MAX);` | W:1280 (fn `clampWindowSize` at W:1277, called from `commitWindow` at W:2746) | d735d454… |

**What Hyprland does when the client commits a different size:** nothing size-specific. In
these two files, no code compares the committed geometry against the configured size; `m_realSize`
is only ever re-derived from the layout (`layoutTarget()->setPositionGlobal` at W:1286 inside
`clampWindowSize`) and the animated-variable callbacks. A client that keeps its own size keeps
being sent Hyprland's box on the next goal-size change; there is no drift correction and no
protocol error.

## F. What these sources do NOT say (negative facts)

| # | negative | basis |
|---|---|---|
| N1 | No path writes `m_realSize` from a client-supplied size; every write is layout/`setPositionGlobal`/`warp` | grep `m_realSize` in W: 26 hits, none assigns from `m_current.geometry` |
| N2 | `ackedSize` is written exactly once (W:1526) and read exactly once (W:1865); it is never compared to `m_realSize` | `grep -rn ackedSize .` over the whole pin set: 2 hits |
| N3 | `Window.cpp` never reads the toplevel's committed geometry for sizing — `geometry()` has 0 hits in W | `grep -n "geometry()" Hyprland-Window.cpp` → empty |
| N4 | `m_pendingSizeAcks` has no cap and no timeout: the only mutation besides the `emplace_back` (W:1753) is the erase on ack (W:1521). A client that never acks leaves entries forever | 4 occurrences in W: 1515, 1517, 1521, 1753 |
| N5 | There is no symbol `reportedSize`; the field is `m_reportedSize`; it is refreshed from `m_pendingReportedSize` at W:837, W:2544, W:2740 and from the X11 request box at W:1549/W:1574 — never from a Wayland commit | `grep -n reportedSize` in W |
| N6 | The default value of `m_pendingApply.size` is not in these pins (the toplevel header is not fetched), so a configure emitted by `setMaximized`/`setFullscreen` before any `setSize` carries a size these files do not establish | X has no `m_pendingApply` initializer; declaration lives in an unfetched header |
| N7 | Neither file mentions GTK, gkeep, `set_default_size`, or 420x500; the behaviour here is application-agnostic | `grep -in "gtk\|gkeep\|default_size"` on both → empty |
| N8 | No code path re-sends the configure when a client ignores/refuses one, and no error is raised for a non-conforming commit | F29 + absence of any error call in the commit path X:518-547 |
| N9 | Coalescing detail worth carrying into C2: two `setSize` calls before the event loop drains return the **same** serial (X:631 latch) and push **two** entries with that serial; the reverse search (F7) picks the later (newest) entry and the erase (F9) retires both | X:630-636 + W:1515-1521 |
| N10 | `sendWindowSize` is not synchronous: on Wayland it only enqueues two `doLaterLock` callbacks, so an observation taken before the loop drains cannot see the configure | X:448, X:633 |
| N11 | The `m_pending.ackedSize` -> `m_current.ackedSize` promotion and the `updated.bits.acked` consumption live in the wl_surface commit handler (compositor surface resource), which is **not in the pinned files**; these pins therefore cannot fix the ordering of the ack write relative to the xdg commit, nor what reads the dirty bit | `updated.bits.acked` has exactly 1 hit in W (the write at W:1527) and 0 in X |

## G. What this supports for C2 (and what it does not)

Supports:
- The claim that Hyprland has **one** xdg size path (`setSize`) and **one** X11 path
  (`configure`) inside a single `sendWindowSize` (F5/F6): the xdg branch is guarded by
  `m_xdgSurface && m_xdgSurface->m_toplevel`, the X11 branch by `m_isX11 && m_xwaylandSurface`,
  so a given window takes exactly one of them per call.
- The claim that a maximized/fullscreen box reaches the client as a **configure the client must
  ack** (F6/F18-F25): the serial that `setSize` returns is the same serial the client acks, and
  the acked size only becomes `getReportedSize()` after the surface commit (F13, N11).
- The claim that a client's own chosen size is not authoritative (N1-N3, F29): Hyprland keeps
  `m_realSize` from the layout and re-reports it, so a GTK window that ignores the configure is
  not resized by Hyprland to its own default size.

Does not establish (must not be quoted as source fact):
- Any per-session **count** of `setSize`/`configure` calls: the number depends on how often the
  layout moves `m_realSize->goal()`, which is outside these files, and the F4 early return
  suppresses all repeats of the same size.
- That a configure was actually *delivered*: F23/F24 only show it is enqueued (N10).
- Any GTK/gkeep-specific behaviour (N7): the size request/compliance half of C2 must come from
  the xdg-shell spec pin, the GTK pin, and the gkeep pin.
