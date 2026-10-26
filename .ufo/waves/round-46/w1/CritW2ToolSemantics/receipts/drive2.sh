T="python3 -I ../mado-monitors.py"
c(){ label="$1"; conf="$2"; json="$3"; echo "### $label"; printf '%s' "$conf" > x.conf; $T --monitors "$json" --config x.conf; echo "rc=$?"; echo; }
c "R3e self-mirror rule; live mirrorOf=none (Hyprland refuses self)" 'monitor = DP-1, 3440x1440@100, 0x0, 1
monitor = DP-2, 3440x1440@100, 0x0, 1, mirror, DP-2
' two.json
c "R3f chained mirror: DP-1 rule mirrors DP-2, DP-2 rule mirrors DP-1" 'monitor = DP-1, 3440x1440@100, 0x0, 1, mirror, DP-2
monitor = DP-2, 3440x1440@100, 0x0, 1, mirror, DP-1
' two-chained.json
c "R3g mirror target desc:Dell Inc.; live mirrorOf=0" 'monitor = DP-1, 3440x1440@100, 0x0, 1
monitor = DP-2, 3440x1440@100, 0x0, 1, mirror, desc:Dell Inc.
' two-mirror.json
c "R7a config holds only source = monitors.conf (no monitor lines)" 'source = monitors.conf
' one.json
c "R7b monitorv2[ DP-1 ] with inner spaces" 'monitor = DP-1, 1920x1080@60, 0x0, 1
monitorv2[ DP-1 ] {
    mode = 3440x1440@100
}
' one.json
c "R7c monitorv2{ (no space before brace)" 'monitor = DP-1, 1920x1080@60, 0x0, 1
monitorv2{
    output = DP-1
    mode = 3440x1440@100
}
' one.json
c "R8a transform modifier with no prior rule (both: nothing happens)" 'monitor = DP-2, transform, 3
' two.json
c "R8b addreserved with extra trailing fields" 'monitor = DP-1, 3440x1440@100, 0x0, 1
monitor = DP-1, addreserved, 10, 20, 30, 40, transform, 3
' one.json
