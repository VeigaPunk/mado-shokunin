#!/usr/bin/env bash
# Sequential base/tip runs, one child at a time, each driver under prlimit.
# Usage: run-matrix.sh RECEIPT_DIR FIXTURE...
set -u
O=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/w2/out/AttackPerf
R=$1; shift
mkdir -p "$R"
for fx in "$@"; do
  name=$(basename "$fx" .jsonl)
  for mode in module-main cli; do
    for tool in base tip; do
      prlimit --as=402653184 --cpu=15 python3 -I -B "$O/drive.py" "$O/tool-$tool.py" "$fx" "$mode" "$tool" \
        > "$R/$name.$mode.$tool.json" 2> "$R/$name.$mode.$tool.driver-stderr"
      echo "driver_exit=$? $name $mode $tool"
    done
  done
done
