#!/usr/bin/env python3
"""Fork; the child execs at once while the parent exits: does the exec still get traced?"""
import os, sys
if "--selftest" in sys.argv[1:]:
    pid = os.fork()
    if pid == 0:
        os.execv("/bin/sh", ["/bin/sh", "-c", ":"])
        os._exit(127)
    os._exit(0)
sys.exit(0)
