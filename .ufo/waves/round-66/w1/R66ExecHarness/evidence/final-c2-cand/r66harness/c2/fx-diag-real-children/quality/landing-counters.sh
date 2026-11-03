#!/usr/bin/env bash
# Round-66 C2: four child contracts; GREEN/RED/ERROR exit 0/1/2.
# All writes are confined to caller-declared scratch. No network or host changes.
set -u
# Remove every Git steering variable, including GIT_CONFIG_COUNT and indexed keys.
for git_var in "${!GIT_@}"; do unset "$git_var"; done
PROG=landing-counters.sh
N=0 P=0
fail() { printf '%s: %s\n' "$PROG" "$*" >&2; exit 2; }
SELF_PATH=$(readlink -f -- "$0") || fail 'cannot resolve own path'
SELF_DIR=${SELF_PATH%/*}
USEDBY_SIBLING="$SELF_DIR/counters/c3-r56-used-by.py"
LEDGER_SIBLING="$SELF_DIR/check-tool-ledger.py"
CITECHECK_SIBLING="$SELF_DIR/../tools/mado-receipt-citecheck.py"
usage() { printf 'usage: %s --repo DIR --rev REV --round N --scratch-root DIR [--citecheck-paths PATH ...] | --selftest --scratch-root DIR\n' "$PROG"; }
check() { N=$((N+1)); if [ "$2" = "$3" ]; then P=$((P+1)); printf 'SELFTEST ok %d: %s\n' "$N" "$1"; else printf 'SELFTEST FAIL %d: %s want=%s got=%s\n' "$N" "$1" "$2" "$3"; fi; }
leg_nav() (
  cd "$REPO_ABS" || exit 2
  REV="$REV" python3 - <<'PY'
import os, re, subprocess
from collections import Counter
rev = os.environ['REV']
def git(*args):
    return subprocess.check_output(['git', *args], text=True)
notes = {p for p in git('ls-tree', '--name-only', rev + ':corpus/knowledge').splitlines() if p.endswith('.md')}
rows = re.findall(r'^\| `knowledge/([^`]+\.md)`', git('show', rev + ':corpus/README.md'), re.M)
counts = Counter(rows)
missing = sorted(notes - counts.keys())
dangling = sorted(counts.keys() - notes)
duplicates = sorted(p for p, n in counts.items() if n != 1)
covered = sum(counts[p] == 1 for p in notes)
print(f'revision={rev} indexed={covered}/{len(notes)} missing={len(missing)} dangling={len(dangling)} duplicates={len(duplicates)} coverage={10*covered/len(notes) if notes else 0:.4f}/10')
for kind, paths in (('missing', missing), ('dangling', dangling), ('duplicate', duplicates)):
    for path in paths:
        print(f'{kind}: knowledge/{path}')
raise SystemExit(1 if not notes or missing or dangling or duplicates else 0)
PY
)
leg_usedby() { python3 "$USEDBY_SIBLING" --repo "$REPO_ABS" --rev "$REV" --work "$SCRATCH_ABS/ub"; }
leg_ledger() { python3 "$LEDGER_SIBLING" --repo "$REPO_ABS" --rev "$REV"; }
leg_citecheck() { python3 "$CITECHECK_SIBLING" --repo "$REPO_ABS" --rev "$REV" --paths "${CITE_PATHS[@]}"; }
# Validate exactly one child-owned marker, its revision and verdict against its rc.
# These are structural witnesses, not an authenticity guarantee against malicious children.
marker_valid() {
  local leg=$1 rc=$2 out=$3 line marker= count=0 prefix met field
  [ "$rc" -le 1 ] || return 1
  case "$leg" in nav) prefix=revision= ;; usedby) prefix='MADO_USED_BY:' ;; ledger) prefix='LEDGER:' ;; citecheck) prefix='MADO_CITECHECK:' ;; esac
  while IFS= read -r line; do
    if [[ "$line" == "$prefix"* ]]; then marker=$line; count=$((count+1)); fi
  done <<<"$out"
  [ "$count" -eq 1 ] || return 1
  if [ "$leg" = nav ]; then
    [[ "$marker" =~ ^revision=([^\ ]+)\ indexed=([0-9]+)/([0-9]+)\ missing=([0-9]+)\ dangling=([0-9]+)\ duplicates=([0-9]+)\ coverage=[0-9.]+/10$ ]] || return 1
    [ "${BASH_REMATCH[1]}" = "$REV" ] || return 1
    local a=${BASH_REMATCH[2]} b=${BASH_REMATCH[3]} m=${BASH_REMATCH[4]} d=${BASH_REMATCH[5]} dup=${BASH_REMATCH[6]}
    [ "$a" -le "$b" ] || return 1
    met=1
    if [ "$b" -gt 0 ] && [ "$a" -eq "$b" ] && [ "$m" -eq 0 ] && [ "$d" -eq 0 ] && [ "$dup" -eq 0 ]; then met=0; fi
    [ "$rc" -eq "$met" ]
    return
  fi
  [[ " $marker " == *" rev=$REV "* ]] || return 1
  if [ "$rc" -eq 0 ]; then met=TARGET_MET; else met=TARGET_MISSED; fi
  [[ " $marker " == *" verdict=$met "* ]] || return 1
  # Refuse contradictory or duplicated verdict fields as malformed evidence.
  field=${marker#*verdict=}; field=${field%% *}
  [ "$field" = "$met" ] && [[ "${marker#*verdict=}" != *verdict=* ]] || return 1
  if [ "$leg" = citecheck ]; then
    [[ "$marker" =~ \ citations=([0-9]+)\ resolved=([0-9]+)\ missing=([0-9]+)\  ]] || return 1
    local citations=${BASH_REMATCH[1]} resolved=${BASH_REMATCH[2]} missing=${BASH_REMATCH[3]}
    [ "$citations" -gt 0 ] && [ "$citations" -eq "$((resolved+missing))" ] || return 1
    if [ "$rc" -eq 0 ]; then [ "$missing" -eq 0 ]; else [ "$missing" -gt 0 ]; fi
  fi
}
run_selftest() {
  local SW="$SCRATCH_ABS/selftest.$$" D top out rc leg mode expected witness real_python
  mkdir -p -- "$SW" || return 2
  SELFTEST_WORK=$SW
  trap 'rm -rf -- "$SELFTEST_WORK"' EXIT
  D="$SW/fixture"
  mkdir -p "$D/corpus/knowledge" "$D/.ufo/waves/round-66/receipts" "$D/.ufo/waves/round-65/receipts" "$SW/instrument/quality/counters" "$SW/instrument/tools" "$SW/shim"
  printf '| `knowledge/n.md` |\n' >"$D/corpus/README.md"
  printf '# note\n' >"$D/corpus/knowledge/n.md"
  printf 'cite corpus/README.md\n' >"$D/.ufo/waves/round-66/receipts/a.txt"
  printf 'decoy\n' >"$D/.ufo/waves/round-65/receipts/a.txt"
  git -C "$D" init -q || return 2
  top=$(git -C "$D" rev-parse --show-toplevel) || return 2
  [ "$top" = "$D" ] || return 2
  git -C "$D" add -A && git -C "$D" -c user.name=mado-selftest -c user.email=selftest@example.invalid -c commit.gpgsign=false commit -qm fixture || return 2
  local rev_f
  rev_f=$(git -C "$D" rev-parse HEAD) || return 2
  cp -- "$SELF_PATH" "$SW/instrument/quality/landing-counters.sh"
  for leg in "$SW/instrument/quality/counters/c3-r56-used-by.py" "$SW/instrument/quality/check-tool-ledger.py" "$SW/instrument/tools/mado-receipt-citecheck.py"; do printf '# fixture child dispatched by shim\n' >"$leg"; done
  real_python=$(command -v python3)
  cat >"$SW/shim/python3" <<'SHIM'
#!/usr/bin/env bash
case "$1" in
  -) leg=nav ;;
  */c3-r56-used-by.py) leg=usedby ;;
  */check-tool-ledger.py) leg=ledger ;;
  */mado-receipt-citecheck.py) leg=citecheck ;;
  *) exit 2 ;;
