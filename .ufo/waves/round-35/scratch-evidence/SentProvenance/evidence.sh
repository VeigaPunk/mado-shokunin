#!/bin/bash
R=/home/vgpnk/Projects/shokunin/mado-shokunin
O=/home/vgpnk/.local/share/omarchy
run() { local id="$1"; shift; local out; out=$("$@" 2>&1); local rc=$?; printf '%s\t%s\t%s\n' "$id" "$rc" "$(printf '%s' "$out" | tr '\n' '|' | cut -c1-200)"; }
echo -e "id\trc\toutput"
run S203.sha sha256sum $O/bin/omarchy-first-run
run S203.size stat -c '%s' $O/bin/omarchy-first-run
run S203.shcount bash -c "ls -1 $O/install/first-run/*.sh | wc -l"
run S203.allcount bash -c "ls -1 $O/install/first-run | wc -l"
run S203.bashcalls bash -c "grep -c 'bash \"\$OMARCHY_PATH/install/first-run/' $O/bin/omarchy-first-run"
run S203.idlehits bash -c "grep -ril idle $O/install/first-run | wc -l"
run S203.line3 sed -n '3p' $O/bin/omarchy-first-run
run S204.cmd bash -c "journalctl --user --no-pager | grep -c 'omarchy-toggle'"
run S204.hypridlelines bash -c "journalctl --user --no-pager | grep -ci hypridle"
run S204.apphypridle bash -c "journalctl --user --no-pager | grep -c 'app -- hypridle'"
run S204.boots bash -c "journalctl --user --list-boots --no-pager | tail -n +2 | wc -l"
run S204.earliest bash -c "journalctl --user --no-pager | head -1 | cut -c1-15"
run S204.startlines bash -c "journalctl --user --no-pager | grep 'Started hypridle' | tr '\n' ';'"
run S204.stoplines bash -c "journalctl --user --no-pager | grep 'Stopped hypridle' | tr '\n' ';'"
run S204.shcount bash -c "ls -1 $O/install/first-run/*.sh | wc -l"
run S205.pgrep bash -c "pgrep -a hypridle"
run S205.pgrep_rc bash -c "pgrep -x hyprlock; echo hyprlock_rc=\$?"
run S205.confsha sha256sum /home/vgpnk/.config/hypr/hypridle.conf
run S205.confbytes stat -c '%s' /home/vgpnk/.config/hypr/hypridle.conf
run S205.timeouts bash -c "grep -n 'timeout = ' /home/vgpnk/.config/hypr/hypridle.conf | tr '\n' ';'"
run S205.isactive bash -c "systemctl --user is-active hypridle"
run S205.decl bash -c "sed -n '2p;3p;5p;11p;17p' /home/vgpnk/.config/hypr/hypridle.conf | tr '\n' ';'"
run S205.scope bash -c "systemctl --user list-units --all --no-pager | grep -i hypridle | tr -s ' ' | cut -c1-90"
run S206.sha sha256sum /home/vgpnk/.config/waybar/config.jsonc
run S206.size stat -c '%s' /home/vgpnk/.config/waybar/config.jsonc
run S206.lines bash -c "sed -n '18p;19p' /home/vgpnk/.config/waybar/config.jsonc | tr '\n' ';'"
run S206.block bash -c "sed -n '207,212p' /home/vgpnk/.config/waybar/config.jsonc | tr '\n' ';'"
run S206.handlers bash -c "grep -c omarchy-toggle-idle /home/vgpnk/.config/waybar/config.jsonc"
run S207.sha sha256sum $O/default/waybar/indicators/idle.sh
run S207.size stat -c '%s' $O/default/waybar/indicators/idle.sh
run S207.body bash -c "sed -n '3,6p' $O/default/waybar/indicators/idle.sh | tr '\n' ';'"
run S207.tooltip bash -c "grep -c 'Idle lock disabled' $O/default/waybar/indicators/idle.sh"
run S207.lines stat -c '%s' $O/default/waybar/indicators/idle.sh
run S208.sha sha256sum $O/bin/omarchy-menu
run S208.size stat -c '%s' $O/bin/omarchy-menu
run S208.l207 bash -c "sed -n '207p' $O/bin/omarchy-menu | cut -c1-120"
run S208.l212 bash -c "sed -n '212p' $O/bin/omarchy-menu"
run S208.arms bash -c "grep -c omarchy-toggle-idle $O/bin/omarchy-menu"
run S209.count bash -c "ls -1 /home/vgpnk/.config/waybar/config.jsonc.bak* | wc -l"
run S209.handlers bash -c "for f in /home/vgpnk/.config/waybar/config.jsonc.bak*; do printf '%s=%s ' \$(basename \$f) \$(grep -c omarchy-toggle-idle \$f); done"
run S209.mtimes bash -c "stat -c '%y %n' /home/vgpnk/.config/waybar/config.jsonc.bak* | sed 's#/home/vgpnk/.config/waybar/##' | tr '\n' ';'"
run S209.oldest bash -c "stat -c '%Y %y %n' /home/vgpnk/.config/waybar/config.jsonc.bak* | sort -n | head -1"
run S209.epoch bash -c "date -d @1791314470 -Is"
run S210.count bash -c "ls -1A /home/vgpnk/.local/state/omarchy/toggles/hypr | wc -l"
run S210.names bash -c "ls -1A /home/vgpnk/.local/state/omarchy/toggles/hypr | tr '\n' ';'"
run S210.idlefiles bash -c "grep -ril idle /home/vgpnk/.local/state/omarchy/toggles/hypr | wc -l"
run S210.onlydir bash -c "ls -1A /home/vgpnk/.local/state/omarchy/toggles | tr '\n' ';'"
run S210.togglewrites bash -c "grep -c 'toggles' $O/bin/omarchy-toggle-idle"
