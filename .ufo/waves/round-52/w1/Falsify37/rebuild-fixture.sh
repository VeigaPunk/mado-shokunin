#!/usr/bin/env bash
# Rebuild the Falsify37 fixture repo from lane base 85d57a8 + seat-dir copies.
# Usage: rebuild-fixture.sh <fixture-dir>
# Reads the lane repo READ-ONLY (git archive); writes only <fixture-dir>.
# Then run:
#   python3 "$SEAT/pred-c2-r52-frozen.py" "$FIX" "$REV" "$BASE_REV" <scratch>
#   python3 "$SEAT/pred-c2-r52-frozen.py" "$FIX" "$BASE_REV" "$BASE_REV" <scratch>
set -euo pipefail
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
BASE=85d57a818c3707397e21c840b6498b105ba798aa
SEAT="$LANE/.ufo/waves/round-52/w1/Falsify37"
FIX="${1:?usage: rebuild-fixture.sh <fixture-dir>}"
FIX=$(readlink -f "$FIX")

test "$(git -C "$LANE" rev-parse --show-toplevel)" = "$LANE"   # lane intact; read-only use
rm -rf "$FIX" && mkdir -p "$FIX"
git -C "$LANE" archive "$BASE" corpus .ufo/waves/round-51/fetch | tar -x -C "$FIX"

git -C "$FIX" init -q -b main
test "$(git -C "$FIX" rev-parse --show-toplevel)" = "$FIX"     # guard: fixture toplevel
git -C "$FIX" add -A
git -C "$FIX" -c user.email=falsify37@seat -c user.name=Falsify37 \
    commit -qm "base snapshot $BASE (corpus + round-51 fetch pins)"
BASE_REV=$(git -C "$FIX" rev-parse HEAD)

mkdir -p "$FIX/corpus/knowledge"
cp "$SEAT/fixture-entry.md"  "$FIX/corpus/knowledge/hyprland-dispatcher-entail-bypass-r52.md"
cp "$SEAT/fixture-README.md" "$FIX/corpus/README.md"
git -C "$FIX" add -A
git -C "$FIX" -c user.email=falsify37@seat -c user.name=Falsify37 \
    commit -qm "adversarial entry: four propositions, each bound to a real quote that does not entail it"
REV=$(git -C "$FIX" rev-parse HEAD)

echo "base_rev=$BASE_REV"
echo "rev=$REV"
