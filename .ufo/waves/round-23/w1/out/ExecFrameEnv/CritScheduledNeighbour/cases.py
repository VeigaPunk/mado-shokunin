#!/usr/bin/env python3
"""Builds cases.json: fixture sha256, mechanical truth (truth.py's recording
fake subprocess), base-classifier rows (round-21 oracle scan helper, one
child, 384 MiB / 15 s) and the base label for each CritScheduledNeighbour
fixture. Base bytes come from `git show BASE:tools/mado-tripwire.py` and are
refused unless their sha256 is the registered base classifier.

Label precedence: base-false-observed (an observed row for an argv that never
executed) > base-unparsed (eval_unparsed + unparsed_spawns > 0) >
base-silent-miss (an executed argv with no row at any tier) > base-correct
(repair-set exact pass rule holds) > base-other.

Usage: python3 -I cases.py
"""
import ast, hashlib, json, runpy, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
BASE = "a28e4815aabfa85f55274884000fb2608355f8cf"
BASE_SHA = "cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84"
HELPER = LANE / ".ufo/waves/round-21/oracle/measure.py"
REPAIR_MEASURE = LANE / ".ufo/waves/round-23/repair/measure.py"
CLASS = {"-Q": "package_query", "-S": "host_mutation"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def literal_argvs(code):
    found = set()
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.List) and node.elts and all(
                isinstance(e, ast.Constant) and isinstance(e.value, str) for e in node.elts):
            found.add(" ".join(e.value for e in node.elts))
    return found


def label(truth, rows, unparsed, passed):
    observed = {cmd for _, cmd, ev in rows if ev == "observed"}
    seen = {cmd for _, cmd, _ in rows}
    if observed - truth:
        return "base-false-observed"
    if unparsed:
        return "base-unparsed"
    if truth - seen:
        return "base-silent-miss"
    return "base-correct" if passed else "base-other"


def main():
    truth_mod = runpy.run_path(str(HERE / "truth.py"))
    scan = runpy.run_path(str(HELPER))["scan"]
    judge = runpy.run_path(str(REPAIR_MEASURE))["judge"]
    raw_tool = subprocess.run(["git", "-C", str(LANE), "show", BASE + ":tools/mado-tripwire.py"],
                              capture_output=True, check=True).stdout
    if sha(raw_tool) != BASE_SHA:
        raise SystemExit("base classifier sha mismatch")
    cases = []
    with tempfile.TemporaryDirectory() as tmp:
        tool = Path(tmp) / "mado-tripwire.py"
        tool.write_bytes(raw_tool)
        for fixture in sorted((HERE / "fixtures").glob("*.jsonl")):
            code = truth_mod["code_of"](fixture)
            truth = truth_mod["executed"](fixture)
            if "executed" not in truth:
                raise SystemExit("truth failed for %s: %s" % (fixture.name, truth))
            executed = truth["executed"]
            spec = dict(kind="exact",
                        forbid_any=sorted(literal_argvs(code) - set(executed)),
                        want=[dict(**{"class": CLASS[cmd.split()[1]]}, command=cmd, evidence="observed")
                              for cmd in sorted(set(executed))])
            got = scan(tool, fixture)
            passed, unparsed, rows = judge(spec, got)
            keys = [(r.get("class"), r.get("command"), r.get("evidence")) for r in rows]
            cases.append(dict(
                id=fixture.stem, fixture="fixtures/" + fixture.name, sha256=sha(fixture.read_bytes()),
                truth=dict(executed=executed, runner="truth.py (recording fake subprocess, real threading)"),
                expectation=spec,
                base=dict(exit=got.get("exit"), error=got.get("error"), rows=keys, unparsed=unparsed,
                          files=(got.get("payload") or {}).get("files", []),
                          exact_rule_pass=passed,
                          label=label(set(executed), keys, unparsed, passed))))
        if sha(tool.read_bytes()) != BASE_SHA:
            raise SystemExit("base classifier changed during measurement")
    out = dict(schema="mado-r23-w1-critscheduled-cases-v1", base_commit=BASE,
               base_classifier_sha256=BASE_SHA, scan_helper=str(HELPER.relative_to(LANE)),
               scan_helper_sha256=sha(HELPER.read_bytes()),
               pass_rule="repair/measure.py judge(), kind exact",
               python=sys.version.split()[0], cases=cases)
    (HERE / "cases.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({c["id"]: c["base"]["label"] for c in cases}, indent=1))


if __name__ == "__main__":
    main()
