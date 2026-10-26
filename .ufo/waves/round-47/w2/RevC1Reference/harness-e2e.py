#!/usr/bin/env python3
"""RevC1Reference e2e: real xdg-terminal-exec vs L1 draft mado-terminal.py on divergence candidates.
Real runs NEVER without a --print-* option; XDG_CACHE_HOME is per-tree; timeout 15 s; no empty argv."""
import os
import shutil
import subprocess

S = "/fast/scratch/hyaku/mado-r47/RevC1Reference/e2e"
REAL = "/usr/bin/xdg-terminal-exec"
DRAFT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/l1-draft/mado-terminal.py"

TERM = "[Desktop Entry]\nType=Application\nName=%s\nExec=%s\nCategories=System;TerminalEmulator;\n"


def build(root, files, execs):
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root + "/cache")
    os.makedirs(root + "/home")
    os.makedirs(root + "/ext")
    for tool in ("tr", "find", "awk", "ls", "md5sum", "mkdir", "rm"):
        shutil.copy2("/usr/bin/" + tool, root + "/ext/" + tool)
    for rel, txt in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(txt.encode())
    for rel in execs:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write("#!/bin/sh\nexit 1\n")
        os.chmod(p, 0o755)


def env_for(root, drop=()):
    e = {"HOME": root + "/home", "PATH": root + "/bin:" + root + "/ext", "XDG_CURRENT_DESKTOP": "Hyprland",
         "XDG_CONFIG_HOME": root + "/home/.config", "XDG_CONFIG_DIRS": root + "/etc/xdg",
         "XDG_DATA_HOME": root + "/home/.local/share", "XDG_DATA_DIRS": root + "/usr/share",
         "XDG_CACHE_HOME": root + "/cache", "LANG": "C.UTF-8"}
    for k in drop:
        e.pop(k, None)
    return e


def run_case(name, files, execs, args, drop=(), post=None):
    r1, r2 = S + "/" + name + "-r1", S + "/" + name + "-r2"
    for root in (r1, r2):
        build(root, files, execs)
    if post:
        for root in (r1, r2):
            post(root)
    outs = []
    for who, cmd, root in (("REAL", [REAL], r1), ("DRAFT", ["/usr/bin/python3", "-I", DRAFT, "print"], r2)):
        try:
            p = subprocess.run(cmd + args, env=env_for(root, drop), cwd=S, capture_output=True, timeout=15)
            outs.append((who, p.returncode, p.stdout, p.stderr))
        except subprocess.TimeoutExpired:
            outs.append((who, "TIMEOUT", b"", b""))
    same = outs[0][1:3] == outs[1][1:3]
    n0 = outs[0][2].replace(r1.encode(), b"$ROOT")
    n1 = outs[1][2].replace(r2.encode(), b"$ROOT")
    same = (outs[0][1], n0) == (outs[1][1], n1)
    print("== %s ==  %s" % (name, "AGREE" if same else "*** DIVERGE ***"))
    for who, rc, out, err in outs:
        root = r1 if who == "REAL" else r2
        out = out.replace(root.encode(), b"$ROOT")
        print("  %s rc=%s out=%r err=%r" % (who, rc, out[:200], err[:200]))


F_FOOT = {"usr/share/applications/foot.desktop": TERM % ("foot", "foot")}
L_FOOT = {"home/.config/xdg-terminals.list": "foot.desktop\n"}
E_DIGIT = {"usr/share/applications/2048qt.desktop": TERM % ("2048qt", "2048qt")}

run_case("e1a-digit-listed", {**E_DIGIT, "home/.config/xdg-terminals.list": "2048qt.desktop\n"},
         ["bin/2048qt"], ["--print-id"])
run_case("e1b-digit-fallback", E_DIGIT, ["bin/2048qt"], ["--print-id"])
run_case("e1c-letter-control", F_FOOT, ["bin/foot"], ["--print-id"])
run_case("e2-home-unset", {**F_FOOT, **L_FOOT}, ["bin/foot"], ["--print-id"], drop=("HOME",))
run_case("e3-path-unset", {**F_FOOT, **L_FOOT}, ["bin/foot"], ["--print-id"], drop=("PATH",))
run_case("e8-content-plus-cmd", F_FOOT, ["bin/foot"], ["--print-content", "--print-cmd"])
run_case("e9-actions-empty",
         {"usr/share/applications/foot.desktop":
          TERM % ("foot", "foot") + "Actions=\n[Desktop Action act]\nExec=footclient\n",
          "home/.config/xdg-terminals.list": "foot.desktop:act\n"},
         ["bin/foot", "bin/footclient"], ["--print-id"])
run_case("e12-content-no-final-nl",
         {"usr/share/applications/foot.desktop": "[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;"},
         ["bin/foot"], ["--print-content"])
run_case("e14-action-id-path",
         {"usr/share/applications/foot.desktop":
          TERM % ("foot", "foot") + "Actions=srv;\n[Desktop Action srv]\nExec=footclient\n",
          "home/.config/xdg-terminals.list": "foot.desktop:srv\n"},
         ["bin/foot", "bin/footclient"], ["--print-id", "--print-path"])
run_case("e15-execarg-consumes",
         {"usr/share/applications/foot.desktop": TERM % ("foot", "foot") + "X-TerminalArgExec=-x\n"},
         ["bin/foot"], ["--print-cmd", "-x"])
run_case("s1-test-beats-cmd", F_FOOT, ["bin/foot"], ["--test", "--print-cmd"])
run_case("s2-unknown-option-discard", F_FOOT, ["bin/foot"], ["--print-cmd", "-q", "--", "a"])
run_case("s3-last-cmd-delim-wins", F_FOOT, ["bin/foot"], ["--print-cmd", "--print-cmd=\\t", "--", "a"])
run_case("s6-upper-desktop", {**F_FOOT, **L_FOOT,
                              "home/.config/hyprland-xdg-terminals.list": "foot.desktop\n"},
         ["bin/foot"], ["--print-id"])
run_case("e17-empty-delimiter", F_FOOT, ["bin/foot"], ["--print-id", "--print-path", "--print-delimiter="])
run_case("e3b-path-unset-exec-sh", {**{"usr/share/applications/foot.desktop": TERM % ("foot", "sh")},
                                     **L_FOOT}, ["bin/foot"], ["--print-id"], drop=("PATH",))
run_case("e2b-home-unset-default-paths", F_FOOT, ["bin/foot"], ["--print-id"],
         drop=("HOME", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME"))
run_case("e18-unreadable-list", {**F_FOOT, **L_FOOT}, ["bin/foot"], ["--print-id"],
         post=lambda root: os.chmod(root + "/home/.config/xdg-terminals.list", 0))
