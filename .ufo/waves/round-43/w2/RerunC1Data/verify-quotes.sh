#!/bin/sh
# Every quote in the RerunC1Data report must occur in a seat evidence file.
set -u
W=$(cd "$(dirname "$0")" && pwd)
fail=0
chk() { # file, quote
  if grep -Fq -- "$2" "$W/$1"; then echo "OK   $1 :: $2"; else echo "FAIL $1 :: $2"; fail=1; fi
}
chk n1.err 'RecursionError: Stack overflow (used 8140 kB) while decoding a JSON array from a unicode string'
grep -Fq -- 'MADO_GEOMETRY: SETUP <reason>' /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r42-geometry.py && echo 'OK   counter docstring :: MADO_GEOMETRY: SETUP <reason>' || { echo 'FAIL counter docstring'; fail=1; }
chk run4-replay.txt 'PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET rev=1959770657f1f8665097c1aed4be6c1cbb07139f nonce=57661d91ef2f1d52'
chk run5-base.txt 'PRED-C1-r42: fixtures=0/37 tool=absent verdict=TARGET_MISSED rev=a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f'
chk u4.out 'MADO_GEOMETRY: rules=1 float_rules=0 other=0 unsupported=0'
echo "fail=$fail"
exit $fail
