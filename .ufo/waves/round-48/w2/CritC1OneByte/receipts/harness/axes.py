import importlib.util, json, os, shutil, subprocess, sys, time
S = "/fast/scratch/hyaku/mado-r48/CritC1OneByte"
R = S + "/repo/r48"
def load(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
ctr = load("ctr", R + "/quality/counters/c1-r48-terminal-cache.py")
FX = json.loads(open(R + "/quality/counters/c1-r48-fixtures.json", "rb").read())
box = ctr.Box(S + "/work", R + "/tools/mado-terminal.py")
WD = S + "/work/axes"; os.makedirs(WD, exist_ok=True)
OUT = open(S + "/receipts/axes-all.jsonl", "a")
LANG = "C.UTF-8"
LO, HI = int(sys.argv[1]), int(sys.argv[2])

def raw(root, env, args, dc=False):
    p = subprocess.run(box.argv(root, env, True, args, default_cache=dc), capture_output=True, timeout=120, env={"PATH": "/usr/bin"})
    return p.returncode, p.stdout.decode("utf-8", "surrogateescape")

def axes(data):
    lines = data.split(b"\n")
    if len(lines) < 11:
        return
    j = b"j"
    tail = lines[10][:-len(b"\x1eEND_OF_EXEC_USEP")]
    yield ("term-line50", b"\n".join(lines[:10] + [j] * 39 + lines[10:]))
    yield ("term-line49", b"\n".join(lines[:10] + [j] * 38 + lines[10:]))
    yield ("no-final-newline", data[:-1] if data.endswith(b"\n") else data + b"\n")
    yield ("empty-cmdline", b"\n".join(lines[:10] + [b""] + lines[10:]))
    yield ("empty-cmdline2", b"\n".join(lines[:10] + [b"", b""] + lines[10:]))
    yield ("rs-terminator-1f", data.replace(b"\x1eEND_OF_EXEC_USEP", b"\x1fEND_OF_EXEC_USEP", 1))
    yield ("rs-terminator-removed", data.replace(b"\x1eEND_OF_EXEC_USEP", b"", 1))
    yield ("usep-only", b"\n".join(lines[:10] + [b"\x1f\x1eEND_OF_EXEC_USEP"] + lines[11:]))
    yield ("usep-trail", b"\n".join(lines[:10] + [tail + b"\x1f\x1eEND_OF_EXEC_USEP"] + lines[11:]))
    body = b"\n".join(lines[10:-1]) if lines[-1] == b"" else b"\n".join(lines[10:])
    END = b"\x1eEND_OF_EXEC_USEP"
    head = body[:-len(END)]
    if len(head) > 1:
        newhead = head[:1] + b"\n" + head[2:]
        mut = b"\n".join(lines[:10] + (newhead + END).split(b"\n"))
        yield ("firstword-newline", mut + (b"\n" if data.endswith(b"\n") else b""))

n = bad = 0
t0 = time.time()
for idx, case in enumerate(FX):
    if idx < LO or idx >= HI:
        continue
    root = WD + "/" + case["id"].replace("/", "_") + "/r"
    shutil.rmtree(os.path.dirname(root), ignore_errors=True)
    try:
        ctr.prepare(box, root, case, LANG)
    except Exception as e:
        print("PREP-FAIL %s %s" % (case["id"], e)); continue
    cp = ctr.cache_host(root)
    if not os.path.isfile(cp):
        print("%s: no cache (%s)" % (case["id"], case.get("state"))); continue
    data = open(cp, "rb").read()
    args = [a.replace("$ROOT", root) for a in case["args"]]
    et = ctr.case_env(case, root, LANG, "scored")
    tried = 0
    for mut, mdata in axes(data):
        tried += 1
        with open(cp, "wb") as fh:
            fh.write(mdata)
        t_rc, t_out = raw(root, et, ["print"] + args, case.get("default_cache", False))
        if open(cp, "rb").read() != mdata:
            with open(cp, "wb") as fh:
                fh.write(mdata)
            t_rc, t_out = raw(root, et, ["print"] + args, case.get("default_cache", False))
        o_norm, o_state = ctr.oracle_side(box, case, root, LANG)
        t_out = t_out.replace(root, "$ROOT")
        n += 1
        same = (o_norm[0], o_norm[1]) == (t_rc, t_out)
        rec = {"fixture": case["id"], "class": case["class"], "mut": mut, "pin": list(o_norm), "pin_state": o_state,
               "tool": [t_rc, t_out], "same": same}
        if not same:
            bad += 1
            print("DIVERGE %s %s pin=%r tool=%r" % (case["id"], mut, o_norm, (t_rc, t_out)))
            OUT.write(json.dumps(rec) + "\n"); OUT.flush()
        if mut == "firstword-newline":
            with open(cp, "wb") as fh:
                fh.write(mdata)
            _, x_out = raw(root, et, ["explain"], case.get("default_cache", False))
            rec["explain_parseable"] = ctr.term_line("MADO_TERM: " + x_out.split("MADO_TERM: ")[-1].split("\n")[0]) is not None
            rec["explain_two_lines"] = x_out.split("MADO_TERM: ")[-1].count("\n") > 1
            OUT.write(json.dumps(rec) + "\n"); OUT.flush()
    print("%s %s state=%s axes=%d %.1fs" % (case["id"], case["class"], case.get("state"), tried, time.time() - t0))
print("RANGE %d..%d mutations=%d divergences=%d %.1fs" % (LO, HI, n, bad, time.time() - t0))
