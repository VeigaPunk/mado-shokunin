#!/usr/bin/env python3
"""SentC1Host part 3: wall + peak RSS for tool vs the pinned real script; same fixtures, same env."""
import os, resource, shutil, subprocess, sys, time

S = "/fast/scratch/hyaku/mado-r47/SentC1Host"
TOOL = S + "/tool.py"
REAL = S + "/real"
OUT = S + "/results3.txt"
lines = []

def note(s):
    lines.append(s); print(s, flush=True)

def env_for(c, path=None):
    return {
        "HOME": c + "/home", "PATH": (path or (c + "/bin:/usr/bin:/bin")),
        "TMPDIR": S + "/tmp",
        "XDG_CONFIG_HOME": c + "/home/.config", "XDG_CONFIG_DIRS": c + "/etcxdg",
        "XDG_DATA_HOME": c + "/home/.local/share", "XDG_DATA_DIRS": c + "/share",
        "XDG_CACHE_HOME": c + "/cache", "XDG_CURRENT_DESKTOP": "Hyprland",
    }

def run(argv, env, cwd, limit_as=None, timeout=180):
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    t0 = time.time()
    def pre():
        if limit_as:
            resource.setrlimit(resource.RLIMIT_AS, (limit_as, limit_as))
    try:
        p = subprocess.run(argv, env=env, cwd=cwd, capture_output=True, timeout=timeout,
                           preexec_fn=pre)
        rc, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as ex:
        rc, out, err = 124, ex.stdout or b"", ex.stderr or b""
    wall = time.time() - t0
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    # ru_maxrss of children is the high-water mark across all children so far; report the delta of the max
    rss = after.ru_maxrss
    return rc, out, err, wall, rss, before.ru_maxrss

def mkcase(c):
    for d in ("/home/.config", "/home/.local/share/applications", "/cache", "/bin", "/share", "/etcxdg"):
        os.makedirs(c + d, exist_ok=True)
    with open(c + "/home/.local/share/applications/good.desktop", "w") as f:
        f.write("[Desktop Entry]\nType=Application\nName=Foot\nExec=foot\nCategories=System;TerminalEmulator;\n")
    with open(c + "/bin/foot", "w") as f:
        f.write("#!/bin/sh\n")
    os.chmod(c + "/bin/foot", 0o755)

def both(label, c, tool_args, real_args, limit_as=None, timeout=180):
    rc, out, err, wall, rss, _ = run(["/usr/bin/python3", "-I", TOOL] + tool_args, env_for(c), c,
                                     limit_as=limit_as, timeout=timeout)
    note("%-22s tool rc=%-4d wall=%6.2fs maxrss_kb=%7d out=%r err=%r" % (
        label, rc, wall, rss, out[-160:].decode("latin-1", "replace"), err[-200:].decode("latin-1", "replace")))
    rc2, out2, err2, wall2, rss2, _ = run([REAL] + real_args, env_for(c), c, limit_as=limit_as, timeout=timeout)
    note("%-22s real rc=%-4d wall=%6.2fs maxrss_kb=%7d out=%r err=%r" % (
        "", rc2, wall2, rss2, out2[-160:].decode("latin-1", "replace"), err2[-200:].decode("latin-1", "replace")))

P = ["--print-id", "--print-path"]

# 1 clean
c = S + "/c/P1"; mkcase(c)
both("P1-clean", c, ["explain"], P)

# 2 42 MiB list file, 2M entry lines
c = S + "/c/P2"; mkcase(c)
with open(c + "/home/.config/xdg-terminals.list", "w") as f:
    for i in range(2000000):
        f.write("entry%07d.desktop\n" % i)
note("P2 list bytes=%d" % os.path.getsize(c + "/home/.config/xdg-terminals.list"))
both("P2-biglist", c, ["explain"], P)

# 3 177 MiB entry, 1.8M short lines
c = S + "/c/P3"; mkcase(c)
with open(c + "/home/.local/share/applications/big.desktop", "w") as f:
    for i in range(1800000):
        f.write("X-Comment-%06d=%s\n" % (i, "the quick brown fox jumps over the lazy dog " * 3))
note("P3 entry bytes=%d" % os.path.getsize(c + "/home/.local/share/applications/big.desktop"))
both("P3-bigentry", c, ["explain"], P)

# 4 1400-deep tree
c = S + "/c/P4"; mkcase(c)
p = c + "/home/.local/share/applications"
for _ in range(1400):
    p += "/d"
os.makedirs(p)
with open(p + "/deep.desktop", "w") as f:
    f.write("[Desktop Entry]\nType=Application\nName=Deep\nExec=foot\nCategories=System;TerminalEmulator;\n")
both("P4-deep1400", c, ["explain"], P)

# 5 symlink out of the applications dir
c = S + "/c/P5"; mkcase(c)
os.symlink("/usr/share/doc", c + "/home/.local/share/applications/out")
both("P5-symlink-out", c, ["explain"], P)

# 6 4 GiB sparse entry (no newline), memory capped at 1.5 GiB
c = S + "/c/P6"; mkcase(c)
with open(c + "/home/.local/share/applications/huge.desktop", "wb") as f:
    f.truncate(4 * 1024**3)
both("P6-sparse-4G", c, ["explain"], P, limit_as=1500 * 1024 * 1024)

# 7 900 MiB of lines (streams in bash, buffered by the tool), memory capped at 1.5 GiB
c = S + "/c/P7"; mkcase(c)
with open(c + "/home/.local/share/applications/lines.desktop", "w") as f:
    row = "X-Comment=%s\n" % ("abcdefghij" * 20)
    for _ in range(900 * 1024**2 // len(row)):
        f.write(row)
note("P7 entry bytes=%d" % os.path.getsize(c + "/home/.local/share/applications/lines.desktop"))
both("P7-900M-lines", c, ["explain"], P, limit_as=1500 * 1024 * 1024)

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
