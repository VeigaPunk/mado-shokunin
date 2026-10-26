#!/usr/bin/env python3
"""Follow-up batch: the 3 mutants whose patterns collided, with tighter anchors."""
import concurrent.futures, json, os, subprocess, sys, time

SCRATCH = "/fast/scratch/hyaku/mado-r43/MutC1CounterGates"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(SCRATCH, "counter-orig.py")
CTL = os.path.join(SCRATCH, "ctl")
TMP = os.path.join(SCRATCH, "tmp")
MUT2 = os.path.join(SCRATCH, "mut2")
RES = os.path.join(SCRATCH, "results2.jsonl")
REV = "a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f"
NONCE = "42aa42aa42aa42aa"
REF = os.path.join(CTL, "REF.py")
PANEL = ["M01-fifo-block", "M04-toolarge-ge", "M27-nomatch-rc", "K1-zero-test-selftest",
         "K3-exec-model", "K4-child-interpreter", "K5-getattr", "D1-constant"]

FIX = [
    ("call-eval", 'CALL_DENY = {"exec", "eval",', 'CALL_DENY = {"exec",'),
    ("call-import", '"__import__"}', '}'),
    ("streq-builtins", '"popen",\n               "builtins", "__builtins__"',
     '"popen",\n               "__builtins__"'),
]
os.makedirs(MUT2, exist_ok=True)
src0 = open(COUNTER).read()
built = []
for name, old, new in FIX:
    n = src0.count(old)
    assert n == 1, (name, n)
    text = src0.replace(old, new)
    open(os.path.join(MUT2, name + ".py"), "w").write(text)
    compile(text, name, "exec")
    built.append(name)
print("fixed mutants built:", built)


def run_one(counter_path, tool_path, tag):
    env = dict(os.environ, C1R42_TMP=TMP)
    cmd = [sys.executable, "-I", counter_path, "--repo", LANE, "--rev", REV, "--nonce", NONCE]
    if tool_path:
        cmd += ["--tool", tool_path]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=600)
    dt = time.time() - t0
    final = [ln for ln in p.stdout.splitlines() if ln.startswith("PRED-C1-r42:")]
    cl = [ln for ln in p.stdout.splitlines() if " clauses=" in ln]
    failed = [ln.split("fixture=")[1].split(" ok=0")[0] for ln in p.stdout.splitlines() if " ok=0 " in ln]
    met = bool(final) and "TARGET_MET" in final[-1]
    return {"counter": os.path.basename(counter_path), "target": tag, "rc": p.returncode,
            "sec": round(dt, 1), "met": met,
            "final": final[-1] if final else "NO_FINAL_LINE " + (p.stdout[-160:] + p.stderr[-160:]).replace("\n", " | "),
            "clauses": cl[-1].split(" clauses=")[1] if cl else "-", "failed": failed}


jobs = []
for name in built:
    cp = os.path.join(MUT2, name + ".py")
    jobs.append((cp, REF, "REF"))
    for n in PANEL:
        jobs.append((cp, os.path.join(CTL, n + ".py"), n))
with open(RES, "w") as fh:
    with concurrent.futures.ThreadPoolExecutor(max_workers=14) as ex:
        for r in ex.map(run_one, [j[0] for j in jobs], [j[1] for j in jobs], [j[2] for j in jobs]):
            fh.write(json.dumps(r) + "\n")
print("done", len(jobs))
