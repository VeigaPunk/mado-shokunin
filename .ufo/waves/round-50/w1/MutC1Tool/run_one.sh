#!/bin/bash
# MutC1Tool driver: score ONE mutant (or the pristine BASE) with the frozen PRED-C1-r49
# counter on a fresh --shared scratch clone whose fixture commit replaces
# tools/mado-keysym.py. Unwrapped counter (no outer tracer - see SentHostState R-SHS-3);
# HOME/XDG_* and TMPDIR under scratch; fixed nonce 20261027; restoration evidence printed.
ulimit -f 65536
set -u
S=/fast/scratch/hyaku/mado-r50/MutC1Tool
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-50/w1/MutC1Tool
CTR=/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r49-keysym.py
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
ID="${1:?usage: run_one.sh BASE|MNN}"
REC="$SEAT/receipts"
mkdir -p "$REC"
mkdir -p "$S/home" "$S/tmp" "$S/work"
export HOME="$S/home" XDG_CACHE_HOME="$S/home/.cache" XDG_CONFIG_HOME="$S/home/.config"
export XDG_DATA_HOME="$S/home/.data" XDG_STATE_HOME="$S/home/.state" TMPDIR="$S/tmp"

if [ "$ID" = BASE ]; then
  D=$S/clone-base
  REV=$(git -C "$D" rev-parse HEAD)
else
  D=$S/clone-$ID
  rm -rf "$D"
  git clone -q --shared "$LANE" "$D" || { echo "CLONE-FAIL $ID"; exit 9; }
  T=$(git -C "$D" rev-parse --show-toplevel)
  [ "$T" = "$D" ] || { echo "TOPLEVEL-MISMATCH $ID"; exit 9; }
  git -C "$D" checkout -q -b "mut-$ID"
  cp "$SEAT/mutants/$ID.py" "$D/tools/mado-keysym.py"
  git -C "$D" -c user.name=mutc1tool -c user.email=mut@scratch.local -c commit.gpgsign=false commit -q -m "mutant $ID" -- tools/mado-keysym.py
  REV=$(git -C "$D" rev-parse HEAD)
fi
MSHA=$(sha256sum "$D/tools/mado-keysym.py" | cut -d' ' -f1)

env -i PATH=/usr/bin:/bin HOME=$S/home XDG_CACHE_HOME=$S/home/.cache XDG_CONFIG_HOME=$S/home/.config \
  XDG_DATA_HOME=$S/home/.data XDG_STATE_HOME=$S/home/.state TMPDIR=$S/tmp \
  python3 "$CTR" --repo "$D" --rev "$REV" --work "$S/work" --nonce 20261027 > "$REC/$ID.txt" 2>&1
RC=$?

if [ "$ID" = BASE ]; then
  echo "BASE REV=$REV rc=$RC tool_sha=$MSHA"
else
  PB=$(git -C "$D" rev-parse "$REV^")
  PBSHA=$(git -C "$D" show "$PB:tools/mado-keysym.py" | sha256sum | cut -d' ' -f1)
  git -C "$D" checkout -q "$PB" -- tools/mado-keysym.py
  RSHA=$(sha256sum "$D/tools/mado-keysym.py" | cut -d' ' -f1)
  PRISTINE=dcc13cce3b7134946208116cd98599fb8f56a2b81fc6f26b9598ac5429b40265
  if [ "$RSHA" = "$PRISTINE" ] && [ "$PBSHA" = "$PRISTINE" ]; then ROK=restored-equal; else ROK=RESTORE-DRIFT; fi
  echo "MUT=$ID REV=$REV rc=$RC mutant_sha=$MSHA parent=$PB parent_blob_sha=$PBSHA restored_sha=$RSHA $ROK"
fi
grep -E "clause=s |clause=f fixtures|clause=g generated|clause=r |verdict=|SETUP" "$REC/$ID.txt" | tail -8
