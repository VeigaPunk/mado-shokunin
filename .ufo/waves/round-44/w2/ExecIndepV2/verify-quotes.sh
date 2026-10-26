#!/usr/bin/env bash
# Verify every quote in .ufo/waves/round-44/w2/ExecIndepV2.md that the seat lifted from a source:
# each fragment must be present verbatim (grep -F) on the cited line of the cited file.
set -u
cd /home/vgpnk/Projects/shokunin/mado-shokunin || exit 1
C1V2=quality/counters/c1-r44-geometry-states-v2.py
C1R42=quality/counters/c1-r42-geometry.py
fail=0
check () { # label file expected-line fragment
  local label=$1 file=$2 want=$3 frag=$4 got
  got=$(grep -n -F -- "$frag" "$file" | cut -d: -f1 | tr '\n' ',' | sed 's/,$//')
  if [ "$got" = "$want" ]; then
    printf 'OK   %-6s %s:%s  %s\n' "$label" "$file" "$got" "$frag"
  else
    printf 'FAIL %-6s %s want=%s got=%s  %s\n' "$label" "$file" "$want" "$got" "$frag"
    fail=1
  fi
}
check A1a "$C1V2" 17 'the summary line carries ` maximized=<n> fullscreen=<n>` between `badsize=<n>` and'
check A1b "$C1V2" 18 'exactly when maximized + fullscreen > 0, else it is byte-identical to the round-43 line'
check A6  "$C1V2" 17 'the summary line carries ` maximized=<n> fullscreen=<n>` between `badsize=<n>` and'
check A6b "$C1V2" 18 '` verdict=` exactly when maximized + fullscreen > 0, else it is byte-identical to the round-43 line'
check A7a "$C1V2" 16 'the client line is unchanged except'
check A7b "$C1V2" 17 'for the two new words; the summary line carries'
check A2a "$C1V2" 19 'verdict is tested in the order NO_SIZE_RULES (rules=0; exit 4) | DIFFER (differ>0; exit 1) | NO_MATCHING_CLIENT'
check A2b "$C1V2" 20 'NOT_COMPARED (agree=0 and maximized + fullscreen > 0; exit 5) | OK (exit 0)'
check A3a "$C1V2" 31 'the comparison sites of every function'
check A3b "$C1V2" 32 'whose body holds a string constant containing `fullscreen` (any case) number >= 6'
check A5  "$C1V2" 28 'and sometimes a `fullscreenClient` value'
check A8a "$C1V2" 30 '`--selftest` exits 0 printing `MADO_GEOMETRY_SELFTEST: k/n passed`, k == n, n >= 80'
check A8b "$C1V2" 36 'the selftest asserts state verdicts through the JSON path'
check A9  "$C1V2" 39 'and stdout and exit code must equal the sandboxed run'
check A10a "$C1V2" 14 'else 0 (absent, null, 0,'
check A10b "$C1V2" 15 '3, -1, true, 2.0, "2", lists and objects are 0)'
check A4  "$C1R42" 55 'V = NO_SIZE_RULES (rules=0; exit 4)'
exit "$fail"
