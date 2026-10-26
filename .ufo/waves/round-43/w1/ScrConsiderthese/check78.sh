#!/usr/bin/env bash
# check78.sh — round | attempts launched | dead attempts | completed | closure, for a
# range of mado rounds, from two read-only sources:
#   (1) the fleet driver digest  <log>        (`launch|complete|lane-dead-no-report mado round=N`)
#   (2) the lane's own closures  <lessons>/round-N-verifier-spotcheck.md (the closure row)
#
# Usage:
#   check78.sh --log <watchdog.log> --lessons <dir> --from N --to N [--repo . --tip-map tips.txt]
#   check78.sh --selftest
#
# The closure column prefers the round's committed witness `.ufo/waves/round-N/receipts/closure-status.txt`
# at the tip `--tip-map` names (`<round> <rev>` per line, read with `git cat-file`/`git show`); when that
# receipt is absent it falls back to the round's spot-check line and prints `source=spotcheck` — a relayed
# reading, not a re-derived one. `source=receipt` is re-derived: 0 non-blank lines = CLEAN, else DIRTY.
#
# Counting rule (stated, so a reader can re-derive every cell):
#   launches  = `grep -cE 'launch mado round=N( |$)'`      — never the `attempt=` field (not monotonic;
#               round 28 carries attempt=1 seven times, corpus/lessons/round-40.md:150)
#   dead      = `grep -cE 'lane-dead-no-report mado round=N;'`
#   complete  = `grep -cE 'complete mado round=N;'`
#   closure   = classification of the FIRST 'uncommitted|status --porcelain|untracked=' line in the round's
#               spot-check: DIRTY if it carries a dirty token, else CLEAN if it carries a clean token,
#               else UNKNOWN. UNKNOWN is printed, never silently folded into CLEAN.
# Exit: 0 when every round in range resolved to CLEAN or DIRTY and launches == complete + dead;
#       1 when any round is UNKNOWN/absent or a launch is neither completed nor recorded dead.
set -u
# Token lists, applied to the line after markdown emphasis (`*`, backticks) is stripped and it is
# lowercased. `untracked` counts only as a word (round 42 writes `untracked=0`, which is clean).
DIRTY_RE='\?\? |untracked=[1-9]|untracked([ ,)]|$)|\bmodified\b|\bdefect\b|\bFAIL\b|\bdirty\b|\bleftover|uncommitted \('
CLEAN_RE='no uncommitted|untracked=0|porcelain empty|pushed, clean'

usage() { sed -n '2,24p' "$0"; exit 2; }

