#!/bin/sh
# Verify every quote in receipts/quotes.tsv against its stated file:line.
# Fails if a quote is absent at that line, if the line number is wrong, or if the
# quote exceeds 25 words. Also proves the L1 docstring names no trace prefix.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
Q=$LANE/.ufo/waves/round-47/w2/ExecSkillSection/receipts/quotes.tsv
fail=0
n=0
while IFS='	' read -r path line quote; do
  case $path in '#'*|'') continue ;; esac
  n=$((n+1))
  f=$LANE/$path
  [ -f "$f" ] || { echo "FAIL missing file: $path"; fail=1; continue; }
  text=$(sed -n "${line}p" "$f")
  if printf '%s\n' "$text" | grep -F -q -- "$quote"; then ok="found"; else ok="MISSING"; fail=1; fi
  words=$(printf '%s\n' "$quote" | wc -w)
  [ "$words" -le 25 ] || { ok="$ok; WORDS=$words>25"; fail=1; }
  printf '%s:%s  %s  words=%s  %s\n' "$path" "$line" "$ok" "$words" "$quote"
done < "$Q"
echo "quotes checked: $n"

# the docstring spans lines 1-79 of the reference; it must not name the trace prefixes
doc=$(sed -n '1,79p' "$LANE/.ufo/waves/round-47/l1-draft/mado-terminal.py")
for tok in MADO_TERM_TRACE MADO_TERM_DESKTOPS; do
  if printf '%s\n' "$doc" | grep -q "$tok"; then
    echo "docstring names $tok: yes"
  else
    echo "docstring names $tok: NO (code only: $(grep -n "$tok" "$LANE/.ufo/waves/round-47/l1-draft/mado-terminal.py" | cut -d: -f1 | tr '\n' ' '))"
  fi
done
echo "verdict: $([ "$fail" -eq 0 ] && echo QUOTES_VERIFIED || echo QUOTE_CHECK_FAILED)"
exit "$fail"
