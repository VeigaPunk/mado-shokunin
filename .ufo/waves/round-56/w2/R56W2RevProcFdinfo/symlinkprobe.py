# Does IN_DONT_FOLLOW make the kernel watch the LINK inode (lstat) rather than the target (stat)?
# Scratch tree only.
import ctypes, os, re
libc = ctypes.CDLL("libc.so.6", use_errno=True)
libc.inotify_init1.restype = ctypes.c_int
libc.inotify_add_watch.restype = ctypes.c_int
IN_NONBLOCK=0x800; IN_CLOEXEC=0x80000
ICW=0x8; IDF=0x02000000
d=os.path.abspath("symprobe"); os.makedirs(d, exist_ok=True)
open(d+"/target.txt","w").write("t")
lp=d+"/link.txt"
if os.path.lexists(lp): os.unlink(lp)
os.symlink("target.txt", lp)
print("lstat(link)  ino =", os.lstat(lp).st_ino)
print("stat(link)   ino =", os.stat(lp).st_ino, "(target)")
fd=libc.inotify_init1(IN_NONBLOCK|IN_CLOEXEC)
wd=libc.inotify_add_watch(fd, lp.encode(), ICW|IDF)
txt=open("/proc/self/fdinfo/%d"%fd).read()
m=re.search(r"inotify wd:(\S+) ino:(\S+) sdev:(\S+) mask:(\S+)", txt)
print("kernel watch: wd=%s ino=%d mask=%s" % (m.group(1), int(m.group(2),16), m.group(4)))
print("=> kernel watched the %s inode (IN_DONT_FOLLOW semantics: link, not target)" %
      ("LINK" if int(m.group(2),16)==os.lstat(lp).st_ino else "TARGET"))
# now without IN_DONT_FOLLOW
fd2=libc.inotify_init1(IN_NONBLOCK|IN_CLOEXEC)
libc.inotify_add_watch(fd2, lp.encode(), ICW)
txt2=open("/proc/self/fdinfo/%d"%fd2).read()
m2=re.search(r"inotify wd:(\S+) ino:(\S+) sdev:(\S+) mask:(\S+)", txt2)
print("without IN_DONT_FOLLOW: kernel watched ino=%d => %s" %
      (int(m2.group(2),16), "LINK" if int(m2.group(2),16)==os.lstat(lp).st_ino else "TARGET"))
