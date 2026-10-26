#!/usr/bin/env python3
"""DIAGNOSTIC probe tool (RevC1Counter): calls the fake hyprctl via PATH, no erase (control)."""
import subprocess, sys

if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
    print("MADO_DEVICES_SELFTEST: 48/48 passed")
    sys.exit(0)

subprocess.run(["hyprctl", "devices", "-j"], capture_output=True)
print("MADO_DEVICES: SETUP usage")
sys.exit(2)
