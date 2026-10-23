#!/usr/bin/env bash
# Green fixture for round-24 defect M23-5: the r23 L1 attack run, corrected.
# Measured tool: tools/mado-tripwire.py sha256:cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84
# Every result and data path below is absolute; result files are deleted before each run.
set -euo pipefail
L=/home/vgpnk/Projects/shokunin/mado-shokunin
D=/fast/scratch/hyaku/mado-r24/ExecCheckM235/green/L1-green
R=/fast/scratch/hyaku/mado-r24/ExecCheckM235/green/results
F=/fast/scratch/hyaku/mado-r24/ExecCheckM235/green/fixtures
PIN=cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84
rm -rf "$D"; git clone -q "$L" "$D"
T="$D/tools/mado-tripwire.py"
B="$D/.ufo/waves/round-23/evidence/tool-base-cd9da20c.py"
[ "$(sha256sum "$T" | cut -d' ' -f1)" = "$PIN" ] || { echo "measured tool sha256 mismatch: $T"; exit 3; }
mkdir -p "$R" "$F/probes" "$F/probes2"
rm -f "$R/afs-p1.json" "$R/afs-p2.json" "$R/afs-fx.json" "$R/rr-cases1.json" "$R/rr-cases2.json" "$R/rr-cases-final.json"
python3 -I "$D/.ufo/waves/round-23/w2/out/AttackFrameScopes/discovery/mkprobes.py" "$F/probes"
python3 -I "$D/.ufo/waves/round-23/w2/out/AttackFrameScopes/discovery/probe.py" "$F/probes" "$R/afs-p1.json"
python3 -I "$D/.ufo/waves/round-23/w2/out/AttackFrameScopes/discovery/mkprobes2.py" "$F/probes2"
python3 -I "$D/.ufo/waves/round-23/w2/out/AttackFrameScopes/discovery/probe.py" "$F/probes2" "$R/afs-p2.json"
python3 -I "$D/.ufo/waves/round-23/w2/out/AttackFrameScopes/discovery/probe.py" "$D/.ufo/waves/round-23/w2/out/AttackFrameScopes/fixtures" "$R/afs-fx.json"
for c in cases1 cases2 cases-final; do
  python3 -I "$D/.ufo/waves/round-23/w2/out/AttackRecallRegress/probe.py" "$D/.ufo/waves/round-23/w2/out/AttackRecallRegress/$c.json" "$R/rr-$c" "$R/rr-$c.json" "$T"
  python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print(sys.argv[2],len(d.get("results") or d.get("cases") or []))' "$R/rr-$c.json" "$c"
done
python3 -I "$D/.ufo/waves/round-23/w2/out/AttackEscapeGate/run.py" "$B" "$T"
