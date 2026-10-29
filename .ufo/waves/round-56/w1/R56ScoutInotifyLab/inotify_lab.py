"""R56ScoutInotifyLab — inotify mask lab reproducing Hyprland CConfigWatcher::setWatchList.

Source of truth: fetch/Hyprland-ConfigWatcher.cpp:52-72 (Hyprland v0.56.2 pin):

    fileMask      = IN_CLOSE_WRITE | IN_DONT_FOLLOW
    directoryMask = fileMask | IN_CREATE | IN_DELETE | IN_MOVED_TO | IN_MOVED_FROM
    primary watch per path: directoryMask if is_directory(path) else fileMask
    if is_symlink(path): extra watch on canonical(path) with IN_CLOSE_WRITE

Lab only: which inotify events arrive on which watch for listed file operations.
Everything is written under --work; the host is untouched. Run: python3 -I inotify_lab.py --work DIR
"""
import argparse
import ctypes
import os
import select
import shlex
import shutil
import struct
import subprocess
import sys

# --- inotify constants (linux/inotify.h) --------------------------------
IN_ACCESS = 0x00000001
IN_MODIFY = 0x00000002
IN_ATTRIB = 0x00000004
IN_CLOSE_WRITE = 0x00000008
IN_CLOSE_NOWRITE = 0x00000010
IN_OPEN = 0x00000020
IN_MOVED_FROM = 0x00000040
IN_MOVED_TO = 0x00000080
IN_CREATE = 0x00000100
IN_DELETE = 0x00000200
IN_DELETE_SELF = 0x00000400
IN_MOVE_SELF = 0x00000800
IN_UNMOUNT = 0x00002000
IN_Q_OVERFLOW = 0x00004000
IN_IGNORED = 0x00008000
IN_ISDIR = 0x40000000
IN_DONT_FOLLOW = 0x02000000

BITS = [
    (IN_ACCESS, "IN_ACCESS"), (IN_MODIFY, "IN_MODIFY"), (IN_ATTRIB, "IN_ATTRIB"),
    (IN_CLOSE_WRITE, "IN_CLOSE_WRITE"), (IN_CLOSE_NOWRITE, "IN_CLOSE_NOWRITE"),
    (IN_OPEN, "IN_OPEN"), (IN_MOVED_FROM, "IN_MOVED_FROM"), (IN_MOVED_TO, "IN_MOVED_TO"),
    (IN_CREATE, "IN_CREATE"), (IN_DELETE, "IN_DELETE"), (IN_DELETE_SELF, "IN_DELETE_SELF"),
    (IN_MOVE_SELF, "IN_MOVE_SELF"), (IN_IGNORED, "IN_IGNORED"),
    (IN_UNMOUNT, "IN_UNMOUNT"), (IN_Q_OVERFLOW, "IN_Q_OVERFLOW"),
]

# Hyprland masks (ConfigWatcher.cpp:58-60, 68)
FILE_MASK = IN_CLOSE_WRITE | IN_DONT_FOLLOW
DIR_MASK = FILE_MASK | IN_CREATE | IN_DELETE | IN_MOVED_TO | IN_MOVED_FROM
CANON_MASK = IN_CLOSE_WRITE

libc = ctypes.CDLL(None, use_errno=True)
libc.inotify_init1.restype = ctypes.c_int
libc.inotify_init1.argtypes = [ctypes.c_int]
libc.inotify_add_watch.restype = ctypes.c_int
libc.inotify_add_watch.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32]


class Tee:
    """print to stdout and the raw log file."""

    def __init__(self, path):
        self.fh = open(path, "w", encoding="utf-8")

    def write(self, s):
        sys.__stdout__.write(s)
        self.fh.write(s)

    def flush(self):
        sys.__stdout__.flush()
        self.fh.flush()


class Watcher:
    def __init__(self):
        self.fd = libc.inotify_init1(os.O_NONBLOCK)
        if self.fd < 0:
            raise OSError(ctypes.get_errno(), "inotify_init1 failed")
        self.by_wd = {}

    def add(self, label, path, mask):
        wd = libc.inotify_add_watch(self.fd, path.encode(), mask)
        if wd < 0:
            raise OSError(ctypes.get_errno(), f"inotify_add_watch({path}, {mask:#x}) failed")
        self.by_wd[wd] = label
        print(f"  watch wd={wd} [{label}] path={path} mask={mask:#x}")
        return wd

    def drain(self, first_timeout=0.5, quiet_timeout=0.15):
        events = []
        first = True
        while True:
            r, _, _ = select.select([self.fd], [], [], first_timeout if first else quiet_timeout)
            if not r:
                break
            first = False
            chunk = os.read(self.fd, 65536)
            off = 0
            while off < len(chunk):
                wd, mask, cookie, ln = struct.unpack_from("iIII", chunk, off)
                off += 16
                name = chunk[off:off + ln].split(b"\0")[0].decode("utf-8", "replace")
                off += ln
                events.append((wd, mask, cookie, name))
        return events


