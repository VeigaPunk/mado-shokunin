#!/usr/bin/env python3
"""Same sandbox: HOME absent in combination with the XDG defaults that need it."""
import importlib.util, os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
WORK = "/fast/scratch/hyaku/mado-r48/ScrD1Line/boxwork"
spec = importlib.util.spec_from_file_location("c1r47", os.path.join(LANE, "quality/counters/c1-r47-terminal.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
box = mod.Box(WORK, tool_path=os.path.join(LANE, "tools/mado-terminal.py"))
root = os.path.join(WORK, "root")

cases = {
    "HOME absent, every XDG_* set": {"XDG_CONFIG_HOME": root+"/cfg", "XDG_CONFIG_DIRS": root+"/cfgdirs",
                                     "XDG_DATA_HOME": root+"/data2", "XDG_DATA_DIRS": root+"/data1",
                                     "XDG_CACHE_HOME": root+"/.rw/cache", "PATH": root+"/bin:/oracle/bin"},
    "HOME absent, XDG_CACHE_HOME absent": {"XDG_CONFIG_HOME": root+"/cfg", "XDG_CONFIG_DIRS": root+"/cfgdirs",
                                           "XDG_DATA_HOME": root+"/data2", "XDG_DATA_DIRS": root+"/data1",
                                           "PATH": root+"/bin:/oracle/bin"},
    "HOME absent, no XDG_*": {"PATH": root+"/bin:/oracle/bin"},
    "HOME set to the root's home, no XDG_*": {"HOME": root+"/home", "PATH": root+"/bin:/oracle/bin"},
}
for label, env in cases.items():
    o = box.run(root, env, False, ["--print-id"])
    t = box.run(root, env, True, ["print", "--print-id"])
    print("%-42s pin rc=%d out=%r | tool rc=%d out=%r" % (label, o[0], o[1], t[0], t[1]))
print("trips:", box.trips)
