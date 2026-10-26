#!/usr/bin/env python3
"""ExecFixtureMap probes: the two measurement facts the map depends on, made reproducible.

 1. LINENO inside a heredoc-attached $( ) body: which line does bash report? (find_entry_paths
    793-797 and gen_hash 190-202). Shows the raw `+`-prefixed trace lines with their text so a
    shifted line number is visible, not asserted.
 2. The forked save_cache child: does a run ever leave a cache file behind, and is its trace
    stable? Runs one --print-cmd fixture three times in one materialized root.

Usage: probe-artifacts.py --work DIR    (scratch only under --work)
"""
import argparse
import importlib.util
import json
import os
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("mapper", os.path.join(HERE, "map-fixtures.py"))
mapper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mapper)

CASE = "aa3-long-name-and-exec"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    work = tempfile.mkdtemp(dir=a.work, prefix="probe-")
    fixtures = json.load(open(mapper.FIXTURES))
    case = [c for c in fixtures if c["id"] == CASE][0]
    script = os.path.join(work, "xte.map")
    with open(script, "wb") as fh:
        fh.write(open(mapper.PIN, "rb").read())
    os.chmod(script, 0o755)
    box = mapper.Box(work, script)
    root = os.path.join(work, "r")
    mapper.materialize(root, case)
    args = [x.replace("$ROOT", root) for x in case["args"]]
    env = mapper.case_env(case, root, "C.UTF-8")
    out = open(a.out, "w")
    for k in (1, 2, 3):
        cache = os.path.join(root, ".rw", "cache")
        before = sorted(os.listdir(cache))
        rc, so, se, why = box.run(root, env, args)
        after = sorted(os.listdir(cache))
        out.write("run %d: rc=%s stdout=%r cache_before=%r cache_after=%r why=%r\n"
                  % (k, rc, so, before, after, why))
        hits = sorted({int(m.group(1)) for m in
                       (mapper.TRACE.match(l) for l in se.split("\n")) if m})
        out.write("  traced lines: %d distinct\n" % len(hits))
        out.write("  in 185..215: %r\n" % [h for h in hits if 185 <= h <= 215])
        out.write("  in 750..800: %r\n" % [h for h in hits if 750 <= h <= 800])
        for ln in se.split("\n"):
            m = mapper.TRACE.match(ln)
            if m and (185 <= int(m.group(1)) <= 215 or 750 <= int(m.group(1)) <= 800):
                out.write("  raw| %s\n" % ln[:140])
        out.write("\n")
    out.close()
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
