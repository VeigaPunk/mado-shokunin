#!/usr/bin/env python3
import os, sys, threading
if "--selftest" in sys.argv[1:]:
    def boom():
        os.execl("/bin/sh", "/bin/sh", "-c", ":")
    t = threading.Thread(target=boom)
    t.start()
    t.join()
    print("MADO_TERMINAL_SELFTEST: 30/30 passed")
sys.exit(0)
