#!/usr/bin/env python3
"""live-ident.py — exact-equality scan for live host identity values.

Reads the live values from the process environment (HYPRLAND_INSTANCE_SIGNATURE,
WAYLAND_DISPLAY, hostname) and, optionally, a `hyprctl -j monitors` JSON file,
then reports every committed blob at --rev that contains one of them. Only the
class name, counts and file:line locators are printed; a value is never echoed,
so the receipt is safe to commit.

Usage: live-ident.py --repo DIR --rev REV --path PATH [--monitors F]
Exit status 0 always (a count of zero is the passing result).
"""
import argparse
import collections
import json
import os
import subprocess
import sys


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo, *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    if proc.returncode != 0:
        sys.exit("git %s failed" % " ".join(args))
    return proc.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--path", required=True)
    ap.add_argument("--monitors")
    args = ap.parse_args()

    values = {}
    for key, name in (("HYPRLAND_INSTANCE_SIGNATURE", "instance_sig"),
                      ("WAYLAND_DISPLAY", "wayland_display")):
        val = os.environ.get(key, "")
        if len(val) >= 3:
            values[name] = val
    host = os.uname().nodename
    if len(host) >= 3:
        values["hostname"] = host
    if args.monitors:
        with open(args.monitors, "r", encoding="utf-8") as fh:
            for mon in json.load(fh):
                for key in ("serial", "description", "make", "model"):
                    val = mon.get(key)
                    if isinstance(val, str) and len(val.strip()) >= 4:
                        values["monitor_" + key] = val.strip()

    names = git(args.repo, "ls-tree", "-r", "--name-only", args.rev, "--",
                args.path).decode("utf-8", "surrogateescape").split()
    hits = collections.Counter()
    locs = collections.defaultdict(list)
    for name in names:
        body = git(args.repo, "show", "%s:%s" % (args.rev, name))
        if b"\x00" in body[:8192]:
            continue
        text = body.decode("utf-8", "replace")
        for key, val in values.items():
            pos = text.find(val)
            if pos >= 0:
                hits[key] += 1
                if len(locs[key]) < 6:
                    locs[key].append("%s:%d" % (name, text[:pos].count("\n") + 1))

    for key in sorted(values):
        print("LIVEVALUE key=%s files=%d %s" % (key, hits[key], " ".join(locs[key])))
    total = sum(hits.values())
    print("LIVE_IDENT: values=%d files=%d matches=%d" % (len(values), len(names), total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
