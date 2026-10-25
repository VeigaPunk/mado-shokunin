#!/bin/bash
# check70 - wave-control marker discipline at a revision (QUALITY criterion 70).
#
# Every dispatch/ready marker a wave writes (`*.ready`, `*.ready.dispatched`) is either
# committed at the revision the round closes on, or absent from the tree. A marker left
# untracked means the round's own run state is not reproducible from the tip.
#
# Usage: check70.sh <repo> <rev> <wave-dir>
# Exit 0 = CLEAN, 1 = DIRTY_MARKER.
set -u
repo=$1; rev=$2; dir=$3
fail=0

tracked=$(git -C "$repo" ls-tree -r --name-only "$rev" -- "$dir" | grep -E '\.ready(\.dispatched)?$' || true)
echo "TRACKED_MARKERS:"
if [ -n "$tracked" ]; then printf '%s\n' "$tracked" | sed 's/^/  /'; else echo "  (none)"; fi

for f in "$repo/$dir"/*.ready "$repo/$dir"/*.ready.dispatched; do
  [ -e "$f" ] || continue
  rel=${f#"$repo"/}
  if [ -n "$tracked" ] && printf '%s\n' "$tracked" | grep -qxF "$rel"; then
    echo "COMMITTED $rel"
  else
    echo "UNTRACKED $rel"
    fail=1
  fi
done

dirty=$(git -C "$repo" status --porcelain -- "$dir" 2>/dev/null | grep -E '\.ready' || true)
if [ -n "$dirty" ]; then
  echo "DIRTY:"
  printf '%s\n' "$dirty" | sed 's/^/  /'
  fail=1
fi

if [ "$fail" -eq 0 ]; then echo "VERDICT: CLEAN"; else echo "VERDICT: DIRTY_MARKER"; fi
exit "$fail"
