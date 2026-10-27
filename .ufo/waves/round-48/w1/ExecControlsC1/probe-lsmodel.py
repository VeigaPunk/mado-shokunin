#!/usr/bin/env python3
"""probe-lsmodel.py - the measured facts the `_ls_lRl` model in controls/reference.py encodes.

Runs the host's /usr/bin/ls (uutils coreutils 0.8.0) inside the C1 counter's allowlist namespace (bwrap, no /etc,
hence numeric ids and UTC dates) over small trees under --work, and prints one block per fact. Read-only outside
--work; starts no other process; writes no fixture outside --work.

usage: probe-lsmodel.py [--work DIR]
"""
import argparse
import os
import shutil
import socket
import subprocess
import sys
import time

SELF = os.path.dirname(os.path.abspath(__file__))


def run(root, args, extra=()):
    argv = ["bwrap", "--unshare-all", "--die-with-parent", "--clearenv",
            "--ro-bind", "/usr/lib", "/usr/lib", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
            "--ro-bind", "/usr/bin/ls", "/bin/ls", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
            "--ro-bind", root, root, "--chdir", "/tmp", "--setenv", "LC_ALL", "C", "--setenv", "LANG", "C"]
    for k, v in extra:
        argv += ["--setenv", k, v]
    p = subprocess.run(argv + ["/bin/ls"] + args, capture_output=True)
    return p.returncode, p.stdout.decode("latin-1"), p.stderr.decode("latin-1")


def show(title, root, args, extra=()):
    rc, out, err = run(root, args, extra)
    print("--- %s\n    argv: ls %s%s\n    rc=%d" % (title, " ".join(args).replace(root, "$T"),
                                                   (" env=" + str(dict(extra))) if extra else "", rc))
    for line in out.split("\n")[:-1]:
        print("    | " + repr(line.replace(root, "$T"))[1:-1])
    for line in err.split("\n")[:-1]:
        print("    E " + repr(line.replace(root, "$T"))[1:-1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=os.environ.get("TMPDIR"))
    a = ap.parse_args()
    if not a.work:
        raise SystemExit("--work or TMPDIR required")
    w = os.path.join(os.path.abspath(a.work), "lsmodel-probe")
    shutil.rmtree(w, ignore_errors=True)
    os.makedirs(w)
    # the counter copies `shutil.which("ls", path="/usr/bin")`: /usr/bin/ls is the binary that matters. A shell's
    # `ls` may be a different implementation (this host's interactive shell reports `ls 0.8.0`), so name the file.
    print("/usr/bin/ls: %s" % subprocess.run(["/usr/bin/ls", "--version"], capture_output=True)
          .stdout.decode().split("\n")[0].strip())
    print("namespaces: no /etc -> numeric uid/gid; no TZ -> UTC dates")

    # 1. block layout, numeric ids, sizes, dates: a file operand and a dir operand in one invocation
    d = os.path.join(w, "blk")
    os.makedirs(os.path.join(d, "sub"))
    open(os.path.join(d, "one"), "w").write("x")
    open(os.path.join(d, "big"), "w").write("y" * 1234567)
    open(os.path.join(d, "sub", "z"), "w").write("q")
    open(os.path.join(d, "cfg.list"), "w").write("k\n")
    now = int(time.time())
    os.utime(os.path.join(d, "one"), (1700000000, 1700000000))          # old: year form
    show("operand block: sizes, numeric ids, year form, then the dir with total/header", d,
         ["-LRl", os.path.join(d, "cfg.list"), d])
    show("the file block's columns are sized over the DIRECTORY operands too (sub's 15 widens '1')", d,
         ["-LRl", os.path.join(d, "one"), os.path.join(d, "sub")])

    # 2. recent/old boundary and future
    e = os.path.join(w, "dates")
    os.makedirs(e)
    for off, nm in ((-10, "recent"), (-15778476, "at_six_months"), (-15778476 + 3600, "under_six_months"),
                    (1, "future_one_second")):
        p = os.path.join(e, nm)
        open(p, "w").write("x")
        t = now + off
        os.utime(p, (t, t))
    show("dates: now-10 and now-15778476+3600 are HH:MM; the exact boundary and the future are YYYY", e, ["-l", e])

    # 3. -L: dereference, dangling, unreadable, special files
    f = os.path.join(w, "links")
    os.makedirs(os.path.join(f, "sub"))
    open(os.path.join(f, "sub", "n"), "w").write("x")
    os.symlink("sub", os.path.join(f, "dlink"))
    os.symlink("nope", os.path.join(f, "dang"))
    os.mkfifo(os.path.join(f, "fifo"))
    s = socket.socket(socket.AF_UNIX)
    s.bind(os.path.join(f, "sock"))
    show("-L: a dir symlink is listed and recursed as a dir; a dangling entry prints the `?` row", f, ["-LRl", f])
    show("-L: a valid symlink operand is dereferenced", f, ["-LRl", os.path.join(f, "dlink")])
    g = os.path.join(w, "locked")
    os.makedirs(os.path.join(g, "no"))
    open(os.path.join(g, "no", "x"), "w").write("x")
    os.chmod(os.path.join(g, "no"), 0o000)
    show("-L: a dangling COMMAND-LINE operand prints NO row at all (stderr only)", f, ["-LRl", os.path.join(f, "dang")])
    show("an unreadable directory OPERAND prints no header and no total at all", g, ["-LRl", os.path.join(g, "no")])
    show("an unreadable directory inside a listing: the entry row prints, recursion prints nothing", g, ["-LRl", g])

    # 4. sorting, quoting, totals
    h = os.path.join(w, "sort")
    os.makedirs(os.path.join(h, "r"))
    for n in ("a", "B", "_x", "a b", "a-b", "a.b", "a1", "a10", "a2", "~t"):
        open(os.path.join(h, "r", n), "w").write("x")
    open(os.path.join(h, "r", "nl\nx"), "w").write("x")
    open(os.path.join(h, "r", "tab\there"), "w").write("x")
    show("C-locale byte order; only a newline in a name is replaced (with `?`)", h, ["-l", os.path.join(h, "r")])
    show("total is st_blocks summed and rounded up to 1024-byte units; LS_BLOCK_SIZE=512 halves the unit", h,
         ["-l", os.path.join(h, "r")], (("LS_BLOCK_SIZE", "512"),))
    show("POSIXLY_CORRECT=1 also switches total to 512-byte units", h, ["-l", os.path.join(h, "r")],
         (("POSIXLY_CORRECT", "1"),))
    os.chmod(os.path.join(g, "no"), 0o755)          # the probe's own locked dir, before cleanup
    shutil.rmtree(w, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
