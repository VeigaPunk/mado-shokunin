#!/bin/bash
# freeze-r97.sh -- copy the wave's final .v2 inputs to the frozen names the declaration's
# counting commands name, byte-exact, and print the sha256 of every copy (both sides).
# Read-only over the sources; writes only the frozen copies under the wave's controls/.
set -u
W=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-97
C=$W/controls
cp -p "$C/filetype-cases-v2.json"        "$C/filetype-cases-r97-frozen.json"
cp -p "$C/filetype-mutants-v2.json"      "$C/filetype-mutants-r97-frozen.json"
cp -p "$C/counter-selftest-panel-v2.json" "$C/counter-selftest-panel-r97.json"
for n in filetype-cases-v2.json filetype-mutants-v2.json counter-selftest-panel-v2.json; do
  echo "SRC $n $(sha256sum "$C/$n" | cut -d' ' -f1)"
done
for n in filetype-cases-r97-frozen.json filetype-mutants-r97-frozen.json counter-selftest-panel-r97.json; do
  echo "DST $n $(sha256sum "$C/$n" | cut -d' ' -f1)"
done
for n in filetype-fresh-r97.py filetype-host-r97.txt host-db-r97.json; do
  echo "INPUT $n $(sha256sum "$C/$n" | cut -d' ' -f1)"
done
