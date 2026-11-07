#!/usr/bin/env python3
"""R91MResidC1: run the FROZEN candidate on the rs fixtures under the counter's own sandbox.

Imports the frozen counter module (sha256 91ef46d17e0398c315f6b9ef3e5597ce67f105d93cc723b413cc1680576ede26)
and uses its sandbox_argv / run_tool / correct verbatim, so this is exactly the measurement
environment, only pointed at the new fixtures.
"""
import importlib.util, json, os, sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
S = "/fast/scratch/hyaku/mado-r91/R91MResidC1"

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

counter = load("c1_counter_r91", LANE + "/quality/counters/c1-r91-mime-resolution.py")
oracle = load("mime_oracle_r91", LANE + "/.ufo/waves/round-91/controls/mime-oracle-r91.py")

doc = json.load(open(sys.argv[1] if len(sys.argv) > 1 else S + "/rs-labelled.json", encoding="utf-8"))
cases = doc["cases"]
assert doc["oracle"]["gio_sha256"] == counter.sha(counter.GIO)
assert doc["oracle"]["libgio_sha256"] == counter.sha(counter.LIBGIO)

import shutil, tempfile
work = tempfile.mkdtemp(prefix="rsdrv-", dir=S)
# the sandbox tmpfs's the scratch root and binds only `work` back — like the counter's
# write_tool(), the scored copy must live INSIDE work or it is invisible to the tool
CAND = os.path.join(work, "mado-mime.py")
shutil.copyfile(S + "/mado-mime.frozen.py", CAND)
sandbox = counter.sandbox_argv(LANE, work)

bad = 0
for i, c in enumerate(cases):
    root = os.path.join(work, f"r{i:04d}")
    os.makedirs(root)
    oracle.materialise(c, root)
    ans = counter.run_tool(CAND, c, root, oracle, sandbox)
    ok = counter.correct(ans, c["expect"])
    if not ok:
        bad += 1
        print(f"DISAGREE {c['id']}")
        print(f"  expect: {json.dumps(c['expect'], sort_keys=True)}")
        print(f"  got:    {json.dumps(ans, sort_keys=True)}")
    else:
        print(f"ok {c['id']}")
        for t, lab in c["expect"].items():
            print(f"    {t}: default={lab['default']} registered={lab['registered']} recommended={lab['recommended']}")

print(f"RS_SUMMARY: cases={len(cases)} disagree={bad}")
sys.exit(1 if bad else 0)
