#!/usr/bin/env bash
# Decisive, self-contained probe of the dead digest clause (M35-2), no junk tree needed.
# C1 reads root/corpus/SOURCES.md, the three entries and the eight fetch receipts; it does
# not read git. So a minimal root proves the clause.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
D=$LANE/.ufo/waves/round-35/scratch/CritAxisClaims/digest
C1=$LANE/.ufo/waves/round-35/c1/count.py
F=$LANE/.ufo/waves/round-35/c1/frozen.json

rm -rf "$D"; mkdir -p "$D/corpus/knowledge" "$D/.ufo/waves/round-35/fetch"
cp "$LANE/corpus/SOURCES.md" "$D/corpus/SOURCES.md"
for n in idle-lock-never-asked-r12.md idle-lock-chain-armed-r14.md idle-lock-offered-in-the-bar-r15.md; do
  cp "$LANE/corpus/knowledge/$n" "$D/corpus/knowledge/$n"
done
cp "$LANE"/.ufo/waves/round-35/fetch/S2*.receipt.txt "$D/.ufo/waves/round-35/fetch/"

run() { python3 -I "$C1" --root "$D" --frozen "$F"; echo "  exit=$?"; }

echo "== D0 minimal root, real receipts =="
run

echo "== D1 one receipt mutated (one byte appended) — clause named 'anchor cell carries the sha256 of the named receipt' =="
cp "$D/.ufo/waves/round-35/fetch/S203.receipt.txt" "$D/S203.bak"
printf 'x' >> "$D/.ufo/waves/round-35/fetch/S203.receipt.txt"
run
cp "$D/S203.bak" "$D/.ufo/waves/round-35/fetch/S203.receipt.txt"

echo "== D2 S203 receipt replaced by a different file with the same name =="
: > "$D/.ufo/waves/round-35/fetch/S203.receipt.txt"
run

echo "== D4 S203 receipt fabricated: different bytes, the gate-quote still present =="
printf 'FABRICATED RECEIPT, this is not the measured bytes\nlocated: install/first-run/ lists 12 scripts; the omarchy-first-run body runs all 12; none is idle-lock\n' \
  > "$D/.ufo/waves/round-35/fetch/S203.receipt.txt"
run
echo "  sha256 of the fabricated receipt vs the frozen digest:"
sha256sum "$D/.ufo/waves/round-35/fetch/S203.receipt.txt"

echo "== D3 control bite: S203 row's anchor digest zeroed (this is what controls/c1-digest kills) =="
cp "$D/S203.bak" "$D/.ufo/waves/round-35/fetch/S203.receipt.txt"
python3 - "$D/corpus/SOURCES.md" <<'PY'
import sys
p = sys.argv[1]
t = open(p).read()
t = t.replace("1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646", "0" * 64)
open(p, "w").write(t)
PY
run

rm -rf "$D"
