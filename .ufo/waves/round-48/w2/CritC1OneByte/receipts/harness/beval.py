import importlib.util, json, os, shutil, sys, time
S = "/fast/scratch/hyaku/mado-r48/CritC1OneByte"
R = S + "/repo/r48"
spec = importlib.util.spec_from_file_location("ctr", R + "/quality/counters/c1-r48-terminal-cache.py")
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)
FX = json.loads(open(R + "/quality/counters/c1-r48-fixtures.json", "rb").read())
byid = {f["id"]: f for f in FX}
box = ctr.Box(S + "/work", R + "/tools/mado-terminal.py")
WD = S + "/work/beval"
os.makedirs(WD, exist_ok=True)
OUT = open(sys.argv[2] if len(sys.argv) > 2 else S + "/receipts/beval.jsonl", "a")
LANG = "C.UTF-8"

ALPHA = [0x00, 0x0a, 0x0d, 0x1e, 0x1f, 0x20, 0x41, 0xff]
INS = [0x0a, 0x1e, 0x1f, 0x20, 0x41]

def mutations(data, skip=()):
    for i in range(len(data)):
        if i in skip:
            continue
        for v in ALPHA:
            if v != data[i]:
                yield ("sub@%d:%02x>%02x" % (i, data[i], v), data[:i] + bytes([v]) + data[i + 1:])
    for i in range(len(data)):
        if i in skip:
            continue
        yield ("del@%d:%02x" % (i, data[i]), data[:i] + data[i + 1:])
    for i in range(len(data) + 1):
        if i - 1 in skip:
            continue
        for v in INS:
            yield ("ins@%d:%02x" % (i, v), data[:i] + bytes([v]) + data[i:])

def run(fid, limit=None):
    case = byid[fid]
    root = WD + "/" + fid + "/r"
    shutil.rmtree(WD + "/" + fid, ignore_errors=True)
    ctr.prepare(box, root, case, LANG)
    cp = ctr.cache_host(root)
    data = open(cp, "rb").read()
    args = [a.replace("$ROOT", root) for a in case["args"]]
    eo = ctr.case_env(case, root, LANG, "scored"); eo["XTE_DEBUG"] = "1"
    et = ctr.case_env(case, root, LANG, "scored")
    print("=== %s %s args=%r state=%r cache=%d bytes" % (fid, case["class"], case["args"], case.get("state"), len(data)))
    base_o = ctr.oracle_side(box, case, root, LANG)
    base_t = box.run(root, et, True, ["print"] + args)
    print("baseline pin=%r tool=(%r,%r)" % (base_o, base_t[0], base_t[1]))
    assert (base_o[0][0], base_o[0][1]) == (base_t[0], base_t[1]), "baseline disagrees"
    n = bad = 0
    t0 = time.time()
    for mut, mdata in mutations(data):
        if limit and n >= limit:
            break
        with open(cp, "wb") as fh:
            fh.write(mdata)
        t_rc, t_out, t_err = box.run(root, et, True, ["print"] + args)
        with open(cp, "wb") as fh:
            fh.write(mdata)
        o_norm, o_state = ctr.oracle_side(box, case, root, LANG)
        n += 1
        od = (o_norm[0], o_norm[1])
        td = (t_rc, t_out)
        if od != td:
            bad += 1
            rec = {"fixture": fid, "mut": mut, "pin": list(od), "pin_state": o_state, "tool": list(td),
                   "tool_err": t_err[:200], "cache_hex": mdata.hex()}
            print("DIVERGE %s %s\n  pin=%r state=%s\n  tool=%r" % (fid, mut, od, o_state, td))
            OUT.write(json.dumps(rec) + "\n"); OUT.flush()
        else:
            x_rc, x_out, _ = box.run(root, et, True, ["explain"])
            t_state = "-"
            for line in x_out.split("\n"):
                if line.startswith("MADO_TERM: "):
                    t_state = line.rsplit("cache=", 1)[-1].split()[0] if "cache=" in line else "-"
            if t_state != o_state:
                bad += 1
                rec = {"fixture": fid, "mut": mut, "pin": list(od), "pin_state": o_state, "tool": list(td),
                       "tool_state": t_state, "cache_hex": mdata.hex()}
                print("STATE-DIVERGE %s %s pin_state=%s tool_state=%s pin=%r tool=%r" % (fid, mut, o_state, t_state, od, td))
                OUT.write(json.dumps(rec) + "\n"); OUT.flush()
        if n % 200 == 0:
            print("  %d mutations %.1fs bad=%d" % (n, time.time() - t0, bad))
    print("--- %s mutations=%d divergences=%d %.1fs" % (fid, n, bad, time.time() - t0))
    return n, bad

tot = badt = 0
for fid in sys.argv[1].split(","):
    n, bad = run(fid)
    tot += n; badt += bad
print("TOTAL %d mutations %d divergences" % (tot, badt))
