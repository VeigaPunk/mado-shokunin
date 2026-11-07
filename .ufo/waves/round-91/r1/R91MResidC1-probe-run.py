#!/usr/bin/env python3
"""Run probe-tool.py under the frozen counter's verbatim sandbox_argv + run_tool env/cwd."""
import importlib.util, json, os, shutil, subprocess, sys, tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
S = "/fast/scratch/hyaku/mado-r91/R91MResidC1"

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

counter = load("c1_counter_r91", LANE + "/quality/counters/c1-r91-mime-resolution.py")
oracle = load("mime_oracle_r91", LANE + "/.ufo/waves/round-91/controls/mime-oracle-r91.py")

work = tempfile.mkdtemp(prefix="rsprobe-", dir=S)
sandbox = counter.sandbox_argv(LANE, work)
# probe must be visible to itself: place a copy inside work, like a scored tool copy
ppath = os.path.join(work, "mado-mime.py")
shutil.copyfile(S + "/probe-tool.py", ppath)

case = {"id": "probe", "desktop": None, "path": ["bin"], "types": ["text/plain"],
        "roots": {"config_home": "cfg", "config_dirs": [], "data_home": "home", "data_dirs": []},
        "files": {}}
root = os.path.join(work, "p0000")
os.makedirs(root)
oracle.materialise(case, root)

# exactly counter.run_tool's invocation, but we keep stdout
a = oracle.abspaths(case, root)
args = [sys.executable, "-I", ppath, "--json", "--config-home", a["config_home"], "--config-dirs", a["config_dirs"],
        "--data-home", a["data_home"], "--data-dirs", a["data_dirs"], "--path", a["path"], "--desktop-unset",
        "--", "text/plain"]
env = {"LC_ALL": "C", "HOME": root, "PATH": "/nonexistent"}
r = subprocess.run(sandbox + args, capture_output=True, text=True, env=env, timeout=60, cwd=root)
print(f"PROBE_RC={r.returncode}")
print(r.stdout)
if r.stderr.strip():
    print("PROBE_STDERR:", r.stderr.strip()[:400])
shutil.rmtree(work, ignore_errors=True)
