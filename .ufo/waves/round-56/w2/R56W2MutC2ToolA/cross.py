#!/usr/bin/env python3
"""Cross-kill matrix (seat R56W2MutC2ToolA): every proposed killing fixture against every named mutant.

A mutant is credited to a fixture only when the fixture separates THAT mutant from the pristine tool through the
harness' staged bwrap run. ONE stage per proposal is shared by the pristine run and every mutant run, so the raw
stage paths printed in the output are identical across the comparison.

Usage: python3 -I cross.py --repo DIR --work DIR --out DIR --mutants M16,M17,...
"""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mutate import MUTANTS, TOOL_REL  # noqa: E402
from kill2 import PROPOSALS, build_stage, staged_run, SAFE_PATH  # noqa: E402
from extra import EXTRA  # noqa: E402

ALL = PROPOSALS + EXTRA


def main(argv):
    repo = work = out = None
    want = []
    i = 0
    while i < len(argv):
        if argv[i] == "--repo":
            repo = argv[i + 1]; i += 2
        elif argv[i] == "--work":
            work = argv[i + 1]; i += 2
        elif argv[i] == "--out":
            out = argv[i + 1]; i += 2
        elif argv[i] == "--mutants":
            want = argv[i + 1].split(","); i += 2
        else:
            print("usage"); return 2
    os.makedirs(work, exist_ok=True)
    os.makedirs(out, exist_ok=True)
    pristine_path = os.path.join(repo, TOOL_REL)
    pristine_src = open(pristine_path, "rb").read().decode("utf-8")
    python = shutil.which("python3", path=SAFE_PATH)
    stages = {}
    for kid, _pmid, desc, files, args in ALL:
        stage = os.path.join(work, "stage-%s" % kid)
        shutil.rmtree(stage, ignore_errors=True)
        os.makedirs(stage)
        build_stage(files, stage)
        cwd = os.path.join(work, "cwd-%s" % kid)
        shutil.rmtree(cwd, ignore_errors=True)
        os.makedirs(cwd)
        env = {"PATH": SAFE_PATH, "HOME": cwd, "TMPDIR": cwd, "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
        argv_real = [a.replace("{FX}", stage) for a in args]
        po, prc, _e = staged_run(python, pristine_path, argv_real, stage, cwd, env)
        stages[kid] = (stage, cwd, env, argv_real, po, prc)
    matrix = {}
    for mid in want:
        m = [x for x in MUTANTS if x[0] == mid][0]
        if pristine_src.count(m[2]) != 1:
            print("%s: snippet ambiguous" % mid)
            continue
        mpath = os.path.join(out, "cross-%s.py" % mid)
        with open(mpath, "wb") as fh:
            fh.write(pristine_src.replace(m[2], m[3]).encode("utf-8"))
        killers = []
        for kid, _pmid, desc, files, args in ALL:
            stage, cwd, env, argv_real, po, prc = stages[kid]
            mo, mrc, _err = staged_run(python, mpath, argv_real, stage, cwd, env)
            if (po, prc) != (mo, mrc):
                killers.append(kid)
        matrix[mid] = killers
        print("%-5s killed by: %s" % (mid, ", ".join(killers) if killers else "NONE"))
    with open(os.path.join(out, "cross-matrix.json"), "w") as fh:
        json.dump(matrix, fh, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
