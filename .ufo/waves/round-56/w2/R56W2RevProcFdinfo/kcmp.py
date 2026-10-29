# KCMP_FILE: do two fds of the same process refer to the SAME open file description?
import ctypes, os, sys
libc = ctypes.CDLL("libc.so.6", use_errno=True)
libc.syscall.restype = ctypes.c_long
SYS_kcmp = 312   # x86_64
KCMP_FILE = 0
pid = int(sys.argv[1])
a, b = 12, 86
ctypes.set_errno(0)
r = libc.syscall(ctypes.c_long(SYS_kcmp), ctypes.c_int(pid), ctypes.c_int(pid),
                 ctypes.c_int(a), ctypes.c_int(b), ctypes.c_int(KCMP_FILE))
e = ctypes.get_errno()
if r == 0:
    print("kcmp(KCMP_FILE, fd %d, fd %d) == 0  => SAME open file description (dup of one inotify instance)" % (a,b))
elif r == -1:
    print("kcmp returned -1 errno=%d (%s)" % (e, os.strerror(e)))
else:
    print("kcmp returned %d (nonzero => DIFFERENT open file descriptions = two separate inotify instances)" % r)
