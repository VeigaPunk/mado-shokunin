#!/usr/bin/env bash
# Score the shape-keeping do-nothing entry variants against PRED-C2-r44-v2.
# Every git call names -C $D (fixture clone); the lane is never written.
set -u
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/w2/ExecDoNothingV2
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
S=/fast/scratch/hyaku/mado-r44/ExecDoNothingV2
D=$S/fixture
DATA=e46789213830597348fe96a351ae004d10587385
ENTRY=corpus/knowledge/hyprland-gkeep-size-request-r44.md
COUNTER=$LANE/quality/counters/c2-r44-gkeep-size-request-v2.py
mkdir -p "$S" "$SEAT/receipts"
if [ ! -d "$D/.git" ]; then
  git clone -q --shared "$LANE" "$D" || exit 9
fi
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "fixture toplevel wrong"; exit 9; }

run() {  # name variant-file
  local name=$1 file=$2
  git -C "$D" checkout -q -B "v-$name" "$DATA" || return 9
  cp "$file" "$D/$ENTRY"
  git -C "$D" add -A
  git -C "$D" -c user.name=ExecDoNothingV2 -c user.email=exec@lane.invalid \
      commit -q -m "do-nothing control: $name" || return 9
  local rev; rev=$(git -C "$D" rev-parse HEAD)
  ( cd "$LANE" && python3 -I "$COUNTER" --repo "$D" --rev "$rev" ) \
      > "$SEAT/receipts/c2-$name.txt" 2>&1
  local rc=$?
  echo "== $name rev=$rev exit=$rc"
  grep -E 'clause=[a-j] |admitted=|verdict=' "$SEAT/receipts/c2-$name.txt" | tail -6
}
mkdir -p "$SEAT/receipts"
run min      "$SEAT/variants/min.md"
run minfalse "$SEAT/variants/minfalse.md"
run wide     "$SEAT/variants/wide.md"
