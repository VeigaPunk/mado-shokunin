# ScoutS210 — toggle-state sweep re-run (read-only, 2026-10-24)

## Finding

Count is **0** — confirmed. The directory holds exactly 2 files and neither names the idle lock. Receipt S210 is accurate on both claims.

## Directory contents

`/home/vgpnk/.local/state/omarchy/toggles/hypr/` — 2 files, no other entries:

| file | content | names idle lock? |
|---|---|---|
| `flags.conf` (135 B) | Placeholder comment only: "intended for permanent config toggle flags. Do not remove this file" | no |
| `window-no-gaps.conf` (141 B) | Hyprland snippet zeroing `gaps_out`, `gaps_in`, `border_size`, `rounding` | no |

No idle-lock toggle (no hypridle/hyprlock/idle entry) exists in this directory.

## Evidence

- `read /home/vgpnk/.local/state/omarchy/toggles/hypr/` → lists `window-no-gaps.conf`, `flags.conf` only.
- `read` on each file → contents above; no occurrence of `idle`, `lock`, `hypridle`, `hyprlock`, or `swayidle` in either.
- Receipt compared: `.ufo/waves/round-35/fetch/S210.receipt.txt` states 2 files / 0 idle-lock files — matches live state.
