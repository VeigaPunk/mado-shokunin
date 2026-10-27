#!/usr/bin/env python3
"""Diagnose a probe tool's fixture misses that fall inside its own ceiling class.

Reads a counter run log, keeps the clause=f FAIL lines, re-derives the judge's stdout for those
fixtures through the counter's Judge, runs the probe tool, and prints the first differing line plus
the judge's row levels -- so the report can say what the cheap reader actually misses.

Usage: diagnose_misses.py <counter.py> <work-dir> <run-log> <probe-tool> [<ceiling-class> ...]
"""
import importlib.util
import os
import subprocess
import sys


def load_counter(path):
    spec = importlib.util.spec_from_file_location("frozen_c1", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def depth(out, rc):
    if rc != 0:
        return "rc%d" % rc
    body = [ln for ln in out.decode("utf-8", "surrogateescape").splitlines()
            if ln and not ln.startswith(("keysym:", "KEYCODE", "==="))]
    if not body:
        return "zero-row"
    levels = {int(ln.rpartition(" [ ")[0].split()[-1]) for ln in body}
    return "level1-only" if max(levels) == 1 else ("level2-max" if max(levels) == 2 else "level3+")


def main(argv):
    counter, work, log, tool = argv[1], argv[2], argv[3], argv[4]
    want = set(argv[5:] or ["zero-row", "rc2", "level1-only"])
    fm = load_counter(counter)
    fixtures = {c["id"]: c for c in fm.load_fixtures()}
    judge = fm.Judge(work)
    ids = []
    for line in open(log, encoding="utf-8", errors="replace"):
        if "clause=f fixture=" in line and " FAIL" in line:
            ids.append(line.split("fixture=")[1].split()[0])
    shown = 0
    inside = 0
    for fid in ids:
        case = fixtures[fid]
        km = judge.keymap(case["rmlvo"])
        rc, out = judge.run(km, case["arg"])
        cls = depth(out, rc)
        if cls not in want:
            continue
        inside += 1
        if shown >= 8:
            continue
        shown += 1
        p = subprocess.run([sys.executable, "-I", tool, "how-to-type", "--keymap", km,
                            "--disable-compose", "--keysym", case["arg"]],
                           capture_output=True)
        j_lines = out.decode("utf-8", "surrogateescape").splitlines()
        t_lines = p.stdout.decode("utf-8", "surrogateescape").splitlines()
        diff = "same-length" if len(j_lines) == len(t_lines) else "len judge=%d tool=%d" % (
            len(j_lines), len(t_lines))
        first = next((i for i in range(min(len(j_lines), len(t_lines))) if j_lines[i] != t_lines[i]), None)
        print("%s class=%s depth=%s arg=%r rmlvo=%r f_fail_shapes=%s" % (
            fid, case["class"], cls, case["arg"], case["rmlvo"], diff))
        if first is not None:
            print("   first diff line %d: judge=%r tool=%r" % (first, j_lines[first], t_lines[first]))
    print("fixture misses inside the ceiling classes %s: %d of %d fails" % (sorted(want), inside, len(ids)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