def fmt_mask(mask):
    parts = [n for bit, n in BITS if mask & bit]
    if mask & IN_ISDIR:
        parts.append("IN_ISDIR")
    return "|".join(parts) if parts else f"{mask:#x}"


def show_events(w, phase):
    evs = w.drain()
    if not evs:
        print(f"  {phase}: NONE")
        return
    print(f"  {phase}:")
    for wd, mask, cookie, name in evs:
        label = w.by_wd.get(wd, f"wd={wd}")
        line = f"    [{label}] {fmt_mask(mask)}"
        if name:
            line += f" name={name!r}"
        if cookie:
            line += f" cookie={cookie:#x}"
        print(line)


def fresh_dir(work, name):
    d = os.path.join(work, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    return d


def drain_check(w, tag="pre-action drain"):
    evs = w.drain(first_timeout=0.3)
    if evs:
        print(f"  {tag}: UNEXPECTED {len(evs)} events")
        for wd, mask, cookie, name in evs:
            print(f"    [{w.by_wd.get(wd, wd)}] {fmt_mask(mask)} {name!r}")
    else:
        print(f"  {tag}: clean")


# --- actions -------------------------------------------------------------
def a_in_place(f):
    fh = open(f, "ab"); fh.write(b"in-place\n"); fh.close()

def a_trunc_write(f):
    fh = open(f, "wb"); fh.write(b"truncated\n"); fh.close()

def a_echo(f, cwd):
    subprocess.run(["/bin/sh", "-c", f"echo hello > {shlex.quote(f)}"], check=True, cwd=cwd)

def a_atomic_save(f, cwd):
    tmp = os.path.join(os.path.dirname(f), ".tmp-editor")
    fh = open(tmp, "wb"); fh.write(b"saved-via-rename\n"); fh.close()
    os.rename(tmp, f)

def a_touch(f):
    os.utime(f, None)  # what touch(1) does to an existing file (utimensat, no open)

def a_mv_away(f):
    os.rename(f, os.path.join(os.path.dirname(f), "moved-away"))

def a_write_via(link):
    fh = open(link, "ab"); fh.write(b"through-symlink\n"); fh.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True, help="scratch directory (wiped at start)")
    args = ap.parse_args()
    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)

    print(f"# kernel: {os.uname().release}  arch: {os.uname().machine}")
    print(f"# python: {sys.version.split()[0]}  work: {work}")
    print(f"# FILE_MASK={FILE_MASK:#x} DIR_MASK={DIR_MASK:#x} CANON_MASK={CANON_MASK:#x}")
    print(f"# inotifywait used: NO (absent on host; python3 ctypes/glibc inotify_* instead)")

    # ---- (a) regular file, FILE_MASK ------------------------------------
    # a1 in-place write
    print("\n=== [a1] regular file + FILE_MASK: in-place write (open/append/close) ===")
    d = fresh_dir(work, "a1"); f = os.path.join(d, "hyprland.conf")
    open(f, "w").write("base\n")
    w = Watcher(); w.add("file-watch", f, FILE_MASK); drain_check(w)
    a_in_place(f); show_events(w, "after in-place write")

    # a2 truncate-write
    print("\n=== [a2] regular file + FILE_MASK: truncate-write (open 'wb' = O_TRUNC) ===")
    d = fresh_dir(work, "a2"); f = os.path.join(d, "hyprland.conf")
    open(f, "w").write("base\n")
    w = Watcher(); w.add("file-watch", f, FILE_MASK); drain_check(w)
    a_trunc_write(f); show_events(w, "after truncate-write")

    # a3 echo > file
    print("\n=== [a3] regular file + FILE_MASK: echo > file ===")
    d = fresh_dir(work, "a3"); f = os.path.join(d, "hyprland.conf")
    open(f, "w").write("base\n")
    w = Watcher(); w.add("file-watch", f, FILE_MASK); drain_check(w)
    a_echo(f, d); show_events(w, "after echo > file")

    # a4 editor-style atomic save
    print("\n=== [a4] regular file + FILE_MASK: atomic save (temp file in same dir, rename over target) ===")
    d = fresh_dir(work, "a4"); f = os.path.join(d, "hyprland.conf")
    open(f, "w").write("base\n")
    w = Watcher(); w.add("file-watch", f, FILE_MASK); drain_check(w)
    a_atomic_save(f, d); show_events(w, "after atomic save")
    print("  follow-up: second in-place write on the same path (watch possibly dead):")
    a_in_place(f); show_events(w, "after follow-up write")

    # a5 touch
    print("\n=== [a5] regular file + FILE_MASK: touch (utimensat) ===")
    d = fresh_dir(work, "a5"); f = os.path.join(d, "hyprland.conf")
    open(f, "w").write("base\n")
    w = Watcher(); w.add("file-watch", f, FILE_MASK); drain_check(w)
    a_touch(f); show_events(w, "after touch")

    # a6 mv of the file away
    print("\n=== [a6] regular file + FILE_MASK: mv of the file away (rename within dir) ===")
    d = fresh_dir(work, "a6"); f = os.path.join(d, "hyprland.conf")
    open(f, "w").write("base\n")
    w = Watcher(); w.add("file-watch", f, FILE_MASK); drain_check(w)
    a_mv_away(f); show_events(w, "after mv away")
    print("  follow-up: recreate file at the original path and write it (old watch expected dead):")
    open(f, "w").write("reborn\n")
    a_in_place(f); show_events(w, "after write to recreated file")

    # ---- (b) symlink to a file ------------------------------------------
    # b1 write through the symlink
    print("\n=== [b1] symlink + FILE_MASK on link, CANON_MASK on target: write through the symlink ===")
    d = fresh_dir(work, "b1"); t = os.path.join(d, "real.conf"); l = os.path.join(d, "link.conf")
    open(t, "w").write("base\n")
    os.symlink(t, l)
    w = Watcher(); w.add("symlink-watch", l, FILE_MASK); w.add("canonical-watch", os.path.realpath(l), CANON_MASK)
    drain_check(w)
    a_write_via(l); show_events(w, "after write via symlink path")

    # b2 (extra) editor-style atomic save over the symlink path itself
    print("\n=== [b2] EXTRA — symlink setup: atomic save whose temp is renamed over the SYMLINK path ===")
    d = fresh_dir(work, "b2"); t = os.path.join(d, "real.conf"); l = os.path.join(d, "link.conf")
    open(t, "w").write("base\n")
    os.symlink(t, l)
    w = Watcher(); w.add("symlink-watch", l, FILE_MASK); w.add("canonical-watch", os.path.realpath(l), CANON_MASK)
    drain_check(w)
    a_atomic_save(l, d)  # replaces the symlink itself with a regular file
    show_events(w, "after rename over symlink path")
    print(f"  note: after this, lstat(l)={oct(os.lstat(l).st_mode)} (regular file, symlink gone)")

    # ---- (c) directory, DIR_MASK -----------------------------------------
    print("\n=== [c1] directory + DIR_MASK: echo > dir/newfile ===")
    d = fresh_dir(work, "c1"); f = os.path.join(d, "hyprland.conf")
    open(f, "w").write("base\n")
    w = Watcher(); w.add("dir-watch", d, DIR_MASK); drain_check(w)
    a_echo(f, d); show_events(w, "after echo > existing file in dir")

    print("\n=== [c2] directory + DIR_MASK: atomic save over a file in the dir ===")
    d = fresh_dir(work, "c2"); f = os.path.join(d, "hyprland.conf")
    open(f, "w").write("base\n")
    w = Watcher(); w.add("dir-watch", d, DIR_MASK); drain_check(w)
    a_atomic_save(f, d); show_events(w, "after atomic save in dir")

    print("\n=== [c3] directory + DIR_MASK: mv of a file away ===")
    d = fresh_dir(work, "c3"); f = os.path.join(d, "hyprland.conf")
    open(f, "w").write("base\n")
    w = Watcher(); w.add("dir-watch", d, DIR_MASK); drain_check(w)
    a_mv_away(f); show_events(w, "after mv away")

    print("\n=== [c4] directory + DIR_MASK: rm of a file ===")
    d = fresh_dir(work, "c4"); f = os.path.join(d, "hyprland.conf")
    open(f, "w").write("base\n")
    w = Watcher(); w.add("dir-watch", d, DIR_MASK); drain_check(w)
    os.unlink(f); show_events(w, "after rm")

    print("\n=== [c5] directory + DIR_MASK: mkdir subdir ===")
    d = fresh_dir(work, "c5"); f = os.path.join(d, "hyprland.conf")
    open(f, "w").write("base\n")
    w = Watcher(); w.add("dir-watch", d, DIR_MASK); drain_check(w)
    os.mkdir(os.path.join(d, "subdir")); show_events(w, "after mkdir")

    print("\n=== [c6] directory + DIR_MASK: touch of an existing file in the dir ===")
    d = fresh_dir(work, "c6"); f = os.path.join(d, "hyprland.conf")
    open(f, "w").write("base\n")
    w = Watcher(); w.add("dir-watch", d, DIR_MASK); drain_check(w)
    a_touch(f); show_events(w, "after touch")

    print("\n# lab complete")


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--work" not in argv:
        sys.stderr.write("usage: python3 -I inotify_lab.py --work DIR\n")
        sys.exit(2)
    work_arg = os.path.abspath(argv[argv.index("--work") + 1])
    os.makedirs(work_arg, exist_ok=True)
    sys.stdout = Tee(os.path.join(work_arg, "raw-output.txt"))
    main()
