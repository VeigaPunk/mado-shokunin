#!/bin/bash
# CritC1Narrow: install each surviving variant on its own scratch clone and score it with the FROZEN counter, 3 nonces.
set -u
SCR=/fast/scratch/hyaku/mado-r46/CritC1Narrow
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
REV=8c5434c60e03f147ee1f75ab195e8bc3f0db4dec
COUNTER=$LANE/quality/counters/c1-r46-devices.py
OUT=$SCR/real-counter.txt
: >> "$OUT"
mkdir -p "$SCR/w"
score_one() {
  name=$1
  D=$SCR/c-$name
  rm -rf "$D"
  git clone -q --shared --no-checkout "$LANE" "$D"
  test "$(git -C "$D" rev-parse --show-toplevel)" = "$D" || { echo "$name CLONE-BAD" >> "$OUT"; return; }
  git -C "$D" checkout -q --detach "$REV"
  cp "$SCR/work-$name/mado-devices.py" "$D/tools/mado-devices.py"
  git -C "$D" add tools/mado-devices.py
  git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m "variant $name"
  for n in 4646 12345 987654; do
    line=$(python3 -I "$COUNTER" --repo "$D" --rev HEAD --work "$SCR/w" --nonce "$n" 2>&1 | tail -1)
    echo "$name nonce=$n $line" >> "$OUT"
  done
}
export -f score_one 2>/dev/null || true
for v in "$@"; do
  score_one "$v"
done
echo DONE >> "$OUT"
