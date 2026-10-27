import importlib.util, json, os, random, shutil
S = "/fast/scratch/hyaku/mado-r48/CritC1OneByte"
R = S + "/repo/r48"
def load(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
ctr = load("ctr", R + "/quality/counters/c1-r48-terminal-cache.py")
box = ctr.Box(S + "/work", R + "/tools/mado-terminal.py")
WD = S + "/work/final"
shutil.rmtree(WD, ignore_errors=True); os.makedirs(WD)
LANG = "C.UTF-8"
CONFIGS = {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
           "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share",
           "XDG_CURRENT_DESKTOP": "Hyprland"}
case = {
    "id": "W2-CRIT-01-cached-cmd-newline", "class": "WARM-DIFFERS",
    "env": dict(CONFIGS),
    "files": {"home/.config/hyprland-xdg-terminals.list": "foot.desktop\n",
              "usr/share/applications/foot.desktop":
                  "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=foot\n"},
    "exec": ["bin/foot"], "args": ["--print-cmd"], "mtime": 1600000000,
    "prime": {"args": ["--print-cmd"]},
    "after": {"cache_lines": {"11": "f\not\x1eEND_OF_EXEC_USEP"}, "mtime": 1600000000},
}
# 1) the primed cache and the one-byte difference
p0 = WD + "/p0/r"
ctr.prepare(box, p0, {k: v for k, v in case.items() if k != "after"}, LANG)
primed = open(ctr.cache_host(p0), "rb").read()
print("primed cache line 11 = %r" % primed.split(b"\n")[10])
print("after  cache line 11 = %r" % case["after"]["cache_lines"]["11"].encode())
print("one byte? %r" % (len(primed.split(b"\n")[10]) == len(case["after"]["cache_lines"]["11"].encode())))
# 2) oracle record (expect / cold / state), exactly as score() derives them
o = WD + "/o/r"
ctr.prepare(box, o, case, LANG)
warm, state = ctr.oracle_side(box, case, o, LANG)
c = WD + "/c/r"
ctr.prepare(box, c, case, LANG, cold=True)
cold, cstate = ctr.oracle_side(box, case, c, LANG)
case["expect"] = {"rc": warm[0], "stdout": warm[1]}
case["cold"] = {"rc": cold[0], "stdout": cold[1]}
case["state"] = state
print("oracle warm=%r state=%r | cold=%r cstate=%r" % (warm, state, cold, cstate))
# 3) schema check exactly as load_fixtures does
ctr.check_case(case, "added")
print("check_case: ok")
# 4) the counter's own three judgements on this one fixture
rng = random.Random(4848)
ok, warm_n, why, st, cold_n = ctr.run_case(box, case, "A", rng)
print("clause w run_case: ok=%r oracle=%r state=%r why=%r" % (ok, warm_n, st, why))
ok_b = ctr.run_case(box, case, "B", rng)[0]
print("clause w variant B: ok=%r" % ok_b)
try:
    ctr.check_premise(case, st, cold_n); print("check_premise: ok")
except ctr.Setup as e:
    print("check_premise: Setup %s" % e)
okx, whyx = ctr.explain_case(box, case, rng)
print("clause x explain_case: ok=%r why=%r" % (okx, whyx))
# 5) the raw explain record, byte for byte
env = ctr.case_env(case, o, LANG, "scored")
rc, out, err = box.run(o, env, True, ["explain"])
rec = out.split("MADO_TERM: ")[-1]
print("explain rc=%r record=%r" % (rc, "MADO_TERM: " + rec))
print("term_line -> %r" % (ctr.term_line("MADO_TERM: " + rec.split("\n")[0]),))
print("tool print: %r" % (box.run(o, env, True, ["print", "--print-cmd"]),))
json.dump(case, open(S + "/receipts/fixture-W2-CRIT-01.json", "w"), indent=1)
