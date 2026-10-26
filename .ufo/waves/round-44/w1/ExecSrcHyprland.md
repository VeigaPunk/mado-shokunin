# ExecSrcHyprland — round 44 w1 — compositor-side fact table for C2

Status: **COMPLETE**. No tracked file edited; no counter/control/registration/reference touched.

## Files written (all inside the lane)
| path | what |
|---|---|
| `.ufo/waves/round-44/w1/ExecSrcHyprland/facts.md` | the deliverable: 30 located-quote facts (F1–F29, F26b) + 11 negatives (N1–N11) + a C2-relevance section |
| `.ufo/waves/round-44/w1/ExecSrcHyprland/verify-quotes.sh` | the verifier (41 checks) |
| `.ufo/waves/round-44/w1/ExecSrcHyprland/quotes-verified.txt` | its output, `CHECKS=41 FAILURES=0` |
| `.ufo/waves/round-44/w1/ExecSrcHyprland.md` | this report |

## Pins re-opened (sha256 verified in `quotes-verified.txt` §"pin hashes", both `OK`)
- `fetch/Hyprland-Window.cpp` 2966 lines — `d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded`
- `fetch/Hyprland-XDGShell.cpp` 980 lines — `d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0`
Both match `receipts/fetch-sha256.txt`. Nothing else read for the facts.

## Behaviour established (the chain, with the fact ids)
1. **Report size is the compositor's.** `realToReportSize()` returns
   `m_realSize->goal().clamp(Vector2D{0,0}, MAX)` for Wayland (F1, W:1687) and `clamp({1,1}, …)` for
   X11 (F2, W:1691). The client's own size never enters.
2. **Early return.** `sendWindowSize` bails when the pending report size is unchanged and (position
   unchanged or not X11) (F4, W:1743), so repeats of the same box send nothing.
3. **Two branches, one per backend.** X11: `m_xwaylandSurface->configure({REPORTPOS, REPORTSIZE})`
   (F5, W:1751). xdg: `m_pendingSizeAcks.emplace_back(m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor())`
   (F6, W:1753).
4. **setSize → scheduleStateApplication → scheduleConfigure → sendConfigure.** `setSize` stores
   `m_pendingApply.size` (F18, X:355) then `m_owner->scheduleConfigure()` (F19, X:357). Both schedulers
   latch on `m_stateUpdate` (F20 X:445; F22 X:629-635 minting the serial with
   `wl_display_next_serial`). The toplevel configure carrying the size is emitted later from the
   event loop: `sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr)` (F21, X:455);
   the xdg_surface configure carrying the serial is `sendConfigure(m_scheduledSerial)` (F23, X:642).
5. **Ack.** The client acks the serial; `setAckConfigure` drops serials older than the last seen
   (F24, X:602) and re-emits (F25, X:605) to `CWindow::onAck` (subscribed F14, W:184). `onAck`
   searches `m_pendingSizeAcks` **in reverse** for the newest entry with `serial <= acked`
   (F7, W:1515), drops out-of-range acks (F8, W:1517), erases every entry up to the match
   (F9, W:1521), returns early for X11 (F10, W:1523), and writes the acked size into the
   **wl_surface** pending state with `updated.bits.acked` set (F11 W:1526, F26b W:1527), then
   consumes `m_pendingSizeAck` (F12, W:1528).
6. **Where the acked size surfaces.** `getReportedSize()` returns `m_current.ackedSize` for Wayland
   (F13, W:1865), `m_reportedSize` for X11.
7. **Every `sendWindowSize` call site** (5 occurrences in W = def + 1 log line + 3 calls; 0 in X):
   W:809 inside `CWindow::onMap`'s `m_realSize->setCallbackOnBegin(...)` deferred by `doLater`
   — the **sole non-X11 path**, triggered whenever the layout moves the goal size (F15);
   W:1559 inside `onX11ConfigureRequest` forced (F16); W:2852 inside `unmanagedSetGeometry`
   forced, override-redirect only (F17). A second, direct `setSize` call bypasses `sendWindowSize`
   entirely on the initial commit: `m_xdgSurface->m_toplevel->setSize(predSize)` (F28, W:2732).
