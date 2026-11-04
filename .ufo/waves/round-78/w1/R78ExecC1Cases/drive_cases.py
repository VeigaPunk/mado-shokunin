#!/usr/bin/env python3
"""R78ExecC1Cases — run the frozen r78 tool and the held r77 base tool on each frozen case.

Read-only on the repo; writes fixtures only under the seat scratch. The agree check
reproduces the counter's expected_ok contract (subset comparison over expect keys,
"ERROR (" required for error cases) exactly as frozen in quality/counters/c1-r78-margins.py.
"""
import json
import os
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SCRATCH = "/fast/scratch/hyaku/mado-r78/R78ExecC1Cases"
TOOLS = {
    "r78": os.path.join(REPO, "tools", "mado-barfoot.py"),
    "r77": os.path.join(SCRATCH, "mado-barfoot-base.py"),
}


def parse_result(stdout):
    m = re.search(r"^MADO_BARFOOT_RESULT: .*?box=(\S+) reserved=(\S+)"
                  r"(?: band=(-?\d+) expected=(-?\d+))?.*?verdict=(\S+)\s*$",
                  stdout, re.M)
    if not m:
        return None
    band = int(m.group(3)) if m.group(3) is not None else None
    expected = int(m.group(4)) if m.group(4) is not None else None
    return {"box": m.group(1), "reserved": m.group(2), "band": band,
            "expected": expected, "verdict": m.group(5)}


def expected_ok(case, rc, stdout):
    exp = case["expect"]
    if exp.get("error"):
        return rc == exp["rc"] and "ERROR (" in stdout
    got = parse_result(stdout)
    if got is None:
        return False
    got["rc"] = rc
    return all(got[k] == exp[k] for k in exp)


def main():
    with open(os.path.join(REPO, ".ufo", "waves", "round-78", "controls",
                           "c1-cases-r78.json")) as fh:
        cases = json.load(fh)["cases"]
    for label, tool in TOOLS.items():
        print("== %s ==" % label)
        correct = 0
        for i, case in enumerate(cases):
            d = os.path.join(SCRATCH, "cases", "%s-%02d" % (label, i))
            os.makedirs(d, exist_ok=True)
            cfg = os.path.join(d, "config.json")
            lay = os.path.join(d, "layers.json")
            mon = os.path.join(d, "monitors.json")
            with open(cfg, "w") as fh:
                json.dump(case["config"], fh)
            with open(lay, "w") as fh:
                json.dump(case["layers"], fh)
            with open(mon, "w") as fh:
                json.dump(case["monitors"], fh)
            argv = [sys.executable, "-I", tool, "--config", cfg,
                    "--layers", lay, "--monitors", mon]
            if case.get("monitor"):
                argv += ["--monitor", case["monitor"]]
            proc = subprocess.run(argv, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, cwd=d)
            out = proc.stdout.decode("utf-8", "replace")
            got = parse_result(out)
            ok = expected_ok(case, proc.returncode, out)
            correct += 1 if ok else 0
            fields = (" ".join("%s=%s" % (k, got[k]) for k in
                               ("box", "reserved", "band", "expected", "verdict"))
                      if got else ("ERROR (" in out and "ERROR (" or out.strip()[:60]))
            print("%-24s rc=%d %-58s %s"
                  % (case["name"], proc.returncode, str(fields),
                     "AGREE" if ok else "DISAGREE"))
        print("%s correct=%d/%d" % (label, correct, len(cases)))


if __name__ == "__main__":
    main()
