#!/bin/bash
f="$1"; b=$(basename "$f" .py); R=/fast/scratch/hyaku/mado-r55/R55W2MutC1CounterA/run/$b; mkdir -p $R/st $R/h
cp "$f" $R/counter.py
cd $R
python3 -I $R/counter.py --selftest --repo /fast/scratch/hyaku/mado-r55/R55W2MutC1CounterA/repo.m50L --rev HEAD --work $R/st > $R/st.out 2> $R/st.err; echo "st_rc=$?" >> $R/st.out
python3 -I /fast/scratch/hyaku/mado-r55/R55W2MutC1CounterA/repo.m50L/quality/check-r55-controls.py --claim c1 --repo /fast/scratch/hyaku/mado-r55/R55W2MutC1CounterA/repo.m50L --rev HEAD --work $R/h --counter $R/counter.py > $R/h.out 2> $R/h.err; echo "h_rc=$?" >> $R/h.out
echo done $b
