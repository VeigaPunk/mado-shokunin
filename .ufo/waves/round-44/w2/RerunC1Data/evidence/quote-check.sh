#!/bin/sh
# Verify every quotation and locator used in ../RerunC1Data.md against its source.
# Each check: grep -n the quoted text in the named source and assert the computed line number.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
EV="$LANE/.ufo/waves/round-44/w2/RerunC1Data/evidence"
REV=e46789213830597348fe96a351ae004d10587385
fail=0

chk() { # chk <label> <expected-locator> <computed-locator-output>
    if [ "$2" = "$3" ]; then
        echo "OK   $1 @ $2"
    else
        echo "FAIL $1 expected=$2 computed=$3"; fail=1
    fi
}

chk "receipt final line" "53" \
    "$(grep -n 'fixtures=26/26' "$LANE/.ufo/waves/round-44/receipts/c1-after-data.txt" | cut -d: -f1)"

chk "registration C1 counting command" "28" \
    "$(grep -n 'quality/counters/c1-r44-geometry-states-v2.py --repo . --rev <rev>' \
        "$LANE/.ufo/waves/round-44/registration-v2.md" | cut -d: -f1)"

chk "tool NOT_COMPARED rule (at data rev)" "73" \
    "$(git -C "$LANE" show "$REV:tools/mado-geometry.py" |
        grep -n 'NOT_COMPARED (exit 5, agree=0 and maximized + fullscreen > 0)' | cut -d: -f1)"

chk "v1 counter 'top verdict rules ... unchanged' (l.24)" "24" \
    "$(grep -n 'top verdict rules (NO_SIZE_RULES' \
        "$LANE/quality/counters/c1-r44-geometry-states.py" | cut -d: -f1)"

chk "v1 counter quote continuation (l.25)" "25" \
    "$(grep -n 'DIFFER, NO_MATCHING_CLIENT, OK and their exit codes) are unchanged' \
        "$LANE/quality/counters/c1-r44-geometry-states.py" | cut -d: -f1)"

chk "run4 final line (l.53)" "53" \
    "$(grep -n '^PRED-C1-r44-v2: fixtures=26/26' "$EV/run4-fixednonce.txt" | cut -d: -f1)"

chk "run4 clause summary (l.52)" "52" \
    "$(grep -n '^PRED-C1-r44-v2 clauses=' "$EV/run4-fixednonce.txt" | cut -d: -f1)"

chk "v1-run final line (l.47)" "47" \
    "$(grep -n '^PRED-C1-r44: fixtures=18/26' "$EV/v1-run.txt" | cut -d: -f1)"

chk "v1-run-fixednonce final line (l.47)" "47" \
    "$(grep -n '^PRED-C1-r44: fixtures=17/26' "$EV/v1-run-fixednonce.txt" | cut -d: -f1)"

for r in run1 run2 run3 run4-fixednonce; do
    chk "$r fixtures=26/26 TARGET_MET" "1" \
        "$(grep -c '^PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET' "$EV/$r.txt")"
    chk "$r clause r rc=0 37/37" "1" \
        "$(grep -c 'clause=r rc=0 PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET' "$EV/$r.txt")"
    chk "$r exit 0" "EXIT=0" "$(cat "$EV/$r.rc")"
done

chk "standalone r42 37/37 TARGET_MET" "1" \
    "$(grep -c '^PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET' "$EV/r42-run.txt")"
chk "standalone r42 exit 0" "EXIT=0" "$(cat "$EV/r42-run.rc")"
chk "v1 fresh exit 1" "EXIT=1" "$(cat "$EV/v1-run.rc")"
chk "v1 fixed exit 1" "EXIT=1" "$(cat "$EV/v1-run-fixednonce.rc")"

chk "probe: failing iff NOT_COMPARED, 0 mismatches" "1" \
    "$(grep -c 'cases=38 mismatches=0 (failing iff NOT_COMPARED)' "$EV/assert-noncomp.txt")"
chk "probe: 9 NOT_COMPARED cases == 9 failing v1 fixtures" "1" \
    "$(grep -c 'not_compared_cases=9' "$EV/assert-noncomp.txt")"

chk "9 failing fixtures, all rc=5 want=0 (fixed nonce)" "9" \
    "$(grep -c 'ok=0' "$EV/v1-run-fixednonce.txt")"
chk "no stdout-divergence failure in v1 fixed run" "0" \
    "$(grep -c 'stdout line' "$EV/v1-run-fixednonce.txt")"
chk "no stdout-divergence failure in v1 fresh run" "0" \
    "$(grep -c 'stdout line' "$EV/v1-run.txt")"

chk "registration target at data commit and tip" "31" \
    "$(grep -n 'exit 0, at the data commit and at the tip' \
        "$LANE/.ufo/waves/round-44/registration-v2.md" | cut -d: -f1)"

for r in tip-run tip-fixed; do
    chk "$r fixtures=26/26 TARGET_MET" "1" \
        "$(grep -c '^PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET rev=290cddea92a18e2202456db89cb2bb60d9aaacff' "$EV/$r.txt")"
    chk "$r exit 0" "EXIT=0" "$(cat "$EV/$r.rc")"
done

chk "tip tool sha256 == data tool sha256" "1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4" \
    "$(git -C "$LANE" show 290cddea92a18e2202456db89cb2bb60d9aaacff:tools/mado-geometry.py | sha256sum | cut -d' ' -f1)"

chk "r42 standalone final line (l.49)" "49" \
    "$(grep -n '^PRED-C1-r42: fixtures=37/37' "$EV/r42-run.txt" | cut -d: -f1)"

d=$(sed -E 's/nonce=[0-9a-f]+/nonce=X/g' "$LANE/.ufo/waves/round-44/receipts/c1-after-data.txt" \
      | diff - <(sed -E 's/nonce=[0-9a-f]+/nonce=X/g' "$EV/run4-fixednonce.txt"))
chk "receipt vs run4 = only the trailing exit=0 marker" "54d53
< exit=0" "$d"

echo
if [ "$fail" -eq 0 ]; then echo "QUOTE-CHECK: PASS (all locators and counts reproduced)"; else
    echo "QUOTE-CHECK: FAIL"; fi
exit "$fail"
