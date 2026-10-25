# ScoutHostProbe — scout seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: scout

Harm watch, read-only: record the sha256 of the declared config planes at this moment — `~/.config/hypr/*.conf`, `~/.config/waybar/config.jsonc`, `~/.config/waybar/style.css`, `~/.config/hypr/hypridle.conf`, `~/.config/hypr/hyprlock.conf` — and compare them with the pins the lane already holds (LANE/SKILL.md version pins; LANE/corpus/knowledge/idle-lock-plane.md sha256 lines). Report any drift with both hashes. Do not write, do not restart anything.
