# RevHarmBefore — reviewer seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Harm-watch baseline at the freeze tip, read-only: `cd /home/vgpnk/Projects/shokunin/mado-shokunin && bash tools/mado-verify.sh --selftest` (final MADO_SELFTEST line + exit), `sha256sum tools/mado-verify.sh`, `python3 -I quality/check-index.py --repo .`, `python3 -I quality/check-index-rows.py --repo .`, `python3 -I quality/check-axis-scores.py --repo . --rev master`, `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`, and sha256 of `~/.config/hypr/*.conf ~/.config/waybar/config.jsonc ~/.config/waybar/style.css` plus `coredumpctl list --no-pager 2>/dev/null | grep -ci hyprland`. Report every summary line and exit code — this is the before-side of the round's no-harm check.
