import importlib.util, json, os, shutil, re
S = "/fast/scratch/hyaku/mado-r48/CritC1OneByte"
R = S + "/repo/r48"
def load(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
ctr = load("ctr", R + "/quality/counters/c1-r48-terminal-cache.py")
FX = json.loads(open(R + "/quality/counters/c1-r48-fixtures.json", "rb").read())
byid = {f["id"]: f for f in FX}
box = ctr.Box(S + "/work", R + "/tools/mado-terminal.py")
WD = S + "/work/conf"; shutil.rmtree(WD, ignore_errors=True); os.makedirs(WD)
LANG = "C.UTF-8"

def show(tag, case, root):
    env = ctr.case_env(case, root, LANG, "scored")
    o = ctr.oracle_side(box, case, root, LANG)
    t = box.run(root, env, True, ["print"] + [a.replace("$ROOT", root) for a in case["args"]])
    rc, out, err = box.run(root, env, True, ["explain"])
    lines = [l for l in out.split("\n") if l.startswith("MADO_TERM: ")]
    parsed = ctr.term_line(lines[-1]) if lines else None
    print("=== %s" % tag)
    print("  pin  : rc=%r out=%r state=%r" % (o[0][0], o[0][1], o[1]))
    print("  tool : rc=%r out=%r" % (t[0], t[1]))
    print("  explain rc=%d term_line=%r" % (rc, parsed))
    print("  tail  : %r" % out.split("MADO_TERM_TRACE")[-1][-160:])

# 1) COLD entry whose first Exec word carries an escaped newline (no cache involved)
case = {"id": "COLD-NL", "class": "WARM-SAME",
        "env": {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
                "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share",
                "XDG_CURRENT_DESKTOP": "Hyprland"},
        "files": {"home/.config/hyprland-xdg-terminals.list": "foot.desktop\n",
                  "usr/share/applications/foot.desktop":
                      "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=\"a\\nb\" x\nName=T\n"},
        "exec": ["bin/foot"], "args": ["--print-cmd"], "mtime": 1600000000}
root = WD + "/coldnl/r"; ctr.prepare(box, root, case, LANG)
show("cold first word with newline", case, root)

# 2) warm hit, cached entry path carries a newline (one byte in line 3)
base = byid["v2-wd-01-exec-firstword"]
case = json.loads(json.dumps(base))
case.pop("expect", None); case.pop("cold", None); case.pop("state", None)
case["after"] = dict(case.get("after") or {})
case["after"]["cache_lines"] = {"3": "$ROOT/home/.local/share/applications/./fo\not.desktop"}
root = WD + "/pathnl/r"; ctr.prepare(box, root, case, LANG)
show("cached path with newline (line 3, one byte)", case, root)

# 3) warm hit, cached entry id carries a newline (one byte in line 4)
case = json.loads(json.dumps(base))
case.pop("expect", None); case.pop("cold", None); case.pop("state", None)
case["after"] = dict(case.get("after") or {})
case["after"]["cache_lines"] = {"4": "foot.deskt\np.desktop"}
root = WD + "/idcr/r"; ctr.prepare(box, root, case, LANG)
show("cached id with CR (line 4, one byte)", case, root)
