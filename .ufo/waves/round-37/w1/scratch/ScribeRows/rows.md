# ScribeRows — draft SOURCES.md registry rows, mado round 37 (scratch, not appended)

Schema: `/home/vgpnk/Projects/shokunin/CORPUS.md` § "SOURCES.md — where a shokunin learns"
(11 columns: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by).
Style models: LANE `corpus/SOURCES.md` rows S189 (line 201, code, backticked anchors) and
S201 (line 203); own-work style from S203–S210 (` - ` separators, receipt sha256).

## New rows (append at the end of `## Registry`, after S211)

| S212 | Waybar 0.15.0 Hyprland workspaces module — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/workspaces.cpp | code | A | Which compositor events the bar's workspace module, the event-socket client this host runs, subscribes to | `src/modules/hyprland/workspaces.cpp:803` (registerIpc), `:804-815` (twelve unconditional event registrations), `:817-821` (windowtitlev2 only when a rewrite rule or the taskbar uses the title) @ tag `0.15.0`, 41392 B, sha256 prefix `1e19d92638e7923f` | The workspace module registers twelve compositor events unconditionally (workspacev2, activespecial, createworkspacev2, destroyworkspacev2, focusedmonv2, moveworkspacev2, renameworkspace, openwindow, closewindow, movewindowv2, urgent, configreloaded) and windowtitlev2 only when a rewrite rule or the taskbar uses the title, so the bar's workspace element is fed by the event socket | mined | 2026-10-25 | 90d | corpus/knowledge/event-delivery-limits-r26.md |
| S213 | host compositor log channels - the current session log, the compositor unit journal and the live debug log options, counted for the two event-socket failure markers (measured on this host) - .ufo/waves/round-37/fetch/S213.receipt.txt | own-work | A | Whether this host's compositor log channels can show that an event-socket client was dropped | sections session log, compositor unit journal and live options in .ufo/waves/round-37/fetch/S213.receipt.txt, taken 2026-10-25T09:00:04-03:00 against Hyprland v0.56.2 efb50993780079460b0cbed1363e2166a2de1d9f; receipt 1814 B, sha256 1c1b0ce149ecd7b1d20b0a83f266197c89c9f5334d17dc035fe499d93272ce58 | On this host debug:disable_logs is 1, the session log's 21 core-logger lines end at line 21 and every later line is from aquamarine, and both the log and the unit journal count zero for the overflow and write-failure markers - a null channel that cannot tell never-overflowed from not-logged | mined | 2026-10-25 | on-change | corpus/knowledge/event-queue-observability-r37.md |
| S214 | Hyprland v0.56.2 core logger — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/log/Logger.cpp | code | A | Whether the compositor's core logger writes any line, the event-socket failure markers included, when debug:disable_logs is set | `src/debug/log/Logger.cpp:14-16` (log returns when logs are disabled), `:21-24` (rolling-log follower and file write come after that return), `:37` (recheck on config reload), `:42` (reads debug:disable_logs), `:48` (m_logsEnabled = !disable_logs) @ commit `efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2), 1789 B, sha256 prefix `d04e3a2fe5c73ad8` | With debug:disable_logs set, CLogger::log returns before the rolling-log follower, the log file and stdout, so every core-logger line, including the event manager's overflow and write-failure markers, is dropped at the source | mined | 2026-10-25 | 90d | corpus/knowledge/event-queue-observability-r37.md |

## In-place used-by changes (log old→new in the round lesson, CORPUS.md SOURCES rule 2)

| id | column | old | new |
|---|---|---|---|
| S189 | used-by | `corpus/knowledge/ipc-contract-r25.md` | `corpus/knowledge/ipc-contract-r25.md, corpus/knowledge/event-delivery-limits-r26.md, corpus/knowledge/event-queue-observability-r37.md` |
| S201 | used-by | `corpus/knowledge/waybar-module-text-route-r25.md` | `corpus/knowledge/waybar-module-text-route-r25.md, corpus/knowledge/event-delivery-limits-r26.md` |

Full S189 / S201 rows are otherwise unchanged (status `mined`, opened `2026-10-24`, recheck `90d`).
