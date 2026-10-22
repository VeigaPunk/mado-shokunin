#!/usr/bin/env python3
"""Round-23 repair-set counter: scans each frozen fixture with the given
tripwire bytes through the unchanged round-21 oracle scan helper (one child,
384 MiB, 15 s) and applies expected.json's pass rule. Prints JSON with
passed/total; exit 0 iff all cases pass, 1 if any fails, 2 on tamper/error.

Usage: python3 -I measure.py --tool PATH   (PATH may be a file extracted with
`git show REV:tools/mado-tripwire.py`)."""
import argparse, hashlib, json, runpy, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANE = ROOT.parents[3]
EXPECTED_SHA = "53e34d2691f1a456ce6a4387795c84e5a55d3449b94245d68de516023187c6b9"
HELPER = LANE / ".ufo/waves/round-21/oracle/measure.py"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    raw = (ROOT / "expected.json").read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA:
        raise ValueError("snapshot_tampered: expected.json")
    data = json.loads(raw)
    if len(data["cases"]) != 12:
        raise ValueError("incomplete repair population")
    for case in data["cases"]:
        if sha(ROOT / case["fixture"]) != case["sha256"]:
            raise ValueError("snapshot_tampered: " + case["id"])
    return data


def judge(case, got):
    payload = got.get("payload", {}) or {}
    rows = payload.get("findings", [])
    unparsed = sum(row.get("eval_unparsed", 0) + row.get("unparsed_spawns", 0)
                   for row in payload.get("files", []))
    clean = got.get("exit") in (0, 1) and not got.get("error")
    forbidden = any(row.get("command") in case["forbid_any"] for row in rows)
    if case["kind"] == "exact":
        keys = sorted((r.get("class"), r.get("command"), r.get("evidence")) for r in rows)
        want = sorted((w["class"], w["command"], w["evidence"]) for w in case["want"])
        passed = clean and keys == want and unparsed == 0 and not forbidden
    else:
        present = {r.get("command") for r in rows if r.get("evidence") in ("observed", "lead")}
        passed = clean and set(case["want_present"]) <= present and not forbidden
    return passed, unparsed, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", required=True, type=Path)
    args = parser.parse_args()
    try:
        data = verify()
        tool = args.tool.resolve(strict=True)
        tool_sha, helper_sha = sha(tool), sha(HELPER)
        scan = runpy.run_path(str(HELPER))["scan"]
        results = []
        for case in data["cases"]:
            got = scan(tool, ROOT / case["fixture"])
            passed, unparsed, rows = judge(case, got)
            results.append(dict(id=case["id"], kind=case["kind"], passed=passed, unparsed=unparsed,
                                exit=got.get("exit"), error=got.get("error"),
                                rows=[(r.get("class"), r.get("command"), r.get("evidence")) for r in rows]))
        verify()
        if sha(tool) != tool_sha or sha(HELPER) != helper_sha:
            raise ValueError("tool or helper changed during measurement")
    except Exception as exc:  # tamper or harness failure is never a pass
        print(json.dumps(dict(schema="mado-r23-repair-measure-v1", error=str(exc))))
        return 2
    ok = sum(r["passed"] for r in results)
    print(json.dumps(dict(schema="mado-r23-repair-measure-v1", expected_sha256=EXPECTED_SHA,
                          tool_sha256=tool_sha, helper_sha256=helper_sha,
                          passed=ok, total=len(results), results=results), indent=1))
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
