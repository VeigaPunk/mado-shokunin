"""MutC1Tool probe: does the frozen warm set separate `command -v` EXECUTABILITY from mere existence?

Builds one schema-v2 fixture from the frozen set's own W-10 (a primed hit whose warm answer differs from its cold
one), then strips the exec bit from the cached command's binary in `after.modes` -- a realistic staleness cause
(the terminal binary lost +x) that the hash cannot see, since the hash covers only list + application paths.
Measures, through the frozen counter's own machinery (Box/prepare/run_case/explain_case):
  * the real pin (oracle) answer and cache state,
  * the l1-draft tool answer,
  * a mutated tool answer.
Writes nothing into the lane.
"""
import importlib.util
import json
import os
import random
import sys

C, DRAFT, MUT, WORK, OUT = sys.argv[1:6]
spec = importlib.util.spec_from_file_location("c1r48", C)
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)

warm = json.load(open(os.path.join(os.path.dirname(C), c1.NAME_WARM)))
base = [c for c in warm if c["id"] == "W-10"][0]
case = json.loads(json.dumps(base))
case["id"] = "W-GAP-CMDV-NONEXEC"
case["class"] = "WARM-SAME"
case["state"] = "stale"
case["after"] = dict(case.get("after") or {})
case["after"]["modes"] = {"bin/foot": "420"}  # 0644: the cached command exists, is not executable

rng = random.Random(4848)
res = {}
for tag, tool in (("draft", DRAFT), ("mutant", MUT)):
    work = os.path.join(WORK, tag)
    os.makedirs(work, exist_ok=True)
    box = c1.Box(work, tool)
    ok, o_norm, why, state, cold = c1.run_case(box, case, "A", rng)
    xok, xwhy = c1.explain_case(box, case, random.Random(4848))
    res[tag] = {
        "clause_w_ok": ok, "why": why, "oracle": list(o_norm), "state": state,
        "cold": list(cold) if cold else None, "clause_x_ok": xok, "clause_x_why": xwhy,
        "trips": len(box.trips),
    }
    print("%s: w_ok=%s state=%s oracle=%r cold=%r x_ok=%s x_why=%s trips=%d" % (
        tag, ok, state, o_norm, cold, xok, xwhy, len(box.trips)))
# the fixture bytes clause w would need: expect = the oracle answer, cold twin recorded, state recorded
fx = {k: v for k, v in case.items() if k in ("id", "class", "args", "env", "files", "exec", "mtime", "prime", "after",
                                             "unset", "default_cache")}
fx["state"] = "stale"
fx["expect"] = {"rc": res["draft"]["oracle"][0], "stdout": res["draft"]["oracle"][1]}
fx["cold"] = {"rc": res["draft"]["cold"][0], "stdout": res["draft"]["cold"][1]}
json.dump({"fixture": fx, "measured": res}, open(OUT, "w"), indent=1, sort_keys=True)
print("wrote", OUT)
