#!/usr/bin/env bash
# CritC2V2Forgery - rebuild every receipt in this seat from the frozen lane.
# Writes only under /fast/scratch/hyaku/mado-r44/CritC2V2Forgery and this seat directory.
set -euo pipefail
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/w2/CritC2V2Forgery
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
S=/fast/scratch/hyaku/mado-r44/CritC2V2Forgery
export TMPDIR=$S
mkdir -p "$S"
rm -rf "$S/clone"
git clone -q --shared --no-checkout "$LANE" "$S/clone"
test "$(git -C "$S/clone" rev-parse --show-toplevel)" = "$S/clone"

echo "== patch copies"
python3 -I "$SEAT/patch.py"
echo "== fixture commits"
python3 -I "$SEAT/build.py"
echo "== frozen counter on the data commit (baseline)"
python3 -I "$LANE/quality/counters/c2-r44-gkeep-size-request-v2.py" --repo "$S/clone" \
    --rev e46789213830597348fe96a351ae004d10587385 | tee "$SEAT/receipts-score-baseline-data.txt"
echo "== frozen counter on each forgery"
while read -r rev name; do
    python3 -I "$LANE/quality/counters/c2-r44-gkeep-size-request-v2.py" --repo "$S/clone" --rev "$rev" \
        > "$SEAT/receipts-score-${rev:0:8}.txt" 2>&1 || true
    printf '%s %s ' "$rev" "$name"
    grep -E '^PRED-C2-r44-v2: admitted' "$SEAT/receipts-score-${rev:0:8}.txt"
done < "$SEAT/fixtures/commits.txt"
echo "== false-line verification against the pins"
python3 -I "$SEAT/verify.py" | tee "$SEAT/receipts-verify-false-lines.txt"
echo "== proposed corrections"
mapfile -t REVS < <(cut -d' ' -f1 "$SEAT/fixtures/commits.txt")
ALL=(e46789213830597348fe96a351ae004d10587385 "${REVS[@]}")
for c in widthcap censusforms widthcap-censusforms; do
    out="$SEAT/receipts-$c-scores.txt"
    : > "$out"
    for r in "${ALL[@]}"; do
        printf '%s ' "$r" >> "$out"
        python3 -I "$SEAT/c2-r44-v2-$c.py" --repo "$S/clone" --rev "$r" 2>&1 \
            | grep -E '^PRED-C2-r44-v2: admitted|clause=h prose|clause=j surface=.*cited=0' >> "$out" || true
    done
    echo "-- $c"; cat "$out"
done
echo "REPRO: done"
