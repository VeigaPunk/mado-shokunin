#!/bin/bash
# ExecCaptureStable: three read-only native captures, one minute apart.
# Only compositor verb: hyprctl getoption -j KEY (read-only). No writes outside seat dir.
set -u
S="$(dirname "$0")"
KEYS="$S/keys.txt"
cd "$S" || exit 1
: > timings.txt
for i in 1 2 3; do
  ts_start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  t0=$(date +%s.%N)
  : > "cap$i.raw"
  while IFS= read -r k; do
    [ -z "$k" ] && continue
    out=$(hyprctl getoption -j "$k" 2>&1)
    rc=$?
    printf '%s\t%s\t%s\n' "$k" "$rc" "$(printf '%s' "$out" | tr '\n' ' ')" >> "cap$i.raw"
  done < "$KEYS"
  t1=$(date +%s.%N)
  ts_end=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  printf 'cap%s start=%s end=%s dur=%.2fs lines=%s\n' "$i" "$ts_start" "$ts_end" \
    "$(echo "$t1 - $t0" | bc)" "$(wc -l < "cap$i.raw")" >> timings.txt
  if [ "$i" -lt 3 ]; then sleep 60; fi
done
echo DONE
