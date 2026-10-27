#!/bin/bash
# Score the C2-r49 draft over the POS tree and one-clause controls.
# All work happens in the scratch clone passed as $1; receipts go to $2.
set -u
ulimit -f 65536
D=$1
OUT=$2
S=$(dirname "$D")
C=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49/w1/ExecCounterC2/c2-r49-bind-entry.py
M=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49/w1/ExecCounterC2/controls/mutate.py
POS=${POS_REV:-353b85cd1f97b5ae4a3c7e93bdd264de62864d13}
[ "$(git -C "$D" cat-file -t "$POS")" = commit ] || { echo "POS rev missing: $POS"; exit 1; }
BASE=03e4ae76aff7a4be59cb69970dd553baa319695a
LANE_TIP=5f37c1b87b3ce5e438d19284e32b2e46fd548a92
TMP=$S/tmprun
mkdir -p "$TMP" "$OUT"
GIT="git -C $D -c user.name=control -c user.email=control@local"

run() { # name rev [base]
    local name=$1 rev=$2 base=${3:-$BASE}
    echo "===== $name rev=$rev base=$base"
    TMPDIR="$TMP" python3 "$C" --repo "$D" --rev "$rev" --base "$base" 2>&1
    echo "exit=$?"
}

{
echo "# controls: C2-r49 draft vs POS and one-clause mutants"
echo "pos=$POS tempdir=$TMP"
run base-miss "$BASE"
run do-nothing-lane-tip "$LANE_TIP"
run pos "$POS"
echo "===== setup-entry-at-base (rc must be 2)"
TMPDIR="$TMP" python3 "$C" --repo "$D" --rev "$POS" --base "$POS" 2>&1
echo "exit=$?"
echo "===== tmpdir-refused (rc must be 2)"
TMPDIR=/tmp python3 "$C" --repo "$D" --rev "$POS" --base "$BASE" 2>&1
echo "exit=$?"
for m in quote-word range-9999 quote-long paraphrase step-quote branch-url pin-digest pin-and-file held-row-moved \
         held-not-cited held-rereg receipt-renamed receipt-absent receipt-typed receipt-resolve receipt-json \
         entry-digest entry-total nosteps limits-gone gate-missing paste-body row-unused row-used-by-held registry-unused \
         opened-old; do
    $GIT checkout -q -B "m_$m" "$POS" || exit 1
    python3 "$M" "$D" "$m" >/dev/null || { echo "MUTATION FAILED $m"; continue; }
    $GIT add -A || exit 1
    $GIT commit -q -m "control: $m" || exit 1
    rev=$(git -C "$D" rev-parse HEAD)
    run "$m" "$rev"
done
} > "$OUT/controls.txt" 2>&1
echo "controls written to $OUT/controls.txt"
