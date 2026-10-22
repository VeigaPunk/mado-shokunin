#!/usr/bin/env python3
"""AttackRecallRegress probe harness: fixture -> recording-fake truth -> base and tip scans.

Usage: python3 -I probe.py CASES.json OUTDIR RESULT.json
CASES.json maps case id -> eval code. Writes OUTDIR/<id>.jsonl (same JSONL shape as the
round-23 repair fixtures) and prints a JSON verdict per case."""
import ast, hashlib, json, runpy, subprocess, sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
HELPER = LANE / ".ufo/waves/round-21/oracle/measure.py"
BASE = LANE / ".ufo/waves/round-23/evidence/tool-base-cd9da20c.py"
TIP = Path("/fast/scratch/hyaku/mado-r23/w2/AttackRecallRegress/tool.py")
TRUTH = LANE / ".ufo/waves/round-23/repair/truth.py"


def child_and_safe():
    src = TRUTH.read_text()
    tree = ast.parse(src)
    ns = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and node.targets[0].id == "CHILD":
            ns["CHILD"] = ast.literal_eval(node.value)
        if isinstance(node, ast.FunctionDef) and node.name == "safe":
            exec(compile(ast.Module(body=[node], type_ignores=[]), "truth.safe", "exec"), {"ast": ast}, ns)
    return ns["CHILD"], ns["safe"]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def judge(got, executed):
    payload = got.get("payload", {}) or {}
    rows = [(r.get("class"), r.get("command"), r.get("evidence")) for r in payload.get("findings", [])]
    unparsed = sum(f.get("eval_unparsed", 0) + f.get("unparsed_spawns", 0) for f in payload.get("files", []))
    seen = {c for _, c, e in rows if e in ("observed", "lead")}
    missed = sorted(set(executed) - seen)
    false_obs = sorted({c for _, c, e in rows if e == "observed" and c not in executed})
    false_any = sorted({c for _, c, e in rows if c not in executed})
    clean = got.get("exit") in (0, 1) and not got.get("error")
    correct = clean and not missed and not false_obs and unparsed == 0
    return dict(exit=got.get("exit"), error=got.get("error"), rows=rows, unparsed=unparsed,
                missed=missed, false_observed=false_obs, foreign_rows=false_any, correct=correct)


def verdict(b, t):
    if b["correct"] and t["correct"]:
        return "same-correct"
    if not b["correct"] and t["correct"]:
        return "improved"
    if b["correct"] and not t["correct"]:
        return "REGRESSED"
    worse = (len(t["missed"]) > len(b["missed"]) or len(t["false_observed"]) > len(b["false_observed"])
             or t["unparsed"] > b["unparsed"])
    better = (len(t["missed"]) < len(b["missed"]) or len(t["false_observed"]) < len(b["false_observed"])
              or t["unparsed"] < b["unparsed"])
    if worse and not better:
        return "REGRESSED"
    if better and not worse:
        return "improved"
    return "same-wrong"


def main():
    global TIP
    if len(sys.argv) > 4:
        TIP = Path(sys.argv[4]).resolve(strict=True)
    cases = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    child, safe = child_and_safe()
    scan = runpy.run_path(str(HELPER))["scan"]
    hashes = dict(base=sha(BASE), tip=sha(TIP), helper=sha(HELPER), truth=sha(TRUTH))
    results = []
    for cid, code in cases.items():
        record = {"type": "message", "message": {"role": "assistant", "content": [
            {"type": "toolCall", "name": "eval", "id": cid + "-0",
             "arguments": {"language": "py", "reset": False, "code": code}}]}}
        fx = out / (cid + ".jsonl")
        fx.write_text(json.dumps(record) + "\n")
        if not safe(code):
            results.append(dict(id=cid, error="unsafe_fixture"))
            continue
        proc = subprocess.run([sys.executable, "-I", "-S", "-c", child], input=code,
                              capture_output=True, text=True, timeout=15)
        if proc.returncode != 0:
            results.append(dict(id=cid, error="truth_failed", stderr=proc.stderr[-400:]))
            continue
        executed = json.loads(proc.stdout)
        b = judge(scan(BASE, fx), executed)
        t = judge(scan(TIP, fx), executed)
        results.append(dict(id=cid, fixture=str(fx), fixture_sha256=sha(fx), executed=executed,
                            base=b, tip=t, verdict=verdict(b, t)))
    if hashes != dict(base=sha(BASE), tip=sha(TIP), helper=sha(HELPER), truth=sha(TRUTH)):
        raise SystemExit("tool/helper/truth changed during probe")
    doc = dict(schema="mado-r23-w2-attackrecallregress-v1", python=sys.version.split()[0],
               hashes=hashes, results=results)
    Path(sys.argv[3]).write_text(json.dumps(doc, indent=1) + "\n")
    for r in results:
        if "verdict" not in r:
            print(r["id"], r.get("error"), r.get("stderr", ""))
            continue
        print("%-34s %-12s exec=%s\n    base=%s miss=%s fobs=%s unp=%s\n    tip =%s miss=%s fobs=%s unp=%s" % (
            r["id"], r["verdict"], r["executed"],
            r["base"]["rows"], r["base"]["missed"], r["base"]["false_observed"], r["base"]["unparsed"],
            r["tip"]["rows"], r["tip"]["missed"], r["tip"]["false_observed"], r["tip"]["unparsed"]))


if __name__ == "__main__":
    main()
