#!/usr/bin/env python3
"""probe_fallback.py - the one branch where the two sides stop being the same function:
Hyprland's "failed to find a clean divisor" arm (Monitor.cpp:1031-1036) sets
m_scale = getDefaultScale() (Monitor.cpp:1402-1420: 1 | 1.5 | 2), while the tool
returns None and the contract says "the scale is not compared".

Counts how often a rule scale on the 1/120 grid lands in that arm, and shows that
getDefaultScale() cannot coincide with the requested scale.
"""
import struct
import subprocess
import sys

BIN = sys.argv[1]
SIZES = [(640, 480), (800, 600), (1024, 768), (1366, 768), (1920, 1080), (2560, 1440), (3440, 1440),
         (3840, 2160), (5120, 1440), (7680, 4320), (1000, 1000), (1234, 567), (999, 777), (6016, 3384),
         (1600, 1200), (1280, 720), (2560, 1600), (4096, 2304), (3200, 1800), (2880, 1800)]
ks = list(range(30, 361))
cases = [(k, w, h) for k in ks for w, h in SIZES]
inp = "".join("%.9f %d %d\n" % (k / 120.0, w, h) for k, w, h in cases)
out = subprocess.run([BIN], input=inp, capture_output=True, text=True, check=True).stdout.split("\n")
fb = []
for (k, w, h), ln in zip(cases, out):
    sb, rb, st = ln.split()
    if st == "0":
        fb.append((k, w, h))
print("cases:", len(cases))
print("Hyprland 'no clean divisor' arm:", len(fb), "= %.1f%%" % (100.0 * len(fb) / len(cases)))
print("k range in that arm:", (min(f[0] for f in fb), max(f[0] for f in fb)) if fb else None)
print("requested scale range:", ("%.4f" % (min(f[0] for f in fb) / 120.0),
                                 "%.4f" % (max(f[0] for f in fb) / 120.0)) if fb else None)
print("first 8:", fb[:8])
vals = {1.0, 1.5, 2.0}
print("getDefaultScale() can return:", sorted(vals),
      "-> coincides with a requested scale in the arm:",
      sorted({round(f[0] / 120.0, 6) for f in fb} & vals))
