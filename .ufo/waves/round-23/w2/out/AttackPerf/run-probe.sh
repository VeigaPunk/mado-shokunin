#!/usr/bin/env bash
# Probe-only runs of probe-tip-corrected.py (not a lane candidate), one child at a time.
# Usage: run-probe.sh RECEIPT_DIR FIXTURE...
set -u
O=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/out/AttackPerf
R=$1; shift
mkdir -p "$R"
for fx in "$@"; do
  name=$(basename "$fx" .jsonl)
  for mode in module-main cli; do
    prlimit --as=402653184 --cpu=15 python3 -I -B "$O/drive.py" "$O/probe-tip-corrected.py" "$fx" "$mode" probe \
      > "$R/$name.$mode.probe.json" 2> "$R/$name.$mode.probe.driver-stderr"
    echo "driver_exit=$? $name $mode probe"
  done
done
