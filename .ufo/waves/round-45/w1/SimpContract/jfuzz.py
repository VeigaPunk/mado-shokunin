#!/usr/bin/env python3
"""Clause-j locator regex: the (?!d) tail, fuzzed for identical findall."""
import re
import random

NAME = "Hyprland-Monitor.cpp"
A = re.compile(r"(?<![\w.-])%s:(\d+)(?:-(\d+))?(?!\d)" % re.escape(NAME))
B = re.compile(r"(?<![\w.-])%s:(\d+)(?:-(\d+))?" % re.escape(NAME))
ALPHA = "0123456789-HyprlandMonitor.cpx :,()[]/|"
rng = random.Random(7)
bad = 0
for _ in range(200000):
    s = "".join(rng.choice(ALPHA) for _ in range(rng.randint(0, 40)))
    if rng.random() < 0.6:
        k = len(s) // 2
        s = s[:k] + NAME + ":" + s[k:]
    if A.findall(s) != B.findall(s):
        bad += 1
        if bad < 5:
            print("DIFF", repr(s), A.findall(s), B.findall(s))
print("fuzz strings=200000 diffs=%d" % bad)
for s in ["x" + NAME + ":12", NAME + ":12-34", NAME + ":1-2-3", NAME + ":123x",
          NAME + ":0", "-" + NAME + ":9", NAME + ":12 34"]:
    print("%-40r A=%r B=%r same=%s" % (s, A.findall(s), B.findall(s), A.findall(s) == B.findall(s)))
