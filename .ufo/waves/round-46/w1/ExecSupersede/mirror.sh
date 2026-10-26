#!/usr/bin/env bash
# ExecSupersede (round 46 w1) - census proof for the S326-S333 supersession.
# One read-only copy of the lane tree under the seat scratch dir (no .git); each variant swaps only
# corpus/SOURCES.md (and, for m2, the used-by target), then runs the fleet census with --file.
# Starts no git command and writes no lane file.
set -u
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/w1/ExecSupersede
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
BASE=${1:?scratch base dir}
ROWS="$SEAT/rows-block.txt"
OUT="$SEAT"
TREE="$BASE/tree"
USEDBY=.ufo/waves/round-46/w1/ExecSupersede/rows.md

mkdir -p -- "$BASE"
[ -d "$TREE" ] || { mkdir -p -- "$TREE"; ( cd "$LANE" && tar -cf - --exclude=.git . ) | ( cd "$TREE" && tar -xf - ); }
# the used-by target is this seat's rows.md: keep the mirror copy byte-identical to the lane file
mkdir -p -- "$TREE/$(dirname "$USEDBY")"
cp "$SEAT/rows.md" "$TREE/$USEDBY"

apply() { # $1 mode
  local mode=$1 f="$TREE/corpus/SOURCES.md"
  case "$mode" in
    none) : ;;
    rows|rows-no-opener|rows-no-usedby|rows-unused)
      awk -v rows="$ROWS" -v mode="$mode" '
        { print }
        /^\|[[:space:]]*S315[[:space:]]*\|/ {
          while ((getline line < rows) > 0) {
            if (mode == "rows-no-opener") sub(/supersedes S[0-9][0-9][0-9] — /, "", line)
            if (mode == "rows-no-usedby") sub(/\| \.ufo\/waves\/round-46\/w1\/ExecSupersede\/rows\.md \|$/, "| .ufo/waves/round-46/w1/ExecSupersede/missing.md |", line)
            if (mode == "rows-unused") sub(/\| \.ufo\/waves\/round-46\/w1\/ExecSupersede\/rows\.md \|$/, "| — |", line)
            print line
          }
        }
      ' "$f" > "$f.new" && mv -- "$f.new" "$f"
      ;;
    prose-errata)
      cat >> "$f" <<'EOF'

## Errata (round 46 w1, prose form - control)

- S290, S291, S292, S293, S294: the teaches cell overstates what the cited file shows; read the successor row.
- S296, S297: the teaches cell treats one snapshot as history and the anchor locators as ui.py lines.
EOF
      ;;
    table-errata)
      cat >> "$f" <<'EOF'

## Errata (round 46 w1, table form - control)

| S900 | errata |  |
|---|---|---|
| S290 | teaches overstates the file | read S326 |
EOF
      ;;
  esac
}

run() { # $1 variant, $2 mode
  local v=$1 mode=$2 f="$TREE/corpus/SOURCES.md"
  cp "$f" "$BASE/SOURCES.orig"
  apply "$mode"
  local nrows; nrows=$(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$f")
  bash "$CENSUS" validate --file "$f" > "$OUT/census-$v.txt" 2>&1
  local rc=$?
  cp "$BASE/SOURCES.orig" "$f"
  printf '%-4s %-15s exit=%d rows=%d  E=%s W=%s  E=[%s] W=[%s]\n' "$v" "$mode" "$rc" "$nrows" \
    "$(grep -cE $'\tE[0-9]{2}\t' "$OUT/census-$v.txt")" "$(grep -cE $'\tW[0-9]{2}\t' "$OUT/census-$v.txt")" \
    "$(grep -oE $'\tE[0-9]{2}\t' "$OUT/census-$v.txt" | tr -d '\t' | sort | uniq -c | tr '\n' ' ')" \
    "$(grep -oE $'\tW[0-9]{2}\t' "$OUT/census-$v.txt" | tr -d '\t' | sort | uniq -c | tr '\n' ' ')"
}

# row count of each variant file (for m1 etc. the applied file, captured before restore)
counts() { # $1 mode
  local f="$TREE/corpus/SOURCES.md" n
  cp "$f" "$BASE/SOURCES.orig"
  apply "$1"
  n=$(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$f")
  cp "$BASE/SOURCES.orig" "$f"
  printf '%s' "$n"
}

echo "# variant table (exit / rows after applying the variant / findings)"
run m0 none
run m1 rows
run m2 rows-no-usedby
run m3 prose-errata
run m4 table-errata
run m5 rows-no-opener
run m6 rows-unused
echo
echo "# row counts: m0=$(counts none) m1=$(counts rows) m3=$(counts prose-errata) m4=$(counts table-errata) m5=$(counts rows-no-opener) m6=$(counts rows-unused)"
echo
echo "# m1 full output (the recommended landing)"
cat "$OUT/census-m1.txt"
