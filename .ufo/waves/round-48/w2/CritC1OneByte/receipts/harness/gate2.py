import importlib.util, json, os, shutil, subprocess
S = "/fast/scratch/hyaku/mado-r48/CritC1OneByte"
R = S + "/repo/r48"
def load(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
ctr = load("ctr", R + "/quality/counters/c1-r48-terminal-cache.py")
box = ctr.Box(S + "/work", R + "/tools/mado-terminal.py")
WD = S + "/work/gate2"; shutil.rmtree(WD, ignore_errors=True); os.makedirs(WD)
LANG = "C.UTF-8"
case = {"id": "GATE", "class": "WARM-SAME",
        "env": {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
                "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share",
                "XDG_CURRENT_DESKTOP": "Hyprland"},
        "files": {"home/.config/hyprland-xdg-terminals.list": "foot.desktop\n",
                  "usr/share/applications/foot.desktop":
                      "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=foot\n"},
        "exec": ["bin/foot"], "args": ["--print-id"], "mtime": 1600000000, "prime": {"args": ["--print-cmd"]}}
root = WD + "/r"
ctr.prepare(box, root, case, LANG)
cp = ctr.cache_host(root)
pristine = open(cp, "rb").read()
env = ctr.case_env(case, root, LANG, "scored"); env["XTE_DEBUG"] = "1"
et = ctr.case_env(case, root, LANG, "scored")

def state(name, line2):
    lines = pristine.split(b"\n")
    lines[1] = line2
    data = b"\n".join(lines)
    with open(cp, "wb") as fh:
        fh.write(data)
    _n, st = ctr.oracle_side(box, case, root, LANG)
    with open(cp, "wb") as fh:
        fh.write(data)
    _, out, _e = box.run(root, et, True, ["explain"])
    t = None
    for ln in out.split("\n"):
        if ln.startswith("MADO_TERM: "):
            t = ln.rsplit("cache=", 1)[-1].split()[0] if "cache=" in ln else "?"
    return st, t

names = []
base = "foot"
for i in range(len(base)):
    names.append(("del@%d" % i, base[:i] + base[i + 1:]))
    for c in "-/.:a 0\\":
        names.append(("sub@%d=%r" % (i, c), base[:i] + c + base[i + 1:]))
    for c in "-/.":
        names.append(("ins@%d=%r" % (i, c), base[:i] + c + base[i:]))
names += [(n, n) for n in ["foot", "", "--", "-", "-p", "-pv", "-pV", "-q", "-oot", "-e", "\x1f", ".",
                           "..", "echo", "printf", "if", "then", "[", "test", "true", "false", "time", "{", "}",
                           "[[", "!", "read_cache", "gen_hash", "save_cache", "find_entry", "shoot",
                           "/bin/sh", "/bin", "/tmp", "/", "bin/foot", "./bin/foot", "foot/", "foot//",
                           "foo t", "foo\tt", "FOOT", "feot", "foou"]]
bad = 0
for tag, name in names:
    st, t = state(tag, name.encode("latin-1"))
    if st != t:
        bad += 1
        print("GATE-DIVERGE %-12s name=%r pin_state=%r tool_state=%r" % (tag, name, st, t))
print("names=%d divergences=%d" % (len(names), bad))
