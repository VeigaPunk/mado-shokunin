#!/usr/bin/env python3
"""CritFrameNeighbour: mechanical truth plus base-classifier result per fixture.

Truth: the CHILD runner copied byte-for-byte from round-23/repair/truth.py
(recording fake `subprocess`; no real subprocess is ever spawned by fixture
code) behind the same safe() gate. Base: the unchanged round-21 oracle
`scan` helper (python3 -I child, 384 MiB, 15 s), one fixture at a time.

Usage: python3 -I measure.py --tool PATH   (writes cases.json next to this file)
"""
import argparse, ast, hashlib, json, runpy, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
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


def foreign_of(code):
    """Every literal argv in the fixture, joined like the fake runner joins them."""
    out = set()
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.List) and node.elts and all(
                isinstance(e, ast.Constant) and isinstance(e.value, str) for e in node.elts):
            out.add(" ".join(e.value for e in node.elts))
    return out


def truth(code):
    proc = subprocess.run([sys.executable, "-I", "-S", "-c", CHILD], input=code,
                          capture_output=True, text=True, timeout=15)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr[-400:])
    return json.loads(proc.stdout)


def verdict(executed, rows, unparsed):
    seen = {r[1]: r[2] for r in rows}
    foreign = [r for r in rows if r[1] not in executed]
    if any(r[2] == "observed" for r in foreign):
        return "base-false-observed"
    if unparsed:
        return "base-unparsed"
    if any(cmd not in seen for cmd in executed):
        return "base-silent-miss"
    if foreign or any(seen[cmd] != "observed" for cmd in executed):
        return "base-correct-with-foreign-or-weak-tier"
    return "base-correct"


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
        literals = foreign_of(code)
        got = scan(tool, fixture)
        payload = got.get("payload", {}) or {}
        rows = [(r.get("class"), r.get("command"), r.get("evidence")) for r in payload.get("findings", [])]
        unparsed = sum(f.get("eval_unparsed", 0) + f.get("unparsed_spawns", 0) for f in payload.get("files", []))
        cases.append(dict(
            id=fixture.stem, fixture="fixtures/" + fixture.name, sha256=sha(fixture),
            truth=dict(executed=executed, forbid_any=sorted(literals - set(executed))),
            base=dict(exit=got.get("exit"), error=got.get("error"), rows=rows, unparsed=unparsed,
                      stderr_tail=(got.get("stderr") or "")[-400:]),
            verdict=verdict(executed, rows, unparsed)))
    if sha(tool) != tool_sha or sha(HELPER) != helper_sha:
        raise SystemExit("tool or helper changed during measurement")
    out = dict(schema="mado-r23-critframeneighbour-v1", tool_sha256=tool_sha, helper_sha256=helper_sha,
               measure_sha256=sha(Path(__file__)), python=sys.version.split()[0], cases=cases)
    (ROOT / "cases.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
