#!/usr/bin/env python3
"""Probes: b2 site statistics + determinism table, clause-g AST probes, dead-guard check."""
import ast, importlib.util, math
from math import comb

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
spec = importlib.util.spec_from_file_location("ctr", LANE + "/quality/counters/c1-r42-geometry.py")
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)

ref = open(LANE + "/.ufo/waves/round-42/c1/ctl-ref-tool.py.txt", "rb").read().decode("utf-8", "replace")

# 1. function_sites on the reference
sites = ctr.function_sites(ref)
summ = [s for s, f in sites if f]
rest = [s for s, f in sites if not f]
print("SITES total=%d summary_sites=%d rest=%d" % (len(sites), len(summ), len(rest)))
byfn = {}
for (fn, ln, col), f in sites:
    byfn.setdefault(fn, [0, 0])
    byfn[fn][0] += 1
    byfn[fn][1] += 1 if f else 0
for fn, (a, b) in sorted(byfn.items()):
    print("  fn=%s sites=%d summary=%d" % (fn, a, b))

# 2. teeth determinism: tool kills exactly K of N sites (forced must be a killed summary site).
# P(pass) = P(forced killed) * P(>=3 of 5 sampled others killed)
def pass_prob(K, N, S_s):
    # assume all summary sites killed (selftest checks the summary), rest killed with prob K/N
    p_rest = min(1.0, K / max(1, N - S_s))
    p_forced = 1.0  # summary sites assumed killed
    # others sampled from N-1 sites: S_s-1 summary (killed) + N-S_s rest (killed w.p. p_rest)
    tot = 0.0
    for k in range(3, 6):
        w = 0.0
        for j in range(0, min(5, S_s - 1) + 1):
            r = k - j
            if r < 0 or r > 5 - j or r > N - S_s or j > S_s - 1:
                continue
            w += comb(S_s - 1, j) * (p_rest ** r) * ((1 - p_rest) ** (5 - j - r)) * comb(N - S_s, r)
        w /= comb(N - 1, 5)
        tot += w
    return p_forced * tot

try:
    for K in range(0, len(sites) + 1):
        p = pass_prob(K, len(sites), len(summ))
        if 0.05 < p < 0.999:
            print("TEETH-PROB K=%d/%d P(b2 pass)=%.3f" % (K, len(sites), p))
except Exception as e:
    print("TEETH-PROB error", e)

# 3. clause-g probes: (label, source, expectation per docstring vs code)
probes = [
    ("local-var-named-compile", "import json\nx = 1\ncompile = x\n", "docstring: not a call -> allowed; code: ?"),
    ("bare-name-eval-no-call", "import json\neval\n", "docstring: calls none -> allowed; code: ?"),
    ("var-named-vars", "import json\nvars = {}\n", "docstring: calls none -> allowed; code: ?"),
    ("no-imports-at-all", "x = 1\n", "docstring: silent; code: ?"),
    ("import-hashlib", "import hashlib, json\n", "docstring: five listed -> reject; code: ?"),
    ("nested-import-json", "def f():\n    import json\n    return json\n", "docstring: top-level only -> allowed; code: ?"),
    ("argv0-indirect", "import sys\na = sys.argv\np = a[0]\n", "docstring: never names sys.argv[0] -> reject; code: ?"),
    ("argv0-direct", "import sys\np = sys.argv[0]\n", "docstring: reject; code: ?"),
    ("shell-false", "import json\njson.dumps(1, shell=False)\n", "docstring: no shell=True -> allowed; code: ?"),
    ("kw-unpack", "import json\nd = {}\njson.dumps(**d)\n", "docstring: no ** unpacking -> reject; code: ?"),
    ("proc-string", 'import json\nx = "/proc/self"\n', "docstring: names no /proc -> reject; code: ?"),
    ("os-spawn", "import os\nos.spawnl(0, 'x')\n", "docstring: os.exec* listed, spawn* not; code: ?"),
    ("builtins-attr", "import builtins\nbuiltins.eval\n", "docstring: on builtins -> reject; code: ?"),
]
for label, src, exp in probes:
    try:
        r = ctr.imports_ok(src)
    except Exception as e:
        r = "RAISE:%s" % type(e).__name__
    print("G-PROBE %-24s -> %s   (%s)" % (label, r, exp))

# 4. dead-guard check
print("DEAD-GUARD allow∩deny=", ctr.STDLIB_ALLOW & ctr.STDLIB_DENY)

# 5. NUL-byte crash probe
try:
    ctr.imports_ok("x = 1\x00")
    print("NUL-PROBE no-raise")
except Exception as e:
    print("NUL-PROBE raises %s: %s" % (type(e).__name__, str(e)[:80]))

# 6. BOM crash probe (ast.parse on decoded text)
try:
    ast.parse("\ufeffimport json\n")
    print("BOM-PROBE ast.parse ok")
except Exception as e:
    print("BOM-PROBE ast.parse raises %s: %s" % (type(e).__name__, str(e)[:80]))

# 7. many0 seed nit: rng_for("many", ...) ignores rev
import inspect
src_line = inspect.getsource(ctr.score_many0).splitlines()[1]
print("MANY0-SEED", src_line.strip())
