# ScoutWaybarDrop — scout seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: scout

Re-open Waybar 0.15.0's Hyprland IPC backend yourself (https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp; `cmp` with /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/fetch/S201.bin) and answer with line citations: what does `socketListener()` do when the compositor closes the connection (read returns 0 or error) — does it reconnect, retry, log, or stop silently? What is the read buffer size and how is a partial / multi-event read split? Is the event socket read on its own thread (so a slow module handler cannot stall the read)? Then say whether the package's inference "a blocked custom-module producer can cost the bar its whole compositor-event feed … with no error shown" holds, is contradicted, or is undetermined by these bytes.
