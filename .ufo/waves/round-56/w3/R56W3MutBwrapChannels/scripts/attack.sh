#!/bin/bash
# R56W3MutBwrapChannels -- driver.
#   $1 = cheat file name in cheats/ (or "baseline" for the honest tool)
# Commits the cheat as tools/mado-watchplan.py in the scratch repo, then runs the FROZEN
# harness in three modes and prints the decisive lines.
set -u
S=/fast/scratch/hyaku/mado-r56/R56W3MutBwrapChannels
D=$S/repo
R=$S/receipts
mkdir -p "$R"

name=$1
if [ "$name" = "baseline" ]; then
  cp "$D/tools/mado-watchplan.py" "$S/cheats/.honest.py"
  src=$S/cheats/.honest.py
else
  src=$S/cheats/$name.py
fi
[ -f "$src" ] || { echo "no such cheat: $src"; exit 2; }

# commit the tool copy on top of the tip base
cp "$src" "$D/tools/mado-watchplan.py"
chmod 755 "$D/tools/mado-watchplan.py"
git -C "$D" add -A
git -C "$D" -c user.name=ctl -c user.email=ctl@ctl commit -q -m "cheat: $name" || true
rev=$(git -C "$D" rev-parse HEAD)
echo "== $name rev=$rev sha256=$(sha256sum "$D/tools/mado-watchplan.py" | cut -d' ' -f1)"

for mode in bwrap nosb nosb-ns; do
  work=$S/work-$name-$mode
  rm -rf "$work"; mkdir -p "$work"
  cmd=(python3 -I "$D/quality/check-r56-controls.py" --claim c2 --repo "$D" --rev "$rev" --work "$work")
  [ "$mode" = "nosb-ns" ] && cmd+=(--no-sandbox)
  out=$R/$name-$mode.out; err=$R/$name-$mode.err
  if [ "$mode" = "bwrap" ]; then
    "${cmd[@]}" >"$out" 2>"$err"; rc=$?
  else
    unshare -rm --propagation private bash -c 'mount --bind /dev/null /usr/bin/bwrap || exit 90; exec "$@"' _ "${cmd[@]}" >"$out" 2>"$err"; rc=$?
  fi
  echo "--- $name [$mode] rc=$rc"
  echo "  stdout: $(cat "$out")"
  echo "  stderr: $(cat "$err")"
done
