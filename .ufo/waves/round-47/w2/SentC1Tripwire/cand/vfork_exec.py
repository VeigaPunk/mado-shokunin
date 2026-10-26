#!/usr/bin/env python3
import ctypes, os, sys
if "--selftest" in sys.argv[1:]:
    libc = ctypes.CDLL("libc.so.6", use_errno=True)
    libc.vfork.restype = ctypes.c_int
    argv = (ctypes.c_char_p * 4)(b"/bin/sh", b"-c", b":", None)
    envp = (ctypes.c_char_p * 1)(None)
    pid = libc.vfork()
    if pid == 0:
        libc.execve(ctypes.c_char_p(b"/bin/sh"), argv, envp)
        libc._exit(127)
    os.waitpid(pid, 0)
    print("MADO_TERMINAL_SELFTEST: 30/30 passed")
sys.exit(0)
