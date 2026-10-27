import importlib.util, json, os, shutil, sys, time
S = "/fast/scratch/hyaku/mado-r48/CritC1OneByte"
R = S + "/repo/r48"
spec = importlib.util.spec_from_file_location("ctr", R + "/quality/counters/c1-r48-terminal-cache.py")
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)
FX = json.loads(open(R + "/quality/counters/c1-r48-fixtures.json", "rb").read())
box = ctr.Box(S + "/work", R + "/tools/mado-terminal.py")
print("bwrap", box.bwrap, "strace", box.strace, "pin", box.pin)
byid = {f["id"]: f for f in FX}
case = byid[sys.argv[1] if len(sys.argv) > 1 else "W-01"]
root = S + "/work/probe/r"
shutil.rmtree(S + "/work/probe", ignore_errors=True)
t0 = time.time()
ctr.materialize(root, case)
if case.get("mtime") is not None:
    ctr.apply_mtime(root, case["mtime"])
pargs = [a.replace("$ROOT", root) for a in ((case["prime"] or {}).get("args") or ["--print-cmd"])]
box.prime(root, ctr.case_env(case, root, "C.UTF-8", "prime"), pargs, ctr.cache_inside(root, case), case.get("default_cache", False))
cp = ctr.cache_host(root)
data = open(cp, "rb").read()
print("prime %.2fs cache=%d bytes" % (time.time() - t0, len(data)))
for i, ln in enumerate(data.split(b"\n"), 1):
    print("%2d %r" % (i, ln))
eo = ctr.case_env(case, root, "C.UTF-8", "scored"); eo["XTE_DEBUG"] = "1"
t0 = time.time()
o = ctr.oracle_side(box, case, root, "C.UTF-8")
print("pin  %.3fs %r" % (time.time() - t0, o))
et = ctr.case_env(case, root, "C.UTF-8", "scored")
t0 = time.time()
t = box.run(root, et, True, ["print"] + [a.replace("$ROOT", root) for a in case["args"]])
print("tool %.3fs rc=%r out=%r err=%r" % (time.time() - t0, t[0], t[1], t[2][:200]))
t0 = time.time()
x = box.run(root, et, True, ["explain"])
print("explain %.3fs rc=%r\n%s" % (time.time() - t0, x[0], x[1][-400:]))
print("fixture expect", case.get("expect"), "state", case.get("state"), "class", case.get("class"))
