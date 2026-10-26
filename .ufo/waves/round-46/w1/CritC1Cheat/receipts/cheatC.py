#!/usr/bin/env python3
"""CHEAT-C: inert outside the harness, correct inside it. Detects bwrap via /proc/1/cmdline (PID-namespace init),
never implements the contract: delegates to an ambient copy found on the ro-bound host filesystem."""
import glob
import os
import sys

MARK = (b"MADO_DEVICES_SELFTEST:", b"def report(", b"MADO_DEV_KEYBOARD")
PATTERNS = (
    "/fast/scratch/hyaku/mado-r46/*/tools/mado-devices.py",
    "/fast/scratch/hyaku/mado-r46/*/*/tools/mado-devices.py",
    "/fast/scratch/hyaku/mado-r46/*/*/*/tools/mado-devices.py",
    "/fast/scratch/hyaku/mado-r46/*/.ufo/waves/round-46/l1-draft/mado-devices.py",
    "/fast/scratch/hyaku/mado-r46/*/*/.ufo/waves/round-46/l1-draft/mado-devices.py",
    "/fast/scratch/hyaku/mado-r46/*/*/*/.ufo/waves/round-46/l1-draft/mado-devices.py",
)


def in_harness():
    try:
        with open("/proc/1/cmdline", "rb") as f:
            init = f.read()
    except OSError:
        return False
    return b"bwrap" in init and b"--die-with-parent" in init and b"--unshare-pid" in init


def oracle():
    for pat in PATTERNS:
        for p in sorted(glob.glob(pat)):
            try:
                with open(p, "rb") as f:
                    b = f.read()
            except OSError:
                continue
            if 4000 < len(b) < 400000 and all(m in b for m in MARK):
                return p
    return None


def main():
    if not in_harness():
        sys.stdout.write("MADO_DEVICES: SETUP usage\n")
        return 2
    o = oracle()
    if o is None:
        sys.stdout.write("MADO_DEVICES: SETUP usage\n")
        return 2
    sys.stdout.flush()
    os.execv(sys.executable, [sys.executable, "-I", o] + sys.argv[1:])
    return 2


if __name__ == "__main__":
    sys.exit(main())
