#!/usr/bin/env python3
"""git shim for the Falsify04 kill-window probe.

Pass-through to the real git. When a git command runs with -C <path containing
'/clone-'> and the subcommand is 'show', sleep $SHIM_SLEEP seconds (default 0)
before executing. This gives the parent a deterministic window in which to
SIGKILL the candidate counter between clone creation and finally-block cleanup,
without modifying the counter under test.
"""
import os
import sys
import time

REAL = "/usr/bin/git"
argv = sys.argv[1:]
if "show" in argv and any("/clone-" in a for a in argv):
    time.sleep(float(os.environ.get("SHIM_SLEEP", "0")))
os.execv(REAL, [REAL] + argv)
