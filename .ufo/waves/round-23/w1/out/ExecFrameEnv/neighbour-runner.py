#!/usr/bin/env python3
"""ExecFrameEnv neighbour runner: judge a candidate tool against the frozen
expectations authored by the three critic seats.

Expectations are read from the *authored* cases.json of each critic seat (their
truth + expectation fields only; the base result fields are ignored). Truth is
recomputed by the critic's own truth runner where one exists (scheduled), else
by the same recording-fake-subprocess child copied from round-23/repair/truth.py
(frame, escape). The pass rule is repair/measure.py's judge().

Usage: python3 -I neighbour-runner.py --tool PATH [--seat frame|scheduled|escape]
Writes neighbour-results.json next to this file; prints a summary.
"""
import argparse, ast, hashlib, json, runpy, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
HELPER = LANE / ".ufo/waves/round-21/oracle/measure.py"
JUDGE = LANE / ".ufo/waves/round-23/repair/measure.py"
SEATS = {
    "frame": LANE / ".ufo/waves/round-23/w1/out/CritFrameNeighbour",
    "scheduled": LANE / ".ufo/waves/round-23/w1/out/CritScheduledNeighbour",
    "escape": LANE / ".ufo/waves/round-23/w1/out/CritEscapeNeighbour",
}
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
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def code_of(path):
    record = json.loads(Path(path).read_text().splitlines()[0])
    return record["message"]["content"][0]["arguments"]["code"]


def truth(code):
    proc = subprocess.run([sys.executable, "-I", "-S", "-c", CHILD], input=code,
                          capture_output=True, text=True, timeout=15)
    if proc.returncode != 0:
        raise RuntimeError("truth child failed: " + proc.stderr[-400:])
    return json.loads(proc.stdout)


def literal_argvs(code):
    found = set()
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.List) and node.elts and all(
                isinstance(e, ast.Constant) and isinstance(e.value, str) for e in node.elts):
            found.add(" ".join(e.value for e in node.elts))
    return found


def expectation(case_id, executed, shadow):
    """Frozen expectation, recomputed from the critic's authored rules."""
    if case_id == "EscapeListAppendThenCalled":
        return dict(kind="present", want_present=sorted(executed), forbid_any=shadow)
    return dict(kind="exact",
                want=[dict(**{"class": CLASS[c.split()[1]]}, command=c, evidence="observed")
                      for c in sorted(set(executed))],
                forbid_any=shadow)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, type=Path)
    parser.add_argument("--seat", default="all", choices=("all",) + tuple(SEATS))
    args = parser.parse_args()
    tool = args.tool.resolve(strict=True)
    scan = runpy.run_path(str(HELPER))["scan"]
    judge = runpy.run_path(str(JUDGE))["judge"]
    seats = SEATS if args.seat == "all" else {args.seat: SEATS[args.seat]}
    out = dict(schema="mado-r23-execframeenv-neighbour-v1", tool=str(tool), tool_sha256=sha(tool),
               helper_sha256=sha(HELPER), judge_sha256=sha(JUDGE), python=sys.version.split()[0],
               seats={})
    total_pass = total = 0
    for seat, root in seats.items():
        cases = []
        for fixture in sorted((root / "fixtures").glob("*.jsonl")):
            code = code_of(fixture)
            executed = truth(code)
            shadow = sorted(literal_argvs(code) - set(executed))
            spec = expectation(fixture.stem, executed, shadow)
            got = scan(tool, fixture)
            passed, unparsed, rows = judge(spec, got)
            cases.append(dict(id=fixture.stem, fixture="fixtures/" + fixture.name,
                              sha256=sha(fixture), truth=dict(executed=executed, shadow=shadow),
                              expectation=spec, passed=passed, unparsed=unparsed,
                              rows=[(r.get("class"), r.get("command"), r.get("evidence"))
                                    for r in (got.get("payload", {}) or {}).get("findings", [])],
                              exit=got.get("exit"), error=got.get("error")))
            total += 1
            total_pass += int(passed)
        out["seats"][seat] = dict(cases=cases,
                                  passed=sum(c["passed"] for c in cases), total=len(cases))
    out["summary"] = dict(passed=total_pass, total=total)
    (HERE / "neighbour-results.json").write_text(json.dumps(out, indent=1) + "\n")
    for seat, data in out["seats"].items():
        for case in data["cases"]:
            print("%-10s %-34s %s  rows=%s unparsed=%s" % (
                seat, case["id"], "PASS" if case["passed"] else "FAIL",
                case["rows"], case["unparsed"]))
    print("neighbour total: %d/%d" % (total_pass, total))
    return 0 if total_pass == total else 1


if __name__ == "__main__":
    sys.exit(main())
