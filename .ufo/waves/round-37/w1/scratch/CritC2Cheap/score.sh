#!/usr/bin/env bash
# usage: score.sh <name> <tool.py> <snapshot-file> [counter]
# Builds a sandbox clone of LANE at 80b83c8, commits the tool, the snapshot and a receipt
# produced by running the tool itself on the snapshot (+ tool_sha256), then scores.
set -euo pipefail
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
W=/dev/shm/mado37-CritC2Cheap
name=$1 tool=$2 snap=$3 counter=${4:-$LANE/quality/counters/c2-r37-eventq.py}
sb=$W/sb-$name
rm -rf "$sb"
env -u GIT_DIR -u GIT_INDEX_FILE git clone -q --no-local --no-checkout "$LANE" "$sb"
cd "$sb"
git sparse-checkout set --no-cone /tools/ /.ufo/waves/round-37/receipts/
git checkout -q 80b83c8
git config user.name sandbox; git config user.email sandbox@invalid
mkdir -p tools .ufo/waves/round-37/receipts
cp "$tool" tools/mado-eventq.py
cp "$snap" .ufo/waves/round-37/receipts/eventq-live-ss.txt
R=.ufo/waves/round-37/receipts/eventq-live.txt
{ echo "tool_sha256=$(sha256sum tools/mado-eventq.py | cut -d' ' -f1)"
  python3 -I tools/mado-eventq.py --ss-file .ufo/waves/round-37/receipts/eventq-live-ss.txt \
    --log /dev/null --journal-file /dev/null --disable-logs 1 || true; } > "$R"
git add -A; git commit -q -m "crib $name"
t0=$(date +%s%N)
rc=0; python3 -I "$counter" --repo "$sb" --rev HEAD || rc=$?
echo "counter_exit=$rc counter_wall_ms=$(( ($(date +%s%N) - t0) / 1000000 ))"
