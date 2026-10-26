#!/bin/bash
# RerunControlsV2 verify: every tally in report.md is re-derived here from files on disk.
set -u
L=/home/vgpnk/Projects/shokunin/mado-shokunin
S=$L/.ufo/waves/round-43/w2/RerunControlsV2
norm() { grep -v '^exit=' "$1"; }

echo "== python =="; python3 --version
echo "== counter sha (claim: 9a83407...) =="
sha256sum "$L/quality/counters/c2-r43-gkeep-entry-v2.py"

echo
echo "== controls: committed vs rerun =="
diff <(norm "$L/.ufo/waves/round-43/receipts/ctl-c2-v2.txt") "$S/ctl-c2-v2.rerun.txt" \
  && echo "IDENTICAL (modulo the invoker's 'exit=' line)"
echo "control lines: committed=$(grep -c '^control=' "$L/.ufo/waves/round-43/receipts/ctl-c2-v2.txt") rerun=$(grep -c '^control=' "$S/ctl-c2-v2.rerun.txt")"
echo "ok=1 lines:    committed=$(grep -c 'ok=1$' "$L/.ufo/waves/round-43/receipts/ctl-c2-v2.txt") rerun=$(grep -c 'ok=1$' "$S/ctl-c2-v2.rerun.txt")"
echo "final: $(tail -1 "$S/ctl-c2-v2.rerun.txt")"

echo
echo "== forge: committed vs rerun =="
diff <(norm "$L/.ufo/waves/round-43/ctl/v2-forgeries/forge-v2.log") "$S/forge-v2.rerun.log" \
  && echo "IDENTICAL (modulo 'exit=')"
echo "ADMITTED by name (rerun):"; grep ' ADMITTED$' "$S/forge-v2.rerun.log" | sed 's/^### //;s/ .*//' | tr '\n' ' '; echo
echo "rejected by name (rerun):"; grep ' rejected$' "$S/forge-v2.rerun.log" | sed 's/^### //;s/ .*//' | tr '\n' ' '; echo
echo "final: $(grep '^=== ' "$S/forge-v2.rerun.log")"

echo
echo "== more: committed vs rerun =="
diff <(norm "$L/.ufo/waves/round-43/ctl/v2-forgeries/more-v2.log") "$S/more-v2.rerun.log" \
  && echo "IDENTICAL (modulo 'exit=')"
echo "admitted by name (rerun):"; grep -E 'admitted=1/1' "$S/more-v2.rerun.log" | sed 's/^\(probe=[^ ]* \)\?//;s/ *rc=.*//' | tr '\n' ' '; echo
echo "rejected by name (rerun):"; grep -E 'admitted=0/1' "$S/more-v2.rerun.log" | sed 's/^\(probe=[^ ]* \)\?//;s/ *rc=.*//' | tr '\n' ' '; echo

echo
echo "== fixture dumps: committed vs rerun =="
diff -r "$L/.ufo/waves/round-43/ctl/v2-forgeries/fixtures" "$S/fixtures" && echo "IDENTICAL tree"
echo "files: committed=$(find "$L/.ufo/waves/round-43/ctl/v2-forgeries/fixtures" -type f | wc -l) rerun=$(find "$S/fixtures" -type f | wc -l)"

echo
echo "== teeth =="
for m in v2 v1 always-admit; do echo "$m: $(tail -1 "$S/teeth-$m.txt")"; done

echo
echo "== controls are v2-specific in their clause columns =="
echo "v1 vs v2 committed control receipts, changed lines: $(diff "$L/.ufo/waves/round-43/receipts/ctl-c2.txt" "$L/.ufo/waves/round-43/receipts/ctl-c2-v2.txt" | grep -c '^[<>]')"
echo "of which clause i:1 -> i:0 flips: $(diff "$L/.ufo/waves/round-43/receipts/ctl-c2.txt" "$L/.ufo/waves/round-43/receipts/ctl-c2-v2.txt" | grep -c '^>.*i:0')"

echo
echo "== quotes cited in report.md, located and grepped =="
grep -Fn 'still admitted: A1, A2, D1, E2, H1, X1' .ufo/waves/round-43/registration-v2.md | sed 's/^/registration-v2.md:/'
grep -Fn 'CTL_C2: controls=74 correct=74/74' .ufo/waves/round-43/registration-v2.md | sed 's/^/registration-v2.md:/'
grep -Fn '=== forged fixtures admitted by the frozen counter: 6/15' .ufo/waves/round-43/ctl/v2-forgeries/forge-v2.log | sed 's/^/forge-v2.log:/'
grep -Fn 'CTL_C2: controls=74 correct=74/74' .ufo/waves/round-43/w2/RerunControlsV2/ctl-c2-v2.rerun.txt | sed 's/^/rerun:/'

echo
echo "== the v1->v2 source of the 23 changed control lines (clause-i only?) =="
python3 - "496340d" <<'PY'
import subprocess, sys
rev = sys.argv[1]
def lines(p):
    t = subprocess.run(["git", "show", "%s:%s" % (rev, p)], capture_output=True, text=True).stdout
    return {l.split()[0].split("=", 1)[1]: l for l in t.splitlines() if l.startswith("control=")}
A = lines(".ufo/waves/round-43/receipts/ctl-c2.txt")
B = lines(".ufo/waves/round-43/receipts/ctl-c2-v2.txt")
assert set(A) == set(B)
d = [n for n in A if A[n] != B[n]]
only = all(A[n].split("clauses=")[1].split(" admitted")[0].replace("i:1", "i:0")
           == B[n].split("clauses=")[1].split(" admitted")[0] for n in d)
same_ok = all(A[n].split(" ok=")[1] == B[n].split(" ok=")[1] for n in d)
print("controls=%d differing=%d only-i-changed=%s ok-unchanged=%s" % (len(A), len(d), only, same_ok))
PY
