source: S189 — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp — `CEventManager::postEvent`, `CEventManager::flushClient` — commit `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2)
source: S201 — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp — `IPC::socketListener`, `IPC::parseIPC` — tag `0.15.0`
source: S212 — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/workspaces.cpp — `Workspaces::registerIpc` — tag `0.15.0`
verified-at: 2026-10-25
recheck: 90d
ground: the event-socket half of the bar's contract — `knowledge/arc-synthesis.md` §6 gap-ledger row "waybar module text" and the `corpus/README.md` Frontier bullet "Rendered UI, Waybar module text, Walker socket protocol …"

# What happens to an event client that stops reading

Lane: mado-shokunin. Round 37, re-grounding of a package entry (see `## Assimilation`). Substrates READ-ONLY.

**OBS** Evidence is the bytes of three source files as re-opened by the lane on 2026-10-25 (receipts `.ufo/waves/round-37/fetch/S189.bin` sha256 `eea605df…`, `S201.bin` `799bf02f…`, `S212.bin` `1e19d926…`); no socket was connected and no event was observed.

## §1 The compositor side — Hyprland v0.56.2 `EventManager.cpp` (S189)

**OBS** The event socket is `.socket2.sock` under the instance path, and every accepted client socket is non-blocking (S189:21; S189:73 `SOCK_CLOEXEC | SOCK_NONBLOCK`).

**OBS** Each accepted client gets its own `SClient` entry with its own `events` queue; one formatted string per event is shared by all the clients' queues (S189:89-93, :170, :180).

**OBS** The per-client cap is explicit in `postEvent` (S189:169): `const size_t MAX_QUEUED_EVENTS = 64;`

**OBS** The check runs once per posted event, before that event is queued: a client already holding 64 or more unwritten events is removed, not throttled, and the event that found it full is not queued for it (S189:172-177): `Log::logger->log(Log::ERR, "Socket2 fd {} overflowed event queue, removing", it->fd.get());`

**INF** The queue only grows when `write` reports `EAGAIN`/`EWOULDBLOCK` (S189:149-150), so the 64 counts events beyond what the kernel socket buffer already accepted; the kernel buffer size is not in these bytes.

**OBS** After queueing, `postEvent` writes at once; if bytes remain and the queue was empty before, it arms `WL_EVENT_WRITABLE` on the client's event-loop source, and that callback flushes again or removes the client (S189:180-188, :105-109, :88).

**OBS** Partial writes are resumed, not restarted: `writeOffset` advances by the bytes written and the event stays at the head until it is finished (S189:136-146); `EAGAIN`/`EWOULDBLOCK` leaves it queued (S189:149-150) and `EINTR` retries (S189:152-153).

**OBS** Any other write result — an error, or `write` returning 0 — logs `"Socket2 fd {} failed writing event: {}"` at ERR and the client is removed (S189:155-156, :182-183, :108-109).

**OBS** A client the event loop reports as hung up or in error is removed with a DEBUG line `"Socket2 fd {} hung up"` (S189:99-102).

**OBS** While the compositor is shutting down, `postEvent` drops each event with a WARN line `"Suppressed (shutting down) event of type {}, content: {}"` instead of queueing it (S189:164-166).

**OBS** Event data is cut to 1024 bytes before framing as `EVENT>>DATA\n` (S189:128), so one framed line can exceed 1024 bytes by the event name, `>>` and the newline.

**INF** Removal erases the `SClient`, which owns the socket as a `CFileDescriptor` (S189:73, :90, :123); that the descriptor is closed, so the client reads end-of-file, follows from that ownership, but the `CFileDescriptor` destructor is not in these bytes.

## §2 The client side — Waybar 0.15.0 (S201, S212)

**OBS** All of Waybar's Hyprland modules reach the compositor through one `IPC` singleton (S201:72-75); the workspaces module binds it in its constructor (S212:21).

**OBS** The singleton opens one blocking socket2 connection on one thread, started once from its constructor (S201:48, :89, :98, :105); S201:105 is the only socket2 `connect` in the file, so these bytes contain no reconnect path.

**OBS** The reader reads lines with `fgets` into a 1024-byte buffer (S201:115, :117): `std::array<char, 1024> buffer;  // Hyprland socket2 events are max 1024 bytes`

**OBS** That comment does not describe the compositor's framing: S189:128 caps the data alone at 1024 bytes, and the framed line adds the event name, `>>` and a newline (S201:115; S189:128).

**INF** `fgets` stores at most one byte less than the size it is given (C library semantics, not in these bytes), so each read returns at most 1023 bytes (S201:117), and a line longer than that is split across reads: the first piece is dispatched under its event name with cut data, and the rest arrives as a separate message whose text before the first `>` will normally match no registered event name (S201:124-125, :142-147).

