#!/usr/bin/env python3
"""Build a diagnostic copy of the frozen C1 counter with 11 proposed fixtures, and score REF and each cheat."""
import json
import os
import subprocess
import sys
import tempfile

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FROZEN = os.path.join(LANE, "quality/counters/c1-r45-monitors.py")
BASE = "0c89478af821a6424c9ac922eafe02e39630cf4f"
PLUS = os.path.join(S, "c1-r45-monitors-plus.py")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}

sys.path.insert(0, S)
from probe import M, run  # noqa: E402

A, B, C, D = "DP-5", "eDP-7", "DVI-D-5", "Dell Inc. 6AHUHV"
TBL = {"A": A, "B": B, "C": C, "D": D}

CASES = [
    ("scale-1.4-corrected", "monitor = {A}, 2560x1440@60, 0x0, 1.4\n",
     '[M("{A}", w=2560, rr=59.951, scale=1.33333333)]'),
    ("scale-1.4-as-written", "monitor = {A}, 2560x1440@60, 0x0, 1.4\n",
     '[M("{A}", w=2560, rr=59.951, scale=1.4)]'),
    ("icc-key", "monitor = {A}, 3440x1440@100, 0x0, 1, icc, /usr/share/color/icc/x.icc\n",
     '[M("{A}")]'),
    ("sdrsaturation-key", "monitor = {A}, 3440x1440@100, 0x0, 1, sdrsaturation, 1.5\n",
     '[M("{A}")]'),
    ("sdrbrightness-key", "monitor = {A}, 3440x1440@100, 0x0, 1, sdrbrightness, 1.5\n",
     '[M("{A}")]'),
    ("v2-with-differ", "monitorv2 {\n  output = {A}\n}\nmonitor = {A}, 1920x1080@60, 0x0, 1\n",
     '[M("{A}")]'),
    ("mirror-other-output-id",
     "monitor = {A}, 3440x1440@100, 0x0, 1\nmonitor = {B}, 3440x1440@100, 0x0, 1, mirror, {A}\n",
     '[M("{A}", mid=4), M("{B}", mid=5, mirror="6"), M("{C}", w=1920, h=1080, rr=60.0, x=3440, mid=6)]'),
    ("addreserved-bad-fields", "monitor = {A}, addreserved, 10x, 0, 0, 0\n", '[M("{A}")]'),
    ("desc-text-space", "monitor = desc: {A}, 3440x1440@100, 0x0, 1\n", '[M("{A}", desc="{A} 0x0001")]'),
    ("desc-empty", "monitor = desc:, preferred, auto, auto\n",
     '[M("{A}", w=1920, h=1080, rr=60.0, scale=1.25)]'),
    ("rate-165-tolerance", "monitor = {A}, 2560x1440@165, 0x0, 1\n", '[M("{A}", w=2560, rr=164.5)]'),
    ("desc-long-not-in-dump", "monitor = desc:{D}, 3440x1440@100, 0x0, 1\n",
     '[dict(M("{A}", desc="X"), longDescription="{D} panel")]'),
]


def sub(s):
    for k, v in TBL.items():
        s = s.replace("{%s}" % k, v)
    return s


def back(line):
    for k in ("D", "A", "B", "C"):
        line = line.replace(TBL[k], "{%s}" % k)
    return line


def build_plus():
    entries = []
    for label, cfg, dump_src in CASES:
        dump = eval(sub(dump_src), {"M": M})
        rc, lines = run(os.path.join(S, "ref.py"), [sub(cfg)], dump)
        entries.append('    (%r, [%r], %s, False, [%s], %d),' % (
            label, cfg, dump_src, ", ".join(repr(back(l)) for l in lines), rc))
        print("fixture %-26s ref rc=%d lines=%d" % (label, rc, len(lines)))
    text = open(FROZEN).read()
    anchor = '    ("setup-usage", "usage", [M("{A}")], False, ["MADO_MONITORS: SETUP usage"], 2),\n]'
    if text.count(anchor) != 1:
        raise SystemExit("anchor count %d" % text.count(anchor))
    text = text.replace(
        anchor,
        '    ("setup-usage", "usage", [M("{A}")], False, ["MADO_MONITORS: SETUP usage"], 2),\n'
        + "\n".join(entries) + "\n]")
    text = ("# DIAGNOSTIC COPY (CritC1Cheat): the frozen counter plus 11 proposed fixtures. Not installed.\n"
            + text)
    open(PLUS, "w").write(text)
    return len(CASES)


def repo_for(text, name, work):
    d = tempfile.mkdtemp(dir=work, prefix=name + "-")
    subprocess.run(["git", "-C", work, "clone", "-q", "--shared", "--no-checkout", LANE, d],
                   check=True, capture_output=True, env=ENV)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"], capture_output=True,
                         env=ENV, check=True).stdout.decode().strip()
    if top != os.path.realpath(d):
        raise SystemExit("toplevel mismatch")
    subprocess.run(["git", "-C", d, "checkout", "-q", "--detach", BASE], check=True, capture_output=True, env=ENV)
    os.makedirs(os.path.join(d, "tools"), exist_ok=True)
    with open(os.path.join(d, "tools", "mado-monitors.py"), "w") as f:
        f.write(text)
    subprocess.run(["git", "-C", d, "add", "tools/mado-monitors.py"], check=True, capture_output=True, env=ENV)
    subprocess.run(["git", "-C", d, "-c", "user.name=seat", "-c", "user.email=seat@scratch.invalid",
                    "commit", "-q", "-m", name], check=True, capture_output=True, env=ENV)
    return d


def score(counter, repo, work, seed=None):
    w = tempfile.mkdtemp(dir=work, prefix="w-")
    cmd = [sys.executable, "-I", counter, "--repo", repo, "--rev", "HEAD", "--work", w]
    if seed is not None:
        cmd += ["--seed", str(seed)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    fails = [l.split("fixture=")[1].split()[0] for l in p.stdout.split("\n")
             if "clause=f fixture=" in l and " FAIL" in l]
    return p.returncode, p.stdout.strip().split("\n")[-1], fails


def main():
    n = build_plus()
    work = tempfile.mkdtemp(dir=S, prefix="plus-")
    tools = [("REF", "ref.py")] + [(c[:-3], c) for c in sorted(os.listdir(S))
                                   if c.startswith("cheat-") and c.endswith(".py")]
    print("\n# diagnostic counter = frozen + %d fixtures; frozen fixtures 49" % n)
    for name, path in tools:
        d = repo_for(open(os.path.join(S, path)).read(), name, work)
        rc, last, fails = score(PLUS, d, work)
        print("%-28s rc=%d %s" % (name, rc, last))
        if fails:
            print("%-28s FAILED: %s" % ("", ",".join(fails)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
