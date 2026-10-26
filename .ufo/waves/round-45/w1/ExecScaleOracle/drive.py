#!/usr/bin/env python3
"""drive.py - differential driver: C++ transcription of Hyprland 0.56.2 applyMonitorRule
explicit-scale correction vs expected_scale() of the round-45 l1 draft tool.

Case protocol with the binary: "S W H" -> "SBITS RBITS STATE".
STATE 1 = corrected scale selected, 2 = m_scale untouched (positive branch),
0 = "failed to find a clean divisor" fallback (autoScale == false -> getDefaultScale()).

Level 1 (algorithm) : expected_scale(f32(cpp_parsed_s), w, h) vs C++ bits.   s identical on both sides.
Level 2 (end-to-end): expected_scale(f32(struct(text)), w, h) vs C++ bits.   models the tool's own parse.
"""
import importlib.util
import json
import math
import random
import struct
import subprocess
import sys

DRAFT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/l1-draft/mado-monitors.py"
BIN = sys.argv[1]
OUT = sys.argv[2]

spec = importlib.util.spec_from_file_location("mado", DRAFT)
mado = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mado)
expected_scale = mado.expected_scale


def f32_from_bits(b):
    return struct.unpack("<f", struct.pack("<I", b))[0]


def bits_of(x):
    return struct.unpack("<I", struct.pack("<f", x))[0]


def f32_of_text(t):
    return struct.unpack("<f", struct.pack("<f", float(t)))[0]


SIZES = [
    (640, 480), (800, 600), (1024, 768), (1024, 600), (1280, 720), (1280, 800), (1280, 1024), (1280, 480),
    (1366, 768), (1365, 767), (1440, 900), (1440, 2560), (1600, 900), (1600, 1200), (1680, 1050),
    (1920, 1080), (1919, 1079), (1920, 1200), (1920, 1440), (2048, 1152), (2160, 1440), (2560, 1080),
    (2560, 1440), (2560, 1600), (2560, 1920), (2880, 1800), (3200, 1800), (3440, 1440), (3441, 1439),
    (3840, 1080), (3840, 1600), (3840, 2160), (3840, 2400), (4096, 2160), (4096, 2304), (5120, 1440),
    (5120, 2160), (5120, 2880), (6016, 3384), (7680, 4320), (1080, 1920), (768, 1366), (1000, 1000),
    (1234, 567), (999, 777),
]

rng = random.Random(20261026)

scales = []          # (text, family)


def add(text, fam):
    scales.append((text, fam))


# A: 0.25 .. 3.00 in 0.01
for i in range(276):
    add("%.2f" % (0.25 + 0.01 * i), "A-0.01")
# B: k/120 as a 6-decimal literal a user could type
for k in range(30, 361):
    add("%.6f" % (k / 120.0), "B-k/120-6dp")
# D: f32 nearest of k/120, shortest decimal that round-trips
for k in range(30, 361):
    v = f32_of_text("%.9f" % (k / 120.0))
    for d in range(1, 10):
        t = "%.*f" % (d, k / 120.0)
        if f32_of_text(t) == v:
            break
    add(t, "D-1/120-exact")
# E: exact .5 ties in the *120 rounding
for m in range(30, 360):
    add("%.6f" % ((m + 0.5) / 120.0), "E-tie")
# F: either side of the tie
for m in range(30, 360, 3):
    add("%.7f" % ((m + 0.4999999) / 120.0), "F-tie-eps-down")
    add("%.7f" % ((m + 0.5000001) / 120.0), "F-tie-eps-up")
# C: random <= 6 decimals, full range
for _ in range(3000):
    add("%.6f" % rng.uniform(0.25, 3.0), "C-random")
# G: low scales (k <= 89) where the down-candidate reaches 0 and goes negative
for _ in range(2000):
    add("%.6f" % rng.uniform(0.25, 0.75), "G-low")

cases = []
for text, fam in scales:
    for w, h in SIZES:
        cases.append((text, w, h, fam))

inp = "".join("%s %d %d\n" % (t, w, h) for t, w, h, _ in cases)
proc = subprocess.run([BIN], input=inp, capture_output=True, text=True, check=True)
lines = proc.stdout.split("\n")
assert len(lines) - 1 == len(cases), (len(lines), len(cases))

