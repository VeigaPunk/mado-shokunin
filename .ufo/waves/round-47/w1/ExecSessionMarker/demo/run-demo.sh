#!/usr/bin/env bash
# run-demo.sh — rebuild every measurement in .ufo/waves/round-47/w1/ExecSessionMarker.md
#
# Writes receipts into <seat>/receipts/, the install sets into <seat>/demo/.
# Everything happens in scratch clones of the lane; the lane itself is only
# read (git clone --shared). No host mutation, no compositor write. The live
# monitor dump is read once with `hyprctl monitors all -j` (an allowed read
# verb) and never printed; receipts hold the gate's counts only.
#
#   c1  the base revision + the installed gate            (markers, then plants)
#   c3  the base revision + gate + this seat's tree       (the install set)
#   c4  c3 + the two stale gate copies refreshed          (how the 6 close)
#
# Usage:  bash run-demo.sh [BASE_REV]
# Env:    LANE (default: the mado-shokunin checkout), MADO_R47_SCRATCH
set -u

LANE=${LANE:-/home/vgpnk/Projects/shokunin/mado-shokunin}
BASE=${1:-60edb66e2f1cb90acc6e9442fc93ded0ca42d750}
W1DIR=$LANE/.ufo/waves/round-47/w1
SEAT=${SEAT:-$W1DIR/ExecSessionMarker}
REPORT=${REPORT:-$W1DIR/ExecSessionMarker.md}
S=${MADO_R47_SCRATCH:-/fast/scratch/hyaku/mado-r47/ExecSessionMarker}
WORK=$S/demo
REAL_DUMP=$S/real-monitors.json
GATE=$SEAT/check-session-material.py
REC=$SEAT/receipts
TMPDIR=$S/tmp
export TMPDIR

mkdir -p "$S/tmp" "$REC" "$SEAT/demo"
rm -rf "$WORK"
mkdir -p "$WORK"

die() { echo "DEMO FAILED: $*" >&2; exit 1; }

assert_toplevel() {  # assert_toplevel <dir>
    top=$(git -C "$1" rev-parse --show-toplevel) || die "no toplevel in $1"
    [ "$(cd "$top" && pwd -P)" = "$(cd "$1" && pwd -P)" ] || die "toplevel $top != $1"
}

clone_at() {  # clone_at <dir> <rev>
    git clone -q --shared --no-checkout "$LANE" "$1" || die "clone $1"
    git -C "$1" checkout -q --detach "$2" || die "checkout $1"
    assert_toplevel "$1"
}

commit() {  # commit <repo> <message>
    git -C "$1" add -A
    git -C "$1" -c user.name=session-marker -c user.email=session-marker@scratch.invalid \
        commit -q -m "$2" || die "commit in $1"
}

run_gate() {  # run_gate <repo> <gate-path> <rev> <receipt> [extra args...]
    repo=$1; gatebin=$2; rev=$3; out=$4; shift 4
    python3 -I "$gatebin" --repo "$repo" --rev "$rev" "$@" > "$out" 2>&1
    rc=$?
    printf 'EXIT rc=%d cmd=%s --repo . --rev %s %s\n' "$rc" "$(basename "$gatebin")" "$rev" "$*" >> "$out"
    return $rc
}

export_sidecars() {  # export_sidecars <repo> <dest> <registry>
    repo=$1; dest=$2; reg=$3
    rm -rf "$dest"; mkdir -p "$dest"
    rows=0
    while read -r relpath _sha _rules _kind; do
        case "$relpath" in ''|'#'*) continue ;; esac
        mkdir -p "$dest/$(dirname "$relpath")"
        cp "$repo/$relpath.synthetic" "$dest/$relpath.synthetic" ||
            die "missing sidecar for $relpath"
        rows=$((rows + 1))
    done < "$reg"
    echo "sidecars: dest=${dest#$SEAT/} rows=$rows files=$(cd "$dest" && find . -name '*.synthetic' | wc -l)"
}

# ---------------------------------------------------------------- live dump
if [ ! -s "$REAL_DUMP" ]; then
    python3 - "$REAL_DUMP" <<'PY' || die "cannot read the live monitor dump"
import json, subprocess, sys
proc = subprocess.run(["hyprctl", "monitors", "all", "-j"], capture_output=True, text=True)
if proc.returncode != 0:
    raise SystemExit("hyprctl exited %d" % proc.returncode)
