#!/usr/bin/env bash
# apply-and-count.sh <workdir> — round-47 w2 / ExecRegistryMirror.
# Applies the round's registry changes (S290-S297 supersession draft + ScrRows new rows) to a
# scratch MIRROR of the lane corpus, then runs the fleet census and the prompt's id-collision
# guard on the mirror. Nothing here writes into the lane.
set -u
W=${1:?usage: apply-and-count.sh <workdir>}
L=/home/vgpnk/Projects/shokunin/mado-shokunin
SEAT=$L/.ufo/waves/round-47/w2/ExecRegistryMirror
SUP=$L/.ufo/waves/round-47/w1/ExecSupersede/rows-block.txt
NEW=$L/.ufo/waves/round-47/w1/ScrRows/rows.md
APPEND=/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
TREE=$W/tree
SRC=$TREE/corpus/SOURCES.md
ENTRY=$TREE/corpus/knowledge/xdg-terminal-selection-r47.md

mkdir -p "$W/mirror-src" "$W/gate"
[ -f "$W/pristine-SOURCES.md" ] || cp "$SRC" "$W/pristine-SOURCES.md"

# the 13 new rows, extracted from the draft table (data rows only, single line each)
grep -E '^[|] S3' "$NEW" > "$W/mirror-src/new-rows.txt"
# the 8 supersession rows
cat "$SUP" > "$W/mirror-src/sup-rows.txt"
wc -l "$W/mirror-src/new-rows.txt" "$W/mirror-src/sup-rows.txt" > "$W/mirror-src/row-counts.txt"

rows() { grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$SRC"; }

insert() { # insert <first-file> <second-file>  -> pristine + both blocks before ## Paths
  awk -v a="$1" -v b="$2" '
    /^## Paths/ && !done { while ((getline l < a) > 0) print l; while ((getline l < b) > 0) print l; done=1 }
    { print }
  ' "$W/pristine-SOURCES.md" > "$SRC"
}

standin() { # mirror-only stand-in so used-by resolves (the real entry is C2's deliverable)
  printf '# xdg-terminal-selection-r47 (mirror-only stand-in, not the C2 entry)\n\nused-by resolution target for the registry proof.\n' > "$ENTRY"
}

count() { # count <name>
  local name=$1
  local out=$W/gate/census-$name.txt
  local rc e w
  bash "$CENSUS" validate --today 2026-10-26 --file "$SRC" > "$out" 2>&1
  rc=$?
  e=$(grep -c $'\tE[0-9][0-9]\t' "$out" || true)
  w=$(grep -c $'\tW[0-9][0-9]\t' "$out" || true)
  printf '%-10s exit=%s rows=%s E=%s W=%s  %s\n' "$name" "$rc" "$(rows)" "$e" "$w" "$(tail -1 "$out")"
}

guard() { # guard <name> — the prompt's 0-3-space id collision check on the mirror
  local name=$1 d=$W/guard-$1; mkdir -p "$d"
  grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$SRC" | grep -oE 'S[0-9]+' | sort > "$d/reg-ids"
  grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$APPEND" | grep -oE 'S[0-9]+' | sort > "$d/staged-ids"
  comm -12 "$d/reg-ids" "$d/staged-ids" > "$d/collisions"
  printf '%-10s reg=%s staged=%s collisions=%s\n' "$name" "$(wc -l < "$d/reg-ids")" \
    "$(wc -l < "$d/staged-ids")" "$(wc -l < "$d/collisions")"
}

# g0 — baseline guard at the untouched mirror (registry S001..S325, 262 rows)
cp "$W/pristine-SOURCES.md" "$SRC"; guard g0

# a0 — round rows applied, NO entry stand-in (E11 dependency on the C2 deliverable)
rm -f "$ENTRY"; insert "$W/mirror-src/new-rows.txt" "$W/mirror-src/sup-rows.txt"; count a0

# a1 — same tree WITH the stand-in (the real target configuration)
standin; count a1

# append-only proof: only additions between pristine and a1
diff "$W/pristine-SOURCES.md" "$SRC" > "$W/gate/append-only.diff" 2>&1
printf 'append-only  removed_lines=%s added_lines=%s\n' \
  "$(grep -c '^<' "$W/gate/append-only.diff" || true)" \
  "$(grep -c '^>' "$W/gate/append-only.diff" || true)"

# g1 — guard on the applied mirror (same call as g0, registry now S001..S353 with the gap)
guard g1
# g1-delta — which staged ids the round's append newly steals
cp "$W/guard-g0/collisions" "$W/gate/collisions-g0.txt"
cp "$W/guard-g1/collisions" "$W/gate/collisions-g1.txt"
comm -13 "$W/gate/collisions-g0.txt" "$W/gate/collisions-g1.txt" > "$W/gate/collisions-new.txt"
printf 'collisions new by the round append=%s: %s\n' \
  "$(wc -l < "$W/gate/collisions-new.txt")" "$(tr '\n' ' ' < "$W/gate/collisions-new.txt")"

# b0 — reverse apply order (supersession block first, then the new rows): does order matter?
cp "$W/pristine-SOURCES.md" "$SRC"; standin
insert "$W/mirror-src/sup-rows.txt" "$W/mirror-src/new-rows.txt"; count b0

# restore the intended landing state
cp "$W/pristine-SOURCES.md" "$SRC"; standin
insert "$W/mirror-src/new-rows.txt" "$W/mirror-src/sup-rows.txt"
cp "$SRC" "$W/applied-SOURCES.md"
cp "$W/gate/"* "$SEAT/" 2>/dev/null || true
cp "$W/mirror-src/"* "$SEAT/" 2>/dev/null || true
