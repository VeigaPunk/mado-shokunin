#!/usr/bin/env python3
"""Round-67 pre-freeze control: score the SUPERSEDED r66 register counter on the
frozen six-case control set. This is the do-nothing baseline for C1: the bytes
that exist before round 67 lands, read at --base, evaluated on the same controls
the r67 candidate must score.

Read-only: extracts the r66 counter source from git into scratch and imports it.
Exit 0 when every control is scored (baseline correctness is printed, not judged),
2 on setup error.
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys


def git(repo, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_OPTIONAL_LOCKS="0", GIT_PAGER="cat", LC_ALL="C", GIT_NO_REPLACE_OBJECTS="1")
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, env=env, timeout=120)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--base", required=True)
    ap.add_argument("--controls", required=True)
    ap.add_argument("--scratch-root", required=True)
    args = ap.parse_args(argv)
    scratch = os.path.abspath(args.scratch_root)
    if scratch.startswith(("/tmp", "/var/tmp", "/dev/shm")) or scratch == "/":
        print("BASELINE_C1: unsafe scratch root", file=sys.stderr)
        return 2
    os.makedirs(scratch, exist_ok=True)
    rev = git(args.repo, "rev-parse", "--verify", "--end-of-options", args.base + "^{commit}")
    if rev.returncode:
        print("BASELINE_C1: bad base", file=sys.stderr)
        return 2
    rev = rev.stdout.decode().strip()
    path = "quality/counters/c1-r66-register.py"
    src = git(args.repo, "show", f"{rev}:{path}")
    if src.returncode:
        print(f"BASELINE_C1: {path} unreadable at {rev}", file=sys.stderr)
        return 2
    module_path = os.path.join(scratch, "c1-r66-register.py")
    with open(module_path, "wb") as fh:
        fh.write(src.stdout)
    spec = importlib.util.spec_from_file_location("c1_r66", module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    doc = json.load(open(args.controls, encoding="utf-8"))
    correct = 0
    for case in doc["cases"]:
        reasons, summary = mod.assess(case["province"], case["objects"].get)
        accepted = not reasons
        want = case["expect"] == "accept"
        ok = accepted == want
        correct += ok
        print(f"BASELINE_C1 case={case['name']} accepted={accepted} expect={case['expect']} correct={'yes' if ok else 'no'} :: {summary}")
    print(f"BASELINE_C1: counter={path} base={rev} controls={len(doc['cases'])} correct={correct}/{len(doc['cases'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