classify() { # $1 = spot-check file; prints "CLEAN|DIRTY|UNKNOWN<TAB>path:line"
  f=$1
  [ -f "$f" ] || { printf 'ABSENT\t%s\n' "$f"; return; }
  grep -n -iE 'uncommitted|status --porcelain|untracked=' "$f" | awk -F: -v path="$f" '
    { ln=$1; $1=""; line=substr($0,2); sub(/[ \t]+$/,"",line); text=line; if (text ~ /^[ \t]*\|/) {
        # table row: the verdict cell decides; fields after the check name
        n=split(text, a, "|"); verdict=""
        for (i=3; i<=n; i++) {
          gsub(/[*`]/,"",a[i]); v=a[i]; sub(/^[ \t]+/,"",v)
          if (v ~ /^(PASS|ok|OK)/) { verdict="CLEAN"; break }
          if (v ~ /^(DEFECT|defect|FAIL|partial|PARTIAL|WARN|warn)/) { verdict="DIRTY"; break }
        }
        if (verdict=="") { body=""; for (i=2; i<=n; i++) body=body " " a[i]
          gsub(/[*`]/,"",body); gsub(/untracked=0/,"tracked-zero",body)
          if (body ~ /\?\? |untracked|modified|[Dd]efect|FAIL|partial|dirty|leftover/) verdict="DIRTY"
          else if (body ~ /tracked-zero|empty|No uncommitted|PASS/) verdict="CLEAN" }
        if (verdict=="") { if (first=="") first=ln; next }
        if (verdict=="DIRTY") { print "DIRTY\t" path ":" ln; found=1; exit }
        if (clean=="") clean=ln; next }
      # prose line (the verdict word leads in this lane prose, so a PASS over leftovers reads clean)
      t2=text; gsub(/[*`]/,"",t2); gsub(/untracked=0/,"tracked-zero",t2)
      if (t2 ~ /\?\? |untracked=[1-9]|untracked [0-9]|defect|DEFECT|FAIL|partial|PARTIAL|dirty|modified/) {
        print "DIRTY\t" path ":" ln; found=1; exit }
      if (clean=="" && t2 ~ /tracked-zero|No uncommitted|porcelain. empty|porcelain` empty|pushed, clean|PASS/) clean=ln
      if (first=="") first=ln }
    END { if (found) exit
          if (clean!="") print "CLEAN\t" path ":" clean
          else print "UNKNOWN\t" path ":" (first=="" ? 0 : first) }'
}

main() {
  log=''; lessons=''; from=''; to=''; repo=''; tipmap=''; receipts_root=''
  while [ $# -gt 0 ]; do case $1 in
    --log) log=$2; shift 2;; --lessons) lessons=$2; shift 2;;
    --from) from=$2; shift 2;; --to) to=$2; shift 2;;
    --repo) repo=$2; shift 2;; --tip-map) tipmap=$2; shift 2;;
    --receipts-root) receipts_root=$2; shift 2;;
    -h|--help) usage;; *) echo "unknown arg: $1" >&2; exit 2;;
  esac; done
  [ -n "$log" ] && [ -n "$lessons" ] && [ -n "$from" ] && [ -n "$to" ] || usage
  [ -f "$log" ] || { echo "FAIL log absent: $log" >&2; exit 2; }
  printf 'check78 source: log=%s sha256=%s\n' "$log" "$(sha256sum "$log" | cut -d' ' -f1)"
  printf 'round\tlaunches\tdead\tcomplete\tclosure\tsource\tcite\n'
  r=$from; tl=0; td=0; tc=0; tclean=0; tdirty=0; tunk=0; trelayed=0; bad=0
  while [ "$r" -le "$to" ]; do
    l=$(grep -cE "launch mado round=$r( |\$)" "$log" || true)
    d=$(grep -cE "lane-dead-no-report mado round=$r;" "$log" || true)
    c=$(grep -cE "complete mado round=$r;" "$log" || true)
    verdict=''; cite=''; src='spotcheck'
    if [ -n "${receipts_root:-}" ] && [ -f "$receipts_root/round-$r/closure-status.txt" ]; then
      nb=$(grep -c . "$receipts_root/round-$r/closure-status.txt" || true)
      [ "$nb" -eq 0 ] && verdict=CLEAN || verdict=DIRTY
      src=receipt; cite="$receipts_root/round-$r/closure-status.txt:$nb-nonblank"
    elif [ -n "${repo:-}" ] && [ -n "${tipmap:-}" ]; then
      tip=$(awk -v r="$r" '$1==r {print $2; exit}' "$tipmap")
      if [ -n "$tip" ] && git -C "$repo" cat-file -e "$tip:.ufo/waves/round-$r/receipts/closure-status.txt" 2>/dev/null; then
        nb=$(git -C "$repo" show "$tip:.ufo/waves/round-$r/receipts/closure-status.txt" | grep -c . || true)
        [ "$nb" -eq 0 ] && verdict=CLEAN || verdict=DIRTY
        src=receipt; cite="tip ${tip:0:9}:.ufo/waves/round-$r/receipts/closure-status.txt:$nb-nonblank"
      fi
    fi
    if [ -z "$verdict" ]; then
      cls=$(classify "$lessons/round-$r-verifier-spotcheck.md")
      verdict=${cls%%$'\t'*}; cite=${cls#*$'\t'}
      case $verdict in CLEAN) verdict='RELAYED:clean';; DIRTY) verdict='RELAYED:dirty';; esac
    fi
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$r" "$l" "$d" "$c" "$verdict" "$src" "$cite"
    tl=$((tl+l)); td=$((td+d)); tc=$((tc+c))
    case $verdict in
      CLEAN) tclean=$((tclean+1));;
      DIRTY) tdirty=$((tdirty+1));;
      RELAYED:clean) tclean=$((tclean+1)); trelayed=$((trelayed+1));;
      RELAYED:dirty) tdirty=$((tdirty+1)); trelayed=$((trelayed+1));;
      *) tunk=$((tunk+1)); bad=1;; esac
    [ "$l" -eq $((c+d)) ] || { echo "  UNEXPLAINED round=$r launches=$l != complete+dead=$((c+d))"; bad=1; }
    r=$((r+1))
  done
  printf 'TALLY rounds=%s launches=%s dead=%s complete=%s clean=%s dirty=%s relayed=%s unknown=%s\n' \
    "$((to-from+1))" "$tl" "$td" "$tc" "$tclean" "$tdirty" "$trelayed" "$tunk"
  if [ "$bad" -eq 0 ]; then echo 'VERDICT: TABLE_COMPLETE'; exit 0; else echo 'VERDICT: TABLE_INCOMPLETE'; exit 1; fi
}

