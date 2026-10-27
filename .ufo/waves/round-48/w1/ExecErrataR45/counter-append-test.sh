#!/bin/bash
# ExecErrataR45 (round 48 w1, R4b): does the append block keep the frozen round-45 C2
# counters green? Everything happens in a throwaway clone; the lane is only read.
#
# usage: counter-append-test.sh <scratch-dir> <block.md> <receipts-dir>
set -u
S=${1:?scratch dir}
BLOCK=${2:?block}
OUT=${3:?receipts dir}
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
C1=$LANE/quality/counters/c2-r45-monitor-entry.py
C2=$LANE/quality/counters/c2-r45-monitor-entry-v2.py
ENTRY=corpus/knowledge/hyprland-monitor-rule-r45.md
VERIFY=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/w1/ExecErrataR45/verify-locators.py
R45=4d22eeb66c2835af8aaa3fac6ad838fa616aa663
R48=579f694b45c797a9c39761fdb4f9e0a1b71b3585
HEAD=$(git -C "$LANE" rev-parse HEAD)

mkdir -p "$S" "$OUT" || exit 2
export TMPDIR="$S"
trap 'rm -rf -- "$S"' EXIT
D=$(mktemp -d -p "$S" clone-XXXX) || exit 2
git clone -q --shared --no-checkout "$LANE" "$D" || exit 2
if [ "$(git -C "$D" rev-parse --show-toplevel)" != "$D" ]; then
    echo "REFUSING: clone toplevel is not $D"; exit 2
fi
echo "# clone $D of $LANE"
echo "# base entry sha256 $(git -C "$D" show "$R48:$ENTRY" | sha256sum | cut -d' ' -f1)"
echo "# block $BLOCK sha256 $(sha256sum "$BLOCK" | cut -d' ' -f1) lines $(wc -l <"$BLOCK")"
echo "# lane HEAD $HEAD"

run_one() { # $1 counter
    local out rc
    out=$(python3 -I "$1" --repo "$D" --rev HEAD)
    rc=$?
    printf '%s\n' "$out" | grep -E '^PRED-C2-r45.*admitted='
    echo "  exit=$rc"
}

run_both() {
    run_one "$C1"
    run_one "$C2"
}

# negative controls: the same block with the source id put back into E6, and the
# round-47 as-drafted block. Both must leave the entry out of the predicate.
CTRL1=$S/control-id-in-E6.md
python3 - "$BLOCK" "$CTRL1" <<'PY'
import sys
src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
old = "(the legacy handler file the entry's source list names)"
assert old in text, "anchor for the control is gone"
open(dst, "w", encoding="utf-8").write(text.replace(old, "(S303)"))
PY
CTRL2=$LANE/.ufo/waves/round-47/w2/ExecErrataR45/block-as-drafted.md

control() { # $1 label, $2 block file
    git -C "$D" checkout -q --detach "$R48" || return 1
    cat "$2" >>"$D/$ENTRY"
    git -C "$D" add "$ENTRY" || return 1
    git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid \
        commit -q -m "control $1" || return 1
    echo
    echo "== control $1 (expected: both counters TARGET_MISSED) =="
    run_both
}

for REV in "$R45" "$R48" "$HEAD"; do
    git -C "$D" checkout -q --detach "$REV" || exit 2
    echo
    echo "== rev $REV baseline (no errata) =="
    run_both
    cat "$BLOCK" >>"$D/$ENTRY"
    git -C "$D" add "$ENTRY" || exit 2
    git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid \
        commit -q -m "errata r45 appended (seat ExecErrataR45, round 48)" || exit 2
    echo "== rev $REV + block: commit $(git -C "$D" rev-parse HEAD) =="
    echo "   entry lines $(wc -l <"$D/$ENTRY") sha256 $(sha256sum "$D/$ENTRY" | cut -d' ' -f1)"
    run_both
    if [ "$REV" != "$R45" ]; then
        echo "-- round-48 locator check in the appended tree ($REV) --"
        python3 -I "$VERIFY" --repo "$D" --block "$BLOCK" | tail -3
    fi
done

control "S-id put back in E6" "$CTRL1"
control "round-47 block as drafted" "$CTRL2"
