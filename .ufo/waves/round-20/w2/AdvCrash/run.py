#!/usr/bin/env python3
"""Run both tripwire revisions over every fixture; report exit/label diffs."""
import json
import os
import subprocess
import sys

FIXTURES = sys.argv[1]
OUT = sys.argv[2]
TOOLS = {"28c6837": "/tmp/tw-28c6837.py", "1f7f995": "/tmp/tw-1f7f995.py"}
TIMEOUT = 20

results = []
for fn in sorted(os.listdir(FIXTURES)):
    if not fn.endswith(".jsonl"):
        continue
    path = os.path.join(FIXTURES, fn)
    row = {"fixture": fn}
    for rev, tool in TOOLS.items():
        try:
            p = subprocess.run(
                ["python3", "-I", tool, "--scan", path],
                capture_output=True, text=True, timeout=TIMEOUT)
            first = p.stdout.splitlines()[0] if p.stdout else ""
            err = ""
            try:
                err = json.loads(p.stdout.splitlines()[1]).get("error", "")
            except Exception:
                pass
            row[rev] = {"exit": p.returncode, "label": first,
                        "error": err,
                        "stderr_tail": p.stderr.strip()[-200:]}
        except subprocess.TimeoutExpired:
            row[rev] = {"exit": "timeout", "label": "", "error": "timeout>%ds" % TIMEOUT,
                        "stderr_tail": ""}
    results.append(row)

with open(OUT, "w") as fh:
    json.dump(results, fh, indent=1)

regress, both2, crash_new, timeouts = [], [], [], []
for r in results:
    a, b = r["28c6837"], r["1f7f995"]
    if a["exit"] == 2 and b["exit"] != 2:
        regress.append(r)
    if a["exit"] == 2 and b["exit"] == 2:
        both2.append(r)
    if isinstance(a["exit"], int) and a["exit"] not in (0, 1, 2):
        crash_new.append(r)
    if a["exit"] == "timeout":
        timeouts.append(r)

print("== REGRESSION: 28c6837 exit2, 1f7f995 not ==", len(regress))
for r in regress:
    print("  %-28s new:%s %r  old:%s %r" % (
        r["fixture"], r["28c6837"]["exit"], r["28c6837"]["error"],
        r["1f7f995"]["exit"], r["1f7f995"]["error"]))
print("== BOTH exit2 (pre-existing or agreed) ==", len(both2))
for r in both2:
    print("  %-28s new:%r old:%r" % (
        r["fixture"], r["28c6837"]["error"], r["1f7f995"]["error"]))
print("== 28c6837 uncaught crash (exit not 0/1/2) ==", len(crash_new))
for r in crash_new:
    print("  %-28s exit=%s stderr=%r" % (r["fixture"], r["28c6837"]["exit"],
                                         r["28c6837"]["stderr_tail"]))
print("== 28c6837 timeouts ==", len(timeouts))
for r in timeouts:
    print("  %-28s old:%s" % (r["fixture"], r["1f7f995"]["exit"]))