div1, div2, parse_diff = [], [], []
stats = {"cases": len(cases), "state1": 0, "state2": 0, "fallback": 0,
         "py_none": 0, "cpp_nonpositive": 0, "py_nonpositive": 0, "nonpositive_both": 0}
max_drift = 0.0
for (text, w, h, fam), ln in zip(cases, lines):
    sb, rb, st = ln.split()
    sb, rb, st = int(sb, 16), int(rb, 16), int(st)
    s_cpp = f32_from_bits(sb)
    s_py = f32_of_text(text)
    if bits_of(s_py) != sb:
        parse_diff.append({"text": text, "cpp_bits": "%08x" % sb, "py_bits": "%08x" % bits_of(s_py)})
    cpp_val = f32_from_bits(rb)
    e1 = expected_scale(s_cpp, w, h)     # level 1: identical s
    e2 = expected_scale(s_py, w, h)      # level 2: tool's own parse
    stats["state1" if st == 1 else "state2" if st == 2 else "fallback"] += 1
    if e1 is None:
        stats["py_none"] += 1
    if st != 0 and cpp_val <= 0:
        stats["cpp_nonpositive"] += 1
    if e1 is not None and e1 <= 0:
        stats["py_nonpositive"] += 1
    if st != 0 and cpp_val <= 0 and e1 is not None and e1 <= 0:
        stats["nonpositive_both"] += 1
    if st == 0:
        if e1 is not None:
            div1.append({"text": text, "s": s_cpp, "w": w, "h": h, "fam": fam, "kind": "cpp-fallback-vs-py",
                         "cpp": "getDefaultScale()", "py": e1})
    else:
        if e1 is None:
            div1.append({"text": text, "s": s_cpp, "w": w, "h": h, "fam": fam, "kind": "cpp-value-vs-py-none",
                         "cpp": cpp_val, "py": None})
        elif bits_of(cpp_val) != bits_of(e1):
            d = abs(cpp_val - e1)
            max_drift = max(max_drift, d)
            div1.append({"text": text, "s": s_cpp, "w": w, "h": h, "fam": fam, "kind": "value-mismatch",
                         "cpp": cpp_val, "py": e1, "delta": d})
    if e2 is None:
        if st != 0:
            div2.append({"text": text, "w": w, "h": h, "fam": fam, "kind": "cpp-value-vs-py-none"})
    elif st != 0 and bits_of(cpp_val) != bits_of(e2):
        div2.append({"text": text, "w": w, "h": h, "fam": fam, "kind": "value-mismatch",
                     "cpp_bits": "%08x" % rb, "py_bits": "%08x" % bits_of(e2), "s_py_bits": "%08x" % bits_of(s_py)})

# --- tolerance analysis ---------------------------------------------------
# Spacing between adjacent admissible scales is 1/120; the live `scale` field is a float
# printed by std::format("{}") (shortest round-trip decimal for float), so the tool's
# parsed double can drift from the true float value.
def shortest_repr(v):
    for d in range(1, 10):
        t = "%.*g" % (d, v)
        if f32_of_text(t) == v:
            return t
    return "%.9g" % v


worst_repr = (0.0, None)
for k in range(30, 361):
    v = f32_of_text("%.9f" % (k / 120.0))
    t = shortest_repr(v)
    d = abs(float(t) - v)
    if d > worst_repr[0]:
        worst_repr = (d, (t, "%.9g" % v))
for i in range(276):
    v = f32_of_text("%.2f" % (0.25 + 0.01 * i))
    t = shortest_repr(v)
    d = abs(float(t) - v)
    if d > worst_repr[0]:
        worst_repr = (d, (t, "%.9g" % v))

res = {
    "stats": stats,
    "divergences_level1": div1,
    "divergences_level2": div2,
    "parse_diff_count": len(parse_diff),
    "parse_diff_examples": parse_diff[:5],
    "max_value_drift": max_drift,
    "candidate_spacing": 1.0 / 120.0,
    "tolerance": 1e-4,
    "worst_float_repr_drift": {"abs": worst_repr[0], "example": worst_repr[1]},
    "families": sorted({f for _, f in scales}),
    "distinct_scales": len(scales),
}
with open(OUT, "w") as fh:
    json.dump(res, fh, indent=1)
print(json.dumps({k: v for k, v in res.items() if not k.startswith("divergences")}, indent=1))
print("divergences_level1 =", len(div1))
print("divergences_level2 =", len(div2))
for d in div1[:10]:
    print("DIV1", d)
