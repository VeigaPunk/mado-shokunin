#!/usr/bin/env python3
"""MutC1CounterGates setup: copy counter, regenerate controls, benchmark one pristine run."""
import os, shutil, subprocess, sys, time, hashlib

SCRATCH = "/fast/scratch/hyaku/mado-r43/MutC1CounterGates"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality/counters/c1-r42-geometry.py")
RUNNER = os.path.join(LANE, ".ufo/waves/round-42/ctl/run-c1-controls.py")
REF = os.path.join(LANE, ".ufo/waves/round-42/c1/ctl-ref-tool.py.txt")
REV = "a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f"
NONCE = "42aa42aa42aa42aa"
CTLDIR = os.path.join(SCRATCH, "ctl")
TMP = os.path.join(SCRATCH, "tmp")
LOGS = os.path.join(SCRATCH, "logs")
for d in (CTLDIR, TMP, LOGS):
    os.makedirs(d, exist_ok=True)

# 1. pristine copy of the frozen counter (never edited in place)
dst = os.path.join(SCRATCH, "counter-orig.py")
shutil.copyfile(COUNTER, dst)
h = hashlib.sha256(open(dst, "rb").read()).hexdigest()
h0 = hashlib.sha256(open(COUNTER, "rb").read()).hexdigest()
assert h == h0 == "ed78d6930545aedc1b529f06dd3f9bce0d1ead88832ae3f53a125263a316ff99", (h, h0)

# 2. regenerate controls exactly as the frozen runner does (exec its source, no pycache writes)
src = open(RUNNER).read()
code = compile(src, RUNNER, "exec")
g = {"__name__": "ctlgen", "__file__": RUNNER}
exec(code, g)
MUTANTS, do_nothing = g["MUTANTS"], g["do_nothing"]

# reference byte-copy as a control input (the runner scores REF via --tool too)
shutil.copyfile(REF, os.path.join(CTLDIR, "REF.py"))
made = ["REF.py"]
for name, old, new in MUTANTS:
    n = open(REF).read().count(old)
    assert n == 1, (name, n)
    path = os.path.join(CTLDIR, name + ".py")
    open(path, "w").write(open(REF).read().replace(old, new))
    made.append(name + ".py")
for name, text in do_nothing().items():
    path = os.path.join(CTLDIR, name + ".py")
    open(path, "w").write(text)
    made.append(name + ".py")
print("controls generated:", len(made))

# 3. benchmark one pristine counter run on the reference
env = dict(os.environ, C1R42_TMP=TMP)
t0 = time.time()
p = subprocess.run([sys.executable, "-I", dst, "--repo", LANE, "--rev", REV,
                    "--nonce", NONCE, "--tool", os.path.join(CTLDIR, "REF.py")],
                   capture_output=True, text=True, env=env)
dt = time.time() - t0
final = [ln for ln in p.stdout.splitlines() if ln.startswith("PRED-C1-r42:")]
cl = [ln for ln in p.stdout.splitlines() if " clauses=" in ln]
failed = [ln.split("fixture=")[1].split(" ok=0")[0] for ln in p.stdout.splitlines() if " ok=0 " in ln]
print("pristine REF: rc=%d %.1fs" % (p.returncode, dt))
print(" final:", final[-1] if final else "NONE")
print(" clauses:", cl[-1].split(" clauses=")[1] if cl else "-")
print(" failed:", ",".join(failed) or "-")
open(os.path.join(LOGS, "pristine-REF.log"), "w").write(p.stdout + "\nSTDERR:\n" + p.stderr)
print("BENCH_SECONDS %.1f" % dt)
