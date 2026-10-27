import importlib.util, json, os, shutil, subprocess, sys
S = "/fast/scratch/hyaku/mado-r48/CritC1OneByte"
R = S + "/repo/r48"
def load(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
ctr = load("ctr", R + "/quality/counters/c1-r48-terminal-cache.py")
tool = load("tool", R + "/tools/mado-terminal.py")
FX = json.loads(open(R + "/quality/counters/c1-r48-fixtures.json", "rb").read())
byid = {f["id"]: f for f in FX}
box = ctr.Box(S + "/work", R + "/tools/mado-terminal.py")
WD = S + "/work/gate"
os.makedirs(WD, exist_ok=True)
LANG = "C.UTF-8"
case = byid["v2-wd-01-exec-firstword"]
root = WD + "/r"
shutil.rmtree(WD, ignore_errors=True); os.makedirs(WD)
ctr.materialize(root, case)
ctr.apply_mtime(root, case["mtime"])
# after-state: the entry was edited and a bin/feot added (as in the fixture's scored phase)
ctr.apply_after(root, case.get("after") or {})
env = ctr.case_env(case, root, LANG, "scored")

def bash_gate(name):
    argv = box.prefix(root, False, False)
    for k in sorted(env):
        argv += ["--setenv", k, env[k]]
    argv += ["--chdir", root, "/bin/bash", "-c", 'command -v -- "$1" > /dev/null 2>&1; echo $?', "_", name]
    p = subprocess.run(argv, capture_output=True, env={"PATH": "/usr/bin"}, timeout=60)
    return p.stdout.decode().strip() == "0"

def tool_gate(name):
    r = tool.Resolver(env, cwd=root)
    r.aliases = {}
    try:
        return r.command_v(name)
    except tool.OutOfContract as ex:
        return "OOC:%s" % ex

names = set()
for base in ("foot", "kitty", "wezterm", "alacritty", "ghostty", "konsole", "xterm", "feot", "ls", "tr"):
    names.add(base)
    for i in range(len(base)):
        names.add(base[:i] + base[i + 1:])
        for c in "-p.~* $/aA0\u00ff":
            names.add(base[:i] + c + base[i + 1:])
        for c in "-/a. ":
            names.add(base[:i] + c + base[i:])
for extra in ["--", "-", "", "-p", "-pv", "-pV", "-q", "-x", "-oot", "--print-cmd", "--help", "echo", "printf",
              "if", "then", "!", "{", "}", "[[", "]", "time", "read_cache", "gen_hash", "save_cache", "find_entry",
              "command", "exec", "true", "false", "type", "ls", "rm", "mkdir", "md5sum", "awk", "find", "tr",
              "/bin/sh", "/bin", "/tmp", "/", ".", "..", "./foot", "../bin/foot", "bin/foot", "bin", "bin/",
              "foot/", "foot//", "foo\tt", "foo t", "a=b", "~", "~root", "\u00ffoot", "foot\r", "foot "]:
    names.add(extra)
bad = 0
for name in sorted(names):
    b = bash_gate(name)
    t = tool_gate(name)
    if b != t:
        bad += 1
        print("GATE-DIVERGE name=%r bash=%r tool=%r" % (name, b, t))
print("names=%d divergences=%d" % (len(names), bad))