esac
if [ "$leg" != nav ] && [ ! -r "$1" ]; then
  printf 'fixture child missing: %s\n' "$1" >&2
  exit 2
fi
printf '%s\n' "$leg" >>"$WITNESS"
if [ "$leg" = "$TEST_LEG" ]; then
  case "$TEST_MODE" in skip) exit 0 ;; crash) exit 2 ;; esac
fi
rc=0 verdict=TARGET_MET
if [ "$leg" = "$TEST_LEG" ] && [ "$TEST_MODE" = red ]; then rc=1 verdict=TARGET_MISSED; fi
output=$(case "$leg" in
  nav)
    if [ "$rc" = 0 ]; then exec "$REAL_PYTHON" "$@"; fi
    printf 'revision=%s indexed=0/1 missing=1 dangling=0 duplicates=0 coverage=0.0000/10\n' "$FIXTURE_REV" ;;
  usedby) printf 'MADO_USED_BY: rev=%s entries=1 rows=1 missing=%s extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=0 verdict=%s missed=none\n' "$FIXTURE_REV" "$rc" "$verdict" ;;
  ledger) printf 'LEDGER: population=1 ledger_rows=1 uncovered=%s dangling=0 bad_pointer=0 empty_desc=0 verdict=%s rev=%s\n' "$rc" "$verdict" "$FIXTURE_REV" ;;
  citecheck) printf 'MADO_CITECHECK: rev=%s files=1 citations=1 resolved=%s missing=%s skipped_large=0 verdict=%s\n' "$FIXTURE_REV" "$((1-rc))" "$rc" "$verdict" ;;
