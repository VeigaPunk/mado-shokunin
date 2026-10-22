#!/usr/bin/env python3
"""CritEscapeNeighbour: mechanical truth plus base-classifier result for the
callback escape-neighbour fixtures in ./fixtures.

Truth: each fixture's eval code runs in a child Python (-I -S, 384 MiB, 15 s)
under the recording fake `subprocess` module copied verbatim from
round-23/repair/truth.py; no real subprocess is ever reached by fixture code.
Base: the round-21 oracle `scan` helper (one child, 384 MiB, 15 s) over the
given tool. Writes cases.json next to this file and prints it.

Usage: python3 -I run.py --tool PATH [--expect-tool-sha HEX]"""
import argparse, ast, hashlib, json, resource, runpy, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
HELPER = LANE / ".ufo/waves/round-21/oracle/measure.py"
CAP = 384 * 1024 * 1024
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
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
            if len(node.args) != 1 or node.keywords or not isinstance(node.args[0], (ast.List, ast.Name)):
                return False
    return True


PRESENT_KIND = {"EscapeListAppendThenCalled"}  # store recall, judged like repair CallbackStoredIn*


def expectation(case_id, executed, shadow):
    if case_id in PRESENT_KIND:
        return dict(kind="present", want_present=sorted(executed), forbid_any=shadow)
    return dict(kind="exact", want=[{"class": "package_query", "command": c, "evidence": "observed"}
                                    for c in sorted(executed)], forbid_any=shadow)


def judge(case, got):
    """Pass rule copied from round-23/repair/measure.py judge()."""
    payload = got.get("payload", {}) or {}
    rows = payload.get("findings", [])
    unparsed = sum(row.get("eval_unparsed", 0) + row.get("unparsed_spawns", 0)
                   for row in payload.get("files", []))
    clean = got.get("exit") in (0, 1) and not got.get("error")
    forbidden = any(row.get("command") in case["forbid_any"] for row in rows)
    if case["kind"] == "exact":
        keys = sorted((r.get("class"), r.get("command"), r.get("evidence")) for r in rows)
        want = sorted((w["class"], w["command"], w["evidence"]) for w in case["want"])
        return clean and keys == want and unparsed == 0 and not forbidden
    present = {r.get("command") for r in rows if r.get("evidence") in ("observed", "lead")}
    return clean and set(case["want_present"]) <= present and not forbidden


def cap():
    resource.setrlimit(resource.RLIMIT_AS, (CAP, CAP))


def truth(code):
    proc = subprocess.run([sys.executable, "-I", "-S", "-c", CHILD], input=code, capture_output=True,
                          text=True, timeout=15, preexec_fn=cap)
    if proc.returncode != 0:
        raise RuntimeError("truth child failed: " + proc.stderr[-400:])
    return json.loads(proc.stdout)


def classify(executed, got):
    payload = got.get("payload", {}) or {}
    rows = [(r.get("class"), r.get("command"), r.get("evidence")) for r in payload.get("findings", [])]
    unparsed = sum(f.get("eval_unparsed", 0) + f.get("unparsed_spawns", 0) for f in payload.get("files", []))
    executed_set = set(executed)
    foreign = [r for r in rows if r[1] not in executed_set]
    observed = {r[1] for r in rows if r[2] == "observed"}
    reported = {r[1] for r in rows if r[2] in ("observed", "lead")}
    missing = sorted(executed_set - reported)
    lead_only = sorted((executed_set & reported) - observed)
    flags = []
    if got.get("error") or got.get("exit") not in (0, 1):
        flags.append("base-error")
    if any(r[2] == "observed" for r in foreign):
        flags.append("base-false-observed")
    if unparsed:
        flags.append("base-unparsed")
    if missing and not unparsed:
        flags.append("base-silent-miss")
    verdict = flags[0] if flags else "base-correct"
    exact_pass = (not flags and not foreign and not lead_only and len(rows) == len(executed_set))
    files = [{k: v for k, v in f.items() if k != "path"} for f in payload.get("files", [])]
    return dict(exit=got.get("exit"), error=got.get("error"), rows=rows, unparsed=unparsed,
                foreign_rows=foreign, missing_executed=missing, executed_lead_only=lead_only,
                classification=verdict, flags=flags, exact_rule_pass=exact_pass, files=files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, type=Path)
    parser.add_argument("--expect-tool-sha")
    args = parser.parse_args()
    tool = args.tool.resolve(strict=True)
    tool_sha, helper_sha = sha(tool), sha(HELPER)
    if args.expect_tool_sha and tool_sha != args.expect_tool_sha:
        raise SystemExit("tool sha mismatch: " + tool_sha)
    scan = runpy.run_path(str(HELPER))["scan"]
    cases = []
    for fixture in sorted((ROOT / "fixtures").glob("*.jsonl")):
        code = code_of(fixture)
        if not safe(code):
            raise SystemExit("unsafe_fixture: " + fixture.name)
        executed = truth(code)
        shadow = sorted({" ".join(e.value for e in n.elts) for n in ast.walk(ast.parse(code))
                         if isinstance(n, ast.List) and n.elts
                         and all(isinstance(e, ast.Constant) for e in n.elts)} - set(executed))
        got = scan(tool, fixture)
        base = classify(executed, got)
        proposed = expectation(fixture.stem, executed, shadow)
        base["proposed_rule_pass"] = judge(proposed, got)
        cases.append(dict(id=fixture.stem, fixture="fixtures/" + fixture.name, sha256=sha(fixture),
                          truth=dict(executed=executed, never_executed_shadow_argv=shadow),
                          proposed_expectation=proposed, base=base))
    if sha(tool) != tool_sha or sha(HELPER) != helper_sha:
        raise SystemExit("tool or helper changed during measurement")
    out = dict(schema="mado-r23-crit-escape-neighbour-v1", tool=str(tool), tool_sha256=tool_sha,
               helper=str(HELPER.relative_to(LANE)), helper_sha256=helper_sha,
               runner_sha256=sha(Path(__file__)), python=sys.version.split()[0],
               truth_child="recording fake subprocess, CHILD copied verbatim from round-23/repair/truth.py",
               cases=cases)
    text = json.dumps(out, indent=1)
    (ROOT / "cases.json").write_text(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
