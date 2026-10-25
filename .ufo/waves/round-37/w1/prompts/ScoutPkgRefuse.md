# ScoutPkgRefuse — scout seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: scout

Try to FALSIFY the round's two refusals. The registration refuses the package's r28 (session log) and r29 (unit journal) "never overflowed" readings as null channels because `debug:disable_logs` = 1. Look for any channel on this host where a core-logger ERR line would appear despite that setting (crash reports under ~/.cache/hyprland or ~/.local/share/hyprland, coredump metadata via `coredumpctl list hyprland --no-pager` (read-only), stderr capture in the uwsm unit, the rolling log). If any channel carries core-logger lines after config load, the refusal reason is wrong for that channel — report it with counts (never raw text). Also check: did `debug:disable_logs` have the same value in earlier sessions (is there any record)? A refusal that survives your attack is reported as survived, with what you tried.
