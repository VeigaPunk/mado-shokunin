#!/bin/sh
# run-selftest.sh — reproduce the harness's own discrimination and safety self-test.
#
# Three throwaway stub counters are driven through the harness:
#   stub-correct.py             -> harness verdict=PASS  (green pass, red fail naming both defects)
#   stub-always-accept.py       -> harness verdict=FAIL  (red case must not be accepted)
#   stub-writes-source-tree.py  -> harness verdict=FAIL  (lane_unchanged must be False)
#
# The third case runs against a throwaway repository created under the scratch tree, never
# against the lane.  Everything is written under $WORK (default
# /fast/scratch/hyaku/mado-r52/C1Fixture/selftest); evidence copies land in the seat's
# receipts/selftest/ directory.

set -eu

SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/C1Fixture
HARNESS="$SEAT/harness/c1-fixture-harness.py"
PROFILE="$SEAT/harness/profiles/default.json"
CONTROL=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/controls/c1-do-nothing.md
REV=85d57a818c3707397e21c840b6498b105ba798aa
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
WORK=${WORK:-/fast/scratch/hyaku/mado-r52/C1Fixture/selftest}
OUT="$SEAT/receipts/selftest"

mkdir -p "$WORK" "$OUT"

# A throwaway stand-in repository: the write-detection case must never touch the lane.
THROWAWAY="$WORK/throwaway-repo"
rm -rf "$THROWAWAY"
mkdir -p "$THROWAWAY/quality"
printf '# throwaway ledger\n\n| `tools/x.py` | does x. | `README.md` |\n' \
    > "$THROWAWAY/quality/tool-ledger.md"
printf '# throwaway\n' > "$THROWAWAY/README.md"
(
    cd "$THROWAWAY"
    git init -q .
    git add -A
    git -c user.name=C1Fixture -c user.email=c1fixture@invalid \
        -c commit.gpgsign=false commit -q -m "throwaway base"
)
THROW_REV=$(git -C "$THROWAWAY" rev-parse HEAD)

run() {
    name=$1
    repo=$2
    rev=$3
    counter=$4
    want=$5
    want_lane=$6
    rm -rf "$WORK/$name"
    mkdir -p "$WORK/$name" "$OUT/$name"
    set +e
    python3 -I "$HARNESS" \
        --repo "$repo" \
        --rev "$rev" \
        --counter "$counter" \
        --control "$CONTROL" \
        --profile "$PROFILE" \
        --work "$WORK/$name" \
        --out "$OUT/$name" > "$OUT/$name/console.txt" 2>&1
    rc=$?
    set -e
    got=$(grep -o 'HARNESS: verdict=[A-Z]*' "$OUT/$name/console.txt" | tail -1 | cut -d= -f2)
    lane=$(grep -o 'lane_unchanged=[A-Za-z]*' "$OUT/$name/console.txt" | tail -1 | cut -d= -f2)
    printf '%s: harness_rc=%s verdict=%s (want %s) lane_unchanged=%s (want %s)\n' \
        "$name" "$rc" "$got" "$want" "$lane" "$want_lane"
    if [ "$got" != "$want" ] || [ "$lane" != "$want_lane" ]; then
        printf '%s: MISMATCH\n' "$name"
        return 1
    fi
    return 0
}

run correct "$LANE" "$REV" "$SEAT/harness/selftest/stub-correct.py" PASS True
run always_accept "$LANE" "$REV" "$SEAT/harness/selftest/stub-always-accept.py" FAIL True
run writes_source_tree "$THROWAWAY" "$THROW_REV" \
    "$SEAT/harness/selftest/stub-writes-source-tree.py" FAIL False

# The scratch argument must reach the counter: the probe writes into the --work
# directory it was handed, and the harness must list that file under scratch_files_after.
rm -rf "$WORK/writes_in_work"
mkdir -p "$WORK/writes_in_work" "$OUT/writes_in_work"
set +e
python3 -I "$HARNESS" \
    --repo "$LANE" --rev "$REV" \
    --counter "$SEAT/harness/selftest/stub-writes-in-work.py" \
    --control "$CONTROL" --profile "$PROFILE" \
    --work "$WORK/writes_in_work" --out "$OUT/writes_in_work" \
    --cases green > "$OUT/writes_in_work/console.txt" 2>&1
set -e
probe=$(python3 - "$OUT/writes_in_work/harness-summary.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
files = d["cases"][0]["scratch_files_after"]
print("yes" if any(f.endswith("WORK-PROBE.txt") for f in files) else "no")
PY
)
printf 'writes_in_work: probe_file_observed=%s (want yes)\n' "$probe"
if [ "$probe" != "yes" ]; then
    printf 'writes_in_work: MISMATCH\n'
    exit 1
fi

echo "selftest: ok"