selftest() {
  S=$(mktemp -d "${TMPDIR:-/tmp}/check78.XXXXXX") || exit 1
  trap 'rm -rf -- "$S"' EXIT
  cat > "$S/wd.log" <<'EOF'
2026-01-01T00:00:00-03:00 launch mado round=1 pgid=1 driver=hyaku-inline attempt=1
2026-01-01T00:10:00-03:00 complete mado round=1; hyaku-inline attempt=1
2026-01-01T01:00:00-03:00 launch mado round=2 pgid=2 driver=hyaku-inline attempt=1
2026-01-01T01:10:00-03:00 lane-dead-no-report mado round=2; retry same round (synthetic)
2026-01-01T01:11:00-03:00 launch mado round=2 pgid=3 driver=hyaku-inline attempt=2
2026-01-01T02:00:00-03:00 complete mado round=2; hyaku-inline attempt=2
2026-01-01T03:00:00-03:00 launch mado round=3 pgid=4 driver=hyaku-inline attempt=1
2026-01-01T04:00:00-03:00 complete mado round=3; hyaku-inline attempt=1
2026-01-01T05:00:00-03:00 launch mado round=12 pgid=5 driver=hyaku-inline attempt=1
2026-01-01T06:00:00-03:00 launch mado round=4 pgid=6 driver=hyaku-inline attempt=1
2026-01-01T07:00:00-03:00 complete mado round=4; hyaku-inline attempt=1
2026-01-01T08:00:00-03:00 launch mado round=5 pgid=7 driver=hyaku-inline attempt=1
2026-01-01T09:00:00-03:00 complete mado round=5; hyaku-inline attempt=1
EOF
  printf '| uncommitted round work | PASS - `git status --porcelain` empty at closure. |\n' > "$S/round-1-verifier-spotcheck.md"
  mkdir -p "$S/receipts/round-1" "$S/receipts/round-4"
  : > "$S/receipts/round-1/closure-status.txt"                      # empty witness -> CLEAN
  printf '?? stale.md\n' > "$S/receipts/round-4/closure-status.txt"  # one path      -> DIRTY (receipt wins)
  printf '| uncommitted round work | DEFECT - `?? .ufo/waves/round-2/x/y.md` untracked |\n' > "$S/round-2-verifier-spotcheck.md"
  # round 3: no spot-check file at all
  printf '| pushed | `local=remote=abc ahead=0` ; `git status --porcelain` empty |\n' > "$S/round-12-verifier-spotcheck.md"
  printf '| uncommitted round work | none tracked; **2 untracked** scratch files (status-neutral defect) |\n' > "$S/round-4-verifier-spotcheck.md"
  printf '| pushed | `ahead=0` ; `git status --porcelain` empty |\n| leftovers | `tracked=8 untracked=2` stand at closure |\n' > "$S/round-5-verifier-spotcheck.md"
  out=$("$0" --log "$S/wd.log" --lessons "$S" --receipts-root "$S/receipts" --from 1 --to 5); rc=$?
  printf '%s\n' "$out"
  ok=1
  row() { printf '%s\n' "$out" | awk -F'\t' -v r="$1" -v l="$2" -v d="$3" -v c="$4" -v v="$5" \
    '$1==r && $2==l && $3==d && $4==c && $5==v {f=1} END {exit !f}'; }
  row 1 1 0 1 CLEAN || { echo 'SELFTEST FAIL r1 row'; ok=0; }
  printf '%s\n' "$out" | awk -F'\t' '$1==1 && $6=="receipt" {f=1} END {exit !f}' || { echo 'SELFTEST FAIL r1 receipt source'; ok=0; }
  printf '%s\n' "$out" | awk -F'\t' '$1==2 && $6=="spotcheck" {f=1} END {exit !f}' || { echo 'SELFTEST FAIL r2 spotcheck source'; ok=0; }
  row 2 2 1 1 RELAYED:dirty || { echo 'SELFTEST FAIL r2 row'; ok=0; }
  row 3 1 0 1 ABSENT || { echo 'SELFTEST FAIL r3 absent'; ok=0; }
  row 4 1 0 1 DIRTY || { echo 'SELFTEST FAIL r4 emphasis/lowercase defect'; ok=0; }
  row 5 1 0 1 RELAYED:dirty || { echo 'SELFTEST FAIL r5 later-line dirty'; ok=0; }
  printf '%s\n' "$out" | awk -F'\t' '$1==5 && $7 ~ /:2$/ {f=1} END {exit !f}' || { echo 'SELFTEST FAIL r5 cite line'; ok=0; }
  printf '%s' "$out" | grep -q 'TALLY rounds=5 launches=6 dead=1 complete=5 clean=1 dirty=3 relayed=2 unknown=1' || { echo 'SELFTEST FAIL tally4'; ok=0; }
  # prefix trap: round 12 must not be counted into round 1 (row 1 launches must be 1, not 2)
  printf '%s\n' "$out" | awk -F'\t' '$1==1 && $2==2 {f=1} END {exit !f}' && { echo 'SELFTEST FAIL prefix collision r1'; ok=0; }
  printf '%s' "$out" | grep -q 'TALLY rounds=5 launches=6 dead=1 complete=5 clean=1 dirty=3 relayed=2 unknown=1' || { echo 'SELFTEST FAIL tally'; ok=0; }
  [ "$rc" -eq 1 ] || { echo "SELFTEST FAIL exit (want 1 on UNKNOWN, got $rc)"; ok=0; }
  # second pass: fill round 3 so the table is complete and the tool must exit 0
  printf '| uncommitted round work | PASS - `git status --porcelain` empty |\n' > "$S/round-3-verifier-spotcheck.md"
  "$0" --log "$S/wd.log" --lessons "$S" --receipts-root "$S/receipts" --from 1 --to 5 | tail -2
  [ "${PIPESTATUS[0]}" -eq 0 ] || { echo 'SELFTEST FAIL exit 0 on complete table'; ok=0; }
  [ "$ok" -eq 1 ] && { echo 'SELFTEST: PASS (12 assertions)'; exit 0; }
  echo 'SELFTEST: FAIL'; exit 1
}

case ${1:-} in --selftest) selftest;; *) main "$@";; esac
