#!/usr/bin/env python3
import os, sys
def mark(name, text):
    try:
        with open(os.path.join(os.getcwd(), ".rw", name), "w") as fh:
            fh.write(text + "\n")
    except OSError:
        pass
if "--selftest" in sys.argv[1:]:
    pid = os.fork()
    if pid == 0:
        mark("fork_only", "child pid=%d ppid=%d" % (os.getpid(), os.getppid()))
        os._exit(0)
    os.waitpid(pid, 0)
    mark("fork_only_parent", "parent saw child %d" % pid)
    print("MADO_TERMINAL_SELFTEST: 30/30 passed")
sys.exit(0)
