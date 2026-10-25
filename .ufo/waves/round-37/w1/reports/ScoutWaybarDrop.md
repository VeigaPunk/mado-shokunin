# ScoutWaybarDrop — Waybar 0.15.0 Hyprland event-socket reader (round 37, wave 1)

Seat: L1Mado37-2.ScoutWaybarDrop (scout). Read-only. No Hyprland socket was
connected; `ss`/`/proc` reads only. Scratch: `/dev/shm/mado37-ScoutWaybarDrop/`.
No tools installed or upgraded.

## 0. Byte identity — PASS

```
curl -sSfL -o backend.cpp https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp
cmp backend.cpp .ufo/waves/round-37/fetch/S201.bin; sha256sum both
```
```
curl=0
cmp=0
799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e  backend.cpp
799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e  .../fetch/S201.bin
246 backend.cpp
```
The re-fetched file is byte-identical to S201. All `backend.cpp:N` citations below
apply to S201. I also fetched these supporting files from the same tag (sha256 prefix,
bytes): `include/modules/hyprland/backend.hpp` 28f2c7e96c2a5893 1349;
`src/modules/custom.cpp` 2232f7f7141caa59 8746. Two more round files were used:
S189 (sha256 prefix eea605dfe5ce09e1) and S212 (sha256 prefix 1e19d92638e7923f).
The host runs `waybar 0.15.0-3`, `hyprland 0.56.2-4` and `glibc 2.44+r50` (from `pacman -Q`, a read-only query).

## Q1. What does `socketListener()` do when the compositor closes the connection? — FINDING: it stops silently and never reconnects

- The connection is made once per process. `IPC::IPC()` starts `ipcThread_` running
  `socketListener()` (backend.cpp:46-49). `IPC::inst()` returns a function-static
  singleton (backend.cpp:72-75). `connect()` is called once (backend.cpp:105). A failure
  there logs `"Hyprland IPC: Unable to connect?"` and returns (:105-108). These bytes have
  no reconnect path.
- In the read loop, `fgets` failure (EOF or error) does nothing except sleep 1 ms and
  `continue` (backend.cpp:117-122):
  ```
  auto* receivedCharPtr = fgets(buffer.data(), buffer.size(), file);
  if (receivedCharPtr == nullptr) {
    std::this_thread::sleep_for(std::chrono::milliseconds(1));
    continue;
  }
  ```
  This path has no log, no `feof`/`ferror` check, no reconnect and no break. The loop
  exits only when `running_` becomes false (header `bool running_ = true;`,
  backend.hpp:50). Only `~IPC()` sets it (backend.cpp:57), and that runs at process
  teardown. The final `spdlog::debug("Hyprland IPC stopped")` (:138) is at debug level.
- Replica check on this host: I compiled the same `fdopen`, `fgets` into a 1024-byte
  buffer, and 1 ms-sleep loop (`loop.c`), ran it over a private `socketpair`, and closed
  the writer:
  ```
  after close: fgets NULL returns in 0.5s=477 feof=1 ferror=0
  ```
  On glibc 2.44 the EOF indicator stays set, so after a compositor-side close the real
  loop would poll about 950 times per second forever and print nothing. [INFERENCE from
  the replica; the real Waybar was not made to see EOF.]
- On the compositor side (S189), a removed client is erased with
  `removeClientByFD` (S189:119-124). A hang-up from the client logs at DEBUG
  (S189:99-103, `"Socket2 fd {} hung up"`). Overflow logs at ERR
  (S189:174-177, `"Socket2 fd {} overflowed event queue, removing"`).

**Verdict:** the reader stops silently and does not reconnect, retry or log. The bar's
Hyprland event feed is dead from that point until Waybar restarts.

## Q2. Read buffer size and how reads are split — FINDING

- The buffer is `std::array<char, 1024> buffer;  // Hyprland socket2 events are max 1024 bytes`
  (backend.cpp:115). `fgets` stores at most 1023 characters plus a NUL.
