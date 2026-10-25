#!/bin/bash
# run-checks.sh - re-derive every QUALITY 69-72 check in both directions from committed bytes.
# Usage: bash run-checks.sh [LANE]   (default: the lane root this file lives under)
# Writes nothing outside this seat directory; every git call is read-only and names -C.
set -u
LANE=${1:-$(cd "$(dirname "$0")/../../../../.." && pwd)}
S="$LANE/.ufo/waves/round-41/w1/ScrQualityCriteria"
cd "$LANE" || exit 2
echo "lane=$LANE"
echo "head=$(git rev-parse HEAD)"
echo

echo "### 69 FAIL side - the round-40 tip claim, as the spot-check records it"
python3 "$S/check69.py" --repo . --rev fb49621 \
  --report "$S/scratch/report-claim-r40.txt" \
  --receipts .ufo/waves/round-40/receipts --text; echo "exit=$?"
echo
echo "### 69 PASS side - the round-41 base measurement at the freeze"
python3 "$S/check69.py" --repo . --rev 60c3914 \
  --report "$S/scratch/report-claim-r41-base.txt" \
  --receipts .ufo/waves/round-41/receipts --text; echo "exit=$?"
echo

echo "### 70 FAIL side - round-40 tip fb49621: marker on disk, absent from the revision"
bash "$S/check70.sh" . fb49621 .ufo/waves/round-40; echo "exit=$?"
echo
echo "### 70 PASS side - the same wave at cd950ec, where the marker is committed"
bash "$S/check70.sh" . cd950ec .ufo/waves/round-40; echo "exit=$?"
echo

echo "### 71 FAIL side - round-40 results at fb49621"
python3 "$S/check71.py" --repo . --rev fb49621 \
  --results .ufo/waves/round-40/w1-results.json --round 40; echo "exit=$?"
echo
echo "### 71 PASS side - the same results with the two non-resolving rows dropped"
python3 "$S/check71.py" --repo . --rev fb49621 --results x --round 40 \
  --results-file "$S/scratch/results-r40-fixed.json"; echo "exit=$?"
echo

echo "### 72 FAIL side - the measured survivor (partial M38: read cap dropped, post-check kept)"
python3 "$S/check72.py" --repo . --rev fb49621 \
  --controls .ufo/waves/round-40/ctl/run-c1-v2-controls.py \
  --receipt "$S/scratch/ctl-c1-v2-with-survivor.txt" --files; echo "exit=$?"
echo
echo "### 72 PASS side A - committed c1 v2 controls + receipt"
python3 "$S/check72.py" --repo . --rev fb49621 \
  --controls .ufo/waves/round-40/ctl/run-c1-v2-controls.py \
  --receipt .ufo/waves/round-40/receipts/ctl-c1-v2.txt; echo "exit=$?"
echo
echo "### 72 PASS side B - committed c2 v2 controls + receipt (X15 declared via site)"
python3 "$S/check72.py" --repo . --rev fb49621 \
  --controls .ufo/waves/round-40/ctl/run-c2-v2-controls.py \
  --receipt .ufo/waves/round-40/receipts/ctl-c2-v2.txt; echo "exit=$?"
echo

echo "### ground bytes (read-only git)"
echo -n "receipts naming fb49621 under round-40: "
git grep -l fb49621 fb49621 -- .ufo/waves/round-40/receipts/ | wc -l
echo -n "round-40 w1.ready.dispatched at fb49621: "
git cat-file -e fb49621:.ufo/waves/round-40/w1.ready.dispatched 2>&1 | head -1
echo -n "round-40 w1.ready at fb49621: "
git cat-file -e fb49621:.ufo/waves/round-40/w1.ready && echo tracked
echo -n "round-49 report at fb49621: "
git cat-file -e fb49621:.ufo/waves/round-49/w1/ConnCrossClaim.md 2>&1 | head -1
echo -n "M38 control row: "; grep -h "^control=M38" .ufo/waves/round-40/receipts/ctl-c1-v2.txt
echo -n "M43 declaration: "; sed -n '163,164p' .ufo/waves/round-40/ctl/run-c1-v2-controls.py
echo -n "X15 declaration: "; sed -n '247p' .ufo/waves/round-40/ctl/run-c2-v2-controls.py

echo
echo "### 70 FIXTURE - a throwaway repo (mktemp), both directions"
D=$(mktemp -d)
git -C "$D" init -q
echo "toplevel=$(git -C "$D" rev-parse --show-toplevel) D=$D"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "FIXTURE-ABORT toplevel mismatch"; exit 2; }
mkdir -p "$D/.ufo/waves/round-99"
printf 'ready\n' > "$D/.ufo/waves/round-99/w1.ready"
printf 'dispatched\n' > "$D/.ufo/waves/round-99/w1.ready.dispatched"
git -C "$D" add -A
git -C "$D" -c user.name=fixture -c user.email=fixture@localhost commit -qm fixture
echo "-- both markers committed"
bash "$S/check70.sh" "$D" HEAD .ufo/waves/round-99; echo "exit=$?"
printf 'third\n' > "$D/.ufo/waves/round-99/w2.ready"
echo "-- a third marker on disk, untracked"
bash "$S/check70.sh" "$D" HEAD .ufo/waves/round-99; echo "exit=$?"
rm -rf "$D"
echo "fixture cleaned: $D absent=$([ -e "$D" ] && echo no || echo yes)"

echo
echo "### quote + locator verification (verify-quotes.py)"
python3 "$S/verify-quotes.py"; echo "exit=$?"
