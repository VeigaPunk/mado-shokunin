#!/usr/bin/env bash
# Differential C1 runs on paths the 13 controls never reach; byte-compare every counter version.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
W=$LANE/.ufo/waves/round-37/w1/scratch/SimplifyCounters
BASE=b4e47e980bfb0cbc8a4e788f59a41db858751fd8
E1=corpus/knowledge/event-delivery-limits-r26.md
SB=/dev/shm/mado37-SimplifyCounters/c1sb
for k in $(env | sed -n 's/^\(GIT_[^=]*\)=.*/\1/p'); do unset "$k"; done
export GIT_AUTHOR_NAME=sandbox GIT_AUTHOR_EMAIL=sandbox@invalid GIT_COMMITTER_NAME=sandbox GIT_COMMITTER_EMAIL=sandbox@invalid
rm -rf "$SB"
git clone -q --no-local --no-checkout "$LANE" "$SB"
g() { git -C "$SB" "$@"; }
g sparse-checkout set --no-cone /corpus/ /.ufo/waves/round-37/
g checkout -q --detach "$BASE"
commit() { g add -A && g commit -q --allow-empty -m "$1" && g rev-parse HEAD; }

# A: E1 present at base as a token-free file
mkdir -p "$SB/corpus/knowledge"; printf '# placeholder\n' > "$SB/$E1"
A=$(commit A)
# B: golden wiring on top of A (controls.wire, frozen copy)
python3 - "$SB" <<'EOF'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("ctl", "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/w1/scratch/SimplifyCounters/orig/controls.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); m.wire(sys.argv[1])
EOF
B=$(commit B)
# D: E1 path is a directory at base
g checkout -q --detach "$BASE"; mkdir -p "$SB/$E1"; printf 'token-free\n' > "$SB/$E1/x.md"
D=$(commit D)
# H: ground held at base
g checkout -q --detach "$BASE"; mkdir -p "$SB/corpus/knowledge"; printf 'MAX_QUEUED_EVENTS\n' > "$SB/corpus/knowledge/held.md"
H=$(commit H)
echo "A=$A B=$B D=$D H=$H"

run() { python3 -I "$1" "${@:2}" 2>&1; echo "rc=$?"; }
for v in orig P1 P2 ALL; do
  c=$W/$v/c1-r37-event-ground.py; o=$W/out/c1diff-$v.txt; : > "$o"
  { echo "## r1 existed-at-base file"; run "$c" --repo "$SB" --rev "$B" --base "$A"
    echo "## r2 directory-at-base";    run "$c" --repo "$SB" --rev "$B" --base "$D"
    echo "## r3 ground-held";          run "$c" --repo "$SB" --rev "$B" --base "$H"
    echo "## r4 unresolvable rev";     run "$c" --repo "$SB" --rev nosuchrev
    echo "## r5 golden default base";  run "$c" --repo "$SB" --rev "$B"
    echo "## r6 lane HEAD (read-only)"; run "$c" --repo "$LANE" --rev HEAD | sed -E 's/rev=[0-9a-f]{40}/rev=LANEHEAD/'
  } >> "$o"
done
for v in P1 P2 ALL; do
  if cmp -s "$W/out/c1diff-orig.txt" "$W/out/c1diff-$v.txt"; then echo "c1diff $v == orig"; else echo "c1diff $v DIFFERS:"; diff "$W/out/c1diff-orig.txt" "$W/out/c1diff-$v.txt"; fi
done
rm -rf "$SB"
