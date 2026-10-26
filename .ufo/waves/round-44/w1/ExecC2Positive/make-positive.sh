#!/usr/bin/env bash
# Rebuild the round-44 C2 positive-control commit ("control P") from the files saved in ./positive,
# applied to a fresh shared clone of the lane at the v2 freeze revision.
#
# Usage: make-positive.sh [DEST]        DEST default /fast/scratch/hyaku/mado-r44/ExecC2Positive/rebuild
# Prints: fixture=<commit> tree=<tree> then the frozen counter's PRED-C2-r44 output (exit code = counter's).
set -euo pipefail
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
FREEZE=e2289516a9a857f55cda7be635933e89b931c3da
BASE=6a1a90528fe533cadee506a9fa3e9d13d15cc41f
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
DEST=${1:-/fast/scratch/hyaku/mado-r44/ExecC2Positive/rebuild}

rm -rf -- "$DEST"
git clone -q --shared --no-checkout "$LANE" "$DEST"
# run-6 fixture guard: every later git call names -C "$DEST", and DEST must be its own toplevel
top=$(git -C "$DEST" rev-parse --show-toplevel)
[ "$top" = "$(realpath -- "$DEST")" ] || { echo "refusing: toplevel $top != $DEST" >&2; exit 1; }
git -C "$DEST" checkout -q --detach "$FREEZE"

cp -r -- "$HERE/positive/corpus" "$DEST"/
git -C "$DEST" add -A
git -C "$DEST" -c user.name=ExecC2Positive -c user.email=exec-c2-positive@scratch.invalid \
    commit -q -m "round-44 w1: C2 positive control - gkeep size-request entry, S298-S301 rows, lesson gate, README row"

printf 'fixture=%s\ntree=%s\n' "$(git -C "$DEST" rev-parse HEAD)" "$(git -C "$DEST" rev-parse 'HEAD^{tree}')"
exec python3 -I "$LANE/quality/counters/c2-r44-gkeep-size-request.py" --repo "$DEST" --rev HEAD \
    --base "$BASE"
