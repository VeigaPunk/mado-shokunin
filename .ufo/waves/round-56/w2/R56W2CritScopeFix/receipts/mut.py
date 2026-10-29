import subprocess, sys, os, re
D = sys.argv[1]
REG = "corpus/SOURCES.md"; ENT = "corpus/knowledge/hyprland-config-autoreload-r56.md"
def git(*a):
    return subprocess.run(["git", "-C", D] + list(a), capture_output=True, text=True, check=True).stdout.strip()
base_reg = open(os.path.join(D, REG), encoding="utf-8").read()
base_ent = open(os.path.join(D, ENT), encoding="utf-8").read()
def commit(name, reg, ent):
    open(os.path.join(D, REG), "w", encoding="utf-8").write(reg)
    open(os.path.join(D, ENT), "w", encoding="utf-8").write(ent)
    git("add", "-A")
    git("-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "--allow-empty", "-m", name)
    return git("rev-parse", "HEAD")
OLD = "ConfigWatcher.cpp:33-34,46,54-56,60,67,69,105 @"
assert base_reg.count(OLD) == 1
def rep(s, old, new):
    assert s.count(old) == 1, old
    return s.replace(old, new)
out = {}
out["base"] = commit("base", base_reg, base_ent)
out["v1_widen_past_eof"] = commit("v1", rep(base_reg, OLD, "ConfigWatcher.cpp:33-34,46,54-56,60,67,69,105-200 @"), base_ent)
out["v2_narrow_below_K12"] = commit("v2", rep(base_reg, OLD, "ConfigWatcher.cpp:33-34,46,54-56,60,67,69,104 @"), base_ent)
out["v3_narrow_below_K08"] = commit("v3", rep(base_reg, OLD, "ConfigWatcher.cpp:33-34,46,54-55,60,67,69,105 @"), base_ent)
out["v4_drop_basename"] = commit("v4", rep(base_reg, OLD, "lines 33-34,46,54-56,60,67,69,105 @"), base_ent)
out["v5_reversed_range"] = commit("v5", rep(base_reg, OLD, "ConfigWatcher.cpp:33-34,46,54-56,60,67,69,105-104 @"), base_ent)
out["v6_prefix_identifier"] = commit("v6", rep(base_reg, OLD, "OldConfigWatcher.cpp:33-34,46,54-56,60,67,69,105 @"), base_ent)
ent6 = base_ent.split("\n")
hits = 0
for i, l in enumerate(ent6):
    if re.match(r"^\| E0[1345677] \|", l) or re.match(r"^\| E06 \|", l):
        new, n = re.subn(r"\| (Hyprland-[A-Za-z0-9.\-]+):(\d+) \|", r"| \1:\2-\2 |", l)
        if n == 1:
            ent6[i] = new; hits += 1
assert hits == 6, hits
out["v7_E_rows_as_range"] = commit("v7", base_reg, "\n".join(ent6))
lines = base_reg.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("| S383 ")]
assert len(idx) == 1
narrow = lines[:]
narrow[idx[0]] = rep(lines[idx[0]], OLD, "ConfigWatcher.cpp:1-2 @")
dup = narrow[:idx[0] + 1] + [lines[idx[0]]] + narrow[idx[0] + 1:]
out["v8_dup_id_last_wins"] = commit("v8", "\n".join(dup), base_ent)
for k, v in out.items():
    print(k, v)
