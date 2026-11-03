#!/usr/bin/env bash
# R66ScribeSources — re-runnable, read-only evidence producer.
# Writes only under its own scratch dir; mutates no lane/git/jj state.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
FLEET=/home/vgpnk/Projects/shokunin
SEAT=$LANE/.ufo/waves/round-66/w1/R66ScribeSources
S=/fast/scratch/hyaku/mado-r66/R66ScribeSources
mkdir -p "$S"
run() { echo "\$ $*"; "$@"; echo "rc=$?"; echo; }

echo "== 0. fetch-if-missing (each source is opened by URL, not from a retained copy) =="
[ -s "$S/bash-exit-status.html" ] || curl -sS --max-time 30 -o "$S/bash-exit-status.html" \
  https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html
[ -s "$S/bash-manual.html" ] || curl -sS --max-time 40 -o "$S/bash-manual.html" \
  https://www.gnu.org/software/bash/manual/bash.html
[ -s "$S/bash-5.3.tar.gz" ] || curl -sS --max-time 120 -o "$S/bash-5.3.tar.gz" \
  https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz
[ -s "$S/bash-5.3/doc/bashref.texi" ] || tar -xzf "$S/bash-5.3.tar.gz" -C "$S" bash-5.3/doc/bashref.texi
[ -s "$S/subprocess.rst" ] || curl -sS --max-time 30 -o "$S/subprocess.rst" \
  https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst
echo "fetched: $(ls -1 "$S"/*.html "$S"/*.tar.gz "$S"/*.rst 2>/dev/null | wc -l) files"; echo

echo "== 1. lane identity =="
run git -C "$LANE" rev-parse HEAD
echo "declared base: eafd500fa7be76dca59e729435e231a5032cc037"; echo

echo "== 2. allocated source: Bash 5.3 release (tarball -> doc/bashref.texi §3.7.5) =="
run sha256sum "$S/bash-5.3.tar.gz" "$S/bash-5.3/doc/bashref.texi"
run wc -c "$S/bash-5.3.tar.gz" "$S/bash-5.3/doc/bashref.texi"
echo "\$ grep -n '@node Exit Status\|@subsection Exit Status\|exit status of zero indicates\|returns a status of 127\|status of 2 to indicate' doc/bashref.texi"
grep -n "@node Exit Status\|@subsection Exit Status\|exit status of zero indicates\|returns a status of 127\|status of 2 to indicate" "$S/bash-5.3/doc/bashref.texi"
echo "rc=$?"; echo
echo "\$ sed -n '/@node Exit Status/,/^So while/p' doc/bashref.texi   (quote at :3905-3906)"
sed -n '/@node Exit Status/,/^So while/p' "$S/bash-5.3/doc/bashref.texi" | tail -3
echo "rc=$?"; echo

echo "== 2b. readable rendering of the same section (HTML node + single-page version line) =="
run sha256sum "$S/bash-exit-status.html" "$S/bash-manual.html"
echo "\$ grep -n 'So while an exit status\|fatal signal whose number\|returns a status of 127\|status of 2 to indicate incorrect usage' Exit-Status.html"
grep -n "So while an exit status\|fatal signal whose number\|returns a status of 127\|status of 2 to indicate incorrect usage" "$S/bash-exit-status.html"
echo "rc=$?"; echo
echo "\$ grep -o 'version 5.3, 18 May 2025' bash-manual.html"
grep -o "version 5.3, 18 May 2025" "$S/bash-manual.html"; echo "rc=$?"; echo
echo "\$ bash --version | head -1"
bash --version | head -1; echo "rc=$?"; echo

echo "== 3. screened-not-allocated candidate (scout CPython subprocess.rst) =="
run sha256sum "$S/subprocess.rst"
echo "\$ sed -n '240,243p' subprocess.rst"
sed -n '240,243p' "$S/subprocess.rst"; echo "rc=$?"; echo
echo "\$ python3 -c word count of the scout quote"
python3 -c "print(len('Exit status of the child process, an integer. If the process exited due to a signal, this will be the negative signal number.'.split()))"; echo "rc=$?"; echo
echo "\$ grep -c 'subprocess.rst' corpus/SOURCES.md (S108 already holds this URL)"
grep -c "subprocess.rst" "$LANE/corpus/SOURCES.md"; echo "rc=$?"; echo

