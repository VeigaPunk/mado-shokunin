#!/usr/bin/env python3
"""MutSelftestFixtures driver: run ctl-ref-tool.py.txt --selftest on pristine
and on each of the 16 MUTANTS from ctl/run-c1-controls.py (same
ref.replace(old, new, 1) semantics as the controls runner).

Scratch copies live in a mktemp dir; the original ref file is never touched.
"""
import hashlib
import importlib.util
import os
import subprocess
import sys
import tempfile

REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/c1/ctl-ref-tool.py.txt"
CONTROLS = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/ctl/run-c1-controls.py"

spec = importlib.util.spec_from_file_location("c1ctl", CONTROLS)
c1ctl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1ctl)
MUTANTS = c1ctl.MUTANTS

ref = open(REF, encoding="utf-8").read()
ref_sha = hashlib.sha256(ref.encode()).hexdigest()
tmp = tempfile.mkdtemp(prefix="mutselftest-")


def run_selftest(path):
    p = subprocess.run([sys.executable, "-I", path, "--selftest"],
                       capture_output=True, text=True, cwd=tmp, timeout=240)
    return p.returncode, p.stdout, p.stderr


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


pristine = os.path.join(tmp, "pristine.py")
open(pristine, "w", encoding="utf-8").write(ref)
rc, out, err = run_selftest(pristine)
base_line = out.strip().splitlines()[-1] if out.strip() else ""
print("BASE rc=%d line=%r sha=%s" % (rc, base_line, sha(pristine)))
base_ok = rc == 0 and "MADO_OPTIONS_SELFTEST: 71/71 passed" in out
print("BASE_OK=%d" % base_ok)
if err.strip():
    print("BASE stderr tail: %r" % err.strip()[-400:])

rows = []
for name in sorted(MUTANTS):
    old, new = MUTANTS[name]
    n = ref.count(old)
    mutated = ref.replace(old, new, 1)
    path = os.path.join(tmp, name + ".py")
    open(path, "w", encoding="utf-8").write(mutated)
    rc, out, err = run_selftest(path)
    line = out.strip().splitlines()[-1] if out.strip() else ""
    survived = (rc == 0 and "MADO_OPTIONS_SELFTEST: 71/71 passed" in out)
    if survived:
        verdict = "SURVIVED"
    elif "MADO_OPTIONS_SELFTEST" in out or "selftest FAIL" in err:
        verdict = "KILLED-assertion"
    elif "Traceback" in err:
        verdict = "KILLED-crash"
    else:
        verdict = "KILLED-other"
    fails = [l for l in err.splitlines() if l.startswith("selftest FAIL")]
    print("%s occ=%d rc=%d line=%r verdict=%s sha=%s" % (name, n, rc, line, verdict, sha(path)))
    for f in fails[:3]:
        print("    %s" % f)
    if verdict == "KILLED-crash":
        tb = [l for l in err.splitlines() if l.strip().startswith("File ") or "Error" in l]
        for t in tb[-3:]:
            print("    TB %s" % t.strip())
    rows.append((name, n, rc, verdict))

print("SUMMARY total=%d survived=%d killed=%d" % (
    len(rows), sum(1 for r in rows if r[3] == "SURVIVED"),
    sum(1 for r in rows if r[3] != "SURVIVED")))
print("SCRATCH=%s" % tmp)
print("REF_SHA=%s" % ref_sha)
print("REF_STILL=%s" % hashlib.sha256(open(REF, "rb").read()).hexdigest())
