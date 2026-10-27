#!/bin/sh
# C1CounterDesign receipt generator — every command and its exact output.
#
#   sh receipts.sh [work_dir]
#
# work_dir defaults to the scratch tree this seat used; it must be outside /tmp,
# /var/tmp and /dev/shm (the counter refuses those roots).
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
SEAT=$LANE/.ufo/waves/round-52/w1/C1CounterDesign
C=$SEAT/c1-r52-ledger.py
REV=85d57a818c3707397e21c840b6498b105ba798aa
W=${1:-/fast/scratch/hyaku/mado-r52/C1CounterDesign/work}
SIMPLE=$LANE/.ufo/waves/round-52/w1/C1Simplify
mkdir -p "$W"

run() { echo "\$ $*"; "$@" 2>&1; echo "exit=$?"; echo; }

echo "# C1CounterDesign receipts — 2026-10-27"
echo "# lane=$LANE"
echo "# rev=$REV (git rev-parse HEAD)"
echo "# counter=$C"
echo "# scratch=$W"

echo "## SELFTEST"
run python3 -I $C --selftest --work $W

echo "## GREEN — production ledger at the frozen base"
run python3 -I $C --repo $LANE --rev $REV --work $W

echo "## RED — frozen do-nothing control (committed in place of the ledger)"
run python3 -I $C --repo $LANE --rev $REV --work $W --ledger $LANE/.ufo/waves/round-52/controls/c1-do-nothing.md

echo "## CONTROLS — population-complete (C1Simplify controls, read-only)"
for f in control-B-row-selfpointer.md control-C-ledger-selfpointer.md control-D-generic-desc.md control-E-one-selfpointer.md control-F3-forged.md control-G-legit-ledger-reader.md control-H-minimal-forgery.md mut-dup.md mut-emptydesc.md mut-badpointer.md; do
  echo "\$ python3 -I c1-r52-ledger.py --repo \$LANE --rev \$REV --work \$W --ledger \$SIMPLE/$f"
  out=$(python3 -I $C --repo $LANE --rev $REV --work $W --ledger $SIMPLE/$f 2>&1)
  rc=$?
  echo "$out" | grep -E "^(detail: (self_pointer|generic_desc|bad_pointer|note)|C1_R52:)" | head -4
  echo "$out" | tail -1
  echo "exit=$rc"
  echo
done

echo "## SETUP ERRORS"
run python3 -I $C --repo /nonexistent --rev $REV --work $W
run python3 -I $C --repo $LANE --rev deadbeefdeadbeefdeadbeefdeadbeefdeadbeef --work $W
run python3 -I $C --repo $LANE --rev $REV --work /tmp/refused
run python3 -I $C --repo $LANE --rev $REV

echo "## LANE UNCHANGED"
cd $LANE && git status --porcelain | head -5
echo "(the round-52 wave directory is the only untracked path; the seat dir is inside it)"

echo "## GATE OWNERSHIP"
echo "quality/check-tool-ledger.py (the round-51 gate) owns: population, ledger_rows,"
echo "  uncovered, dangling, bad_pointer, empty_desc -- it prints a LEDGER: line and says"
echo "  nothing about self_pointer or generic_desc, so it cannot corroborate this counter."
echo "This counter (c1-r52-ledger.py) owns: population, ledger_rows, uncovered, dup,"
echo "  dangling, bad_pointer, self_pointer, generic_desc -- it does not consult the"
echo "  round-51 gate at all, so the two gates are independent and neither's verdict"
echo "  constrains the other's. The integrator decides whether the round-51 gate gains"
echo "  self_pointer/generic_desc fields (to allow a cross-check clause) or whether this"
echo "  counter stands alone without one."
