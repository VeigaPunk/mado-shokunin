#!/usr/bin/env bash
# Round-19 final receipts (L1). Usage: final-receipts.sh COMMIT
# Each file's first line names the lane-relative producer, its sha256 at COMMIT and
# measured_commit=COMMIT (QUALITY 24); refuses when worktree tool bytes differ from COMMIT.
set -u
C=${1:?usage: final-receipts.sh COMMIT}
B=9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
LANE=$(cd "$(dirname "$0")/../../.." && pwd)
cd "$LANE" || exit 2
F=.ufo/waves/round-19/evidence/final
mkdir -p "$F"
receipt() {
  local name=$1 tool=$2; shift 2
  local want have rc
  want=$(git show "$C:$tool" | sha256sum | awk '{print $1}')
  have=$(sha256sum "$tool" | awk '{print $1}')
  if [ "$want" != "$have" ]; then echo "REFUSED $name: worktree $tool differs from $C" >&2; return 2; fi
  {
    echo "RECEIPT tool=$tool tool_sha256=$want measured_commit=$C utc=$(date -u +%FT%TZ) cmd=$*"
    "$@"; rc=$?
    echo "exit=$rc"
  } > "$F/$name.txt" 2>&1
  printf '%s %s\n' "$name" "$(tail -1 "$F/$name.txt")"
}
receipt anchor-durability-red .ufo/waves/round-19/anchor-durability.py python3 -I .ufo/waves/round-19/anchor-durability.py "$B"
receipt anchor-durability-green .ufo/waves/round-19/anchor-durability.py python3 -I .ufo/waves/round-19/anchor-durability.py "$C"
receipt supersede-sweep-red .ufo/waves/round-19/supersede-sweep.py python3 -I .ufo/waves/round-19/supersede-sweep.py "$B"
receipt supersede-sweep-green .ufo/waves/round-19/supersede-sweep.py python3 -I .ufo/waves/round-19/supersede-sweep.py "$C"
receipt measure-after .ufo/waves/round-17/measure.py python3 .ufo/waves/round-17/measure.py "$C"
receipt fresh-pins-after .ufo/waves/round-19/fresh-pins.py python3 -I .ufo/waves/round-19/fresh-pins.py "$C"
receipt tw-recall-after .ufo/waves/round-19/tw-recall.py python3 -I .ufo/waves/round-19/tw-recall.py "$C"
receipt tripwire-frozen-r19 tools/mado-tripwire.py python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-19/frozen
receipt tripwire-frozen-r18 tools/mado-tripwire.py python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen
scan_classes() { (cd .ufo/waves/round-18/frozen && python3 -I ../../../../tools/mado-tripwire.py --scan inputs/*.jsonl); }
receipt tripwire-frozen-scan-classes tools/mado-tripwire.py scan_classes
receipt token-join-check .ufo/waves/round-18/token-join-check.py python3 -I .ufo/waves/round-18/token-join-check.py "$C"
receipt gate-selftest tools/mado-verify.sh bash tools/mado-verify.sh --selftest
