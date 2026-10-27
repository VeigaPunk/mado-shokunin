import importlib.util, json, os, shutil, sys, time
S = "/fast/scratch/hyaku/mado-r48/CritC1OneByte"
R = S + "/repo/r48"
def load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
ctr = load("ctr", R + "/quality/counters/c1-r48-terminal-cache.py")
tool = load("tool", R + "/tools/mado-terminal.py")
FX = json.loads(open(R + "/quality/counters/c1-r48-fixtures.json", "rb").read())
byid = {f["id"]: f for f in FX}
box = ctr.Box(S + "/work", R + "/tools/mado-terminal.py")
WD = S + "/work/fast"
os.makedirs(WD, exist_ok=True)
OUTP = sys.argv[2]
OUT = open(OUTP, "a")
LANG = "C.UTF-8"
ALPHA = [0x00, 0x0a, 0x0d, 0x1e, 0x1f, 0x20, 0x41, 0xff]
INS = [0x0a, 0x1e, 0x1f, 0x20, 0x41]

def muts(data):
    # structured axes first
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
    yield ("axis-usep-trail", b"\n".join(lines[:10] + [lines[10][:-len(b"\x1eEND_OF_EXEC_USEP")] + b"\x1f\x1eEND_OF_EXEC_USEP"] + lines[11:]))
    for i in range(len(data)):
        for v in ALPHA:
            if v != data[i]:
                yield ("sub@%d:%02x>%02x" % (i, data[i], v), data[:i] + bytes([v]) + data[i + 1:])
    for i in range(len(data)):
        yield ("del@%d:%02x" % (i, data[i]), data[:i] + data[i + 1:])
    for i in range(len(data) + 1):
        for v in INS:
            yield ("ins@%d:%02x" % (i, v), data[:i] + bytes([v]) + data[i:])

def tool_side(env, args):
    """(rc, stdout) and the tool's own cache state, in-process (the tool is hermetic by contract)."""
    state = None
    try:
        r = tool.Resolver(env)
        try:
            r.select()
        except tool.Exit as e:
            pass
        state = getattr(r, "cache", "-")
    except tool.OutOfContract:
        state = "ooc"
    try:
        out, rc, err = tool.run_print(env, args)
    except tool.OutOfContract:
        return (2, ""), state, "out_of_contract"
    return (rc, out), state, ""

def run(fid):
    case = byid[fid]
    root = WD + "/" + fid + "/r"
    shutil.rmtree(WD + "/" + fid, ignore_errors=True)
    ctr.prepare(box, root, case, LANG)
    cp = ctr.cache_host(root)
    data = open(cp, "rb").read()
    args = [a.replace("$ROOT", root) for a in case["args"]]
    eo = ctr.case_env(case, root, LANG, "scored"); eo["XTE_DEBUG"] = "1"
    et = ctr.case_env(case, root, LANG, "scored")
    cwd = os.getcwd(); os.chdir(root)
    print("=== %s %s args=%r recorded_state=%r cache=%d" % (fid, case["class"], case["args"], case.get("state"), len(data)))
    n = bad = 0
    t0 = time.time()
    try:
        for mut, mdata in muts(data):
            with open(cp, "wb") as fh:
                fh.write(mdata)
            (t_rc, t_out), t_state, t_note = tool_side(et, args)
            with open(cp, "wb") as fh:
                fh.write(mdata)
            o_norm, o_state = ctr.oracle_side(box, case, root, LANG)
            n += 1
            if (o_norm[0], o_norm[1]) != (t_rc, t_out) or o_state != t_state:
                bad += 1
                rec = {"fixture": fid, "mut": mut, "pin": list(o_norm), "pin_state": o_state,
                       "tool": [t_rc, t_out], "tool_state": t_state, "tool_note": t_note,
                       "cache_hex": mdata.hex()}
                print("%s %s %s\n  pin=%r state=%s\n  tool=%r state=%s" % (
                    "DIVERGE" if (o_norm[0], o_norm[1]) != (t_rc, t_out) else "STATE", fid, mut,
                    o_norm, o_state, (t_rc, t_out), t_state))
                OUT.write(json.dumps(rec) + "\n"); OUT.flush()
                if bad >= 60:
                    print("  (stopping this fixture at 60 divergences)"); break
            if n % 400 == 0:
                print("  %d %.1fs bad=%d" % (n, time.time() - t0, bad))
    finally:
        os.chdir(cwd)
    print("--- %s n=%d bad=%d %.1fs" % (fid, n, bad, time.time() - t0))
    return n, bad

tot = badt = 0
for fid in sys.argv[1].split(","):
    n, bad = run(fid); tot += n; badt += bad
print("TOTAL n=%d bad=%d" % (tot, badt))
