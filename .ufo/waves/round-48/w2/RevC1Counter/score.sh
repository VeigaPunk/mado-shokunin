#!/usr/bin/env bash
# Score one candidate tools/mado-terminal.py against the FROZEN r48 C1 counter.
# A minimal fixture repo (the lane's .git/index is 2771712 B > the 1 MiB file guard, so a lane clone cannot be
# checked out under ulimit -f 2048): the exact freeze blobs the counter reads, verified by sha256.
# Usage: score.sh TOOL TAG NONCE
set -eu
ulimit -f 2048
L=/home/vgpnk/Projects/shokunin/mado-shokunin
FREEZE=3e6c848a0e1bbc9c7058226b86d0faefc5351c9d
S=/fast/scratch/hyaku/mado-r48/RevC1Counter/$2
TOOL=$1; TAG=$2; NONCE=${3:-4848}
rm -rf "$S"; mkdir -p "$S/c" "$S/work"
D=$(mktemp -d -p "$S/c") && git -C "$D" init -q
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "ROOT-MISMATCH"; exit 9; }
mkdir -p "$D/tools" "$D/quality/counters" "$D/.ufo/waves/round-47/fetch"
for p in quality/counters/c1-r48-terminal-cache.py quality/counters/c1-r47-fixtures.json \
         quality/counters/c1-r48-fixtures.json .ufo/waves/round-47/fetch/xdg-terminal-exec; do
  git -C "$L" show "$FREEZE:$p" > "$D/$p"
  a=$(git -C "$L" rev-parse "$FREEZE:$p"); b=$(git -C "$D" hash-object "$D/$p")
  [ "$a" = "$b" ] || { echo "BLOB-MISMATCH $p $a $b"; exit 9; }
done
cp "$TOOL" "$D/tools/mado-terminal.py"
git -C "$D" add -A
git -C "$D" -c user.name=w2probe -c user.email=w2probe@invalid commit -qm "w2 c1 probe $TAG"
echo "REPO=$D TOOL_SHA=$(sha256sum "$D/tools/mado-terminal.py" | cut -d' ' -f1) HEAD=$(git -C "$D" rev-parse HEAD)"
cd "$D"
python3 -I quality/counters/c1-r48-terminal-cache.py --repo "$D" --rev HEAD --work "$S/work" --nonce "$NONCE"
