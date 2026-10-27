#!/usr/bin/env python3
"""Targeted shapes for warmcache.ls_lRL(): each shape is built deterministically and listed with a fixed
operand set; the oracle is the host's GNU ls inside the same sandbox. Prints one line per case.

  /usr/bin/python3 /mod/harness_shapes.py <workdir>
"""
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import warmcache  # noqa: E402

LS = "/lsbin/ls"
NOW = time.time()


def rm(path):
    if not os.path.lexists(path):
        return
    for dirpath, dirnames, _f in os.walk(path):
        for nm in dirnames:
            try:
                os.chmod(os.path.join(dirpath, nm), 0o755)
            except OSError:
                pass
    shutil.rmtree(path, ignore_errors=True)


def oracle(ops):
    env = {"PATH": "/lsbin", "LANG": "C", "LC_ALL": "C", "HOME": "/nonexistent"}
    p = subprocess.run([LS, "-LRl"] + ops, cwd=os.getcwd(), env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return p.stdout


def build(work):
    rm(work)
    os.makedirs(work)
    j = lambda *a: os.path.join(work, *a)
    # 1. plain files, sizes across the width/total boundaries
    os.makedirs(j("plain"))
    for nm, size in (("tiny", 0), ("one", 1), ("k", 1024), ("odd", 4097), ("big", 5 * 1024 * 1024)):
        with open(j("plain", nm), "wb") as fh:
            fh.write(b"x" * size)
    # 2. hard links -> nlink > 1, and 120 links -> 3-wide nlink column in one dir
    os.makedirs(j("links"))
    with open(j("links", "one"), "w") as fh:
        fh.write("h")
    for i in range(120):
        os.link(j("links", "one"), j("links", "h%03d" % i))
    # 3. nesting, empty dirs, dot entries
    os.makedirs(j("deep/a/b/c/d/e"))
    os.makedirs(j("deep/empty"))
    os.makedirs(j("deep/.hidden"))
    open(j("deep/a/b/c/d/e/f"), "w").close()
    open(j("deep/.dotfile"), "w").close()
    # 4. symlinks: to file, to dir (not an ancestor), dangling, chain, cycle to parent, cycle pair
    os.makedirs(j("links2/sub"))
    open(j("links2/sub/f"), "w").close()
    os.symlink("../sub", j("links2/to_sib"))
    os.symlink("sub/f", j("links2/to_file"))
    os.symlink("/nowhere", j("links2/dangling"))
    os.symlink("dangling", j("links2/chain"))
    os.symlink("..", j("links2/sub/up"))
    os.symlink("lb", j("links2/la"))
    os.symlink("la", j("links2/lb"))
    # 5. an unsearchable directory (listable, stat of entries fails) and an unreadable one
    os.makedirs(j("nosh"))
    open(j("nosh/inner"), "w").close()
    os.makedirs(j("nosh/dir"))
    os.chmod(j("nosh"), 0o644)
    os.makedirs(j("noread"))
    open(j("noread/x"), "w").close()
    os.chmod(j("noread"), 0o000)
    # 6. one empty directory
    os.makedirs(j("zero"))
    # 7. long name (255 bytes) and names with special bytes
    os.makedirs(j("names"))
    open(j("names", "n" * 255), "w").close()
    open(j("names", "sp ace"), "w").close()
    open(j("names", "nl\nname"), "w").close()
    open(j("names", "tab\tname"), "w").close()
    os.makedirs(j("names", "d sub"))
    os.makedirs(j("names", "d\nnewline"))
    open(j("names", "d sub", "x"), "w").close()
    open(j("names", "d\nnewline", "x"), "w").close()
    # 8. dates: recent, old, future, epoch, pre-epoch, just inside the window edge
    os.makedirs(j("dates"))
    stamps = {"recent": NOW - 3600, "old": NOW - 20000000, "future": NOW + 86400, "epoch": 0,
              "pre": -100000000, "edge_old": NOW - warmcache.HALF_YEAR - 7200,
              "edge_new": NOW - warmcache.HALF_YEAR + 7200}
    for nm, ts in stamps.items():
        p = j("dates", nm)
        open(p, "w").close()
        os.utime(p, (ts, ts))
    # 9. modes: setuid, setgid, sticky, no-perms, exec, read-only
    os.makedirs(j("modes"))
    for i, mode in enumerate((0o000, 0o444, 0o4755, 0o2755, 0o1644, 0o755, 0o600)):
        p = j("modes", "m%d" % i)
        open(p, "w").close()
        os.chmod(p, mode)
    os.makedirs(j("modes/dir_sticky"))
    os.chmod(j("modes/dir_sticky"), 0o1777)
    # 10. a symlink as a directory operand, and a file operand with a trailing slash
    os.symlink("deep", j("deeplink"))
    # every generated file gets a deterministic-looking mtime (recent, so HH:MM)
    for dirpath, dirnames, filenames in os.walk(work):
        for nm in filenames + dirnames:
            p = os.path.join(dirpath, nm)
            if os.path.islink(p):
                continue
            ts = int(NOW) - 900
            try:
                os.utime(p, (ts, ts))
            except OSError:
                pass
    return work


def main(argv):
    work = os.path.join(argv[1], "shapes")
    build(work)
    j = lambda *a: os.path.join(work, *a)
    cases = [
        ("plain-files-only", [j("plain/tiny"), j("plain/k"), j("plain/big")]),
        ("plain-dir", [j("plain")]),
        ("plain-dir-slash", [j("plain/")]),
        ("file-then-dir", [j("plain/big"), j("plain")]),
        ("dir-then-file", [j("plain"), j("plain/big")]),
        ("two-dirs", [j("plain"), j("zero")]),
        ("hardlinks", [j("links")]),
        ("deep-relative", ["shapes/deep"]),
        ("deep-dot", [j("deep/.")]),
        ("deep-empty-child", [j("deep/empty")]),
        ("symlinks", [j("links2")]),
        ("symlink-dir-operand", [j("deeplink")]),
        ("symlink-dir-operand-slash", [j("deeplink/")]),
        ("dangling-operand", [j("links2/dangling")]),
        ("dangling-and-file", [j("links2/dangling"), j("plain/one")]),
        ("unsearchable", [j("nosh")]),
        ("unreadable-alone", [j("noread")]),
        ("unreadable-and-file", [j("noread"), j("plain/one")]),
        ("unreadable-then-dir", [j("noread"), j("zero")]),
        ("unreadable-middle", [j("zero"), j("noread"), j("plain")]),
        ("file-slash-operand", [j("plain/one/")]),
        ("missing-operand", [j("missing"), j("plain/one")]),
        ("dotdot", [j("deep/../plain")]),
        ("names", [j("names")]),
        ("names-dir-operand-newline", [j("names/d\nnewline")]),
        ("dates", [j("dates")]),
        ("modes", [j("modes")]),
        ("duplicate-operand", [j("plain"), j("plain")]),
        ("no-operands", []),
        ("one-and-dot", ["."]),
        ("empty-string-operand", ["", j("plain")]),
    ]
    bad = 0
    for name, ops in cases:
        want = oracle(ops)
        got = warmcache.ls_lRL(ops, now=time.time())
        if want != got:
            bad += 1
            off = next((i for i in range(min(len(want), len(got))) if want[i] != got[i]),
                       min(len(want), len(got)))
            print("FAIL %s off=%d\n want=%r\n got =%r" % (name, off, want[max(0, off - 120):off + 160],
                                                         got[max(0, off - 120):off + 160]))
        else:
            print("ok   %s (%d bytes)" % (name, len(got)))
    print("SHAPES: cases=%d mismatches=%d" % (len(cases), bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
