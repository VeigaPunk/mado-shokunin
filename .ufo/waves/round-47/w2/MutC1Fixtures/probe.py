#!/usr/bin/env python3
"""Seat MutC1Fixtures: env-level probes for rules the fixture schema cannot express
(case_env force-sets PATH/HOME; the files schema has no mode field).

Probe 1 PATH-EMPTY: command -v must consult cwd for an empty PATH element.
Probe 2 LIST-UNREADABLE: an unreadable list file must end the resolver with exit 1 (errexit).
"""
import importlib.util
import os
import random
import shutil
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SCRATCH = "/fast/scratch/hyaku/mado-r47/MutC1Fixtures"
REFPATH = os.path.join(LANE, ".ufo", "waves", "round-47", "l1-draft", "mado-terminal.py")
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r47-terminal.py")
HERE = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, HERE)
from mutants import MUTANTS

spec = importlib.util.spec_from_file_location("c1r47", COUNTER)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

REF = open(REFPATH).read()
TERM = "[Desktop Entry]\nType=Application\nName=%s\nExec=%s\nCategories=System;TerminalEmulator;\n"


def mutated(mid):
    for name, old, new in MUTANTS:
        if name == mid:
            assert REF.count(old) == 1
            return REF.replace(old, new, 1)
    raise SystemExit("unknown mutant " + mid)


def tree(root):
    os.makedirs(os.path.join(root, "home"))
    os.makedirs(os.path.join(root, ".rw", "cache"))
    os.makedirs(os.path.join(root, "usr", "share", "applications"))
    os.makedirs(os.path.join(root, "home", ".config"))
    os.makedirs(os.path.join(root, "etc", "xdg"))
    os.makedirs(os.path.join(root, "home", ".local", "share"))
    with open(os.path.join(root, "usr", "share", "applications", "foot.desktop"), "w") as fh:
        fh.write(TERM % ("foot", "foot"))


def env(root, **kw):
    e = {"HOME": os.path.join(root, "home"),
         "PATH": os.path.join(root, "bin") + ":/oracle/bin",
         "XDG_CONFIG_HOME": os.path.join(root, "home", ".config"),
         "XDG_CONFIG_DIRS": os.path.join(root, "etc", "xdg"),
         "XDG_DATA_HOME": os.path.join(root, "home", ".local", "share"),
         "XDG_DATA_DIRS": os.path.join(root, "usr", "share"),
         "XDG_CACHE_HOME": os.path.join(root, ".rw", "cache"),
         "LANG": "C.UTF-8",
         "XDG_CURRENT_DESKTOP": "Hyprland"}
    e.update(kw)
    return e


def run_tool(box, root, tool, args):
    return box.run(root, env(root), tool, args)


def probe1():
    work = tempfile.mkdtemp(dir=SCRATCH, prefix="p1-")
    try:
        root = os.path.join(work, "r")
        tree(root)
        os.makedirs(os.path.join(root, "bin"))
        with open(os.path.join(root, "foot"), "w") as fh:
            fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(os.path.join(root, "foot"), 0o755)
        e = env(root)
        e["PATH"] = os.path.join(root, "bin") + "::" + "/oracle/bin"
        mp = os.path.join(work, "mut.py")
        open(mp, "w").write(mutated("I-PATH-EMPTY-SKIP"))
        rp = os.path.join(work, "ref.py")
        open(rp, "w").write(REF)
        box_o = C.Box(work)
        box_r = C.Box(work, tool_path=rp)
        box_m = C.Box(work, tool_path=mp)
        o = box_o.run(root, e, False, ["--print-id"])
        r = box_r.run(root, e, True, ["print", "--print-id"])
        m = box_m.run(root, e, True, ["print", "--print-id"])
        print("PROBE PATH-EMPTY:\n  oracle=(%d, %r)\n  ref=(%d, %r)\n  mutant=(%d, %r)"
              % (o[0], o[1][:60], r[0], r[1][:60], m[0], m[1][:60]))
    finally:
        shutil.rmtree(work, ignore_errors=True)


def probe2():
    work = tempfile.mkdtemp(dir=SCRATCH, prefix="p2-")
    try:
        root = os.path.join(work, "r")
        tree(root)
        lp = os.path.join(root, "home", ".config", "xdg-terminals.list")
        with open(lp, "w") as fh:
            fh.write("foot.desktop\n")
        os.chmod(lp, 0)
        mp = os.path.join(work, "mut.py")
        open(mp, "w").write(mutated("I-LIST-UNREADABLE-SKIP"))
        rp = os.path.join(work, "ref.py")
        open(rp, "w").write(REF)
        box_o = C.Box(work)
        box_r = C.Box(work, tool_path=rp)
        box_m = C.Box(work, tool_path=mp)
        o = box_o.run(root, env(root), False, ["--print-id"])
        r = box_r.run(root, env(root), True, ["print", "--print-id"])
        m = box_m.run(root, env(root), True, ["print", "--print-id"])
        print("PROBE LIST-UNREADABLE:\n  oracle=(%d, %r)\n  ref=(%d, %r)\n  mutant=(%d, %r)"
              % (o[0], o[1][:80], r[0], r[1][:80], m[0], m[1][:80]))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    probe1()
    probe2()
