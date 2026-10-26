T="python3 -I ../mado-monitors.py"
c(){ label="$1"; conf="$2"; json="$3"; echo "### $label"; printf '%s' "$conf" > x.conf; $T --monitors "$json" --config x.conf; echo "rc=$?"; echo; }
c "R1a bracket monitorv2 mode + legacy explicit mode; live = v2 mode" 'monitor = DP-1, 1920x1080@60, 0x0, 1
monitorv2[DP-1] {
    mode = 3440x1440@100
}
' one.json
c "R1b bracket monitorv2 disabled; live disabled=true" 'monitor = DP-1, 3440x1440@100, 0x0, 1
monitorv2[DP-1] {
    disabled = 1
}
' one-disabled.json
c "R2a desc selector padded with spaces" 'monitor = desc:  Dell Inc. DELL U3415W  , 3440x1440@100, 0x0, 1
' one.json
c "R2b desc selector padded with tab" 'monitor = desc:	Dell Inc. DELL U3415W	, 3440x1440@100, 0x0, 1
' one.json
c "R2c desc selector padded with vertical tab (0x0b)" "$(printf 'monitor = desc:\vDell Inc. DELL U3415W\v, 3440x1440@100, 0x0, 1\n')" one.json
c "R3a mirror line with transform key; live transform=3 mirrorOf=0" 'monitor = DP-1, 3440x1440@100, 0x0, 1
monitor = DP-2, 3440x1440@100, 0x0, 1, mirror, DP-1, transform, 3
' two-mirror-t3.json
c "R3b mirror line, transform 07 on the mirror line" 'monitor = DP-1, 3440x1440@100, 0x0, 1
monitor = DP-2, 3440x1440@100, 0x0, 1, mirror, DP-1, transform, 07
' two-mirror-t3.json
c "R3c self-mirror rule; Hyprland refuses (Cannot mirror self)" 'monitor = DP-1, 3440x1440@100, 0x0, 1
monitor = DP-2, 3440x1440@100, 0x0, 1, mirror, DP-2
' two-selfmirror.json
c "R3d mirror target given as desc: selector" 'monitor = DP-1, 3440x1440@100, 0x0, 1
monitor = DP-2, 3440x1440@100, 0x0, 1, mirror, desc:Dell Inc.
' two-mirror-t3.json
c "R4a disable rule; live enabled (runtime re-enable)" 'monitor = DP-1, disable
' one.json
c "R4b disable rule; live disabled" 'monitor = DP-1, disable
' one-disabled.json
c "R5a addreserved with no prior rule (default rule added)" 'monitor = DP-1, addreserved, 10, 20, 30, 40
' one.json
c "R5b addreserved after an explicit rule (reserved not compared)" 'monitor = DP-1, 3440x1440@100, 0x0, 1
monitor = DP-1, addreserved, 10, 20, 30, 40
' one.json
c "R5c addreserved with stoi prefixes +5/10abc/1.5/0x10" 'monitor = DP-1, addreserved, +5, 10abc, 1.5, 0x10
' one.json
c "R5d addreserved with three numbers (stoi of empty throws)" 'monitor = DP-1, addreserved, 10, 20, 30
' one.json
c "R6a auto-left position, live x=3440 (position not compared)" 'monitor = DP-1, 3440x1440@100, auto-left, 1
' two-pos.json
c "R6b auto-right vs live x=3440" 'monitor = DP-1, 3440x1440@100, auto-right, 1
' two-pos.json
