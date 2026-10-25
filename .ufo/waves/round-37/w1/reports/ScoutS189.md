# ScoutS189 — Hyprland v0.56.2 socket2 delivery path (S189), re-opened

Seat: L1Mado37-2.ScoutS189 (scout, read-only). Date: 2026-10-25.
No tool installed or upgraded. No socket connected. hyprctl read verbs only.
Scratch: /dev/shm/mado37-ScoutS189/EventManager.cpp (re-fetch).

## 0. Receipt re-open — PASS

```
$ curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp -o /dev/shm/mado37-ScoutS189/EventManager.cpp
curl rc=0
$ cmp EventManager.cpp .../round-37/fetch/S189.bin
cmp rc=0
eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d  EventManager.cpp
eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d  .../fetch/S189.bin
192 EventManager.cpp
```

The host runs the same commit:

```
$ hyprctl version
Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs).
$ hyprctl getoption debug:disable_logs
int: 1
```

Below, all `:N` cites are lines in S189.bin unless another file is named.
Cross-file bytes I read: S201.bin sha256 `799bf02f…4f9e` (Waybar 0.15.0 backend.cpp) and S214.bin sha256 `d04e3a2f…b868` (Logger.cpp).

## 1. Listen / accept — FINDING (all fds non-blocking)

- Listening socket: `socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC | SOCK_NONBLOCK, 0)` at :14. The path is `m_instancePath + "/.socket2.sock"` (:21). `bind` happens at :29 and `listen(fd, 10)` at :35 (backlog 10, commented "10 max queued" at :34).
- The listen fd is registered with `WL_EVENT_READABLE` and static callback `onClientEvent` (:40). That static callback forwards to the **member** `onServerEvent` (:56-58), so the names are cross-wired (:52-58), but the routing still works. The static `onServerEvent` forwards to the member `onClientEvent`.
- Accept: `accept4(..., SOCK_CLOEXEC | SOCK_NONBLOCK)` (:73). **Accepted fds are non-blocking.**
  - `EAGAIN` returns 0 silently.
  - Any other errno logs ERR and tears down the whole listener (:74-82).
  - ERR/HANGUP on the listen fd also tears down the listener (:61-69).
- Each accepted client gets a wl event source with **mask 0** (:88), meaning no READABLE interest: Hyprland never reads from a socket2 client. The client goes into `m_clients` as `SClient{fd, {} /*events*/, eventSource}` (:89-93). Accept logs at DEBUG (:85).
- [INFERENCE] With mask 0, epoll still reports EPOLLHUP/EPOLLERR. A peer close therefore reaches `onClientEvent` → `removeClientByFD` (:99-102, DEBUG log "hung up"). This is kernel/libwayland behaviour; the bytes do not show it.

## 2. postEvent (:163-192) — FINDING

1. Shutdown suppression (:164-167): if `m_isShuttingDown`, the event is logged at **WARN** with its full content, then dropped for all clients.
2. The event is formatted once (:170 → `formatEvent` :126-131): `"{event}>>{data.substr(0,1024)}\n"`. Newlines inside the payload are replaced by spaces (:129). The cut is **1024 bytes of data**, not of the whole line, so a line can be `len(event)+2+1024+1` bytes. `substr` counts bytes, so it can split a UTF-8 code point. The string is shared, so every client queues the same `SharedPointer<std::string>` (:170, :180).
3. Per client (:171-191):
   - `QUEUESIZE = events.size()` is read **before** the push (:172).
   - **Cap (:169, :174-178):** if `QUEUESIZE >= 64` (64 events already pending, counting a partly written front event), the seat:
     - logs ERR "Socket2 fd {} overflowed event queue, removing" (:175);
     - calls `removeClientByFD` (:176 → :119-124), which runs `wl_event_source_remove` and then `m_clients.erase`;
     - does **not** enqueue the new event for that client.

     The fd closes when the erased `SClient`'s `CFileDescriptor` is destroyed ([INFERENCE]: hyprutils RAII, not in these bytes). No error or close reason is written to the client; it just sees EOF. Because the check precedes the push, a queue never exceeds 64.
   - Otherwise the seat pushes the event (:180) and **flushes synchronously right away** (:182). A failed flush removes the client (:182-185).
   - If events are still pending and the queue was empty before this post (`QUEUESIZE == 0`), the seat arms `WL_EVENT_WRITABLE` (:187-188).
