import importlib.util, json, os, shutil, subprocess, sys, tempfile, time
S = "/fast/scratch/hyaku/mado-r48/CritC1OneByte"
R = S + "/repo/r48"
H = S + "/h"
spec = importlib.util.spec_from_file_location("tool", R + "/tools/mado-terminal.py")
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)
spec2 = importlib.util.spec_from_file_location("ctr", R + "/quality/counters/c1-r48-terminal-cache.py")
ctr = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(ctr)
FX = json.loads(open(R + "/quality/counters/c1-r48-fixtures.json", "rb").read())
byid = {f["id"]: f for f in FX}
box = ctr.Box(S + "/work", R + "/tools/mado-terminal.py")
WD = S + "/work/fuzz"
shutil.rmtree(WD, ignore_errors=True)
os.makedirs(WD)

def primed_cache(fid):
    case = byid[fid]
    root = WD + "/" + fid + "/r"
    ctr.prepare(box, root, case, "C.UTF-8")
    return case, root, open(ctr.cache_host(root), "rb").read()

def tool_parse(data, tag, h1):
    p = WD + "/cache-" + tag
    with open(p, "wb") as fh:
        fh.write(data)
    env = {"HOME": WD, "XDG_CACHE_HOME": WD, "XDG_CONFIG_HOME": WD + "/c", "XDG_DATA_HOME": WD + "/d",
           "XDG_DATA_DIRS": WD + "/s", "PATH": "/usr/bin", "XDG_CURRENT_DESKTOP": "Hyprland"}
    r = tool.Resolver(env)
    r.cache_file = p
    r.t = lambda *a, **k: None
    r.gen_hash = lambda: h1
    r.command_v = lambda name: True
    st = r.read_cache()
    if st != "hit":
        return (st,)
    return ("hit", r.entry_path, r.entry_id, r.entry_action, r.execarg, r.appidarg, r.titlearg, r.dirarg,
            r.holdarg, r.exec_usep)

def pin_parse(data, tag):
    p = WD + "/cache-" + tag
    o = WD + "/pin-" + tag
    if not os.path.exists(p):
        with open(p, "wb") as fh:
            fh.write(data)
    subprocess.run(["bash", H + "/pinloop.sh", p, o], check=True)
    b = open(o, "rb").read()
    parts = b.split(b"\0")
    state = parts[0].decode()
    fields = [x.decode("latin-1") for x in parts[1:11]]
    usep = b.split(b"\0", 11)[11].decode("latin-1")
    if state != "finished":
        return ("invalid",)
    return ("hit",) + tuple(fields[2:10]) + (usep,)

def report(tag, data, a, b, mut):
    print("DIVERGE %s %s\n  pin =%r\n  tool=%r" % (tag, mut, a, b))

alphabet = [0x00, 0x09, 0x0a, 0x0d, 0x1e, 0x1f, 0x20, 0x41, 0x7f, 0xff]
total = 0
div = 0
cases = sys.argv[1:] or ["W-01", "v2-wd-01-exec-firstword"]
for fid in cases:
    case, root, data = primed_cache(fid)
    print("=== %s %s args=%r cache=%d bytes\n    %r" % (fid, case["class"], case["args"], len(data), data))
    muts = []
    for i in range(len(data)):
        for v in alphabet:
            if v != data[i]:
                muts.append(("sub@%d:%02x>%02x" % (i, data[i], v), data[:i] + bytes([v]) + data[i + 1:]))
    for i in range(len(data)):
        muts.append(("del@%d:%02x" % (i, data[i]), data[:i] + data[i + 1:]))
    for i in range(len(data) + 1):
        for v in (0x0a, 0x1e, 0x1f, 0x41, 0x00):
            muts.append(("ins@%d:%02x" % (i, v), data[:i] + bytes([v]) + data[i:]))
    # structured axes: terminator pushed to line 50 / line 49, trailing newline dropped, empty command fields
    lines = data.split(b"\n")
    struct = {
        "axis-term-line50": b"\n".join(lines[:10] + [b"j"] * 39 + lines[10:]),
        "axis-term-line49": b"\n".join(lines[:10] + [b"j"] * 38 + lines[10:]),
        "axis-no-final-newline": data.rstrip(b"\n"),
        "axis-empty-first-cmdline": b"\n".join(lines[:10] + [b""] + lines[10:]),
        "axis-empty-usep-tail": data.replace(b"\x1eEND_OF_EXEC_USEP", b"\x1f\x1eEND_OF_EXEC_USEP", 1),
        "axis-empty-usep-head": data.replace(b"\x1eEND_OF_EXEC_USEP", b"\x1f\x1f\x1eEND_OF_EXEC_USEP", 1),
    }
    for name, m in struct.items():
        muts.append((name, m))
    for mut, mdata in muts:
        tag = "%s-%d" % (fid.replace("/", "_"), total)
        a = pin_parse(mdata, tag)
        h1 = mdata.replace(b"\0", b"").split(b"\n")[0].decode("latin-1")
        b = tool_parse(mdata, tag, h1)
        total += 1
        if a != b:
            div += 1
            if div <= 40:
                report(fid, mdata, a, b, mut)
    print("--- %s: %d mutations, divergences so far %d" % (fid, len(muts), div))
print("TOTAL mutations=%d divergences=%d" % (total, div))
