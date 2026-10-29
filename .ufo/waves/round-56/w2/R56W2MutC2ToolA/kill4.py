#!/usr/bin/env python3
"""Transcripts for every killing proposal against ITS OWN mutant (seat R56W2MutC2ToolA).

Writes receipts/kill-<K>.txt (both full outputs, rc, the verdict) and kill-results.json. Uses the harness' staged
bwrap run; the stage holds only the fixture's tree, the cwd is empty.

Usage: python3 -I kill4.py --repo DIR --work DIR --out DIR
"""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mutate import MUTANTS, TOOL_REL  # noqa: E402
from kill2 import PROPOSALS, build_stage, staged_run, SAFE_PATH  # noqa: E402
from extra import EXTRA  # noqa: E402


def main(argv):
    repo = work = out = None
    i = 0
    while i < len(argv):
        if argv[i] == "--repo":
            repo = argv[i + 1]; i += 2
        elif argv[i] == "--work":
            work = argv[i + 1]; i += 2
        elif argv[i] == "--out":
            out = argv[i + 1]; i += 2
        else:
            print("usage"); return 2
    rdir = os.path.join(out, "receipts")
    os.makedirs(rdir, exist_ok=True)
    os.makedirs(work, exist_ok=True)
    pristine_path = os.path.join(repo, TOOL_REL)
    pristine_src = open(pristine_path, "rb").read().decode("utf-8")
    python = shutil.which("python3", path=SAFE_PATH)
    results = []
    for kid, mid, desc, files, args in PROPOSALS + EXTRA:
        m = [x for x in MUTANTS if x[0] == mid][0]
        mutant_bytes = pristine_src.replace(m[2], m[3]).encode("utf-8")
        assert pristine_src.count(m[2]) == 1, mid
        mpath = os.path.join(work, "mutant-%s.py" % kid)
        with open(mpath, "wb") as fh:
            fh.write(mutant_bytes)
        stage = os.path.join(work, "stage-%s" % kid)
        shutil.rmtree(stage, ignore_errors=True)
        os.makedirs(stage)
        build_stage(files, stage)
        cwd = os.path.join(work, "cwd-%s" % kid)
        shutil.rmtree(cwd, ignore_errors=True)
        os.makedirs(cwd)
        env = {"PATH": SAFE_PATH, "HOME": cwd, "TMPDIR": cwd, "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
        argv_real = [a.replace("{FX}", stage) for a in args]
        po, prc, perr = staged_run(python, pristine_path, argv_real, stage, cwd, env)
        mo, mrc, merr = staged_run(python, mpath, argv_real, stage, cwd, env)
        killed = (po, prc) != (mo, mrc)
        files_desc = {k: (["symlink", v[1]] if isinstance(v, tuple) else "bytes:%d" % len(v)) for k, v in files.items()}
        with open(os.path.join(rdir, "kill-%s.txt" % kid), "w") as fh:
            fh.write("proposal %s  mutant %s\n%s\n" % (kid, mid, desc))
            fh.write("args (after {FX} = staged path): %s\n" % " ".join(argv_real))
            fh.write("files: %s\n" % json.dumps(files_desc, sort_keys=True))
            fh.write("--- pristine rc=%d\n%s" % (prc, po.decode("utf-8", "replace")))
            fh.write("--- mutant %s rc=%d\n%s" % (mid, mrc, mo.decode("utf-8", "replace")))
            if merr.strip():
                fh.write("--- mutant stderr (last line): %s\n" % merr.strip().splitlines()[-1])
            fh.write("VERDICT: %s\n" % ("KILLS" if killed else "DOES NOT KILL"))
        results.append({"proposal": kid, "mutant": mid, "desc": desc, "killed": bool(killed),
                        "args": args, "files": files_desc, "pristine_rc": prc, "mutant_rc": mrc})
        print("%-5s %-5s %s" % (kid, mid, "KILLS" if killed else "NO-KILL"))
    with open(os.path.join(out, "kill-results.json"), "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
