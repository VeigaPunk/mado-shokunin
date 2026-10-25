# Waybar module-text route — the bar's socket2 subscription and the active-window label production

Lane: mado-shokunin. Round: 33 (assimilation draft, staged at
`.ufo/waves/round-33/scratch/ScribeEntryWaybar/` for `corpus/knowledge/`).
Substrates READ-ONLY: no host file, socket, bar process or compositor state was
touched; all evidence is source-byte reading of the two fetched blobs below on
2026-10-24 by the lane itself. This entry is the waybar-side companion that
ipc-contract-r25.md §3 explicitly left unclaimed.

source: S190 — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp — `IPC::getSocketFolder`, `IPC::socketListener`, `IPC::parseIPC`, `IPC::getSocket1Reply` — tag `0.15.0` — fetched bytes `.ufo/waves/round-33/fetch/S190.bin`, 6550 B, sha256 `799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e`
source: S191 — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/window.cpp — `Window::Window`, `Window::onEvent`, `Window::update` — tag `0.15.0` — fetched bytes `.ufo/waves/round-33/fetch/S191.bin`, 8324 B, sha256 `5df496eb3cfe5cae4506d7aa10c6bb54eb0a0b28d9489dcf19dd68ba570c9846`
verified-at: 2026-10-24
recheck: 90d

gate-quote: S190 $XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr
gate-quote: S191 m_ipc.registerForIPC("activewindow", this);

## Gate

Both blobs re-read by the lane on **2026-10-24**; digests above were recomputed
from the fetch bytes with `sha256sum` at write time and match the digests frozen
in `.ufo/waves/round-33/c1/frozen.json`. Each gate-quote line is a contiguous
substring of its blob (`grep -cF` = 1 for each). Line anchors were re-derived
against the fetched bytes; the staged anchor ranges (`S190 :17-33`, `:77-99`,
`:109-116`; `S191 :22-28`) were stale and are not used.

- **S190** — waybar `src/modules/hyprland/backend.cpp` @ tag `0.15.0` — opened
  2026-10-24; 6550 B, sha256 `799bf02f…4f9e`.
  Quote (`:38`, inside `IPC::getSocketFolder` :19-44): `"$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr"`.
  Quote (`:98`, `IPC::socketListener` :77-139): `auto socketPath = IPC::getSocketFolder(his) / ".socket2.sock";`.
  Quote (`:115`): `std::array<char, 1024> buffer;  // Hyprland socket2 events are max 1024 bytes`.
  Quote (`:142`, `IPC::parseIPC` :141-150): `std::string request = ev.substr(0, ev.find_first_of('>'));`.
  Quote (`:237`, `IPC::getSocket1JsonReply` :236-): `std::string reply = getSocket1Reply("j/" + rq);`.
- **S191** — waybar `src/modules/hyprland/window.cpp` @ tag `0.15.0` — opened
  2026-10-24; 8324 B, sha256 `5df496eb…9846`.
  Quote (`:27`, `Window::Window`): `m_ipc.registerForIPC("activewindow", this);`.
  Quote (`:58-64`, `Window::update`): `waybar::util::rewriteString(fmt::format(fmt::runtime(format_), fmt::arg("title", …) …), config_["rewrite"])` handed to `label_.set_markup(label_text);` (`:64`).
  Quote (`:240-241`, `Window::onEvent`): `dp.emit();`.

**GRANTED** — every claim below is carried by a quote located in these bytes on
2026-10-24.

### §1 The subscription (source-read)

**OBS** The active-window module registers one handler — itself — for five
event names in its constructor (S191:27-31): `activewindow` (S191:27),
`closewindow`, `movewindow`, `changefloatingmode`, `fullscreen`. It also emits
one initial `dp.emit()` after its first `update()` (S191:37), so the label is
populated once at construction without waiting for an event.

**OBS** Registration is per (event name, handler) appended to a shared callback
list (S190:152-); dispatch splits the received frame at the first `>` and calls
each handler whose stored event name equals that prefix (S190:141-150,
esp. :142). Combined with the compositor's own `EVENT>>DATA\n` framing
(ipc-contract-r25.md §2, S189), the five subscribed names match the compositor's
EVENT field exactly.

### §2 The text route (source-read)

**OBS** The event payload itself is discarded: `Window::onEvent` ignores the
event string and only queues a redraw via `dp.emit()` (S191:240-241). No module
text is parsed from the socket2 event data.

**OBS** The fresh text is produced synchronously on the GTK thread: `update()`
re-queries the request socket as JSON — `getSocket1JsonReply("activeworkspace")`
(S191:114), plus `clients` for the focused-window record (S191:200) — and takes
the title from the workspace JSON's `lastwindowtitle` field (S191:164), passed
through `waybar::util::sanitize_string` (S191:50).

**OBS** The label text is then `fmt::format` over the four placeholders
`title`, `initialTitle`, `class`, `initialClass` (S191:59-62), wrapped in
`waybar::util::rewriteString` with the module's `rewrite` config (S191:58, :63)
and set as GTK markup on the label (S191:64); the same four arguments feed the
optional `tooltip-format` (S191:76-79). This `set_markup` call is the handoff
point at which this entry stops: everything downstream (GTK rendering, actual
bar pixels) is not claimed and remains the boundary drawn by
waybar-observation-boundaries-r16.md.

### §3 Transport and socket-folder derivation (source-read)

**OBS** All waybar Hyprland modules share one process-wide IPC singleton
(`IPC::inst()`, S190:72-75). Its listener thread connects to
`getSocketFolder(his) / ".socket2.sock"` (S190:98) and reads one event line at a
time into a 1024-byte buffer — the code's own comment pins the event size bound
(S190:115). A module destructor only unregisters its callback (S191:42); the
socket and thread are singleton-owned, not module-owned.

**OBS** The socket folder is derived once and cached: if `$XDG_RUNTIME_DIR` is
set and `$XDG_RUNTIME_DIR/hypr` exists it is used, otherwise waybar logs
`"$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr"` and uses
`/tmp/hypr` (S190:37-39, gate-quote at :38); the instance signature is appended
afterwards (S190:42-43). The request side mirrors this: `getSocket1Reply`
connects to `getSocketFolder(instanceSig) / ".socket.sock"` (S190:198), throws
when `HYPRLAND_INSTANCE_SIGNATURE` is unset (S190:188-193), and
`getSocket1JsonReply` prefixes requests with `j/` (S190:237). This is the
client-side twin of the two-socket paths documented in ipc-contract-r25.md §1-2.

**OBS** If `HYPRLAND_INSTANCE_SIGNATURE` is unset, the listener thread returns
before connecting and logs that Hyprland IPC will not be available
(S190:79-83): the module stays constructed but its five registrations never
fire; only the constructor-time `update()` runs.

### §4 What this entry does not claim

- No socket was connected, no bar process inspected, no rendering observed; the
  route is **source-read** at tag `0.15.0`, not host-observed.
- The `/tmp/hypr` fallback and the 1024-byte event bound are implementation at
  tag `0.15.0` (S190:38, :115); a future tag may change them.
- The staged S191 claim "subscribes to `activewindow` and `closewindow`" was
  dropped as understated — the bytes carry five registrations (S191:27-31) — and
  the staged S190 anchor ranges were dropped as stale against the fetched bytes.
