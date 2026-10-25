#!/bin/bash
# read-only differential: committed count.py vs count-min.py
R=/home/vgpnk/Projects/shokunin/mado-shokunin
A=$R/.ufo/waves/round-35/c1/count.py
B=$R/.ufo/waves/round-35/scratch/SimplifyCounter/count-min.py
F=$R/.ufo/waves/round-35/c1/frozen.json
cd $R || exit 9
n=0; same=0; diff=0
run() { # $1=label $2=root
  ao=$(python3 -I "$A" --root "$2" --frozen "$F" 2>&1); ae=$?
  bo=$(python3 -I "$B" --root "$2" --frozen "$F" 2>&1); be=$?
  n=$((n+1))
  if [ "$ao" = "$bo" ] && [ "$ae" = "$be" ]; then same=$((same+1)); v=SAME; else diff=$((diff+1)); v=DIFF; fi
  printf '%s\t%s\texitA=%s exitB=%s\t%s\n' "$n" "$1" "$ae" "$be" "$v"
  if [ "$v" = DIFF ]; then printf '  A=%s\n  B=%s\n' "$ao" "$bo"; fi
}
for d in .ufo/waves/round-35/controls/*/; do run "dir:$d" "$d"; done
for t in .ufo/waves/round-35/controls/*.txt; do run "txt:$t" "$t"; done
run "root:." "."
echo "TOTAL n=$n same=$same diff=$diff"
