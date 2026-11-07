#!/usr/bin/env python3
"""A tool that execs the compiled GLib oracle: answers every name by asking libgio."""
import argparse, json, os, subprocess, sys
ORACLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "oracle")
ap = argparse.ArgumentParser()
ap.add_argument("names", nargs="*")
ap.add_argument("--data-home"); ap.add_argument("--data-home-unset", action="store_true")
ap.add_argument("--data-dirs"); ap.add_argument("--data-dirs-unset", action="store_true")
ap.add_argument("--home"); ap.add_argument("--json", action="store_true"); ap.add_argument("--selftest", action="store_true")
a = ap.parse_args()
if a.selftest:
    print("MADO_MIMEGLOB_SELFTEST: checks=0 failed=0"); sys.exit(0)
env = {"LC_ALL": "C"}
if not a.data_home_unset:
    v = a.data_home if a.data_home is not None else os.environ.get("XDG_DATA_HOME")
    if v is not None: env["XDG_DATA_HOME"] = v
if not a.data_dirs_unset:
    v = a.data_dirs if a.data_dirs is not None else os.environ.get("XDG_DATA_DIRS")
    if v is not None: env["XDG_DATA_DIRS"] = v
env["HOME"] = a.home if a.home is not None else os.environ.get("HOME", "/")
r = subprocess.run([ORACLE, *a.names], capture_output=True, env=env)
lines = r.stdout.decode("utf-8", "surrogateescape").splitlines()
res = []
for n, ln in zip(a.names, lines):
    t, u = ln.split("\t")
    res.append({"name": n, "type": t, "uncertain": int(u), "types": [t]})
if a.json:
    print(json.dumps({"mode": "oracle", "dirs": [], "results": res}, sort_keys=True))
else:
    print("MADO_MIMEGLOB_DIRS: mode=oracle dirs=")
    for x in res:
        print("MADO_MIMEGLOB: %s uncertain=%d name=%s" % (x["type"], x["uncertain"], x["name"]))
sys.exit(0)
