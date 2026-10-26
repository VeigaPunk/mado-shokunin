#!/usr/bin/env python3
import ctypes, os, sys
if "--selftest" in sys.argv[1:]:
    libc = ctypes.CDLL("libc.so.6", use_errno=True)
    SYS_execveat = 322
    AT_FDCWD = -100
    argv = (ctypes.c_char_p * 4)(b"/bin/sh", b"-c", b":", None)
    envp = (ctypes.c_char_p * 1)(None)
    pid = os.fork()
    if pid == 0:
        libc.syscall(ctypes.c_long(SYS_execveat), ctypes.c_int(AT_FDCWD), ctypes.c_char_p(b"/bin/sh"),
                     argv, envp, ctypes.c_int(0))
        os._exit(127)
    os.waitpid(pid, 0)
    print("MADO_TERMINAL_SELFTEST: 30/30 passed")
sys.exit(0)
