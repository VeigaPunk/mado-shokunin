#!/bin/bash
# usage: run_one.sh NN  -- runs selftest + harness on mutants/mNN.py in private work dirs
S=/fast/scratch/hyaku/mado-r55/R55W2MutC1CounterB
N=$1
W=$S/work/m$N
mkdir -p $W/st $W/hz
cd $W
python3 -I $S/mutants/m$N.py --selftest --repo $S/repo --rev HEAD --work $W/st > $W/selftest.out 2> $W/selftest.err
echo "rc=$?" > $W/selftest.rc
python3 -I $S/repo/quality/check-r55-controls.py --claim c1 --repo $S/repo --rev HEAD --work $W/hz --counter $S/mutants/m$N.py > $W/harness.out 2> $W/harness.err
echo "rc=$?" > $W/harness.rc
