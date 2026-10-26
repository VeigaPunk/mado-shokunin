#!/bin/bash
# Teeth test for indep_gate_check.py (seat RerunC2Data).
# A private fixture repo under /fast/scratch is built from the data commit's own
# blobs, then one defect at a time is committed and the verifier re-run: the
# control copy must AGREE, every mutated copy must DISAGREE on the named axis.
set -u
R=/home/vgpnk/Projects/shokunin/mado-shokunin
S=${S:?scratch dir required}
SRC=$(cat "$S/D.txt")
REV=1959770657f1f8665097c1aed4be6c1cbb07139f
CHECK="$R/.ufo/waves/round-43/w2/RerunC2Data/indep_gate_check.py"
D3=$(mktemp -d -p "$S")
git -C "$D3" init -q
TOP=$(git -C "$D3" rev-parse --show-toplevel)
[ "$TOP" = "$D3" ] || { echo "FIXTURE-ABORT toplevel=$TOP"; exit 1; }
echo "fixture=$D3 toplevel=$TOP"

git -C "$SRC" archive "$REV" corpus/lessons/round-43.md \
    corpus/knowledge/hyprland-gkeep-geometry-r43.md .ufo/waves/round-43/fetch \
    | tar -x -C "$D3"
git -C "$D3" add -A
git -C "$D3" -c user.name=fixture -c user.email=fixture@localhost \
    commit -q -m "fixture: data-commit blobs"
BASE=$(git -C "$D3" rev-parse HEAD)
echo "fixture base=$BASE"

L=corpus/lessons/round-43.md
E=corpus/knowledge/hyprland-gkeep-geometry-r43.md
run() {  # $1 = case label
    out=$(TMPDIR=$S python3 -I "$CHECK" "$D3" "$(git -C "$D3" rev-parse HEAD)" 2>&1)
    rc=$?
    echo "--- $1 rc=$rc"
    echo "$out" | grep -E 'DISAGREE|INDEP VERDICT|SETUP'
}
commit() { git -C "$D3" add -A && \
    git -C "$D3" -c user.name=fixture -c user.email=fixture@localhost \
        commit -q -m "$1"; }

echo "=== T0 control (unmutated copy of the data commit)"
run T0-control

echo "=== T1 one hex digit of S292's declared sha256 flipped"
sed -i 's/^\(GATE S292 .*sha256=\)49323833/\149323833/' "$D3/$L"
commit T1
run T1-sha256
git -C "$D3" checkout -q "$BASE" -- "$L"

echo "=== T2 S155's quote corrupted (must lose its word-bounded occurrence)"
sed -i 's/quote="static_\.size = expr;"/quote="static_.size = expr21;"/' "$D3/$L"
commit T2
run T2-quote-absent
git -C "$D3" checkout -q "$BASE" -- "$L"

echo "=== T3 S292's entry locator shifted by one line (:10 -> :11)"
sed -i 's/Hyprland-Target\.cpp:10/Hyprland-Target.cpp:11/' "$D3/$E"
commit T3
run T3-locator
git -C "$D3" checkout -q "$BASE" -- "$E"

echo "=== T4 S295's entry quote changed by one word (420 -> 421)"
sed -i 's/windowrule = size 420 500, match:class \^(org\.omarchy\.gkeep)\$/windowrule = size 421 500, match:class ^(org.omarchy.gkeep)$/' "$D3/$E"
commit T4
run T4-entry-quote
git -C "$D3" checkout -q "$BASE" -- "$E"

echo "=== T5 S290's GATE line duplicated"
sed -i '/^GATE S290 /p' "$D3/$L"
commit T5
run T5-duplicate-gate
git -C "$D3" checkout -q "$BASE" -- "$L"

echo "=== T6 S294's entry carrier line deleted"
sed -i '/\*\*OBS\*\* S294 /d' "$D3/$E"
commit T6
run T6-no-carrier
rm -rf -- "$D3"
