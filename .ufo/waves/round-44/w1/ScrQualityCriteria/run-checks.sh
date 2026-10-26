#!/usr/bin/env bash
# Re-derive every red/green pair the criteria.md draft cites. Run from the lane root:
#   bash .ufo/waves/round-44/w1/ScrQualityCriteria/run-checks.sh [WORKDIR]
# Reads committed bytes only (git cat-file/show/ls-tree/merge-base) and writes only WORKDIR.
# Synthetic controls are generated from committed bytes; nothing in the lane is written.
set -u
LANE=${PWD}
W=${1:-/fast/scratch/hyaku/mado-r44/ScrQualityCriteria/replay}
S=".ufo/waves/round-44/w1/ScrQualityCriteria"
mkdir -p "$W/green84" "$W/red84" "$W/ctl82" "$W/green85"
BASE=6a1a90528fe533cadee506a9fa3e9d13d15cc41f
DATA=1959770657f1f8665097c1aed4be6c1cbb07139f
TIP=58466627de847d6502283c3bb9e652caea97b411
FREEZE=e2289516a9a857f55cda7be635933e89b931c3da
SRC=.ufo/waves/round-44/fetch-c1/Hyprland-HyprCtl.cpp
REF=.ufo/waves/round-44/c1/ctl-ref-tool.py.txt

run() { echo; echo "\$ $*"; "$@"; echo "exit=$?"; }

echo "# re-derivation transcript: QUALITY criteria 82+ (round 44, seat ScrQualityCriteria)"
echo "# lane=$LANE revs base=$BASE data=$DATA tip=$TIP freeze=$FREEZE"
echo "# host $(uname -sr); python3 $(python3 -V 2>&1 | awk '{print $2}'); util-linux sha256sum"
echo
echo '$ sha256sum of the five checkers'
sha256sum "$S"/check8{2,3,4,5,6}.py "$S"/verify-quotes.py

# ---- check82: state-field audit ----------------------------------------------------------
git -C "$LANE" show "$BASE:tools/mado-geometry.py" > "$W/base-tool.py"
echo; echo "# --- check82: L1/L2/L3 on three tools; keys parsed from the pinned serializer"
run python3 -I "$S/check82.py" --source "$SRC" --tool "$REF" \
    --must fullscreen:Hyprland-HyprCtl.cpp:410 --audit
run python3 -I "$S/check82.py" --source "$SRC" --tool "$W/base-tool.py" \
    --must fullscreen:Hyprland-HyprCtl.cpp:410 --audit
python3 - "$W" <<'PY'
import sys
w = sys.argv[1]
lines = open('.ufo/waves/round-44/c1/ctl-ref-tool.py.txt').read().splitlines()
start = next(i for i, l in enumerate(lines) if l.startswith('def selftest'))
kept = lines[:start] + [l for l in lines[start:] if 'fullscreen' not in l.lower()]
open(w + '/ctl82/ref-no-case.py', 'w').write('\n'.join(kept) + '\n')
print('# control A: reference tool, every selftest line naming fullscreen removed '
      '(%d lines)' % (len(lines) - len(kept)))
PY
run python3 -I "$S/check82.py" --source "$SRC" --tool "$W/ctl82/ref-no-case.py" \
    --must fullscreen:Hyprland-HyprCtl.cpp:410
printf 'IGNORED-FIELD fullscreen: verdict vocabulary stays the round-43 one\n' > "$W/ctl82/declare.txt"
cp "$W/base-tool.py" "$W/ctl82/base-declared.py"
run python3 -I "$S/check82.py" --source "$SRC" --tool "$W/ctl82/base-declared.py" \
    --must fullscreen:Hyprland-HyprCtl.cpp:410 --declare "$W/ctl82/declare.txt"
run python3 -I "$S/check82.py" --source "$SRC" --tool "$REF" \
    --must fullscreen:Hyprland-HyprCtl.cpp:400

# ---- check83: citation resolves at the citing revision -----------------------------------
echo; echo "# --- check83: the round-43 entry at its data commit and at its tip"
run python3 -I "$S/check83.py" --repo . --rev "$DATA" \
    --doc corpus/knowledge/hyprland-gkeep-geometry-r43.md --prefix .ufo/
run python3 -I "$S/check83.py" --repo . --rev "$TIP" \
    --doc corpus/knowledge/hyprland-gkeep-geometry-r43.md --prefix .ufo/

# ---- check84: axis receipt at the closing revision ---------------------------------------
echo; echo "# --- check84: round-43 tip and round-44 freeze, then a synthetic tip receipt"
run python3 -I "$S/check84.py" --repo . --rev "$TIP" --receipts .ufo/waves/round-43/receipts
run python3 -I "$S/check84.py" --repo . --rev "$FREEZE" --receipts .ufo/waves/round-44/receipts
git -C "$LANE" show "$TIP:.ufo/waves/round-43/receipts/axis-base.txt" | sed -n '1,3p' > "$W/green84/axis-tip.txt"
echo 'MADO_AXIS: checked=3 mismatched=0 rev=58466627de847d6502283c3bb9e652caea97b411' >> "$W/green84/axis-tip.txt"
echo 'exit=0' >> "$W/green84/axis-tip.txt"
sed 's/mismatched=0/mismatched=1/; s/^exit=0$/exit=1/' "$W/green84/axis-tip.txt" > "$W/red84/axis-tip.txt"
run python3 -I "$S/check84.py" --repo . --rev "$TIP" --receipts "$W/green84" --disk
run python3 -I "$S/check84.py" --repo . --rev "$TIP" --receipts "$W/red84" --disk

