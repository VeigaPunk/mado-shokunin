#!/usr/bin/env python3
"""R82MutRunbook: five independently authored mutations of c2-r82-runbook.py.

Reads the frozen instrument from the lane, writes only under this scratch dir,
runs each mutant's --selftest and its full frozen run (--no-mutants).
"""
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

S = "/fast/scratch/hyaku/mado-r82/R82MutRunbook"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = os.path.join(S, "c2-base.py")
REV = "780c30fcae12d74ce8ab3b871a0888696c2415d9"
CONTROLS = os.path.join(LANE, ".ufo/waves/round-82/controls/c2-runbook-cases-r82.json")
CARRIED = os.path.join(LANE, ".ufo/waves/round-81/controls/c2-runbook-cases-r81.json")

MUTS = [
    ("regex-search-to-match",
     '    if kind == "regex":\n        return re.search(value, text) is not None',
     '    if kind == "regex":\n        return re.match(value, text) is not None'),
    ("lines-shape-floor-minus-one",
     '        pattern = re.compile(value["regex"])\n'
     '        if len(lines) < value.get("min_lines", 1):\n            return False',
     '        pattern = re.compile(value["regex"])\n'
     '        if len(lines) < value.get("min_lines", 1) - 1:\n            return False'),
    ("array-fields-dict-accepted",
     '        if not isinstance(data, list) or len(data) < value.get("min_items", 1):\n'
     '            return False\n'
     '        return all(fields_ok(item, value) for item in data)',
     '        if not isinstance(data, (list, dict)) or len(data) < value.get("min_items", 1):\n'
     '            return False\n'
     '        items = list(data.values()) if isinstance(data, dict) else data\n'
     '        return all(fields_ok(item, value) for item in items)'),
    ("refusal-stage-prefix",
     '    return rc == value["rc"] and ("ERROR (stage=%s " % value.get("stage", "model")) in stdout',
     '    return rc == value["rc"] and ("ERROR (stage=%s" % value.get("stage", "model")) in stdout'),
    ("row-binding-double-bind-allowed",
     '            if hits[0] in bindings:\n'
     '                raise Setup("row %d is bound by %r and %r"\n'
     '                            % (hits[0], bindings[hits[0]], case["name"]))',
     '            if False:\n'
     '                raise Setup("row %d is bound by %r and %r"\n'
     '                            % (hits[0], bindings[hits[0]], case["name"]))'),
]


def sh(argv, cwd, timeout=900):
    p = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       stdin=subprocess.DEVNULL, timeout=timeout)
    return (p.returncode, p.stdout.decode("utf-8", "replace"),
            p.stderr.decode("utf-8", "replace"))


def probe(name, anchor, repl):
    src = open(BASE).read()
    count = src.count(anchor)
    if count != 1:
        return {"name": name, "error": "anchor count %d" % count}
    path = os.path.join(S, "mutant-%s.py" % name)
    with open(path, "w") as fh:
        fh.write(src.replace(anchor, repl, 1))
    src_rc, src_out, src_err = sh([sys.executable, "-I", path, "--selftest"], S)
    run_rc, run_out, run_err = sh(
        [sys.executable, "-I", path, "--repo", LANE, "--rev", REV,
         "--controls", CONTROLS, "--carried", CARRIED,
         "--scratch-root", os.path.join(S, "work-%s" % name), "--no-mutants"],
        LANE)
    with open(os.path.join(S, "mutant-%s.selftest.txt" % name), "w") as fh:
        fh.write(src_out + ("\n[stderr]\n" + src_err if src_err else ""))
    with open(os.path.join(S, "mutant-%s.run.txt" % name), "w") as fh:
        fh.write(run_out + ("\n[stderr]\n" + run_err if run_err else ""))
    m = re.search(r"MADO_R82_RUNBOOK: cases=(\d+) executed=(\d+) matched=(\d+) "
                  r"shapes=(\d+)/(\d+) anchors=(\d+)/(\d+) rows=(\d+)/(\d+) "
                  r"control_new=(\d+)/(\d+) .*?verdict=(\w+)", run_out)
    broken = [line.split("name=")[1].split()[0]
              for line in run_out.splitlines()
              if "MADO_R82_PROBE:" in line and "match=no" in line]
    selftest_fails = [line.split("FAIL: ")[1]
                      for line in src_out.splitlines()
                      if "SELFTEST_FAIL:" in line]
    st = re.search(r"MADO_R82_RUNBOOK_SELFTEST: (\d+)/(\d+)", src_out)
    return {
        "name": name,
        "anchor": anchor,
        "replacement": repl,
        "selftest_rc": src_rc,
        "selftest": "%s/%s" % (st.group(1), st.group(2)) if st else None,
        "selftest_fails": selftest_fails,
        "run_rc": run_rc,
        "matched": int(m.group(3)) if m else None,
        "summary": m.group(0) if m else None,
        "broken_cases": broken,
        "verdict": m.group(9) if m else None,
        "run_stderr_tail": run_err[-500:],
    }


def main():
    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(lambda t: probe(*t), MUTS))
    with open(os.path.join(S, "mutants.json"), "w") as fh:
        json.dump(results, fh, indent=1)
    for r in results:
        print("== %(name)s" % r)
        if "error" in r:
            print("  ERROR", r["error"])
            continue
        print("  selftest rc=%d %s fails=%s" % (r["selftest_rc"], r["selftest"],
                                                r["selftest_fails"]))
        print("  run rc=%d matched=%s broken=%s" % (r["run_rc"], r["matched"],
                                                    r["broken_cases"]))
        print("  %s" % r["summary"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
