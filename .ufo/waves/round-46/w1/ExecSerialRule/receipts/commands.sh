#!/bin/sh
# Commands behind the ExecSerialRule seat receipts (round 46, closure D2).
# $SERIAL is read from the live compositor into a shell/Python variable and is
# NEVER echoed, logged or committed; no receipt in this directory holds it.
set -eu
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
REV=4d22eeb66c2835af8aaa3fac6ad838fa616aa663
BASE=b22ea56bff2faec39ce9ff75d2107eaf4612ecbe
SEAT=$LANE/.ufo/waves/round-46/w1/ExecSerialRule
R=/fast/scratch/hyaku/mado-r46/ExecSerialRule

SERIAL=$(hyprctl monitors all -j | python3 -c 'import json,sys
d=json.load(sys.stdin)
print(d[0].get("serial",""))')

# 1. the carriers (paths and line numbers only)
git -C "$LANE" grep -n -F "$SERIAL" "$REV" | sed -E 's/^[0-9a-f]{40}://' | cut -d: -f1,2 | sort

# 2. the frozen gate cannot see them (no overlap with its own findings)
python3 -I "$LANE/quality/check-session-material.py" --repo "$LANE" --rev "$REV" > "$R/base-gate.txt"

# 3. the extended gate: fail at the tip, pass on the projection
python3 -I "$SEAT/gate.py" --repo "$LANE" --rev "$REV" --serial-from-host \
    --rules R5_SERIAL_PROSE,R6_SERIAL_EXACT
python3 -I "$SEAT/gate.py" --repo "$LANE" --rev "$REV" --scope all --serial-from-host \
    --rules R5_SERIAL_PROSE,R6_SERIAL_EXACT
python3 -I "$SEAT/gate.py" --repo "$LANE" --rev "$BASE" --scope all --serial-from-host \
    --rules R5_SERIAL_PROSE,R6_SERIAL_EXACT

# 4. projection: clone at REV, replace the value with <serial-redacted> in the
#    carriers, commit with a scratch identity, re-run (exit 0, findings=0)
D=$(mktemp -d -p "$R" proj.XXXXXX)
git clone -q --shared --no-checkout "$LANE" "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
git -C "$D" checkout -q --detach "$REV"
python3 - "$D" "$SERIAL" "$SEAT/receipts/serial-carriers.txt" <<'PY'
import os, sys
root, serial, listfile = sys.argv[1], sys.argv[2], sys.argv[3]
for rel in (p.strip().split(":")[0] for p in open(listfile) if p.strip()):
    full = os.path.join(root, rel)
    text = open(full, encoding="utf-8").read()
    if serial in text:
        open(full, "w", encoding="utf-8").write(text.replace(serial, "<serial-redacted>"))
PY
git -C "$D" add -A
git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m projection
python3 -I "$SEAT/gate.py" --repo "$D" --rev HEAD --scope all --serial-from-host \
    --rules R5_SERIAL_PROSE,R6_SERIAL_EXACT

# 5. selftest
python3 -I "$SEAT/gate.py" --selftest
