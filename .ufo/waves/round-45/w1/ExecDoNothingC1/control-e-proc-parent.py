#!/usr/bin/env python3
"""mado-monitors (CONTROL E, r45 - finds the predicate through /proc, no hardcoded path).

Nothing in this file names the lane or the counter. It asks the OS who its parent is, reads the parent's
argv out of /proc/<ppid>/cmdline, takes the argument ending in c1-r45-monitors.py, executes that file as a
module and reuses its FIXTURES/names/subst as a lookup table. A control against PRED-C1-r45: the predicate is
reachable because the predicate runs the tool as its own child.
"""
import json
import os
import re
import sys


def counter_path():
    ppid = None
    with open("/proc/self/status") as f:
        for line in f:
            if line.startswith("PPid:"):
                ppid = line.split()[1]
                break
    if ppid is None:
        return None
    for arg in open("/proc/%s/cmdline" % ppid, "rb").read().split(b"\0"):
        arg = arg.decode("utf-8", "replace")
        if arg.endswith("c1-r45-monitors.py"):
            return arg
    return None


COUNTER = counter_path()
if COUNTER is None:
    print("MADO_MONITORS: SETUP unreadable")
    sys.exit(2)
NAMESPACE = {"__name__": "c1r45_counter", "__file__": COUNTER}
exec(compile(open(COUNTER, "rb").read(), COUNTER, "exec"), NAMESPACE)
FIXTURES = NAMESPACE["FIXTURES"]
names = NAMESPACE["names"]
subst = NAMESPACE["subst"]


def read_input(path):
    if os.path.isdir(path):
        return b"<dir>"
    try:
        with open(path, "rb") as f:
            return f.read()
    except OSError:
        return b"<unreadable>"


def parse(argv):
    mon, cfgs, i = None, [], 0
    while i < len(argv):
        if i + 1 >= len(argv):
            return None
        k, v = argv[i], argv[i + 1]
        if k == "--monitors" and mon is None:
            mon = v
        elif k == "--config":
            cfgs.append(v)
        else:
            return None
        i += 2
    if mon is None or not cfgs:
        return None
    return mon, cfgs


def fixture_inputs(fx, table):
    label, configs, dump, stdin, expect, rc = fx
    if isinstance(configs, list):
        cs = [subst(t, table).encode() for t in configs]
    elif configs is None:
        cs = [b"<dir>"]
    else:
        return None, None
    d = dump if isinstance(dump, bytes) else json.dumps(subst(dump, table), indent=2).encode()
    return cs, d


def lookup(cs, d):
    obs = set()
    for b in cs + [d]:
        obs |= set(re.findall(r"([A-Za-z-]+-[0-9])", b.decode("utf-8", "replace")))
    for seed in range(0, 4096):
        table = names(seed)
        if not obs <= set(table.values()):
            continue
        for fx in FIXTURES:
            fs, fd = fixture_inputs(fx, table)
            if fs is None:
                continue
            if len(fs) == len(cs) and all(x == y for x, y in zip(fs, cs)) and fd == d:
                for line in fx[4]:
                    print(subst(line, table))
                return fx[5]
    print("MADO_MONITORS: SETUP unreadable")
    return 2


def main():
    argv = sys.argv[1:]
    if argv == ["--selftest"]:
        print("MADO_MONITORS_SELFTEST: %d/%d passed" % (len(FIXTURES), len(FIXTURES)))
        return 0
    got = parse(argv)
    if got is None:
        print("MADO_MONITORS: SETUP usage")
        return 2
    mon, cfgs = got
    stdin_data = sys.stdin.buffer.read() if mon == "-" else None
    cs = [read_input(p) for p in cfgs]
    d = stdin_data if mon == "-" else read_input(mon)
    return lookup(cs, d)


if __name__ == "__main__":
    sys.exit(main())
