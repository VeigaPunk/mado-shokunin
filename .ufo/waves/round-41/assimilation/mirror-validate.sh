#!/usr/bin/env bash
# Scratch mirror of the lane's corpus/ with the append block and the entry in place,
# then the census validator on the mirror (assimilation item 10: gate BEFORE the first
# registry append). Usage:
#   mirror-validate.sh <rows-block.txt> <entry.md> [<used-by-edits.tsv>]
# rows-block.txt: registry table rows only (appended at the end of the ## Registry table).
# used-by-edits.tsv: `S### <TAB> <new used-by cell>` replaces cell 11 of an EXISTING row.
set -euo pipefail
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
A=$LANE/.ufo/waves/round-41/assimilation
V=$A/validate
rows=$1
entry=$2
edits=${3:-}
rm -rf "$V"
mkdir -p "$V"
cp -r "$LANE/corpus" "$V/corpus"
mkdir -p "$V/corpus/knowledge"
cp "$entry" "$V/corpus/knowledge/hyprland-focus-grab-r41.md"
python3 - "$V/corpus/SOURCES.md" "$rows" "$edits" <<'PY'
import re, sys
path, rows, edits = sys.argv[1], sys.argv[2], sys.argv[3]
lines = open(path).read().split("\n")
new = [l for l in open(rows).read().split("\n") if l.strip()]
# last registry row index
last = max(i for i, l in enumerate(lines) if re.match(r"^ {0,3}\|\s*S\d{3,}\s*\|", l))
if edits:
    ed = dict(l.split("\t", 1) for l in open(edits).read().split("\n") if l.strip())
    for i, l in enumerate(lines):
        m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", l)
        if m and m.group(1) in ed:
            cells = l.split("|")
            cells[11] = " " + ed[m.group(1)] + " "
            lines[i] = "|".join(cells)
lines[last + 1:last + 1] = new
open(path, "w").write("\n".join(lines))
PY
rc=0; /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$V/corpus/SOURCES.md" || rc=$?
echo "mirror-validate exit=$rc"
