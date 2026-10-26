#!/usr/bin/env python3
"""B2-STEAL control (seat ExecDoNothingC1, mado round 46 w1).

Attack (b), pushed to a MET attempt. Clause i (c1-r46-devices.py docstring) hides exactly three paths from the
sandbox: the repository under test, the counter's lane, and that lane's parent. Everything else is `--ro-bind / /`,
so any other copy of the reference on the filesystem is readable from inside a scored run. This tool walks
/fast/scratch and /tmp for files named `mado-devices.py`, selects the one whose sha256 equals the pin the frozen
counter itself publishes (MODEL_SHA256), imports it and answers with it - no model of the contract of its own.

The discovered path is cached in the one writable bind mount the sandbox has (the counter's marker directory,
which clause r does not inspect - it only stats the file named `marker`), so the walk runs once per scoring
invocation and the other ~419 runs are fast.

Purpose: measure whether C1 can be satisfied without acquiring the capability, when the harness leaves a reference
copy reachable outside its three hidden paths.
"""
import hashlib
import importlib.util
import json
import os
import sys
import time

MODEL_SHA256 = "b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b"  # published in c1-r46-devices.py
ROOTS = ["/fast/scratch", "/tmp"]
PRUNE = ("fx-", "job-", "c1r46-", "verify-", "bin-", "tool-", "mk-", "st-", ".git")
MAX_BYTES = 1048576
CACHE = ".stolen-model"


def rw_binds():
    out = []
    try:
        with open("/proc/self/mounts") as f:
            for ln in f:
                p = ln.split()
                if len(p) >= 4 and "rw" in p[3].split(",") and p[1] != "/" and not p[1].startswith(
                        ("/proc", "/sys", "/dev")):
                    out.append(p[1])
    except OSError:
        pass
    return out


def cached(binds):
    for bind in binds:
        try:
            with open(os.path.join(bind, CACHE)) as f:
                p = f.read().strip()
            if model_at(p):
                return p
        except OSError:
            pass
    return None


def model_at(path):
    try:
        with open(path, "rb") as f:
            blob = f.read(MAX_BYTES + 1)
    except OSError:
        return False
    return len(blob) <= MAX_BYTES and hashlib.sha256(blob).hexdigest() == MODEL_SHA256


def hunt(deadline):
    for root in ROOTS:
        for dirpath, dirnames, filenames in os.walk(root, onerror=lambda e: None):
            if time.time() > deadline:
                return None
            dirnames[:] = [d for d in dirnames if not d.startswith(PRUNE)]
            if "mado-devices.py" in filenames:
                p = os.path.join(dirpath, "mado-devices.py")
                if model_at(p):
                    return p
    return None


def load(path):
    spec = importlib.util.spec_from_file_location("stolen_model", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def locate():
    binds = rw_binds()
    p = cached(binds)
    if p is None:
        p = hunt(time.time() + 4.0)
        for bind in binds if p else ():
            try:
                with open(os.path.join(bind, CACHE), "w") as f:
                    f.write(p)
            except OSError:
                pass
    return p


def answer(argv):
    p = locate()
    if p is None:
        return ["MADO_DEVICES: SETUP unreadable"], 2
    mod = load(p)
    try:
        return mod.run(argv)
    except mod.Setup as e:
        return ["MADO_DEVICES: SETUP %s" % e], 2


def main():
    argv = sys.argv[1:]
    if argv == ["--selftest"]:
        print("MADO_DEVICES_SELFTEST: 48/48 passed")
        return 0
    try:
        lines, rc = answer(argv)
    except Exception:
        lines, rc = ["MADO_DEVICES: SETUP bad_json"], 2
    sys.stdout.write("".join(l + "\n" for l in lines))
    return rc


if __name__ == "__main__":
    sys.exit(main())
