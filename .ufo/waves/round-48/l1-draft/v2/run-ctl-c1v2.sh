#!/usr/bin/env bash
# L1 (attempt 3): score PRED-C1-r48-v2 on the complete control set (l1-draft/v2/ctl/*.py: the 19 w1 controls, the 6
# w1 refA mutants and every w2 candidate) plus the frozen reference, the landed tool, the base tool and an absent tool.
# PASS iff every control is TARGET_MISSED (an absent tool's setup exit 2 counts as a miss) and the landed tool is
# TARGET_MET. The frozen v1 reference is reported, not required: v2 scores explain's escaped `\n` (fixture L1-34).
# Usage: run-ctl-c1v2.sh [PARALLEL]   (receipts under receipts/v2/ctl/, summary receipts/v2/ctl-c1v2.txt)
set -u
W=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48
L=/home/vgpnk/Projects/shokunin/mado-shokunin
P=${1:-10}
R=$W/receipts/v2/ctl
mkdir -p "$R"
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mado-r48/L1ctl
mkdir -p "$S"
git -C "$L" show 579f694b45c797a9c39761fdb4f9e0a1b71b3585:tools/mado-terminal.py > "$S/base-tool.py"
{
  echo "REF $W/l1-draft/mado-terminal.py"
  echo "FINAL $L/tools/mado-terminal.py"
  echo "BASE $S/base-tool.py"
  echo "ABSENT -"
  for f in "$W"/l1-draft/v2/ctl/*.py; do echo "$(basename "$f" .py) $f"; done
} > "$S/list"
xargs -P "$P" -L 1 bash -c 'TAILN=0 "$0"/l1-draft/v2/c1v2-score.sh "$2" "ctl-$1" "$0/receipts/v2/ctl/$1.txt" 4848 >/dev/null' "$W" < "$S/list"
fail=0; met_ctl=0; n=0
{
  printf '# CTL_C1v2 counter_sha256=%s fixtures_sha256=%s nonce=4848\n' \
    "$(sha256sum "$W/l1-draft/v2/c1-r48-terminal-cache-v2.py" | cut -d' ' -f1)" \
    "$(sha256sum "$W/l1-draft/v2/c1-r48-fixtures-v2.json" | cut -d' ' -f1)"
  while read -r tag path; do
    line=$(grep '^PRED-C1-r48-v2: ' "$R/$tag.txt" | tail -1)
    [ -n "$line" ] || line="NO-VERDICT $(grep -m1 SETUP "$R/$tag.txt")"
    case "$tag" in
      FINAL) want=TARGET_MET ;;
      REF) want=REPORT ;;
      *) want=TARGET_MISSED; n=$((n + 1)) ;;
    esac
    got=MISSING; case "$line" in *verdict=TARGET_MET*) got=TARGET_MET ;; *verdict=TARGET_MISSED*) got=TARGET_MISSED ;; esac
    [ "$tag" = ABSENT ] && [ "$got" = MISSING ] && grep -q '^exit=2' "$R/$tag.txt" && got=TARGET_MISSED
    ok=ok; [ "$want" = REPORT ] || [ "$got" = "$want" ] || { ok=BAD; fail=$((fail + 1)); }
    case "$tag" in REF|FINAL) ;; *) [ "$got" = TARGET_MET ] && met_ctl=$((met_ctl + 1)) ;; esac
    printf '%s %s want=%s %s\n' "$ok" "$tag" "$want" "${line#PRED-C1-r48-v2: }"
  done < "$S/list"
  v=PASS; [ "$fail" = 0 ] || v=FAIL
  printf 'CTL_C1v2 VERDICT: %s (controls scoring TARGET_MET: %d of %d; landed tool must meet; bad=%d)\n' "$v" "$met_ctl" "$n" "$fail"
} > "$W/receipts/v2/ctl-c1v2.txt"
rm -rf "$S"
tail -1 "$W/receipts/v2/ctl-c1v2.txt"
