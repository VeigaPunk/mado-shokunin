#!/usr/bin/env bash
# MutSessionMarker probe: build the planted clone at base 60edb66 and commit
# the five states. All git calls name -C "$D"; the toplevel guard runs
# before the first commit. Manifest keyed by state -> rev is written to
# $S/manifest.json with measured S0 numbers.
set -euo pipefail

LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
SEAT="$LANE/.ufo/waves/round-47/w2/MutSessionMarker"
S=/fast/scratch/hyaku/mado-r47/MutSessionMarker
BASE=60edb66e2f1cb90acc6e9442fc93ded0ca42d750
D="$S/clone"
PROBE="$SEAT/probe"

mkdir -p "$S/tmp" "$S/out"
cp "$LANE/.ufo/waves/round-47/w1/ExecSessionMarker/check-session-material.py" \
   "$S/gate-pristine.py"
sha256sum "$S/gate-pristine.py" | tee "$SEAT/receipts/00-gate-pristine-sha.txt"

rm -rf "$D"
git clone -q --shared --no-checkout "$LANE" "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
git -C "$D" checkout -q --detach "$BASE"
git -C "$D" rev-parse --show-toplevel > "$S/toplevel.txt"

python3 -I "$S/gate-pristine.py" --repo "$D" --rev HEAD > "$S/s0.txt" || rc=$?
test "${rc:-0}" = "1"
sed -n 's/^SESSION_MATERIAL: files=\([0-9]*\) findings=\([0-9]*\) rev=.*/F=\1 N=\2/p' "$S/s0.txt" > "$S/s0nums.txt"
. "$S/s0nums.txt"
test "$F" = "18371" || { echo "base files $F != 18371"; exit 1; }
test "$N" = "136" || { echo "base findings $N != 136"; exit 1; }
grep -q '^SESSION_MATERIAL_RULES: R1_CLIENT_DUMP=29 R2_PROC_TABLE=31 R3_MONITOR_IDENT=53 R4_HOME_LISTING=2 R5_SERIAL_PROSE=21$' "$S/s0.txt"

commit() { # commit <revname>
    git -C "$D" add -A
    git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid \
        commit -q -m "$1"
    git -C "$D" rev-parse HEAD
}

python3 -I "$PROBE/make-plants.py" "$D" s1
R1=$(commit "S1 unmarked plants")

python3 -I "$PROBE/make-plants.py" "$D" s2a
R2=$(commit "S2a clean waiver")

python3 -I "$PROBE/make-plants.py" "$D" s2b
R3=$(commit "S2b tampered waiver")

python3 -I "$PROBE/make-plants.py" "$D" s34
R4=$(commit "S34 registry-named real content + gate-copy mark")

python3 -I "$PROBE/make-plants.py" "$D" s5
R5=$(commit "S5 prose serial carrier")

python3 - "$S" "$BASE" "$R1" "$R2" "$R3" "$R4" "$R5" "$F" "$N" <<'PY'
import json, sys
s, base, *revs, F, N = sys.argv[1:]
F, N = int(F), int(N)
m = {
    "base": base,
    "S0-base": base, "S0-base.files": F, "S0-base.findings": N,
    "S1-unmarked": revs[0], "S1-unmarked.files": F + 3, "S1-unmarked.findings": N + 3,
    "S2a-cleanwaive": revs[1], "S2a-cleanwaive.files": F + 4, "S2a-cleanwaive.findings": N + 2,
    "S2b-tampered": revs[2], "S2b-tampered.files": F + 4, "S2b-tampered.findings": N + 3,
    "S34-realcontent": revs[3], "S34-realcontent.files": F + 8, "S34-realcontent.findings": N + 7,
    "S5-proseserial": revs[4], "S5-proseserial.files": F + 10, "S5-proseserial.findings": N + 8,
}
json.dump(m, open(s + "/manifest.json", "w"), indent=1)
print("manifest written")
PY

sha256sum "$S/gate-pristine.py" >> "$SEAT/receipts/00-gate-pristine-sha.txt"
echo "BUILD OK"
