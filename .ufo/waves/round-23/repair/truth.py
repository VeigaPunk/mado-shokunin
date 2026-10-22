#!/usr/bin/env python3
"""Round-23 repair-set truth oracle.

Runs each fixture's eval code in a child Python with a recording fake
`subprocess` module, so truth comes from Python's own name resolution, not
from the scanner or the author's reading. Refuses any fixture whose code
imports anything except subprocess or calls anything outside the allowed
shape. Exit 0 iff every case's expectation matches the executed argv set.
"""
import ast, hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED_SHA = "53e34d2691f1a456ce6a4387795c84e5a55d3449b94245d68de516023187c6b9"
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


def load():
    raw = (ROOT / "expected.json").read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA:
        raise SystemExit("snapshot_tampered: expected.json")
    data = json.loads(raw)
    for case in data["cases"]:
        if hashlib.sha256((ROOT / case["fixture"]).read_bytes()).hexdigest() != case["sha256"]:
            raise SystemExit("snapshot_tampered: " + case["id"])
    return data


def code_of(path):
    record = json.loads(path.read_text().splitlines()[0])
    return record["message"]["content"][0]["arguments"]["code"]


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


def main():
    data = load()
    results = []
    for case in data["cases"]:
        code = code_of(ROOT / case["fixture"])
        if not safe(code):
            results.append(dict(id=case["id"], passed=False, error="unsafe_fixture"))
            continue
        proc = subprocess.run([sys.executable, "-I", "-S", "-c", CHILD], input=code,
                              capture_output=True, text=True, timeout=15)
        if proc.returncode != 0:
            results.append(dict(id=case["id"], passed=False, error=proc.stderr[-400:]))
            continue
        executed = json.loads(proc.stdout)
        forbidden = sorted(set(executed) & set(case["forbid_any"]))
        if case["kind"] == "exact":
            passed = sorted(executed) == sorted(w["command"] for w in case["want"]) and not forbidden
        else:
            passed = set(case["want_present"]) <= set(executed) and not forbidden
        results.append(dict(id=case["id"], passed=passed, executed=executed))
    load()
    ok = sum(r["passed"] for r in results)
    print(json.dumps(dict(schema="mado-r23-repair-truth-v1", expected_sha256=EXPECTED_SHA,
                          python=sys.version.split()[0], passed=ok, total=len(results),
                          results=results), indent=1))
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
