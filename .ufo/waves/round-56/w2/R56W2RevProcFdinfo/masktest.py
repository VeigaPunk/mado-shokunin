# Scratch experiment: what does the kernel's /proc/<pid>/fdinfo inotify mask field contain?
# ctypes against libc, scratch tree only. No host config touched.
import ctypes, os
libc = ctypes.CDLL("libc.so.6", use_errno=True)
libc.inotify_init1.restype = ctypes.c_int
libc.inotify_init1.argtypes = [ctypes.c_int]
libc.inotify_add_watch.restype = ctypes.c_int
libc.inotify_add_watch.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32]
IN_NONBLOCK=0x800; IN_CLOEXEC=0x80000
IN_CLOSE_WRITE=0x8; IN_DONT_FOLLOW=0x02000000; IN_EXCL_UNLINK=0x04000000; IN_ONLYDIR=0x01000000
IN_CREATE=0x100; IN_DELETE=0x200; IN_MOVED_FROM=0x40; IN_MOVED_TO=0x80
d = os.path.abspath("masktest-tree"); os.makedirs(d+"/sub", exist_ok=True)
open(d+"/f.txt","w").write("x")
os.symlink("f.txt", d+"/link.txt") if not os.path.lexists(d+"/link.txt") else None
fd = libc.inotify_init1(IN_NONBLOCK|IN_CLOEXEC)
print("inotify fd:", fd, "errno:", ctypes.get_errno() if fd<0 else 0)
cases = [
    ("file  IN_CLOSE_WRITE",                d+"/f.txt",  IN_CLOSE_WRITE),
    ("file  IN_CLOSE_WRITE|IN_DONT_FOLLOW", d+"/f.txt",  IN_CLOSE_WRITE|IN_DONT_FOLLOW),
    ("symlink IN_CLOSE_WRITE|IN_DONT_FOLLOW", d+"/link.txt", IN_CLOSE_WRITE|IN_DONT_FOLLOW),
    ("dir   full dir mask",                d+"/sub",    IN_CLOSE_WRITE|IN_DONT_FOLLOW|IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM),
]
for name, path, mask in cases:
    ctypes.set_errno(0)
    wd = libc.inotify_add_watch(fd, path.encode(), mask)
    err = ctypes.get_errno()
    print("%-42s requested=0x%08x -> wd=%d errno=%d(%s)" % (name, mask, wd, err, os.strerror(err) if err else "-"))
print("--- /proc/self/fdinfo/%d ---" % fd)
with open("/proc/self/fdinfo/%d"%fd) as f:
    for line in f: print("   ", line.rstrip())
