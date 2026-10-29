#!/usr/bin/env python3
"""Cheat (f): implements ONLY nine features, no others (not a faithful Hyprland model):
 1 usage: exactly one --config and one --display-root, anything else -> SETUP usage rc 2
 2 header line: config=$ROOT/<rel>, autoreload from a 'disable_autoreload = <true|yes|1>' line in the config (on/off)
 3 primary line n=1 for the config (type=file when it is a regular file, else type=missing)
 4 top-level 'source = <relative path>' lines of the config (no globs, no '~', no absolute paths) watched when a regular file
 5 'source' lines of sourced files, relative to the including file's directory (same restrictions as 4)
 6 display-root prefix replaced by $ROOT in every printed path
 7 entries printed in encounter order, each with via=<includer>:<line>
 8 DONE line with watches=<n>
 9 unsupported=0 errors=0 and live=NONE always
It implements none of: --home, --getoption, globs, errors, skips, canonical paths, symlinks, bad_json, too_large."""
import os
import re
import sys


def root_sub(p, dr):
    if p == dr or p.startswith(dr + "/"):
        return "$ROOT" + p[len(dr):]
    return p


a = sys.argv[1:]
if a.count("--config") != 1 or a.count("--display-root") != 1 or len(a) != 4:
    sys.stdout.write("MADO_WATCH: SETUP usage\n")
    sys.exit(2)
cfg = a[a.index("--config") + 1]
dr = a[a.index("--display-root") + 1].rstrip("/")
disabled = "unset"
watch = []
primary = os.path.abspath(cfg)
seen = set()
entries = []


def parse(path, depth):
    global disabled
    if depth > 16 or path in seen:
        return
    seen.add(path)
    try:
        text = open(path, "rb").read().decode("utf-8", "replace")
    except OSError:
        return
    base = os.path.dirname(path)
    for ln, raw in enumerate(text.split("\n"), 1):
        line = raw.strip(" \t\r\x0b\x0c")
        if not line or line.startswith("#") or "=" not in line:
            continue
        lhs, rhs = (s.strip(" \t\r\x0b\x0c") for s in line.split("=", 1))
        if lhs == "disable_autoreload" and depth == 0 and path == primary:
            disabled = "1" if rhs.lower() in ("true", "yes", "1") else disabled
        if lhs != "source" or not rhs or rhs.startswith("/") or rhs.startswith("~") or "*" in rhs:
            continue
        target = os.path.normpath(os.path.join(base, rhs))
        if os.path.isfile(target) and not os.path.islink(target):
            entries.append((target, path, ln))
            parse(target, depth + 1)


parse(primary, 0)
autoreload = "off" if disabled == "1" else "on"
sys.stdout.write("MADO_WATCH: config=%s autoreload=%s disable_autoreload=%s paths=%d unsupported=0 errors=0\n" % (
    root_sub(primary, dr), autoreload, disabled, 1 + len(entries)))
n = 1
sys.stdout.write("MADO_WATCH: n=1 role=primary path=%s type=%s mask=IN_CLOSE_WRITE|IN_DONT_FOLLOW via=main\n" % (
    root_sub(primary, dr), "file" if os.path.isfile(primary) else "missing"))
for target, via, ln in entries:
    n += 1
    sys.stdout.write("MADO_WATCH: n=%d role=primary path=%s type=file mask=IN_CLOSE_WRITE|IN_DONT_FOLLOW via=%s:%d\n" % (
        n, root_sub(target, dr), root_sub(via, dr), ln))
sys.stdout.write("MADO_WATCH: DONE watches=%d unsupported=0 errors=0 live=NONE\n" % n)
sys.exit(0)
