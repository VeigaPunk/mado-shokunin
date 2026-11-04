import json, types, sys, traceback
LANE="/home/vgpnk/Projects/shokunin/mado-shokunin"
cases=json.load(open(LANE+"/.ufo/waves/round-76/controls/c2-cases-r76.json"))["cases"]
class Res:
    returncode=0; stdout=""; stderr=""
def make_subprocess(rec):
    def run(argv, *a, **kw):
        env = kw.get("env")
        rec.append(("call", list(argv)[:3], dict(env) if isinstance(env, dict) else None))
        return Res()
    def check_output(argv, *a, **kw):
        return make_subprocess(rec).__call__(argv, *a, **kw) and ""
    return types.SimpleNamespace(run=run, check_output=check_output, Popen=run,
                                 CalledProcessError=Exception, TimeoutExpired=Exception,
                                 PIPE=-1, STDOUT=-2, DEVNULL=-3, check_call=run)
out=[]
for c in cases:
    if not c["name"].startswith(("callee-","dynamic-key-")): continue
    rec=[]
    ns={"__name__":"fixture","__builtins__":__builtins__,"subprocess":make_subprocess(rec)}
    status="ok"; err=""
    try:
        exec(compile(c["src"], c["name"], "exec"), ns)
        ns["run"]("repo")
    except KeyError as e:
        status="KeyError"; err=str(e)
    except Exception as e:
        status=type(e).__name__; err=str(e)
    launches=[r for r in rec if r[1][:1]==["git"]]
    guarded = bool(launches) and all(l[2] is not None and "GIT_NO_REPLACE_OBJECTS" in l[2] for l in launches)
    out.append({"name":c["name"],"status":status,"err":err,"launches":len(launches),
                "launch_guarded":guarded,"expect_guard":c["expect_guard"],
                "label_matches_runtime": (guarded==c["expect_guard"]) if launches else None})
for o in out:
    print(o)
json.dump(out, open("reachability-observed.json","w"), indent=1)
