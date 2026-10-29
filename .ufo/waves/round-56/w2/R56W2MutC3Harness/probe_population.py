#!/usr/bin/env python3
"""probe_population.py -- an extra probe (not a mutant): does judge_good validate the counter's POPULATION?

A counter stub that reports entries=0 and rows=0 (an empty registry) but is otherwise green is run against the
UNMUTATED harness.  If the harness still scores `good=ok`, the harness never checks the population it counts
against its own independently computed counts.

The probe then patches judge_good with the one-line fix (parse_line already converts e/r to int) and re-runs:
  * with the population stub  -> good=bad (the fix bites), and
  * with the REAL counter     -> good=ok controls=9/9 verdict=OK (the fix does not break the claim).
"""
import os
import shutil
import subprocess
import sys
import tempfile

S = os.environ.get("SCRATCH", "/fast/scratch/hyaku/mado-r56/R56W2MutC3Harness")
TREE = os.path.join(S, "tree")
MINI = os.path.join(S, "mini")
TARGET = "quality/r56_ctl_c3.py"
REAL_COUNTER = os.path.join(TREE, "quality", "counters", "c3-r56-used-by.py")

STUB = '''#!/usr/bin/env python3
"""stub_pop.py -- green counter stub that reports an EMPTY population (entries=0, rows=0)."""
import sys
rev = ""
a = sys.argv[1:]
for i, x in enumerate(a):
    if x == "--rev" and i + 1 < len(a):
        rev = a[i + 1]
sys.stdout.write("MADO_USED_BY: rev=%s entries=0 rows=0 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 "
                 "exempt=24 verdict=TARGET_MET missed=none\\n" % rev)
sys.exit(0)
'''

FIX_OLD = '    if rc != 0 or d["verdict"] != "TARGET_MET" or any(d["counts"].values()) or d["n"] != "24":'
FIX_NEW = ('    if rc != 0 or d["verdict"] != "TARGET_MET" or any(d["counts"].values()) or d["n"] != "24" '
           'or d["e"] != own["entries"] or d["r"] != own["rows"]:')


def mini_sha():
    with open(os.path.join(S, "mini_sha.txt")) as fh:
        return fh.read().strip()


def run(module, counter, tag):
    w = tempfile.mkdtemp(prefix="w.", dir=os.path.join(S, "mut"))
    try:
        cmd = [sys.executable, "-I", module, "--repo", MINI, "--rev", mini_sha(), "--work", w, "--counter", counter]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=w, timeout=900)
        print("%-42s rc=%d stdout=%s" % (tag, p.returncode, p.stdout.decode().strip()))
        return p.returncode, p.stdout.decode().strip(), p.stderr.decode()
    finally:
        shutil.rmtree(w, ignore_errors=True)


def main():
    stub = os.path.join(S, "stubs", "stub_pop.py")
    with open(stub, "w") as fh:
        fh.write(STUB)
    print("=== probe: the population is never checked (unmutated harness) ===")
    run(os.path.join(TREE, TARGET), stub, "unmutated harness + population stub")
    run(os.path.join(TREE, TARGET), REAL_COUNTER, "unmutated harness + real counter")

    print("\n=== the proposed one-line fix in judge_good ===")
    d = tempfile.mkdtemp(prefix="fix.", dir=os.path.join(S, "mut"))
    try:
        src = open(os.path.join(TREE, TARGET), "rb").read().decode()
        assert src.count(FIX_OLD) == 1, src.count(FIX_OLD)
        p = os.path.join(d, "r56_ctl_c3.py")
        with open(p, "w") as fh:
            fh.write(src.replace(FIX_OLD, FIX_NEW, 1))
        run(p, stub, "patched harness + population stub")
        run(p, REAL_COUNTER, "patched harness + real counter")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
