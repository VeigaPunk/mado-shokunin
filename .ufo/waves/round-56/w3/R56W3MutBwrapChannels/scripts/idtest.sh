#!/bin/bash
# R56W3MutBwrapChannels -- identity test: is the stdout claim line the SAME for a
# sandboxed run and an unsandboxed (--no-sandbox) run of the same rev?
set -u
S=/fast/scratch/hyaku/mado-r56/R56W3MutBwrapChannels
D=$S/repo
R=$S/receipts
rev=$(git -C "$D" rev-parse HEAD)
echo "rev=$rev"

for mode in bwrap nosb nosb-ns; do
  work=$S/work-id-$mode
  rm -rf "$work"; mkdir -p "$work"
  cmd=(python3 -I "$D/quality/check-r56-controls.py" --claim c2 --repo "$D" --rev "$rev" --work "$work")
  [ "$mode" = "nosb-ns" ] && cmd+=(--no-sandbox)
  out=$R/id-$mode.out; err=$R/id-$mode.err
  if [ "$mode" = "bwrap" ]; then
    "${cmd[@]}" >"$out" 2>"$err"; rc=$?
  else
    unshare -rm --propagation private bash -c 'mount --bind /dev/null /usr/bin/bwrap || exit 90; exec "$@"' _ "${cmd[@]}" >"$out" 2>"$err"; rc=$?
  fi
  echo "[$mode] rc=$rc"
  echo "[$mode] stdout: $(cat "$out")"
  echo "[$mode] stderr: $(cat "$err")"
done

echo "=== stdout diff bwrap vs nosb-ns (rev normalised) ==="
if diff <(sed 's/rev=[0-9a-f]*/rev=X/' "$R/id-bwrap.out") <(sed 's/rev=[0-9a-f]*/rev=X/' "$R/id-nosb-ns.out") >/dev/null; then
  echo "STDOUT IDENTICAL (modulo rev)"
else
  echo "stdout differs:"; diff <(sed 's/rev=[0-9a-f]*/rev=X/' "$R/id-bwrap.out") <(sed 's/rev=[0-9a-f]*/rev=X/' "$R/id-nosb-ns.out")
fi
echo "=== stdout bytes: bwrap=$(wc -c < "$R/id-bwrap.out") nosb=$(wc -c < "$R/id-nosb.out") nosb-ns=$(wc -c < "$R/id-nosb-ns.out") ==="
