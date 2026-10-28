import importlib.util, json, random, sys, os
MUT = sys.argv[1]; N = int(sys.argv[2])
def load(p, name):
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
orig = load(os.path.join(MUT, "original/mado-kbdopts.py"), "orig")
VOCAB = ["input {", "device {", "}", "}x", "name = a", "name = b", "name = a # kbd", "name = kbd-a # c",
 "repeat_rate = 30", "repeat_rate = 0x10", "repeat_rate = 201", "repeat_delay = 9", "repeat_delay = 2001",
 "repeat_rate = 30=1", "repeat_delay = 4##0", "repeat_rate = $r", "repeat_rate = 3\\0", "repeat_rate = {{x}}",
 "repeat_rate = 33 # c", "repeat_rate = 30 # $x", "numlock_by_default = true", "numlock_by_default = true$x",
 "numlock_by_default = 1", "numlock_by_default = off", "numlock_by_default = 2", "numlock_by_default = yesterday",
 "repeat_delay = 100", "device[a] {", "device[a]:repeat_rate = 70", "device[a]:sensitivity = 1", "touchpad {", "foo {",
 "# c {", "#note {", "# repeat_rate = 99", "input { # c", "input  {", "source = x", "$v = 1", "=5", "repeat_rate =",
 "repeat_rate", "", "  ", "\t", "repeat_rate = 30\x0c", "repeat_rate = 30\x0b", "input:repeat_rate = 45", "input:repeat_delay = 300",
 "input:numlock_by_default = 1", "$x:repeat_rate = 3", "$x:numlock_by_default = 1", "foo:repeat_rate = 3", "source:repeat_rate = 3", "input:repeat_rate:x = 3", "  repeat_rate\t=\t30\t", "name", "name=a", "device", "input {\r"]
KBS = [None, "a", "b"]
def gen(rng):
    files = []
    for _ in range(rng.choice([1, 1, 2])):
        files.append("\n".join(rng.choice(VOCAB) for _ in range(rng.randint(1, 10))) + rng.choice(["\n", ""]))
    kbs = [k for k in KBS if rng.random() < 0.6] if rng.random() < 0.8 else []
    return files, kbs
def outcome(mod, files, kbs):
    try:
        return "\n".join(mod.report(files, None, kbs))
    except Exception as e:
        return "EXC:" + type(e).__name__
rng = random.Random(5521)
ids = sorted(d for d in os.listdir(MUT) if d.startswith("M") and os.path.isfile(os.path.join(MUT, d, "mado-kbdopts.py")))
mods = {i: load(os.path.join(MUT, i, "mado-kbdopts.py"), "m" + i) for i in ids}
diff = {i: 0 for i in ids}; shortest = {i: None for i in ids}
for _ in range(N):
    files, kbs = gen(rng)
    o = outcome(orig, files, kbs)
    for i in ids:
        if outcome(mods[i], files, kbs) != o:
            diff[i] += 1
            size = sum(len(f) for f in files)
            if shortest[i] is None or size < shortest[i][0]:
                shortest[i] = (size, files, kbs, o, outcome(mods[i], files, kbs))
out = {i: {"disagree": diff[i], "shortest": None if shortest[i] is None else {"files": shortest[i][1], "keyboards": shortest[i][2], "orig": shortest[i][3], "mut": shortest[i][4]}} for i in ids}
json.dump(out, open(os.path.join(MUT, "fuzz-results.json"), "w"), indent=1)
for i in ids:
    print(i, "disagree=%d/%d" % (diff[i], N))