# ---- check85: seat count = results file ---------------------------------------------------
echo; echo "# --- check85: round-43 plan vs results, round-44 bound form, synthetic equal form"
run python3 -I "$S/check85.py" --repo . --rev "$TIP" \
    --registration .ufo/waves/round-43/registration.md \
    --results w1=.ufo/waves/round-43/w1-results.json \
    --results w2=.ufo/waves/round-43/w2-results.json
run python3 -I "$S/check85.py" --repo . --rev "$FREEZE" \
    --registration .ufo/waves/round-44/registration.md
printf '# synthetic registration\nShape: two waves — `w1` (build, 38 seats) and `w2` (falsify, 32 seats); planned round total 70.\n' \
    > "$W/green85/registration.md"
python3 - "$W" <<'PY'
import sys
w = sys.argv[1]
for wave, n in (('w1', 38), ('w2', 32)):
    open('%s/green85/%s-results.json' % (w, wave), 'w').write(
        '{"seats":%d,"results":[%s]}\n' % (n, ','.join(['{}'] * n)))
print('# synthetic results files written: w1 38 rows, w2 32 rows')
PY
run python3 -I "$S/check85.py" --repo . --rev HEAD \
    --registration "$W/green85/registration.md" \
    --results w1="$W/green85/w1-results.json" --results w2="$W/green85/w2-results.json" --text

# ---- check86: locator source resolved in the repo ----------------------------------------
echo; echo "# --- check86: the round-43 oracle receipt's gkeep-shm.c locators, as committed and corrected"
git -C "$LANE" show "$TIP:.ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt" > "$W/obs-fixed.txt"
run python3 -I "$S/check86.py" --repo . --rev "$TIP" \
    --file .ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt --only gkeep-shm.c
sed -i 's/gkeep-shm\.c:156-164/gkeep-shm.c:150-159/' "$W/obs-fixed.txt"
run python3 -I "$S/check86.py" --repo . --rev "$TIP" --file-file "$W/obs-fixed.txt" \
    --text --only gkeep-shm.c

# ---- criterion 69 vs criterion 84: why a lane-only check is needed -----------------------
echo; echo "# --- criterion 69 on the round-43 report (fleet repo): lane-only is a setup error"
FLEET=/home/vgpnk/Projects/shokunin
if git -C "$FLEET" cat-file -e 906cfe70:.ufo/reports/round-43/mado.md 2>/dev/null; then
    git -C "$FLEET" show 906cfe70:.ufo/reports/round-43/mado.md > "$W/report-43.md"
    echo "# read-only input: \$ git -C $FLEET show 906cfe70:.ufo/reports/round-43/mado.md > $W/report-43.md"
    run python3 -I .ufo/waves/round-41/w1/ScrQualityCriteria/check69.py --repo . --rev "$TIP" \
        --report .ufo/reports/round-43/mado.md --receipts .ufo/waves/round-43/receipts
    run python3 -I .ufo/waves/round-41/w1/ScrQualityCriteria/check69.py --repo . --rev "$TIP" \
        --report "$W/report-43.md" --receipts .ufo/waves/round-43/receipts --text
else
    echo "SKIPPED: the round-43 report commit is not readable from $FLEET"
fi

# ---- axis receipts across rounds (informational: none names its carrier commit) ----------
echo; echo "# --- every committed MADO_AXIS receipt in rounds 35-44: carrying commit vs rev="
echo "# rule: carrier = \`git log -1 --format=%H -- <receipt>\` (the commit that last wrote it)"
python3 - <<'PY'
import re, subprocess
def git(*a):
    return subprocess.run(['git'] + list(a), capture_output=True, text=True).stdout
rounds = sorted({l.strip().split('/')[-1] for l in
                 git('ls-tree', '-d', '--name-only', 'HEAD', '.ufo/waves/').splitlines()
                 if re.match(r'\.ufo/waves/round-(3[5-9]|4[0-9])$', l.strip())})
rows = 0
for r in rounds:
    files = [f for f in git('ls-tree', '-r', '--name-only', 'HEAD', '--', '.ufo/waves/%s/receipts' % r).splitlines() if f]
    for f in files:
        for line in git('grep', '-h', 'MADO_AXIS: checked=', 'HEAD', '--', f).splitlines():
            m = re.search(r'rev=([0-9a-f]{7,40})', line)
            if not m:
                continue
            carrier = git('log', '-1', '--format=%H', '--', f).strip()
            rows += 1
            print('AXIS-RECEIPT %s carrier=%s rev=%s match=%d'
                  % (f, carrier[:7], m.group(1)[:7],
                     1 if (carrier and carrier.startswith(m.group(1))) else 0))
print('AXIS-RECEIPT rows=%d naming_carrier=0-or-see-above' % rows)
PY

# ---- the draft's own quotes --------------------------------------------------------------
echo; echo "# --- verify-quotes on criteria.md (prose quotes located, checker output via receipts)"
run python3 -I "$S/verify-quotes.py" --repo . --criteria "$S/criteria.md" --extra "$S/receipts.txt"
