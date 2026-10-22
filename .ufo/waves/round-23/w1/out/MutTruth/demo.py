#!/usr/bin/env python3
"""Concrete single-mutant demonstration on the S9 unsafe-fixture scenario.

Shows pristine refusal vs M4 (safe() gate skipped) vs restored pristine,
with byte-exact restoration evidence.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

D = Path("/fast/scratch/hyaku/mado-r23/MutTruth/scenarios/S9-unsafe-os-only")
base = (D / "truth.py").read_text()
old = ('        if not safe(code):\n'
       '            results.append(dict(id=case["id"], passed=False, error="unsafe_fixture"))\n'
       '            continue\n')
mut = base.replace(old, "")
assert mut != base


def run():
    p = subprocess.run([sys.executable, "-I", str(D / "truth.py")],
                       capture_output=True, text=True, cwd=str(D), timeout=120)
    pr = json.loads(p.stdout)
    row = [r for r in pr["results"] if r["id"] == "ProbeOnlyUnsafeOs"][0]
    return p.returncode, pr["passed"], pr["total"], row


(D / "truth.py").write_text(mut)
rc, ok, tot, row = run()
print("M4 (safe() gate skipped) on S9:")
print("   exit=%s passed=%s/%s  ProbeOnlyUnsafeOs=%s" % (rc, ok, tot, json.dumps(row)))

(D / "truth.py").write_text(base)
rc, ok, tot, row = run()
print("restored pristine on S9:")
print("   exit=%s passed=%s/%s  ProbeOnlyUnsafeOs=%s" % (rc, ok, tot, json.dumps(row)))
print("   restored sha256:", hashlib.sha256((D / "truth.py").read_bytes()).hexdigest())
print("   expected sha256:", hashlib.sha256(base.encode()).hexdigest())
