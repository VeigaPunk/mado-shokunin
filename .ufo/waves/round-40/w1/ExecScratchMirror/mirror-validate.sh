#!/usr/bin/env bash
# mirror-validate.sh — scratch mirror + census gate for a SOURCES.md registry append.
#
# Validates a registry append BEFORE it is applied to the lane's corpus/SOURCES.md: the whole
# append happens in a throwaway tree V=$(mktemp -d) (never inside the lane), the fleet census
# is pointed at the mirror's SOURCES.md, and its verdict becomes this script's exit code.
#
# Usage
#   mirror-validate.sh BLOCK [KNOWLEDGE ...]
#   mirror-validate.sh --block FILE [--knowledge PATH]... [--lane DIR] [--census PATH]
#                      [--today YYYY-MM-DD] [--keep] [--no-closure] [--quiet]
#
#   BLOCK      append-block file: one Markdown registry row per line, no heading, no prose
#   KNOWLEDGE  repo-relative path of a file the appended rows cite; copied from <lane>/<path>
#              to <V>/<path> so the census's E11 used-by check can resolve it
#
# Steps (each one closes a gap the gate would otherwise mis-report):
#   1. copy <lane>/corpus/{SOURCES.md,README.md,knowledge/,lessons/} -> $V/corpus
#   2. insert BLOCK into the ## Registry table, immediately before the blank line ending it
#   3. copy each KNOWLEDGE at its repo-relative path into $V
#   4. closure: copy the used-by targets of the mirror's own mined rows that live outside
#      corpus/ and exist in the lane (--no-closure skips it; the census then reports E11,
#      because corpus/ alone cannot satisfy used-by targets such as tools/ or SKILL.md)
#   5. sources-census.sh validate --file $V/corpus/SOURCES.md
#
# stdout: the census TSV, verbatim.  stderr: MIRROR: trace lines, incl. census-exit=N.
# exit:   the census exit code (0 clean or warnings, 1 E-findings, 2 census env/usage).
#         2 also covers a bad block (empty, heading, non-row line, no table end) or a
#         KNOWLEDGE path that is absolute, escapes the lane, or is not in the lane.
# Read-only towards the lane and the fleet: nothing outside $V is written; $V is removed on
# exit unless --keep. Bash + coreutils + gawk, as the census itself.
set -u

BLOCK=""; LANE=""; CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
TODAY=""; KEEP=0; CLOSURE=1; QUIET=0
declare -a KNOW=()

die() { printf 'MIRROR: ERROR: %s\n' "$*" >&2; exit 2; }
trace() { [ "$QUIET" = 1 ] || printf 'MIRROR: %s\n' "$*" >&2; }

# rows of the ## Registry table (S-ids only), used to prove the insert landed inside it
registry_rows() {
  awk '
    /^##[ \t]+Registry[ \t]*$/ { inreg = 1; next }
    /^#/ { inreg = 0; next }
    inreg && /^ {0,3}\|[ \t]*S[0-9][0-9]*[ \t]*\|/ { n++ }
    END { print n + 0 }
  ' "$1"
}

