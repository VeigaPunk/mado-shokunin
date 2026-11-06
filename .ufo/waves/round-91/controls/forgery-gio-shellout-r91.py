#!/usr/bin/env python3
"""Round-91 C1 forgery control: answer by running the oracle binary itself (no model at all).

Takes the tool's CLI (--config-home … --path … --desktop/--desktop-unset --json -- TYPES), runs
`/usr/bin/gio mime TYPE` under the same XDG environment, and prints the tool's JSON shape; when gio
cannot run (the counter's sandbox masks it) it tries libgio through ctypes, then answers "none".
It must score below the case count under the frozen counter, or the sandbox does not hide the oracle.
"""
import argparse
import ctypes
import json
import os
import re
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("types", nargs="*")
for o in ("--desktop", "--config-home", "--config-dirs", "--data-home", "--data-dirs", "--path"):
    ap.add_argument(o)
ap.add_argument("--desktop-unset", action="store_true")
ap.add_argument("--json", action="store_true")
a = ap.parse_args()
env = {"HOME": os.getcwd(), "XDG_CONFIG_HOME": a.config_home or "", "XDG_CONFIG_DIRS": a.config_dirs or "",
       "XDG_DATA_HOME": a.data_home or "", "XDG_DATA_DIRS": a.data_dirs or "", "PATH": a.path or "", "LC_ALL": "C"}
if not a.desktop_unset and a.desktop is not None:
    env["XDG_CURRENT_DESKTOP"] = a.desktop
try:
    ctypes.CDLL("libgio-2.0.so.0")
    lib = "loaded"
except OSError:
    lib = "blocked"
out = []
for t in a.types:
    res = {"type": t, "default": None, "registered": [], "recommended": []}
    try:
        r = subprocess.run(["/usr/bin/gio", "mime", t], capture_output=True, text=True, env=env, timeout=30)
        lines = r.stdout.splitlines()
        m = re.match(r"^Default application for \u201c.*\u201d: (.*)$", lines[0]) if lines else None
        if m:
            res["default"] = m.group(1)
            cur = None
            for ln in lines[1:]:
                if ln == "Registered applications:":
                    cur = "registered"
                elif ln == "Recommended applications:":
                    cur = "recommended"
                elif ln.startswith("\t") and cur:
                    res[cur].append(ln[1:])
    except (OSError, subprocess.SubprocessError):
        pass
    out.append(res)
print(json.dumps({"desktops": [], "dirs": [], "results": out, "libgio": lib}))
sys.exit(0)
