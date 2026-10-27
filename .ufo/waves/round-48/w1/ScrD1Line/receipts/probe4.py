#!/usr/bin/env python3
"""HOME-unset probe inside the C1 counter's own sandbox (Box.argv: /usr/lib, bash as /bin/sh, no /etc)."""
import importlib.util, os, sys, json

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality/counters/c1-r47-terminal.py")
WORK = "/fast/scratch/hyaku/mado-r48/ScrD1Line/boxwork"
TOOL = os.path.join(LANE, "tools/mado-terminal.py")

os.makedirs(WORK, exist_ok=True)
spec = importlib.util.spec_from_file_location("c1r47", COUNTER)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

box = mod.Box(WORK, tool_path=TOOL)
print("sandbox externals:", sorted(os.listdir(box.bin)))

root = os.path.join(WORK, "root")
os.makedirs(os.path.join(root, "data1/applications"), exist_ok=True)
os.makedirs(os.path.join(root, "data2/applications"), exist_ok=True)
os.makedirs(os.path.join(root, "cfg"), exist_ok=True)
os.makedirs(os.path.join(root, "cfgdirs"), exist_ok=True)
os.makedirs(os.path.join(root, "home"), exist_ok=True)
os.makedirs(os.path.join(root, ".rw/cache"), exist_ok=True)
open(os.path.join(root, "data1/applications/term.desktop"), "w").write(
    "[Desktop Entry]\nType=Application\nName=t\nCategories=TerminalEmulator;\nExec=ls\nTryExec=ls\n")

base_env = {"XDG_CONFIG_HOME": root + "/cfg", "XDG_CONFIG_DIRS": root + "/cfgdirs",
            "XDG_DATA_HOME": root + "/data2", "XDG_DATA_DIRS": root + "/data1",
            "XDG_CACHE_HOME": root + "/.rw/cache", "PATH": root + "/bin:/oracle/bin"}

for label, env in (("with HOME (the counter's case_env shape)", dict(base_env, HOME=root + "/home")),
                   ("HOME absent", dict(base_env))):
    print("\n==", label, "==")
    o = box.run(root, env, False, ["--print-id"])
    print("pin  rc=%d out=%r" % o)
    t = box.run(root, env, True, ["print", "--print-id"])
    print("tool rc=%d out=%r" % t)

print("\ntrips:", box.trips)
