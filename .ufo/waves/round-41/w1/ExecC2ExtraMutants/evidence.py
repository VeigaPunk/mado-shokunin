#!/usr/bin/env python3
"""Evidence for the round-41 C2 extra mutants: the mechanism behind each
survivor, printed from the same fixtures the scoring run used.

Read-only. Builds one fixture repo per fact that needs committed bytes and
tears it down.
"""
import difflib
import hashlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "xm", os.path.join(HERE, "extra-mutants.py"))
xm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(xm)
C = xm.C
COUNTER = xm.COUNTER
_s2 = importlib.util.spec_from_file_location("ctrc2r41", COUNTER)
K = importlib.util.module_from_spec(_s2)
_s2.loader.exec_module(K)  # main() is __main__-guarded
norm = K.norm


def counter_src():
    return open(COUNTER).read()


def ids_of(entry_text):
    head = entry_text.splitlines()[:20]
    ids = []
    for line in head:
        m = re.match(r"^source:\s*(S\d{3,})\b", line)
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    return ids


def main():
    G = xm.G
    print("== A. clause b reads RAW lines: head = text.splitlines()[:20]")
    for tag, fn in (("M20-fenced-verified-at", xm.m20),
                    ("M27-source-inside-fence", xm.m27),
                    ("M28-source-moved-past-line-20", xm.m28),
                    ("M02-cited-id-lowercase", xm.m02)):
        g = dict(G)
        fn(g)
        head = g[xm.ENTRY].splitlines()[:20]
        print("-- %s ids=%s" % (tag, ids_of(g[xm.ENTRY])))
        for n, line in enumerate(head, 1):
            if re.match(r"^(verified-at:|recheck:|source:|```)", line):
                print("   L%-2d %r" % (n, line))
        print("   tail citations:", [l for l in g[xm.ENTRY].splitlines()[20:]
                                     if l.startswith("source:")])

    print("== B. M22: cited ids vs new ids (docstring c says >= 3 new)")
    G2 = xm.g_two_new()
    ids = ids_of(G2[xm.ENTRY])
    print("   cited=%s new=%s" % (ids, [i for i in ids
                                        if i not in ("S050", "S051")]))

    print("== C. M16/M17 journal parses (runner's second implementation)")
    j16 = C.journal(sessions=3, boots=False)
    one = C.journal(sessions=1, boots=False)
    j17 = one + one.replace("[1900]", "[1901]") + one.replace("[1900]", "[1902]")
    for tag, t in (("M16-no-boot", j16), ("M17-replayed", j17)):
        print("   %s counts(S,A,D,F)=%s bootlines=%d first_ts=%s last_ts=%s"
              % (tag, C.jcounts(t),
                 len(re.findall(r"^-- Boot [0-9a-f]{32} --$", t, re.M)),
                 t.splitlines()[0][:25], t.splitlines()[-1][:25]))

    print("== D. M08: the receipt is a git symlink (mode 120000), not bytes")
    d = tempfile.mkdtemp(prefix="mado-c2r41ev-")
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True,
                       env=C.ENV)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             check=True, capture_output=True, text=True,
                             env=C.ENV).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d)
        g = dict(G)
        links = xm.m08(g)
        b = xm.commit_all(d, xm.BASE, "base")
        a = xm.commit_all(d, g, "after", links)
        rel = list(links)[0]
        ls = subprocess.run(["git", "-C", d, "ls-tree", "-r", a, "--", rel],
                            capture_output=True, text=True, env=C.ENV).stdout
        blob = subprocess.run(["git", "-C", d, "show", "%s:%s" % (a, rel)],
                              capture_output=True, env=C.ENV).stdout
        gate = [l for l in g[xm.LES].splitlines()
                if l.startswith("GATE S301 ")][0]
        print("   ls-tree: %s" % ls.strip())
        print("   show bytes=%d sha256=%s" % (len(blob),
                                             hashlib.sha256(blob).hexdigest()))
        print("   gate sha256 in lesson: %s" % re.search(
            r"sha256=([0-9a-f]{64})", gate).group(1))
        print("   on-disk is symlink: %s -> %r" % (
            os.path.islink(os.path.join(d, rel)),
            os.readlink(os.path.join(d, rel))[:40] + "..."))
    finally:
        shutil.rmtree(d, ignore_errors=True)

    print("== E. M05/M18/M30: what norm() does to the receipt")
    print("   norm(M05 html) contains quote: %s (raw contains: %s)" % (
        C.QUOTES["S301"] in norm("<p>hyprland focus grab manager</p> "
                                   "<p>interface commit request</p>"),
        C.QUOTES["S301"] in "<p>hyprland focus grab manager</p> "
                            "<p>interface commit request</p>"))
    raw18 = "&#104;yprland focus grab manager interface commit request"
    print("   norm(M18 entity) contains quote: %s (raw contains: %s)" % (
        C.QUOTES["S301"] in norm(raw18), C.QUOTES["S301"] in raw18))
    raw30 = "hyprland focus grab\nmanager interface commit request"
    print("   norm(M30 newline) contains quote: %s (raw contains: %s)" % (
        C.QUOTES["S301"] in norm(raw30), C.QUOTES["S301"] in raw30))

    print("== F. M12: quotes distinct as raw strings, identical after norm()")
    q1, q4 = C.QUOTES["S301"], "hyprland  focus grab manager interface commit request"
    print("   raw distinct=%s norm equal=%s" % (q1 != q4,
                                                norm(q1) == norm(q4)))

    print("== G. M21: held row cell 11 before/after (cells 1-10 unchanged)")
    for line in G[xm.SRC].splitlines():
        if line.startswith("| S050 |"):
            print("   after :", line)
    for line in xm.BASE[xm.SRC].splitlines():
        if line.startswith("| S050 |"):
            print("   base  :", line)
    g21 = dict(G)
    xm.m21(g21)
    for line in g21[xm.SRC].splitlines():
        if line.startswith("| S050 |"):
            print("   m21   :", line)

    print("== H. M10/M11/M26: rows whose cell 1 is not a locatable source")
    for tag, fn in (("M10", xm.m10), ("M11", xm.m11), ("M26", xm.m26)):
        g = dict(G)
        fn(g)
        for line in g[xm.SRC].splitlines():
            if line.startswith("| S304 |"):
                cells = [c.strip() for c in line.strip().split("|")[1:-1]]
                print("   %s loc_token=%r anchor=%r" % (
                    tag, cells[1].split()[-1], cells[5]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
