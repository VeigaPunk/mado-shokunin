#!/usr/bin/env python3
"""Fixtures for the guard-only survivors M15, M16, M63 (equivalent on the frozen tree, not in general).

var_srcline2 : the `source:` line is moved to line 2 (a blank first line), so the first-15-line window is needed
               to find it. Kills M63 (window reduced to line 1).
var_pinlink  : fetch/Hyprland-ConfigWatcher.cpp becomes a symlink to a regular copy in the same directory.
               The pristine harness refuses the mutation target (_reg); M16 (symlink refusal removed) writes through
               the link; M15 (symlinks=False) dereferences the link at export.
Each fixture is a separate scratch git repo (D=$(mktemp -d -p ...); git -C "$D" ... ; toplevel asserted).
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

SCR = Path("/fast/scratch/hyaku/mado-r56/R56W2MutC1Harness")
REPO = SCR / "repo"
ENV = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C.UTF-8"}
PIN = ".ufo/waves/round-56/fetch"


def git(d, *a):
    return subprocess.run(["git", "-C", str(d), *a], check=True, capture_output=True, text=True, env=ENV).stdout.strip()


def new_repo(name):
    base = SCR / "variants"
    base.mkdir(exist_ok=True)
    d = Path(subprocess.run(["mktemp", "-d", "-p", str(base), name + "-XXXX"], capture_output=True, text=True,
                            check=True).stdout.strip())
    shutil.copytree(REPO, d, symlinks=True, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git"))
    git(d, "init", "-q", "-b", "main")
    assert os.path.realpath(git(d, "rev-parse", "--show-toplevel")) == os.path.realpath(str(d))
    return d


def commit(d, name):
    git(d, "add", "-A")
    subprocess.run(["git", "-C", str(d), "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", name],
                   check=True, env=ENV)
    return git(d, "rev-parse", "HEAD")


def main():
    # var_srcline2
    d = new_repo("var_srcline2")
    p = d / "corpus/knowledge/hyprland-config-autoreload-r56.md"
    p.write_text("\n" + p.read_text())
    sha = commit(d, "var_srcline2")
    print("var_srcline2", sha, d)
    # var_pinlink
    d2 = new_repo("var_pinlink")
    pin = d2 / PIN / "Hyprland-ConfigWatcher.cpp"
    real = d2 / PIN / "Hyprland-ConfigWatcher.cpp.bak"
    shutil.copy(pin, real)
    pin.unlink()
    os.symlink("Hyprland-ConfigWatcher.cpp.bak", pin)
    sha2 = commit(d2, "var_pinlink")
    print("var_pinlink", sha2, d2, "link ->", os.readlink(pin))


if __name__ == "__main__":
    sys.exit(main())