# Placement proof for the insert: the block must sit contiguously at the END of the Registry
# table — preceded by a table row, followed by the blank line that ends the table, with every
# pre-existing Registry row before it and no table line after that blank line. Prints "ok" or
# a one-line reason (and a non-zero exit); the caller turns a reason into a hard failure, so a
# block that landed in the wrong place can never pass the gate.
verify_insert() { # $1 = mirror SOURCES.md, $2 = block, $3 = expected rows before the block
  awk -v blk="$2" -v want="$3" '
    BEGIN {
      nb = 0
      while ((getline l < blk) > 0) { if (l ~ /^[ \t]*$/) continue; nb++; b[nb] = l }
      if (nb == 0) { print "empty-block"; exit 1 }
    }
    { line[NR] = $0 }
    END {
      start = 0
      for (i = 1; i + nb - 1 <= NR; i++) {          # last occurrence wins: the block is appended
        ok = 1
        for (j = 1; j <= nb; j++) if (line[i + j - 1] != b[j]) { ok = 0; break }
        if (ok) start = i
      }
      if (!start) { print "block-not-found"; exit 1 }
      n = 0; inreg = 0
      for (k = 1; k < start; k++) {
        if (line[k] ~ /^##[ \t]+Registry[ \t]*$/) { inreg = 1; continue }
        if (line[k] ~ /^#/) { inreg = 0; continue }
        if (inreg && line[k] ~ /^ {0,3}\|[ \t]*S[0-9]/) n++
      }
      if (n != want) { printf "rows-before-block=%d want=%d\n", n, want; exit 2 }
      if (line[start - 1] !~ /^[ \t]*\|/) { print "block-not-after-a-table-row"; exit 3 }
      if (line[start + nb] !~ /^[ \t]*$/) { print "block-not-before-the-blank-line"; exit 4 }
      for (k = start + nb + 1; k <= NR; k++) {
        if (line[k] ~ /^[ \t]*$/) continue
        if (line[k] ~ /^ {0,3}\|/) { print "table-resumes-after-the-block"; exit 5 }
        break
      }
      print "ok"
    }' "$1"
}

# used-by targets of mined rows in one SOURCES.md (one repo-relative path per line)
usedby_targets() {
  gawk -F'|' '
    function trim(s) { gsub(/^[ \t]+|[ \t]+$/,"",s); return s }
    /^##[ \t]+Registry[ \t]*$/ { inreg = 1; next }
    /^#/ { inreg = 0; next }
    inreg && /^ {0,3}\|/ {
      line = $0; sub(/^ {0,3}/,"",line); $0 = line
      if (trim($2) == "id") next
      if (trim($9) != "mined") next
      u = trim($12)
      if (u == "" || u == "—") next
      n = split(u, a, ",")
      for (i = 1; i <= n; i++) { p = trim(a[i]); if (p != "" && p != "—") print p }
    }' "$1" | sort -u
}

while [ $# -gt 0 ]; do
  case "$1" in
    --block)     [ $# -ge 2 ] || die "--block needs a path"; BLOCK=$2; shift 2 ;;
    --knowledge) [ $# -ge 2 ] || die "--knowledge needs a path"; KNOW+=("$2"); shift 2 ;;
    --lane)      [ $# -ge 2 ] || die "--lane needs a path"; LANE=$2; shift 2 ;;
    --census)    [ $# -ge 2 ] || die "--census needs a path"; CENSUS=$2; shift 2 ;;
    --today)     [ $# -ge 2 ] || die "--today needs a date"; TODAY=$2; shift 2 ;;
    --keep)      KEEP=1; shift ;;
    --no-closure) CLOSURE=0; shift ;;
    --quiet)     QUIET=1; shift ;;
    -h|--help)   sed -n '2,30p' "$0"; exit 0 ;;
    --)          shift; while [ $# -gt 0 ]; do
                   if [ -z "$BLOCK" ]; then BLOCK=$1; else KNOW+=("$1"); fi; shift
                 done ;;
    -*)          die "unknown option: $1" ;;
    *)           if [ -z "$BLOCK" ]; then BLOCK=$1; else KNOW+=("$1"); fi; shift ;;
  esac
done

[ -n "$BLOCK" ] || die "no append block given (see --help)"

# lane: explicit, else the nearest ancestor of this script that carries corpus/SOURCES.md
if [ -z "$LANE" ]; then
  d=$(cd -- "$(dirname -- "$0")" && pwd) || die "cannot resolve the script directory"
  while [ "$d" != "/" ]; do
    [ -f "$d/corpus/SOURCES.md" ] && { LANE=$d; break; }
    d=$(dirname -- "$d")
  done
  [ -n "$LANE" ] || die "cannot locate the lane from $0; pass --lane"
fi
[ -d "$LANE" ] || die "lane is not a directory: $LANE"
[ -f "$LANE/corpus/SOURCES.md" ] || die "lane has no corpus/SOURCES.md: $LANE"
LANE=$(realpath -- "$LANE") || die "cannot resolve lane: $LANE"
[ -f "$CENSUS" ] || die "census script not found: $CENSUS"

# ---- block preconditions: structure only; row quality stays the census's judgment --------
[ -f "$BLOCK" ] || die "append block not found: $BLOCK"
grep -q '[^[:space:]]' -- "$BLOCK" || die "append block is empty: $BLOCK"
if grep -qE '^ {0,3}#' -- "$BLOCK"; then
  die "append block contains a Markdown heading; an append block is rows only"
fi
n=0
while IFS= read -r line || [ -n "$line" ]; do
  n=$((n + 1))
  [ -n "${line//[[:space:]]/}" ] || continue
  case "$line" in
    '|'*) ;;
    *) die "append block line $n is not a table row: $line" ;;
  esac
done < "$BLOCK"
block_rows=$(grep -c '^|' -- "$BLOCK")

