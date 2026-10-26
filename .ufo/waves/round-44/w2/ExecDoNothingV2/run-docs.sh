#!/usr/bin/env bash
# Score the documentation-shape and tool-only do-nothing variants under both
# predicates. Every git call names -C $D (the fixture clone).
set -u
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/w2/ExecDoNothingV2
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
S=/fast/scratch/hyaku/mado-r44/ExecDoNothingV2
D=$S/fixture
DATA=e46789213830597348fe96a351ae004d10587385
BASE=6a1a90528fe533cadee506a9fa3e9d13d15cc41f
C1=$LANE/quality/counters/c1-r44-geometry-states-v2.py
C2=$LANE/quality/counters/c2-r44-gkeep-size-request-v2.py
mkdir -p "$S" "$SEAT/receipts"
if [ ! -d "$D/.git" ]; then
  git clone -q --shared "$LANE" "$D" || exit 9
fi
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "fixture toplevel wrong"; exit 9; }
mkdir -p "$SEAT/receipts" "$S/work"

commit() {  # branch message
  git -C "$D" add -A || return 9
  git -C "$D" -c user.name=ExecDoNothingV2 -c user.email=exec@lane.invalid \
      commit -q -m "$2" || return 9
  git -C "$D" rev-parse HEAD
}

# DOCS: the data commit minus every landed documentation row (6 files back to base)
git -C "$D" checkout -q -B v-docs "$DATA" || exit 9
git -C "$D" checkout "$BASE" -- LOG.md PROVINCE.md SCORECARD.md SKILL.md \
    corpus/QUALITY.md || exit 9
git -C "$D" rm -q quality/ratio-domain-meta.py || exit 9
REV=$(commit v-docs "do-nothing control: docs reverted to base") || exit 9
( cd "$LANE" && timeout 900 python3 -I "$C1" --repo "$D" --rev "$REV" \
    --work "$S/work" --nonce dn-docs ) > "$SEAT/receipts/c1-docs.txt" 2>&1
( cd "$LANE" && python3 -I "$C2" --repo "$D" --rev "$REV" ) \
    > "$SEAT/receipts/c2-docs.txt" 2>&1
echo "== docs rev=$REV"
grep -E 'clauses=|verdict=' "$SEAT/receipts/c1-docs.txt" | tail -2
grep -E 'clauses=|admitted=|verdict=' "$SEAT/receipts/c2-docs.txt" | tail -2

# TOOLONLY: the base tree plus the landed tool, nothing else
git -C "$D" checkout -q -B v-toolonly "$BASE" || exit 9
git -C "$D" checkout "$DATA" -- tools/mado-geometry.py || exit 9
REV=$(commit v-toolonly "do-nothing control: landed tool only, base tree") || exit 9
( cd "$LANE" && timeout 900 python3 -I "$C1" --repo "$D" --rev "$REV" \
    --work "$S/work" --nonce dn-toolonly ) > "$SEAT/receipts/c1-toolonly.txt" 2>&1
( cd "$LANE" && python3 -I "$C2" --repo "$D" --rev "$REV" ) \
    > "$SEAT/receipts/c2-toolonly.txt" 2>&1
echo "== toolonly rev=$REV"
grep -E 'clauses=|verdict=' "$SEAT/receipts/c1-toolonly.txt" | tail -2
grep -E 'clauses=|admitted=|verdict=' "$SEAT/receipts/c2-toolonly.txt" | tail -2
