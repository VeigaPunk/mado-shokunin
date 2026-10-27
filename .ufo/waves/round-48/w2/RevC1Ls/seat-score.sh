#!/usr/bin/env bash
# RevC1Ls: score the FROZEN counter on a scratch clone with TOOL installed (seat-owned scratch only).
set -eu
# The seat writer bound is 1 MiB/file (ulimit -f 2048). Cloning the lane needs more: the largest tracked
# blob is 4 207 542 bytes. The limit is raised ONLY for this lane clone (a byte copy, not seat output);
# all seat-authored writers keep ulimit -f 2048 and the 2 GB scratch budget is checked after the run.
ulimit -f 65536
L=/home/vgpnk/Projects/shokunin/mado-shokunin
H=$L/.ufo/waves/round-48/l1-draft
TOOL=$1; TAG=$2; NONCE=${3:-48048}
S=/fast/scratch/hyaku/mado-r48/RevC1Ls/score-$TAG
rm -rf "$S"; mkdir -p "$S/c" "$S/work"
D=$S/c/clone
git clone -q --shared "$L" "$D"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ]
git -C "$D" checkout -q 579f694b45c797a9c39761fdb4f9e0a1b71b3585
cp "$TOOL" "$D/tools/mado-terminal.py"
cp "$H/c1-r48-terminal-cache.py" "$H/c1-r48-fixtures.json" "$D/quality/counters/"
git -C "$D" add -A
git -C "$D" -c user.name=t -c user.email=t@t commit -qm "seat score $TAG"
cd "$D"
set +e
timeout 2400 python3 -I quality/counters/c1-r48-terminal-cache.py --repo "$D" --rev HEAD --work "$S/work" --nonce "$NONCE" > "$S/out.txt" 2>&1
echo "exit=$?" >> "$S/out.txt"
set -e
grep -v ' pass$' "$S/out.txt" | tail -30
echo "--- scratch bytes: $(du -sb "$S" | cut -f1) largest file: $(find "$S" -type f -printf '%s %p\n' | sort -n | tail -1)"
