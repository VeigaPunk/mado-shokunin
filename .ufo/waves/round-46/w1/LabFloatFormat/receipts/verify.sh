#!/bin/bash
# Re-reads the seat's own transcript (receipts/run.txt) and prints the decisive lines.
# A line missing here is a claim not backed by the transcript.
set -u
D=$(cd "$(dirname "$0")" && pwd)
T="$D/run.txt"
echo "== transcript =="; sha256sum "$T"; wc -l "$T"
echo "== formatter identity =="
grep -E "\(GLIBCXX_3\.4\.29\) std::to_chars\(char\*, char\*, float, std::chars_format, int\)" "$T"
echo "== per-sweep counts =="
grep -E "^(three-decimals|ties|boundaries|random-bits|random-range)=" "$T"
echo "== python vs std::format =="
grep -E "python_vs_float=[0-9]+" "$T"
echo "== exact-decimal oracle =="
grep -E "ORACLE values" "$T"
echo "== end-to-end join through the frozen reference =="
grep -E "REFERENCE-JOIN" "$T"
echo "== compiler / optimisation stability =="
grep -E "^(IDENTICAL|DIFFER) " "$T"
echo "== verdict =="
if grep -qE "python_vs_float_mismatch=[1-9]|python_vs_float=[1-9]|differ=[1-9]|_vs_exact=[1-9]" "$T"; then
  echo "FALSIFIED (a nonzero mismatch is printed above)"
else
  echo "NOT FALSIFIED: every mismatch counter in the transcript is zero"
fi
