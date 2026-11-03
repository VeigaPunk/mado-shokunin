#!/usr/bin/env bash
# landing-counters.sh -- mado round-65 claim C2 (operability) standing landing instrument.
# Frozen contract: .ufo/waves/round-65/claims-declaration-r65.md section C2.
# Four legs (navigation / used-by / ledger / citecheck); each producer's own rc is the evidence
# (QUALITY 26). Writes only under --scratch-root; no mktemp, no network, no sleeps.
set -u

PROG=landing-counters.sh
N=0
P=0

die() { printf '%s: %s\n' "$PROG" "$*" >&2; exit 2; }
usage() {
  printf 'usage: %s --repo DIR --rev REV --scratch-root DIR [--citecheck-paths PATH ...] [--selftest]\n' "$PROG"
}
ok() { N=$((N + 1)); P=$((P + 1)); printf 'SELFTEST ok %d: %s\n' "$N" "$1"; }
bad() { N=$((N + 1)); printf 'SELFTEST FAIL %d: %s\n' "$N" "$1"; }
check_val() { # desc want got
  if [ "$2" = "$3" ]; then ok "$1 (got=$3)"; else bad "$1 (want=$2 got=$3)"; fi
}

SELF_PATH=$(readlink -f "$0") || die "cannot resolve own path"
SELF_DIR=$(cd "$(dirname "$SELF_PATH")" && pwd) || die "cannot resolve own directory"
# Sibling instruments are resolved from the script's own real path (never from cwd).
USEDBY_SIBLING="$SELF_DIR/../quality/counters/c3-r56-used-by.py"
LEDGER_SIBLING="$SELF_DIR/../quality/check-tool-ledger.py"
CITECHECK_SIBLING="$SELF_DIR/../tools/mado-receipt-citecheck.py"

# ---- leg 1: navigation, the SCORECARD literal counter body, verbatim -------------------------
leg_nav() (
  cd "$REPO_ABS" || exit 125
  REV="$REV" python3 - <<'PY'
import os, re, subprocess
from collections import Counter
rev = os.environ["REV"]
def git(*args):
    return subprocess.check_output(["git", *args], text=True)
notes = {p for p in git("ls-tree", "--name-only", rev + ":corpus/knowledge").splitlines() if p.endswith(".md")}
index = git("show", rev + ":corpus/README.md")
rows = re.findall(r"^\| `knowledge/([^`]+\.md)`", index, re.M)
counts = Counter(rows)
missing = sorted(notes - counts.keys())
dangling = sorted(counts.keys() - notes)
duplicates = sorted(p for p, n in counts.items() if n != 1)
covered = sum(counts[p] == 1 for p in notes)
print(f"revision={rev} indexed={covered}/{len(notes)} missing={len(missing)} dangling={len(dangling)} duplicates={len(duplicates)} coverage={10*covered/len(notes):.4f}/10")
for kind, paths in (("missing", missing), ("dangling", dangling), ("duplicate", duplicates)):
    for path in paths:
        print(f"{kind}: knowledge/{path}")
raise SystemExit(1 if missing or dangling or duplicates else 0)
PY
)

leg_usedby() {
  python3 "$USEDBY_SIBLING" --repo "$REPO_ABS" --rev "$REV" --work "$SCRATCH_ABS/ub"
}
leg_ledger() {
  python3 "$LEDGER_SIBLING" --repo "$REPO_ABS" --rev "$REV"
}
leg_citecheck() {
  local -a paths=("$REPO_ABS/.ufo/waves/round-65/receipts")
  if [ "${#CITE_PATHS[@]}" -gt 0 ]; then paths=("${CITE_PATHS[@]}"); fi
  python3 "$CITECHECK_SIBLING" --repo "$REPO_ABS" --rev "$REV" --paths "${paths[@]}"
}

landing_verdict() { # nav_rc usedby_rc ledger_rc citecheck_rc
  if [ "$1" -eq 0 ] && [ "$2" -eq 0 ] && [ "$3" -eq 0 ] && [ "$4" -eq 0 ]; then
    printf 'GREEN\n'
  else
    printf 'RED\n'
  fi
}
landing_exitcode() { if [ "$(landing_verdict "$@")" = GREEN ]; then printf '0\n'; else printf '1\n'; fi; }

