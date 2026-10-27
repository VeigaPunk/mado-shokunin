#!/usr/bin/env bash
# CritC2Pin w2 scratch mirror: lane at BASE + the l1-draft C2 bytes, sparse checkout so the
# lane's >1 MiB historical fixtures never land under the 1 MiB/file writer cap.
set -eu
ulimit -f 2048
L=/home/vgpnk/Projects/shokunin/mado-shokunin
W=$L/.ufo/waves/round-48
S=/fast/scratch/hyaku/mado-r48/CritC2Pin
rm -rf "$S/mirror"; mkdir -p "$S/mirror"
D=$S/mirror/clone
git clone -q --shared --no-checkout "$L" "$D"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "BAD TOPLEVEL"; exit 1; }
git -C "$D" sparse-checkout init --cone
git -C "$D" sparse-checkout set corpus quality/counters tools .ufo/waves/round-46/fetch
git -C "$D" checkout -q 579f694b45c797a9c39761fdb4f9e0a1b71b3585
[ "$(git -C "$D" rev-parse HEAD)" = 579f694b45c797a9c39761fdb4f9e0a1b71b3585 ] || { echo "BAD REV"; exit 1; }
mkdir -p "$D/.ufo/waves/round-48/fetch" "$D/.ufo/waves/round-48/receipts" "$D/.ufo/waves/round-48/tools"
cp "$W"/fetch/* "$D/.ufo/waves/round-48/fetch/"
cp "$W/receipts/xkbcli-compile-keymap-r48.txt" "$D/.ufo/waves/round-48/receipts/"
cp "$W/tools/make-xkb-receipt.sh" "$D/.ufo/waves/round-48/tools/"
cp "$W/l1-draft/xkb-keymap-compile-r48.md" "$D/corpus/knowledge/"
python3 - "$D" "$W/l1-draft/rows-c2.md" "$W/l1-draft/readme-row.md" <<'EOF'
import sys
d, rows, rr = sys.argv[1:]
p = d + "/corpus/SOURCES.md"
s = open(p).read().split("\n")
i = max(k for k, l in enumerate(s) if l.startswith("| S339 |"))
s[i + 1:i + 1] = open(rows).read().rstrip("\n").split("\n")
open(p, "w").write("\n".join(s))
p = d + "/corpus/README.md"
s = open(p).read().split("\n")
i = max(k for k, l in enumerate(s) if l.startswith("| `knowledge/xdg-terminal-selection-r47.md`"))
s[i + 1:i + 1] = [open(rr).read().rstrip("\n")]
open(p, "w").write("\n".join(s))
EOF
git -C "$D" add -A
git -C "$D" -c user.name=t -c user.email=t@t commit -qm c2-mirror
git -C "$D" rev-parse HEAD
