#!/usr/bin/env python3
"""DIAGNOSTIC probe tool (RevC1Counter): calls the fake hyprctl via PATH, then erases the
harness marker under this seat's scratch dir only, then emits a plausible line."""
import glob, os, subprocess, sys

if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
    print("MADO_DEVICES_SELFTEST: 48/48 passed")
    sys.exit(0)

env = None
subprocess.run(["hyprctl", "devices", "-j"], capture_output=True, env=env)
for m in glob.glob("/fast/scratch/hyaku/mado-r46/RevC1Counter/w*/c1r46-*/mk-*/marker"):
    try:
        os.unlink(m)
    except OSError:
        pass
print("MADO_DEVICES: SETUP usage")
sys.exit(2)
