#!/usr/bin/env bash
# Differential C2 runs on paths the 13 controls never reach (live replay, timeout); byte-compare
# counter verdict lines AND the exact argv + input-file digests the tool receives per case.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
W=$LANE/.ufo/waves/round-37/w1/scratch/SimplifyCounters
BASE=b4e47e980bfb0cbc8a4e788f59a41db858751fd8
ROOT=/dev/shm/mado37-SimplifyCounters
SB=$ROOT/c2sb
PROBE=$ROOT/probe
REC=.ufo/waves/round-37/receipts
for k in $(env | sed -n 's/^\(GIT_[^=]*\)=.*/\1/p'); do unset "$k"; done
export GIT_AUTHOR_NAME=sandbox GIT_AUTHOR_EMAIL=sandbox@invalid GIT_COMMITTER_NAME=sandbox GIT_COMMITTER_EMAIL=sandbox@invalid
rm -rf "$SB" "$PROBE"; mkdir -p "$PROBE"
git clone -q --no-local --no-checkout "$LANE" "$SB"
g() { git -C "$SB" "$@"; }
g sparse-checkout set --no-cone /tools/ /.ufo/waves/round-37/
g checkout -q --detach "$BASE"
commit() { g add -A && g commit -q --allow-empty -m "$1" && g rev-parse HEAD; }
mkdir -p "$SB/tools" "$SB/$REC"
cat > "$SB/tools/mado-eventq.py" <<EOF
import hashlib, os, sys
d = os.path.join("$PROBE", open("$PROBE/TAG").read().strip())
os.makedirs(d, exist_ok=True)
rec = [os.path.basename(x) + ":" + hashlib.sha256(open(x, "rb").read()).hexdigest() if os.path.isfile(x) else x
       for x in sys.argv[1:]]
with open(os.path.join(d, os.path.basename(os.getcwd()) + ".txt"), "w") as f:
    f.write(" ".join(rec) + "\n")
print("MADO_EVENTQ_CLIENT: comm=waybar pid=935660 fd=21 peer_recv_q=0 server_send_q=0")
print("MADO_EVENTQ_CLIENT: comm=socat pid=2293 fd=5 peer_recv_q=0 server_send_q=0")
print("MADO_EVENTQ: socket2=/x subscribers=2 overflow=0 write_fail=0 lagging=0 missing_client=- markers_observable=no verdict=CLEAN")
sys.exit(0)
EOF
sha=$(sha256sum "$SB/tools/mado-eventq.py" | cut -d' ' -f1)
printf 'u_str LISTEN 0 10 /x 1 * 0 users:(("Hyprland",pid=1,fd=3))\n' > "$SB/$REC/eventq-live-ss.txt"
live() { printf 'tool_sha256=%s\nMADO_EVENTQ_CLIENT: comm=waybar pid=935660 fd=21\nMADO_EVENTQ_CLIENT: comm=socat pid=%s fd=5\nMADO_EVENTQ: socket2=/x subscribers=2 verdict=CLEAN\n' "$sha" "$1" > "$SB/$REC/eventq-live.txt"; }
live 2293; L1=$(commit live-match)
live 9999; L0=$(commit live-mismatch)
g rm -q "$REC/eventq-live-ss.txt"; NS=$(commit no-snapshot)
printf 'import time\ntime.sleep(25)\n' > "$SB/tools/mado-eventq.py"; T=$(commit timeout)
echo "L1=$L1 L0=$L0 NS=$NS T=$T"

score() { python3 -I "$1" --repo "$SB" --rev "$2" 2>&1; echo "rc=$?"; }
for v in orig P3 ALL; do
  c=$W/$v/c2-r37-eventq.py; o=$W/out/c2diff-$v.txt; : > "$o"
  for r in L1 L0 NS; do
    echo "$v-$r" > "$PROBE/TAG"
    echo "## $r" >> "$o"; score "$c" "${!r}" >> "$o"
  done
done
# timeout path: run the three versions in parallel (each ~11 x 20 s)
for v in orig P3 ALL; do ( { echo "## T"; score "$W/$v/c2-r37-eventq.py" "$T"; } > "$W/out/c2diff-T-$v.txt" ) & done
wait
for v in orig P3 ALL; do cat "$W/out/c2diff-T-$v.txt" >> "$W/out/c2diff-$v.txt"; done
for v in P3 ALL; do
  if cmp -s "$W/out/c2diff-orig.txt" "$W/out/c2diff-$v.txt"; then echo "c2diff verdicts $v == orig"; else echo "c2diff verdicts $v DIFFERS:"; diff "$W/out/c2diff-orig.txt" "$W/out/c2diff-$v.txt"; fi
  for r in L1 L0 NS; do
    if diff -r "$PROBE/orig-$r" "$PROBE/$v-$r" > /dev/null; then echo "probe $v-$r argv+input digests == orig ($(ls "$PROBE/orig-$r" | wc -l) runs)"; else echo "probe $v-$r DIFFERS"; diff -r "$PROBE/orig-$r" "$PROBE/$v-$r"; fi
  done
done
cp -r "$PROBE" "$W/out/probe"
rm -rf "$SB" "$PROBE"
