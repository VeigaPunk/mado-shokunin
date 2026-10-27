#!/usr/bin/env bash
# Falsify05 reproduction — round 52, mado. Source-only: no network, no package query,
# no host read, no git/jj mutation. Reads the lane's existing round-51 pin bytes and
# writes only under $HYAKU_SCRATCH (default /fast/scratch/hyaku) and this seat dir.
set -u
export PYTHONDONTWRITEBYTECODE=1
SEAT="$(cd "$(dirname "$0")" && pwd)"
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
SCRATCH_ROOT="${HYAKU_SCRATCH:-/fast/scratch/hyaku}"
W="$SCRATCH_ROOT/mado-r52/Falsify05-repro"
PINS="$LANE/.ufo/waves/round-51/fetch"

df -h "$SCRATCH_ROOT" | tail -1
rm -rf "$W"; mkdir -p "$W"
cp -a "$SEAT/fixture/base" "$SEAT/fixture/final" "$SEAT/fixture/draft" "$W/"

# pins: real Hyprland bytes at efb50993, already local in the lane fetch dir (read-only use)
mkdir -p "$W/final/pins" "$W/base/pins" "$W/draft/pins"
cp "$PINS/Hyprland-HyprCtl.cpp" "$PINS/Hyprland-ConfigActions.cpp" \
   "$PINS/Hyprland-KeybindManager.cpp" "$PINS/Hyprland-SharedDefs.hpp" "$W/final/pins/"
cp "$PINS/Hyprland-legacy-DispatcherTranslator.cpp" "$PINS/Hyprland-ConfigActions.cpp" \
   "$PINS/Hyprland-ConfigActions.hpp" "$PINS/Hyprland-KeybindManager.cpp" \
   "$PINS/Hyprland-KeybindManager.hpp" "$W/draft/pins/"

# derived fixtures: whole-file span variant, and a wrong-revision variant
cp -a "$W/final" "$W/final-widespan"
sed -i 's|`Hyprland-ConfigActions.cpp:1664-1682`|`Hyprland-ConfigActions.cpp:1-1772`|' \
  "$W/final-widespan/corpus/knowledge/f5-quote-hole.md"
cp -a "$W/final" "$W/final-revmut"
sed -i 's/@ efb50993780079460b0cbed1363e2166a2de1d9f/@ 0000000000000000000000000000000000000000/g' \
  "$W/final-revmut/corpus/SOURCES.md"

{
  echo '# Falsify05 receipts — round 52, seat Falsify05'
  echo '# date: 2026-10-27'
  echo '# harness: c2ref.py, seat-local reference implementation of the frozen C2 counter clauses'
  echo '# draft analysed: .ufo/waves/round-52/w1/C2EntryDraft/entry-draft.md'
  echo
  echo '### R0 pin and draft identity'
  sha256sum "$W"/final/pins/* "$W"/draft/pins/*
  sha256sum "$SEAT/fixture/draft/corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md" \
            "$SEAT/fixture/draft/proposition-map.tsv"
  echo
  echo '### R1 frozen control: target entry absent at base (fixture A slug)'
  python3 "$SEAT/c2ref.py" --root "$W/base" --base "$W/base" \
    --entry corpus/knowledge/f5-prose-hole.md --format text; echo "exit=$?"
  echo
  echo '### R2 fixture A: four mapped propositions + one material proposition only in prose'
  python3 "$SEAT/c2ref.py" --root "$W/final" --base "$W/base" \
    --entry corpus/knowledge/f5-prose-hole.md --dump-sentences --format text; echo "exit=$?"
  echo
  echo '### R3 fixture B: four mapped propositions, row 4 bound to a verbatim in-span non-entailing quote'
  python3 "$SEAT/c2ref.py" --root "$W/final" --base "$W/base" \
    --entry corpus/knowledge/f5-quote-hole.md --format text; echo "exit=$?"
  echo
  echo '### R4 fixture B with a whole-file (1-1772) pin span'
  python3 "$SEAT/c2ref.py" --root "$W/final-widespan" --base "$W/base" \
    --entry corpus/knowledge/f5-quote-hole.md --format text; echo "exit=$?"
  echo
  echo '### R5 revision element: registry anchors rewritten to 000...0, quote bytes unchanged'
  python3 "$SEAT/c2ref.py" --root "$W/final-revmut" --base "$W/base" \
    --entry corpus/knowledge/f5-prose-hole.md --format text; echo "exit=$?"
  echo
  echo '### R6 actual round-52 draft map, strict pin scope (shorthand `:N-M` cells cannot bind)'
  python3 "$SEAT/c2ref.py" --root "$W/draft" --base "$W/base" \
    --entry corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md \
    --pin-scope strict --format text; echo "exit=$?"
  echo
  echo '### R7 actual round-52 draft map, anchor pin scope, quote must sit in the cited span'
  python3 "$SEAT/c2ref.py" --root "$W/draft" --base "$W/base" \
    --entry corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md \
    --pin-scope anchor --format text; echo "exit=$?"
  echo
  echo '### R8 actual round-52 draft map, anchor pin scope, quote anywhere in the pin file'
  python3 "$SEAT/c2ref.py" --root "$W/draft" --base "$W/base" \
    --entry corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md \
    --pin-scope anchor --quote-scope file --format text; echo "exit=$?"
  echo
  echo '### R9 P07 cell split: the `|=` operator inside a markdown table quote'
  python3 - "$SEAT" <<'PY'
import sys
sys.path.insert(0, sys.argv[1])
import c2ref
p = sys.argv[1] + '/fixture/draft/corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md'
for i, l in enumerate(c2ref.read_lines(p), 1):
    if l.startswith('| P07 |'):
        print('line', i)
        for j, c in enumerate(c2ref.cells_of(l.strip())):
            print('  cell[%d]=%r' % (j, c))
PY
  echo
  echo '### R10 failed control: lexical conjunct-overlap proxy (over-flags paraphrase)'
  python3 "$SEAT/clause_coverage.py" \
    "$W/draft/corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md" "$W/draft" | tail -3
} > "$W/receipts.txt" 2>&1

cp "$W/receipts.txt" "$SEAT/receipts/receipts.txt"
echo "receipts: $SEAT/receipts/receipts.txt"
grep -E '^###|^admitted=|^exit=' "$SEAT/receipts/receipts.txt"
echo "scratch kept at $W (remove after reading)"
