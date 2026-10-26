#!/bin/bash
# Score mutant bodies with the frozen PRED-C1-r44 counter, in bounded parallel batches.
# usage: run_sweep.sh NAME [NAME ...]   (NAME without .py, or REF for the reference anchor)
S=/fast/scratch/hyaku/mado-r44/ExecC1ExtraMutants
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
SEAT=$LANE/.ufo/waves/round-44/w1/ExecC1ExtraMutants
REV=e2289516a9a857f55cda7be635933e89b931c3da
NONCE=${NONCE:-mutsweep1}
LOGDIR=${LOGDIR:-$S/logs}
mkdir -p "$LOGDIR"
cd "$LANE" || exit 1
run_one() {
  name=$1
  tool="$SEAT/mutants/$name.py"
  [ "$name" = REF ] && tool="$LANE/.ufo/waves/round-44/c1/ctl-ref-tool.py.txt"
  mkdir -p "$S/work/$name"
  python3 -I quality/counters/c1-r44-geometry-states.py --repo . --rev "$REV" \
      --tool "$tool" --nonce "$NONCE" --work "$S/work/$name" > "$LOGDIR/$name.log" 2>&1
  rc=$?
  printf '%s\trc=%d\t%s\t%s\n' "$name" "$rc" \
      "$(grep -o 'clauses=.*' "$LOGDIR/$name.log" | tail -1)" \
      "$(tail -1 "$LOGDIR/$name.log" | cut -c1-200)" >> "$S/rc-$NONCE.txt"
}
for n in "$@"; do run_one "$n" & done
wait
