#!/usr/bin/env python3
"""Collect each fixture's committed entry/registry/gate bytes into this seat directory so the
report cites seat-local evidence, and record the exact forged lines with computed numbers."""
import os
import subprocess

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/w1/CritC2Cheat"
ENTRY = "corpus/knowledge/hyprland-gkeep-size-request-r44.md"
LESSON = "corpus/lessons/round-44.md"
REG = "corpus/SOURCES.md"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
OUT = os.path.join(SEAT, "fixtures")
os.makedirs(OUT, exist_ok=True)


def g(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True,
                          env=ENV, check=True).stdout


def main():
    rows = []
    for line in open(os.path.join(SEAT, "fixtures.txt")):
        name, d = line.split()
        head = g(d, "rev-parse", "HEAD").strip()
        entry = g(d, "show", "HEAD:" + ENTRY)
        lesson = g(d, "show", "HEAD:" + LESSON)
        reg = g(d, "show", "HEAD:" + REG).split("\n")
        newrows = [l for l in reg if l.startswith("| S164 ") or l.startswith("| S298 ")
                   or l.startswith("| S299 ") or l.startswith("| S300 ")
                   or l.startswith("| S301 ")]
        with open(os.path.join(OUT, name + "-entry.md"), "w") as fh:
            fh.write(entry)
        with open(os.path.join(OUT, name + "-gates.md"), "w") as fh:
            fh.write(lesson)
        with open(os.path.join(OUT, name + "-rows.md"), "w") as fh:
            fh.write("\n".join(newrows) + "\n")
        rows.append((name, head, len(entry.splitlines())))
    with open(os.path.join(SEAT, "fixtures-manifest.md"), "w") as fh:
        fh.write("# fixture commits (throwaway clones of the lane at e2289516)\n\n")
        fh.write("| variant | commit | entry lines |\n|---|---|---|\n")
        for name, head, n in rows:
            fh.write("| %s | %s | %d |\n" % (name, head, n))


if __name__ == "__main__":
    main()