run_selftest() {
  SELFTEST_WORK="$SCRATCH_ABS/selftest.$$"
  local SW="$SELFTEST_WORK"
  local D REV_F top out rc left leg
  rm -rf -- "$SW"
  mkdir -p -- "$SW" || { printf 'MADO_LANDING_COUNTERS_SELFTEST: 0/0 assertions passed (scratch unusable)\n'; return 2; }
  trap 'rm -rf -- "$SELFTEST_WORK"' EXIT
  if [ "${MADO_LANDING_SELFTEST_CHILD:-0}" = 1 ]; then
    mkdir -p -- "$SW/probe" || return 2
    return 0
  fi

  # a1: --rev is required in landing mode
  out=$(bash "$SELF_PATH" --repo "$SW" --scratch-root "$SW/a1" 2>&1); rc=$?
  check_val "a1 missing --rev refused" 2 "$rc"

  # a2: /tmp-family scratch roots are refused and never created
  out=$(bash "$SELF_PATH" --repo "$SW" --rev HEAD --scratch-root "/tmp/mado-r65-selftest-$$" 2>&1); rc=$?
  check_val "a2 scratch-root under /tmp refused" 2 "$rc"
  if [ -e "/tmp/mado-r65-selftest-$$" ]; then bad "a2 nothing created under /tmp"; else ok "a2 nothing created under /tmp"; fi

  # a3: a symlinked scratch root is refused
  mkdir -p -- "$SW/realroot"
  ln -s "$SW/realroot" "$SW/linkroot"
  out=$(bash "$SELF_PATH" --repo "$SW" --rev HEAD --scratch-root "$SW/linkroot" 2>&1); rc=$?
  check_val "a3 symlinked scratch-root refused" 2 "$rc"

  # a4-a6: hermetic fixture repo, every git call through -C, toplevel verified before commit
  D="$SW/fixture"
  mkdir -p "$D/corpus/knowledge" "$D/quality" "$D/.ufo/waves/round-65/receipts"
  printf '# PROVINCE\nfixture\n' >"$D/PROVINCE.md"
  printf '# corpus\n\n| note |\n| --- |\n| `knowledge/fixture-note.md` |\n' >"$D/corpus/README.md"
  printf '# SOURCES\n| id | url |\n| --- | --- |\n' >"$D/corpus/SOURCES.md"
  printf '# fixture note\n' >"$D/corpus/knowledge/fixture-note.md"
  printf '# tool ledger\nfixture\n' >"$D/quality/tool-ledger.md"
  printf 'MADO_FIXTURE: cite corpus/README.md\n' >"$D/.ufo/waves/round-65/receipts/fixture-receipt.txt"
  git -C "$D" init -q >/dev/null 2>&1
  check_val "a4 fixture git repo created" 0 "$?"
  top=$(git -C "$D" rev-parse --show-toplevel 2>/dev/null)
  check_val "a5 fixture toplevel verified before commit" "$(cd "$D" && pwd -P)" "$top"
  git -C "$D" add -A >/dev/null 2>&1
  git -C "$D" -c user.name=mado-selftest -c user.email=selftest@example.invalid \
    -c commit.gpgsign=false commit -q -m fixture >/dev/null 2>&1
  REV_F=$(git -C "$D" rev-parse HEAD 2>/dev/null)
  if [ -n "${REV_F:-}" ]; then ok "a6 fixture commit created (${REV_F:0:12})"; else bad "a6 fixture commit created"; fi

  # a7-a11: all four legs run against the fixture and their own rcs are named in the summary
  out=$(bash "$SELF_PATH" --repo "$D" --rev "$REV_F" --scratch-root "$SW/red" 2>&1); rc=$?
  for leg in nav usedby ledger citecheck; do
    if printf '%s\n' "$out" | grep -qE "^LANDING_LEG $leg rc=[0-9]+\$"; then
      ok "a7 leg $leg ran (rc captured)"
    else
      bad "a7 leg $leg ran (rc captured)"
    fi
  done
  if printf '%s\n' "$out" | grep -qE '^MADO_LANDING_COUNTERS: (GREEN|RED) \(nav=[0-9]+ usedby=[0-9]+ ledger=[0-9]+ citecheck=[0-9]+ rev=[0-9a-f]{7,40}\)$'; then
    ok "a8 summary line carries all four rcs and the rev"
  else
    bad "a8 summary line carries all four rcs and the rev"
  fi
  check_val "a9 fixture landing run exits 1 when a leg is red" 1 "$rc"

  # a10-a11: an all-green run (stub python3 exits 0) is GREEN and exits 0
  mkdir -p "$SW/shim"
  printf '#!/bin/sh\nexit 0\n' >"$SW/shim/python3"
  chmod +x "$SW/shim/python3"
  out=$(PATH="$SW/shim:$PATH" bash "$SELF_PATH" --repo "$D" --rev "$REV_F" --scratch-root "$SW/green" 2>&1); rc=$?
  case "$out" in
    *"MADO_LANDING_COUNTERS: GREEN (nav=0 usedby=0 ledger=0 citecheck=0 rev=$REV_F)"*)
      ok "a10 all four rc=0 yields GREEN" ;;
    *) bad "a10 all four rc=0 yields GREEN" ;;
  esac
  check_val "a11 all four rc=0 exits 0" 0 "$rc"

  # a12-a13: rc arithmetic directly
  check_val "a12 verdict arithmetic RED on mixed rcs" RED "$(landing_verdict 0 0 1 0)"
  check_val "a13 exit arithmetic 1 on mixed rcs" 1 "$(landing_exitcode 0 0 1 0)"

  # a14: the selftest scratch is removed on exit (observed from a bounded child run)
  out=$(MADO_LANDING_SELFTEST_CHILD=1 bash "$SELF_PATH" --selftest --scratch-root "$SW/exitprobe" 2>&1); rc=$?
  check_val "a14 exit-path child selftest rc" 0 "$rc"
  left=$(find "$SW/exitprobe" -mindepth 1 -maxdepth 1 -name 'selftest.*' 2>/dev/null | head -n1)
  if [ -z "$left" ]; then ok "a15 selftest scratch removed on exit"; else bad "a15 selftest scratch removed on exit (left: $left)"; fi

  printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\n' "$P" "$N"
  [ "$P" -eq "$N" ]
}

