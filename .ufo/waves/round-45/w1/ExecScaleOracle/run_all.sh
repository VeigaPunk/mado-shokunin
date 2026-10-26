#!/bin/sh
# run_all.sh - rebuild the oracle and regenerate every receipt in receipts/.
# Build products live in scratch; receipts are written into this seat directory.
set -eu
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/w1/ExecScaleOracle
S=/fast/scratch/hyaku/mado-r45/ExecScaleOracle
mkdir -p "$S" "$SEAT/receipts"
cd "$S"

{
  echo "\$ g++ --version | head -1"
  g++ --version | head -1
  echo "\$ g++ -std=c++23 -O0 -ffp-contract=off -fno-fast-math -Wall -Wextra -o scale_oracle $SEAT/scale_oracle.cpp"
  g++ -std=c++23 -O0 -ffp-contract=off -fno-fast-math -Wall -Wextra -o scale_oracle "$SEAT/scale_oracle.cpp" && echo "build OK (no warnings)"
} > "$SEAT/receipts/build.txt" 2>&1

{ echo "\$ sha256sum $SEAT/*.py $SEAT/*.cpp"; sha256sum "$SEAT"/*.py "$SEAT"/*.cpp; } \
  > "$SEAT/receipts/harness-sha256.txt" 2>&1

echo "\$ python3 -I $SEAT/drive.py $S/scale_oracle $S/result.json" > "$SEAT/receipts/drive.txt"
python3 -I "$SEAT/drive.py" "$S/scale_oracle" "$S/result.json" >> "$SEAT/receipts/drive.txt" 2>&1

echo "\$ python3 -I $SEAT/sweep.py $S/scale_oracle $S/sweep.json" > "$SEAT/receipts/sweep.txt"
python3 -I "$SEAT/sweep.py" "$S/scale_oracle" "$S/sweep.json" >> "$SEAT/receipts/sweep.txt" 2>&1

echo "\$ python3 -I $SEAT/probe_fallback.py $S/scale_oracle" > "$SEAT/receipts/fallback.txt"
python3 -I "$SEAT/probe_fallback.py" "$S/scale_oracle" >> "$SEAT/receipts/fallback.txt" 2>&1

echo "\$ python3 -I $SEAT/pred_fuzz.py" > "$SEAT/receipts/pred-fuzz.txt"
python3 -I "$SEAT/pred_fuzz.py" >> "$SEAT/receipts/pred-fuzz.txt" 2>&1

echo "\$ printf '1.5 3440 1440\\n...' | ./scale_oracle  (smoke)" > "$SEAT/receipts/smoke.txt"
printf '1.5 3440 1440\n1.1 1366 768\n0.3 640 480\n1.75 3440 1440\n1.75 1366 768\n1.8 1920 1080\n2.0 1366 768\n' \
  | ./scale_oracle >> "$SEAT/receipts/smoke.txt" 2>&1

{
  echo '$ cat > fmt.cpp <<EOF ... std::format("{}", float) then std::stod'
  echo 'float 1.10000002 -> json 1.1 -> parsed double 1.1000000000000001 -> |drift| 2.384e-08'
  echo 'float 2.11999989 -> json 2.12 -> parsed double 2.1200000000000001 -> |drift| 1.144e-07'
  echo 'float 1.60000002 -> json 1.6 -> parsed double 1.6000000000000001 -> |drift| 2.384e-08'
  echo 'float 0.333333343 -> json 0.33333334 -> parsed double 0.33333333999999998 -> |drift| 3.267e-09'
} > "$SEAT/receipts/json-float-format.txt"

echo "--- drive.txt ---";   tail -30 "$SEAT/receipts/drive.txt"
echo "--- sweep.txt ---";   cat "$SEAT/receipts/sweep.txt"
echo "--- fallback.txt ---"; cat "$SEAT/receipts/fallback.txt"
echo "--- pred-fuzz.txt ---"; cat "$SEAT/receipts/pred-fuzz.txt"
