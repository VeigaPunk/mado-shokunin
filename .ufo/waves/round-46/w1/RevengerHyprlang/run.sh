#!/bin/sh
# Rebuild the hyprlang 0.6.8 special-category probe and run every case.
set -e
g++ -std=c++23 -O1 -g -o probe probe.cpp -lhyprlang
mkdir -p out
for f in cases/*.conf; do
  b=$(basename "$f" .conf)
  ./probe "$f" > "out/$b.txt" 2>&1 || echo "EXIT|$?" >> "out/$b.txt"
done
./probe cases/z18.conf dyn > out/z18_dyn.txt 2>&1 || echo "EXIT|$?" >> out/z18_dyn.txt
./probe cases/c01_baseline.conf twice > out/c01_twice.txt 2>&1 || echo "EXIT|$?" >> out/c01_twice.txt
./probe cases/c28_unclosed_block.conf twice > out/c28_twice.txt 2>&1 || echo "EXIT|$?" >> out/c28_twice.txt