8. **Client commits a different size → Hyprland does nothing size-specific.** In these two files no
   code compares the committed size to the configured size. `m_realSize` is only re-derived from the
   layout (F29, W:1280 inside `clampWindowSize`, called from `commitWindow` W:2746: it clamps to the
   client's declared min/max, reading `m_realSize`, and writes via `layoutTarget()->setPositionGlobal`).
   The client's `set_window_geometry` is stored (F27, X:610) but only feeds popup positioning and
   min/max offsets; W never calls `geometry()` (N3). No error, no re-configure, no drift correction (N8).

## Negatives the sources force (full list N1–N11 in facts.md)
- `ackedSize` is written once (W:1526) and read once (W:1865) across the whole pin set; never
  compared against `m_realSize` (N2).
- `m_pendingSizeAcks` has no cap and no timeout — 4 occurrences in W, the only mutations being the
  `emplace_back` and the erase-on-ack (N4). A client that never acks leaks entries for the life of
  the window.
- **Coalescing wrinkle for C2** (N9): two `setSize` calls before the loop drains return the *same*
  serial (X:631 latch) and push *two* entries with that serial; the reverse search takes the later
  entry and the erase retires both. So the ack of a coalesced configure maps to the newest size —
  but the "newest `<=`" rule also means an ack can satisfy an entry P whose serial is smaller than the
  size now pending in `m_pendingApply`.
- **The acked-size promotion is out of pin scope** (N11): `m_pending.ackedSize` → `m_current.ackedSize`
  and the `updated.bits.acked` flag are handled by the wl_surface commit handler in the compositor
  surface resource, which is **not** a round-44 pin. These pins cannot order the ack write against the
  xdg commit; `updated.bits.acked` has 1 hit in W (the write) and 0 in X.
- `m_pendingApply`'s default `size` is declared in an unfetched header, so a configure emitted by
  `setMaximized`/`setFullscreen` before any `setSize` carries a size these files do not establish (N6).
- Neither file mentions GTK, gkeep, `set_default_size`, 420 or 500 (N7, grep 0/0) — the
  compliance half of C2 is not in this pin pair.
- `sendWindowSize` is not synchronous: Wayland only enqueues two `doLaterLock` callbacks (N10, X:448/633).

## Evidence actually run
```
cd .ufo/waves/round-44/w1/ExecSrcHyprland
TMPDIR=/fast/scratch/hyaku/mado-r44/ExecSrcHyprland bash verify-quotes.sh
→ CHECKS=41 FAILURES=0        (saved: quotes-verified.txt)
```
Every F-row is checked as: the quote literally `grep -nF`-occurs in the pin file, the cited line is
among the hits, and the quote is present in `facts.md`. All 30 quotes are ≤ 11 words (limit 25).
All `file:line` locators are grep-computed, never typed; the 11 function locators are checked too.
Two corrections were forced by the verifier while writing: `getReportedSize` is at W:1861 (not
1860), and my first F26 claimed W:1515-style promotion for X:519 — that row was rewritten because
X:519 promotes `CXDGSurfaceResource` state (geometry), not the wl_surface `ackedSize`, which is now
N11. Holds no claim that the pins do not support.

## Host / tool state
No host command run beyond file reads; no `hyprctl` needed (no runtime claim made). Scratch dir
`/fast/scratch/hyaku/mado-r44/ExecSrcHyprland` used only as TMPDIR for the verifier, 0 bytes,
removed at exit. No tool installed this seat; no pacman.

## Risks / notes for the integrator
1. **C2's `xdg_setSize=1 x11_configure=1` constants are structurally supported** (exactly one branch
   runs per `sendWindowSize`, F5/F6), but they are *per-call* facts, not per-session counts — any
   counter that derives a count must define its window of observation, since the F4 early return
   suppresses repeats and N9 coalesces.
2. `m_pendingSizeAcks` unbounded growth (N4) is a real compositor-side defect worth a lesson entry
   if it is not already known — it is not part of C2 and I did not widen scope to chase it.
3. N11 is the one gap an integrator may need: to state the ack→current ordering, pin
   `src/protocols/core/Compositor.cpp` (or the surface-resource header) next round.
4. Suggested registry rows unchanged from the task's provisional ids: S298 = XDGShell.cpp.
