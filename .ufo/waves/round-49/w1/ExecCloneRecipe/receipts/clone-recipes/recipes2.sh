#!/bin/bash
# w1/ExecCloneRecipe - clone/read recipes under RLIMIT_FSIZE. bash `ulimit -f` counts 1024-byte units,
# so 1024 = 1 MiB, 2048 = 2 MiB, 65536 = 64 MiB. Every test records its own rc, the files left at the
# cap boundary and the largest file it produced.
set -u
ulimit -f 65536
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
S=/fast/scratch/hyaku/mado-r49/ExecCloneRecipe
R=$S/recipes2
rm -rf "$R"; mkdir -p "$R"
export HOME=$S/home XDG_CONFIG_HOME=$S/xdg XDG_CACHE_HOME=$S/xdg/cache TMPDIR=$S/tmp
mkdir -p "$HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME" "$TMPDIR"
REV=$(git -C "$LANE" rev-parse HEAD)
: > "$R/summary.txt"
{
  echo "lane=$LANE"; echo "lane_head=$REV"; echo "git=$(git --version)"; echo "bash=$(bash --version | head -1)"
  echo "calibration: 'ulimit -f 2048' then head -c 5000000 /dev/zero > probe ->"
  bash -c "ulimit -f 2048; head -c 5000000 /dev/zero > $R/cal.bin 2>/dev/null; echo rc=\$?" >> "$R/summary.txt"
  echo "cal.bin bytes=$(stat -c %s "$R/cal.bin")"
} >> "$R/summary.txt"

capcheck() { # dir cap -> listing of files exactly at the cap
  local capb=$(( $2 * 1024 ))
  find "$1" -type f -size ${capb}c -printf "%s %p\n" 2>/dev/null | head -5
}

report() { # name cap rc dir
  local name=$1 cap=$2 rc=$3 d=$4
  {
    echo "== $name cap_kib=$cap cap_bytes=$((cap*1024)) rc=$rc"
    echo "at_cap:"; capcheck "$d" "$cap"
    echo "files=$(find "$d" -type f 2>/dev/null | wc -l) bytes=$(du -sb "$d" 2>/dev/null | cut -f1)"
    echo "largest:"; find "$d" -type f -printf "%s %p\n" 2>/dev/null | sort -n | tail -2
    echo "index=$(stat -c %s "$d/.git/index" 2>/dev/null || echo absent)"
    echo
  } >> "$R/summary.txt"
}

# --- C: clone, full checkout, three caps ---------------------------------------------------
for cap in 1024 2048 65536; do
  d=$R/clone-full-$cap; mkdir -p "$d"
  ( ulimit -f $cap; timeout 600 git clone -q --shared "$LANE" "$d/c" ) > "$R/clone-full-$cap.log" 2>&1
  rc=$?
  report clone-full-$cap $cap $rc "$d/c"
  echo "  log_tail: $(tail -2 "$R/clone-full-$cap.log" | tr '\n' '|')" >> "$R/summary.txt"
done

# --- N: clone --no-checkout only -----------------------------------------------------------
for cap in 1024 2048; do
  d=$R/clone-nocheckout-$cap; mkdir -p "$d"
  ( ulimit -f $cap; timeout 600 git clone -q --shared --no-checkout "$LANE" "$d/c" ) > "$R/clone-nocheckout-$cap.log" 2>&1
  rc=$?
  report clone-nocheckout-$cap $cap $rc "$d/c"
  echo "  log_tail: $(tail -2 "$R/clone-nocheckout-$cap.log" | tr '\n' '|')" >> "$R/summary.txt"
done

# --- A: --no-checkout + archive|tar of the paths a seat needs, whole recipe under the cap ----
for cap in 1024 2048; do
  d=$R/archive-paths-$cap; mkdir -p "$d"
  ( ulimit -f $cap; cd "$d" && timeout 600 bash -c "git clone -q --shared --no-checkout '$LANE' c && cd c && git archive $REV -- tools quality/counters corpus/knowledge README.md | tar -x" ) > "$R/archive-paths-$cap.log" 2>&1
  rc=$?
  report archive-paths-$cap $cap $rc "$d/c"
  echo "  log_tail: $(tail -3 "$R/archive-paths-$cap.log" | tr '\n' '|')" >> "$R/summary.txt"