# ---- CLI ------------------------------------------------------------------------------------
REPO=
REV=
SCRATCH=
SELFTEST=0
CITE_PATHS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --repo) [ $# -ge 2 ] || die "--repo needs DIR"; REPO=$2; shift 2 ;;
    --rev) [ $# -ge 2 ] || die "--rev needs REV"; REV=$2; shift 2 ;;
    --scratch-root) [ $# -ge 2 ] || die "--scratch-root needs DIR"; SCRATCH=$2; shift 2 ;;
    --citecheck-paths)
      shift
      n=0
      while [ $# -gt 0 ] && [ "${1#--}" = "$1" ]; do CITE_PATHS+=("$1"); shift; n=$((n + 1)); done
      [ "$n" -gt 0 ] || die "--citecheck-paths needs at least one PATH"
      ;;
    --selftest) SELFTEST=1; shift ;;
    -h | --help) usage; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done

[ -n "$SCRATCH" ] || die "--scratch-root DIR is required"
case "$SCRATCH" in
  /tmp | /tmp/* | /var/tmp | /var/tmp/*) die "--scratch-root must not be under /tmp or /var/tmp: $SCRATCH" ;;
esac
if [ -L "$SCRATCH" ]; then die "--scratch-root must not be a symlink: $SCRATCH"; fi
mkdir -p -- "$SCRATCH" 2>/dev/null || die "--scratch-root does not exist and could not be created: $SCRATCH"
SCRATCH_ABS=$(cd "$SCRATCH" && pwd -P) || die "--scratch-root is not a usable directory: $SCRATCH"
case "$SCRATCH_ABS" in
  /tmp | /tmp/* | /var/tmp | /var/tmp/*) die "--scratch-root resolves under /tmp or /var/tmp: $SCRATCH_ABS" ;;
esac

if [ "$SELFTEST" = 1 ]; then
  run_selftest
  exit $?
fi

[ -n "$REPO" ] || die "--repo DIR is required"
[ -n "$REV" ] || die "--rev REV is required"
case "$REV" in -*) die "--rev must not start with '-': $REV" ;; esac
[ -d "$REPO" ] || die "--repo is not a directory: $REPO"
REPO_ABS=$(cd "$REPO" && pwd -P) || die "--repo is not a usable directory: $REPO"

for leg in nav usedby ledger citecheck; do
  printf -- '-- leg %s --\n' "$leg"
  "leg_$leg"
  rc=$?
  printf 'LANDING_LEG %s rc=%d\n' "$leg" "$rc"
  printf -v "${leg}_rc" '%d' "$rc"
done

verdict=$(landing_verdict "$nav_rc" "$usedby_rc" "$ledger_rc" "$citecheck_rc")
printf 'MADO_LANDING_COUNTERS: %s (nav=%d usedby=%d ledger=%d citecheck=%d rev=%s)\n' \
  "$verdict" "$nav_rc" "$usedby_rc" "$ledger_rc" "$citecheck_rc" "$REV"
[ "$verdict" = GREEN ]
exit $?
