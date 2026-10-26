#!/usr/bin/env bash
# verify-quotes.sh — every quoted fragment in table.md, grepped at its own source.
set -u
D=.ufo/waves/round-43/w2/ScribeClosureTable
fail=0
chk() { # $1 = label, $2 = pattern (fixed), $3 = file
  if grep -qF -- "$2" "$3"; then printf 'OK   %-34s %s  <- %s\n' "$1" "$(printf '%s' "$2" | cut -c1-60)" "$3"
  else printf 'MISS %-34s %s  <- %s\n' "$1" "$(printf '%s' "$2" | cut -c1-60)" "$3"; fail=1; fi
}
T=.ufo/waves/round-43/w1/ScrConsiderthese/check78.sh
chk selftest-label 'SELFTEST: PASS (12 assertions)' $D/receipt-selftest.txt
chk tally-36-42 'TALLY rounds=7 launches=8 dead=1 complete=7 clean=3 dirty=4 relayed=7' $D/receipt-t1-36-42.txt
chk tally-32-37 'TALLY rounds=6 launches=8 dead=2 complete=6 clean=2 dirty=4 relayed=6' $D/receipt-t2-32-37.txt
chk unexplained 'UNEXPLAINED round=43 launches=1 != complete+dead=0' $D/receipt-unexplained-demo.txt
chk tool-comment 'round 28 carries attempt=1 seven times, corpus/lessons/round-40.md:150' $T
chk round40-locator-150 'the known round-31' corpus/lessons/round-40.md
chk round42-wave1 'wave 1 never' corpus/lessons/round-42-verifier-spotcheck.md
chk round42-zero-seats '0 seats spawned' corpus/lessons/round-42-verifier-spotcheck.md
chk complete42 'complete mado round=42; hyaku-inline attempt=1' /home/vgpnk/Projects/shokunin/.ufo/watchdog.log
chk round36-cite 'DistillerFindings.md' corpus/lessons/round-36-verifier-spotcheck.md
chk round38-cite '3 modified seat reports' corpus/lessons/round-38-verifier-spotcheck.md
printf 'QUOTES: %s\n' "$([ $fail -eq 0 ] && echo PASS || echo FAIL)"
exit $fail
