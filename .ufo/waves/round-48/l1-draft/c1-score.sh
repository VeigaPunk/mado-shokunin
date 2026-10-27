#!/usr/bin/env bash
# L1 pre-freeze: score the l1-draft C1 counter (+ merged fixtures) on a scratch clone whose tools/mado-terminal.py is TOOL.
# Usage: c1-score.sh TOOL TAG [NONCE]   (writes nothing in the lane; scratch under /fast/scratch/hyaku/mado-r48/L1c1-TAG)
set -eu
L=/home/vgpnk/Projects/shokunin/mado-shokunin
H=$L/.ufo/waves/round-48/l1-draft
TOOL=$1; TAG=$2; NONCE=${3:-4848}
S=/fast/scratch/hyaku/mado-r48/L1c1-$TAG
rm -rf "$S"; mkdir -p "$S/c" "$S/work"
D=$S/c/clone
git clone -q --shared "$L" "$D"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ]
git -C "$D" checkout -q 579f694b45c797a9c39761fdb4f9e0a1b71b3585
if [ "$TOOL" = "-" ]; then rm -f "$D/tools/mado-terminal.py"; else cp "$TOOL" "$D/tools/mado-terminal.py"; fi
cp "$H/c1-r48-terminal-cache.py" "$H/c1-r48-fixtures.json" "$D/quality/counters/"
git -C "$D" add -A
git -C "$D" -c user.name=t -c user.email=t@t commit -qm "c1 score $TAG"
cd "$D"
python3 -I quality/counters/c1-r48-terminal-cache.py --repo "$D" --rev HEAD --work "$S/work" --nonce "$NONCE" > "$S/out.txt" 2>&1 || true
grep -v ' pass$' "$S/out.txt" | tail -${TAILN:-25}
rm -rf "$S/c" "$S/work"