echo "== 4. registry id frontier and shape =="
echo "\$ grep -o '^| S[0-9]{3}' corpus/SOURCES.md | sort -u | tail -3"
grep -o "^| S[0-9]\{3\}" "$LANE/corpus/SOURCES.md" | sort -u | tail -3; echo "rc=$?"
echo "\$ grep -c '^| S435 ' corpus/SOURCES.md"
grep -c "^| S435 " "$LANE/corpus/SOURCES.md"; echo "rc=$?"
echo "\$ grep -c 'bash-5.3.tar.gz\|Exit-Status.html' corpus/SOURCES.md (URLs must be unused)"
grep -c "bash-5.3.tar.gz\|Exit-Status.html" "$LANE/corpus/SOURCES.md"; echo "rc=$?"
echo "\$ sources-census.sh census --root <fleet> mado  (shape baseline before append)"
( cd "$FLEET" && scripts/sources-census.sh census --root "$FLEET" mado 2>&1 | sed -n '1,7p;8p' ); echo "rc=$?"; echo

echo "== 5. census validate on the live lane (start state; receipt outside scanned scope) =="
( cd "$FLEET" && scripts/sources-census.sh validate --root "$FLEET" mado > "$S/census-now.txt" 2>&1; echo "rc=$?" )
echo "\$ diff census-now.txt .ufo/waves/round-66/census-start-r66.txt"
diff "$S/census-now.txt" "$LANE/.ufo/waves/round-66/census-start-r66.txt"
echo "rc=$? (1 = header/trailer only; see diff body)"
echo "\$ grep -c 'W0[14]' census-now.txt"
grep -c "W0[14]" "$S/census-now.txt"; echo "rc=$?"
echo

echo "== 6. census A/B on mirror lanes: base registry vs base+S435 =="
# Mirror lane: corpus/SOURCES.md is a real copy; every other corpus entry and every
# top-level lane entry (dotfiles included) is a symlink into the live lane, so used-by
# paths resolve exactly as they do live. Nothing is written to the lane.
M=$S/mirror
rm -rf "$M"; mkdir -p "$M"
mk_lane() { # $1 = mirror lane dir
  local d=$1
  mkdir -p "$d/corpus/lessons"
  for e in "$LANE"/* "$LANE"/.[!.]*; do
    local b; b=$(basename "$e"); [ "$b" = corpus ] && continue
    ln -s "$e" "$d/$b"
  done
  for e in "$LANE"/corpus/*; do
    local b; b=$(basename "$e"); [ "$b" = SOURCES.md ] && continue
    if [ "$b" = lessons ]; then
      for f in "$e"/*; do ln -s "$f" "$d/corpus/lessons/$(basename "$f")"; done
    else ln -s "$e" "$d/corpus/$b"; fi
  done
  cp "$LANE/corpus/SOURCES.md" "$d/corpus/SOURCES.md"
}
mk_lane "$M/lane-base"; mk_lane "$M/lane-row"
python3 - "$M/lane-row/corpus/SOURCES.md" "$SEAT/SOURCES.append.md" <<'EOF'
import sys
reg, app = sys.argv[1], sys.argv[2]
row = [l for l in open(app) if l.startswith('| S435 ')][0].rstrip('\n')
lines = open(reg).read().split('\n')
at = max(i for i, l in enumerate(lines) if l.startswith('| S434 '))
lines.insert(at + 1, row)
open(reg, 'w').write('\n'.join(lines))
print(f'lane-row: S435 ({len(row.strip("|").split("|"))} cells) inserted after S434 (line {at + 1})')
EOF
printf '# placeholder for the census E11 check only\n' > "$M/lane-row/corpus/lessons/round-66.md"
( cd "$FLEET"
  scripts/sources-census.sh validate --root "$M" "$M/lane-base" > "$S/val-mirror-base.txt" 2>&1; echo "base_rc=$?"
  scripts/sources-census.sh validate --root "$M" "$M/lane-row"  > "$S/val-mirror-row.txt"  2>&1; echo "row_rc=$?"
  scripts/sources-census.sh census   --root "$M" "$M/lane-row" 2>&1 | sed -n '1,7p' )
sed 's/lane-base/LANE/' "$S/val-mirror-base.txt" > "$S/n-base.txt"
sed 's/lane-row/LANE/'  "$S/val-mirror-row.txt"  > "$S/n-row.txt"
echo "\$ diff n-base.txt n-row.txt"
diff "$S/n-base.txt" "$S/n-row.txt"
echo "rc=$? (only the terminal ok-line path should differ)"
echo "\$ grep -c 'W0' n-row.txt"
grep -c "W0" "$S/n-row.txt"; echo "warnings_rc=$?"
echo "\$ grep -c '	S435	' n-row.txt"
grep -c "	S435	" "$S/n-row.txt"; echo "s435_rc=$? (1 = no finding names the new row)"
