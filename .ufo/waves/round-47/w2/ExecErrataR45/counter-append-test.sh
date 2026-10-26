#!/bin/bash
# ExecErrataR45 (round-47 w2, R4b): does appending the errata block to
# corpus/knowledge/hyprland-monitor-rule-r45.md keep the frozen round-45 admission counters green?
#
# usage: counter-append-test.sh <work-dir> <block-as-drafted.md> <block-fixed.md>
# Everything happens in a throwaway clone under <work-dir>; the lane is only read.
set -u
WORK=${1:?work dir}
BLOCK=${2:?as-drafted block}
FIXED=${3:?fixed block}
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
C1=$LANE/quality/counters/c2-r45-monitor-entry.py
C2=$LANE/quality/counters/c2-r45-monitor-entry-v2.py
REV=4d22eeb66c2835af8aaa3fac6ad838fa616aa663
ENTRY=corpus/knowledge/hyprland-monitor-rule-r45.md

mkdir -p "$WORK" || exit 2
export TMPDIR="$WORK"
D=$(mktemp -d -p "$WORK" clone-XXXX) || exit 2
git clone -q --shared --no-checkout "$LANE" "$D" || exit 2
if [ "$(git -C "$D" rev-parse --show-toplevel)" != "$D" ]; then
    echo "REFUSING: clone toplevel is not $D"; exit 2
fi
git -C "$D" checkout -q --detach "$REV" || exit 2
echo "# clone $D at $(git -C "$D" rev-parse HEAD)"

run_both() {
    python3 -I "$C1" --repo "$D" --rev HEAD | grep -E 'clauses=|^PRED-C2-r45:'
    python3 -I "$C2" --repo "$D" --rev HEAD | grep -E '^PRED-C2-r45-v2:'
}

echo "== 1. baseline: frozen entry, no errata =="
run_both

append_and_run() { # $1 label, $2 insert-blank-before (0/1), $3 block file
    git -C "$D" checkout -q --detach "$REV"
    [ "$2" = 1 ] && printf '\n' >>"$D/$ENTRY"
    cat "$3" >>"$D/$ENTRY"
    git -C "$D" add "$ENTRY"
    git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid \
        commit -q -m "$1" || { echo "commit failed"; return 1; }
    echo "== $1 (rev $(git -C "$D" rev-parse --short HEAD)) =="
    run_both
}

append_and_run "verbatim-block-no-blank-line" 0 "$BLOCK"
append_and_run "verbatim-block-with-blank-line" 1 "$BLOCK"
append_and_run "fixed-block" 0 "$FIXED"

rm -rf "$D"
