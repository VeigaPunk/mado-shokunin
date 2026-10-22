#!/usr/bin/env python3
"""Write the four AttackLateCell fixtures, derive truth with the repair
truth.py CHILD, scan with base and tip through the round-21 helper, classify."""
import ast, hashlib, json, runpy, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
OUT = LANE / ".ufo/waves/round-23/w2/out/AttackLateCell"
HELPER = LANE / ".ufo/waves/round-21/oracle/measure.py"
TRUTH_PY = LANE / ".ufo/waves/round-23/repair/truth.py"
TOOLS = {"base": HERE / "base/tool.py", "tip": HERE / "tool.py"}
probe = runpy.run_path(str(HERE / "probe.py"), run_name="probe_mod")
TRUTH = runpy.run_path(str(TRUTH_PY), run_name="truth_mod")
CHILD, safe = TRUTH["CHILD"], TRUTH["safe"]
scan = runpy.run_path(str(HELPER), run_name="oracle_mod")["scan"]

PICK = {
    "LateEnclosingLocalViaRelay": "enclosing local rebound after the nested def, before the call; the call goes through a sibling relay that binds its own same-named local",
    "NonlocalRebindThenCallInSibling": "a sibling nested function rebinds the enclosing cell with nonlocal, then calls the closure",
    "LoopClosureCalledAfterLoop": "closure defined in a for-loop body over the loop variable, called after the loop (late binding: last value only)",
    "SecondFrameInvokesFirstFrameClosure": "closure from the first invocation of outer is called inside a second invocation of the same outer (tip keys frames by def node, not invocation)",
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verdict(rows, unparsed, got, want, forbid, executed):
    observed = {c for _, c, e in rows if e == "observed"}
    present = {c for _, c, _ in rows}
    clean = got.get("exit") in (0, 1) and not got.get("error")
    exact = clean and sorted(rows) == sorted(want) and unparsed == 0
    false_obs = sorted(observed - set(executed))
    forbidden_hit = sorted(present & set(forbid))
    missed = sorted(set(executed) - present)
    silent = sorted(missed) if unparsed == 0 else []
    return dict(correct=exact and not forbidden_hit, false_observed=false_obs,
                forbidden_any_tier=forbidden_hit, missed=missed, silent_miss=silent,
                abstained=unparsed > 0)


def classify(b, t):
    worse = (set(t["false_observed"]) - set(b["false_observed"])) or \
            (set(t["silent_miss"]) - set(b["silent_miss"])) or \
            (set(t["forbidden_any_tier"]) - set(b["forbidden_any_tier"]))
    if b["correct"] and not t["correct"]:
        return "REGRESSED"
    if worse:
        return "REGRESSED"
    if t["correct"] and not b["correct"]:
        return "improved"
    if t["correct"]:
        return "same-correct"
    return "same-wrong"


def main():
    (OUT / "fixtures").mkdir(parents=True, exist_ok=True)
    cases, truth_rows, scan_rows = [], [], []
    tool_sha = {k: sha(v) for k, v in TOOLS.items()}
    for name, why in PICK.items():
        code = probe["CASES"][name]
        assert safe(code), name
        path = OUT / "fixtures" / (name + ".jsonl")
        path.write_text(probe["record"](name, code) + "\n")
        p = subprocess.run([sys.executable, "-I", "-S", "-c", CHILD], input=code,
                           capture_output=True, text=True, timeout=15)
        assert p.returncode == 0, p.stderr
        executed = sorted(set(json.loads(p.stdout)))
        mentioned = sorted({" ".join(e.value for e in node.elts) for node in ast.walk(ast.parse(code))
                            if isinstance(node, ast.List) and node.elts
                            and all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in node.elts)})
        forbid = sorted(set(mentioned) - set(executed))
        want = sorted(("package_query", c, "observed") for c in executed)
        cases.append(dict(id=name, kind="exact", why=why, fixture="fixtures/" + path.name,
                          sha256=sha(path), want=[dict(zip(("class", "command", "evidence"), w)) for w in want],
                          forbid_any=forbid))
        truth_rows.append(dict(id=name, executed=json.loads(p.stdout), passed=sorted(executed) == [w[1] for w in want] and not set(executed) & set(forbid)))
        row = dict(id=name)
        for label, tool in TOOLS.items():
            got = scan(tool, path)
            payload = got.get("payload", {}) or {}
            rows = sorted((r.get("class"), r.get("command"), r.get("evidence")) for r in payload.get("findings", []))
            unparsed = sum(f.get("eval_unparsed", 0) + f.get("unparsed_spawns", 0) for f in payload.get("files", []))
            row[label] = dict(exit=got.get("exit"), error=got.get("error"), unparsed=unparsed, rows=rows,
                              **verdict(rows, unparsed, got, want, forbid, executed))
        row["classification"] = classify(row["base"], row["tip"])
        scan_rows.append(row)
    meta = dict(python=sys.version.split()[0], helper=str(HELPER), helper_sha256=sha(HELPER),
                truth_child_from=str(TRUTH_PY), truth_py_sha256=sha(TRUTH_PY),
                base_sha256=tool_sha["base"], tip_sha256=tool_sha["tip"],
                tip_source="git show 2f1134f38930fc8b067d2d7f5bba126338faabdd:tools/mado-tripwire.py")
    assert {k: sha(v) for k, v in TOOLS.items()} == tool_sha
    (OUT / "cases.json").write_text(json.dumps(dict(schema="mado-r23-w2-attacklatecell-cases-v1", cases=cases), indent=1) + "\n")
    (OUT / "truth-receipt.json").write_text(json.dumps(dict(schema="mado-r23-w2-attacklatecell-truth-v1", **meta,
        passed=sum(r["passed"] for r in truth_rows), total=len(truth_rows), results=truth_rows), indent=1) + "\n")
    tally = {}
    for r in scan_rows:
        tally[r["classification"]] = tally.get(r["classification"], 0) + 1
    (OUT / "scan-receipt.json").write_text(json.dumps(dict(schema="mado-r23-w2-attacklatecell-scan-v1", **meta,
        tally=tally, results=scan_rows), indent=1) + "\n")
    print(json.dumps(dict(tally=tally, cases=[(r["id"], r["classification"]) for r in scan_rows]), indent=1))


if __name__ == "__main__":
    main()
