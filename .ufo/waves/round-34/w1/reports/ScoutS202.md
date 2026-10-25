# ScoutS202 — Waybar 0.15.0 `hyprland/window.cpp` IPC registration census

## Fetch & integrity

- Source: `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/window.cpp`
- Written to: `.ufo/waves/round-34/scratch/ScoutS202/window.cpp`
- sha256: `5df496eb3cfe5cae4506d7aa10c6bb54eb0a0b28d9489dcf19dd68ba570c9846` — **matches expected**
- Byte length: `8324` — **matches expected**
- Verified via: `sha256sum` + `wc -c` on the fetched file.

## `registerForIPC("activewindow", this)` location

- Line **27**: `m_ipc.registerForIPC("activewindow", this);`
- Enclosing function: `Window::Window(const std::string& id, const Bar& bar, const Json::Value& config)` — the `Window` constructor, spanning lines 20–38.
- Executed under `std::unique_lock<std::shared_mutex>` on global `windowIpcSmtx` (line 18 declared, line 22 locked, line 33 unlocked).

## All `registerForIPC` calls

All five calls sit in the `Window` constructor body, lines 27–31, under the `windowIpcSmtx` unique lock:

| Line | Event name          |
|-----:|---------------------|
| 27   | `activewindow`      |
| 28   | `closewindow`       |
| 29   | `movewindow`        |
| 30   | `changefloatingmode`|
| 31   | `fullscreen`        |

Related teardown: line 42 — `m_ipc.unregisterForIPC(this);` inside `Window::~Window()` (lines 40–43), also under the `windowIpcSmtx` unique lock. No other `registerForIPC` calls exist in the file.
