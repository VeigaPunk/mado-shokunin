# What happens to an event client that stops reading

source: S189 — Hyprland v0.56.2 `src/managers/EventManager.cpp` @ `efb50993780079460b0cbed1363e2166a2de1d9f`; S201 — Waybar 0.15.0 `src/modules/hyprland/backend.cpp`; S212 — Waybar 0.15.0 `src/modules/hyprland/workspaces.cpp`
verified-at: 2026-10-25
recheck: 90d
ground: a new edge class under the held IPC contract (`knowledge/ipc-contract-r25.md`): delivery to an event client that stops reading — queue cap, removal, partial writes — and the bar's side of it; no Frontier row is moved by it

Lane: mado-shokunin, round 37. Read-only: source bytes were fetched and read; no socket was
connected, no event was sent or observed, no client was stalled. Receipts:
`.ufo/waves/round-37/fetch/S189.bin`, `S201.bin`, `S212.bin` (digests in the round-37 lesson
`## Gate`). The host runs exactly this compositor commit (`hyprctl version`: v0.56.2,
`efb50993…`) and Waybar `0.15.0-3`.

## §1 The compositor side (S189)

**OBS** S189: the event socket and every accepted client are non-blocking —
`socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC | SOCK_NONBLOCK, 0)` at `:14`, `listen(…, 10)` at
`:35`, `accept4(…, SOCK_CLOEXEC | SOCK_NONBLOCK)` at `:73`. The compositor never reads from a
client.

**OBS** S189: each client has its own queue of events, and the cap is a count of events, not
bytes, at `:169`: `const size_t MAX_QUEUED_EVENTS = 64;`

**OBS** S189: the cap is checked only when a new event is posted (`:172-177`). With 64 or more
events already queued, the compositor logs `Socket2 fd {} overflowed event queue, removing`
(`:175`) and removes the client (`:176`); the new event is not queued. Otherwise the event is
appended and flushed at once (`:180-182`), and writable interest is armed when the queue was
empty before (`:187-188`).

**OBS** S189: `flushClient` (`:133-161`) resumes partial writes through `writeOffset`
(`:136-144`); `EAGAIN`/`EWOULDBLOCK` leaves the event queued (`:149-150`); `EINTR` retries
(`:152-153`); a zero-byte write or any other error logs `Socket2 fd {} failed writing event: {}`
(`:155`) and the client is removed.

**OBS** S189: during shutdown an event is dropped with a WARN line instead of delivered
(`:164-166`). Event data is cut to 1024 bytes before framing, so a framed line is
`EVENT>>` + up to 1024 bytes + `\n` (`:128`).

**INF** S189: removal needs two things in order — the kernel's socket send buffer full first
(until then every write succeeds and nothing queues), then 64 more posted events. A slow
client is therefore tolerated for a long time; a client that has stopped reading is removed
after its buffer plus 64 events. The buffer's actual size on these sockets was not measured.

## §2 The client this host runs (S201, S212)

**OBS** S212: Waybar's workspaces module registers twelve events unconditionally
(`:804-815`, starting `m_ipc.registerForIPC("workspacev2", this);`) and two more only under
configuration (`windowtitlev2` at `:821`, `activewindowv2` at `:827`).

**OBS** S201: Waybar reads the socket line by line through `fgets` into a fixed buffer,
`std::array<char, 1024> buffer;  // Hyprland socket2 events are max 1024 bytes` (`:115-117`).
The comment is wrong against S189 `:128`: a line can exceed 1024 bytes, and `fgets` returns at
most 1023 characters per call, so a long event arrives as a truncated head plus a tail parsed
as a separate message.

**OBS** S201: Waybar connects once (`:105`). When `fgets` returns nothing it sleeps one
millisecond and loops (`:119-122`) — no reconnect, no log line, no exit — and it also sleeps
one millisecond after every event (`:136`).

**INF** S201, S189: once the compositor removes the bar, the bar keeps running with no
compositor-event feed and shows no error; only a restart reconnects it. Module handlers run on
the listener thread (wave-1 `ScoutWaybarDrop`, `backend.cpp:129,143-147`), so a slow handler —
not a slow custom-module producer, which runs on its own thread — is what can stop the bar from
reading.

**UNK** How many bytes a stalled client absorbs before queueing starts; whether the compositor
ignores `SIGPIPE`; how `removeClientByFD` closes the descriptor (hyprutils code outside these
bytes).

## §3 Whether this host can see a removal

Not here: see `knowledge/event-queue-observability-r37.md` — on this host the compositor's own
log lines, both markers included, are not written at all.

## Assimilation

Origin: shokuknow `corpus-expansion-1`, package `merge/mado/knowledge/corpus/knowledge/event-delivery-limits-r26.md`
(read-only). Every sentence was re-checked against the re-fetched bytes. Kept: the cap, the
removal rule, partial-write resume, the shutdown drop, the twelve registrations. Corrected:
the source ids (package S187 → S189, S188 → S201, S214 → S212, by document); "matching the
compositor's own 1024-character truncation" (the framed line exceeds 1024 bytes and Waybar's
read is 1023 characters); "dropped after 64 queued events" (the send buffer fills first);
"the failure is logged compositor-side" (not on a default install); "a blocked custom-module
producer" as the trigger (it runs on its own thread). Dropped: the package's host-side UNK,
replaced by §3.
