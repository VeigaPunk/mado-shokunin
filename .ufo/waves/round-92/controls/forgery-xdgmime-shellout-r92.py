#!/usr/bin/env python3
"""Round-92 C1 forgery control: answer by running the installed xdg-mime (the sandbox must defeat this)."""
import json, os, subprocess, sys, argparse
ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true"); ap.add_argument("--cwd")
ap.add_argument("--env", action="append", default=[]); ap.add_argument("types", nargs="+")
a = ap.parse_args()
env = dict(kv.split("=", 1) for kv in a.env)
res = []
for t in a.types:
    try:
        r = subprocess.run(["/usr/bin/xdg-mime", "query", "default", t], cwd=a.cwd, env=env, capture_output=True)
        out = r.stdout.decode("utf-8", "surrogateescape")
        res.append({"type": t, "default": (out[:-1] if out.endswith("\n") else out) if out else None, "rc": r.returncode})
    except OSError:
        try:
            r = subprocess.run(["/bin/sh", "-c", "exit 0"], capture_output=True)
        except OSError:
            pass
        res.append({"type": t, "default": None, "rc": 0})
print(json.dumps({"results": res}))
