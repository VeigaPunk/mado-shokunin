source: S213 - .ufo/waves/round-37/fetch/S213.receipt.txt (current-session log, unit journal, `hyprctl getoption debug:*`; own work, read-only)
source: S214 - .ufo/waves/round-37/fetch/S214.bin (Hyprland v0.56.2 `src/debug/log/Logger.cpp`)
source: S189 - .ufo/waves/round-37/fetch/S189.bin (Hyprland v0.56.2 `src/managers/EventManager.cpp`, marker strings)
verified-at: 2026-10-25
recheck: on-change - re-read when the Hyprland build changes, when `debug:disable_logs` changes, or when a new session log replaces the S213 instance
ground: F1 - the socket contract under the lane's bar; the event-socket client half named in corpus/README.md Frontier

# On this host the event-queue overflow cannot be seen in the compositor's logs, and the socket table is the observation route

Lane: mado-shokunin. Round: 37. Opened 2026-10-25 by this lane. Substrates read-only: no
socket was connected, no option was set, no event was produced; every host read is a file
read, a journal read or a `hyprctl getoption` read verb. Replaces the package's two host
measurements (`event-queue-host-measurement-r28.md`, `event-queue-journal-measurement-r29.md`),
which are refused below.

### §1 The two failure markers are core-logger lines

- **OBS** The write-failure marker is a core-logger ERR call in `flushClient` (S189:155): `Socket2 fd {} failed writing event: {}`
- **OBS** The overflow marker is a core-logger ERR call in `postEvent`, issued just before the client is removed (S189:175): `Socket2 fd {} overflowed event queue, removing`
- **OBS** Both open with `Log::logger->log(Log::ERR,` (S189:155, S189:175), and the same `Log::logger->log(` call carries the DEBUG lines "Socket2 accepted a new client at FD {}" (S189:85) and "Socket2 fd {} hung up" (S189:100).
- **INF** Every socket2 line the compositor can write, from accept to removal, passes through one logger. Basis: S189:85, :100, :155, :175.

### §2 `debug:disable_logs` gates that logger, and it is 1 here

- **OBS** `CLogger::log` returns before writing anything when logging is disabled; the check comes before any level test (S214 Logger.cpp:15-16): `if (!m_logsEnabled)` / `return;`
- **OBS** The flag is the inverse of the option, set on every config (re)load (S214 Logger.cpp:42, :48, called from :37-38): `m_logsEnabled = !*PDISABLELOGS;`
- **OBS** The same reload turns stdout logging off unless both conditions hold (S214 Logger.cpp:47): `m_logger.setEnableStdout(!*PDISABLELOGS && *PENABLESTDOUT);`
- **OBS** The live option on this host, read with `hyprctl getoption` (S213): `debug:disable_logs: {"option":"debug:disable_logs","int":1,"set":false}`
- **OBS** Stdout logging is also off (S213): `debug:enable_stdout_logs: {"option":"debug:enable_stdout_logs","int":0,"set":false}`
- **INF** `"set":false` with `int` 1 means the 1 is the build default, not a line in the operator's config. Basis: S213 getoption fields.
- **INF** With `m_logsEnabled` false, both markers in §1 are dropped at S214:15-16 whatever their level, ERR included, so neither the file nor stdout ever receives them. Basis: S214:15-16, :47-48 and S213.

### §3 What the two channels actually hold

- **OBS** The session log has 27,331 lines and 4,259,033 B; its origin histogram is 27,280 `DEBUG from aquamarine`, 31 `ERR from aquamarine`, 21 core `DEBUG ]` lines (S213).
- **OBS** The 21 core-logger lines are lines 1-21; config loads are at lines 12 and 18 (S213): `last_core_logger_line_number: 21`
- **OBS** The log holds 0 "overflowed event queue", 0 "failed writing event" and 0 "Socket2 fd" (S213).
- **INF** The core logger stopped three lines after the second config load and wrote none of the later lines, all of them aquamarine's, which is what S214:48 predicts once `debug:disable_logs` = 1 is applied. Basis: S213 line numbers and S214:37-38, :48.
- **OBS** The compositor unit journal (`journalctl --user -u wayland-wm@hyprland.desktop.service`) has 717 lines and 0 of each of the three marker strings (S213).
- **OBS** A probe string from the log is present in the log and absent from the journal (S213): `probe_string: "drm: getCurrentCRTC: No CRTC 0" in_log=7 in_unit_journal=0`
- **INF** The journal is fed by stdout, which S214:47 switches off here, so it cannot carry lines the file log carries. Basis: S214:47, S213 `enable_stdout_logs` 0, and the probe's 7-to-0 split.