# ---- scratch tree, never inside the lane ------------------------------------------------
V=$(mktemp -d "${TMPDIR:-/tmp}/mirror-validate.XXXXXXXX") || die "mktemp -d failed"
V=$(realpath -- "$V") || die "cannot resolve scratch: $V"
case "$V/" in
  "$LANE"/*) rm -rf -- "$V"; die "scratch $V is inside the lane $LANE" ;;
esac
cleanup() {
  if [ "$KEEP" = 1 ]; then printf 'MIRROR: kept %s\n' "$V" >&2; return; fi
  [ -n "$V" ] && rm -rf -- "$V"
}
trap cleanup EXIT
trace "scratch=$V"
trace "lane=$LANE"

# ---- 1. corpus mirror --------------------------------------------------------------------
mkdir -p -- "$V/corpus" || die "cannot create $V/corpus"
for p in SOURCES.md README.md knowledge lessons; do
  [ -e "$LANE/corpus/$p" ] || die "lane corpus is missing $p"
  cp -a -- "$LANE/corpus/$p" "$V/corpus/" || die "copy failed: corpus/$p"
done
trace "corpus-files=$(find "$V/corpus" -type f | wc -l)"

# ---- 2. insert the block before the blank line that ends the ## Registry table ----------
before=$(registry_rows "$LANE/corpus/SOURCES.md")
# The heading is followed by its own blank line before the header row, so the insert point is
# not "the first blank line after the heading": it is the first blank line AFTER the table run
# has started. intable tracks that.
if ! awk -v blk="$BLOCK" '
      BEGIN { while ((getline l < blk) > 0) buf = buf l "\n" }
      /^##[ \t]+Registry[ \t]*$/ { inreg = 1; intable = 0; print; next }
      inreg && !intable && /^[ \t]*\|/ { intable = 1 }
      inreg && intable && !inserted && /^[ \t]*$/ {
        printf "%s", buf; inserted = 1; inreg = 0; intable = 0
      }
      { print }
      END { exit(inserted ? 0 : 3) }
    ' "$V/corpus/SOURCES.md" > "$V/SOURCES.md.new"; then
  rm -f -- "$V/SOURCES.md.new"
  die "no ## Registry table end (heading + table run + terminating blank line) in $V/corpus/SOURCES.md"
fi
mv -- "$V/SOURCES.md.new" "$V/corpus/SOURCES.md" || die "cannot replace $V/corpus/SOURCES.md"
after=$(registry_rows "$V/corpus/SOURCES.md")
[ "$after" -eq $((before + block_rows)) ] \
  || die "insert did not land in the table: rows $before -> $after, block rows $block_rows"
placement=$(verify_insert "$V/corpus/SOURCES.md" "$BLOCK" "$before") \
  || die "insert placement rejected: $placement"
[ "$placement" = ok ] || die "insert placement rejected: $placement"
trace "registry-rows=$before->$after block-rows=$block_rows placement=$placement"

# ---- 3. listed knowledge files, at their repo-relative paths -----------------------------
for k in ${KNOW[@]+"${KNOW[@]}"}; do
  case "$k" in
    /*) die "knowledge path must be repo-relative: $k" ;;
  esac
  case "/$k/" in
    */../*) die "knowledge path escapes the lane: $k" ;;
  esac
  [ -f "$LANE/$k" ] || die "knowledge file is not in the lane: $k"
  mkdir -p -- "$V/$(dirname -- "$k")" || die "cannot create $V/$(dirname -- "$k")"
  cp -p -- "$LANE/$k" "$V/$k" || die "copy failed: $k"
  trace "knowledge-copied $k"
done

# ---- 4. closure: used-by targets of mined rows that live outside corpus/ ----------------
if [ "$CLOSURE" = 1 ]; then
  closure=0
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    [ -e "$V/$p" ] && continue
    case "/$p/" in
      */../*) trace "closure-unsafe $p (not copied: escapes the scratch)"; continue ;;
    esac
    case "$p" in
      /*) trace "closure-unsafe $p (not copied: absolute)"; continue ;;
    esac
    if [ -e "$LANE/$p" ]; then
      mkdir -p -- "$V/$(dirname -- "$p")" || die "cannot create $V/$(dirname -- "$p")"
      cp -p -- "$LANE/$p" "$V/$p" || die "copy failed: $p"
      closure=$((closure + 1))
      trace "closure-copy $p"
    else
      trace "closure-missing $p (left for the census: E11)"
    fi
  done < <(usedby_targets "$V/corpus/SOURCES.md")
  trace "closure-copies=$closure"
else
  trace "closure=off"
fi

# ---- 5. census gate ----------------------------------------------------------------------
trace "census=validate --file $V/corpus/SOURCES.md${TODAY:+ --today $TODAY}"
out=$(bash "$CENSUS" validate --file "$V/corpus/SOURCES.md" ${TODAY:+--today "$TODAY"} 2>&1)
rc=$?
[ -n "$out" ] && printf '%s\n' "$out"
if [ "$rc" = 0 ]; then trace "gate=PASS census-exit=$rc"; else trace "gate=FAIL census-exit=$rc"; fi
exit "$rc"
