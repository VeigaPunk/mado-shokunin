#!/usr/bin/env bash
# compare-w1-data.sh — round 50, w2 seat ScrQuoteVerify2.
# Compares the 12 quote tuples the round-50 lesson's Gate claims were "re-verified 12/12 by
# ScrRowsR50/verify-quotes.sh" against the DATA table committed inside that seat's script at
# the same revision. Committed bytes only (`git show`), read-only.
set -u
REV=${REV:-b4a79843cc2545bbe800db9322e58f6e00436629}
LANE=${LANE:-/home/vgpnk/Projects/shokunin/mado-shokunin}
W=${W:-/fast/scratch/hyaku/mado-r50/ScrQuoteVerify2/run}
ulimit -f 65536 2>/dev/null || true
mkdir -p "$W"
[ "$(git -C "$LANE" rev-parse --show-toplevel)" = "$LANE" ] || { echo "ERROR: wrong toplevel" >&2; exit 2; }

git -C "$LANE" show "$REV:.ufo/waves/round-50/w1/ScrRowsR50/verify-quotes.sh" > "$W/w1-verify-quotes.sh"
git -C "$LANE" show "$REV:corpus/lessons/round-50.md" > "$W/lesson.md"

awk '/^DATA=\$\(cat <</{f=1;next} /^EOF/{f=0} f' "$W/w1-verify-quotes.sh" > "$W/w1-data.tsv"

awk '
  /^- \*\*S[0-9]+ admit\*\*/ {
    id=$0; sub(/^- \*\*/, "", id); sub(/ admit\*\*.*/, "", id)
    file=""; ln=""; words=""; quote=""
    if (match($0, /\.ufo\/waves\/round-50\/fetch\/[A-Za-z0-9._-]+:[0-9]+/)) {
      pin=substr($0, RSTART, RLENGTH); n=split(pin, a, ":"); ln=a[n]; f=a[n-1]; sub(/^.*\//, "", f); file=f
    }
    if (match($0, /»[^«]*«/)) quote=substr($0, RSTART+1, RLENGTH-2)
    if (match($0, /\([0-9]+ words\)/)) { w=substr($0, RSTART+1, RLENGTH-2); sub(/ words/, "", w); words=w }
    printf "%s\t%s\t%s\t%s\t%s\n", id, file, ln, words, quote
  }' "$W/lesson.md" | sort > "$W/lesson-data.tsv"
sort "$W/w1-data.tsv" | awk -F'\t' '{printf "%s\t%s\t%s\t%s\t%s\n", $1, $2, $3, $4, $5}' > "$W/w1-data-sorted.tsv"

echo "REV=$REV"
echo "w1 DATA rows=$(wc -l < "$W/w1-data.tsv")  lesson admit rows=$(wc -l < "$W/lesson-data.tsv")"
if diff -u "$W/w1-data-sorted.tsv" "$W/lesson-data.tsv" > "$W/w1-vs-lesson.diff"; then
  echo "MATCH: every committed lesson admit tuple (id, pin file, line, word count, quote) equals the w1 DATA table row for the same id"
  echo "mismatches=0"
  exit 0
fi
echo "DIFF (left=w1 DATA, right=lesson admits):"
cat "$W/w1-vs-lesson.diff"
echo "mismatches=$(grep -c '^[-+][^-+]' "$W/w1-vs-lesson.diff")"
exit 1
