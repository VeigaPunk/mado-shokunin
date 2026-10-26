#!/bin/bash
# ExecSeparability evidence verifier.
#  1. every backticked counter line quoted in ExecSeparability.md is grepped in a receipt of this seat and its
#     locator (file:line) is computed by grep -n, never typed;
#  2. every receipt records the counter's own exit code;
#  3. the data commit touches no counter file;
#  4. the fixture patches/recipes the report cites exist.
set -u
cd "$(dirname "$0")" || exit 2
fail=0
echo "== quotes in ExecSeparability.md =="
REPORT=../ExecSeparability.md      # the report lives at w2/ExecSeparability.md; receipts at w2/ExecSeparability/
[ -f "$REPORT" ] || REPORT=ExecSeparability.md
quotes=$(grep -o '`PRED-C[12]-r44-v2[^`]*`' "$REPORT" | tr -d '`')
n=0
while IFS= read -r q; do
  [ -n "$q" ] || continue
  n=$((n+1))
  hit=$(grep -Fn -- "$q" receipts/*.txt | cut -d: -f1,2 | paste -sd' ' -)
  if [ -n "$hit" ]; then
    printf 'OK      %s\n        %s\n' "$hit" "$q"
  else
    printf 'MISSING %s\n' "$q"; fail=1
  fi
done <<< "$quotes"
echo "quotes checked: $n"
echo "== receipts carry the counter's exit code =="
for f in receipts/*.txt; do
  if grep -q '^EXIT=' "$f"; then echo "OK      $f $(grep '^EXIT=' "$f")"; else echo "MISSING exit code in $f"; fail=1; fi
done
echo "== data commit touches no counter =="
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
c=$(git -C "$LANE" diff --name-only 03fa5c618b089064a657b3d79d3d4272ae4b6894 e46789213830597348fe96a351ae004d10587385 -- quality/counters/ | wc -l)
echo "counters changed by the data commit: $c (expected 0)"; [ "$c" -eq 0 ] || fail=1
echo "== fixture evidence present =="
for x in A B E F G H I; do [ -s "fixtures/fixture-$x.patch" ] && echo "OK      fixtures/fixture-$x.patch" || { echo "missing patch $x"; fail=1; }; done
[ -s fixtures/fixture-C.txt ] && echo "OK      fixtures/fixture-C.txt" || { echo "missing C recipe"; fail=1; }
echo "VERDICT: $([ $fail -eq 0 ] && echo PASS || echo FAIL)"
exit $fail
