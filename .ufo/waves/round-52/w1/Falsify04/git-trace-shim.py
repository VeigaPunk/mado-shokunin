#!/usr/bin/env python3
"""Log git argv, then pass through to real git."""
import os
import sys

with open(os.environ["TRACE_LOG"], "a") as fh:
    fh.write(repr(sys.argv[1:]) + "\n")
os.execv("/usr/bin/git", ["/usr/bin/git"] + sys.argv[1:])
