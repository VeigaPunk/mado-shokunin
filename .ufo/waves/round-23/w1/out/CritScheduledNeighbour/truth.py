#!/usr/bin/env python3
"""CritScheduledNeighbour truth oracle (CHILD copied from round-23 repair/truth.py).

Runs each fixture's eval code in a child Python with a recording fake
`subprocess` module, so truth comes from Python's own name resolution. The
only change from repair/truth.py is the safety gate: these fixtures exercise
threading.Thread/Timer, so `threading` is admitted as a second import with
only its Thread and Timer attributes. Real threading runs the target; the
fake subprocess records argv and never spawns.

Usage: python3 -I truth.py FIXTURE.jsonl...   (prints JSON; exit 0 iff every
fixture is safe and its child exits 0).
"""
import ast, json, subprocess, sys
from pathlib import Path

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
ATTRS = {"subprocess": {"run"}, "threading": {"Thread", "Timer"}}


def code_of(path):
    record = json.loads(Path(path).read_text().splitlines()[0])
    return record["message"]["content"][0]["arguments"]["code"]


def safe(code):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            return False
        if isinstance(node, ast.Import) and any(a.name not in ATTRS or a.asname for a in node.names):
            return False
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) \
                and node.value.id in ATTRS and node.attr not in ATTRS[node.value.id]:
            return False
        if isinstance(node, ast.Name) and node.id in ("eval", "exec", "open", "__import__", "compile", "getattr", "globals", "os"):
            return False
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess" \
                and not all(isinstance(arg, (ast.List, ast.Name)) for arg in node.args):
            return False
    return True


def executed(path):
    code = code_of(path)
    if not safe(code):
        return dict(error="unsafe_fixture")
    proc = subprocess.run([sys.executable, "-I", "-S", "-c", CHILD], input=code,
                          capture_output=True, text=True, timeout=15)
    if proc.returncode != 0:
        return dict(error=proc.stderr[-400:])
    return dict(executed=json.loads(proc.stdout))


def main(paths):
    results = [dict(fixture=str(p), **executed(p)) for p in paths]
    print(json.dumps(dict(schema="mado-r23-w1-critscheduled-truth-v1", python=sys.version.split()[0],
                          results=results), indent=1))
    return 0 if all("executed" in r for r in results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
