#!/usr/bin/env bash
# Census mirror for ScrSupersedeRows (round 44 w1). Builds read-only copies of the lane's
# corpus tree under scratch, appends the S302-S308 draft rows, and runs the fleet census
# validate. Nothing in the lane is written.
set -u
S=/fast/scratch/hyaku/mado-r44/ScrSupersedeRows
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
ROWS=$LANE/.ufo/waves/round-44/w1/ScrSupersedeRows/rows-block.txt
OUTDIR=$LANE/.ufo/waves/round-44/w1/ScrSupersedeRows
mkdir -p "$S" || exit 2

mirror() { # mirror <name> -> prints mirror root; copies only what E11 resolves
  local m=$S/$1
  rm -rf -- "$m"; mkdir -p "$m/corpus"
  cp -a "$LANE/corpus/." "$m/corpus/"
  python3 - "$LANE/corpus/SOURCES.md" "$m" "$LANE" <<'PY2'
import os, shutil, sys
src, m, lane = sys.argv[1], sys.argv[2], sys.argv[3]
n = 0
for line in open(src, encoding="utf-8"):
    if not line.startswith("| S"):
        continue
    cells = line.rstrip("\n").split("|")
    if len(cells) < 13:
        continue
    for item in [x.strip() for x in cells[11].replace(";", ",").split(",")]:
        if not item:
            continue
        s = os.path.join(lane, item)
        if not os.path.exists(s):
            continue
        d = os.path.join(m, item)
        os.makedirs(os.path.dirname(d) or m, exist_ok=True)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
        n += 1
print("mirror used-by paths copied: %d" % n, file=sys.stderr)
PY2
  printf '%s' "$m"
}

insert_rows() { # insert_rows <mirror> <rowsfile>
  python3 - "$1" "$2" <<'PY'
import sys
m, rows = sys.argv[1], sys.argv[2]
p = m + "/corpus/SOURCES.md"
lines = open(p, encoding="utf-8").read().split("\n")
# last registry row line (0-based index of the S297 row)
idx = max(i for i, l in enumerate(lines) if l.startswith("| S29"))
block = [l for l in open(rows, encoding="utf-8").read().split("\n")
         if l.startswith("| S") and len(l.split("|")) == 13]
assert len(block) == 7 and all(len(l.split("|")) == 13 for l in block), "bad block: %d" % len(block)
lines[idx+1:idx+1] = block
open(p, "w", encoding="utf-8").write("\n".join(lines))
print("inserted %d rows after line %d" % (len(block), idx+1))
PY
}

lesson_stub() { # lesson_stub <mirror> <ids...>
  local m=$1; shift
  {
    printf '# mado round 44 — lesson (mirror stub: only the registry-changes section the rows need)\n\n'
    printf '## Registry changes logged old→new (CORPUS.md rule 2)\n\n'
    printf '| new row | supersedes | cells corrected |\n|---|---|---|\n'
    for pair in "$@"; do printf '%s\n' "$pair"; done
  } > "$m/corpus/lessons/round-44.md"
}

run() { # run <label> <mirror>
  "$CENSUS" validate --file "$2/corpus/SOURCES.md" --today 2026-10-26 > "$OUTDIR/census-$1.txt" 2>&1
  printf '%s exit=%s\n' "$1" "$?"
}

PAIRS=(
 '| S302 | S290 | scope wording kept, `teaches` corrected (class-to-engine binding unpinned, host text is S295), anchor cross-reference added |'
 '| S303 | S291 | title narrowed to the floating path, `teaches` corrected (parse gate, center conditions, downstream clamp), tiled consumer cross-referenced |'
 '| S304 | S292 | `teaches` corrected (round-43 w2 ScoutRowsB: the reported-geometry clause is a cross-row inference) |'
 '| S305 | S293 | title no longer echoes the refuted request premise, `teaches` corrected (both sides at :339, >5 gate at :342, 600x400 and error at :350-364, stored size at :323-326), anchor extended |'
 '| S306 | S294 | `teaches` tail corrected (retained inference dropped) |'
 '| S307 | S296 | scope and `teaches` corrected (reduced fields carry no `fullscreen`, absence is not "never mapped") |'
 '| S308 | S297 | title, anchor locators (ui.py:449/:476) and `teaches` corrected (default size, no `set_size_request`) |'
)