4. Consequence (derived from the lines above): the overflow check runs only inside `postEvent`. A client stuck at 64 pending events is removed only when the **next** (65th) event is posted. A client stuck below 64 is never removed while it stays connected. The queue counts **events, not bytes**, and grows only after `write` returns EAGAIN. The kernel send buffer therefore absorbs output first. [INFERENCE] The host's `net.core.wmem_default` is 212992 bytes (`cat /proc/sys/net/core/wmem_default` → `212992`), so a stalled reader's removal comes after roughly that many bytes plus 64 events. I did not measure this.

## 3. flushClient (:133-161) — FINDING

The function loops while the queue is non-empty and always works on `events.front()`. It writes `length - writeOffset` bytes starting at `c_str() + writeOffset` (:135-137).

| write result | lines | action | return value |
|---|---|---|---|
| `> 0`, partial | :139-142 | `writeOffset += n` and returns **immediately**, with no retry in this call | `true` (stays queued) |
| `> 0`, complete | :143-146 | `writeOffset = 0`, erases the front event, continues | — |
| `< 0`, errno `EAGAIN` or `EWOULDBLOCK` | :149-150 | event stays queued, offset kept | `true` |
| `< 0`, errno `EINTR` | :152-153 | `continue`: rewrites the same event at the same offset | — |
| `0`, or `< 0` with any other errno | :155-156 | logs ERR "Socket2 fd {} failed writing event: {}" (strerror or "write returned 0") | `false`, so the caller removes the client (:108-109 or :182-183) |
| queue drained | :159-160 | `wl_event_source_fd_update(..., 0)`, which disarms WRITABLE | `true` |

## 4. When flush is attempted — FINDING

There are two triggers:

- **(a) Synchronously, on every `postEvent`**, for every client (:182).
- **(b) On the event-loop writable callback**: `onClientEvent` with `mask & WL_EVENT_WRITABLE` → `flushClient` (:104-110).
  - It is armed at :188, when the queue goes from empty to non-empty.
  - It is disarmed at :159, when the queue drains.
  - Invariant (from :159 and :188): a non-empty queue means WRITABLE is armed.
  - The callback does not check `findClientByFD` against `end()` (:106-108). That is not reached in normal flow; noted only.

## 5. State machine (line-cited)

```
LISTENING --accept4 ok (:73)--> CONNECTED_IDLE  [mask 0, events empty] (:88-93)
LISTENING --accept4 errno!=EAGAIN (:75-80) | ERR/HUP (:61-68)--> LISTENER_DEAD (no new clients)

CONNECTED_IDLE --postEvent, write full (:180,182,159)--> CONNECTED_IDLE
CONNECTED_IDLE --postEvent, EAGAIN/partial (:141-142,149-150)--> BACKLOGGED(q=1) + arm WRITABLE (:187-188)
BACKLOGGED(q<64) --postEvent (:180-185)--> BACKLOGGED(q+1) or drains
BACKLOGGED --WRITABLE cb, drained (:104-108,159)--> CONNECTED_IDLE (WRITABLE disarmed)
BACKLOGGED(q==64) --postEvent (:174-177)--> REMOVED  [ERR "overflowed event queue, removing"; new event not queued]
any CONNECTED --write 0 or errno∉{EAGAIN,EWOULDBLOCK,EINTR} (:155-156)--> REMOVED [ERR "failed writing event"]
any CONNECTED --HUP/ERR on client fd (:99-102)--> REMOVED [DEBUG "hung up"]
any --m_isShuttingDown at postEvent (:164-166)--> event dropped [WARN "Suppressed (shutting down)…"]
REMOVED: wl source removed + SClient erased (:121-123); fd closed by RAII [INFERENCE]
```