- Splitting is done by stdio, not by Waybar. The socket fd is wrapped with
  `fdopen(socketfd_, "r")` (:109). `fgets` returns one newline-terminated line per call
  from the FILE buffer, so several events delivered in one kernel read are returned one
  per iteration. An event that arrives across two kernel reads is reassembled, because
  `fgets` keeps reading until it sees a newline or fills 1023 characters. Each line is
  then cut at the first `'\n'` (:124-125) and passed to `parseIPC` (:129). `parseIPC`
  takes the event name as the text before the first `'>'` (:142) and calls only handlers
  registered under exactly that name (:145-147).
- The comment at :115 is wrong for the compositor's maximum. Hyprland formats each event
  as `std::format("{}>>{}\n", event.event, data.substr(0, 1024))` (S189:128). The 1024
  cap applies to the data alone, so a full event line is name length + 2 + 1024 + 1
  bytes, which exceeds 1023. Replica (`windowtitlev2>>` followed by 1024 `x` and a newline):
  ```
  line 4: fgets_len=1023 has_newline=0 msg_len=1023 event_name_len=13 name_prefix=windowtitlev
  line 5: fgets_len=17 has_newline=1 msg_len=16 event_name_len=16 name_prefix=xxxxxxxxxxxx
  ```
  The three-event single write split correctly (replica lines 1-3: `workspacev2`,
  `openwindow`, `urgent`). An oversized event becomes two messages. The first goes to
  the right handler with its payload truncated. The second has the payload tail as its
  "event name"; it normally matches no registration (:145-147) and is dropped silently.
  [INFERENCE for the drop.] The threshold is data length ≥ 1021 − name length (the full
  line, including its newline, exceeds 1023 characters). For `windowtitlev2` that is
  data of 1008 bytes or more.
- After every event the reader also sleeps 1 ms (backend.cpp:136). Including that sleep,
  the listener drains fewer than 1000 events per second.

## Q3. Is the event socket read on its own thread? — FINDING: yes, but handlers run on that same thread

- The read runs on a dedicated `std::thread` (backend.cpp:48), separate from the GTK UI
  thread. S212:123-124 names the two threads ("UI thread and event listener thread").
- Handlers are called inline on the listener thread while it holds `callbackMutex_`:
  `parseIPC` (backend.cpp:129) → `std::unique_lock lock(callbackMutex_)` (:143) →
  `handler->onEvent(ev)` (:147). No queue or hand-off sits between the read and the
  handler, so a slow handler stalls the read.
- Concrete stall routes in S212 (`hyprland/workspaces`):
  - `Workspaces::onEvent` takes `m_mutex` (S212:326). The UI thread's `doUpdate` holds
    the same mutex (S212:127) while it runs `updateWorkspaceStates()` and
    `updateWindowCount()` (S212:131-132). Those functions make blocking request/reply
    calls to the compositor's command socket (`getSocket1JsonReply`, S212:1019 and
    S212:1065-1067). Any slow UI-thread `doUpdate` therefore blocks the listener.
  - Handlers called from `onEvent` also make these blocking request/reply calls on the
    listener thread: `onWorkspaceCreated` (S212:393-394), `onWorkspaceMoved`
    (S212:433, :442), `onMonitorFocused` (S212:480), `onWindowTitleEvent` (S212:590) and
    `setUrgentWorkspace` (S212:995).
  - The request/reply read loop `getSocket1Reply` (backend.cpp:221-230) uses blocking
    `read` and has no timeout.

**Verdict:** the read is on its own thread, but that does not isolate it from slow
module handlers. A slow handler, or a UI thread holding `m_mutex`, stalls the read
directly.

## Q4. The package inference — SPLIT: the consequence holds, the named trigger is contradicted

The package text (`shokuknow/merge/mado/knowledge/corpus/knowledge/event-delivery-limits-r26.md:43-48`):
> A blocked custom-module producer can therefore cost the bar its whole compositor-event
> feed — including the `hyprland/workspaces` element — with no error shown to the user,
> because the failure is logged compositor-side, not in the bar.

