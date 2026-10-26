#!/bin/sh
# probe_tool_agree.sh - end-to-end witness through the reference tool itself:
# a rule scale Hyprland can never apply (its "no clean divisor" arm replaces the
# scale with getDefaultScale()) is not compared by the tool -> AGREE / OK on a
# scale that the output does not actually run.
set -eu
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/w1/ExecScaleOracle
TOOL=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/l1-draft/mado-monitors.py
S=${1:-/fast/scratch/hyaku/mado-r45/ExecScaleOracle}
mkdir -p "$S"
cd "$S"
cat > mons.json <<'EOF'
[{"id":0,"name":"DP-1","description":"Acme XY 123","width":1234,"height":567,"refreshRate":60.0,"x":0,"y":0,"scale":1.0,"transform":0,"mirrorOf":"none","disabled":false}]
EOF
{
  echo "#!/ front matter: live scale 1.0, i.e. what getDefaultScale() gives on a <=140 PPI output"
  for sc in 1.75 1.8 2.0 2.5; do
    printf 'monitor = DP-1, 1234x567, 0x0, %s\n' "$sc" > "cfg-$sc.conf"
    echo "\$ python3 -I $TOOL --monitors mons.json --config cfg-$sc.conf"
    python3 -I "$TOOL" --monitors mons.json --config "cfg-$sc.conf"
    echo "exit=$?"
    echo
  done
  echo "# control: 3440x1440 ruled at 1, the host's own line (scale divides, no correction)"
  cat > mons2.json <<'EOF'
[{"id":0,"name":"DP-1","description":"Acme XY 123","width":3440,"height":1440,"refreshRate":100.0,"x":0,"y":0,"scale":1.0,"transform":0,"mirrorOf":"none","disabled":false}]
EOF
  printf 'monitor = DP-1, 3440x1440@100, 0x0, 1\n' > cfg-host.conf
  echo "\$ python3 -I $TOOL --monitors mons2.json --config cfg-host.conf"
  python3 -I "$TOOL" --monitors mons2.json --config cfg-host.conf
  echo "exit=$?"
} > "$SEAT/receipts/tool-false-agree.txt" 2>&1
cat "$SEAT/receipts/tool-false-agree.txt"
