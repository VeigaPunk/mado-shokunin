#!/usr/bin/env python3
"""Build the (keymap-sha, arg) -> (rc, stdout) table for MutCounterC1Draft exploit tools.

Replicates the r49 counter's Judge exactly (pinned compile-keymap + how-to-type, clean env) and records:
  - every embedded fixture (57)
  - every gen_case draw under nonce 424242 (60)
Also reports g424242 collisions with the fixture pairs (for the f-exploit corruption check).
"""
import base64
import hashlib
import importlib.util
import json
import os
import random
import subprocess
import sys

COUNTER = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49/w1/MutCounterC1Draft/c1r49-pristine.py"
OUT = "/fast/scratch/hyaku/mado-r49/MutCounterC1Draft/table.json"
NONCE = 424242

spec = importlib.util.spec_from_file_location("ctr", COUNTER)
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)

work = "/fast/scratch/hyaku/mado-r49/MutCounterC1Draft/tablebuild"
home = os.path.join(work, "judge-home")
cfg = os.path.join(work, "judge-cfg")
kmdir = os.path.join(work, "keymaps")
for d in (home, cfg, kmdir):
    os.makedirs(d, exist_ok=True)
ENV = {"PATH": "/usr/bin", "HOME": home, "XDG_CONFIG_HOME": cfg, "LC_ALL": "C"}


def compile_keymap(rmlvo):
    argv = [ctr.COMPILE, "--rules", rmlvo.get("rules") or ctr.DEFAULTS["rules"],
            "--model", rmlvo.get("model") or ctr.DEFAULTS["model"]]
    for f in ("layout", "variant", "options"):
        if rmlvo.get(f) is not None:
            argv += ["--" + f, rmlvo[f]]
    p = subprocess.run(argv, capture_output=True, timeout=60, cwd=work, env=ENV)
    if p.returncode != 0 or not p.stdout:
        return None, p.stderr.decode("utf-8", "surrogateescape")[:120]
    return p.stdout, None


def judge(kmbytes, arg):
    kmsha = hashlib.sha256(kmbytes).hexdigest()
    path = os.path.join(kmdir, kmsha[:24] + ".xkb")
    if not os.path.exists(path):
        with open(path, "wb") as fh:
            fh.write(kmbytes)
    p = subprocess.run([ctr.JUDGE, "--keymap=" + path, "--disable-compose", "--keysym", arg],
                       capture_output=True, timeout=60, cwd=work, env=ENV)
    return p.returncode, p.stdout


fx = ctr.load_fixtures()
rng = random.Random(NONCE)
gen = [ctr.gen_case(rng, k) for k in range(ctr.GEN)]
print("fixtures=%d generated=%d" % (len(fx), len(gen)), flush=True)

table = {}          # (kmsha, arg) -> [rc, b85(stdout)]
kmcache = {}        # rmlvo-tuple -> kmbytes
failures = []
for case in fx + gen:
    key = tuple((k, case["rmlvo"].get(k)) for k in ctr.RMLVO_KEYS)
    if key not in kmcache:
        km, err = compile_keymap(case["rmlvo"])
        kmcache[key] = km
        if km is None:
            failures.append(("compile", case["id"], err))
            continue
    km = kmcache[key]
    if km is None:
        continue
    rc, out = judge(km, case["arg"])
    table[(hashlib.sha256(km).hexdigest(), case["arg"])] = [rc, base64.b85encode(out).decode()]

# fixture drift check: my judge replication vs the recorded sha256
drift = []
for case in fx:
    key = tuple((k, case["rmlvo"].get(k)) for k in ctr.RMLVO_KEYS)
    km = kmcache[key]
    if km is None:
        drift.append(case["id"])
        continue
    rc, out = judge(km, case["arg"])
    if rc != case["rc"] or hashlib.sha256(out).hexdigest() != case["sha256"]:
        drift.append(case["id"])
print("fixture-drift=%s" % (drift or "none"), flush=True)
print("compile-failures=%s" % (failures or "none"), flush=True)

# g424242 collision check against fixture pairs (for the f-exploit corruption)
fxkeys = set()
for case in fx:
    key = tuple((k, case["rmlvo"].get(k)) for k in ctr.RMLVO_KEYS)
    km = kmcache.get(key)
    if km is not None:
        fxkeys.add((hashlib.sha256(km).hexdigest(), case["arg"]))
coll = []
for case in gen:
    key = tuple((k, case["rmlvo"].get(k)) for k in ctr.RMLVO_KEYS)
    km = kmcache.get(key)
    if km is None:
        continue
    kk = (hashlib.sha256(km).hexdigest(), case["arg"])
    if kk in fxkeys:
        coll.append((case["id"], case["arg"]))
print("g424242-fixture-collisions=%s" % (coll or "none"), flush=True)

ser = {"|".join(k): v for k, v in table.items()}
with open(OUT, "w") as fh:
    json.dump(ser, fh)
print("table-entries=%d bytes=%d" % (len(ser), os.path.getsize(OUT)), flush=True)
