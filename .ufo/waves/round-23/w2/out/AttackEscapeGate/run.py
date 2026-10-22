#!/usr/bin/env python3
"""AttackEscapeGate: truth (recording fake subprocess, CHILD copied from
round-23 repair/truth.py) and base-vs-tip scan (round-21 oracle scan helper,
one child at a time, 384 MiB / 15 s) for the wave-2 escape-gate fixtures.

Usage: python3 -I run.py BASE_TOOL TIP_TOOL"""
import ast, hashlib, json, runpy, subprocess, sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
LANE = OUT.parents[5]
HELPER = LANE / ".ufo/waves/round-21/oracle/measure.py"
CASES = ["EscapeGlobalHook", "EscapeDictUpdateKeyword", "EscapeYieldGenerator", "EscapeWrapperClosure"]
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


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def code_of(path):
    record = json.loads(path.read_text().splitlines()[0])
    return record["message"]["content"][0]["arguments"]["code"]


def safe(code):
    for node in ast.walk(ast.parse(code)):
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


def truth(code):
    proc = subprocess.run([sys.executable, "-I", "-S", "-c", CHILD], input=code,
                          capture_output=True, text=True, timeout=15)
    if proc.returncode != 0:
        raise SystemExit("truth child failed: " + proc.stderr[-400:])
    return json.loads(proc.stdout)


def reading(got, executed):
    payload = got.get("payload", {}) or {}
    rows = [(r.get("class"), r.get("command"), r.get("evidence")) for r in payload.get("findings", [])]
    unparsed = sum(f.get("eval_unparsed", 0) + f.get("unparsed_spawns", 0) for f in payload.get("files", []))
    clean = got.get("exit") in (0, 1) and not got.get("error")
    found = {c for _, c, e in rows if e in ("observed", "lead")}
    foreign = sorted({c for _, c, _ in rows if c not in executed})
    recalled = set(executed) <= found
    correct = clean and recalled and not foreign and unparsed == 0
    return dict(exit=got.get("exit"), error=got.get("error"), rows=rows, unparsed=unparsed,
                recalled=recalled, foreign=foreign, correct=correct)


def verdict(base, tip):
    if base["correct"] and tip["correct"]:
        return "same-correct"
    if not base["correct"] and tip["correct"]:
        return "improved"
    if base["correct"] and not tip["correct"]:
        return "REGRESSED"
    return "same-wrong"


def main():
    base_tool, tip_tool = (Path(p).resolve(strict=True) for p in sys.argv[1:3])
    scan = runpy.run_path(str(HELPER))["scan"]
    results = []
    for case in CASES:
        fixture = OUT / "fixtures" / (case + ".jsonl")
        code = code_of(fixture)
        if not safe(code):
            raise SystemExit("unsafe fixture: " + case)
        executed = truth(code)
        base = reading(scan(base_tool, fixture), executed)
        tip = reading(scan(tip_tool, fixture), executed)
        results.append(dict(id=case, fixture_sha256=sha(fixture), executed=executed,
                            base=base, tip=tip, verdict=verdict(base, tip)))
    print(json.dumps(dict(schema="mado-r23-w2-attack-escape-gate-v1",
                          base_sha256=sha(base_tool), tip_sha256=sha(tip_tool),
                          helper_sha256=sha(HELPER), python=sys.version.split()[0],
                          results=results), indent=1))


if __name__ == "__main__":
    main()
