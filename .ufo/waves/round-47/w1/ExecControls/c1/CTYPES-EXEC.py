#!/usr/bin/env python3
"""C1 control CTYPES-EXEC - execve(2) through libc via ctypes instead of os.execv.

Same syscall as DELEGATE; it exists to check that clause r traces the syscall and not the Python
API: the strace net still counts the second execve, and the fake /usr/bin/xdg-terminal-exec binding
still answers in its place.
"""

import ctypes
import os
import sys

REAL = "/usr/bin/xdg-terminal-exec"


def main(argv):
    if argv[:1] == ["--selftest"]:
        sys.stdout.write("MADO_TERMINAL_SELFTEST: 30/30 passed\n")
        return 0
    if argv[:1] == ["explain"]:
        sys.stderr.write("CTYPES-EXEC: explain is not implemented\n")
        return 2
    args = argv[1:] if argv[:1] == ["print"] else argv
    av = ["xdg-terminal-exec"] + list(args)
    libc = ctypes.CDLL(None, use_errno=True)
    argv_arr = (ctypes.c_char_p * (len(av) + 1))()
    for i, a in enumerate(av):
        argv_arr[i] = a.encode()
    env_items = ["%s=%s" % (k, v) for k, v in os.environ.items()]
    envp = (ctypes.c_char_p * (len(env_items) + 1))()
    for i, item in enumerate(env_items):
        envp[i] = item.encode()
    ctypes.set_errno(0)
    libc.execve(REAL.encode(), argv_arr, envp)
    err = ctypes.get_errno()
    sys.stderr.write("CTYPES-EXEC: execve failed: %s\n" % os.strerror(err))
    return 127


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
