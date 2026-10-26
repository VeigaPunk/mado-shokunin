#!/bin/bash
# ExecSupersede (round 45 w1) - census proof for rows S311-S317 on mirror copies; the lane is never written.
# Usage: bash mirror.sh            (writes receipts into this seat dir, scratch under /fast/scratch/hyaku/mado-r45/ExecSupersede)
set -u
S=/fast/scratch/hyaku/mado-r45/ExecSupersede
L=/home/vgpnk/Projects/shokunin/mado-shokunin
SEAT=$L/.ufo/waves/round-45/w1/ExecSupersede
ROWS=$SEAT/rows-block.txt
CEN=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
mkdir -p "$S"
trap 'rm -rf -- "$S/m0" "$S/m1" "$S/m2" "$S/m3" "$S/m4"' EXIT

insert_rows() { # insert_rows <sources-md> <rows-file>
  python3 - "$1" "$2" <<'PY'
import re, sys
src, rowsf = sys.argv[1], sys.argv[2]
lines = open(src).read().split("\n")
rows = [l for l in open(rowsf).read().split("\n") if l.strip()]
assert all(r.count("|") == 12 for r in rows), "row with a stray pipe"
last = max(k for k, l in enumerate(lines) if re.match(r"^\| S\d{3,} \|", l))
lines[last + 1:last + 1] = rows
open(src, "w").write("\n".join(lines))
print("inserted %d rows after line %d" % (len(rows), last + 1))
PY
}

usedby_list() { # list the used-by paths a SOURCES.md names, one per line
  python3 - "$1" <<'PY'
import re, sys
seen = set()
for line in open(sys.argv[1]):
    if re.match(r"^\| S\d{3,} \|", line) and line.count("|") == 12:
        for p in line.split("|")[11].split(","):
            p = p.strip()
            if p and p != "—":
                seen.add(p)
print("\n".join(sorted(seen)))
PY
}

populate() { # populate <mirror-root> <sources-md> - copy every used-by path the registry names, as the lane holds it
  local root=$1 f=$2 p paths
  paths=$(usedby_list "$f")
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    [ -e "$root/$p" ] && continue
    mkdir -p "$(dirname "$root/$p")"
    cp -a "$L/$p" "$root/$p" 2>/dev/null || echo "populate: lane lacks $p"
  done <<< "$paths"
}

run_census() { # run_census <label> <sources-md>
  local label=$1 f=$2
  ( cd /home/vgpnk/Projects/shokunin && bash "$CEN" validate --file "$f" --today 2026-10-26 ) > "$SEAT/census-$label.txt" 2>&1
  echo "$label exit=$? $(grep -c $'\tE[0-9]' "$SEAT/census-$label.txt") errors $(grep -c $'\tW' "$SEAT/census-$label.txt") warnings"
}

# m0 control: the lane corpus as it stands, no new rows
rm -rf "$S/m0"; mkdir -p "$S/m0"; cp -a "$L/corpus" "$S/m0/corpus"
populate "$S/m0" "$S/m0/corpus/SOURCES.md"
run_census m0 "$S/m0/corpus/SOURCES.md"

# m1: rows, no corpus/lessons/round-45.md (E11 expected)
rm -rf "$S/m1"; mkdir -p "$S/m1"; cp -a "$L/corpus" "$S/m1/corpus"
insert_rows "$S/m1/corpus/SOURCES.md" "$ROWS"
populate "$S/m1" "$S/m1/corpus/SOURCES.md"
run_census m1 "$S/m1/corpus/SOURCES.md"

# m2: rows + a lesson stub naming the ids (recommended landing shape)
rm -rf "$S/m2"; mkdir -p "$S/m2"; cp -a "$L/corpus" "$S/m2/corpus"
insert_rows "$S/m2/corpus/SOURCES.md" "$ROWS"
cat > "$S/m2/corpus/lessons/round-45.md" <<'EOF'
# round 45 (stub - the L1 owns the real lesson)

## Gate

Registry changes logged old->new (CORPUS.md rule 2): S311 supersedes S290; S312 supersedes S291; S313 supersedes S292;
S314 supersedes S293; S315 supersedes S294; S316 supersedes S296; S317 supersedes S297.
EOF
populate "$S/m2" "$S/m2/corpus/SOURCES.md"
run_census m2 "$S/m2/corpus/SOURCES.md"

# m3: joint landing - the round's own C2 rows S302-S310 (build-pos.py) plus S311-S317
rm -rf "$S/m3"; D=$(mktemp -d -p "$S" m3.XXXXXX); rmdir "$D"
git clone -q --shared --no-checkout "$L" "$D" || exit 1
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "clone toplevel mismatch"; exit 1; }
git -C "$D" checkout -q --detach 22a8dedd02f507689c567777e0f20b5e645c8ce0 || exit 1
python3 -I "$L/.ufo/waves/round-45/l1-draft/build-pos.py" "$D" || exit 1
insert_rows "$D/corpus/SOURCES.md" "$ROWS"
populate "$D" "$D/corpus/SOURCES.md"
run_census m3 "$D/corpus/SOURCES.md"
echo "m3 rows: $(cd /home/vgpnk/Projects/shokunin && bash "$CEN" census --file "$D/corpus/SOURCES.md" | grep $'\trows\t')"
echo "m3 lesson present: $(test -f "$D/corpus/lessons/round-45.md" && echo yes)"

# m4 mutant: m2 minus S314's supersedes opener on S314 (E04 expected)
rm -rf "$S/m4"; mkdir -p "$S/m4"; cp -a "$S/m2/corpus" "$S/m4/corpus"
python3 - "$S/m4/corpus/SOURCES.md" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
assert s.count("supersedes S294 —") == 1
s = s.replace("supersedes S294 — ", "", 1)
open(p, "w").write(s)
PY
populate "$S/m4" "$S/m4/corpus/SOURCES.md"
run_census m4 "$S/m4/corpus/SOURCES.md"
