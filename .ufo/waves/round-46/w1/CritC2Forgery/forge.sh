#!/bin/sh
# Reproduce every CritC2Forgery round-46 PRED-C2-r46 forgery from lane content.
#   sh forge.sh            -> build the positive control, apply each patch, score it
# Needs: the lane at the freeze commit, build-pos.py, the frozen counter, git, python3.
set -e
LANE=${LANE:-/home/vgpnk/Projects/shokunin/mado-shokunin}
SEAT=$LANE/.ufo/waves/round-46/w1/CritC2Forgery
CTR=$LANE/quality/counters/c2-r46-input-device-entry.py
FREEZE=8c5434c60e03f147ee1f75ab195e8bc3f0db4dec
BASE=b22ea56bff2faec39ce9ff75d2107eaf4612ecbe
W=${W:-/fast/scratch/hyaku/mado-r46/CritC2Forgery-repro}
rm -rf "$W"
mkdir -p "$W"
D=$W/repo
git clone -q --shared --no-checkout "$LANE" "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
git -C "$D" checkout -q --detach "$FREEZE"
python3 -I "$LANE/.ufo/waves/round-46/l1-draft/build-pos.py" "$D"
git -C "$D" add -A
git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m pos
P0=$(git -C "$D" rev-parse HEAD)
echo "pos rev=$P0"
python3 -I "$CTR" --repo "$D" --rev "$P0" --base "$BASE" | tail -1
: > "$W/revs"
for p in "$SEAT"/patches/F1.patch "$SEAT"/patches/F2.patch "$SEAT"/patches/F3.patch \
         "$SEAT"/patches/F4.patch "$SEAT"/patches/F5.patch "$SEAT"/patches/F5c.patch \
         "$SEAT"/patches/F5d.patch \
         "$SEAT"/patches/F6.patch "$SEAT"/patches/F7.patch "$SEAT"/patches/F8.patch \
         "$SEAT"/patches/F9.patch "$SEAT"/patches/F10.patch; do
  n=$(basename "$p" .patch)
  git -C "$D" checkout -q -f "$P0" -- .
  git -C "$D" apply "$p"
  git -C "$D" add -A
  git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m "$n"
  r=$(git -C "$D" rev-parse HEAD)
  printf '%s\t%s\t%s\t' "$n" "$(sha256sum "$p" | cut -c1-16)" "$(git -C "$D" rev-parse --short=12 HEAD)"
  python3 -I "$CTR" --repo "$D" --rev "$r" --base "$BASE" | tail -1
  echo "$r" >> "$W/revs"
done
echo "--- tightening candidates (A..G) on pos and every forgery"
python3 -I "$SEAT/tighten.py" "$D" "$P0" $(cat "$W/revs")
