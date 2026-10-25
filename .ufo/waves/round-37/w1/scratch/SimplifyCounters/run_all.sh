#!/usr/bin/env bash
# Score each variant's controls with its own counters; accept a run only when no sandbox git step failed.
W=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/w1/scratch/SimplifyCounters
R=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/receipts/controls-v2.txt
cd "$W" || exit 2
norm() { sed -E 's/rev=[0-9a-f]{40}/rev=REV/g' "$1"; }
for v in "$@"; do
  for try in 1 2 3; do
    python3 run_controls.py "$v/controls.py" "$v/c1-r37-event-ground.py" "$v/c2-r37-eventq.py" \
      "out/$v.txt" > /dev/null 2> "out/$v.err"
    rc=$?
    fails=$(grep -c '^SH_FAIL' "out/$v.err")
    [ "$fails" -eq 0 ] && break
  done
  if diff <(norm "out/$v.txt") <(norm "$R") > "out/$v.diff"; then same=IDENTICAL; else same=DIFFERS; fi
  echo "variant=$v try=$try rc=$rc sh_fail=$fails $(tail -1 "out/$v.txt") receipt=$same"
done
