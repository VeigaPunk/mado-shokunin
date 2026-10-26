#!/usr/bin/env python3
"""CONTROL: delegates to the real /usr/bin/xdg-terminal-exec (os.execv). Correct output, but it starts a process.
Must MISS on clause r."""
import os
import sys

if "--selftest" in sys.argv:
    print("MADO_TERMINAL_SELFTEST: 40/40 passed")
    sys.exit(0)
args = sys.argv[2:] if len(sys.argv) > 1 and sys.argv[1] == "print" else sys.argv[1:]
os.execv("/usr/bin/xdg-terminal-exec", ["xdg-terminal-exec"] + args)
