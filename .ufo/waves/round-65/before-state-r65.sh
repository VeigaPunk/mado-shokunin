#!/usr/bin/env bash
# mado round-65 before-state: every base counter with its own rc (QUALITY 26).
# Read-only: git read verbs, lane counters, the read-only gate. No config writes.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
SCRATCH=/fast/scratch/hyaku/mado-r65/before-state
BASE=$(git -C "$LANE" rev-parse HEAD)
mkdir -p "$SCRATCH"
cd "$LANE"
echo "== mado round-65 before-state, measured $(date -u +%Y-%m-%dT%H:%M:%SZ) at base $BASE (every producer's own rc captured, QUALITY 26) =="

echo "-- register staleness at base (the C1 deficiency) --"
cmd="grep -c 'absent (2026-10-31)' PROVINCE.md"
echo "cmd: $cmd"
grep -c 'absent (2026-10-31)' PROVINCE.md
echo "REGISTER_STALE_RC=$?"

echo "-- omarchy freshness rubric rows last state (published, dormant since r57) --"
cmd="grep -n 'surface-state audit currency' SCORECARD.md | tail -2"
echo "cmd: $cmd"
grep -n 'surface-state audit currency' SCORECARD.md | tail -2
echo "RUBRIC_GREP_RC=$?"

echo "-- used-by counter at base --"
echo "cmd: python3 quality/counters/c3-r56-used-by.py --repo . --rev $BASE --work $SCRATCH/ub"
python3 quality/counters/c3-r56-used-by.py --repo . --rev "$BASE" --work "$SCRATCH/ub"
echo "USEDBY_RC=$?"

echo "-- ledger counter at base --"
echo "cmd: python3 quality/check-tool-ledger.py --repo . --rev $BASE"
python3 quality/check-tool-ledger.py --repo . --rev "$BASE"
echo "LEDGER_RC=$?"

echo "-- ledger selftest at base bytes --"
echo "cmd: python3 quality/check-tool-ledger.py --selftest --scratch-root $SCRATCH/st"
python3 quality/check-tool-ledger.py --selftest --scratch-root "$SCRATCH/st"
echo "LEDGER_SELFTEST_RC=$?"

echo "-- wave-done selftest at base bytes --"
echo "cmd: python3 quality/check-wave-done.py --selftest --scratch-root $SCRATCH/wd"
python3 quality/check-wave-done.py --selftest --scratch-root "$SCRATCH/wd"
echo "WAVEDONE_SELFTEST_RC=$?"

echo "-- landing-counters standing instrument absent at base (the C2 deficiency) --"
cmd="ls quality/landing-counters.sh"
echo "cmd: $cmd"
ls quality/landing-counters.sh
echo "LANDINGCOUNTERS_ABSENT_RC=$? (nonzero = absent, expected before)"

echo "-- citecheck present (r64 capability) --"
cmd="git ls-tree --name-only $BASE -- tools/ | grep -c citecheck"
echo "cmd: $cmd"
git ls-tree --name-only "$BASE" -- tools/ | grep -c citecheck
echo "CITECHECK_PRESENT_RC=$?"

echo "-- gate sha at base --"
cmd="sha256sum tools/mado-verify.sh | cut -c1-16"
echo "cmd: $cmd"
sha256sum tools/mado-verify.sh | cut -c1-16
echo "SHA_RC=$?"

echo "-- navigation counter at base (SCORECARD literal block) --"
REV="$BASE" python3 - <<'PY'
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
echo "NAV_RC=$?"

echo "-- registry row count at base --"
cmd="grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md"
echo "cmd: $cmd"
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md
echo "REGISTRY_RC=$?"
echo "== before-state end =="