**OBS** After every line, and after every `fgets` that returns null, the reader sleeps 1 ms; a null return is not logged (S201:119-122, :136).

**OBS** Handlers run on the reader thread: `parseIPC` calls each matching handler's `onEvent` synchronously while holding `callbackMutex_` (S201:129, :143-148).

**OBS** The workspaces module subscribes to 12 events unconditionally — `workspacev2`, `activespecial`, `createworkspacev2`, `destroyworkspacev2`, `focusedmonv2`, `moveworkspacev2`, `renameworkspace`, `openwindow`, `closewindow`, `movewindowv2`, `urgent`, `configreloaded` (S212:804-815); the first is `m_ipc.registerForIPC("workspacev2", this);`

**OBS** Two more are conditional: `windowtitlev2` when `windowRewriteConfigUsesTitle() || m_taskbarWithTitle` (S212:817-821), and `activewindowv2` when `m_updateActiveWindow`, logged as "'update-active-window' is set" (S212:823-827) — 12 to 14 subscriptions in all.

**OBS** The workspaces handler takes `m_mutex`, which the UI thread's `doUpdate` also takes (S212:326, :126-127), and several of its event paths make synchronous socket1 requests through `getSocket1JsonReply` — `onWorkspaceCreated` (S212:393-394), `onWorkspaceMoved` (S212:433, :442), `onMonitorFocused` (S212:480), `onWindowTitleEvent` (S212:590) — each a connect/write/read round trip (S201:178-234).

## §3 The consequence for this lane's bar

**INF** The bar is a socket2 client with a single reader thread, so anything that holds that thread — a slow socket1 round trip inside a handler, `m_mutex` held by the UI thread, or the fixed 1 ms per line — lets events pile up first in the kernel buffer and then in the compositor's per-client queue; with 64 queued, the next event removes the client (S201:136, :143-148; S212:326, :393; S189:172-177).

**INF** After removal the reader gets end-of-file and loops on sleep-and-retry with no log line and no reconnect, so every handler on the singleton — `hyprland/workspaces` among them — stops receiving events while the bar keeps running; in these bytes the only record of the removal is the compositor's ERR line (S189:175; S201:72-75, :105, :119-121).

**UNK** Whether the cap was ever reached on this host, and whether that line can be seen: see [event-queue-observability-r37.md](event-queue-observability-r37.md).

## Assimilation

- **Origin:** package entry `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/event-delivery-limits-r26.md` (57 lines, sha256 `debe52a9a233bed3934d463812c62262172dce1994b97a804dd7f4c58d93038a`; "corpus-expansion-2, round 2", verified-at 2026-10-23), read-only. Package ids renumbered by document (`.ufo/waves/round-37/assimilation/renumber-map.md`): staged S214 (`workspaces.cpp`) → S212; merge-note S187 (`EventManager.cpp`) → S189; merge-note S188 (`backend.cpp`) → S201. The merge note is folded into the three `source:` lines.
- **Kept:** the 64-event cap and its quote; removal (not throttling) on overflow and its log line; partial-write resume via `writeOffset`, `EAGAIN`/`EWOULDBLOCK` keep, `EINTR` retry; other write failures log and end the client; events dropped with a warning during shutdown; the bar is an event client and its compositor-event feed can be lost with the error logged compositor-side only.
- **Corrected:** "the lane's event socket" → the compositor's socket2 (S189:21); the overflow condition stated exactly (checked per posted event, before queueing; S189:172-177); "twelve event subscriptions" → 12 unconditional (S212:804-815) plus 2 conditional (S212:821, :827); "the backend reads at most 1024 bytes per event, matching the compositor's 1024-character truncation" → the compositor caps the data alone at 1024, so a framed line can exceed the buffer, and `fgets` into it takes at most 1023 bytes per read, so long lines split (S201:115-117, S189:128; the 1023 is C library semantics, tagged INF); `recheck:` reduced to a cadence; `ground:` re-pointed — the package's "F1" and "arc-synthesis §6 U1" name no row in the lane's `arc-synthesis.md` §6.
- **Dropped:** "a blocked custom-module producer can therefore cost the bar its whole compositor-event feed" — no custom-module code is in S189, S201 or S212, so the bytes cannot carry the cause; replaced by the stall routes the bytes do show (§3). The §2 UNK about the host's log is replaced by the pointer to `event-queue-observability-r37.md`, which owns host observation.
- **Added from the same bytes:** non-blocking client sockets (S189:73), hang-up removal (S189:99-102), the single shared reader with no reconnect and silent end-of-file (S201:48, :72-75, :105, :119-122), the 1 ms sleep per line (S201:136), synchronous handlers and their socket1 round trips (S201:143-148; S212:326, :393-394, :433, :442, :480, :590).
