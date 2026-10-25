#!/usr/bin/env python3
"""Rejected-candidate measurement for the w1 SimpMergeUnify seat (evidence only).

The other way to make the two merges share one comparison: feed the
`--getoption` records through `native_equal` and delete `values_equal`
(DESIGN-A).  It is shorter, and it is NOT behaviour-preserving: measured
against the BASE tool on the BASE selftest's own fixtures, on the counter's
nine generated dumps and on the host capture dump.
"""
import hashlib
import importlib.util
import json
import os
import random
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = LANE + "/.ufo/waves/round-40/w1/SimpMergeUnify"
REV = "5e7e88525cc539563de7746361b2650802e81809"
CTR = LANE + "/quality/counters/c1-r40-live.py"
CAP = LANE + "/.ufo/waves/round-40/c1/native-capture.jsonl"
tmp = tempfile.mkdtemp(prefix="design-a-")

base = os.path.join(tmp, "base.py")
with open(base, "wb") as fh:
    fh.write(subprocess.run(["git", "-C", LANE, "show",
                             REV + ":tools/mado-options.py"],
                            capture_output=True, check=True).stdout)
src = open(SEAT + "/unified.py").read()
design_a = src.replace(
    "merge_rows(rows, st.options, live.get, live, equal=values_equal)",
    "merge_rows(rows, st.options, live.get, live)")
assert design_a != src
da = os.path.join(tmp, "design-a.py")
with open(da, "w") as fh:
    fh.write(design_a)

spec = importlib.util.spec_from_file_location("c1ctr", CTR)
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)


def run(tool, home, extra):
    p = subprocess.run([sys.executable, "-I", tool, "--home", home] + extra,
                       capture_output=True, text=True)
    return p.returncode, p.stdout


def labels(stdout):
    return {r["key"]: r.get("agreement") for r in json.loads(stdout)}


def flips(a, b):
    la, lb = labels(a[1]), labels(b[1])
    return [(k, la[k], lb[k]) for k in la if la[k] != lb.get(k)]


def file_dump(table):
    out = {}
    for key, rec in table.items():
        if not rec:
            continue
        form = [f for f in ctr.FORMS if f in rec][0]
        out[key] = {"value": rec[form], "custom_type": form,
                    "set": bool(rec["set"])}
    return out


# S1 — the BASE selftest's own fixture tree and live.json
DRIVER = '''
import os, runpy, shutil, sys, tempfile
root, tool = sys.argv[2], sys.argv[1]
def mkdtemp(prefix=None, suffix=None, dir=None):
    os.makedirs(root, exist_ok=True)
    return root
tempfile.mkdtemp = mkdtemp
shutil.rmtree = lambda *a, **k: None
sys.argv = [tool, "--selftest"]
try:
    runpy.run_path(tool, run_name="__main__")
except SystemExit:
    pass
'''
driver = os.path.join(tmp, "driver.py")
with open(driver, "w") as fh:
    fh.write(DRIVER)
root = os.path.join(tmp, "st")
subprocess.run([sys.executable, "-I", driver, base, root],
               capture_output=True, text=True)
home = os.path.join(root, "home")
live = os.path.join(root, "live.json")
a = run(base, home, ["--getoption", live])
b = run(da, home, ["--getoption", live])
print("S1 selftest fixture: byte-identical=%s bytes=%d/%d"
      % (a[1] == b[1], len(a[1]), len(b[1])))
for f in flips(a, b):
    print("   flip %-26s BASE=%-11s DESIGN-A=%s" % f)

# S2 — the counter's nine dumps (native-typed records)
total = 0
for i in list(range(8)) + ["probe"]:
    if i == "probe":
        fx = ctr.small_fixture(REV, "probe")
        extra = {"zzprobe:one": {"option": "zzprobe:one", "int": 3,
                                 "set": False},
                 "zzprobe:two": {"option": "zzprobe:two", "str": "q",
                                 "set": False}}
    else:
        seed = int(hashlib.sha256(("%s:%d" % (REV, i)).encode()).hexdigest(),
                   16)
        fx = ctr.Fixture(random.Random(seed), "x%d" % i)
        fx.build()
        extra = {}
    h = os.path.join(tmp, "h%s" % i)
    fx.render(h)
    table = fx.table()
    table.update(extra)
    dump = os.path.join(tmp, "d%s.json" % i)
    with open(dump, "w") as fh:
        json.dump(file_dump(table), fh)
    a = run(base, h, ["--getoption", dump])
    b = run(da, h, ["--getoption", dump])
    n = len(flips(a, b))
    total += n
    print("   x%-5s byte-identical=%-5s flips=%d" % (i, a[1] == b[1], n))
print("S2 counter dumps: total flips=%d" % total)

# S3 — the host capture as a file dump
capture = {}
with open(CAP) as fh:
    for line in fh:
        if line.strip():
            o = json.loads(line)
            capture[o["option"]] = o
dump = os.path.join(tmp, "host.json")
with open(dump, "w") as fh:
    json.dump(file_dump(capture), fh)
a = run(base, os.path.expanduser("~"), ["--getoption", dump])
b = run(da, os.path.expanduser("~"), ["--getoption", dump])
f = flips(a, b)
print("S3 host dump: byte-identical=%s flips=%d/%d"
      % (a[1] == b[1], len(f), len(labels(a[1]))))
for row in f:
    print("   flip %-34s BASE=%-11s DESIGN-A=%s" % row)
print("scratch=%s" % tmp)
