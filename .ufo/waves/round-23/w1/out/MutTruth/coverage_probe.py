#!/usr/bin/env python3
"""Which truth.py guards does the frozen 12-case repair set actually exercise?

Instruments a COPY of truth.py in scratch (never the lane) with counters that
separate "branch reached" from "branch taken", then runs it over the frozen
set. A guard whose TAKEN counter is 0 is a guard the frozen set cannot kill:
a mutant that removes it survives the frozen set by construction.
"""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair")
SCRATCH = Path("/fast/scratch/hyaku/mado-r23/MutTruth")
D = SCRATCH / "coverage"
shutil.rmtree(D, ignore_errors=True)
(D / "fixtures").mkdir(parents=True)
for f in sorted((LANE / "fixtures").iterdir()):
    shutil.copy2(f, D / "fixtures" / f.name)
shutil.copy2(LANE / "expected.json", D / "expected.json")

src = (LANE / "truth.py").read_text()
COUNTERS = '{"exact": 0, "present": 0, "forbid_nonempty": 0, "forbid_empty": 0, ' \
           '"safe_reached": 0, "unsafe_taken": 0, "child_error_reached": 0, ' \
           '"child_error_taken": 0, "cases_multicall": 0, "calls_total": 0}'

def rep(old, new):
    global src
    assert src.count(old) == 1, old
    src = src.replace(old, new)

rep("import ast, hashlib, json, subprocess, sys",
    "import ast, hashlib, json, subprocess, sys\nCOUNTS = " + COUNTERS)
rep('        forbidden = sorted(set(executed) & set(case["forbid_any"]))',
    '        forbidden = sorted(set(executed) & set(case["forbid_any"]))\n'
    '        COUNTS["forbid_nonempty" if forbidden else "forbid_empty"] += 1')
rep('        if case["kind"] == "exact":',
    '        COUNTS["exact" if case["kind"] == "exact" else "present"] += 1\n'
    '        if case["kind"] == "exact":')
rep('        if not safe(code):',
    '        COUNTS["safe_reached"] += 1\n'
    '        if not safe(code):\n'
    '            COUNTS["unsafe_taken"] += 1')
rep('        if proc.returncode != 0:',
    '        COUNTS["child_error_reached"] += 1\n'
    '        if proc.returncode != 0:\n'
    '            COUNTS["child_error_taken"] += 1')
rep('        executed = json.loads(proc.stdout)',
    '        executed = json.loads(proc.stdout)\n'
    '        COUNTS["cases_multicall"] += (1 if len(executed) > 1 else 0)\n'
    '        COUNTS["calls_total"] += len(executed)')
rep('    return 0 if ok == len(results) else 1',
    '    print("COUNTS " + json.dumps(COUNTS), file=sys.stderr)\n'
    '    return 0 if ok == len(results) else 1')

(D / "truth.py").write_text(src)
compile(src, "<instrumented>", "exec")

p = subprocess.run([sys.executable, "-I", str(D / "truth.py")],
                   capture_output=True, text=True, cwd=str(D), timeout=180)
counts = None
for line in p.stderr.splitlines():
    if line.startswith("COUNTS "):
        counts = json.loads(line[7:])
out = {"instrumented_truth_sha256": hashlib.sha256(src.encode()).hexdigest(),
       "lane_truth_sha256": hashlib.sha256((LANE / "truth.py").read_bytes()).hexdigest(),
       "exit": p.returncode, "counts": counts,
       "stderr": p.stderr.strip()[:400]}
print(json.dumps(out, indent=1))
(SCRATCH / "receipts" / "coverage.json").write_text(json.dumps(out, indent=1))
