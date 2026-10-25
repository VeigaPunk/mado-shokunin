# ScoutS197 — Waybar 0.15.0 `workspaces.cpp` fetch, hash, IPC registrations

Seat: scout (round-33 w1). Target: Waybar 0.15.0
`src/modules/hyprland/workspaces.cpp`, fetched fresh to
`.ufo/waves/round-33/scratch/ScoutS197/S197.bin` (41392 bytes).
All commands run in `/home/vgpnk/Projects/shokunin/mado-shokunin`.

## Fetch & hash — CONFIRMED

```sh
$ curl -fsSL -o .ufo/waves/round-33/scratch/ScoutS197/S197.bin \
    https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/workspaces.cpp
$ sha256sum .ufo/waves/round-33/scratch/ScoutS197/S197.bin
1e19d92638e7923f0e72f6e65c83f579e32b41d588d166d6efef543c3f97d7e9  .ufo/waves/round-33/scratch/ScoutS197/S197.bin
```

sha256 `1e19d92638e7923f0e72f6e65c83f579e32b41d588d166d6efef543c3f97d7e9`
matches the required digest exactly. Fetch succeeded; no inference from the
staged entry was needed.

## `Workspaces::registerIpc` — 14 `registerForIPC` calls

`auto Workspaces::registerIpc() -> void` spans S197.bin lines **803–829**.
It contains **14** `m_ipc.registerForIPC(...)` calls: 12 unconditional
(lines 804–815), then 2 inside `if` blocks (lines 821, 827). No other
`registerForIPC` calls exist in the file (the only other IPC call is
`m_ipc.unregisterForIPC(this)` at line 37).

Unconditional event names, in source order:

| line | event |
|------|-------|
| 804 | `workspacev2` |
| 805 | `activespecial` |
| 806 | `createworkspacev2` |
| 807 | `destroyworkspacev2` |
| 808 | `focusedmonv2` |
| 809 | `moveworkspacev2` |
| 810 | `renameworkspace` |
| 811 | `openwindow` |
| 812 | `closewindow` |
| 813 | `movewindowv2` |
| 814 | `urgent` |
| 815 | `configreloaded` |

Conditional event names:

| line | event | condition |
|------|-------|-----------|
| 821 | `windowtitlev2` | `if (windowRewriteConfigUsesTitle() || m_taskbarWithTitle)` |
| 827 | `activewindowv2` | `if (m_updateActiveWindow)` |

Verbatim region (S197.bin:803–829, trimmed):

```cpp
auto Workspaces::registerIpc() -> void {
  m_ipc.registerForIPC("workspacev2", this);
  m_ipc.registerForIPC("activespecial", this);
  m_ipc.registerForIPC("createworkspacev2", this);
  m_ipc.registerForIPC("destroyworkspacev2", this);
  m_ipc.registerForIPC("focusedmonv2", this);
  m_ipc.registerForIPC("moveworkspacev2", this);
  m_ipc.registerForIPC("renameworkspace", this);
  m_ipc.registerForIPC("openwindow", this);
  m_ipc.registerForIPC("closewindow", this);
  m_ipc.registerForIPC("movewindowv2", this);
  m_ipc.registerForIPC("urgent", this);
  m_ipc.registerForIPC("configreloaded", this);

  if (windowRewriteConfigUsesTitle() || m_taskbarWithTitle) {
    ...
    m_ipc.registerForIPC("windowtitlev2", this);
  }
  if (m_updateActiveWindow) {
    ...
    m_ipc.registerForIPC("activewindowv2", this);
  }
}
```

## Frozen quote — CONFIRMED

`m_ipc.registerForIPC("workspacev2", this);` is present verbatim at
**S197.bin line 804** — the first statement of `Workspaces::registerIpc`.
