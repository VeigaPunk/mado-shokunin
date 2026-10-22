#!/usr/bin/env python3
"""Scratch probe harness: truth via recording fake subprocess (CHILD copied
byte-for-byte from round-23 repair/truth.py), scans via the round-21 oracle
scan helper for base and tip. Usage: probe.py PROBES_DIR OUT_JSON"""
import ast, json, runpy, subprocess, sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
HELPER = LANE / ".ufo/waves/round-21/oracle/measure.py"
HERE = Path(__file__).resolve().parent
TOOLS = {"base": HERE / "base.py", "tip": HERE / "tool.py"}
CHILD = r"""
import json, sys, types
calls = []
fake = types.ModuleType("subprocess")
def run(argv, *a, **k):
    calls.append(" ".join(argv))
fake.run = run
sys.modules["subprocess"] = fake
code = sys.stdin.read()
exec(compile(code, "<fixture>", "exec"), {"__name__": "__main__"})
print(json.dumps(calls))
"""


def safe(code):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module]
            if names != ["subprocess"]:
                return False
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) \
                and node.value.id == "subprocess" and node.attr != "run":
            return False
        if isinstance(node, ast.Name) and node.id in ("eval", "exec", "open", "__import__", "compile", "getattr", "globals", "os"):
            return False
    return True


def code_of(path):
    record = json.loads(path.read_text().splitlines()[0])
    return record["message"]["content"][0]["arguments"]["code"]


def grade(executed, got):
    payload = got.get("payload", {}) or {}
    rows = [(r.get("class"), r.get("command"), r.get("evidence")) for r in payload.get("findings", [])]
    unparsed = sum(f.get("eval_unparsed", 0) + f.get("unparsed_spawns", 0) for f in payload.get("files", []))
    truth = set(executed)
    observed = {c for _, c, e in rows if e == "observed"}
    lead = {c for _, c, e in rows if e == "lead"}
    false_rows = sorted((observed | lead) - truth)
    false_observed = sorted(observed - truth)
    missed = sorted(truth - observed - lead)
    weak = sorted((truth & lead) - observed)
    clean = got.get("exit") in (0, 1) and not got.get("error")
    exact = clean and observed == truth and not lead - truth and unparsed == 0 and not weak
    return dict(rows=rows, unparsed=unparsed, exit=got.get("exit"), error=got.get("error"),
                false_observed=false_observed, false_rows=false_rows, missed=missed,
                lead_only=weak, exact=exact)


def badness(g):
    return (len(g["false_observed"]) * 4 + len(g["missed"]) * 4 + (len(g["false_rows"]) - len(g["false_observed"])) * 2
            + len(g["lead_only"]) + g["unparsed"] + (10 if g["error"] or g["exit"] not in (0, 1) else 0))


def verdict(b, t):
    if t["exact"] and b["exact"]:
        return "same-correct"
    if t["exact"]:
        return "improved"
    worse = (set(t["false_observed"]) - set(b["false_observed"]) or set(t["missed"]) - set(b["missed"])
             or (t["unparsed"] > b["unparsed"] and b["exact"]) or (b["exact"] and not t["exact"]))
    if worse:
        return "REGRESSED"
    if badness(t) < badness(b):
        return "improved"
    return "same-wrong"


def main():
    probes, out = Path(sys.argv[1]), Path(sys.argv[2])
    scan = runpy.run_path(str(HELPER))["scan"]
    results = []
    for fixture in sorted(probes.glob("*.jsonl")):
        code = code_of(fixture)
        if not safe(code):
            results.append(dict(id=fixture.stem, error="unsafe_fixture"))
            continue
        proc = subprocess.run([sys.executable, "-I", "-S", "-c", CHILD], input=code,
                              capture_output=True, text=True, timeout=15)
        if proc.returncode != 0:
            results.append(dict(id=fixture.stem, error="truth: " + proc.stderr[-400:]))
            continue
        executed = json.loads(proc.stdout)
        sides = {name: grade(executed, scan(tool, fixture)) for name, tool in TOOLS.items()}
        results.append(dict(id=fixture.stem, executed=executed, base=sides["base"], tip=sides["tip"],
                            verdict=verdict(sides["base"], sides["tip"])))
    out.write_text(json.dumps(results, indent=1))
    for r in results:
        if "error" in r:
            print(r["id"], "ERROR", r["error"])
            continue
        print(f'{r["verdict"]:13} {r["id"]}')
        print("   truth:", r["executed"])
        for side in ("base", "tip"):
            g = r[side]
            print(f'   {side}: rows={[(c, e) for _, c, e in g["rows"]]} unparsed={g["unparsed"]} exit={g["exit"]} err={g["error"]}')


if __name__ == "__main__":
    main()
