# Round 54 source opens — L1 pre-freeze manifest (2026-10-27)

All pins fetched 2026-10-27 (America/Sao_Paulo) by the lane L1 before any wave
dispatch, from the canonical upstream of the host-installed uwsm 0.27.1
(`uwsm --version` → `uwsm 0.27.1`; `/usr/bin/uwsm-app` shell client present).
GitHub mirror of Vladimir-csp/uwsm pinned at annotated-tag commit
`0727985c9bae655bda488f87f99ea69a6ac1c003` (tag `v0.27.1`); the freedesktop
GitLab primary carries only tags ≤ v0.27.0 at open time, so the mirror tag is
the pin (recorded, not assumed).

| file | source URL | bytes |
|---|---|---|
| `uwsm-0.27.1-README.md` | https://raw.githubusercontent.com/Vladimir-csp/uwsm/0727985c9bae655bda488f87f99ea69a6ac1c003/README.md | 49,717 |
| `uwsm-0.27.1-main.py` | https://raw.githubusercontent.com/Vladimir-csp/uwsm/0727985c9bae655bda488f87f99ea69a6ac1c003/uwsm/main.py | 199,361 |
| `uwsm-0.27.1-uwsm-app.1.scd` | https://raw.githubusercontent.com/Vladimir-csp/uwsm/0727985c9bae655bda488f87f99ea69a6ac1c003/man/uwsm-app.1.scd | 2,309 |

Hashes in `SHA256SUMS.txt`. Host join points read-only at the same time:
`~/.local/share/omarchy/default/hypr/autostart.conf:1-6` (six `exec-once = uwsm-app -- …` lines: hypridle, mako, waybar, fcitx5, swaybg, omarchy-hyprland-monitor-watch), `~/.config/hypr/bindings.conf:2` (`SUPER, RETURN` → `uwsm-app -- xdg-terminal-exec …`), `~/.local/share/omarchy/bin/omarchy-toggle-idle:9` (`uwsm-app -- hypridle`). See `../registration.md` C2 fixture inventory.
