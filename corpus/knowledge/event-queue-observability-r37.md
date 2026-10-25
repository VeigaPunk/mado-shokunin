# On this host an event-socket removal is not logged anywhere; the socket table is the route

source: S213 — host log-channel receipt `.ufo/waves/round-37/fetch/S213.receipt.txt`; S217 — Hyprland v0.56.2 `src/debug/log/Logger.hpp`; S214 — Hyprland v0.56.2 `src/debug/log/Logger.cpp`; S215 — Hyprland v0.56.2 `src/config/values/ConfigValues.cpp`; S216 — Hyprland v0.56.2 `src/Compositor.cpp`; S189 — Hyprland v0.56.2 `src/managers/EventManager.cpp`
verified-at: 2026-10-25
recheck: on-change
ground: host observability of that edge class (whether a removal can be seen here); supersedes the package's two "never overflowed" host readings, refused in the round-37 lesson

Lane: mado-shokunin, round 37. Read-only: files and the journal were counted, two
`hyprctl getoption` read verbs were run; no socket was connected and no event was observed.
Companion: `knowledge/event-delivery-limits-r26.md` (what the compositor does to a stalled
client).

## §1 Both removal markers are core-logger lines

**OBS** S189: the two removal markers are written by the compositor's own logger —
`Log::logger->log(Log::ERR, "Socket2 fd {} overflowed event queue, removing", …)` at `:175`
and `Socket2 fd {} failed writing event: {}` at `:155`.

## §2 The default switches the core logger off

**OBS** S215: `debug:disable_logs` defaults to on — `MS<Bool>("debug:disable_logs", "disable logging to a file", true),`
(`:629`); `debug:enable_stdout_logs` defaults to off (`:632`).

**OBS** S217: both markers are formatted calls, which resolve to the template overload whose
first statement is the gate — `if (!m_logsEnabled)` / `return;` (`Logger.hpp:22-24`), before
any formatting; the flag starts open, `bool                    m_logsEnabled = true;` (`:42`).

**OBS** S214: the setting decides the flag at every level — `m_logsEnabled = !*PDISABLELOGS;`
(`:48`) — and the string overload checks it again first (`:15-16`), before the rolling-log feed
(`:21-22`) and the file and stdout write (`:24`). Stdout is enabled only when logs are on and
`enable_stdout_logs` is set (`:47`).

**OBS** S216: the switch is applied in `Log::logger->initCallbacks();` (`:298`), after the first
initialisation stage; aquamarine (the backend library) is handed the raw hyprutils logger
instead (`conn->setName("aquamarine");`, `:304-307`), so its lines bypass the switch.

**OBS** S213: on this host the switch is at its default —
`debug:disable_logs: {"option":"debug:disable_logs","int":1,"set":false}` — and
`enable_stdout_logs` is `int 0`.

## §3 What the host's channels hold

**OBS** S213: the session log (27,331 lines) holds 21 core-logger lines, the last at line 21,
three lines after the second config load (line 18); every later line is from aquamarine
(27,280 DEBUG, 31 ERR). Zero lines match either removal marker.

**OBS** S213: the compositor's unit journal (717 lines) carries 4 start-up `Using config` lines
and none of the runtime log: a string the session log carries 7 times
(`drm: getCurrentCRTC: No CRTC 0`) appears 0 times there. Zero lines match either marker.

**INF** S213, S214, S217: the zero counts are a null channel, not a measurement — the logger
that would write the markers stopped writing at line 21, and reaches the journal only through stdout before that point, so
"never overflowed" and "not logged" give the same zero. The open window before line 21 cannot
carry a marker: no event client is accepted until the event loop runs (wave-1
`CritNullChannel` SC2). A second, independent lag: the file is written without a flush, so the
newest lines sit in the rolling buffer before they reach `hyprland.log` (wave-1
`ScoutRollingLog`: the last 18 lines were missing from disk). The same holds for `hyprctl rollinglog`,
which is fed after the same return (wave-1 `ScoutRollingLog`: 26 lines, all aquamarine). A
growing `hyprland.log` proves only that aquamarine is logging.

## §4 Consequence for the corpus

**INF** S213, S214, S215: the package readings "the event queue has never overflowed on this
host" (session log) and "the overflow markers appear nowhere in the retained history" (journal)
are refused (round-37 lesson, `### Assimilation` and M37-2). The blind spot is the shipped default, not a local
choice, so it applies to any v0.56.2 host that has not set `debug:disable_logs = false`.

## §5 The route that does work: the kernel's socket table

**INF** S189: the compositor never reads from an event client, and removal closes the client's
connection. Whether a given client is still subscribed is therefore visible without connecting
to anything: the kernel's unix-socket table (`ss -xpa`) lists the compositor's server ends on
`.socket2.sock`, each one's peer inode, and the process holding that peer, with the bytes the
peer has not read (its Recv-Q).

**INF** S201: Waybar never reconnects (`backend.cpp:105,119-122`), so a Waybar process holding
an established `.socket2.sock` connection has not been removed since that process started.

**UNK** Whether `debug:disable_logs` was ever 0 in an earlier session (`getoption` shows only
the current value); whether any removal happened before this reading; the kernel send-buffer
size on these sockets.

## Flip

Set `debug:disable_logs = false` (operator-owned; this lane never changes it), confirm core lines
appear after the config load, then re-count both markers in the session log.