**Observability (S214):** every log above goes through `CLogger::log`, which returns at S214:15-16 when `!m_logsEnabled`. S214:48 sets `m_logsEnabled = !*PDISABLELOGS`, and the host has `disable_logs` = 1. The same early return comes **before** the rolling-log feed (S214:21-22), so `hyprctl rollinglog` cannot show the marker either. This confirms the brief's key finding: on this host, a zero marker count in the log, journal or rollinglog cannot mean "never overflowed".

## 6. r26 entry sentences checked against the bytes

File: /home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/event-delivery-limits-r26.md

| r26 line | sentence (short) | verdict | basis |
|---|---|---|---|
| 20-21 | each client gets its own queue; the compositor writes from its event loop | PASS (refine) | Each client has its own `events` vector of shared strings (:89-93, :170, :180). Writes happen synchronously in `postEvent` (:182) **and** in the writable callback (:104-108). |
| 23-26 | `MAX_QUEUED_EVENTS = 64` | PASS | :169 is verbatim. The host commit is efb50993 (hyprctl version). |
| 28-31 | a client "at or over the cap is removed, not throttled", with the quoted log line | PASS (refine) | :174-176 is verbatim. "Over" can never happen, since the check precedes the push. Removal happens only at the next `postEvent`, and the triggering event is not delivered. |
| 33-36 | writeOffset resume, EAGAIN keeps, EINTR retries, other failure logs "failed writing event" and ends the client | PASS (refine) | :139-156. The real string has a `: {}` suffix, and `write` returning 0 also counts as failure (:155). A partial write returns without retrying in the same call (:141-142). |
| 38-39 | during shutdown, events are dropped with a warning | PASS (refine) | :164-166 is WARN, and the warning includes the event content. Under `disable_logs` = 1 the warning itself is suppressed (S214:15-16). |
| 43-48 | "drop it after 64 queued events … the failure is logged compositor-side" | **PARTLY CONTRADICTED** | The count is 64 user-space events **after the kernel send buffer is full** (:180-182, :149-150), and removal comes at the 65th post. "Logged compositor-side" is **false on this host**: the ERR at :175 is discarded by S214:15-16 and :48 with `disable_logs` = 1. Supporting, client side: Waybar's loop on EOF just sleeps 1 ms and `continue`s, with no log and no reconnect (S201:119-121). "No error shown to the user" is corroborated. |
| 50-52 | "Waybar backend reads at most 1024 bytes per event, **matching** the compositor's own 1024-character truncation of event data" | **CONTRADICTED** | The compositor truncates **data** to 1024 **bytes** (`substr`, :128). The full line is `event + ">>" + ≤1024 + "\n"`, which is longer than 1024. Waybar uses `fgets(buffer, 1024, file)` (S201:115-117), which returns at most **1023** bytes per call. A long line is split, and the tail is parsed as a separate bogus message (S201:124-129, :142). The comment at S201:115, "Hyprland socket2 events are max 1024 bytes", is itself wrong against :128. The sizes do not match. |
| 54-55 | UNK: whether the cap was ever reached | stands, and gets stronger | Even a log read could not settle this on this host, because of S214:15-16 and :48. |
| 4-10, 12-17 | source rows and the merge note (S214 = Waybar workspaces.cpp; wave-1 S187/S188) | renumber note | In round 37, S214 is Logger.cpp, Waybar workspaces.cpp is S212, and the event manager is S189 (renumber-map.md:19). The entry's IDs must be re-mapped when it is re-grounded. |

## 7. Addendum — lead from ExecProcCrosscheck (doubled fds): REFUTED as a lookup bug

ExecProcCrosscheck saw every socket2 fd held twice by Hyprland. Their lead: if libwayland passes the dup to the callback, `findClientByFD(fd)` at :106 / :120 would miss.

