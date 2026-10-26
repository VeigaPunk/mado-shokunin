#!/usr/bin/env python3
"""Seat MutC1Fixtures: explain-clause probe for I-EXPLAIN-CACHE-SWAP.

Runs the reference and the mutant `explain` in the sandbox with a cache file present
and absent, and shows the MADO_TERM cache= field flips while everything else stays.
The frozen counter's clause x never reads cache= (nor cmd=), so a wrong cache field
cannot trip it.
"""
import importlib.util
import os
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


def main():
    work = tempfile.mkdtemp(dir=SCRATCH, prefix="ep-")
    try:
        root = os.path.join(work, "r")
        for sub in ("home", ".rw/cache", "usr/share/applications", "home/.config", "etc/xdg", "home/.local/share", "bin"):
            os.makedirs(os.path.join(root, sub), exist_ok=True)
        open(os.path.join(root, "usr/share/applications/foot.desktop"), "w").write(TERM % ("foot", "foot"))
        with open(os.path.join(root, "bin/foot"), "w") as fh:
            fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(os.path.join(root, "bin/foot"), 0o755)
        env = {"HOME": root + "/home", "PATH": root + "/bin:/oracle/bin",
               "XDG_CONFIG_HOME": root + "/home/.config", "XDG_CONFIG_DIRS": root + "/etc/xdg",
               "XDG_DATA_HOME": root + "/home/.local/share", "XDG_DATA_DIRS": root + "/usr/share",
               "XDG_CACHE_HOME": root + "/.rw/cache", "LANG": "C.UTF-8",
               "XDG_CURRENT_DESKTOP": "Hyprland"}
        mp = os.path.join(work, "mut.py")
        open(mp, "w").write(mutated("I-EXPLAIN-CACHE-SWAP"))
        rp = os.path.join(work, "ref.py")
        open(rp, "w").write(REF)
        for cache_file in (False, True):
            if cache_file:
                open(os.path.join(root, ".rw", "cache", "xdg-terminal-exec"), "w").write("x\n")
            else:
                p = os.path.join(root, ".rw", "cache", "xdg-terminal-exec")
                if os.path.exists(p):
                    os.unlink(p)
            r = C.Box(work, tool_path=rp).run(root, env, True, ["explain"])
            m = C.Box(work, tool_path=mp).run(root, env, True, ["explain"])
            rl = [l for l in r[1].split("\n") if l.startswith("MADO_TERM: ")]
            ml = [l for l in m[1].split("\n") if l.startswith("MADO_TERM: ")]
            print("CACHE_FILE=%s ref=(%d, %s) mut=(%d, %s)"
                  % (cache_file, r[0], rl[-1] if rl else "?", m[0], ml[-1] if ml else "?"))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