# --- control: the lane's own registry, unmodified
M=$(mirror m0); run m0 "$M"
# --- control 2: the mirror with no rows must equal the lane's own validate
"$CENSUS" validate --file "$LANE/corpus/SOURCES.md" --today 2026-10-26 > "$OUTDIR/census-lane.txt" 2>&1
printf 'lane exit=%s\n' "$?"
cmp -s "$OUTDIR/census-m0.txt" "$OUTDIR/census-lane.txt" && echo "m0 == lane copy" || echo "m0 != lane copy"

# --- M1: rows, used-by=corpus/lessons/round-44.md, but no lesson yet (expect E11 x7)
M=$(mirror m1); insert_rows "$M" "$ROWS"; run m1 "$M"
# --- M2: rows + lesson stub naming every id (expect clean, W04 x7 baseline only)
M=$(mirror m2); insert_rows "$M" "$ROWS"; lesson_stub "$M" "${PAIRS[@]}"; run m2 "$M"
# --- M3: S302 scope narrowed to the window-rule wording (measures the extra W04)
M=$(mirror m3); insert_rows "$M" "$ROWS"
python3 - "$M" <<'PY'
import sys
p = sys.argv[1] + "/corpus/SOURCES.md"
t = open(p, encoding="utf-8").read()
old = "| S302 | Hyprland v0.56.2 rule match engine - how a window-rule class expression becomes a boolean"
assert old in t
t = t.replace("The test a host `match:class` regex is put through, and the `negative:` prefix",
              "The test a window-rule regex string is put through, and the `negative:` prefix", 1)
open(p, "w", encoding="utf-8").write(t)
PY
lesson_stub "$M" "${PAIRS[@]}"; run m3 "$M"
# --- M4: mutant — S304 loses its `supersedes S292 —` opener (proves the E04 exemption is load-bearing)
M=$(mirror m4); insert_rows "$M" "$ROWS"
sed -i 's/| supersedes S292 — A target keeps/| A target keeps/' "$M/corpus/SOURCES.md"
lesson_stub "$M" "${PAIRS[@]}"; run m4 "$M"
# --- M5: rows with used-by = em dash (landable now, expect W03 x7)
M=$(mirror m5); insert_rows "$M" "$ROWS"
sed -i 's#| corpus/lessons/round-44.md |#| \xe2\x80\x94 |#' "$M/corpus/SOURCES.md"
run m5 "$M"
# --- M6: rows with used-by = the round-43 entry (census-clean only if that entry names the ids)
M=$(mirror m6); insert_rows "$M" "$ROWS"
sed -i 's#| corpus/lessons/round-44.md |#| corpus/knowledge/hyprland-gkeep-geometry-r43.md |#' "$M/corpus/SOURCES.md"
run m6 "$M"

# --- M5: each row's teaches opener the census regex sees (independent re-read of the block)
awk -F'|' 'NF==13 && /^\| S3[0-9][0-9] /{gsub(/^ +| +$/,"",$8); printf "%s\t%s\n", $2, substr($8,1,26)}' "$ROWS" > "$OUTDIR/opener-check.txt"

echo "--- verdicts ---"
for f in m0 lane m1 m2 m3 m4 m5 m6; do
  printf '%-5s exit-line: %s\n' "$f" "$(tail -1 "$OUTDIR/census-$f.txt")"
done
echo "--- finding counts ---"
for f in m0 m1 m2 m3 m4; do
  printf '%-4s E=%s W=%s W04=%s E04=%s E11=%s\n' "$f" \
    "$(grep -c $'\tE[0-9][0-9]\t' "$OUTDIR/census-$f.txt")" \
    "$(grep -c $'\tW[0-9][0-9]\t' "$OUTDIR/census-$f.txt")" \
    "$(grep -c $'\tW04\t' "$OUTDIR/census-$f.txt")" \
    "$(grep -c $'\tE04\t' "$OUTDIR/census-$f.txt")" \
    "$(grep -c $'\tE11\t' "$OUTDIR/census-$f.txt")"
done
