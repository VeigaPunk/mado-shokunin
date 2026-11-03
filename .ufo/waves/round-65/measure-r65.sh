#!/usr/bin/env bash
# mado round-65 measurement at the landed content commit (argv: REV). Every producer's own rc
# is captured (QUALITY 26). Read-only with respect to the lane; scratch under $HYAKU_SCRATCH only.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
REV=${1:?usage: measure-r65.sh REV}
BASE=524fa1f90b1f2de44b3019bacf833d54e0af13a0
SCRATCH=/fast/scratch/hyaku/mado-r65/meas
mkdir -p "$SCRATCH"
cd "$LANE"
echo "== mado round-65 measurement at $REV (base $BASE) $(date -u +%Y-%m-%dT%H:%M:%SZ) =="

echo "-- C1 counter at measured rev (predicate TARGET_MET) --"
echo "cmd: python3 quality/counters/c1-r65-register.py --repo . --rev $REV"
python3 quality/counters/c1-r65-register.py --repo . --rev "$REV"; echo "C1_RC=$?"

echo "-- C1 do-nothing control at base (predicate must MISS) --"
echo "cmd: python3 quality/counters/c1-r65-register.py --repo . --rev $BASE"
python3 quality/counters/c1-r65-register.py --repo . --rev "$BASE"; echo "C1_BASE_RC=$?"

echo "-- register staleness at measured rev --"
echo "cmd: git show $REV:PROVINCE.md | grep -c 'absent (2026-10-31)'"
git show "$REV:PROVINCE.md" | grep -c 'absent (2026-10-31)'; echo "STALE_RC=$?"

echo "-- C2 driver at measured rev (predicate TARGET_MET) --"
echo "cmd: python3 quality/counters/c2-r65-landing-instrument.py --repo . --rev $REV --scratch-root $SCRATCH/c2"
python3 quality/counters/c2-r65-landing-instrument.py --repo . --rev "$REV" --scratch-root "$SCRATCH/c2"; echo "C2_RC=$?"

echo "-- C2 driver control at base (predicate must MISS: instrument absent at base) --"
echo "cmd: python3 quality/counters/c2-r65-landing-instrument.py --repo . --rev $BASE --scratch-root $SCRATCH/c2base"
python3 quality/counters/c2-r65-landing-instrument.py --repo . --rev "$BASE" --scratch-root "$SCRATCH/c2base"; echo "C2_BASE_RC=$?"

echo "-- landing instrument directly at measured rev (four legs, own rc lines) --"
echo "cmd: bash quality/landing-counters.sh --repo . --rev $REV --scratch-root $SCRATCH/land"
git -C "$LANE" status --porcelain -- .ufo/waves/round-65/receipts | head -2
bash quality/landing-counters.sh --repo . --rev "$REV" --scratch-root "$SCRATCH/land"; echo "LAND_RC=$?"

echo "-- navigation counter at measured rev --"
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
raise SystemExit(1 if missing or dangling or duplicates else 0)
PY
echo "NAV_RC=$?"

echo "-- used-by counter at measured rev --"
echo "cmd: python3 quality/counters/c3-r56-used-by.py --repo . --rev $REV --work $SCRATCH/ub"
python3 quality/counters/c3-r56-used-by.py --repo . --rev "$REV" --work "$SCRATCH/ub"; echo "USEDBY_RC=$?"

echo "-- tool ledger at measured rev --"
echo "cmd: python3 quality/check-tool-ledger.py --repo . --rev $REV"
python3 quality/check-tool-ledger.py --repo . --rev "$REV"; echo "LEDGER_RC=$?"

echo "-- citecheck over round-65 receipts at measured rev --"
echo "cmd: python3 tools/mado-receipt-citecheck.py --repo . --rev $REV --paths .ufo/waves/round-65/receipts"
python3 tools/mado-receipt-citecheck.py --repo . --rev "$REV" --paths .ufo/waves/round-65/receipts; echo "CITECHECK_RC=$?"

echo "-- selftests (fail-closed checkers, caller-declared scratch) --"
echo "cmd: python3 quality/check-tool-ledger.py --selftest --scratch-root $SCRATCH/st-l"
python3 quality/check-tool-ledger.py --selftest --scratch-root "$SCRATCH/st-l" | tail -1; echo "LEDGER_ST_RC=$?"
echo "cmd: python3 quality/check-wave-done.py --selftest --scratch-root $SCRATCH/st-w"
python3 quality/check-wave-done.py --selftest --scratch-root "$SCRATCH/st-w" | tail -1; echo "WAVEDONE_ST_RC=$?"
echo "cmd: python3 tools/mado-receipt-citecheck.py --selftest --scratch-root $SCRATCH/st-c"
python3 tools/mado-receipt-citecheck.py --selftest --scratch-root "$SCRATCH/st-c" | tail -1; echo "CITECHECK_ST_RC=$?"
echo "cmd: bash quality/landing-counters.sh --selftest --scratch-root $SCRATCH/st-n"
bash quality/landing-counters.sh --selftest --scratch-root "$SCRATCH/st-n" | tail -1; echo "LANDING_ST_RC=$?"

echo "-- gate (freshness file plane + live) at measured rev; the live run is the lane's bytes --"
echo "cmd: bash tools/mado-verify.sh --no-live | tail -1 ; bash tools/mado-verify.sh | tail -1"
bash tools/mado-verify.sh --no-live | tail -1; echo "GATE_FILE_RC=${PIPESTATUS[0]}"
bash tools/mado-verify.sh | tail -1; echo "GATE_LIVE_RC=${PIPESTATUS[0]}"
echo "cmd: sha256sum tools/mado-verify.sh | cut -c1-16"
sha256sum tools/mado-verify.sh | cut -c1-16; echo "SHA_RC=$?"
echo "cmd: bash tools/mado-verify.sh --selftest | tail -1"
bash tools/mado-verify.sh --selftest | tail -1; echo "GATE_SELFTEST_RC=${PIPESTATUS[0]}"

echo "-- census at round end (fleet validator, exit 0 required) --"
echo "cmd: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado"
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado > "$SCRATCH/census-end.txt" 2>&1; echo "CENSUS_END_RC=$?"
echo "== measurement end =="
