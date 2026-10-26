import json, os, random, subprocess, sys, tempfile, collections

MINE = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/w1/ExecIndepB/mado-monitors.py"
REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/l1-draft/mado-monitors.py"
root = tempfile.mkdtemp(prefix="fuzz-", dir="/fast/scratch/hyaku/mado-r45/ExecIndepB/diff")
TOOLS = {"mine": MINE, "ref": REF}

NAMES = ["DP-1", "DP-2", "HDMI-A-1", "eDP-1", ""]
DESCS = ["Dell Inc. U34", "LG X", ""]
MODES = ["", "preferred", "pref", "highrr", "highres", "maxwidth", "modeline 1 2 3",
         "1920x1080", "3440x1440@100", "3440x1440@100.5", "0x0", "1920x1080@100Hz", "99999x99999@999"]
POSES = ["", "auto", "auto-left", "0x0", "-1920x0", "1x", "1x2x3", "0x0 "]
SCALES = ["", "auto", "1", "1.25", "1.6", "1.3", "0.2", "0.25", "12.345678", "1e3", "2"]
KEYS = ["mirror", "bitdepth", "cm", "sdrsaturation", "sdrbrightness", "transform", "vrr", "icc",
        "wat", "sdr_eotf", "transform "]
VALS = ["0", "1", "7", "9", "10", "hdr", "DP-1", "", "2"]

def line(rng):
    kind = rng.random()
    sel = rng.choice(NAMES + ["desc:" + rng.choice(DESCS), "desc:", "$x"])
    if kind < 0.12:
        body = "%s, %s" % (sel, rng.choice(["disable", "disabled", "DISABLE"]))
    elif kind < 0.22:
        body = "%s, transform, %s" % (sel, rng.choice(["0", "1", "7", "8", "9", "", "0 1"]))
    elif kind < 0.30:
        body = "%s, addreserved, %s" % (sel, ", ".join(rng.choice(["0", "10", "-5", "x", "1", "9999999"]) for _ in range(rng.randint(2, 5))))
    else:
        parts = [sel, rng.choice(MODES), rng.choice(POSES), rng.choice(SCALES)]
        for _ in range(rng.randint(0, 2)):
            parts.append(rng.choice(KEYS)); parts.append(rng.choice(VALS))
        body = ", ".join(parts)
    if rng.random() < 0.15:
        body += rng.choice([" # note", "##", " $v", " \\", "#x"])
    prefix = rng.choice(["monitor = ", "monitor=", "monitor  =  ", "monitor =", "monitorv2 ", "# monitor = "])
    return prefix + body

def live(rng, name):
    def maybe(v, alt):
        return v if rng.random() < 0.85 else alt
    return {"id": maybe(rng.randint(0, 9), rng.choice(["4", 4.5, None])),
            "name": maybe(name, rng.choice([None, 3, ""])),
            "description": maybe(rng.choice(DESCS), rng.choice([None, 5])),
            "width": maybe(rng.choice([3440, 2560, 1920, 1, 0]), rng.choice(["3440", 3440.0, None, True])),
            "height": maybe(rng.choice([1440, 1080, 1, 0]), rng.choice(["1440", None])),
            "refreshRate": maybe(rng.choice([99.997, 100.0, 99.0, 60.0, 59.99, 143.912, 30.0, 120.0]),
                                 rng.choice(["100", None, True])),
            "x": maybe(rng.choice([0, -1920, 3440, 50]), rng.choice(["0", False, None])),
            "y": maybe(rng.choice([0, 5, -100]), rng.choice(["0", None])),
            "scale": maybe(rng.choice([1, 1.25, 1.6, 1.3, 1.33333333, 1.5, 0.5]), rng.choice(["1", None, True])),
            "transform": maybe(rng.choice([0, 1, 3, 5]), rng.choice(["1", True, None])),
            "disabled": maybe(rng.choice([False, True]), rng.choice([1, "false", None])),
            "mirrorOf": maybe(rng.choice(["none", "4", "7", "0"]), rng.choice([4, None, True]))}

def run(tool, confs, dump):
    d = tempfile.mkdtemp(dir=root)
    dp = os.path.join(d, "m.json"); open(dp, "wb").write(json.dumps(dump).encode())
    args = ["--monitors", dp]
    for i, t in enumerate(confs):
        p = os.path.join(d, "c%d.conf" % i); open(p, "w").write(t); args += ["--config", p]
    p = subprocess.run([sys.executable, "-I", tool] + args, capture_output=True,
                       env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": d})
    return p.returncode, p.stdout.decode(), p.stderr.decode()

rng = random.Random(4517)
diffs = collections.Counter()
examples = {}
N = 1200
for n in range(N):
    nlines = rng.randint(1, 4)
    confs = []
    for _ in range(rng.randint(1, 2)):
        confs.append("\n".join(line(rng) for _ in range(rng.randint(1, 3))) + "\n")
    dump = [live(rng, rng.choice(NAMES)) for _ in range(rng.randint(0, 3))]
    a = run(MINE, confs, dump); b = run(REF, confs, dump)
    if (a[0], a[1]) != (b[0], b[1]):
        key = (a[0], b[0], a[2][:40] != b[2][:40])
        diffs[key] += 1
        examples.setdefault(key, (confs, dump, a, b))
print("cases", N, "differing", sum(diffs.values()))
for key, count in diffs.most_common(10):
    print("family", key, "count", count)
    confs, dump, a, b = examples[key]
    print("  conf:", confs)
    print("  dump:", json.dumps(dump))
    for tag, r in (("mine", a), ("ref", b)):
        print("  %s rc=%d err=%r" % (tag, r[0], r[2][-160:]))
        for l in r[1].splitlines():
            print("     ", l)
