#!/usr/bin/env bash
# L1 (attempt 3) pre-data check: clone the lane at its tip, overlay the WORKING-TREE data files named below, commit in
# the scratch clone only, and run one counter on it. Usage: data-mirror.sh TAG OUT -- COUNTER-ARGS...
# (COUNTER-ARGS use @D for the clone path and @W for a scratch work dir). Writes nothing in the lane.
set -eu
L=/home/vgpnk/Projects/shokunin/mado-shokunin
TAG=$1; OUT=$2; shift 2; [ "$1" = "--" ] && shift
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mado-r48/L1mirror-$TAG
rm -rf "$S"; mkdir -p "$S/c" "$S/work"
trap 'rm -rf -- "$S"' EXIT
D=$S/c/clone
git clone -q --shared "$L" "$D"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ]
git -C "$D" checkout -q "$(git -C "$L" rev-parse master)"
for f in corpus/knowledge/xkb-keymap-compile-r48.md corpus/SOURCES.md corpus/README.md tools/mado-terminal.py .ufo/waves/round-48/fetch/xkbcommon-keymap.c \
         quality/counters/c1-r48-terminal-cache-v2.py quality/counters/c1-r48-fixtures-v2.json; do
  if [ -f "$L/$f" ]; then mkdir -p "$(dirname "$D/$f")"; cp "$L/$f" "$D/$f"; fi
done
git -C "$D" add -A
git -C "$D" -c user.name=t -c user.email=t@t commit -qm "data mirror $TAG"
args=()
for a in "$@"; do a=${a//@D/$D}; a=${a//@W/$S/work}; args+=("$a"); done
cd "$D"
{ echo "# data-mirror TAG=$TAG lane_tip=$(git -C "$L" rev-parse master) mirror=$(git -C "$D" rev-parse HEAD)"
  "${args[@]}"; echo "exit=$?"; } > "$OUT" 2>&1 || true
grep -v ' ok$\| pass$' "$OUT" | tail -n "${TAILN:-8}"
