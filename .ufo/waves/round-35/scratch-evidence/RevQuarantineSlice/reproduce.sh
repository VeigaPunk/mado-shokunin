#!/usr/bin/env bash
# RevQuarantineSlice — re-derivation of the mado slice of the absent-defect register.
# Read-only over REG and LANE. Writes only into this scratch dir.
set -uo pipefail

REG=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
APPEND=/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
OUT=$(cd "$(dirname "$0")" && pwd)

echo "## A. assigned command (verbatim)"
awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$REG" \
  | tee "$OUT/slice.raw.txt"
echo "awk_exit=$?"
echo "rows=$(wc -l < "$OUT/slice.raw.txt")"

echo
echo "## B. split the two tables (line boundary of each section header)"
awk -F'|' -v l='mado' 'NR<232  && $2 ~ ("`" l "`") && $4 ~ /S[0-9]+/ {print "T1", $4, $3}' "$REG" > "$OUT/t1.txt"
awk -F'|' -v l='mado' 'NR>266  && $2 ~ ("`" l "`") && $4 ~ /S[0-9]+/ {print "T2", $4, $3}' "$REG" > "$OUT/t2.txt"
cat "$OUT/t1.txt" "$OUT/t2.txt"
echo "T1_rows=$(wc -l < "$OUT/t1.txt")  T2_rows=$(wc -l < "$OUT/t2.txt")"
echo "T1_exit=$?  T2_exit=$?"

echo
echo "## C. independent recount: all lines whose lane cell is exactly \`mado\`"
grep -c '^| `mado` |' "$REG"; echo "grep_exit=$?"
echo "line_numbers:"; grep -n '^| `mado` |' "$REG" | cut -d: -f1 | tr '\n' ' '; echo

echo
echo "## D. register-wide table sizes (for the share denominators)"
echo -n "S1_all_lanes="; awk 'NR>27 && NR<232 && /^\| `/{n++} END{print n+0}' "$REG"
echo -n "S2_all_lanes="; awk 'NR>266 && /^\| `/{n++} END{print n+0}' "$REG"
echo -n "by_lane_sum=";  awk -F'|' 'NR>234 && NR<256 && $2 ~ /`/ {gsub(/[^0-9]/,"",$3); s+=$3} END{print s+0}' "$REG"
echo -n "by_lane_mado_row="; grep -n '^| `mado` | [0-9]' "$REG" | cut -c1-40

echo
echo "## E. comm: slice ids vs the eight adopted ids S203-S210"
awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {gsub(/[^S0-9]/,"",$4); print $4}' "$REG" | LC_ALL=C sort > "$OUT/slice_ids.txt"
printf 'S203\nS204\nS205\nS206\nS207\nS208\nS209\nS210\n' | LC_ALL=C sort > "$OUT/adopted.txt"
echo -n "slice_ids="; tr '\n' ' ' < "$OUT/slice_ids.txt"; echo
echo -n "adopted  ="; tr '\n' ' ' < "$OUT/adopted.txt"; echo
echo "intersection:"; LC_ALL=C comm -12 "$OUT/slice_ids.txt" "$OUT/adopted.txt" | tee "$OUT/comm12.txt"
echo "comm_exit=$?"
echo "adopted_not_in_slice:"; LC_ALL=C comm -13 "$OUT/slice_ids.txt" "$OUT/adopted.txt" | tr '\n' ' '; echo

echo
echo "## F. packaging offset: does register id + 17 name the same document downstream?"
while read -r id; do
  pack=$(printf 'S%03d' $(( ${id#S} + 17 )))
  src=$(grep -E "^\| $pack " "$APPEND" 2>/dev/null | cut -d'|' -f3 | cut -c1-72)
  echo "$id -> $pack : ${src:-<<absent>>}"
done < "$OUT/slice_ids.txt"

echo
echo "## G. slice ids after packaging that land inside the adopted band S203-S210"
while read -r id; do
  n=$(( ${id#S} + 17 ))
  if [ "$n" -ge 203 ] && [ "$n" -le 210 ]; then printf 'S%03d (from %s)\n' "$n" "$id"; fi
done < "$OUT/slice_ids.txt"

echo
echo "## H. lane ledger size / max id / the two colliding rows"
grep -oE '^\| S[0-9]{3} ' "$LANE/corpus/SOURCES.md" | tr -d '| ' | LC_ALL=C sort | wc -l
grep -oE '^\| S[0-9]{3} ' "$LANE/corpus/SOURCES.md" | tr -d '| ' | LC_ALL=C sort | tail -1
grep -nE '^\| S20[59] ' "$LANE/corpus/SOURCES.md" | cut -c1-120

echo
echo "DONE rc=$?"
