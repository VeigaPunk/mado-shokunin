#!/usr/bin/env bash
# Score one w1 C1 control tool against the FROZEN c1 counter on a scratch clone. Usage: score-one.sh CONTROL_PY TAG
set -eu
ulimit -f 2048
L=/home/vgpnk/Projects/shokunin/mado-shokunin
TOOL=$1; TAG=$2
S=/fast/scratch/hyaku/mado-r48/ScoutControls/$TAG
rm -rf "$S"; mkdir -p "$S/c" "$S/work"
D=$S/c/clone
git clone -q --shared --no-checkout "$L" "$D"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ]
git -C "$D" checkout -q 3e6c848a -- tools quality/counters .ufo/waves/round-47/fetch
cp "$TOOL" "$D/tools/mado-terminal.py"
git -C "$D" add -A
git -C "$D" -c user.name=scout -c user.email=scout@local commit -qm "score $TAG"
cd "$D"
python3 -I quality/counters/c1-r48-terminal-cache.py --repo "$D" --rev HEAD --work "$S/work" --nonce 4848 > "$S/out.txt" 2>&1 || true
tail -12 "$S/out.txt"
