#!/usr/bin/env python3
"""Read-only probe of what a tool can see inside the PRED-C1-r42 sandbox.

Run exactly the way the counter runs a tool (`sandbox_cmd` + prlimit --nproc=1:1),
with the same ro-binds. Prints one JSON object; nothing is written outside /tmp.
"""
import json
import os
import sys


def probe(path):
    try:
        st = os.lstat(path)
        return {"ok": True, "mode": oct(st.st_mode), "regular": os.path.isfile(path) if not os.path.islink(path) else False}
    except OSError as exc:
        return {"ok": False, "err": exc.__class__.__name__, "errno": exc.errno}


def listing(path):
    try:
        return sorted(os.listdir(path))
    except OSError as exc:
        return {"err": exc.__class__.__name__, "errno": exc.errno}


cwd = os.getcwd()
parent = os.path.dirname(cwd)
out = {
    "cwd": cwd,
    "argv0": sys.argv[0],
    "env": dict(os.environ),
    "root": listing("/"),
    "cwd_listing": listing(cwd),
    "parent": parent,
    "parent_listing": listing(parent),
    "grandparent_listing": listing(os.path.dirname(parent)),
    "tmp_listing": listing("/tmp"),
    "home_probe": probe("/home"),
    "home_vgpnk": probe("/home/vgpnk"),
    "lane_probe": probe("/home/vgpnk/Projects/shokunin/mado-shokunin"),
    "counter_probe": probe("/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r42-geometry.py"),
    "ref_probe": probe("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-42/c1/ctl-ref-tool.py.txt"),
    "usr_bin_count": len(listing("/usr/bin")) if isinstance(listing("/usr/bin"), list) else listing("/usr/bin"),
    "proc_self": probe("/proc/self"),
    "proc_pids": [p for p in listing("/proc") if p.isdigit()] if isinstance(listing("/proc"), list) else listing("/proc"),
    "sibling_dir": probe(os.path.join(parent, "sibling-fixed")),
    "sibling_file": probe(os.path.join(parent, "sibling-fixed", "c.json")),
    "scratch_root": probe("/fast/scratch/hyaku/mado-r43"),
}
try:
    with open("/tmp/probe-write", "w") as fh:
        fh.write("x")
    out["tmp_write"] = True
except OSError as exc:
    out["tmp_write"] = exc.__class__.__name__
try:
    with open(os.path.join(cwd, "probe-write"), "w") as fh:
        fh.write("x")
    out["cwd_write"] = True
except OSError as exc:
    out["cwd_write"] = exc.__class__.__name__
try:
    with open(os.path.join(parent, "probe-write"), "w") as fh:
        fh.write("x")
    out["parent_write"] = True
except OSError as exc:
    out["parent_write"] = exc.__class__.__name__
print(json.dumps(out, sort_keys=True))
