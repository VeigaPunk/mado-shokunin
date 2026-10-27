#!/usr/bin/env bash
# Score one TOOL with the frozen C1 counter (l1-draft counter + fixtures) in a scratch clone of the lane at BASE.
# Sparse checkout: the lane carries >1 MiB corpus files and this shell is under `ulimit -Sf 2048` (1 MiB per file).
# The counter itself copies /usr/bin/gawk (1,274,872 B) into its sandbox, so the python call runs at 2 MiB.
# Usage: run-one.sh TOOLFILE TAG [NONCE]
set -eu
ulimit -Sf 2048
L=/home/vgpnk/Projects/shokunin/mado-shokunin
H=$L/.ufo/waves/round-48/l1-draft
S=/fast/scratch/hyaku/mado-r48/RevC1Explain
TOOL=$1; TAG=$2; NONCE=${3:-4848}
D=$S/c-$TAG/clone
rm -rf -- "$S/c-$TAG" "$S/work-$TAG"; mkdir -p "$D" "$S/work-$TAG"
git clone -q --shared --no-checkout "$L" "$D"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "clone root mismatch" >&2; exit 9; }
git -C "$D" config index.sparse true
git -C "$D" sparse-checkout init --cone
git -C "$D" sparse-checkout set tools quality .ufo/waves/round-47/fetch
git -C "$D" checkout -q 579f694b45c797a9c39761fdb4f9e0a1b71b3585
cp "$TOOL" "$D/tools/mado-terminal.py"
cp "$H/c1-r48-terminal-cache.py" "$H/c1-r48-fixtures.json" "$D/quality/counters/"
git -C "$D" add -A
git -C "$D" -c user.name=t -c user.email=t@t commit -qm "c1 score $TAG" >/dev/null
cd "$D"
( ulimit -Sf 4096 && python3 -I quality/counters/c1-r48-terminal-cache.py --repo "$D" --rev HEAD \
    --work "$S/work-$TAG" --nonce "$NONCE" > "$S/out-$TAG.txt" 2>&1 ) || true
echo "=== $TAG final:"; tail -1 "$S/out-$TAG.txt"
echo "=== $TAG clause lines:"; grep -E 'clause=(f cold|w warm|x explained|g generated|r trips|s rc|a tool)' "$S/out-$TAG.txt" | head -12
rm -rf -- "$S/c-$TAG" "$S/work-$TAG"
