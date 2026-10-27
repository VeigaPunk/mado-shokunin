#!/bin/sh
# batch.sh PLANFILE [PAR] : run each "CELL COUNTER REV" line
set -u
S=/fast/scratch/hyaku/mado-r48/MutC1Counter
PLAN=$1; PAR=${2:-10}
ulimit -f 3072
xargs -a "$PLAN" -L 1 -P "$PAR" sh -c '"$0/run1.sh" "$1" "$2" "$3"' "$S"
