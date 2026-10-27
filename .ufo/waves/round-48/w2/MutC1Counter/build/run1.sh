#!/bin/sh
# run1.sh CELL COUNTER REV : one counter run, log under $S/out/CELL.log
set -u
# The frozen counter copies the judge own externals into its sandbox; /usr/bin/gawk is 1,274,872 B
# (1.216 MiB), so a 1 MiB RLIMIT_FSIZE aborts the judge itself. 3072 units = 1.5 MiB, the smallest
# limit that admits the judge copy; every file this seat writes by hand stays under 1 MiB.
ulimit -f 3072
S=/fast/scratch/hyaku/mado-r48/MutC1Counter
CELL=$1; COUNTER=$2; REV=$3
W=$(mktemp -d -p "$S/work")
t0=$(date +%s)
python3 -I "$COUNTER" --repo "$S/tree/lane" --rev "$REV" --work "$W" --nonce 4848 > "$S/out/$CELL.log" 2>&1
rc=$?
t1=$(date +%s)
rm -rf "$W"
{ echo "CELL $CELL rc=$rc seconds=$((t1-t0)) counter=$(sha256sum "$COUNTER" | cut -d' ' -f1) rev=$REV";
  grep -E '^PRED-C1-r48 (clause=.( |$)|: )' "$S/out/$CELL.log" | tail -30; } >> "$S/out/index.txt"
printf '%s rc=%s %ss\n' "$CELL" "$rc" "$((t1-t0))"
