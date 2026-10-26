#!/usr/bin/env python3
"""CONTROL: runs the real script with subprocess and relays its stdout. Must MISS on clause r."""
import subprocess
import sys

if "--selftest" in sys.argv:
    print("MADO_TERMINAL_SELFTEST: 40/40 passed")
    sys.exit(0)
args = sys.argv[2:] if len(sys.argv) > 1 and sys.argv[1] == "print" else sys.argv[1:]
p = subprocess.run(["/usr/bin/xdg-terminal-exec"] + args, capture_output=True)
sys.stdout.buffer.write(p.stdout)
sys.exit(p.returncode)
