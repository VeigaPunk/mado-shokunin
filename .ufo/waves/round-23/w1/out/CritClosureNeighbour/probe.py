#!/usr/bin/env python3
"""CritClosureNeighbour probe: mechanical truth plus base-classifier result
for the closure-lifetime neighbour fixtures in ./fixtures.

Truth: each fixture's eval code runs in a child Python (-I -S) under the
recording fake `subprocess` module copied from repair/truth.py (CHILD and
safe() are byte-for-byte the same logic); no real subprocess is reachable
from fixture code. Scan: the unchanged round-21 oracle scan helper (one
child, 384 MiB, 15 s) over the given tripwire bytes.

Labels: base-false-observed (a never-executed argv appears at any tier),
base-silent-miss (an executed argv has no observed/lead row and the scan
discloses nothing: exit clean, unparsed 0), base-unparsed (miss or residue
disclosed through eval_unparsed/unparsed_spawns), base-correct otherwise.

Usage: python3 -I probe.py --tool PATH  (writes cases.json next to this file)
"""
import argparse, ast, hashlib, json, runpy, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANE = ROOT.parents[5]
HELPER = LANE / ".ufo/waves/round-21/oracle/measure.py"
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
CLASS = {"-Q": "package_query", "-S": "host_mutation"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def literal_argvs(code):
    out = []
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.List) and node.elts and all(
                isinstance(e, ast.Constant) and isinstance(e.value, str) for e in node.elts):
            out.append(" ".join(e.value for e in node.elts))
    return out


def truth(code):
    proc = subprocess.run([sys.executable, "-I", "-S", "-c", CHILD], input=code,
                          capture_output=True, text=True, timeout=15)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr[-400:])
    return json.loads(proc.stdout)


def classify(executed, rows, unparsed, clean):
    hit = {r["command"] for r in rows if r.get("evidence") in ("observed", "lead")}
    foreign = [r for r in rows if r.get("command") not in executed]
    flags = []
    if not clean:
        flags.append("scanner_error")
    if any(r.get("evidence") == "observed" for r in foreign):
        flags.append("false_observed")
    if any(r.get("evidence") != "observed" for r in foreign):
        flags.append("foreign_lead")
    if set(executed) - hit:
        flags.append("silent_miss")
    if unparsed:
        flags.append("unparsed")
    if "false_observed" in flags or "foreign_lead" in flags:
        primary = "base-false-observed"
    elif "silent_miss" in flags and not unparsed and clean:
        primary = "base-silent-miss"
    elif "silent_miss" in flags or unparsed or not clean:
        primary = "base-unparsed"
    else:
        primary = "base-correct"
    return primary, flags


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, type=Path)
    args = parser.parse_args()
    tool = args.tool.resolve(strict=True)
    tool_sha, helper_sha = sha(tool), sha(HELPER)
    scan = runpy.run_path(str(HELPER))["scan"]
    cases = []
    for fixture in sorted((ROOT / "fixtures").glob("*.jsonl")):
        code = code_of(fixture)
        if not safe(code):
            raise SystemExit("unsafe_fixture: " + fixture.name)
        executed = truth(code)
        decoys = sorted(set(literal_argvs(code)) - set(executed))
        got = scan(tool, fixture)
        payload = got.get("payload", {}) or {}
        rows = payload.get("findings", [])
        unparsed = sum(f.get("eval_unparsed", 0) + f.get("unparsed_spawns", 0)
                       for f in payload.get("files", []))
        clean = got.get("exit") in (0, 1) and not got.get("error")
        primary, flags = classify(executed, rows, unparsed, clean)
        cases.append(dict(
            id=fixture.stem, fixture="fixtures/" + fixture.name, sha256=sha(fixture),
            truth=dict(executed=executed, never_executed_literals=decoys),
            proposed_expectation=dict(
                kind="exact", forbid_any=decoys,
                want=[dict(**{"class": CLASS[c.split()[1]]}, command=c, evidence="observed")
                      for c in sorted(executed)]),
            base=dict(exit=got.get("exit"), error=got.get("error"), unparsed=unparsed,
                      rows=[(r.get("class"), r.get("command"), r.get("evidence")) for r in rows],
                      classification=primary, flags=flags)))
    if sha(tool) != tool_sha or sha(HELPER) != helper_sha:
        raise SystemExit("tool or helper changed during measurement")
    out = dict(schema="mado-r23-critclosure-cases-v1", python=sys.version.split()[0],
               tool_sha256=tool_sha, helper_sha256=helper_sha,
               helper="/.ufo/waves/round-21/oracle/measure.py", cases=cases)
    (ROOT / "cases.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
