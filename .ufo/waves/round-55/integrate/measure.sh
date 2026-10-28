#!/usr/bin/env bash
# L1 final measurement (round 55): every counting command of the report against ONE content revision, outputs and exit codes verbatim.
# usage: measure.sh <rev> <scratch-work-dir>      run from the lane root
set -u
R=$1; W=$2; mkdir -p "$W"
run() { echo "\$ $*"; "$@" 2>&1; echo "exit=$?"; echo; }
echo "== measured at $R $(date -Is) =="
run python3 -I quality/counters/c1-r55-kbd-entry.py --repo . --rev "$R" --work "$W"
run python3 -I quality/check-r55-controls.py --claim c1 --repo . --rev "$R" --work "$W"
run python3 -I quality/check-r55-controls.py --claim c2 --repo . --rev "$R" --work "$W"
run python3 -I quality/counters/c3-r55-p19.py --repo . --rev "$R" --work "$W"
run python3 -I quality/check-r55-controls.py --claim c3 --repo . --rev "$R" --work "$W"
run python3 -I quality/check-freeze-order.py --repo . --rev fe03bb3b2ec05fbf906b83096c637fd6a05b3dc8 --round 54 --wave w1 --work "$W"
run python3 -I quality/check-freeze-order.py --repo . --rev "$R" --round 55 --wave w1 --work "$W"
run python3 -I quality/check-freeze-order.py --repo . --rev "$R" --round 55 --wave w2 --work "$W"
run python3 -I quality/check-wave-done.py --repo . --rev "$R" --round 55
run python3 -I quality/check-index.py --rev "$R" --repo .
run python3 -I quality/check-tool-ledger.py --repo . --rev "$R"
run python3 -I tools/mado-kbdopts.py --selftest
run python3 -I quality/check-freeze-order.py --selftest --work "$W"
run python3 -I quality/counters/c1-r55-kbd-entry.py --selftest --repo . --rev "$R" --work "$W"
run python3 -I quality/counters/c3-r55-p19.py --selftest --repo . --rev "$R" --work "$W"
echo "\$ TMPDIR=$W bash tools/mado-verify.sh --selftest"; TMPDIR=$W bash tools/mado-verify.sh --selftest 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"; echo
echo "\$ sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado"; /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado 2>&1; echo "exit=$?"
echo "\$ registry rows"; grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
echo "\$ knowledge files / README index rows"; git ls-tree -r --name-only "$R" corpus/knowledge | wc -l; git show "$R:corpus/README.md" | grep -cE '^\| `knowledge/'
