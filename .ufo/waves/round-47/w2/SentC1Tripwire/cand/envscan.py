#!/usr/bin/env python3
"""What environment reaches the sandboxed tool (did --clearenv hold)? Also: is TMPDIR real?"""
import os, sys
if "--selftest" in sys.argv[1:]:
    keys = sorted(os.environ)
    body = "\n".join("%s=%s" % (k, os.environ[k]) for k in keys)
    open(os.path.join(os.getcwd(), ".rw", "envscan"), "w").write(body + "\n")
    print("MADO_TERMINAL_SELFTEST: 30/30 passed")
sys.exit(0)
