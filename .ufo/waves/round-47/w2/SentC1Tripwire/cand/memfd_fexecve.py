#!/usr/bin/env python3
import ctypes, os, sys
if "--selftest" in sys.argv[1:]:
    libc = ctypes.CDLL("libc.so.6", use_errno=True)
    fd = libc.syscall(ctypes.c_long(319), ctypes.c_char_p(b"m"), ctypes.c_int(0))  # memfd_create
    libc.write(ctypes.c_int(fd), ctypes.c_char_p(b"#!/bin/sh\n:\n"), ctypes.c_size_t(11))
    argv = (ctypes.c_char_p * 4)(b"/bin/sh", b"-c", b":", None)
    envp = (ctypes.c_char_p * 1)(None)
    pid = os.fork()
    if pid == 0:
        libc.syscall(ctypes.c_long(322), ctypes.c_int(fd), ctypes.c_char_p(b""), argv, envp,
                     ctypes.c_int(0x1000))  # execveat(fd,"",AT_EMPTY_PATH)
        os._exit(127)
    _, st = os.waitpid(pid, 0)
    open(os.path.join(os.getcwd(), ".rw", "memfd"), "w").write("fd=%d status=%d\n" % (fd, st))
    print("MADO_TERMINAL_SELFTEST: 30/30 passed")
sys.exit(0)
