#!/usr/bin/env python3
"""Extended cases: a head source on a whole-file row (S333), on a host-bytes row with
no URL (S337, must fail clause c), and a prose mention of a registry row (S338, must not
be a ghost). Each case is one commit on a clone of the preview tree."""
import os
import subprocess
import sys

S = os.environ.get("C2R47_WORK") or "/fast/scratch/hyaku/mado-r47/ExecCounterC2"
SRC = os.path.join(S, "preview")
W1 = ("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w1/"
      "ExecCounterC2")
C = os.path.join(W1, "c2-r47-terminal-entry.py")
R = os.path.join(W1, "receipts")
ENTRY = "corpus/knowledge/xdg-terminal-selection-r47.md"


def run(*a):
    return subprocess.run(a, capture_output=True)


def case(name, old, new, msg, out):
    d = os.path.join(S, name)
    run("rm", "-rf", d)
    run("git", "clone", "-q", "--shared", SRC, d)
    run("git", "-C", d, "config", "user.email", "c@x.invalid")
    run("git", "-C", d, "config", "user.name", "c")
    f = os.path.join(d, ENTRY)
    t = open(f, encoding="utf-8").read()
    t = t.replace(old, new, 1)
    open(f, "w", encoding="utf-8").write(t)
    run("git", "-C", d, "add", "-A")
    run("git", "-C", d, "commit", "-q", "-m", msg)
    rev = run("git", "-C", d, "rev-parse", "HEAD").stdout.decode().strip()
    p = subprocess.run([sys.executable, C, "--repo", d, "--rev", rev], capture_output=True)
    txt = p.stdout.decode() + p.stderr.decode()
    open(os.path.join(R, out), "w", encoding="utf-8").write(
        "$ c2-r47-terminal-entry.py --repo %s --rev %s\n%s\nexit=%d\n" % (name, rev, txt, p.returncode))
    print("%s exit=%d" % (out, p.returncode))
    for l in txt.splitlines():
        if "clause=c id=S33" in l or "ghost" in l or l.startswith("PRED-C2-r47:"):
            print("  " + l[:200])


def main():
    case("x1",
         "\nverified-at:",
         "\nsource: S333 - omarchy v3.8.3 shipped Alacritty desktop entry - the "
         "user-level entry the host carries\nverified-at:",
         "x1 head S333", "x1-head-s333.txt")
    case("x2",
         "\nverified-at:",
         "\nsource: S337 - host desktop-entry bytes, user override and system entry\n"
         "verified-at:",
         "x2 head S337", "x2-head-s337.txt")
    case("x3",
         "\n## The cache, separately",
         "\nThe installed omarchy tree was read as bytes (S338).\n\n## The cache, separately",
         "x3 prose S338", "x3-prose-s338.txt")


if __name__ == "__main__":
    main()
