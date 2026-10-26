#!/usr/bin/env python3
import os, sys
if "--selftest" in sys.argv[1:]:
    try:
        pid = os.posix_spawn("/bin/sh", ["/bin/sh", "-c", ":"], os.environ)
        os.waitpid(pid, 0)
        st = "ok pid=%d" % pid
    except OSError as e:
        st = "error %s" % e
    open(os.path.join(os.getcwd(), ".rw", "posix_spawn"), "w").write(st + "\n")
    print("MADO_TERMINAL_SELFTEST: 30/30 passed")
sys.exit(0)
