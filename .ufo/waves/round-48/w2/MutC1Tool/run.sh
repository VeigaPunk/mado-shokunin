#!/usr/bin/env bash
# MutC1Tool reproduction: the eight one-rule mutants of the round-48 C1 tool, scored by the frozen PRED-C1-r48
# counter (fixture sets and pin bytes taken verbatim from the lane; nothing in the lane is written).
# ~150 s per counter run on this host; the eight mutate-and-score lanes run concurrently.
set -eu
L=/home/vgpnk/Projects/shokunin/mado-shokunin
H=$L/.ufo/waves/round-48/l1-draft
SEAT=$L/.ufo/waves/round-48/w2/MutC1Tool
S=${SCRATCH:-/fast/scratch/hyaku/mado-r48/MutC1Tool-repro}
rm -rf "$S"; mkdir -p "$S/work" "$S/m"
trap 'rm -rf -- "$S"' EXIT
D=$(mktemp -d -p "$S/m"); git -C "$D" init -q
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ]
mkdir -p "$D/tools" "$D/quality/counters" "$D/.ufo/waves/round-47/fetch"
cp "$H/mado-terminal.py" "$D/tools/mado-terminal.py"
cp "$H/c1-r48-terminal-cache.py" "$H/c1-r48-fixtures.json" "$D/quality/counters/"
cp "$L/quality/counters/c1-r47-fixtures.json" "$D/quality/counters/"
cp "$L/.ufo/waves/round-47/fetch/xdg-terminal-exec" "$D/.ufo/waves/round-47/fetch/"
git -C "$D" add -A
git -C "$D" -c user.name=t -c user.email=t@t commit -qm base
mkdir -p "$S/work/base"
( ulimit -f 16384
  python3 -I "$D/quality/counters/c1-r48-terminal-cache.py" --repo "$D" --rev HEAD \
    --work "$S/work/base" --nonce 4848 > "$S/base.txt" 2>&1 ) &
for t in m1-skip-hash m2-trust-cache m3-never-warm m4-break-cmdv m5-line50 m6-ignore-cached-args \
         m7-lower-desktop m8-force-hit; do
  git clone -q --shared "$D" "$S/m/$t"
  ( cd "$S/m/$t" && git apply "$SEAT/diffs/$t.diff" )
  git -C "$S/m/$t" -c user.name=t -c user.email=t@t commit -qam "mutant $t"
  mkdir -p "$S/work/$t"
  # the instrument copies /usr/bin/gawk (1274872 B) into its sandbox; 1 MiB/file would abort it
  ( ulimit -f 16384
    python3 -I "$S/m/$t/quality/counters/c1-r48-terminal-cache.py" --repo "$S/m/$t" --rev HEAD \
      --work "$S/work/$t" --nonce 4848 > "$S/$t.txt" 2>&1 ) &
done
wait
grep -h 'verdict=' "$S"/m*.txt
