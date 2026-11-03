
### Surface state register (2026-11-03, rehearsal copy — NOT a landing)

Rehearsal of the C1 landing shape: eight rows, one per surface group, each with a probe and a
committed round-65 receipt pointer; the live gate run is
`.ufo/waves/round-65/receipts/gate-live-r65.txt` and the file-plane run
`.ufo/waves/round-65/receipts/gate-fileplane-r65.txt`.

| surface group | state (2026-11-03) | probe (read-only) | receipt |
|---|---|---|---|
| hypr plane | present (2026-11-03) | `hyprctl -j version` → 0.56.2 | `.ufo/waves/round-65/receipts/before-register-probes-r65.txt` |
| waybar | present (2026-11-03) | `command -v waybar` | `.ufo/waves/round-65/receipts/before-register-probes-r65.txt` |
| walker | present (2026-11-03) | `command -v walker` | `.ufo/waves/round-65/receipts/before-register-probes-r65.txt` |
| terminal configs | present (2026-11-03) | `test -d ~/.config/alacritty` | `.ufo/waves/round-65/receipts/before-register-probes-r65.txt` |
| theme/wallpaper omarchy plane | present (2026-11-03) | `test -d ~/.config/omarchy` | `.ufo/waves/round-65/receipts/before-state-r65.txt` |
| idle/lock plane | present (2026-11-03) | `command -v hypridle hyprlock` | `.ufo/waves/round-65/receipts/census-start-r65.txt` |
| omarchy skill docs | present (2026-11-03) | `test -d ~/.agents/skills/omarchy` | `.ufo/waves/round-65/receipts/control-c1-c2-base-r65.txt` |
| windows desktop plane | unobservable (2026-11-03) | `command -v powershell` → not found | `.ufo/waves/round-65/receipts/gate-fileplane-r65.txt` |

<!-- r65 register end -->
