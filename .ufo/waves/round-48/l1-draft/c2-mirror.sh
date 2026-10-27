#!/usr/bin/env bash
# L1 pre-freeze check: build a scratch clone of the lane with the C2 data applied (entry, rows S340-S350, README row,
# fetch pins, receipt) and score a C2 counter on it, plus the census on the mirror. Usage: c2-mirror.sh COUNTER [SCRATCH]
set -eu
L=/home/vgpnk/Projects/shokunin/mado-shokunin
W=$L/.ufo/waves/round-48
C=$1
S=${2:-/fast/scratch/hyaku/mado-r48/L1c2}
rm -rf "$S"; mkdir -p "$S/m"
D=$S/m/clone
git clone -q --shared "$L" "$D"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ]
git -C "$D" checkout -q 579f694b45c797a9c39761fdb4f9e0a1b71b3585
mkdir -p "$D/.ufo/waves/round-48/fetch" "$D/.ufo/waves/round-48/receipts"
cp "$W"/fetch/* "$D/.ufo/waves/round-48/fetch/"
cp "$W/receipts/xkbcli-compile-keymap-r48.txt" "$D/.ufo/waves/round-48/receipts/"
mkdir -p "$D/.ufo/waves/round-48/tools"; cp "$W/tools/make-xkb-receipt.sh" "$D/.ufo/waves/round-48/tools/"
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
mkdir -p "$S/replay"
TMPDIR="$S/replay" python3 -I "$C" --repo "$D" --rev HEAD | grep -v ' ok$' | tail -30
echo "counter exit=${PIPESTATUS[0]}"
mkdir -p "$S/v/x-shokunin"; cp -r "$D/corpus" "$S/v/x-shokunin/"
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$D/corpus/SOURCES.md" | grep -v W04 | tail -5
echo "census exit=${PIPESTATUS[0]}"