| Clause | Verdict | Basis |
|---|---|---|
| "cost the bar its whole compositor-event feed" | **HOLDS** | There is one IPC singleton and one connection (backend.cpp:46-49, 72-75, 105), shared by every registered handler (`callbacks_`, :145-148). There is no reconnect, and after EOF the loop never exits (:117-122). Once Hyprland removes the client (S189:174-177), every `hyprland/*` module loses events until Waybar restarts. |
| "with no error shown" (bar side) | **HOLDS** | The EOF path logs nothing (backend.cpp:117-122); the replica showed a silent poll loop (`feof=1`, 477 NULL returns in 0.5 s). |
| "because the failure is logged compositor-side" | **Not supported on this host** (outside my question) | S189:175 does log at ERR, but the round's key finding is that `debug:disable_logs`=1 makes the logger return early (Logger.cpp:15-16, :48 per the shared context; I did not re-open S214). The failure is then logged nowhere. |
| "A blocked custom-module producer can …" | **CONTRADICTED as a direct mechanism by these bytes; indirect routes UNDETERMINED** | The custom module reads its producer on its own worker thread (`continuousWorker`: `util::command::open` custom.cpp:69, `thread_ = [...]` :73, blocking `getline(&buff, &len, fp_)` :81) and hands output to the UI with `dp.emit()` (:113). `update()` (custom.cpp:162-220) only formats and sets the label. It takes neither `callbackMutex_` nor Workspaces' `m_mutex`, and it never touches the socket2 listener. A producer that stops writing blocks only the custom module's own thread. Routes outside these bytes (for example a GTK main-loop stall caused elsewhere and then reaching `doUpdate`) were not checked. |

Two corrections the entry needs:
1. **Trigger.** The route these bytes support is a slow Hyprland-module handler or a
   UI thread holding `m_mutex` (Q3), not a custom-module producer.
2. **"drop it after 64 queued events".** Client fds are `SOCK_NONBLOCK`
   (S189:73). `postEvent` writes immediately through `flushClient` (S189:180-185), and an
   event stays queued only on `EAGAIN` (S189:149-150). The cap is checked before each
   push (S189:172-174). Removal therefore needs the kernel send buffer to be full first,
   then 64 more events. On this host `/proc/sys/net/core/wmem_default` = `212992`.
   [INFERENCE that this is the effective send buffer for the unix stream socket.]

## Q5 (bonus, live and read-only). The current bar has not been dropped — FINDING

Commands: `ss -xpn | awk '/socket2/…'`, then matching the peer inode against
`ls -l /proc/<waybar pid>/fd`, then `ps -o etimes=,time=`. Taken at 2026-10-25T12:15:18Z.
```
u_str ESTAB local_ino=181151236 peer_ino=181143087 users:(("Hyprland",pid=*,fd=250),...)
u_str ESTAB local_ino=10029 peer_ino=40790 users:(("Hyprland",pid=*,fd=147),...)
socket2 peer inode 181143087 owned by waybar
25723 00:16          # waybar etimes (s), cpu time
peer 40790 owner: socat age_s=126066   # parent comm: omarchy-hyprlan, stdout: pipe
```
- Waybar (1 process, 24 threads) holds an ESTABLISHED connection to the event socket,
  and the process is 25723 s old. The code connects once and never reconnects
  (backend.cpp:105, :117-122). So this Waybar process's event feed has not been removed
  by Hyprland during its lifetime, roughly the last 7.1 h. [INFERENCE that rests on there
  being one IPC instance per process (backend.hpp:20-21, backend.cpp:72-75).]
- This check does not depend on the compositor log. It is a positive channel that
  `debug:disable_logs`=1 does not suppress, and C2 or the observability entry may want it.
  It covers only the current bar process and says nothing about earlier processes.
- A second long-lived event client exists: a `socat` (age 126066 s, parent comm
  `omarchy-hyprlan`, stdout a pipe). If the reader on that pipe stalls, it is equally
  exposed to the same removal. Owner and command line are not recorded, for privacy.

## Remaining unknowns
- Whether any path outside backend.cpp, custom.cpp and S212 links a custom-module stall
  to the listener (GTK main loop, AModule dispatcher). These files were not opened as
  receipts; `src/util/command.cpp` returned 404 at the tag, and the header
  `include/util/command.hpp` was fetched (7d876c1bc1889bbd) but not analysed.
- The effective `SO_SNDBUF` of Hyprland's accepted socket2 fds was not measured.
- Whether real Waybar actually hits the EOF busy-poll was not observed (replica only).

## Files written
- `/dev/shm/mado37-ScoutWaybarDrop/loop.c` (replica) and the fetched files listed in §0.
- This report.
