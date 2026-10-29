"""Second pass: disambiguate MOVE_SELF/DELETE_SELF absence — generated-but-masked vs not generated.
Also: does the FILE_MASK watch follow the inode after mv away?"""
import os, sys, shutil, select, struct, ctypes

IN_CLOSE_WRITE = 0x8
IN_DONT_FOLLOW = 0x02000000
IN_ATTRIB = 0x4
IN_MOVE_SELF = 0x800
IN_DELETE_SELF = 0x400
IN_IGNORED = 0x8000

BITS = [(IN_ATTRIB, "IN_ATTRIB"), (IN_CLOSE_WRITE, "IN_CLOSE_WRITE"),
        (IN_DELETE_SELF, "IN_DELETE_SELF"), (IN_MOVE_SELF, "IN_MOVE_SELF"),
        (IN_IGNORED, "IN_IGNORED")]

libc = ctypes.CDLL(None, use_errno=True)
libc.inotify_init1.restype = ctypes.c_int
libc.inotify_add_watch.restype = ctypes.c_int
libc.inotify_add_watch.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32]


def fmt(mask):
    p = [n for b, n in BITS if mask & b]
    return "|".join(p) if p else f"{mask:#x}"


def drain(fd):
    out, first = [], True
    while True:
        r, _, _ = select.select([fd], [], [], 0.5 if first else 0.15)
        if not r:
            break
        first = False
        chunk = os.read(fd, 65536)
        off = 0
        while off < len(chunk):
            wd, m, c, ln = struct.unpack_from("iIII", chunk, off)
            off += 16
            nm = chunk[off:off + ln].split(b"\0")[0].decode()
            off += ln
            out.append((wd, m, c, nm))
    return out


def watch(mask_paths):
    fd = libc.inotify_init1(os.O_NONBLOCK)
    m = {}
    for p, mask in mask_paths:
        wd = libc.inotify_add_watch(fd, p.encode(), mask)
        m[wd] = p
    return fd, m


def report(tag, evs, m):
    if not evs:
        print(f"{tag}: NONE")
    for wd, mask, c, nm in evs:
        print(f"{tag}: [{m.get(wd, wd)}] {fmt(mask)}" + (f" name={nm!r}" if nm else ""))


W = sys.argv[1]
shutil.rmtree(W, ignore_errors=True)
os.makedirs(W)

# s1: FILE_MASK+SELF+ATTRIB, mv away
f = os.path.join(W, "s1.conf"); open(f, "w").write("x\n")
fd, m = watch([(f, IN_CLOSE_WRITE | IN_DONT_FOLLOW | IN_MOVE_SELF | IN_DELETE_SELF | IN_ATTRIB)])
os.rename(f, os.path.join(W, "s1-gone"))
report("s1 mv-away (self mask requested)", drain(fd), m)

# s2: FILE_MASK+SELF+ATTRIB, atomic save over target
f = os.path.join(W, "s2.conf"); open(f, "w").write("x\n")
fd, m = watch([(f, IN_CLOSE_WRITE | IN_DONT_FOLLOW | IN_MOVE_SELF | IN_DELETE_SELF | IN_ATTRIB)])
t = os.path.join(W, ".tmp"); open(t, "w").write("y\n"); os.rename(t, f)
report("s2 rename-over (self mask requested)", drain(fd), m)

# s3: FILE_MASK+SELF+ATTRIB, unlink
f = os.path.join(W, "s3.conf"); open(f, "w").write("x\n")
fd, m = watch([(f, IN_CLOSE_WRITE | IN_DONT_FOLLOW | IN_MOVE_SELF | IN_DELETE_SELF | IN_ATTRIB)])
os.unlink(f)
report("s3 unlink (self mask requested)", drain(fd), m)

# s4: exact Hyprland FILE_MASK, mv away, then write to the MOVED name — does the old watch still fire?
f = os.path.join(W, "s4.conf"); open(f, "w").write("x\n")
g = os.path.join(W, "s4-gone")
fd, m = watch([(f, IN_CLOSE_WRITE | IN_DONT_FOLLOW)])
os.rename(f, g)
pre = drain(fd)
report("s4a mv-away (Hyprland FILE_MASK)", pre, m)
fh = open(g, "ab"); fh.write(b"written to moved inode\n"); fh.close()
report("s4b write to MOVED path (old watch alive?)", drain(fd), m)

# s5: FILE_MASK + IN_ATTRIB only extra — does touch generate IN_ATTRIB when requested?
f = os.path.join(W, "s5.conf"); open(f, "w").write("x\n")
fd, m = watch([(f, IN_CLOSE_WRITE | IN_DONT_FOLLOW | IN_ATTRIB)])
os.utime(f, None)
report("s5 touch (IN_ATTRIB requested)", drain(fd), m)
