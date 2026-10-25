# Waybar module text for a Hyprland bar — the event-socket client

Lane: mado-shokunin. Round: 34. Opened 2026-10-24 by this lane. Substrates
read-only: no bar was started, no producer was executed, and the host Waybar
configuration was not read. The evidence is two tagged upstream files.

source: S201 — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp — tag 0.15.0
source: S202 — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/window.cpp — tag 0.15.0
verified-at: 2026-10-24
recheck: 90d

gate-quote: S201 // socket path, specified by EventManager
gate-quote: S202 m_ipc.registerForIPC("activewindow", this);

### What the bytes say

**OBS** The Hyprland backend derives a socket folder and warns when
`$XDG_RUNTIME_DIR/hypr` is absent (S201 line 38). That warning is the
event-socket client path, not the request socket.

**OBS** The window module registers for `activewindow` (S202 line 27). The
module text is formed upstream of any pixel.

### What this does not license

**UNK** Whether this host's bar uses the Hyprland window module is unverified.
No module text was observed. Upstream source is not host behavior.
