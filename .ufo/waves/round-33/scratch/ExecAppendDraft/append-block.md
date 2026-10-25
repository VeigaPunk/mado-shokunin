# Draft append block — corpus/SOURCES.md (round-33 w1)

Source rows: `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md` lines 11, 12, 18.
Normalizations applied per seat prompt: `status` -> `mined`, `opened` -> `2026-10-24`,
`recheck` -> `90d`, `used-by` -> exactly the admitting entry. Anchor corrections taken
from the w1 scout re-fetches (ScoutS190, ScoutS191, ScoutS197 reports) are folded into
the `anchor` and `teaches` cells — the staged anchor ranges did not cover the named
symbols and the staged registration counts understate the code.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S190 | Waybar 0.15.0 Hyprland IPC backend — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/backend.cpp | code | A | How the bar's Hyprland modules obtain their data: socket-folder derivation, the socket2 subscription, the event-name split and the event read size | `src/modules/hyprland/backend.cpp:19-44` (`getSocketFolder`, socket path and `/tmp/hypr` fallback), `:77-139` (`socketListener`, `.socket2.sock` connect and 1024-byte read buffer), `:141-150` (`parseIPC`) @ tag `0.15.0`, 6550 B, sha256 prefix `799bf02f6d18ae04` | Waybar connects to the compositor's `.socket2.sock` under `$XDG_RUNTIME_DIR/hypr/[HIS]` (falling back to `/tmp/hypr`), reads each event line into a 1024-byte buffer and splits the event name at the first `>` | mined | 2026-10-24 | 90d | corpus/knowledge/waybar-module-text-route-r25.md |
| S191 | Waybar 0.15.0 Hyprland window module — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/window.cpp | code | A | Where the bar's active-window module text is formed and handed to the widget: the module-text production step that stands upstream of any rendering | `src/modules/hyprland/window.cpp:27-31` (five `registerForIPC` calls in the constructor), `:54-64` (`fmt` + `rewriteString` + `set_markup`) @ tag `0.15.0`, 8324 B, sha256 prefix `5df496eb3cfe5cae` | The window module subscribes to `activewindow`, `closewindow`, `movewindow`, `changefloatingmode` and `fullscreen`, builds its text from the `title`, `initialTitle`, `class` and `initialClass` placeholders, applies the rewrite rules and sets the result as GTK markup | mined | 2026-10-24 | 90d | corpus/knowledge/waybar-module-text-route-r25.md |
| S197 | Waybar 0.15.0 Hyprland workspaces module — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/workspaces.cpp | code | A | The producer of the one bar element this host actually uses from the Hyprland family: how the workspace module subscribes to compositor events and how its label text is formed | `src/modules/hyprland/workspaces.cpp:154-159` (window rewrite via `fmt::format`), `:803-829` (`registerIpc`: twelve unconditional registrations plus conditional `windowtitlev2` and `activewindowv2`) @ tag `0.15.0`, 41392 B (sha256 prefix `1e19d92638e7923f`) | The workspace module subscribes unconditionally to `workspacev2`, `activespecial`, `createworkspacev2`, `destroyworkspacev2`, `focusedmonv2`, `moveworkspacev2`, `renameworkspace`, `openwindow`, `closewindow`, `movewindowv2`, `urgent` and `configreloaded`, and conditionally to `windowtitlev2` (when the title rewrite or taskbar-with-title is configured) and `activewindowv2` (when active-window tracking is enabled), then formats the label through fmt placeholders | mined | 2026-10-24 | 90d | corpus/knowledge/event-delivery-limits-r26.md |

## Stripped recheck prose

Original staged `recheck` cells, replaced by `90d` above, recorded verbatim:

- S190: `on-release — re-pull at tag 0.15.0 and compare sha256 (expect prefix 799bf02f6d18ae04) (ran 2026-10-23)`
- S191: `on-release — re-pull at tag 0.15.0 and compare sha256 (expect prefix 5df496eb3cfe5cae) (ran 2026-10-23)`
- S197: `on-release — re-pull at tag 0.15.0 and compare sha256 (expect prefix 1e19d92638e7923f) (ran 2026-10-23)`
