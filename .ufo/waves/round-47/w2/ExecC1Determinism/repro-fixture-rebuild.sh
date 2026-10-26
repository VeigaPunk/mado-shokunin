#!/bin/sh
# Repro 3 (round 47 w2, ExecC1Determinism): rebuilding the C1 fixtures on a different filesystem
# reproduces quality/counters/c1-r47-fixtures.json byte for byte -> no frozen fixture depends on
# readdir order (the builder varies only path depth, build-fixtures.py:68-70, so it would not have
# caught an order-dependent case either).
# usage: repro-fixture-rebuild.sh <work-dir-on-target-fs> <out-json>
set -eu
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
W=${1:?work dir}; OUT=${2:?out path}
mkdir -p "$W"
python3 -I "$LANE/.ufo/waves/round-47/ctl/build-fixtures.py" --work "$W" --out "$OUT"
echo "work fs: $(stat -f -c %T "$W")"
sha256sum "$LANE/quality/counters/c1-r47-fixtures.json" "$OUT"
if cmp -s "$LANE/quality/counters/c1-r47-fixtures.json" "$OUT"; then echo "BYTE_IDENTICAL"; else echo "DIFFERS"; exit 1; fi
