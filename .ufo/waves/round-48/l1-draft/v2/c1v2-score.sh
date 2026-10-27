#!/usr/bin/env bash
# L1 (attempt 3): score PRED-C1-r48-v2 (l1-draft/v2 counter + v2 fixtures) on a scratch clone at the freeze whose
# tools/mado-terminal.py is TOOL ("-" = absent). Writes nothing in the lane; full output to OUT.
# Usage: c1v2-score.sh TOOL TAG OUT [NONCE]
set -eu
L=/home/vgpnk/Projects/shokunin/mado-shokunin
H=$L/.ufo/waves/round-48/l1-draft/v2
TOOL=$1; TAG=$2; OUT=$3; NONCE=${4:-4848}
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mado-r48/L1v2-$TAG
rm -rf "$S"; mkdir -p "$S/c" "$S/work"
trap 'rm -rf -- "$S"' EXIT
D=$S/c/clone
git clone -q --shared "$L" "$D"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ]
git -C "$D" checkout -q 579f694b45c797a9c39761fdb4f9e0a1b71b3585
if [ "$TOOL" = "-" ]; then rm -f "$D/tools/mado-terminal.py"; else cp "$TOOL" "$D/tools/mado-terminal.py"; fi
cp "$H/c1-r48-terminal-cache-v2.py" "$H/c1-r48-fixtures-v2.json" "$L/quality/counters/c1-r47-fixtures.json" "$D/quality/counters/"
mkdir -p "$D/.ufo/waves/round-47/fetch"; cp "$L/.ufo/waves/round-47/fetch/xdg-terminal-exec" "$D/.ufo/waves/round-47/fetch/"
git -C "$D" add -A
git -C "$D" -c user.name=t -c user.email=t@t commit -qm "c1 v2 score $TAG"
cd "$D"
{ echo "# c1v2-score TAG=$TAG TOOL=$TOOL tool_sha256=$( [ "$TOOL" = - ] && echo absent || sha256sum "$TOOL" | cut -d' ' -f1) counter_sha256=$(sha256sum "$H/c1-r48-terminal-cache-v2.py" | cut -d' ' -f1)"
  python3 -I quality/counters/c1-r48-terminal-cache-v2.py --repo "$D" --rev HEAD --work "$S/work" --nonce "$NONCE"
  echo "exit=$?"; } > "$OUT" 2>&1 || true
grep -v ' pass$' "$OUT" | tail -n "${TAILN:-6}"
