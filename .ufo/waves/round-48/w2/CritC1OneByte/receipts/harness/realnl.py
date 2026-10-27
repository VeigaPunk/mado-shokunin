import importlib.util, json, os, shutil
S = "/fast/scratch/hyaku/mado-r48/CritC1OneByte"
R = S + "/repo/r48"
def load(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
ctr = load("ctr", R + "/quality/counters/c1-r48-terminal-cache.py")
box = ctr.Box(S + "/work", R + "/tools/mado-terminal.py")
WD = S + "/work/realnl"
shutil.rmtree(WD, ignore_errors=True); os.makedirs(WD)
LANG = "C.UTF-8"
entry = ("[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\n"
         "Exec=foot \"a\\nb\"\nName=Terminal\n")
case = {"id": "REAL-NL", "class": "WARM-SAME",
        "env": {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
                "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share",
                "XDG_CURRENT_DESKTOP": "Hyprland"},
        "files": {"home/.config/hyprland-xdg-terminals.list": "foot.desktop\n",
                  "usr/share/applications/foot.desktop": entry},
        "exec": ["bin/foot"], "args": ["--print-cmd"], "mtime": 1600000000,
        "prime": {"args": ["--print-cmd"]}, "expect": {"rc": 0, "stdout": ""}}
root = WD + "/r"
ctr.prepare(box, root, case, LANG)
data = open(ctr.cache_host(root), "rb").read()
print("cache %d bytes, %d lines:" % (len(data), len(data.split(b"\n"))))
for i, ln in enumerate(data.split(b"\n"), 1):
    print("%2d %r" % (i, ln))
o = ctr.oracle_side(box, case, root, LANG)
print("pin oracle:", o)
env = ctr.case_env(case, root, LANG, "scored")
print("tool print:", box.run(root, env, True, ["print", "--print-cmd"]))
rc, out, err = box.run(root, env, True, ["explain"])
print("tool explain rc=%r\n%s" % (rc, out[-300:]))
