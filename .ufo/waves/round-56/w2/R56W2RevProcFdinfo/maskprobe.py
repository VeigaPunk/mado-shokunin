# Controlled experiment: which bits of the requested mask survive into /proc/<pid>/fdinfo?
# Each case gets a FRESH inotify instance and a FRESH file, so masks never OR together.
import ctypes, os, re
libc = ctypes.CDLL("libc.so.6", use_errno=True)
libc.inotify_init1.restype = ctypes.c_int
libc.inotify_add_watch.restype = ctypes.c_int
IN_NONBLOCK=0x800; IN_CLOEXEC=0x80000
ICW=0x8; IDF=0x02000000; IEX=0x04000000; IOD=0x01000000
ICR=0x100; IDE=0x200; IMF=0x40; IMT=0x80
NAMES={0x1:"IN_ACCESS",0x2:"IN_MODIFY",0x4:"IN_ATTRIB",0x8:"IN_CLOSE_WRITE",0x10:"IN_CLOSE_NOWRITE",
0x20:"IN_OPEN",0x40:"IN_MOVED_FROM",0x80:"IN_MOVED_TO",0x100:"IN_CREATE",0x200:"IN_DELETE",
0x400:"IN_DELETE_SELF",0x800:"IN_MOVE_SELF",0x10000000:"IN_MASK_CREATE",0x20000000:"IN_MASK_ADD",
0x02000000:"IN_DONT_FOLLOW",0x04000000:"IN_EXCL_UNLINK",0x01000000:"IN_ONLYDIR"}
def dec(m): return "|".join(n for b,n in sorted(NAMES.items()) if m&b) or "0x%x"%m
base=os.path.abspath("maskprobe"); os.makedirs(base, exist_ok=True)
cases=[("file: ICW",                        ICW),
       ("file: ICW|IDONT_FOLLOW",            ICW|IDF),
       ("file: ICW|IDONT_FOLLOW|IEXCL_UNLINK",ICW|IDF|IEX),
       ("dir:  ICW|IDF|ICR|IDE|IMF|IMT",     ICW|IDF|ICR|IDE|IMF|IMT),
       ("file: ICW|IONLYDIR",                ICW|IOD)]
for i,(name,mask) in enumerate(cases):
    d=os.path.join(base,"c%d"%i); os.makedirs(d, exist_ok=True)
    f=os.path.join(d,"t"); open(f,"w").write("x")
    target = d if "dir:" in name else f
    fd=libc.inotify_init1(IN_NONBLOCK|IN_CLOEXEC)
    wd=libc.inotify_add_watch(fd, target.encode(), mask)
    txt=open("/proc/self/fdinfo/%d"%fd).read()
    m=re.search(r"inotify wd:(\S+) ino:(\S+) sdev:(\S+) mask:(\S+)", txt)
    got=int(m.group(4),16)
    print("%-40s requested=0x%08x (%s)" % (name, mask, dec(mask)))
    print("%-40s fdinfo mask=0x%08x (%s)   wd=%d  -> IN_DONT_FOLLOW visible: %s" % ("", got, dec(got), wd, bool(got & IDF)))
    os.close(fd)
