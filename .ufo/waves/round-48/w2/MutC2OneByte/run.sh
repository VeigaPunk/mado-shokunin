#!/usr/bin/env bash
# w2/MutC2OneByte - C2 quote/anchor mutations scored by frozen PRED-C2-r48.
# Replay commits are built by git plumbing (no worktree checkout): the lane tracks
# files above the 1 MiB per-file bound, so only blobs are written, each < 64 KiB.
set -eu
ulimit -f 2048
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/w2/MutC2OneByte
L=/home/vgpnk/Projects/shokunin/mado-shokunin
COUNTER=$L/quality/counters/c2-r48-xkb-entry.py
BASE=579f694b45c797a9c39761fdb4f9e0a1b71b3585
S=/fast/scratch/hyaku/mado-r48/MutC2OneByte
trap 'rm -rf -- "$S"' EXIT
rm -rf "$S"
mkdir -p "$S/replay" "$S/ev" "$SEAT/receipts"
D=$S/m/clone
git clone -q --no-checkout --shared "$L" "$D"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ]
git -C "$D" rev-parse --verify --quiet "$BASE^{commit}" >/dev/null
python3 "$SEAT/build.py" "$D" "$S" >"$SEAT/receipts/revs.txt"
REV0=$(awk '$1=="M0_base_overlay"{print $2}' "$SEAT/receipts/revs.txt")
echo "overlay_rev=$REV0"
cp "$S/overlay-diff.txt" "$SEAT/receipts/overlay-diff.txt"

score () {
  local rev=$1 name=$2
  local out=$S/ev/$name.log
  set +e
  ( cd "$D" && TMPDIR="$S/replay" python3 -I "$COUNTER" --repo "$D" --rev "$rev" ) \
    >"$out" 2>&1
  local rc=$?
  set -e
  echo "== $name rev=$rev exit=$rc"
  grep -E 'clauses=|verdict=|clause=[a-z]+ .*(bad|mismatch|out_of|not_in|disagree|missing|no_|absent|ghost|unresolved|short|steps|words|present_at_base|redirect|other)' \
    "$out" | head -10 || true
  echo "exit=$rc" >>"$out"
  cp "$out" "$SEAT/receipts/$name.log"
  git -C "$D" diff --numstat "$REV0" "$rev" >"$S/ev/$name.numstat"
  cp "$S/ev/$name.numstat" "$SEAT/receipts/$name.numstat"
  git -C "$D" diff "$REV0" "$rev" >"$S/ev/$name.patch"
  cp "$S/ev/$name.patch" "$SEAT/receipts/$name.patch"
}

score "$REV0" "M0_base_overlay"

while read -r name rev; do
  case "$name" in
    base=*) continue ;;
    APPLY-FAILED) echo "== APPLY-FAILED $rev"; continue ;;
    M0_base_overlay) continue ;;
  esac
  score "$rev" "$name"
done <"$SEAT/receipts/revs.txt"

{
  echo "== largest files in scratch (bytes path)"
  find "$S" -type f -printf '%s %p\n' | sort -n | tail -5
  echo "== scratch bytes"
  du -sb "$S"
  echo "== replay leftover entries"
  find "$S/replay" -mindepth 1 | head -5
  echo "== clone worktree listing (empty = plumbing only)"
  ls "$D"
} >"$SEAT/receipts/scratch-bound.txt" 2>&1
cat "$SEAT/receipts/scratch-bound.txt"
cp "$S/digests.txt" "$SEAT/receipts/overlay-digests.txt"
