#!/usr/bin/env bash
# verify-quotes.sh — checks every Gate line in gate-lines.md against its receipt file.
# For each line `id  url  accessed  receipt:line  quote` inside the first fenced block,
# the quote must be a literal substring of the receipt line at the stated line number.
set -u
cd -- "$(dirname -- "$0")" || exit 2
pass=0; fail=0
in_block=0
while IFS= read -r line; do
  case "$line" in
  '```') if [ "$in_block" = 0 ]; then in_block=1; else in_block=0; fi; continue ;;
  esac
  [ "$in_block" = 1 ] || continue
  [ -n "$line" ] || continue
  IFS=$'\t' read -r id url accessed locator quote <<< "$line"
  file=${locator%:*}; want=${locator##*:}
  [ -f "$file" ] || { printf 'FAIL %s receipt missing %s\n' "$id" "$file"; fail=$((fail+1)); continue; }
  [ -n "$quote" ] || { printf 'FAIL %s empty quote\n' "$id"; fail=$((fail+1)); continue; }
  got=$(sed -n "${want}p" "$file")
  if printf '%s\n' "$got" | grep -qF -- "$quote"; then
    printf 'PASS %s %s:%s\n' "$id" "$file" "$want"
    pass=$((pass+1))
  else
    printf 'FAIL %s %s:%s quote not on that line\n' "$id" "$file" "$want"
    fail=$((fail+1))
  fi
done < gate-lines.md
printf 'QUOTES: %d passed, %d failed\n' "$pass" "$fail"
[ "$fail" = 0 ]