done

# --- AA: archive every path (dies on the >cap blobs) ---------------------------------------
for cap in 1024 2048 65536; do
  d=$R/archive-all-$cap; mkdir -p "$d"
  ( ulimit -f $cap; cd "$d" && timeout 600 bash -c "git clone -q --shared --no-checkout '$LANE' c && cd c && git archive $REV | tar -x" ) > "$R/archive-all-$cap.log" 2>&1
  rc=$?
  report archive-all-$cap $cap $rc "$d/c"
  echo "  log_tail: $(tail -3 "$R/archive-all-$cap.log" | tr '\n' '|')" >> "$R/summary.txt"
done

# --- SP: sparse checkout (cone) of the same paths ------------------------------------------
for cap in 1024 2048 65536; do
  d=$R/sparse-$cap; mkdir -p "$d"
  ( ulimit -f $cap; cd "$d" && timeout 600 bash -c "git clone -q --shared --no-checkout '$LANE' c && cd c && git sparse-checkout set tools quality corpus/knowledge && git checkout -q $REV" ) > "$R/sparse-$cap.log" 2>&1
  rc=$?
  report sparse-$cap $cap $rc "$d/c"
  echo "  log_tail: $(tail -3 "$R/sparse-$cap.log" | tr '\n' '|')" >> "$R/summary.txt"
done

# --- SP4: sparse checkout with index v4 (path-compressed index) -----------------------------
for cap in 1024 2048; do
  d=$R/sparse-v4-$cap; mkdir -p "$d"
  ( ulimit -f $cap; cd "$d" && timeout 600 bash -c "git clone -q --shared --no-checkout '$LANE' c && cd c && git sparse-checkout set tools quality corpus/knowledge && git -c index.version=4 checkout -q $REV && git -c index.version=4 update-index --index-version 4" ) > "$R/sparse-v4-$cap.log" 2>&1
  rc=$?
  report sparse-v4-$cap $cap $rc "$d/c"
  echo "  log_tail: $(tail -3 "$R/sparse-v4-$cap.log" | tr '\n' '|')" >> "$R/summary.txt"
done

# --- SH: git show one blob ------------------------------------------------------------------
BIG=.ufo/waves/round-20/w2/CorpusRuntime/full-sweep.jsonl
SMALL=tools/mado-terminal.py
for cap in 1024 2048 65536; do
  for kind in big small; do
    [ $kind = big ] && p=$BIG || p=$SMALL
    o=$R/show-$kind-$cap.out
    ( ulimit -f $cap; timeout 120 git --git-dir="$LANE/.git" show "$REV:$p" > "$o" 2> "$R/show-$kind-$cap.err" )
    rc=$?
    echo "== show-$kind-$cap cap_bytes=$((cap*1024)) rc=$rc bytes=$(stat -c %s "$o") err=$(stat -c %s "$R/show-$kind-$cap.err")" >> "$R/summary.txt"
    echo "   stderr: $(head -1 "$R/show-$kind-$cap.err")" >> "$R/summary.txt"
  done
done

# --- AR1: archive ONE big path through tar, under the cap ----------------------------------
for cap in 1024 2048; do
  d=$R/archive-bigpath-$cap; mkdir -p "$d"
  ( ulimit -f $cap; cd "$d" && timeout 600 bash -c "git clone -q --shared --no-checkout '$LANE' c && cd c && git archive $REV -- $BIG | tar -x" ) > "$R/archive-bigpath-$cap.log" 2>&1
  rc=$?
  report archive-bigpath-$cap $cap $rc "$d/c"
  echo "  log_tail: $(tail -3 "$R/archive-bigpath-$cap.log" | tr '\n' '|')" >> "$R/summary.txt"
done

echo DONE
