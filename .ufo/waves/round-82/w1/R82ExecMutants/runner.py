#!/usr/bin/env python3
"""Independent replay of the frozen C1 case set (own driver, not the counter's)."""
import json
import os
import re
import subprocess
import sys

RESULT_RE = re.compile(
    r"^MADO_BARFOOT_RESULT: monitor=\S+ box=(\S+)"
    r"(?: boxes=(\S+))?(?: reserved=(\S+))?"
    r"(?: band=(-?\d+) expected=(-?\d+))?(?: attributed=(-?\d+))?"
    r"(?: gt=(-?[\d,]+))?(?: attr=(-?[\d,]+))?(?: ls=(\S+))?"
    r".*?verdict=(\S+)\s*$", re.M)
ATTR_RE = re.compile(
    r"^MADO_BARFOOT_ATTR: monitor=\S+ level=\d+ ns=(\S+) edge=(\S+) contribution=(-?\d+)", re.M)
FIELDS = ("box", "boxes", "reserved", "band", "expected", "attributed", "gt", "attr", "ls",
          "verdict")


def parse(stdout):
    m = RESULT_RE.search(stdout)
    if not m:
        return None
    out = {}
    for key, raw in zip(FIELDS, m.groups()):
        if key in ("band", "expected", "attributed"):
            out[key] = int(raw) if raw is not None else None
        else:
            out[key] = raw
    return out


def write_case(case, outdir):
    os.makedirs(outdir, exist_ok=True)
    paths = {}
    for name, key in (("config.json", "config"), ("layers.json", "layers"),
                      ("monitors.json", "monitors")):
        path = os.path.join(outdir, name)
        with open(path, "w") as fh:
            if key == "layers" and "layers_raw" in case:
                fh.write(case["layers_raw"])
            else:
                json.dump(case[key], fh)
        paths[key] = path
    if "rules" in case:
        p = os.path.join(outdir, "rules.conf")
        open(p, "w").write(case["rules"])
        paths["rules"] = p
    if "surfaces" in case:
        p = os.path.join(outdir, "surfaces.json")
        json.dump(case["surfaces"], open(p, "w"))
        paths["surfaces"] = p
    if "allocation" in case:
        p = os.path.join(outdir, "allocation.json")
        json.dump(case["allocation"], open(p, "w"))
        paths["allocation"] = p
    return paths


def matches(case, rc, stdout):
    exp = case["expect"]
    if exp.get("error"):
        stage = exp.get("stage", "model")
        return rc == exp["rc"] and ("ERROR (stage=%s " % stage) in stdout
    got = parse(stdout)
    if got is None:
        return False
    got["rc"] = rc
    for key, want in exp.items():
        if key in ("error", "stage"):
            continue
        if key == "attr_ns":
            seen = dict((m.group(1), "%s:%s" % (m.group(2), m.group(3)))
                        for m in ATTR_RE.finditer(stdout))
            if seen != want:
                return False
        elif got.get(key) != want:
            return False
    return True


def main(tool, cases_path, workroot, label):
    tool = os.path.abspath(tool)
    cases_path = os.path.abspath(cases_path)
    workroot = os.path.abspath(workroot)
    cases = json.load(open(cases_path))["cases"]
    passed, failed = 0, []
    for index, case in enumerate(cases):
        outdir = os.path.join(workroot, "%s-%02d" % (label, index))
        paths = write_case(case, outdir)
        argv = [sys.executable, "-I", tool, "--config", paths["config"],
                "--layers", paths["layers"], "--monitors", paths["monitors"]]
        for key in ("rules", "surfaces", "allocation"):
            if key in paths:
                argv += ["--" + key, paths[key]]
        if case.get("monitor"):
            argv += ["--monitor", case["monitor"]]
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C", "LANG": "C",
               "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": outdir}
        proc = subprocess.run(argv, cwd=outdir, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, timeout=60)
        ok = matches(case, proc.returncode, proc.stdout.decode("utf-8", "replace"))
        if ok:
            passed += 1
        else:
            failed.append(case["name"])
    return passed, len(cases), failed


if __name__ == "__main__":
    tool, cases, workroot, label = sys.argv[1:5]
    p, n, f = main(tool, cases, workroot, label)
    print("PASS %d/%d FAIL %d: %s" % (p, n, len(f), ",".join(f) if f else "-"))
    sys.exit(0 if p == n else 1)