data = json.loads(proc.stdout)
with open(sys.argv[1], "w", encoding="utf-8") as handle:
    json.dump(data, handle, indent=1)
print("live dump: monitors=%d with_serial=%d" % (len(data), sum(1 for m in data if m.get("serial"))))
PY
fi

# ------------------------------------------------- clone 1: the as-is state
C1=$WORK/c1
clone_at "$C1" "$BASE"

# (0) baseline: the tracked gate at the base revision, untouched.
git -C "$C1" show "$BASE":quality/check-session-material.py > "$S/tracked-gate.py"
run_gate "$C1" "$S/tracked-gate.py" "$BASE" "$REC/01-baseline.txt"

# (1) install the marker gate itself.
cp "$GATE" "$C1/quality/check-session-material.py"
commit "$C1" "install the marker gate"
run_gate "$C1" "$C1/quality/check-session-material.py" HEAD "$REC/02-new-gate-no-markers.txt"

# (2) the gate decides which findings are synthetic; the registry follows.
python3 -I "$SEAT/demo/triage.py" --repo "$C1" --rev HEAD \
    --registry "$WORK/registry-c1.txt" \
    --triage "$SEAT/demo/triage-as-is.tsv" > "$REC/03-triage.txt" 2>&1
echo "EXIT rc=$?" >> "$REC/03-triage.txt"
run_gate "$C1" "$C1/quality/check-session-material.py" HEAD "$REC/04-with-markers.txt"

# (3) a real dump planted where no marker names it.
PLANT=.ufo/waves/round-47/w1/PlantedSeat/live-monitors.json
mkdir -p "$C1/$(dirname "$PLANT")"
cp "$REAL_DUMP" "$C1/$PLANT"
commit "$C1" "plant a real dump, unmarked"
run_gate "$C1" "$C1/quality/check-session-material.py" HEAD "$REC/05-planted-real-dump.txt"

# (4) the same real dump appended inside an already-waived fixture.
MARKED=$(awk '$4=="kind=fixture"{print $1; exit}' "$WORK/registry-c1.txt")
[ -n "${MARKED:-}" ] || die "no fixture row in the registry"
printf '%s\n' "$MARKED" > "$REC/06-marked-file.txt"
cat "$REAL_DUMP" >> "$C1/$MARKED"
commit "$C1" "append a real dump to a marked file"
run_gate "$C1" "$C1/quality/check-session-material.py" HEAD "$REC/06-real-dump-in-marked-file.txt"

# (5) the registry names a file that carries a real serial.
python3 -I "$SEAT/demo/mark.py" --repo "$C1" --path "$PLANT" \
    --kind fixture --rules R3_MONITOR_IDENT > "$REC/07a-marker-written.txt" 2>&1
commit "$C1" "register the file with the real serial"
run_gate "$C1" "$C1/quality/check-session-material.py" HEAD \
    "$REC/07-registry-names-real-serial.txt" --serial-from-host
printf 'MARKED_APPENDIX path=%s\n' "$PLANT" >> "$REC/07-registry-names-real-serial.txt"

# (6) the exact-value rule on the same tree.
run_gate "$C1" "$C1/quality/check-session-material.py" HEAD \
    "$REC/08-r6-exact-host-serial.txt" --serial-from-host

# ------------------------------- clone 3: the shape the lane will commit
C3=$WORK/c3
clone_at "$C3" "$BASE"
cp "$GATE" "$C3/quality/check-session-material.py"
mkdir -p "$C3/.ufo/waves/round-47/w1"
cp -a "$SEAT" "$C3/.ufo/waves/round-47/w1/ExecSessionMarker"
if [ -f "$REPORT" ]; then cp "$REPORT" "$C3/.ufo/waves/round-47/w1/ExecSessionMarker.md"; fi
commit "$C3" "install the gate and this seat's tree"
run_gate "$C3" "$C3/quality/check-session-material.py" HEAD "$REC/12a-seat-tree-no-markers.txt"
python3 -I "$SEAT/demo/triage.py" --repo "$C3" --rev HEAD \
    --registry "$SEAT/demo/registry-round47.txt" \
    --triage "$SEAT/demo/triage-round47.tsv" > "$REC/12-triage-seat-tree.txt" 2>&1
echo "EXIT rc=$?" >> "$REC/12-triage-seat-tree.txt"
run_gate "$C3" "$C3/quality/check-session-material.py" HEAD "$REC/13-seat-tree-with-markers.txt"
export_sidecars "$C3" "$SEAT/demo/sidecars" "$SEAT/demo/registry-round47.txt"

