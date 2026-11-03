# Fixture province (R65ExecC1Counter resolution leg control: one pointer names no file)

Intro line; no receipt pointers here.

### Surface state register (2026-11-03, fixture host)

| surface group | state (2026-11-03) | probe (read-only) | receipt |
|---|---|---|---|
| hypr plane | present (2026-11-03) | `command -v hyprctl` → /usr/bin/hyprctl | `.ufo/waves/round-65/receipts/probe-hypr-r65.txt` |
| waybar | present (2026-11-03) | `command -v waybar` → /usr/bin/waybar | `.ufo/waves/round-65/receipts/gate-live-r65.txt` |
| walker | present (2026-11-03) | `command -v walker` → /usr/bin/walker | `.ufo/waves/round-65/receipts/absent-r65.txt` |
| terminal configs | present (2026-11-03) | `test -d ~/.config/alacritty` → yes | `.ufo/waves/round-65/receipts/probe-hypr-r65.txt` |
| theme/wallpaper omarchy plane | present (2026-11-03) | `test -d ~/.config/omarchy` → yes | `.ufo/waves/round-65/receipts/probe-hypr-r65.txt` |
| idle/lock plane | present (2026-11-03) | `command -v hypridle hyprlock` → both | `.ufo/waves/round-65/receipts/probe-hypr-r65.txt` |
| omarchy skill docs | present (2026-11-03) | `test -d ~/.agents/skills/omarchy` → yes | `.ufo/waves/round-65/receipts/probe-hypr-r65.txt` |
| windows desktop plane | unobservable (2026-11-03) | `command -v powershell` → not found | `.ufo/waves/round-65/receipts/probe-hypr-r65.txt` |

<!-- r65 register end -->
