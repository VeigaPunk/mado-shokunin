#!/usr/bin/env python3
"""MutC1ToolRandom round-50 w2 campaign runner.

Runs the landed tools/mado-keysym.py at attack rev against the pinned judge
/usr/lib/xkbcommon/xkbcli-how-to-type on the generated campaign spec.

Usage: run_campaign.py CAMPAIGN_JSON LANE_CLONE WORK_DIR OUT_DIR
Writes OUT_DIR/results.jsonl (one line per pair: ki,arg,judge_rc,tool_rc,match)
and OUT_DIR/summary.json. Keymaps compiled into WORK_DIR/keymaps/.
Clean env for every child: PATH=/usr/bin HOME/XDG under WORK_DIR, LC_ALL=C,
TMPDIR=WORK_DIR/tmp, stdin /dev/null.
"""
import concurrent.futures as cf
import hashlib
import json
import os
import subprocess
import sys
import time

JUDGE = "/usr/lib/xkbcommon/xkbcli-how-to-type"
COMPILE = "/usr/lib/xkbcommon/xkbcli-compile-keymap"
XKB_INCLUDE = "/usr/share/xkeyboard-config-2"
TIMEOUT = 60
WORKERS = 24

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def env_for(work):
    return {
        "PATH": "/usr/bin",
        "HOME": os.path.join(work, "fakehome"),
        "XDG_CONFIG_HOME": os.path.join(work, "fakehome/.config"),
        "XDG_CACHE_HOME": os.path.join(work, "fakehome/.cache"),
        "XDG_DATA_HOME": os.path.join(work, "fakehome/.local/share"),
        "XDG_STATE_HOME": os.path.join(work, "fakehome/.local/state"),
        "TMPDIR": os.path.join(work, "tmp"),
        "LC_ALL": "C",
    }

def compile_one(spec, km_path, env):
    cmd = [COMPILE, "--include=" + XKB_INCLUDE,
           "--rules=evdev", "--model=" + spec["model"],
           "--layout=" + spec["layout"], "--variant=" + spec["variant"],
           "--options=" + spec["options"]]
    with open(km_path, "wb") as out:
        r = subprocess.run(cmd, stdout=out, stderr=subprocess.DEVNULL,
                           env=env, stdin=subprocess.DEVNULL, timeout=TIMEOUT)
    return r.returncode

def run_pair(args):
    ki, arg, km_path, tool, env, jout, tout = args
    try:
        jr = subprocess.run([JUDGE, "--keymap=" + km_path, "--disable-compose",
                             "--keysym", arg], stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, env=env,
                            stdin=subprocess.DEVNULL, timeout=TIMEOUT)
        jrc, jout_b = jr.returncode, jr.stdout
    except subprocess.TimeoutExpired:
        jrc, jout_b = -1, b"TIMEOUT"
    try:
        tr = subprocess.run(["python3", "-I", tool, "how-to-type",
                             "--keymap", km_path, "--disable-compose",
                             "--keysym", arg], stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, env=env,
                            stdin=subprocess.DEVNULL, timeout=TIMEOUT)
        trc, tout_b = tr.returncode, tr.stdout
    except subprocess.TimeoutExpired:
        trc, tout_b = -1, b"TIMEOUT"
    match = (jrc == trc and jout_b == tout_b)
    if not match:
        return (ki, arg, jrc, trc, match, hashlib.sha256(jout_b).hexdigest(), hashlib.sha256(tout_b).hexdigest())
    return (ki, arg, jrc, trc, match)

def main():
    camp_path, lane, work, outdir = sys.argv[1:5]
    tool = os.path.join(lane, "tools", "mado-keysym.py")
    os.makedirs(os.path.join(work, "keymaps"), exist_ok=True)
    os.makedirs(os.path.join(work, "tmp"), exist_ok=True)
    os.makedirs(os.path.join(work, "fakehome", ".config"), exist_ok=True)
    os.makedirs(os.path.join(work, "fakehome", ".cache"), exist_ok=True)
    os.makedirs(os.path.join(work, "fakehome", ".local", "share"), exist_ok=True)
    os.makedirs(os.path.join(work, "fakehome", ".local", "state"), exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    env = env_for(work)

    camp = json.load(open(camp_path))
    specs = camp["keymaps"]
    pairs = camp["pairs"]
    exot = camp["exotic"]

    km_paths = []
    compile_fail = []
    for i, spec in enumerate(specs):
        p = os.path.join(work, "keymaps", "k%03d.xkb" % i)
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            rc = compile_one(spec, p, env)
            if rc != 0 or os.path.getsize(p) == 0:
                compile_fail.append((i, spec, rc))
        km_paths.append(p)

    mismatches = []
    n = 0
    t0 = time.time()
    res_path = os.path.join(outdir, "results.jsonl")
    with open(res_path, "w") as res, cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        args = [(ki, arg, km_paths[ki], tool, env, None, None)
                for ki, arg in pairs]
        for r in ex.map(run_pair, args, chunksize=64):
            res.write(json.dumps(r) + "\n")
            n += 1
            if not r[4]:
                mismatches.append(r)
    dt = time.time() - t0

    summ = {
        "tool_sha256": sha256_file(tool),
        "judge_sha256": sha256_file(JUDGE),
        "campaign_sha256": sha256_file(camp_path),
        "seeds": camp["seeds"],
        "algo": camp["algo"],
        "n_keymaps": len(specs),
        "compile_failures": compile_fail,
        "n_pairs_attempted": n,
        "n_pairs_compared": n - len([1 for i,_ in enumerate(specs) if i in {f[0] for f in compile_fail}]),
        "mismatches": len(mismatches),
        "mismatch_rows": [list(m) for m in mismatches[:200]],
        "elapsed_s": round(dt, 1),
    }
    with open(os.path.join(outdir, "summary.json"), "w") as fh:
        json.dump(summ, fh, indent=1)
    print(json.dumps(summ, indent=1)[:4000])

if __name__ == "__main__":
    main()