The host's libwayland is `wayland 1.26.0-1` (`pacman -Q wayland`). I fetched the official source to scratch: `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/src/event-loop.c`, curl rc=0, sha256 `eabcb4d685be84a2794166b1f394c5503d348bab17ebda6b00a9915ea78a71b7`, 1122 lines.

- The dup is real: `source->base.fd = wl_os_dupfd_cloexec(fd, 0);` (event-loop.c:188). The **dup** is what epoll registers (`epoll_ctl(..., EPOLL_CTL_ADD, source->fd, &ep)`, :142, with `source` = base) and what `fd_update` modifies (:228). That explains the two fds per socket.
- The callback gets the **original**: `source->fd = fd;` (:190, the `wl_event_source_fd.fd` field) and `return fd_source->func(fd_source->fd, mask, source->data);` (:113). So `findClientByFD(fd)` compares the original against `SClient.fd` (the original) and matches. The S189 lookup at :106 and :120 is correct.
- On removal, `wl_event_source_remove` runs `EPOLL_CTL_DEL` and closes **only the dup** (:836-841). The original is closed when `m_clients.erase` destroys the `CFileDescriptor` (S189:123; RAII, still [INFERENCE] from hyprutils). The peer sees EOF only after both are closed, and both close in the same `removeClientByFD` call.
- This also settles half of §1's hangup [INFERENCE]: with mask 0, `add_source` registers `ep.events = 0` (:135-140). Dispatch maps `EPOLLHUP`/`EPOLLERR` to `WL_EVENT_HANGUP`/`WL_EVENT_ERROR` (:108-111). That epoll always reports HUP/ERR whatever the requested events is kernel behaviour, still [INFERENCE].

- Which fd of a pair is the original? `Socket2 fd {}` in the logs at S189:175 and :155 prints `client.fd`, which is the original `accept4` fd. The dup is made by `wl_os_dupfd_cloexec(fd, 0)` → `fcntl(fd, F_DUPFD_CLOEXEC, 0)` (wayland-os.c:133-145 at 1.26.0, sha256 `5b0ff635…899e`). `F_DUPFD` with minfd 0 returns the **lowest free** fd number, so the dup can come out *lower* than the original whenever a lower slot is free. Narrowed with ExecProcCrosscheck: `accept4` also takes the lowest free fd, so the dup lands lower **only if a lower fd is freed between S189:73 and :88**. In that window the main thread closes nothing; [INFERENCE] another Hyprland thread would have to. A non-adjacent pair (145+147, 236+250) means the gap slots were *occupied* at dup time. That fits original-is-lower and is not evidence of fd reuse. The rule "lower = original" is very likely right but still unproven. The DEBUG line "Socket2 accepted a new client at FD {}" (S189:85) would settle it, but on this host it is **never written**: `debug:disable_logs` = 1, so `CLogger::log` returns before any sink, including the rolling log (S214:15-16, :48, :21-22).

- I re-checked the live log on 2026-10-25 (ExecProcCrosscheck reported it first). `/run/user/1000/hypr/efb50993…_1792804449_426444678/hyprland.log`: `wc -l` → 27331; `grep -c 'Socket2'` → **0**. Line 13 reads "!!!!HEY YOU, YES YOU!!!!: further logs to stdout / logfile are disabled by default…". No Socket2 line of any kind appears: no accept (:85), hangup (:100), overflow (:175) or write-fail (:155). So the log can neither show the order fds were created in nor give evidence about overflow, which confirms §5 "Observability" with observed bytes.

## Remaining unknowns

- How the fd gets closed on removal: hyprutils `CFileDescriptor` RAII, outside these bytes.
- Whether SIGPIPE is ignored process-wide. `write` to a closed peer raises EPIPE (:155) only if SIGPIPE is ignored; that code is outside S189.
- The actual stall byte budget: kernel buffer plus 64 events. Not measured, since measuring would require connecting to socket2, which is forbidden.
