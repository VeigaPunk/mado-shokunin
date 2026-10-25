# ScoutLogger — scout seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: scout

Re-open Hyprland v0.56.2's logger (https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/log/Logger.cpp; `cmp` with /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/fetch/S214.bin) and, at the same commit, find: (1) where `debug:disable_logs` is declared and its default (search the config descriptions/defaults sources via `https://api.github.com/repos/hyprwm/Hyprland/git/trees/efb50993780079460b0cbed1363e2166a2de1d9f?recursive=1` then raw files); (2) how aquamarine's log lines reach hyprland.log — do they bypass `m_logsEnabled` (find the aquamarine/hyprutils log callback wiring, e.g. in Compositor.cpp, cite lines); (3) whether ERR/CRIT levels are exempt from `m_logsEnabled` anywhere. Report line-cited answers; these decide the observability entry's §2-§3 and its Unknowns.
