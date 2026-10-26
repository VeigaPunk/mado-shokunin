#!/usr/bin/env bash
# guard-proof.sh <workdir> — proves the prompt's id-collision guard before trusting it.
# (a) the 0-3-space extractor catches an INDENTED registry row that a column-zero-only
#     extractor misses (the documented false-green); (b) the current registry has no indented
#     rows, so the two extractors agree today; (c) E03 is what a collision costs at append time.
set -u
W=${1:?usage: guard-proof.sh <workdir>}
L=/home/vgpnk/Projects/shokunin/mado-shokunin
APPEND=/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
OUT=$W/gate

# (a) indented-collision fixture: an indented registry row S002 against a staged S002
F=$W/guard-proof; rm -rf "$F"; mkdir -p "$F"
printf '| S001 | a | code | A | s | a | t | mined | 2026-10-01 | on-release | x |\n  | S002 | b | code | A | s | a | t | mined | 2026-10-01 | on-release | x |\n' > "$F/reg.md"
printf '| S002 | c | code | A | s | a | t | mined | 2026-10-01 | on-release | x |\n' > "$F/staged.md"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$F/reg.md" | grep -oE 'S[0-9]+' | sort > "$F/reg-ids-0to3"
grep -oE '^\|[[:space:]]*S[0-9]{3,}'        "$F/reg.md" | grep -oE 'S[0-9]+' | sort > "$F/reg-ids-col0"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$F/staged.md" | grep -oE 'S[0-9]+' | sort > "$F/staged-ids"
comm -12 "$F/reg-ids-0to3" "$F/staged-ids" > "$F/coll-0to3"
comm -12 "$F/reg-ids-col0" "$F/staged-ids" > "$F/coll-col0"
{
  echo "guard-proof (a): indented registry row vs staged row"
  echo "  0-3-space collisions: $(tr '\n' ' ' < "$F/coll-0to3")  count=$(wc -l < "$F/coll-0to3")"
  echo "  column-0    collisions: $(tr '\n' ' ' < "$F/coll-col0")  count=$(wc -l < "$F/coll-col0")"
  grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$F/reg.md" > "$F/matched-rows"; echo "  extractor matched lines:"; sed 's/^/    /' "$F/matched-rows"
} | tee "$OUT/guard-proof-a.txt"

# (b) the lane registry / mirror registry today: any indented rows?
{
  echo "guard-proof (b): indented registry rows in the applied mirror"
  printf '  0-3-space pattern rows: %s\n' "$(grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$W/applied-SOURCES.md")"
  printf '  column-0   pattern rows: %s\n' "$(grep -cE '^\|[[:space:]]*S[0-9]{3,}' "$W/applied-SOURCES.md")"
  printf '  indented rows (1-3 spaces): %s\n' "$(grep -cE '^ {1,3}\|[[:space:]]*S[0-9]{3,}' "$W/applied-SOURCES.md" || true)"
  printf '  indented rows in SOURCES.append.md: %s\n' "$(grep -cE '^ {1,3}\|[[:space:]]*S[0-9]{3,}' "$APPEND" || true)"
} | tee "$OUT/guard-proof-b.txt"

# (c) reverse order at append time: staged package first, then the round's 21 rows
T=$W/tree-c; rm -rf "$T"; mkdir -p "$T"
rsync -a "$W/tree/" "$T/" 2>/dev/null
STRC=$T/corpus/SOURCES.md
cp "$W/pristine-SOURCES.md" "$STRC"
grep -E '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$APPEND" > "$W/mirror-src/staged-rows.txt"
awk -v a="$W/mirror-src/staged-rows.txt" -v b="$W/mirror-src/new-rows.txt" -v c="$W/mirror-src/sup-rows.txt" '
  /^## Paths/ && !done { w=1
    while ((getline l < a) > 0) print l
    while ((getline l < b) > 0) print l
    while ((getline l < c) > 0) print l
    done=1 }
  { print }
' "$W/pristine-SOURCES.md" > "$STRC"
cp "$W/tree/corpus/knowledge/xdg-terminal-selection-r47.md" "$T/corpus/knowledge/xdg-terminal-selection-r47.md"
bash "$CENSUS" validate --today 2026-10-26 --file "$STRC" > "$OUT/census-c0-staged-first.txt" 2>&1
RC=$?
printf 'c0 staged-first exit=%s rows=%s E03=%s E01=%s E04=%s E11=%s\n' \
  "$RC" \
  "$(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$STRC")" \
  "$(grep -c $'\tE03\t' "$OUT/census-c0-staged-first.txt" || true)" \
  "$(grep -c $'\tE01\t' "$OUT/census-c0-staged-first.txt" || true)" \
  "$(grep -c $'\tE04\t' "$OUT/census-c0-staged-first.txt" || true)" \
  "$(grep -c $'\tE11\t' "$OUT/census-c0-staged-first.txt" || true)" | tee "$OUT/guard-proof-c.txt"
grep $'\tE03\t' "$OUT/census-c0-staged-first.txt" | head -20 >> "$OUT/guard-proof-c.txt"