### §4 Consequence: the package's two "never overflowed" readings are refused

- **INF** The package's r28 entry reads 0 markers in a session log as "has never hit its per-client event-queue cap"; on this host that zero is from a null channel, so the reading is refused. Basis: §2 and §3.
- **INF** The package's r29 entry reads 0 markers in the unit journal as "never overflowed on this host in the retained history"; the journal is a null channel for the same logger (S214:47), so that reading is refused too. Basis: §2 and §3.
- **INF** Neither zero separates "never overflowed" from "overflowed and not logged". A log-based measurement becomes meaningful again only on a session started with `debug:disable_logs` = 0. Basis: S214:15-16, :48.
- **INF** The package's r28 log (instance `_1792772698_564628331`) is no longer on the host; S213 measures a different session's log. Basis: the S213 path, instance `_1792804449_426444678`.

### §5 The route that does work: the kernel's unix-socket table

- **INF** `ss -xpa` is a read-only table read: `-x` selects unix-domain sockets, `-p` shows the owning processes, `-a` includes listening and non-listening sockets (ss(8), iproute2). It reads the kernel table and does not connect to any socket. Basis: ss(8).
- **INF** The table names each process holding a client end of `$XDG_RUNTIME_DIR/hypr/<instance>/.socket2.sock` and, per socket, its Recv-Q (bytes queued, not yet read). A client that stops reading shows a growing Recv-Q before the compositor ever queues an event in user space. Basis: ss(8) columns; S189:137-150 (a full socket returns `EAGAIN` and the event stays queued).
- **INF** The bound path appears on the compositor's rows (the listener and each accepted connection). The client end carries no address of its own and is matched through the peer's socket inode. Basis: unix-socket binding semantics; not stated in ss(8).
- **INF** The table shows kernel buffer bytes, not the compositor's 64-event user-space queue: events pile up in `client.events` only after the kernel buffer is full (S189:169-180). It shows the precursor, and after removal the subscriber's absence, not the overflow count.
- **INF** A client removed on overflow is erased from `m_clients` (S189:119-124, :176). A previously listed subscriber whose row is gone is the table-side trace of a removal or a hang-up; the table cannot tell which.

## Unknowns

- **UNK** Why 27,311 aquamarine lines (S213 histogram) reach the log while `m_logsEnabled` is false: whether aquamarine's callback writes through `CLogger::hu()` (S214:57-59) to the inner logger and so bypasses the `log()` gate. Answerable by reading the aquamarine log-callback wiring, which S214 does not contain.
- **UNK** Whether `Log::logger` in S189 is the `CLogger` of S214; the declaration (`Logger.hpp`) is not fetched. If it is, ERR is suppressed with the rest (§2); this is settled only by reading that code.
- **UNK** The initial value of `m_logsEnabled` before the first `recheckCfg()`, which would explain the 21 startup core lines; it is declared in `Logger.hpp`, not fetched.
- **UNK** Whether ss's Recv-Q/Send-Q on a unix stream socket count exactly the unread bytes on each end; ss(8) does not define them for unix sockets, and the kernel's sock_diag code is not read here.
- **UNK** Whether `SClient` removal closes the client's descriptor (RAII of `CFileDescriptor`) or leaves the row in the table; Hyprutils is not fetched.
- **UNK** Whether any read-only verb exposes the per-client queue depth (`client.events.size()`) without connecting to the event socket.
- **UNK** Whether this host's compositor ever overflowed a client queue in this or any earlier session: no channel read here could have recorded it.