# --no-waivers must return the pre-marker findings, line for line.
run_gate "$C3" "$C3/quality/check-session-material.py" HEAD "$REC/14-no-waivers.txt" --no-waivers
{
    echo "compare: 12a (no markers) vs 14 (markers present, --no-waivers)"
    diff <(awk '/^(FINDING|SESSION_MATERIAL_RULES)/' "$REC/12a-seat-tree-no-markers.txt") \
         <(awk '/^(FINDING|SESSION_MATERIAL_RULES)/' "$REC/14-no-waivers.txt") \
        && echo "PARITY ok: identical FINDING and RULES lines"
} > "$REC/15-no-waivers-parity.txt" 2>&1
echo "EXIT rc=$?" >> "$REC/15-no-waivers-parity.txt"

# the wider scope, for the integrator: the three held corpus copies appear here.
run_gate "$C3" "$C3/quality/check-session-material.py" HEAD "$REC/16-scope-all.txt" --scope all

# --------------- clone 4: the same tree with the two stale gate copies refreshed
C4=$WORK/c4
git clone -q --shared "$C3" "$C4" || die "clone c4"
git -C "$C4" checkout -q --detach HEAD || die "checkout c4"
assert_toplevel "$C4"
cp "$GATE" "$C4/.ufo/waves/round-45/w1/ExecPrivacyGate/check-session-material.py"
cp "$GATE" "$C4/.ufo/waves/round-46/w1/ExecSessionTriage/check-session-material.py"
commit "$C4" "refresh the two stale gate copies"
python3 -I "$SEAT/demo/triage.py" --repo "$C4" --rev HEAD \
    --registry "$SEAT/demo/registry-round47-refreshed.txt" \
    --triage "$SEAT/demo/triage-refreshed.tsv" > "$REC/09-triage-refreshed-copies.txt" 2>&1
echo "EXIT rc=$?" >> "$REC/09-triage-refreshed-copies.txt"
run_gate "$C4" "$C4/quality/check-session-material.py" HEAD "$REC/10-refreshed-with-markers.txt"

# the two rows that close the stale copies need their own sidecars
rm -rf "$SEAT/demo/sidecars-refreshed"
mkdir -p "$SEAT/demo/sidecars-refreshed"
for relpath in .ufo/waves/round-45/w1/ExecPrivacyGate/check-session-material.py.synthetic \
               .ufo/waves/round-46/w1/ExecSessionTriage/check-session-material.py.synthetic; do
    mkdir -p "$SEAT/demo/sidecars-refreshed/$(dirname "$relpath")"
    cp "$C4/$relpath" "$SEAT/demo/sidecars-refreshed/$relpath" ||
        die "missing refreshed sidecar $relpath"
done
echo "sidecars-refreshed: files=$(cd "$SEAT/demo/sidecars-refreshed" && find . -name '*.synthetic' | wc -l)"

# ---------------------------------------- the report's numbers, against receipts
python3 -I "$SEAT/demo/verify-claims.py" --seat "$SEAT" > "$REC/17-claims-check.txt" 2>&1
echo "EXIT rc=$?" >> "$REC/17-claims-check.txt"

# ------------------------------------------------ the seat never holds a value
python3 - "$SEAT" "$REAL_DUMP" "$REPORT" > "$REC/11-seat-scan.txt" 2>&1 <<'PY'
import json, os, sys
seat, dump, report = sys.argv[1], sys.argv[2], sys.argv[3]
with open(dump, encoding="utf-8") as handle:
    data = json.load(handle)
values = set()
for monitor in data:
    for key in ("serial", "description", "make", "model"):
        value = monitor.get(key)
        if isinstance(value, str) and value.strip():
            values.add(value.strip())
values = {v for v in values if len(v) >= 4}
paths = []
for root, _dirs, files in os.walk(seat):
    paths.extend(os.path.join(root, name) for name in files)
if os.path.exists(report):
    paths.append(report)
hits = 0
for path in paths:
    with open(path, "rb") as handle:
        blob = handle.read()
    for value in values:
        if value.encode("utf-8") in blob:
            hits += 1
            print("HIT %s" % os.path.relpath(path, seat))
print("SEAT_SCAN files=%d values=%d hits=%d" % (len(paths), len(values), hits))
raise SystemExit(1 if hits else 0)
PY
echo "EXIT rc=$?" >> "$REC/11-seat-scan.txt"

echo "demo complete: receipts in $REC"
