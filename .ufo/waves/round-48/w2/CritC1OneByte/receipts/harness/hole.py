import importlib.util, json, os, shutil, sys, time
S = "/fast/scratch/hyaku/mado-r48/CritC1OneByte"
R = S + "/repo/r48"
def load(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
ctr = load("ctr", R + "/quality/counters/c1-r48-terminal-cache.py")
FX = json.loads(open(R + "/quality/counters/c1-r48-fixtures.json", "rb").read())
byid = {f["id"]: f for f in FX}
box = ctr.Box(S + "/work", R + "/tools/mado-terminal.py")
WD = S + "/work/hole"
os.makedirs(WD, exist_ok=True)
LANG = "C.UTF-8"
base = byid["v2-wd-01-exec-firstword"]
# one-byte mutation of the primed cache's command line: 'foot' -> 'f\not' (o -> LF)
MUT = "f\not\x1f--a\x1eEND_OF_EXEC_USEP"
case = json.loads(json.dumps(base))
case["id"] = "W2-CRIT-01-cached-cmd-newline"
case["class"] = "WARM-DIFFERS"
case["after"] = dict(base.get("after") or {})
case["after"]["cache_lines"] = {"11": MUT}
case.pop("expect", None); case.pop("cold", None); case.pop("state", None)

# baseline: what the primed cache is, and does the mutation differ by one byte?
root = WD + "/prime/r"
shutil.rmtree(WD + "/prime", ignore_errors=True)
ctr.prepare(box, root, base, LANG)
orig = open(ctr.cache_host(root), "rb").read()
print("pristine line11 = %r" % orig.split(b"\n")[10])
print("mutated  line11 = %r" % MUT.encode())

# record expect/state/cold exactly as score()'s oracle does
o = WD + "/o/r"
shutil.rmtree(WD + "/o", ignore_errors=True)
ctr.prepare(box, o, case, LANG)
warm, state = ctr.oracle_side(box, case, o, LANG)
c = WD + "/c/r"
shutil.rmtree(WD + "/c", ignore_errors=True)
ctr.prepare(box, c, case, LANG, cold=True)
cold, cstate = ctr.oracle_side(box, case, c, LANG)
case["expect"] = {"rc": warm[0], "stdout": warm[1]}
case["cold"] = {"rc": cold[0], "stdout": cold[1]}
case["state"] = state
print("oracle warm=%r state=%r cold=%r cstate=%r" % (warm, state, cold, cstate))
print("tool explain output on the hit tree:")
env = ctr.case_env(case, o, LANG, "scored")
rc, out, err = box.run(o, env, True, ["explain"])
print("  explain rc=%r\n  ---\n%s  ---" % (rc, out))
print("counter term_line(out) ->", ctr.term_line([l for l in out.split("\n") if l.startswith("MADO_TERM: ")][-1] if any(l.startswith("MADO_TERM: ") for l in out.split("\n")) else ""))
rng = __import__("random").Random(4848)
ok, warm_n, why, st, cold_n = ctr.run_case(box, case, "A", rng)
print("clause w run_case ok=%r state=%r why=%r" % (ok, st, why))
try:
    ctr.check_premise(case, st, cold_n)
    print("check_premise: ok")
except ctr.Setup as e:
    print("check_premise: Setup %s" % e)
okx, whyx = ctr.explain_case(box, case, rng)
print("clause x explain_case ok=%r why=%r" % (okx, whyx))
json.dump(case, open(S + "/receipts/added-fixture.json", "w"), indent=1)
print("fixture written")
