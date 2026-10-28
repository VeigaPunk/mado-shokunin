#!/bin/sh
# usage: runone.sh <harness.py> <label>; runs the harness against the real counter and four stubs.
S=/fast/scratch/hyaku/mado-r55/R55W2MutC1Harness
H="$1"
L="$2"
D=$S/repo
OUT=$S/results
mkdir -p "$OUT" "$S/work"
for c in real green red_min red_shot silent; do
  W=$(mktemp -d -p "$S/work")
  X=""
  case $c in
    green) X="--counter $S/stubs/always_green.py" ;;
    red_min) X="--counter $S/stubs/always_red_minimal.py" ;;
    red_shot) X="--counter $S/stubs/always_red_shotgun.py" ;;
    silent) X="--counter $S/stubs/silent.py" ;;
  esac
  python3 -I "$H" --repo "$D" --rev HEAD --work "$W" $X > "$OUT/$L.$c.out" 2> "$OUT/$L.$c.err"
  echo "rc=$?" >> "$OUT/$L.$c.out"
  rm -rf "$W"
done
echo done "$L"