esac)
child_status=$?
if [ "$leg" = nav ] && [ "$rc" -eq 0 ]; then rc=$child_status; fi
printf '%s\n' "$output"
if [ "$leg" = "$TEST_LEG" ] && [ "$TEST_MODE" = duplicate ]; then printf '%s\n' "$output"; fi
exit "$rc"
SHIM
  chmod +x "$SW/shim/python3"
  local instrument="$SW/instrument/quality/landing-counters.sh"
  export WITNESS="$SW/witness" FIXTURE_REV="$rev_f" REAL_PYTHON="$real_python" TEST_LEG=none TEST_MODE=green
  local -a cmd=(bash "$instrument" --repo "$D" --rev "$rev_f" --round 66 --scratch-root "$SW/run")
  for leg in none nav usedby ledger citecheck; do
    for mode in green red crash skip duplicate; do
      [ "$leg" != none ] || [ "$mode" = green ] || continue
      TEST_LEG=$leg TEST_MODE=$mode
      : >"$WITNESS"
      out=$(PATH="$SW/shim:$PATH" "${cmd[@]}" 2>&1); rc=$?
      expected=0
      case "$mode" in red) expected=1 ;; crash|skip|duplicate) expected=2 ;; esac
      check "$leg $mode rc" "$expected" "$rc"
      witness=$(<"$WITNESS")
      check "$leg $mode all execution witnesses" $'nav\nusedby\nledger\ncitecheck' "$witness"
    done
  done
  TEST_LEG=none TEST_MODE=green
  rm -- "$SW/instrument/quality/counters/c3-r56-used-by.py"
  out=$(PATH="$SW/shim:$PATH" "${cmd[@]}" 2>&1); rc=$?
  check 'missing sibling' 2 "$rc"
  check 'missing sibling emits ERROR classification' yes "$([[ "$out" == *'MADO_LANDING_COUNTERS: ERROR ('* ]] && printf yes || printf no)"
  printf '# fixture child\n' >"$SW/instrument/quality/counters/c3-r56-used-by.py"
  # Exercise absent --round while both candidate/default receipt trees are clean.
  out=$(PATH="$SW/shim:$PATH" bash "$instrument" --repo "$D" --rev "$rev_f" --scratch-root "$SW/clean-no-round" 2>&1); rc=$?
  check 'round required on clean fixture' 2 "$rc"
  printf 'dirty decoy\n' >>"$D/.ufo/waves/round-65/receipts/a.txt"
  out=$(PATH="$SW/shim:$PATH" "${cmd[@]}" 2>&1); rc=$?
  check 'round-65 dirty decoy does not select scope' 0 "$rc"
  printf 'dirty selected\n' >>"$D/.ufo/waves/round-66/receipts/a.txt"
  out=$(PATH="$SW/shim:$PATH" "${cmd[@]}" 2>&1); rc=$?
  check 'round-66 dirty selected scope' 2 "$rc"
  out=$(PATH="$SW/shim:$PATH" "${cmd[@]}" --citecheck-paths .ufo/waves/round-65/receipts 2>&1); rc=$?
  check 'explicit paths dirty guard' 2 "$rc"
  # Reset only fixture bytes, never the lane or another seat.
  printf 'cite corpus/README.md\n' >"$D/.ufo/waves/round-66/receipts/a.txt"
  out=$(GIT_DIR="$SW/absent" GIT_WORK_TREE="$SW" GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.worktree GIT_CONFIG_VALUE_0="$SW" PATH="$SW/shim:$PATH" "${cmd[@]}" 2>&1); rc=$?
  check 'all inherited Git steering isolated' 0 "$rc"
  out=$(bash "$instrument" --repo "$D" --rev "$rev_f" --scratch-root "$SW/no-round" 2>&1); rc=$?
  check 'round required' 2 "$rc"
  out=$(bash "$instrument" --repo "$D" --round 66 --scratch-root "$SW/no-rev" 2>&1); rc=$?
  check 'revision required' 2 "$rc"
  for top in /tmp /var/tmp /dev/shm; do
    out=$(bash "$instrument" --selftest --scratch-root "$top/mado-selftest-$$" 2>&1); rc=$?
    check "scratch rejects $top" 2 "$rc"
  done
  ln -s "$SW" "$SW/link"
  out=$(bash "$instrument" --selftest --scratch-root "$SW/link/not-created/child" 2>&1); rc=$?
  check 'symlink scratch parent refused' 2 "$rc"
  check 'symlink escape creates nothing' no "$([ -e "$SW/not-created" ] && printf yes || printf no)"
  # Real navigation must stay red on an empty population, never vacuously green.
  rm -- "$D/corpus/knowledge/n.md"
  printf '# directory placeholder\n' >"$D/corpus/knowledge/.keep"
  printf '# empty index\n' >"$D/corpus/README.md"
  [ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || return 2
  git -C "$D" add -A && git -C "$D" -c user.name=mado-selftest -c user.email=selftest@example.invalid -c commit.gpgsign=false commit -qm empty-population || return 2
  FIXTURE_REV=$(git -C "$D" rev-parse HEAD) || return 2
  out=$(PATH="$SW/shim:$PATH" bash "$instrument" --repo "$D" --rev "$FIXTURE_REV" --round 66 --scratch-root "$SW/empty" 2>&1); rc=$?
  check 'empty population genuine red' 1 "$rc"
  check 'empty population summary RED' yes "$([[ "$out" == *'MADO_LANDING_COUNTERS: RED (nav=1 '* ]] && printf yes || printf no)"
  printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\n' "$P" "$N"
  [ "$P" -eq "$N" ]
}
REPO= REV= SCRATCH= ROUND= SELFTEST=0
CITE_PATHS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --repo|--rev|--round|--scratch-root)
      [ $# -ge 2 ] || fail "$1 needs a value"
      case "$1" in --repo) REPO=$2 ;; --rev) REV=$2 ;; --round) ROUND=$2 ;; --scratch-root) SCRATCH=$2 ;; esac
      shift 2 ;;
    --citecheck-paths)
      shift; n=0
      while [ $# -gt 0 ] && [[ "$1" != --* ]]; do CITE_PATHS+=("$1"); shift; n=$((n+1)); done
      [ "$n" -gt 0 ] || fail '--citecheck-paths requires paths' ;;
    --selftest) SELFTEST=1; shift ;;
    --help|-h) usage; exit 0 ;;
    *) fail "unknown argument: $1" ;;
  esac
