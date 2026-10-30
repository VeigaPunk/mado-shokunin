#!/usr/bin/env python3
"""Round-57 candidate: per-run sealed C2 fixture scorer.

Usage: python3 -I r56_ctl_c2_reseal.py --tool TOOL --committed DIR --holdout DIR
       --sealed-sha256 HEX --work DIR
The holdout digest is checked before execution; expected bytes are kept in this process
and each tool invocation receives only a staged tree, the exported tool, and empty cwd.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

IDS = (["F%02d" % i for i in range(1, 19)], ["H%02d" % i for i in range(1, 9)])
TIMEOUT = 30
SAFE_PATH = "/usr/local/bin:/usr/bin:/bin"


def commitment(root):
    """Frozen C2 digest: sorted relpath, NUL, f|l, NUL, content SHA-256, newline."""
    rows = []
    for dp, dirs, files in os.walk(root, followlinks=False):
        for name in list(dirs):
            full = os.path.join(dp, name)
            if os.path.islink(full):
                dirs.remove(name)
                rows.append((os.fsencode(os.path.relpath(full, root)), b"l",
                             hashlib.sha256(os.fsencode(os.readlink(full))).hexdigest().encode()))
        for name in files:
            full = os.path.join(dp, name)
            rel = os.fsencode(os.path.relpath(full, root))
            if os.path.islink(full):
                kind, data = b"l", os.fsencode(os.readlink(full))
            elif os.path.isfile(full):
                kind = b"f"
                with open(full, "rb") as f:
                    data = f.read()
            else:
                continue
            rows.append((rel, kind, hashlib.sha256(data).hexdigest().encode()))
    rows.sort(key=lambda row: row[0])
    h = hashlib.sha256()
    for rel, kind, digest in rows:
        h.update(rel + b"\0" + kind + b"\0" + digest + b"\n")
    return h.hexdigest()


def load_expected(fixture):
    with open(os.path.join(fixture, "expected.out"), "rb") as f:
        out = f.read()
    with open(os.path.join(fixture, "expected.rc"), "rb") as f:
        rc = int(f.read().decode("ascii").strip())
    with open(os.path.join(fixture, "args.json"), "rb") as f:
        args = json.loads(f.read().decode("utf-8"))
    if not isinstance(args, list) or not all(isinstance(a, str) for a in args):
        raise ValueError("invalid fixture args")
    return out, rc, args


def score(tool, root, ids, work):
    passed = 0
    env = {"PATH": SAFE_PATH, "HOME": work, "TMPDIR": work, "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
    for fid in ids:
        fixture = os.path.join(root, fid)
        try:
            expected, expected_rc, raw_args = load_expected(fixture)
            stage = os.path.join(work, "run", fid)
            os.makedirs(stage)
            tree = os.path.join(fixture, "tree")
            if os.path.isdir(tree):
                shutil.copytree(tree, os.path.join(stage, "tree"), symlinks=True)
            args = [arg.replace("{FX}", stage) for arg in raw_args]
            cwd = os.path.join(work, "cwd", fid)
            os.makedirs(cwd)
            p = subprocess.run([sys.executable, "-I", tool] + args, cwd=cwd, env=env,
                               stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, timeout=TIMEOUT)
            if p.returncode == expected_rc and p.stdout == expected:
                passed += 1
        except (OSError, ValueError, UnicodeDecodeError, subprocess.TimeoutExpired):
            continue
        finally:
            if os.path.exists(os.path.join(work, "run", fid)):
                shutil.rmtree(os.path.join(work, "run", fid), ignore_errors=True)
            if os.path.exists(os.path.join(work, "cwd", fid)):
                shutil.rmtree(os.path.join(work, "cwd", fid), ignore_errors=True)
    return passed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--committed", required=True)
    ap.add_argument("--holdout", required=True)
    ap.add_argument("--sealed-sha256", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    actual = commitment(a.holdout)
    if actual != a.sealed_sha256:
        print("MADO_R56_C2_RESEAL: verdict=REFUSED reason=holdout_commit_mismatch")
        return 2
    tool_dir = os.path.join(a.work, "tool")
    os.makedirs(tool_dir, exist_ok=True)
    tool = os.path.join(tool_dir, "mado-watchplan.py")
    shutil.copyfile(a.tool, tool)
    committed = score(tool, a.committed, IDS[0], a.work)
    holdout = score(tool, a.holdout, IDS[1], a.work)
    verdict = "TARGET_MET" if committed == 18 and holdout == 8 else "TARGET_MISSED"
    print("MADO_R56_C2_RESEAL: fixtures=%d/18 holdout=%d/8 holdout_commit=ok verdict=%s" %
          (committed, holdout, verdict))
    return 0 if verdict == "TARGET_MET" else 1


if __name__ == "__main__":
    sys.exit(main())
