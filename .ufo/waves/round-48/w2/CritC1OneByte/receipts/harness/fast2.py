import importlib.util, json, os, shutil, subprocess, sys, time
S = "/fast/scratch/hyaku/mado-r48/CritC1OneByte"
R = S + "/repo/r48"
def load(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
ctr = load("ctr", R + "/quality/counters/c1-r48-terminal-cache.py")
FX = json.loads(open(R + "/quality/counters/c1-r48-fixtures.json", "rb").read())
byid = {f["id"]: f for f in FX}
box = ctr.Box(S + "/work", R + "/tools/mado-terminal.py")
WD = S + "/work/fast2"
os.makedirs(WD, exist_ok=True)
OUT = open(sys.argv[2], "a")
LANG = "C.UTF-8"
MODE = sys.argv[3] if len(sys.argv) > 3 else "full"
ALPHA = [0x00, 0x0a, 0x0d, 0x1e, 0x1f, 0x20, 0x41, 0xff] if MODE == "full" else [0x00, 0x0a, 0x1e, 0x1f, 0x41]
INS = [0x0a, 0x1e, 0x1f, 0x20, 0x41] if MODE == "full" else [0x0a, 0x1f]

def muts(data):
    lines = data.split(b"\n")
    j = b"j"
    yield ("axis-term-line50", b"\n".join(lines[:10] + [j] * 39 + lines[10:]))
    yield ("axis-term-line49", b"\n".join(lines[:10] + [j] * 38 + lines[10:]))
    yield ("axis-term-line48", b"\n".join(lines[:10] + [j] * 37 + lines[10:]))
    yield ("axis-no-final-newline", data[:-1] if data.endswith(b"\n") else data + b"\n")
    yield ("axis-empty-cmdline", b"\n".join(lines[:10] + [b""] + lines[10:]))
    yield ("axis-empty-cmdline2", b"\n".join(lines[:10] + [b"", b""] + lines[10:]))
    yield ("axis-usep-only", b"\n".join(lines[:10] + [b"\x1f\x1eEND_OF_EXEC_USEP"] + lines[11:]))
    yield ("axis-usep-double", b"\n".join(lines[:10] + [b"\x1f\x1f\x1eEND_OF_EXEC_USEP"] + lines[11:]))
    tail = lines[10][:-len(b"\x1eEND_OF_EXEC_USEP")]
    yield ("axis-usep-trail", b"\n".join(lines[:10] + [tail + b"\x1f\x1eEND_OF_EXEC_USEP"] + lines[11:]))
    for i in range(len(data)):
        for v in ALPHA:
            if v != data[i]:
                yield ("sub@%d:%02x>%02x" % (i, data[i], v), data[:i] + bytes([v]) + data[i + 1:])
    for i in range(len(data)):
        yield ("del@%d:%02x" % (i, data[i]), data[:i] + data[i + 1:])
    for i in range(len(data) + 1):
        for v in INS:
            yield ("ins@%d:%02x" % (i, v), data[:i] + bytes([v]) + data[i:])

def raw(root, env, args):
    p = subprocess.run(box.argv(root, env, True, args), capture_output=True, timeout=120, env={"PATH": "/usr/bin"})
    return p.returncode, p.stdout.decode("utf-8", "surrogateescape"), p.stderr.decode("utf-8", "surrogateescape")

import re
ML = re.compile(r"MADO_TERM: .*?cache=(\w+) verdict=", re.S)

def state_of(out):
    m = ML.search(out)
    if m:
        return m.group(1)
    if "MADO_TERM: " in out:
        return "unparseable"
    return None

def run(fid, skip=0):
    case = byid[fid]
    root = WD + "/" + fid + "/r"
    shutil.rmtree(WD + "/" + fid, ignore_errors=True)
    ctr.prepare(box, root, case, LANG)
    cp = ctr.cache_host(root)
    data = open(cp, "rb").read()
    args = [a.replace("$ROOT", root) for a in case["args"]]
    et = ctr.case_env(case, root, LANG, "scored")
    print("=== %s %s args=%r recorded_state=%r cache=%d bytes" % (fid, case["class"], case["args"], case.get("state"), len(data)))
    t_rc0, t_out0, _ = raw(root, et, ["print"] + args)
    t_out0 = t_out0.replace(root, "$ROOT")
    x_rc0, x_out0, _ = raw(root, et, ["explain"])
    print("baseline tool=(%r,%r) state=%s pin=%r" % (t_rc0, t_out0, state_of(x_out0), ctr.oracle_side(box, case, root, LANG)))
    n = bad = racy = 0
    t0 = time.time()
    last = skip
    for k, (mut, mdata) in enumerate(muts(data)):
        if k < skip:
            continue
        last = k
        with open(cp, "wb") as fh:
            fh.write(mdata)
        t_rc, t_out, t_err = raw(root, et, ["print"] + args)
        if open(cp, "rb").read() != mdata:
            # a background cache save from a previous pin run landed during the tool read: retry once
            racy += 1
            with open(cp, "wb") as fh:
                fh.write(mdata)
            t_rc, t_out, t_err = raw(root, et, ["print"] + args)
            if open(cp, "rb").read() != mdata:
                print("RACY %s %s" % (fid, mut)); continue
        o_norm, o_state = ctr.oracle_side(box, case, root, LANG)
        n += 1
        t_out = t_out.replace(root, "$ROOT")
        same = (o_norm[0], o_norm[1]) == (t_rc, t_out)
        t_state = None
        if same:
            with open(cp, "wb") as fh:
                fh.write(mdata)
            _, x_out, _ = raw(root, et, ["explain"])
            t_state = state_of(x_out)
        if not same or t_state != o_state:
            bad += 1
            rec = {"fixture": fid, "mut": mut, "pin": list(o_norm), "pin_state": o_state,
                   "tool": [t_rc, t_out], "tool_state": t_state, "tool_err": t_err[:200], "cache_hex": mdata.hex()}
            print("%s %s %s\n  pin=%r state=%s\n  tool=%r state=%s" % (
                "DIVERGE" if not same else "STATE", fid, mut, o_norm, o_state, (t_rc, t_out), t_state))
            OUT.write(json.dumps(rec) + "\n"); OUT.flush()
            if bad >= 40:
                print("  (stop at 40)"); break
        if n % 300 == 0:
            print("  %d %.1fs bad=%d racy=%d" % (n, time.time() - t0, bad, racy))
    print("--- %s n=%d bad=%d racy=%d last_index=%d %.1fs" % (fid, n, bad, racy, last, time.time() - t0))
    return n, bad

tot = badt = 0
for spec in sys.argv[1].split(","):
    fid, _, sk = spec.partition(":")
    n, bad = run(fid, int(sk or 0)); tot += n; badt += bad
print("TOTAL n=%d bad=%d" % (tot, badt))
