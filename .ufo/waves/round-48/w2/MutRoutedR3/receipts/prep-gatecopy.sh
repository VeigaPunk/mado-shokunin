#!/bin/sh
# MutRoutedR3 prep — commit the gate-copy target bytes, run the pristine detector.
set -u
S=/fast/scratch/hyaku/mado-r48/MutRoutedR3
CLONE=$S/clone
OUT=$S/out
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/w1/ExecSessionMarker
ID="-c user.name=MutRoutedR3 -c user.email=mutroutedr3@scratch.invalid"
ulimit -Sf 2048
export TMPDIR=$S/tmp
exec >> "$OUT/log3.txt" 2>&1
gitx() { sh -c 'ulimit -Sf unlimited; exec git "$@"' git "$@"; }

T=.ufo/waves/round-48/w1/ExecSessionMarker/check-session-material.py
mkdir -p "$CLONE/$(dirname "$T")"
cp "$SEAT/check-session-material.py" "$CLONE/$T"
sha256sum "$CLONE/$T"
gitx -C "$CLONE" add -- "$T"
TL=$(git -C "$CLONE" rev-parse --show-toplevel)
[ "$TL" = "$CLONE" ] || { echo "TOPLEVEL GUARD FAILED: $TL" >&2; exit 9; }
gitx -C "$CLONE" $ID commit -qm "scratch: add gate-copy target (MutRoutedR3)"
echo "gatecopy-commit=$(git -C "$CLONE" rev-parse HEAD)" >> "$OUT/commits.txt"

start=$(date +%s)
python3 -I "$CLONE/quality/check-session-material.py" --repo "$CLONE" --rev HEAD > "$OUT/D-pre-gatecopy.txt" 2>&1
rc=$?
printf 'PRE-gatecopy rc=%d %ss\n' "$rc" "$(( $(date +%s) - start ))" | tee -a "$OUT/rcs.txt"
grep -E '^(SESSION_MATERIAL|WAIVER file=.ufo/waves/round-48/w1/ExecSessionMarker/check)' "$OUT/D-pre-gatecopy.txt" | tail -6
