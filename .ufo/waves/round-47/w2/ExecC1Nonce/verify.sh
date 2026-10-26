#!/bin/bash
# ExecC1Nonce seat self-check: re-greps the receipt and the logs it summarises. Read-only.
# Usage: bash verify.sh   (from anywhere; paths are absolute)
set -uo pipefail
W=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w2/ExecC1Nonce
R="$W/receipt.txt"
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
BAD=0
ck() { if eval "$2"; then echo "PASS $1"; else echo "FAIL $1"; BAD=1; fi; }

ck "12 run logs present"            '[ "$(ls -1 "$W"/logs/*.txt | wc -l)" -eq 12 ]'
ck "no FAIL line in any log"        '! grep -q FAIL "$W"/logs/*.txt'
ck "every log carries a summary"    '[ "$(grep -lc "PRED-C1-r47: " "$W"/logs/*.txt | wc -l)" -eq 12 ]'
ck "every summary is TARGET_MET"    '! grep -h "PRED-C1-r47: " "$W"/logs/*.txt | grep -qv "verdict=TARGET_MET"'
ck "every summary is at the candidate rev" '! grep -h "PRED-C1-r47: " "$W"/logs/*.txt | grep -qv "rev=ddac61bcbd01d5e2de2dbdde914bf7289dcf1579"'
ck "every run trips=0"              '! grep -h "clause=r trips" "$W"/logs/*.txt | grep -qv "trips=0 "'
ck "every run selftest 43/43"       '! grep -h "clause=s " "$W"/logs/*.txt | grep -qv "MADO_TERMINAL_SELFTEST: 43/43 passed"'
ck "receipt lists all 12 summaries" '[ "$(grep -c "fail_lines=" "$R")" -eq 12 ]'
ck "receipt determinism note x2"    '[ "$(grep -c "IDENTICAL line-for-line" "$R")" -eq 2 ]'
ck "pin sha256 in receipt = pin"    'grep -q "pin sha256      -> $(sha256sum "$LANE"/.ufo/waves/round-47/fetch/xdg-terminal-exec | cut -d" " -f1)" "$R"'
ck "fixtures sha256 in receipt"     'grep -q "fixtures sha256 -> $(sha256sum "$LANE"/quality/counters/c1-r47-fixtures.json | cut -d" " -f1)" "$R"'
ck "l1-draft sha256 in receipt"     'grep -q "l1-draft sha256 -> $(sha256sum "$LANE"/.ufo/waves/round-47/l1-draft/mado-terminal.py | cut -d" " -f1)" "$R"'
# quoted material cited in the report (<= 25 words), located by computed grep -n, not typed
L=$(grep -n "args, timeout=30" "$LANE"/quality/counters/c1-r47-terminal.py | cut -d: -f1)
ck "quote 'timeout=30' is at the cited line ($L)" 'sed -n "${L}p" "$LANE/quality/counters/c1-r47-terminal.py" | grep -q "args, timeout=30"'
ck "report cites that line"         'grep -q "c1-r47-terminal.py:$L" "$W/../ExecC1Nonce.md"'
echo "----"
if [ "$BAD" -eq 0 ]; then echo "VERDICT: all seat checks pass"; else echo "VERDICT: seat self-check FAILED"; fi
exit "$BAD"
