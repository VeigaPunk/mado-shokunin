#!/bin/bash
# Full reproduction of the seat's float-format lab. Deterministic: fixed seeds, no host state.
set -u
cd /fast/scratch/hyaku/mado-r46/LabFloatFormat || exit 1
OUT=run.txt
exec > >(tee "$OUT") 2>&1

echo "== environment =="
g++ --version | head -1
clang++ --version | head -1
python3 -VV
echo "libstdc++: $(readlink -f /usr/lib/libstdc++.so.6)"
echo "== the symbol HyprCtl's {:.2f} resolves to, in the host binary and in libstdc++ =="
objdump -T /usr/bin/Hyprland | c++filt | grep 'to_chars(char\*, char\*, float, std::chars_format, int)'
nm -D --defined-only /usr/lib/libstdc++.so.6 | c++filt | grep 'to_chars(char\*, char\*, float, std::chars_format, int)'
echo "== builds =="
g++ -std=c++23 -O2 -o fmt-gcc fmt.cpp && echo "built fmt-gcc"
clang++ -std=c++23 -O2 -o fmt-clang fmt.cpp && echo "built fmt-clang"
for O in O0 O1 O3 Os; do g++ -std=c++23 -$O -o "fmt-$O" fmt.cpp && echo "built fmt-$O"; done
echo "== sweeps =="
./fmt-gcc three-decimals   > three-gcc.tsv
./fmt-clang three-decimals > three-clang.tsv
./fmt-gcc ties             > ties.tsv
./fmt-gcc boundaries       > bound-gcc.tsv
./fmt-clang boundaries     > bound-clang.tsv
./fmt-gcc random-bits 100000 46    > randbits-gcc.tsv
./fmt-clang random-bits 100000 46  > randbits-clang.tsv
./fmt-gcc random-range 100000 46   > randrange-gcc.tsv
./fmt-gcc random-bits 1000000 7    > randbits1m.tsv
./fmt-gcc random-range 1000000 2026 > randrange1m.tsv
for O in O0 O1 O3 Os; do ./fmt-$O three-decimals > "three-$O.tsv"; done
echo "== compiler/optimisation stability of the 3-decimal grid =="
for f in three-clang.tsv three-O0.tsv three-O1.tsv three-O3.tsv three-Os.tsv; do
  if cmp -s three-gcc.tsv "$f"; then echo "IDENTICAL three-gcc.tsv $f"; else echo "DIFFER three-gcc.tsv $f"; fi
done
for f in bound-clang.tsv; do
  if cmp -s bound-gcc.tsv "$f"; then echo "IDENTICAL bound-gcc.tsv $f"; else echo "DIFFER bound-gcc.tsv $f"; fi
done
if cmp -s randbits-gcc.tsv randbits-clang.tsv; then echo "IDENTICAL randbits-gcc.tsv randbits-clang.tsv"; else echo "DIFFER randbits"; fi
echo "== python %.2f vs std::format (float column) vs std::format (double column) =="
python3 -I compare.py three-gcc.tsv ties.tsv bound-gcc.tsv randbits-gcc.tsv randrange-gcc.tsv
python3 -I compare.py three-clang.tsv bound-clang.tsv randbits-clang.tsv
python3 -I compare.py randbits1m.tsv randrange1m.tsv
echo "== independent exact-decimal oracle (Decimal of the binary value, ROUND_HALF_EVEN) =="
python3 -I oracle.py three-gcc.tsv ties.tsv bound-gcc.tsv randrange1m.tsv randbits1m.tsv
echo "== end-to-end join through the frozen reference (dumps carry the std::format text) =="
awk -F'\t' '{print $1"\t"$2}' three-gcc.tsv   > three2.tsv
awk -F'\t' '{print $1"\t"$2}' bound-gcc.tsv   > bound2.tsv
awk -F'\t' '{print $1"\t"$2}' randrange-gcc.tsv > range2.tsv
awk -F'\t' '{print $1"\t"$2}' ties.tsv        > ties2.tsv
awk -F'\t' '{print $1"\t"$2}' randbits-gcc.tsv > bits2.tsv
awk -F'\t' '{print $1"\t"$2}' randrange1m.tsv > range1m2.tsv
awk -F'\t' '{print $1"\t"$2}' randbits1m.tsv  > bits1m2.tsv
python3 -I join.py /fast/scratch/hyaku/mado-r46/LabFloatFormat three2.tsv bound2.tsv range2.tsv ties2.tsv bits2.tsv
python3 -I join.py /fast/scratch/hyaku/mado-r46/LabFloatFormat range1m2.tsv bits1m2.tsv
echo "== hashes =="
sha256sum fmt.cpp compare.py join.py oracle.py three-gcc.tsv ties.tsv bound-gcc.tsv randbits-gcc.tsv randrange-gcc.tsv randbits1m.tsv randrange1m.tsv
echo "== done =="
