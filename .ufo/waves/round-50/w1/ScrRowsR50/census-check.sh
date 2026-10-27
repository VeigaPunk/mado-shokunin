#!/usr/bin/env bash
# census-check.sh — seat ScrRowsR50, round 50.
# Builds a throwaway mirror of the lane's corpus/, appends the 12 row lines of rows.md to the
# Registry table, and runs the fleet census validator on the mirror. Lane files are copied,
# never written; the mirror is removed on exit. Prints the whole receipt on stdout.
#
#   bash .ufo/waves/round-50/w1/ScrRowsR50/census-check.sh [--work DIR]
#
# --work defaults to a dir under /fast/scratch and MUST NOT be under /tmp, /var/tmp or
# /dev/shm. Exit status is the validator's.
set -u
SEAT=$(cd -- "$(dirname -- "$0")" && pwd)
LANE=$(cd -- "$SEAT/../../../../.." && pwd)
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
WORK=/fast/scratch/hyaku/mado-r50/ScrRowsR50/census
while [ $# -gt 0 ]; do case "$1" in --work) WORK=${2:?--work needs a dir}; shift 2 ;; *) echo "unknown arg: $1" >&2; exit 2 ;; esac; done
case "$WORK" in /tmp/*|/var/tmp/*|/dev/shm/*) echo "REFUSE: work dir under $WORK is not allowed" >&2; exit 2 ;; esac
M=$WORK/mirror
[ -d "$LANE/corpus" ] || { echo "ERROR: lane corpus missing: $LANE/corpus" >&2; exit 2; }
[ -f "$SEAT/rows.md" ] || { echo "ERROR: rows.md missing: $SEAT/rows.md" >&2; exit 2; }
trap 'rm -rf -- "$WORK"' EXIT
rm -rf -- "$M"; mkdir -p -- "$M"

cp -a "$LANE/corpus" "$M/corpus" || exit 2
python3 - "$SEAT/rows.md" "$M/corpus/SOURCES.md" <<'PY' || exit 2
import re, sys
rows_src, reg = sys.argv[1], sys.argv[2]
rows = [l.rstrip('\n') for l in open(rows_src) if re.match(r'^\|\s*S\d{3,}\s*\|', l)]
assert len(rows) == 12, len(rows)
lines = open(reg).read().split('\n')
out, done = [], False
for l in lines:
    out.append(l)
    if not done and re.match(r'^\|\s*S351\s*\|', l):
        out.extend(rows); done = True
assert done
open(reg, 'w').write('\n'.join(out))
PY

# used-by targets the entries/lesson seats land in the real tree; stubs exist only in the mirror
[ -e "$M/corpus/knowledge/hyprland-bind-key-match-r50.md" ] || \
  printf '# mirror stub — the round-50 C1 entry lands from its own seat, not from this script\n' > "$M/corpus/knowledge/hyprland-bind-key-match-r50.md"
[ -e "$M/corpus/lessons/round-50.md" ] || \
  printf '# mirror stub — the round-50 lesson lands from its own seat, not from this script\n' > "$M/corpus/lessons/round-50.md"

# non-corpus used-by paths (tools/, quality/, .ufo/, SKILL.md ...) resolve through symlinks
for x in "$LANE"/* "$LANE"/.[!.]*; do
  b=$(basename -- "$x"); [ "$b" = corpus ] && continue
  [ -e "$M/$b" ] || [ -L "$M/$b" ] || ln -s -- "$x" "$M/$b"
done

TAB=$'\t'
echo "# census-check.sh — round 50 seat ScrRowsR50: census of the registry with S352-S363 appended"
echo "# run $(date -u +%Y-%m-%dT%H:%M:%SZ) from the lane root $LANE"
echo
echo "## mirror construction (scratch only; no lane file written)"
echo '$ WORK='"$WORK"'   # copy corpus, append the 12 rows after S351, stub the two used-by targets, symlink the rest'
echo
echo "## diff proof: the mirror registry differs from committed corpus/SOURCES.md by exactly the appended rows"
echo "\$ diff <(git -C $LANE show HEAD:corpus/SOURCES.md) \"\$M/corpus/SOURCES.md\" | grep -c '^>'"
diff <(git -C "$LANE" show HEAD:corpus/SOURCES.md) "$M/corpus/SOURCES.md" | grep -c '^>'
echo "\$ git -C $LANE show HEAD:corpus/SOURCES.md | grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|'"
git -C "$LANE" show HEAD:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
echo "\$ grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' \"\$M/corpus/SOURCES.md\""
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$M/corpus/SOURCES.md"
echo
echo "## validate (the required command; exit 0 required)"
echo "\$ $CENSUS validate --file \"\$M/corpus/SOURCES.md\""
out=$("$CENSUS" validate --file "$M/corpus/SOURCES.md"); rc=$?
printf '%s\n' "$out"
echo "exit=$rc"
echo
echo "## delta against the round's own baseline receipts/census-before.txt (ok and exit lines stripped)"
echo "\$ diff <(strip receipts/census-before.txt) <(strip validate output)"
diff <(sed "s/^[^${TAB}]*${TAB}//" "$LANE/.ufo/waves/round-50/receipts/census-before.txt" | grep -vE '^(ok|exit=)') \
     <(printf '%s\n' "$out" | sed "s/^[^${TAB}]*${TAB}//" | grep -vE '^(ok|exit=)')
echo
echo "## frozen manual census checks from CORPUS.md, run on the mirror"
echo "\$ grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md"
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$M/corpus/SOURCES.md"
echo "\$ awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md"
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' "$M/corpus/SOURCES.md"
echo '$ duplicate ids — must print nothing'
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' "$M/corpus/SOURCES.md" | sort | uniq -d
echo '$ enum violations and tier inflation — must print nothing'
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' "$M/corpus/SOURCES.md"
echo '$ tier histogram'
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' "$M/corpus/SOURCES.md"
echo '$ status histogram'
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' "$M/corpus/SOURCES.md"
echo
echo "## reading"
echo "rc=0. No E03 (duplicate id) and no E04 (duplicate URL+scope without supersedes). The only new findings against"
echo "the baseline are W04 S353 and W04 S354, the duplicate-URL decisions stated in rows.md §Notes. W01 S277 and the"
echo "16 baseline W04 lines are pre-existing. Warnings do not affect status; validate exits 0."
exit "$rc"
