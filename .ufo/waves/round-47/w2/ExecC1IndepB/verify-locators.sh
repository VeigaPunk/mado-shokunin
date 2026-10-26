#!/bin/bash
# verify-locators.sh - re-checks every quote and locator used in
# .ufo/waves/round-47/w2/ExecC1IndepB.md against the lane's own files.
# Run from /home/vgpnk/Projects/shokunin/mado-shokunin.
set -u
cd "$(dirname "$0")/../../../../.." || exit 1
D=.ufo/waves/round-47/l1-draft/mado-terminal.py
X=.ufo/waves/round-47/fetch/xdg-terminal-exec
C=quality/counters/c1-r47-terminal.py
fail=0
check() { # file line needle
    local f=$1 l=$2 n=$3 got
    got=$(sed -n "${l}p" "$f")
    if printf '%s' "$got" | grep -qF -- "$n"; then
        printf 'OK   %s:%s  %s\n' "$f" "$l" "$n"
    else
        printf 'FAIL %s:%s  %s   (line: %s)\n' "$f" "$l" "$n" "$got"
        fail=1
    fi
}
check "$D" 44 "split at the first ':' into id and action with bash \`read\`"
check "$D" 50 "directory entries in readdir"
check "$D" 65 "tokenized by the shell-quoting rules of x:561-692"
check "$D" 66 "its first word must be found by \`command -v\` (reject otherwise)"
check "$D" 67 "ends while the last executed step failed also rejects (POSIX while-loop status)"
check "$D" 71 "finds aliases (ids registered in step 4 and not yet tried)"
check "$D" 78 "values pass through bash \`printf %b\`"
check "$X" 407 "IFS=':' read -r _directive xte__entry_id xte__execarg_default"
check "$X" 436 "IFS=':' read -r xte__entry_id xte__action_id"
check "$X" 624 "return 1"
check "$X" 623 "Encountered unquoted character"
check "$X" 683 "Double quote was not closed"
check "$X" 729 "unknown % field in argument"
check "$X" 738 "XTE__EXEC_USEP=\$xte__exec_usep"
check "$X" 958 'de_tokenize_exec "$XTE__EXPANDED_STR"'
check "$X" 960 "de_strip_fields"
check "$X" 989 "[Desktop Entry]'*) [ -z"
check "$X" 997 'check_entry_key "$xte__line" "$xte__value"'
check "$X" 1014 "'['*) ["
check "$X" 1238 "IFS='=' read -r _opt XTE__APPIDVAL"
check "$X" 1299 "IFS='=' read -r _arg XTE__PRINT_CMD_DELIMITER"
check "$X" 1307 "IFS='=' read -r _arg XTE__PRINT_DELIMITER"
check "$C" 141 '"--ro-bind", self.bash, "/bin/sh"'
check "$C" 268 "f = dict(kv.split"
check "$D" 19 "MADO_TERM: selected="
check "$D" 46 "'+id' protects id from a later '-id'"
check "$D" 48 "duplicates included"
check "$D" 49 'find -L <dir>/. -type f'
check "$D" 59 "counts as Categories), value = text after the first"
check "$D" 68 "an entry that is read but lacks an Exec word"
check "$D" 70 "The first candidate left wins"
check "$D" 76 "folded, --print-content the entry's lines"
check "$D" 79 "line per word."
check "$X" 168 'XTE__APPLICATIONS_DIRS=${xte__dir%/}/applications/'
check "$X" 790 'XTE__FALLBACK_ENTRY_IDS=${xte__entry_id}'
check "$X" 1083 'eval "$xte__entry_id"'
check "$X" 1085 'unalias "$xte__entry_id"'
check "$C" 306 'Exec={n} %f %u'
printf 'VERIFY: %s\n' "$([ "$fail" = 0 ] && echo ALL_LOCATORS_HOLD || echo LOCATOR_DRIFT)"
exit "$fail"
