#!/bin/sh
# Critic run (R56CritDoNothing). Scratch: /fast/scratch/hyaku/mado-r56/R56CritDoNothing. Base = freeze copy (BASE_DIR).
# Every command below was executed; output captured in receipts/critic-run.txt.
set -u
S=/fast/scratch/hyaku/mado-r56/R56CritDoNothing
W=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56CritDoNothing
D=$(cat "$S/BASE_DIR")
cd "$S" || exit 2
echo "## C3 checker on freeze copy (baseline, expect 70/319/65/0/0)"
python3 -I "$W/c3_check.py" --repo "$D" --rev HEAD --work "$S/w3"; echo "rc=$?"
echo "## C1 checker on freeze copy (entry absent, expect TARGET_MISSED)"
python3 -I "$W/c1_check.py" --repo "$D" --rev HEAD --work "$S/w1base" | cut -c1-200; echo "rc=$?"
echo "## C2 reference tool, full model (must reproduce 18 committed fixtures)"
python3 -I "$W/c2_harness.py" --base "$D" --tool "$W/c2_ref.py"
for a in source symlink disable; do
  echo "## C2 ablation: $a"
  python3 -I "$W/c2_harness.py" --base "$D" --tool "$W/c2_ref.py" --ablate "$a"
done
echo "## C2 contract stubs (ctl/) and replay control"
cp "$W/c2_replay.py" "$D/.ufo/waves/round-56/ctl/c2-replay.py"
python3 -I "$W/c2_harness.py" --base "$D" --tool "$D/.ufo/waves/round-56/ctl/c2-replay.py"
rm -f "$D/.ufo/waves/round-56/ctl/c2-replay.py"
for t in empty.py const-host.py lookup-committed.py; do
  python3 -I "$W/c2_harness.py" --base "$D" --tool "$D/.ufo/waves/round-56/ctl/$t"
done
echo "## C1/C3 cheap variants (each a fresh scratch commit; checkers from c1_check.py / c3_check.py)"
KEEP=1 python3 -I "$W/mk_variants.py" --scratch "$S" --out "$W/receipts"
