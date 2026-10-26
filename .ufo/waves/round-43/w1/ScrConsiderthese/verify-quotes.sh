#!/usr/bin/env bash
# verify-quotes.sh — every quote this seat's proposal.md lifts from a source must be present on the
# line it names. Reads the proposal, checks each `quote|file|line` triple against that file's bytes.
# Usage: bash .ufo/waves/round-43/w1/ScrConsiderthese/verify-quotes.sh [--repo <lane>]
set -u
REPO=$(cd "$(dirname "$0")/../../../../.." && pwd)   # seat dir -> lane root (mado-shokunin)
[ "${1:-}" = "--repo" ] && REPO=$2
Q="$REPO/.ufo/waves/round-43/w1/ScrConsiderthese/quotes.txt"
n=0; bad=0
while IFS='|' read -r file line text; do
  case $file in ''|\#*) continue;; esac
  n=$((n+1))
  if [ ! -f "$REPO/$file" ]; then echo "QUOTE $n MISSING-FILE $file"; bad=$((bad+1)); continue; fi
  hay=$(sed -n "${line}p" "$REPO/$file" | tr '\n' ' ' | tr -s ' ')
  tset=$(printf '%s' "$text" | tr '\n' ' ' | tr -s ' ')
  case $hay in *"$tset"*) echo "QUOTE $n OK $file:$line \"$text\"";;
    *) echo "QUOTE $n FAIL $file:$line \"$text\""; bad=$((bad+1));; esac
done < "$Q"
# every quote listed must also appear in the proposal's own text
p="$REPO/.ufo/waves/round-43/w1/ScrConsiderthese/proposal.md"
flat=$(tr '\n' ' ' < "$p" | tr -s ' ')
while IFS='|' read -r file line text; do
  case $file in ''|\#*) continue;; esac
  tset=$(printf '%s' "$text" | tr '\n' ' ' | tr -s ' ')
  case $flat in *"$tset"*) :;; *) echo "PROPOSAL MISSING QUOTE: \"$text\""; bad=$((bad+1));; esac
done < "$Q"
echo "QUOTES checked=$n failed=$bad"
[ "$n" -gt 0 ] || { echo 'VERDICT: QUOTES_FAILED (no quotes read: the table path is wrong)'; exit 1; }
[ "$bad" -eq 0 ] && { echo 'VERDICT: QUOTES_OK'; exit 0; } || { echo 'VERDICT: QUOTES_FAILED'; exit 1; }
