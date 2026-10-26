#!/usr/bin/env bash
# mirror.sh <workdir> — census proof for the round-47 S290-S297 supersession block.
# Copies the lane tree once (no .git/.jj), then applies one variant at a time to the shared
# copy's corpus/SOURCES.md (restoring the pristine file between variants) and runs the fleet
# census with --file. Every variant writes census-<name>.txt and one summary line on stdout.
# Nothing here writes into the lane.
set -u
W=${1:?usage: mirror.sh <workdir>}
L=/home/vgpnk/Projects/shokunin/mado-shokunin
SEAT=$L/.ufo/waves/round-47/w1/ExecSupersede
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
TREE=$W/tree
SRC=$TREE/corpus/SOURCES.md

mkdir -p "$W"
rsync -a --exclude .git --exclude .jj --exclude .ruff_cache "$L/" "$TREE/"
[ -f "$W/pristine-SOURCES.md" ] || cp "$SRC" "$W/pristine-SOURCES.md"

rows() { grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$SRC"; }

apply_block() { # append rows-block.txt inside ## Registry, before ## Paths
  awk -v block="$SEAT/rows-block.txt" '
    /^## Paths/ && !done { while ((getline line < block) > 0) print line; done=1 }
    { print }
  ' "$W/pristine-SOURCES.md" > "$SRC"
}

run() { # run <name>  (expects $SRC already in the variant state)
  local name=$1
  local out=$W/census-$name.txt
  local rc
  bash "$CENSUS" validate --today 2026-10-26 --file "$SRC" > "$out" 2>&1
  rc=$?
  local e w
  e=$(grep -c $'\tE[0-9][0-9]\t' "$out" || true)
  w=$(grep -c $'\tW[0-9][0-9]\t' "$out" || true)
  printf '%-6s exit=%s rows=%s E=%s W=%s  %s\n' "$name" "$rc" "$(rows)" "$e" "$w" "$(tail -1 "$out")"
  cp "$out" "$SEAT/" 2>/dev/null || true
}

# m0 — baseline: the lane registry untouched
cp "$W/pristine-SOURCES.md" "$SRC"; run m0

# m1 — the eight rows (recommended landing)
apply_block; run m1

# m2 — rows, used-by pointing at a path that does not exist (E11 control)
apply_block
python3 - "$SRC" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
t = t.replace(".ufo/waves/round-47/w1/ExecSupersede/rows.md", "corpus/lessons/round-47.md")
open(p, "w", encoding="utf-8").write(t)
PY
run m2

# m3 — rows with the `supersedes S3NN —` opener stripped (E04 control)
apply_block
python3 - "$SRC" <<'PY'
import re, sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
t = re.sub(r"supersedes S[0-9]{3} — ", "", t)
open(p, "w", encoding="utf-8").write(t)
PY
run m3

# m4 — the block renumbered onto an id the registry already holds (E03 control)
apply_block
python3 - "$SRC" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
t = t.replace("| S346 |", "| S325 |")
open(p, "w", encoding="utf-8").write(t)
PY
run m4

# m5 — prose errata appended outside ## Registry, no new row (control: no cell changes)
cp "$W/pristine-SOURCES.md" "$SRC"
printf '\n## Errata (round 47, R4a control)\n\nS290-S297 are superseded: see .ufo/waves/round-47/w1/ExecSupersede/rows.md.\n' >> "$SRC"
run m5
cp "$W/pristine-SOURCES.md" "$SRC"
