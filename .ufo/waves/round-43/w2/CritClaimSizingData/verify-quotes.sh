#!/bin/sh
# verify-quotes.sh - every quote used in findings.md must occur in a receipt in this seat dir.
# Each case: <receipt> <quote>  (grep -F, fixed string, exactly as it appears in the source line).
S="$(dirname "$0")"
fail=0
check() {
  if grep -qF -- "$2" "$S/$1"; then
    printf 'OK   %-28s %s\n' "$1" "$2"
  else
    printf 'MISS %-28s %s\n' "$1" "$2"; fail=1
  fi
}
check receipt-quotes.txt 'C1 lands `tools/mado-geometry.py` (operability, capability acquisition)'
check receipt-quotes.txt 'every published axis ties at its maximum at base'
check receipt-quotes.txt 'held-row edits this round are the used-by additions on S155 and S158'
check receipt-quotes.txt 'The seven Hyprland pins are byte-identical to the round-42 pins'
check receipt-quotes.txt 'at the tip: `receipts/c1-after-tip.txt`'
check receipt-quotes.txt 'at the tip: `receipts/c2-after-tip.txt`'
check receipt-quotes.txt 'names a committed receipt under that round'
check receipt-quotes.txt 'the rule, not the client, is the origin of 420x500'
check receipt-quotes.txt "the round's entry is expected to cite no held id"
check receipt-quotes.txt 'never installed, never run on the host as a tool of the lane'
check receipt-quotes.txt 'reference installed as `tools/mado-geometry.py`, falsified by three independent implementations'
check receipt-quotes.txt 'the entry and SKILL.md read `locators=15 miss=0`'
check receipt-tool-identity.txt 'e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99'
check receipt-check79.txt 'CHECK79: pointers=2 non_ok=2 verdict=FAIL'
check receipt-pointers.txt 'ExecOracleGkeep/20-observation.txt @1959770: ABSENT'
check receipt-counters.txt 'coverage=10.0000/10'
check receipt-cleared.txt 'C1 — operability (capability acquisition)'
check receipt-cleared.txt 'exit 0, at the data commit and at the tip'
check receipt-cleared.txt 'only after confirming it exists at the named commit'
check receipt-cleared.txt 'byte-identical to `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt`'
check receipt-cleared.txt '"size": [420, 500]'
check receipt-cleared.txt "sha and this seat's copy sha"
check receipt-cleared.txt '6,632 differential cases'
check receipt-pointers.txt 'measured at the data commit: `receipts/c2-after-data.txt`'
check receipt-counter-clauses.txt 'ids present at BASE keep cells 1-9 byte-equal'
check receipt-axis-universals.txt 'AXES = ("navigation", "calibration", "operability")'
check receipt-cleared.txt '`sha256sum tools/mado-geometry.py` at this seat gives'
[ "$fail" = 0 ] && echo 'VERIFY_QUOTES: all quotes located in a seat receipt' || echo 'VERIFY_QUOTES: FAIL'
exit "$fail"
