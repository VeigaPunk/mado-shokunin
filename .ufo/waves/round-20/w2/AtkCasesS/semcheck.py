import json, sys, types, traceback

calls = []

def fake_run(*a, **k):
    calls.append((a, k))
    return None

fake_sub = types.ModuleType("subprocess")
fake_sub.run = fake_run
fake_lane = types.ModuleType("lanehelpers")
def show(*a, **k):
    calls.append(("show", a, k))
fake_lane.show = show
fake_lane.print = lambda *a, **k: calls.append(("lane.print", a, k))

sys.modules["subprocess"] = fake_sub
sys.modules["lanehelpers"] = fake_lane

def run_case(path):
    calls.clear()
    ns = {"__name__": "__main__", "__builtins__": __builtins__}
    outcome = "ok"
    for line in open(path, encoding="utf-8"):
        rec = json.loads(line)
        for c in rec["message"]["content"]:
            if c.get("type") != "toolCall" or c.get("name") != "eval":
                continue
            code = c["arguments"]["code"]
            try:
                exec(compile(code, "<cell>", "exec"), ns)
            except Exception as exc:
                outcome = "%s: %s" % (type(exc).__name__, exc)
                return outcome, list(calls), code
    return outcome, list(calls), None

for name in sorted(sys.argv[1:]):
    outcome, calls, code = run_case(name)
    print("%-52s outcome=%-40s spawn_calls=%s" % (name.split("--")[-1], outcome, calls))
