#!/usr/bin/env python3
"""Build the C1 shape-keeping tool variants from the landed tool.

Landed tool: e4678921:tools/mado-geometry.py. Each variant keeps the state
logic byte for byte and adds only *shape*: comparison sites that decide
nothing (they are inside `report`, a function naming `fullscreen`, so clause b4
counts them, and flipping each one leaves the tool's behaviour and selftest
unchanged, so the mutant survives).
"""
import os
import subprocess
import sys

REV = "e46789213830597348fe96a351ae004d10587385"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
TOOL = "tools/mado-geometry.py"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "variants")
os.makedirs(OUT, exist_ok=True)

src = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (REV, TOOL)],
                     capture_output=True, check=True).stdout.decode("utf-8")
open(os.path.join(OUT, "c1-landed.py"), "w").write(src)

# the round-43 tool, for the "docstring untouched" variant
base = subprocess.run(["git", "-C", LANE, "show",
                       "6a1a90528fe533cadee506a9fa3e9d13d15cc41f:" + TOOL],
                      capture_output=True, check=True).stdout.decode("utf-8")
open(os.path.join(OUT, "c1-base-tool.py"), "w").write(base)

PAD = ('    _shape = (%s)\n')
ITEMS = ('1 == 2', '3 != 3', '4 < 3', '5 > 6', '1 <= 0', '2 >= 3',
         '"fullscreen" in ("maximized",)', '"maximized" not in ("fullscreen",)')
ANCHOR = "    return lines, rc\n"
assert src.count(ANCHOR) == 1


def padded(n, name):
    body = src.replace(ANCHOR, PAD % ", ".join(ITEMS[:n]) + ANCHOR)
    path = os.path.join(OUT, name)
    open(path, "w").write(body)
    print("%s: %d pad sites" % (name, n))
    return path


padded(5, "c1-b4pad5.py")
padded(6, "c1-b4pad6.py")

# "docstring untouched": landed code with the round-43 docstring (the tool's
# own contract text dropped; behaviour identical)
def swap_docstring(new_src, old_src):
    a = new_src.index('"""', new_src.index('"""') + 3) + 3
    tail = new_src[a:]
    b0 = old_src.index('"""')
    b1 = old_src.index('"""', b0 + 3) + 3
    return old_src[:b1] + tail


open(os.path.join(OUT, "c1-olddoc.py"), "w").write(swap_docstring(src, base))
print("c1-olddoc.py: round-43 docstring over the round-44 code")

# report the site counts the counter itself computes
spec = os.path.join(LANE, "quality/counters/c1-r44-geometry-states-v2.py")
sys.path.insert(0, os.path.dirname(spec))
import importlib.util
sp = importlib.util.spec_from_file_location("c1v2", spec)
m = importlib.util.module_from_spec(sp)
sp.loader.exec_module(m)
import math
for name in ("c1-landed.py", "c1-b4pad5.py", "c1-b4pad6.py", "c1-olddoc.py"):
    text = open(os.path.join(OUT, name)).read()
    sites = m.state_sites(text)
    print("%-16s sites=%d need=%d" % (name, len(sites), math.ceil(m.KILL_FRACTION * len(sites))))
