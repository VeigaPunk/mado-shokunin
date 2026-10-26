#!/usr/bin/env python3
"""ReDoS probe: feed a supported rule whose REGEX is ambiguous, and an
attacker-chosen class string, to the reference tool; time it."""
import json
import os
import subprocess
import sys
import time

TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin", "mado-geometry.py")
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "redos")
os.makedirs(WORK, exist_ok=True)


def run(rx, cls, timeout=20.0, label=""):
    rules = os.path.join(WORK, "r.conf")
    clients = os.path.join(WORK, "c.json")
    with open(rules, "w") as f:
        f.write("windowrule = size 420 500, match:class %s\n" % rx)
    with open(clients, "w") as f:
        f.write(json.dumps([{"class": cls, "size": [420, 500], "floating": True,
                             "mapped": True, "address": "0x1"}]))
    t0 = time.monotonic()
    try:
        p = subprocess.run([sys.executable, "-I", TOOL, "--clients", clients, "--rules", rules],
                           capture_output=True, timeout=timeout)
        dt = time.monotonic() - t0
        return dt, p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace"), False
    except subprocess.TimeoutExpired:
        return time.monotonic() - t0, None, "", "", True


def head(out):
    for line in out.splitlines():
        if line.startswith("MADO_GEOMETRY:"):
            return line
    return out.splitlines()[-1] if out.splitlines() else ""


def sg(label, rx, cls, timeout=20.0):
    dt, rc, out, err, to = run(rx, cls, timeout, label)
    print("%-28s len=%6d rx=%-10s %s time=%8.3fs rc=%s %s" % (
        label, len(cls), rx, "TIMEOUT" if to else "     ", dt, rc,
        (head(out)[:70] if not to else "")))
    return dt, rc, to, out, err


if __name__ == "__main__":
    print("python", sys.version.split()[0])
    # 1. the rule IS accepted (contract admits it): short class, immediate
    for rx in ("(a+)+$", "(a|aa)+$", "(a*)*b", "(a|b)+$"):
        sg("accepted?", rx, "zzz", 20.0)
    print()
    # 2. growth series on a failing class ("a"*N + "!" -> no match, must backtrack)
    for rx in ("(a+)+$", "(a|aa)+$"):
        for n in (14, 16, 18, 20, 22, 24, 26):
            sg("growth %s" % rx, rx, "a" * n + "!", 20.0)
        print()
    for n in (1000, 4000, 8000, 16000, 32000, 40000):
        sg("attack %s" % "(a+)+$", "(a+)+$", "a" * n + "!", 10.0)
        sg("attack %s" % "(a|aa)+$", "(a|aa)+$", "a" * n + "!", 10.0)
        sg("attack %s" % "(a*)*b", "(a*)*b", "a" * n, 10.0)
    print()
    # 3. linear control at the same sizes (no ambiguity)
    for n in (40000, 100000):
        sg("linear (a|b)+$", "(a|b)+$", "a" * n, 20.0)
    # 4. polynomial wildcards (no group needed)
    for rx in (".*.*.*b", ".*.*.*.*b"):
        for n in (200, 400, 800, 1600, 40000):
            sg("wild %s" % rx, rx, "a" * n, 10.0)
    # 5. a rule set: 1 ambiguous rule is enough among many safe ones
    print()
    rules = os.path.join(WORK, "mixed.conf")
    with open(rules, "w") as f:
        for i in range(299):
            f.write("windowrule = float on, match:class gkeep%d\n" % i)
        f.write("windowrule = size 420 500, match:class (a|aa)+$\n")
    clients = os.path.join(WORK, "c2.json")
    with open(clients, "w") as f:
        f.write(json.dumps([{"class": "a" * 34 + "!", "size": [420, 500], "floating": True,
                             "mapped": True, "address": "0x1"}]))
    t0 = time.monotonic()
    try:
        p = subprocess.run([sys.executable, "-I", TOOL, "--clients", clients, "--rules", rules],
                           capture_output=True, timeout=10)
        print("mixed 300 rules: time=%.3fs rc=%s" % (time.monotonic() - t0, p.returncode))
    except subprocess.TimeoutExpired:
        print("mixed 300 rules: TIMEOUT after 10s")
