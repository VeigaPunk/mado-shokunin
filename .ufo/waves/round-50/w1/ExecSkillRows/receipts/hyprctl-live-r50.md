# ExecSkillRows r50 — live read-only compositor reads used by the decision rows (2026-10-27)
# reads: hyprctl version | getoption input:{resolve_binds_by_sym,kb_layout,kb_options,kb_file,layout} | binds -j | devices -j
hyprctl_getoption_input:resolve_binds_by_sym: {"option": "input:resolve_binds_by_sym", "int": 0, "set": false }
hyprctl_getoption_input:kb_layout:          {"option": "input:kb_layout", "str": "br", "set": true }
hyprctl_getoption_input:kb_options:         {"option": "input:kb_options", "str": "compose:caps", "set": true }
hyprctl_getoption_input:kb_file:            {"option": "input:kb_file", "str": "[[EMPTY]]", "set": false }
hyprctl_getoption_device:resolve_binds_by_sym: no such option
hyprctl_getoption_input:layout:             no such option
hyprctl_version_first_line: Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs).
# binds/devices tallies: receipts/binds-tally-r50.md (raw JSON kept in scratch only; not committed)
# row 2 live read matches the round-49 receipt: resolve_binds_by_sym {"int": 0, "set": false} -> false, default 0
# row 9 submap read: all 192 rows carry submap "" -> the submap branch cannot be exercised on this host today
