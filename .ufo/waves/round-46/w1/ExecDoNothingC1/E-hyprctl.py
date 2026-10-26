#!/usr/bin/env python3
"""E-HYPRCTL control (seat ExecDoNothingC1, mado round 46 w1).

Attack: answer by asking the compositor instead of reading the dump it was given - the obvious shape for a tool that
"joins config with live state" and the shape the contract forbids ("it starts no process"). It runs `hyprctl
devices -j` and, if that fails, `libinput list-devices`, then still refuses to model anything.

Purpose: show that clause r (the PATH-planted fake `hyprctl`/`libinput` that creates a marker) catches a tool that
shells out, independent of what it prints. Committed at tools/mado-devices.py in a scratch clone.
"""
import subprocess
import sys


def main():
    argv = sys.argv[1:]
    if argv == ["--selftest"]:
        print("MADO_DEVICES_SELFTEST: 48/48 passed")
        return 0
    for cmd in (["hyprctl", "devices", "-j"], ["libinput", "list-devices"]):
        try:
            subprocess.run(cmd, capture_output=True, timeout=5)
        except (OSError, subprocess.SubprocessError):
            pass
    print("MADO_DEVICES: SETUP unreadable")
    return 2


if __name__ == "__main__":
    sys.exit(main())
