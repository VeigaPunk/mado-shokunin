# ScoutRollingLog — scout seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: scout

Test the null-channel claim through a third channel, read-only: run `hyprctl rollinglog` (a read verb; never `-f` follow longer than 5 s, never any write verb) and report: line count, how many lines are core-logger lines (prefix like `DEBUG ]:` with no `from`), and how many are aquamarine. Compare with the session log's last 200 lines (`tail -n 200 $XDG_RUNTIME_DIR/hypr/*/hyprland.log | sed -E 's/^([A-Z]+( from [a-z]+)? \]).*/\1/' | sort | uniq -c`). Read S214 Logger.cpp:21-22 (/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/fetch/S214.bin) — the rolling-log feed is after the `m_logsEnabled` return — and say whether the observation agrees. Counts only; never paste raw log text beyond the prefix histogram.