done
[ -n "$SCRATCH" ] || fail '--scratch-root is required'
# Check both lexical components and resolved location BEFORE mkdir (including missing suffixes).
case "$SCRATCH" in /*) ;; *) SCRATCH="$PWD/$SCRATCH" ;; esac
probe=$SCRATCH
while [ "$probe" != / ]; do
  [ ! -L "$probe" ] || fail 'scratch contains a symlink component'
  probe=${probe%/*}; [ -n "$probe" ] || probe=/
done
SCRATCH_ABS=$(realpath -m -- "$SCRATCH") || fail 'invalid scratch path'
case "$SCRATCH_ABS" in /|/tmp|/tmp/*|/var/tmp|/var/tmp/*|/dev/shm|/dev/shm/*) fail 'unsafe scratch root' ;; esac
mkdir -p -- "$SCRATCH_ABS" || fail 'cannot create scratch root'
if [ "$SELFTEST" -eq 1 ]; then run_selftest; exit $?; fi
[ -n "$REPO" ] && [ -n "$REV" ] || fail '--repo and --rev required'
[[ "$ROUND" =~ ^[1-9][0-9]*$ ]] || fail '--round N required (positive integer)'
[[ "$REV" != -* ]] || fail 'revision cannot begin with dash'
REPO_ABS=$(cd "$REPO" && pwd -P) || fail 'invalid repo'
REV=$(git -C "$REPO_ABS" rev-parse --verify "$REV^{commit}") || fail 'invalid revision'
[ "${#CITE_PATHS[@]}" -gt 0 ] || CITE_PATHS=(".ufo/waves/round-$ROUND/receipts")
for i in "${!CITE_PATHS[@]}"; do
  path=${CITE_PATHS[$i]}
  case "$path" in /*) ;; *) path="$REPO_ABS/$path" ;; esac
  path=$(realpath -m -- "$path") || fail 'cannot resolve citecheck path'
  case "$path" in "$REPO_ABS"/*) ;; *) fail 'citecheck paths must be inside repository for dirty guard' ;; esac
  [ -e "$path" ] || fail "citecheck path missing: $path"
  relative=${path#"$REPO_ABS/"}
  dirty=$(git -C "$REPO_ABS" --literal-pathspecs status --porcelain --untracked-files=all --ignored -- "$relative") || fail 'cannot inspect citecheck paths'
  [ -z "$dirty" ] || fail "citecheck path has uncommitted changes: $relative"
  CITE_PATHS[$i]=$path
done
verdict=GREEN exitcode=0
for leg in nav usedby ledger citecheck; do
  printf -- '-- leg %s --\n' "$leg"
  out=$("leg_$leg" 2>&1); rc=$?
  printf '%s\n' "$out"
  printf 'LANDING_LEG %s rc=%d\n' "$leg" "$rc"
  printf -v "${leg}_rc" '%d' "$rc"
  if ! marker_valid "$leg" "$rc" "$out"; then
    printf 'LANDING_CONTRACT %s ERROR (rc=%d; missing, malformed or inconsistent child marker)\n' "$leg" "$rc"
    verdict=ERROR exitcode=2
  elif [ "$rc" -eq 1 ] && [ "$exitcode" -eq 0 ]; then
    verdict=RED exitcode=1
  fi
done
printf 'MADO_LANDING_COUNTERS: %s (nav=%d usedby=%d ledger=%d citecheck=%d rev=%s)\n' "$verdict" "$nav_rc" "$usedby_rc" "$ledger_rc" "$citecheck_rc" "$REV"
exit "$exitcode"
